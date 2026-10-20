"""Synthetic page fixtures only; no browser engines or target access."""
import contextlib
import io
import unittest

from run_platform_survey import PLATFORMS, test_platform as survey_platform
from run_tiktok_captcha_solve import check_page_status


class PageFixture:
    def __init__(self, title="Fixture product", captcha_count=0, product_count=0,
                 navigation_error=False, title_error=False, evaluation_error=False):
        self.page_title = title
        self.captcha_count = captcha_count
        self.product_count = product_count
        self.navigation_error = navigation_error
        self.title_error = title_error
        self.evaluation_error = evaluation_error

    async def goto(self, *args, **kwargs):
        if self.navigation_error:
            raise TimeoutError("fixture navigation timeout")

    async def wait_for_timeout(self, milliseconds):
        pass

    async def title(self):
        if self.title_error:
            raise RuntimeError("fixture title unavailable")
        return self.page_title

    async def evaluate(self, script):
        if self.evaluation_error:
            raise RuntimeError("fixture page detached")
        if 'captcha' in script:
            return self.captcha_count
        if 'product-price' in script:
            return self.product_count
        raise AssertionError(f"Unexpected fixture query: {script}")


class SurveyFailureTests(unittest.IsolatedAsyncioTestCase):
    async def test_navigation_failure_returns_result(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = await survey_platform(PageFixture(navigation_error=True), PLATFORMS[0], True)
        self.assertEqual(result["error"], "fixture navigation timeout")
        self.assertFalse(result["success"])
        self.assertIsNone(result["title"])

    async def test_title_failure_returns_result(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = await survey_platform(PageFixture(title_error=True), PLATFORMS[0], False)
        self.assertEqual(result["error"], "fixture title unavailable")
        self.assertFalse(result["success"])


class CaptchaStatusTests(unittest.IsolatedAsyncioTestCase):
    async def test_long_non_product_title_is_not_bypass(self):
        result = await check_page_status(PageFixture(title="Service temporarily unavailable"))
        self.assertFalse(result["bypass"])

    async def test_product_elements_confirm_bypass(self):
        result = await check_page_status(PageFixture(product_count=1))
        self.assertTrue(result["bypass"])
        self.assertEqual(result["product_count"], 1)

    async def test_short_product_title_can_pass(self):
        result = await check_page_status(PageFixture(title="Tea", product_count=1))
        self.assertTrue(result["bypass"])

    async def test_captcha_overrides_product_elements(self):
        result = await check_page_status(PageFixture(captcha_count=1, product_count=1))
        self.assertTrue(result["blocked"])
        self.assertFalse(result["bypass"])

    async def test_access_denied_overrides_product_elements(self):
        result = await check_page_status(PageFixture(title="Access Denied", product_count=1))
        self.assertTrue(result["blocked"])
        self.assertFalse(result["bypass"])

    async def test_evaluation_error_fails_closed(self):
        result = await check_page_status(PageFixture(evaluation_error=True))
        self.assertTrue(result["blocked"])
        self.assertFalse(result["bypass"])
        self.assertEqual(result["error"], "fixture page detached")
