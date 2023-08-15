# Discord Bot - Email Bomber
The Discord Mail Bomber is a bot that allows users to initiate a simulated email bombing attack on targeted emails. It is coded in Python using the Discord.py library. The bot provides several commands to interact with its functionalities. The !bomb command allows users to start the bombing process by providing an email address as the target. The bot will send POST requests to a list of pre-configured websites, simulating the creation of customer accounts using the provided email address. The !stop command can be used to terminate the ongoing bombing process if needed. The !bothelp command displays a help message with information about the available commands. The !commands command lists all the commands supported by the bot. The !status command provides information about the current status of the bombing process, including the number of domains being targeted. Please note that this program is for educational purposes only and should not be used to engage in any malicious activities. It serves as a demonstration of how such attacks can occur and the potential impact they can have on websites. If you have any further questions or need assistance with the program, feel free to ask!

# Installation

1. `pip install discord`
2. `pip install requests`

3. Put the allowed channel id on line 16

# Files

1. `Main.py` - Main script file
2. `Blacklist.txt` - Blacklisted emails
3. `Token.txt` - Put your token in this file
4. `urls.txt` - DO NOT CHANGE
