import sqlite3

config_file = "setting.db"


class Setting:
    """my_setting(user, pause, eula, forward_type)"""
    my_id = None
    is_pause = 1
    eula = 0
    forward_type = ""
    forward_setting = []
    """user INTEGER, forward_to INTEGER, enable INTEGER, forward_self INTEGER"""
    point = ""
    temp_uid = 0
    temp_cid = 0
    temp_callbackdata = None
    temp_name = ""

    def load_all(self):
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        print("Loading setting")
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='my_setting'")
        if cur.fetchone()[0] == 1:
            print('table "my_setting" exist.')
        else:
            print('Table "my_setting" does not exist, creating...')
            cur.execute("CREATE TABLE my_setting(user INTEGER, pause INTEGER, eula INTEGER, forward_type TEXT)")
            data = [(0, 1, 0, "offline")]
            cur.executemany("INSERT INTO my_setting VALUES(?, ?, ?, ?)", data)
            print("Created!")

        cur.execute("PRAGMA table_info('my_setting')")
        columns = [column[1] for column in cur.fetchall()]
        if 'forward_type' not in columns:
            cur.execute("ALTER TABLE my_setting ADD COLUMN forward_type TEXT")
        if 'eula' not in columns:
            cur.execute("ALTER TABLE my_setting ADD COLUMN eula INTEGER")

        for row in cur.execute("SELECT user, pause, eula, forward_type FROM my_setting ORDER BY user"):
            self.my_id = row[0]
            self.is_pause = row[1]
            self.eula = row[2]
            self.forward_type = row[3]
        cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='forward_setting'")
        if cur.fetchone()[0] == 1:
            print('Table "forward_setting" exists.')
        else:
            print('Table "forward_setting" does not exist, creating...')
            cur.execute("CREATE TABLE forward_setting(user INTEGER, forward_to INTEGER, enable INTEGER, forward_self"
                        " INTEGER)")
            print("Created!")
        for row in cur.execute("SELECT user, forward_to, enable, forward_self FROM forward_setting ORDER BY user"):
            self.forward_setting.append(list(row))
        con.commit()
        print("All setting loaded!")

    def forward_update(self):
        """Need for update configs forwarding"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        self.forward_setting.clear()
        for row in cur.execute("SELECT user, forward_to, enable, forward_self FROM forward_setting ORDER BY user"):
            self.forward_setting.append(row)
        con.commit()

    def main_setting_update(self):
        """Updating main setting"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        for row in cur.execute(
                "SELECT user, pause, eula, forward_type FROM my_setting ORDER BY user"):
            self.my_id = row[0]
            self.is_pause = row[1]
            self.eula = row[2]
            self.forward_type = row[3]
        con.commit()

    def add_to_forwarding(self, user_id, forward_to):
        """Adding user and destination channel to forwarding"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        to = forward_to
        data = [(user_id, to, 1, 1)]
        cur.executemany("INSERT INTO forward_setting VALUES(?, ?, ?, ?)", data)
        con.commit()
        self.forward_update()

    def forward_contact_enable(self, user_id, status):
        """Adding parameters user | enable/disable forwarding from chat"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = f"UPDATE forward_setting SET enable = {status} WHERE user = {user_id}"
        cur.execute(sql)
        con.commit()
        self.forward_update()

    def forward_edit_destination(self, user_id, forward_to):
        """Edit destination channel for forwarding from chat"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = f"UPDATE forward_setting SET forward_to = {forward_to} WHERE user = {user_id}"
        cur.execute(sql)
        con.commit()
        self.forward_update()

    def pause(self, status):
        """Select pause status of all forwarding (bot run/pause forwarding)"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = f"UPDATE my_setting SET pause = {status} WHERE user = {self.my_id}"
        cur.execute(sql)
        con.commit()
        self.main_setting_update()

    def forward_self(self, user_id, status):
        """Select status of forwarding self messages"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = f"UPDATE forward_setting SET forward_self = {status} WHERE user = {user_id}"
        cur.execute(sql)
        con.commit()
        self.forward_update()

    def del_forward(self, user_id):
        """Remove user from forward setting"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = f"DELETE FROM forward_setting WHERE user = {user_id}"
        cur.execute(sql)
        con.commit()
        self.forward_update()

    def license_accept(self, status):
        """Select status of license accept (not used at this moment added for #future)"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = f"UPDATE my_setting SET eula = {status} WHERE user = {self.my_id}"
        # CHECK THIS SHIT (SQL LINE) AFTER ADDING FUNCTION
        cur.execute(sql)
        con.commit()
        self.main_setting_update()

    def del_all_forwarding(self):
        """WIPE all forward setting"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = "DELETE FROM forward_setting"
        cur.execute(sql)
        con.commit()
        self.forward_update()

    def add_my_id(self, my_id):
        """Adding user id to main setting. INT"""
        con = sqlite3.connect(config_file)
        cur = con.cursor()
        sql = f"UPDATE my_setting SET user = {my_id} WHERE user = 0"
        cur.execute(sql)
        con.commit()
        self.main_setting_update()
