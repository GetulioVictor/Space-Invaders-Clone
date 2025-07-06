settings = {
    "volume": 0.5,
    "fullscreen": False,
    "selected_level": 1,
    "player_name": "",
    "last_score": 0
}

def change_volume(delta):
    settings["volume"] = max(0.0, min(1.0, settings["volume"] + delta))

def toggle_fullscreen():
    settings["fullscreen"] = not settings["fullscreen"]

def set_player_name(name):
    settings["player_name"] = name

def set_last_score(score):
    settings["last_score"] = score
