import os
from typing import Dict, List, Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from config.report import report_settings


def generate_bypass_dashboard_image(df: pd.DataFrame, output_dir: str) -> str:
    """Generate a dashboard of bypass benchmark results"""

    plt.figure(figsize=report_settings.visualization.figure_size_large)
    plt.suptitle("Browser Engine Benchmark Results", fontsize=24, y=0.99)

    if df.empty:
        plt.text(0.5, 0.5, "No bypass data available",
                 ha='center', va='center', fontsize=16)
        image_path = os.path.join(output_dir, report_settings.filenames.bypass_dashboard)
        plt.savefig(image_path, dpi=report_settings.visualization.dpi)
        plt.close('all')
        return image_path

    # calculate engines sorted by bypass rate for ordering
    engines = df.groupby("engine")["bypass"].mean().sort_values(ascending=False).index.tolist()
    colors = plt.cm.get_cmap('viridis')(np.linspace(0, 1, len(engines)))
    engine_colors = {engine: color for engine, color in zip(engines, colors)}

    # create subplots
    _create_bypass_rate_subplot(df, engine_colors)
    _create_protection_heatmap_subplot(df, engines)
    _create_resource_usage_subplot(df)
    _create_load_time_subplot(df)

    # layout adjustments
    plt.tight_layout(rect=(0, 0, 1.0, 0.96))

    # add note
    _add_dashboard_note()

    image_path = os.path.join(output_dir, report_settings.filenames.bypass_dashboard)
    plt.savefig(image_path, dpi=report_settings.visualization.dpi, bbox_inches="tight")
    plt.close('all')

    return image_path


def generate_recaptcha_score_image(df: pd.DataFrame, output_dir: str) -> str:
    """Generate image for Recaptcha scores"""

    plt.figure(figsize=report_settings.visualization.figure_size_medium)
    plt.title("Recaptcha Scores by Browser", fontsize=16)

    recaptcha_df = df.dropna(subset=["recaptcha_score"])

    if recaptcha_df.empty:
        plt.text(0.5, 0.5, "No reCAPTCHA data available",
                 ha='center', va='center', fontsize=16)
        image_path = os.path.join(output_dir, report_settings.filenames.recaptcha_scores)
        plt.savefig(image_path, dpi=report_settings.visualization.dpi)
        plt.close('all')
        return image_path

    _create_recaptcha_plot(recaptcha_df)
    _add_recaptcha_note()

    image_path = os.path.join(output_dir, report_settings.filenames.recaptcha_scores)
    plt.tight_layout(rect=(0, 0.1, 1.0, 1.0))
    plt.savefig(image_path, dpi=report_settings.visualization.dpi, bbox_inches="tight")
    plt.close('all')

    return image_path


def generate_creepjs_image(df: pd.DataFrame, output_dir: str) -> str:
    """Generate image for CreepJS scores"""

    plt.figure(figsize=report_settings.visualization.figure_size_medium)
    plt.title("CreepJS by Browser", fontsize=16)

    creepjs_df = df.dropna(subset=["creepjs_trust_score"])

    if creepjs_df.empty:
        plt.text(0.5, 0.5, "No CreepJS data available",
                 ha='center', va='center', fontsize=16)
        image_path = os.path.join(output_dir, report_settings.filenames.creepjs_scores)
        plt.savefig(image_path, dpi=report_settings.visualization.dpi)
        plt.close('all')
        return image_path

    _create_creepjs_plot(creepjs_df)
    _add_creepjs_note()

    image_path = os.path.join(output_dir, report_settings.filenames.creepjs_scores)
    plt.tight_layout(rect=(0, 0.04, 1.0, 1.0))
    plt.savefig(image_path, dpi=report_settings.visualization.dpi, bbox_inches="tight")
    plt.close('all')

    return image_path


def _create_bypass_rate_subplot(df: pd.DataFrame, engine_colors: Dict[str, Any]) -> None:
    """Create the bypass rate subplot (top left)"""

    plt.subplot(2, 2, 1)
    bypass_by_engine = df.groupby("engine")["bypass"].mean().reset_index()
    bypass_by_engine["bypass_percent"] = bypass_by_engine["bypass"] * 100
    bypass_by_engine = bypass_by_engine.sort_values("bypass_percent", ascending=False)

    bars = plt.bar(bypass_by_engine["engine"], bypass_by_engine["bypass_percent"],
                   color=[engine_colors[e] for e in bypass_by_engine["engine"]])

    # value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + 1,
                 f'{height:.1f}%', ha='center', va='bottom', fontsize=9)

    plt.title("Bypass Rate by Browser", fontsize=16)
    plt.ylabel("Bypass Rate (%)", fontsize=12)
    plt.ylim(0, max(1, max(bypass_by_engine["bypass_percent"])) * 1.15)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.grid(axis="y", **report_settings.colors.grid_style)


def _create_protection_heatmap_subplot(df: pd.DataFrame, engines: List[str]) -> None:
    """Create the protection type heatmap subplot (top right)"""

    plt.subplot(2, 2, 2)

    if "protection_type" not in df.columns:
        df = df.copy()
        df["protection_type"] = df["target"]

    # ensure bypass column is a number
    df["bypass"] = pd.to_numeric(df["bypass"], errors="coerce").fillna(0)

    heatmap_data = pd.pivot_table(
        df, values="bypass",
        index="engine", columns="protection_type",
        aggfunc="mean",
        fill_value=0
    )

    if not heatmap_data.empty:
        heatmap_data = heatmap_data.reindex(engines)
        heatmap_data = heatmap_data.astype(float)

    sns.heatmap(heatmap_data, annot=True, cmap="RdYlGn", vmin=0, vmax=1,
                fmt=".2f", linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title("Bypass Rate by Protection Type", fontsize=16)
    plt.tight_layout()


def _create_resource_usage_subplot(df: pd.DataFrame) -> None:
    """Create the resource usage subplot (bottom left)"""

    plt.subplot(2, 2, 3)

    # prepare data
    resource_data = df.groupby("engine")[["avg_memory_mb", "avg_cpu_percent"]].mean().reset_index()
    resource_data = resource_data.sort_values("avg_memory_mb")

    # grouped bars for memory and CPU
    x = np.arange(len(resource_data))
    width = 0.35

    # normalize values to make them comparable on same scale
    max_memory = max(0.1, resource_data["avg_memory_mb"].max())
    max_cpu = max(0.1, resource_data["avg_cpu_percent"].max())
    resource_data["memory_normalized"] = resource_data["avg_memory_mb"] / max_memory * 100
    resource_data["cpu_normalized"] = resource_data["avg_cpu_percent"] / max_cpu * 100

    bar1 = plt.bar(x - width / 2, resource_data["memory_normalized"], width,
                   label="Memory", alpha=0.7, color="steelblue")
    bar2 = plt.bar(x + width / 2, resource_data["cpu_normalized"], width,
                   label="CPU", alpha=0.7, color="firebrick")

    # annotations
    for i, bars in enumerate(zip(bar1, bar2)):
        for j, bar in enumerate(bars):
            value = resource_data.iloc[i]["avg_memory_mb"] if j == 0 else resource_data.iloc[i]["avg_cpu_percent"]
            unit = "MB" if j == 0 else "%"
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                     f'{value:.1f}{unit}', ha='center', va='bottom', fontsize=8)

    plt.title("Resource Usage (Normalized)", fontsize=16)
    plt.ylabel("Usage (% of maximum)", fontsize=12)
    plt.xticks(x, resource_data["engine"].tolist(), rotation=45, ha="right", fontsize=10)
    plt.legend(loc="upper right")
    plt.grid(axis="y", **report_settings.colors.grid_style)
    plt.ylim(0, 120)


def _create_load_time_subplot(df: pd.DataFrame) -> None:
    """Create the load time subplot (bottom right)"""

    plt.subplot(2, 2, 4)

    if "load_time_ms" not in df.columns and "load_time" in df.columns:
        df = df.copy()
        df["load_time_ms"] = df["load_time"] * 1000
    elif "load_time_ms" not in df.columns:
        df = df.copy()
        df["load_time_ms"] = 0

    # average page load time by engine
    load_time_by_engine = df.groupby("engine")["load_time_ms"].mean().reset_index()
    load_time_by_engine = load_time_by_engine.sort_values("load_time_ms")

    bar_plot = sns.barplot(x="engine", y="load_time_ms", hue="engine",
                           data=load_time_by_engine, palette="viridis", legend=False)

    plt.title("Average Page Load Time by Browser", fontsize=16)
    plt.xlabel("Browser", fontsize=12)
    plt.ylabel("Load Time (ms)", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)

    # value labels on bars
    for i, v in enumerate(load_time_by_engine["load_time_ms"]):
        bar_plot.text(i, v + 50, f"{v:.0f} ms", ha="center", fontsize=10)


def _create_recaptcha_plot(recaptcha_df: pd.DataFrame) -> None:
    """Create the reCAPTCHA scores plot"""
    recaptcha_data = recaptcha_df.groupby("engine")["recaptcha_score"].mean().reset_index()
    recaptcha_data = recaptcha_data.sort_values("recaptcha_score", ascending=False)

    sns.barplot(x="engine", y="recaptcha_score", hue="engine",
                data=recaptcha_data, palette="viridis", legend=False)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.ylabel("Recaptcha Score (0-1)", fontsize=12)
    plt.ylim(0, 1.05)

    # reference lines for good scores
    plt.axhline(y=report_settings.thresholds.highlight_good_score, color='green', linestyle='--',
                alpha=0.5, label="Good Score (0.8+)")
    plt.axhline(y=report_settings.thresholds.highlight_bad_score, color='red', linestyle='--',
                alpha=0.5, label="Bad Score (0.2-)")

    plt.legend(loc="upper right", fontsize=9)
    plt.grid(axis="y", **report_settings.colors.grid_style)

    # value annotations
    for i, v in enumerate(recaptcha_data["recaptcha_score"]):
        plt.text(i, v + 0.02, f'{v:.2f}', ha='center', va='bottom', fontsize=9)


def _create_creepjs_plot(creepjs_df: pd.DataFrame) -> None:
    """Create the CreepJS scores plot"""

    creepjs_data = creepjs_df.groupby("engine")[["creepjs_trust_score", "creepjs_bot_score"]].mean().reset_index()
    creepjs_data = creepjs_data.sort_values("creepjs_trust_score", ascending=False)

    x = np.arange(len(creepjs_data))
    width = 0.35

    bar1 = plt.bar(x - width / 2, creepjs_data["creepjs_trust_score"], width,
                   label="Trust Score (higher is better)", color=report_settings.colors.success)
    bar2 = plt.bar(x + width / 2, creepjs_data["creepjs_bot_score"], width,
                   label="Bot Score (lower is better)", color=report_settings.colors.failure)

    plt.xticks(x, creepjs_data["engine"].tolist(), rotation=45, ha="right", fontsize=10)
    plt.ylabel("Score (0-100%)", fontsize=12)
    plt.ylim(0, 105)

    # reference lines for good scores
    plt.axhline(y=report_settings.thresholds.creepjs_good_trust_score, color='green', linestyle='--',
                alpha=0.5, label="Good Trust Score")
    plt.axhline(y=report_settings.thresholds.creepjs_good_bot_score, color='red', linestyle='--',
                alpha=0.5, label="Good Bot Score")

    plt.legend(loc="upper right", fontsize=9)
    plt.grid(axis="y", **report_settings.colors.grid_style)

    # Value annotations
    for i, bars in enumerate(zip(bar1, bar2)):
        for j, bar in enumerate(bars):
            value = creepjs_data.iloc[i]["creepjs_trust_score"] if j == 0 else creepjs_data.iloc[i]["creepjs_bot_score"]
            plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                     f'{value}%', ha='center', va='bottom', fontsize=9)


def _add_dashboard_note() -> None:
    """Add explanatory note to dashboard"""

    ax = plt.axes((0.40, 0.01, 0.2, 0.02), frameon=False)
    ax.text(0.5, 0.5, 'Lower values are better for resource usage and load time',
            ha='center', va='center', fontsize=10, style='italic')
    ax.set_xticks([])
    ax.set_yticks([])


def _add_recaptcha_note() -> None:
    """Explanatory note for reCAPTCHA plot"""

    plt.figtext(0.5, 0.01,
                "The Score shows if Google considers you as HUMAN or BOT: 1.0 - human, 0.0 - bot\n"
                "With score < 0.3 you'll get a slow reCAPTCHA 2, it would be hard to solve it.\n"
                "with score >= 0.7 it will be much easier.",
                ha='center', fontsize=10, style='italic')


def _add_creepjs_note() -> None:
    """Explanatory note for CreepJS plot"""

    plt.figtext(0.5, 0.01,
                "Higher trust score = better fingerprinting protection\nLower bot score = less bot-like behavior",
                ha='center', fontsize=10, style='italic')
