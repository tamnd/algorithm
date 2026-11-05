---
title: Lazy rebuilding keeps a (1 + ε)-approximate matching
proves: [correctness]
status: full
---

Write $\nu(G)$ for the size of a maximum matching of $G$. Fix $\varepsilon > 0$. We prove that after every update the structure holds a matching $M$ of the current graph with $(1 + \varepsilon)|M| \ge \nu(G)$.

**Lemma 1 (one update moves $\nu$ by at most one).** If $G'$ is $G$ with one edge inserted or deleted, then $|\nu(G') - \nu(G)| \le 1$.

*Proof.* Let $e$ be the edge. A maximum matching of the graph with $e$ loses at most one edge, namely $e$, when $e$ is removed, and what remains is a matching of the graph without $e$. A matching of the graph without $e$ is also a matching of the graph with $e$. So the two values differ by at most one. $\square$

**Lemma 2 ($M$ stays a matching of the current graph).** After every update, $M$ is a matching, and all its edges are edges of the current graph.

*Proof.* A rebuild returns a matching of the current graph. Line L2 adds an edge of the graph whose two ends are free, so $M$ stays a matching. Line L3 removes the deleted edge from $M$ if it was there, so every edge of $M$ is still present. No other line changes $M$ or the graph. $\square$

**Lemma 3 (stability).** Let $M_0$ be the matching right after a rebuild of the graph $G_0$, with $\nu(G_0) = |M_0|$. After $t$ more updates, with no rebuild in between, the matching $M_t$ and the graph $G_t$ satisfy

$$\nu(G_t) \le |M_0| + t \quad \text{and} \quad |M_t| \ge |M_0| - t.$$

*Proof.* The first inequality follows from Lemma 1 by induction on $t$. For the second, between rebuilds only line L3 removes edges from $M$, at most one per update, and line L2 only adds edges. $\square$

**Lemma 4 (the budget is enough).** If $t \le b = \lfloor \varepsilon |M_0| / (2 + \varepsilon) \rfloor$, then $(1 + \varepsilon)|M_t| \ge \nu(G_t)$.

*Proof.* From $t \le \varepsilon |M_0| / (2 + \varepsilon)$ we get $(2 + \varepsilon) t \le \varepsilon |M_0|$, that is, $|M_0| + t \le (1 + \varepsilon)(|M_0| - t)$. By Lemma 3, $\nu(G_t) \le |M_0| + t \le (1 + \varepsilon)(|M_0| - t) \le (1 + \varepsilon) |M_t|$. $\square$

**Theorem.** After every update, $M$ is a matching of the current graph with $(1 + \varepsilon)|M| \ge \nu(G)$.

*Proof.* $M$ is a matching of the current graph by Lemma 2. Consider the last rebuild before or at the current update, with matching $M_0$ and budget $b$. If the rebuild happened at this update, then $M = M_0$ is maximum and the bound is clear. Otherwise the counter $c$ equals the number $t$ of updates since that rebuild, and since line L5 did not rebuild, $t \le b$. Lemma 4 gives the bound. The structure starts with a rebuild of the empty graph, so a last rebuild always exists. $\blacksquare$
