from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, base64

upload_bp = Blueprint('upload', __name__)
ALLOWED = {
    'pdf': {'application/pdf'},
    'image': {'image/jpeg', 'image/png', 'image/gif', 'image/webp'},
    'audio': {'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4'},
    'video': {'video/mp4', 'video/webm', 'video/ogg'}
}

def get_file_type(mime):
    for ftype, mimes in ALLOWED.items():
        if mime in mimes:
            return ftype
    return None

@upload_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    f = request.files['file']
    if not f.filename:
        return jsonify({'error': 'Empty filename'}), 400

    mime = f.mimetype
    ftype = get_file_type(mime)
    if not ftype:
        return jsonify({'error': 'File type not supported'}), 400

    if not current_user.is_pro and ftype in ('audio', 'video'):
        return jsonify({'error': 'Audio/Video upload requires Pro plan', 'upgrade': True}), 403

    fname = secure_filename(f.filename)
    folder = os.path.join('uploads', ftype + 's')
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{current_user.id}_{fname}")
    f.save(path)

    context = extract_context(path, ftype, fname)
    return jsonify({'success': True, 'file_type': ftype, 'file_name': fname, 'context': context})

def extract_context(path, ftype, fname):
    if ftype == 'pdf':
        try:
            import PyPDF2
            with open(path, 'rb') as pf:
                reader = PyPDF2.PdfReader(pf)
                text = ''
                for i, page in enumerate(reader.pages[:10]):
                    text += page.extract_text() or ''
                    if len(text) > 8000:
                        break
            return f"PDF Content ({len(reader.pages)} pages):\n{text[:8000]}"
        except Exception as e:
            return f"PDF file attached: {fname}. (Could not extract text: {e})"
    elif ftype == 'image':
        try:
            with open(path, 'rb') as img:
                b64 = base64.b64encode(img.read()).decode()
            return f"[IMAGE_B64:{b64[:100]}...]"
        except:
            return f"Image attached: {fname}"
    elif ftype == 'audio':
        return f"Audio file attached: {fname}. Please analyse and summarise this audio content."
    elif ftype == 'video':
        return f"Video file attached: {fname}. Please analyse and summarise this video content."
    return f"File attached: {fname}"
