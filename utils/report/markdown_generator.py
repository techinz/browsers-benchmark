import os
from typing import Dict

import pandas as pd

from config.report import report_settings
from config.settings import settings
from .data_processor import summarize_detection

VERDICT_ICONS = {"human": "✅", "suspicious": "⚠️", "bot": "❌"}


def generate_markdown_summary(
        bypass_df: pd.DataFrame,
        browser_data_df: pd.DataFrame,
        detection_df: pd.DataFrame,
        output_dir: str,
        image_paths: Dict[str, str]
) -> None:
    """
    Generate markdown summary of benchmark results

    :param bypass_df: DataFrame containing bypass results
    :param browser_data_df: DataFrame containing browser data results
    :param detection_df: DataFrame containing bot detection test verdicts
    :param output_dir: Directory to save the generated markdown file
    :param image_paths: Dictionary mapping visualization names to their file paths
    """

    with open(os.path.join(output_dir, report_settings.filenames.summary), "w", encoding="utf-8") as f:
        _write_report_header(f)
        _write_bypass_section(f, bypass_df, detection_df)
        _write_detection_section(f, detection_df)
        _write_resource_section(f, bypass_df)
        _write_recaptcha_section(f, browser_data_df)
        _write_webrtc_section(f, browser_data_df)
        _write_ip_section(f, browser_data_df)
        _write_visualization_sections(f, image_paths)


def _write_report_header(f) -> None:
    """
    Write the report header

    :param f: File object to write the header to
    """

    f.write("# Browser Benchmark Results Summary\n\n")
    f.write(f"*Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n\n")


def _write_bypass_section(f, bypass_df: pd.DataFrame, detection_df: pd.DataFrame) -> None:
    """
    Write the overall ranking: bypass rate combined with the bot detection risk

    :param f: File object to write the section to
    :param bypass_df: DataFrame containing bypass results
    :param detection_df: DataFrame containing bot detection test verdicts
    """

    f.write("## Overall Ranking\n\n")

    if bypass_df.empty:
        f.write("*No bypass data available*\n\n")
        return

    bypass_by_engine = bypass_df.groupby("engine")["bypass"].mean().reset_index()
    bypass_by_engine.loc[:, "bypass_percent"] = bypass_by_engine["bypass"] * 100
    detection = summarize_detection(detection_df)

    if detection.empty:
        bypass_by_engine = bypass_by_engine.sort_values(["bypass_percent", "engine"], ascending=[False, True])
        f.write("| Engine | Bypass Rate (%) |\n")
        f.write("|-----------------|----------------:|\n")
        for _, row in bypass_by_engine.iterrows():
            f.write(f"| {row['engine']} | {row['bypass_percent']:.1f} |\n")
        return

    bypass_by_engine.loc[:, "risk"] = bypass_by_engine["engine"].map(detection["risk"])
    bypass_by_engine.loc[:, "score"] = (bypass_by_engine["bypass_percent"] + 100 - bypass_by_engine["risk"]) / 2
    bypass_by_engine = bypass_by_engine.sort_values(["score", "bypass_percent", "engine"], ascending=[False, False, True],
                                                    na_position="last")

    f.write("Overall score is the average of the bypass rate and 100 minus the detection risk "
            "(see Bot Detection Tests), both weighted equally.\n\n")
    f.write("| Engine | Overall score | Bypass Rate (%) | Detected by | Detection risk |\n")
    f.write("|-----------------|--------------:|----------------:|------------:|---------------:|\n")
    for _, row in bypass_by_engine.iterrows():
        if row["engine"] in detection.index:
            counts = detection.loc[row["engine"]]
            score = f"{row['score']:.1f}"
            detected_by, risk = f"{counts['detected']:.0f}/{counts['total']:.0f}", f"{counts['risk']:.0f}"
        else:
            score, detected_by, risk = "-", "-", "-"
        f.write(f"| {row['engine']} | {score} | {row['bypass_percent']:.1f} | {detected_by} | {risk} |\n")


def _write_detection_section(f, detection_df: pd.DataFrame) -> None:
    """
    Write the bot detection tests section: how each test site classified each engine

    :param f: File object to write the section to
    :param detection_df: DataFrame containing bot detection test verdicts
    """

    f.write("\n\n## Bot Detection Tests\n\n")

    if detection_df.empty:
        f.write("*No bot detection data available*\n\n")
        return

    f.write("✅ looks human · ⚠️ suspicious · ❌ detected as bot · ❔ test didn't finish (not counted)\n\n")
    f.write("Risk (0 - human, 100 - bot) is the average over the tests: the site's own score where it has one "
            "(CleanTalk: 100 - Human Score, APIVoid: risk score, CreepJS: headless/stealth %, "
            "Fingerprint-Scan: bot score), otherwise its verdict (✅ 0, ⚠️ 50, ❌ 100). "
            "Engines are sorted by it.\n\n")

    targets = list(dict.fromkeys(detection_df["target"]))
    cells = detection_df.set_index(["engine", "target"])

    f.write("| Engine | " + " | ".join(targets) + " | Detected by | Risk |\n")
    f.write("|-----------------|" + "|".join(":---:" for _ in targets) + "|------------:|-----:|\n")
    for engine, counts in summarize_detection(detection_df).iterrows():
        row = []
        for target in targets:
            if (engine, target) not in cells.index:
                row.append("-")
                continue
            cell = cells.loc[(engine, target)]
            row.append(f"{VERDICT_ICONS[cell['verdict']]} {cell['summary']}" if cell["verdict"] else "❔ error")
        f.write(f"| {engine} | " + " | ".join(row) + f" | {counts['detected']:.0f}/{counts['total']:.0f} | {counts['risk']:.0f} |\n")


def _write_resource_section(f, bypass_df: pd.DataFrame) -> None:
    """
    Write the resource usage section

    :param f: File object to write the section to
    :param bypass_df: DataFrame containing bypass results with resource usage
    """

    f.write("\n\n## Resource Usage Comparison\n\n")

    if bypass_df.empty:
        f.write("*No resource usage data available*\n\n")
        return

    resources_by_engine = bypass_df.groupby("engine")[["avg_memory_mb", "avg_cpu_percent"]].mean().reset_index()
    resources_by_engine = resources_by_engine.sort_values("avg_memory_mb")

    f.write("| Engine | Memory Usage (MB) | CPU Usage (%) |\n")
    f.write("|-----------------|------------------:|--------------:|\n")
    for _, row in resources_by_engine.iterrows():
        f.write(f"| {row['engine']} | {row['avg_memory_mb']:.1f} | {row['avg_cpu_percent']:.1f} |\n")

    f.write('\n\n')


def _write_recaptcha_section(f, browser_data_df: pd.DataFrame) -> None:
    """
    Write the reCAPTCHA section

    :param f: File object to write the section to
    :param browser_data_df: DataFrame containing browser data results with reCAPTCHA scores
    """

    f.write("## Recaptcha Scores\n\n")

    if browser_data_df.empty or "recaptcha_score" not in browser_data_df.columns:
        f.write("*No reCAPTCHA data available*\n\n")
        return

    recaptcha_data = browser_data_df.groupby("engine")["recaptcha_score"].mean().reset_index()

    if recaptcha_data.empty:
        f.write("*No reCAPTCHA data available*\n\n")
        return

    recaptcha_data = recaptcha_data.sort_values("recaptcha_score", ascending=False)

    f.write("| Engine | Recaptcha Score (0-1) |\n")
    f.write("|-----------------|--------------------:|\n")
    for _, row in recaptcha_data.iterrows():
        f.write(f"| {row['engine']} | {row['recaptcha_score']:.2f} |\n")

    f.write('\n\n')


def _write_webrtc_section(f, browser_data_df: pd.DataFrame) -> None:
    """
    Write the WebRTC IP section (IP seen by CreepJS through WebRTC, a leak if it's the real IP)

    :param f: File object to write the section to
    :param browser_data_df: DataFrame containing browser data results with WebRTC IPs
    """

    f.write("## WebRTC IP (CreepJS)\n\n")

    if "creepjs_webrtc_ip" not in browser_data_df.columns:
        f.write("*No WebRTC data available*\n\n")
        return

    webrtc_data = browser_data_df.groupby("engine")["creepjs_webrtc_ip"].agg(
        lambda x: x[x.notna() & (x != "")].iloc[0] if (x.notna() & (x != "")).any() else "Not detected"
    ).reset_index()

    f.write("| Engine | WebRTC IP |\n")
    f.write("|-----------------|----------:|\n")
    for _, row in webrtc_data.iterrows():
        f.write(f"| {row['engine']} | {row['creepjs_webrtc_ip']} |\n")

    f.write('\n\n')


def _write_ip_section(f, browser_data_df: pd.DataFrame) -> None:
    """
    Write the IP section

    :param f: File object to write the section to
    :param browser_data_df: DataFrame containing browser data results with IP information
    """

    f.write("## IP (Ipify) \n\n")

    if "ip" not in browser_data_df.columns:
        f.write("*No IP data available*\n\n")
        return

    try:
        ip_data = browser_data_df.groupby("engine")["ip"].agg(
            lambda x: x.mode().iloc[0] if not x.isna().all() and len(x) > 0 else "Not detected"
        ).reset_index()
    except Exception:
        ip_data = browser_data_df.groupby("engine")["ip"].first().reset_index()
        ip_data["ip"] = ip_data["ip"].fillna("Not detected")

    f.write("| Engine | IP |\n")
    f.write("|-----------------|----------:|\n")
    for _, row in ip_data.iterrows():
        f.write(f"| {row['engine']} | {row['ip']} |\n")

    f.write('\n\n')


def _write_visualization_sections(f, image_paths: Dict[str, str]) -> None:
    """
    Write the visualization sections

    :param f: File object to write the sections to
    :param image_paths: Dictionary mapping visualization names to their file paths
    """

    # visual dashboard
    f.write("## Visual Dashboard\n\n")
    if "bypass_dashboard_image" in image_paths and image_paths["bypass_dashboard_image"]:
        f.write(
            f"![Bypass Dashboard]({os.path.join(settings.paths.media_dir, os.path.basename(image_paths['bypass_dashboard_image']))})\n\n")
    else:
        f.write("*No dashboard image available*\n\n")

    # recaptcha visualization
    f.write("## Recaptcha Score Visualization\n\n")
    if "recaptcha_score_image" in image_paths and image_paths["recaptcha_score_image"]:
        f.write(
            f"![Recaptcha Scores]({os.path.join(settings.paths.media_dir, os.path.basename(image_paths['recaptcha_score_image']))})\n\n")
    else:
        f.write("*No reCAPTCHA image available*\n\n")

    # bot detection visualization
    f.write("## Bot Detection Visualization\n\n")
    if "detection_image" in image_paths and image_paths["detection_image"]:
        f.write(
            f"![Bot Detection Tests]({os.path.join(settings.paths.media_dir, os.path.basename(image_paths['detection_image']))})\n\n")
    else:
        f.write("*No bot detection image available*\n\n")
