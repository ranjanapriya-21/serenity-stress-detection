import random

def detect_emotion_and_respond(message):
    """Detect emotion from message with negation handling"""
    message_lower = message.lower()
    
    # First, check for negation words
    negation_words = ['not', "don't", 'dont', 'never', 'no', "can't", 'cant', "won't", 'wont', "didn't", 'didnt', "wasn't", 'wasnt']
    
    # Split message into words for better negation detection
    words = message_lower.split()
    
    # Function to check if a keyword is negated
    def is_negated(index, words, keyword):
        # Check previous word for negation
        if index > 0 and words[index-1] in negation_words:
            return True
        # Check for "not" before phrases like "not feeling happy"
        if index > 1 and words[index-2] in negation_words:
            return True
        # Check for "n't" contractions (like don't, can't)
        if index > 0 and any(neg in words[index-1] for neg in ["n't", "not"]):
            return True
        return False
    
    # -------------------------------------------------------------------
    # HAPPY / POSITIVE DETECTION (with negation check)
    # -------------------------------------------------------------------
    happy_keywords = ['happy', 'good', 'great', 'wonderful', 'excellent', 'joy', 'glad', 'fantastic', 'amazing', 'love']
    for i, word in enumerate(words):
        if word in happy_keywords:
            if is_negated(i, words, word):
                # They said "not happy" -> sadness
                return sad_response("negated_happy")
            else:
                # They said "happy" -> happiness
                return happy_response()
    
    # -------------------------------------------------------------------
    # SAD / LONELY DETECTION (with negation check)
    # -------------------------------------------------------------------
    sad_keywords = ['sad', 'lonely', 'alone', 'depressed', 'empty', 'hurt', 'heartbroken', 'unhappy', 'miserable']
    for i, word in enumerate(words):
        if word in sad_keywords:
            if is_negated(i, words, word):
                # They said "not sad" -> they might be okay
                return default_response()
            else:
                return sad_response()
    
    # -------------------------------------------------------------------
    # EXAM / STUDY STRESS
    # -------------------------------------------------------------------
    exam_keywords = ['exam', 'test', 'study', 'assignment', 'grade', 'fail', 'pass', 'paper', 'homework', 'class']
    for i, word in enumerate(words):
        if word in exam_keywords and not is_negated(i, words, word):
            return exam_stress_response()
    
    # -------------------------------------------------------------------
    # WORK PRESSURE
    # -------------------------------------------------------------------
    work_keywords = ['work', 'deadline', 'boss', 'job', 'office', 'colleague', 'pressure', 'overload', 'meeting']
    for i, word in enumerate(words):
        if word in work_keywords and not is_negated(i, words, word):
            return work_pressure_response()
    
    # -------------------------------------------------------------------
    # ANGER / FRUSTRATION
    # -------------------------------------------------------------------
    anger_keywords = ['angry', 'frustrated', 'annoyed', 'mad', 'irritated', 'hate', 'furious', 'upset']
    for i, word in enumerate(words):
        if word in anger_keywords and not is_negated(i, words, word):
            return anger_response()
    
    # -------------------------------------------------------------------
    # ANXIETY / WORRY
    # -------------------------------------------------------------------
    anxiety_keywords = ['anxious', 'worry', 'nervous', 'scared', 'fear', 'panic', 'overthink', 'stress', 'worried']
    for i, word in enumerate(words):
        if word in anxiety_keywords and not is_negated(i, words, word):
            return anxiety_response()
    
    # -------------------------------------------------------------------
    # TIRED / BURNOUT
    # -------------------------------------------------------------------
    tired_keywords = ['tired', 'exhausted', 'burnout', 'drained', 'fatigue', 'sleepy', 'worn out']
    for i, word in enumerate(words):
        if word in tired_keywords and not is_negated(i, words, word):
            return tired_response()
    
    # -------------------------------------------------------------------
    # RELATIONSHIP ISSUES
    # -------------------------------------------------------------------
    relationship_keywords = ['relationship', 'boyfriend', 'girlfriend', 'partner', 'friend', 'fight', 'argument', 'love', 'breakup', 'divorce']
    for i, word in enumerate(words):
        if word in relationship_keywords and not is_negated(i, words, word):
            return relationship_response()
    
    # -------------------------------------------------------------------
    # DEFAULT RESPONSE
    # -------------------------------------------------------------------
    return default_response()


# -------------------------------------------------------------------
# RESPONSE FUNCTIONS
# -------------------------------------------------------------------

def happy_response():
    return {
        'emotion': 'Happiness',
        'stress_score': 1,
        'stress_level': 'Low',
        'stress_icon': '🟢',
        'caring_response': """I'm so glad to hear you're feeling happy, dear! 😊 

That wonderful energy you're feeling - hold onto it. You deserve these moments of joy. What's bringing you happiness today? I'd love to share in your joy.""",
        'tips': [
            "🌸 Savor this moment - happiness is precious",
            "📝 Write down what made you happy today",
            "💫 Share your joy with someone close to you",
            "🌿 Let this happiness recharge your spirit"
        ]
    }

def sad_response(reason="general"):
    if reason == "negated_happy":
        caring_msg = """Oh sweetie, I hear that you're not feeling happy right now. 🤗 

It's okay to feel this way. Sometimes when we say we're 'not happy', there's something deeper going on. Would you like to tell me more about what's making you feel this way? I'm here to listen, no judgment, just care."""
    else:
        caring_msg = """Oh sweetie, I hear the sadness in your words. 🤗 

It's okay to feel this way. Emotions come and go like clouds. You're not alone - I'm right here with you. Would you like to tell me more about what's making you feel sad?"""
    
    return {
        'emotion': 'Sadness',
        'stress_score': 6,
        'stress_level': 'Medium',
        'stress_icon': '🟡',
        'caring_response': caring_msg,
        'tips': [
            "🎵 Listen to some comforting music",
            "🛋️ Wrap yourself in a cozy blanket",
            "☎️ Call or text someone who cares about you",
            "🌱 Remember, tomorrow is a new day",
            "💧 Let yourself cry if you need to - it helps release emotions"
        ]
    }

def exam_stress_response():
    return {
        'emotion': 'Exam Stress',
        'stress_score': 8,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': """Oh sweetheart, exams can feel so overwhelming, can't they? 🌸 

I can hear the worry in your words. Take a deep breath with me... in through your nose... and out through your mouth. 

You've worked so hard, and that alone is something to be proud of. Remember, exams don't define your worth - your effort and growth do. 

Would you like to tell me which subject is worrying you the most? Sometimes sharing makes the burden lighter.""",
        'tips': [
            "🌸 Take short 5-minute breaks every 25 minutes - your brain needs rest",
            "🍵 Drink some warm chamomile tea while you study, it's calming",
            "🥗 Don't skip meals - your brain needs fuel, darling",
            "😴 Sleep is more important than extra studying. Rest helps memory.",
            "💝 You're doing better than you think you are"
        ]
    }

def work_pressure_response():
    return {
        'emotion': 'Work Pressure',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': """My dear, work can be so demanding these days. 🤗 

I can feel how much this is weighing on your heart. Remember that you're doing your best, and that's always, always enough. 

Your peace of mind comes first - no job is worth your wellbeing. What part of work feels heaviest right now? Let's talk it through together.""",
        'tips': [
            "🌿 Set small boundaries - even a 5-minute walk helps",
            "📝 Make a list and do just ONE thing at a time",
            "💬 Talk to someone you trust - you're not alone",
            "🏠 Leave work at work; your home is your sanctuary",
            "✨ Tomorrow is a new day with new possibilities"
        ]
    }

def anger_response():
    return {
        'emotion': 'Anger/Frustration',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': """I can sense the frustration in your words, and it's completely okay to feel this way. 💫 

Take a deep breath with me... in through your nose... and out through your mouth. 

Sometimes anger is just sadness or fear wearing a loud jacket. What happened that made you feel this way? I'm here to listen, no judgment, just love.""",
        'tips': [
            "🚶 Step away for 10 minutes if you can - distance helps",
            "✍️ Write down what you're feeling, then tear the paper",
            "💦 Splash cold water on your face - it's refreshing",
            "🌬️ Take three deep breaths right now",
            "👂 Talk to someone who will just listen"
        ]
    }

def anxiety_response():
    return {
        'emotion': 'Anxiety',
        'stress_score': 8,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': """Oh my dear, anxiety can feel so overwhelming. 🦋 

I want you to know that you're safe right now, in this moment. Take my hand (virtually) and let's breathe together. 

Breathe in for 4 counts... hold for 4... out for 4. 

What's worrying you right now? Sometimes naming our fears makes them smaller.""",
        'tips': [
            "🔍 Try the 5-4-3-2-1 technique: name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
            "🌬️ Breathe slowly - your body will follow",
            "🌈 This feeling will pass, it always does",
            "💪 You've gotten through 100% of your hard days so far",
            "💭 Be kind to your anxious thoughts, they're trying to protect you"
        ]
    }

def tired_response():
    return {
        'emotion': 'Burnout/Exhaustion',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': """Oh sweetheart, you sound so tired. Your body and mind are telling you they need rest. 🌙 

It's not weak to rest - it's necessary, like charging a phone. You can't pour from an empty cup. 

When did you last take time just for yourself, doing absolutely nothing? Let's talk about giving you permission to rest.""",
        'tips': [
            "🐢 Take today slowly - do only what's absolutely necessary",
            "🛌 Sleep is medicine, darling - rest early tonight",
            "☁️ Even 10 minutes of doing nothing helps reset",
            "🥗 Eat something nourishing, your body needs fuel",
            "🚫 Say 'no' to one thing today - protect your energy"
        ]
    }

def relationship_response():
    return {
        'emotion': 'Relationship Concern',
        'stress_score': 6,
        'stress_level': 'Medium',
        'stress_icon': '🟡',
        'caring_response': """Relationships can be so beautiful and so hard at the same time, can't they? 💝 

I hear the hurt in your words. Remember that all relationships have difficult moments - it doesn't mean anything is broken. 

It just means you're human, caring deeply. Would you like to talk about what happened? Sometimes saying it out loud helps us understand our own feelings better.""",
        'tips': [
            "💗 Give yourself space to feel before reacting",
            "📝 Write down what you'd really like to say",
            "🤲 Remember that you deserve to be treated with kindness",
            "👥 Talk to someone who will support you",
            "🧘 It's okay to take time for yourself"
        ]
    }

def default_response():
    responses = [
        """Thank you for sharing with me, dear. 🤍 Sometimes just saying things out loud helps us understand our own feelings better. I'm here to listen, not to judge. How are you feeling right now, in this moment? Take your time.""",
        
        """I'm here, sweetheart. 🌸 You don't have to have the perfect words. Just being here, reaching out - that's brave. Tell me more about what's on your mind.""",
        
        """I hear you, love. 💫 Whatever you're feeling right now is valid. There's no right or wrong way to feel. Would you like to tell me more? I'm listening with my whole heart."""
    ]
    
    return {
        'emotion': 'Gentle Conversation',
        'stress_score': 2,
        'stress_level': 'Low',
        'stress_icon': '🟢',
        'caring_response': random.choice(responses),
        'tips': [
            "🌬️ Take three deep breaths right now",
            "💧 Drink a glass of water - it's self-care",
            "🌟 You're doing the best you can, and that's wonderful",
            "💝 This moment is yours - be gentle with yourself",
            "🌈 I'm proud of you for reaching out"
        ]
    }