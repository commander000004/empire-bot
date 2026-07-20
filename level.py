# level.py


def xp_need(level):

    return level * level * 100



def check_level(user):

    level_up = False


    while user["xp"] >= xp_need(user["level"]):

        user["xp"] -= xp_need(
            user["level"]
        )

        user["level"] += 1

        level_up = True


    return level_up