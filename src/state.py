from enum import Enum


class State(Enum):
    NoChanges = 0
    GeneratingTest = 1
    Testing = 2
    Statistics = 3
    EndRunning = 4
