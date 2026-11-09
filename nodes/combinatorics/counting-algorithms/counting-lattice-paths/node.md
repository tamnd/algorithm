---
tag: WEMZ6K
kind: problem
slug: counting-lattice-paths
name: Counting lattice paths
aliases:
- monotone lattice paths
- grid path counting
- counting monotone paths
area: combinatorics/counting-algorithms
level: core
summary: Counting monotone paths between grid points, possibly avoiding a boundary.
prereqs: [binomial-coefficient]
see_also: [grid-paths-with-obstacles, reflection-principle, catalan-numbers, ballot-theorem, lindstrom-gessel-viennot-lemma, binomial-coefficient-computation, lucas-theorem, transfer-matrix-method]
sources:
  - book: isbn:9780471257080
    title: William Feller, An Introduction to Probability Theory and Its Applications, Volume 1, third edition, Wiley, 1968
    locator: Chapter III, Fluctuations in Coin Tossing and Random Walks (Section 1, paths and the reflection principle)
  - book: isbn:9781107427747
    title: Richard P. Stanley, Catalan Numbers, Cambridge University Press, 2015
    locator: Chapter 1, Basic properties (lattice paths below the diagonal)
  - book: isbn:9783662572641
    title: Martin Aigner and Günter M. Ziegler, Proofs from THE BOOK, sixth edition, Springer, 2018
    locator: Chapter Lattice paths and determinants
  - paper: doi:10.1016/0001-8708(85)90121-5
    title: Ira Gessel and Gérard Viennot, Binomial determinants, paths, and hook length formulae, Advances in Mathematics 58 (1985), 300-321
    locator: the whole paper (families of nonintersecting lattice paths)
---

Counting lattice paths asks how many paths of unit steps join two points of the integer grid, usually with steps east and north only, and often with a boundary, a forbidden set of points or several paths that must not touch. Without constraints the answer is a [binomial coefficient](/binomial-coefficient/), and many classic numbers are counts of constrained paths: the Catalan, ballot, Delannoy, Schröder and Motzkin numbers. The tools are a dynamic-programming table, the [reflection principle](/reflection-principle/), inclusion-exclusion over forbidden points, and the [Lindström-Gessel-Viennot lemma](/lindstrom-gessel-viennot-lemma/) for families of paths.

## In plain words

A city has a square street grid. You walk from one corner to another and may go only east or north. How many different routes are there? Each route is a list of east and north moves, and you only choose where the north moves go, so the answer is a count of choices. The problem becomes harder when some crossings are closed, when you must stay on one side of a diagonal street, or when several people walk at once and may never meet. Each of these has its own counting trick, and a table that adds the counts of the two neighbours always works for small grids.

## Definition

**Notation.** $n, k, a, b$ are non-negative integers, $C(n, k)$ is the binomial coefficient, with $C(n, k) = 0$ for $k < 0$ or $k > n$, and $[n] = \{1, \ldots, n\}$. A *step* $E$ is $(1, 0)$ and a step $N$ is $(0, 1)$. A *monotone lattice path* from $(x_0, y_0)$ to $(x_1, y_1)$ is a sequence of points of $\mathbb{Z}^2$ from the first to the second in which each point is the previous one plus $E$ or $N$. $N$ (without a step meaning) also denotes the count that the problem outputs.

**Input:** the two endpoints, and in the variants a set of forbidden points, a boundary line, other step sets, a family of $k$ start and end points, or a modulus.

**Output:** the number of paths that satisfy the constraints, exactly or modulo a given integer.

**Theorem 1 (free paths).** The number of monotone paths from $(0, 0)$ to $(a, b)$ is $C(a + b, a)$.

*Proof.* A path has exactly $a$ steps $E$ and $b$ steps $N$, in some order, so it is a word of length $a + b$ with $a$ letters $E$. The path is fixed by the set of positions of the $E$ steps, which is any subset of $[a + b]$ of size $a$. $\square$

**Theorem 2 (below the diagonal).** For $a \ge b$, the number of monotone paths from $(0, 0)$ to $(a, b)$ that never go above the line $y = x$ is

$$C(a + b, b) - C(a + b, b - 1) = \frac{a - b + 1}{a + 1}\, C(a + b, b).$$

*Proof.* A path that goes above the line touches $y = x + 1$. Reflect the part before its first touch in this line, which swaps $E$ and $N$ in that part. The start $(0, 0)$ goes to $(-1, 1)$, so the result is a free path from $(-1, 1)$ to $(a, b)$, and every such path crosses $y = x + 1$ because it starts above it and ends below it. Reflecting back before the first touch inverts the map. There are $C(a + b, a + 1) = C(a + b, b - 1)$ free paths from $(-1, 1)$ to $(a, b)$. The second form follows from $C(a + b, b - 1) = \frac{b}{a + 1} C(a + b, b)$. $\square$

For $a = b = n$ this is the Catalan number $C_n = C(2n, n)/(n + 1)$, see [Catalan numbers](/catalan-numbers/). The same proof with the line $y = x + t + 1$ shows that the paths from $(0, 0)$ to $(a, b)$ that stay weakly below $y = x + t$, for $t \ge 0$ and $b \le a + t$, number $C(a + b, b) - C(a + b, b - t - 1)$.

**Theorem 3 (forbidden points).** Let $p_1, \ldots, p_m$ be forbidden points, sorted so that $p_i \le p_j$ coordinatewise implies $i \le j$, and let $p_{m+1}$ be the target. For each $j$, let $g_j$ be the number of paths from $(0, 0)$ to $p_j$ that avoid $p_1, \ldots, p_{j-1}$. Then

$$g_j = P((0, 0), p_j) - \sum_{i < j,\ p_i \le p_j} g_i\, P(p_i, p_j),$$

where $P(u, v)$ is the free count of Theorem 1 between $u$ and $v$, and $g_{m+1}$ is the answer.

*Proof.* Split the free paths to $p_j$ by the first forbidden point they visit. If it is $p_i$, the path is a path to $p_i$ that avoids the earlier points, followed by any free path from $p_i$ to $p_j$. A path can visit $p_i$ before $p_j$ only if $p_i \le p_j$, and then $i < j$ by the sort order. $\square$

## Variants

- **Paths below a line.** Theorem 2 and its shifted form. For a line through $(0, 0)$ and $(a, b)$ with $\gcd(a, b) = 1$, the paths from $(0, 0)$ to $(a, b)$ that stay weakly below the line number $C(a + b, a)/(a + b)$, by the [cycle lemma](/cycle-lemma/). For $(a, b) = (5, 3)$ this is $56/8 = 7$.
- **Paths in a strip.** Paths that must stay between two parallel lines: apply the reflection in both lines repeatedly, which gives an alternating sum of binomial coefficients, see the [reflection principle](/reflection-principle/).
- **Other step sets.** With steps $E$, $N$ and the diagonal $(1, 1)$, the paths from $(0, 0)$ to $(n, n)$ are counted by the central Delannoy numbers $D_n = \sum_k C(n, k)^2 2^k$: $1, 3, 13, 63, 321, 1683, 8989$ (OEIS A001850). If they also stay below $y = x$, the counts are the large Schröder numbers $1, 2, 6, 22, 90, 394, 1806$ (OEIS A006318). Paths of length $n$ with steps $(1, 1)$, $(1, 0)$ and $(1, -1)$ from height $0$ to height $0$ that never go below $0$ are counted by the Motzkin numbers $1, 1, 2, 4, 9, 21, 51, 127, 323, 835$ (OEIS A001006).
- **Higher dimensions.** Monotone paths in $\mathbb{Z}^d$ from the origin to $(a_1, \ldots, a_d)$ number the multinomial coefficient $(a_1 + \cdots + a_d)!/(a_1! \cdots a_d!)$. For $(n, n, n)$ this is $1, 6, 90, 1680, 34650, 756756$ (OEIS A006480).
- **Nonintersecting families.** Count $k$-tuples of paths from $u_1, \ldots, u_k$ to $v_1, \ldots, v_k$ that share no point. When every such tuple joins $u_i$ to $v_i$, the count is $\det [P(u_i, v_j)]$ by the [Lindström-Gessel-Viennot lemma](/lindstrom-gessel-viennot-lemma/).

## Examples

**Example 1.** From $(0, 0)$ to $(3, 2)$ there are $C(5, 2) = 10$ paths. To $(n, n)$ there are $C(2n, n)$: $1, 2, 6, 20, 70, 252, 924, 3432, 12870, 48620, 184756$ for $n = 0, \ldots, 10$ (OEIS A000984).

**Example 2: the ballot table.** The counts of Theorem 2 for $0 \le b \le a \le 4$, with row $a$ and column $b$:

| $a$ \ $b$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 1 | | | | |
| 1 | 1 | 1 | | | |
| 2 | 1 | 2 | 2 | | |
| 3 | 1 | 3 | 5 | 5 | |
| 4 | 1 | 4 | 9 | 14 | 14 |

This is Catalan's triangle (OEIS A009766), and the diagonal $1, 1, 2, 5, 14$ gives the Catalan numbers (OEIS A000108). Each entry is the sum of the entry above and the entry to the left, because the last step is $E$ or $N$.

**Example 3: one forbidden point.** From $(0, 0)$ to $(4, 4)$ there are $C(8, 4) = 70$ paths. Those through $(2, 2)$ number $C(4, 2) \cdot C(4, 2) = 36$, so $70 - 36 = 34$ avoid it.

## Known algorithms

**Closed forms.** Theorems 1 and 2 reduce the free and the diagonal cases to one or two binomial coefficients, see [binomial coefficient computation](/binomial-coefficient-computation/). Exactly, $C(a + b, a) \le 2^{a + b}$ has at most $a + b$ bits, and the product formula costs $O(\min(a, b))$ multiplications and divisions of numbers with $O(a + b)$ bits. Modulo a prime $p > a + b$, use a table of factorials and inverse factorials, built in $O(a + b)$ operations, and then $O(1)$ operations per binomial. For a small prime $p$ and huge coordinates, use [Lucas's theorem](/lucas-theorem/), which costs $O(\log_p (a + b))$ binomials of numbers below $p$.

**Table.** For any set of forbidden points in an $a \times b$ box, fill $T(x, y) = T(x - 1, y) + T(x, y - 1)$, with $T = 0$ at forbidden points and $T(0, 0) = 1$. This uses $O(ab)$ additions. The values have at most $a + b$ bits, so the exact bit cost is $O(ab(a + b))$, and modulo a word-size prime it is $O(ab)$ word operations. This is the method of [counting paths on grids with obstacles](/grid-paths-with-obstacles/), and it works for any step set by summing over the allowed last steps.

**Few forbidden points in a huge grid.** Theorem 3 uses $O(m^2)$ binomials after a sort, so $O(m^2 + a + b)$ operations modulo a prime $p > a + b$. It does not depend on the area $ab$.

**Boundaries.** For one line use Theorem 2. For two parallel lines use the alternating sum of the reflection principle, with $O((a + b)/w)$ terms for a strip of width $w$. For a narrow strip a [transfer matrix](/transfer-matrix-method/) with $w + 1$ states is an alternative.

**Families of paths.** Build the $k \times k$ matrix of free counts and take its [determinant](/determinant/), with $O(k^3)$ operations modulo a prime, or with the [Bareiss algorithm](/bareiss-algorithm/) for exact integers.

## Bounds

- **Size of the answer.** The free count to $(n, n)$ satisfies $\frac{4^n}{2n + 1} \le C(2n, n) \le 4^n$, since it is the largest of the $2n + 1$ terms of $(1 + 1)^{2n} = 4^n$. So the exact answer can have $\Theta(a + b)$ bits, and any exact algorithm needs $\Omega(a + b)$ bit operations to write it.
- **Asymptotics.** $C(2n, n) \sim 4^n / \sqrt{\pi n}$ and $C_n \sim 4^n / (\sqrt{\pi}\, n^{3/2})$. So the paths that stay below the diagonal are a fraction $\sim 1/n$ of all paths.
- **The table is optimal for general obstacles.** With forbidden points given as a bitmap of the $a \times b$ box, an algorithm must read all $ab$ bits in the worst case, so the $O(ab)$ additions of the table cannot be beaten by more than the cost of one addition.

## Reductions

- Monotone paths from $(0, 0)$ to $(a, b)$ correspond one to one to binary words with $a$ letters $E$ and $b$ letters $N$, and to subsets of size $a$ of $[a + b]$.
- Paths that stay below the diagonal correspond to [Dyck words](/dyck-word/) and to [balanced parentheses](/balanced-parentheses/): read $E$ as "(" and $N$ as ")". See [counting balanced bracket sequences](/counting-balanced-bracket-sequences/).
- A grid with forbidden points is a directed acyclic graph, and counting its paths is a dynamic program on the topological order.
- Nonintersecting families reduce to a determinant by the Lindström-Gessel-Viennot lemma, and plane partitions and rhombus tilings of a hexagon reduce to such families.

## Applications

- **Random walks.** A simple random walk of $n$ steps is a lattice path, and probabilities of events such as "the walk never goes below 0" are counts of paths divided by $2^n$. The [ballot theorem](/ballot-theorem/) is one such count.
- **Dynamic programming on grids.** Many exercises count routes in a grid with walls, which is the table above.
- **Enumeration of other objects.** Binary trees, triangulations, Young tableaux with two rows and plane partitions are counted by translating them into lattice paths.

## References
