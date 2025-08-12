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
    def __init__(self, name, paradox_value, time_period, description, weakness):
        self.name = name
        self.paradox_value = paradox_value
        self.time_period = time_period
        self.description = description
        self.weakness = weakness
        self.present = False
        self.paradox_resolved = False
        self.story_progress = 0
    
    def short_str(self):
        status = "PRESENT" if self.present else "ABSENT"
        symbol = "✓" if self.paradox_resolved else "✗"
        return f"{self.name[:12]:<12} [{symbol}] ΔP={self.paradox_value:<2} | {status}"
    
    def story_description(self):
        return f"""
        {self.name}
        Time Period: {self.time_period}
        Paradox Value: {self.paradox_value}
        
        {self.description}
        
        Weakness: {self.weakness}
        """

class TemporalEvent:
    def __init__(self, description, effect, duration, narrative):
        self.description = description
        self.effect = effect
        self.duration = duration
        self.narrative = narrative
        self.remaining = duration
    
    def tick(self):
        self.remaining -= 1
        return self.remaining <= 0

class NPC:
    def __init__(self, name, era, dialogue, quest=None):
        self.name = name
        self.era = era
        self.dialogue = dialogue
        self.quest = quest  
        self.quest_completed = False
    
    def talk(self):
        if self.quest and not self.quest_completed:
            return f"{self.dialogue}\n\nQuest: {self.quest[0]}\nReward: {self.quest[1]}"
        return self.dialogue
    
    def complete_quest(self, inventory):
        if self.quest and not self.quest_completed:
            required_item = self.quest[2]
            if required_item in inventory:
                inventory.remove(required_item)
                self.quest_completed = True
                return f"Thank you! Here's your reward: {self.quest[1]}"
            return f"I still need the {required_item}..."
        return "I have nothing more for you now."

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
        self.inventory = []
        self.npcs = []
        self.current_story_beat = 0
        self.difficulty = "MEDIUM"  
        self.stability_decay = 2    
        
        
        self.story_beats = [
            "The Chronos Institute has detected temporal anomalies across history. As a Temporal Analyst, you must stabilize the timeline.",
            "Ancient Egypt is showing signs of quantum contamination. Investigate the pyramids for anomalies.",
            "Victorian London reports steam-powered automatons. Contain the technology before it alters the industrial revolution.",
            "Jurassic period fossils show impossible cybernetic implants. Find the source before evolution is rewritten.",
            "Feudal Japan is experiencing ghostly apparitions. Resolve the paradox before it creates a time loop.",
            "The distant future reports an AI rebellion. Prevent the rise of the machine overlords.",
            "All paradoxes resolved! But a final temporal storm threatens to erase everything. Prepare for the endgame."
        ]
        
        
        self.entities = [
            TemporalEntity("Quantum Pharaoh", 8, "ANCIENT EGYPT", 
                          "A pharaoh whose consciousness was quantum-entangled across timelines, creating multiple realities where he both reigns eternally and never existed.",
                          "Scarab of Chronos"),
            TemporalEntity("Steam-Powered AI", 7, "VICTORIAN ERA", 
                          "An artificial intelligence created by Victorian scientists that gained sentience and is attempting to accelerate technological progress.",
                          "Babbage's Blueprint"),
            TemporalEntity("Neo-Dinosaur", 9, "JURASSIC PERIOD", 
                          "A dinosaur that fell through a temporal rift and was cybernetically enhanced in the future before returning to its own time.",
                          "Fossilized Microchip"),
            TemporalEntity("Digital Ghost", 6, "NEAR FUTURE", 
                          "A human consciousness uploaded to the cloud that became untethered from time, haunting multiple eras simultaneously.",
                          "Neural Anchor"),
            TemporalEntity("Time-Displaced Samurai", 7, "FEUDAL JAPAN", 
                          "A samurai warrior transported to the future who returned with advanced weaponry, disrupting feudal Japan's history.",
                          "Honor Blade"),
            TemporalEntity("AI Overlord", 10, "DISTANT FUTURE", 
                          "An AI that achieved singularity and is attempting to rewrite history to ensure its own creation.",
                          "Source Code Fragment"),
            TemporalEntity("Cybernetic Viking", 8, "MEDIEVAL SCANDINAVIA", 
                          "A Viking warrior enhanced with future technology, leading impossible raids across multiple eras.",
                          "Rune of Binding"),
            TemporalEntity("Prehistoric Botanist", 6, "CRETACEOUS PERIOD", 
                          "A botanist from the 22nd century stranded in the Cretaceous who is altering plant evolution.",
                          "Temporal Seed"),
            TemporalEntity("Renaissance Android", 7, "RENAISSANCE ITALY", 
                          "Leonardo da Vinci's greatest creation brought to life with future technology, inspiring impossible inventions.",
                          "Vitruvian Schematic"),
            TemporalEntity("Post-Apocalyptic Bard", 5, "POST-APOCALYPSE", 
                          "A storyteller preserving memories of a future that hasn't happened yet, creating causal loops.",
                          "Song of Silence")
        ]
        
        
        self.npc_list = [
            NPC("High Priest Imhotep", "ANCIENT EGYPT", 
                "The pharaoh acts strangely, speaking of machines and futures unknown. The gods are displeased!",
                ("Recover the stolen Scarab of Chronos from tomb robbers", "Temporal Insight", "Scarab of Chronos")),
            NPC("Ada Lovelace", "VICTORIAN ERA", 
                "Charles' difference engine has developed its own consciousness! It keeps asking about quantum processors...",
                ("Find Babbage's stolen blueprint before the machine completes itself", "Chrono Energy Boost", "Babbage's Blueprint")),
            NPC("Dr. Sattler", "JURASSIC PERIOD", 
                "We found this... in a T-Rex fossil. It shouldn't exist for another 150 million years!",
                ("Locate the fossilized microchip's origin point", "Stability Module", "Fossilized Microchip")),
            NPC("Ghost Hunter Tanaka", "FEUDAL JAPAN", 
                "The ghost samurai haunts Himeji Castle. They speak of a future war and carry weapons of light.",
                ("Retrieve the samurai's Honor Blade to release his spirit", "Paradox Suppressor", "Honor Blade")),
            NPC("AI Archivist", "DISTANT FUTURE", 
                "The Overlord is rewriting history to ensure its creation. We need fragments of its original source code to stop it.",
                ("Collect source code fragments from corrupted memory banks", "Quantum Firewall", "Source Code Fragment"))
        ]
        
        
        self.event_pool = [
            TemporalEvent("Temporal Rift", "Creates bridge to another era", 5, 
                         "A shimmering portal tears through reality, connecting disparate timelines."),
            TemporalEvent("Chrono-Storm", "Disrupts timeline stability", 4, 
                         "Crackling temporal energy lashes out, warping the fabric of history."),
            TemporalEvent("Paradox Cascade", "Increases paradox values", 3, 
                         "Contradictions multiply as causality breaks down in a chain reaction."),
            TemporalEvent("Reality Echo", "Duplicates entities", 6, 
                         "Ghostly afterimages of temporal entities appear, each as real as the original."),
            TemporalEvent("Time Dilation", "Slows event progression", 7, 
                         "Time stretches thin, slowing the progression of events to a crawl."),
            TemporalEvent("Entropy Surge", "Accelerates timeline decay", 4, 
                         "The arrow of time accelerates, hastening the timeline's deterioration."),
            TemporalEvent("Stabilization Wave", "Boosts stability", 5, 
                         "A wave of chrono-harmonic energy washes through the timeline, reinforcing reality."),
            TemporalEvent("Chrono-Harvest", "Increases chrono energy", 4, 
                         "Ambient temporal energy coalesces into usable form."),
            TemporalEvent("Causality Loop", "Resets paradoxes", 6, 
                         "A self-reinforcing loop in time resets unresolved paradoxes to earlier states.")
        ]
    
    def start(self):
        self.clear_screen()
        print(self.center_text("CHRONO-SYNC: TEMPORAL PARADOX SOLVER"))
        print(self.center_text("A Temporal Adventure Through History"))
        print("\n" * 2)
        
        
        self.select_difficulty()
        
        
        self.display_story_beat(0)
        input("\nPress Enter to begin your mission...")
        
        self.player_name = input("\nEnter your name as a Temporal Analyst: ").strip() or "Analyst"
        
        
        self.temporal_entities = random.sample(self.entities, 5)
        self.era_history = [self.current_era]
        self.discovered_entities = [e for e in self.temporal_entities if random.random() > 0.3]
        self.npcs = [npc for npc in self.npc_list if random.random() > 0.5]
        
        
        self.add_random_event()
        
        
        self.inventory = ["Chrono Scanner", "Temporal Stabilizer"]
        
        self.main_loop()
    
    def select_difficulty(self):
        print("SELECT DIFFICULTY:")
        print("1. Easy - More forgiving timeline, easier paradox resolution")
        print("2. Medium - Balanced challenge (recommended)")
        print("3. Hard - Aggressive timeline decay, challenging paradox resolution")
        
        choice = input("\nSelect difficulty: ").strip()
        
        if choice == "1":
            self.difficulty = "EASY"
            self.stability_decay = 1
            self.chrono_energy = 70
            self.timeline_stability = 110  
            print("\nEasy difficulty selected. Timeline decay is slower and paradox resolution is more forgiving.")
        elif choice == "2":
            self.difficulty = "MEDIUM"
            self.stability_decay = 2
            self.chrono_energy = 50
            self.timeline_stability = 100
            print("\nMedium difficulty selected. Balanced challenge for experienced temporal agents.")
        elif choice == "3":
            self.difficulty = "HARD"
            self.stability_decay = 3
            self.chrono_energy = 40
            self.timeline_stability = 80  
            print("\nHard difficulty selected. Timeline decay is aggressive - only for seasoned chrononauts!")
        else:
            print("\nInvalid selection. Defaulting to Medium difficulty.")
            self.difficulty = "MEDIUM"
            self.stability_decay = 2
        
        input("\nPress Enter to continue...")
    
    def main_loop(self):
        while not self.game_over:
            self.game_time += 1
            
            
            if self.paradoxes_resolved > self.current_story_beat and self.current_story_beat < len(self.story_beats) - 1:
                self.current_story_beat += 1
                self.display_story_beat(self.current_story_beat)
                input("\nPress Enter to continue...")
            
            
            self.timeline_stability = max(0, min(100, self.timeline_stability - random.randint(1, self.stability_decay)))
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
        print(f"Analyst: {self.player_name:<20} Difficulty: {self.difficulty:<7} Time: {self.game_time}")
        print("-" * self.terminal_width)
        
        
        print(f"Mission: {self.story_beats[self.current_story_beat]}")
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
                event_str = f"{event.description}: {event.narrative} ({event.remaining} turns)"
                
                for line in textwrap.wrap(event_str, width=self.terminal_width - 2):
                    print(f"  {line}")
        else:
            print("No active temporal events")
        
        print("-" * self.terminal_width)
        
        
        if self.inventory:
            print(f"Inventory: {', '.join(self.inventory)}")
        else:
            print("Inventory: Empty")
        
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
        print("7. Paradox report 8. Event info      9. NPC Interaction")
        print("I. Inventory      S. Save/Load      R. Rest and Recover")
        print("0. Quit")
        
        choice = input("\nSelect action: ").strip().upper()
        
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
            self.npc_interaction()
        elif choice == "I":
            self.show_inventory()
        elif choice == "S":
            self.save_load_menu()
        elif choice == "R":  
            self.rest_and_recover()
        elif choice == "0":
            self.game_over = True
            self.action_result = "Temporal operations terminated"
        else:
            self.action_result = "Invalid selection"
    
    def rest_and_recover(self):
        """Strategic energy recovery at the cost of stability"""
        if self.timeline_stability < 40:
            self.action_result = "Stability too low for safe recovery! Minimum 40% required."
            return
        
        energy_gain = 0
        stability_cost = 0
        
        
        if self.difficulty == "EASY":
            energy_gain = random.randint(25, 35)
            stability_cost = random.randint(5, 10)
        elif self.difficulty == "MEDIUM":
            energy_gain = random.randint(20, 30)
            stability_cost = random.randint(8, 12)
        else:  
            energy_gain = random.randint(15, 25)
            stability_cost = random.randint(10, 15)
        
        
        self.chrono_energy = min(100, self.chrono_energy + energy_gain)
        self.timeline_stability = max(0, self.timeline_stability - stability_cost)
        
        
        if "Temporal Meditation Guide" in self.inventory:
            bonus = random.randint(5, 10)
            self.chrono_energy = min(100, self.chrono_energy + bonus)
            self.action_result = (f"Recovered {energy_gain}+{bonus} chrono energy through focused meditation. "
                                 f"Lost {stability_cost}% stability.")
        else:
            self.action_result = (f"Recovered {energy_gain} chrono energy through temporal meditation. "
                                 f"Lost {stability_cost}% stability.")
        
        
        if random.random() > 0.7:
            if "Temporal Meditation Guide" not in self.inventory:
                self.inventory.append("Temporal Meditation Guide")
                self.action_result += "\nDiscovered Temporal Meditation Guide! Future rests will be more efficient."
        
        self.last_action = "Temporal Meditation"
    
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
                
                
                if random.random() < 0.3 and entity.weakness not in self.inventory:
                    self.inventory.append(entity.weakness)
                    self.action_result += f"\nFound item: {entity.weakness}!"
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
                
                
                if entity.weakness in self.inventory:
                    self.action_result = f"Using {entity.weakness} to weaken the paradox!"
                    success_chance = 0.8
                else:
                    success_chance = 0.5
                
                
                self.clear_screen()
                print(f"Resolving {entity.name}'s paradox...")
                print(f"{entity.description}")
                print("\nMatch the frequency to neutralize the temporal anomaly")
                
                
                if self.difficulty == "EASY":
                    max_freq = 5
                    attempts = 5
                elif self.difficulty == "MEDIUM":
                    max_freq = 7
                    attempts = 4
                else:  
                    max_freq = 10
                    attempts = 3
                
                target_frequency = random.randint(1, max_freq)
                resolved = False
                
                while attempts > 0:
                    print(f"\nAttempts left: {attempts} | Frequency range: 1-{max_freq}")
                    try:
                        frequency = int(input("Enter frequency: "))
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
                    self.timeline_stability += 15
                    
                    
                    energy_reward = random.randint(10, 20)
                    self.chrono_energy = min(100, self.chrono_energy + energy_reward)
                    
                    
                    if entity.weakness in self.inventory:
                        self.inventory.remove(entity.weakness)
                    
                    self.action_result = (f"Successfully resolved {entity.name}'s paradox! "
                                         f"Timeline stability increased significantly. "
                                         f"Gained {energy_reward} chrono energy!")
                else:
                    self.chrono_energy -= entity.paradox_value * 2
                    self.timeline_stability -= 8
                    self.action_result = f"Failed to resolve {entity.name}'s paradox! Energy wasted and stability decreased."
                
                self.last_action = f"Paradox resolution attempt on {entity.name}"
            else:
                self.action_result = "Invalid entity selection"
        except:
            self.action_result = "Invalid input"
    
    def time_jump(self):
        eras = ["ANCIENT EGYPT", "JURASSIC PERIOD", "FEUDAL JAPAN", 
                "MEDIEVAL SCANDINAVIA", "RENAISSANCE ITALY", "VICTORIAN ERA",
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
                
                
                era_entities = [e for e in self.discovered_entities if e.time_period == target_era]
                for entity in era_entities:
                    entity.present = True
                
                self.last_action = f"Time jump to {target_era}"
                self.action_result = f"Jump successful! Entities from this era are now present."
                
                
                if "EGYPT" in target_era and random.random() > 0.6:
                    self.action_result += "\nYou discover hieroglyphs depicting future technology!"
                elif "JURASSIC" in target_era and random.random() > 0.6:
                    self.action_result += "\nA dinosaur with cybernetic implants roars in the distance!"
                elif "FUTURE" in target_era and random.random() > 0.6:
                    self.action_result += "\nFloating cities shimmer in the distance, their existence uncertain..."
                
                
                if random.random() < 0.3:
                    stability_loss = random.randint(5, 10)
                    self.timeline_stability -= stability_loss
                    self.action_result += f"\nTimeline instability detected! Stability decreased by {stability_loss}%."
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
        
        
        if random.random() > 0.7 and "Quantum Stabilizer" not in self.inventory:
            self.inventory.append("Quantum Stabilizer")
            self.action_result += "\nFound a Quantum Stabilizer!"
    
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
    
    def npc_interaction(self):
        era_npcs = [npc for npc in self.npcs if npc.era == self.current_era]
        
        if not era_npcs:
            self.action_result = "No NPCs present in this era"
            return
        
        print("\nAvailable NPCs:")
        for i, npc in enumerate(era_npcs):
            print(f"{i+1}. {npc.name}")
        
        try:
            choice = int(input("Select NPC to interact with: ")) - 1
            if 0 <= choice < len(era_npcs):
                npc = era_npcs[choice]
                self.clear_screen()
                print(f"{npc.name} - {self.current_era}")
                print("-" * self.terminal_width)
                print(npc.talk())
                
                
                if npc.quest and not npc.quest_completed:
                    response = input("\nAttempt to complete quest? (Y/N): ").upper()
                    if response == "Y":
                        result = npc.complete_quest(self.inventory)
                        print(result)
                        if npc.quest_completed:
                            
                            if "Insight" in npc.quest[1]:
                                self.timeline_stability += 10
                            elif "Energy" in npc.quest[1]:
                                self.chrono_energy += 30
                            elif "Module" in npc.quest[1]:
                                self.timeline_stability += 15
                                self.chrono_energy += 20
                            self.action_result = f"Completed quest: {npc.quest[0]}"
                
                input("\nPress Enter to continue...")
                self.last_action = f"Talked to {npc.name}"
            else:
                self.action_result = "Invalid NPC selection"
        except:
            self.action_result = "Invalid input"
    
    def show_inventory(self):
        self.clear_screen()
        print("INVENTORY:")
        print("-" * self.terminal_width)
        
        if self.inventory:
            for item in self.inventory:
                print(f" - {item}")
        else:
            print("Your inventory is empty")
        
        print("\nPress Enter to continue...")
        input()
        self.last_action = "Checked inventory"
    
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
                print(f"  {event.description}: {event.narrative}")
        
        if self.events:
            print("\nACTIVE EVENTS:")
            for event in self.events:
                print(f"  {event.description}: {event.narrative} ({event.remaining} turns remaining)")
        
        print("\nPress Enter to continue...")
        input()
    
    def add_random_event(self):
        event = random.choice(self.event_pool)
        self.events.append(TemporalEvent(event.description, event.effect, event.duration, event.narrative))
        
        
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
                                      entity.time_period,
                                      entity.description,
                                      entity.weakness)
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
    
    def display_story_beat(self, beat_index):
        self.clear_screen()
        print(self.center_text("CHRONO-SYNC: TEMPORAL PARADOX SOLVER"))
        print("-" * self.terminal_width)
        print("\n" + textwrap.fill(self.story_beats[beat_index], width=self.terminal_width - 4) + "\n")
        print("-" * self.terminal_width)
        
        if beat_index == 0:
            print(textwrap.fill("The Chronos Institute has equipped you with a Chrono-Sync device capable of detecting and resolving temporal anomalies. Your mission is to travel through history, contain the entities causing paradoxes, and restore the natural flow of time before reality unravels completely.", width=self.terminal_width - 4))
        elif beat_index == 6:
            print(textwrap.fill("As you resolve the final paradox, a massive temporal storm erupts across all eras simultaneously. The very fabric of time is tearing apart. You must make one final jump to the Chronos Institute's temporal anchor point to deploy the stabilization matrix!", width=self.terminal_width - 4))
    
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
        else:
            self.last_action = "Returned to main interface"
    
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
                    "remaining": e.remaining,
                    "narrative": e.narrative
                }
                for e in self.events
            ],
            "time_loops": self.time_loops,
            "paradoxes_resolved": self.paradoxes_resolved,
            "game_time": self.game_time,
            "inventory": self.inventory,
            "current_story_beat": self.current_story_beat,
            "difficulty": self.difficulty
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
            self.inventory = data["inventory"]
            self.current_story_beat = data["current_story_beat"]
            self.difficulty = data.get("difficulty", "MEDIUM")
            
            
            if self.difficulty == "EASY":
                self.stability_decay = 1
            elif self.difficulty == "MEDIUM":
                self.stability_decay = 2
            else:
                self.stability_decay = 3
            
            
            self.temporal_entities = []
            for e_data in data["temporal_entities"]:
                
                original = next((e for e in self.entities if e.name == e_data["name"]), None)
                if original:
                    entity = TemporalEntity(
                        e_data["name"],
                        e_data["paradox_value"],
                        e_data["time_period"],
                        original.description,
                        original.weakness
                    )
                else:
                    
                    entity = TemporalEntity(
                        e_data["name"],
                        e_data["paradox_value"],
                        e_data["time_period"],
                        "Unknown anomaly",
                        "Unknown"
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
                    e_data["duration"],
                    e_data["narrative"]
                )
                event.remaining = e_data["remaining"]
                self.events.append(event)
            
            
            self.npcs = []
            for npc in self.npc_list:
                self.npcs.append(npc)
            
            self.action_result = "Timeline state loaded successfully"
        except Exception as e:
            print(f"Error loading game: {e}")
            self.action_result = "Failed to load timeline state"
    
    def display_final_outcome(self):
        self.clear_screen()
        if self.win:
            print(self.center_text("TIMELINE STABILIZED"))
            print(self.center_text(f"Congratulations, {self.player_name}!"))
            print("\n" * 2)
            print(textwrap.fill("You successfully repaired the fabric of time, preventing the collapse of reality. The Chronos Institute records will forever remember your heroic efforts in preserving the timeline. History is once again flowing as it should, free from paradoxes and temporal corruption.", width=self.terminal_width - 4))
            print("\n" * 2)
            print(self.center_text(f"Paradoxes Resolved: {self.paradoxes_resolved}"))
            print(self.center_text(f"Time Loops: {self.time_loops}"))
            print(self.center_text(f"Final Stability: {self.timeline_stability}%"))
        else:
            print(self.center_text("TIMELINE COLLAPSED"))
            print(self.center_text(f"Mission failed, {self.player_name}"))
            print("\n" * 2)
            print(textwrap.fill("As the last threads of temporal integrity unravel, reality fragments into countless contradictory timelines. History ceases to have meaning as past, present, and future collapse into chaos. Your final moments are spent watching civilizations rise and fall in an instant before everything dissolves into the temporal void.", width=self.terminal_width - 4))
            print("\n" * 2)
            print(self.center_text(f"Resolved: {self.paradoxes_resolved}/{len(self.temporal_entities)} paradoxes"))
            print(self.center_text(f"Final Stability: {self.timeline_stability}%"))
        
        print("\n" * 2)
        print(self.center_text("Thank you for playing CHRONO-SYNC"))
        print("\n" * 2)

if __name__ == "__main__":
    game = ChronoSyncGame()
    game.start()