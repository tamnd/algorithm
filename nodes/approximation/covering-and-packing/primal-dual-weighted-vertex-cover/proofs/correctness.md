---
title: The primal-dual algorithm returns a vertex cover of weight at most twice the optimum
proves: [correctness]
status: full
---

The input is a graph $G = (V, E)$ with $n$ vertices, $m$ edges, no self-loops, and weights $w(v) \ge 0$. For a vector $y$ on the edges, the *load* of a vertex is $\ell_v(y) = \sum_{e \ni v} y_e$, and $v$ is *tight* if $\ell_v(y) = w(v)$. The LP relaxation of weighted vertex cover and its dual are

$$\min \sum_{v} w(v) x_v \ \text{ s.t. } x_u + x_v \ge 1 \text{ for each } \{u, v\} \in E,\ x \ge 0; \qquad \max \sum_{e} y_e \ \text{ s.t. } \ell_v(y) \le w(v) \text{ for each } v,\ y \ge 0.$$

In the implementation, the residual of $v$ is $w(v) - \ell_v(y)$, and $C$ is the set of vertices added in line L6. Edges not yet visited have $y_e = 0$.

**Lemma 1 (the invariant).** At the start of each iteration of line L2, and at the end:

1. $y \ge 0$ and $\ell_v(y) \le w(v)$ for each $v$, so $y$ is dual feasible;
2. each vertex in $C$ is tight.

*Proof.* At the start, $y = 0$, $w \ge 0$ and $C = \emptyset$. Take the iteration for the edge $e = \{u, v\}$. If line L3 finds $u \in C$ or $v \in C$, then $y_e$ stays 0 and nothing changes. Else line L4 sets $\delta = \min(w(u) - \ell_u, w(v) - \ell_v) \ge 0$, by part 1. Line L5 sets $y_e = \delta$, which adds $\delta$ to the loads of $u$ and $v$ only. Their new loads are at most $w(u)$ and $w(v)$, by the choice of $\delta$, so part 1 holds. The vertices of $C$ are not $u$ or $v$, so their loads do not change and they stay tight. Line L6 adds only tight vertices. So part 2 holds. $\square$

**Lemma 2 (a cover).** At the end, each edge has an endpoint in $C$.

*Proof.* Take the edge $\{u, v\}$ in its iteration. If an endpoint is already in $C$, it stays there. Else $\delta$ equals the residual of $u$ or of $v$, so after line L5 that endpoint has residual 0, and line L6 adds it to $C$. $\square$

**Theorem (Bar-Yehuda and Even 1981).** The algorithm returns a vertex cover $C$ with

$$w(C) \le 2 \sum_{e \in E} y_e \le 2 \cdot \text{LP}^* \le 2 \cdot \text{OPT}.$$

*Proof.* By Lemma 2, $C$ is a cover. By part 2 of Lemma 1, each $v \in C$ is tight, so

$$w(C) = \sum_{v \in C} \sum_{e \ni v} y_e = \sum_{e \in E} y_e \, |e \cap C| \le 2 \sum_{e \in E} y_e,$$

because an edge has two endpoints and $y \ge 0$. By part 1 of Lemma 1 and weak duality, $\sum_e y_e \le \text{LP}^*$. An optimal cover gives a feasible 0-1 point of the LP, so $\text{LP}^* \le \text{OPT}$. $\blacksquare$

**Remark (local ratio form).** Line L5 can be read as follows: subtract $\delta$ from the weights of $u$ and $v$. The weight function $\delta \cdot [u \text{ or } v]$ is 2-effective: each minimal cover pays at most $2\delta$ for it, and each cover pays at least $\delta$, because it holds $u$ or $v$. The local ratio theorem then gives the same bound 2; see the [local ratio technique](/local-ratio-technique/).
