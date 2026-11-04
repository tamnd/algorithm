---
tag: W4XPW3
kind: problem
slug: optimal-text-wrapping
name: Optimal text wrapping
aliases:
- word wrap
- minimum raggedness
area: techniques/dynamic-programming
level: advanced
summary: Break a sequence of words into lines so that a total penalty such as raggedness is minimal.
prereqs: [printing-neatly, monge-property, dp-on-dag]
see_also: [printing-neatly, knuth-plass-line-breaking, monge-property, row-minima-of-totally-monotone-matrices, smawk-algorithm, greedy-stays-ahead, aliens-trick, text-segmentation]
sources:
  - paper: doi:10.1137/0216043
    title: D. S. Hirschberg and L. L. Larmore, The least weight subsequence problem, SIAM Journal on Computing 16(4), 628-638, 1987
    locator: the definition of the least weight subsequence problem, line breaking as the main example, and the O(n log n) algorithm for concave weights
  - paper: doi:10.1016/0196-6774(88)90032-6
    title: Robert Wilber, The concave least-weight subsequence problem revisited, Journal of Algorithms 9(3), 418-425, 1988
    locator: the O(n) algorithm with matrix searching
  - paper: doi:10.1016/0020-0190(90)90215-j
    title: Zvi Galil and Kunsoo Park, A linear-time algorithm for concave one-dimensional dynamic programming, Information Processing Letters 33(6), 309-311, 1990
    locator: the whole note
  - paper: doi:10.1137/0403009
    title: Maria M. Klawe and Daniel J. Kleitman, An almost linear time algorithm for generalized matrix searching, SIAM Journal on Discrete Mathematics 3(1), 81-97, 1990
    locator: the application to the convex least weight subsequence problem
  - paper: doi:10.1002/spe.4380111102
    title: Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software, Practice and Experience 11(11), 1119-1184, 1981
    locator: the comparison of first-fit and total-fit line breaking
---

Optimal text wrapping is the general problem of breaking a sequence of words into lines of width at most $W$ so that the sum of a cost per line is least, where the cost of a line depends on the words it holds, usually through its slack (the free space at its end). It is the main example of the **least weight subsequence** problem of Hirschberg and Larmore: choose break points $0 = b_0 < b_1 < \cdots < b_t = n$ to minimize $\sum_s w(b_{s-1}, b_s)$. The dynamic program $F(j) = \min_{i < j} \bigl( F(i) + w(i, j) \bigr)$ takes $O(n^2)$ time for any $w$. For the usual costs, a convex function of the slack, $w$ has the [Monge property](/monge-property/), and the time drops to $O(n \log n)$ (Hirschberg and Larmore) and then to $O(n)$ (Wilber; Galil and Park). With cost 1 per line, the greedy rule is optimal. This page treats the general problem. The CLRS instance with cubed slack is [printing neatly](/printing-neatly/), and the TeX method with stretchable spaces is the [Knuth-Plass algorithm](/knuth-plass-line-breaking/).

## In plain words

Breaking a paragraph into lines is a choice of where each line ends. A bad line is one with a large gap at its end, and you add up a penalty over the lines. Different penalties give different problems: count the lines, add the squares of the gaps, or add their cubes.

If you only count lines, the simple rule "put as many words as fit, then start a new line" is the best. For penalties that grow faster than the gap, that rule can leave one very bad line, and a better layout spreads the gaps.

The best layout can always be found by trying every possible last line and reusing the best layout of the words before it. For the usual penalties, a special property of the costs means you do not have to try every last line, and the work becomes linear in the number of words.

## Definition

**Input.** Word widths $l_1, \ldots, l_n > 0$, a space width (taken as 1), a line width $W \ge \max_k l_k$, and a line cost $w(i, j) \in \mathbb{R} \cup \{\infty\}$ for the line that holds words $i + 1, \ldots, j$, for $0 \le i < j \le n$.

**Slack.** With $Q_k = \sum_{t \le k} (l_t + 1)$, the line of words $i + 1, \ldots, j$ has length $Q_j - Q_i - 1$ and slack $s(i, j) = W + 1 - (Q_j - Q_i)$. It fits when $s(i, j) \ge 0$.

**Typical costs.** $w(i, j) = f(s(i, j))$ if the line fits and $\infty$ if not, with:

- $f \equiv 1$: fewest lines;
- $f(s) = s^2$: minimum raggedness;
- $f(s) = s^3$: [printing neatly](/printing-neatly/);

and often $w(i, n) = 0$ for a last line that fits.

**Output.** Break points $0 = b_0 < \cdots < b_t = n$ that minimize $\sum_{s=1}^{t} w(b_{s-1}, b_s)$.

## Variants

- **Fewest lines.** Solved by the greedy rule, as shown below.
- **Exactly $k$ lines**, or a balanced layout with a given number of lines. A table over (lines, words) solves it in $O(kn^2)$ time, or $O(kn \log n)$ with the [divide and conquer optimization](/divide-and-conquer-optimization/); for Monge costs the [Aliens trick](/aliens-trick/) removes the factor $k$.
- **Worst line.** Minimize the largest line cost instead of the sum. The same recurrence with $\max$ in place of $+$ solves it in $O(n^2)$ time.
- **Typesetting.** Spaces that stretch and shrink, hyphenation points with penalties, and costs that depend on adjacent lines. This is the box, glue and penalty model of the [Knuth-Plass algorithm](/knuth-plass-line-breaking/).
- **Word-free segmentation.** If the words are not given and the problem is to find them, it is [text segmentation](/text-segmentation/), with the same suffix structure.

## Examples

Words `aaa bb cc ddddd` with $W = 6$, the squared slack and a free last line:

| layout | slacks | fewest lines cost | squared cost |
|---|---|---|---|
| `aaa bb` / `cc` / `ddddd` (greedy) | 0, 4, free | 3 | 16 |
| `aaa` / `bb cc` / `ddddd` | 3, 1, free | 3 | 10 |

Both layouts use 3 lines, the fewest possible, but only the second is optimal for the squared cost. With the cubed cost the two layouts cost 64 and 28.

A longer case is the sentence "Dynamic programming finds the best way to break a paragraph into lines" with $W = 21$ and squared slack. The greedy layout `Dynamic programming` / `finds the best way to` / `break a paragraph` / `into lines` costs $4 + 0 + 16 = 20$; the optimum `Dynamic programming` / `finds the best way` / `to break a paragraph` / `into lines` costs $4 + 9 + 1 = 14$.

## Known algorithms

**Greedy is optimal for the fewest lines.** The greedy rule puts as many words as fit on each line. Let greedy end its lines at $g_1 < g_2 < \cdots$ and some layout end its lines at $b_1 < b_2 < \cdots$. Then $g_s \ge b_s$ for all $s$, by induction: $g_1 \ge b_1$ because greedy takes the most words that fit; and if $g_{s-1} \ge b_{s-1}$, then either $g_{s-1} \ge b_s$ already, or the words $g_{s-1} + 1, \ldots, b_s$ are a suffix of the words $b_{s-1} + 1, \ldots, b_s$, which fit on one line, so they fit too, and greedy reaches at least $b_s$. So greedy reaches word $n$ no later than any layout. This is a [greedy stays ahead](/greedy-stays-ahead/) argument, and it takes $O(n)$ time.

**Dynamic program, $O(n^2)$.** With $F(0) = 0$,

$$F(j) = \min_{0 \le i < j} \bigl( F(i) + w(i, j) \bigr),$$

and the answer is $F(n)$. The last line of an optimal layout of words $1, \ldots, j$ holds words $i + 1, \ldots, j$ for some $i$, and the lines before it are an optimal layout of words $1, \ldots, i$. This is a shortest path in a [DAG](/dp-on-dag/) on $0, \ldots, n$. Only lines that fit matter, and a line holds at most $\lceil W/2 \rceil$ words, so the time is $O(n \min(n, W))$.

**The costs are Monge.** Let $f$ be convex on $s \ge 0$ and let $w(i, j) = h(Q_j - Q_i)$ with $h(x) = f(W + 1 - x)$ for $x \le W + 1$ and $h(x) = \infty$ otherwise. Then $h$ is convex as a function with values in $\mathbb{R} \cup \{\infty\}$. For $i < i' \le j < j'$, put $x_1 = Q_j - Q_{i'}$, $x_2 = Q_j - Q_i$, $x_3 = Q_{j'} - Q_{i'}$ and $x_4 = Q_{j'} - Q_i$. Then $x_1 \le x_2, x_3 \le x_4$ and $x_1 + x_4 = x_2 + x_3$, and convexity of $h$ gives

$$w(i, j) + w(i', j') = h(x_2) + h(x_3) \le h(x_1) + h(x_4) = w(i', j) + w(i, j'),$$

which is the quadrangle inequality. If also $f$ is nondecreasing, a free last line keeps the inequality: for $j' = n$ and a last line $i + 1, \ldots, n$ that fits, the lines $(i, j)$ and $(i', j)$ fit, and $w(i, j) = f(s(i, j)) \le f(s(i', j)) = w(i', j)$ because $s(i, j) \le s(i', j)$. So all the costs above are Monge. A check of all quadruples on 3000 random instances with squares and cubes finds no violation.

**Concave least weight subsequence, $O(n \log n)$.** Hirschberg and Larmore call a weight with the quadrangle inequality *concave*. For such weights, if a candidate $i'$ beats an earlier candidate $i$ at some $j$, it beats it at all later $j$. So the candidates that can still win form a queue, each one best on an interval of future positions, and a new candidate is placed with a binary search. Each $F(j)$ then costs $O(\log n)$ amortized.

**Linear time.** The matrix $F(i) + w(i, j)$ is [totally monotone](/row-minima-of-totally-monotone-matrices/), but its entries in column $j$ depend on $F$ values that are not yet known, so [SMAWK](/smawk-algorithm/) cannot be applied to the whole matrix at once. Wilber gave an $O(n)$ algorithm that applies matrix searching to blocks in the right order, and Galil and Park gave a simpler $O(n)$ algorithm.

**Convex weights.** For weights with the reverse inequality, Klawe and Kleitman gave an almost linear algorithm. Line costs that are convex in the slack fall into the concave case above, not this one.

## Bounds

- $O(n)$ for fewest lines, by greedy.
- $O(n \min(n, W))$ for any line cost, by the dynamic program.
- $O(n \log n)$ and $O(n)$ for costs that are convex functions of the slack, by the concave least weight subsequence algorithms.
- $\Omega(n)$, since every word width must be read.

## Reductions

- **To a shortest path** in the DAG on the break points $0, \ldots, n$ with edge weights $w(i, j)$.
- **To matrix searching.** The row minima of a Monge matrix, see [Monge property](/monge-property/) and [row minima of totally monotone matrices](/row-minima-of-totally-monotone-matrices/), with the online issue above.
- **Special cases.** [Printing neatly](/printing-neatly/) is $f(s) = s^3$ with a free last line. The Knuth-Plass model reduces to this problem when spaces cannot stretch or shrink and there are no hyphens.

## Applications

- **Text formatters and editors.** Many tools use the greedy rule. TeX uses the total-fit method of Knuth and Plass, who compare it with the first-fit (greedy) method and show that it gives more even spacing.
- **Typesetting of narrow columns**, where bad breaks are more visible and more costly.
- **Teaching.** A clear case where greedy is optimal for one cost and not for another on the same input, and an entry point to the Monge speedups.

## References
