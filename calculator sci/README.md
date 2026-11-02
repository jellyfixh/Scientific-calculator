# Scientific Calculator report

Source files for generating the Thai PDF report about the scientific calculator website in `../index.html`.

The editable diagrams.net file `calculator-class-diagram.drawio` has two pages: the classes in the local calculator and a separate reference model for NumerProject.

## Build

Requires Python 3.9 or later and ReportLab. From this folder run:

```powershell
python -m pip install -r requirements.txt
python build_report.py
```

The PDF is written to `../output/pdf/scientific-calculator-report.pdf` by default. Choose a different destination with:

```powershell
python build_report.py --output .\dist\my-report.pdf
```

The report uses the standard Tahoma font installed on Windows. Mali assets are retained in `assets/` for the website and its diagrams; see `assets/OFL.txt` for their license.

## Sources and scope

The report content is derived from the local scientific calculator source. The public Numerical Methods website remains the reference model on the second page of the editable diagram:

- https://numer.wilar.in.th/
- https://github.com/tonkaew131/NumerProject

The attached PDF informed only the section outline. Update `build_report.py` when the local calculator changes.
