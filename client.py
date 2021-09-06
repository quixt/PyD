import guild, presences
import asyncio
import aiohttp
import threading
import time
import random, json, sys
import functools, types, requests
from presences import Activities, Status
import time, user
from typing import Coroutine, Optional
import commands, errors
class Client:
    def __init__(self,*,intents:int = None):
        if intents == None:
            self.intents = 3072
        else:
            self.intents = intents
        self.ws = None
        self.loop = asyncio.get_event_loop()
        self.last_sequence = None
        self._command_jsons = {}
    def run(self, token):

        async def establish_connection(self):
            self.token = token
            gateway_url = "wss://gateway.discord.gg/?v=8&encoding=json"
            self.session = aiohttp.ClientSession()
            self.ws = await self.session.ws_connect(gateway_url)
            #self.ws.receive
            op10 = await self.ws.receive_json()
            heartbeat = int(op10["d"]["heartbeat_interval"])

            
            async def heartbeat_connection(self):
                heartbeat_json = {"op":1,
                                  "d":str(self.last_sequence) if self.last_sequence is not None else self.last_sequence
                                }
                while True:
                    await asyncio.sleep(heartbeat/1000 )
                    await self.ws.send_json(heartbeat_json)
            
            self.loop.create_task(heartbeat_connection(self))
            await GatewayConnection.identify(self.ws, token, self.intents)
            ready_event = await self.ws.receive_json()
            try:
                ready = getattr(self,'ready')
                await ready()
            except AttributeError:
                pass
            self.last_sequence = ready_event['s']
            self.id = ready_event['d']['user']['id']
            self.api_endpoint = f'https://discord.com/api/v8/applications/{self.id}'
            self.global_commands_url = f'{self.api_endpoint}/commands'
            self.headers = {'Authorization':f'Bot {self.token}'}

            await self.http_commands()
            await self._create_task()
        self.loop.create_task(establish_connection(self))
        self.loop.run_forever()
    def create_command(self, func, name, desc, args):
        json = {
            "name":name,
            "type":1,
            "description":desc,
            "options":args
        }
        self._command_jsons[name] = {'json':json,'func':func}
    def create_guild_command(self, func, name, desc, args, guilds : list):
        json = {
            "guilds":guilds,
            "name":name,
            "type":1,
            "description":desc,
            "options":args
        }
        self._command_jsons[name] = {'json':json,'func':func}
    def command(self,*,description=''):
        def inner(func):
            arg_list = list(func.__code__.co_varnames)
            args = [{"name":arg,"required":True} for arg in arg_list[1:len(arg_list)-1]]
            self.create_command(func, func.__name__, description, args)
            return func 
        return inner    
    def guild_command(self,*,description = "",guilds:list):
        def inner(func):
            arg_list = list(func.__code__.co_varnames)
            args = [{"name":arg,"required":True} for arg in arg_list[1:len(arg_list)-1]]
            self.create_guild_command(func, func.__name__, description, args, guilds)
            return func 
        return inner
    async def change_presence(self,*,activity:Activities,status:Optional[Status]):
        if status == None:
            strstatus = "online"
        else:
            strstatus = status.st
        json = {
            "op":3,
            "d":{
                "since":time.time(),
                "activities":[
                    {
                        "name":activity.name,
                        "type":activity.type
                    }
                ],
                "status":strstatus,
                "afk":False
            }
        }
        j = await self.ws.send_json(json)
    async def http_commands(self):
        command_jsons = self._command_jsons
      

        for key in command_jsons.keys():
            json = command_jsons[key]['json']
            if 'guilds' in json:
                guilds = json['guilds']
                del json['guilds']
                for i in guilds:
                    url = f'https://discord.com/api/v8/applications/{self.id}/guilds/{i}/commands'

                    code = await self.session.post(url, json=json, headers = self.headers)
                if code.status == 403:
                    raise("403 Forbidden")
            else:
                code = await self.session.post(f'{self.global_commands_url}',json=json, headers=self.headers)

                if code.status == 403:
                    raise('403 Forbidden')
            await asyncio.sleep(2)
    def event(self, coro:Coroutine):
        setattr(self, coro.__name__, coro)
    async def close(self):
        await self.ws.close(code=1000)
    async def get_commands(self):
        r = await self.session.get(f'https://discord.com/api/v8/applications/{self.id}/commands', headers={'Authorization':f'Bot {self.token}'})
        data = await r.json()
        cm = []
        for i in range(0,len(data)):
            c = commands.ApplicationCommand(data[i])
            cm.append(c)
        return cm
    async def _get_commands_clientusage(self):
        r = await self.session.get(f'https://discord.com/api/v8/applications/{self.id}/commands', headers={'Authorization':f'Bot {self.token}'})
        data = await r.json()
    async def _websocket_listener(self):
        while True:
            d = await self.ws.receive_json()
            if d['op'] != 11: self.last_sequence = d['s']
            if d['t'] == 'INTERACTION_CREATE':
                #print(d['d'])
                await self._interaction_handler(d['d'])
    async def _create_task(self):
        task = self.loop.create_task(self._websocket_listener())

    

    async def _interaction_handler(self, data):
        try:
            command = self._command_jsons[data['data']['name']]
        except:
            raise errors.UnknownApplicationCommand
        ctx = commands.Context(user.Member(data['member']),data['token'],data['id'],self.session, self.headers, self.id)
        await command['func'](ctx)
class GatewayConnection:
    async def identify(ws, token, intents):
        op2 = {
                    "op": 2,
                    "d": {
                    "token": f"{token}",
                    "intents": intents,
                    "properties": {
                        "$os": f"{sys.platform}",
                        "$browser": "discpy",
                        "$device": "discpy"
                    },
                    "presence": {
                        "activities":[{
                        "name":"Fortnite",
                        "type":0
                        }],
                        "status":"dnd"
                    }
                    },
                    "s":None,
                    "t":None
                }
        await ws.send_json(op2)

        
        
            

