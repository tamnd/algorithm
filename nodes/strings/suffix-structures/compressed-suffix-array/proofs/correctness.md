---
title: Lookup, extraction and search on the compressed suffix array are correct
proves: [correctness, termination, time.worst]
status: full
---

**Notation.** $T = T[0 \ldots n-1]$ has symbols coded $1, \ldots, \sigma$; $T' = T\$$ with $\$ = 0$ unique and smallest. Positions and rows are 0-based, $T'_p = T'[p \ldots n]$, $SA$ is the suffix array of $T'$ and $ISA$ its inverse. $F(i) = T'[SA[i]]$, $\Psi(i) = ISA[(SA[i] + 1) \bmod (n + 1)]$ and $V(i) = F(i)(n + 1) + \Psi(i)$. A position is *sampled* if it is a multiple of $s$ or equals $n$. Since $\$$ is unique and smallest, different suffixes of $T'$ differ at some position, and none is a prefix of another.

**Lemma 1 ($\Psi$ steps).** If $SA[i] < n$, then $SA[\Psi(i)] = SA[i] + 1$. So for $0 \le j \le n - SA[i]$, $F(\Psi^j(i)) = T'[SA[i] + j]$.

*Proof.* The first claim is the definition, since $SA[i] + 1 \le n$. The second follows by induction on $j$. $\square$

**Lemma 2 (monotone blocks).** If $i < j$ and $F(i) = F(j) = c \ne \$$, then $\Psi(i) < \Psi(j)$. Hence $V$ is strictly increasing over the rows $0, \ldots, n$.

*Proof.* $T'_{SA[i]} = c\,T'_{SA[i]+1}$ and $T'_{SA[j]} = c\,T'_{SA[j]+1}$, and the first is smaller, so $T'_{SA[i]+1} < T'_{SA[j]+1}$: their rows satisfy $\Psi(i) < \Psi(j)$. The symbol $\$$ is at row 0 only. Since $F$ is nondecreasing in $i$ (the suffixes are sorted by their first symbol first) and $0 \le \Psi(i) \le n$, the value $F(i)(n+1) + \Psi(i)$ increases strictly: within a block by the first part, and across blocks because $F$ grows by at least 1, which adds at least $n + 1 > \Psi(i) - \Psi(i')$. $\square$

So all gaps $V(i) - V(i-1)$ are positive and have gamma codes, and decoding the sample of the block of $i$ plus $i \bmod b$ gaps gives $V(i)$, from which $\Psi(i) = V(i) \bmod (n + 1)$ and $F(i) = \lfloor V(i)/(n+1) \rfloor$.

**Theorem 1 (lookup).** CSA-LOOKUP$(i)$ returns $SA[i]$ after at most $s - 1$ steps of $\Psi$.

*Proof.* Let $i_0$ be the input row and $t$ the number of steps taken. Invariant: $SA[i] = SA[i_0] + t$. It holds with $t = 0$. If $SA[i]$ is not sampled, then $SA[i] < n$, because $n$ is sampled, so by Lemma 1 the step $i \gets \Psi(i)$ gives $SA[\Psi(i)] = SA[i] + 1$, and the invariant holds with $t + 1$. The positions $SA[i_0], SA[i_0] + 1, \ldots$ reach a multiple of $s$ or $n$ within $s - 1$ steps, so the loop stops after at most $s - 1$ steps. At that point the stored sample is $SA[i]$, and the result $SA[i] - t$ equals $SA[i_0]$. $\square$

**Theorem 2 (inverse and extract).** `inverse(p)` returns $ISA[p]$, and `extract(l, r)` returns $T[l \ldots r-1]$.

*Proof.* Let $q = \lfloor p/s \rfloor s \le p$. The stored row is $ISA[q]$, and by Lemma 1 each of the $p - q$ steps moves from the row of position $q + j$ to that of $q + j + 1$, as $q + j < p \le n$. For extract, start at the row of $l$; by Lemma 1, the $j$-th output is $F(\Psi^j(ISA[l])) = T'[l + j]$, for $j < r - l$, and $l + j < r \le n$, so it is a symbol of $T$. $\square$

**Theorem 3 (search).** COMPARE$(i, P)$ returns the sign of the comparison of $T'_{SA[i]}[0 \ldots m-1]$ with $P$ (0 when $P$ is a prefix of the suffix), and CSA-FIND$(P)$ returns the rows of the suffixes that start with $P$.

*Proof.* By Lemma 1, the loop reads $T'[SA[i]], T'[SA[i] + 1], \ldots$ while they equal $P$. The suffix cannot run out before a difference is found, because its last symbol is $\$$, which differs from every symbol of $P$; so every step before a difference has $SA[\Psi^j(i)] < n$ and Lemma 1 applies. The first difference decides the order, and if there is none, $P$ is a prefix. Since the suffixes are sorted, the sign of COMPARE is nondecreasing in $i$: all rows with sign $-1$, then all with 0, then all with $+1$. The first binary search finds the first row with sign at least 0, the second the first row with sign $+1$, so the range between them is the set of rows with sign 0. $\square$

**Time.** A $\Psi$ or $F$ value costs at most $b - 1$ gamma decodes. Lookup and inverse take at most $s - 1$ such steps; extract takes $s - 1 + r - l$; each COMPARE takes at most $m$ steps, and the two binary searches $O(\log n)$ comparisons. All loops are bounded, so every operation terminates. With a structure that gives $\Psi$ in $O(1)$ time, the costs are $O(s)$, $O(s + r - l)$ and $O(m \log n)$. $\blacksquare$
