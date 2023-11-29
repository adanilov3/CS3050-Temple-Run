import arcade
import random

SCREEN_HEIGHT = 700
SCREEN_CENTER = 500

"""
Quasi-Singleton class that has a list of each subtype of obstacle, as well as coins, and instantiates them
at the top of the screen at variable distances from center
"""
class Object_Randomizer:
    # Constructor
    def __init__(self, obstacles_list, coin, gap, tree, obstacle_interval, coin_interval, gap_interval, tree_interval, lhs_range, rhs_range) -> None:
        self.obstacles = obstacles_list
        self.coin = coin
        self.gap = gap
        self.tree = tree
        self.obstacle_timer = 0.0
        self.coin_timer = 0.0
        self.gap_timer = 0.0
        self.tree_timer = 0.0
        self.obstacle_interval = obstacle_interval
        self.coin_interval = coin_interval
        self.gap_interval = gap_interval
        self.tree_interval = tree_interval
        self.lhs_range = lhs_range
        self.rhs_range = rhs_range
        self.make_gap = 0
        self.max_gap = 10
        self.gap_loc = 0
        self.active_obstacles = []
        self.active_coins = []
        self.active_gaps = []
        self.active_trees = []

    # Getters and Setters for the range parameters. This lets us do paths that narrow at some points.
    def get_lhs_range(self):
        return self.lhs_range
    
    def get_rhs_range(self):
        return self.rhs_range
    
    def get_lhs_range(self, new_range):
        self.lhs_range = new_range
    
    def get_rhs_range(self, new_range):
        self.rhs_range = new_range

    
    # Tick function. Call using On_Update in the main driver
    def tick(self, delta_time, renderer):
        self.obstacle_timer += delta_time
        self.coin_timer += delta_time
        self.gap_timer += delta_time
        self.tree_timer += delta_time

        # Check if we've surpassed our interval. If so, make a new obstacle
        if(self.obstacle_timer >= self.obstacle_interval + random.uniform(0, 1) and self.make_gap == 0):
            obstacle = self.obstacles[random.randrange(0, len(self.obstacles))]
            xPos = SCREEN_CENTER + random.randrange(self.lhs_range, self.rhs_range)
            new_obstacle = obstacle(xPos, 550)
            new_obstacle.set_angle(renderer.getAngleSprite(new_obstacle.sprite))
            self.active_obstacles.append(new_obstacle)
            self.obstacle_timer = 0.0


        # See above, but for coins
        if(self.coin_timer >= self.coin_interval and self.make_gap == 0):
            xPos = SCREEN_CENTER + random.randrange(self.lhs_range, self.rhs_range)
            new_coin = self.coin(xPos, 550)
            new_coin.set_angle(renderer.getAngleSprite(new_coin.sprite))
            self.active_coins.append(new_coin)
            self.coin_timer = 0.0

        # See above, but for gaps
        if (self.gap_timer >= self.gap_interval):
            self.make_gap = 1
            self.gap_loc = random.randrange(-1, 1)
            self.gap_timer = 0

        # See above, but for trees
        if (self.tree_timer >= self.tree_interval and self.make_gap == 0):
            xPos = 425
            new_tree = self.tree(xPos, 550)
            new_tree.set_angle(renderer.getAngle(new_tree))
            self.active_trees.append(new_tree)
            self.tree_timer = 0.0

        if self.make_gap > 0:
            self.make_gap += 1
            new_gap = self.gap(1000, 775, self.gap_loc)
            new_gap.set_angle(renderer.getAngle(new_gap))
            self.active_gaps.append(new_gap)
            if (self.make_gap > 60):
                self.make_gap = 0

        for tree in self.active_trees:
            if tree.rotating == 0:
                if random.uniform(0.0000,1.0000) < 0.05 and tree.getY() < 550:
                    tree.start_rotating()
            elif tree.rotating == 1:
                tree.rotate()
