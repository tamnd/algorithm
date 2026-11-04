---
tag: 8Z8378
kind: theorem
slug: max-min-lower-bound
name: Simultaneous maximum and minimum lower bound
aliases:
- max-min lower bound
- ceil(3n/2) comparisons
area: foundations/lower-bounds
level: core
summary: Finding both the maximum and the minimum needs ceil(3n/2) - 2 comparisons.
prereqs: [max-finding-lower-bound, adversary-argument, comparison-model]
see_also: [minimum-and-maximum-finding, max-finding-lower-bound, adversary-argument, second-largest-lower-bound, decision-tree-method, information-theoretic-bound, small-order-statistics, selection-lower-bound]
sources:
  - paper: doi:10.1145/361405.361423
    title: Ira Pohl, A sorting problem and its complexity, Communications of the ACM 15(6) (1972)
    locator: pp. 462 to 464 (the worst-case bound ceil(3n/2) - 2 for the maximum and the minimum, and the matching algorithm)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.1, Minimum and maximum (the algorithm by pairs with at most 3 floor(n/2) comparisons, and the exercise that asks for the lower bound ceil(3n/2) - 2)
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.3, Minimum-comparison selection (the maximum and the minimum together, in the text and exercises)
---

The simultaneous maximum and minimum lower bound says that every comparison algorithm that finds both the largest and the smallest of $n$ distinct items makes at least $\lceil 3n/2 \rceil - 2$ comparisons in the worst case. An algorithm that compares the items in pairs meets the bound, so the value is exact for every $n \ge 1$. The proof is an [adversary argument](/adversary-argument/) with a potential that counts what is still unknown about each item. Two separate scans make $2n - 3$ comparisons, so the bound shows that working on both ends at once saves about $n/2$ comparisons and no more.

## Statement

**Theorem (Pohl, 1972).** Let $n \ge 1$, and let $MM(n)$ be the least number $t$ such that some deterministic comparison algorithm finds the index of the largest and the index of the smallest of any $n$ distinct keys with at most $t$ comparisons. Then

$$MM(n) = \left\lceil \frac{3n}{2} \right\rceil - 2 \quad (n \ge 2), \qquad MM(1) = 0.$$

So $MM(n) = 3n/2 - 2$ for even $n$ and $MM(n) = (3n - 3)/2$ for odd $n$.

## In plain words

To be sure of the largest item, every other item must have lost a comparison. To be sure of the smallest, every other item must have won one. So almost every item needs one win and one loss, which is twice as much to learn as for the largest item alone.

A comparison of two fresh items gives a win to one and a loss to the other, so it does two pieces of this work at once. Any other comparison can be answered so that it does only one piece. Fresh items run out after about half of the items are paired. So about half of the work comes two pieces at a time, and the rest one piece at a time. This gives about one and a half comparisons per item.

## Proof

**Upper bound.** If $n$ is even, compare $x_1$ with $x_2$ and take the larger as the current maximum and the smaller as the current minimum: 1 comparison. If $n$ is odd, take $x_1$ as both: 0 comparisons. Then take the remaining items two at a time. Compare the two items of a pair with each other, compare the larger with the current maximum, and compare the smaller with the current minimum: 3 comparisons per pair. This is correct, because each item that is not the final maximum lost to its partner or to a current maximum, and the same for the minimum. The count is

$$1 + 3 \cdot \frac{n-2}{2} = \frac{3n}{2} - 2 \ \ (n \text{ even}), \qquad 3 \cdot \frac{n-1}{2} = \frac{3n-3}{2} \ \ (n \text{ odd}),$$

which is $\lceil 3n/2 \rceil - 2$ in both cases (for odd $n$, $\lceil 3n/2 \rceil = (3n+1)/2$).

```pseudo id=pairs
MAX-AND-MIN(x[1..n])
L1  if n is even then
L2      if x[1] > x[2] then (hi, lo) ← (1, 2) else (hi, lo) ← (2, 1)
L3      i ← 3
L4  else
L5      (hi, lo) ← (1, 1); i ← 2
L6  while i < n do
L7      if x[i] > x[i+1] then (a, b) ← (i, i+1) else (a, b) ← (i+1, i)
L8      if x[a] > x[hi] then hi ← a
L9      if x[b] < x[lo] then lo ← b
L10     i ← i + 2
L11 return (hi, lo)
```

**Lower bound.** Let $n \ge 2$. During the run of an algorithm, give each item one of four labels.

| label | meaning | units |
|---|---|---|
| N | not yet in any comparison | 2 |
| W | has won at least once and never lost | 1 |
| L | has lost at least once and never won | 1 |
| M | has won and lost | 0 |

An item counts 1 unit for "has never lost" and 1 unit for "has never won". Let $U$ be the total number of units. At the start, all items are N, so $U = 2n$.

*The adversary.* The adversary keeps a value for each item, all values distinct, so that its answers so far are those of the current values. Before a comparison it may change values in three ways that keep all earlier answers true:

- an N item has been in no comparison, so it may get any value;
- a W item has only won, so it may be raised above all values;
- an L item has only lost, so it may be lowered below all values.

Before each comparison, the adversary raises each W item and lowers each L item that takes part. For an N item, it gives the value that the table below needs, above all values or below all values. Then it answers by the values. This is an input of distinct keys that agrees with all answers, at each step. The answers and the change of $U$:

| comparison | answer | new labels | change of $U$ |
|---|---|---|---|
| N with N | either one wins | W and L | $-2$ |
| N with W | W wins | L and W | $-1$ |
| N with L | N wins | W and L | $-1$ |
| N with M | N wins | W and M | $-1$ |
| W with W | either one wins | W and M | $-1$ |
| L with L | either one wins | M and L | $-1$ |
| W with L | W wins | W and L | 0 |
| W with M, L with M, M with M | by the values, W wins and L loses | no change | 0 |

*The end condition.* Suppose that the algorithm stops with outputs $h$ (largest) and $\ell$ (smallest). If an item $y \ne h$ has never lost, it is N or W, and the adversary may raise it above all values without changing an answer. Then $y$ is the largest key, and the output $h$ is wrong. So at the stop each item other than $h$ has lost. In the same way, each item other than $\ell$ has won. Since $n \ge 2$ and the keys are distinct, $h \ne \ell$, so at the stop $U = 2$: one unit for $h$ and one for $\ell$.

*The count.* Let $c_2$ be the number of comparisons of two N items, and $c$ the number of all comparisons. Each comparison of two N items lowers $U$ by 2, and each other comparison lowers $U$ by at most 1. So

$$2n - 2 \le 2 c_2 + (c - c_2) = c + c_2.$$

A comparison of two N items turns both into W or L, and no item becomes N again, so $c_2 \le \lfloor n/2 \rfloor$. Hence

$$c \ge 2n - 2 - \left\lfloor \frac{n}{2} \right\rfloor = \left\lceil \frac{3n}{2} \right\rceil - 2,$$

since $2n - \lfloor n/2 \rfloor = \lceil 3n/2 \rceil$. ∎

## Consequences

- **The saving is exactly a quarter.** Two scans, one for the maximum ($n - 1$ comparisons) and one for the minimum among the other $n - 1$ items ($n - 2$ comparisons), make $2n - 3$. The pairs algorithm saves $\lfloor n/2 \rfloor - 1$ comparisons, and the theorem shows that no algorithm saves more.
- **Counting is weak here.** There are $n(n-1)$ possible outputs, so the [information-theoretic bound](/information-theoretic-bound/) gives $\lceil \lg(n(n-1)) \rceil$, which grows like $2 \lg n$.
- **A model for other selection bounds.** The same kind of potential, with weights in place of labels, gives the bound $n + \lceil \lg n \rceil - 2$ for the [second largest](/second-largest-lower-bound/), and labels of this kind appear in lower bounds for [selection](/selection-lower-bound/).

| $n$ | $\lceil \lg(n(n-1)) \rceil$ | $MM(n) = \lceil 3n/2 \rceil - 2$ | two scans $2n - 3$ |
|---|---|---|---|
| 2 | 1 | 1 | 1 |
| 3 | 3 | 3 | 3 |
| 4 | 4 | 4 | 5 |
| 5 | 5 | 6 | 7 |
| 6 | 5 | 7 | 9 |
| 8 | 6 | 10 | 13 |
| 10 | 7 | 13 | 17 |
| 100 | 14 | 148 | 197 |
| 1000 | 20 | 1498 | 1997 |
| $10^6$ | 40 | 1499998 | 1999997 |

## Tightness

The bound is exact for every $n$, by the pairs algorithm. For $n \le 4$ the counting bound is also exact, and from $n = 5$ on the adversary bound is larger.

The bound is for the worst case only. Unlike the bound for the [maximum alone](/max-finding-lower-bound/), it does not hold on every input.

### Pitfalls

- **Not every input is hard.** For $n = 3$ and keys $x_1 < x_2 < x_3$, the algorithm "compare $x_1$ with $x_2$, then $x_2$ with $x_3$" learns the full order after 2 comparisons, while $MM(3) = 3$. On a fixed input, a comparison of an N item with a W item can lower $U$ by 2 if the N item wins. The adversary is what stops this.
- **The adversary must stay consistent.** It may raise a W item or lower an L item, but it may not raise an L item, which has lost to some item that may now be smaller. Each rule in the table needs a value change of the allowed kinds.
- **The end condition needs $n \ge 2$.** For $n = 1$ the same item is both answers, $U$ ends at 2 with one item, and the bound $\lceil 3/2 \rceil - 2 = 0$ is right but the proof reads differently.
- **Counting comparisons, not time.** The pairs algorithm makes about $1.5n$ comparisons against $2n$ for two scans, but on a modern computer the time also depends on branches and memory access, so the measured gain can be smaller.

## History

Pohl (1972) proved that $\lceil 3n/2 \rceil - 2$ comparisons are necessary and sufficient for the maximum and minimum together. Knuth, Volume 3, Section 5.3.3, treats the problem with minimum-comparison selection. CLRS, Section 9.1, gives the algorithm by pairs with at most $3 \lfloor n/2 \rfloor$ comparisons and asks for the lower bound $\lceil 3n/2 \rceil - 2$ in an exercise.

## References
