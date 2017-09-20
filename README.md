# DiscordBot

## Core
Initialises the bot and runs the client. Registers the other modules.

## Modules
### Admin
Contains commands meant to be used only by the bot Admin

#### Commands
* ```kill```
* ```restart```
* ```exec```
* ```eval```
* ```refresh```
* ```auth```
* ```auth_remove```
* ```sleep``` (WIP)

### Command
Creates, registers, and executes commands.

### Chat
Functions related to the bot's chatting capabilities.

Trains a hidden Markov model on chat messages tagged by the NLTK perceptron tagger. After a while it will start to generate new sentences based on fragments of the chat history.

Some results after being trained on over 10,000 words:

"Pardon me, but why is Lieutenant Barclay being referred to clandestinely as a form of transport.. for their heads."    
"Police and rioters come together to help a fat cow and hang up."    
"I don't know how to reload"    
"Dood, you were watching me when I was a broken jpeg."

#### Commands
* ```hello```
* ```say```
* ```quote```

### Util
Utility functions for other modules as well as chat.

#### Wrapper Functions
* ```sendMessage(discord.Message, content)```
* ```editMessage(discord.Message)```
* ```deleteMessage(discord.Message)```

#### Commands
* ```help```
* ```whoami```

### Crawler
Work in progress

APIs and packages used:

NLTK Package: https://github.com/nltk/nltk    
Markovify Package: https://github.com/jsvine/markovify    
Discord API Wrapper for Python: https://github.com/Rapptz/discord.py    
