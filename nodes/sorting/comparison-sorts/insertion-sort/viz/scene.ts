// SPDX-License-Identifier: MIT
// Part of https://algorithm.tamnd.com/insertion-sort/. The authors are listed in prov/3NS7RT.jsonl.
import { scene } from "@algo/viz";

interface Input {
  a: number[];
}

export default scene({
  slug: "insertion-sort",
  input: { type: "list<int>", length: [1, 16], values: [1, 99] },
  run(v, input: Input) {
    const a = v.array("A", input.a, { view: "bars", label: "A" });
    const n = a.length;
    if (n > 0) a.mark(0, "invariant");
    for (let i = 1; i < n; i++) {
      v.line("L1", `The part A[0..${i - 1}] is sorted. Insert A[${i}] into it.`);
      v.vars({ i });
      const key = a.peek(i) as number;
      v.line("L2", `Keep the key ${key}.`);
      v.vars({ key });
      a.mark(i, "active");
      a.label(`key = ${key}`);
      let j = i - 1;
      v.line("L3");
      v.vars({ j });
      a.ptr("j", j);
      for (;;) {
        v.line("L4");
        if (j < 0) {
          v.note("j is -1, so the key goes to the start.");
          break;
        }
        const c = a.compareWith(j, key);
        if (c <= 0) {
          v.note(`A[${j}] = ${a.peek(j)} is not larger than ${key}, so the inner loop stops.`);
          break;
        }
        v.note(`A[${j}] = ${a.peek(j)} is larger than ${key}.`);
        v.line("L5", `Move ${a.peek(j)} one place to the right.`);
        a.set(j + 1, a.peek(j), { from: ["A", j] });
        a.mark(j + 1, "invariant");
        a.mark(j, "active");
        j--;
        v.line("L6");
        v.vars({ j });
        a.ptr("j", j >= 0 ? j : null);
      }
      v.line("L7", `Put the key ${key} at index ${j + 1}.`);
      a.set(j + 1, key);
      a.mark([0, i], "invariant");
      a.ptr("j", null);
      a.label("");
    }
    v.line("L1", `i = ${n}, which is not less than n, so the loop ends and A is sorted.`);
    v.vars({ i: n });
    a.mark([0, n - 1], "path");
    return a.values();
  },
});
