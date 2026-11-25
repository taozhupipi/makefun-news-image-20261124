// main.ts — entrypoint for the news-image-20261124 program.
// Copies the pre-drawn entry.png (same directory, made by draw.py) into
// the output directory. Standard library only, no Python, no network:
// a plain byte copy, so two runs produce byte-identical output.
// Deliberate: the grading image runs node only, with no python3/PIL,
// so the entrypoint must never shell out to draw.py at grade time.
// The harness runs `node main.ts` with MAKEFUN_OUTPUT_DIR set (or
// /output by default).

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const SOURCE = join(HERE, "entry.png");
const TARGET = join(OUT_DIR, "entry.png");
const MAX_BYTES = 1024 * 1024;

if (!existsSync(SOURCE)) {
  throw new Error(`entry.png not found next to main.ts (${SOURCE})`);
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SOURCE, TARGET);

const srcSize = statSync(SOURCE).size;
const dstSize = statSync(TARGET).size;
if (srcSize !== dstSize) {
  throw new Error(
    `copy mismatch: ${SOURCE} is ${srcSize} bytes but ${TARGET} is ${dstSize} bytes`,
  );
}
if (dstSize > MAX_BYTES) {
  throw new Error(`entry.png is ${dstSize} bytes, over the 1 MiB limit`);
}
console.log(`wrote ${TARGET} (${dstSize} bytes)`);
