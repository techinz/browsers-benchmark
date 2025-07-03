from typing import Dict, Optional

from engines.nodriver_base import NoDriverBase


class NoDriverEngine(NoDriverBase):
    def __init__(
            self,
            name: str = "nodriver-chrome",

            user_agent: Optional[str] = None,
            headless: bool = True,

            proxy: Optional[Dict[str, str]] = None,
            **kwargs
    ):
        super().__init__(name, user_agent, headless, proxy)
