from __future__ import annotations
from component import Component
from collision import AABB
from actor import Actor

class BoxComponent(Component):
    def __init__(self, owner: Actor):
        super().__init__(owner)
        self._owner.game.physics.add_box(self)
        self.__object_box: AABB = None
        self.__world_box: AABB = None

    def __del__(self):
        self._owner.game.physics.remove_box(self)
        super().__del__()

    def update(self, delta_time: float):
        self.__world_box = self.__object_box
        self.__world_box.min_pos *= self._owner.scale
        self.__world_box.max_pos *= self._owner.scale
        self.__world_box.min_pos += self._owner.position
        self.__world_box.max_pos += self._owner.position

    def set_object_box(self, model: AABB):
        self.__object_box = model

    def get_world_box(self):
        return self.__world_box
