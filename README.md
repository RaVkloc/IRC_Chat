# IRC_Chat
Application is implementation of our own IRC chat protocol. Application is divided into two main parts server an client. It works in local network or can be deployed to external server.
Communication between client and server is encrypted. All important events are stored as logs.


## Requirements
- Python>=3.8
- mysql-connector==2.2.9
- PyQt5==5.15.0
- PyQt5-sip==12.8.0
- PyQt5-stubs==5.14.2.2

`pip install -r requirements.txt`


## Server
Based on multi-theading architecture so it can serve many users at the same time.
Support for Internet Protocol version 4 and 6. Using MySQL databse.
Database keeps:
- users data (id, username, hashed password, token, current room)
- room data (id, name, owner) 


## Client
Structure of client core is independent from a way of displaying communication. 
There a two default clients available at this moment:
- terminal,
- Qt based desktop.

You can easily add a new by creating a new class inherited by "client" and customize.

## HOW TO START
`git clone https://github.com/RaVkloc/IRC_Chat.git`

#### Editable params
You can set your own client/server values or use defaults:
- IPv4/IPv6,
- port,
- certificates
- pair of key

Params can be changed in `settings.py` files.

#### Run
1. cd IRC_Chat
2. export PYTHONPATH=.../IRC_Chat
3. python3.8 xserver/coreserver/server_core.py
4. Client:
   - Desktop: python3.8  xclient_gui/desktop/main.py 
   - Terminal: python3.8 xclient/client/main.py
 
 
 For more information look at [Wiki](https://github.com/RaVkloc/IRC_Chat/wiki).
