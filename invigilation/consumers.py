# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Conflict

class ConflictConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("conflicts", self.channel_name)
        
        # إرسال عدد التعارضات غير المحلولة عند الاتصال
        unresolved_count = await sync_to_async(Conflict.objects.filter(resolved=False).count)()
        await self.send(text_data=json.dumps({
            'type': 'initial_count',
            'count': unresolved_count
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("conflicts", self.channel_name)

    async def receive(self, text_data):
        pass

    async def conflict_alert(self, event):
        # إرسال تنبيه عن تعارض جديد
        await self.send(text_data=json.dumps({
            'type': 'new_conflict',
            'message': event['message'],
            'conflict_id': event['conflict_id'],
            'conflict_type': event['conflict_type']
        }))

    async def conflict_resolved(self, event):
        # إرسال تنبيه عن تعارض تم حله
        await self.send(text_data=json.dumps({
            'type': 'conflict_resolved',
            'message': event['message'],
            'conflict_id': event['conflict_id']
        }))