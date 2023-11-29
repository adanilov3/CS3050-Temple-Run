import arcade

"""
Collision Function. Checks Object Type, checks for a collision with the player and offsets by the
Object type. Returns true if the collision still applies and false if not.
"""
def runner_collision(player, other, is_jump, is_slide):
    # Check if the collision even occured, using the built in system
    collided = arcade.check_for_collision(player, other.sprite)

    if (collided == False):
        return collided

    # Determine type and check corresponding overlaps (not applicable for unspecified type)
    if (other.type == "HEAD"):
        if(is_slide):
            collided = False
    elif (other.type == "FOOT"):
        if(is_jump):
            collided = False

    return collided

def prim_collision_tree(player, other, is_jump):
    collided = False
    if other.rotating != 2:
        cy = other.y
        cx = other.x
        w = other.width / 2
        h = other.height / 2
    else:
        cy = other.py
        cx = other.x + cy
        w = other.height / 2
        h = other.width / 2
    if (player.center_x < cx + w and
            player.center_x + (player.width / 2) > cx and
            player.center_y < cy + h and
            player.center_y + (player.height / 2) > cy):
        collided = True
    if is_jump and other.rotating == 2:
        collided = False
    return collided

def prim_collision_gap(player, other, is_jump):
    collided = False
    if (player.center_x < other.x + (other.width / 2) and
            player.center_x + (player.width / 2) > other.x and
            player.center_y < other.y + (other.height / 2) and
            player.center_y + (player.height / 2) > other.y):
        collided = True
    if is_jump:
        collided = False
    return collided