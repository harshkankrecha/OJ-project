test = {
  'name': 'phase_1',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> Dragon.food_cost
          0
          >>> HarvesterDragon.food_cost
          2
          >>> ThrowerDragon.food_cost
          3
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing HarvesterDragon action
          >>> # Note that initializing a Dragon here doesn't cost food, only
          >>> # deploying a Dragon in the game simulation does
          >>> #
          >>> # Create a test layout where the colony is a single row with 9 tiles
          >>> skynet = Skynet(make_test_assault_plan())
          >>> colony = DragonColony(None, skynet, dragon_types(), dry_layout, (1, 9))
          >>> #
          >>> colony.food = 4
          >>> harvester = HarvesterDragon()
          >>> harvester.action(colony)
          >>> colony.food
          5
          >>> harvester.action(colony)
          >>> colony.food
          6
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      >>> from assault_plans import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from dragons import *
          >>> HarvesterDragon.implemented
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Simple test for Place
          >>> place0 = Place('place_0')
          >>> print(place0.exit)
          None
          >>> print(place0.entrance)
          None
          >>> place1 = Place('place_1', place0)
          >>> place1.exit is place0
          True
          >>> place0.entrance is place1
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing if entrances are properly initialized
          >>> tunnel_len = 9
          >>> len(colony.terminator_entrances)
          1
          >>> tile_1 = colony.terminator_entrances[0]
          >>> tile_2 = tile_1.exit
          >>> tile_3 = tile_2.exit
          >>> tile_1.entrance is colony.skynet
          True
          >>> tile_1.exit is tile_2
          True
          >>> tile_2.entrance is tile_1
          True
          >>> tile_2.exit is tile_3
          True
          >>> tile_3.entrance is tile_2
          True
          >>> tile_3.exit is colony.base
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      >>> from assault_plans import *
      >>> #
      >>> # Create a test layout where the colony is a single row with 3 tiles
      >>> skynet, layout = Skynet(make_test_assault_plan()), dry_layout
      >>> dimensions = (1, 3)
      >>> colony = DragonColony(None, skynet, dragon_types(), layout, dimensions)
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing nearest_terminator
          >>> near_terminator = Terminator(2) # A Terminator with 2 armor
          >>> far_terminator = Terminator(3)  # A Terminator with 3 armor
          >>> near_place = colony.places['tunnel_0_3']
          >>> far_place = colony.places['tunnel_0_6']
          >>> near_place.add_fighter(near_terminator)
          >>> far_place.add_fighter(far_terminator)
          >>> nearest_terminator = thrower.nearest_terminator(colony.skynet)
          >>> thrower.nearest_terminator(colony.skynet) is far_terminator
          False
          >>> thrower.nearest_terminator(colony.skynet) is near_terminator
          True
          >>> nearest_terminator.armor
          2
          >>> thrower.action(colony)    # Attack! ThrowerDragons do 1 damage
          >>> near_terminator.armor
          1
          >>> far_terminator.armor
          3
          >>> thrower.place is dragon_place    # Don't change self.place!
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing Nearest terminator not in the skynet
          >>> skynet = colony.skynet
          >>> terminator = Terminator(2)
          >>> skynet.add_fighter(terminator)      # Adding a terminator to the skynet
          >>> thrower.nearest_terminator(skynet) is terminator
          False
          >>> thrower.action(colony)    # Attempt to attack
          >>> terminator.armor                 # Terminator armor should not change
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Test that ThrowerDragon attacks terminators on its own square
          >>> near_terminator = Terminator(2)
          >>> dragon_place.add_fighter(near_terminator)
          >>> thrower.nearest_terminator(colony.skynet) is near_terminator
          True
          >>> thrower.action(colony)   # Attack!
          >>> near_terminator.armor           # should do 1 damage
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Test that ThrowerDragon attacks terminators at end of tunnel
          >>> near_terminator = Terminator(2)
          >>> colony.places["tunnel_0_8"].add_fighter(near_terminator)
          >>> thrower.nearest_terminator(colony.skynet) is near_terminator
          True
          >>> thrower.action(colony)   # Attack!
          >>> near_terminator.armor           # should do 1 damage
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Test that ThrowerDragon attacks terminators 4 places away
          >>> near_terminator = Terminator(2)
          >>> colony.places["tunnel_0_4"].add_fighter(near_terminator)
          >>> thrower.nearest_terminator(colony.skynet) is near_terminator
          True
          >>> thrower.action(colony)   # Attack!
          >>> near_terminator.armor           # should do 1 damage
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing ThrowerDragon chooses a random target
          >>> terminator1 = Terminator(1001)
          >>> terminator2 = Terminator(1001)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator1)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator2)
          >>> # Throw 1000 times. The first terminator should take ~1000*1/2 = ~500 damage,
          >>> # and have ~501 remaining.
          >>> for _ in range(1000):
          ...     thrower.action(colony)
          >>> # Test if damage to terminator1 is within 6 standard deviations (~95 damage)
          >>> # If terminators are chosen uniformly, this is true 99.9999998% of the time.
          >>> def dmg_within_tolerance():
          ...     return abs(terminator1.armor-501) < 95
          >>> dmg_within_tolerance()
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      >>> skynet, layout = Skynet(AssaultPlan()), dry_layout
      >>> dimensions = (1, 9)
      >>> colony = DragonColony(None, skynet, dragon_types(), layout, dimensions)
      >>> thrower = ThrowerDragon()
      >>> dragon_place = colony.places["tunnel_0_0"]
      >>> dragon_place.add_fighter(thrower)
      >>> #
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from dragons import *
          >>> ThrowerDragon.implemented
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
