---
title: The Edmonds-Johnson algorithm returns a shortest covering closed walk
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be an undirected multigraph with weights $w \ge 0$ and $m \ge 1$ edges, all in one component (otherwise line L1 returns NIL, and no closed walk covers all edges, since a walk stays in one component). Let $T$ be the set of vertices of odd degree, where a self-loop adds 2. All steps are finite (Dijkstra's algorithm, a matching on finitely many points, Hierholzer's algorithm), so the algorithm stops.

**Definitions.** A *multiset of edges* $X$ assigns to each $e \in E$ a number $x_e \ge 0$ of copies. Its degree $d_X(v)$ counts each copy of an edge at $v$, and a loop twice. $X$ is a *$T$-join* if $d_X(v)$ is odd exactly for $v \in T$. Its weight is $w(X) = \sum_e x_e w(e)$. $G + X$ is the multigraph with $1 + x_e$ copies of $e$.

**Lemma 1 (walks and joins).** (i) If $W$ is a closed walk that uses every edge of $G$ at least once, and $X$ counts the uses beyond the first ($x_e$ = number of uses of $e$ minus 1), then $X$ is a $T$-join and $w(W) = w(E) + w(X)$. (ii) If $X$ is a $T$-join, then $G + X$ has an Eulerian circuit, and it is a closed walk in $G$ that uses every edge at least once, of weight $w(E) + w(X)$.

*Proof.* (i) $W$ is an Eulerian circuit of $G + X$, so every degree of $G + X$ is even. Since $d_{G+X}(v) = d_G(v) + d_X(v)$, $d_X(v)$ is odd exactly when $d_G(v)$ is odd, that is for $v \in T$. The weight count is immediate. (ii) Each degree of $G + X$ is $d_G(v) + d_X(v)$, which is even. Every edge of $G + X$ is a copy of an edge of $G$, so all edges of $G + X$ lie in the one component that holds the edges of $G$. By Euler's theorem, $G + X$ has an Eulerian circuit. Mapping each copy to its original edge gives a closed walk in $G$ with the stated properties. $\square$

So the optimum is $w(E) + \tau$, where $\tau$ is the least weight of a $T$-join, and it remains to show that $X$ of line L5 is a $T$-join of weight $\tau$.

**Lemma 2 (reduction to a set).** There is a $T$-join of weight $\tau$ in which every $x_e \in \{0, 1\}$ and no loop is used.

*Proof.* Replace each $x_e$ by $x_e \bmod 2$, and set $x_e = 0$ for every loop. Removing two copies of an edge, or one copy of a loop, changes each degree by an even number, so the result is still a $T$-join, and since $w \ge 0$ its weight does not increase. $\square$

**Lemma 3 (pairing trails).** Let $J \subseteq E$ be a set of non-loop edges whose odd vertices are exactly $T$. Then $J$ contains $|T|/2$ edge-disjoint trails whose ends pair up the vertices of $T$.

*Proof.* By induction on $|T|$; if $T = \emptyset$ there is nothing to show. Otherwise take $t \in T$ and walk from $t$ along edges of $J$, never using an edge twice, as long as the current vertex has an unused edge. When the walk is at a vertex $x \ne t$, it has used an odd number of the edges at $x$ (one more entry than exits); when it is at $t$ after leaving it, it has used an even number of the edges at $t$. So if the current vertex is $t$, or is not in $T$, its degree in $J$ differs in parity from the used count, and an unused edge remains. The walk is finite, so it stops at a vertex $t' \in T$ with $t' \ne t$. It is a trail from $t$ to $t'$. Removing its edges from $J$ changes the parity only at $t$ and $t'$, so the rest has odd vertices $T \setminus \{t, t'\}$, and the induction hypothesis gives the other trails, edge-disjoint from the first. $\square$

**Lemma 4 (the matching bound).** Let $\mu$ be the weight of a minimum weight perfect matching of the complete graph on $T$ with weights $d(s, t)$. Then $\tau = \mu$.

*Proof.* ($\tau \ge \mu$.) Take a $T$-join $J$ of weight $\tau$ as in Lemma 2 and the trails of Lemma 3. The trails pair up $T$, so they define a perfect matching $N$ of $T$. A trail from $s$ to $t$ weighs at least $d(s, t)$, and the trails are edge-disjoint parts of $J$, so $\tau = w(J) \ge \sum_{\{s, t\} \in N} d(s, t) \ge \mu$.

($\tau \le \mu$.) Let $X$ be as in line L5, built from the optimal matching $M$. A path from $s$ to $t$ with $s \ne t$ has odd degree at $s$ and $t$ and even degree at its inner vertices. Adding up the paths for all pairs of $M$, each vertex of $T$ is the end of exactly one path, and each other vertex is an end of none. So $d_X(v)$ is odd exactly for $v \in T$, and $X$ is a $T$-join of weight $\sum_{\{s, t\} \in M} d(s, t) = \mu$. So $\tau \le \mu$. $\square$

The shortest paths exist because all odd vertices are in the one component of the edges, and Dijkstra's algorithm computes them because $w \ge 0$.

**Theorem.** If the edges of $G$ are not in one component, EDMONDS-JOHNSON returns NIL, and no covering closed walk exists. Otherwise it returns a closed walk that uses every edge at least once, of the least possible weight $w(E) + \mu$.

*Proof.* The first part is line L1. Otherwise, the set $X$ of line L5 is a $T$-join of weight $\mu = \tau$ by Lemma 4, so by Lemma 1 (ii) line L6 finds an Eulerian circuit of $G + X$, which is a covering closed walk of weight $w(E) + \tau$. By Lemma 1 (i), every covering closed walk has weight at least $w(E) + \tau$. $\blacksquare$
