import json
import logging
import os
from typing import Dict, Optional

from config.settings import settings
from .data_processor import process_bypass_data, process_browser_data
from .markdown_generator import generate_markdown_summary
from .visualizations import (
    generate_bypass_dashboard_image,
    generate_recaptcha_score_image,
    generate_creepjs_image
)

logger = logging.getLogger(__name__)


def generate_report(results_file: str, output_dir: Optional[str] = None) -> None:
    """Generate image & markdown reports from benchmark results"""

    if output_dir is None:
        output_dir = os.path.dirname(results_file)

    media_output_dir = os.path.join(output_dir, settings.paths.media_dir)

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(media_output_dir, exist_ok=True)

    try:
        results = _load_results(results_file)

        # process data into dataframes
        bypass_df = process_bypass_data(results)
        browser_data_df = process_browser_data(results)

        logger.info(f"Processed {len(bypass_df)} bypass results and {len(browser_data_df)} browser data points")

        # generate visualization images
        image_paths = _generate_all_visualizations(bypass_df, browser_data_df, media_output_dir)

        # generate markdown summary
        generate_markdown_summary(bypass_df, browser_data_df, output_dir, image_paths)

        logger.info(f"Report generated successfully in {output_dir}")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to load or process results file: {str(e)}")
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}", exc_info=True)


def _load_results(results_file: str) -> list:
    """Load and parse the results JSON file"""

    with open(results_file, "r", encoding="utf-8") as f:
        return json.load(f)


def _generate_all_visualizations(bypass_df, browser_data_df, media_output_dir: str) -> Dict[str, str]:
    """Generate all visualization images and return their paths"""

    return {
        "bypass_dashboard_image": generate_bypass_dashboard_image(bypass_df, media_output_dir),
        "recaptcha_score_image": generate_recaptcha_score_image(browser_data_df, media_output_dir),
        "creepjs_image": generate_creepjs_image(browser_data_df, media_output_dir),
    }
