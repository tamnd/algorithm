/-
Copyright (c) 2026 The Algorithm encyclopedia authors. Released under Apache 2.0 license.
-/
module

public import Mathlib.Data.List.Perm.Basic
public import Mathlib.Data.List.Sort

/-!
# The sorting problem

The spec of the node `sorting-problem`. Each sorting algorithm imports it.
-/

@[expose] public section

namespace Algo.Sorting.SortingProblem

/-- `out` is a sorted rearrangement of `xs`. This is the definition of the sorting problem page: the output has the same elements as the input, with the same multiplicities, in non-decreasing order. -/
def IsSort {α : Type} [LinearOrder α] (xs out : List α) : Prop :=
  out.Pairwise (· ≤ ·) ∧ out.Perm xs

instance {α : Type} [LinearOrder α] (xs out : List α) : Decidable (IsSort xs out) :=
  inferInstanceAs (Decidable (_ ∧ _))

end Algo.Sorting.SortingProblem
