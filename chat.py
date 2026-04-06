from flask import Blueprint, render_template, request, jsonify, Response, stream_with_context
from flask_login import login_required, current_user
from extensions import db
from models.models import Conversation, Message
from openai import AzureOpenAI
import os
import json

chat_bp = Blueprint('chat', __name__)

# Initialize Azure OpenAI Client
azure_deployment = os.environ.get('AZURE_CHAT_DEPLOYMENT_NAME', 'gpt-4-turbo')
client = AzureOpenAI(
    api_key=os.environ.get('AZURE_OPENAI_API_KEY', ''),
    api_version=os.environ.get('AZURE_API_VERSION', '2024-02-15-preview'),
    azure_endpoint=os.environ.get('AZURE_END_POINT', '')
)

@chat_bp.route('/chat')
@login_required
def chat_page():
    conversations = Conversation.query.filter_by(user_id=current_user.id)\
        .order_by(Conversation.updated_at.desc()).limit(50).all()
    return render_template('chat.html', conversations=conversations)

@chat_bp.route('/chat/new', methods=['POST'])
@login_required
def new_conversation():
    conv = Conversation(user_id=current_user.id, title='New Chat')
    db.session.add(conv)
    db.session.commit()
    return jsonify({'id': conv.id, 'title': conv.title})

@chat_bp.route('/chat/<int:conv_id>/messages')
@login_required
def get_messages(conv_id):
    conv = Conversation.query.filter_by(id=conv_id, user_id=current_user.id).first_or_404()
    msgs = [{'role': m.role, 'content': m.content, 'file_type': m.file_type,
             'file_name': m.file_name, 'timestamp': m.timestamp.isoformat()}
            for m in conv.messages]
    return jsonify({'messages': msgs, 'title': conv.title})

@chat_bp.route('/chat/<int:conv_id>/send', methods=['POST'])
@login_required
def send_message(conv_id):
    conv = Conversation.query.filter_by(id=conv_id, user_id=current_user.id).first_or_404()
    data = request.get_json()
    user_text = data.get('message', '')
    file_context = data.get('file_context', '')
    file_type = data.get('file_type', '')
    file_name = data.get('file_name', '')

    full_content = user_text
    if file_context:
        full_content = f"[Attached {file_type}: {file_name}]\n\n{file_context}\n\nUser: {user_text}"

    user_msg = Message(role='user', content=user_text, file_type=file_type or None,
                       file_name=file_name or None, conversation_id=conv_id)
    db.session.add(user_msg)

    if conv.title == 'New Chat' and user_text:
        conv.title = user_text[:60] + ('...' if len(user_text) > 60 else '')

    history = [{"role": "system", "content": "You are Nexus, an advanced AI research assistant. You help with research, analysis, summarisation, and answering questions. You can process PDFs, images, audio transcripts, and video content. Be helpful, precise, and insightful."}]
    for m in conv.messages[:-1]:
        history.append({'role': m.role, 'content': m.content})
    history.append({'role': 'user', 'content': full_content})

    db.session.commit()

    def generate():
        full_response = ''
        try:
            response = client.chat.completions.create(
                model=azure_deployment,
                messages=history,
                stream=True
            )
            for chunk in response:
                if chunk.choices and chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    full_response += text
                    yield f"data: {json.dumps({'token': text})}\n\n"
        except Exception as e:
            err = str(e)
            if 'api_key' in err.lower() or 'authentication' in err.lower() or '401' in err or 'quota' in err.lower():
                mock = f"I'm Nexus, your AI research assistant! To get real responses, ensure your AZURE_OPENAI_API_KEY and endpoint are correctly set. Request error: {err[:150]}"
            else:
                mock = f"Azure response error: {err[:200]}"
            for word in mock.split():
                full_response += word + ' '
                yield f"data: {json.dumps({'token': word + ' '})}\n\n"

        ai_msg = Message(role='assistant', content=full_response.strip(), conversation_id=conv_id)
        db.session.add(ai_msg)
        db.session.commit()
        yield f"data: {json.dumps({'done': True, 'title': conv.title})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream',
                    headers={'X-Accel-Buffering': 'no', 'Cache-Control': 'no-cache'})

@chat_bp.route('/chat/<int:conv_id>/delete', methods=['DELETE'])
@login_required
def delete_conversation(conv_id):
    conv = Conversation.query.filter_by(id=conv_id, user_id=current_user.id).first_or_404()
    db.session.delete(conv)
    db.session.commit()
    return jsonify({'success': True})


