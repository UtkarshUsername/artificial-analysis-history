# Artificial Analysis leaderboard animation

Code for animating historical Artificial Analysis Intelligence Index charts and exporting them to video.

## Video

https://github.com/user-attachments/assets/e96825f6-e4c1-481e-8c7d-fbc85ebad868

[Download the video](artificial-analysis-history-2026-11-01.mp4)

Selected snapshots from 2024 through **1 November 2026**. 1080p, 30 fps, 88.2 seconds. Each snapshot lasts 1.4 seconds, with instant cuts.

Sources: [Artificial Analysis](https://artificialanalysis.ai/evaluations/artificial-analysis-intelligence-index) and [Internet Archive](https://web.archive.org/web/https://artificialanalysis.ai/).

Earlier versions were called the Quality Index. Scores are not comparable across benchmark versions. Historical coverage is sampled, and older model selections are reconstructed. Asterisks indicate estimated scores.

## Build

Requires Python 3.10+. Supply your own data; the historical dataset is not included.

```sh
python build.py /path/to/your/snapshots.json
```

Open `build/history.html`. Space plays or pauses, R restarts, and arrow keys step through snapshots. Add `?autoplay=1` to start automatically.

The input is a JSON array sorted by date. Each snapshot needs `date` (`YYYY-MM-DD`), `version`, and a nonempty `models` array. Each model needs `name` and a finite, nonnegative `score`. Optional fields: `color`, `lab`, `estimated`, and `logo` (an inline image data URI).

Use `python build.py --help` for title, attribution, output, and timing options. Generated HTML embeds your data; only share it if you have redistribution rights.

## Export

Install FFmpeg and make sure it is on your PATH, then run:

```sh
python -m pip install -r requirements.txt
python -m playwright install chromium
python export.py build/history.html --output build/history.mp4
```

Use `--browser` to select an existing Chrome or Chromium executable. Export checks logo loading and label clipping or overlap. Fonts affect layout; the original video used Calibri with Segoe UI as fallback.

## License

Code and documentation: [MIT](LICENSE). The video and its third-party data and logos are excluded. See [third-party notices](THIRD_PARTY_NOTICES.md).
