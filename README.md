# Scientific-calculator

A pastel Thai scientific calculator website with statistics, function plotting, calculation history, and keyboard support.

## Run the website

Open `index.html` in a modern web browser. The page uses the Mali font files in this repository; see `OFL.txt` for the font license.

## Features

- Scientific expressions, trigonometric functions, logarithms, constants, factorials, and DEG/RAD mode
- Descriptive statistics: mean, median, mode, population standard deviation, minimum, and maximum
- Function plotting with a configurable x range
- Calculation history stored in browser local storage
- Responsive layout and keyboard controls

## Project files

- `index.html` — website and its JavaScript classes
- `calculator sci/calculator-class-diagram.drawio` — editable diagrams.net class diagrams
- `calculator sci/class-diagram-1.png` and `class-diagram-2.png` — diagram images
- `calculator sci/build_report.py` — generates the project report PDF (requires Python, ReportLab, and Tahoma on Windows)

To build the report, install `calculator sci/requirements.txt`, then run:

```powershell
python "calculator sci/build_report.py"
```
