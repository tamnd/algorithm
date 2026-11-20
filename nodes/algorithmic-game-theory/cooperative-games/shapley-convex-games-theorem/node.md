---
tag: 5VHCK9
kind: theorem
slug: shapley-convex-games-theorem
name: "Shapley's theorem on convex games"
aliases:
- core of convex games
area: algorithmic-game-theory/cooperative-games
level: advanced
summary: "The core of a convex game is not empty, it is the convex hull of the marginal vectors, each marginal vector is a corner, and the Shapley value lies in it."
prereqs: [convex-game, core-of-a-cooperative-game, shapley-value]
see_also: [bondareva-shapley-theorem, bankruptcy-problem, airport-game, submodular-function, matroid, extreme-point, polyhedron, nucleolus]
sources:
  - paper: doi:10.1007/BF01753431
    title: "Lloyd S. Shapley, Cores of convex games, International Journal of Game Theory 1(1) (1971), 11-26"
    locator: the theorem that the core of a convex game is the convex hull of the marginal vectors and contains the Shapley value
  - paper: "Tatsuro Ichiishi, Super-modularity, applications to convex games and to the greedy algorithm for LP, Journal of Economic Theory 25(2) (1981), 283-286"
    locator: the converse, that a game whose core contains all marginal vectors is convex
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Section 17.7 (the core of a convex game) and Section 18.7 (the Shapley value of a convex game is in the core)
  - book: "Bezalel Peleg and Peter Sudholter, Introduction to the Theory of Cooperative Games, 2nd edition, Theory and Decision Library C 34, Springer, 2007"
    title: Introduction to the Theory of Cooperative Games
    locator: Chapter 3, The core (pp. 27-49), convex games
---

Shapley's theorem on convex games describes the [core](/core-of-a-cooperative-game/) of a [convex game](/convex-game/) completely. Pick an order of the players, let them join one at a time, and pay each one what it adds to the coalition already there; this marginal vector is a corner of the core, and every corner arises in this way. So the core is not empty, and the [Shapley value](/shapley-value/), which averages the marginal vectors, is in it. The [Bondareva-Shapley theorem](/bondareva-shapley-theorem/) says when a general game has a nonempty core; this theorem says what the core looks like for convex games, and its proof needs no LP solver.

## Statement

Let $(N, v)$ be a TU game with $N = \{1, \ldots, n\}$. For an order $\sigma = (\sigma_1, \ldots, \sigma_n)$ of the players, let $S_k = \{\sigma_1, \ldots, \sigma_k\}$, with $S_0 = \emptyset$. The marginal vector $m^\sigma$ pays each player what it adds when it joins:

$$m^\sigma_{\sigma_k} = v(S_k) - v(S_{k-1}), \qquad k = 1, \ldots, n.$$

The Weber set is the convex hull of the $n!$ marginal vectors.

**Theorem (Shapley 1971).** If $v$ is convex, then

1. every marginal vector is in the core;
2. the core is the Weber set, and every marginal vector is a corner of the core;
3. the Shapley value $\phi(v) = \frac{1}{n!} \sum_\sigma m^\sigma$ is in the core.

**Converse (Ichiishi 1981).** If every marginal vector of $v$ is in the core, then $v$ is convex. So a game is convex exactly when its core equals its Weber set.

### Example

For the [bankruptcy problem](/bankruptcy-problem/) with claims $(100, 200, 300)$ and estate 200, the game has $v(\{2, 3\}) = 100$, $v(N) = 200$, and value 0 for every other coalition. It is convex. The six orders give four distinct marginal vectors:

| order | marginal vector |
|---|---|
| 1, 2, 3 and 2, 1, 3 | $(0, 0, 200)$ |
| 1, 3, 2 and 3, 1, 2 | $(0, 200, 0)$ |
| 2, 3, 1 | $(100, 0, 100)$ |
| 3, 2, 1 | $(100, 100, 0)$ |

These are the four corners of the core, which is the set of award vectors $x$ with $0 \le x_1 \le 100$, $x_2, x_3 \ge 0$ and $x_1 + x_2 + x_3 = 200$. The average of the six marginal vectors is $(100/3, 250/3, 250/3)$, the Shapley value, which is the random arrival rule.

## In plain words

Let the players arrive one at a time, and pay each one the extra value that it brings to the group already there. In a convex game a player brings more to a larger group. So any group that thinks of leaving was paid at least what it could make alone: each member arrived after some of the others, and so was paid at least what it adds to the part of the group before it. This makes every such payment a stable split. Different arrival orders give different stable splits, and these are exactly the corners of the set of all stable splits. Averaging over all orders gives the Shapley value, which is then stable too. If the game is not convex, some arrival order pays a group too little.

## Proof

Write $x(S) = \sum_{i \in S} x_i$. Convexity will be used in its marginal form: $v(P \cup \{i\}) - v(P) \ge v(Q \cup \{i\}) - v(Q)$ whenever $Q \subseteq P \subseteq N \setminus \{i\}$ (see [convex game](/convex-game/) for the equivalence).

**Part 1.** Let $x = m^\sigma$. The sum telescopes: $x(N) = \sum_k (v(S_k) - v(S_{k-1})) = v(N)$. Take a nonempty $S$ and list its members in the order of $\sigma$ as $i_1, \ldots, i_s$. Let $Q_j = \{i_1, \ldots, i_{j-1}\}$, and let $P_j$ be the set of players before $i_j$ in $\sigma$. Then $Q_j \subseteq P_j$, so

$$x_{i_j} = v(P_j \cup \{i_j\}) - v(P_j) \ge v(Q_j \cup \{i_j\}) - v(Q_j).$$

Summing over $j$, the right side telescopes to $v(S) - v(\emptyset) = v(S)$. So $x(S) \ge v(S)$, and $x$ is in the core.

**Part 2.** Fix $c \in \mathbb{R}^n$ and an order $\sigma$ with $c_{\sigma_1} \ge c_{\sigma_2} \ge \cdots \ge c_{\sigma_n}$. For every $x$ with $x(N) = v(N)$, summation by parts gives

$$c \cdot x = \sum_{k=1}^{n-1} (c_{\sigma_k} - c_{\sigma_{k+1}})\, x(S_k) + c_{\sigma_n} x(N).$$

If $x$ is in the core, then $x(S_k) \ge v(S_k)$, and the coefficients $c_{\sigma_k} - c_{\sigma_{k+1}}$ are at least 0. The marginal vector has $m^\sigma(S_k) = v(S_k)$ for every $k$, so

$$c \cdot x \ge \sum_{k=1}^{n-1} (c_{\sigma_k} - c_{\sigma_{k+1}})\, v(S_k) + c_{\sigma_n} v(N) = c \cdot m^\sigma.$$

With Part 1, $m^\sigma$ minimizes $c \cdot x$ over the core.

The core is a bounded [polyhedron](/polyhedron/), and it is not empty by Part 1, so it is the convex hull of its corners. Let $p$ be a corner. Some $c$ has $p$ as its only minimizer over the core; take $\sigma$ for this $c$ as above. Then $m^\sigma$ is also a minimizer, so $p = m^\sigma$. So every corner is a marginal vector, and the core is contained in the Weber set. The core is convex and contains every marginal vector by Part 1, so it contains the Weber set. The two sets are equal.

Each marginal vector $m^\sigma$ is a corner: it lies in the core and makes the $n$ constraints $x(S_k) \ge v(S_k)$, $k = 1, \ldots, n$, tight. The indicator vectors of the chain $S_1 \subset S_2 \subset \cdots \subset S_n$ are linearly independent, so $m^\sigma$ is the only point with these $n$ equalities. A point of a polyhedron at which $n$ linearly independent constraints are tight is an [extreme point](/extreme-point/).

**Part 3.** $\phi(v)$ is the average of the marginal vectors, a convex combination of core points, and the core is convex.

**Converse.** Let every marginal vector be in the core, and take $S, T \subseteq N$. Choose an order that lists $S \cap T$ first, then $S \setminus T$, then $T \setminus S$, then the rest. Then $S \cap T$, $S$ and $S \cup T$ are initial segments, so $m(S \cap T) = v(S \cap T)$, $m(S) = v(S)$ and $m(T \setminus S) = v(S \cup T) - v(S)$. The core constraint for $T$ gives

$$v(T) \le m(T) = m(S \cap T) + m(T \setminus S) = v(S \cap T) + v(S \cup T) - v(S),$$

which is convexity. $\square$

## Consequences

- **Convex games are balanced and totally balanced.** Every subgame of a convex game is convex, so every subgame has a nonempty core.
- **The Shapley value is stable.** For bankruptcy games, the random arrival rule gives an award vector. For the [airport game](/airport-game/), the Shapley value cost shares are in the core of the cost game.
- **The nucleolus is in the core.** Since the core is not empty, the [nucleolus](/nucleolus/) is in it.
- **Greedy optimization over the core.** Part 2 is a greedy algorithm: sort $c$ in decreasing order and take one marginal vector, with $n$ values of $v$ and $O(n \log n)$ time. It is Edmonds' greedy algorithm for polymatroids and [matroids](/matroid/) applied to the supermodular function $v$.
- **Core membership.** Testing whether $x$ is in the core asks whether $\min_S (x(S) - v(S)) \ge 0$. For convex $v$ the function $S \mapsto x(S) - v(S)$ is a [submodular function](/submodular-function/), so the test is submodular function minimization, which runs in polynomial time with an oracle for $v$.
- **The corners of a strictly convex game.** If the convexity inequality is strict whenever neither of $S$ and $T$ contains the other, then the $n!$ marginal vectors are distinct, and the core has exactly $n!$ corners.

## Tightness

- **Without convexity, Part 1 fails.** In the glove game, $v(\{1, 2\}) = v(\{1, 3\}) = v(N) = 1$ and 0 otherwise. The order $1, 2, 3$ gives $(0, 1, 0)$, and the coalition $\{1, 3\}$ gets $0 < 1$. The core is the single point $(1, 0, 0)$, the Weber set is larger, and the Shapley value $(2/3, 1/6, 1/6)$ is not in the core.
- **The converse shows that convexity is exactly the right condition.** A game whose marginal vectors all lie in the core is convex. So no weaker condition gives Part 1.
- **The core can have fewer than $n!$ corners.** Different orders can give the same marginal vector, as in the bankruptcy example, where six orders give four corners. An additive game has only one marginal vector, and its core is one point.

## History

Lloyd Shapley defined convex games and proved the theorem in 1971, in the first issue of the International Journal of Game Theory. The same paper shows that the core of a convex game is a stable set in the sense of von Neumann and Morgenstern. Tatsuro Ichiishi published the converse in 1981, with the link to the greedy algorithm for linear programs over polymatroids, which Jack Edmonds had studied in 1970.

## References
