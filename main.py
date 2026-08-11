from battle_sim import make_roster, assign_positions, run_battle

if __name__ == "__main__":
    roster = make_roster()

    team_a = [roster["Hoshino"], roster["Aru"], roster["Hifumi"]]
    team_b = [roster["Iori"], roster["Shiroko"], roster["Yuzu"]]

    assign_positions(team_a, "A")
    assign_positions(team_b, "B")

    print("Positions:")
    for c in team_a + team_b:
        print(f"  {c.name}: {c.pos} ({c.role})")

    run_battle(team_a, team_b, target_strategy="random")