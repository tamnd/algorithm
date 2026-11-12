---
tag: 7GGJ22
kind: algorithm
slug: threshold-algorithm
name: Threshold algorithm
aliases:
- Fagin-Lotem-Naor threshold algorithm
- threshold algorithm for top-k aggregation
area: systems/database-algorithms
level: advanced
summary: "Top-k over m graded lists: score each object on first sight by random access, and stop once k objects score at least t applied to the last grades read."
solves: [top-k-query]
model: query-model
complexity:
  vars: {n: the number of objects, m: the number of lists, k: the number of answers}
  time: {worst: O(m^2 n)}
  space: {extra: O(k + m)}
properties: {deterministic: true, recursive: false, online: true}
prereqs: [top-k-query, fagin-algorithm, priority-queue]
see_also: [no-random-access-algorithm, top-k-selection, binary-heap, k-way-merge, pareto-front-computation, hash-table]
sources:
  - paper: doi:10.1016/S0022-0000(03)00026-6
    title: Ronald Fagin, Amnon Lotem and Moni Naor, Optimal aggregation algorithms for middleware, Journal of Computer and System Sciences 66(4), 614 to 656 (2003); first in PODS 2001, 102 to 113
    locator: Section 4 (TA, Theorem 4.1 on correctness, Theorem 4.2 on bounded buffers), Section 5 (instance optimality), Section 6 (Theorem 6.1, Corollary 6.2, Example 6.3, Theorem 6.4)
  - paper: doi:10.1006/jcss.1998.1600
    title: Ronald Fagin, Combining fuzzy information from multiple systems, Journal of Computer and System Sciences 58(1), 83 to 99 (1999)
    locator: Fagin's algorithm, which TA improves on
  - paper: doi:10.1145/1391729.1391730
    title: Ihab F. Ilyas, George Beskales and Mohamed A. Soliman, A survey of top-k query processing techniques in relational database systems, ACM Computing Surveys 40(4), Article 11 (2008)
    locator: the section on top-k processing over sorted lists, and the variants of TA
---

The threshold algorithm (TA) finds the $k$ objects with the highest combined score over $m$ lists, each sorted by one grade. It reads the lists in parallel from the top. Each time it sees an object, it fetches the object's other grades by random access and computes the exact score. After each round it computes the *threshold* $\tau$, the combining function applied to the last grade read in each list; no unseen object can score above $\tau$. TA stops as soon as $k$ objects score at least $\tau$. Fagin, Lotem and Naor (2001) proved that TA is *instance optimal*: on every database, its cost is within a constant factor of the cost of any correct algorithm that makes no wild guesses.

## In plain words

Two web sites rank the same hotels, one by rooms and one by service. You want the best 2 by the sum of both scores.

Read both lists from the top, one line from each at a time. Each time you meet a new hotel, ask the other site for its score, add the two scores, and keep the best 2 hotels so far.

After each line, add up the two scores you just read. A hotel you have not met yet is lower on both lists, so its total is at most this sum. Once your best 2 hotels both have totals at least this sum, no hotel you have not met can beat them, and you stop.

## The problem

The input is a [top-k query](/top-k-query/): $m$ lists over the same $N$ objects, list $L_i$ sorted by grade $x_i(R)$ from high to low, a monotone aggregation $t$ (raising one grade never lowers the score), and $k$. The output is $k$ objects with the highest scores $t(R) = t(x_1(R), \ldots, x_m(R))$, with their scores. A *sorted access* reads the next entry of a list; a *random access* asks for the grade of a given object in a given list. The cost is $s c_S + r c_R$ for $s$ sorted and $r$ random accesses.

## The algorithm

```pseudo id=main
THRESHOLD(L_1 .. L_m, t, k)
L1  Y ← an empty buffer of at most k (object, score) pairs; d ← 0
L2  while d < N do
L3      for i ← 1 to m do
L4          (R, x̲_i) ← L_i[d]                       ▷ sorted access
L5          if R ∉ Y then get the other grades of R by random access; s ← t(R)
L6              put (R, s) in Y if Y has fewer than k pairs or s beats the worst one
L7      τ ← t(x̲_1, ..., x̲_m)                        ▷ the threshold
L8      d ← d + 1
L9      if Y has k pairs and each score in Y is at least τ then stop
L10 return Y, best first
```

The buffer is a min-[heap](/binary-heap/) on score, so line L6 takes $O(\log k)$ time. Objects that left the buffer are not remembered; if one is seen again in another list, it is looked up again. This keeps the memory at $O(k + m)$.

## Example

Find the top 2 under $t = $ sum:

| depth | $L_1$ | $L_2$ |
|---|---|---|
| 1 | a 0.9 | c 0.9 |
| 2 | b 0.8 | a 0.8 |
| 3 | c 0.7 | e 0.7 |
| 4 | d 0.6 | b 0.4 |
| 5 | e 0.1 | d 0.2 |

| depth | seen now | score by random access | buffer | threshold $\tau$ | stop? |
|---|---|---|---|---|---|
| 1 | a, c | a 1.7, c 1.6 | a 1.7, c 1.6 | 0.9 + 0.9 = 1.8 | no |
| 2 | b (a is in the buffer) | b 1.2 | a 1.7, c 1.6 | 0.8 + 0.8 = 1.6 | yes |

TA stops after 4 sorted and 3 random accesses. [Fagin's algorithm](/fagin-algorithm/) on the same lists reads to depth 3, where c becomes the second object seen in both lists. With $t = \max$ and $k = 1$, TA always stops at depth 1, because the best object of the first round scores the threshold itself.

## Correctness

The buffer holds the $k$ best objects seen so far. An object that has not been seen lies below depth $d$ in each list, so each of its grades is at most the last grade read in that list, and by monotonicity its score is at most $\tau$. When TA stops, each buffered object scores at least $\tau$, so it beats every unseen object, and it beats every seen object outside the buffer by the buffer rule. When $k$ objects have been seen in all lists, as in Fagin's algorithm, each of them scores at least $\tau$, so TA never reads deeper than FA. The full proof is in the proof file.

## Complexity

- **Per depth.** At depth $d$, TA has made $m d$ sorted accesses and at most $m (m - 1) d$ random accesses.
- **Instance optimality.** Let $A$ be any algorithm that is correct on every database and never makes a *wild guess* (a random access to an object it has not seen by sorted access). If $A$ sees $a$ distinct objects, TA stops by depth $a + k$. So for every database $D$,

  $$\mathrm{cost}(TA, D) \le \Bigl(m + m(m-1)\frac{c_R}{c_S}\Bigr) \mathrm{cost}(A, D) + O(1).$$

  For a strict $t$ such as min, this ratio is exact, and no deterministic algorithm without wild guesses has a smaller one.
- **Worst case.** $m N$ sorted and $m(m-1) N$ random accesses, when the answer is only known after reading the whole lists.
- **Space.** $O(k + m)$: the buffer and the last grades. Fagin's algorithm needs memory for all seen objects.

## Properties

- **Correct for every monotone $t$**, with exact scores.
- **No later than Fagin's algorithm** on every database, in sorted accesses.
- **Instance optimal** over algorithms without wild guesses; with wild guesses, no algorithm is instance optimal (Example 6.3 of Fagin, Lotem and Naor: a lucky guess can find the answer in two random accesses where any algorithm without guesses needs $n + 1$ sorted accesses).
- **Anytime.** At any depth, the buffer with the current $\tau$ gives a guarantee: each buffered object is within a factor $\tau / \min_Y t$ of being correct for positive scores.

## Variants and improvements

- **[NRA](/no-random-access-algorithm/).** When random access is impossible, keep a lower and an upper bound on each score instead.
- **Combined algorithm (CA).** Does random accesses only every $h = \lfloor c_R / c_S \rfloor$ rounds and only for the most promising objects, to get an optimality ratio that does not depend on $c_R / c_S$ in some settings.
- **Approximation, TA with $\theta$.** Stop when $k$ objects score at least $\tau / \theta$ to get a $\theta$-approximate top $k$ earlier.
- **Restricted sorted access.** Some lists may allow only random access (TAz).
- **Memoization.** Remembering every seen object avoids repeated random accesses for an object seen in several lists, at the cost of unbounded memory.
- **Uneven rates.** The lists need not be read in lockstep; the results hold if the rates of sorted access are within constant factors.

## When to use it

Use TA when each source supports both sorted and cheap random access, for example inverted lists with a document index, or ranked results from several services that can also score a given object. It is the standard algorithm for top-k aggregation over ranked lists, and the basis of many top-k joins and rank-aware query operators. If random access is costly compared to sorted access, prefer CA or NRA.

## Pitfalls

- **Non-monotone $t$.** The threshold bound fails, and TA can stop with a wrong answer.
- **Grades of skipped objects.** An object already in the buffer must not be inserted twice; an object that left the buffer cannot come back, since its score is at most the buffer's minimum.
- **Stop test with ties.** The test is "at least $\tau$", not "greater than $\tau$". With a strict test, TA can read to the end on lists with many equal grades.
- **Expensive random access.** The optimality ratio grows with $c_R / c_S$; if random access is 1000 times slower, TA can be far from the best plan in practice.

## Implementations

## History

Fagin, Lotem and Naor presented TA at PODS 2001, and the journal version appeared in 2003; the paper received the Gödel Prize in 2014. They noted that the same algorithm had been found independently by Nepal and Ramakrishna (ICDE 1999, the first to publish it) and by Güntzer, Balke and Kießling (VLDB 2000, as the basic version of "Quick-Combine"), but the instance optimality results were new.

## References
