"""Build a self-contained leaderboard HTML from a user-supplied JSON file."""
import argparse
from datetime import date
import json
import math
from pathlib import Path


def normalize_frames(value):
    if not isinstance(value, list) or not value:
        raise ValueError("Input must be a nonempty array of dated snapshots.")
    frames = []
    previous_date = None
    for index, frame in enumerate(value):
        capture_date = date.fromisoformat(frame["date"])
        if previous_date and capture_date < previous_date:
            raise ValueError(f"Snapshot {index} is out of date order.")
        previous_date = capture_date
        if not isinstance(frame["version"], str) or not frame["version"].strip():
            raise ValueError(f"Snapshot {index} needs a benchmark version.")
        if not isinstance(frame["models"], list) or not frame["models"]:
            raise ValueError(f"Snapshot {index} needs at least one model.")
        models = []
        for model in frame["models"]:
            name, score = model["name"], model["score"]
            if not isinstance(name, str) or not name.strip():
                raise ValueError(f"Snapshot {index} contains an empty model name.")
            if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or score < 0:
                raise ValueError(f"Invalid score for {name} in snapshot {index}.")
            logo = model.get("logo") or ""
            if not isinstance(logo, str) or (logo and not logo.startswith("data:image/")):
                raise ValueError(f"Logo for {name} must be an inline image data URI.")
            models.append({
                "name": name, "score": score,
                "color": model.get("color") or "#666666",
                "lab": model.get("lab") or "",
                "logo": logo, "estimated": bool(model.get("estimated", False)),
            })
        frames.append({"date": frame["date"], "version": frame["version"], "models": sorted(models, key=lambda model: -model["score"])})
    return frames


def script_json(value):
    # Prevent user-supplied text from terminating the inline script element.
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False).replace("<", "\\u003c")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, help="Path to your own dated JSON snapshots")
    parser.add_argument("--output", type=Path, default=Path("build/history.html"))
    parser.add_argument("--title", default="Artificial Analysis Intelligence Index")
    parser.add_argument("--source", default="Source: Artificial Analysis · Internet Archive")
    parser.add_argument("--hold-ms", type=int, default=1400)
    args = parser.parse_args()
    if args.hold_ms <= 0:
        parser.error("--hold-ms must be positive")
    frames = normalize_frames(json.loads(args.data.read_text(encoding="utf-8-sig")))
    logos = list(dict.fromkeys(model["logo"] for frame in frames for model in frame["models"] if model["logo"]))
    logo_indices = {logo: index for index, logo in enumerate(logos)}
    for frame in frames:
        for model in frame["models"]:
            model["logo"] = logo_indices.get(model["logo"], -1)
    values = {
        "__FRAMES_JSON__": script_json(frames), "__LOGOS_JSON__": script_json(logos),
        "__TITLE_JSON__": script_json(args.title), "__SOURCE_JSON__": script_json(args.source),
        "__FRAME_DURATION_MS__": str(args.hold_ms),
    }
    template = Path(__file__).with_name("chart-template.html").read_text(encoding="utf-8")
    # One substitution pass keeps marker-like text in user data untouched.
    import re
    html = re.sub("|".join(map(re.escape, values)), lambda match: values[match.group()], template)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"Built {len(frames)} snapshots and {len(logos)} inline logos into {args.output}.")


if __name__ == "__main__":
    main()
