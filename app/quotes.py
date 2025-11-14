# ===== FILE: app/quotes.py =====
from datetime import datetime

ANIME_QUOTES = [
    {"anime": "Haikyu!!", "quote": "Being the best decoy ever is as cool as being the ace."},
    {"anime": "Run with the Wind", "quote": "We run because we love to run, not because we're fast."},
    {"anime": "Kuroko's Basketball", "quote": "Individual ability is important, but teamwork is everything."},
    {"anime": "My Hero Academia", "quote": "Plus Ultra! Go beyond, plus ultra!"},
    {"anime": "Attack on Titan", "quote": "Shinzou wo Sasageyo! Give your hearts!"},
    {"anime": "Demon Slayer", "quote": "Don't give up. Keep moving forward."},
    {"anime": "Jujutsu Kaisen", "quote": "I want the kind of death where I have no regrets."},
    {"anime": "Naruto", "quote": "Hard work is worthless for those that don't believe in themselves."},
    {"anime": "One Piece", "quote": "Being alone is more painful than getting hurt."},
    {"anime": "Death Note", "quote": "The only way to fight evil is with evil."},
    {"anime": "Bleach", "quote": "No matter how far you run, the past always catches up."},
    {"anime": "Soul Eater", "quote": "Let's make a team and become stronger!"},
    {"anime": "Fairy Tail", "quote": "I'm not fighting to win. I'm fighting because I can't lose!"},
    {"anime": "Black Clover", "quote": "I'm never giving up!"},
    {"anime": "Fire Force", "quote": "Protect what matters most to you."},
    {"anime": "Tower of God", "quote": "Climb higher, become stronger."},
    {"anime": "Vinland Saga", "quote": "Revenge is like a deep fog that clouds the eyes."},
    {"anime": "The Rising of the Shield Hero", "quote": "I must move forward, no matter what."},
    {"anime": "Solo Leveling", "quote": "The only way out is forward."},
    {"anime": "Sword Art Online", "quote": "Don't lose! Keep going forward!"},
    {"anime": "Assassination Classroom", "quote": "Every moment is precious."},
    {"anime": "Code Geass", "quote": "The power to change the world rests in determination."},
    {"anime": "Gurren Lagann", "quote": "Believe in the me that believes in you!"},
    {"anime": "Evangelion", "quote": "I mustn't run away. I mustn't run away."},
    {"anime": "Fullmetal Alchemist", "quote": "Some think it's cruel to love what can't be saved."},
    {"anime": "Hunter x Hunter", "quote": "I'm not gonna run. I'm gonna walk forward."},
    {"anime": "Dragon Ball Z", "quote": "I'll never give up!"},
    {"anime": "JoJo's Bizarre Adventure", "quote": "GURETO DAZE! That's great!"},
    {"anime": "Mob Psycho 100", "quote": "Let's do our best today!"},
    {"anime": "Steins;Gate", "quote": "I am mad scientist. It's so cool!"},
] + [
    {"anime": "Generic Motivation", "quote": f"Day {i}: Every step forward counts. Keep pushing!"}
    for i in range(470)
]

class QuoteEngine:
    def __init__(self):
        self.quotes = ANIME_QUOTES
    
    def get_daily_quote(self):
        today = datetime.now().day
        idx = today % len(self.quotes)
        return self.quotes[idx]