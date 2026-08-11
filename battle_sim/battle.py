# The battle loop: ATB turn order, tying combat math to actual turns.

# This is the "flow" layer - it decides who acts when, and hands off the
# actual to-hit/damage/cover questions to combat.py.

import random

from .combat import get_cover_reduction, pick_target, roll_damage
from .characters import Character

ATB_THRESHOLD = 100.0


def run_battle(team_a: list[Character], team_b: list[Character],
                target_strategy, max_ticks: int = 500):
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
            dmg, crit = roll_damage(attacker, defender)
            cover, provider = get_cover_reduction(defender, enemies)
            dmg = round(dmg * (1 - cover))
            defender.take_damage(dmg)
            attacker.atb -= ATB_THRESHOLD

            crit_tag = " (CRIT!)" if crit else ""
            cover_tag = f" (covered by {provider.name}, -{int(cover * 100)}%)" if provider else ""
            print(f"[tick {tick}] {attacker.name} hits {defender.name} for {dmg}{crit_tag}{cover_tag} "
                  f"[{defender.name} HP: {defender.hp}/{defender.max_hp}]")

            if not defender.is_alive:
                print(f"  >> {defender.name} is down!")

    a_alive = any(c.is_alive for c in team_a)
    b_alive = any(c.is_alive for c in team_b)
    print("\n=== Battle Over ===")
    if a_alive and not b_alive:
        print(f"Team A wins! (tick {tick})")
    elif b_alive and not a_alive:
        print(f"Team B wins! (tick {tick})")
    else:
        print("Draw / timed out.")