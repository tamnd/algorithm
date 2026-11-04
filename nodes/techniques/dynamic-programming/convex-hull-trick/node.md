---
tag: MM27CJ
kind: technique
slug: convex-hull-trick
name: Convex hull trick
aliases:
- CHT
- lines envelope optimisation
area: techniques/dynamic-programming
level: advanced
summary: Speed up DP transitions that take a minimum of linear functions by keeping their lower envelope.
prereqs: [convex-hull, deque, binary-search, prefix-sums]
see_also: [li-chao-tree, convex-hull, divide-and-conquer-optimization, monge-property, aliens-trick, slope-trick, segmented-least-squares]
sources:
  - paper: doi:10.1016/0166-218x(94)00146-5
    title: Peter Brucker, Efficient algorithms for some path partitioning problems, Discrete Applied Mathematics 62(1-3), 77-85, 1995
    locator: the linear-time algorithms for partitioning a path when the cost of a part is linear in a parameter of its end
  - paper: doi:10.1016/0304-3975(92)90135-3
    title: Zvi Galil and Kunsoo Park, Dynamic programming with convexity, concavity and sparsity, Theoretical Computer Science 92(1), 49-76, 1992
    locator: the one-dimensional recurrences with convex and concave weights
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 8, Section 8.2, Duality (lower envelopes of lines and convex hulls of points)
---

The convex hull trick speeds up a dynamic program whose transition is a minimum (or maximum) of linear functions of the query point: $E(j) = \min_{i < j} \bigl( m_i x_j + b_i \bigr) + c_j$, where the slope $m_i$ and the intercept $b_i$ depend only on $i$, and $x_j$ only on $j$. Each earlier state $i$ is a line, and the minimum over all lines at $x_j$ is the lower envelope of the lines, a concave piecewise linear function. Keeping only the lines that appear on the envelope turns the $O(n^2)$ scan into $O(n \log n)$ with binary search, or into $O(n)$ with a [deque](/deque/) when the slopes and the queries come in sorted order. The name comes from duality: the lines on the lower envelope correspond to the points on a [convex hull](/convex-hull/).

## In plain words

Some DP rules say: the best value at step $j$ is the smallest of many expressions, one for each earlier step $i$, and each expression is a straight line in one number that depends on $j$. Checking every earlier step for every $j$ is slow.

Draw all the lines. For any query number, the smallest value is on the lowest line at that point. Most lines are never the lowest anywhere, and you can throw them away for good. The lines that remain form a chain, ordered by slope. If the query numbers only grow, you also never need to go back along the chain, so each line is added once and removed once.

## When it applies

- The transition can be written as $\min_i (m_i x_j + b_i)$ plus terms that depend on $j$ only. Typical source: a cost $(S_j - S_i)^2$ or $S_j \cdot T_i$ that, after expanding, has one product of a $j$ term and an $i$ term.
- **Monotone case.** The slopes of the lines arrive in decreasing order (for a minimum), and the query points increase. Then a deque gives $O(1)$ amortized time per step.
- **Slopes sorted, queries in any order.** Keep the envelope in an array and answer a query by [binary search](/binary-search/) on the breakpoints, in $O(\log n)$.
- **No order at all.** Use a [Li Chao tree](/li-chao-tree/), or a balanced tree of lines sorted by slope, in $O(\log n)$ per operation.

## The template

The monotone case for a minimum: slopes strictly decreasing as lines are added, queries nondecreasing. The holes are the line of a state, the query point and the extra term.

```pseudo id=main
CHT-DP(n)
L1  E[0] ← base; Q ← empty deque; ADD(line(0))        ▷ hole: line(i) = (m_i, b_i) from E[i]
L2  for j ← 1 to n do
L3      x ← x_j                                         ▷ hole: the query point of j
L4      while |Q| ≥ 2 and value(Q[1], x) ≤ value(Q[0], x) do pop front of Q
L5      E[j] ← value(Q[0], x) + c_j                     ▷ hole: the term that depends on j only
L6      ADD(line(j))
L7  return E[n]

ADD(ℓ)
L8  while |Q| ≥ 2 and USELESS(Q[−2], Q[−1], ℓ) do pop back of Q
L9  push ℓ at the back of Q

USELESS((m1, b1), (m2, b2), (m3, b3))                   ▷ m1 > m2 > m3
L10 return (b3 − b1)(m1 − m2) ≤ (b2 − b1)(m1 − m3)
```

**Why line L10 is the right test.** For lines with $m_1 > m_2 > m_3$, line 1 is lowest far to the left and line 3 far to the right. Line 1 meets line 2 at $x_{12} = (b_2 - b_1)/(m_1 - m_2)$ and meets line 3 at $x_{13} = (b_3 - b_1)/(m_1 - m_3)$. Line 2 is on the lower envelope of the three exactly when it is below both others somewhere, which is when $x_{12} < x_{13}$. Line L10 is $x_{13} \le x_{12}$ with the two positive denominators multiplied out, so it uses only integer arithmetic when the inputs are integers. A line removed in line L8 is never needed later, because the new line and the line before it already cover every point where it was lowest, and later lines can only cover more.

**Why line L4 is safe.** The deque holds the envelope from left to right, with breakpoints increasing. If the second line is at least as low as the first at $x$, then the first line is above the envelope at $x$ and at every larger $x$, so with nondecreasing queries it is never needed again.

**Cost.** Each line is pushed once and popped at most once, by line L4 or by line L8. So all $n$ steps take $O(n)$ time in total, with $O(n)$ space.

## Classic examples

### Splitting an array with a square cost and a fixed charge

Cut $a = (2, 3, 1, 4)$ into parts; a part with sum $s$ costs $s^2 + C$, with $C = 5$. With prefix sums $S = (0, 2, 5, 6, 10)$,

$$E(j) = \min_{i < j} \bigl( E(i) + (S_j - S_i)^2 \bigr) + C = \min_{i < j} \bigl( -2 S_i \cdot S_j + E(i) + S_i^2 \bigr) + S_j^2 + C.$$

So state $i$ is the line with slope $-2 S_i$ and intercept $E(i) + S_i^2$, the query is $x_j = S_j$, and $c_j = S_j^2 + C$. The slopes decrease and the queries increase because all $a_k \ge 1$.

| $j$ | $x_j = S_j$ | lines in the deque | their values at $x_j$ | $E(j)$ |
|---|---|---|---|---|
| 1 | 2 | $(0, 0)$ | 0 | $0 + 4 + 5 = 9$ |
| 2 | 5 | $(0, 0)$, $(-4, 13)$ | 0, $-7$ | $-7 + 25 + 5 = 23$ |
| 3 | 6 | $(-4, 13)$, $(-10, 48)$ | $-11$, $-12$ | $-12 + 36 + 5 = 29$ |
| 4 | 10 | $(-10, 48)$, $(-12, 65)$ | $-52$, $-55$ | $-55 + 100 + 5 = 50$ |

The table shows the deque when line L4 starts. At $j = 2$, line L4 removes $(0, 0)$, because $(-4, 13)$ is lower at $x = 5$; at $j = 3$ it removes $(-4, 13)$ and at $j = 4$ it removes $(-10, 48)$ in the same way. The answer is $E(4) = 50$, which cuts every element into its own part: $4 + 9 + 1 + 16 + 4 \cdot 5 = 50$. The plain $O(n^2)$ recurrence gives the same table, and on 500 random inputs the two methods agree.

### Other uses

- **Batching problems.** Brucker's path partitioning problems, and scheduling of jobs in batches, where a batch costs a setup time plus a product of a sum and a weight.
- **Kinetic or parametric minima.** "For each query $x$, which of these lines is lowest" in any setting, for example the cheapest plan as a function of a price.
- **Inside other methods.** With the [aliens trick](/aliens-trick/), the remaining one-parameter problem is often solved by the convex hull trick.

## Variations

- **Maximum instead of minimum.** Negate the lines, or keep the upper envelope with the slopes in increasing order.
- **Queries in any order.** Do not pop the front; find the line for $x$ by binary search on the breakpoints of the deque. $O(\log n)$ per query.
- **Lines in any order.** A [Li Chao tree](/li-chao-tree/) over the range of queries inserts a line and answers a query in $O(\log X)$; a balanced tree of the envelope (sometimes called a dynamic hull) does the same in $O(\log n)$.
- **Divide and conquer on time.** When the slopes are not sorted, but all queries are offline, a recursion on the order of the states (often called CDQ divide and conquer) sorts the lines and the queries in each half.
- **Beyond lines.** When the functions are not lines but any two of them cross at most once, the same deque works with the crossing test replaced. This is the concave or convex least weight subsequence method of [optimal text wrapping](/optimal-text-wrapping/).

## Pitfalls

- **Equal slopes.** Line L10 divides by $m_1 - m_2$ in spirit. If two lines have the same slope, keep only the one with the smaller intercept before calling ADD.
- **Overflow.** The products in line L10 have about twice the bits of the inputs. With values near $10^9$ the products are near $10^{36}$; use 128-bit integers or exact rationals, or compare the intersection points as fractions with care.
- **Floating point.** Computing the intersection points with floating point can remove a needed line when two breakpoints are very close. Prefer the integer test.
- **Order assumptions.** The monotone deque is wrong if the slopes or the queries are not sorted. Check the signs: for a minimum with increasing queries, the slopes must decrease.
- **The wrong envelope.** For a maximum, the test and the order flip. Mixing them gives an envelope that is neither.

## Exercises

1. Show that the lower envelope of $n$ lines has at most $n$ pieces, and that the lines on it appear in decreasing order of slope from left to right.
2. Prove that the test of line L10 is equivalent to $x_{13} \le x_{12}$.
3. Solve the example recurrence when some $a_k$ may be 0, so that equal slopes occur.
   <details><summary>Hint</summary>Equal prefix sums give lines with the same slope; keep the lower one, which is the one with the smaller $E(i)$.</details>
4. Given $n$ points $(p_i, q_i)$ and queries $x$, answer $\max_i (p_i x + q_i)$ for queries in any order in $O((n + q) \log n)$ time.

## References
