import os
from typing import Dict

import pandas as pd

from config.report import report_settings
from config.settings import settings


def generate_markdown_summary(
        bypass_df: pd.DataFrame,
        browser_data_df: pd.DataFrame,
        output_dir: str,
        image_paths: Dict[str, str]
) -> None:
    """Generate markdown summary of benchmark results"""

    with open(os.path.join(output_dir, report_settings.filenames.summary), "w", encoding="utf-8") as f:
        _write_report_header(f)
        _write_bypass_section(f, bypass_df)
        _write_resource_section(f, bypass_df)
        _write_recaptcha_section(f, browser_data_df)
        _write_creepjs_section(f, browser_data_df)
        _write_ip_section(f, browser_data_df)
        _write_visualization_sections(f, image_paths)


def _write_report_header(f) -> None:
    """Write the report header"""

    f.write("# Browser Benchmark Results Summary\n\n")
    f.write(f"*Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}*\n\n")


def _write_bypass_section(f, bypass_df: pd.DataFrame) -> None:
    """Write the bypass rate section"""

    f.write("## Overall Bypass Rate\n\n")

    if bypass_df.empty:
        f.write("*No bypass data available*\n\n")
        return

    bypass_by_engine = bypass_df.groupby("engine")["bypass"].mean().reset_index()
    bypass_by_engine["bypass_percent"] = bypass_by_engine["bypass"] * 100
    bypass_by_engine = bypass_by_engine.sort_values("bypass_percent", ascending=False)

    f.write("| Engine | Bypass Rate (%) |\n")
    f.write("|-----------------|----------------:|\n")
    for _, row in bypass_by_engine.iterrows():
        f.write(f"| {row['engine']} | {row['bypass_percent']:.1f} |\n")


def _write_resource_section(f, bypass_df: pd.DataFrame) -> None:
    """Write the resource usage section"""

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
    """Write the reCAPTCHA section"""

    f.write("## Recaptcha Scores\n\n")

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


def _write_creepjs_section(f, browser_data_df: pd.DataFrame) -> None:
    """Write the CreepJS section"""

    f.write("## CreepJS Scores\n\n")

    if "creepjs_trust_score" not in browser_data_df.columns:
        f.write("*No CreepJS data available*\n\n")
        return

    # calculate the metrics
    creepjs_numeric_data = browser_data_df.groupby("engine")[
        ["creepjs_trust_score", "creepjs_bot_score"]].mean().reset_index()

    if creepjs_numeric_data.empty:
        f.write("*No CreepJS data available*\n\n")
        return

    try:
        creepjs_webrtc_ip_data = browser_data_df.groupby("engine")["creepjs_webrtc_ip"].agg(
            lambda x: x.mode().iloc[0] if not x.isna().all() and len(x) > 0 else "Not detected"
        ).reset_index()
    except Exception:
        creepjs_webrtc_ip_data = browser_data_df.groupby("engine")["creepjs_webrtc_ip"].first().reset_index()
        creepjs_webrtc_ip_data["creepjs_webrtc_ip"] = creepjs_webrtc_ip_data["creepjs_webrtc_ip"].fillna("Not detected")

    # merge data and sort
    creepjs_data = pd.merge(creepjs_numeric_data, creepjs_webrtc_ip_data, on="engine")
    creepjs_data = creepjs_data.sort_values("creepjs_trust_score", ascending=False)

    f.write("| Engine | Trust Score (%) | Bot Score (%) | WebRTC IP |\n")
    f.write("|-----------------|----------------:|--------------:|----------:|\n")
    for _, row in creepjs_data.iterrows():
        f.write(f"| {row['engine']} "
                f"| {row['creepjs_trust_score']:.2f} "
                f"| {row['creepjs_bot_score']:.2f} "
                f"| {row['creepjs_webrtc_ip']} |\n")

    f.write('\n\n')


def _write_ip_section(f, browser_data_df: pd.DataFrame) -> None:
    """Write the IP section"""

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
    """Write the visualization sections"""

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

    # creepJS visualization
    f.write("## CreepJS Visualization\n\n")
    if "creepjs_image" in image_paths and image_paths["creepjs_image"]:
        f.write(
            f"![CreepJS Scores]({os.path.join(settings.paths.media_dir, os.path.basename(image_paths['creepjs_image']))})\n\n")
    else:
        f.write("*No CreepJS image available*\n\n")
