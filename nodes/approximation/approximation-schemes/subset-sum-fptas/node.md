---
tag: MWFG11
kind: algorithm
slug: subset-sum-fptas
name: Subset sum FPTAS
aliases:
- subset sum approximation scheme
- APPROX-SUBSET-SUM
- approximate subset sum by trimming
area: approximation/approximation-schemes
level: core
summary: Build the sorted list of reachable subset sums item by item, and trim each list so that no two kept sums are within a factor 1 + ε/2n. The result is at least OPT/(1 + ε).
solves: [subset-sum-problem]
model: word-ram
complexity:
  vars: {n: the number of items, t: the target, ε: "the accuracy parameter, 0 < ε ≤ 1"}
  time: {worst: O(n^2 log(t) / ε)}
  space: {extra: O(n^2 log(t) / ε)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1975
  people: [Oscar H. Ibarra, Chul E. Kim]
  note: Ibarra and Kim gave the first FPTAS for subset sum and knapsack in 1975. The trimmed list form on this page is the one in Cormen, Leiserson, Rivest and Stein.
prereqs: [subset-sum-problem, approximation-ratio, trimming-technique]
see_also: [fptas, knapsack-fptas, rounding-and-scaling, profit-indexed-dynamic-programming, knapsack-dynamic-programming, partition-problem, pseudo-polynomial-time, approximate-pareto-set]
sources:
  - book: isbn:9780262033848
    title: Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest and Clifford Stein, Introduction to Algorithms, third edition, MIT Press, 2009
    locator: Section 35.5 (The subset-sum problem), Theorem 35.8
  - paper: doi:10.1145/321906.321909
    title: Oscar H. Ibarra and Chul E. Kim, Fast approximation algorithms for the knapsack and sum of subset problems, Journal of the ACM 22(4), 1975
    locator: pages 463 to 468
  - book: isbn:9783540402862
    title: Hans Kellerer, Ulrich Pferschy and David Pisinger, Knapsack Problems, Springer, 2004
    locator: the chapter on the subset sum problem (approximation schemes)
  - title: Hans Kellerer, Renata Mansini, Ulrich Pferschy and Maria Grazia Speranza, An efficient fully polynomial approximation scheme for the Subset-Sum Problem, Journal of Computer and System Sciences 66(2), 2003
    locator: the main theorem (time O(min(n/ε, n + (1/ε^2) log(1/ε))) and space O(n + 1/ε))
---

The subset sum FPTAS is a [fully polynomial-time approximation scheme](/fptas/) for the optimization form of the [subset sum problem](/subset-sum-problem/): given positive integers $x_1, \ldots, x_n$ and a target $t$, find a subset whose sum is as large as possible but at most $t$. The exact method keeps the sorted list of all reachable sums, which can have $2^n$ entries. This algorithm adds the items one at a time and, after each item, [trims](/trimming-technique/) the list: a sum is dropped when a kept sum is smaller by at most a factor $1 + \varepsilon / (2n)$. The lists stay short, of length $O(n \log t / \varepsilon)$, and the result is at least $\mathrm{OPT} / (1 + \varepsilon)$.

## In plain words

To find the best subset sum exactly, you can write down every sum that some subset reaches. Each new number doubles the list in the worst case, so the list soon becomes much too long.

The fix is to keep only sums that are clearly different. If two sums in the list are very close, for example 100 and 101, keep only the smaller one, and let it stand for both. Later sums built on 101 are then built on 100 instead, and they lose only a little. The algorithm keeps a sum only when it is larger than the last kept sum by a small fixed factor. After $n$ steps the small losses multiply, but by the choice of the factor their product stays below $1 + \varepsilon$. The kept sums grow by a fixed factor each time, so few of them fit below $t$.

## The problem

The input is $n$ positive integers $x_1, \ldots, x_n$, an integer target $t \ge 0$ and an accuracy parameter $0 < \varepsilon \le 1$. Let

$$
\mathrm{OPT} = \max \Big\{ \sum_{i \in S} x_i : S \subseteq \{1, \ldots, n\},\ \sum_{i \in S} x_i \le t \Big\}.
$$

The task is a subset $S$ with sum $z$ such that $z \le t$ and $z \ge \mathrm{OPT} / (1 + \varepsilon)$. This is a maximization problem, so in the convention of [the approximation ratio](/approximation-ratio/) the guarantee is $\mathrm{ALG} \ge \alpha \cdot \mathrm{OPT}$ with $\alpha = 1 / (1 + \varepsilon) \ge 1 - \varepsilon$. The decision form (is there a subset with sum exactly $t$?) is NP-complete, so no algorithm decides it in polynomial time unless P = NP. The optimization form, as above, can be approximated to any accuracy.

## The algorithm

The algorithm is APPROX-SUBSET-SUM of Cormen et al., Section 35.5. For a list $L$ and a number $x$, $L + x$ is the list that adds $x$ to each entry. MERGE-LISTS merges two sorted lists into one sorted list and drops the repeated values.

```pseudo id=main
APPROX-SUBSET-SUM(x[1 .. n], t, ε)                     ▷ 0 < ε ≤ 1
L1  δ ← ε / (2n)
L2  L_0 ← ⟨0⟩
L3  for i ← 1 to n do
L4      L_i ← MERGE-LISTS(L_{i−1}, L_{i−1} + x_i)
L5      L_i ← TRIM(L_i, δ)
L6      remove from L_i every entry greater than t
L7  return z* ← the largest entry of L_n, with the subset that gives it

TRIM(⟨y_1 < y_2 < ... < y_m⟩, δ)
L8  L′ ← ⟨y_1⟩; last ← y_1
L9  for k ← 2 to m do
L10     if y_k > last · (1 + δ) then append y_k to L′; last ← y_k
L11 return L′
```

Without lines L5 and L6, the list $L_i$ is the set of all subset sums of the first $i$ numbers, and line L7 would give the exact answer after exponential work. Line L5 removes each sum that is within a factor $1 + \delta$ above the last kept sum, so the removed sum $y$ has a kept stand-in $z$ with $y / (1 + \delta) \le z \le y$. Line L6 removes the sums that are too large. To return the subset and not only its sum, each entry carries a pointer to the entry of $L_{i-1}$ that it came from, and a flag that says whether it adds $x_i$.

## Example

Take $x = \langle 29, 34, 36, 42, 46 \rangle$, $t = 82$ and $\varepsilon = 1$, so $\delta = 1/10$. A sum $y$ is kept only when $y > 1.1 \cdot \mathit{last}$.

| step $i$ | $x_i$ | merged list (line L4) | removed by TRIM | removed by line L6 | $L_i$ |
|---|---|---|---|---|---|
| 1 | 29 | 0, 29 | none | none | 0, 29 |
| 2 | 34 | 0, 29, 34, 63 | none | none | 0, 29, 34, 63 |
| 3 | 36 | 0, 29, 34, 36, 63, 65, 70, 99 | 36 (≤ 37.4), 65 (≤ 69.3) | 99 | 0, 29, 34, 63, 70 |
| 4 | 42 | 0, 29, 34, 42, 63, 70, 71, 76, 105, 112 | 71 and 76 (≤ 77), 112 (≤ 115.5) | 105 | 0, 29, 34, 42, 63, 70 |
| 5 | 46 | 0, 29, 34, 42, 46, 63, 70, 75, 80, 88, 109, 116 | 46 (≤ 46.2), 75 (≤ 77), 88 (≤ 88), 116 (≤ 119.9) | 109 | 0, 29, 34, 42, 63, 70, 80 |

The result is $z^* = 80 = 34 + 46$. The optimum is $82 = 36 + 46$. In step 3, the sum 36 was removed because 34 is within the factor 1.1 below it, so in step 5 the sum $34 + 46 = 80$ stands in for $36 + 46 = 82$. The ratio is $80 / 82 \approx 0.976$, well above the guarantee $1 / (1 + \varepsilon) = 1/2$.

Cormen et al. use $x = \langle 104, 102, 201, 101 \rangle$, $t = 308$ and $\varepsilon = 0.4$. There $L_4 = \langle 0, 101, 201, 302 \rangle$, the result is $302 = 201 + 101$, and the optimum is $307 = 104 + 102 + 101$.

## Correctness

The proof has three parts. Each entry of each list is a real subset sum of at most $t$, because the lists are built from $\langle 0 \rangle$ by adding numbers and removing entries. The main invariant is that for each subset sum $y \le t$ of the first $i$ numbers, the list $L_i$ holds a $z$ with

$$
\frac{y}{(1 + \delta)^i} \le z \le y.
$$

It holds by induction: the stand-in of $y - x_i$ in $L_{i-1}$, plus $x_i$, is in the merged list, and TRIM loses at most one more factor $1 + \delta$. With $y = \mathrm{OPT}$ and $i = n$, the result is at least $\mathrm{OPT} / (1 + \varepsilon / (2n))^n$, and $(1 + \varepsilon / (2n))^n \le e^{\varepsilon / 2} \le 1 + \varepsilon$ for $\varepsilon \le 1$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **List length.** The positive entries of a trimmed list grow by more than the factor $1 + \delta$ from each entry to the next, the smallest is at least 1, and the largest is at most $t$. So $|L_i| \le \log_{1 + \delta} t + 2 \le 3 n \ln t / \varepsilon + 2$.
- **Time.** Lines L4 to L6 make one pass over lists of this length, so each step takes $O(n \log t / \varepsilon)$ time, and the $n$ steps take $O(n^2 \log t / \varepsilon)$ time in the worst case, on the [word RAM](/word-ram/).
- **Space.** The current list takes $O(n \log t / \varepsilon)$ space. The pointers that recover the subset take $O(n^2 \log t / \varepsilon)$ space in the worst case, or less if the pointers that no list uses are freed.

The input has $\Omega(n + \log t)$ bits, so the time is polynomial in the input size and in $1 / \varepsilon$. The exact dynamic program over all sums $0, \ldots, t$ takes $\Theta(nt)$ time, which is only [pseudo-polynomial](/pseudo-polynomial-time/).

## Properties

- **Deterministic.** The output depends only on the input.
- **Always feasible.** Each returned sum is a true subset sum of at most $t$. Only the list of candidates is thinned, never the numbers.
- **Exact for a tiny ε.** For $\varepsilon < 1 / t$, the bound gives $z^* \ge \mathrm{OPT} / (1 + \varepsilon) > \mathrm{OPT} - 1$, so $z^* = \mathrm{OPT}$, in time polynomial in $n$ and $t$. This is consistent with subset sum being only [weakly NP-hard](/weak-np-hardness/).
- **Trimming beats rounding here.** The numbers are not rounded, so no loss comes from the size of the numbers, only from the merging of close sums.

## Variants and improvements

- **Scaling in place of trimming.** Ibarra and Kim (1975) got their scheme for subset sum as the special case $p_i = w_i$ of the [knapsack FPTAS](/knapsack-fptas/), with the profits scaled and rounded. Trimming and scaling give the same kind of bound; trimming works on the sums, and scaling works on the numbers.
- **Faster schemes.** Kellerer, Mansini, Pferschy and Speranza (2003) gave a scheme in $O(\min(n / \varepsilon, n + (1/\varepsilon^2) \log(1/\varepsilon)))$ time and $O(n + 1/\varepsilon)$ space. Later work reached time near $n + 1/\varepsilon^2$ with conditional lower bounds of the same order; see the knapsack literature for the exact statements.
- **A smaller δ for better constants.** With $\delta = \ln(1 + \varepsilon) / n$, the factor is exactly $(1 + \delta)^n \le e^{\ln(1 + \varepsilon)} = 1 + \varepsilon$, and the lists are about half as long. The choice $\delta = \varepsilon / (2n)$ is the simple one.
- **Knapsack by trimming.** The same method works for the [0/1 knapsack problem](/knapsack-problem/), with lists of (weight, profit) pairs. A pair is removed when a pair with at most the same weight has a profit within a factor $1 + \delta$. See the [trimming technique](/trimming-technique/).
- **Partition.** For the [partition problem](/partition-problem/), run the scheme with $t = \lfloor \sum_i x_i / 2 \rfloor$.

## When to use it

Use the scheme when the numbers are large, so that the exact table with $t + 1$ columns is too big, and a sum close to the best is enough. If $nt$ is small, the exact dynamic program is simpler and gives the optimum. If an exact answer is needed and $n$ is at most about 40, the meet-in-the-middle method in $O(2^{n/2} n)$ time is often better.

## Pitfalls

- **Trimming against the wrong entry.** Line L10 compares $y_k$ with the last kept entry, not with the entry just before it in the input list. With the entry just before, a chain of small steps can remove a long run of sums and lose much more than one factor $1 + \delta$.
- **Removing large sums before trimming.** Lines L5 and L6 can be swapped, but line L6 must not be dropped. Without it, sums above $t$ stay in the list and can be returned.
- **δ = ε in place of ε/2n.** The loss of each step multiplies over the $n$ steps. With $\delta = \varepsilon$, the bound is only $(1 + \varepsilon)^n$.
- **Floating point factors.** With a floating point $1 + \delta$, the test of line L10 can go the wrong way near equality. With $\varepsilon = a / b$ rational, the integer test $2nb \cdot y_k > (2nb + a) \cdot \mathit{last}$ is exact.
- **Losing the subset.** The lists hold sums only. To return the subset, store a pointer to the parent entry; the merge and the trim keep the pointer with the entry.

## Implementations

## History

Ibarra and Kim published the first fully polynomial-time approximation scheme for the knapsack problem and for subset sum, which they called the sum of subset problem, in the Journal of the ACM in 1975. The trimmed list form with $\delta = \varepsilon / (2n)$, called APPROX-SUBSET-SUM, is the form in Cormen, Leiserson, Rivest and Stein (Section 35.5, Theorem 35.8). Kellerer, Mansini, Pferschy and Speranza (2003) gave a scheme with time near linear in $n$ and space $O(n + 1/\varepsilon)$.

## References
