---
tag: V2066X
kind: algorithm
slug: three-sum-two-pointer-scan
name: 3SUM by sorting and two-pointer scan
aliases:
- 3SUM O(n^2) algorithm
area: techniques/two-pointers-and-windows
level: core
summary: Sort, fix one element, and run a two-pointer scan on the rest, giving O(n^2) time.
solves: [3sum]
model: word-ram
complexity:
  vars: {n: the number of input values}
  time: {worst: Θ(n^2), average: Θ(n^2)}
  space: {extra: Θ(1)}
properties: {stable: false, in_place: true, adaptive: false, online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [two-pointer-pair-search, two-sum-sorted, loop-invariant]
see_also: [3sum, 3sum-conjecture, 3sum-hardness, k-sum, two-pointers, linear-decision-tree, hash-table]
sources:
  - paper: doi:10.1016/0925-7721(95)00022-2
    title: Anka Gajentaan and Mark H. Overmars, On a class of O(n^2) problems in computational geometry, Computational Geometry 5(3), 1995
    locator: pp. 165 to 185 (the 3SUM problem and 3SUM-hard problems)
  - url: https://jeffe.cs.illinois.edu/pubs/linsat.html
    title: Jeff Erickson, Lower bounds for linear satisfiability problems, Chicago Journal of Theoretical Computer Science 1999, article 8
    locator: the Ω(n^⌈r/2⌉) bound in the r-linear decision tree model; Ω(n^2) for 3SUM
  - paper: doi:10.1145/3185378
    title: Allan Grønlund and Seth Pettie, Threesomes, degenerates, and love triangles, Journal of the ACM 65(4), 2018
    locator: Article 22 (subquadratic algorithms for 3SUM; conference version FOCS 2014)
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition
    locator: Chapter 4, Sorting (applications of sorting)
---

This algorithm solves [3SUM](/3sum/): it finds the triples of values, taken from three different positions of an array, whose sum is a target $t$ (usually 0). It sorts the array, fixes the smallest value of the triple, and runs a [two-pointer pair search](/two-pointer-pair-search/) on the values to its right. It takes $\Theta(n^2)$ time and $O(1)$ extra space besides the sort, and with a skip over equal values it lists each distinct value triple once. Its quadratic bound is the reference point of [3SUM-hardness](/3sum-hardness/).

## In plain words

Put the numbers in order. Take the first number as the smallest member of the triple. Now you need two numbers to its right whose sum is the target minus that first number. That is the two sum problem on a sorted list, and two pointers solve it in one sweep: one pointer starts just right of the fixed number, one starts at the end, and the one that makes the sum wrong moves inward.

Then fix the next number and sweep again, and so on. If the next number is equal to the one you just fixed, skip it: it would only find the same triples again. Inside a sweep, after a hit, also move past copies of the two numbers you found. Then each triple of values comes out once.

## The problem

The input is a list of $n$ integers $v_0, \ldots, v_{n-1}$ and a target $t$. A *solution* is a value triple $(x, y, z)$ with $x \le y \le z$ and $x + y + z = t$ such that $x$, $y$ and $z$ are the values at three different positions of the list. The output is the set of all solutions, each one once. The decision version, which asks only if a solution exists, is the [3SUM](/3sum/) problem.

## The algorithm

```pseudo id=main
THREE-SUM(v, t)
L1  A ← v sorted in non-decreasing order, n ← |A|
L2  for i ← 0 to n − 3 do
L3      if i > 0 and A[i] = A[i − 1] then continue     ▷ same x as before
L4      lo ← i + 1, hi ← n − 1
L5      while lo < hi do
L6          s ← A[i] + A[lo] + A[hi]
L7          if s < t then lo ← lo + 1
L8          else if s > t then hi ← hi − 1
L9          else report (A[i], A[lo], A[hi])
L10              lo ← lo + 1; while lo < hi and A[lo] = A[lo − 1] do lo ← lo + 1
L11              hi ← hi − 1; while lo < hi and A[hi] = A[hi + 1] do hi ← hi − 1
L12 return the reported triples
```

Lines L4 to L11 are the [two-pointer pair search](/two-pointer-pair-search/) for the target $t - A[i]$ on $A[i+1 \ldots n-1]$, changed in one way: after a hit it does not stop. It moves $lo$ past all copies of the value it found, and $hi$ past all copies of its value, and goes on. Line L3 runs the sweep only for the first position of each value of $x$.

## Example

Run THREE-SUM on $v = [-1, 0, 1, 2, -1, -4]$ with $t = 0$. Line L1 gives $A = [-4, -1, -1, 0, 1, 2]$.

| $i$ | $A[i]$ | $lo$ | $hi$ | $A[lo]$ | $A[hi]$ | $s$ | action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | $-4$ | 1 | 5 | $-1$ | 2 | $-3$ | $lo \leftarrow 2$ |
| 0 | $-4$ | 2 | 5 | $-1$ | 2 | $-3$ | $lo \leftarrow 3$ |
| 0 | $-4$ | 3 | 5 | 0 | 2 | $-2$ | $lo \leftarrow 4$ |
| 0 | $-4$ | 4 | 5 | 1 | 2 | $-1$ | $lo \leftarrow 5$, sweep ends |
| 1 | $-1$ | 2 | 5 | $-1$ | 2 | 0 | report $(-1, -1, 2)$; $lo \leftarrow 3$, $hi \leftarrow 4$ |
| 1 | $-1$ | 3 | 4 | 0 | 1 | 0 | report $(-1, 0, 1)$; $lo \leftarrow 4$, $hi \leftarrow 3$ |
| 2 | $-1$ | | | | | | line L3: same as $A[1]$, skip |
| 3 | 0 | 4 | 5 | 1 | 2 | 3 | $hi \leftarrow 4$, sweep ends |

The output is $(-1, -1, 2)$ and $(-1, 0, 1)$. Without line L3, the sweep for $i = 2$ would report $(-1, 0, 1)$ a second time.

## Correctness

The sweep for a fixed $i$ keeps this invariant at the test of line L5: (a) each solution with $x = A[i]$ that uses positions $p, q > i$ and is not yet reported has such positions with $lo \le p < q \le hi$; (b) each pair $(y, z)$ reported in this sweep has $y < A[lo]$ and $z > A[hi]$. Lines L7 and L8 keep (a) by the argument of the pair search: if $s < t$, the value $A[lo]$ is too small even with the largest partner $A[hi]$, so no solution in the range uses position $lo$; the case $s > t$ is the mirror. After a hit $(y_0, z_0)$, each other solution in the range has $y > y_0$ and $z < z_0$, so lines L10 and L11 skip only positions that hold $y_0$ or $z_0$, which no unreported solution needs. Part (b) shows that no pair is reported twice. Line L3 is safe because a solution that uses position $i$ and two positions to its right can use position $i - 1$ instead when $A[i-1] = A[i]$. The full proof is in the proof below.

## Complexity

- **Sort.** Line L1 takes $O(n \log n)$ time with a comparison sort.
- **One sweep.** Each iteration of the loop of line L5 decreases $hi - lo$ by at least 1, and the value starts at $n - 2 - i$. So the sweep for $i$ runs at most $n - 2 - i$ times.
- **All sweeps.** At most $\sum_{i=0}^{n-3} (n - 2 - i) = \frac{(n-1)(n-2)}{2}$ iterations in total, each $O(1)$. So the time is $O(n^2)$.
- **Matching lower bound for this algorithm.** If the values are distinct and no solution exists, no line L3 skips and no hit happens, so each sweep runs exactly $n - 2 - i$ times, and the total is exactly $\frac{(n-1)(n-2)}{2}$. With distinct values each iteration decreases $hi - lo$ by at most 2, so each sweep runs at least $\frac{n - 2 - i}{2}$ times, and the time is $\Theta(n^2)$ on every input of distinct values.
- **Space.** $O(1)$ extra words besides the sorted array and the output. If the caller allows the input to be sorted in place, no copy is needed.

The output has at most $O(n^2)$ triples: after $x$ and $y$ are fixed, $z = t - x - y$ is fixed.

## Properties

- **Exact output.** Each distinct value triple is reported once, and in lexicographic order: $x$ grows with $i$, and inside a sweep $y$ grows with $lo$.
- **Deterministic and comparison-based on sums.** The only tests are the signs of $A[i] + A[lo] + A[hi] - t$ and equality tests of two values. This is a 3-linear decision tree, the model of Erickson's lower bound below.
- **Not adaptive.** On distinct values the time is $\Theta(n^2)$ even if the first sweep finds a solution, unless the caller stops at the first hit.

## Variants and improvements

- **Decision version.** Return YES at the first hit. The worst case is still $\Theta(n^2)$ time.
- **Index triples.** To list index triples instead of value triples, drop lines L3, L10 and L11 and count blocks of equal values as in the counting variant of the [pair search](/two-pointer-pair-search/). The output can then have $\Theta(n^3)$ triples, for example when all values are 0.
- **Closest sum.** Record the triple with the smallest $|s - t|$ and move the pointers as in lines L7 and L8.
- **Hash table.** For each $i$, scan $j > i$ and look up $t - A[i] - A[j]$ in a [hash table](/hash-table/) of the values seen in this scan. This is $O(n^2)$ expected time and needs no sort, but $\Theta(n)$ extra space.
- **Three arrays.** For $a \in A$, $b \in B$, $c \in C$, sort $B$ and $C$, and for each $a$ run one pointer up $B$ and one down $C$. This is $O(|A| (|B| + |C|))$ time.
- **[k-sum](/k-sum/).** Fix the $k - 2$ smallest values by nested loops and run the pair search: $O(n^{k-1})$ time. Meet-in-the-middle gives $O(n^{\lceil k/2 \rceil} \log n)$.
- **Subquadratic algorithms.** Grønlund and Pettie (FOCS 2014, JACM 2018) gave the first algorithms for real-valued 3SUM that beat $n^2$ by a factor that grows with $n$: the deterministic one takes $O(n^2 / (\log n / \log \log n)^{2/3})$ time. They also showed that the decision tree complexity of 3SUM is $O(n^{3/2} \sqrt{\log n})$. Later work improved the logarithmic factors. No algorithm with time $O(n^{2 - \varepsilon})$ for a constant $\varepsilon > 0$ is known; the conjecture that none exists is the [3SUM conjecture](/3sum-conjecture/).

## When to use it

This is the standard practical algorithm for 3SUM. It needs no extra memory and no hashing, and its inner loop is a linear scan of a sorted array, which is fast in practice. Use the hash table variant only when the input must not be sorted. The subquadratic algorithms are of theoretical interest: their gain over this scan is a small power of $\log n$.

## Pitfalls

- **No skip at line L3.** Without line L3, the input $[-1, -1, 0, 1]$ gives $(-1, 0, 1)$ twice, once from each $-1$.
- **Skipping the wrong copy.** A test $A[i] = A[i+1]$ at line L3 skips the *first* copy of a value instead of the later ones. On $[-1, -1, 2]$ it skips $i = 0$, and the sweep for $i = 1$ has only one position to its right, so the solution $(-1, -1, 2)$ is lost. Compare with the copy on the left, $A[i - 1]$.
- **No skip after a hit.** Without the inner while loops of lines L10 and L11, the sweep for $x = -2$ on $[-2, 0, 0, 2, 2]$ reports $(-2, 0, 2)$ twice.
- **Stopping the sweep at the first hit.** A `break` after line L9 loses the other solutions with the same $x$. On $[-4, 0, 1, 3, 4]$ with $t = 0$, the sweep for $x = -4$ first finds $(-4, 0, 4)$, and a `break` loses $(-4, 1, 3)$.
- **The range of $i$.** The loop of line L2 stops at $n - 3$. A sweep for a larger $i$ has fewer than two positions to its right and does nothing, so this is a speed-up, not a correctness need. But in a language with unsigned sizes, $n - 3$ wraps around when $n < 3$.
- **Overflow.** The sum of three 64-bit values can overflow. Use a wider type, or compare $A[lo] + A[hi]$ with $t - A[i]$ when the ranges allow.

## Implementations

## History

Gajentaan and Overmars (1995) named the problem 3SUM and defined 3SUM-hard problems in computational geometry, problems to which 3SUM reduces with subquadratic overhead. They took the quadratic time of the sort-and-scan algorithm as the bound that these problems seemed unable to beat. Erickson (1999) proved an $\Omega(n^2)$ lower bound for 3SUM in the 3-linear decision tree model, the model in which this algorithm works. Grønlund and Pettie (2014) showed that the quadratic bound is not tight in more general models.

## References
