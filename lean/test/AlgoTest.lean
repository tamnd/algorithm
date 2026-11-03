/-
Copyright (c) 2026 The Algorithm encyclopedia authors. Released under Apache 2.0 license.
-/
module

public import Algo

/-!
# Tests

Each test runs a model on a small input and checks the value and the count of ticks. A test that fails stops the build.
-/

open Algo.Sorting.MergeSort

-- The model sorts the example of the node page.
example : (mergeSort [5, 2, 4, 6, 1, 3]).ret = [1, 2, 3, 4, 5, 6] := by decide +kernel

-- The output is a sort of the input.
example : Algo.Sorting.SortingProblem.IsSort [3, 1, 2] (mergeSort [3, 1, 2]).ret := by decide +kernel

-- Merge of [1, 3] and [2, 4] makes three comparisons.
example : (merge [1, 3] [2, 4]).time = 3 := by decide +kernel

-- A list that is sorted already costs fewer comparisons than the bound.
example : (mergeSort [1, 2, 3, 4]).time ≤ 4 * Nat.clog 2 4 := by decide +kernel
