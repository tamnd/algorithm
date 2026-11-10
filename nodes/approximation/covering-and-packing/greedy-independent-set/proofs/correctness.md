---
title: Minimum-degree greedy returns an independent set of size at least the Caro-Wei bound
proves: [correctness]
status: full
---

The input is a graph $G = (V, E)$ with $n$ vertices, $m$ edges and no self-loops. $H$ is the remaining graph, $d_H(u)$ is the degree of $u$ in $H$, $N_H[v]$ is $v$ with its neighbours in $H$, and $I$ is the output list. For a graph $H$ let

$$\Phi(H) = \sum_{u \in V(H)} \frac{1}{d_H(u) + 1},$$

so $\Phi$ of the empty graph is 0.

**Lemma 1 (the invariant).** At the start of each iteration of line L2, $I$ is an independent set of $G$, and no vertex of $H$ is in $I$ or adjacent in $G$ to a vertex of $I$.

*Proof.* At the start, $I = \emptyset$ and $H = G$. Suppose the claim holds, and line L3 picks $v$ in $H$. By the claim, $v$ has no neighbour in $I$, so $I$ with $v$ added is independent. Line L5 deletes $v$ and each neighbour of $v$ in $H$. A vertex $u$ that stays in $H$ is not adjacent to $v$ in $G$: an edge $\{u, v\}$ of $G$ with both ends in $H$ is an edge of $H$, because $H$ is an induced subgraph of $G$, so $u$ would be in $N_H[v]$. So the claim holds after the iteration. $\square$

**Lemma 2 (maximality).** At the end, $I$ is a maximal independent set of $G$.

*Proof.* The loop stops when $H$ is empty. Each vertex left $H$ in line L5, as a picked vertex or as a neighbour of one. So each vertex of $G$ is in $I$ or adjacent to a vertex of $I$, and no vertex can be added to $I$. By Lemma 1, $I$ is independent. $\square$

**Lemma 3 (one step loses at most 1).** If $v$ has minimum degree $d$ in $H$, and $H' = H - N_H[v]$, then $\Phi(H') \ge \Phi(H) - 1$.

*Proof.* The set $N_H[v]$ has $d + 1$ vertices. Each $u \in N_H[v]$ has $d_H(u) \ge d$, because $d$ is the minimum degree, so its term in $\Phi(H)$ is at most $1/(d + 1)$, and these $d + 1$ terms add up to at most 1. Each vertex $u$ of $H'$ has $d_{H'}(u) \le d_H(u)$, because $H'$ is an induced subgraph of $H$, so its term does not fall. So $\Phi(H') \ge \Phi(H) - 1$. $\square$

**Theorem.** The algorithm returns a maximal independent set $I$ of $G$ with

$$|I| \ge \Phi(G) = \sum_{v \in V} \frac{1}{\deg(v) + 1}.$$

*Proof.* By Lemma 2, $I$ is a maximal independent set. Let $H_0 = G, H_1, \ldots, H_t$ be the graphs at the start of each iteration and at the end, with $t = |I|$ and $H_t$ empty. By Lemma 3, $\Phi(H_{i+1}) \ge \Phi(H_i) - 1$ for each $i$. Sum over $i = 0, \ldots, t - 1$: $0 = \Phi(H_t) \ge \Phi(G) - t$. So $|I| = t \ge \Phi(G)$. $\blacksquare$

**Corollary (Turán bound).** With average degree $\bar d = 2m/n$, the output has $|I| \ge n/(\bar d + 1)$.

*Proof.* The function $x \mapsto 1/(x + 1)$ is convex for $x \ge 0$, so by Jensen's inequality $\frac{1}{n}\sum_v \frac{1}{\deg(v) + 1} \ge \frac{1}{\bar d + 1}$. Multiply by $n$ and apply the theorem. $\square$

**Remark (the ratio in terms of the maximum degree).** If each degree is at most $\Delta$, then $\Phi(G) \ge n/(\Delta + 1)$, and $\alpha(G) \le n$, so the theorem gives the ratio $\alpha(G)/|I| \le \Delta + 1$. Halldórsson and Radhakrishnan (1997) proved the sharper ratio $(\Delta + 2)/3$ for $\Delta \ge 1$ with a finer charging argument; that proof is not given here.
