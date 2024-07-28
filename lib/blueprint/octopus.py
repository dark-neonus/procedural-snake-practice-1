from lib.blueprint.blueprint_object import BlueprintObject, write_to_file, read_from_file

import os
import pyglet

from lib.procedural_objects.snake import ProceduralSnake
from lib.procedural_objects.circle import ProceduralCircle
from lib.procedural_objects.octopus import Octopus
from lib.snake_behavior import SnakeBehavior, behaviours, BEH_DO_NOTHING, BEH_FOLLOW_MOUSE, BEH_MOVE_ON_ITSELF, BEH_SET_POS

from typing import Dict, List

class OctopusBlueprint(BlueprintObject):
    def __init__(
            self,
            head_sizes: None | List[int] = None,
            tentacle_lengths: None | List[int] = None,
            tentacle_angles: None | List[int] = None,
            tentacle_start_size: int = None,
            tentacle_size_reduction: float = None,
            fill_color: tuple = None
            ) -> None:

        self.head_sizes = head_sizes
        self.tentacle_lengths = tentacle_lengths
        self.tentacle_angles = tentacle_angles
        
        self.tentacle_start_size = tentacle_start_size
        self.tentacle_size_reduction = tentacle_size_reduction

        if self.tentacle_angles is not None:
            if len(self.tentacle_angles) != len(self.tentacle_lengths):
                raise ValueError("Tentacle angles and lengths should have the same length!")

            for i in range(len(tentacle_lengths)):
                if self.tentacle_start_size - self.tentacle_size_reduction * tentacle_lengths[i] < 0:
                    raise ValueError("Tentacle at index \"{i}\" start size is too small or reduction is too big! ")

        self.fill_color = fill_color

    def __dict__(self) -> dict:
        return {
            "head_sizes": self.head_sizes,
            "tentacle_lengths": self.tentacle_lengths,
            "tentacle_angles": self.tentacle_angles,
            "tentacle_start_size": self.tentacle_start_size,
            "tentacle_size_reduction": self.tentacle_size_reduction,
            "fill_color": self.fill_color
        }
    
    def load(self, path: os.path) -> None:
        dictionary = read_from_file(path)

        self.head_sizes = dictionary["head_sizes"]
        self.tentacle_lengths = dictionary["tentacle_lengths"]
        self.tentacle_angles = dictionary["tentacle_angles"]
        self.tentacle_start_size = dictionary["tentacle_start_size"]
        self.tentacle_size_reduction = dictionary["tentacle_size_reduction"]
        self.fill_color = dictionary["fill_color"]

    def create_octopus(
            self,
            batch: pyglet.graphics.Batch,
            debug_draw: bool = False,
            behavior: int = BEH_DO_NOTHING,
            additional_tentacle_calculation_radius = 0
            ) -> Octopus:
        
        head_segments: List[ProceduralCircle] = [ProceduralCircle(
                calculation_radius=head_size // 2, radius=head_size
            ) for head_size in self.head_sizes]

        head: ProceduralSnake = ProceduralSnake(
            segments=head_segments,
            batch=batch,
            debug_draw=debug_draw,
            fill_color=self.fill_color,
            behavior=behavior
            )

        tentacles: Dict[float, ProceduralSnake] = {}
        for i in range(len(self.tentacle_lengths)):
            segments = [ProceduralCircle(
                    calculation_radius= (self.tentacle_start_size + additional_tentacle_calculation_radius - int(self.tentacle_size_reduction * j)) * 1.5,
                    radius=(self.tentacle_start_size - self.tentacle_size_reduction * j)
                ) for j in range(self.tentacle_lengths[i])]

            tentacles[self.tentacle_angles[i]] = ProceduralSnake(
                segments=segments,
                batch=batch,
                debug_draw=debug_draw,
                fill_color=self.fill_color,
                behavior=BEH_SET_POS
                )

        res = Octopus(
            head=head,
            tentacles=tentacles,
            debug_draw=debug_draw,
            behavior=behavior
        )

        return res