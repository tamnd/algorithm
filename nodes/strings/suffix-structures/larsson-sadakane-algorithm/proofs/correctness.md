---
title: Larsson-Sadakane suffix sorting is correct and ends after O(log n) passes
proves: [correctness, termination]
status: full
---

**Notation.** $T = T[0 \ldots n-1]$ with $n \ge 1$, 0-based, no sentinel, and $T_i = T[i \ldots n-1]$. The order of strings is lexicographic, with a proper prefix before the longer string. The algorithm keeps a permutation $I$ of the positions (the array `sa`), and a partition of the ranks $0, \ldots, n-1$ into consecutive blocks, the *groups*. For a position $x$, $V[x]$ is the last rank of the group that holds $x$. A group of size 1 is *sorted*.

**Invariant.** At the start of each pass with the value $h$:

> **(A)** For ranks $r < r'$ in different groups, $T_{I[r]} < T_{I[r']}$.
>
> **(B)** The positions of one group all have the same prefix of length $h$; in particular each of their suffixes has length at least $h$.
>
> **(C)** $V[I[r]]$ is the last rank of the group of $r$.

From (A) and (C), $V[x] < V[y]$ implies $T_x < T_y$. From (B) and (C), $V[x] = V[y]$ implies that $T_x$ and $T_y$ share a prefix of length $h$.

**Lemma 1 (keys).** At any moment during a pass with the value $h$, (A) and (C) hold, and each group shares a prefix of length at least $h$.

*Proof.* A split replaces a group by subgroups in consecutive ranks and gives each subgroup the number of its last rank, so (C) holds after each split. We show below that the subgroups are ordered by their suffixes, so (A) holds after each split. A subgroup is a subset of a group, so its members still share a prefix of length $h$. $\square$

**Lemma 2 (one split).** Let $G = I[s \ldots e-1]$ be a group that is split during the pass with the value $h$. For $x \in G$, let $key(x) = V[x + h]$ if $x + h < n$ and $-1$ otherwise, read at the moment the split of $G$ starts. Then for $x, y \in G$: if $key(x) < key(y)$, then $T_x < T_y$; and if $key(x) = key(y)$, then $T_x$ and $T_y$ share a prefix of length $2h$.

*Proof.* By Lemma 1, $x$ and $y$ share a prefix $u$ of length $h$, so $T_x = u\,T_{x+h}$ and $T_y = u\,T_{y+h}$, and $T_x < T_y$ if and only if $T_{x+h} < T_{y+h}$, where $T_n$ is the empty string. If $key(x) = -1$, then $T_{x+h}$ is empty and $T_x = u$ is a proper prefix of $T_y$, unless $y = x$; only one member of $G$ can have $x + h = n$, because the suffix lengths differ. So $key(x) < key(y)$ with $key(x) = -1$ gives $T_x < T_y$. If both keys are at least 0, then by Lemma 1 at the moment of reading, $V[x + h] < V[y + h]$ implies $T_{x+h} < T_{y+h}$, and $V[x + h] = V[y + h]$ implies that $T_{x+h}$ and $T_{y+h}$ share a prefix of length $h$, so $T_x$ and $T_y$ share a prefix of length $2h$. $\square$

The ternary-split quicksort sorts $G$ by $key$ and makes each block of equal keys a subgroup. By Lemma 2 the subgroups are in the order of their suffixes, so (A) holds after the split, and each subgroup shares a prefix of length $2h$.

**Theorem 1 (pass).** If (A), (B) and (C) hold at the start of a pass with the value $h$, they hold at the start of the next pass with the value $2h$.

*Proof.* The pass walks over all ranks. The sorted runs are skipped; they consist of groups of size 1, for which (B) holds for every length. Every group that is not sorted is split once, and by Lemma 2 each of its subgroups shares a prefix of length $2h$. Lemma 1 gives (A) and (C). So (B) holds for $2h$. $\square$

**Initialization.** Line L2 sorts the positions by their first symbol and makes each block of equal symbols a group numbered by its last rank. (A) holds for different first symbols, (B) holds for $h = 1$, and (C) holds by construction.

**Theorem 2 (result and termination).** The algorithm ends after at most $\lceil \log_2 n \rceil + 1$ passes, and then $I$ is the suffix array and $V$ is its inverse.

*Proof.* By (B), after the passes with $h = 1, 2, \ldots, 2^k$, each group shares a prefix of length $2^{k+1}$. Two different suffixes cannot share a prefix of length $n$, since only $T_0$ has length $n$. So once $2^{k+1} \ge n$, all groups have size 1, and the next pass finds no unsorted group and returns (line L9). When all groups have size 1, (A) says that $I$ lists the suffixes in increasing order, and (C) says that $V[I[r]] = r$. $\blacksquare$
