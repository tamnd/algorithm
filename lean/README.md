# The Lean package

This directory is the Lean package `Algo` (spec 07). It has the formal part of the nodes: the spec of each problem, the model of each algorithm, and the proofs of correctness and cost.

| Path | Content |
|---|---|
| `Algo/Cost.lean` | the cost model: `TimeM` from CSLib and one `tick` for each unit of the model |
| `Algo/Sorting/SortingProblem.lean` | `IsSort`, the spec of the sorting problem |
| `Algo/Sorting/MergeSort.lean` | the model of merge sort, its correctness, and its bound of `n ⌈lg n⌉` comparisons |
| `test/AlgoTest.lean` | small runs of the models, checked by the kernel |

The package uses Lean v4.35.0, Mathlib v4.35.0 and CSLib v4.35.0.

To build it:

```sh
cd lean
lake exe cache get
lake build
lake test
```

The front matter of a node names its module and its declarations in the `lean` field. A proof can use only the axioms `propext`, `Classical.choice` and `Quot.sound`. CI audits the axioms of each declaration in `Algo`.
