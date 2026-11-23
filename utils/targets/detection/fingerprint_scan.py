import re

from engines.base import BrowserEngine
from utils.targets.detection.page import BOT, HUMAN, SUSPICIOUS, detection, wait_for

RESULT_SCRIPT = """
const badges = [...document.querySelectorAll('[data-slot="badge"]')].map(b => b.textContent.replace(/\\s+/g, ' ').trim());
const score = badges.find(b => /^Bot score \\d+/.test(b));
const categories = badges.filter(b => /:\\s*(LOW|MEDIUM|HIGH)/.test(b));
return JSON.stringify(score && categories.length ? {score: score, categories: categories} : null);
"""


async def check_fingerprint_scan(engine: BrowserEngine) -> dict:
    """
    Fingerprint-Scan - bot score 0-100 split into categories rated LOW, MEDIUM or HIGH

    :param engine: BrowserEngine instance
    """

    result = await wait_for(engine, RESULT_SCRIPT, timeout_s=120)
    if not result:
        raise Exception("Fingerprint-Scan result not found")

    score = int(re.search(r"Bot score (\d+)", result["score"]).group(1))
    categories = {}
    for badge in result["categories"]:
        name, level, points = re.match(r"(.+?):\s*(LOW|MEDIUM|HIGH)\s*(\+\d+)?", badge).groups()
        categories[name.strip()] = f"{level} {points}" if points else level

    levels = " ".join(categories.values())
    verdict = BOT if "HIGH" in levels else SUSPICIOUS if "MEDIUM" in levels else HUMAN

    return detection(verdict, f"bot score {score}", risk=score, score=score, categories=categories)
