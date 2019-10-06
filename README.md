# Server Monitoring Bot
## Installation
1. Make sure to install python3
2. Install psutil and telepot library using pip.
    ```
    pip3 install telepot
    pip3 install psutil
    ```
## Command
* Commands
  * `/status` - give information about memory, cpu usage, etc.
  * `/shell`  - goes into shell executing mode and send you the output
  * `/changedir` - goes into change directory mode and change current directory

## Usage
* Telegram bot key and tokens.pys
  * Create a bot and get a key from [BotFather](https://telegram.me/BotFather)
  * In tokens.py file. Add your key into telegrambot variable
    `telegrambot = 'this is your key'`
  * In tokens.py file. Add your telegram chat id into the adminchatid variable. You can add chat id more than one user.
    `adminchatid = [7213123,1231231]`
  * Run the bot using python3 
    `python3 main.py`
  


