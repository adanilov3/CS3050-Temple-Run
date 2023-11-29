"""
Class that holds obstacle data. Basically just a struct with some extra data compared to the base sprite class
"""

import arcade
import math
from shapes import Path, ObstacleTree


class Object:

    def __init__(self, sprite, obj_type, center_x, center_y, h, w, scale):
        self.sprite = sprite
        self.type = obj_type
        self.sprite.center_x = center_x
        self.sprite.center_y = center_y
        self.sprite.height = h
        self.sprite.width = w
        self.sprite.angle = None
        self.sprite.scale = scale

    def set_angle(self, angle):
        self.sprite.angle = angle

    def get_sprite(self):
        return self.sprite


class Rock(Object):
    def __init__(self, center_x, center_y):
        super().__init__(arcade.Sprite(arcade.load_texture(":resources:images/space_shooter/meteorGrey_big1.png")),
                         "FOOT",
                         center_x,
                         center_y,
                         10,
                         10,
                         0.3)

class StaticTree(Object):
    def __init__(self, center_x, center_y):
        super().__init__(arcade.Sprite(arcade.load_texture("images/tree.png")),
                         "FOOT",
                         center_x,
                         center_y,
                         10,
                         10,
                         0.3)


class Coin(Object):
    def __init__(self, center_x, center_y):
        super().__init__(arcade.Sprite(arcade.load_texture(":resources:images/items/coinGold.png")),
                         None,
                         center_x,
                         center_y,
                         5,
                         5,
                         0.3)
        self.is_collected = False

class TurnTree(ObstacleTree):
    def __init__(self, center_x, center_y):
        super().__init__(center_x, center_y, 30, 150, arcade.color.WOOD_BROWN, 1, math.pi / 96, -1)

    def set_angle(self, angle):
        self.angle = angle

class Gap(Path):
    def __init__(self, w, h, l):
        super().__init__(w, h, (125, 206, 235, 255), l)

    def set_angle(self, angle):
        self.angle = angle
