import random

def detect_emotion_and_respond(message):
    """Detect emotion from message and return caring response with tips and stress level"""
    message_lower = message.lower()
    
    # Calculate stress score (0-10)
    stress_score = 0
    stress_keywords = {
        'exam': 3, 'test': 3, 'study': 2, 'assignment': 2, 'grade': 2, 'fail': 4, 'pass': 2,
        'work': 2, 'deadline': 4, 'boss': 3, 'job': 2, 'office': 2, 'pressure': 4, 'overload': 4,
        'anxious': 4, 'worry': 3, 'nervous': 3, 'scared': 3, 'fear': 3, 'panic': 5, 'overthink': 3,
        'tired': 2, 'exhausted': 3, 'burnout': 5, 'drained': 3, 'sleep': 1,
        'angry': 3, 'frustrated': 3, 'annoyed': 2, 'mad': 3,
        'sad': 2, 'lonely': 3, 'alone': 2, 'cry': 2,
        'relationship': 2, 'fight': 3, 'argument': 3, 'breakup': 4
    }
    
    for word, score in stress_keywords.items():
        if word in message_lower:
            stress_score += score
    
    # Cap at 10
    stress_score = min(stress_score, 10)
    
    # Determine stress level
    if stress_score >= 7:
        stress_level = "High"
        level_color = "#b76e79"  # Rose red
        level_icon = "🔴"
    elif stress_score >= 4:
        stress_level = "Medium"
        level_color = "#d48c98"  # Light rose
        level_icon = "🟡"
    else:
        stress_level = "Low"
        level_color = "#a7b89e"  # Sage green
        level_icon = "🟢"
    
    # Exam/Study Stress
    if any(word in message_lower for word in ['exam', 'test', 'study', 'assignment', 'grade', 'fail', 'pass', 'paper']):
        return {
            'emotion': 'Exam Stress',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': f"""Oh sweetheart, exams can feel so overwhelming, can't they? 🌸 

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
    
    # Work Pressure
    elif any(word in message_lower for word in ['work', 'deadline', 'boss', 'job', 'office', 'colleague', 'pressure', 'overload']):
        return {
            'emotion': 'Work Pressure',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': f"""My dear, work can be so demanding these days. 🤗 

I can feel how much this is weighing on your heart. Remember that you're doing your best, and that's always, always enough. 

Your peace of mind comes first - no job is worth your wellbeing. What part of work feels heaviest right now? 

Let's talk it through together, like we always do.""",
            'tips': [
                "🌿 Set small boundaries - even a 5-minute walk helps",
                "📝 Make a list and do just ONE thing at a time",
                "💬 Talk to someone you trust - you're not alone",
                "🏠 Leave work at work; your home is your sanctuary",
                "✨ Tomorrow is a new day with new possibilities"
            ]
        }
    
    # Sadness/Loneliness
    elif any(word in message_lower for word in ['sad', 'cry', 'lonely', 'alone', 'depressed', 'empty', 'hurt', 'heartbroken']):
        return {
            'emotion': 'Sadness',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': f"""Oh sweetie, come here. 🤗 

I'm so sorry you're feeling this way. It's okay to feel sad, and it's okay to cry. Emotions are like clouds - they come and go. 

You're not alone, even when it feels that way. I'm right here, listening to every word. 

Would you like to tell me what's making you feel this way? Sometimes sharing the weight makes it lighter. And remember - tomorrow is a new day, and this feeling will pass.""",
            'tips': [
                "🎵 Put on some soft music and just rest for a while",
                "🛋️ Wrap yourself in a cozy blanket - comfort helps",
                "🌱 Step outside for just 5 minutes of fresh air",
                "📞 Call or text someone who cares about you",
                "💕 Be gentle with yourself today"
            ]
        }
    
    # Anger/Frustration
    elif any(word in message_lower for word in ['angry', 'frustrated', 'annoyed', 'mad', 'irritated', 'hate', 'furious']):
        return {
            'emotion': 'Anger/Frustration',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': f"""I can sense the frustration in your words, and it's completely okay to feel this way. 💫 

Take a deep breath with me... in through your nose... and out through your mouth. 

Sometimes anger is just sadness or fear wearing a loud jacket. What happened that made you feel this way? 

I'm here to listen, no judgment, just love.""",
            'tips': [
                "🚶 Step away for 10 minutes if you can - distance helps",
                "✍️ Write down what you're feeling, then tear the paper",
                "💦 Splash cold water on your face - it's refreshing",
                "🌬️ Take three deep breaths right now",
                "👂 Talk to someone who will just listen"
            ]
        }
    
    # Anxiety/Worry
    elif any(word in message_lower for word in ['anxious', 'worry', 'nervous', 'scared', 'fear', 'panic', 'overthink', 'stress']):
        return {
            'emotion': 'Anxiety',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': f"""Oh my dear, anxiety can feel so overwhelming. 🦋 

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
    
    # Tired/Burnout
    elif any(word in message_lower for word in ['tired', 'exhausted', 'burnout', 'no energy', 'drained', 'sleep', 'fatigue']):
        return {
            'emotion': 'Burnout/Exhaustion',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': f"""Oh sweetheart, you sound so tired. Your body and mind are telling you they need rest. 🌙 

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
    
    # Relationship Issues
    elif any(word in message_lower for word in ['relationship', 'boyfriend', 'girlfriend', 'partner', 'friend', 'fight', 'argument', 'love', 'breakup']):
        return {
            'emotion': 'Relationship Concern',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': f"""Relationships can be so beautiful and so hard at the same time, can't they? 💝 

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
    
    # Default response for general conversations
    else:
        responses = [
            f"""Thank you for sharing with me, dear. 🤍 Sometimes just saying things out loud helps us understand our own feelings better. I'm here to listen, not to judge. How are you feeling right now, in this moment? Take your time.""",
            
            f"""I'm here, sweetheart. 🌸 You don't have to have the perfect words. Just being here, reaching out - that's brave. Tell me more about what's on your mind.""",
            
            f"""I hear you, love. 💫 Whatever you're feeling right now is valid. There's no right or wrong way to feel. Would you like to tell me more? I'm listening with my whole heart."""
        ]
        
        return {
            'emotion': 'Gentle Conversation',
            'stress_score': stress_score,
            'stress_level': stress_level,
            'stress_icon': level_icon,
            'caring_response': random.choice(responses),
            'tips': [
                "🌬️ Take three deep breaths right now",
                "💧 Drink a glass of water - it's self-care",
                "🌟 You're doing the best you can, and that's wonderful",
                "💝 This moment is yours - be gentle with yourself",
                "🌈 I'm proud of you for reaching out"
            ]
        }