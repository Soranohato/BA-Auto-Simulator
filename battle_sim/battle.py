# The battle loop: ATB turn order, tying combat math to actual turns.

# This is the "flow" layer - it decides who acts when, and hands off the
# actual to-hit/damage/cover questions to combat.py.

import random
import time

from .combat import pick_target, roll_damage
from .cover import get_cover_reduction, CoverObject
from .characters import Character
from .movement import is_in_range, move_toward

ATB_THRESHOLD = 100.0


def run_battle(team_a: list[Character], team_b: list[Character],
                target_strategy, cover_objects: list["CoverObject"], 
                max_ticks: int = 500):
    all_units = team_a + team_b

    # small random stagger so units don't all act in lockstep on tick 1
    for u in all_units:
        u.atb = random.uniform(0, 20)

    tick = 0
    while tick < max_ticks:
        if not any(u.is_alive for u in team_a) or not any(u.is_alive for u in team_b):
            break
        tick += 1

        for u in all_units:
            if u.is_alive:
                u.atb += u.spd

        ready = sorted(
            (u for u in all_units if u.is_alive and u.atb >= ATB_THRESHOLD),
            key=lambda u: u.atb, reverse=True,
        )

        for attacker in ready:
            if not attacker.is_alive:
                continue
            enemies = team_b if attacker in team_a else team_a
            if not any(e.is_alive for e in enemies):
                break

            defender = pick_target(attacker, enemies, strategy=target_strategy)

            if not is_in_range(attacker, defender):
                move_toward(attacker, defender, cover_objects, all_units)
                print(f"[tick {tick}] {attacker.name} moved to {attacker.pos}")
                time.sleep(0.5)
                attacker.atb -= ATB_THRESHOLD
                continue

            dmg, crit = roll_damage(attacker, defender)
            cover, provider = get_cover_reduction(defender, cover_objects)
            reduced_dmg = round(dmg * (1 - cover))

            if provider is not None:
                absorbed = dmg - reduced_dmg # TODO: tune this later
                provider.take_damage(absorbed)
                if provider.is_destroyed:
                    print(f"  >> {provider.name} was destroyed!")
                    time.sleep(1)
            
            defender.take_damage(reduced_dmg)
            attacker.atb -= ATB_THRESHOLD

            crit_tag = " (CRIT!)" if crit else ""
            cover_tag = f" (covered by {provider.name}, -{int(cover * 100)}%)" if provider else ""
            print(f"[tick {tick}] {attacker.name} hits {defender.name} for {dmg}{crit_tag}{cover_tag} "
                  f"[{defender.name} HP: {defender.hp}/{defender.max_hp}]")
            time.sleep(1)  # pause so it reads like real time


            if not defender.is_alive:
                print(f"  >> {defender.name} is down!")
                time.sleep(1)

    a_alive = any(c.is_alive for c in team_a)
    b_alive = any(c.is_alive for c in team_b)
    print("\n=== Battle Over ===")
    if a_alive and not b_alive:
        print(f"Team A wins! (tick {tick})")
    elif b_alive and not a_alive:
        print(f"Team B wins! (tick {tick})")
    else:
        print("Draw / timed out.")