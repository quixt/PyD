# Dispy
Discord API Wrapper written in python

# Client connection to Gateway
```py
c = client.Client()

c.run('<token here>')
```

# Ready event

```py
@c.event
async def ready():
  print('bot online')
```

# Slash commands (Not ready)

```py
@c.command()
async def help():
  pass
  
@c.guild_command(guilds = [<ids>])
async def test():
  pass
```
