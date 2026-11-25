// main.ts — entrypoint for the news-image-20261124 program.
// It runs the Pillow drawing program (draw.py, same directory) with the
// output path as its argument, then checks the file it wrote exists.
// The harness runs `node main.ts` with MAKEFUN_OUTPUT_DIR set (or
// /output by default) and no network.
import { spawnSync } from "node:child_process";
import { existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const TARGET = join(OUT_DIR, "entry.png");
const DRAW = join(HERE, "draw.py");

mkdirSync(OUT_DIR, { recursive: true });
const run = spawnSync("python3", [DRAW, TARGET], { stdio: "inherit" });
if (run.status !== 0) {
  throw new Error(`draw.py exited with status ${run.status}`);
}
if (!existsSync(TARGET)) {
  throw new Error(`draw.py did not write ${TARGET}`);
}
const size = statSync(TARGET).size;
if (size > 1048576) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
console.log(`wrote ${TARGET} (${size} bytes)`);
