---
tag: BREBA5
kind: problem
slug: least-weight-subsequence
name: Least weight subsequence problem
aliases:
- least weight subsequence
area: strings/text-processing-and-typesetting
level: advanced
summary: Choose indices 0 = i0 < ... < ik = n minimizing the sum of w(i_j, i_j+1); line breaking with a concave cost is the main example.
prereqs: [dp-on-dag, monge-property]
see_also: [optimal-text-wrapping, printing-neatly, knuth-plass-line-breaking, dag-shortest-paths, smawk-algorithm, row-minima-of-totally-monotone-matrices, aliens-trick, convex-hull-trick]
sources:
  - paper: doi:10.1137/0216043
    title: "D. S. Hirschberg and L. L. Larmore, The least weight subsequence problem, SIAM Journal on Computing 16(4), 628-638, 1987"
    locator: "the definition of the problem, the concave condition, the O(n log n) algorithm and line breaking as the main application"
  - paper: doi:10.1016/0196-6774(88)90032-6
    title: "Robert Wilber, The concave least-weight subsequence problem revisited, Journal of Algorithms 9(3), 418-425, 1988"
    locator: "the O(n) algorithm for concave weights"
  - paper: doi:10.1016/0020-0190(90)90215-J
    title: "Zvi Galil and Kunsoo Park, A linear-time algorithm for concave one-dimensional dynamic programming, Information Processing Letters 33(6), 309-311, 1990"
    locator: "the simpler O(n) algorithm"
  - paper: doi:10.1137/0403009
    title: "Maria M. Klawe and Daniel J. Kleitman, An almost linear time algorithm for generalized matrix searching, SIAM Journal on Discrete Mathematics 3(1), 81-97, 1990"
    locator: "the application to the case with the reverse inequality"
  - paper: doi:10.1002/spe.4380111102
    title: "Donald E. Knuth and Michael F. Plass, Breaking paragraphs into lines, Software: Practice and Experience 11(11), 1119-1184, 1981"
    locator: "the line breaking problem with demerits that motivates the abstract problem"
---

The least weight subsequence problem asks for the cheapest way to go from position 0 to position $n$ by jumps forward, when a jump from $i$ to $j$ costs a given weight $w(i, j)$. It is a shortest path in a DAG whose nodes are $0, \ldots, n$ and whose edges are all pairs $i < j$, so the plain dynamic program takes $O(n^2)$ time. Hirschberg and Larmore named it in 1987, with line breaking as the main example: the positions are the places between words, and $w(i, j)$ is the cost of a line with the words $i + 1$ to $j$. When the weight satisfies the quadrangle inequality, which they called concave, the time drops to $O(n \log n)$ and then to $O(n)$.

## In plain words

Think of a row of stepping stones numbered 0 to $n$. You stand on stone 0 and must reach stone $n$, always stepping forward, and each step from one stone to a later one has a price that you can look up. You want the cheapest walk.

For each stone, the cheapest walk to it ends with one last step, from some earlier stone. So the cheapest price of stone $j$ is the smallest of "cheapest price of $i$ plus the price of the step from $i$ to $j$" over all earlier $i$. Working from left to right, this takes about $n^2/2$ lookups.

When long steps get expensive fast enough, in the precise sense of the inequality below, most earlier stones can be ruled out without looking, and far fewer lookups are needed.

## Definition

The input is an integer $n \ge 1$ and a weight $w(i, j) \in \mathbb{R} \cup \{+\infty\}$ for each pair $0 \le i < j \le n$, given by a procedure that returns any $w(i, j)$ in $O(1)$ time. A *subsequence* is a list $0 = i_0 < i_1 < \cdots < i_k = n$, for any $k \ge 1$, and its weight is $\sum_{t=1}^{k} w(i_{t-1}, i_t)$. The problem is to find a subsequence of least weight.

The values

$$F(0) = 0, \qquad F(j) = \min_{0 \le i < j} \bigl( F(i) + w(i, j) \bigr) \quad (1 \le j \le n)$$

are the least weights of the subsequences that end at $j$, and $F(n)$ is the answer. The index $i$ that gives the minimum for $j$ is the last break before $j$, and following these indices back from $n$ gives an optimal subsequence.

**The concave case.** Hirschberg and Larmore call $w$ *concave* when

$$w(i, j) + w(i', j') \le w(i, j') + w(i', j) \qquad \text{for all } 0 \le i \le i' < j \le j' \le n.$$

This is the quadrangle inequality, the inequality of the [Monge property](/monge-property/) for the array $w$. Some authors call the same condition convex, because $w(i, j) = f(S_j - S_i)$ satisfies it when $f$ is a convex function, so the reader must check which inequality a paper means. The condition with $\ge$ is then usually called the *convex* case.

## Variants

- **Concave weights.** The inequality above. This is the case of line breaking, and it has $O(n)$ algorithms.
- **Convex weights.** The reverse inequality. It has algorithms of almost linear time, but no simple queue method of the kind that works for concave weights.
- **Exactly $k$ parts.** Ask for a subsequence with a given number $k$ of jumps. The dynamic program gets a second index, and for concave weights a Lagrangian method, the [aliens trick](/aliens-trick/), often removes it.
- **States.** The weight of a jump may depend on more than its two ends, for example on the jump before it. Then the nodes must carry this state, and the problem is a shortest path in a larger DAG. The demerits of the [Knuth-Plass algorithm](/knuth-plass-line-breaking/) are of this kind: the fitness classes and the extra cost for two hyphens in a row depend on the line before, so they are not a function $w(i, j)$ of two breaks, and the fast methods for the concave case do not apply to them directly.
- **Online.** The weights $w(i, j)$ are known only when $j$ is reached, as when text arrives one word at a time.

## Examples

**A check value.** Take $n = 10$ and $w(i, j) = (j - i - 3)^2$, a cost that wants every jump to have length 3. The weight is $f(j - i)$ with $f$ convex, so it is concave in the sense above. The dynamic program gives

| $j$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| $F(j)$ | 0 | 4 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |

and the subsequence 0, 3, 6, 10 has weight $0 + 0 + 1 = 1$. The tests of the pages on the [Hirschberg-Larmore algorithm](/hirschberg-larmore-algorithm/) and on [Wilber's algorithm](/wilber-algorithm/) use this instance.

**Line breaking with rigid spaces.** Let the words have widths $a_1, \ldots, a_n$, let each space be 1 wide, and let $S_j = a_1 + \cdots + a_j$. The line with words $i + 1$ to $j$ has width $(S_j + j) - (S_i + i) - 1$. Put $w(i, j) = (l - \text{width})^3$ when the width is at most $l$, and $+\infty$ when it is larger. This is [printing neatly](/printing-neatly/) without the free last line. It is $f(T_j - T_i)$ for $T_j = S_j + j$ and a convex $f$ with values in $\mathbb{R} \cup \{+\infty\}$, so it is concave.

**Fewest lines.** With $w(i, j) = 1$ when the line fits and $+\infty$ otherwise, the answer is the fewest lines. This weight is also concave, and [greedy line breaking](/greedy-line-breaking/) solves it in linear time without a dynamic program.

**Non-example: the last line free.** Many layouts do not charge for the empty space of the last line, so $w(i, n) = 0$ for every $i$ whose last line fits. With $w(i, j) = (j - i - 3)^2$ for $j < n$ and $w(i, n) = 0$, take $i = 0$, $i' = 3$, $j = 6$ and $j' = n = 10$: the left side is $w(0, 6) + w(3, 10) = 9 + 0$ and the right side is $w(0, 10) + w(3, 6) = 0 + 0$, so the inequality fails. The fix is to solve the problem for $j < n$ with the concave weight and then take $F(n) = \min_i \bigl( F(i) + w(i, n) \bigr)$ in one more $O(n)$ step.

**Non-example: capped badness.** The badness of TeX, $\min(100 |r|^3, 10000)$, is not concave in general, because of the cap. For words of widths 2, 5 and 1, glue of width 2 with stretch 1 and shrink 1, and $l = 18$: $w(0, 2) + w(1, 3) = 10000 + 10000$, but $w(0, 3) + w(1, 2) = 2700 + 10000$.

## Known algorithms

| algorithm | weights | time | notes |
|---|---|---|---|
| dynamic program ([DP on a DAG](/dp-on-dag/)) | any | $O(n^2)$ | all pairs |
| [Hirschberg-Larmore](/hirschberg-larmore-algorithm/) | concave | $O(n \log n)$ | a queue of candidates and binary search; finds $F(1), F(2), \ldots$ in order |
| [Wilber](/wilber-algorithm/) | concave | $O(n)$ | [SMAWK](/smawk-algorithm/) on blocks; guesses values ahead and checks them |
| Galil and Park | concave | $O(n)$ | a simpler linear method |
| Klawe and Kleitman | convex | $O(n \alpha(n))$ | $\alpha$ is the inverse Ackermann function |
| [greedy](/greedy-line-breaking/) | 1 or $+\infty$ by fit | $O(n)$ | fewest lines only |

The fast methods need each weight in $O(1)$ time, which for line breaking means prefix sums of the widths. They also need finite weights or care with $+\infty$: ties between infinite values can break the matrix searching of Wilber's method, and a large finite penalty for a line that is too long avoids this.

## Bounds

- **General weights.** In the model where $w$ is read through the procedure, every exact algorithm must read all $n(n+1)/2$ weights in the worst case. If it skips $w(i, j)$, an adversary can make that weight small enough that the only optimal subsequence uses the jump from $i$ to $j$.
- **Concave weights.** $O(n)$ time and weight reads by Wilber's method. This is optimal when all the values $F(1), \ldots, F(n)$ are wanted, since they are $n$ numbers.
- **Space.** $\Theta(n)$ for the values $F$ and the back pointers.

## Reductions

- **To shortest paths.** The problem is the shortest path from 0 to $n$ in the DAG with an edge $i \to j$ of weight $w(i, j)$ for each $i < j$ ([shortest paths in a DAG](/dag-shortest-paths/)). The nodes are already in topological order.
- **To row minima.** Put $B(j, i) = F(i) + w(i, j)$ for $i < j$. In the concave case this array is totally monotone, so the minimum of each row could be found by [row minima of totally monotone matrices](/row-minima-of-totally-monotone-matrices/). But the entries of column $i$ need $F(i)$, which is known only after row $i$ is solved, so the matrix is not given in advance. Wilber's method solves this by working on blocks whose columns are already known, and by checking its guesses.
- **From line breaking.** [Optimal text wrapping](/optimal-text-wrapping/), [printing neatly](/printing-neatly/) and the fewest-lines problem reduce to this problem, with the positions between words as indices.

## Applications

- **Line breaking.** The main example. The fast algorithms apply when the cost of a line depends only on its two ends and is a convex function of its width, as for rigid spaces and ragged-right text.
- **Splitting a sequence into blocks.** Cutting a list of records into pages, a signal into pieces, or a text into segments ([text segmentation](/text-segmentation/)) with a cost per piece is the same problem.
- **Dynamic programs with a convex cost of the distance.** Many recurrences of the form $F(j) = \min_i F(i) + f(x_j - x_i)$ with a convex $f$ are concave instances; the [convex hull trick](/convex-hull-trick/) solves the special case where the cost is linear in $j$ for each fixed $i$.

## References
