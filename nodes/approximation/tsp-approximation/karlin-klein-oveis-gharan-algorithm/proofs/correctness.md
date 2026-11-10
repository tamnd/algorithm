---
title: The max entropy tree algorithm returns a tour of expected cost at most 3/2 LP*, and an outline of the KKO improvement
proves: [correctness]
status: sketch
---

This file has two parts. Part 1 is a full proof that the algorithm of this page, which uses the marginals $z = (1 - 1/n)x^*$, returns a tour with $\mathbb{E}[\text{ALG}] \le \tfrac{3}{2} \cdot \text{LP}^*$; it uses three cited polyhedral theorems. Part 2 is only an outline of why the algorithm of Karlin, Klein and Oveis Gharan gets $\tfrac{3}{2} - 10^{-36}$. Part 2 is not a proof.

## Part 1: the bound 3/2 (full, with cited theorems)

The costs $c$ on $V$, with $|V| = n \ge 3$, are symmetric, non-negative and satisfy the triangle inequality. $E$ is the set of pairs. For $S \subseteq V$, $\delta(S)$ is the set of pairs with one end in $S$, $E(S)$ the set of pairs inside $S$, and $x(F) = \sum_{e \in F} x_e$. The subtour LP is

$$\min\ c \cdot x \quad \text{s.t.} \quad x(\delta(v)) = 2 \ (v \in V), \quad x(\delta(S)) \ge 2 \ (\emptyset \ne S \subsetneq V), \quad 0 \le x \le 1,$$

and $x^*$ is an optimal solution with value LP*. The incidence vector of each tour is feasible, so $\text{LP}^* \le \text{OPT}$.

**Lemma 1 (the LP point).** $x^*(E) = n$, and $x^*(E(S)) \le |S| - 1$ for each $S \subsetneq V$ with $|S| \ge 2$.

*Proof.* Each pair has two ends, so $2x^*(E) = \sum_v x^*(\delta(v)) = 2n$. For $S$, the same count gives $2x^*(E(S)) + x^*(\delta(S)) = \sum_{v \in S} x^*(\delta(v)) = 2|S|$. With $x^*(\delta(S)) \ge 2$ this gives $x^*(E(S)) \le |S| - 1$. $\square$

**Lemma 2 (the marginals).** $z = (1 - 1/n)x^*$ lies in the spanning tree polytope of the support graph $G^* = (V, E^*)$, $E^* = \{e : x^*_e > 0\}$, and in its relative interior. So there are weights $\lambda_e > 0$ on $E^*$ such that the distribution $\Pr[T] \propto \prod_{e \in T} \lambda_e$ on the spanning trees of $G^*$ has $\Pr[e \in T] = z_e$ for each $e \in E^*$.

*Proof.* By Edmonds (1971), the spanning tree polytope of a graph is the set of $z \ge 0$ with $z(E) = n - 1$ and $z(E(S)) \le |S| - 1$ for each $S$ with $|S| \ge 2$. By Lemma 1, $z(E) = (1 - 1/n)n = n - 1$, and $z(E(S)) \le (1 - 1/n)(|S| - 1) < |S| - 1$ for each proper $S$ with $|S| \ge 2$. Also $z_e > 0$ on $E^*$. So each inequality that is not forced to be an equation on the polytope of $G^*$ holds strictly at $z$, and $z$ is in the relative interior. In particular $G^*$ is connected, since $z$ is a convex combination of its spanning trees. The existence of $\lambda$ for a point of the relative interior is the result on maximum entropy distributions of Asadpour, Goemans, Mądry, Oveis Gharan and Saberi (cited): the entropy maximum under the marginal constraints is attained, and the optimality conditions of this convex program give the product form. $\square$

The proof below uses only the marginals, not the product form. So it holds for any distribution of trees with marginals $z$. The code finds $\lambda$ numerically, and the tests check that the marginals equal $z$ to $10^{-8}$; with marginals off by at most $\eta$ on each edge, the bound below grows by at most $\eta \cdot c(E^*)$.

**Lemma 3 (the expected tree).** $\mathbb{E}[c(T)] = (1 - 1/n) \cdot \text{LP}^*$.

*Proof.* By linearity, $\mathbb{E}[c(T)] = \sum_{e} c_e \Pr[e \in T] = \sum_e c_e z_e = (1 - 1/n)\, c \cdot x^*$. $\square$

**Lemma 4 (the matching, Wolsey 1980).** For each spanning tree $T$, let $O$ be its set of vertices of odd degree. A minimum weight perfect matching $J$ on $O$ has $c(J) \le \text{LP}^*/2$.

*Proof.* $|O|$ is even by the handshaking lemma. An $O$-join is a set $F$ of pairs in which the vertices of odd degree are exactly those of $O$. By Edmonds and Johnson (1973), for non-negative costs the least cost of an $O$-join is the least value of $c \cdot y$ over the polyhedron $\{y \ge 0 : y(\delta(S)) \ge 1 \text{ for each } S \text{ with } |S \cap O| \text{ odd}\}$. The point $y = x^*/2$ is in this polyhedron, because each such $S$ is nonempty and not $V$ (as $|O|$ is even), so $x^*(\delta(S)) \ge 2$. So there is an $O$-join $F$ with $c(F) \le c \cdot x^*/2 = \text{LP}^*/2$.

Now turn $F$ into a perfect matching of $O$. In each connected part of $(V, F)$ the number of odd vertices is even. So while $O' \ne \emptyset$, where $O'$ is the set of vertices of odd degree in what is left of $F$, take a path in $F$ between two vertices $a, b \in O'$ of the same part, and remove the edges of the path. This changes the parity only at $a$ and $b$. The pairs $\{a, b\}$ form a perfect matching of $O$, and the paths have no common edges. By the triangle inequality $c(a, b)$ is at most the cost of its path, so this matching costs at most $c(F)$. $J$ is a minimum matching, so $c(J) \le c(F) \le \text{LP}^*/2$. $\square$

**Lemma 5 (the tour).** For each tree $T$, the tour $H$ of lines L5 to L8 has $c(H) \le c(T) + c(J)$.

*Proof.* Each vertex of $O$ gets one more edge, so all degrees in the multigraph $T + J$ are even, and $T + J$ is connected because $T$ is spanning. So the Euler circuit $W$ of line L7 exists and $c(W) = c(T) + c(J)$. Line L8 keeps the first visit of each vertex. Each edge of $H$ replaces a part of $W$, the parts do not overlap, and by the triangle inequality each edge costs at most its part. So $c(H) \le c(W)$. $\square$

**Theorem.** The tour $H$ is a Hamiltonian cycle and

$$\mathbb{E}[\text{ALG}] \le \Big(1 - \frac{1}{n}\Big)\text{LP}^* + \frac{\text{LP}^*}{2} < \frac{3}{2}\,\text{LP}^* \le \frac{3}{2}\,\text{OPT}.$$

*Proof.* $W$ visits each vertex, and line L8 keeps each vertex once, so $H$ is a tour. By Lemma 5 and Lemma 4, $c(H) \le c(T) + \text{LP}^*/2$ for each sampled $T$. Take the expectation and use Lemma 3. $\blacksquare$

The bound is in expectation. Lemma 4 holds for each tree, but $c(T)$ can be larger than its mean, so one run can cost more than $\tfrac{3}{2}\text{LP}^*$. By Markov's inequality applied to $c(T) \ge 0$, a run has $c(T) \le (1 + \varepsilon)(1 - 1/n)\text{LP}^*$ with probability at least $\varepsilon / (1 + \varepsilon)$, so $O(1/\varepsilon)$ runs and the best tour give $(\tfrac{3}{2} + \varepsilon)\text{LP}^*$ with a constant probability.

## Part 2: the KKO improvement (an outline, not a proof)

Karlin, Klein and Oveis Gharan (STOC 2021, with the comparison to LP* in FOCS 2022) prove that a variant of the same algorithm has $\mathbb{E}[\text{ALG}] \le (\tfrac{3}{2} - \varepsilon)\,\text{LP}^*$ for a constant $\varepsilon > 10^{-36}$. Their variant changes the graph a little, by splitting one vertex, so that the marginals are $x^*$ itself and not a scaled copy. The outline below names the main steps; each step is a long argument in the papers.

1. **The tree part stays the same.** $\mathbb{E}[c(T)]$ is at most about $\text{LP}^*$, as in Lemma 3.
2. **The matching part gets cheaper.** Instead of the fixed point $x^*/2$ of Lemma 4, they build a random vector $y$, which depends on $T$, in the $O$-join polyhedron, with $\mathbb{E}[c \cdot y] \le (\tfrac{1}{2} - \varepsilon')\,\text{LP}^*$ for a constant $\varepsilon' > 0$. Then $\mathbb{E}[c(J)] \le \mathbb{E}[c \cdot y]$ by the theorem of Edmonds and Johnson.
3. **Only near minimum cuts matter.** The constraint $y(\delta(S)) \ge 1$ is needed only when $|\delta(S) \cap T|$ is odd. If $x^*(\delta(S))$ is much larger than 2, the point $x^*/2$ has slack on $\delta(S)$ already. So the hard cuts are those with $x^*(\delta(S)) \le 2 + \eta$ for a small $\eta$.
4. **Even cuts give a saving.** When $T$ has exactly two edges in a near minimum cut, that cut is even and its constraint is not needed. The construction lowers $y_e$ below $x^*_e/2$ on an edge $e$ when the near minimum cuts that hold $e$ are even, and raises $y$ on other edges to repair the odd cuts. The core of the analysis is that the lowering wins on average.
5. **Max entropy trees are strongly Rayleigh.** The distribution $\Pr[T] \propto \prod_{e \in T} \lambda_e$ is strongly Rayleigh, so it has strong negative dependence. With this, and with the structure of near minimum cuts (the cactus and the polygon representations), they show that each such cut is even in $T$ with a probability that is at least a constant.
6. **The constant.** The constants in each step are small, and together they give $\varepsilon > 10^{-36}$.

So Part 1 is the result that is proved here, and the ratio $\tfrac{3}{2} - 10^{-36}$ is cited from the papers.
