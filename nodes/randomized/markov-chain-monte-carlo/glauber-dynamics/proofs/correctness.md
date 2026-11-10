---
title: Glauber dynamics on colorings is reversible, ergodic and rapidly mixing for q > 2Δ
proves: [correctness]
status: full
---

**Setting.** $G = (V, E)$ is a graph with $n$ vertices and maximum degree $\Delta$, and $C = \{1, \ldots, q\}$. A coloring is any $x : V \to C$; it is proper if $x(v) \ne x(w)$ for every edge $vw$. Let $\Omega$ be the set of proper colorings and $A_v(x) = C \setminus \{x(w) : w \sim v\}$. One step of the chain picks $v$ uniformly from $V$ and sets $x(v)$ to a uniform element of $A_v(x)$ (lines L2 to L4). Write $d(t) = \max_{x \in \Omega}\|P^t(x, \cdot) - \pi\|_{TV}$, $t_{mix}(\varepsilon) = \min\{t : d(t) \le \varepsilon\}$ and $t_{mix} = t_{mix}(1/4)$, with $\pi$ uniform on $\Omega$.

**Lemma 1 (the step is defined and keeps $\Omega$).** If $q \ge \Delta + 1$, then $|A_v(x)| \ge q - \deg(v) \ge q - \Delta \ge 1$ for every coloring $x$. If $x$ is proper, the new coloring is proper. If $x$ is not proper, the set of edges with equal colors at both ends does not grow, and it loses every such edge at $v$.

*Proof.* At most $\deg(v)$ colors are removed from $C$. The new color at $v$ differs from all neighbor colors, so no edge at $v$ is in conflict after the step, and edges not at $v$ do not change. $\square$

So from any start, once every vertex has been chosen at least once, the coloring is proper and stays proper.

**Lemma 2 (reversibility).** For $x, y \in \Omega$, $P(x, y) = P(y, x)$. Hence $\pi$, the uniform law on $\Omega$, satisfies $\pi(x)P(x, y) = \pi(y)P(y, x)$ and is stationary.

*Proof.* If $x$ and $y$ differ at two or more vertices, both sides are 0. If they differ at exactly one vertex $v$, the only way to move between them is to choose $v$. The set $A_v(x)$ depends only on the colors of the neighbors of $v$, which $x$ and $y$ share, so $A_v(x) = A_v(y)$, and $P(x, y) = \frac1n\cdot\frac1{|A_v(x)|} = P(y, x)$. For $x = y$ there is nothing to prove. Summing detailed balance over $x$ gives $\pi P = \pi$. $\square$

*The general heat bath.* For a positive $\pi$ on $S^V$, the step at $v$ moves $x$ to $y = x^{v \to s}$ with probability $\pi(y)/Z_v(x)$, where $Z_v(x) = \sum_{s'}\pi(x^{v \to s'})$ depends only on the values off $v$. So $\pi(x)P(x, y) = \pi(x)\pi(y)/(nZ_v(x))$, which is symmetric in $x$ and $y$ because $Z_v(x) = Z_v(y)$. The same argument applies.

**Lemma 3 (irreducibility for $q \ge \Delta + 2$).** For $x, y \in \Omega$ there is a sequence of single-vertex recolorings, each giving a proper coloring, that changes $x$ into $y$.

*Proof.* Order the vertices $v_1, \ldots, v_n$. Assume that $v_1, \ldots, v_{k-1}$ already have their colors in $y$. Let $c = y(v_k)$. For each neighbor $w$ of $v_k$ with current color $c$: $w$ is not among $v_1, \ldots, v_{k-1}$, because those have $y$-colors and $y(w) \ne c$. Recolor $w$ with a color that is not $c$ and not used by any neighbor of $w$. This excludes at most $\Delta + 1$ colors, so with $q \ge \Delta + 2$ one is left. The coloring stays proper, and $v_1, \ldots, v_{k-1}$ are not changed. Now no neighbor of $v_k$ has color $c$, so recolor $v_k$ with $c$. After $n$ stages the coloring is $y$. Each recoloring of a vertex $u$ to a color in $A_u$ has probability at least $1/(nq)$ under the chain, so $P^m(x, y) > 0$ for some $m$. $\square$

The bound $q \ge \Delta + 2$ is needed in general: on the triangle with $q = 3$, each $A_v(x)$ is the single color $x(v)$, so $P$ is the identity on the 6 proper colorings.

**Lemma 4 (aperiodicity).** $P(x, x) \ge \frac1n\sum_v\frac1{|A_v(x)|} > 0$, because $x(v) \in A_v(x)$ for proper $x$. So every state has period 1.

By Lemmas 2 to 4 and the convergence theorem for [ergodic](/ergodicity/) chains, $P^t(x, \cdot) \to \pi$ for every $x \in \Omega$ when $q \ge \Delta + 2$.

**Theorem (rapid mixing for $q > 2\Delta$).** Let $\alpha = \frac{q - 2\Delta}{n(q - \Delta)}$. Then $d(t) \le n(1 - \alpha)^t \le ne^{-\alpha t}$, and
$$
t_{mix}(\varepsilon) \le \Big\lceil\frac{q - \Delta}{q - 2\Delta}\,n\,\ln\frac n\varepsilon\Big\rceil.
$$

*Proof.* Extend the chain to all $q^n$ colorings with the same rule; by Lemma 1 the step is defined. Let $\rho$ be the Hamming distance. Two colorings at distance $r$ are joined by a path of $r$ colorings, each at distance 1 from the next, possibly through improper colorings. By the path coupling theorem of Bubley and Dyer (see [path coupling](/path-coupling/)), it suffices to give, for every pair $x, y$ with $\rho(x, y) = 1$, a coupling of one step with $\mathbb E[\rho(X_1, Y_1)] \le 1 - \alpha$.

Let $x$ and $y$ differ only at $w$. Choose the same uniform $v$ in both copies.

- If $v = w$: $A_w(x) = A_w(y)$, since the neighbors of $w$ have the same colors. Use the same color in both copies. The distance becomes 0.
- If $v \ne w$ and $v$ is not a neighbor of $w$: again $A_v(x) = A_v(y)$, use the same color, and the distance stays 1.
- If $v$ is a neighbor of $w$: let $S$ be the set of colors of the other neighbors of $v$. Then $A = A_v(x) = C \setminus (S \cup \{x(w)\})$ and $B = A_v(y) = C \setminus (S \cup \{y(w)\})$, so $|A \cap B| \ge \max(|A|, |B|) - 1$. Use an optimal coupling of the uniform laws on $A$ and $B$. The colors differ with probability
$$
\|\mathrm{U}(A) - \mathrm{U}(B)\|_{TV} = 1 - \frac{|A \cap B|}{\max(|A|, |B|)} \le \frac1{\max(|A|, |B|)} \le \frac1{q - \Delta},
$$
using $|A| \ge q - \Delta$ from Lemma 1. The distance becomes at most 2, and it is 2 only if the colors differ.

Since $w$ has at most $\Delta$ neighbors,
$$
\mathbb E[\rho(X_1, Y_1)] \le 1 - \frac1n + \frac\Delta n\cdot\frac1{q - \Delta} = 1 - \frac{q - 2\Delta}{n(q - \Delta)} = 1 - \alpha.
$$
Path coupling extends this to all pairs: $\mathbb E[\rho(X_t, Y_t)] \le (1 - \alpha)^t\rho(x, y) \le n(1 - \alpha)^t$. Start $X$ at any $x \in \Omega$ and $Y$ from $\pi$. Both chains stay in $\Omega$ by Lemma 1, $Y_t \sim \pi$, and by the [coupling inequality](/coupling-inequality/),
$$
\|P^t(x, \cdot) - \pi\|_{TV} \le \Pr[X_t \ne Y_t] \le \mathbb E[\rho(X_t, Y_t)] \le n(1 - \alpha)^t \le ne^{-\alpha t}.
$$
This is at most $\varepsilon$ when $t \ge \alpha^{-1}\ln(n/\varepsilon)$, which is the stated bound. $\square$

**Check on small graphs.** With exact fractions, the path with 3 vertices and $q = 5$ has $t_{mix} = 6$ and the bound for $\varepsilon = 1/4$ gives $\lceil 9\ln 12\rceil = 23$. The edge with $q = 3$ has $t_{mix} = 4$ against $\lceil 4\ln 8\rceil = 9$. On both, $d(t) \le n(1 - \alpha)^t$ holds for every $t$ up to the bound, and the one-step contraction holds for every pair of colorings at distance 1, proper or not.
