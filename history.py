from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from models.models import Conversation

history_bp = Blueprint('history', __name__)

@history_bp.route('/history')
@login_required
def get_history():
    convs = Conversation.query.filter_by(user_id=current_user.id)\
        .order_by(Conversation.updated_at.desc()).all()
    return jsonify([{
        'id': c.id, 'title': c.title,
        'updated_at': c.updated_at.isoformat(),
        'message_count': len(c.messages)
    } for c in convs])
