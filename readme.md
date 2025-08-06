# Chrono-Sync: Temporal Paradox Solver

![Gameplay Screenshot](https://github.com/piter231/chrono_sync/raw/main/terminal_screenshot.png)

Chrono-Sync is a text-based temporal anomaly resolution game where you play as a Temporal Analyst tasked with stabilizing collapsing timelines. Navigate through different eras, resolve paradoxes, and prevent the complete unraveling of reality!

## Game Overview

In Chrono-Sync, you'll:

- Discover temporal entities displaced from their native eras
- Resolve paradoxes caused by these displaced entities
- Manage timeline stability and chrono energy resources
- Jump between historical eras to contain anomalies
- Deal with temporal events that can help or hinder your mission

The fate of the timeline rests in your hands!

## Features

- 🌌 **Temporal Management Gameplay**: Balance timeline stability against chrono energy
- 🕰️ **Multiple Historical Eras**: Travel from Jurassic Period to Distant Future
- 👾 **Diverse Temporal Entities**: Quantum Pharaohs, Steam-Powered AIs, and more
- ⚡ **Dynamic Events**: Temporal rifts, chrono-storms, and paradox cascades
- 🧩 **Paradox Resolution Minigames**: Test your temporal tuning skills
- 💾 **Save/Load System**: Preserve your timeline progress
- 📊 **Detailed Status Display**: Visual progress bars and entity statuses

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

- **Timeline Stability**: Keep this above 0% to avoid game over
- **Chrono Energy**: Required for all major actions
- **Entities**: Discover and resolve paradoxes to stabilize the timeline
- **Events**: Temporal phenomena with various effects on gameplay

### Basic Controls

```
ACTIONS:
1. Scan anomalies  2. Resolve paradox  3. Time jump
4. Contain entity  5. Stabilize       6. Analyze
7. Paradox report  8. Event info      9. Save/Load
0. Quit
```

### Detailed Action Information

#### 1. Scan Anomalies

- **Cost**: 15 energy
- **Effects**:
  - 40% chance to discover a new temporal entity
  - Otherwise, makes a random absent entity present
- **Strategy**: Essential for discovering entities and making them available for resolution

#### 2. Resolve Paradox

The core puzzle mechanic where you neutralize temporal anomalies through frequency matching.

- **Cost**: Entity's Paradox Value (ΔP) × 5 energy
- **Requirements**:
  - Entity must be present
  - Entity must not already be resolved
- **Minigame**:

  ```
  Resolving Quantum Pharaoh's paradox...
  Match the frequency to neutralize the temporal anomaly

  Attempts left: 3
  Enter frequency (1-10):
  ```

- **Mechanics**:
  - 3 attempts to guess a random target (1-10)
  - Feedback system:
    - `Correct`: Exact match - paradox resolved!
    - `Close`: Guess within ±2 of target (e.g., target=5 → 3-7)
    - `Way off`: Guess ≥3 away from target
- **Success Effects**:
  - Paradox resolved (✓)
  - +10% timeline stability
- **Failure Effects**:
  - Lose ΔP × 2 energy
  - -5% timeline stability
- **Strategy Tips**:
  - Start with 5 (middle value)
  - After "close" feedback, adjust by 1-2 points
  - After "way off" feedback, make larger adjustments

#### 3. Time Jump

- **Cost**: 25 + (distance × 5) energy
  - Distance = difference in positions between current and target era
- **Effects**:
  - Travel to selected era
  - Makes all entities from that era present
  - 30% chance to cause -5% to -10% stability
- **Strategy**: Use to access specific entities or contain era-specific anomalies

#### 4. Contain Entity

- **Cost**: 20 energy
- **Requirements**: Entity must be present
- **Effects**:
  - Removes entity from present timeline
  - If resolved: +5% stability
  - If unresolved: No stability change
- **Strategy**: Temporary solution for unstable situations with unresolved entities

#### 5. Stabilize Timeline

- **Cost**: 30 energy
- **Effects**: +15% to +25% stability (random)
- **Strategy**: Efficient way to convert energy to stability when needed

#### 6. Analyze Timeline

- **Cost**: Free
- **Effects**:
  - Reveals a random hidden entity (if any)
  - If no hidden entities, predicts a future event
- **Strategy**: Use when you need more information before taking costly actions

#### 7. Paradox Report

- **Cost**: Free
- **Effects**: Shows detailed report of resolved/unresolved entities
- **Strategy**: Essential for planning your paradox resolution strategy

#### 8. Event Info

- **Cost**: Free
- **Effects**: Shows information about active and predicted events
- **Strategy**: Monitor events that could significantly impact your timeline

#### 9. Save/Load

- **Cost**: Free
- **Effects**: Save or load your game state
- **Strategy**: Preserve your progress before risky actions

#### 0. Quit

- **Cost**: Free
- **Effects**: Exit the game

### Turn-Based Changes

Each turn automatically:

- **Stability decreases**: 1-3%
- **Energy increases**: 1-2 (capped at 100)

### Entity Paradox Values (ΔP)

| Entity                 | ΔP  | Era                  | Native Era Bonus |
| ---------------------- | --- | -------------------- | ---------------- |
| Quantum Pharaoh        | 8   | Ancient Egypt        | ±1 → ±3 range    |
| Steam-Powered AI       | 7   | Victorian Era        | ±1 → ±3 range    |
| Neo-Dinosaur           | 9   | Jurassic Period      | ±1 → ±3 range    |
| Digital Ghost          | 6   | Near Future          | ±1 → ±3 range    |
| Time-Displaced Samurai | 7   | Feudal Japan         | ±1 → ±3 range    |
| AI Overlord            | 10  | Distant Future       | ±1 → ±3 range    |
| Cybernetic Viking      | 8   | Medieval Scandinavia | ±1 → ±3 range    |
| Prehistoric Botanist   | 6   | Cretaceous Period    | ±1 → ±3 range    |
| Renaissance Android    | 7   | Renaissance Italy    | ±1 → ±3 range    |
| Post-Apocalyptic Bard  | 5   | Post-Apocalypse      | ±1 → ±3 range    |

_Native Era Bonus: "Close" range expands to ±3 when resolving in entity's native era_

## Gameplay Tips

- **Frequency Strategy**:
  - First guess: 5 (middle value)
  - After "close": Adjust by 1-2 points
  - After "way off": Jump to opposite half of scale
- **Energy Management**: Always maintain enough energy for critical actions
- **Priority Targeting**: Focus on high-ΔP entities first for maximum stability gains
- **Strategic Jumping**: Plan era jumps to minimize distance costs
- **Native Era Advantage**: Resolve entities in their home eras for easier minigame
- **Event Awareness**: Temporal events can dramatically change game conditions
- **Containment Strategy**: Use containment for temporary relief with unresolved entities
- **Regular Scanning**: Discover new entities early to prevent surprises
- **Save Often**: Preserve your progress before risky paradox resolution attempts

## Paradox Resolution Examples

**Scenario 1: Target = 5**

- Guess 5: "Correct!" - Paradox resolved
- Guess 4: "Close! Adjust slightly"
- Guess 6: "Close! Adjust slightly"
- Guess 3: "Close! Adjust slightly" (in native era)
- Guess 1: "Way off! Try different approach"

**Scenario 2: Target = 8**

- Guess 5: "Way off! Try different approach"
- Guess 9: "Close! Adjust slightly"
- Guess 8: "Correct!" - Paradox resolved

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
