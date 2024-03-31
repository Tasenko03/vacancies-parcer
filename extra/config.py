class ConfigD:
    """
    Type annotations for configurations
    """

    seed_urls: list[str]
    headers: dict[str, str]
    encoding: str
    timeout: int
    should_verify_certificate: bool
    headless_mode: bool

    def __init__(self,
                 seed_urls: list[str],
                 headers: dict[str, str],
                 encoding: str,
                 timeout: int,
                 should_verify_certificate: bool,
                 headless_mode: bool
                 ):
        """
        Initializes an instance of the ConfigDTO class
        """

        self.seed_urls = seed_urls
        self.headers = headers
        self.encoding = encoding
        self.timeout = timeout
        self.should_verify_certificate = should_verify_certificate
        self.headless_mode = headless_mode
