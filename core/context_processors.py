from questions.data import USERS

POPULAR_TAGS = [
    ("python", "t-big t-dark"), ("MySQL", "t-mid t-red"),
    ("perl", "t-small t-blue"), ("django", "t-big t-green"),
    ("TechnoPark", "t-mid t-dark"), ("Firefox", "t-small t-orange"),
    ("css", "t-mid t-purple"), ("VK", "t-small t-dark"),
    ("bootstrap", "t-mid t-blue"), ("nginx", "t-small t-red"),
]


def sidebar(request):
    return {"popular_tags": POPULAR_TAGS, "best_members": USERS[1:], "demo_user": USERS[0]}
