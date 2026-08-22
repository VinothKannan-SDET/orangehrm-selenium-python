from configparser import ConfigParser


class ConfigReader:
    """
    Configuration reader for the OrangeHRM automation framework.

    Reads application configuration values from config.ini and
    provides access to the application URL and login credentials.
    """

    def __init__(self):
        """
        Initialize ConfigReader and load configuration
        from the application configuration file.
        """

        # Step 1: Create ConfigParser instance
        self.config = ConfigParser()

        # Step 2: Load configuration from config.ini
        self.config.read("config/config.ini")

    # ── Application Configuration ──

    @property
    def base_url(self):
        """
        Return the OrangeHRM application base URL.

        :return: Application URL configured in config.ini
        """

        # Step 1: Read application URL from configuration
        return self.config["application"]["url"]

    @property
    def username(self):
        """
        Return the OrangeHRM login username.

        :return: Login username configured in config.ini
        """

        # Step 1: Read login username from configuration
        return self.config["application"]["login_username"]

    @property
    def password(self):
        """
        Return the OrangeHRM login password.

        :return: Login password configured in config.ini
        """

        # Step 1: Read login password from configuration
        return self.config["application"]["login_password"]