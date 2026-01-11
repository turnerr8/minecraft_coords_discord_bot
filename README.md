# Minecraft Coordinate Saver Discord Bot
This is a bot built using discord.py and sqlite to save and find important coordinates for a minecraft world



## Installation

### Bot Creation
Create a bot [here](https://discord.com/developers/applications?new_application=true) and make sure to regenerate and copy the token

### Server-End
1. Clone git repository
2. Create a `.env` file containing the following info:
``` 
.env

TOKEN= [YOUR BOT TOKEN]
SERVER_ID = [ID TO DESIRED SERVER THE BOT RUNS ON]
 ```

`SERVER_ID` can be accessed by right clicking on your server profile when developer mode is on.
3. Create a `data` directory in the root directory of the project

4. create a `docker-compose.yml` file with the following contents
```
services:
  bot:
    build: .
    container_name: discord-bot
    env_file:
      - .env
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

5. run docker image!