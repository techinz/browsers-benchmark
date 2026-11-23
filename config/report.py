"""
Configuration settings for report generation using pydantic.
"""

from typing import Any, Dict, Tuple

from pydantic import BaseModel
from pydantic_settings import BaseSettings


class VisualizationSettings(BaseModel):
    """Configuration settings for visualization"""

    figure_size_large: Tuple[int, int] = (20, 16)
    figure_size_medium: Tuple[int, int] = (12, 8)
    dpi: int = 300

    model_config = {"extra": "ignore"}


class ColorSettings(BaseModel):
    """Configuration settings for color schemes"""

    success: str = "forestgreen"
    failure: str = "firebrick"
    human: str = "#1a9850"
    suspicious: str = "#fdd75f"
    bot: str = "#d73027"
    error: str = "#bdbdbd"
    grid_linestyle: str = "--"
    grid_alpha: float = 0.3

    @property
    def score(self) -> Dict[str, str]:
        """Return score colors as dictionary"""

        return {
            "success": self.success,
            "failure": self.failure,
        }

    @property
    def verdict(self) -> Dict[str, str]:
        """Return bot detection verdict colors as dictionary"""

        return {
            "human": self.human,
            "suspicious": self.suspicious,
            "bot": self.bot,
            "error": self.error,
        }

    @property
    def grid_style(self) -> Dict[str, Any]:
        """Return grid styling as dictionary"""

        return {
            "linestyle": self.grid_linestyle,
            "alpha": self.grid_alpha
        }

    model_config = {"extra": "ignore"}


class ScoreThresholds(BaseModel):
    """Configuration settings for score thresholds"""

    highlight_good_score: float = 0.8
    highlight_bad_score: float = 0.2

    model_config = {"extra": "ignore"}


class FilenameSettings(BaseModel):
    """Configuration settings for output filenames"""

    bypass_dashboard: str = "bypass_dashboard.png"
    recaptcha_scores: str = "recaptcha_scores.png"
    detection_tests: str = "detection_tests.png"
    summary: str = "summary.md"

    model_config = {"extra": "ignore"}


class ReportSettings(BaseSettings):
    """Report configuration settings"""

    # visualization settings
    FIGURE_SIZE_LARGE_WIDTH: int = 20
    FIGURE_SIZE_LARGE_HEIGHT: int = 16
    FIGURE_SIZE_MEDIUM_WIDTH: int = 12
    FIGURE_SIZE_MEDIUM_HEIGHT: int = 8
    DPI: int = 300

    # color settings
    SUCCESS_COLOR: str = "forestgreen"
    FAILURE_COLOR: str = "firebrick"
    GRID_LINESTYLE: str = "--"
    GRID_ALPHA: float = 0.3

    # score thresholds
    HIGHLIGHT_GOOD_SCORE: float = 0.8
    HIGHLIGHT_BAD_SCORE: float = 0.2

    # output filenames
    BYPASS_DASHBOARD_FILENAME: str = "bypass_dashboard.png"
    RECAPTCHA_SCORES_FILENAME: str = "recaptcha_scores.png"
    DETECTION_TESTS_FILENAME: str = "detection_tests.png"
    SUMMARY_FILENAME: str = "summary.md"

    @property
    def visualization(self) -> VisualizationSettings:
        """Get visualization configuration"""

        return VisualizationSettings(
            figure_size_large=(self.FIGURE_SIZE_LARGE_WIDTH, self.FIGURE_SIZE_LARGE_HEIGHT),
            figure_size_medium=(self.FIGURE_SIZE_MEDIUM_WIDTH, self.FIGURE_SIZE_MEDIUM_HEIGHT),
            dpi=self.DPI
        )

    @property
    def colors(self) -> ColorSettings:
        """Get color configuration"""

        return ColorSettings(
            success=self.SUCCESS_COLOR,
            failure=self.FAILURE_COLOR,
            grid_linestyle=self.GRID_LINESTYLE,
            grid_alpha=self.GRID_ALPHA
        )

    @property
    def thresholds(self) -> ScoreThresholds:
        """Get score threshold configuration"""

        return ScoreThresholds(
            highlight_good_score=self.HIGHLIGHT_GOOD_SCORE,
            highlight_bad_score=self.HIGHLIGHT_BAD_SCORE
        )

    @property
    def filenames(self) -> FilenameSettings:
        """Get filename configuration"""

        return FilenameSettings(
            bypass_dashboard=self.BYPASS_DASHBOARD_FILENAME,
            recaptcha_scores=self.RECAPTCHA_SCORES_FILENAME,
            detection_tests=self.DETECTION_TESTS_FILENAME,
            summary=self.SUMMARY_FILENAME
        )

    model_config = {
        "case_sensitive": True,
        "extra": "ignore",
    }


report_settings = ReportSettings()
