import random

def detect_emotion_and_respond(message, age=20):
    """Detect emotion from message with age-based personalization and response variety"""
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
        if index > 0 and words[index-1] in negation_words:
            return True
        if index > 1 and words[index-2] in negation_words:
            return True
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


# ======================================================================
# RESPONSE POOLS - MULTIPLE VARIATIONS FOR EACH EMOTION AND AGE GROUP
# ======================================================================

# ----------------------------------------------------------------------
# HAPPINESS RESPONSES
# ----------------------------------------------------------------------
def happy_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """That's wonderful to hear you're feeling happy! 😊 Your energy is contagious! What's bringing you joy today? Is it friends, a hobby, or something exciting happening at school?""",
                "tips": ["🌸 Hold onto this feeling - you deserve it!", "📱 Share your joy with friends - they'll love it!", "🎵 Dance to your favorite music!", "📸 Take a photo of something that made you smile today"]
            },
            {
                "msg": """I love seeing you happy! 😊 It lights up my heart. Tell me more about what's making you feel this way - I'd love to share in your joy!""",
                "tips": ["💫 This happiness is yours to enjoy!", "🎮 Do something you love today!", "☀️ Get outside and enjoy the day!", "📝 Write down three good things about today"]
            },
            {
                "msg": """Happiness looks beautiful on you! 😊 These moments are precious. What's the best part of your day so far?""",
                "tips": ["🎵 Sing along to your favorite song!", "🍦 Treat yourself to something you enjoy!", "💬 Call or text a friend who makes you laugh!", "🌟 You deserve every bit of this happiness"]
            }
        ],
        "young_adult": [
            {
                "msg": """I'm so glad you're feeling happy! 😊 That positive energy is wonderful. Whether it's achievements, relationships, or just a good day - celebrate these moments. What's contributing to your happiness right now?""",
                "tips": ["🌸 Savor these moments - they matter", "📝 Write down what made you happy today", "☕ Treat yourself to something you enjoy", "💫 Share your joy with someone close to you"]
            },
            {
                "msg": """Happiness in the midst of busy adult life is something to cherish! 😊 What's bringing you this joy today?""",
                "tips": ["🌿 Take a moment to really feel this happiness", "📞 Call someone who would love to hear from you", "🎯 Celebrate your wins, big or small", "💝 You deserve happiness"]
            },
            {
                "msg": """Your happiness makes my day! 😊 Tell me more - what's going well for you right now?""",
                "tips": ["☀️ Enjoy this feeling while it lasts", "📖 Remember this moment on harder days", "👥 Share your joy with others", "💫 You're doing something right!"]
            }
        ],
        "adult": [
            {
                "msg": """What a beautiful thing to hear - happiness is precious at any age. 😊 In the midst of responsibilities and routines, moments of joy are treasures. What's bringing you happiness today?""",
                "tips": ["🌸 Let yourself fully enjoy this feeling", "📞 Share with someone who matters to you", "🌿 Take a moment to breathe and appreciate", "💝 You deserve every bit of this happiness"]
            },
            {
                "msg": """I'm so happy to hear you're happy! 😊 Adult life can be so demanding - these moments of joy are precious. What's going well for you?""",
                "tips": ["🎯 Celebrate this moment", "👨‍👩‍👧 Share your happiness with family", "📝 Note what's working in your life", "💪 Let this energy fuel you"]
            },
            {
                "msg": """Happiness at your stage of life often comes from deeper places - and that's beautiful. 😊 What's bringing you this joy?""",
                "tips": ["🌿 Appreciate the simple pleasures", "📞 Connect with someone who shares your joy", "☕ Savor a quiet moment", "💝 You've earned this happiness"]
            }
        ],
        "senior": [
            {
                "msg": """Hearing that you're happy warms my heart. 😊 At your stage of life, happiness often comes from a deeper place - family connections, good health, peaceful moments, or fond memories. What's bringing you joy today, dear?""",
                "tips": ["🌸 Cherish this moment of happiness", "📞 Call someone who would love to hear from you", "📖 Write about this happy moment", "🌿 Simple joys are often the deepest"]
            },
            {
                "msg": """What a blessing to hear you're happy! 😊 At this stage of life, every moment of joy is precious. What's making you smile today?""",
                "tips": ["📸 Capture this happy moment", "👵 Share your joy with loved ones", "☕ Enjoy a peaceful moment", "💝 Happiness suits you, dear"]
            },
            {
                "msg": """Your happiness brings me joy too! 😊 Tell me what's brightening your days lately."",
                "tips": ["🌿 Peace and joy go hand in hand", "📞 Reach out to someone who cares", "📖 Reflect on life's blessings", "🌸 You deserve all the happiness"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Happiness',
        'stress_score': 1,
        'stress_level': 'Low',
        'stress_icon': '🟢',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# SADNESS RESPONSES
# ----------------------------------------------------------------------
def sad_response(age_group, reason="general"):
    response_pool = {
        "teen": {
            "general": [
                {
                    "msg": """Oh sweetie, I hear that you're feeling sad. 🤗 Being a teenager is tough sometimes - with school, friends, and figuring out who you are. Whatever you're going through, your feelings are valid. Want to tell me more?""",
                    "tips": ["🎵 Listen to music that matches or lifts your mood", "📱 Text a friend who gets you", "🛋️ Take some time for yourself", "🧸 Do something small that usually brings you comfort"]
                },
                {
                    "msg": """I'm so sorry you're feeling this way, sweetheart. 🤗 It's okay to be sad. Emotions come and go like clouds. Would you like to talk about what's bothering you?""",
                    "tips": ["💧 Let yourself cry if you need to", "🎨 Draw or paint how you feel", "📝 Write in a journal", "🐶 Spend time with a pet if you have one"]
                },
                {
                    "msg": """My heart goes out to you, dear. 🤗 Being young doesn't mean your feelings aren't real and deep. What's weighing on your heart today?""",
                    "tips": ["🌱 Remember this feeling will pass", "📱 Reach out to someone who understands", "🎮 Do something distracting for a bit", "😴 Rest - emotions are tiring"]
                }
            ],
            "negated": [
                {
                    "msg": """I hear that you're not feeling happy right now. 🤗 Sometimes when we say we're 'not happy', there's something deeper going on. Is everything okay? I'm here to listen.""",
                    "tips": ["💭 What would make today better?", "📝 Try writing down your thoughts", "☕ Take a moment for yourself", "🌱 Small steps help"]
                },
                {
                    "msg": """Not feeling happy is completely okay sometimes. 🤗 Life has ups and downs. What's been on your mind lately?""",
                    "tips": ["🎵 Music might help shift your mood", "📞 Call someone who makes you smile", "🚶 A short walk might help", "💫 Tomorrow is a new day"]
                }
            ]
        },
        "young_adult": {
            "general": [
                {
                    "msg": """I hear the sadness in your words, and it's okay to feel this way. 🤗 Young adulthood comes with so many pressures - studies, career, relationships, finances. It's a lot to carry. Would you like to talk about what's weighing on your heart?""",
                    "tips": ["🎵 Put on music that comforts you", "☕ Take a break with a warm drink", "📝 Write down what you're feeling", "🌱 Remember, this feeling will pass"]
                },
                {
                    "msg": """I'm here with you in this sadness. 🤗 Your 20s can be such a confusing time. What's making you feel this way?""",
                    "tips": ["🌬️ Breathe deeply for a moment", "📞 Call someone who gets it", "🚶 A change of scenery might help", "💪 You've survived hard days before"]
                },
                {
                    "msg": """Sadness at your age is so valid. 🤗 There's so much pressure to have it all figured out. But nobody really does. What's happening?""",
                    "tips": ["📖 Read something comforting", "☕ Treat yourself gently today", "🧘 Give yourself permission to rest", "🌈 This too shall pass"]
                }
            ],
            "negated": [
                {
                    "msg": """I hear that you're not feeling your best right now. 🤗 It's okay to have days when things don't feel right. What's been going on?""",
                    "tips": ["🌱 Start with something small today", "📝 Check in with yourself", "☕ Little comforts help", "💫 Better days are ahead"]
                },
                {
                    "msg": """Not every day can be a good day, and that's okay. 🤗 What would help you feel even a little better right now?""",
                    "tips": ["🎵 Play a favorite song", "📞 Text someone who cares", "🚶 Step outside for air", "🌟 You're doing okay"]
                }
            ]
        },
        "adult": {
            "general": [
                {
                    "msg": """I'm so sorry you're feeling this sadness. 🤗 As adults, we often feel we have to be strong for everyone else. But it's okay to not be okay. Life's challenges - work, family, responsibilities - can feel overwhelming sometimes. What's on your mind?""",
                    "tips": ["🌿 Give yourself permission to rest", "📞 Call someone who understands you", "☕ Take a quiet moment for yourself", "💪 You've gotten through hard days before"]
                },
                {
                    "msg": """This weight you're carrying - I can feel it through your words. 🤗 Adult life can be so heavy sometimes. What's the heaviest part right now?""",
                    "tips": ["🌬️ Breathe - just for a moment", "📝 Write down what's overwhelming you", "👥 You don't have to carry it alone", "🌱 Small steps, one at a time"]
                },
                {
                    "msg": """I'm here, and I'm listening. 🤗 Sadness at this stage of life often has many layers. What's beneath the surface for you today?""",
                    "tips": ["💧 It's okay to let it out", "📞 Reach out to a trusted friend", "🚶 Sometimes a walk helps clear the mind", "💝 Be gentle with yourself"]
                }
            ],
            "negated": [
                {
                    "msg": """I hear that things aren't feeling good right now. 🤗 Sometimes the weight of daily responsibilities can leave us feeling empty. You don't have to carry it all alone. Want to share what's been happening?""",
                    "tips": ["🌿 Start with one small thing", "📝 Check in with your feelings", "☕ A small comfort can help", "💫 This moment will pass"]
                },
                {
                    "msg": """Not feeling good is completely valid. 🤗 What would make today even slightly better?""",
                    "tips": ["🎵 Something that usually lifts you", "📞 A quick call to someone", "🚶 Fresh air and movement", "🌟 You're doing your best"]
                }
            ]
        },
        "senior": {
            "general": [
                {
                    "msg": """My heart goes out to you, dear. 🤗 At this stage of life, sadness can come from many places - missing loved ones, health concerns, or reflecting on the past. Whatever it is, you're not alone. Would you like to share what's on your heart?""",
                    "tips": ["📖 Look at photos that bring back happy memories", "📞 Call someone who would love to hear your voice", "🌿 Spend time in nature if you can", "☕ Have a cup of tea and be gentle with yourself"]
                },
                {
                    "msg": """I'm sitting with you in this moment of sadness. 🤗 Life's journey has so many chapters - some happy, some hard. What's weighing on you today?""",
                    "tips": ["📖 Reflect on happy memories too", "👵 Reach out to family or friends", "🌿 A quiet moment in nature helps", "💝 You are loved"]
                },
                {
                    "msg": """Your feelings matter at every age, dear. 🤗 What's causing this sadness today?""",
                    "tips": ["☕ A warm drink and quiet time", "📞 Call someone who cares", "📖 Read something comforting", "🌸 Be gentle with your heart"]
                }
            ],
            "negated": [
                {
                    "msg": """I'm sorry you're not feeling well today, dear. 🤗 Some days are harder than others, and that's completely normal. Is there something specific troubling you?""",
                    "tips": ["🌿 Rest if you need to", "☕ A small comfort helps", "📞 Someone would love to hear from you", "💫 Tomorrow may be brighter"]
                },
                {
                    "msg": """Not every day can be bright, and that's okay. 🤗 What might bring you a moment of peace today?""",
                    "tips": ["📖 Read a few pages of something", "🌿 Look out the window at nature", "☕ Sip something warm slowly", "💝 Be kind to yourself today"]
                }
            ]
        }
    }
    
    key = "negated" if reason == "negated_happy" else "general"
    selected = random.choice(response_pool[age_group][key])
    
    return {
        'emotion': 'Sadness',
        'stress_score': 6,
        'stress_level': 'Medium',
        'stress_icon': '🟡',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# TIRED / BURNOUT RESPONSES (with variety)
# ----------------------------------------------------------------------
def tired_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """You sound exhausted, sweetheart. School, activities, social life - it's a lot. 🌙 Your body and mind are telling you they need rest. It's okay to take a break. When did you last really rest?""",
                "tips": ["😴 Sleep is your best friend", "📱 Put your phone away an hour before bed", "🛏️ Make your room cozy and calm", "🌙 Even 10 minutes of doing nothing helps"]
            },
            {
                "msg": """I can hear how tired you are. 🌙 Being a teenager is exhausting - so much pressure, so little sleep. Please be kind to yourself and rest when you can.""",
                "tips": ["😴 Aim for 8-9 hours of sleep", "📵 No screens before bed", "🎵 Calming music helps", "🌙 Rest is productive too"]
            },
            {
                "msg": """You sound drained, sweetheart. 🌙 Between school, activities, and social life, it's no wonder. Your body is asking for a break. Will you give it one?""",
                "tips": ["😴 Sleep is when you grow and heal", "🛏️ Make your bedroom a cozy nest", "🧘 Try some deep breathing", "🌙 You can't pour from an empty cup"]
            }
        ],
        "young_adult": [
            {
                "msg": """Burnout in your 20s is real - trying to build a career, maintain relationships, and figure out life. 🌙 You're not a machine. You need rest to recharge. When did you last take time just for yourself?""",
                "tips": ["😴 Sleep 7-8 hours - it's non-negotiable", "🚫 Say 'no' to one thing this week", "🥗 Eat something nourishing", "☁️ Do absolutely nothing for 10 minutes"]
            },
            {
                "msg": """I hear the exhaustion in your words. 🌙 Your 20s can be so demanding. But burning out helps no one. What's one thing you can let go of today?""",
                "tips": ["😴 Prioritize sleep like it's your job", "📵 Put devices away before bed", "🚶 A short walk might help", "🌿 Rest is not lazy - it's necessary"]
            },
            {
                "msg": """You sound completely drained. 🌙 The hustle culture tells you to keep going, but your body is waving a white flag. Please listen to it.""",
                "tips": ["😴 Sleep is your superpower", "🚫 Protect your energy fiercely", "🥗 Nourish yourself", "☁️ Rest, guilt-free"]
            }
        ],
        "adult": [
            {
                "msg": """Exhaustion as an adult is so common - work, kids, responsibilities never end. 🌙 But you can't pour from an empty cup. Rest isn't lazy, it's necessary. What's one thing you can let go of today?""",
                "tips": ["🛌 Sleep is medicine - rest early tonight", "🐢 Take today slowly - do only what's necessary", "🥗 Fuel your body with good food", "🚫 Protect your energy - say no to something"]
            },
            {
                "msg": """Adult fatigue is real and valid. 🌙 Juggling everything is exhausting. But you matter too. When did you last do something just for you?""",
                "tips": ["😴 Prioritize rest this week", "📞 Delegate if you can", "🌿 Even 15 minutes of peace helps", "💪 You can't do it all - and that's okay"]
            },
            {
                "msg": """The weight of adult responsibilities is heavy. 🌙 No wonder you're tired. What would one hour of guilt-free rest look like for you?""",
                "tips": ["😴 Sleep is not optional - it's essential", "🚫 Say no without explaining", "🥗 Eat something that nourishes", "🌿 Rest recharges your patience too"]
            }
        ],
        "senior": [
            {
                "msg": """Fatigue can be harder as we age, dear. Your body knows what it needs. 🌙 Listen to it. Rest is not a weakness - it's wisdom. Have you been able to rest well lately?""",
                "tips": ["😴 Rest when you need to - no guilt", "☕ A warm drink and quiet moment helps", "🌿 Gentle movement if you feel up to it", "📖 Rest can also mean peaceful activities"]
            },
            {
                "msg": """I hear your tiredness, dear. 🌙 At your stage, energy is precious. Don't waste it on things that don't matter. Rest when you need to.""",
                "tips": ["😴 Listen to your body's signals", "☕ Rest with a cup of tea", "📖 A good book and quiet time", "🌿 Peace is more important than productivity"]
            },
            {
                "msg": """You've earned the right to rest whenever you need, dear. 🌙 Don't feel guilty about it. Rest is wisdom, not weakness.""",
                "tips": ["😴 Sleep when you're tired", "☕ Enjoy quiet moments", "📞 Rest doesn't mean isolation - call someone", "🌿 Gentle days are good days"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Burnout/Exhaustion',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# EXAM STRESS RESPONSES (with variety)
# ----------------------------------------------------------------------
def exam_stress_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """Oh sweetheart, exams can feel like the whole world right now. 🌸 But here's the truth - one test does NOT define you. You're so much more than a grade. What subject is worrying you most?""",
                "tips": ["📚 Study in 25-minute chunks with 5-minute breaks", "🍫 Treat yourself after each study session", "💬 Talk to your friends - they're stressed too!", "😴 Sleep is your best friend before an exam"]
            },
            {
                "msg": """I remember how much pressure school exams can bring. 🌸 Your best is always enough, no matter what the score says. How can I support you right now?""",
                "tips": ["📝 Make a study plan - small steps help", "🎯 Focus on progress, not perfection", "🥗 Don't skip meals - your brain needs fuel", "💪 You've prepared for this"]
            },
            {
                "msg": """Exam stress is real, and it's okay to feel it. 🌸 But don't let it convince you that you're not smart enough. You are. What's the hardest subject for you?""",
                "tips": ["📚 One topic at a time", "🧠 Teach someone else - it helps you learn", "💧 Stay hydrated - your brain needs water", "😴 All-nighters do more harm than good"]
            }
        ],
        "young_adult": [
            {
                "msg": """I hear you - college exams, certifications, or important tests can be incredibly stressful. 🌸 You're at a stage where exams can feel like they determine your future. But they don't. They're just one step in a long journey.""",
                "tips": ["☕ Take breaks - all-nighters do more harm than good", "📝 Practice past papers - they're gold", "🥗 Eat well - your brain needs fuel", "🎯 Focus on understanding, not just memorizing"]
            },
            {
                "msg": """The pressure you're under is real. 🌸 Exams at this stage feel so high-stakes. But you've gotten through every challenge so far - you'll get through this too.""",
                "tips": ["📚 Create a study schedule you can stick to", "🧠 Active recall works better than re-reading", "👥 Study groups can help", "💪 Trust your preparation"]
            },
            {
                "msg": """I can feel your exam anxiety through your words. 🌸 Remember that this moment is temporary. A few years from now, this exam will be a distant memory.""",
                "tips": ["🎯 Focus on what you can control", "🌬️ Breathe when you feel overwhelmed", "📝 Write down what you know", "😴 Sleep consolidates memory - don't skip it"]
            }
        ],
        "adult": [
            {
                "msg": """Professional exams or certifications while juggling work and family? That's genuinely tough. 🌸 The fact that you're still pushing forward shows your dedication. But remember - your health matters more than any test.""",
                "tips": ["⏰ Schedule study time like important meetings", "🏃 Take short walks to clear your mind", "👨‍👩‍👧 Involve your family in your journey", "💪 You're building skills, not just passing tests"]
            },
            {
                "msg": """Returning to exams as an adult is brave and challenging. 🌸 Life is already full - adding study pressure is no small thing. Be proud of yourself for taking this on.""",
                "tips": ["📚 Study when you're most alert", "🎯 Prioritize - you don't need to know everything", "👥 Find other adult learners for support", "😴 Sleep is when your brain processes learning"]
            },
            {
                "msg": """I admire your dedication to keep learning at this stage. 🌸 But don't let exams steal your peace. What's the biggest challenge you're facing with studying?""",
                "tips": ["📝 Break material into smaller chunks", "🌿 Study in a calm, organized space", "🥗 Brain foods - nuts, berries, fish", "💪 You're adding to your skills, not just passing"]
            }
        ],
        "senior": [
            {
                "msg": """Learning at any age is beautiful and brave. 🌸 Whether you're studying for interest, qualification, or personal growth - I admire your dedication. Go at your own pace, and be proud of yourself.""",
                "tips": ["📖 Enjoy the learning - no rush", "☕ Make it a pleasant ritual with tea", "🧠 Keep that mind active and young", "🌟 Be proud of yourself for growing"]
            },
            {
                "msg": """How wonderful that you're still learning! 🌸 Exams may feel different at this stage, but your commitment is inspiring. How can I support you?""",
                "tips": ["📚 Study when you feel most alert", "🌿 Take breaks when you need them", "🧠 Learning keeps your mind sharp", "💝 Be gentle with yourself - you're doing great"]
            },
            {
                "msg": """Learning has no age limit, and I'm so proud of you. 🌸 What motivated you to take on this study?""",
                "tips": ["📖 Focus on understanding, not memorizing", "☕ Pair study with something pleasant", "🧠 Your experience is your advantage", "🌟 Every step forward counts"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Exam Stress',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# WORK PRESSURE RESPONSES (with variety)
# ----------------------------------------------------------------------
def work_pressure_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """Even at your age, there can be pressure - maybe from part-time jobs, school responsibilities, or family expectations. 🌸 Whatever it is, you shouldn't have to carry it alone. What's weighing on you?""",
                "tips": ["🌿 It's okay to say 'no' sometimes", "💬 Talk to someone you trust", "🎯 Break tasks into smaller pieces", "😴 Rest is not lazy - it's necessary"]
            },
            {
                "msg": """I hear you're under pressure. 🌸 You're young - you shouldn't have to carry so much. What's the biggest source of stress for you?""",
                "tips": ["📝 Write down what's overwhelming you", "🎯 One thing at a time", "💬 Talk to an adult you trust", "🌿 You're allowed to take breaks"]
            }
        ],
        "young_adult": [
            {
                "msg": """Work pressure in your 20s can be intense - building a career, proving yourself, financial pressure. 🌸 I see how hard you're working, and I'm proud of you. But don't forget - you're a human being, not a machine.""",
                "tips": ["🌿 Set boundaries - even small ones help", "📝 Make a list and do just ONE thing at a time", "💬 Talk to colleagues - you're not alone", "🏠 Leave work at work when you can"]
            },
            {
                "msg": """The pressure to establish yourself is real. 🌸 But burning out won't help your career. What's the most overwhelming part of work right now?""",
                "tips": ["⏰ Time-block your day", "🚫 Learn to say no gracefully", "👥 Find a mentor or supporter", "💪 You're building skills, not just completing tasks"]
            },
            {
                "msg": """I can feel how much pressure you're under. 🌸 Your 20s are for learning, not for killing yourself over work. What would help lighten the load?""",
                "tips": ["🌿 Separate work from home life", "📝 Prioritize ruthlessly", "💬 Talk to your manager if possible", "😴 Sleep is not negotiable"]
            }
        ],
        "adult": [
            {
                "msg": """Work pressure in your 40s often comes with so much responsibility - managing teams, meeting targets, while balancing family. 🌸 That's a lot for anyone to carry. Remember why you started, but also know when to pause.""",
                "tips": ["🌿 Delegate when possible", "📞 Talk to someone who understands", "🏃 Take short breaks during the day", "👨‍👩‍👧 Don't let work steal family time"]
            },
            {
                "msg": """The weight of mid-career responsibility is heavy. 🌸 You're carrying so much - for your team, your family, yourself. What's one thing you could let go of?""",
                "tips": ["🌿 Set firmer boundaries", "📝 Focus on high-impact tasks", "👥 Build a support network at work", "💪 You've handled challenges before"]
            },
            {
                "msg": """I hear the exhaustion in your words about work. 🌸 Adulting is hard, and work often takes more than it gives. What would make tomorrow better?""",
                "tips": ["🌿 Protect your time off fiercely", "🎯 One goal per day is enough", "📞 Connect with understanding colleagues", "😴 Rest is how you sustain performance"]
            }
        ],
        "senior": [
            {
                "msg": """Even in your 60s, work can still bring pressure - whether it's professional or personal projects. 🌸 But at this stage, hopefully you've learned that peace matters more. Is there a way to lighten your load?""",
                "tips": ["🌿 Prioritize what truly matters", "☕ Take time for yourself daily", "👵 Don't be afraid to ask for help", "🌟 You've earned the right to pace yourself"]
            },
            {
                "msg": """You've worked so hard throughout your life. 🌸 If work is still stressful, maybe it's time to ask - is this still serving you?""",
                "tips": ["🌿 Consider what you truly want", "📞 Talk to family about your stress", "🧘 Peace is more valuable than productivity", "💝 Your well-being comes first"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Work Pressure',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# ANGER RESPONSES (with variety)
# ----------------------------------------------------------------------
def anger_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """I can feel your frustration, and it's completely okay to feel this way. 💫 Being a teenager comes with so many emotions - sometimes it all just bubbles over. Take a deep breath with me. What happened?""",
                "tips": ["🚶 Step away for a few minutes", "✍️ Write down what you're feeling", "🎵 Listen to music that helps", "💬 Talk to someone who will just listen"]
            },
            {
                "msg": """That anger is real and valid. 💫 Before you react, take a moment. What's really underneath the anger? Hurt? Fear? Disappointment?""",
                "tips": ["🌬️ Take three deep breaths", "🏃 Physical activity helps release anger", "📝 Journal your feelings", "🧸 Do something that calms you"]
            }
        ],
        "young_adult": [
            {
                "msg": """Anger and frustration are valid emotions - especially when you're dealing with so many pressures. 💫 Sometimes anger is just sadness or fear in disguise. Take a moment to breathe. What triggered this?""",
                "tips": ["🚶 Take a walk to clear your head", "✍️ Journal your feelings", "💦 Splash cold water on your face", "👂 Talk to someone who will listen without judging"]
            },
            {
                "msg": """I hear how frustrated you are. 💫 Life in your 20s can feel so unfair sometimes. What's really going on beneath the anger?""",
                "tips": ["🌬️ Breathe before you speak or act", "🎵 Intense music can help release", "🏋️ Physical exercise helps", "📞 Call someone who calms you"]
            }
        ],
        "adult": [
            {
                "msg": """I hear the frustration in your voice. Life's demands can be overwhelming. 💫 Before reacting, take a breath. What's the root of this anger - work, relationships, or feeling unheard?""",
                "tips": ["🌬️ Take three deep breaths right now", "🚶 Step away from the situation temporarily", "📞 Talk to someone who supports you", "💪 Channel that energy into something constructive"]
            },
            {
                "msg": """Anger at this stage of life often comes from feeling powerless or unappreciated. 💫 What's really at the heart of this?""",
                "tips": ["📝 Write down what you need to say", "🌿 Find a healthy outlet", "👥 Seek understanding, not just venting", "🧘 Give yourself space to cool down"]
            }
        ],
        "senior": [
            {
                "msg": """It's never easy to feel angry or frustrated, especially at this stage of life. 💫 Maybe things aren't as they used to be, or people aren't understanding you. What's troubling you, dear?""",
                "tips": ["🌿 Take a quiet moment for yourself", "📖 Read or do something calming", "☕ Have a cup of tea and breathe", "💬 Talk to someone patient and kind"]
            },
            {
                "msg": """Anger at any age is hard to carry. 💫 What's causing this feeling? Sometimes just naming it helps.""",
                "tips": ["🌬️ Breathe slowly", "🚶 A gentle walk might help", "📞 Call someone who listens", "🌿 Peace is precious - protect yours"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Anger/Frustration',
        'stress_score': 7,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# ANXIETY RESPONSES (with variety)
# ----------------------------------------------------------------------
def anxiety_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """Anxiety at your age can feel so overwhelming - with school, friends, and figuring out who you are. 🦋 You're safe right now. Let's breathe together. In for 4, hold for 4, out for 4. What's making you feel anxious?""",
                "tips": ["🌬️ Breathe slowly - in through nose, out through mouth", "📱 Talk to a friend who makes you feel calm", "🎵 Listen to calming music", "🧸 Do something that comforts you"]
            },
            {
                "msg": """That anxious feeling is so uncomfortable, I know. 🦋 Your brain is trying to protect you, but it's overworking right now. Let's ground ourselves. What can you see around you?""",
                "tips": ["🔍 Name 5 things you can see", "🖐️ 4 things you can touch", "👂 3 things you can hear", "🌬️ Breathe slowly"]
            }
        ],
        "young_adult": [
            {
                "msg": """Anxiety in your 20s is so common - with career, relationships, and future uncertainty. 🦋 But you're here, you're trying, and that counts for so much. Let's ground ourselves. What's worrying you most right now?""",
                "tips": ["🔍 Name 5 things you can see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste", "🌬️ Breathe slowly - your body will follow", "🌈 This feeling will pass, it always does", "💪 You've survived 100% of your hard days so far"]
            },
            {
                "msg": """That knot of anxiety in your chest - I know it well. 🦋 Let's untangle it together, one breath at a time. What's at the root of this worry?""",
                "tips": ["📝 Write down your worries", "🎯 Focus on what you can control", "🌬️ Extend your exhale - it calms the nervous system", "📞 Call someone who feels safe"]
            }
        ],
        "adult": [
            {
                "msg": """Anxiety when you're juggling work, family, and responsibilities is completely understandable. 🦋 But right now, in this moment, you're safe. Let's breathe together. What's the main source of worry for you today?""",
                "tips": ["🌬️ Take 5 deep breaths, slowly", "📝 Write down what you can and cannot control", "🏃 Move your body - even a short walk helps", "💭 Be kind to your anxious thoughts"]
            },
            {
                "msg": """Adult anxiety often comes from carrying too much. 🦋 What's one responsibility you could set down, even just for today?""",
                "tips": ["🌿 Give yourself permission to rest", "📞 Talk to someone who understands", "🎯 One thing at a time", "💪 You're stronger than your anxiety"]
            }
        ],
        "senior": [
            {
                "msg": """Anxiety can come at any age - health concerns, family worries, or just the uncertainty of life. 🦋 You've lived through so much already. You're stronger than you know. What's troubling your heart today?""",
                "tips": ["🌬️ Gentle, slow breathing", "☕ Sit quietly with a warm drink", "📞 Call someone who brings you comfort", "🌿 Remember all you've overcome"]
            },
            {
                "msg": """Worry at this stage is so understandable, dear. 🦋 But you've weathered so many storms. You'll get through this too.""",
                "tips": ["📖 Read something comforting", "🌿 Spend time in nature", "👵 Reach out to loved ones", "💝 Be gentle with yourself"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Anxiety',
        'stress_score': 8,
        'stress_level': 'High',
        'stress_icon': '🔴',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# RELATIONSHIP RESPONSES (with variety)
# ----------------------------------------------------------------------
def relationship_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """Relationships - whether with friends, family, or first loves - can be so hard at your age. 💝 Everything feels so intense. What happened? I'm here to listen without any judgment.""",
                "tips": ["💗 Your feelings are valid", "📝 Write down what you wish you could say", "💬 Talk to someone you trust", "🧘 Take time for yourself too"]
            },
            {
                "msg": """Friendship or relationship struggles at your age can feel world-ending. 💝 They're not, but they hurt deeply. What's happening?""",
                "tips": ["💗 Give yourself space to cry if needed", "📱 Reach out to a different friend", "🎵 Music can help process feelings", "🌱 This pain will ease with time"]
            }
        ],
        "young_adult": [
            {
                "msg": """Relationships in your 20s can be complicated - friendships changing, romantic relationships, family dynamics. 💝 It's a lot to navigate. What's happening that's hurting you?""",
                "tips": ["💗 Give yourself space to feel", "📝 Journal your thoughts", "👥 Talk to someone who supports you", "🤲 You deserve to be treated with kindness"]
            },
            {
                "msg": """I hear the hurt in your words about relationships. 💝 Your 20s are when we learn so much about love and loss. What's weighing on your heart?""",
                "tips": ["💗 You are worthy of love", "📞 Reach out to a trusted friend", "🌿 Take time to heal", "💪 This pain is teaching you something"]
            }
        ],
        "adult": [
            {
                "msg": """Relationships at this stage - marriage, partnerships, friendships - they require so much work. 💝 It's okay to struggle. What's weighing on your heart right now?""",
                "tips": ["💗 Communicate what you need", "📝 Sometimes writing helps clarify feelings", "👥 Don't isolate yourself", "🧘 Take care of yourself first"]
            },
            {
                "msg": """Long-term relationships have seasons of difficulty. 💝 That doesn't mean it's broken. What's challenging you right now?""",
                "tips": ["💗 Patience with yourself and others", "📞 Consider talking to someone neutral", "🌿 Reflect on what you truly need", "💪 You've worked through hard things before"]
            }
        ],
        "senior": [
            {
                "msg": """Relationship challenges don't get easier with age, dear. 💝 Whether it's family, children, or friends - our hearts remain tender. What's troubling you?""",
                "tips": ["💗 Your feelings matter at any age", "📞 Reach out to someone understanding", "📖 Reflect on what truly matters to you", "🌿 Peace is precious - protect yours"]
            },
            {
                "msg": """At this stage of life, relationships with adult children or aging friends bring unique challenges. 💝 What's on your heart?""",
                "tips": ["💗 It's okay to set boundaries", "📞 Connection, even brief, helps", "🌿 Focus on quality over quantity", "💝 You deserve respect and kindness"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Relationship Concern',
        'stress_score': 6,
        'stress_level': 'Medium',
        'stress_icon': '🟡',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }


# ----------------------------------------------------------------------
# DEFAULT RESPONSES (with variety)
# ----------------------------------------------------------------------
def default_response(age_group):
    response_pool = {
        "teen": [
            {
                "msg": """Thank you for sharing with me. 🤍 How are you feeling right now? Sometimes just talking helps.""",
                "tips": ["🌬️ Take three deep breaths", "📱 Text a friend who makes you smile", "🎵 Listen to your favorite song", "🌟 You're doing better than you think"]
            },
            {
                "msg": """I'm here for you. 🌸 Tell me more about what's on your mind - I'm listening without judgment.""",
                "tips": ["💧 Drink some water", "📝 Write down your thoughts", "🚶 Take a short walk", "💫 Your feelings matter"]
            },
            {
                "msg": """Whatever you're feeling is valid. 💫 Would you like to tell me more?"",
                "tips": ["🎵 Play a song you love", "📞 Call someone who gets you", "😴 Rest if you're tired", "🌟 You're not alone"]
            }
        ],
        "young_adult": [
            {
                "msg": """Thank you for reaching out. 🤍 How are you doing right now, in this moment?"",
                "tips": ["🌬️ Breathe deeply for a moment", "☕ Take a break with something warm", "📝 Journal your thoughts if you can", "💪 You've got this"]
            },
            {
                "msg": """I'm here to listen. 🌸 Take your time and tell me what's on your mind.""",
                "tips": ["🌿 Step outside for fresh air", "📞 Call someone who lifts you up", "🎯 One thing at a time", "💫 This moment is yours"]
            },
            {
                "msg": """Your feelings matter. 💫 What's been happening with you lately?"",
                "tips": ["📝 Write three things you're grateful for", "☕ Savor a warm drink", "🚶 Move your body gently", "🌟 You're exactly where you need to be"]
            }
        ],
        "adult": [
            {
                "msg": """Thank you for taking time to talk. 🤍 How are you feeling today?"",
                "tips": ["🌬️ Take a few deep breaths", "☕ Give yourself a quiet moment", "🌿 Small breaks make a difference", "💝 Be gentle with yourself"]
            },
            {
                "msg": """I appreciate you sharing. 🌸 What's been on your heart lately?"",
                "tips": ["📝 Check in with yourself", "📞 Connect with someone who matters", "🚶 A short walk can shift perspective", "💪 You're handling a lot"]
            },
            {
                "msg": """Life can be so busy - I'm glad you're here. 💫 What would you like to talk about?"",
                "tips": ["🌿 Prioritize one thing today", "☕ Create a small moment of peace", "👥 You don't have to do it alone", "🌟 You're doing enough"]
            }
        ],
        "senior": [
            {
                "msg": """Thank you for your time, dear. 🤍 How are you feeling today?"",
                "tips": ["🌬️ Breathe slowly and gently", "☕ Enjoy a quiet moment", "🌿 Peace starts within", "💝 You're exactly where you need to be"]
            },
            {
                "msg": """I'm always here to listen. 🌸 What's on your mind today?"",
                "tips": ["📞 Call someone who cares", "📖 Read something comforting", "🌿 Look out the window at nature", "💫 Your presence here matters"]
            },
            {
                "msg": """Your presence here means a lot. 💫 What would you like to share?"",
                "tips": ["☕ Sip something warm slowly", "📝 Write down a happy memory", "👵 Reach out to family", "🌸 Be kind to yourself today"]
            }
        ]
    }
    
    selected = random.choice(response_pool[age_group])
    return {
        'emotion': 'Gentle Conversation',
        'stress_score': 2,
        'stress_level': 'Low',
        'stress_icon': '🟢',
        'caring_response': selected["msg"],
        'tips': selected["tips"]
    }