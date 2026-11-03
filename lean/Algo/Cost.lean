/-
Copyright (c) 2026 The Algorithm encyclopedia authors. Released under Apache 2.0 license.
-/
module

public import Cslib.Algorithms.Lean.TimeM

/-!
# The cost model

This module gives the cost conventions of the Algo package (spec 07.4). A model is a function into `TimeM`, which returns a value and a count of ticks. One tick is one unit of the model of the node: one comparison of two keys in the comparison model, one probe for binary search on the word RAM.

`TimeM` comes from CSLib. If CSLib changes it, this module changes and the algorithm modules stay the same.
-/

@[expose] public section

namespace Algo.Cost

/-- A computation that returns a value of type `α` and counts its ticks in `ℕ`. -/
abbrev TimeM (α : Type) : Type := Cslib.Algorithms.Lean.TimeM ℕ α

/-- One tick. Each call in a model has a comment with the pseudocode line that it counts. -/
def tick : TimeM PUnit := Cslib.Algorithms.Lean.TimeM.tick 1

@[simp] theorem ret_tick : tick.ret = () := rfl

@[simp] theorem time_tick : tick.time = 1 := rfl

/-- `f` runs in at most `g (size x)` ticks on each input `x`. -/
def TimeBound {α β : Type} (f : α → TimeM β) (size : α → ℕ) (g : ℕ → ℕ) : Prop :=
  ∀ x, (f x).time ≤ g (size x)

/-- For each size `n`, some input of size `n` needs at least `g n` ticks. -/
def TimeLowerBound {α β : Type} (f : α → TimeM β) (size : α → ℕ) (g : ℕ → ℕ) : Prop :=
  ∀ n, ∃ x, size x = n ∧ g n ≤ (f x).time

end Algo.Cost
