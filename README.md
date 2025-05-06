# anilist_ntfy
Simple python script to read [Anilist.co]([url](https://anilist.co/)) notifications and push them to own [ntfy]([url](https://github.com/binwiederhier/ntfy)) instance.

## Prerequisites
- you must have an Anilist account
- you must have a Ntfy instance to use - I have setup a local one using docker
- a topic in ntfy
- the ntfy app on your phone, if you wish

## Installation
You may simply download the `anilist_ntfy.py` script somewhere in your path such as `$HOME/.local/bin/`:
```sh
wget https://raw.githubusercontent.com/Rareshp/anilist_ntfy/refs/heads/main/anilist_ntfy.py -O $HOME/.local/bin/anilist_ntfy.py
```

Furthermore you will find the `anilist_ntfy.conf` file as well, to be placed in `$HOME/.config/` which you will have to edit as per the instructions below.
```sh
wget https://raw.githubusercontent.com/Rareshp/anilist_ntfy/refs/heads/main/anilist_ntfy.conf -O $HOME/.config/anilist_ntfy.conf
```

## Conf file
The one item you need to modify that needs instructions is the "token". To obtain the token follow these steps:
1. go [anilist > settings > developer](https://anilist.co/settings/developer) and click the "Create New Client" button. Name it "ntfy" and the "Redirection URL" needs to be `https://anilist.co/api/v2/oauth/pin`
2. now that the app is created it will appear in the list, and you will some new fields (if not click the app). Copy your ID. For example: 12345
3. navigate to a URL like this one, with your ID: `https://anilist.co/api/v2/oauth/authorize?client_id=12345&response_type=token` and authorize the app
4. you will see a new page for "Authorization Request" - click the authorize button
5. copy your token, then paste as is into the `anilist_ntfy.conf` file - DO NOT add quotes. Make sure is one line.

You can reveke access at any time from the developer page.

## Cron job
If you run `crontab -e` you may add a line such as this one to run the script automatically every 20 minutes. Keep in mind that your conf file interval should be longer.
```
*/20 * * * * /usr/bin/python3 /home/username/.local/bin/anilist_ntfy.py
```
