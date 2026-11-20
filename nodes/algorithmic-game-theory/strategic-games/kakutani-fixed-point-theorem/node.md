---
tag: 0QER4Q
kind: theorem
slug: kakutani-fixed-point-theorem
name: Kakutani fixed-point theorem
aliases:
- "Kakutani's theorem"
area: algorithmic-game-theory/strategic-games
level: advanced
summary: "Every set-valued map from a compact convex set to itself with nonempty convex values and a closed graph (equivalently, upper hemicontinuous with closed values) has a fixed point."
prereqs: [brouwer-fixed-point-theorem, convex-set]
see_also: [brouwer-fixed-point-theorem, nash-existence-theorem, best-response, minimax-theorem, arrow-debreu-existence-theorem, nash-equilibrium, competitive-equilibrium, ppad]
sources:
  - paper: doi:10.1215/S0012-7094-41-00838-4
    title: "Shizuo Kakutani, A generalization of Brouwer's fixed point theorem, Duke Mathematical Journal 8(3) (1941), 457-459"
    locator: the theorem for upper semicontinuous point-to-set maps of a simplex to nonempty closed convex subsets, the corollary for bounded closed convex sets, the proof by Brouwer's theorem on piecewise linear approximations, and the application to von Neumann's minimax theorem
  - paper: doi:10.1073/pnas.36.1.48
    title: "John F. Nash, Equilibrium points in n-person games, Proceedings of the National Academy of Sciences 36(1) (1950), 48-49"
    locator: the existence of equilibrium points by Kakutani's theorem applied to the best-response correspondence
  - paper: doi:10.2307/1969529
    title: "John Nash, Non-cooperative games, Annals of Mathematics 54(2) (1951), 286-295"
    locator: the later proof that uses the Brouwer theorem instead
  - paper: "Kenneth J. Arrow and Gerard Debreu, Existence of an equilibrium for a competitive economy, Econometrica 22(3) (1954), 265-290"
    title: Existence of an equilibrium for a competitive economy
    locator: the existence of competitive equilibrium through an abstract economy whose equilibrium is a fixed point of a set-valued map
  - paper: "Irving L. Glicksberg, A further generalization of the Kakutani fixed point theorem, with application to Nash equilibrium points, Proceedings of the American Mathematical Society 3(1) (1952), 170-174"
    title: A further generalization of the Kakutani fixed point theorem, with application to Nash equilibrium points
    locator: the extension to compact convex sets in locally convex spaces and to games with continuous strategy sets
---

The Kakutani fixed-point theorem extends the [Brouwer fixed-point theorem](/brouwer-fixed-point-theorem/) from functions to set-valued maps: if each point $x$ of a compact convex set is sent to a nonempty convex set $F(x)$ of points, and the graph of $F$ is closed, then some $x$ lies in its own image $F(x)$. Shizuo Kakutani proved it in 1941 and used it to prove the [minimax theorem](/minimax-theorem/). It fits game theory because [best responses](/best-response/) form exactly such a map, and John Nash used it in 1950 for the first proof that equilibria exist ([Nash's theorem](/nash-existence-theorem/)); his 1951 paper used Brouwer's theorem instead.

## Statement

A *set-valued map* (correspondence) $F$ from $K$ to $K$ assigns to each $x \in K$ a subset $F(x) \subseteq K$. Its *graph* is $\{(x, y) : y \in F(x)\} \subseteq K \times K$. The map is *upper hemicontinuous* at $x$ if for every open set $V \supseteq F(x)$ there is a neighbourhood $U$ of $x$ with $F(x') \subseteq V$ for all $x' \in U \cap K$. A *fixed point* of $F$ is a point $x$ with $x \in F(x)$.

**Theorem (Kakutani 1941).** Let $K \subseteq \mathbb{R}^n$ be nonempty, compact and convex, and let $F$ be a set-valued map from $K$ to $K$ such that

1. $F(x)$ is nonempty and convex for every $x \in K$, and
2. the graph of $F$ is closed.

Then $F$ has a fixed point.

**Closed graph and upper hemicontinuity.** Since $K$ is compact, condition 2 holds if and only if $F$ is upper hemicontinuous and every $F(x)$ is closed. If the graph is closed, every $F(x)$ is closed; if $F$ were not upper hemicontinuous at $x$, there would be an open $V \supseteq F(x)$ and points $x_k \to x$ with $y_k \in F(x_k) \setminus V$, and a subsequence $y_k \to y$ with $y \notin V$, while the closed graph gives $y \in F(x)$, a contradiction. Conversely, let $F$ be upper hemicontinuous with closed values, and let $(x_k, y_k) \to (x, y)$ with $y_k \in F(x_k)$. If $y \notin F(x)$, the compact set $F(x)$ has distance $3\delta > 0$ from $y$; the open $\delta$-neighbourhood $V$ of $F(x)$ contains $F(x_k)$ for large $k$, so $y_k \in V$ and $y$ is within $\delta$ of $F(x)$, a contradiction. Kakutani stated the theorem with upper semicontinuity and closed values; most texts in game theory state it with the closed graph.

When every $F(x)$ is a single point $\{f(x)\}$, the closed graph condition says that $f$ is continuous, and the theorem is Brouwer's theorem.

## In plain words

Suppose each point of a solid, rounded region points to a whole patch of allowed targets inside the region, instead of to one target. Each patch must be in one piece with no dents, and the patches must change without sudden shrinking or jumping away as the point moves. Then some point is among its own allowed targets. In a game, a point is a choice for every player, and its patch is the set of choices in which each player picks a best reply to the others. A point that is in its own patch is a choice where nobody wants to change: an equilibrium. The theorem shows such a point exists but does not say how to find it.

## Proof

**Step 1: the simplex.** Let $K = \Delta$ be an $n$-simplex. Let $T_1, T_2, \ldots$ be triangulations of $\Delta$ whose largest cell diameter tends to 0, for example iterated barycentric subdivisions. For each $k$ define $f_k: \Delta \to \Delta$ as follows: at each vertex $v$ of $T_k$ choose a point $f_k(v) \in F(v)$, and on each cell extend $f_k$ affinely, so that $f_k\big(\sum_j \lambda_j v^j\big) = \sum_j \lambda_j f_k(v^j)$ for a cell with vertices $v^0, \ldots, v^n$ and barycentric weights $\lambda_j \ge 0$, $\sum_j \lambda_j = 1$. The two definitions agree on shared faces, so $f_k$ is continuous, and it maps into $\Delta$ because $\Delta$ is convex. By Brouwer's theorem it has a fixed point $x_k$.

Let $x_k$ lie in the cell with vertices $v^{k,0}, \ldots, v^{k,n}$, with weights $\lambda^{k}$. Then

$$x_k = f_k(x_k) = \sum_{j=0}^n \lambda^{k}_j\, y^{k,j}, \qquad y^{k,j} = f_k(v^{k,j}) \in F(v^{k,j}).$$

All these sequences lie in compact sets, so along a subsequence $x_k \to x^*$, $\lambda^k \to \lambda^*$ and $y^{k,j} \to y^j$ for every $j$. Since the cell diameters tend to 0, $v^{k,j} \to x^*$ for every $j$. The pairs $(v^{k,j}, y^{k,j})$ are in the graph of $F$, which is closed, so $y^j \in F(x^*)$. Taking limits, $x^* = \sum_j \lambda^*_j y^j$, a convex combination of points of $F(x^*)$, which is convex. So $x^* \in F(x^*)$.

**Step 2: any compact convex set.** Let $K \subseteq \mathbb{R}^n$ be nonempty, compact and convex, choose an $n$-simplex $D \supseteq K$, and let $r: D \to K$ be the nearest-point map, which is continuous and fixes $K$ (Step 3 of the proof of [Brouwer's theorem](/brouwer-fixed-point-theorem/)). Let $G(y) = F(r(y))$ for $y \in D$. Its values are nonempty, convex and inside $K \subseteq D$, and its graph is closed: if $y_k \to y$ and $z_k \in F(r(y_k))$ with $z_k \to z$, then $r(y_k) \to r(y)$, and the closed graph of $F$ gives $z \in F(r(y))$. By Step 1, $x \in G(x)$ for some $x$. Then $x \in K$, so $r(x) = x$ and $x \in F(x)$. $\square$

## Consequences

- **Nash equilibria exist (Nash 1950).** In a finite game, let $\Sigma = \prod_i \Delta(S_i)$ be the set of mixed profiles, a compact convex set, and let $B(\sigma) = \prod_i \mathrm{BR}_i(\sigma_{-i})$, where $\mathrm{BR}_i(\sigma_{-i})$ is the set of mixed [best responses](/best-response/) of player $i$. Each $\mathrm{BR}_i(\sigma_{-i})$ is nonempty, since a linear function has a maximum on a simplex, and convex, since it is the set of mixed strategies whose support lies in the set of pure best responses, a face of the simplex. The graph of $B$ is closed because each $u_i$ is continuous. A fixed point $\sigma \in B(\sigma)$ is a profile in which every player plays a best response: a Nash equilibrium. Nash's 1951 paper replaced this argument by Brouwer's theorem applied to an explicit improvement map.
- **The minimax theorem.** For a two-player zero-sum game with payoff matrix $A$, a fixed point $(x, y)$ of the best-response map satisfies $x'^{\top} A y \le x^{\top} A y \le x^{\top} A y'$ for all mixed $x', y'$. So $\max_{x'} \min_{y'} x'^{\top} A y' \ge \min_{y'} \max_{x'} x'^{\top} A y'$, and the reverse inequality always holds, which is von Neumann's [minimax theorem](/minimax-theorem/). Kakutani gave this application in his 1941 paper.
- **Competitive equilibria.** Arrow and Debreu (1954) proved that a competitive economy has an equilibrium by finding a fixed point of a set-valued map built from demand and supply ([Arrow-Debreu existence theorem](/arrow-debreu-existence-theorem/), [competitive equilibrium](/competitive-equilibrium/)).
- **Infinite games.** Glicksberg (1952) and Ky Fan (1952) extended the theorem to compact convex sets in locally convex spaces, which gives mixed equilibria of games with compact strategy sets and continuous payoffs.
- **Computation.** The theorem is no easier to apply algorithmically than Brouwer's, of which it is a generalization: finding an approximate fixed point is PPAD-hard already for continuous functions ([PPAD](/ppad/)), and finding a Nash equilibrium of a bimatrix game is PPAD-complete.

## Tightness

- *Convex values.* On $[0, 1]$ let $F(x) = \{1\}$ for $x < 1/2$, $F(1/2) = \{0, 1\}$ and $F(x) = \{0\}$ for $x > 1/2$. The graph is closed and the values are nonempty and closed, but $F(1/2)$ is not convex, and $F$ has no fixed point. Replacing $F(1/2)$ by $[0, 1]$ makes it convex and creates the fixed point $1/2$.
- *Closed graph.* On $[0, 1]$ let $F(x) = \{1\}$ for $x < 1/2$ and $F(x) = \{0\}$ for $x \ge 1/2$. The values are convex, but the graph misses its limit point $(1/2, 1)$, and there is no fixed point.
- *Nonempty values.* If some $F(x)$ may be empty, the map $F(x) = \emptyset$ for every $x$ has no fixed point.
- *The domain.* The examples on the page of Brouwer's theorem, for an unbounded set, an open interval, an annulus and the unit ball of $\ell^2$, are single-valued maps and so also show that the conditions on $K$ are needed here.
- *Mixed strategies.* In matching pennies with pure strategies only, the best-response map on the four pure profiles has no fixed point; the set of pure profiles is not convex, and mixing is what makes Kakutani's theorem apply.

## History

Shizuo Kakutani published the theorem in the Duke Mathematical Journal in 1941, for upper semicontinuous maps from a simplex to its nonempty closed convex subsets, with a corollary for bounded closed convex sets in $\mathbb{R}^n$. He proved it by applying Brouwer's theorem to piecewise linear approximations, as above, and applied it to von Neumann's minimax theorem. John Nash used it in his 1950 note in the Proceedings of the National Academy of Sciences to prove that every finite game has an equilibrium point, and in his 1951 paper in the Annals of Mathematics he gave a second proof with Brouwer's theorem. Fan and Glicksberg extended the theorem to infinite-dimensional spaces in 1952, and Arrow and Debreu used a fixed point argument of this kind for competitive equilibrium in 1954.

## References
