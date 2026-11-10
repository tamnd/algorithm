---
title: Israeli-Itai returns a maximal matching, removes a constant fraction of the edges per round in expectation, and does linear expected work
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ has $n$ vertices and $m$ edges. In round $t$ (counting from 0), $G_t$ is the remaining graph, $m_t$ its number of edges, and $A_t$ the set of its vertices with at least one edge; $n_t = |A_t|$. $N(v)$ and $d(v)$ are taken in $G_t$. In round $t$, every $v \in A_t$ proposes to a uniformly random $\pi(v) \in N(v)$, independently; every vertex that got a proposal keeps one of them by any rule; $H$ is the set of edges $\{v, \pi(v)\}$ for which $\pi(v)$ kept the proposal of $v$; every vertex with an edge in $H$ picks one of its edges in $H$ uniformly at random, independently; the edges picked by both ends join $M$.

**Lemma 1 (invariant).** At the start of each round, $M$ is a matching, no vertex of $G_t$ is matched, and every edge of $G$ that is not in $G_t$ has a matched end.

*Proof.* At the start, $M = \emptyset$ and $G_0 = G$. Assume the claim at the start of round $t$. Each vertex picks at most one edge, so a vertex is an end of at most one edge added in round $t$; the added edges are edges of $G_t$, whose ends are not matched by the old $M$. So the new $M$ is a matching. Line L8 removes exactly the newly matched vertices and their edges, so no vertex of $G_{t+1}$ is matched, and every removed edge has a matched end. $\square$

**Lemma 2.** Every vertex has at most two edges in $H$.

*Proof.* An edge of $H$ at $v$ is either $\{v, \pi(v)\}$, from the proposal of $v$, or $\{u, v\}$ with $v = \pi(u)$ and $v$ keeping the proposal of $u$. There is at most one edge of each kind. $\square$

**Lemma 3 (half of the edges have a good end).** Call $v \in A_t$ good if at least $d(v)/3$ of its neighbours $u$ have $d(u) \le d(v)$. At least $m_t / 2$ edges of $G_t$ have a good end.

*Proof.* Orient each edge of $G_t$ from the end with the smaller pair $(d, \text{name})$ to the end with the larger pair. Let $v$ be a vertex that is not good. More than $2 d(v)/3$ of its neighbours have $d(u) > d(v)$, and all those edges point out of $v$, so $out(v) > 2 d(v)/3$ and $in(v) = d(v) - out(v) < d(v)/3$. So $out(v) > 2\, in(v)$, and we can map the in-edges of $v$ injectively to pairwise disjoint pairs of out-edges of $v$.

Let $B$ be the set of edges with both ends not good. Map each $e = (u \to v) \in B$ to the pair of out-edges of $v$ given above. Two edges of $B$ with the same head get disjoint pairs by construction; two edges with different heads $v \ne v'$ get disjoint pairs, because an edge is an out-edge of only its tail. So the $|B|$ pairs are pairwise disjoint subsets of the edges of $G_t$, and $2 |B| \le m_t$. The other $m_t - |B| \ge m_t / 2$ edges have a good end. $\square$

**Lemma 4 (a good vertex is matched with constant probability).** For a good vertex $v$, $\Pr[v \text{ is matched in round } t \mid G_t] \ge p = (1 - e^{-1/3}) / 2$.

*Proof.* Let $U$ be the set of neighbours $u$ of $v$ with $d(u) \le d(v)$; $|U| \ge d(v)/3$ and $d(v) \ge 1$. Each $u \in U$ proposes to $v$ with probability $1/d(u) \ge 1/d(v)$, independently. So

$$\Pr[v \text{ gets no proposal}] \le \left(1 - \frac{1}{d(v)}\right)^{|U|} \le e^{-|U| / d(v)} \le e^{-1/3}.$$

If $v$ gets a proposal, it keeps one, so $v$ has $k \in \{1, 2\}$ edges in $H$ by Lemma 2. Fix the proposals and the kept proposals, which fixes $H$; the picks are independent of them. For an edge $\{v, w\}$ of $H$, $v$ picks it with probability $1/k$ and $w$ picks it with probability at least $1/2$, by Lemma 2, independently. The events for the $k$ edges at $v$ are disjoint, since $v$ picks only one edge. So $v$ is matched with probability at least $k \cdot \frac{1}{k} \cdot \frac{1}{2} = \frac{1}{2}$. Multiplying, $\Pr[v \text{ matched}] \ge (1 - e^{-1/3}) \cdot \frac{1}{2} = p$. $\square$

**Theorem 1 (edges shrink).** $E[m_{t+1} \mid G_t] \le q\, m_t$ with $q = 1 - p/2 = 1 - (1 - e^{-1/3})/4 < 0.93$.

*Proof.* An edge with a good end $v$ is removed when $v$ is matched, which by Lemma 4 has probability at least $p$. By Lemma 3 and linearity of expectation, the expected number of removed edges is at least $p\, m_t / 2$. $\square$

**Theorem 2 (correctness, termination and rounds).** Let $R$ be the number of rounds. With probability 1 the algorithm stops, and then $M$ is a maximal matching. Moreover $\Pr[R > k] \le m q^k$ for every $k \ge 0$, so $\Pr[R > \lceil (c + 2) \ln n / \ln(1/q) \rceil] \le n^{-c}$ for $n \ge 2$, and $E[R] \le \log_{1/q} m + 1 + 1/(1 - q)$.

*Proof.* The loop runs round $t$ exactly when $m_t \ge 1$, and $m_t$ never grows, so $R > k$ holds exactly when $m_k \ge 1$. Taking expectations in Theorem 1, $E[m_k] \le q^k m$, and by Markov's inequality $\Pr[m_k \ge 1] \le m q^k$. This tends to 0, so the algorithm stops with probability 1. When it stops, no edge remains, so by Lemma 1 every edge of $G$ has a matched end, and $M$ is a maximal matching.

For $k \ge (c + 2) \ln n / \ln(1/q)$, $q^k \le n^{-(c + 2)}$ and $m q^k < n^2 \cdot n^{-(c + 2)} = n^{-c}$. With $t_0 = \lceil \log_{1/q} m \rceil$,

$$E[R] = \sum_{k \ge 0} \Pr[R > k] \le t_0 + \sum_{k \ge t_0} m q^k \le t_0 + \frac{1}{1 - q}. \qquad \blacksquare$$

Numerically, $1/(1 - q) < 14.2$ and $1 / \log_2(1/q) < 9.5$, so $E[R] \le 9.8 \log_2 m + 16$ and the w.h.p. bound is at most $\lceil 9.8 (c + 2) \log_2 n \rceil$.

**Theorem 3 (work).** If a round costs $O(n_t + m_t)$ work, the expected total work is $O(n + m)$.

*Proof.* Every vertex of $A_t$ has an edge, so $n_t \le 2 m_t$. By Theorem 1, $E[\sum_t m_t] \le \sum_t q^t m = m / (1 - q)$. So $E[\sum_t (n_t + m_t)] \le 3m / (1 - q) = O(m)$, and with the $O(n + m)$ setup the expected work is $O(n + m)$. $\blacksquare$
