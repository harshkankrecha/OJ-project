test = {
    'name': 'phase_4',
    'points': 0,
    'suites': [
        {
            'cases': [
                {
                    'code': r"""
          >>> # Testing water with Dragons
          >>> test_water = Water('Water Test1')
          >>> dragon = HarvesterDragon()
          >>> test_water.add_fighter(dragon)
          >>> (dragon.armor, test_water.dragon is None)
          (0, True)
          >>> dragon = Dragon()
          >>> test_water.add_fighter(dragon)
          >>> (dragon.armor, test_water.dragon is None)
          (0, True)
          >>> dragon = ThrowerDragon()
          >>> test_water.add_fighter(dragon)
          >>> (dragon.armor, test_water.dragon is None)
          (0, True)
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing water with soggy (non-watersafe) terminators
          >>> test_terminator = Terminator(1000000)
          >>> test_terminator.is_watersafe = False    # Make Terminator non-watersafe
          >>> test_water = Water('Water Test2')
          >>> test_water.add_fighter(test_terminator)
          >>> test_terminator.armor
          0
          >>> test_water.terminators
          []
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing water with watersafe terminators
          >>> test_terminator = Terminator(1)
          >>> test_water = Water('Water Test3')
          >>> test_water.add_fighter(test_terminator)
          >>> test_terminator.armor
          1
          >>> test_water.terminators == [test_terminator]
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
          >>> place = Water('Water Test4')
          >>> soggy_terminator = Terminator(1)
          >>> soggy_terminator.is_watersafe = False
          >>> place.add_fighter(soggy_terminator)
          fighter died
          >>> place.add_fighter(Terminator(1))
          >>> place.add_fighter(ThrowerDragon())
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
          >>> # Testing water inheritance
          >>> old_add_fighter = Place.add_fighter
          >>> def new_add_fighter(self, fighter):
          ...     print("called add_fighter")
          ...     old_add_fighter(self, fighter)
          >>> Place.add_fighter = new_add_fighter
          >>> test_terminator = Terminator(1)
          >>> test_water = Water('Water Test4')
          >>> test_water.add_fighter(test_terminator) # if this fails you probably didn't call `add_fighter`
          called add_fighter
          >>> Place.add_fighter = old_add_fighter
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
      >>> old_add_fighter = Place.add_fighter
      """,
            'teardown': r"""
      >>> Place.add_fighter = old_add_fighter
      """,
            'type': 'doctest'
        },
        {
            'cases': [
                {
                    'code': r"""
          >>> # Testing ScubaThrower parameters
          >>> scuba = ScubaThrower()
          >>> ScubaThrower.food_cost
          6
          >>> scuba.armor
          1
          """,
                    'hidden': False,
                    'locked': False
                }
            ],
            'scored': False,
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
          >>> # Testing if ScubaThrower is watersafe
          >>> water = Water('Water')
          >>> dragon = ScubaThrower()
          >>> water.add_fighter(dragon)
          >>> dragon.place is water
          True
          >>> dragon.armor
          1
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing that ThrowerDragon is not watersafe
          >>> water = Water('Water')
          >>> dragon = ThrowerDragon()
          >>> water.add_fighter(dragon)
          >>> dragon.place is water
          False
          >>> dragon.armor
          0
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing ScubaThrower on land
          >>> place1 = colony.places["tunnel_0_0"]
          >>> place2 = colony.places["tunnel_0_4"]
          >>> dragon = ScubaThrower()
          >>> terminator = Terminator(3)
          >>> place1.add_fighter(dragon)
          >>> place2.add_fighter(terminator)
          >>> dragon.action(colony)
          >>> terminator.armor  # ScubaThrower can throw on land
          2
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing ScubaThrower in the water
          >>> water = Water("water")
          >>> water.entrance = colony.places["tunnel_0_1"]
          >>> target = colony.places["tunnel_0_4"]
          >>> dragon = ScubaThrower()
          >>> terminator = Terminator(3)
          >>> water.add_fighter(dragon)
          >>> target.add_fighter(terminator)
          >>> dragon.action(colony)
          >>> terminator.armor  # ScubaThrower can throw in water
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
            'teardown': '',
            'type': 'doctest'
        },
        {
            'cases': [
                {
                    'code': r"""
          >>> # Testing ScubaThrower Inheritance from ThrowerDragon
          >>> def new_action(self, colony):
          ...     raise NotImplementedError()
          >>> def new_throw_at(self, target):
          ...     raise NotImplementedError()
          >>> ThrowerDragon.action = new_action
          >>> test_scuba = ScubaThrower()
          >>> try:
          ...     test_scuba.action(colony)
          ... except NotImplementedError:
          ...     print('inherits action!')
          inherits action!
          >>> ThrowerDragon.action = old_thrower_action
          >>> ThrowerDragon.throw_at = new_throw_at
          >>> test_scuba = ScubaThrower()
          >>> try:
          ...     test_scuba.throw_at(Terminator(1))
          ... except NotImplementedError:
          ...     print('inherits throw_at!')
          inherits throw_at!
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
      >>> old_thrower_action = ThrowerDragon.action
      >>> old_throw_at = ThrowerDragon.throw_at
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
          >>> ScubaThrower.implemented
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
          >>> # Testing DragonKing parameters
          >>> DragonKing.food_cost
          7
          >>> king = DragonKing()
          >>> king.armor
          1
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
          >>> # DragonKing Placement
          >>> king = dragons.DragonKing()
          >>> impostor = dragons.DragonKing()
          >>> front_dragon, back_dragon = dragons.ThrowerDragon(), dragons.ThrowerDragon()
          >>> tunnel = [colony.places['tunnel_0_{0}'.format(i)]
          ...         for i in range(9)]
          >>> tunnel[1].add_fighter(back_dragon)
          >>> tunnel[7].add_fighter(front_dragon)
          >>> tunnel[4].add_fighter(impostor)
          >>> impostor.action(colony)
          >>> impostor.armor            # Impostors must die!
          0
          >>> tunnel[4].dragon is None
          True
          >>> back_dragon.damage           # Dragons should not be buffed
          1
          >>> front_dragon.damage
          1
          >>> tunnel[4].add_fighter(king)
          >>> king.action(colony)
          >>> king.armor               # Long live the King!
          1
          >>> back_dragon.damage           # Dragons behind king should be buffed
          2
          >>> front_dragon.damage
          1
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # DragonKing Removal
          >>> king = dragons.DragonKing()
          >>> impostor = dragons.DragonKing()
          >>> place = colony.places['tunnel_0_2']
          >>> place.add_fighter(impostor)
          >>> place.remove_fighter(impostor)
          >>> place.dragon is None         # Impostors can be removed
          True
          >>> place.add_fighter(king)
          >>> place.remove_fighter(king)
          >>> place.dragon is king        # True king cannot be removed
          True
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # DragonKing knows how to swim
          >>> king = dragons.DragonKing()
          >>> water = dragons.Water('Water')
          >>> water.add_fighter(king)
          >>> king.armor
          1
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing damage multiplier
          >>> king_tunnel, side_tunnel = [[colony.places['tunnel_{0}_{1}'.format(i, j)]
          ...         for j in range(9)] for i in range(2)]
          >>> # layout
          >>> # king_tunnel: [Back, Guard/Guarded, King, Front, Terminator     ]
          >>> # side_tunnel : [Side,              ,      ,      , Side Terminator]
          >>> king = dragons.DragonKing()
          >>> back = dragons.ThrowerDragon()
          >>> front = dragons.ThrowerDragon()
          >>> guard = dragons.BodyguardDragon()
          >>> guarded = dragons.ThrowerDragon()
          >>> side = dragons.ThrowerDragon()
          >>> terminator = dragons.Terminator(10)
          >>> side_terminator = dragons.Terminator(10)
          >>> king_tunnel[0].add_fighter(back)
          >>> king_tunnel[1].add_fighter(guard)
          >>> king_tunnel[1].add_fighter(guarded)
          >>> king_tunnel[2].add_fighter(king)
          >>> king_tunnel[3].add_fighter(front)
          >>> side_tunnel[0].add_fighter(side)
          >>> king_tunnel[4].add_fighter(terminator)
          >>> side_tunnel[4].add_fighter(side_terminator)
          >>> king.action(colony)
          >>> terminator.armor
          9
          >>> back.action(colony)
          >>> terminator.armor
          7
          >>> front.action(colony)
          >>> terminator.armor
          6
          >>> guard.action(colony)
          >>> terminator.armor # if this is 5 you probably forgot to buff the contents of guard
          4
          >>> side.action(colony)
          >>> side_terminator.armor
          9
          """,
                    'hidden': False,
                    'locked': False
                }
            ],
            'scored': True,
            'setup': r"""
      >>> import dragons, importlib
      >>> importlib.reload(dragons)
      >>> skynet = dragons.Skynet(dragons.AssaultPlan())
      >>> dimensions = (2, 9)
      >>> colony = dragons.DragonColony(None, skynet, dragons.dragon_types(),
      ...         dragons.dry_layout, dimensions)
      >>> dragons.terminators_win = lambda: None
      """,
            'teardown': '',
            'type': 'doctest'
        },
        {
            'cases': [
                {
                    'code': r"""
          >>> # Testing game over
          >>> king = dragons.DragonKing()
          >>> impostor = dragons.DragonKing()
          >>> tunnel = [colony.places['tunnel_0_{0}'.format(i)]
          ...         for i in range(9)]
          >>> tunnel[4].add_fighter(king)
          >>> tunnel[6].add_fighter(impostor)
          >>> terminator = dragons.Terminator(3)
          >>> tunnel[6].add_fighter(terminator)     # Terminator in place with impostor
          >>> terminator.action(colony)            # Game should not end

          >>> terminator.move_to(tunnel[4])        # Terminator moved to place with true king
          >>> terminator.action(colony)            # Game should end
          TerminatorsWinException
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing if king will not crash with no one to buff
          >>> king = dragons.DragonKing()
          >>> colony.places['tunnel_0_2'].add_fighter(king)
          >>> king.action(colony)
          >>> # Attack a terminator
          >>> terminator = dragons.Terminator(3)
          >>> colony.places['tunnel_0_4'].add_fighter(terminator)
          >>> king.action(colony)
          >>> terminator.armor # King should still hit the terminator
          2
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing DragonKing action method
          >>> king = dragons.DragonKing()
          >>> impostor = dragons.DragonKing()
          >>> terminator = dragons.Terminator(10)
          >>> dragon = dragons.ThrowerDragon()
          >>> colony.places['tunnel_0_0'].add_fighter(dragon)
          >>> colony.places['tunnel_0_1'].add_fighter(king)
          >>> colony.places['tunnel_0_2'].add_fighter(impostor)
          >>> colony.places['tunnel_0_4'].add_fighter(terminator)

          >>> impostor.action(colony)
          >>> terminator.armor   # Impostor should not damage terminator
          10
          >>> dragon.damage  # Impostor should not double damage
          1

          >>> king.action(colony)
          >>> terminator.armor   # King should damage terminator
          9
          >>> dragon.damage  # King should double damage
          2
          >>> dragon.action(colony)
          >>> terminator.armor   # If failed, ThrowerDragon has incorrect damage
          7

          >>> king.armor   # Long live the King
          1
          >>> impostor.armor  # Short-lived impostor
          0
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Extensive damage doubling tests
          >>> king_tunnel, side_tunnel = [[colony.places['tunnel_{0}_{1}'.format(i, j)]
          ...         for j in range(9)] for i in range(2)]
          >>> king = dragons.DragonKing()
          >>> king_tunnel[7].add_fighter(king)
          >>> # Turn 0
          >>> thrower = dragons.ThrowerDragon()
          >>> fire = dragons.FireDragon()
          >>> ninja = dragons.NinjaDragon()
          >>> side = dragons.ThrowerDragon()
          >>> front = dragons.NinjaDragon()
          >>> king_tunnel[0].add_fighter(thrower)
          >>> king_tunnel[1].add_fighter(fire)
          >>> king_tunnel[2].add_fighter(ninja)
          >>> king_tunnel[8].add_fighter(front)
          >>> side_tunnel[0].add_fighter(side)
          >>> # layout right now
          >>> # [thrower, fire, ninja, , , , , king, front]
          >>> # [side   ,     ,      , , , , ,      ,      ]
          >>> thrower.damage, fire.damage, ninja.damage = 101, 102, 103
          >>> front.damage, side.damage = 104, 105
          >>> king.action(colony)
          >>> (thrower.damage, fire.damage, ninja.damage)
          (202, 204, 206)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> # Turn 1
          >>> tank = dragons.TankDragon()
          >>> guard = dragons.BodyguardDragon()
          >>> king_tank = dragons.TankDragon()
          >>> king_tunnel[6].add_fighter(tank)          # Not protecting a dragon
          >>> king_tunnel[1].add_fighter(guard)         # Guarding FireDragon
          >>> king_tunnel[7].add_fighter(king_tank)    # Guarding DragonKing
          >>> # layout right now
          >>> # [thrower, guard/fire, ninja, , , , tank, king_tank/king, front]
          >>> # [side   ,           ,      , , , ,     ,                 ,      ]
          >>> tank.damage, guard.damage, king_tank.damage = 1001, 1002, 1003
          >>> king.action(colony)
          >>> # unchanged
          >>> (thrower.damage, fire.damage, ninja.damage)
          (202, 204, 206)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> (tank.damage, guard.damage)
          (2002, 2004)
          >>> king_tank.damage
          1003
          >>> # Turn 2
          >>> thrower1 = dragons.ThrowerDragon()
          >>> thrower2 = dragons.ThrowerDragon()
          >>> king_tunnel[6].add_fighter(thrower1)      # Add thrower1 in TankDragon
          >>> king_tunnel[5].add_fighter(thrower2)
          >>> # layout right now
          >>> # [thrower, guard/fire, ninja, , , thrower2, tank/thrower1, king_tank/king, front]
          >>> # [side   ,           ,      , , ,         ,              ,                 ,      ]
          >>> thrower1.damage, thrower2.damage = 10001, 10002
          >>> king.action(colony)
          >>> (thrower.damage, fire.damage, ninja.damage)
          (202, 204, 206)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> (tank.damage, guard.damage)
          (2002, 2004)
          >>> king_tank.damage
          1003
          >>> (thrower1.damage, thrower2.damage)
          (20002, 20004)
          >>> # Turn 3
          >>> tank.reduce_armor(tank.armor)             # Expose thrower1
          >>> king.action(colony)
          >>> (thrower.damage, fire.damage, ninja.damage)
          (202, 204, 206)
          >>> (front.damage, side.damage)
          (104, 105)
          >>> guard.damage
          2004
          >>> king_tank.damage
          1003
          >>> (thrower1.damage, thrower2.damage)
          (20002, 20004)
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Adding/Removing DragonKing with Container
          >>> place = colony.places['tunnel_0_3']
          >>> king = dragons.DragonKing()
          >>> impostor = dragons.DragonKing()
          >>> container = dragons.TankDragon()
          >>> place.add_fighter(container)
          >>> place.add_fighter(impostor)
          >>> impostor.action(colony)
          >>> place.dragon is container
          True
          >>> container.place is place
          True
          >>> container.contained_dragon is None
          True
          >>> impostor.place is None
          True
          >>> place.add_fighter(king)
          >>> place.remove_fighter(king)
          >>> container.contained_dragon is king
          True
          >>> king.place is place
          True
          >>> king.action(colony) # should not error
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # test proper call to death callback
          >>> original_death_callback = dragons.Fighter.death_callback
          >>> dragons.Fighter.death_callback = lambda x: print("fighter died")
          >>> real = dragons.DragonKing()
          >>> impostor = dragons.DragonKing()
          >>> colony.places['tunnel_0_2'].add_fighter(real)
          >>> colony.places['tunnel_0_3'].add_fighter(impostor)
          >>> impostor.action(colony)
          fighter died
          >>> dragons.Fighter.death_callback = original_death_callback
          """,
                    'hidden': False,
                    'locked': False
                }
            ],
            'scored': True,
            'setup': r"""
      >>> import dragons, importlib
      >>> importlib.reload(dragons)
      >>> skynet = dragons.Skynet(dragons.AssaultPlan())
      >>> dimensions = (2, 9)
      >>> colony = dragons.DragonColony(None, skynet, dragons.dragon_types(),
      ...         dragons.dry_layout, dimensions)
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
          >>> DragonKing.implemented
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
          >>> # Testing status parameters
          >>> slow = SlowThrower()
          >>> scary = ScaryThrower()
          >>> SlowThrower.food_cost
          4
          >>> ScaryThrower.food_cost
          6
          >>> slow.armor
          1
          >>> scary.armor
          1
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing Slow
          >>> slow = SlowThrower()
          >>> terminator = Terminator(3)
          >>> colony.places["tunnel_0_0"].add_fighter(slow)
          >>> colony.places["tunnel_0_4"].add_fighter(terminator)
          >>> slow.action(colony)
          >>> colony.time = 1
          >>> terminator.action(colony)
          >>> terminator.place.name # SlowThrower should cause slowness on odd turns
          'tunnel_0_4'
          >>> colony.time += 1
          >>> terminator.action(colony)
          >>> terminator.place.name # SlowThrower should cause slowness on odd turns
          'tunnel_0_3'
          >>> for _ in range(3):
          ...     colony.time += 1
          ...     terminator.action(colony)
          >>> terminator.place.name
          'tunnel_0_1'
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing Scare
          >>> scary = ScaryThrower()
          >>> terminator = Terminator(3)
          >>> colony.places["tunnel_0_0"].add_fighter(scary)
          >>> colony.places["tunnel_0_4"].add_fighter(terminator)
          >>> scary.action(colony)
          >>> terminator.action(colony)
          >>> terminator.place.name # ScaryThrower should scare for two turns
          'tunnel_0_5'
          >>> terminator.action(colony)
          >>> terminator.place.name # ScaryThrower should scare for two turns
          'tunnel_0_6'
          >>> terminator.action(colony)
          >>> terminator.place.name
          'tunnel_0_5'
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Scary stings a dragon
          >>> scary = ScaryThrower()
          >>> harvester = HarvesterDragon()
          >>> terminator = Terminator(3)
          >>> colony.places["tunnel_0_0"].add_fighter(scary)
          >>> colony.places["tunnel_0_4"].add_fighter(terminator)
          >>> colony.places["tunnel_0_5"].add_fighter(harvester)
          >>> scary.action(colony)
          >>> terminator.action(colony)
          >>> terminator.place.name # ScaryThrower should scare for two turns
          'tunnel_0_5'
          >>> harvester.armor
          1
          >>> terminator.action(colony)
          >>> harvester.armor
          0
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing if effects stack
          >>> slow = SlowThrower()
          >>> terminator = Terminator(3)
          >>> slow_place = colony.places["tunnel_0_0"]
          >>> terminator_place = colony.places["tunnel_0_8"]
          >>> slow_place.add_fighter(slow)
          >>> terminator_place.add_fighter(terminator)
          >>> slow.action(colony)    # slow terminator two times
          >>> slow.action(colony)
          >>> colony.time = 1
          >>> terminator.action(colony) # do nothing. The outer slow has 2 turns to go, the inner one still has 3 turns
          >>> terminator.place.name
          'tunnel_0_8'
          >>> colony.time = 2
          >>> terminator.action(colony) # moves forward. The outer slow has 1 turn to go, the inner one has 2 turns
          >>> terminator.place.name
          'tunnel_0_7'
          >>> colony.time = 3
          >>> terminator.action(colony) # do nothing. The outer slow has no turns left, the inner one has 2 turns
          >>> terminator.place.name
          'tunnel_0_7'
          >>> colony.time = 4
          >>> terminator.action(colony) # moves forward. The inner slow has 1 turn
          >>> terminator.place.name
          'tunnel_0_6'
          >>> colony.time = 5
          >>> terminator.action(colony) # does nothing. The inner slow has no turns
          >>> terminator.place.name
          'tunnel_0_6'
          >>> colony.time = 6      # slow effects have worn off
          >>> terminator.action(colony)
          >>> terminator.place.name
          'tunnel_0_5'
          >>> colony.time = 7      # slow effects have worn off
          >>> terminator.action(colony)
          >>> terminator.place.name
          'tunnel_0_4'
          >>> colony.time = 8      # slow effects have worn off
          >>> terminator.action(colony)
          >>> terminator.place.name
          'tunnel_0_3'
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing multiple scared terminators
          >>> scare1 = ScaryThrower()
          >>> scare2 = ScaryThrower()
          >>> terminator1 = Terminator(3)
          >>> terminator2 = Terminator(3)

          >>> colony.places["tunnel_0_0"].add_fighter(scare1)
          >>> colony.places["tunnel_0_1"].add_fighter(terminator1)
          >>> colony.places["tunnel_0_4"].add_fighter(scare2)
          >>> colony.places["tunnel_0_5"].add_fighter(terminator2)

          >>> scare1.action(colony)
          >>> scare2.action(colony)
          >>> terminator1.action(colony)
          >>> terminator2.action(colony)

          >>> terminator1.place.name
          'tunnel_0_2'
          >>> terminator2.place.name
          'tunnel_0_6'

          >>> terminator1.action(colony)
          >>> terminator2.action(colony)

          >>> terminator1.place.name
          'tunnel_0_3'
          >>> terminator2.place.name
          'tunnel_0_7'

          >>> terminator1.action(colony)
          >>> terminator2.action(colony)

          >>> terminator1.place.name
          'tunnel_0_2'
          >>> terminator2.place.name
          'tunnel_0_6'
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> scare = ScaryThrower()
          >>> terminator = Terminator(3)
          >>> colony.places["tunnel_0_0"].add_fighter(scare)
          >>> colony.places["tunnel_0_1"].add_fighter(terminator)

          >>> scare.action(colony)
          >>> terminator.action(colony)

          >>> terminator.place.name
          'tunnel_0_2'

          >>> terminator.action(colony)

          >>> terminator.place.name
          'tunnel_0_3'

          >>> #
          >>> # Same terminator should not be scared more than once
          >>> scare.action(colony)
          >>> terminator.action(colony)

          >>> terminator.place.name
          'tunnel_0_2'
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> # Testing long effect stack
          >>> scary = ScaryThrower()
          >>> slow = SlowThrower()
          >>> terminator = Terminator(3)
          >>> colony.places["tunnel_0_0"].add_fighter(scary)
          >>> colony.places["tunnel_0_1"].add_fighter(slow)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator)

          >>> scary.action(colony) # scare terminator once

          >>> colony.time = 0
          >>> terminator.action(colony) # scared
          >>> terminator.place.name
          'tunnel_0_4'

          >>> for _ in range(3): # slow terminator three times
          ...     slow.action(colony)

          >>> colony.time = 1
          >>> terminator.action(colony) # scared, but also slowed thrice
          >>> terminator.place.name
          'tunnel_0_4'

          >>> colony.time = 2
          >>> terminator.action(colony) # scared and slowed thrice
          >>> terminator.place.name
          'tunnel_0_5'

          >>> colony.time = 3
          >>> terminator.action(colony) # slowed thrice
          >>> terminator.place.name
          'tunnel_0_5'

          >>> colony.time = 4
          >>> terminator.action(colony) # slowed twice
          >>> terminator.place.name
          'tunnel_0_4'

          >>> colony.time = 5
          >>> terminator.action(colony) # slowed twice
          >>> terminator.place.name
          'tunnel_0_4'

          >>> colony.time = 6
          >>> terminator.action(colony) # slowed once
          >>> terminator.place.name
          'tunnel_0_3'

          >>> colony.time = 7
          >>> terminator.action(colony) # status effects have worn off
          >>> terminator.place.name
          'tunnel_0_2'
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> scary = ScaryThrower()
          >>> slow = SlowThrower()
          >>> terminator = Terminator(3)
          >>> colony.places["tunnel_0_0"].add_fighter(scary)
          >>> colony.places["tunnel_0_1"].add_fighter(slow)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator)

          >>> slow.action(colony) # slow terminator
          >>> scary.action(colony) # scare terminator

          >>> terminator.place.name
          'tunnel_0_3'

          >>> colony.time = 0
          >>> terminator.action(colony) # scared and slowed
          >>> terminator.place.name
          'tunnel_0_4'

          >>> colony.time = 1
          >>> terminator.action(colony) # scared and slowed
          >>> terminator.place.name
          'tunnel_0_4'

          >>> colony.time = 2
          >>> terminator.action(colony) # slowed
          >>> terminator.place.name
          'tunnel_0_3'
          """,
                    'hidden': False,
                    'locked': False
                },
                {
                    'code': r"""
          >>> from dragons import *
          >>> ScaryThrower.implemented
          True
          >>> SlowThrower.implemented
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
      """,
            'teardown': '',
            'type': 'doctest'
        },
        {
            'cases': [
                {
                    'code': r"""
          >>> laser = LaserDragon()
          >>> dragon = HarvesterDragon(2)
          >>> terminator1 = Terminator(2)
          >>> terminator2 = Terminator(2)
          >>> terminator3 = Terminator(2)
          >>> terminator4 = Terminator(2)
          >>> colony.places["tunnel_0_0"].add_fighter(laser)
          >>> colony.places["tunnel_0_0"].add_fighter(terminator4)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator1)
          >>> colony.places["tunnel_0_3"].add_fighter(terminator2)
          >>> colony.places["tunnel_0_4"].add_fighter(dragon)
          >>> colony.places["tunnel_0_5"].add_fighter(terminator3)
          >>> laser.action(colony)
          >>> round(terminator4.armor, 2)
          0.0
          >>> round(terminator1.armor, 2)
          0.65
          >>> round(terminator2.armor, 2)
          0.7
          >>> round(dragon.armor, 2)
          0.95
          >>> round(terminator3.armor, 2)
          1.2
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
      """,
            'teardown': '',
            'type': 'doctest'
        },
        {
            'cases': [
                {
                    'code': r"""
          >>> from dragons import *
          >>> LaserDragon.implemented
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
