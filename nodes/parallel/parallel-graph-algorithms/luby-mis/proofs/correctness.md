---
title: Luby's algorithm returns a maximal independent set, halves the edges in expectation, and does linear expected work
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $G = (V, E)$ has $n$ vertices and $m$ edges. In round $t$ (counting from 0), $L_t$ is the set of live vertices, $G_t$ the subgraph induced by $L_t$, $n_t = |L_t|$ and $m_t$ the number of edges of $G_t$. $N(v)$ and $d(v)$ are taken in $G_t$. The priorities of round $t$ are a uniformly random permutation of $L_t$, independent of everything before.

**Lemma 1 (invariant).** At the start of every round: $I$ is independent; no vertex of $L_t$ is in $I$ or adjacent to a vertex of $I$; and every vertex of $V \setminus L_t$ is in $I$ or adjacent to a vertex of $I$.

*Proof.* At the start, $I = \emptyset$ and $L_0 = V$. Assume the invariant at the start of round $t$, and let $J$ be the set of vertices with $join$ true. Two adjacent live vertices $u, v$ cannot both be in $J$, since $r(u) < r(v)$ and $r(v) < r(u)$ cannot both hold. By the invariant, no vertex of $J \subseteq L_t$ is adjacent to $I$. So $I \cup J$ is independent. Line L6 removes $J$ and every live neighbour of $J$; the vertices removed are in $I \cup J$ or adjacent to $J$. A vertex that stays live is not in $J$, has no neighbour in $J$, and by the invariant has no neighbour in the old $I$. $\square$

**Theorem 1 (correctness and termination).** The algorithm stops after at most $n$ rounds and returns a maximal independent set.

*Proof.* In each round with $L_t \ne \emptyset$, the vertex of least priority in $L_t$ has $join$ true, so $n_{t+1} < n_t$. When $L_t = \emptyset$, Lemma 1 says $I$ is independent and every vertex is in $I$ or adjacent to it. $\blacksquare$

**Lemma 2 (half of the edges).** $E[m_{t+1} \mid L_t] \le m_t / 2$.

*Proof.* Fix $L_t$. For an ordered pair $(u, v)$ with $\{u, v\}$ an edge of $G_t$, let $A(u \to v)$ be the event that $r(u)$ is the least priority in $N(u) \cup N(v)$. This set contains $u$ (as $u \in N(v)$) and has at most $d(u) + d(v)$ elements, and the priorities are a uniform permutation, so $\Pr[A(u \to v)] \ge 1 / (d(u) + d(v))$.

If $A(u \to v)$ happens, $r(u)$ is less than $r(w)$ for every $w \in N(u)$, so $u$ joins, and $v \in N(u)$ is removed with all its $d(v)$ edges. For a fixed $v$, the events $A(u \to v)$ and $A(w \to v)$ with $u \ne w$ are disjoint: both sets contain $N(v) \ni u, w$, and $u$ and $w$ cannot both have the least priority. Let $B_v$ be the event that some $A(u \to v)$ happens. Then $\Pr[B_v] = \sum_{u \in N(v)} \Pr[A(u \to v)]$.

Let $X$ be the number of edges of $G_t$ removed in round $t$. Each edge at a vertex $v$ with $B_v$ is removed, and an edge has two ends, so $X \ge \frac{1}{2} \sum_v d(v) \mathbf{1}[B_v]$. By [linearity of expectation](/linearity-of-expectation/),

$$E[X] \ge \frac{1}{2} \sum_v \sum_{u \in N(v)} \frac{d(v)}{d(u) + d(v)} = \frac{1}{2} \sum_{\{u, v\} \in E(G_t)} \left( \frac{d(v)}{d(u) + d(v)} + \frac{d(u)}{d(u) + d(v)} \right) = \frac{m_t}{2}.$$

The edges of $G_{t+1}$ are the edges of $G_t$ that are not removed, so $E[m_{t+1} \mid L_t] = m_t - E[X] \le m_t / 2$. $\square$

**Theorem 2 (rounds).** Let $T = \min\{t : m_t = 0\}$ and let $R$ be the number of rounds. Then $R = T + 1$ if $n \ge 1$, $E[m_t] \le m / 2^t$, $E[R] \le \log_2 m + 4$ for $m \ge 1$, and $\Pr[R > (c + 2) \log_2 n + 2] \le n^{-c}$ for every $c > 0$ and $n \ge 2$.

*Proof.* In round $T$ the live vertices have no live neighbours, so all of them join and $L_{T+1} = \emptyset$; in earlier rounds $m_t \ge 1$, so $L_t$ is not empty. So $R = T + 1$. Taking expectations in Lemma 2 and iterating gives $E[m_t] \le m / 2^t$. By [Markov's inequality](/markov-inequality/), $\Pr[T > t] = \Pr[m_t \ge 1] \le m / 2^t$. Let $t_0 = \lceil \log_2 m \rceil$. Then

$$E[T] = \sum_{t \ge 0} \Pr[T > t] \le t_0 + \sum_{t \ge t_0} m 2^{-t} \le t_0 + 2,$$

so $E[R] \le \log_2 m + 4$. Edges are never added, so $m_t$ does not grow, and $T > k$ holds exactly when $m_k \ge 1$. Let $s = (c + 2) \log_2 n + 1$ and $k = \lfloor s \rfloor \ge s - 1$. Then $\Pr[R > s + 1] = \Pr[T > s] = \Pr[m_k \ge 1] \le m / 2^{k} \le m / 2^{s - 1} = m / n^{c + 2} \le n^{-c}$, using $m < n^2$. $\blacksquare$

**Theorem 3 (work).** The expected total of $n_t + m_t$ over all rounds is at most $n + 6m$. So with $O(n_t + m_t)$ expected work per round, the expected work is $O(n + m)$.

*Proof.* A vertex of $L_t$ with a live neighbour is an end of one of the $m_t$ edges, so there are at most $2 m_t$ such vertices. A vertex of $L_t$ with no live neighbour joins in round $t$, so it is counted in only one round. So $\sum_t n_t \le n + 2 \sum_t m_t$. By Theorem 2, $E[\sum_t m_t] \le \sum_t m / 2^t = 2m$. So $E[\sum_t (n_t + m_t)] \le n + 3 \cdot 2m = n + 6m$. $\blacksquare$
