from cp_bot import keyboards
import copy
from pyrogram.types import InlineKeyboardButton
from proxy_class import setting


class Keyboard:

    async def build(self, list_for_build=None, prefix=None, user_id=None, cmd=None):
        if list_for_build and prefix:
            keyboard = []
            keyboard_add = None
            for item in list_for_build:
                i = [InlineKeyboardButton(item[0], callback_data=f"{prefix}{item[1]}")]
                keyboard.append(i)
            kb = list(self.chunk_list(keyboard, chunk_size=10))
            if prefix == "select_existing_":
                keyboard_add = copy.deepcopy(keyboards.select_existing)
            elif prefix == "remove_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            elif prefix == "freeze_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            elif prefix == "unfreeze_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            elif prefix == "select_channel_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            elif prefix == "exist_chat_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            elif prefix == "forward_my_step2_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            elif prefix == "add_cg_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            elif prefix == "sync_contact_":
                keyboard_add = copy.deepcopy(keyboards.bottom_button)
            if len(list_for_build) < 11:
                kb[0].append(keyboard_add[0])
                kb[0].append(keyboard_add[1])
            else:
                position = 0
                end_position = len(kb) - 1
                for i in kb:
                    if position == 0:
                        i.append(copy.deepcopy(keyboards.nav_list[0]))
                    elif position == end_position:
                        i.append(copy.deepcopy(keyboards.nav_list[1]))
                    else:
                        i.append(copy.deepcopy(keyboards.nav_list[0]))
                        i.append(copy.deepcopy(keyboards.nav_list[1]))
                    for button in keyboard_add:
                        i.append(button)
                    position += 1
            setting.user_setting[f"{user_id}"]["kb_list"] = kb
            setting.user_setting[f"{user_id}"]["kb_list_point"] = 0
            return kb[0]
        elif cmd:
            if cmd == "in_list_next":
                position = setting.user_setting[f"{user_id}"]["kb_list_point"] + 1
            elif cmd == "in_list_previous":
                position = setting.user_setting[f"{user_id}"]["kb_list_point"] - 1
            setting.user_setting[f"{user_id}"]["kb_list_point"] = position
            return setting.user_setting[f"{user_id}"]["kb_list"][position]

    @staticmethod
    def chunk_list(lst, chunk_size):
        for i in range(0, len(lst), chunk_size):
            yield lst[i:i + chunk_size]
