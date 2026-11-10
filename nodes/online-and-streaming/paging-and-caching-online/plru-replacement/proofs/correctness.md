---
title: Tree PLRU keeps the log2 k + 1 most recent blocks, and with 4 ways it is not competitive
proves: [correctness]
status: full
---

**Setting.** One set has $k = 2^d$ ways, the leaves of a complete binary tree of depth $d$. For a node $v$, let $T(v)$ be the set of ways below $v$. Each access *touches* one way $w$ (line L6 puts the block there), and line L7 then updates the bits on the path to $w$. Let $\tau(w)$ be the time of the last touch of way $w$, with $\tau(w) = -1$ if $w$ was never touched, and let $\tau(T) = \max_{w \in T} \tau(w)$.

**Serving.** After lines L3 to L6, the block $x$ is in the set, so each access is served.

**Lemma 1 (what the bits mean).** After each access, for each internal node $v$ with children $v_L$ and $v_R$: if some way of $T(v)$ was touched, the bit $b[v]$ points to the child whose subtree does *not* hold the way touched last in $T(v)$. If no way of $T(v)$ was touched, $b[v] = 0$.

*Proof.* By induction on the number of accesses. At the start, all bits are $0$ and nothing was touched. Let an access touch way $w$. For a node $v$ on the path to $w$, line L7 sets $b[v]$ to point to the child not on the path, and $w$ is now the way touched last in $T(v)$. For a node $v$ not on the path, $w \notin T(v)$, so the way touched last in $T(v)$ does not change, and neither does $b[v]$. $\square$

So when all ways are full and have distinct touch times, line L5 goes at each node to the child with the smaller $\tau$, that is, to the half used less recently.

**Lemma 2 (the victim is not recent).** Let all $k$ ways be full, and let line L5 choose the way $w$. Then at least $d$ other ways were touched after $w$.

*Proof.* Let $v_0, v_1, \ldots, v_d = w$ be the path from the root to $w$, so line L5 goes from $v_i$ to $v_{i+1}$ for $i = 0, \ldots, d-1$. Let $u_i$ be the other child of $v_i$. By Lemma 1, the way $m_i$ touched last in $T(v_i)$ lies in $T(u_i)$, so $m_i \ne w$ and $\tau(m_i) > \tau(w)$; the times are distinct because all ways are full and each touch has its own time. The sets $T(u_0), \ldots, T(u_{d-1})$ are disjoint, so $m_0, \ldots, m_{d-1}$ are $d$ distinct ways, each touched after $w$. $\square$

**Theorem 1 (the recent blocks stay).** After each access, the $d + 1 = \log_2 k + 1$ most recently used distinct blocks are all in the set.

*Proof.* Each block in the set sits in the way that was touched at its last use, so the order of the blocks by last use is the order of their ways by $\tau$. Let $R$ be the list of the $d + 1$ most recently used distinct blocks before an access to $x$, and assume that all of them are in the set.

- *Hit, or a miss with an empty way.* Nothing is evicted. The new list is $x$ followed by the blocks of $R$ other than $x$, all in the set.
- *Miss with a full set.* By Lemma 2, at least $d$ blocks in the set were used after the victim. So the victim is not among the $d$ most recently used blocks, and the first $d$ blocks of $R$ stay. The new list is $x$ and these $d$ blocks, all in the set.

By induction on the accesses, the claim holds after each access. $\square$

**Corollary 2.** On every sequence $\sigma$, $\mathrm{PLRU}_k(\sigma) \le \mathrm{LRU}_{d+1}(\sigma)$, where the index is the number of ways.

*Proof.* LRU with $d + 1$ ways holds exactly the $d + 1$ most recently used distinct blocks. If it hits on $x$, then $x$ is among them, so by Theorem 1, PLRU with $k$ ways also hits. $\square$

With the theorem of Sleator and Tarjan, $\mathrm{LRU}_{d+1}(\sigma) \le \frac{d+1}{d+1-h+1} \mathrm{OPT}_h(\sigma) + b$ for $h \le d + 1$ and a constant $b$, so PLRU is competitive against an offline cache with at most $\log_2 k + 1$ ways.

**Theorem 3 (not competitive with 4 ways).** For $k = 4$ there are no constants $c$ and $b$ with $\mathrm{PLRU}_4(\sigma) \le c \cdot \mathrm{OPT}_4(\sigma) + b$ for all $\sigma$.

*Proof.* Let $\sigma_r$ be $a, b, c, d, e$ followed by $r$ copies of $P = a, b, c, a, b, d$. We follow the bits $b[1], b[2], b[3]$ of the rule.

The first $11$ accesses are traced in the example table of the main page. They give $8$ misses and end in the state: ways $e, b, a, d$ and bits $0, 0, 0$. Call this state $S$. From $S$, one copy of $P$ goes as follows.

| access | result | ways after | bits after |
|---|---|---|---|
| a | hit (way 2) | e, b, a, d | 0, 0, 1 |
| b | hit (way 1) | e, b, a, d | 1, 0, 1 |
| c | miss, the bits point to way 3, evict d | e, b, a, c | 0, 0, 0 |
| a | hit (way 2) | e, b, a, c | 0, 0, 1 |
| b | hit (way 1) | e, b, a, c | 1, 0, 1 |
| d | miss, the bits point to way 3, evict c | e, b, a, d | 0, 0, 0 |

Each bit after an access follows from line L7: a touch of way 2 sets $b[1] = 0$ and $b[3] = 1$; a touch of way 1 sets $b[1] = 1$ and $b[2] = 0$; a touch of way 3 sets $b[1] = 0$ and $b[3] = 0$. The copy ends in the state $S$ again, with $2$ misses. By induction, $\mathrm{PLRU}_4(\sigma_r) = 8 + 2(r - 1) = 6 + 2r$.

The offline optimum with $4$ ways can evict $e$ at the first miss after the prefix. It then holds $a, b, c, d$ and has no more misses. So $\mathrm{OPT}_4(\sigma_r) \le 5 + 1 = 6$ for all $r$. Then $6 + 2r \le 6c + b$ fails for large $r$, whatever $c$ and $b$ are. $\blacksquare$

The tests check Lemma 1 against an independent model that compares touch times, Theorem 1 for $2$ to $16$ ways on random sequences, Corollary 2 for $k = 2$ (where PLRU is LRU), the example of Section 2.2.6 of Reineke's dissertation, and the counts of Theorem 3.
