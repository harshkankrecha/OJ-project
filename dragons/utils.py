import random


def random_or_none(s):
    """Return a random element of sequence S, or return None if S is empty."""
    assert isinstance(s, list), \
        "random_or_none's argument should be a list but was a %s" % type(
            s).__name__
    if s:
        return random.choice(s)


def dragons_win():
    """Signal that Dragons win."""
    raise DragonsWinException()


def terminators_win():
    """Signal that Terminators win."""
    raise TerminatorsWinException()


def make_slow(action, terminator):
    """Return a new action method that calls ACTION every other turn.

    action -- An action method of some Terminator
    """
    # BEGIN 4.4
    "*** YOUR CODE HERE ***"
    # END 4.4


def make_scare(action, terminator):
    """Return a new action method that makes the terminator go backwards.

    action -- An action method of some Terminator
    """
    # BEGIN 4.4
    "*** YOUR CODE HERE ***"
    # END 4.4


def apply_effect(effect, terminator, duration):
    """Apply a status effect to a TERMINATOR that lasts for DURATION turns."""
    # BEGIN 4.4
    "*** YOUR CODE HERE ***"
    # END 4.4


class GameOverException(Exception):
    """Base game over Exception."""
    pass


class DragonsWinException(GameOverException):
    """Exception to signal that the dragons win."""
    pass


class TerminatorsWinException(GameOverException):
    """Exception to signal that the terminators win."""
    pass


def class_method_wrapper(method, pre=None, post=None):
    """Given a class METHOD and two wrapper function, a PRE-function and
    POST-function, first calls the pre-wrapper, calls the wrapped class method,
    and then calls the post-wrapper.

    All wrappers should have the parameters (self, rv, *args). However,
    pre-wrappers will always have `None` passed in as `rv`, since a return
    value has not been evaluated yet.

    >>> def pre_wrapper(instance, rv, *args):
    ...     print('Pre-wrapper called: {0}'.format(args))
    >>> def post_wrapper(instance, rv, *args):
    ...     print('Post-wrapper called: {0} -> {1}'.format(args, rv))
    >>> class Foo(object):
    ...     def __init__(self):
    ...         self.bar = 20
    ...     def method(self, var1, var2):
    ...         print('Original method called')
    ...         return var1 + var2 + self.bar
    >>> Foo.method = class_method_wrapper(Foo.method, pre_wrapper, post_wrapper)
    >>> f = Foo()
    >>> x = f.method(1, 2)
    Pre-wrapper called: (1, 2)
    Original method called
    Post-wrapper called: (1, 2) -> 23
    >>> x
    23
    """

    def wrapped_method(self, *args):
        pre(self, None, *args) if pre else None
        rv = method(self, *args)
        post(self, rv, *args) if post else None
        return rv

    return wrapped_method


def print_expired_fighters(self, rv, *args):
    """Post-wrapper for Fighter.reduce_armor, and will print a message if the
    fighter has expired (armor reduced to 0).

    >>> from dragons import Fighter, Terminator, ThrowerDragon, Place
    >>> Fighter.reduce_armor = class_method_wrapper(Fighter.reduce_armor,
    ...         pre=print_expired_fighters)
    >>> place = Place('Test')
    >>> terminator = Terminator(3)
    >>> place.add_fighter(terminator)
    >>> terminator.reduce_armor(2)
    >>> terminator.reduce_armor(1)
    Terminator(Test) ran out of armor and expired
    >>> thrower = ThrowerDragon()
    >>> place.add_fighter(thrower)
    >>> thrower.reduce_armor(1)
    ThrowerDragon(Test) ran out of armor and expired
    """
    if self.armor <= args[0]:
        print('{0}({1}) ran out of armor and expired'.format(
            type(self).__name__, self.place))


def print_thrower_target(self, rv, *args):
    """Prints the target of a ThrowerDragon, if the ThrowerDragon found a target.

    >>> from dragons import *
    >>> skynet = Skynet(AssaultPlan())
    >>> dimensions = (1, 9)
    >>> colony = DragonColony(None, skynet, dragon_types(), dry_layout, dimensions)
    >>> ThrowerDragon.nearest_terminator = class_method_wrapper(ThrowerDragon.nearest_terminator,
    ...         post=print_thrower_target)
    >>> thrower = ThrowerDragon()
    >>> short = ShortThrower()
    >>> terminator = Terminator(5)
    >>> colony.places['tunnel_0_1'].add_fighter(short)
    >>> colony.places['tunnel_0_0'].add_fighter(thrower)
    >>> colony.places['tunnel_0_5'].add_fighter(terminator)
    >>> thrower.action(colony)
    ThrowerDragon(1, tunnel_0_0) targeted Terminator(5, tunnel_0_5)
    >>> short.action(colony)    # Terminator not in range of ShortThrower
    >>> terminator.action(colony)      # Terminator moves into range
    >>> short.action(colony)
    ShortThrower(1, tunnel_0_1) targeted Terminator(4, tunnel_0_4)
    """
    if rv is not None:
        print('{0} targeted {1}'.format(self, rv))
