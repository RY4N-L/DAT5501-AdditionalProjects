# DAT5501 Additional Projects

This repository contains additional projects for the DAT5501 module portfolio.  
Currently, it includes a **Calculator App** built using Python’s Tkinter library and a **Hex Pathfinding Visualiser** built with pygame.  
  
  PLEASE NOTE: The **Hex Pathfinding Visualiser** is currently fully AI-generated (using Copilot AI) and adapted for this project based on my original C# implementation.

---

## 🌟 Highlights

- Developed a **GUI calculator** with Tkinter.  
- Supports basic arithmetic operations: addition, subtraction, multiplication, division.  
- Includes extra functionality: decimal input, negation (+/−), clear/reset, and error handling (e.g., divide by zero).  
- Demonstrates event-driven programming and widget layout management with Tkinter’s grid system.  

- Used Copilot to generate code for an **interactive hex pathfinding visualiser** with pygame.  
- Inspired by a pathfinding visualisation tool I originally created in **Unity using C#**, with over 200 pages of documentation.
- Implements A* search, Dijkstra’s algorithm, and Depth‑First Search (DFS).  
- Provides real-time visualization of algorithm progress on a hexagonal grid.  
- Includes intuitive controls: mouse clicks to set start/end or toggle walls, keyboard shortcuts to run/reset algorithms.  

---

## 📂 Folder Structure

- `calculator_app.py` – main application file containing all logic and GUI components for calculator.  
- `hex_pathfinder_visualisation.py` – interactive pathfinding visualiser using hexagonal grids (pygame).  

---

## ⚙️ Requirements

- Python 3.9+  
- Tkinter (included in the Python standard library)  
- pygame  

Install dependencies:
```bash
pip install pygame
```

---

## 🚀 How to Run
Clone the repository:
``` bash
git clone https://github.com/RY4N-L/DAT5501-additional-projects.git
cd DAT5501-additional-projects
```
Run the calculator app:
``` bash
python calculator_app.py
```
Run the pathfinder visualiser:
```bash
python hex_pathfinder_visualisation.py
```

---
## 📝 Outstanding Tasks / To‑Do
- [ ] Add support for advanced operations (square root, exponentiation) in the calculator.
- [ ] Improve calculator GUI styling (fonts, colors, button layout).
- [ ] Add keyboard input support for calculator.
- [ ] Extend error handling for invalid inputs in both apps.
- [ ] Add grid size selection in pathfinder.
- [ ] Implement weighted edges for more complex pathfinding scenarios.
- [ ] Add GUI controls for all keyboard mapped buttons on pathfinder e.g. alogorithm selection and GO buttons.
---
