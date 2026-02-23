import random

def detect_emotion_and_respond(message, age=20):
    """Detect emotion from message with age-based personalization"""
    message_lower = message.lower()
    
    # Determine age group
    if age < 18:
        age_group = "teen"
    elif age < 30:
        age_group = "young_adult"
    elif age < 50:
        age_group = "adult"
    else:
        age_group = "senior"
    
    # Negation words list
    negation_words = ['not', "don't", 'dont', 'never', 'no', "can't", 'cant', "won't", 'wont', "didn't", 'didnt', "wasn't", 'wasnt']
    
    # Split message into words
    words = message_lower.split()
    
    # Function to check if a keyword is negated
    def is_negated(index, words, keyword):
        # Check previous word for negation
        if index > 0 and words[index-1] in negation_words:
            return True
        # Check for "not" before phrases
        if index > 1 and words[index-2] in negation_words:
            return True
        # Check for "n't" contractions
        if index > 0 and any(neg in words[index-1] for neg in ["n't", "not"]):
            return True
        return False
    
    # -------------------------------------------------------------------
    # HAPPY / POSITIVE DETECTION
    # -------------------------------------------------------------------
    happy_keywords = ['happy', 'good', 'great', 'wonderful', 'excellent', 'joy', 'glad', 'fantastic', 'amazing', 'love']
    for i, word in enumerate(words):
        if word in happy_keywords:
            if is_negated(i, words, word):
                return sad_response(age_group, "negated_happy")
            else:
                return happy_response(age_group)
    
    # -------------------------------------------------------------------
    # SAD / LONELY DETECTION
    # -------------------------------------------------------------------
    sad_keywords = ['sad', 'lonely', 'alone', 'depressed', 'empty', 'hurt', 'heartbroken', 'unhappy', 'miserable']
    for i, word in enumerate(words):
        if word in sad_keywords:
            if is_negated(i, words, word):
                return default_response(age_group)
            else:
                return sad_response(age_group)
    
    # -------------------------------------------------------------------
    # EXAM / STUDY STRESS
    # -------------------------------------------------------------------
    exam_keywords = ['exam', 'test', 'study', 'assignment', 'grade', 'fail', 'pass', 'paper', 'homework', 'class']
    for i, word in enumerate(words):
        if word in exam_keywords and not is_negated(i, words, word):
            return exam_stress_response(age_group)
    
    # -------------------------------------------------------------------
    # WORK PRESSURE
    # -------------------------------------------------------------------
    work_keywords = ['work', 'deadline', 'boss', 'job', 'office', 'colleague', 'pressure', 'overload', 'meeting', 'career']
    for i, word in enumerate(words):
        if word in work_keywords and not is_negated(i, words, word):
            return work_pressure_response(age_group)
    
    # -------------------------------------------------------------------
    # ANGER / FRUSTRATION
    # -------------------------------------------------------------------
    anger_keywords = ['angry', 'frustrated', 'annoyed', 'mad', 'irritated', 'hate', 'furious', 'upset']
    for i, word in enumerate(words):
        if word in anger_keywords and not is_negated(i, words, word):
            return anger_response(age_group)
    
    # -------------------------------------------------------------------
    # ANXIETY / WORRY
    # -------------------------------------------------------------------
    anxiety_keywords = ['anxious', 'worry', 'nervous', 'scared', 'fear', 'panic', 'overthink', 'stress', 'worried']
    for i, word in enumerate(words):
        if word in anxiety_keywords and not is_negated(i, words, word):
            return anxiety_response(age_group)
    
    # -------------------------------------------------------------------
    # TIRED / BURNOUT
    # -------------------------------------------------------------------
    tired_keywords = ['tired', 'exhausted', 'burnout', 'drained', 'fatigue', 'sleepy', 'worn out']
    for i, word in enumerate(words):
        if word in tired_keywords and not is_negated(i, words, word):
            return tired_response(age_group)
    
    # -------------------------------------------------------------------
    # RELATIONSHIP ISSUES
    # -------------------------------------------------------------------
    relationship_keywords = ['relationship', 'boyfriend', 'girlfriend', 'partner', 'friend', 'fight', 'argument', 'love', 'breakup', 'divorce']
    for i, word in enumerate(words):
        if word in relationship_keywords and not is_negated(i, words, word):
            return relationship_response(age_group)
    
    # -------------------------------------------------------------------
    # DEFAULT RESPONSE
    # -------------------------------------------------------------------
    return default_response(age_group)


# -------------------------------------------------------------------
# AGE-BASED RESPONSE FUNCTIONS
# -------------------------------------------------------------------

def happy_response(age_group):
    responses = {
        "teen": {
            "msg": """That's wonderful to hear you're feeling happy! 😊 

Your energy is contagious! What's bringing you joy today? Is it friends, a hobby, or something exciting happening at school? Share your happiness with me!""",
            "tips": [
                "🌸 Hold onto this feeling - you deserve it!",
                "📱 Share your joy with friends - they'll love it!",
                "🎵 Dance to your favorite music",
                "📸 Take a photo of something that made you smile today"
            ]
        },
        "young_adult": {
            "msg": """I'm so glad you're feeling happy! 😊 

That positive energy is wonderful. Whether it's achievements, relationships, or just a good day - celebrate these moments. What's contributing to your happiness right now?""",
            "tips": [
                "🌸 Savor these moments - they matter",
                "📝 Write down what made you happy today",
                "☕ Treat yourself to something you enjoy",
                "💫 Share your joy with someone close to you"
            ]
        },
        "adult": {
            "msg": """What a beautiful thing to hear - happiness is precious at any age. 😊 

In the midst of responsibilities and routines, moments of joy are treasures. What's bringing you happiness today? Is it family, work achievements, or simply some peace and quiet?""",
            "tips": [
                "🌸 Let yourself fully enjoy this feeling",
                "📞 Share with someone who matters to you",
                "🌿 Take a moment to breathe and appreciate",
                "💝 You deserve every bit of this happiness"
            ]
        },
        "senior": {
            "msg": """Hearing that you're happy warms my heart. 😊 

At your stage of life, happiness often comes from a deeper place - family connections, good health, peaceful moments, or fond memories. What's bringing you joy today, dear?""",
            "tips": [
                "🌸 Cherish this moment of happiness",
                "📞 Call someone who would love to hear from you",
                "📖 Write about this happy moment",
                "🌿 Simple joys are often the deepest"
            ]
        }
    }
    
    return {
        'emotion': 'Happiness',
        'stress_score': 1,
        'stress_level': 'Low',
        'stress_icon': '🟢',
        'caring_response': responses[age_group]["msg"],
        'tips': responses[age_group]["tips"]
    }


def sad_response(age_group, reason="general"):
    responses = {
        "teen": {
            "general": """Oh sweetie, I hear that you're feeling sad. 🤗 

Being a teenager is tough sometimes - with school, friends, and figuring out who you are. Whatever you're going through, your feelings are valid. Want to tell me more about what's making you feel this way?""",
            "negated": """I hear that you're not feeling happy right now. 🤗 

Sometimes when we say we're 'not happy', there's something deeper going on. Is everything okay? I'm here to listen, no judgment.""",
            "tips": [
                "🎵 Listen to music that matches or lifts your mood",
                "📱 Text a friend who gets you",
                "🛋️ Take some time for yourself",
                "🧸 Do something small that usually brings you comfort"
            ]
        },
        "young_adult": {
            "general": """I hear the sadness in your words, and it's okay to feel this way. 🤗 

Young adulthood comes with so many pressures - studies, career, relationships, finances. It's a lot to carry. Would you like to talk about what's weighing on your heart?""",
            "negated": """I hear that you're not feeling your best right now. 🤗 

It's okay to have days when things don't feel right. What's been going on? Sometimes just talking about it helps lighten the load.""",
            "tips": [
                "🎵 Put on music that comforts you",
                "☕ Take a break with a warm drink",
                "📝 Write down what you're feeling",
                "🌱 Remember, this feeling will pass"
            ]
        },
        "adult": {
            "general": """I'm so sorry you're feeling this sadness. 🤗 

As adults, we often feel we have to be strong for everyone else. But it's okay to not be okay. Life's challenges - work, family, responsibilities - can feel overwhelming sometimes. What's on your mind?""",
            "negated": """I hear that things aren't feeling good right now. 🤗 

Sometimes the weight of daily responsibilities can leave us feeling empty. You don't have to carry it all alone. Want to share what's been happening?""",
            "tips": [
                "🌿 Give yourself permission to rest",
                "📞 Call someone who understands you",
                "☕ Take a quiet moment for yourself",
                "💪 You've gotten through hard days before"
            ]
        },
        "senior": {
            "general": """My heart goes out to you, dear. 🤗 

At this stage of life, sadness can come from many places - missing loved ones, health concerns, or reflecting on the past. Whatever it is, you're not alone. Would you like to share what's on your heart?""",
            "negated": """I'm sorry you're not feeling well today, dear. 🤗 

Some days are harder than others, and that's completely normal. Is there something specific troubling you, or is it just one of those days?""",
            "tips": [
                "📖 Look at photos that bring back happy memories",
                "📞 Call someone who would love to hear your voice",
                "🌿 Spend time in nature if you can",
                "☕ Have a cup of tea and be gentle with yourself"
            ]
        }
    }
    
    key = "negated" if reason == "negated_happy" else "general"
    
    return {
        'emotion': 'Sadness',
        'stress_score': 6,
        'stress_level': 'Medium',
        'stress_icon': '🟡',
        'caring_response': responses[age_group][key],
        'tips': responses[age_group]["tips"]
    }


def exam_stress_response(age_group):
    responses = {
        "teen": {
            "msg": """Oh sweetheart, exams can feel like the whole world right now. 🌸 

I remember how much pressure school exams can bring. But here's the truth - one test does NOT define you. You're so much more than a grade. What subject is worrying you most? Maybe we can break it down together.""",
            "tips": [
                "📚 Study in 25-minute chunks with 5-minute breaks",
                "🍫 Treat yourself after each study session",
                "💬 Talk to your friends - they're stressed too!",
                "😴 Sleep is your best friend before an exam",
                "🎯 Focus on progress, not perfection"
            ]
        },
        "young_adult": {
            "msg": """I hear you - college exams, certifications, or important tests can be incredibly stressful. 🌸 

You're at a stage where exams can feel like they determine your future. But they don't. They're just one step in a long journey. You've gotten through every challenge so far - you'll get through this too.""",
            "tips": [
                "☕ Take breaks - all-nighters do more harm than good",
                "📝 Practice past papers - they're gold",
                "🥗 Eat well - your brain needs fuel",
                "🎯 Focus on understanding, not just memorizing",
                "💪 Trust your preparation"
            ]
        },
        "adult": {
            "msg": """Professional exams or certifications while juggling work and family? That's genuinely tough. 🌸 

The fact that you're still pushing forward shows your dedication. But remember - your health matters more than any test. How can we make this more manageable for you?""",
            "tips": [
                "⏰ Schedule study time like important meetings",
                "🏃 Take short walks to clear your mind",
                "👨‍👩‍👧 Involve your family in your journey",
                "💪 You're building skills, not just passing tests",
                "🎯 One chapter at a time"
            ]
        },
        "senior": {
            "msg": """Learning at any age is beautiful and brave. 🌸 

Whether you're studying for interest, qualification, or personal growth - I admire your dedication. Go at your own pace, and be proud of yourself for continuing to grow.""",
            "tips": [
                "📖 Enjoy the learning - no rush",
                "☕ Make it a pleasant ritual with tea",
                "🧠 Keep that mind active and young",
                "🌟 Be proud of yourself for growing",
                "🎯 Small progress is still progress"
            ]
        }
    }
    
    return {
        'emotion': 'Exam Stress',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': responses[age_group]["msg"],
        'tips': responses[age_group]["tips"]
    }


def work_pressure_response(age_group):
    responses = {
        "teen": {
            "msg": """Even at your age, there can be pressure - maybe from part-time jobs, school responsibilities, or family expectations. 🌸 

Whatever it is, you shouldn't have to carry it alone. What's weighing on you?""",
            "tips": [
                "🌿 It's okay to say 'no' sometimes",
                "💬 Talk to someone you trust",
                "🎯 Break tasks into smaller pieces",
                "😴 Rest is not lazy - it's necessary"
            ]
        },
        "young_adult": {
            "msg": """Work pressure in your 20s can be intense - building a career, proving yourself, financial pressure. 🌸 

I see how hard you're working, and I'm proud of you. But don't forget - you're a human being, not a machine. What part of work feels heaviest right now?""",
            "tips": [
                "🌿 Set boundaries - even small ones help",
                "📝 Make a list and do just ONE thing at a time",
                "💬 Talk to colleagues - you're not alone",
                "🏠 Leave work at work when you can",
                "💪 You're building skills, not just completing tasks"
            ]
        },
        "adult": {
            "msg": """Work pressure in your 40s often comes with so much responsibility - managing teams, meeting targets, while balancing family. 🌸 

That's a lot for anyone to carry. Remember why you started, but also know when to pause. What's the most overwhelming part right now?""",
            "tips": [
                "🌿 Delegate when possible",
                "📞 Talk to someone who understands",
                "🏃 Take short breaks during the day",
                "👨‍👩‍👧 Don't let work steal family time",
                "💪 You've handled challenges before"
            ]
        },
        "senior": {
            "msg": """Even in your 60s, work can still bring pressure - whether it's professional or personal projects. 🌸 

But at this stage, hopefully you've learned that peace matters more. Is there a way to lighten your load?""",
            "tips": [
                "🌿 Prioritize what truly matters",
                "☕ Take time for yourself daily",
                "👵 Don't be afraid to ask for help",
                "🌟 You've earned the right to pace yourself"
            ]
        }
    }
    
    return {
        'emotion': 'Work Pressure',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': responses[age_group]["msg"],
        'tips': responses[age_group]["tips"]
    }


def anger_response(age_group):
    responses = {
        "teen": {
            "msg": """I can feel your frustration, and it's completely okay to feel this way. 💫 

Being a teenager comes with so many emotions - sometimes it all just bubbles over. Take a deep breath with me. What happened that made you so upset?""",
            "tips": [
                "🚶 Step away for a few minutes",
                "✍️ Write down what you're feeling",
                "🎵 Listen to music that helps",
                "💬 Talk to someone who will just listen"
            ]
        },
        "young_adult": {
            "msg": """Anger and frustration are valid emotions - especially when you're dealing with so many pressures. 💫 

Sometimes anger is just sadness or fear in disguise. Take a moment to breathe. What triggered this feeling?""",
            "tips": [
                "🚶 Take a walk to clear your head",
                "✍️ Journal your feelings",
                "💦 Splash cold water on your face",
                "👂 Talk to someone who will listen without judging"
            ]
        },
        "adult": {
            "msg": """I hear the frustration in your voice. Life's demands can be overwhelming. 💫 

Before reacting, take a breath. What's the root of this anger - is it work, relationships, or feeling unheard?""",
            "tips": [
                "🌬️ Take three deep breaths right now",
                "🚶 Step away from the situation temporarily",
                "📞 Talk to someone who supports you",
                "💪 Channel that energy into something constructive"
            ]
        },
        "senior": {
            "msg": """It's never easy to feel angry or frustrated, especially at this stage of life. 💫 

Maybe things aren't as they used to be, or people aren't understanding you. What's troubling you, dear?""",
            "tips": [
                "🌿 Take a quiet moment for yourself",
                "📖 Read or do something calming",
                "☕ Have a cup of tea and breathe",
                "💬 Talk to someone patient and kind"
            ]
        }
    }
    
    return {
        'emotion': 'Anger/Frustration',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': responses[age_group]["msg"],
        'tips': responses[age_group]["tips"]
    }


def anxiety_response(age_group):
    responses = {
        "teen": {
            "msg": """Anxiety at your age can feel so overwhelming - with school, friends, and figuring out who you are. 🦋 

You're safe right now. Let's breathe together. In for 4, hold for 4, out for 4. What's making you feel anxious?""",
            "tips": [
                "🌬️ Breathe slowly - in through nose, out through mouth",
                "📱 Talk to a friend who makes you feel calm",
                "🎵 Listen to calming music",
                "🧸 Do something that comforts you"
            ]
        },
        "young_adult": {
            "msg": """Anxiety in your 20s is so common - with career, relationships, and future uncertainty. 🦋 

But you're here, you're trying, and that counts for so much. Let's ground ourselves. What's worrying you most right now?""",
            "tips": [
                "🔍 Name 5 things you can see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste",
                "🌬️ Breathe slowly - your body will follow",
                "🌈 This feeling will pass, it always does",
                "💪 You've survived 100% of your hard days so far"
            ]
        },
        "adult": {
            "msg": """Anxiety when you're juggling work, family, and responsibilities is completely understandable. 🦋 

But right now, in this moment, you're safe. Let's breathe together. What's the main source of worry for you today?""",
            "tips": [
                "🌬️ Take 5 deep breaths, slowly",
                "📝 Write down what you can and cannot control",
                "🏃 Move your body - even a short walk helps",
                "💭 Be kind to your anxious thoughts"
            ]
        },
        "senior": {
            "msg": """Anxiety can come at any age - health concerns, family worries, or just the uncertainty of life. 🦋 

You've lived through so much already. You're stronger than you know. What's troubling your heart today?""",
            "tips": [
                "🌬️ Gentle, slow breathing",
                "☕ Sit quietly with a warm drink",
                "📞 Call someone who brings you comfort",
                "🌿 Remember all you've overcome"
            ]
        }
    }
    
    return {
        'emotion': 'Anxiety',
        'stress_score': 8,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': responses[age_group]["msg"],
        'tips': responses[age_group]["tips"]
    }


def tired_response(age_group):
    responses = {
        "teen": {
            "msg": """You sound exhausted, sweetheart. School, activities, social life - it's a lot. 🌙 

Your body and mind are telling you they need rest. It's okay to take a break. When did you last really rest?""",
            "tips": [
                "😴 Sleep is your best friend",
                "📱 Put your phone away an hour before bed",
                "🛏️ Make your room cozy and calm",
                "🌙 Even 10 minutes of doing nothing helps"
            ]
        },
        "young_adult": {
            "msg": """Burnout in your 20s is real - trying to build a career, maintain relationships, and figure out life. 🌙 

You're not a machine. You need rest to recharge. When did you last take time just for yourself?""",
            "tips": [
                "😴 Sleep 7-8 hours - it's non-negotiable",
                "🚫 Say 'no' to one thing this week",
                "🥗 Eat something nourishing",
                "☁️ Do absolutely nothing for 10 minutes"
            ]
        },
        "adult": {
            "msg": """Exhaustion as an adult is so common - work, kids, responsibilities never end. 🌙 

But you can't pour from an empty cup. Rest isn't lazy, it's necessary. What's one thing you can let go of today?""",
            "tips": [
                "🛌 Sleep is medicine - rest early tonight",
                "🐢 Take today slowly - do only what's necessary",
                "🥗 Fuel your body with good food",
                "🚫 Protect your energy - say no to something"
            ]
        },
        "senior": {
            "msg": """Fatigue can be harder as we age, dear. Your body knows what it needs. 🌙 

Listen to it. Rest is not a weakness - it's wisdom. Have you been able to rest well lately?""",
            "tips": [
                "😴 Rest when you need to - no guilt",
                "☕ A warm drink and quiet moment helps",
                "🌿 Gentle movement if you feel up to it",
                "📖 Rest can also mean peaceful activities"
            ]
        }
    }
    
    return {
        'emotion': 'Burnout/Exhaustion',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': responses[age_group]["msg"],
        'tips': responses[age_group]["tips"]
    }


def relationship_response(age_group):
    responses = {
        "teen": {
            "msg": """Relationships - whether with friends, family, or first loves - can be so hard at your age. 💝 

Everything feels so intense. What happened? I'm here to listen without any judgment.""",
            "tips": [
                "💗 Your feelings are valid",
                "📝 Write down what you wish you could say",
                "💬 Talk to someone you trust",
                "🧘 Take time for yourself too"
            ]
        },
        "young_adult": {
            "msg": """Relationships in your 20s can be complicated - friendships changing, romantic relationships, family dynamics. 💝 

It's a lot to navigate. What's happening that's hurting you?""",
            "tips": [
                "💗 Give yourself space to feel",
                "📝 Journal your thoughts",
                "👥 Talk to someone who supports you",
                "🤲 You deserve to be treated with kindness"
            ]
        },
        "adult": {
            "msg": """Relationships at this stage - marriage, partnerships, friendships - they require so much work. 💝 

It's okay to struggle. What's weighing on your heart right now?""",
            "tips": [
                "💗 Communicate what you need",
                "📝 Sometimes writing helps clarify feelings",
                "👥 Don't isolate yourself",
                "🧘 Take care of yourself first"
            ]
        },
        "senior": {
            "msg": """Relationship challenges don't get easier with age, dear. 💝 

Whether it's family, children, or friends - our hearts remain tender. What's troubling you?""",
            "tips": [
                "💗 Your feelings matter at any age",
                "📞 Reach out to someone understanding",
                "📖 Reflect on what truly matters to you",
                "🌿 Peace is precious - protect yours"
            ]
        }
    }
    
    return {
        'emotion': 'Relationship Concern',
        'stress_score': 6,
        'stress_level': 'Medium',
        'stress_icon': '🟡',
        'caring_response': responses[age_group]["msg"],
        'tips': responses[age_group]["tips"]
    }


def default_response(age_group):
    responses = {
        "teen": [
            """Thank you for sharing with me. 🤍 How are you feeling right now? Sometimes just talking helps.""",
            """I'm here for you. 🌸 Tell me more about what's on your mind - I'm listening without judgment.""",
            """Whatever you're feeling is valid. 💫 Would you like to tell me more?"""
        ],
        "young_adult": [
            """Thank you for reaching out. 🤍 How are you doing right now, in this moment?""",
            """I'm here to listen. 🌸 Take your time and tell me what's on your mind.""",
            """Your feelings matter. 💫 What's been happening with you lately?"""
        ],
        "adult": [
            """Thank you for taking time to talk. 🤍 How are you feeling today?""",
            """I appreciate you sharing. 🌸 What's been on your heart lately?""",
            """Life can be so busy - I'm glad you're here. 💫 What would you like to talk about?"""
        ],
        "senior": [
            """Thank you for your time, dear. 🤍 How are you feeling today?""",
            """I'm always here to listen. 🌸 What's on your mind today?""",
            """Your presence here means a lot. 💫 What would you like to share?"""
        ]
    }
    
    # Age-specific tips
    tips_by_age = {
        "teen": [
            "🌬️ Take three deep breaths",
            "📱 Text a friend who makes you smile",
            "🎵 Listen to your favorite song",
            "🌟 You're doing better than you think"
        ],
        "young_adult": [
            "🌬️ Breathe deeply for a moment",
            "☕ Take a break with something warm",
            "📝 Journal your thoughts if you can",
            "💪 You've got this"
        ],
        "adult": [
            "🌬️ Take a few deep breaths",
            "☕ Give yourself a quiet moment",
            "🌿 Small breaks make a difference",
            "💝 Be gentle with yourself"
        ],
        "senior": [
            "🌬️ Breathe slowly and gently",
            "☕ Enjoy a quiet moment",
            "🌿 Peace starts within",
            "💝 You're exactly where you need to be"
        ]
    }
    
    return {
        'emotion': 'Gentle Conversation',
        'stress_score': 2,
        'stress_level': 'Low',
        'stress_icon': '🟢',
        'caring_response': random.choice(responses[age_group]),
        'tips': tips_by_age[age_group]
    }