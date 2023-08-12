# telegram_af_userbot
Userbot for auto forward messages from users UA|EN|RU description

UA (12.08.2023 v 0.1.2.0 beta)
Юзербот (той який авторизується як додаток у ваш Телеграм аккаунт, не плутати зі звичайним ботом в Телеграм) для автоматичних пересилань особистих повідомлень від користувачів
Базується на бібліотеці "Pyrogram"

Передісторія:
Мене задовбали мої контакти, котрі пишуть і видаляють повідомлення до того як я їх прочитав, тому я створив бота, який автоматично пересилатиме повідомлення від необхідних користувачів в окремий канал, де я в разі видалення зможу їх спокійнесенько прочитати.

Попередження!
Ви використовуєте його на свій страх і ризик, я не несу ніякої відповідальності і не приймаю претензії за будь-які можливі наслідки при використанні цього бота (як от можливий бан вашого аккаунту в Телеграм)! Використовуючи цього бота ви підтверджуєте те, що ви знаєте що робите і до яих наслідків це може призвести!

Як почати:
Завантаж бота
Встанови необхідні бібліотеки Python з файлу "requipments.txt"
Зарусти "setup.py" і слідуючи підказкам вводь необхідні дані на основі яких заповняться поля (api_id, api_hash, bot_token, admin_id) в файлі "config/th_config.py"
Запусти бота через файл "main.py"
Після запуску перейди в бота та авторизуйся в свій телеграм аккаунт (тепер наявна авторизація з хмарним паролем)
Після авторизації зайди в налаштування телеграм, вибери сесію бота з якого ти зайшов в телеграм та вимкни можливість для цієї сесії отримувати дзвінки та секретні чати
Додай корискувачів/чати/канали в пересилку через відповідне меню
Запусти пересилку в меню налаштувань відповідною кнопкою


Фічі які реалізовані:
- (NEW!) Авторизація з увімкненим хмарним паролем
- (NEW!) Код авторизації телеграм тепер вводиться за допомогою клавіатури бота
- (NEW!) Виведення помилок при авторизації
- (NEW!) Код повторно відправляється, якщо скасовано
- (NEW!) Код авторизації пропонується ввести повторно, якщо був введений не правильно
- Авторизація через самого бота
- Мультиаккаунт - одна панель управління для кількох користувачів
- Панель управління через телеграм бота
- Навігація через кнопки бота не використовуючи команди, окрім як /start
- Збереження та завантаження налаштувань з/в базу даних SQLite
- Додавання/видалення користувача в пересилку
- Можливість заморозити/розморозити пересилку окремого користувача незалежно від інших
- Можливість запустити/зупинити пересилку всіх користувачів (глобально, заморозка/розморозка пересилання окремо по користувачу лишаються незмінними)
- Можливість вимкнути/ввімкнути пересилку своїх повідомлень в чаті з доданими користувачами
- Виведення списку всіх доданих пересилок по кожному користувачу з їх статусами активності
- Пересилка повідомлень від користувачів в свій приватний канал
- Пересилка повідомлень від каналів (в тому числі з захищеним контентом)
- Пересилка повідомлень з груп (в тому числі з захищеним контентом)
- Додавання в пересилку через:
- - Відправлення контакту користувача з його профілю Телеграм
- - Вибір наявного чату з користувачем
- - Вибір синхронізованого контакту користувача в Телеграм
- - Додавання через переслане повідомлення користувача, якщо у нього в налаштуваннях приватності не активний пункт приховання посилання на його аккаунт при пересилці повідомлення
- При додаванні в пересилку є можливість:
- - Автоматично створити новий канал (створюється приватний канал)
- - Вибрати вже наявний (приватний канал, творцем якого являєшся ти)
- Можливість змінити канал куди пересилаються повідомлення (той же вибір, який надається при додаванні користувача в пересилку)
- Видалення користувача з пересилки (канал куди пересилалися повідомлення зберігається)
- Повний вайп налаштувань пересилки повідомлень з їх каналами (незворотня дія)
- Пересилання типів повідомлень:
- - Текст
- - Фото (в тому числі згораємі)
- - Відео (в тому числі згораємі)
- - Відео повідомлення (оті кружочки :))
- - Голосові повідомлення
- - Геопозиція (не плутати з маячком)
- - Переслані повідомлення як від інших користувачів так і з каналів
- - Стікери
- - Гіфки
- - Файли
- - Група медіа (є нюанс, дивись в можливих проблемах)
- Статус онлайн не змінюється (невидимка, пояснення дивись в пункті "можливі проблеми")
- Статус прочитки повідомлень не змінюється, в тому числі і для згораємих фото/відео
- Сповіщення про неможливість переслати повідомлення, якщо бот не бачить канал

Можливі проблеми:
- Група медіа пересилається по одному файлу, але вона є одним повідомленням - Так це така фіча чомусь бібліотека Pyrogram баче їх як окремі повідомлення, і з цим є проблеми по флуду, ще не вирішив її тому в консоль буде кидати повідомлення про повторнц спробу надсилання через 2 секунди.
- Якщо поступає група пересланих повідомлень вони пересилаються по одному та з затримкою - Так, це кожне окреме повідомлення, тому ситуація така сама як з групованими медіа вище.
- Про статус онлайн і зайві сповіщення - Пересилання повідомлень реалізоване через відкладені повідомлення з таймером в одну хвилину (можна налаштувати в файлі "user_processor.py" -> class UserMessages -> forward_processor -> date -> minutes=1). Це пов'язане з тим, що при прямій пересилці в тебе активується статус "онлайн". Це не моя забаганка, так реалізований механізм самого Телеграм. Також, хоча відкладені повідомлення публікуються зі статусом "не сповіщати" тобі приходитимуть сповіщення. Частково це лікується вимкненням сповіщеннів від каналу. Чому частково? На телефоні (принаймні з ОС Андроїд) після цього сповіщення перестають йти, але в телеграм клієнті для ПК спливаючі сповіщення лишаться, бо так влаштований телеграм клієнт.
- Користувач відредагував повідомлення, а в пересланих воно не змінилося  - Звісно, так працюють переслан повідомлення, спробуй сам  переслати своє повідомлення а потім відредагувати його і порівняти. Тимпаче бот пересилає їх одразу коли вони приходять  (можливо вийняток групи медіа та групи пересланих повідомлень).

EN (12.08.2023 v 0.1.2.0 beta)
A userbot (the one that logs in as an application to your Telegram account, not to be confused with a regular Telegram bot) for automatic sending of personal messages from users
Based on the "Pyrogram" library

Background:
I was fed up with my contacts writing and deleting messages before I read them, so I created a bot that would automatically forward messages from the necessary users to a separate channel where I could read them in case of deletion.

Warning.
You use it at your own risk, I do not bear any responsibility and do not accept any claims for any possible consequences of using this bot (such as a possible ban of your Telegram account)! By using this bot, you confirm that you know what you are doing and the consequences it may entail!

How to get started:
Download the bot
Install the necessary Python libraries from the file "requipments.txt"
Run the "setup.py" file and follow the prompts to enter the necessary data based on which the fields (api_id, api_hash, bot_token, admin_id) in the "config/th_config.py" file will be filled in
Run the bot through the file "main.py"
After launching, go to the bot and log in to your Telegram account (now you have authorization with a cloud password)
After authorization, go to the telegram settings, select the bot session from which you logged into telegram and disable the ability for this session to receive calls and secret chats
Add users/chats/channels to the forwarding via the corresponding menu
Start forwarding in the settings menu with the corresponding button


Features that have been implemented:
- (NEW!) Authorization with cloud password enabled
- (NEW!) Telegram authorization code is now entered using the bot keyboard
- (NEW!) Display of errors during authorization
- (NEW!) Code is resent if canceled
- (NEW!) Authorization code is prompted to re-enter if it was entered incorrectly
- Authorization through the bot itself
- Multi-account - one control panel for several users
- Control panel through the bot's telegram
- Navigation through the bot buttons without using commands other than /start
- Saving and loading settings from/to SQLite database
- Adding/removing a user to the list
- Ability to freeze/unfreeze a single user's transfer independently of others
- Ability to start/stop the forwarding of all users (globally, freezing/unfreezing the forwarding separately for each user remains unchanged)
- Ability to disable/enable forwarding of your messages in chat with added users
- Displaying a list of all added forwards for each user with their activity statuses
- Forwarding messages from users to your private channel
- Forwarding messages from channels (including those with protected content)
- Forwarding messages from groups (including those with protected content)
- Add to forwarding by:
- - Sending a user's contact from their Telegram profile
- - Selecting an existing chat with the user
- - Selecting a synchronized user contact in Telegram
- - Adding a user through a forwarded message if the option to hide the link to their account when forwarding a message is not active in their privacy settings
- When adding to a forwarded message, you can:
- - Automatically create a new channel (a private channel is created)
- - Select an existing channel (a private channel created by you)
- Ability to change the channel to which messages are sent (the same choice that is provided when adding a user to the list)
- Removing a user from the forwarding (the channel to which messages were forwarded is saved)
- Full wipe of message forwarding settings with their channels (irreversible)
- Forwarding message types:
- - Text
- - Photos (including burnable ones)
- - Video (including burnable ones)
- - Video messages (those circles :))
- - Voice messages
- - Geo-position (not to be confused with a beacon)
- - Forwarded messages from other users and from channels
- - Stickers
- - Gifs
- - Files
- - Media group (there is a nuance, see possible problems)
- The online status does not change (invisible, see the explanation in the "possible problems" paragraph)
- The status of reading messages does not change, including for burned photos/videos
- Notification about the inability to forward a message if the bot does not see the channel

Possible problems:
- A group of media is forwarded in one file, but it is one message - Yes, this is such a feature, for some reason the Pyrogram library sees them as separate messages, and there are problems with this due to flooding, I have not solved it yet, so the console will throw a message about repeated attempts to send via 2 seconds.
- If a group of forwarded messages arrives, they are forwarded one at a time and with a delay - Yes, this is each individual message, so the situation is the same as with grouped media above.
- About online status and redundant notifications - Forwarding of messages is implemented through delayed messages with a timer of one minute (can be configured in the file "user_processor.py" -> class UserMessages -> forward_processor -> date -> minutes=1). This is due to the fact that the "online" status is activated for you during a direct transfer. This is not my whim, this is the implemented mechanism of Telegram itself. Also, although snoozed messages are published with a "do not notify" status, you will receive notifications. This is partially remedied by turning off notifications from the channel. Why partially? On the phone (at least with the Android OS), notifications stop going after this, but pop-up notifications remain in the Telegram client for PC, because this is how the Telegram client is arranged.
- The user edited the message, but it has not changed in forwarded messages - Of course, this is how forwarded messages work, try to forward your message yourself and then edit it and compare. Instead, the bot forwards them as soon as they arrive (with the possible exception of the media group and forwarded message group).

RU (12.08.2023 v 0.1.2.0 beta)
Юзербот (тот который авторизуется как приложение в ваш Телеграм аккаунт, не путать с обычным ботом в Телеграм) для автоматических пересылок личных сообщений от пользователей
Базируется на библиотеке "Pyrogram"

Предыстория:
Меня задолбали мои контакты, которые пишут и удаляют сообщения до того как я их прочитал, поэтому я создал бота, который автоматически будет пересылать сообщения от необходимых пользователей в отдельный канал, где я в случае удаления смогу их спокойно прочитать.

Предупреждение!
Вы используете его на свой страх и риск, я не несу никакой ответственности и не принимаю претензии за любые возможные последствия при использовании этого бота (как вот возможный бан вашего аккаунта в Телеграм)! Используя этого бота вы подтверждаете то, что вы знаете что делаете и к яих последствиям это может привести!

Как начать:
Загрузи бота
Установи необходимые библиотеки Python из файла "requipments.txt"
Заруби "setup.py" и следуя подсказкам вводи необходимые данные на основе которых заполнятся поля (api_id, api_hash, bot_token, admin_id) в файле "config/th_config.py"
Запусти бота через файл "main.py"
После запуска перейди в бота и авторизуйся в свой телеграмм аккаунт (теперь имеется авторизация с облачным паролем)
После авторизации зайди в настройки телеграмм, выбери сессию бота с которого ты зашел в телеграмм и выключи возможность для этой сессии получать звонки и секретные чаты
Добавь пользователей/чаты/каналы в пересылку через соответствующее меню
Запусти пересылку в меню настроек соответствующей кнопкой


Фичи которые реализованы:
- (NEW!) Авторизация с включенным облачным паролем
- (NEW!) Код авторизации телеграмм теперь вводится с помощью клавиатуры бота
- (NEW!) Вывод ошибок при авторизации
- (NEW!) Код повторно отправляется, если отменен
- (NEW!) Код авторизации предлагается ввести повторно, если был введен не правильно
- Авторизация через самого бота
- Мультиаккаунт - одна панель управления для нескольких пользователей
- Панель управления через телеграм бота
- Навигация через кнопки бота не используя команды, кроме как /start
- Сохранение и загрузка настроек из/в базу данных SQLite
- Добавление/удаление пользователя в пересылку
- Возможность заморозить/разморозить пересылку отдельного пользователя независимо от других
- Возможность запустить/остановить пересылку всех пользователей (глобально, заморозка/разморозка пересылки отдельно по пользователю остаются неизменными)
- Возможность отключить/включить пересылку своих сообщений в чате с добавленными пользователями
- Вывод списка всех добавленных пересылок по каждому пользователю с их статусами активности
- Пересылка сообщений от пользователей в свой приватный канал
- Пересылка сообщений от каналов (в том числе с защищенным контентом)
- Пересылка сообщений из групп (в том числе с защищенным контентом)
- Добавление в пересылку через:
- - Отправку контакта пользователя из его профиля Телеграм
- - Выбор имеющегося чата с пользователем
- - Выбор синхронизированного контакта пользователя в Телеграм
- - Добавление через пересланное сообщение пользователя, если у него в настройках приватности не активен пункт скрытия ссылки на его аккаунт при пересылке сообщения
- При добавлении в пересылку есть возможность:
- - Автоматически создать новый канал (создается приватный канал)
- - Выбрать уже имеющийся (приватный канал, создателем которого являешься ты)
- Возможность изменить канал куда пересылаются сообщения (тот же выбор, который предоставляется при добавлении пользователя в пересылку)
- Удаление пользователя из пересылки (канал куда пересылались сообщения сохраняется)
- Полный вайп настроек пересылки сообщений с их каналами (необратимое действие)
- Пересылка типов сообщений:
- - Текст
- - Фото (в том числе сгораемые)
- - Видео (в том числе сгораемые)
- - Видео сообщения (те кружочки :))
- - Голосовые сообщения
- - Геопозиция (не путать с маячком)
- - Пересланные сообщения как от других пользователей так и с каналов
- - Стикеры
- - Гифки
- - Файлы
- - Группа медиа (есть нюанс, смотри в возможных проблемах)
- Статус онлайн не меняется (невидимка, объяснение смотри в пункте "возможные проблемы")
- Статус прочитки сообщений не меняется, в том числе и для сгораемых фото/видео
- Оповещение о невозможности переслать сообщение, если бот не видит канал

Возможные проблемы:
- Группа медиа пересылается по одному файлу, но она является одним сообщением - Так это такая фича почему-то библиотека Pyrogram видит их как отдельные сообщения, и с этим есть проблемы по флуду, еще не решил ее поэтому в консоль будет бросать сообщение о повторной попытке отправки через 2 секунды.
- Если поступает группа пересланных сообщений они пересылаются по одному и с задержкой. - Да, это каждое отдельное сообщение, поэтому ситуация такая же как с группированными медиа выше.
- О статусе онлайн и лишних оповещениях - Пересылка сообщений реализована через отложенные сообщения с таймером в одну минуту (можно настроить в файле "user_processor.py" -> class UserMessages -> forward_processor -> date -> minutes=1). Это связано с тем, что при прямой пересылке у тебя активируется статус "онлайн". Это не моя прихоть, так реализован механизм самого телеграммы. Также, хотя отложенные сообщения публикуются со статусом "не оповещать" тебе будут приходить уведомления. Частично это лечится отключением извещений от канала. Почему отчасти? На телефоне (по крайней мере с ОС Андроид) после этого уведомления перестают идти, но в телеграммах клиенты для ПК всплывающие уведомления останутся, так устроен телеграмм клиент.
– Пользователь отредактировал сообщение, а у пересланных оно не изменилось – Конечно, так работают пересланное сообщение, попробуй сам переслать свое сообщение а затем отредактировать его и сравнить. Тем более бот пересылает их сразу когда они приходят (возможно исключение группы медиа и группы пересланных сообщений).
