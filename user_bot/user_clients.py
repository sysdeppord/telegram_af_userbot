import os
from pyrogram import Client
from config.app_config import *
from config.tg_config import *
from proxy_class import setting


class UserClients:

    def __init__(self):
        self.users = []

    def add_user_client(self):
        print("Building users apps")
        for usr in setting.user_setting:
            if setting.user_setting[f"{usr}"]["authorised"] and os.path.exists(f"./files/users/u{usr}"):
                user_id = usr
                name = f"u{user_id}"
                self.users.append(Client(name, api_id=api_id, api_hash=api_hash, app_version=name_app + ver_app,
                                    device_model=device_model, system_version=system_version,
                                    workdir=f"./files/users/{name}"))
        print("OK")

    def run_user_client(self):
        pass
