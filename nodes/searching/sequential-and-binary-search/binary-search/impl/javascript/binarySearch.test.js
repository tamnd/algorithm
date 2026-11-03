// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/binary-search/. The authors are listed in prov/2B7QDX.jsonl.

import { test } from "node:test";
import assert from "node:assert/strict";
import { binarySearch } from "./binarySearch.js";

test("examples", () => {
  const a = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91];
  assert.equal(binarySearch(a, 23), 5);
  assert.equal(binarySearch(a, 2), 0);
  assert.equal(binarySearch(a, 91), 9);
  assert.equal(binarySearch(a, 30), -1);
  assert.equal(binarySearch(a, 1), -1);
  assert.equal(binarySearch(a, 100), -1);
});

test("edges", () => {
  assert.equal(binarySearch([], 1), -1);
  assert.equal(binarySearch([7], 7), 0);
  assert.equal(binarySearch(["ant", "bee", "cat"], "bee"), 1);
});

test("random against a linear scan", () => {
  let s = 2150;
  const next = (m) => {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    return (s >>> 8) % m;
  };
  for (let t = 0; t < 2000; t++) {
    const a = Array.from({ length: next(31) }, () => next(41) - 20).sort((p, q) => p - q);
    const x = next(51) - 25;
    const i = binarySearch(a, x);
    if (a.includes(x)) assert.equal(a[i], x);
    else assert.equal(i, -1);
  }
});
