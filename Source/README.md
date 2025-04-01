# The folder contains files necessary for the telegram bot to work.
### 1. main.py
   The file contains the main code necessary for telegram bot operation. Asynchronous methods are used in the code to ensure smooth operation of the bot, even under heavy load. The Aiogram module is used to send messages. Also, pandas and time libraries are used in the code.
### 2. email_sender.py
   The file contains additional code necessary for sending complaints and suggestions via telegram bot to the company mail. The code implements methods for sending emails using smtplib module.
### 3. dbw.py
   The file contains additional code necessary to work with the telegram bot's user database. Asynchronous methods are used in the code, for smooth operation of the bot, even under heavy load, with the help of asyncio module. The datetime and aiosqlite modules are used for correct work with the database.
