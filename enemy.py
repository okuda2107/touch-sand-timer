from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import copy
import random
from actor import Actor
from sprite_component import SpriteComponent
from circle_component import CircleComponent, Kind
from collision import Sphere

if TYPE_CHECKING:
    from game import Game

class Enemy(Actor):
    def __init__(self, game: Game):
        super().__init__(game)
        self.forward: np.array = np.array([0.0, 0.0])
        self.speed = random.uniform(0, 2)
        sc = SpriteComponent(self)
        sc.set_image('asset/white.png', (20, 20))
        cc = CircleComponent(self, Kind.enemy)
        sphere = Sphere()
        sphere.center = self.position
        sphere.radius = sc.image_size[0] / self.game.screen_size[0]
        cc.set_sphere(sphere)

    def __del__(self):
        return super().__del__()
    
    def update_actor(self, delta_time: float) -> None:
        super().update_actor(delta_time)
        pre_position = copy.deepcopy(self.position)
        self.position = self.position + self.forward * self.speed * delta_time
        if ((self.position <= np.zeros(2)) | (np.ones(2) <= self.position)).any() and ((np.zeros(2) < pre_position) & (pre_position < np.ones(2))).any():
            if self.position[0] <= 0 or self.position[0] >= 1:
                self.forward[0] *= -1
            if self.position[1] <= 0 or self.position[1] >= 1:
                self.forward[1] *= -1