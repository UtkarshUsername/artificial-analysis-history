"""Render a generated chart to PNG frames, then encode an H.264 video."""
import argparse
from pathlib import Path
import subprocess
from playwright.sync_api import sync_playwright

GEOMETRY = """() => {
 const labels=[...document.querySelectorAll('[data-model-label]')].map(e=>{
  const b=e.getBBox(),t=e.getCTM();
  return {name:e.dataset.modelLabel,p:[[b.x,b.y],[b.x+b.width,b.y],[b.x+b.width,b.y+b.height],[b.x,b.y+b.height]].map(([x,y])=>({x:t.a*x+t.c*y+t.e,y:t.b*x+t.d*y+t.f}))};
 });
 const overlap=(a,b)=>{
  for(const p of [a,b])for(let i=0;i<4;i++){
   const q=p[(i+1)%4],n={x:-(q.y-p[i].y),y:q.x-p[i].x};
   const u=a.map(v=>v.x*n.x+v.y*n.y),v=b.map(v=>v.x*n.x+v.y*n.y);
   if(Math.max(...u)<=Math.min(...v)||Math.max(...v)<=Math.min(...u))return false;
  }
  return true;
 };
 const errors=[];
 for(let i=0;i<labels.length;i++){
  const a=labels[i];if(a.p.some(p=>p.x<0||p.x>1920||p.y<0||p.y>976))errors.push('Clipped label: '+a.name);
  for(let j=i+1;j<labels.length;j++)if(overlap(a.p,labels[j].p))errors.push('Label overlap: '+a.name+' / '+labels[j].name);
 }
 return errors;
}"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="HTML produced by build.py")
    parser.add_argument("--output", type=Path, default=Path("build/history.mp4"))
    parser.add_argument("--browser", help="Optional Chromium executable path")
    args = parser.parse_args()
    html = args.html.resolve(strict=True)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    destination = output.parent / (output.stem + "-frames")
    destination.mkdir(exist_ok=True)

    with sync_playwright() as playwright:
        options = {"headless": True}
        if args.browser:
            options["executable_path"] = args.browser
        browser = playwright.chromium.launch(**options)
        try:
            page = browser.new_page(viewport={"width": 1920, "height": 1080}, device_scale_factor=1)
            page.goto(html.as_uri())
            page.evaluate("document.fonts.ready")
            page.evaluate("async () => { for (const src of logos) { const image = new Image(); image.src = src; await image.decode(); } }")
            count = page.evaluate("historyAnimation.frameCount")
            hold = page.evaluate("historyAnimation.frameDurationMs")
            for index in range(count):
                page.evaluate("index => historyAnimation.show(index)", index)
                errors = page.evaluate(GEOMETRY)
                if errors:
                    raise ValueError(f"Frame {index}: {errors}")
                page.screenshot(path=str(destination / f"frame-{index:03}.png"))
        finally:
            browser.close()

    subprocess.run([
        "ffmpeg", "-y", "-hide_banner", "-loglevel", "warning",
        "-framerate", f"1000/{hold}", "-i", str(destination / "frame-%03d.png"),
        "-vf", "fps=30", "-t", str(count * hold / 1000),
        "-c:v", "libx264", "-preset", "medium", "-crf", "16",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(output),
    ], check=True)
    print(f"Exported {count} snapshots to {output} ({count * hold / 1000:g} seconds).")


if __name__ == "__main__":
    main()
