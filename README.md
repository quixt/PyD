# PyD
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

# Slash commands (Not fully ready)

```py
@c.command()
async def hello(ctx):
  await ctx.send('Hello there!')
  await asyncio.sleep(2)
  message = await ctx.send('How are you doing today?')
  await asyncio.sleep(1)
  await message.edit('I am doing well')
  
@c.guild_command(guilds = [<ids>])
async def test():
  await ctx.send('This is a guild command.')
```
## Notes about Slash commands:
A send coroutine must be run in the first 3 seconds after the command is called or it will not work.
To wait more than three seconds before sending a message, use `await ctx.wait()`.

The first `send` coroutine run is the initial message that lets Discord know you've recieved the command, editing and deleting is different.
for the first message, do not asign the `send` to a variable (no `m = await ctx.send()`).
Only use await `ctx.send()`. To edit the initial message use `ctx.edit()` instead of `m.edit()`, and for deleting `ctx.delete()` instead of `m.delete()`.

Options (Arguments) are currently in the works.

## Installation

There is no `pip install` or any method of installation. You need to manually download the files and use them. Sorry :(.
