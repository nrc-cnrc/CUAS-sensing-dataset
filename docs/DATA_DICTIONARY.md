# Data Dictionary

Two file formats are used in this dataset. Both originate from the Echodyne
EchoGuard (MESA) radar system log, recorded at a 10 Hz track-update rate. Each
row is one update of one track; a track is the time-ordered sequence of rows
sharing the same track ID.

---

## 1. Annotated Excel workbooks (`.xlsx`)

Used in `Demo-0`, `Demo-2`, `Demo-3`, `Demo-5`, `Demo-6`.

### Sheet 1 — track data (11 columns)

| Column | Unit | Description |
|--------|------|-------------|
| `SystemTrackID` | — | Track identifier assigned by the radar system. All rows with the same ID belong to one track. May be `N/A` for a few unassociated rows. |
| `azimuth` | deg | Azimuth angle of the target relative to the radar boresight. |
| `elevation` | deg | Elevation angle of the target relative to the radar horizontal. |
| `range` | m | Slant range from radar to target. |
| `posX`, `posY`, `posZ` | m | Estimated target position in the radar's local Cartesian frame. |
| `veloX`, `veloY`, `veloZ` | m/s | Estimated target velocity components in the same frame. |
| `rcs` | dBsm | Radar cross-section of the associated measurement. `NaN` when no measurement was associated on that update. |

Note: `Demo-0` files order the columns `…, range, posX…posZ, veloX…veloZ, rcs`;
the Echodyne_Log files order them `…, posX…posZ, range, rcs, veloX…veloZ`.
Access columns by name, not position.

### Sheet 2 (`Sheet1`) — ground-truth labels

| Column | Description |
|--------|-------------|
| `SystemTrackID` | Track ID, joins to Sheet 1. |
| `Classification` | Expert-assigned ground-truth label, confirmed visually with the PTZ camera. |

Raw label values and their normalized equivalents (used in
[`../metadata/track_labels.csv`](../metadata/track_labels.csv)):

| Normalized | Raw values found in workbooks |
|------------|-------------------------------|
| `UAV` | `UAV` |
| `BIRD` | `Bird`, `BIRD`, `Burd` (typo) |
| `HUMAN` | `People`, `Human`, `Human/dog` |
| `VEHICLE` | `Car`, `Vehicle`, `Truck`, `small 4x4` |
| `MIXED` | `Mix of birds, people, car` and variants — sessions/tracks where multiple non-UAV target types could not be separated |
| `UNKNOWN` | blank / unresolved |

---

## 2. Raw radar log CSVs (`.csv`, `.csv.gz`)

Used in `Demo-1` (semicolon-delimited, 39 columns), `Demo-4` and `Demo-7`
(comma-delimited, 40 columns — the extra column is `SensorTrackID`).

Files named `Echodyne_Log_<date>_<time>.csv(.gz)` are complete session logs
containing every track the radar initiated (including clutter). Files named
`*_UAV_<id>.csv`, `*_TRUCK_<id>.csv`, or `DRONE_Id_<id>.csv` are curated
extracts of a single (occasionally a few) track(s) whose true class was
confirmed by ground-truth observation; the class and system track ID are
encoded in the file name.

| Column | Unit | Description |
|--------|------|-------------|
| `DOCAMeters` | m | Distance of closest approach (predicted) to the protected point. |
| `LifeTime` | updates | Age of the track (number of updates since initiation). |
| `LogDate` | — | Log date, `DD/MM/YYYY` (local time). |
| `LogTime` | — | Log wall-clock time (local), `HH:MM:SS.mmm` (truncated in some files). |
| `SensorTrackID` | — | Track ID assigned by the radar sensor (40-column format only). |
| `SystemTrackID` | — | Track ID assigned at system level after classification (`N/A` until assigned). |
| `TOCADays`, `TOCAMill` | days, ms | Time of closest approach (days part / milliseconds part). |
| `TrackExtendedNature` | — | Extended track nature reported by the system (e.g. `CLASSIF_UAV`, `CLASSIF_UNKNOWN`). |
| `TrackSource` | — | Originating sensor; always `ECHODYNE_MESA` in this dataset. |
| `UpdatedTrackType` | — | Radar/system real-time classification of the track at this update (`CLASSIF_UAV`, `CLASSIF_UNKNOWN`, …). This is the *system's* output, **not** ground truth. |
| `acquiredTimeDays`, `acuiredTimeMills` | days, ms | Track acquisition time (note: `acuired` typo is in the original log format). |
| `associatedMeasurementChiStatistic1..3` | — | Chi-square association statistics of the most recent associated measurements. |
| `associatedMeasurementId1..3` | — | IDs of the recent associated measurements. |
| `azimuth` | deg | Azimuth angle of the target. |
| `confidenceLevel` | % | Track confidence reported by the radar. |
| `elevation` | deg | Elevation angle of the target. |
| `id` | — | Sensor-level track identifier (matches `SensorTrackID` where present; use this to group rows into tracks). |
| `lastAssociatedDataTimeDays`, `lastAssociatedsDataTimeMills` | days, ms | Time of last associated measurement. |
| `lastUpdateTimeDays`, `lastUpdateTimeMills` | days, ms | Time of last track update. |
| `measurments` | — | Number of measurements associated on this update (typo in original format). |
| `posX`, `posY`, `posZ` | m | Estimated target position in the radar's local Cartesian frame. |
| `probUav` | 0–1 | Radar's estimated probability that the target is a UAV. |
| `probUnknow` | 0–1 | Radar's estimated probability that the target is unknown/other. |
| `range` | m | Slant range to target. |
| `rcs` | dBsm | Radar cross-section (`NaN`/empty when unavailable). |
| `state` | — | Track state machine value (e.g. 2 = confirmed/active). |
| `timeStamp` | — | UTC timestamp, ISO 8601 (`YYYYMMDDTHHMMSS.mmmZ`). Use this for time alignment. |
| `veloX`, `veloY`, `veloZ` | m/s | Estimated target velocity components. |

Some comma-delimited files carry a trailing empty column (`Unnamed: 40` in
pandas) caused by a trailing comma; it can be dropped.

---

## Consolidated metadata files

- [`../metadata/track_labels.csv`](../metadata/track_labels.csv) — one row per
  labeled track across the whole dataset: `folder`, `file`,
  `system_track_id`, `label` (normalized), `label_raw`, `label_source`
  (`manual annotation` = from an xlsx label sheet; `filename (curated
  extract)` = class encoded in a curated CSV's file name).
- [`../metadata/file_manifest.csv`](../metadata/file_manifest.csv) — one row
  per data file: format, size, row count, and number of labeled tracks.
