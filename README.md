# discord_message_deleter
A fast and sequential message-deleter without using search functionality

> [!WARNING]
> Using your account during the script's operation will lead to stricter rate-limits and degraded experience for both you and the script.

> [!CAUTION]
> I'm not responsible for any risks that come with using this. Make sure you have a phone attached to your account to reduce risks.

# Introduction 

## Why not use [Undiscord](github.com/victornpb/undiscord)?
Undiscord (*or formerly deleteDiscordMessages.js as I knew it*) was a fast and convenient script back in the day.
Nowadays, it is extremely janky, slow, and gets rate-limited to oblivion, likely due to the fact that it appears to be using search functionality.

## How is this better?
This project does not use search functionality. It simply iterates message history, which is very light on rate-limits.

## How is this worse?
Iterating over channel history/messages is a linear operation and works best only in direct messages, where there's always 2 recipients talking.
This is completely unsuitable for mixed-author channels, such as guild channels. Furthermore, you do not get an estimate of how many messages will be purged in total.

### Worst-case scenario example
Assume you have sent only 1 message, somewhere in the middle of a channel, in a server with thousands of members that speak daily.
The script would have to fetch and process every single message, up until the beginning of the channel. Now is a good time to read about O(N).

# Usage
## Install dependencies
Assuming you have downloaded the files and have pip, run:
```sh
pip install -r requirements.txt
```
## Now run main.py
```sh
python ./main.py
```

You will be asked to enter a token, then select a channel ID from the list given. 

> [!NOTE]
> The script randomly introduces a small jitter to the base delay to appear more "human"

### [Not sure how to get your token? Click here](https://gist.github.com/MarvNC/e601f3603df22f36ebd3102c501116c6)
