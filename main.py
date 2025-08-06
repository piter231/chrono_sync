import os
import time
import random
import json
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
        self.present = False
        self.paradox_resolved = False
    
    def short_str(self):
        status = "PRESENT" if self.present else "ABSENT"
        symbol = "✓" if self.paradox_resolved else "✗"
        return f"{self.name[:12]:<12} [{symbol}] ΔP={self.paradox_value:<2} | {status}"

class TemporalEvent:
    def __init__(self, description, effect, duration):
        self.description = description
        self.effect = effect
        self.duration = duration
        self.remaining = duration
    
    def tick(self):
        self.remaining -= 1
        return self.remaining <= 0

class ChronoSyncGame:
    def __init__(self):
        self.timeline_stability = 100
        self.chrono_energy = 50
        self.current_era = "PRESENT"
        self.era_history = []
        self.temporal_entities = []
        self.events = []
        self.time_loops = 0
        self.paradoxes_resolved = 0
        self.game_time = 0
        self.player_name = ""
        self.game_over = False
        self.win = False
        self.last_action = ""
        self.action_result = ""
        self.discovered_entities = []
        self.known_events = []
        self.terminal_width = 80
        
        self.entities = [
            TemporalEntity("Quantum Pharaoh", 8, "ANCIENT EGYPT"),
            TemporalEntity("Steam-Powered AI", 7, "VICTORIAN ERA"),
            TemporalEntity("Neo-Dinosaur", 9, "JURASSIC PERIOD"),
            TemporalEntity("Digital Ghost", 6, "NEAR FUTURE"),
            TemporalEntity("Time-Displaced Samurai", 7, "FEUDAL JAPAN"),
            TemporalEntity("AI Overlord", 10, "DISTANT FUTURE"),
            TemporalEntity("Cybernetic Viking", 8, "MEDIEVAL SCANDINAVIA"),
            TemporalEntity("Prehistoric Botanist", 6, "CRETACEOUS PERIOD"),
            TemporalEntity("Renaissance Android", 7, "RENAISSANCE ITALY"),
            TemporalEntity("Post-Apocalyptic Bard", 5, "POST-APOCALYPSE")
        ]
        
        self.event_pool = [
            TemporalEvent("Temporal Rift", "Creates bridge to another era", 5),
            TemporalEvent("Chrono-Storm", "Disrupts timeline stability", 4),
            TemporalEvent("Paradox Cascade", "Increases paradox values", 3),
            TemporalEvent("Reality Echo", "Duplicates entities", 6),
            TemporalEvent("Time Dilation", "Slows event progression", 7),
            TemporalEvent("Entropy Surge", "Accelerates timeline decay", 4),
            TemporalEvent("Stabilization Wave", "Boosts stability", 5),
            TemporalEvent("Chrono-Harvest", "Increases chrono energy", 4),
            TemporalEvent("Causality Loop", "Resets paradoxes", 6)
        ]
    
    def start(self):
        self.clear_screen()
        print(self.center_text("CHRONO-SYNC: TEMPORAL PARADOX SOLVER"))
        print(self.center_text("A Temporal Anomaly Resolution Experience"))
        print("\n" * 2)
        
        self.player_name = input("Enter your name as a Temporal Analyst: ").strip() or "Analyst"
        
        self.temporal_entities = random.sample(self.entities, 5)
        self.era_history = [self.current_era]
        self.discovered_entities = [e for e in self.temporal_entities if random.random() > 0.5]
        
        self.add_random_event()
        
        self.main_loop()
    
    def main_loop(self):
        while not self.game_over:
            self.game_time += 1
            self.timeline_stability = max(0, min(100, self.timeline_stability - random.randint(1, 3)))
            self.chrono_energy = min(100, self.chrono_energy + random.randint(1, 2))
            
            self.update_events()
            
            if random.random() < 0.3:
                self.add_random_event()
            
            if random.random() < 0.2 and len(self.discovered_entities) < len(self.temporal_entities):
                undiscovered = [e for e in self.temporal_entities if e not in self.discovered_entities]
                if undiscovered:
                    self.discovered_entities.append(random.choice(undiscovered))
                    self.action_result = f"Discovered: {self.discovered_entities[-1].name}"
            
            if self.timeline_stability <= 0:
                self.game_over = True
                self.win = False
            elif all(e.paradox_resolved for e in self.temporal_entities):
                self.game_over = True
                self.win = True
            
            self.display()
            
            if not self.game_over:
                self.get_player_action()
        
        self.display_final_outcome()
    
    def display(self):
        self.clear_screen()
        
        print(self.center_text("CHRONO-SYNC: TEMPORAL PARADOX SOLVER"))
        print(f"Analyst: {self.player_name:<20} Time Loops: {self.time_loops:<3} Game Time: {self.game_time}")
        print("-" * self.terminal_width)
        
        stability_status = self.get_timeline_status()
        print(f"Timeline Stability: {self.timeline_stability}/100 [{stability_status}]")
        print(self.progress_bar(self.timeline_stability, 100))
        print(f"Chrono Energy: {self.chrono_energy}/100")
        print(self.progress_bar(self.chrono_energy, 100, filled_char="▓", empty_char="░"))
        print("-" * self.terminal_width)
        
        print(f"Current Era: {self.current_era}")
        history_display = ' → '.join(self.era_history[-5:])
        if len(history_display) > self.terminal_width - 15:
            history_display = '...' + history_display[-self.terminal_width + 20:]
        print(f"Era History: {history_display}")
        print("-" * self.terminal_width)
        
        print("TEMPORAL ENTITIES:")
        if not self.discovered_entities:
            print("  No entities discovered - scan for anomalies")
        else:
            col_width = self.terminal_width // 2 - 2
            for i in range(0, len(self.discovered_entities), 2):
                line = ""
                if i < len(self.discovered_entities):
                    line += self.discovered_entities[i].short_str().ljust(col_width)
                if i + 1 < len(self.discovered_entities):
                    line += self.discovered_entities[i+1].short_str()
                print(line)
        print("-" * self.terminal_width)
        
        if self.events:
            print("ACTIVE TEMPORAL EVENTS:")
            for event in self.events:
                event_str = f"{event.description}: {event.effect} ({event.remaining} turns)"
                for line in textwrap.wrap(event_str, width=self.terminal_width - 2):
                    print(f"  {line}")
        else:
            print("No active temporal events")
        
        print("-" * self.terminal_width)
        
        if self.last_action:
            print(f"Last action: {self.last_action}")
        if self.action_result:
            for line in textwrap.wrap(self.action_result, width=self.terminal_width - 8):
                print(f"Result: {line}")
        
        print("-" * self.terminal_width)
    
    def get_player_action(self):
        print("ACTIONS:")
        print("1. Scan anomalies  2. Resolve paradox  3. Time jump")
        print("4. Contain entity  5. Stabilize       6. Analyze")
        print("7. Paradox report 8. Event info      9. Save/Load")
        print("0. Quit")
        
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
            self.contain_entity()
        elif choice == "5":
            self.stabilize_timeline()
        elif choice == "6":
            self.analyze_timeline()
        elif choice == "7":
            self.paradox_report()
        elif choice == "8":
            self.event_info()
        elif choice == "9":
            self.save_load_menu()
        elif choice == "0":
            self.game_over = True
            self.action_result = "Temporal operations terminated"
        else:
            self.action_result = "Invalid selection"
    
    def scan_for_anomalies(self):
        if self.chrono_energy < 15:
            self.action_result = "Insufficient chrono energy for scan"
            return
        
        self.chrono_energy -= 15
        self.last_action = "Scanning for temporal anomalies"
        
        if random.random() < 0.4 and len(self.discovered_entities) < len(self.temporal_entities):
            undiscovered = [e for e in self.temporal_entities if e not in self.discovered_entities]
            if undiscovered:
                new_entity = random.choice(undiscovered)
                self.discovered_entities.append(new_entity)
                self.action_result = f"Discovered new temporal entity: {new_entity.name}"
            else:
                self.action_result = "Scan completed - no new entities found"
        else:
            absent_entities = [e for e in self.discovered_entities if not e.present]
            if absent_entities:
                entity = random.choice(absent_entities)
                entity.present = True
                self.action_result = f"Detected temporal presence: {entity.name}"
            else:
                self.action_result = "Scan completed - all known entities already present"
    
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
                    self.action_result = f"{entity.name}'s paradox is already resolved"
                    return
                
                if not entity.present:
                    self.action_result = f"{entity.name} is not present in this timeline"
                    return
                
                if self.chrono_energy < entity.paradox_value * 5:
                    self.action_result = f"Insufficient energy to resolve {entity.name}'s paradox"
                    return
                
                self.clear_screen()
                print(f"Resolving {entity.name}'s paradox...")
                print("Match the frequency to neutralize the temporal anomaly")
                
                target_frequency = random.randint(1, 10)
                attempts = 3
                resolved = False
                
                while attempts > 0:
                    print(f"\nAttempts left: {attempts}")
                    try:
                        frequency = int(input("Enter frequency (1-10): "))
                        if frequency == target_frequency:
                            resolved = True
                            break
                        else:
                            diff = abs(target_frequency - frequency)
                            if diff <= 2:
                                print("Close! Adjust slightly")
                            else:
                                print("Way off! Try a different approach")
                            attempts -= 1
                    except:
                        attempts -= 1
                
                if resolved:
                    self.chrono_energy -= entity.paradox_value * 5
                    entity.paradox_resolved = True
                    self.paradoxes_resolved += 1
                    self.timeline_stability += 10
                    self.action_result = f"Successfully resolved {entity.name}'s paradox! Stability increased."
                else:
                    self.chrono_energy -= entity.paradox_value * 2
                    self.timeline_stability -= 5
                    self.action_result = f"Failed to resolve {entity.name}'s paradox! Energy wasted."
                
                self.last_action = f"Paradox resolution attempt on {entity.name}"
            else:
                self.action_result = "Invalid entity selection"
        except:
            self.action_result = "Invalid input"
    
    def time_jump(self):
        eras = ["ANCIENT EGYPT", "JURASSIC", "FEUDAL JAPAN", 
                "MEDIEVAL", "RENAISSANCE", "VICTORIAN",
                "PRESENT", "NEAR FUTURE", "DISTANT FUTURE", "POST-APOCALYPSE"]
        
        print("\nAvailable eras:")
        for i, era in enumerate(eras):
            print(f"{i+1}. {era}")
        
        try:
            choice = int(input("Select era to jump to: ")) - 1
            if 0 <= choice < len(eras):
                target_era = eras[choice]
                
                if target_era == self.current_era:
                    self.action_result = "Already in this era"
                    return
                
                cost = 25 + abs(choice - eras.index(self.current_era)) * 5
                
                if self.chrono_energy < cost:
                    self.action_result = f"Insufficient energy for jump to {target_era}"
                    return
                
                self.chrono_energy -= cost
                self.current_era = target_era
                self.era_history.append(target_era)
                
                era_entities = [e for e in self.discovered_entities if e.time_period.startswith(target_era)]
                for entity in era_entities:
                    entity.present = True
                
                self.last_action = f"Time jump to {target_era}"
                self.action_result = f"Jump successful! Entities from this era are now present."
                
                if random.random() < 0.3:
                    self.timeline_stability -= random.randint(5, 10)
                    self.action_result += " Timeline instability detected."
            else:
                self.action_result = "Invalid era selection"
        except:
            self.action_result = "Invalid input"
    
    def contain_entity(self):
        if not self.discovered_entities:
            self.action_result = "No entities to contain"
            return
        
        present_entities = [e for e in self.discovered_entities if e.present]
        if not present_entities:
            self.action_result = "No entities present to contain"
            return
        
        print("\nSelect entity to contain:")
        for i, entity in enumerate(present_entities):
            print(f"{i+1}. {entity.name}")
        
        try:
            choice = int(input("Selection: ")) - 1
            if 0 <= choice < len(present_entities):
                entity = present_entities[choice]
                
                if self.chrono_energy < 20:
                    self.action_result = "Insufficient energy for containment"
                    return
                
                self.chrono_energy -= 20
                entity.present = False
                
                if entity.paradox_resolved:
                    self.timeline_stability += 5
                    self.action_result = f"{entity.name} safely contained. Stability improved."
                else:
                    self.action_result = f"{entity.name} contained. Paradox remains unresolved."
                
                self.last_action = f"Containment of {entity.name}"
            else:
                self.action_result = "Invalid entity selection"
        except:
            self.action_result = "Invalid input"
    
    def stabilize_timeline(self):
        cost = 30
        if self.chrono_energy < cost:
            self.action_result = "Insufficient energy for stabilization"
            return
        
        self.chrono_energy -= cost
        stability_gain = random.randint(15, 25)
        self.timeline_stability = min(100, self.timeline_stability + stability_gain)
        
        self.last_action = "Timeline stabilization"
        self.action_result = f"Stability increased by {stability_gain}%"
    
    def analyze_timeline(self):
        self.last_action = "Timeline analysis"
        
        hidden_entities = [e for e in self.temporal_entities if e not in self.discovered_entities]
        if hidden_entities:
            entity = random.choice(hidden_entities)
            self.discovered_entities.append(entity)
            self.action_result = f"Analysis revealed hidden entity: {entity.name}"
        else:
            future_event = random.choice(self.event_pool)
            self.known_events.append(future_event)
            self.action_result = f"Analysis predicted future event: {future_event.description}"
    
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
    
    def event_info(self):
        if not self.known_events and not self.events:
            self.action_result = "No events to display"
            return
        
        self.clear_screen()
        print("TEMPORAL EVENT INFORMATION")
        print("-" * self.terminal_width)
        
        if self.known_events:
            print("PREDICTED EVENTS:")
            for event in self.known_events:
                print(f"  {event.description}: {event.effect}")
        
        if self.events:
            print("\nACTIVE EVENTS:")
            for event in self.events:
                print(f"  {event.description}: {event.effect} ({event.remaining} turns remaining)")
        
        print("\nPress Enter to continue...")
        input()
    
    def add_random_event(self):
        event = random.choice(self.event_pool)
        self.events.append(TemporalEvent(event.description, event.effect, event.duration))
        
        if "Rift" in event.description:
            all_entities = [e for e in self.entities if e not in self.temporal_entities]
            if all_entities:
                new_entity = random.choice(all_entities)
                self.temporal_entities.append(new_entity)
                if random.random() > 0.7:
                    self.discovered_entities.append(new_entity)
        elif "Storm" in event.description:
            self.timeline_stability -= 10
        elif "Cascade" in event.description:
            for entity in self.temporal_entities:
                if not entity.paradox_resolved:
                    entity.paradox_value = min(10, entity.paradox_value + 1)
        elif "Echo" in event.description:
            if self.temporal_entities:
                entity = random.choice(self.temporal_entities)
                clone = TemporalEntity(f"Echo of {entity.name}", 
                                      entity.paradox_value, 
                                      entity.time_period)
                clone.present = True
                self.temporal_entities.append(clone)
                self.discovered_entities.append(clone)
        elif "Dilation" in event.description:
            for e in self.events:
                if e != event:
                    e.remaining += 2
        elif "Entropy" in event.description:
            self.timeline_stability -= 15
        elif "Stabilization" in event.description:
            self.timeline_stability += 15
        elif "Harvest" in event.description:
            self.chrono_energy += 30
        elif "Loop" in event.description:
            for entity in self.temporal_entities:
                if not entity.paradox_resolved:
                    entity.paradox_value = max(5, entity.paradox_value - 2)
    
    def update_events(self):
        completed = []
        for event in self.events:
            if event.tick():
                completed.append(event)
        
        for event in completed:
            self.events.remove(event)
    
    def get_timeline_status(self):
        if self.timeline_stability >= 80:
            return TimelineState.STABLE.value
        elif self.timeline_stability >= 40:
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
    
    def save_load_menu(self):
        self.clear_screen()
        print("TEMPORAL ARCHIVE SYSTEM")
        print("1. Save Timeline  2. Load Timeline  3. Back")
        
        choice = input("Selection: ").strip()
        
        if choice == "1":
            self.save_game()
        elif choice == "2":
            self.load_game()
    
    def save_game(self):
        data = {
            "player_name": self.player_name,
            "timeline_stability": self.timeline_stability,
            "chrono_energy": self.chrono_energy,
            "current_era": self.current_era,
            "era_history": self.era_history,
            "temporal_entities": [
                {
                    "name": e.name,
                    "paradox_value": e.paradox_value,
                    "time_period": e.time_period,
                    "present": e.present,
                    "paradox_resolved": e.paradox_resolved
                } 
                for e in self.temporal_entities
            ],
            "discovered_entities": [e.name for e in self.discovered_entities],
            "events": [
                {
                    "description": e.description,
                    "effect": e.effect,
                    "duration": e.duration,
                    "remaining": e.remaining
                }
                for e in self.events
            ],
            "time_loops": self.time_loops,
            "paradoxes_resolved": self.paradoxes_resolved,
            "game_time": self.game_time
        }
        
        with open("chrono_sync_save.json", "w") as f:
            json.dump(data, f)
        
        self.action_result = "Timeline state saved successfully"
    
    def load_game(self):
        try:
            with open("chrono_sync_save.json", "r") as f:
                data = json.load(f)
            
            self.player_name = data["player_name"]
            self.timeline_stability = data["timeline_stability"]
            self.chrono_energy = data["chrono_energy"]
            self.current_era = data["current_era"]
            self.era_history = data["era_history"]
            self.time_loops = data["time_loops"]
            self.paradoxes_resolved = data["paradoxes_resolved"]
            self.game_time = data["game_time"]
            
            self.temporal_entities = []
            for e_data in data["temporal_entities"]:
                entity = TemporalEntity(
                    e_data["name"],
                    e_data["paradox_value"],
                    e_data["time_period"]
                )
                entity.present = e_data["present"]
                entity.paradox_resolved = e_data["paradox_resolved"]
                self.temporal_entities.append(entity)
            
            self.discovered_entities = []
            for name in data["discovered_entities"]:
                for entity in self.temporal_entities:
                    if entity.name == name:
                        self.discovered_entities.append(entity)
                        break
            
            self.events = []
            for e_data in data["events"]:
                event = TemporalEvent(
                    e_data["description"],
                    e_data["effect"],
                    e_data["duration"]
                )
                event.remaining = e_data["remaining"]
                self.events.append(event)
            
            self.action_result = "Timeline state loaded successfully"
        except:
            self.action_result = "Failed to load timeline state"
    
    def display_final_outcome(self):
        self.clear_screen()
        if self.win:
            print(self.center_text("TIMELINE STABILIZED"))
            print(self.center_text(f"Congratulations, {self.player_name}!"))
            print("\n" * 2)
            print(self.center_text("You successfully resolved all temporal paradoxes"))
            print(self.center_text(f"Resolved: {self.paradoxes_resolved} paradoxes"))
            print(self.center_text(f"Time Loops: {self.time_loops}"))
            print(self.center_text(f"Final Stability: {self.timeline_stability}%"))
        else:
            print(self.center_text("TIMELINE COLLAPSED"))
            print(self.center_text(f"Mission failed, {self.player_name}"))
            print("\n" * 2)
            print(self.center_text("The fabric of time unraveled due to instability"))
            print(self.center_text(f"Resolved: {self.paradoxes_resolved}/{len(self.temporal_entities)} paradoxes"))
            print(self.center_text(f"Final Stability: {self.timeline_stability}%"))
        
        print("\n" * 2)
        print(self.center_text("Thank you for playing CHRONO-SYNC"))
        print("\n" * 2)

if __name__ == "__main__":
    game = ChronoSyncGame()
    game.start()