import os
from pathlib import Path
from flask import request
from .channel_client import ChannelClient


def register_channel(app, service):
    config=Path(os.environ.get('CHANNEL_CONFIG_FILE') or Path(__file__).resolve().parents[1]/'.local/web/channel.json')
    def client():return ChannelClient(config)
    def submit():
        data=request.json;aid=str(data.get('account_id',''));uid=str(data.get('uid',''))
        account=service.accounts.get(aid)
        snapshot=service.conversation.list(uid,{'account_id':aid,'limit':20})
        context={'peer_id':uid,'messages':[{k:m.get(k) for k in ('record_id','message_id','text','message','direction','message_type','attempted_at')} for m in snapshot['items']]}
        text=data.get('text','根据最近对话起草简短自然的中文回复。')
        message_id=data.get('message_id')
        if not isinstance(text,str) or len(text)>4000:raise ValueError('处理要求最多 4000 字')
        if not isinstance(message_id,str) or not 8<=len(message_id)<=160:raise ValueError('请提供唯一消息 ID')
        return client().send(str(account.get('uid') or aid),message_id,text,category='reply_draft',conversation_id=uid,context=context,surface='dm',event_type='dm.draft_requested'),202
    def status(event_id):
        account=service.accounts.get(str(request.args.get('account_id','')))
        return client().status(event_id,str(account.get('uid') or account['id']))
    app.add_url_rule('/api/channel/messages','channel_submit',submit,methods=['POST'])
    app.add_url_rule('/api/channel/messages/<event_id>','channel_status',status)
