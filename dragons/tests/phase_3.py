test = {
  'name': 'phase_3',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing EarthDragon parameters
          >>> earth = EarthDragon()
          >>> earth.name
          'Earth'
          >>> earth.armor
          4
          >>> # `armor` should not be a class attribute
          >>> not hasattr(EarthDragon, 'armor')
          True
          >>> EarthDragon.food_cost
          4
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing EarthDragon holds strong
          >>> skynet, layout = Skynet(AssaultPlan()), dry_layout
          >>> colony = DragonColony(None, skynet, dragon_types(), layout, (1, 9))
          >>> place = colony.places['tunnel_0_4']
          >>> earth = EarthDragon()
          >>> terminator = Terminator(1000)
          >>> place.add_fighter(earth)
          >>> place.add_fighter(terminator)
          >>> for i in range(3):
          ...     terminator.action(colony)
          ...     earth.action(colony)   # EarthDragon does nothing
          >>> earth.armor
          1
          >>> terminator.armor
          1000
          >>> earth.place is place
          True
          >>> terminator.place is place
          True
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from dragons import *
          >>> EarthDragon.implemented
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
          >>> # Testing BodyguardDragon parameters
          >>> bodyguard = BodyguardDragon()
          >>> BodyguardDragon.food_cost
          4
          >>> bodyguard.armor
          2
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> bodyguard = BodyguardDragon()
          >>> bodyguard.action(colony) # Action without contained dragon should not error
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguard performs thrower's action
          >>> bodyguard = BodyguardDragon()
          >>> thrower = ThrowerDragon()
          >>> terminator = Terminator(2)
          >>> # Place bodyguard before thrower
          >>> colony.places["tunnel_0_0"].add_fighter(bodyguard)
          >>> colony.places["tunnel_0_0"].add_fighter(thrower)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator)
          >>> bodyguard.action(colony)
          >>> terminator.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguard performs thrower's action
          >>> bodyguard = BodyguardDragon()
          >>> thrower = ThrowerDragon()
          >>> terminator = Terminator(2)
          >>> # Place thrower before bodyguard
          >>> colony.places["tunnel_0_0"].add_fighter(thrower)
          >>> colony.places["tunnel_0_0"].add_fighter(bodyguard)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator)
          >>> bodyguard.action(colony)
          >>> terminator.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing removing a bodyguard doesn't remove contained dragon
          >>> place = colony.places['tunnel_0_0']
          >>> bodyguard = BodyguardDragon()
          >>> test_dragon = Dragon(1)
          >>> # add bodyguard first
          >>> place.add_fighter(bodyguard)
          >>> place.add_fighter(test_dragon)
          >>> colony.remove_dragon('tunnel_0_0')
          >>> place.dragon is test_dragon
          True
          >>> bodyguard.place is None
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing removing a bodyguard doesn't remove contained dragon
          >>> place = colony.places['tunnel_0_0']
          >>> bodyguard = BodyguardDragon()
          >>> test_dragon = Dragon(1)
          >>> # add dragon first
          >>> place.add_fighter(test_dragon)
          >>> place.add_fighter(bodyguard)
          >>> colony.remove_dragon('tunnel_0_0')
          >>> place.dragon is test_dragon
          True
          >>> bodyguard.place is None
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing bodyguarded dragon keeps instance attributes
          >>> test_dragon = Dragon()
          >>> def new_action(colony):
          ...     test_dragon.armor += 9000
          >>> test_dragon.action = new_action
          >>> place = colony.places['tunnel_0_0']
          >>> bodyguard = BodyguardDragon()
          >>> place.add_fighter(test_dragon)
          >>> place.add_fighter(bodyguard)
          >>> place.dragon.action(colony)
          >>> place.dragon.contained_dragon.armor
          9001
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing single BodyguardDragon cannot hold two other dragons
          >>> bodyguard = BodyguardDragon()
          >>> first_dragon = ThrowerDragon()
          >>> place = colony.places['tunnel_0_0']
          >>> place.add_fighter(bodyguard)
          >>> place.add_fighter(first_dragon)
          >>> second_dragon = ThrowerDragon()
          >>> place.add_fighter(second_dragon)
          Traceback (most recent call last):
          ...
          AssertionError: Two dragons in tunnel_0_0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing BodyguardDragon cannot hold another BodyguardDragon
          >>> bodyguard1 = BodyguardDragon()
          >>> bodyguard2 = BodyguardDragon()
          >>> place = colony.places['tunnel_0_0']
          >>> place.add_fighter(bodyguard1)
          >>> place.add_fighter(bodyguard2)
          Traceback (most recent call last):
          ...
          AssertionError: Two dragons in tunnel_0_0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing BodyguardDragon takes all the damage
          >>> thrower = ThrowerDragon()
          >>> bodyguard = BodyguardDragon()
          >>> terminator = Terminator(1)
          >>> place = colony.places['tunnel_0_0']
          >>> place.add_fighter(thrower)
          >>> place.add_fighter(bodyguard)
          >>> place.add_fighter(terminator)
          >>> bodyguard.armor
          2
          >>> terminator.action(colony)
          >>> (bodyguard.armor, thrower.armor)
          (1, 1)
          >>> terminator.action(colony)
          >>> (bodyguard.armor, thrower.armor)
          (0, 1)
          >>> bodyguard.place is None
          True
          >>> place.dragon is thrower
          True
          >>> terminator.action(colony)
          >>> thrower.armor
          0
          >>> place.dragon is None
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # test proper call to death callback
          >>> original_death_callback = Fighter.death_callback
          >>> Fighter.death_callback = lambda x: print("fighter died")
          >>> place = colony.places["tunnel_0_0"]
          >>> terminator = Terminator(3)
          >>> bodyguard = BodyguardDragon()
          >>> dragon = ThrowerDragon()
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> place.add_fighter(bodyguard)
          >>> terminator.action(colony)
          >>> terminator.action(colony)
          fighter died
          >>> terminator.action(colony) # if you fail this test you probably didn't correctly call Dragon.reduce_armor or Fighter.reduce_armor
          fighter died
          >>> Fighter.death_callback = original_death_callback
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      >>> skynet, layout = Skynet(AssaultPlan()), dry_layout
      >>> colony = DragonColony(None, skynet, dragon_types(), layout, (1, 9))
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
          >>> BodyguardDragon.implemented
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
          >>> # Testing TankDragon parameters
          >>> TankDragon.food_cost
          6
          >>> TankDragon.damage
          1
          >>> tank = TankDragon()
          >>> tank.armor
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing TankDragon action
          >>> tank = TankDragon()
          >>> place = colony.places['tunnel_0_1']
          >>> other_place = colony.places['tunnel_0_2']
          >>> place.add_fighter(tank)
          >>> for _ in range(3):
          ...     place.add_fighter(Terminator(3))
          >>> other_place.add_fighter(Terminator(3))
          >>> tank.action(colony)
          >>> [terminator.armor for terminator in place.terminators]
          [2, 2, 2]
          >>> [terminator.armor for terminator in other_place.terminators]
          [3]
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing TankDragon container methods
          >>> tank = TankDragon()
          >>> thrower = ThrowerDragon()
          >>> place = colony.places['tunnel_0_1']
          >>> place.add_fighter(thrower)
          >>> place.add_fighter(tank)
          >>> place.dragon is tank
          True
          >>> terminator = Terminator(3)
          >>> place.add_fighter(terminator)
          >>> tank.action(colony)   # Both dragons attack terminator
          >>> terminator.armor
          1
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      >>> from assault_plans import *
      >>> skynet, layout = Skynet(make_test_assault_plan()), dry_layout
      >>> dimensions = (1, 9)
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
          >>> # Testing TankDragon action
          >>> tank = TankDragon()
          >>> place = colony.places['tunnel_0_1']
          >>> place.add_fighter(tank)
          >>> for _ in range(3):
          ...     place.add_fighter(Terminator(1))
          >>> tank.action(colony)
          >>> len(place.terminators)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing TankDragon.damage
          >>> tank = TankDragon()
          >>> tank.damage = 100
          >>> place = colony.places['tunnel_0_1']
          >>> place.add_fighter(tank)
          >>> for _ in range(3):
          ...     place.add_fighter(Terminator(100))
          >>> tank.action(colony)
          >>> len(place.terminators)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Placement of dragons
          >>> tank = TankDragon()
          >>> harvester = HarvesterDragon()
          >>> place = colony.places['tunnel_0_0']
          >>> # Add tank before harvester
          >>> place.add_fighter(tank)
          >>> place.add_fighter(harvester)
          >>> colony.food = 0
          >>> tank.action(colony)
          >>> colony.food
          1
          >>> try:
          ...   place.add_fighter(TankDragon())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.dragon is tank
          True
          >>> tank.contained_dragon is harvester
          True
          >>> try:
          ...   place.add_fighter(HarvesterDragon())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.dragon is tank
          True
          >>> tank.contained_dragon is harvester
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Placement of dragons
          >>> tank = TankDragon()
          >>> harvester = HarvesterDragon()
          >>> place = colony.places['tunnel_0_0']
          >>> # Add harvester before tank
          >>> place.add_fighter(harvester)
          >>> place.add_fighter(tank)
          >>> colony.food = 0
          >>> tank.action(colony)
          >>> colony.food
          1
          >>> try:
          ...   place.add_fighter(TankDragon())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.dragon is tank
          True
          >>> tank.contained_dragon is harvester
          True
          >>> try:
          ...   place.add_fighter(HarvesterDragon())
          ... except AssertionError:
          ...   print("error!")
          error!
          >>> place.dragon is tank
          True
          >>> tank.contained_dragon is harvester
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Removing dragons
          >>> tank = TankDragon()
          >>> test_dragon = Dragon()
          >>> place = Place('Test')
          >>> place.add_fighter(tank)
          >>> place.add_fighter(test_dragon)
          >>> place.remove_fighter(test_dragon)
          >>> tank.contained_dragon is None
          True
          >>> test_dragon.place is None
          True
          >>> place.remove_fighter(tank)
          >>> place.dragon is None
          True
          >>> tank.place is None
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> tank = TankDragon()
          >>> place = Place('Test')
          >>> place.add_fighter(tank)
          >>> tank.action(colony) # Action without contained dragon should not error
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # test proper call to death callback
          >>> original_death_callback = Fighter.death_callback
          >>> Fighter.death_callback = lambda x: print("fighter died")
          >>> place = colony.places["tunnel_0_0"]
          >>> terminator = Terminator(3)
          >>> tank = TankDragon()
          >>> dragon = ThrowerDragon()
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> place.add_fighter(tank)
          >>> terminator.action(colony)
          >>> terminator.action(colony)
          fighter died
          >>> terminator.action(colony) # if you fail this test you probably didn't correctly call Dragon.reduce_armor or Fighter.reduce_armor
          fighter died
          >>> Fighter.death_callback = original_death_callback
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      >>> from assault_plans import *
      >>> skynet, layout = Skynet(make_test_assault_plan()), dry_layout
      >>> dimensions = (1, 9)
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
          >>> from dragons import *
          >>> TankDragon.implemented
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
