// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/merge-sort/. The authors are listed in prov/4MRG7S.jsonl.
import { scene, type Viz, type ArrayView } from "@algo/viz";

interface Input {
  a: number[];
}

function sort(v: Viz, a: ArrayView, lo: number, hi: number): void {
  v.line("L1", hi - lo <= 1 ? `The part [${lo}, ${hi}) has ${hi - lo} item, so it is sorted.` : `Sort the part [${lo}, ${hi}).`);
  v.vars({ lo, hi });
  if (hi - lo <= 1) return;
  const mid = lo + Math.floor((hi - lo) / 2);
  v.line("L2", `Split the part at index ${mid}.`);
  v.vars({ mid });
  a.bracket(lo, mid, hi - 1);
  v.line("L3", `Sort the left half [${lo}, ${mid}).`);
  sort(v, a, lo, mid);
  v.line("L4", `Sort the right half [${mid}, ${hi}).`);
  v.vars({ lo, mid, hi });
  a.bracket(lo, mid, hi - 1);
  sort(v, a, mid, hi);
  v.line("L5", `Merge the two sorted halves of [${lo}, ${hi}).`);
  v.vars({ lo, mid, hi });
  a.bracket(lo, mid, hi - 1);
  merge(v, a, lo, mid, hi);
}

function merge(v: Viz, a: ArrayView, lo: number, mid: number, hi: number): void {
  const items: number[] = [];
  for (let t = lo; t < mid; t++) items.push(a.peek(t) as number);
  v.line("L6", `Copy the left half ${JSON.stringify(items)} to the buffer B.`);
  const b = v.array("B", items, { view: "bars", label: "B" });
  let i = 0;
  let j = mid;
  let k = lo;
  v.line("L7");
  v.vars({ i, j, k });
  b.ptr("i", 0);
  a.ptr("j", j < hi ? j : null);
  a.ptr("k", k);
  for (;;) {
    v.line("L8");
    if (!(i < items.length && j < hi)) {
      v.note(i < items.length ? "The right half is empty." : "The buffer is empty.");
      break;
    }
    const c = a.compareWith(j, b.peek(i));
    b.mark(i, "compare");
    v.line("L9");
    if (c >= 0) {
      v.note(`B[${i}] = ${b.peek(i)} is not larger than A[${j}] = ${a.peek(j)}, so take it from the buffer.`);
      a.set(k, b.peek(i), { from: ["B", i] });
      b.mark(i, "visited");
      i++;
      b.ptr("i", i < items.length ? i : null);
    } else {
      v.line("L10", `A[${j}] = ${a.peek(j)} is smaller than B[${i}] = ${b.peek(i)}, so take it from the right half.`);
      b.unmark(i);
      a.set(k, a.peek(j), { from: ["A", j] });
      j++;
      a.ptr("j", j < hi ? j : null);
    }
    a.mark(k, "invariant");
    k++;
    v.line("L11");
    v.vars({ i, j, k });
    a.ptr("k", k < hi ? k : null);
  }
  for (;;) {
    v.line("L12");
    if (i >= items.length) break;
    v.line("L13", `Copy B[${i}] = ${b.peek(i)} to A[${k}].`);
    a.set(k, b.peek(i), { from: ["B", i] });
    b.mark(i, "visited");
    a.mark(k, "invariant");
    i++;
    k++;
    v.vars({ i, k });
  }
  a.unmark([lo, hi - 1]);
  a.ptr("j", null);
  a.ptr("k", null);
  v.destroy("B");
}

export default scene({
  slug: "merge-sort",
  input: { type: "list<int>", length: [1, 16], values: [1, 99] },
  run(v, input: Input) {
    const a = v.array("A", input.a, { view: "bars", label: "A" });
    v.phase("MERGE-SORT(A, 0, n)");
    sort(v, a, 0, a.length);
    a.bracket(null);
    a.mark([0, a.length - 1], "path");
    v.note("The array is sorted.");
    return a.values();
  },
});
