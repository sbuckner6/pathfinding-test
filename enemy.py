import random
import numpy as np
from game_functions import distance
from mobile_game_object import MobileGameObject

class Enemy(MobileGameObject):

    grid = []
    last_player_location = None

    def __init__(self, game, x, y, width, height, color):
        MobileGameObject.__init__(self, game, x, y, width, height, color)
        self.path = []
        self.player_dx = 0
        self.player_dy = 0
        self.chasing = True
        self.target = self.get_random_point()
        self.refresh_grid()
        self.times_collided = 0

    def get_random_point(self):
        x = random.randint(0, self.game.map_width - 1)
        y = random.randint(0, self.game.map_height - 1)
        return (x * self.game.tile_size + (self.game.tile_size >> 1),
                y * self.game.tile_size + (self.game.tile_size >> 1))


    def can_see_player(self):
        collisions = self.get_collisions_between(self.game.player.x(),
                                                 self.game.player.y(),
                                                 (255, 195, 0))
        return collisions == 0

    def can_see_target(self):
        collisions = self.get_collisions_between(self.target[0],
                                                 self.target[1],
                                                 (200, 0, 0))
        return collisions == 0

    def update(self):
        if self.can_see_player():
            self.target = (self.game.player.x(), self.game.player.y())
            self.path = []
            Enemy.last_player_location = (self.game.player.x(), self.game.player.y())
            self.chasing = True
        else:
            if self.chasing:
                # self.player_dx = self.game.player.dx >> 1
                # self.player_dy = self.game.player.dy >> 1
                self.chasing = False
                self.refresh_grid()
            if not self.can_see_target() and len(self.path) == 0:
                self.find_path()

        if distance(self.x(), self.y(), self.target[0], self.target[1]) <= 10:
            if len(self.path) > 0:
                self.target = self.path.pop()
            elif Enemy.last_player_location:
                self.target = Enemy.last_player_location
                Enemy.last_player_location = None
            else:
                self.target = self.get_random_point()
                self.refresh_grid()

        if self.target[0] < self.x():
            self.dx = -1
        else:
            self.dx = 1

        if self.target[1] < self.y():
            self.dy = -1
        else:
            self.dy = 1

        self.rect.left += self.dx
        self.rect.top += self.dy
        if self.handle_collision():
            self.times_collided += 1
        else:
            self.times_collided = 0
        if self.times_collided == 3:
            self.path = []
            self.find_path()
            self.times_collided = 0

    def get_orthogonal_neighbors(self, x, y):
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < self.game.map_width - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < self.game.map_height - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def find_path(self):
        if Enemy.last_player_location:
            self.path = [Enemy.last_player_location]
        else:
            self.path = [self.target]
        end_x = int(self.target[0] / self.game.tile_size)
        end_y = int(self.target[1] / self.game.tile_size)
        start_x = int(self.x() / self.game.tile_size)
        start_y = int(self.y() / self.game.tile_size)
        iterations = np.abs(end_x - start_x) + np.abs(end_y - start_y)
        x = start_x
        y = start_y
        visited = {}
        for iter in range(iterations):
            neighbors = self.get_orthogonal_neighbors(x, y)
            neighbors = list(filter(
                lambda n: n not in visited, neighbors))
            if len(neighbors) == 0:
                break
            dists = [Enemy.grid[i][j] for (j, i) in neighbors]
            min_index = dists.index(min(dists))
            min_neighbor = neighbors[min_index]
            x = min_neighbor[0]
            y = min_neighbor[1]
            visited[(x, y)] = True
            new_point = (x * self.game.tile_size + (self.game.tile_size >> 1),
                         y * self.game.tile_size + (self.game.tile_size >> 1))
            self.path = self.path[:1] + [new_point] + self.path[1:]

        self.target = self.path.pop()

    def refresh_grid(self):
        Enemy.grid = []

        for i in range(self.game.map_height):
            row = [999] * self.game.map_width
            Enemy.grid.append(row)

        visited = {}
        start_x = int(self.target[0] / self.game.tile_size)
        start_y = int(self.target[1] / self.game.tile_size)
        end_x = int(self.x() / self.game.tile_size)
        end_y = int(self.y() / self.game.tile_size)

        for other_object in self.game.game_objects:
            if other_object.id == self.id or other_object.id == self.game.player.id:
                continue
            other_x = int(other_object.x() / self.game.tile_size)
            other_y = int(other_object.y() / self.game.tile_size)
            visited[(other_x, other_y)] = 999

        while (start_x, start_y) in visited:
            self.target = self.get_random_point()
            start_x = int(self.target[0] / self.game.tile_size)
            start_y = int(self.target[1] / self.game.tile_size)

        queue = [(start_x, start_y, 0)]

        while len(queue) > 0:
            point = queue[0]
            x = point[0]
            y = point[1]
            # if x == end_x and y == end_y:
            #     break
            dist = point[2]
            queue = queue[1:]
            if (x, y) in visited:
                continue

            visited[(x, y)] = dist
            Enemy.grid[y][x] = dist
            neighbors = self.get_orthogonal_neighbors(x, y)
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append((neighbor[0], neighbor[1], dist + 1))

    def get_max_collide_dist(self):
        return 25 #todo: calculate this better?

    def get_collisions_between(self, x, y, debug_color=None):
        origin = np.array([self.x(), self.y()])
        delta = np.array([x, y])
        dist_self_to_target = distance(self.x(), self.y(), x, y)

        collisions = 0

        for other_object in self.game.game_objects:
            if other_object.id == self.id or other_object.id == self.game.player.id:
                continue

            object_point = np.array([other_object.x(), other_object.y()])
            dist_to_line = np.abs(np.cross(delta - origin, origin - object_point) / np.linalg.norm(delta - origin))
            dist_obj_to_self = distance(self.x(), self.y(), other_object.x(), other_object.y())

            if dist_to_line <= self.get_max_collide_dist() \
                    and dist_obj_to_self < dist_self_to_target \
                    and (other_object.x() - self.x()) ^ (x - self.x()) > 0 \
                    and (other_object.y() - self.y()) ^ (y - self.y()) > 0 :
                collisions += 1
                if self.game.debug and debug_color:
                    other_object.color = debug_color
            elif self.game.debug and other_object.color == debug_color:
                other_object.color = other_object.old_color

        return collisions