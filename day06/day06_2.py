from typing import Literal, Tuple
from dataclasses import dataclass
from enum import Enum


class MapEntry(Enum):
    FREE: str = '.'
    OBSTACLE: str = '#'
    EXTRA_OBSTACLE: str = 'O'
    PATROL_ROUTE: str = 'X'
    GUARD_NORTH: str = '^'
    GUARD_EAST: str = '>'
    GUARD_SOUTH: str = 'v'
    GUARD_WEST: str = '<'


@dataclass
class GuardState:
    x: int
    y: int
    direction: Literal[MapEntry.GUARD_NORTH, MapEntry.GUARD_EAST, MapEntry.GUARD_SOUTH, MapEntry.GUARD_WEST]

    def __eq__(self, other: 'GuardState'):
        return (self.x, self.y, self.direction) == (other.x, other.y, other.direction)

    def __hash__(self):
        return hash(self.x) ^ hash(self.y) ^ hash(self.direction)


class LoopError(Exception):
    pass


class PatrolPathPredicter:
    def __init__(self, initial_map: list[list[MapEntry]]) -> None:
        self._map = initial_map
        self._current_guard_state = None
        self._prediction_complete = False
        self._guard_state_history: set[GuardState] = set()
        for y in range(len(self._map)):
            for x in range(len(self._map[y])):
                v = self._map[y][x]
                if v in (MapEntry.GUARD_NORTH, MapEntry.GUARD_EAST, MapEntry.GUARD_SOUTH, MapEntry.GUARD_WEST):
                    self._current_guard_state = GuardState(x=x, y=y, direction=v)

    def _get_target_xy(self) -> Tuple[int, int] | None:
        x = self._current_guard_state.x
        y = self._current_guard_state.y

        match self._current_guard_state.direction:
            case MapEntry.GUARD_NORTH:
                y -= 1
            case MapEntry.GUARD_EAST:
                x += 1
            case MapEntry.GUARD_SOUTH:
                y += 1
            case MapEntry.GUARD_WEST:
                x -= 1
            case _:
                pass

        if x < 0 or x >= len(self._map[0]):
            return None
        if y < 0 or y >= len(self._map):
            return None

        return (x, y)

    def _get_new_guard_direction(self) -> Literal[MapEntry.GUARD_NORTH, MapEntry.GUARD_EAST, MapEntry.GUARD_SOUTH, MapEntry.GUARD_WEST]:
        match self._current_guard_state.direction:
            case MapEntry.GUARD_NORTH:
                return MapEntry.GUARD_EAST
            case MapEntry.GUARD_EAST:
                return MapEntry.GUARD_SOUTH
            case MapEntry.GUARD_SOUTH:
                return MapEntry.GUARD_WEST
            case MapEntry.GUARD_WEST:
                return MapEntry.GUARD_NORTH

    def _get_new_guard_state(self) -> GuardState | None:
        target_xy = self._get_target_xy()

        if target_xy is None:
            return None

        tx, ty = target_xy
        tdir = self._current_guard_state.direction

        if self._map[ty][tx] in (MapEntry.OBSTACLE, MapEntry.EXTRA_OBSTACLE):
            tdir = self._get_new_guard_direction()
            tx, ty = (self._current_guard_state.x, self._current_guard_state.y)

        return GuardState(x=tx, y=ty, direction=tdir)

    def print_current_map(self) -> None:
        for r in self._map:
            print(''.join((c.value for c in r)))

    def perform_action(self) -> bool:
        if self._current_guard_state is None:
            self._prediction_complete = True
            return False
        self._map[self._current_guard_state.y][self._current_guard_state.x] = MapEntry.PATROL_ROUTE

        new_guard_state = self._get_new_guard_state()
        if new_guard_state is not None:
            if new_guard_state in self._guard_state_history:
                raise LoopError('Loop detected')
            self._guard_state_history.add(new_guard_state)
            self._map[new_guard_state.y][new_guard_state.x] = new_guard_state.direction
        self._current_guard_state = new_guard_state

        return True

    def predict_patrol_path(self) -> None:
        if self._prediction_complete:
            return
        while self.perform_action():
            pass

    @property
    def patrol_fields_count(self):
        flattened = [c for r in self._map for c in r]
        return flattened.count(MapEntry.PATROL_ROUTE)


def read_input(filepath: str) -> list[list[MapEntry]]:
    map = []
    with open(filepath, 'r') as f:
        for line in f:
            map.append([MapEntry(c) for c in line.strip()])
    return map


if __name__ == '__main__':
    import sys
    import copy
    map = read_input(sys.argv[1])

    ppp = PatrolPathPredicter(copy.deepcopy(map))
    ppp.predict_patrol_path()

    coords_of_interest = set((gs.x, gs.y) for gs in ppp._guard_state_history)

    total_maps_to_test = len(coords_of_interest) - 1
    i = 0
    loops_detected = 0

    for x, y in coords_of_interest:
        loop_ppp = PatrolPathPredicter(copy.deepcopy(map))
        if loop_ppp._map[y][x] not in (MapEntry.GUARD_NORTH, MapEntry.GUARD_EAST, MapEntry.GUARD_SOUTH, MapEntry.GUARD_WEST):
            i += 1
            print(f'Predicting map {i} of {total_maps_to_test}...')
            loop_ppp._map[y][x] = MapEntry.EXTRA_OBSTACLE
            try:
                loop_ppp.predict_patrol_path()
            except LoopError:
                print('Loop detected!')
                loops_detected += 1
    print(f'{loops_detected=}')
