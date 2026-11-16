# Artificial Analysis leaderboard animation

Animation and export code for the historical Artificial Analysis Intelligence Index video. The included video ends on **1 November 2026** and shows selected snapshots from 2024 to 2026.

This repository contains code and the rendered video. It does not include the historical dataset, generated HTML with embedded scores, archived webpages, downloaded site code, or standalone logo assets. No synthetic dataset is bundled.

## Video

https://github.com/user-attachments/assets/e96825f6-e4c1-481e-8c7d-fbc85ebad868

[Download the video](artificial-analysis-history-2026-11-01.mp4)

1920 × 1080, 30 fps, H.264, 88.2 seconds, no audio. Each snapshot lasts 1.4 seconds with instant cuts, no fades, and no bar-growth animation.

Source: [Artificial Analysis Intelligence Index](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) and [Internet Archive](https://web.archive.org/web/https://artificialanalysis.ai/). Earlier versions were called the Quality Index. Scores are not comparable across benchmark versions. Older model selections are reconstructed, archive coverage is sampled, and not every release or benchmark revision is shown. Asterisks preserve the source's estimated-score flags. This independent reconstruction is not an official Artificial Analysis product.

## Build with your own data

Python 3.10 or newer is required. The build uses only the Python standard library.

```sh
python build.py /path/to/your/snapshots.json
```

Open `build/history.html` in your browser. Space plays or pauses; R or Home restarts; arrow keys step through frames. Add `?autoplay=1` to the file URL to start automatically.

The input is a JSON array of snapshots sorted by date. Each snapshot has:

| Field | Format |
| --- | --- |
| `date` | ISO date, `YYYY-MM-DD` |
| `version` | Historical benchmark name and version |
| `models` | Nonempty array of model records |

Each model has a `name` and a finite, nonnegative numeric `score`. Optional fields are `color` (CSS color), `lab` (creator name), `estimated` (boolean), and `logo` (inline image data URI). Logos default to creator initials when omitted. Models are sorted by score within each snapshot. Extra input metadata is not included in the generated HTML.

Supply only data and assets you have permission to use. Keep benchmark versions, dates, model configurations, and attribution accurate. The default title and source credit are for this Artificial Analysis video; override them for other data:

```sh
python build.py /path/to/your/snapshots.json --title "Your leaderboard" --source "Source: Your source" --output build/history.html --hold-ms 1400
```

Generated HTML contains the supplied data. Keep it private if you do not have redistribution rights. Files under `build/` and JSON/CSV inputs are ignored by Git.

## Export an MP4

Install FFmpeg and ensure `ffmpeg` is on your PATH, then install the renderer:

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python export.py build/history.html --output build/history.mp4
```

Alternatively pass `--browser` with the path to an existing Chrome or Chromium executable. The renderer opens the local HTML directly, checks logo decoding and model-label geometry, saves lossless PNG frames next to the output, and combines them with FFmpeg. No web server is needed. Playback timing comes from the generated HTML.

The original video used Calibri on Windows, with Segoe UI as fallback. Font availability on other systems can affect wrapping and appearance; the geometry checks stop export when labels clip or overlap. Inspect your output before sharing it.

## License

Original code and documentation are available under the [MIT license](LICENSE), credited to Utkarsh Patil. The included video and its third-party scores, names, and logos are excluded from that license. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). We do not grant redistribution rights for Artificial Analysis's dataset or trademark rights for the model creators' logos.

## Contributing

Edit `chart-template.html` for chart behavior and layout, `build.py` for input handling, and `export.py` for rendering and encoding. Use your own permitted local data to verify changes. Do not commit datasets, generated HTML, source-page archives, credentials, or additional exports. Preserve source attribution and the video license exclusions.
