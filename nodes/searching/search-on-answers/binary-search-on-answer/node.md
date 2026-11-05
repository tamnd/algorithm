---
tag: 4PKE10
kind: technique
slug: binary-search-on-answer
name: Binary search on the answer
aliases:
- answer binary search
- binary search on the result
- bisection over the answer
area: searching/search-on-answers
level: intro
summary: Find the best feasible value by binary searching over candidate answers with a monotone feasibility test.
prereqs: [binary-search, monotone-predicate, optimization-to-decision-reduction]
see_also: [lower-and-upper-bound-search, binary-search-on-real-numbers, minimax-partition, maximin-placement, kth-smallest-pair-distance, parallel-binary-search, parametric-search, aliens-trick]
sources:
  - book: isbn:9783319725468
    title: Antti Laaksonen, Guide to Competitive Programming, first edition, Springer, 2017
    locator: Section 4.3.2, Finding Optimal Solutions
  - url: https://cp-algorithms.com/num_methods/binary_search.html
    title: cp-algorithms, Binary search
    note: the sections Search on arbitrary predicate and Binary search on the answer
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 34, the overview at the start of the chapter (decision problems versus optimization problems)
---

Binary search on the answer finds the optimal value of a problem by a [binary search](/binary-search/) over the candidate values, where each step runs a feasibility test "can the answer be $t$ or better?" instead of comparing with an array item. It is correct exactly when the test is a [monotone predicate](/monotone-predicate/) in $t$, and it costs $\lceil \lg(U - L + 1) \rceil$ tests for integer answers in $[L, U]$. It is the programming form of the [optimization-to-decision reduction](/optimization-to-decision-reduction/), and it turns many problems with a hard optimum but an easy greedy check into $O(n \log U)$ algorithms.

## In plain words

You must pick a number, such as the size of a truck or the speed of a worker, and you want the smallest number that works. You do not know a formula for it. But for any one number you can check quickly whether it works, for example by loading the truck and counting the trips.

If a number works, every larger number also works. So the numbers that fail come first and the numbers that work come after them. You look for the first number that works in the same way as you look for a word in a dictionary. Try the middle number. If it works, the answer is that number or a smaller one. If it fails, the answer is larger. Each check halves the range that is left.

## When it applies

- **An answer on an ordered scale.** The quantity to find is an integer, a real number, or an element of a sorted list of candidates, and lower and upper bounds $L \le \mathrm{OPT} \le U$ are known or easy to find.
- **A monotone test.** For a minimization, the test $\mathrm{FEASIBLE}(t)$, "is there a solution with cost at most $t$?", satisfies: $t \le t'$ and $\mathrm{FEASIBLE}(t)$ imply $\mathrm{FEASIBLE}(t')$. For a maximization, the test "is there a solution with value at least $t$?" is true for small $t$ and false for large $t$. Monotonicity usually comes from one of two facts: a solution for $t$ is also a solution for each looser $t'$, or the test compares a non-decreasing function of $t$ with a constant.
- **A test that is cheaper than the optimization.** The test is often a greedy pass, a graph search or a counting loop, in linear or near-linear time, while no direct method for the optimum is known or simple.
- **Typical words in the problem statement.** "Minimize the maximum", "maximize the minimum", "the smallest capacity, speed or time such that", "the k-th smallest value of a large implicit set".

## The template

The first form finds the smallest feasible value of a minimization. The range $[lo, hi]$ is closed, and $hi$ must be feasible.

```pseudo id=main
SMALLEST-FEASIBLE(lo, hi)                   ▷ FEASIBLE is monotone and FEASIBLE(hi) is true
L1  while lo < hi do
L2      mid ← lo + ⌊(hi − lo) / 2⌋            ▷ lo ≤ mid < hi
L3      if FEASIBLE(mid) then hi ← mid       ▷ the answer is mid or smaller
L4      else lo ← mid + 1                    ▷ the answer is larger than mid
L5  return lo

LARGEST-FEASIBLE(lo, hi)                    ▷ FEASIBLE is true then false and FEASIBLE(lo) is true
L6  while lo < hi do
L7      mid ← lo + ⌈(hi − lo) / 2⌉            ▷ lo < mid ≤ hi: round up here
L8      if FEASIBLE(mid) then lo ← mid       ▷ the answer is mid or larger
L9      else hi ← mid − 1                    ▷ the answer is smaller than mid
L10 return lo
```

The hole is FEASIBLE. The rest is the loop of [lower bound search](/lower-and-upper-bound-search/), which this page does not repeat.

**Correctness of SMALLEST-FEASIBLE.** Let $k$ be the smallest $t$ in the initial range with FEASIBLE$(t)$; it exists because FEASIBLE$(hi)$ is true. The invariant is $lo \le k \le hi$. It holds at the start. In line L3, FEASIBLE$(mid)$ true gives $k \le mid$, so $k \le$ the new $hi$. In line L4, FEASIBLE$(mid)$ false gives $mid < k$ by monotonicity (if $k \le mid$, then FEASIBLE$(mid)$ would be true), so the new $lo = mid + 1 \le k$. When the loop stops, $lo = hi$, so $lo = k$.

**Termination and cost.** Let $\ell = hi - lo \ge 1$. Line L3 makes the new length $\lfloor \ell/2 \rfloor$, and line L4 makes it $\ell - \lfloor \ell/2 \rfloor - 1 = \lceil \ell/2 \rceil - 1 \le \lfloor \ell/2 \rfloor$. So each step at least halves the length (rounding down) and decreases it by at least 1. Starting from $\ell = U - L$, the loop runs at most $\lfloor \lg(U - L) \rfloor + 1 = \lceil \lg(U - L + 1) \rceil$ times for $U > L$. With a test of cost $T(n)$, the total time is $O(T(n) \log(U - L + 1))$. LARGEST-FEASIBLE is the mirror image, and the same argument applies with the rounding of line L7.

## Classic examples

### The slowest speed that finishes in time

Piles of $3, 6, 7, 11$ items must be eaten in at most $8$ hours, one pile at a time, at most $v$ items per hour, with the rest of an hour wasted when a pile ends. The hours needed are $h(v) = \sum_i \lceil p_i / v \rceil$, which is non-increasing in $v$, so FEASIBLE$(v) = (h(v) \le 8)$ is monotone. The bounds are $L = 1$ and $U = 11$, the largest pile, since $h(11) = 4 \le 8$. SMALLEST-FEASIBLE$(1, 11)$ tests:

| lo | hi | mid | $h(mid)$ | feasible |
|---|---|---|---|---|
| 1 | 11 | 6 | 6 | yes |
| 1 | 6 | 3 | 10 | no |
| 4 | 6 | 5 | 8 | yes |
| 4 | 5 | 4 | 8 | yes |

It returns $v = 4$: $h(4) = 1 + 2 + 2 + 3 = 8$ and $h(3) = 1 + 2 + 3 + 4 = 10$.

### The first time when the machines are done

Three machines make one item in $2$, $3$ and $7$ minutes, and $10$ items are needed. In $t$ minutes they make $c(t) = \lfloor t/2 \rfloor + \lfloor t/3 \rfloor + \lfloor t/7 \rfloor$ items, which is non-decreasing in $t$. SMALLEST-FEASIBLE$(0, 20)$ with FEASIBLE$(t) = (c(t) \ge 10)$ tests $t = 10, 15, 13, 12, 11$ and returns $12$: $c(11) = 5 + 3 + 1 = 9$ and $c(12) = 6 + 4 + 1 = 11$. No closed form for this optimum is known in general.

### The integer square root

The largest $x$ with $x^2 \le 40$ is LARGEST-FEASIBLE$(0, 40)$ with FEASIBLE$(x) = (x^2 \le 40)$. It tests $x = 20, 10, 5, 7, 6$ and returns $6$. This is one method of the [integer square root](/integer-square-root/).

### Problems of this area

- [Linear partition](/minimax-partition/): the smallest largest block sum, with a greedy test in $O(n)$.
- [Maximin placement](/maximin-placement/): the largest smallest gap, with a greedy test in $O(n)$; a LARGEST-FEASIBLE search.
- [k-th smallest pair distance](/kth-smallest-pair-distance/): the smallest $d$ with at least $k$ pairs at distance at most $d$, with a [two-pointer](/two-pointers/) count in $O(n)$.
- [Minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/): the smallest $t$ such that the edges of weight at most $t$ connect the graph.

## Variations

- **A sorted list of candidates.** When the optimum is one of a known set of values (edge weights, pairwise differences, endpoints of intervals), sort the set and search on its index. This gives an exact answer and $\lceil \lg N \rceil$ tests for $N$ candidates, independent of the size of the numbers.
- **Real answers.** Search on a real interval until it is shorter than a tolerance, or for a fixed number of steps. See [binary search on real numbers](/binary-search-on-real-numbers/).
- **No upper bound.** Double $t$ until the test is true, then search the last gap, as in [exponential search](/exponential-search/). The cost is $O(\log \mathrm{OPT})$ tests.
- **Many queries.** When many independent searches share one expensive test structure, run them together in rounds: [parallel binary search](/parallel-binary-search/).
- **Exact real optimum.** [Parametric search](/parametric-search/) runs the test at the unknown optimum and resolves each comparison that the test makes, so it returns the exact value without a tolerance.
- **A penalty instead of a bound.** When the constraint is a count ("exactly $k$ parts"), a search on a penalty per part replaces the count; see the [Aliens trick](/aliens-trick/).
- **Ratios.** For "minimize $a(s)/b(s)$", the test "is $\min_s (a(s) - t\,b(s)) \le 0$?" is monotone in $t$; see [fractional programming](/fractional-programming/).

## Pitfalls

- **A test that is not monotone.** The search returns some point where the test changes, with no warning. Prove monotonicity before writing the loop; a test of each value of a small range against the search result catches most mistakes.
- **A test that is wrong on part of the range.** Packages $5, 1, 1, 1, 5$ must leave in order within 4 days. A greedy that opens a new day when a package does not fit, but never checks that one package fits in an empty day, reports 4 days for capacity 3. The search on $[1, 13]$ then returns 3, which is infeasible; the answer is 5. Start the search at the largest single package, or make the test reject it.
- **An upper bound that is not feasible.** SMALLEST-FEASIBLE assumes FEASIBLE$(hi)$. If no value is feasible, it returns $hi$ as if it were. Test $hi$ first when the instance may have no solution.
- **Rounding down in LARGEST-FEASIBLE.** With $mid = lo + \lfloor (hi - lo)/2 \rfloor$, the range $lo = 3$, $hi = 4$ gives $mid = 3$, and a true test sets $lo \leftarrow 3$ again: the loop never ends. Round up in line L7.
- **Overflow.** For answers near the limit of the integer type, $lo + hi$ can overflow. Use $lo + \lfloor (hi - lo)/2 \rfloor$. The test itself can also overflow, for example $x^2$ or a sum of many large blocks.
- **The value but not the solution.** The search returns the optimal value. Keep the witness of the last true test, or run the test once more at the answer, to get the solution itself.

## Exercises

1. Prove that LARGEST-FEASIBLE returns the largest feasible value and runs at most $\lceil \lg(hi - lo + 1) \rceil$ times.
2. Give an example of a test that is monotone on $[L, U]$ but for which the loop with $mid = \lfloor (lo + hi)/2 \rfloor$ fails when $lo$ and $hi$ can be negative, in a language whose integer division rounds toward zero.
3. Packages of weights $w_1, \ldots, w_n$ must ship in order within $D$ days. Show that the greedy test is correct when the capacity is at least $\max_i w_i$, and that the number of days it uses is non-increasing in the capacity.
4. A test costs $\Theta(n)$ and the answer is an integer in $[0, 10^{18}]$. How many tests does the search make? How many would a search over a sorted list of $n^2$ candidates make, and when is that better?

## References
