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
        """
        Initialize the NoDriverEngine with the given parameters

        :param name: Name of the engine instance
        :param user_agent: Custom user agent string
        :param headless: Whether to run the browser in headless
        :param proxy: Proxy settings, if any
        """

        super().__init__(name, user_agent, headless, proxy)
