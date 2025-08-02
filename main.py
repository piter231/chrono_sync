import os
import time
import random
from enum import Enum
import textwrap

class TimelineState(Enum):
    STABLE = "STABLE"
    UNSTABLE = "UNSTABLE"
    COLLAPSED = "COLLAPSED"

class TemporalEntity:
    def __init__(self, name, paradox_value, time_period):
        self.name = name
        self.paradox_value = paradox_value
        self.time_period = time_period
        self.paradox_resolved = False
    
    def short_str(self):
        symbol = "✓" if self.paradox_resolved else "✗"
        return f"{self.name[:12]:<12} [{symbol}] ΔP={self.paradox_value:<2}"

class ChronoSyncGame:
    def __init__(self):
        self.timeline_stability = 100
        self.chrono_energy = 50
        self.current_era = "PRESENT"
        self.entities = []
        self.time_loops = 0
        self.paradoxes_resolved = 0
        self.game_time = 0
        self.player_name = ""
        self.game_over = False
        self.win = False
        self.last_action = ""
        self.action_result = ""
        self.discovered_entities = []
        self.terminal_width = 80
        
        # Game entities
        self.entity_pool = [
            TemporalEntity("Quantum Pharaoh", 4, "ANCIENT EGYPT"),
            TemporalEntity("Steam-Powered AI", 5, "VICTORIAN ERA"),
            TemporalEntity("Neo-Dinosaur", 6, "JURASSIC PERIOD"),
            TemporalEntity("Digital Ghost", 3, "NEAR FUTURE"),
            TemporalEntity("Time-Displaced Samurai", 5, "FEUDAL JAPAN"),
            TemporalEntity("AI Overlord", 7, "DISTANT FUTURE")
        ]
    
    def start(self):
        self.clear_screen()
        print(self.center_text("CHRONO-SYNC: TEMPORAL PARADOX SOLVER"))
        print(self.center_text("A Temporal Anomaly Resolution Experience"))
        print("\n" * 2)
        
        self.player_name = input("Enter your name as a Temporal Analyst: ").strip() or "Analyst"
        
        # Initialize game state
        self.entities = random.sample(self.entity_pool, 4)
        self.discovered_entities = [self.entities[0], self.entities[1]]
        
        self.main_loop()
    
    def main_loop(self):
        while not self.game_over:
            self.game_time += 1
            self.timeline_stability = max(0, min(100, self.timeline_stability - random.randint(1, 2)))
            self.chrono_energy = min(100, self.chrono_energy + random.randint(1, 2))
            
            # Check win/loss conditions
            if self.timeline_stability <= 0:
                self.game_over = True
                self.win = False
            elif all(e.paradox_resolved for e in self.entities):
                self.game_over = True
                self.win = True
            
            # Display game state
            self.display()
            
            if not self.game_over:
                self.get_player_action()
        
        self.display_final_outcome()
    
    def display(self):
        self.clear_screen()
        
        # Header
        print(self.center_text("CHRONO-SYNC: TEMPORAL PARADOX SOLVER"))
        print(f"Analyst: {self.player_name:<20} Time: {self.game_time}")
        print("-" * self.terminal_width)
        
        # Stability and energy
        stability_status = self.get_timeline_status()
        print(f"Timeline Stability: {self.timeline_stability}/100 [{stability_status}]")
        print(self.progress_bar(self.timeline_stability, 100))
        print(f"Chrono Energy: {self.chrono_energy}/100")
        print(self.progress_bar(self.chrono_energy, 100, filled_char="▓", empty_char="░"))
        print("-" * self.terminal_width)
        
        # Current era
        print(f"Current Era: {self.current_era}")
        print("-" * self.terminal_width)
        
        # Temporal entities
        print("TEMPORAL ENTITIES:")
        if not self.discovered_entities:
            print("  No entities discovered - scan for anomalies")
        else:
            # Display in two columns
            col_width = self.terminal_width // 2 - 2
            for i in range(0, len(self.discovered_entities), 2):
                line = ""
                # First column
                if i < len(self.discovered_entities):
                    line += self.discovered_entities[i].short_str().ljust(col_width)
                # Second column
                if i + 1 < len(self.discovered_entities):
                    line += self.discovered_entities[i+1].short_str()
                print(line)
        print("-" * self.terminal_width)
        
        # Action feedback
        if self.last_action:
            print(f"Last action: {self.last_action}")
        if self.action_result:
            # Wrap long result messages
            for line in textwrap.wrap(self.action_result, width=self.terminal_width - 8):
                print(f"Result: {line}")
        
        print("-" * self.terminal_width)
    
    def get_player_action(self):
        print("ACTIONS:")
        print("1. Scan anomalies  2. Resolve paradox  3. Time jump")
        print("4. Stabilize       5. Paradox report   0. Quit")
        
        choice = input("\nSelect action: ").strip()
        
        self.last_action = ""
        self.action_result = ""
        
        if choice == "1":
            self.scan_for_anomalies()
        elif choice == "2":
            self.resolve_paradox()
        elif choice == "3":
            self.time_jump()
        elif choice == "4":
            self.stabilize_timeline()
        elif choice == "5":
            self.paradox_report()
        elif choice == "0":
            self.game_over = True
            self.action_result = "Temporal operations terminated"
        else:
            self.action_result = "Invalid selection"
    
    def scan_for_anomalies(self):
        if self.chrono_energy < 10:
            self.action_result = "Insufficient chrono energy for scan"
            return
        
        self.chrono_energy -= 10
        self.last_action = "Scanning for temporal anomalies"
        
        # Discover new entity
        if len(self.discovered_entities) < len(self.entities):
            undiscovered = [e for e in self.entities if e not in self.discovered_entities]
            if undiscovered:
                new_entity = random.choice(undiscovered)
                self.discovered_entities.append(new_entity)
                self.action_result = f"Discovered: {new_entity.name}"
            else:
                self.action_result = "Scan completed - all entities discovered"
        else:
            self.action_result = "Scan completed - all entities already discovered"
    
    def resolve_paradox(self):
        if not self.discovered_entities:
            self.action_result = "No entities to resolve"
            return
        
        print("\nSelect entity to resolve:")
        for i, entity in enumerate(self.discovered_entities):
            print(f"{i+1}. {entity.name} (ΔP={entity.paradox_value})")
        
        try:
            choice = int(input("Selection: ")) - 1
            if 0 <= choice < len(self.discovered_entities):
                entity = self.discovered_entities[choice]
                
                if entity.paradox_resolved:
                    self.action_result = f"{entity.name}'s paradox already resolved"
                    return
                
                if self.chrono_energy < entity.paradox_value * 4:
                    self.action_result = f"Need {entity.paradox_value*4} energy to resolve"
                    return
                
                # Paradox resolution minigame
                self.clear_screen()
                print(f"Resolving {entity.name}'s paradox...")
                print("Match the frequency to neutralize anomaly (1-5)")
                
                target_frequency = random.randint(1, 5)
                attempts = 2
                resolved = False
                
                while attempts > 0:
                    print(f"\nAttempts left: {attempts}")
                    try:
                        frequency = int(input("Enter frequency: "))
                        if frequency == target_frequency:
                            resolved = True
                            break
                        else:
                            diff = abs(target_frequency - frequency)
                            if diff == 1:
                                print("Close! Adjust slightly")
                            else:
                                print("Way off! Try different approach")
                            attempts -= 1
                    except:
                        attempts -= 1
                
                if resolved:
                    self.chrono_energy -= entity.paradox_value * 4
                    entity.paradox_resolved = True
                    self.paradoxes_resolved += 1
                    self.timeline_stability += 15
                    self.action_result = f"Resolved {entity.name}'s paradox! +15 stability"
                else:
                    self.chrono_energy -= entity.paradox_value * 2
                    self.timeline_stability -= 5
                    self.action_result = f"Failed to resolve {entity.name}'s paradox"
                
                self.last_action = f"Paradox resolution on {entity.name}"
            else:
                self.action_result = "Invalid entity selection"
        except:
            self.action_result = "Invalid input"
    
    def time_jump(self):
        eras = ["ANCIENT EGYPT", "JURASSIC", "FEUDAL JAPAN", 
                "VICTORIAN", "PRESENT", "NEAR FUTURE", "DISTANT FUTURE"]
        
        print("\nAvailable eras:")
        for i, era in enumerate(eras):
            print(f"{i+1}. {era}")
        
        try:
            choice = int(input("Select era: ")) - 1
            if 0 <= choice < len(eras):
                target_era = eras[choice]
                
                if target_era == self.current_era:
                    self.action_result = "Already in this era"
                    return
                
                cost = 20
                
                if self.chrono_energy < cost:
                    self.action_result = f"Need {cost} energy for jump"
                    return
                
                self.chrono_energy -= cost
                self.current_era = target_era
                
                self.last_action = f"Jump to {target_era}"
                self.action_result = f"Jump successful! Timeline stabilized"
                
                # Era jump stabilizes timeline
                self.timeline_stability += 10
            else:
                self.action_result = "Invalid era selection"
        except:
            self.action_result = "Invalid input"
    
    def stabilize_timeline(self):
        cost = 25
        if self.chrono_energy < cost:
            self.action_result = "Insufficient energy for stabilization"
            return
        
        self.chrono_energy -= cost
        stability_gain = random.randint(15, 25)
        self.timeline_stability = min(100, self.timeline_stability + stability_gain)
        
        self.last_action = "Timeline stabilization"
        self.action_result = f"Stability increased by {stability_gain}%"
    
    def paradox_report(self):
        self.clear_screen()
        print("PARADOX RESOLUTION REPORT")
        print("-" * self.terminal_width)
        
        resolved = [e for e in self.discovered_entities if e.paradox_resolved]
        unresolved = [e for e in self.discovered_entities if not e.paradox_resolved]
        
        print(f"Resolved: {len(resolved)}/{len(self.discovered_entities)}")
        for entity in resolved:
            print(f"  ✓ {entity.name}")
        
        print(f"\nUnresolved: {len(unresolved)}/{len(self.discovered_entities)}")
        for entity in unresolved:
            print(f"  ✗ {entity.name} (ΔP={entity.paradox_value})")
        
        print("\nPress Enter to continue...")
        input()
    
    def get_timeline_status(self):
        if self.timeline_stability >= 70:
            return TimelineState.STABLE.value
        elif self.timeline_stability >= 30:
            return TimelineState.UNSTABLE.value
        else:
            return TimelineState.COLLAPSED.value
    
    def progress_bar(self, value, max_value, length=30, filled_char="█", empty_char=" "):
        filled_length = int(length * value // max_value)
        bar = filled_char * filled_length + empty_char * (length - filled_length)
        return f"[{bar}]"
    
    def center_text(self, text):
        return text.center(self.terminal_width)
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_final_outcome(self):
        self.clear_screen()
        if self.win:
            print(self.center_text("TIMELINE STABILIZED"))
            print(self.center_text(f"Congratulations, {self.player_name}!"))
            print("\n" * 2)
            print(self.center_text("You successfully resolved all temporal paradoxes"))
            print(self.center_text(f"Resolved: {self.paradoxes_resolved} paradoxes"))
            print(self.center_text(f"Final Stability: {self.timeline_stability}%"))
        else:
            print(self.center_text("TIMELINE COLLAPSED"))
            print(self.center_text(f"Mission failed, {self.player_name}"))
            print("\n" * 2)
            print(self.center_text("The fabric of time unraveled due to instability"))
            print(self.center_text(f"Resolved: {self.paradoxes_resolved}/{len(self.entities)} paradoxes"))
            print(self.center_text(f"Final Stability: {self.timeline_stability}%"))
        
        print("\n" * 2)
        print(self.center_text("Thank you for playing CHRONO-SYNC"))
        print("\n" * 2)

if __name__ == "__main__":
    game = ChronoSyncGame()
    game.start()