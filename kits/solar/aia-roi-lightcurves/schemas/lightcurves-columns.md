# AIA ROI Light-Curve Columns

Typical columns:

- `UTC`: timestamp in UTC.
- `Box_A`, `Box_B`, ...: one light curve per selected ROI box.
- `EXPTIME`: AIA exposure time when available.
- `QUALITY`: AIA quality flag when available.
- `Box_A_sat_frac`, `Box_B_sat_frac`, ...: estimated saturation fraction when
  emitted by the OpenMonitor export.

Exact column availability can vary by export version. The notebook detects the
available ROI columns automatically.
