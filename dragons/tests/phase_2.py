test = {
  'name': 'phase_2',
  'points': 0,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> # Testing Long/ShortThrower parameters
          >>> ShortThrower.food_cost
          2
          >>> LongThrower.food_cost
          2
          >>> short_t = ShortThrower()
          >>> long_t = LongThrower()
          >>> short_t.armor
          1
          >>> long_t.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Test LongThrower Hit
          >>> dragon = LongThrower()
          >>> in_range = Terminator(2)
          >>> colony.places['tunnel_0_0'].add_fighter(dragon)
          >>> colony.places["tunnel_0_5"].add_fighter(in_range)
          >>> dragon.action(colony)
          >>> in_range.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing LongThrower miss
          >>> dragon = LongThrower()
          >>> out_of_range = Terminator(2)
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> colony.places["tunnel_0_4"].add_fighter(out_of_range)
          >>> dragon.action(colony)
          >>> out_of_range.armor
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing LongThrower miss next to the skynet
          >>> dragon = LongThrower()
          >>> colony.places["tunnel_0_4"].add_fighter(dragon)
          >>> dragon.action(colony) # should not error
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing LongThrower targets farther one
          >>> dragon = LongThrower()
          >>> out_of_range = Terminator(2)
          >>> in_range = Terminator(2)
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> colony.places["tunnel_0_4"].add_fighter(out_of_range)
          >>> colony.places["tunnel_0_5"].add_fighter(in_range)
          >>> dragon.action(colony)
          >>> out_of_range.armor
          2
          >>> in_range.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Test ShortThrower hit
          >>> dragon = ShortThrower()
          >>> in_range = Terminator(2)
          >>> colony.places['tunnel_0_0'].add_fighter(dragon)
          >>> colony.places["tunnel_0_3"].add_fighter(in_range)
          >>> dragon.action(colony)
          >>> in_range.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing ShortThrower miss
          >>> dragon = ShortThrower()
          >>> out_of_range = Terminator(2)
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> colony.places["tunnel_0_4"].add_fighter(out_of_range)
          >>> dragon.action(colony)
          >>> out_of_range.armor
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing LongThrower ignores terminators outside range
          >>> thrower = LongThrower()
          >>> colony.places["tunnel_0_0"].add_fighter(thrower)
          >>> terminator1 = Terminator(1001)
          >>> terminator2 = Terminator(1001)
          >>> colony.places["tunnel_0_4"].add_fighter(terminator1)
          >>> colony.places["tunnel_0_5"].add_fighter(terminator2)
          >>> thrower.action(colony)
          >>> terminator1.armor
          1001
          >>> terminator2.armor
          1000
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing LongThrower attacks nearest terminator in range
          >>> thrower = LongThrower()
          >>> colony.places["tunnel_0_0"].add_fighter(thrower)
          >>> terminator1 = Terminator(1001)
          >>> terminator2 = Terminator(1001)
          >>> colony.places["tunnel_0_5"].add_fighter(terminator1)
          >>> colony.places["tunnel_0_6"].add_fighter(terminator2)
          >>> thrower.action(colony)
          >>> terminator1.armor
          1000
          >>> terminator2.armor
          1001
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing if max_range is looked up in the instance
          >>> dragon = ShortThrower()
          >>> dragon.max_range = 10   # Buff the dragon's range
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> terminator = Terminator(2)
          >>> colony.places["tunnel_0_6"].add_fighter(terminator)
          >>> dragon.action(colony)
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
      >>> skynet, layout = Skynet(AssaultPlan()), dry_layout
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
          >>> # Testing if min_range is set appropriately in ThrowerDragon
          >>> dragon = ThrowerDragon()
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> terminator = Terminator(2)
          >>> colony.places["tunnel_0_0"].add_fighter(terminator)
          >>> dragon.action(colony)
          >>> terminator.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing if max_range is set appropriately in ThrowerDragon
          >>> dragon = ThrowerDragon()
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> terminator = Terminator(2)
          >>> colony.places["tunnel_0_99"].add_fighter(terminator)
          >>> dragon.action(colony)
          >>> terminator.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Special thrower class that just hits things 6 away
          >>> class JustSixThrower(ThrowerDragon):
          ...   min_range = max_range = 6
          >>> dragon = JustSixThrower()
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> exact_terminator = Terminator(2)
          >>> colony.places["tunnel_0_6"].add_fighter(exact_terminator)
          >>> dragon.action(colony)
          >>> exact_terminator.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Special thrower class that just hits things 6 away
          >>> class JustSixThrower(ThrowerDragon):
          ...   min_range = max_range = 6
          >>> dragon = JustSixThrower()
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> close_terminator = Terminator(2)
          >>> colony.places["tunnel_0_5"].add_fighter(close_terminator)
          >>> dragon.action(colony)
          >>> close_terminator.armor
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Special thrower class that just hits things 6 away
          >>> class JustSixThrower(ThrowerDragon):
          ...   min_range = max_range = 6
          >>> dragon = JustSixThrower()
          >>> colony.places["tunnel_0_0"].add_fighter(dragon)
          >>> far_terminator = Terminator(2)
          >>> colony.places["tunnel_0_7"].add_fighter(far_terminator)
          >>> dragon.action(colony)
          >>> far_terminator.armor
          2
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from dragons import *
      >>> skynet, layout = Skynet(AssaultPlan()), dry_layout
      >>> dimensions = (1, 100)
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
          >>> # Testing LongThrower Inheritance from ThrowerDragon
          >>> def new_action(self, colony):
          ...     raise NotImplementedError()
          >>> def new_throw_at(self, target):
          ...     raise NotImplementedError()
          >>> old_thrower_action = ThrowerDragon.action
          >>> old_throw_at = ThrowerDragon.throw_at
          
          >>> ThrowerDragon.action = new_action
          >>> test_long = LongThrower()
          >>> passed = 0
          >>> try:
          ...     test_long.action(colony)
          ... except NotImplementedError:
          ...     passed += 1
          >>> ThrowerDragon.action = old_thrower_action
          >>> ThrowerDragon.throw_at = new_throw_at
          >>> test_long = LongThrower()
          >>> try:
          ...     test_long.throw_at(Terminator(1))
          ... except NotImplementedError:
          ...     passed += 1
          >>> ThrowerDragon.throw_at = old_throw_at
          >>> passed
          2
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing ShortThrower Inheritance from ThrowerDragon
          >>> def new_action(self, colony):
          ...     raise NotImplementedError()
          >>> def new_throw_at(self, target):
          ...     raise NotImplementedError()
          >>> old_thrower_action = ThrowerDragon.action
          >>> old_throw_at = ThrowerDragon.throw_at
          
          >>> ThrowerDragon.action = new_action
          >>> test_short = ShortThrower()
          >>> passed = 0
          >>> try:
          ...     test_short.action(colony)
          ... except NotImplementedError:
          ...     passed += 1
          
          >>> ThrowerDragon.action = old_thrower_action
          >>> ThrowerDragon.throw_at = new_throw_at
          >>> test_short = ShortThrower()
          >>> try:
          ...     test_short.throw_at(Terminator(1))
          ... except NotImplementedError:
          ...     passed += 1
          
          >>> ThrowerDragon.throw_at = old_throw_at
          >>> passed
          2
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
      >>> #
      """,
      'teardown': r"""
      >>> ThrowerDragon.action = old_thrower_action
      >>> ThrowerDragon.throw_at = old_throw_at
      """,
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> from dragons import *
          >>> LongThrower.implemented
          True
          >>> ShortThrower.implemented
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
          >>> # Testing FireDragon parameters
          >>> fire = FireDragon()
          >>> FireDragon.food_cost
          5
          >>> fire.armor
          3
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing fire does damage to all Terminators in its Place
          >>> place = colony.places['tunnel_0_4']
          >>> fire = FireDragon(armor=1)
          >>> place.add_fighter(fire)        # Add a FireDragon with 1 armor
          >>> place.add_fighter(Terminator(3))      # Add a Terminator with 3 armor
          >>> place.add_fighter(Terminator(5))      # Add a Terminator with 5 armor
          >>> len(place.terminators)               # How many terminators are there?
          2
          >>> place.terminators[0].action(colony)  # The first Terminator attacks FireDragon
          >>> fire.armor
          0
          >>> fire.place is None
          True
          >>> len(place.terminators)               # How many terminators are left?
          1
          >>> place.terminators[0].armor           # What is the armor of the remaining Terminator?
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> place = colony.places['tunnel_0_4']
          >>> dragon = FireDragon(1)           # Create a FireDragon with 1 armor
          >>> place.add_fighter(dragon)      # Add a FireDragon to place
          >>> dragon.place is place
          True
          >>> place.remove_fighter(dragon)   # Remove FireDragon from place
          >>> dragon.place is place         # Is the dragon's place still that place?
          False
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing fire damage when the fire dragon does not die
          >>> place = colony.places['tunnel_0_4']
          >>> terminator = Terminator(5)
          >>> dragon = FireDragon(armor=100)
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> terminator.action(colony) # attack the FireDragon
          >>> dragon.armor
          99
          >>> terminator.armor
          4
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing no hardcoded 3
          >>> place = colony.places['tunnel_0_4']
          >>> terminator = Terminator(100)
          >>> dragon = FireDragon(armor=1)
          >>> dragon.damage = 49
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> terminator.action(colony) # attack the FireDragon
          >>> dragon.armor
          0
          >>> terminator.armor
          50
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing fire damage when the fire dragon does die
          >>> place = colony.places['tunnel_0_4']
          >>> terminator = Terminator(5)
          >>> dragon = FireDragon(armor=1)
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> terminator.action(colony) # attack the FireDragon
          >>> dragon.armor
          0
          >>> terminator.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing fire does damage to all Terminators in its Place
          >>> place = colony.places['tunnel_0_4']
          >>> place.add_fighter(FireDragon(1))
          >>> for i in range(100):          # Add 100 Terminators with 3 armor
          ...     place.add_fighter(Terminator(3))
          >>> place.terminators[0].action(colony)  # The first Terminator attacks FireDragon
          >>> len(place.terminators)               # How many terminators are left?
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing fire damage is instance attribute
          >>> place = colony.places['tunnel_0_4']
          >>> terminator = Terminator(900)
          >>> buffDragon = FireDragon(1)
          >>> buffDragon.damage = 500   # Feel the burn!
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(buffDragon)
          >>> terminator.action(colony) # attack the FireDragon
          >>> terminator.armor  # is damage an instance attribute?
          399
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # General FireDragon Test
          >>> place = colony.places['tunnel_0_4']
          >>> terminator = Terminator(10)
          >>> dragon = FireDragon(1)
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> terminator.action(colony)    # Attack the FireDragon
          >>> terminator.armor
          6
          >>> dragon.armor
          0
          >>> place.dragon is None     # The FireDragon should not occupy the place anymore
          True
          >>> terminator.action(colony)
          >>> terminator.armor             # Terminator should not get damaged again
          6
          >>> terminator.place.name        # Terminator should not have been blocked
          'tunnel_0_3'
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # General FireDragon Test
          >>> place = colony.places['tunnel_0_4']
          >>> terminator = Terminator(10)
          >>> dragon = FireDragon()
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> dragon.reduce_armor(0.1) # Poke the FireDragon
          >>> terminator.armor             # Terminator should only get slightly damaged
          9.9
          >>> dragon.armor
          2.9
          >>> place.dragon is dragon      # The FireDragon should still be at place
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
          >>> dragon = FireDragon()
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> terminator.action(colony)
          >>> terminator.action(colony)
          >>> terminator.action(colony) # if you fail this test you probably didn't correctly call Dragon.reduce_armor or Fighter.reduce_armor
          fighter died
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
          >>> FireDragon.implemented
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
          >>> # Testing HungryDragon parameters
          >>> hungry = HungryDragon()
          >>> HungryDragon.food_cost
          4
          >>> hungry.armor
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing HungryDragon eats and digests
          >>> hungry = HungryDragon()
          >>> terminator1 = Terminator(1000)              # A Terminator with 1000 armor
          >>> place = colony.places["tunnel_0_0"]
          >>> place.add_fighter(hungry)
          >>> place.add_fighter(terminator1)         # Add the Terminator to the same place as HungryDragon
          >>> hungry.action(colony)
          >>> terminator1.armor
          0
          >>> terminator2 = Terminator(1)                 # A Terminator with 1 armor
          >>> place.add_fighter(terminator2)
          >>> for _ in range(3):
          ...     hungry.action(colony)     # Digesting...not eating
          >>> terminator2.armor
          1
          >>> hungry.action(colony)
          >>> terminator2.armor
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing HungryDragon eats and digests
          >>> hungry = HungryDragon()
          >>> super_terminator, wimpy_terminator = Terminator(1000), Terminator(1)
          >>> place = colony.places["tunnel_0_0"]
          >>> place.add_fighter(hungry)
          >>> place.add_fighter(super_terminator)
          >>> hungry.action(colony)         # super_terminator is no match for HungryDragon!
          >>> super_terminator.armor
          0
          >>> place.add_fighter(wimpy_terminator)
          >>> for _ in range(3):
          ...     hungry.action(colony)     # digesting...not eating
          >>> wimpy_terminator.armor
          1
          >>> hungry.action(colony)         # back to eating!
          >>> wimpy_terminator.armor
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing HungryDragon only waits when digesting
          >>> hungry = HungryDragon()
          >>> place = colony.places["tunnel_0_0"]
          >>> place.add_fighter(hungry)
          >>> # Wait a few turns before adding Terminator
          >>> for _ in range(5):
          ...     hungry.action(colony)  # shouldn't be digesting
          >>> terminator = Terminator(3)
          >>> place.add_fighter(terminator)
          >>> hungry.action(colony)  # Eating time!
          >>> terminator.armor
          0
          >>> terminator = Terminator(3)
          >>> place.add_fighter(terminator)
          >>> for _ in range(3):
          ...     hungry.action(colony)     # Should be digesting
          >>> terminator.armor
          3
          >>> hungry.action(colony)
          >>> terminator.armor
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing HungryDragon digest time looked up on instance
          >>> very_hungry = HungryDragon()  # Add very hungry caterpi- um, dragon
          >>> very_hungry.time_to_digest = 0
          >>> place = colony.places["tunnel_0_0"]
          >>> place.add_fighter(very_hungry)
          >>> for _ in range(100):
          ...     place.add_fighter(Terminator(3))
          >>> for _ in range(100):
          ...     very_hungry.action(colony)   # Eat all the terminators!
          >>> len(place.terminators)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing HungryDragon dies while eating
          >>> hungry = HungryDragon()
          >>> place = colony.places["tunnel_0_0"]
          >>> place.add_fighter(hungry)
          >>> place.add_fighter(Terminator(3))
          >>> hungry.action(colony)
          >>> len(place.terminators)
          0
          >>> terminator = Terminator(3)
          >>> place.add_fighter(terminator)
          >>> terminator.action(colony) # Terminator kills digesting dragon
          >>> place.dragon is None
          True
          >>> len(place.terminators)
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing HungryDragon can't eat a terminator at another space
          >>> hungry = HungryDragon()
          >>> colony.places["tunnel_0_0"].add_fighter(hungry)
          >>> colony.places["tunnel_0_1"].add_fighter(Terminator(3))
          >>> hungry.action(colony)
          >>> len(colony.places["tunnel_0_1"].terminators)
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # test proper call to death callback
          >>> original_death_callback = Fighter.death_callback
          >>> Fighter.death_callback = lambda x: print("fighter died")
          >>> dragon = HungryDragon()
          >>> terminator = Terminator(1000)              # A Terminator with 1000 armor
          >>> place = colony.places["tunnel_0_0"]
          >>> place.add_fighter(terminator)
          >>> place.add_fighter(dragon)
          >>> dragon.action(colony) # if you fail this test you probably didn't correctly call Dragon.reduce_armor or Fighter.reduce_armor
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
          >>> HungryDragon.implemented
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
          >>> # Testing NinjaDragon parameters
          >>> ninja = NinjaDragon()
          >>> ninja.armor
          1
          >>> NinjaDragon.food_cost
          5
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing blocks_path
          >>> NinjaDragon.blocks_path
          False
          >>> HungryDragon.blocks_path
          True
          >>> FireDragon.blocks_path
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaDragons do not block terminators
          >>> p0 = colony.places["tunnel_0_0"]
          >>> p1 = colony.places["tunnel_0_1"]  # p0 is p1's exit
          >>> terminator = Terminator(2)
          >>> ninja = NinjaDragon()
          >>> thrower = ThrowerDragon()
          >>> p0.add_fighter(thrower)            # Add ThrowerDragon to p0
          >>> p1.add_fighter(terminator)
          >>> p1.add_fighter(ninja)              # Add the Terminator and NinjaDragon to p1
          >>> terminator.action(colony)
          >>> terminator.place is ninja.place          # Did NinjaDragon block the Terminator from moving?
          False
          >>> terminator.place is p0
          True
          >>> ninja.armor
          1
          >>> terminator.action(colony)
          >>> terminator.place is p0                   # Did ThrowerDragon block the Terminator from moving?
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing non-blocking dragons do not block terminators
          >>> p0 = colony.places["tunnel_0_0"]
          >>> p1 = colony.places["tunnel_0_1"]  # p0 is p1's exit
          >>> terminator = Terminator(2)
          >>> ninja_fire = FireDragon(1)
          >>> ninja_fire.blocks_path = False
          >>> thrower = ThrowerDragon()
          >>> p0.add_fighter(thrower)            # Add ThrowerDragon to p0
          >>> p1.add_fighter(terminator)
          >>> p1.add_fighter(ninja_fire)              # Add the Terminator and NinjaDragon to p1
          >>> terminator.action(colony)
          >>> terminator.place is ninja_fire.place          # Did the "ninjaish" FireDragon block the Terminator from moving?
          False
          >>> terminator.place is p0
          True
          >>> ninja_fire.armor
          1
          >>> terminator.action(colony)
          >>> terminator.place is p0                   # Did ThrowerDragon block the Terminator from moving?
          True
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaDragon strikes all terminators in its place
          >>> test_place = colony.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_fighter(Terminator(2))
          >>> ninja = NinjaDragon()
          >>> test_place.add_fighter(ninja)
          >>> ninja.action(colony)   # should strike all terminators in place
          >>> [terminator.armor for terminator in test_place.terminators]
          [1, 1, 1]
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaDragon doesn't hardcode damage
          >>> test_place = colony.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_fighter(Terminator(100))
          >>> ninja = NinjaDragon()
          >>> ninja.damage = 50
          >>> test_place.add_fighter(ninja)
          >>> ninja.action(colony)   # should strike all terminators in place
          >>> [terminator.armor for terminator in test_place.terminators]
          [50, 50, 50]
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing NinjaDragon strikes all terminators, even if some expire
          >>> test_place = colony.places["tunnel_0_0"]
          >>> for _ in range(3):
          ...     test_place.add_fighter(Terminator(1))
          >>> ninja = NinjaDragon()
          >>> test_place.add_fighter(ninja)
          >>> ninja.action(colony)   # should strike all terminators in place
          >>> len(test_place.terminators)
          0
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing damage is looked up on the instance
          >>> place = colony.places["tunnel_0_0"]
          >>> terminator = Terminator(900)
          >>> place.add_fighter(terminator)
          >>> buffNinja = NinjaDragon()
          >>> buffNinja.damage = 500  # Sharpen the sword
          >>> place.add_fighter(buffNinja)
          >>> buffNinja.action(colony)
          >>> terminator.armor
          400
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing Ninja dragon does not crash when left alone
          >>> ninja = NinjaDragon()
          >>> colony.places["tunnel_0_0"].add_fighter(ninja)
          >>> ninja.action(colony)
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> # Testing Terminator does not crash when left alone
          >>> terminator = Terminator(3)
          >>> colony.places["tunnel_0_1"].add_fighter(terminator)
          >>> terminator.action(colony)
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
          >>> NinjaDragon.implemented
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
