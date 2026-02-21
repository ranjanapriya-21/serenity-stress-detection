import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from emotion_detection import detect_emotion_and_respond
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# -------------------------------------------------------------------
# Database Models
# -------------------------------------------------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    conversations = db.relationship('Conversation', backref='user', lazy=True)
    journal_entries = db.relationship('Journal', backref='user', lazy=True)
    favorite_tips = db.relationship('FavoriteTip', backref='user', lazy=True)

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_message = db.Column(db.Text, nullable=False)
    bot_response = db.Column(db.Text, nullable=False)
    detected_emotion = db.Column(db.String(100))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Journal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FavoriteTip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tip_text = db.Column(db.Text, nullable=False)
    emotion = db.Column(db.String(100))
    saved_from = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------------------------------------------------
# User Loader for Flask-Login
# -------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------------------------------------------------------------
# Context Processor for Template Filters
# -------------------------------------------------------------------

@app.context_processor
def utility_processor():
    def get_most_common_emotion(conversations):
        if not conversations:
            return "N/A"
        
        emotion_counts = {}
        for conv in conversations:
            emotion = conv.detected_emotion
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if emotion_counts:
            return max(emotion_counts, key=emotion_counts.get)
        return "N/A"
    
    return dict(get_most_common_emotion=get_most_common_emotion)

# -------------------------------------------------------------------
# Error Handlers
# -------------------------------------------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# -------------------------------------------------------------------
# Routes
# -------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# -------------------------------------------------------------------
# Register
# -------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Username already exists. Please choose another."
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

# -------------------------------------------------------------------
# Login
# -------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('chat'))
        else:
            return "Invalid username or password"
    
    return render_template('login.html')

# -------------------------------------------------------------------
# Logout
# -------------------------------------------------------------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# -------------------------------------------------------------------
# Dashboard
# -------------------------------------------------------------------

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# -------------------------------------------------------------------
# Profile Page
# -------------------------------------------------------------------

@app.route('/profile')
@login_required
def profile():
    conversations = Conversation.query.filter_by(user_id=current_user.id).all()
    
    total_conversations = len(conversations)
    
    emotion_counts = {}
    for conv in conversations:
        emotion = conv.detected_emotion
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    unique_emotions = len(emotion_counts)
    
    if conversations:
        last_conv = max(conversations, key=lambda x: x.timestamp)
        last_active = last_conv.timestamp.strftime('%b %d, %Y')
    else:
        last_active = 'Never'
    
    # Calculate average stress score
    avg_stress = 0
    stress_icon = "🟢"
    
    if conversations:
        stress_map = {
            'Exam Stress': 7,
            'Work Pressure': 7,
            'Anxiety': 8,
            'Anger/Frustration': 6,
            'Burnout/Exhaustion': 8,
            'Sadness': 5,
            'Relationship Concern': 6,
            'Gentle Conversation': 2
        }
        
        total_stress = 0
        for conv in conversations:
            total_stress += stress_map.get(conv.detected_emotion, 3)
        
        avg_stress = round(total_stress / len(conversations), 1)
        
        if avg_stress >= 7:
            stress_icon = "🔴"
        elif avg_stress >= 4:
            stress_icon = "🟡"
        else:
            stress_icon = "🟢"
    
    return render_template('profile.html',
                         username=current_user.username,
                         created_at=current_user.created_at,
                         total_conversations=total_conversations,
                         unique_emotions=unique_emotions,
                         last_active=last_active,
                         emotion_stats=emotion_counts,
                         avg_stress=avg_stress,
                         stress_icon=stress_icon)

# -------------------------------------------------------------------
# Mood Tracker
# -------------------------------------------------------------------

@app.route('/mood-tracker')
@login_required
def mood_tracker():
    conversations = Conversation.query.filter_by(user_id=current_user.id)\
                    .order_by(Conversation.timestamp).all()
    
    dates = []
    emotion_data = []
    emotion_counts = {}
    
    emotion_map = {
        'Exam Stress': 1,
        'Work Pressure': 2,
        'Sadness': 3,
        'Anxiety': 4,
        'Anger/Frustration': 5,
        'Burnout/Exhaustion': 6,
        'Relationship Concern': 7,
        'Gentle Conversation': 8
    }
    
    for conv in conversations:
        date_str = conv.timestamp.strftime('%b %d')
        dates.append(date_str)
        
        emotion = conv.detected_emotion
        emotion_data.append(emotion_map.get(emotion, 5))
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    total_chats = len(conversations)
    unique_emotions = len(emotion_counts)
    
    most_common = 'N/A'
    if emotion_counts:
        most_common = max(emotion_counts, key=emotion_counts.get)
    
    return render_template('mood_tracker.html',
                         dates=dates,
                         emotion_data=emotion_data,
                         emotion_counts=emotion_counts,
                         total_chats=total_chats,
                         unique_emotions=unique_emotions,
                         most_common=most_common)

# -------------------------------------------------------------------
# Journal Routes
# -------------------------------------------------------------------

@app.route('/journal')
@login_required
def journal():
    entries = Journal.query.filter_by(user_id=current_user.id)\
              .order_by(Journal.created_at.desc()).all()
    
    return render_template('journal.html', entries=entries)

@app.route('/add_journal', methods=['POST'])
@login_required
def add_journal():
    title = request.form['title']
    content = request.form['content']
    mood = request.form['mood']
    
    new_entry = Journal(
        user_id=current_user.id,
        title=title,
        content=content,
        mood=mood
    )
    
    db.session.add(new_entry)
    db.session.commit()
    
    return redirect(url_for('journal'))

@app.route('/delete_journal/<int:id>')
@login_required
def delete_journal(id):
    entry = Journal.query.get_or_404(id)
    
    if entry.user_id != current_user.id:
        return "Unauthorized", 403
    
    db.session.delete(entry)
    db.session.commit()
    
    return redirect(url_for('journal'))

# -------------------------------------------------------------------
# Favorite Tips Routes
# -------------------------------------------------------------------

@app.route('/favorites')
@login_required
def favorites():
    tips = FavoriteTip.query.filter_by(user_id=current_user.id)\
           .order_by(FavoriteTip.created_at.desc()).all()
    
    tips_by_emotion = {}
    for tip in tips:
        if tip.emotion not in tips_by_emotion:
            tips_by_emotion[tip.emotion] = []
        tips_by_emotion[tip.emotion].append(tip)
    
    return render_template('favorites.html', 
                         tips_by_emotion=tips_by_emotion,
                         total_tips=len(tips))

@app.route('/save_favorite', methods=['POST'])
@login_required
def save_favorite():
    data = request.get_json()
    tip_text = data.get('tip')
    emotion = data.get('emotion', 'General')
    
    if not tip_text:
        return {'error': 'No tip provided'}, 400
    
    existing = FavoriteTip.query.filter_by(
        user_id=current_user.id, 
        tip_text=tip_text
    ).first()
    
    if existing:
        return {'message': 'Tip already saved'}, 200
    
    new_tip = FavoriteTip(
        user_id=current_user.id,
        tip_text=tip_text,
        emotion=emotion,
        saved_from='Chat Conversation'
    )
    
    db.session.add(new_tip)
    db.session.commit()
    
    return {'message': 'Tip saved successfully'}, 200

@app.route('/delete_favorite/<int:id>')
@login_required
def delete_favorite(id):
    tip = FavoriteTip.query.get_or_404(id)
    
    if tip.user_id != current_user.id:
        return "Unauthorized", 403
    
    db.session.delete(tip)
    db.session.commit()
    
    return redirect(url_for('favorites'))

# -------------------------------------------------------------------
# Chat Page
# -------------------------------------------------------------------

@app.route('/chat')
@login_required
def chat():
    return render_template('chat.html', username=current_user.username)

# -------------------------------------------------------------------
# API Detect Emotion
# -------------------------------------------------------------------

@app.route('/api/detect', methods=['POST'])
@login_required
def detect():
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return {'error': 'Tell me what\'s on your mind, sweetheart'}, 400
    
    response = detect_emotion_and_respond(message)
    
    conversation = Conversation(
        user_id=current_user.id,
        user_message=message,
        bot_response=response['caring_response'],
        detected_emotion=response['emotion']
    )
    db.session.add(conversation)
    db.session.commit()
    
    return {
        'emotion': response['emotion'],
        'stress_score': response['stress_score'],
        'stress_level': response['stress_level'],
        'stress_icon': response['stress_icon'],
        'caring_response': response['caring_response'],
        'tips': response['tips']
    }

# -------------------------------------------------------------------
# History Page
# -------------------------------------------------------------------

@app.route('/history')
@login_required
def history():
    conversations = Conversation.query.filter_by(user_id=current_user.id)\
                    .order_by(Conversation.timestamp.desc()).all()
    
    return render_template('history.html', 
                         username=current_user.username,
                         conversations=conversations)

# -------------------------------------------------------------------
# View All Users (Protected)
# -------------------------------------------------------------------

@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users.html', users=all_users)

# -------------------------------------------------------------------
# Run App
# -------------------------------------------------------------------

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)