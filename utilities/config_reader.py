import os
from configparser import ConfigParser
from dotenv import load_dotenv


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
        # Load environment variables from .env
        load_dotenv(override=True)

        # Step 1: Create ConfigParser instance
        self.config = ConfigParser()

        # Step 2: Load configuration from config.ini
        self.config.read("config/config.ini")

    # ── Application Configuration ──

    @property
    def base_url(self):
        """
        Return the OrangeHRM application base URL.

        :return: :return: Application URL configured through BASE_URL environment variable
        """

        # Step 1: Read application URL from configuration
        base_url = self.config["application"]["url"]

        if not base_url:
            raise RuntimeError(
                "Application URL is not configured in config.ini."
            )

        return base_url

    @property
    def username(self):
        """
        Return the OrangeHRM login username.

        :return: Login username configured in config.ini
        """

        # Step 1: Read login username from configuration
        username = os.getenv("APP_USERNAME")

        if not username:
            raise RuntimeError(
                "APP_USERNAME environment variable is not configured."
            )

        return username

    @property
    def password(self):
        """
        Return the OrangeHRM login password.

        :return: Login password configured in config.ini
        """

        # Step 1: Read login password from configuration
        password = os.getenv("APP_PASSWORD")

        if not password:
            raise RuntimeError(
                "APP_PASSWORD environment variable is not configured."
            )

        return password