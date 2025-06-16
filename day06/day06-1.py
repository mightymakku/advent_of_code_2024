from typing import Literal, Tuple
from dataclasses import dataclass
from enum import Enum


class MapEntry(Enum):
    FREE: str = '.'
    OBSTACLE: str = '#'
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


class PatrolPathPredicter:
    def __init__(self, initial_map: list[list[MapEntry]]) -> None:
        self._map = initial_map
        self._current_guard_state = None
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

        if self._map[ty][tx] == MapEntry.OBSTACLE:
            tdir = self._get_new_guard_direction()
            tx, ty = (self._current_guard_state.x, self._current_guard_state.y)

        return GuardState(x=tx, y=ty, direction=tdir)

    def print_current_map(self) -> None:
        for r in self._map:
            print(''.join((c.value for c in r)))

    def perform_action(self) -> bool:
        if self._current_guard_state is None:
            return False
        self._map[self._current_guard_state.y][self._current_guard_state.x] = MapEntry.PATROL_ROUTE

        new_guard_state = self._get_new_guard_state()
        if new_guard_state is not None:
            self._map[new_guard_state.y][new_guard_state.x] = new_guard_state.direction
        self._current_guard_state = new_guard_state

        return True

    def predict_patrol_path(self) -> None:
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
    map = read_input(sys.argv[1])
    ppp = PatrolPathPredicter(map)
    ppp.predict_patrol_path()

    print()
    ppp.print_current_map()
    print()
    print(f'{ppp.patrol_fields_count=}')
