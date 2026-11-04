---
title: A binary fuse filter accepts every key of its set
proves: [correctness, invariant, termination]
status: full
---

Let $S$ be a set of $n$ distinct keys and write $E(x) = \{h_0(x), h_1(x), h_2(x)\}$. Since $h_j(x)$ lies in segment $s(x) + j$, the three cells are distinct, and they lie in $\{0, \ldots, (t + 2)L - 1\}$ because $s(x) \le t - 1$.

**Lemma 1 (peeling order).** If PEEL$(S)$ succeeds, the order $(x_1, c_1), \ldots, (x_n, c_n)$ lists each key once, and for each $i$, $c_i \in E(x_i)$ and $c_i \notin E(x_{i'})$ for each $i' > i$.

*Proof.* Lines L7 and L10 keep, for each cell, the count and the xor of the indices of the keys that are not yet in the order and use it. When line L9 takes a cell with count 1, the xor is the index of the only such key, and the keys appended later were not yet in the order at that time, so they do not use the cell. $\square$

**Lemma 2.** In the loop of lines L4 and L5, cell $c_i$ is written only at step $i$, and after step $i$ no cell of $E(x_i)$ is written.

*Proof.* Step $i'$ writes only $c_{i'} \in E(x_{i'})$. For $i' > i$, $c_i \notin E(x_{i'})$, so $c_{i'} \ne c_i$. The steps after step $i$ are those with $i' < i$, and $c_{i'} \notin E(x_i)$ by Lemma 1, since $i > i'$. $\square$

**Theorem 1 (invariant (X)).** After BUILD, $B[h_0(x)] \oplus B[h_1(x)] \oplus B[h_2(x)] = \mathrm{fp}(x)$ for each $x \in S$, so QUERY returns true on $S$.

*Proof.* For $x = x_i$ with other cells $u, v$, line L5 makes $B[c_i] \oplus B[u] \oplus B[v] = \mathrm{fp}(x_i)$, and by Lemma 2 none of the three cells changes later. $\square$

**Lemma 3 (room).** If $n \ge 2$ and $L, t$ follow the size rule, then $(t + 2)(L - 1) \ge n$.

*Proof.* The rule gives $(t + 2)L \ge \lceil \text{capacity}/L \rceil L \ge \text{capacity} \ge n \phi - 1/2$, where $\phi = \max(1.125, 0.875 + 0.25 \ln(10^6)/\ln n)$ is the size factor. If $n \ge 9$, then $\ln 9/\ln 3.33 + 2.25 > 4$, so $L \ge 16$ and $(t + 2)(L - 1) \ge \tfrac{15}{16}(1.125 n - 1/2) \ge n$, since $0.0547 n \ge 0.47$ for $n \ge 9$. If $2 \le n \le 8$, then $L \ge 4$ and $\phi \ge 0.875 + 0.25 \cdot 13.81/\ln 8 > 2.5$, so $(t + 2)(L - 1) \ge \tfrac34 (2.5 n - 1/2) \ge n$. $\square$

**Theorem 2 (termination).** Under ideal hashing, with independent hash functions in each try, and $(t + 2)(L - 1) \ge n$ (true by Lemma 3 for the size rule and $n \ge 2$, and trivial for $n \le 1$, where at most one key has three cells of count 1), BUILD ends with probability 1, after a geometric number of tries.

*Proof.* Each try succeeds with the same probability $p$, independently, so it suffices to show $p > 0$. Reserve cell $jL$ of each segment $j$ as a spare. The other $(t + 2)(L - 1) \ge n$ cells can be given to the keys as distinct private cells. For a key with private cell $\pi$ in segment $j$, choose its start segment $s = \min(j, t - 1)$; then $j - s \in \{0, 1, 2\}$, because $j \le t + 1$. Let its cell in segment $j$ be $\pi$ and its cells in the other two segments of its window be their spares. Every private cell then has count 1, so every key is peeled from its private cell. This choice of the hash values has positive probability, so $p > 0$. Each try has $O(n + tL)$ steps, as for the xor filter. $\blacksquare$
