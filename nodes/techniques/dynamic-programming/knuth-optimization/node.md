---
tag: ARYT52
kind: technique
slug: knuth-optimization
name: Knuth's optimization
aliases:
- Knuth's DP speedup
- Knuth-Yao speedup
- quadrangle inequality speedup
area: techniques/dynamic-programming
level: advanced
summary: Restrict the split point of an interval DP to a monotone range, cutting O(n^3) time to O(n^2).
prereqs: [interval-dp, monge-property]
see_also: [interval-dp, optimal-binary-search-tree, monge-property, divide-and-conquer-optimization, matrix-chain-multiplication, row-minima-of-totally-monotone-matrices]
sources:
  - paper: doi:10.1007/BF00264289
    title: Donald E. Knuth, Optimum binary search trees, Acta Informatica 1(1), 14-25, 1971
    locator: the monotonicity of the roots and the O(n^2) algorithm for optimum binary search trees
  - paper: doi:10.1145/800141.804691
    title: F. Frances Yao, Efficient dynamic programming using quadrangle inequalities, Proceedings of the 12th ACM STOC, 429-435, 1980
    locator: the lemma that the quadrangle inequality of w carries over to c, and the theorem on the monotone split points
  - paper: doi:10.1137/0603055
    title: F. Frances Yao, Speed-up in dynamic programming, SIAM Journal on Algebraic and Discrete Methods 3(4), 532-540, 1982
    locator: the extension of the quadrangle inequality method to more general recurrences
  - paper: doi:10.1145/1644015.1644032
    title: Wolfgang Bein, Mordecai J. Golin, Lawrence L. Larmore and Yan Zhang, The Knuth-Yao quadrangle-inequality speedup is a consequence of total monotonicity, ACM Transactions on Algorithms 6(1), 2009
    locator: the main theorem
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 6.2.2, optimum binary search trees
---

Knuth's optimization speeds up an [interval dynamic program](/interval-dp/) of the form $c(i, j) = w(i, j) + \min_{i < k \le j} \bigl( c(i, k-1) + c(k, j) \bigr)$ from $O(n^3)$ to $O(n^2)$ time. When the cost $w$ satisfies the quadrangle inequality of the [Monge property](/monge-property/) and grows with the interval, the best split point $K(i, j)$ is monotone: $K(i, j-1) \le K(i, j) \le K(i+1, j)$. So the search for $K(i, j)$ only scans that range, and the ranges of one diagonal of the table add up to $O(n)$. Knuth found the bound for [optimal binary search trees](/optimal-binary-search-tree/) in 1971, and Yao proved it in 1980 for every cost with these two properties.

## In plain words

Many interval problems choose, for each stretch of items, the best place to split it in two. The plain method tries every split of every stretch, which is slow for long inputs.

Often the best split moves in a regular way. If you add one item at the right end of a stretch, the best split does not move to the left. If you remove one item from the left end, the best split does not move to the left either. So the best split of a stretch lies between the best splits of the two stretches that are one item shorter. Those were computed earlier. You only try the splits between them.

For each length, these small ranges fit together end to end, so the total work for one length is about the number of items, not its square.

## When it applies

Look for these signals.

- The recurrence has exactly the form above: a cost $c(i, j)$ of an interval, a split point $k$, the two sub-intervals $[i, k-1]$ and $[k, j]$, and an added cost $w(i, j)$ that depends on the interval only, not on $k$.
- $w$ satisfies the **quadrangle inequality**: $w(i, j) + w(i', j') \le w(i, j') + w(i', j)$ for all $i \le i' \le j \le j'$.
- $w$ is **monotone on intervals**: $w(i', j) \le w(i, j')$ for all $i \le i' \le j \le j'$. A wider interval never costs less.
- Typical costs that have both properties: the sum of nonnegative weights in the interval, and $g(\text{sum})$ for a convex nondecreasing $g$, such as the square of the sum.

Matrix-chain multiplication does not fit, because its added cost $p_{i-1} p_k p_j$ depends on the split $k$.

## The template

Let $c(i, i) = 0$ for $0 \le i \le n$, and for $i < j$

$$c(i, j) = w(i, j) + \min_{i < k \le j} \bigl( c(i, k-1) + c(k, j) \bigr).$$

Let $K(i, j)$ be the largest $k$ that attains the minimum. The holes are the cost $w$ (which must pass the two tests above) and the base values. The program fills the table by increasing length $d = j - i$.

```pseudo id=main
KNUTH-DP(w, n)
L1  for i ← 0 to n do c[i, i] ← 0
L2  for i ← 0 to n − 1 do c[i, i+1] ← w(i, i+1), K[i, i+1] ← i + 1     ▷ only one split
L3  for d ← 2 to n do
L4      for i ← 0 to n − d do
L5          j ← i + d
L6          best ← +∞
L7          for k ← K[i, j−1] to K[i+1, j] do                       ▷ the plain method uses i + 1 to j
L8              if c[i, k−1] + c[k, j] ≤ best then best ← c[i, k−1] + c[k, j], K[i, j] ← k
L9          c[i, j] ← w(i, j) + best                                   ▷ hole: the cost w
L10 return c[0, n]
```

The test $\le$ in line L8 keeps the largest minimizing $k$, which is the $K$ of the theorem. Both bounds of line L7 belong to intervals of length $d - 1$, which are already filled.

### Why the range of line L7 is right

Write $c_k(i, j) = w(i, j) + c(i, k-1) + c(k, j)$. Assume the quadrangle inequality (QI) and the monotonicity (M) of $w$.

**Lemma 1 (Yao).** $c$ satisfies the quadrangle inequality: $c(i, j) + c(i', j') \le c(i, j') + c(i', j)$ for $i \le i' \le j \le j'$.

*Proof.* By strong induction on $j' - i$. If $i = i'$ or $j = j'$, both sides are equal. So let $i < i'$ and $j < j'$.

*Case $i' = j$.* We need $c(i, j) + c(j, j') \le c(i, j')$, since $c(j, j) = 0$. Let $z = K(i, j')$, so $c(i, j') = c_z(i, j')$.
If $z \le j$, then $z$ is a valid split of $(i, j)$, so $c(i, j) \le w(i, j) + c(i, z-1) + c(z, j)$. By the hypothesis on $z \le j \le j \le j'$, which has a smaller span, $c(z, j) + c(j, j') \le c(z, j')$. By (M), $w(i, j) \le w(i, j')$. Adding gives $c(i, j) + c(j, j') \le c_z(i, j') = c(i, j')$.
If $z > j$, then $z$ is a valid split of $(j, j')$, so $c(j, j') \le w(j, j') + c(j, z-1) + c(z, j')$. By the hypothesis on $i \le j \le j \le z - 1$, $c(i, j) + c(j, z-1) \le c(i, z-1)$. By (M), $w(j, j') \le w(i, j')$. Adding gives the claim.

*Case $i' < j$.* Let $y = K(i', j)$ and $z = K(i, j')$.
If $z \le y$, then $i < z \le j$ and $i' < y \le j'$, so $z$ is a valid split of $(i, j)$ and $y$ of $(i', j')$. Then
$c(i, j) + c(i', j') \le c_z(i, j) + c_y(i', j')$. By (QI) of $w$, $w(i, j) + w(i', j') \le w(i, j') + w(i', j)$. By the hypothesis on $z \le y \le j \le j'$, $c(z, j) + c(y, j') \le c(y, j) + c(z, j')$. Adding these gives $c(i, j) + c(i', j') \le c_z(i, j') + c_y(i', j) = c(i, j') + c(i', j)$.
If $z > y$, then $i < y \le j$ and $i' < z \le j'$, so $y$ is a valid split of $(i, j)$ and $z$ of $(i', j')$. In the same way, use (QI) of $w$ and the hypothesis on $i \le i' \le y - 1 \le z - 1$, which gives $c(i, y-1) + c(i', z-1) \le c(i', y-1) + c(i, z-1)$. Adding gives $c(i, j) + c(i', j') \le c_y(i', j) + c_z(i, j') = c(i', j) + c(i, j')$.

Each use of the hypothesis has a span less than $j' - i$. $\square$

**Lemma 2 (Knuth, Yao).** For $i < j$ with $j + 1 \le n$: $K(i, j) \le K(i, j+1) \le K(i+1, j+1)$.

*Proof.* Left inequality. Let $k = K(i, j)$ and take $i < k' < k$. Lemma 1 on $k' \le k \le j \le j + 1$ gives $c(k', j) + c(k, j+1) \le c(k, j) + c(k', j+1)$. Add $w(i, j) + w(i, j+1) + c(i, k'-1) + c(i, k-1)$ to both sides: $c_{k'}(i, j) + c_k(i, j+1) \le c_k(i, j) + c_{k'}(i, j+1)$. Since $k$ is optimal for $(i, j)$, $c_k(i, j) \le c_{k'}(i, j)$, so $c_k(i, j+1) \le c_{k'}(i, j+1)$. So if some $k' < k$ were optimal for $(i, j+1)$, then $k$ would be optimal too, and the largest optimal split is at least $k$.

Right inequality. Let $k = K(i+1, j+1)$, so $k \ge i + 2$, and take $k < k' \le j + 1$. Since $k$ is the largest optimal split of $(i+1, j+1)$, $c_{k'}(i+1, j+1) > c_k(i+1, j+1)$. Lemma 1 on $i \le i+1 \le k-1 \le k'-1$ gives $c(i, k-1) + c(i+1, k'-1) \le c(i+1, k-1) + c(i, k'-1)$. Add $w(i, j+1) + w(i+1, j+1) + c(k, j+1) + c(k', j+1)$: $c_k(i, j+1) + c_{k'}(i+1, j+1) \le c_k(i+1, j+1) + c_{k'}(i, j+1)$. With the strict inequality above, $c_k(i, j+1) < c_{k'}(i, j+1)$. So no $k' > k$ is optimal for $(i, j+1)$. $\square$

### The cost

For a fixed length $d \ge 2$, line L7 for the interval $(i, i+d)$ scans $K(i+1, i+d) - K(i, i+d-1) + 1$ values. The sum over $i = 0, \ldots, n-d$ telescopes:

$$\sum_{i=0}^{n-d} \bigl( K(i+1, i+d) - K(i, i+d-1) + 1 \bigr) = K(n-d+1, n) - K(0, d-1) + (n - d + 1) \le 2n.$$

There are $n - 1$ lengths, so the total is $O(n^2)$ time, against $\Theta(n^3)$ for the plain scan. The table $K$ adds $O(n^2)$ space.

## Classic examples

### Merging adjacent piles

Piles with weights $q_0, \ldots, q_n$ stand in a row. A step merges two adjacent piles into one, at a cost equal to the total weight of the new pile. Find the least total cost to merge all the piles. Let $c(i, j)$ be the cost for the piles $i$ to $j$. The last merge joins the piles $i$ to $k - 1$ and $k$ to $j$, for some $i < k \le j$, and costs $w(i, j) = q_i + \cdots + q_j$. This $w$ is the template cost. It satisfies the quadrangle inequality with equality, since $w(i, j) + w(i', j') = w(i, j') + w(i', j)$ for $i \le i' \le j \le j'$, and it is monotone because the weights are nonnegative.

For $q = (3, 1, 4, 1, 5, 9)$, so $n = 5$, the tables are:

| $c(i, j)$ | $j = 1$ | $j = 2$ | $j = 3$ | $j = 4$ | $j = 5$ |
|---|---|---|---|---|---|
| $i = 0$ | 4 | 12 | 18 | 32 | 55 |
| $i = 1$ | | 5 | 11 | 22 | 42 |
| $i = 2$ | | | 5 | 15 | 34 |
| $i = 3$ | | | | 6 | 21 |
| $i = 4$ | | | | | 14 |

| $K(i, j)$ | $j = 1$ | $j = 2$ | $j = 3$ | $j = 4$ | $j = 5$ |
|---|---|---|---|---|---|
| $i = 0$ | 1 | 2 | 2 | 4 | 5 |
| $i = 1$ | | 2 | 3 | 4 | 5 |
| $i = 2$ | | | 3 | 4 | 5 |
| $i = 3$ | | | | 4 | 5 |
| $i = 4$ | | | | | 5 |

Each row of $K$ is nondecreasing from left to right and each column is nondecreasing from top to bottom, as Lemma 2 says. For the full interval, line L7 tries only $k \in \{K(0, 4), \ldots, K(1, 5)\} = \{4, 5\}$, instead of the 5 values 1 to 5. The least cost is 55: merge the piles 0 to 3 at a cost of 18, merge the result with 5 and then with 9.

On 101 random piles with weights from 1 to 100, line L8 runs 10,298 times with the restricted range, against 171,700 times with the full range, and both give the same answer.

### Optimal binary search trees

For keys $k_1 < \cdots < k_n$ with search probabilities, the cost of an [optimal binary search tree](/optimal-binary-search-tree/) on the keys $i+1, \ldots, j$ has the template form with the root $k$ as the split and $w(i, j)$ the total probability of the keys and gaps in the range. This $w$ is a sum of nonnegative terms, so both conditions hold. Knuth proved the monotonicity of the roots for this case and got an $O(n^2)$ algorithm, against the $O(n^3)$ of CLRS Section 14.5.

### Other uses

- Optimal alphabetic codes and Hu-Tucker style trees, which are the merging of adjacent piles under another name.
- Some breaking of a string or a stick at given points, where the cost of a cut is the length of the piece being cut. The cost is the sum of the lengths, which satisfies both conditions.
- Costs $g(q_i + \cdots + q_j)$ for convex nondecreasing $g$ and nonnegative $q$.

## Variations

- **Yao's general form.** Yao's 1982 paper extends the quadrangle inequality method to other recurrences, including some where the minimum is taken over more general sets of splits.
- **Layered problems.** For $f_t(j) = \min_{k < j} (f_{t-1}(k) + w(k, j))$, the same inequality gives monotone split points along $j$. The tools there are the [divide and conquer optimization](/divide-and-conquer-optimization/) and, for linear time per layer, the [SMAWK algorithm](/smawk-algorithm/). Knuth's form also works for layered problems, with the bound $K(t-1, j) \le K(t, j) \le K(t, j+1)$, and gives $O(n^2)$ for all layers together.
- **Total monotonicity.** Bein, Golin, Larmore and Zhang showed that the Knuth-Yao speedup can be derived from the total monotonicity of suitable matrices, which links it to the [row minima problem](/row-minima-of-totally-monotone-matrices/).

## Pitfalls

- **Using it without the quadrangle inequality.** Merge adjacent piles with the cost of a merge equal to the square root of the new pile. This cost is monotone but concave, and the quadrangle inequality fails. For the piles $(9, 2, 7, 2, 6)$, the plain recurrence gives about 15.051, and the restricted range gives about 15.117, which is wrong.
- **Using it without monotonicity.** Let $w(i, j)$ be the least weight among the piles $i$ to $j$. For the piles $(8, 5, 6, 4)$, the plain recurrence gives 12, and the restricted range gives 13. Here $K(0, 2) = 2$ but $K(0, 3) = 1$, so the split points are not monotone.
- **An added cost that depends on $k$.** In matrix-chain multiplication the term $p_{i-1} p_k p_j$ depends on the split, and the theorem does not apply. Use the plain $O(n^3)$ loop, or the $O(n \log n)$ method of Hu and Shing for that problem.
- **Index conventions.** The theorem is about the form with sub-intervals $[i, k-1]$ and $[k, j]$. For the common form $dp[i][j] = \min_{i \le m < j} (dp[i][m] + dp[m+1][j]) + w(i, j)$, put $k = m + 1$. Mixing the two shifts the bounds of line L7 by one and can make the range miss the optimum.
- **The tie rule.** Lemma 2 is proved for the largest optimal split. Taking the smallest also works with the mirror argument, but the choice must be the same in all cells.

## Exercises

1. Prove that $w(i, j) = (q_i + \cdots + q_j)^2$ with $q \ge 0$ satisfies the quadrangle inequality and the monotonicity condition.
2. Show that for the merging of adjacent piles, the bound of line L7 is never empty: $K(i, j-1) \le K(i+1, j)$ for $j - i \ge 2$.
   <details><summary>Hint</summary>Apply Lemma 2 to $(i, j-1)$ and then to $(i+1, j)$, or use $K(i, j-1) \le K(i, j) \le K(i+1, j)$.</details>
3. Find a cost $w$ that satisfies the quadrangle inequality but not the monotonicity, and an input where the restricted range gives a wrong answer.
4. Write the $O(n^2)$ program for optimal binary search trees in the form of CLRS Section 14.5, and state the bounds on $root[i, j]$ that replace line L7.

## References
