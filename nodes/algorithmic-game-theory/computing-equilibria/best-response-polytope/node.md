---
tag: 6Z6QR3
kind: definition
slug: best-response-polytope
name: Best response polytope
aliases:
- best response polyhedron
area: algorithmic-game-theory/computing-equilibria
level: advanced
summary: A polytope for each player of a bimatrix game whose labeled vertices encode the mixed strategies and the best responses to them.
prereqs: [bimatrix-game, mixed-strategy, best-response, polyhedron]
see_also: [lemke-howson-algorithm, support-enumeration, nash-equilibrium-computation, linear-complementarity-problem, vertex-enumeration, indifference-principle, savani-von-stengel-theorem, basic-feasible-solution]
sources:
  - book: isbn:9780521872829
    title: Noam Nisan, Tim Roughgarden, Éva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007
    locator: Chapter 3 (Bernhard von Stengel, Equilibrium computation for two-player games in strategic and extensive form), best response polyhedra and polytopes, labels, and the 3 x 2 example game
  - book: isbn:9780521899437
    title: Yoav Shoham and Kevin Leyton-Brown, Multiagent Systems, Algorithmic, Game-Theoretic, and Logical Foundations, Cambridge University Press, 2009
    locator: Chapter 4, the Lemke-Howson algorithm and its geometric form with labeled polytopes
  - paper: doi:10.1137/0112033
    title: "C. E. Lemke and J. T. Howson, Jr., Equilibrium points of bimatrix games, Journal of the Society for Industrial and Applied Mathematics 12(2) (1964), 413-423"
    locator: the equilibrium problem as a complementary pivoting problem on two polyhedra
---

The best response polytopes of a two-player game $(A, B)$ are two polytopes, one for each player, whose points are scaled mixed strategies and whose facets say "this pure strategy is not played" or "this pure strategy of the other player is a best response". A Nash equilibrium is then a pair of vertices, one in each polytope, that together carry all the labels. This page defines the polytopes and the labels. The [Lemke-Howson algorithm](/lemke-howson-algorithm/) is a path-following method on them, [support enumeration](/support-enumeration/) and [vertex enumeration](/vertex-enumeration/) are search methods that can be read on them, and the [Nash equilibrium computation](/nash-equilibrium-computation/) page covers the problem and its complexity.

## Definition

Let $(A, B)$ be an $m \times n$ [bimatrix game](/bimatrix-game/): the row player has $m$ pure strategies and payoff matrix $A$, the column player has $n$ and payoff matrix $B$. Here $m$ and $n$ count strategies, not players. Assume that $A$ and $B^{\mathsf T}$ are nonnegative and have no zero column; adding the same constant to all entries of a matrix does not change the [best responses](/best-response/), so a shift makes all entries positive.

The **best response polytopes** are

$$P = \{x \in \mathbb{R}^m : x \ge 0,\ B^{\mathsf T} x \le \mathbf 1\}, \qquad Q = \{y \in \mathbb{R}^n : A y \le \mathbf 1,\ y \ge 0\}.$$

Under the assumption they are bounded, so they are polytopes, and both contain $0$.

**Labels.** Number the pure strategies of the row player $1, \ldots, m$ and those of the column player $m + 1, \ldots, m + n$. A point $x \in P$ has

- label $i$ if $x_i = 0$, and
- label $m + j$ if $(B^{\mathsf T} x)_j = 1$.

A point $y \in Q$ has

- label $i$ if $(A y)_i = 1$, and
- label $m + j$ if $y_j = 0$.

So each of the $m + n$ inequalities of $P$, and of $Q$, has a label, and a point carries the labels of the inequalities that are tight at it. A pair $(x, y) \in P \times Q$ is **completely labeled** if each of the labels $1, \ldots, m + n$ is a label of $x$ or of $y$. The [Lemke-Howson algorithm](/lemke-howson-algorithm/) page numbers the same labels from 0.

**Meaning.** For $x \in P$ with $x \ne 0$, the [mixed strategy](/mixed-strategy/) $\bar x = x / \sum_i x_i$ gives the column player the payoffs $B^{\mathsf T} \bar x$. A label $m + j$ of $x$ means that column $j$ is a best response to $\bar x$, because the constraint $(B^{\mathsf T} x)_j \le 1$ is tight and no column can give more than 1. The column player's best payoff is $1 / \sum_i x_i$ when $x$ has at least one label $m + j$. The same holds for $y \in Q$ and the row player.

**Best response condition.** A pair of mixed strategies is a [Nash equilibrium](/nash-equilibrium/) if and only if every pure strategy that one player uses with positive probability is a best response to the strategy of the other. In terms of labels:

> **Theorem.** A pair $(x, y) \in P \times Q$ other than $(0, 0)$ is completely labeled if and only if $(x / \sum_i x_i,\ y / \sum_j y_j)$ is a Nash equilibrium of $(A, B)$.

A label $i$ means that row $i$ is unused (at $x$) or a best response (at $y$), and the same for a label $m + j$. A completely labeled pair with $x \ne 0$ has $y \ne 0$, because a nonzero $x$ uses a row whose label must then come from $y$. Each equilibrium is obtained this way from one pair: scale $\bar x$ by the inverse of the column player's equilibrium payoff and $\bar y$ by the inverse of the row player's.

**Nondegeneracy.** The game is nondegenerate if no point of $P$ has more than $m$ labels and no point of $Q$ has more than $n$. Equivalently, no mixed strategy with $k$ pure strategies in its support has more than $k$ pure best responses. Then every vertex of $P$ has exactly $m$ labels and every vertex of $Q$ exactly $n$, and in a completely labeled pair both points are vertices and each label appears exactly once.

## Examples and non-examples

- **A $3 \times 2$ game.** This is the game of von Stengel's chapter in NRTV, $A = \begin{pmatrix} 3 & 3 \\ 2 & 5 \\ 0 & 6 \end{pmatrix}$ and $B = \begin{pmatrix} 3 & 2 \\ 2 & 6 \\ 3 & 1 \end{pmatrix}$, with labels 1, 2, 3 for the rows and 4, 5 for the columns. $A$ has no zero column and $B^{\mathsf T}$ has none either, so no shift is needed. The vertices and their labels are:

| vertex of $P$ | labels | | vertex of $Q$ | labels |
|---|---|---|---|---|
| $(0, 0, 0)$ | 1, 2, 3 | | $(0, 0)$ | 4, 5 |
| $(1/3, 0, 0)$ | 2, 3, 4 | | $(1/3, 0)$ | 1, 5 |
| $(2/7, 1/14, 0)$ | 3, 4, 5 | | $(2/9, 1/9)$ | 1, 2 |
| $(0, 1/6, 0)$ | 1, 3, 5 | | $(1/12, 1/6)$ | 2, 3 |
| $(0, 1/8, 1/4)$ | 1, 4, 5 | | $(0, 1/6)$ | 3, 4 |
| $(0, 0, 1/3)$ | 1, 2, 4 | | | |

The game is nondegenerate: each vertex of $P$ has 3 labels and each vertex of $Q$ has 2. The completely labeled pairs are $(0, 0)$ and three more:

| $x \in P$ | $y \in Q$ | equilibrium after scaling | payoffs (row, column) |
|---|---|---|---|
| $(1/3, 0, 0)$ | $(1/3, 0)$ | $((1, 0, 0), (1, 0))$ | $3, 3$ |
| $(2/7, 1/14, 0)$ | $(2/9, 1/9)$ | $((4/5, 1/5, 0), (2/3, 1/3))$ | $3, 14/5$ |
| $(0, 1/8, 1/4)$ | $(1/12, 1/6)$ | $((0, 1/3, 2/3), (1/3, 2/3))$ | $4, 8/3$ |

The payoffs follow the meaning above. For $x = (2/7, 1/14, 0)$, the column player gets $1 / (2/7 + 1/14) = 14/5$. For $y = (2/9, 1/9)$, the row player gets $1 / (1/3) = 3$.

- **Not completely labeled.** The pair $x = (0, 1/6, 0)$, $y = (0, 1/6)$ has the labels $\{1, 3, 5\} \cup \{3, 4\}$, so label 2 is missing and label 3 appears twice. Row 2 is played at $x$ but is not a best response to $y = (0, 1)$, where row 3 gives 6 and row 2 gives 5. Pairs with exactly one missing label and one double label are the points of the Lemke-Howson paths.
- **The artificial pair.** $(0, 0)$ is completely labeled but is not an equilibrium, since it cannot be scaled. It is the start of every Lemke-Howson path.
- **A degenerate game.** For $A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}$ and $B = \begin{pmatrix} 1 & 1 \\ 0 & 3 \end{pmatrix}$, the vertex $x = (1, 0)$ of $P$ has the labels 2, 3 and 4: the pure strategy row 1 has both columns as best responses. That is 3 labels on a vertex of a 2-dimensional polytope, so the game is degenerate. The equilibria $((1, 0), y)$ with $y = (t, 1 - t)$ and $1/2 \le t \le 1$ form a segment, and in $Q$ only its ends are vertices.
- **Unbounded without the shift.** For the matching pennies matrix $A = \begin{pmatrix} 1 & -1 \\ -1 & 1 \end{pmatrix}$, the set $\{y \ge 0 : A y \le \mathbf 1\}$ contains $(t, t)$ for every $t \ge 0$, so it is not a polytope. After adding 2 to all entries it is bounded, with the same labels on its vertices.

## Related definitions

- **Best response polyhedron.** The form with an explicit payoff variable: $\bar P = \{(x, v) \in \mathbb{R}^m \times \mathbb{R} : x \ge 0,\ \mathbf 1^{\mathsf T} x = 1,\ B^{\mathsf T} x \le v \mathbf 1\}$, and $\bar Q$ in the same way. Its points are mixed strategies $x$ with an upper bound $v$ on the other player's payoff, and its labels are defined in the same way. When all payoffs are positive, the map $(x, v) \mapsto x / v$ sends $\bar P$ one-to-one onto $P \setminus \{0\}$ and keeps the labels. It is a projective map, so it also keeps the faces and the vertices, and the unbounded direction of $\bar P$, in which $v$ grows, goes to the vertex $0$ of $P$. This is the step from the polyhedron to the polytope.
- **Complementarity.** The conditions "label $i$ at $x$ or at $y$" are $x_i (1 - (A y)_i) = 0$ and $y_j (1 - (B^{\mathsf T} x)_j) = 0$. With the slack variables they form a [linear complementarity problem](/linear-complementarity-problem/), and a vertex of $P$ or $Q$ is a [basic feasible solution](/basic-feasible-solution/) of its system.
- **Indifference.** At a vertex $y$ of $Q$, the tight constraints $(A y)_i = 1$ say that the rows $i$ all give the same payoff against $y$. These are the equations of the [indifference principle](/indifference-principle/).

## References
