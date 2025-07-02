import os
from pathlib import Path

import aiofiles

JS_BASE_DIR = Path(__file__).parent.parent / 'utils' / 'js_scripts'


async def load_js_script(file_name: str) -> str:
    """
    Load a JavaScript file content as string

    :param file_name: Name of the JavaScript file to load

    :return: The contents of the JavaScript file
    """

    file_path = JS_BASE_DIR / file_name.replace('/', os.sep)

    try:
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            return await f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"JavaScript file not found: {file_path}")
