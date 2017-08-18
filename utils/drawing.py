from .. preferences import get_preferences

def set_color(pref)
    bgR = get_preferences().pref[0]
    bgG = get_preferences().pref[1]
    bgB = get_preferences().pref[2]
    bgA = get_preferences().pref[3]
    glColor4f(bgR, bgG, bgB, bgA)