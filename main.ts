/**
 * make.fun entry: "Sum up 24 November's world news in one image".
 *
 * The infographic (entry.png) is rendered by draw.py with Pillow.
 * This program only copies that pre-drawn image into the output
 * directory. It uses the Node standard library alone and performs a
 * plain byte copy, so two runs write byte-identical output.
 */
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png not found next to main.ts (${source})`);
}

mkdirSync(outDir, { recursive: true });
const dest = join(outDir, "entry.png");
copyFileSync(source, dest);

const srcBytes = statSync(source).size;
const dstBytes = statSync(dest).size;
if (srcBytes !== dstBytes) {
  throw new Error(
    `copy mismatch: ${source} is ${srcBytes} bytes but ${dest} is ${dstBytes} bytes`,
  );
}
// The gate requires a PNG or JPEG of at most 1 MiB and 1024x1024.
if (dstBytes > 1048576) {
  throw new Error(`entry.png is ${dstBytes} bytes, over the 1 MiB limit`);
}
console.log(`wrote ${dest} (${dstBytes} bytes)`);
