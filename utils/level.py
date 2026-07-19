def get_needed_xp(level):

    return level * 100



def check_level_up(user):

    leveled_up = False


    needed = get_needed_xp(
        user["level"]
    )


    while user["xp"] >= needed:

        user["xp"] -= needed

        user["level"] += 1

        leveled_up = True


        needed = get_needed_xp(
            user["level"]
        )


    return leveled_up