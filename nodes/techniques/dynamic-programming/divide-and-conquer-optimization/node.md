---
tag: AHWCKX
kind: technique
slug: divide-and-conquer-optimization
name: Divide-and-conquer optimization
aliases:
- D&C DP optimisation
- monotone matrix row minima by divide and conquer
area: techniques/dynamic-programming
level: advanced
summary: Speed up layered DP when the optimal split points are monotone.
prereqs: [monge-property, row-minima-of-totally-monotone-matrices]
see_also: [knuth-optimization, smawk-algorithm, row-minima-of-totally-monotone-matrices, monge-property, aliens-trick, convex-hull-trick, segmented-least-squares]
sources:
  - paper: doi:10.1016/0304-3975(92)90135-3
    title: Zvi Galil and Kunsoo Park, Dynamic programming with convexity, concavity and sparsity, Theoretical Computer Science 92(1), 49-76, 1992
    locator: the survey of the recurrences with Monge (convex and concave) weights and of the matrix searching methods
  - paper: doi:10.1007/BF01840359
    title: Alok Aggarwal, Maria M. Klawe, Shlomo Moran, Peter Shor and Robert Wilber, Geometric applications of a matrix-searching algorithm, Algorithmica 2, 195-208, 1987
    locator: monotone and totally monotone matrices and their row minima
  - paper: doi:10.1016/0166-218X(95)00103-X
    title: Rainer E. Burkard, Bettina Klinz and Rüdiger Rudolf, Perspectives of Monge properties in optimization, Discrete Applied Mathematics 70(2), 95-161, 1996
    locator: the sections on row minima of Monge matrices and on dynamic programming
---

The divide-and-conquer optimization computes one layer $F_t(j) = \min_{k < j} \bigl( F_{t-1}(k) + w(k, j) \bigr)$ of a layered dynamic program in $O(n \log n)$ time instead of $O(n^2)$, when the best $k$ for $j$ moves only to the right as $j$ grows. It finds the best $k$ for the middle $j$ by a scan, and then solves the left half with the candidates up to that $k$ and the right half with the candidates from that $k$. The monotone condition holds whenever $w$ satisfies the quadrangle inequality of the [Monge property](/monge-property/). The method is the simple form of the [row minima](/row-minima-of-totally-monotone-matrices/) search for monotone matrices; the [SMAWK algorithm](/smawk-algorithm/) does the same layer in $O(n)$.

## In plain words

You must cut a row of items into a fixed number of groups, and each group has a cost. You build the answer one group at a time. For each end point, you look for the best place where the last group starts. Trying every place for every end point is slow.

Often the best start moves only to the right when the end point moves to the right. Then you can find the best start for the middle end point first. All end points to its left have their best start at or before it, and all end points to its right have their best start at or after it. You split the problem in two halves with smaller search ranges and repeat. Each round of halving costs about one pass over the items.

## When it applies

- The recurrence has layers: $F_t$ is computed from $F_{t-1}$ only, by $F_t(j) = \min_{k < j} \bigl( F_{t-1}(k) + w(k, j) \bigr)$. Typical sources: cut an array into exactly $T$ contiguous parts, place $T$ facilities on a line, or any [segmented least squares](/segmented-least-squares/) type problem with a fixed number of segments.
- Let $opt_t(j)$ be the leftmost $k$ that attains the minimum. The method needs $opt_t(j) \le opt_t(j+1)$ for all $j$.
- A sufficient test: $w$ satisfies the **quadrangle inequality** $w(a, c) + w(b, d) \le w(a, d) + w(b, c)$ for all $a \le b \le c \le d$. For a cost $g(S_j - S_k)$ of a part, with prefix sums $S$ of nonnegative numbers, this holds when $g$ is convex.
- $w(k, j)$ must be computable in $O(1)$ time, usually from prefix sums.

The proof of the test is short. Let $j < j'$, let $k = opt_t(j)$ and suppose $k' = opt_t(j') < k$. Since $k$ is the leftmost minimum for $j$, $F_{t-1}(k') + w(k', j) > F_{t-1}(k) + w(k, j)$. The quadrangle inequality on $k' \le k \le j \le j'$ gives $w(k', j') - w(k, j') \ge w(k', j) - w(k, j)$. Adding the two, $F_{t-1}(k') + w(k', j') > F_{t-1}(k) + w(k, j')$, so $k'$ is not a minimum for $j'$, a contradiction. Here $k < j$, so both $k$ and $k'$ are valid candidates for $j$ and for $j'$.

## The template

The holes are the cost $w$, the base layer $F_0$ and the number of layers. The procedure fills $F_t(j)$ for $lo \le j \le hi$, knowing that $opt_t(j)$ lies in $[optlo, opthi]$.

```pseudo id=main
SOLVE-LAYER(t, lo, hi, optlo, opthi)
L1  if lo > hi then return
L2  mid ← ⌊(lo + hi) / 2⌋
L3  best ← +∞, bestk ← optlo
L4  for k ← optlo to min(mid − 1, opthi) do
L5      v ← F[t−1][k] + w(k, mid)                  ▷ hole: the cost w
L6      if v < best then best ← v, bestk ← k        ▷ strict: keep the leftmost
L7  F[t][mid] ← best
L8  SOLVE-LAYER(t, lo, mid − 1, optlo, bestk)
L9  SOLVE-LAYER(t, mid + 1, hi, bestk, opthi)

LAYERED-DP(n, T)
L10 F[0][0] ← 0, F[0][j] ← +∞ for 1 ≤ j ≤ n      ▷ hole: the base layer
L11 for t ← 1 to T do SOLVE-LAYER(t, 1, n, 0, n − 1)
L12 return F[T][n]
```

**Why lines L8 and L9 are safe.** By the monotone condition, every $j < mid$ has $opt_t(j) \le opt_t(mid) = bestk$, and every $j > mid$ has $opt_t(j) \ge bestk$. So the true optimum of each $j$ stays inside the range passed to its call, and line L4 scans it. If all values in the range are $+\infty$ (for example, $j$ is too small to hold $t$ parts), line L7 stores $+\infty$, and $bestk = optlo$ is a safe bound for both halves.

**Why the cost is $O(n \log n)$ per layer.** The calls at one depth of the recursion have disjoint ranges of $j$, and their ranges of $k$ overlap only at their ends, since a call passes $[optlo, bestk]$ and $[bestk, opthi]$ to its children. So one depth scans at most $n$ plus the number of calls values of $k$, which is $O(n)$. There are $\lceil \lg(n+1) \rceil$ depths. With $T$ layers the total is $O(T n \log n)$ time and $O(n)$ space per layer, against $O(T n^2)$ for the plain scan.

## Classic examples

### Cutting an array into parts

Cut $a = (4, 1, 3, 2, 5, 1, 2)$ into $T = 3$ contiguous nonempty parts, and minimize the sum of the squares of the part sums. With prefix sums $S$, $w(k, j) = (S_j - S_k)^2$, which satisfies the quadrangle inequality because $x \mapsto x^2$ is convex. The layers, with $j$ the number of items covered, are:

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $F_1(j)$ | 16 | 25 | 64 | 100 | 225 | 256 | 324 |
| $F_2(j)$ | | 17 | 32 | 50 | 113 | 128 | 164 |
| $opt_2(j)$ | | 1 | 1 | 2 | 3 | 3 | 3 |
| $F_3(j)$ | | | 26 | 36 | 75 | 86 | 114 |
| $opt_3(j)$ | | | 2 | 3 | 4 | 4 | 4 |

The rows of $opt$ are nondecreasing, as the condition says. For layer 3, the first call takes $mid = 4$, scans $k \in \{0, 1, 2, 3\}$ and finds $opt_3(4) = 3$. Then $j \in \{1, 2, 3\}$ only scans $k \le 3$ and $j \in \{5, 6, 7\}$ only scans $k \ge 3$. The answer is $F_3(7) = 114$, with the parts $(4, 1)$, $(3, 2)$ and $(5, 1, 2)$ of sums 5, 5 and 8, and $25 + 25 + 64 = 114$.

For 1000 random items and 10 layers, line L5 runs 96,248 times, against 5,005,000 for the plain scan.

### Other uses

- **Placing facilities on a line.** Put $T$ facilities among $n$ sorted villages and minimize the total distance from each village to its nearest facility. The cost of serving a run of villages by one facility at their median satisfies the quadrangle inequality.
- **Histogram and data partition.** Split a sorted list into $T$ buckets with the least total squared error, as in the [segmented least squares](/segmented-least-squares/) problem with a fixed number of segments, or one-dimensional [k-means](/k-means/).
- **As the inner loop of other methods.** With the [aliens trick](/aliens-trick/), the layer count is removed, and the remaining one-layer recurrence can again use a monotone search.

## Variations

- **Linear time per layer.** Each layer is a row minima problem on the matrix $A[j][k] = F_{t-1}(k) + w(k, j)$, which is Monge when $w$ is (adding a term that depends only on the column keeps the property). The [SMAWK algorithm](/smawk-algorithm/) solves it in $O(n)$, at the cost of a more complex program. The entries with $k \ge j$ must be set to $+\infty$ in a way that keeps total monotonicity, or the problem must be handled as a staircase matrix.
- **Online layers.** When $F(j)$ depends on $F(k)$ of the same layer, as in $E(j) = \min_{k < j} (E(k) + w(k, j))$, the values are not all known in advance, and this method does not apply directly. Use the queue of candidates of the concave least weight subsequence method (see [optimal text wrapping](/optimal-text-wrapping/)), or the [convex hull trick](/convex-hull-trick/) for linear costs.
- **Interval problems.** For $c(i, j) = w(i, j) + \min_k (c(i, k-1) + c(k, j))$, use [Knuth's optimization](/knuth-optimization/), which uses the monotone split points in two directions and gives $O(n^2)$.
- **Rightmost optimum.** With the test $\le$ in line L6, the procedure keeps the rightmost minimum. Under the quadrangle inequality the rightmost minima are also nondecreasing, so both choices work, but the choice must be the same in all calls.

## Pitfalls

- **A cost that is not Monge.** With $w(k, j) = \sqrt{S_j - S_k}$, a concave cost, the optima need not be monotone. For $a = (6, 8, 5, 4, 4, 8)$ and $T = 2$, the plain scan gives about 7.835 and the divide-and-conquer method gives about 8.025.
- **Off-by-one in the ranges.** Line L4 must stop at $\min(mid - 1, opthi)$, because $k < j$. Passing $bestk - 1$ or $bestk + 1$ to the children, instead of $bestk$, can cut the true optimum out of a range when two values of $j$ share the same optimum.
- **Recursion depth.** The depth is only $O(\log n)$, but a program that recurses on each layer inside another recursion can still be slow in some languages. An iterative version with an explicit stack is simple.
- **Using it where a same-layer dependency exists.** The method needs the whole row $F_{t-1}$ before it starts the layer $t$.

## Exercises

1. Prove that $w(k, j) = (S_j - S_k)^2$ satisfies the quadrangle inequality when $S$ is nondecreasing.
2. Prove that the rightmost optima are also nondecreasing when $w$ satisfies the quadrangle inequality.
   <details><summary>Hint</summary>Repeat the proof for the leftmost optimum with the roles of the strict and the non-strict inequality swapped.</details>
3. Show that the calls at one depth of the recursion scan at most $n$ plus the number of these calls values of $k$, and conclude that one layer scans $O(n \log n)$ values.
4. For the facility problem, show that the cost of serving the villages $k+1, \ldots, j$ from their median satisfies the quadrangle inequality.

## References
