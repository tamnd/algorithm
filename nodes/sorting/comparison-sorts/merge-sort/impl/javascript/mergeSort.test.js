// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.

import { test } from "node:test";
import assert from "node:assert/strict";
import { mergeSort } from "./mergeSort.js";

test("example", () => {
  assert.deepEqual(mergeSort([38, 27, 43, 3, 9, 82, 10]), [3, 9, 10, 27, 38, 43, 82]);
});

test("edges", () => {
  assert.deepEqual(mergeSort([]), []);
  assert.deepEqual(mergeSort([1]), [1]);
  assert.deepEqual(mergeSort([3, 2, 1, 1]), [1, 1, 2, 3]);
  assert.deepEqual(mergeSort(["pear", "fig", "apple"]), ["apple", "fig", "pear"]);
});

test("random against Array.prototype.sort", () => {
  let s = 2150;
  const next = (m) => {
    s = (Math.imul(s, 1103515245) + 12345) >>> 0;
    return (s >>> 8) % m;
  };
  for (let t = 0; t < 500; t++) {
    const a = Array.from({ length: next(61) }, () => next(101) - 50);
    const want = [...a].sort((p, q) => p - q);
    assert.deepEqual(mergeSort([...a]), want);
  }
});
