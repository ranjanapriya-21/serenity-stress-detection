from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from emotion_detection import detect_emotion_and_respond
import os
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Secret key for sessions
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-secret-key-change-this')

# -------------------------------------------------------------------
# Database Configuration - With Persistent Disk Support for Render
# -------------------------------------------------------------------

# Determine database path based on environment
if os.path.exists('/opt/render/data'):
    # On Render with persistent disk
    db_path = '/opt/render/data/users.db'
    logger.info("✅ Using persistent disk on Render")
else:
    # Local development - use temp directory
    import tempfile
    db_path = os.path.join(tempfile.gettempdir(), 'users.db')
    logger.info(f"📁 Using local temp directory: {db_path}")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f"🗄️ Database will be stored at: {db_path}")

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
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        return "Homepage loading error", 500

@app.route('/about')
def about():
    return render_template('about.html')

# -------------------------------------------------------------------
# Register
# -------------------------------------------------------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            # Check if user exists
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                return "Username already exists. Please choose another."
            
            # Hash password and create user
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            
            logger.info(f"✅ New user registered: {username}")
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return "Registration failed. Please try again.", 500
    
    return render_template('register.html')

# -------------------------------------------------------------------
# Login
# -------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                logger.info(f"✅ User logged in: {username}")
                return redirect(url_for('chat'))
            else:
                return "Invalid username or password"
        except Exception as e:
            logger.error(f"Login error: {e}")
            return "Login failed. Please try again.", 500
    
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
    try:
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
    except Exception as e:
        logger.error(f"Profile error: {e}")
        return "Profile loading error", 500

# -------------------------------------------------------------------
# Mood Tracker
# -------------------------------------------------------------------

@app.route('/mood-tracker')
@login_required
def mood_tracker():
    try:
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
    except Exception as e:
        logger.error(f"Mood tracker error: {e}")
        return "Mood tracker error", 500

# -------------------------------------------------------------------
# Journal Routes
# -------------------------------------------------------------------

@app.route('/journal')
@login_required
def journal():
    try:
        entries = Journal.query.filter_by(user_id=current_user.id)\
                  .order_by(Journal.created_at.desc()).all()
        
        return render_template('journal.html', entries=entries)
    except Exception as e:
        logger.error(f"Journal error: {e}")
        return "Journal error", 500

@app.route('/add_journal', methods=['POST'])
@login_required
def add_journal():
    try:
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
    except Exception as e:
        logger.error(f"Add journal error: {e}")
        return "Failed to add journal entry", 500

@app.route('/delete_journal/<int:id>')
@login_required
def delete_journal(id):
    try:
        entry = Journal.query.get_or_404(id)
        
        if entry.user_id != current_user.id:
            return "Unauthorized", 403
        
        db.session.delete(entry)
        db.session.commit()
        
        return redirect(url_for('journal'))
    except Exception as e:
        logger.error(f"Delete journal error: {e}")
        return "Failed to delete journal entry", 500

# -------------------------------------------------------------------
# Favorite Tips Routes
# -------------------------------------------------------------------

@app.route('/favorites')
@login_required
def favorites():
    try:
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
    except Exception as e:
        logger.error(f"Favorites error: {e}")
        return "Favorites error", 500

@app.route('/save_favorite', methods=['POST'])
@login_required
def save_favorite():
    try:
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
    except Exception as e:
        logger.error(f"Save favorite error: {e}")
        return {'error': 'Failed to save tip'}, 500

@app.route('/delete_favorite/<int:id>')
@login_required
def delete_favorite(id):
    try:
        tip = FavoriteTip.query.get_or_404(id)
        
        if tip.user_id != current_user.id:
            return "Unauthorized", 403
        
        db.session.delete(tip)
        db.session.commit()
        
        return redirect(url_for('favorites'))
    except Exception as e:
        logger.error(f"Delete favorite error: {e}")
        return "Failed to delete favorite", 500

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
    try:
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
    except Exception as e:
        logger.error(f"Detect API error: {e}")
        return {'error': 'Something went wrong'}, 500

# -------------------------------------------------------------------
# History Page
# -------------------------------------------------------------------

@app.route('/history')
@login_required
def history():
    try:
        conversations = Conversation.query.filter_by(user_id=current_user.id)\
                        .order_by(Conversation.timestamp.desc()).all()
        
        return render_template('history.html', 
                             username=current_user.username,
                             conversations=conversations)
    except Exception as e:
        logger.error(f"History error: {e}")
        return "History error", 500

# -------------------------------------------------------------------
# View All Users (Protected)
# -------------------------------------------------------------------

@app.route('/users')
@login_required
def users():
    try:
        all_users = User.query.all()
        return render_template('users.html', users=all_users)
    except Exception as e:
        logger.error(f"Users error: {e}")
        return "Users page error", 500

# -------------------------------------------------------------------
# Export User Data (Backup)
# -------------------------------------------------------------------
@app.route('/export-data')
@login_required
def export_data():
    try:
        # Get user's data
        conversations = Conversation.query.filter_by(user_id=current_user.id).all()
        journal_entries = Journal.query.filter_by(user_id=current_user.id).all()
        favorite_tips = FavoriteTip.query.filter_by(user_id=current_user.id).all()
        
        # Prepare data dictionary
        user_data = {
            'username': current_user.username,
            'export_date': datetime.utcnow().isoformat(),
            'conversations': [],
            'journal_entries': [],
            'favorite_tips': []
        }
        
        # Add conversations
        for conv in conversations:
            user_data['conversations'].append({
                'user_message': conv.user_message,
                'bot_response': conv.bot_response,
                'detected_emotion': conv.detected_emotion,
                'timestamp': conv.timestamp.isoformat() if conv.timestamp else None
            })
        
        # Add journal entries
        for journal in journal_entries:
            user_data['journal_entries'].append({
                'title': journal.title,
                'content': journal.content,
                'mood': journal.mood,
                'created_at': journal.created_at.isoformat() if journal.created_at else None
            })
        
        # Add favorite tips
        for tip in favorite_tips:
            user_data['favorite_tips'].append({
                'tip_text': tip.tip_text,
                'emotion': tip.emotion,
                'saved_from': tip.saved_from,
                'created_at': tip.created_at.isoformat() if tip.created_at else None
            })
        
        # Create response with JSON file
        response = Response(
            json.dumps(user_data, indent=2),
            mimetype='application/json',
            headers={'Content-Disposition': f'attachment; filename=serenity_backup_{current_user.username}.json'}
        )
        return response
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        return "Export failed", 500

# -------------------------------------------------------------------
# Import User Data (Restore)
# -------------------------------------------------------------------
@app.route('/import-data', methods=['POST'])
@login_required
def import_data():
    try:
        # Get uploaded file
        file = request.files.get('backup_file')
        if not file:
            return "No file uploaded", 400
        
        # Read and parse JSON
        file_content = file.read().decode('utf-8')
        imported_data = json.loads(file_content)
        
        # Verify it's the right user (optional)
        if imported_data.get('username') != current_user.username:
            return "Warning: This backup belongs to a different user. Import anyway?", 400
        
        # Clear existing data (optional - comment out if you want to merge instead)
        Conversation.query.filter_by(user_id=current_user.id).delete()
        Journal.query.filter_by(user_id=current_user.id).delete()
        FavoriteTip.query.filter_by(user_id=current_user.id).delete()
        
        # Import conversations
        for conv_data in imported_data.get('conversations', []):
            conv = Conversation(
                user_id=current_user.id,
                user_message=conv_data['user_message'],
                bot_response=conv_data['bot_response'],
                detected_emotion=conv_data['detected_emotion'],
                timestamp=datetime.fromisoformat(conv_data['timestamp']) if conv_data.get('timestamp') else datetime.utcnow()
            )
            db.session.add(conv)
        
        # Import journal entries
        for journal_data in imported_data.get('journal_entries', []):
            journal = Journal(
                user_id=current_user.id,
                title=journal_data['title'],
                content=journal_data['content'],
                mood=journal_data['mood'],
                created_at=datetime.fromisoformat(journal_data['created_at']) if journal_data.get('created_at') else datetime.utcnow()
            )
            db.session.add(journal)
        
        # Import favorite tips
        for tip_data in imported_data.get('favorite_tips', []):
            tip = FavoriteTip(
                user_id=current_user.id,
                tip_text=tip_data['tip_text'],
                emotion=tip_data['emotion'],
                saved_from=tip_data.get('saved_from', 'Imported'),
                created_at=datetime.fromisoformat(tip_data['created_at']) if tip_data.get('created_at') else datetime.utcnow()
            )
            db.session.add(tip)
        
        db.session.commit()
        
        return redirect(url_for('profile'))
        
    except Exception as e:
        logger.error(f"Import error: {e}")
        return f"Import failed: {str(e)}", 500

# -------------------------------------------------------------------
# Backup Page
# -------------------------------------------------------------------
@app.route('/backup')
@login_required
def backup_page():
    return render_template('backup.html')

# -------------------------------------------------------------------
# Debug: Check Database Tables
# -------------------------------------------------------------------
@app.route('/debug-db')
def debug_database():
    try:
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        user_count = 0
        if 'user' in tables:
            user_count = User.query.count()
        
        return {
            'database_path': db_path,
            'file_exists': os.path.exists(db_path),
            'file_size': os.path.getsize(db_path) if os.path.exists(db_path) else 0,
            'tables': tables,
            'user_count': user_count,
            'status': 'healthy' if 'user' in tables else 'missing tables'
        }
    except Exception as e:
        return {'error': str(e), 'database_path': db_path}

# -------------------------------------------------------------------
# Health Check (Important for Render)
# -------------------------------------------------------------------
@app.route('/health')
def health():
    return {"status": "healthy", "database": db_path}, 200

# -------------------------------------------------------------------
# Force database creation - CRITICAL FIX FOR RENDER
# -------------------------------------------------------------------
def init_database():
    with app.app_context():
        try:
            # Force create all tables
            db.create_all()
            logger.info("✅ Database tables created successfully")
            
            # Verify tables exist by trying a simple query
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            logger.info(f"📊 Tables in database: {tables}")
            
            # Log database location
            if os.path.exists(db_path):
                size = os.path.getsize(db_path)
                logger.info(f"📁 Database file: {db_path} ({size} bytes)")
            else:
                logger.warning("⚠️ Database file not found after creation")
                
        except Exception as e:
            logger.error(f"❌ Database creation error: {e}")

# Call it twice to be sure!
logger.info("🚀 First database initialization attempt...")
init_database()
logger.info("🚀 Second database initialization attempt...")
init_database()

# -------------------------------------------------------------------
# Run App - FIXED FOR RENDER
# -------------------------------------------------------------------

if __name__ != '__main__':
    # This runs when gunicorn imports the app
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    # Get port from environment variable
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🚀 Starting app on port {port}")
    
    # Bind to 0.0.0.0 to allow external connections
    app.run(host='0.0.0.0', port=port, debug=False)