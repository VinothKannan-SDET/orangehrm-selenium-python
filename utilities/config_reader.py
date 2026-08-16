from configparser import ConfigParser

class ConfigReader:
    def __init__(self):
        self.config = ConfigParser()
        self.config.read("config/config.ini")

    @property
    def base_url(self):
        return self.config["application"]["url"]

    @property
    def username(self):
        return self.config["application"]["login_username"]

    @property
    def password(self):
        return self.config["application"]["login_password"]