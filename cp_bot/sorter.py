from cp_bot.reg_user import NotRegistered
from cp_bot.admin_panel import AdminPanel
from cp_bot.get_info import GetInfo
from cp_bot.bot_processor import Processor
from proxy_class import setting


class Sorter:
    def __init__(self, client, users, message=None, callback_data=None):
        self.message = message
        self.callback_data = callback_data
        if message:
            self.user_id = message.from_user.id
        if callback_data:
            self.user_id = callback_data.from_user.id
        self.processor = Processor(client, message, users, callback_data)
        self.client = client
        self.users = users

    async def callback_filter(self):
        data = self.callback_data.data
        user_app = await GetInfo().get_user_app(self.user_id, self.users)
        if data == "setting":
            await self.processor.setting()
        elif data.startswith("a_"):
            a_panel = AdminPanel()
            await a_panel.cmd_processor(self.client, self.callback_data)
        elif data == "start":
            await self.processor.start()
        elif data == "stop":
            await self.processor.stop()
        elif data == "add":
            await self.processor.add()
        elif data == "remove_step1":
            await self.processor.remove_step1(user_app)
        elif data == "freeze_step1":
            await self.processor.freeze_step1(user_app)
        elif data == "unfreeze_step1":
            await self.processor.unfreeze_step1(user_app)
        elif data == "forward_my_step1":
            await self.processor.forward_my_step1(user_app)
        elif data == "change_destination_step1":
            await self.processor.change_destination_step1(user_app)
        elif data == "main_menu":
            await self.processor.main_menu()
        elif data == "about":
            await self.processor.about()
        elif data == "status":
            await self.processor.status()
        elif data == "list":
            await self.processor.list(user_app)
        elif data == "help":
            await self.processor.help()
        elif data.startswith("select_existing_"):
            await self.processor.destination_select_existing_step2(user_app)
        elif data.startswith("remove_"):
            await self.processor.remove_step2(user_app)
        elif data.startswith("freeze_"):
            await self.processor.freeze_step2(user_app)
        elif data.startswith("unfreeze_"):
            await self.processor.unfreeze_step2(user_app)
        elif data.startswith("change_destination_"):
            await self.processor.change_destination_step2(user_app)
        elif data.startswith("select_channel_"):
            await self.processor.change_destination_step3(user_app)
        elif data.startswith("exist_chat_"):
            await self.processor.add_from_exist_chat_step2(user_app)
        elif data.startswith("sync_contact_"):
            await self.processor.add_from_sync_contact_step2(user_app)
        elif data.startswith("forward_my_step2_"):
            await self.processor.forward_my_step2(user_app)
        elif data.startswith("add_to_forward_channel") or data.startswith("add_to_forward_group"):
            await self.processor.add_to_forward_cg_step1(user_app)
        elif data.startswith("add_cg_"):
            await self.processor.add_to_forward_cg_step2(user_app)
        elif data == "add_from_send_contact_step1":
            await self.processor.add_from_send_contact_step1()
        elif data == "add_from_exist_chat_step1":
            await self.processor.add_from_exist_chat_step1(user_app)
        elif data == "add_from_sync_contact_step1":
            await self.processor.add_from_sync_contact_step1(user_app)
        elif data == "add_from_forwarded_message_step1":
            await self.processor.add_from_forwarded_message_step1()
        elif data == "destination_create_new":
            await self.processor.destination_create_new(user_app)
        elif data == "destination_select_existing_step1":
            await self.processor.destination_select_existing_step1(user_app)
        elif data == "burn_all":
            await self.processor.burn_all()
        elif data == "fbi_open_up":
            await self.processor.fbi_open_up(user_app)
        elif data == "forward_my_off":
            await self.processor.forward_my_off()
        elif data == "forward_my_on":
            await self.processor.forward_my_on()
        elif data == "wipe_me":
            await self.processor.wipe_me()
        elif data.startswith("code_"):
            not_registered = NotRegistered()
            await not_registered.input_auth_code(self.callback_data, self.user_id, self.users, self.client)
        elif data.startswith("wipe_me_"):
            await self.processor.start_wipe_user()
        elif data.startswith("in_list_"):
            await self.processor.nav_list()

    async def message_filter(self):
        get_info = GetInfo()
        user = await get_info.get_user_app(self.user_id, self.users)
        if await get_info.is_register(self.user_id):
            if self.message.text == "/start":
                if setting.user_setting[f"{self.user_id}"]["is_blocked"]:
                    await self.processor.blocked_message()
                else:
                    await self.processor.start_message()
            if setting.user_setting[f"{self.user_id}"]["menu_point"] == "add_from_send_contact_step2":
                await self.processor.add_from_send_contact_step2(user)
            if setting.user_setting[f"{self.user_id}"]["menu_point"] == "add_from_forwarded_message_step2":
                await self.processor.add_from_forwarded_message_step2(user)
            if self.message.text == "/upd_start":
                await self.processor.upd_start()
            if self.message.text == "/upd_end":
                await self.processor.upd_end()
            if self.message.text.startswith("/all"):
                await self.processor.global_message()
            if self.message.text.startswith("/i_am_god"):
                print(1)
                a_panel = AdminPanel()
                await a_panel.god_mode(self.client, self.message)
        elif not await get_info.is_register(self.user_id):
            not_registered = NotRegistered()
            await not_registered.filter(self.message, self.users, self.client)
