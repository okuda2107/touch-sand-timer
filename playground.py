from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np
import random
from actor import Actor, state
from collision import intersect
from circle_component import Kind
from core import Core
from pointer import Pointer
from enemy_generator import EnemyGenerator
from result import Result
from text_component import TextComponent

if TYPE_CHECKING:
    from game import Game

class PlayGround(Actor):
    def __init__(self, game: Game):
        super().__init__(game)
        self.cores: list[Core] = []
        self.pointers: list[Pointer] = []
        self.counter = Actor(self.game)
        self.counter.position = self.game.screen_size * [0.45, 0.4]
        self.counter_text = TextComponent(self.counter, 100)
        self.counter_text.set_color((255, 255, 255))
        self.counter_text.set_font('asset/DSEG14ClassicMini-Italic.ttf')
        self.counter_text.set_text('3')
        self.start_flag = False
        self.timer = 3

        self.enemy_gen = EnemyGenerator(self.game)
        self.enemy_gen.state = state.paused
        self.actor = Actor(self.game)
        self.actor.position = self.game.screen_size * [0, 0]
        self.tc = TextComponent(self.actor, 80)
        self.tc.set_font('asset/DSEG14ClassicMini-Italic.ttf')
        self.tc.set_color((255, 255, 255))

    def __del__(self):
        super().__del__()

    def load_properties(self, obj: dict[str, Any]) -> None:
        super().load_properties(obj)
        core_num = obj.get('coreNum')
        if core_num != None and type(core_num) is int:
            rng = np.random.default_rng()
            for _ in range(core_num):
                core = Core(self.game)
                core.position = self.game.screen_size * rng.uniform(0.3, 0.7, 2)
                core.state = state.paused
                self.cores.append(core)
        pointer_nums = obj.get('pointers')
        if pointer_nums != None:
            for p in pointer_nums:
                self.pointers.append(Pointer(self.game, p))

    def update_actor(self, delta_time: float) -> None:
        super().update_actor(delta_time)
        if not self.start_flag:
            self.timer -= delta_time
            if self.timer <= -1:
                self.start_game()
            elif self.timer <= 0:
                self.counter_text.set_text('Go!!!')
            elif self.timer <= 1:
                self.counter_text.set_text('1')
            elif self.timer <= 2:
                self.counter_text.set_text('2')
            return
        self.enemy_gen.target_pos = random.choice(self.cores).position
        self.timer += delta_time
        self.tc.set_text('Time: ' + str(round(self.timer, 1)))
        circles = self.game.physics.circles
        for p in circles[Kind.pointer.value]:
            for c in circles[Kind.core.value]:
                if intersect(p.circle, c.circle):
                    self.next_scene()
                    return
                for e in circles[Kind.enemy.value]:
                    if intersect(p.circle, e.circle):
                        e.get_owner().state = state.dead
                    if intersect(c.circle, e.circle):
                        self.next_scene()
                        return

    def start_game(self):
        self.start_flag = True
        self.timer = 0
        self.counter.state = state.dead
        self.enemy_gen.state = state.active
        for core in self.cores:
            core.state = state.active
        self.tc.set_text('Time: ' + str(round(self.timer, 1)))

    def next_scene(self):
        self.state = state.dead
        self.actor.state = state.dead
        for c in self.cores:
            c.state = state.dead
        for p in self.pointers:
            p.state = state.dead
        self.enemy_gen.state = state.dead
        for e in self.enemy_gen.enemies:
            e.state = state.dead
        Result(self.game, 'Time: ' + str(round(self.timer, 1)))
