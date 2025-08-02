import time
import random

class Move:
    def __init__(self, name, fuel_cost, uses=float('inf')):
        self.name = name
        self.fuel_cost = fuel_cost
        self.remaining_uses = uses

    def can_use(self, current_fuel):
        return self.remaining_uses > 0 and current_fuel >= self.fuel_cost

    def use(self):
        if self.remaining_uses != float('inf'):
            self.remaining_uses -= 1


class OffensiveMove(Move):
    def __init__(self, name, fuel_cost, tire_damage, uses=float('inf')):
        super().__init__(name, fuel_cost, uses)
        self.tire_damage = tire_damage


class DefensiveMove(Move):
    def __init__(self, name, fuel_cost, damage_reduction_percent, uses=float('inf')):
        super().__init__(name, fuel_cost, uses)
        self.damage_reduction_percent = damage_reduction_percent


class Driver:
    def __init__(self, name, offensive_moves, defensive_moves):
        self.name = name
        self.tire_health = 100
        self.fuel = 500
        self.offensive_moves = offensive_moves
        self.defensive_moves = defensive_moves

    def is_alive(self):
        return self.tire_health > 0

    def choose_offensive_move(self):
        usable = [m for m in self.offensive_moves if m.can_use(self.fuel)]
        return random.choice(usable) if usable else None

    def choose_defensive_move(self):
        usable = [m for m in self.defensive_moves if m.can_use(self.fuel)]
        return random.choice(usable) if usable else None

    def has_usable_move(self):
        for move in self.offensive_moves + self.defensive_moves:
            if move.can_use(self.fuel):
                return True
        return False

    def apply_damage(self, amount): 
        self.tire_health -= amount
        if self.tire_health < 0:
            self.tire_health = 0

    def use_fuel(self, amount):
        self.fuel -= amount
        if self.fuel < 0:
            self.fuel = 0

    def show_status(self):
        print(f"{self.name} | Tire Health: {self.tire_health:.1f} | Fuel: {self.fuel:.1f}")


class Verstappen(Driver):
    def __init__(self):
        offensive = [
            OffensiveMove("DRS Boost", 45, 12),
            OffensiveMove("Red Bull Surge", 80, 20),
            OffensiveMove("Precision Turn", 30, 8)
        ]
        defensive = [
            DefensiveMove("Brake Late", 25, 30),
            DefensiveMove("ERS Deployment", 40, 50, uses=3)
        ]
        super().__init__("Verstappen", offensive, defensive)


class Mostafa(Driver):
    def __init__(self):
        offensive = [
            OffensiveMove("Turbo Start", 50, 10),
            OffensiveMove("Mercedes Charge", 90, 22),
            OffensiveMove("Corner Mastery", 25, 7)
        ]
        defensive = [
            DefensiveMove("Slipstream Cut", 20, 40),
            DefensiveMove("Aggressive Block", 35, 100, uses=2)
        ]
        super().__init__("Mostafa", offensive, defensive)


class Race:
    def __init__(self, driver1, driver2):
        self.driver1 = driver1
        self.driver2 = driver2
        self.turn = 0
        self.MAX_TURNS = 100  # ⛳ Maximum number of turns allowed

    def run(self):
        print("The Race Begins!\n")

        while self.driver1.is_alive() and self.driver2.is_alive():

            if self.turn >= self.MAX_TURNS:
                print("\n⏱️ Maximum turn limit reached. The race ends in a draw!")
                return

            if not self.driver1.has_usable_move() and not self.driver2.has_usable_move():
                print("\n⚠️ Both drivers are out of usable moves. The race ends in a tie!")
                return

            attacker = self.driver1 if self.turn % 2 == 0 else self.driver2
            defender = self.driver2 if self.turn % 2 == 0 else self.driver1

            print(f"\n🔄 Turn {self.turn + 1}: {attacker.name}'s turn to attack!")

            attack_move = attacker.choose_offensive_move()
            if not attack_move:
                print(f"{attacker.name} has no offensive moves left!")
                self.turn += 1
                continue

            attacker.use_fuel(attack_move.fuel_cost)
            attack_move.use()

            print(f"{attacker.name} uses {attack_move.name} (Fuel Cost: {attack_move.fuel_cost})")

            counter_moves = [m for m in defender.defensive_moves + defender.offensive_moves if m.can_use(defender.fuel)]
            counter_move = random.choice(counter_moves) if counter_moves else None

            if not counter_move:
                print(f"{defender.name} cannot defend or counterattack!")
                actual_damage = attack_move.tire_damage

            elif isinstance(counter_move, DefensiveMove):
                defender.use_fuel(counter_move.fuel_cost)
                counter_move.use()
                reduction = attack_move.tire_damage * (counter_move.damage_reduction_percent / 100)
                actual_damage = attack_move.tire_damage - reduction
                print(f"{defender.name} defends with {counter_move.name} (Reduces {counter_move.damage_reduction_percent}%)")
                print(f"💥 Final Damage = {actual_damage:.1f}")

            elif isinstance(counter_move, OffensiveMove):
                defender.use_fuel(counter_move.fuel_cost)
                counter_move.use()
                print(f"{defender.name} counterattacks with {counter_move.name}!")
                attacker.apply_damage(counter_move.tire_damage)
                actual_damage = attack_move.tire_damage
                print(f"{attacker.name} takes counterattack damage: {counter_move.tire_damage}")

            defender.apply_damage(actual_damage)

            print("\n📊 Status After Turn:")
            self.driver1.show_status()
            self.driver2.show_status()

            if not self.driver1.is_alive() or not self.driver2.is_alive():
                break

            self.turn += 1
            time.sleep(1)

        print("\n🏁 RACE FINISHED!")
        if self.driver1.is_alive() and not self.driver2.is_alive():
            print(f"🥇 {self.driver1.name} wins!")
        elif self.driver2.is_alive() and not self.driver1.is_alive():
            print(f"🥇 {self.driver2.name} wins!")
        else:
            print("🤝 It's a draw!")


if __name__ == "__main__":
    race = Race(Verstappen(), Mostafa())
    race.run()
