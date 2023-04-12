# telegram_af_userbot
Userbot for auto forward messages from users UA|EN|RU description

UA
Юзербот (той який авторизується як додаток у ваш Телеграм аккаунт, не плутати зі звичайним ботом в Телеграм) для автоматичних пересилань особистих повідомлень від користувачів
Базується на бібліотеці "Pyrogram"

Передісторія:
Мене задовбали мої контакти, котрі пишуть і видаляють повідомлення до того як я їх прочитав, тому я створив бота, який автоматично пересилатиме повідомлення від необхідних користувачів в окремий канал, де я в разі видалення зможу їх спокійнесенько прочитати.

Попередження!
Ви використовуєте його на свій страх і ризик, я не несу ніякої відповідальності і не приймаю претензії за будь-які можливі наслідки при використанні цього бота (як от можливий бан вашого аккаунту в Телеграм)! Використовуючи цього бота ви підтверджуєте те, що ви знаєте що робите і до яих наслідків це може призвести!

Як почати:
Завантаж бота
В файлі "tg_config.py" заміни всі дані на свої
При необхідності змінювати дані в боті з іншого аккаунта відредагуй в файлі "bot_processor.py" змінну "admin_id" на свій id другого Телеграм аккаунта
Запусти бота через файл "main.py"
При першому запуску авторизуйся в свый телеграм аккаунт
Після авторизації зайди в налаштування телеграм, вибери сесію  з якої ти зайшов в телеграм та вимкни можливість для цієї сесії отримувати дзвінки та секретні чати

Фічі які реалізовані:
- Панель управління через телеграм бота
- Навігація через кнопки бота не використовуючи команди, окрім як /start
- Збереження та завантаження налаштувань в базу даних SQLite
- Додавання/видалення користувача в пересилку
- Можливість заморозити/розморозити пересилку окремого користувача незалежно від інших
- Можливість запустити/зупинити пересилку всіх користувачів (глобально, заморозка/розморозка пересилання окремо по користувачу лишаються незмінними)
- Можливість вимкнути/ввімкнути пересилку своїх повідомлень в чаті з доданими користувачами
- Виведення списку всіх доданих пересилок по кожному користувачу з їх статусами активності
- Пересилка повідомлень від користувачів в свій приватний канал
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
- - Повідомлення з каналів
- - Переслані повідомлення від інших користувачів
- - Стікери
- - Гіфки
- - Файли
- - Група медіа (є нюанс, дивись в можливих проблемах)
- Статус онлайн не змінюється (невидидка, пояснення дивись в пункті "можливі проблеми")
- Статус прочитки повідомлень не змінюється, в тому числі і для згораємих фото/відео

Можливі проблеми:
- Група медіа пересилається по одному файлу, але вона є одним повідомленням - Так це така фіча чомусь бібліотека Pyrogram баче їх як окремі повідомлення, і з цим є проблеми по флуду, ще не вирішив її тому в консоль буде кидати повідомлення про повторнц спробу надсилання через 2 секунди.
- Якщо поступає група пересланих повідомлень вони пересилаються по одному та з затримкою - Так, це кожне окреме повідомлення, тому ситуація така сама як з групованими медіа вище.
- Про статус онлайн і зайві сповіщення - Пересилання повідомлень реалізоване через відкладені повідомлення з таймером в одну хвилину (можна налаштувати в файлі "user_processor.py" -> class UserMessages -> forward_processor -> date -> minutes=1). Це пов'язане з тим, що при прямій пересилці в тебе активується статус "онлайн". Це не моя забаганка, так реалізований механізм самого Телеграм. Також, хоча відкладені повідомлення публікуються зі статусом "не сповіщати" тобі приходитимуть сповіщення. Частково це лікується вимкненням сповіщеннів від каналу. Чому частково? На телефоні (принаймні з ОС Андроїд) після цього сповіщення перестають йти, але в телеграм клієнті для ПК спливаючі сповіщення лишаться, бо так влаштований телеграм клієнт.
- Користувач відредагував повідомлення, а в пересланих воно не змінилося  - Звісно, так працюють переслан повідомлення, спробуй сам  переслати своє повідомлення а потім відредагувати його і порівняти. Тимпаче бот пересилає їх одразу коли вони приходять  (можливо вийняток групи медіа та групи пересланих повідомлень).

EN
Userbot (the one that is authorized as an application to your Telegram account, not to be confused with a regular bot in Telegram) for automatic forwarding of personal messages from users
Based on the Pyrogram library

Prehistory:
I was fed up with my contacts who write and delete messages before I read them, so I created a bot that will automatically forward messages from the necessary users to a separate channel, where I can read them in peace if they are deleted.

Warning!
You use it at your own peril and risk, I bear no responsibility and do not accept claims for any possible consequences when using this bot (such as a possible ban of your Telegram account)! By using this bot, you confirm that you know what you are doing and the consequences it can lead to!

How to get started:
Download the bot
In the "tg_config.py" file, replace all data with your own
If you need to change data in the bot from another account, edit the "admin_id" variable in the "bot_processor.py" file to your id of the second Telegram account
Run the bot via the "main.py" file
At the first launch, log in to your Telegram account
After authorization, go to Telegram settings, select the session from which you entered Telegram and turn off the ability to receive calls and secret chats for this session

Implemented features:
- Control panel via Telegram bot
- Navigate through bot buttons without using commands other than /start
- Saving and loading settings to the SQLite database
- Add/remove a user to a shipment
- The ability to freeze/unfreeze the shipment of an individual user independently of others
- Ability to start/stop forwarding of all users (globally, freezing/unfreezing of forwarding separately by user remains unchanged)
- Ability to disable/enable forwarding of your messages in chat with added users
- Displaying a list of all added shipments for each user with their activity statuses
- Forwarding messages from users to your private channel
- Add to shipment through:
- - Sending a user's contact from their Telegram profile
- - Select an existing chat with the user
- - Selecting a synchronized user contact in Telegram
- - Adding through a user's forwarded message, if he does not have an active item in his privacy settings to hide the link to his account when forwarding a message
- When adding to the shipment, it is possible to:
- - Automatically create a new channel (a private channel is created)
- - Choose an existing one (private channel, the creator of which you are)
- The ability to change the channel to which messages are forwarded (the same choice that is provided when adding a user to forwarding)
- Deleting a user from forwarding (the channel where messages were forwarded is saved)
- Full wipe of message forwarding settings with their channels (irreversible action)
- Forwarding types of messages:
- - Text
- - Photos (including burnt ones)
- - Videos (including burned ones)
- - Video message (those circles :))
- - Voice messages
- - Messages from channels
- - Forwarded messages from other users
- - Stickers
- - Gifs
- - Files
- - Media group (there is a nuance, look in possible problems)
- The online status does not change (invisible, see the explanation in the "possible problems" section)
- The status of reading messages does not change, including for burning photos/videos

Possible problems:
- A group of media is forwarded in one file, but it is one message - Yes, this is such a feature, for some reason the Pyrogram library sees them as separate messages, and there are problems with this due to flooding, I have not solved it yet, so the console will throw a message about repeated attempts to send via 2 seconds.
- If a group of forwarded messages arrives, they are forwarded one at a time and with a delay - Yes, this is each individual message, so the situation is the same as with grouped media above.
- About online status and redundant notifications - Forwarding of messages is implemented through delayed messages with a timer of one minute (can be configured in the file "user_processor.py" -> class UserMessages -> forward_processor -> date -> minutes=1). This is due to the fact that the "online" status is activated for you during a direct transfer. This is not my whim, this is the implemented mechanism of Telegram itself. Also, although snoozed messages are published with a "do not notify" status, you will receive notifications. This is partially remedied by turning off notifications from the channel. Why partially? On the phone (at least with the Android OS), notifications stop going after this, but pop-up notifications remain in the Telegram client for PC, because this is how the Telegram client is arranged.
- The user edited the message, but it has not changed in forwarded messages - Of course, this is how forwarded messages work, try to forward your message yourself and then edit it and compare. Instead, the bot forwards them as soon as they arrive (with the possible exception of the media group and forwarded message group).

RU
Юзербот (тот который авторизуется как приложение в вашем Телеграмм аккаунт, не путать с обычным ботом в Телеграмм) для автоматических пересылок личных сообщений от пользователей
Базируется на библиотеке "Pyrogram"

Предыстория:
Меня задолбали мои контакты, которые пишут и удаляют сообщения до того, как я их прочитал, поэтому я создал бота, который будет автоматически пересылать сообщения от необходимых пользователей в отдельный канал, где я в случае удаления смогу их спокойно прочитать.

Предупреждение!
Вы используете его на свой страх и риск, я не несу никакой ответственности и не принимаю претензии за какие-либо возможные последствия при использовании этого бота (как вот возможен бан вашего аккаунта в телеграммах)! Используя этот бот вы подтверждаете то, что вы знаете что делаете и к каким последствиям это может привести!

Как начать:
Загрузи бота
В файле "tg_config.py" замени все данные своими
При необходимости изменять данные в боте с другого аккаунта отредактировать в файле "bot_processor.py" переменную "admin_id" на свой id второго Телеграмм аккаунта
Запусти бота через файл "main.py"
При первом запуске авторизуйся в свой телеграмм аккаунт
После авторизации зайди в настройку телеграмм, выбери сессию из которой ты зашел в телеграмм и выключи возможность для этой сессии получать звонки и секретные чаты

Фичи, которые реализованы:
- панель управления через телеграмм бота
- Навигация через кнопки бота не используя команды, кроме как /start
- Сохранение и загрузка настроек в базу данных SQLite
- Добавление/удаление пользователя в пересылку
- возможность заморозить/разморозить пересылку отдельного пользователя независимо от других
- Возможность запустить/остановить пересылку всех пользователей (глобально, заморозка/разморозка пересылки отдельно по пользователю остаются неизменными)
- Возможность отключить/включить пересылку сообщений в чате с добавленными пользователями
- вывод списка всех добавленных пересылок по каждому пользователю с их статусами активности
- Пересылка сообщений от пользователей в свой приватный канал
- добавление в пересылку через:
- - Отправка контакта пользователя из его профиля Телеграмм
- - Выбор имеющегося чата с пользователем
- - Выбор синхронизированного контакта пользователя в телеграммах
- - Добавление через пересланное сообщение пользователя, если у него в настройках конфиденциальности не активный пункт скрытия ссылки на его аккаунт при пересылке сообщения
- при добавлении в пересылку есть возможность:
- - автоматически создать новый канал (создается частный канал)
- - Выбрать уже имеющийся (частный канал, создателем которого являешься ты)
- возможность изменить канал куда пересылаются сообщения (тот же выбор, который предоставляется при добавлении пользователя в пересылку)
- удаление пользователя с пересылки (канал куда пересылаемые сообщения сохраняется)
- Полный вайп настроек пересылки сообщений с их каналами (необратимое действие)
- Пересылка типов сообщений:
- - Текст
- - Фото (в том числе сгораемые)
- - Видео (в том числе сгораемые)
- - Видео сообщения (те кружочки :))
- - Голосовые сообщения
- - Сообщения по каналам
- - Пересланные сообщения от других пользователей
- - Стикеры
- - Гифки
- - Файлы
- - Группа медиа (есть нюанс, смотри в возможных проблемах)
- Статус онлайн не меняется (невидимка, пояснения смотри в пункте "возможные проблемы")
- Статус прочтения сообщений не меняется, в том числе и для сгораемых фото/видео

Возможные проблемы:
- Группа медиа пересылается по одному файлу, но она является одним сообщением - Так это такая фича почему-то библиотека Pyrogram видит их как отдельные сообщения, и с этим есть проблемы по флуду, еще не решил ее поэтому в консоль будет бросать сообщение о повторной попытке отправки через 2 секунды.
- Если поступает группа пересланных сообщений они пересылаются по одному и с задержкой. - Да, это каждое отдельное сообщение, поэтому ситуация такая же как с группированными медиа выше.
- О статусе онлайн и лишних оповещениях - Пересылка сообщений реализована через отложенные сообщения с таймером в одну минуту (можно настроить в файле "user_processor.py" -> class UserMessages -> forward_processor -> date -> minutes=1). Это связано с тем, что при прямой пересылке у тебя активируется статус "онлайн". Это не моя прихоть, так реализован механизм самого телеграммы. Также, хотя отложенные сообщения публикуются со статусом "не оповещать" тебе будут приходить уведомления. Частично это лечится отключением извещений от канала. Почему отчасти? На телефоне (по крайней мере с ОС Андроид) после этого уведомления перестают идти, но в телеграммах клиенты для ПК всплывающие уведомления останутся, так устроен телеграмм клиент.
– Пользователь отредактировал сообщение, а у пересланных оно не изменилось – Конечно, так работают пересланное сообщение, попробуй сам переслать свое сообщение а затем отредактировать его и сравнить. Тем более бот пересылает их сразу когда они приходят (возможно исключение группы медиа и группы пересланных сообщений).
