# Solar AIA ROI Light Curves

Use this kit if you downloaded an AIA ROI light-curve result from Solar
OpenMonitor.

## Fastest Path

Open the notebook in Google Colab:

```text
https://colab.research.google.com/github/rudimirz/openmonitor-science-kits/blob/main/kits/solar/aia-roi-lightcurves/notebooks/openmonitor_aia_roi_colab.ipynb
```

Paste an OpenMonitor AIA job id, result id, or share link into the notebook.

The notebook is preloaded with this public demo run:

```text
aia_963db1ee7c6b49b9a9
```

Run all cells to download the cached result and inspect the exported FITS,
CSV, metadata, plot, and movie files.

## What Files Do I Need?

For a quick visual check:

- `lightcurves.csv`
- `lightcurves.png`
- `ROI_A.gif` / `ROI_B.gif` if available

For scientific reuse:

- `lightcurves.fits`
- `metadata.json`
- `science_bundle_manifest.json`

For support or reproducibility:

- `result.json`
- `frames_manifest.json`
- `run_manifest.json`

## What The Notebook Does

- downloads or accepts uploaded OpenMonitor AIA ROI exports;
- reads FITS, ECSV, or CSV light curves;
- prints ROI coordinates, wavelength, cadence, processing mode, and quality
  metadata;
- plots the curves on a UTC axis;
- exports a clean table and a metadata summary.

## Important Limitations

Current AIA ROI products are quick-look derived products for event inspection.
They preserve metadata, but they are not a replacement for a full calibrated
AIA reduction workflow.

For AIA ROI light curves, cite OpenMonitor and the underlying SDO/AIA data
providers.
