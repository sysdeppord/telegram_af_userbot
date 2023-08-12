import sqlite3

config_file = "setting.db"


class Setting:
    def __init__(self):
        self.user_setting = {}
        self.con = sqlite3.connect(config_file)
        self.cur = self.con.cursor()
        self.__load_user_setting()
        self.__load_forward_setting()

    def __load_user_setting(self):
        """Check and load main setting from database"""
        print("Loading user setting")
        self.cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='my_setting'")
        if self.cur.fetchone()[0] == 1:
            print('table "my_setting" exist.')
        else:
            print('Table "my_setting" does not exist, creating...')
            self.cur.execute("CREATE TABLE my_setting(user INTEGER, pause INTEGER, eula INTEGER, forward_type TEXT, "
                             "authorized INTEGER, is_blocked INTEGER, blocked_text TEXT)")
            self.con.commit()
            print("Created!")
        self.cur.execute("PRAGMA table_info('my_setting')")
        columns = [column[1] for column in self.cur.fetchall()]
        if 'forward_type' not in columns:
            self.cur.execute("ALTER TABLE my_setting ADD COLUMN forward_type TEXT")
            self.con.commit()
        if 'eula' not in columns:
            self.cur.execute("ALTER TABLE my_setting ADD COLUMN eula INTEGER")
            self.con.commit()
        if 'authorized' not in columns:
            self.cur.execute("ALTER TABLE my_setting ADD COLUMN authorized INTEGER")
            self.con.commit()
        if 'is_blocked' not in columns:
            self.cur.execute("ALTER TABLE my_setting ADD COLUMN is_blocked INTEGER")
            self.con.commit()
        if 'blocked_text' not in columns:
            self.cur.execute("ALTER TABLE my_setting ADD COLUMN blocked_text TEXT")
            self.con.commit()
        for row in self.cur.execute("SELECT user, pause, eula, forward_type, authorized, is_blocked, blocked_text FROM my_setting ORDER BY user"):
            self.user_setting.update({f"{row[0]}": {"pause": row[1],
                                                    "eula": row[2],
                                                    "forward_type": row[3],
                                                    "authorised": row[4],
                                                    "menu_point": "",
                                                    "temp_data": "",
                                                    "auth_code": "",
                                                    "temp_uid": 0,
                                                    "temp_cid": 0,
                                                    "is_blocked": row[5],
                                                    "blocked_text": row[6],
                                                    "temp_callbackdata": None,
                                                    "temp_name": "",
                                                    "forward_setting": {}}})

    def __load_forward_setting(self):
        """Loading user forward setting on start"""
        print("loading forward setting")
        if self.user_setting:
            print("Loading in progress")
            for user in self.user_setting:
                for row in self.cur.execute(f"SELECT user, forward_to, enable, forward_self FROM "
                                            f"u{user}_forward_setting ORDER BY user"):
                    self.user_setting[f"{user}"]["forward_setting"].update({f"{row[0]}": {
                        "forward_to": row[1],
                        "enable": row[2],
                        "forward_self": row[3]}})
        if not self.user_setting:
            print("EMPTY")

    def register(self, user_id):
        """
        Add new user into database
        'user_id' - Telegram user id
        """
        data = [(user_id, 1, 0, "offline", 0, 0, "")]
        self.cur.executemany("INSERT INTO my_setting VALUES(?, ?, ?, ?, ?, ?, ?)", data)
        self.user_setting.update({f"{user_id}": {"pause": 1,
                                                 "eula": 0,
                                                 "forward_type": "offline",
                                                 "authorised": 0,
                                                 "menu_point": "",
                                                 "temp_data": "",
                                                 "auth_code": "",
                                                 "temp_uid": 0,
                                                 "temp_cid": 0,
                                                 "is_blocked": 0,
                                                 "blocked_text": "",
                                                 "temp_callbackdata": None,
                                                 "temp_name": "",
                                                 "forward_setting": {}}})
        self.cur.execute(f"CREATE TABLE u{user_id}_forward_setting(user INTEGER, forward_to INTEGER, enable INTEGER, "
                         f"forward_self INTEGER)")
        self.con.commit()

    def authorise(self, user_id):
        """
        Select user authorise status into database
        'user_id' - Telegram user id
        """
        sql = f"UPDATE my_setting SET authorized = 1 WHERE user = {user_id}"
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["authorised"] = 1

    def add_to_forwarding(self, user_id, forward_user_id, forward_to):
        """
        Adding user and destination channel to forwarding
        'user_id' - id bot user where adding forwarding
        'forward_user_id' - chat id user for add to forwarding
        'forward_to' - channel id where messages forwarding
        """
        to = forward_to
        data = [(forward_user_id, to, 1, 1)]
        self.cur.executemany(f"INSERT INTO u{user_id}_forward_setting VALUES(?, ?, ?, ?)", data)
        self.con.commit()
        self.user_setting[f"{user_id}"]["forward_setting"].update({
            f"{forward_user_id}": {"forward_to": to,
                                   "enable": 1,
                                   "forward_self": 1}})

    def forward_contact_enable(self, user_id, forward_user_id, status):
        # need fix fuckin dictionary for adding auto stop forwarding feature
        """
        Edit status forwarding for chat. NOT GLOBAL PAUSE FORWARDING!
        'user_id' - id bot user where use forwarding
        'forward_user_id' - chat id user for forwarding
        'status' - 0/1 (INT) disable/enable forwarding from this chat
        """
        sql = f"UPDATE u{user_id}_forward_setting SET enable = {status} WHERE user = {forward_user_id}"
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["forward_setting"][f"{forward_user_id}"]["enable"] = status

    def forward_edit_destination(self, user_id, forward_user_id, forward_to):
        """
        Edit destination channel for forwarding from chat
        'user_id' - id bot user where use forwarding
        'forward_user_id' - chat id user for forwarding
        'forward_to' - new channel id to forwarding messages
        """
        sql = f"UPDATE u{user_id}_forward_setting SET forward_to = {forward_to} WHERE user = {forward_user_id}"
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["forward_setting"][f"{forward_user_id}"]["forward_to"] = forward_to

    def pause(self, user_id, status):
        """
        Select pause status of all forwarding (bot run/pause forwarding)
        'user_id' - id bot user where use forwarding
        'status' - 0/1 (INT) disable/enable global forwarding (bot pause)
        """
        sql = f"UPDATE my_setting SET pause = {status} WHERE user = {user_id}"
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["pause"] = status

    def forward_self(self, user_id, forward_user_id, status):
        """
        Select status of forwarding self messages
        'user_id' - id bot user where use forwarding
        'forward_user_id' - chat id user for forwarding
        'status' - 0/1 (INT) disable/enable forwarding self messages in selected chat
        """
        sql = f"UPDATE u{user_id}_forward_setting SET forward_self = {status} WHERE user = {forward_user_id}"
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["forward_setting"][f"{forward_user_id}"]["forward_self"] = status

    def del_forward(self, user_id, forward_user_id):
        """
        Remove user from forward setting (without remove channel where messages forwarded)
        'user_id' - id bot user where use forwarding
        'forward_user_id' - chat id user for remove forwarding
        """
        sql = f"DELETE FROM u{user_id}_forward_setting WHERE user = {forward_user_id}"
        self.cur.execute(sql)
        self.con.commit()
        del self.user_setting[f"{user_id}"]["forward_setting"][f"{forward_user_id}"]

    def __license_accept(self, user_id, status):
        """
        Select status of end user license accept (not used at this moment added for #future)
        """
        sql = f"UPDATE my_setting SET eula = {status} WHERE user = {user_id}"
        # future CHECK THIS SHIT (SQL LINE) AFTER ADDING FUNCTION
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["eula"] = status

    def del_all_forwarding(self, user_id):
        """
        WIPE all forward setting for user
        'user_id' - id bot user to remove forward setting
        """
        sql = f"DELETE FROM u{user_id}_forward_setting"
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["forward_setting"] = {}

    def set_block_user(self, user_id, status, blocked_text):
        """
        Set blocked status and text to user
        'user_id' - id bot user to set status
        'status' - 1/0 block/unblock user
        'blocked_text' - text to show user if him get blocked message
        """
        sql = f"UPDATE my_setting SET is_blocked = {status}, blocked_text = '{blocked_text}' WHERE user = {user_id}"
        self.cur.execute(sql)
        self.con.commit()
        self.user_setting[f"{user_id}"]["is_blocked"] = status
        self.user_setting[f"{user_id}"]["blocked_text"] = blocked_text
