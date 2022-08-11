from .thrower_dragon import ThrowerDragon


class ScaryThrower(ThrowerDragon):
    """ThrowerDragon that intimidates Terminators, making them back away instead of advancing."""

    name = 'Scary'
    # BEGIN 4.4
    implemented = False  # Change to True to view in the GUI

    # END 4.4

    def throw_at(self, target):
        # BEGIN 4.4
        "*** YOUR CODE HERE ***"
        # END 4.4
