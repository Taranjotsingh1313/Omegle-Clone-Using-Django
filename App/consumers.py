from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
    
    async def receive_json(self, content):
        data = content
        if data['command'] == 'join_group':
            await self.channel_layer.group_add(
                data['groupname'],
                self.channel_name
            )
            print(f"user added :- {data['groupname']}")
        elif data['command'] == 'send':
                await self.channel_layer.group_send(
                    data['groupname'],
                    {
                        'type':'chat.message', # this should be a function and . means _
                        'message':data['message'],
                        'command':'message'
                    }
                )
        elif(content['command'] == 'join'):
            await self.channel_layer.group_send( data['groupname'],{
                'type':'join.message',
            })
            
        elif(content['command'] == 'offer'):
            await self.channel_layer.group_send( data['groupname'],{
                'type':'offer.message',
                'offer':content['offer']
            })
        elif(content['command'] == 'answer'):
            await self.channel_layer.group_send(data['groupname'],{
                'type':'answer.message',
                'answer':content['answer']
            })
        elif(content['command'] == 'candidate'):
            await self.channel_layer.group_send(data['groupname'],{
                'type':'candidate.message',
                'candidate':content['candidate'],
                'iscreated':content['iscreated']
            })
    async def join_message(self,event):
        await self.send_json({
            'command':'join'
        })
    
    async def offer_message(self,event):
        await self.send_json({
            'command':'offer',
            'offer':event['offer']
        })
    
    async def answer_message(self,event):
        await self.send_json({
            'command':'answer',
            'answer':event['answer']
        })
    
    async def candidate_message(self,event):
        await self.send_json({
            'command':'candidate',
            'candidate':event['candidate'],
            'iscreated':event['iscreated']
        })
        
    async def chat_message(self,event):
        await self.send_json({
            'message':event['message'],
                'command':'message'
            })

          