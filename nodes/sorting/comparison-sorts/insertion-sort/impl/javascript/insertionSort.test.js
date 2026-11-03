// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.

import { test } from "node:test";
import assert from "node:assert/strict";
import { insertionSort } from "./insertionSort.js";

test("example", () => {
  assert.deepEqual(insertionSort([5, 2, 4, 6, 1, 3]), [1, 2, 3, 4, 5, 6]);
});

test("edges", () => {
  assert.deepEqual(insertionSort([]), []);
  assert.deepEqual(insertionSort([1]), [1]);
  assert.deepEqual(insertionSort([3, 2, 1, 1]), [1, 1, 2, 3]);
  assert.deepEqual(insertionSort(["pear", "fig", "apple"]), ["apple", "fig", "pear"]);
});

test("random against Array.prototype.sort", () => {
  let s = 2150;
  const next = (m) => {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    return (s >>> 8) % m;
  };
  for (let t = 0; t < 500; t++) {
    const a = Array.from({ length: next(41) }, () => next(101) - 50);
    const want = [...a].sort((p, q) => p - q);
    assert.deepEqual(insertionSort([...a]), want);
  }
});
