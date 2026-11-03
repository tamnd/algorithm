/-
Copyright (c) 2026 The Algorithm encyclopedia authors. Released under Apache 2.0 license.
-/
module

public import Algo.Cost
public import Algo.Sorting.SortingProblem
public import Cslib.Algorithms.Lean.MergeSort.MergeSort
import all Cslib.Algorithms.Lean.MergeSort.MergeSort
public import Mathlib.Analysis.Asymptotics.Defs
public import Mathlib.Analysis.SpecialFunctions.Log.Basic
public import Mathlib.Analysis.SpecialFunctions.Pow.Real

/-!
# Merge sort

The Lean part of the node `merge-sort`. The model follows the `main` pseudocode of the node page. The page works on an array and a half-open range. The model works on a list, which is the usual form in Lean. A tick counts one comparison of two keys, at line L9.

The cost bound reuses the recurrence of CSLib, because the two models split a list of length `n` into the same two sizes.
-/

@[expose] public section

namespace Algo.Sorting.MergeSort

open Algo.Cost Algo.Sorting.SortingProblem

variable {α : Type} [LinearOrder α]

/-- Merge two lists. One tick for each comparison of two keys (pseudocode L9). -/
def merge : List α → List α → TimeM (List α)
  | [], ys => pure ys
  | xs, [] => pure xs
  | x :: xs, y :: ys => do
      tick                                    -- L9
      if x ≤ y then
        let r ← merge xs (y :: ys)
        pure (x :: r)                         -- L9, take from the left half
      else
        let r ← merge (x :: xs) ys
        pure (y :: r)                         -- L10, take from the right half
termination_by xs ys => xs.length + ys.length

/-- Merge sort (pseudocode L1 to L5). -/
def mergeSort (xs : List α) : TimeM (List α) :=
  if xs.length < 2 then pure xs               -- L1
  else do
    let half := xs.length / 2                 -- L2
    let l ← mergeSort (xs.take half)          -- L3
    let r ← mergeSort (xs.drop half)          -- L4
    merge l r                                 -- L5
termination_by xs.length
decreasing_by all_goals simp only [List.length_take, List.length_drop]; omega

open Cslib.Algorithms.Lean.TimeM (ret_bind time_bind ret_pure time_pure)

@[simp] theorem merge_nil_left (ys : List α) : merge [] ys = pure ys := by
  rw [merge]

@[simp] theorem merge_nil_right (xs : List α) : merge xs [] = pure xs := by
  cases xs with
  | nil => rw [merge]
  | cons x xs => rw [merge]; simp

theorem merge_cons_cons (x y : α) (xs ys : List α) :
    merge (x :: xs) (y :: ys) = (do
      tick
      if x ≤ y then
        let r ← merge xs (y :: ys)
        pure (x :: r)
      else
        let r ← merge (x :: xs) ys
        pure (y :: r)) := by
  rw [merge]

/-- The model of merge computes `List.merge` with the order `≤`. -/
theorem ret_merge (xs ys : List α) :
    (merge xs ys).ret = xs.merge ys (fun a b => decide (a ≤ b)) := by
  induction xs generalizing ys with
  | nil => simp
  | cons x xs ihx =>
    induction ys with
    | nil => simp
    | cons y ys ihy =>
      rw [merge_cons_cons, List.cons_merge_cons]
      by_cases h : x ≤ y
      · simp [h, ihx]
      · simp [h, ihy]

theorem length_merge (xs ys : List α) :
    (merge xs ys).ret.length = xs.length + ys.length := by
  simp [ret_merge]

/-- Merge makes at most one comparison for each item that it outputs. -/
theorem merge_time_le (xs ys : List α) : (merge xs ys).time ≤ xs.length + ys.length := by
  induction xs generalizing ys with
  | nil => simp
  | cons x xs ihx =>
    induction ys with
    | nil => simp
    | cons y ys ihy =>
      rw [merge_cons_cons]
      by_cases h : x ≤ y
      · have := ihx (y :: ys)
        simp only [h, ↓reduceIte, time_bind, time_tick, time_pure, List.length_cons] at this ⊢
        omega
      · simp only [h, ↓reduceIte, time_bind, time_tick, time_pure, List.length_cons] at ihy ⊢
        omega

theorem merge_perm (xs ys : List α) : (merge xs ys).ret.Perm (xs ++ ys) := by
  rw [ret_merge]
  exact List.merge_perm_append _

theorem merge_sorted {xs ys : List α} (hx : xs.Pairwise (· ≤ ·)) (hy : ys.Pairwise (· ≤ ·)) :
    (merge xs ys).ret.Pairwise (· ≤ ·) := by
  rw [ret_merge]
  have h := List.pairwise_merge (le := fun a b => decide (a ≤ b))
    (fun a b c hab hbc => by simp only [decide_eq_true_eq] at *; exact le_trans hab hbc)
    (fun a b => by simpa using le_total a b)
    xs ys (by simpa using hx) (by simpa using hy)
  simpa using h

theorem mergeSort_of_lt {xs : List α} (h : xs.length < 2) : mergeSort xs = pure xs := by
  rw [mergeSort, ite_eq_left_of_eq_true _ _ (eq_true h)]

theorem mergeSort_of_ge {xs : List α} (h : ¬xs.length < 2) :
    mergeSort xs = (do
      let l ← mergeSort (xs.take (xs.length / 2))
      let r ← mergeSort (xs.drop (xs.length / 2))
      merge l r) := by
  rw [mergeSort, ite_eq_right_of_eq_false _ _ (eq_false h)]

/-- Merge sort sorts: its output is a sorted rearrangement of its input. -/
theorem mergeSort_isSort (xs : List α) : IsSort xs (mergeSort xs).ret := by
  induction hn : xs.length using Nat.strong_induction_on generalizing xs with
  | _ n ih =>
    by_cases h : xs.length < 2
    · rw [mergeSort_of_lt h]
      refine ⟨?_, List.Perm.refl _⟩
      match xs, h with
      | [], _ => simp
      | [_], _ => simp
    · rw [mergeSort_of_ge h]
      simp only [ret_bind]
      have hl := ih _ (by simp; omega) (xs.take (xs.length / 2)) rfl
      have hr := ih _ (by simp; omega) (xs.drop (xs.length / 2)) rfl
      refine ⟨merge_sorted hl.1 hr.1, ?_⟩
      refine (merge_perm _ _).trans ?_
      rw [← List.take_append_drop (xs.length / 2) xs]
      simpa using hl.2.append hr.2

theorem length_mergeSort (xs : List α) : (mergeSort xs).ret.length = xs.length :=
  (mergeSort_isSort xs).2.length_eq

/-- The number of comparisons is at most the CSLib recurrence `timeMergeSortRec` for the length. -/
theorem mergeSort_time_le_rec (xs : List α) :
    (mergeSort xs).time ≤ Cslib.Algorithms.Lean.TimeM.timeMergeSortRec xs.length := by
  induction hn : xs.length using Nat.strong_induction_on generalizing xs with
  | _ n ih =>
    by_cases h : xs.length < 2
    · rw [mergeSort_of_lt h]
      simp
    · rw [mergeSort_of_ge h]
      simp only [time_bind]
      have lt : (xs.take (xs.length / 2)).length = xs.length / 2 := by simp; omega
      have ld : (xs.drop (xs.length / 2)).length = (xs.length - 1) / 2 + 1 := by simp; omega
      have hl := ih _ (by rw [lt]; omega) (xs.take (xs.length / 2)) rfl
      have hr := ih _ (by rw [ld]; omega) (xs.drop (xs.length / 2)) rfl
      have hm := merge_time_le (mergeSort (xs.take (xs.length / 2))).ret
        (mergeSort (xs.drop (xs.length / 2))).ret
      rw [length_mergeSort, length_mergeSort, lt, ld] at hm
      rw [lt] at hl
      rw [ld] at hr
      obtain ⟨k, hk⟩ : ∃ k, xs.length = k + 2 := ⟨xs.length - 2, by omega⟩
      rw [hk] at hl hr hm ⊢
      have e : Cslib.Algorithms.Lean.TimeM.timeMergeSortRec (k + 2) =
          Cslib.Algorithms.Lean.TimeM.timeMergeSortRec ((k + 2) / 2) +
            Cslib.Algorithms.Lean.TimeM.timeMergeSortRec ((k + 2 - 1) / 2 + 1) + (k + 2) := by
        rw [Cslib.Algorithms.Lean.TimeM.timeMergeSortRec]
      rw [← hn, hk, e]
      omega

/-- Merge sort makes at most `n ⌈lg n⌉` comparisons on a list of length `n`. This is the upper side of the worst case Θ(n log n) of the node page. -/
theorem mergeSort_time_le (xs : List α) :
    (mergeSort xs).time ≤ xs.length * Nat.clog 2 xs.length :=
  (mergeSort_time_le_rec xs).trans (Cslib.Algorithms.Lean.TimeM.timeMergeSortRec_le _)

/-- For `n ≥ 2`, `⌈lg n⌉ ≤ (2 / ln 2) ln n`. -/
theorem clog_le_log (n : ℕ) (hn : 2 ≤ n) :
    (Nat.clog 2 n : ℝ) ≤ 2 / Real.log 2 * Real.log n := by
  have h1 : 2 ^ (Nat.clog 2 n).pred < n := Nat.pow_pred_clog_lt_self (by norm_num) (by omega)
  have hpos : 0 < Nat.clog 2 n := Nat.clog_pos (by norm_num) (by omega)
  have h2 : ((Nat.clog 2 n).pred : ℝ) * Real.log 2 < Real.log n := by
    rw [← Real.log_pow]
    apply Real.log_lt_log (by positivity)
    exact_mod_cast h1
  have h3 : Real.log 2 ≤ Real.log n := Real.log_le_log (by norm_num) (by exact_mod_cast hn)
  have hl : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hc : ((Nat.clog 2 n).pred : ℝ) = Nat.clog 2 n - 1 := by
    rw [Nat.pred_eq_sub_one, Nat.cast_sub hpos]
    simp
  rw [hc] at h2
  rw [div_mul_eq_mul_div, le_div_iff₀ hl]
  nlinarith

/-- The class lemma that links the bound `n ⌈lg n⌉` to the class `O(n log n)` of the front matter. -/
theorem mergeSort_bound_isBigO :
    (fun n : ℕ => (n * Nat.clog 2 n : ℝ)) =O[Filter.atTop] (fun n : ℕ => (n : ℝ) * Real.log n) := by
  refine Asymptotics.IsBigO.of_bound (2 / Real.log 2) ?_
  filter_upwards [Filter.eventually_ge_atTop 2] with n hn
  have hlog : 0 ≤ Real.log n := Real.log_nonneg (by exact_mod_cast (by omega : 1 ≤ n))
  rw [Real.norm_of_nonneg (by positivity), Real.norm_of_nonneg (by positivity)]
  calc (n : ℝ) * Nat.clog 2 n ≤ n * (2 / Real.log 2 * Real.log n) := by
        gcongr
        exact clog_le_log n hn
    _ = 2 / Real.log 2 * (n * Real.log n) := by ring

end Algo.Sorting.MergeSort
