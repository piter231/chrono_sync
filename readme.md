# Chrono-Sync: Temporal Paradox Solver - Adventure Edition

![Gameplay Screenshot](https://github.com/piter231/chrono_sync/raw/main/terminal_screenshot.png)

Chrono-Sync is a text-based temporal anomaly resolution adventure where you play as a Temporal Analyst tasked with stabilizing collapsing timelines. Travel through historical eras, interact with key figures, resolve paradoxes, and prevent the complete unraveling of reality!

## Game Overview

In Chrono-Sync, you'll:

- Discover temporal entities displaced from their native eras
- Resolve paradoxes through challenging minigames
- Manage timeline stability and chrono energy resources
- Travel through 10 historical eras from Jurassic Period to Distant Future
- Complete NPC quests and collect powerful items
- Deal with dynamic temporal events that shape gameplay

The fate of the timeline rests in your hands!

## New Features in Adventure Edition

- 📖 **Story-Driven Campaign**: 7 story beats that progress as you resolve paradoxes
- 🧑‍🤝‍🧑 **NPC Interactions**: Meet historical figures with unique quests
- 🎒 **Inventory System**: Collect artifacts to aid in paradox resolution
- ⚖️ **Difficulty Levels**: Choose from Easy, Medium, or Hard modes
- 🧘 **Temporal Meditation**: Convert stability to energy in critical situations
- 🏆 **Enhanced Rewards**: Gain bonus energy after resolving paradoxes

## Installation

1. Clone the repository:

```bash
git clone https://github.com/piter231/chrono_sync.git
```

2. Navigate to the project directory:

```bash
cd chrono_sync
```

3. Run the game:

```bash
python main.py
```

## Requirements

- Python 3.6 or higher
- No additional dependencies required

## How to Play

### Core Mechanics

- **Timeline Stability**: Keep this above 0% to avoid game over (1-3% decay per turn)
- **Chrono Energy**: Required for all major actions (1-2 regeneration per turn)
- **Entities**: Discover and resolve paradoxes to stabilize the timeline
- **Events**: Temporal phenomena with narrative descriptions
- **Inventory**: Collect items that provide advantages in gameplay

### Complete Action List

```
ACTIONS:
1. Scan anomalies  2. Resolve paradox  3. Time jump
4. Contain entity  5. Stabilize       6. Analyze
7. Paradox report  8. Event info      9. NPC Interaction
I. Inventory      S. Save/Load      R. Rest and Recover
0. Quit
```

### Detailed Action Information

#### 1. Scan Anomalies (15 energy)

- 40% chance to discover new entity
- Otherwise makes a random absent entity present
- May find weakness items for entities

#### 2. Resolve Paradox (ΔP × 5 energy)

The core puzzle mechanic where you neutralize temporal anomalies through frequency matching.

- **Difficulty Settings**:
  - Easy: 1-5 range, 5 attempts
  - Medium: 1-7 range, 4 attempts
  - Hard: 1-10 range, 3 attempts
- **Success Effects**:
  - Paradox resolved (✓)
  - +15% timeline stability
  - Gain 10-20 bonus energy
- **Failure Effects**:
  - Lose ΔP × 2 energy
  - -8% timeline stability

#### 3. Time Jump (25 + distance×5 energy)

- Travel to selected era
- Makes all entities from that era present
- Era-specific narrative events
- 30% chance of stability loss

#### 4. Contain Entity (20 energy)

- Removes entity from present timeline
- +5% stability if resolved
- No stability change if unresolved

#### 5. Stabilize Timeline (30 energy)

- +15% to +25% stability
- Chance to find Quantum Stabilizer item

#### 6. Analyze Timeline (Free)

- Reveals random hidden entity OR
- Predicts future temporal event

#### 7. Paradox Report (Free)

- Detailed report of resolved/unresolved entities

#### 8. Event Info (Free)

- Shows information about active and predicted events

#### 9. NPC Interaction (Free)

- Talk to historical figures in current era
- Complete quests for powerful rewards

#### I. Inventory (Free)

- View collected items
- Items provide advantages in gameplay

#### S. Save/Load (Free)

- Preserve timeline progress
- Resume your mission later

#### R. Rest and Recover (Free)

- Convert stability to energy
- Minimum 40% stability required
- Gain 15-35 energy at cost of 5-15% stability
- Find Temporal Meditation Guide for bonuses

#### 0. Quit (Free)

- Exit the game

### Difficulty Levels

Choose your challenge level at game start:

1. **Easy**:

   - Starting stability: 110%
   - Starting energy: 70
   - Paradox minigame: 1-5 range, 5 attempts
   - Stability decay: 1% per turn

2. **Medium (Recommended)**:

   - Starting stability: 100%
   - Starting energy: 50
   - Paradox minigame: 1-7 range, 4 attempts
   - Stability decay: 1-2% per turn

3. **Hard**:
   - Starting stability: 80%
   - Starting energy: 40
   - Paradox minigame: 1-10 range, 3 attempts
   - Stability decay: 1-3% per turn

### Temporal Entities

| Entity                 | ΔP  | Era                  | Weakness             |
| ---------------------- | --- | -------------------- | -------------------- |
| Quantum Pharaoh        | 8   | Ancient Egypt        | Scarab of Chronos    |
| Steam-Powered AI       | 7   | Victorian Era        | Babbage's Blueprint  |
| Neo-Dinosaur           | 9   | Jurassic Period      | Fossilized Microchip |
| Digital Ghost          | 6   | Near Future          | Neural Anchor        |
| Time-Displaced Samurai | 7   | Feudal Japan         | Honor Blade          |
| AI Overlord            | 10  | Distant Future       | Source Code Fragment |
| Cybernetic Viking      | 8   | Medieval Scandinavia | Rune of Binding      |
| Prehistoric Botanist   | 6   | Cretaceous Period    | Temporal Seed        |
| Renaissance Android    | 7   | Renaissance Italy    | Vitruvian Schematic  |
| Post-Apocalyptic Bard  | 5   | Post-Apocalypse      | Song of Silence      |

## Advanced Strategies

### Energy Management

- **Rest and Recover**: Use when stability >60% and energy <30
- **Complete NPC Quests**: Look for energy reward quests
- **Target Low-ΔP Entities**: Resolve easier paradoxes first for energy rewards
- **Monitor Events**: Chrono-Harvest events provide +30 energy

### Stability Preservation

- Contain resolved entities (+5% stability)
- Complete stabilization quests from NPCs
- Use Quantum Stabilizer items when available
- Avoid unnecessary time jumps (risk stability loss)

### Paradox Resolution

1. Start with middle value (5 for Easy, 4 for Medium, 5 for Hard)
2. Use "Close!" feedback to make small adjustments (±1-2)
3. Use "Way off!" feedback to make larger adjustments (±3-4)
4. Leverage weakness items for +30% success chance
5. Prioritize entities in their native eras

### Era Strategy

- **Ancient Egypt**: High chance of finding Scarab of Chronos
- **Victorian Era**: Complete Ada Lovelace quest for energy boost
- **Jurassic Period**: Scan for Fossilized Microchip
- **Near Future**: Higher chance of energy-related events
- **Distant Future**: Critical for resolving AI Overlord

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues or feature requests, please open an issue on the [GitHub repository](https://github.com/piter231/chrono_sync/issues).

---

**Embark on your temporal journey today and save reality from complete collapse!**
