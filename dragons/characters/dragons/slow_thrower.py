from .thrower_dragon import ThrowerDragon
from utils import apply_effect, make_slow


class SlowThrower(ThrowerDragon):
    """ThrowerDragon that causes Slow on Terminators."""

    name = 'Slow'
    # BEGIN 4.4
    implemented = False  # Change to True to view in the GUI

    # END 4.4

    def throw_at(self, target):
        if target:
            apply_effect(make_slow, target, 3)
