---
title: Berlekamp-Massey returns a shortest LFSR for the sequence
proves: [correctness, optimality, termination]
status: full
---

We use the pseudocode of the page. All arithmetic is in a field $F$. An LFSR $(L, C)$ has $L \ge 0$ and $C(x) = \sum_{i=0}^{L} c_i x^i$ with $c_0 = 1$. It generates $s_0, \ldots, s_{N-1}$ if

$$\sum_{i=0}^{L} c_i s_{j-i} = 0 \qquad \text{for all } j \text{ with } L \le j < N. \tag{1}$$

The *discrepancy* of $(L, C)$ at $j$ is $\sum_{i=0}^{L} c_i s_{j-i}$, for $j \ge L$. Write $L_N$ for the linear complexity of $s_0, \ldots, s_{N-1}$, the least $L$ such that some LFSR of length $L$ generates it. Any $(L, C)$ with $L \ge N$ generates it, because (1) is empty, so $L_N \le N$. A register that generates $s_0, \ldots, s_N$ also generates $s_0, \ldots, s_{N-1}$, so $L_N \le L_{N+1}$.

**Lemma 1 (Massey).** Let $(L, C)$ generate $s_0, \ldots, s_{N-1}$ but not $s_0, \ldots, s_N$. Then every LFSR $(L', C')$ that generates $s_0, \ldots, s_N$ has $L' \ge N + 1 - L$.

*Proof.* Since $(L, C)$ fails at $N$, the discrepancy at $N$ is defined, so $L \le N$, and $d = \sum_{i=0}^{L} c_i s_{N-i} \ne 0$. Suppose that $L' \le N - L$. For $0 \le i \le L$ we have $N - i \ge N - L \ge L'$, so (1) for $(L', C')$ at $j = N - i \le N$ gives $s_{N-i} = -\sum_{k=1}^{L'} c'_k s_{N-i-k}$. All indices are at least $N - L - L' \ge 0$. So

$$d = \sum_{i=0}^{L} c_i s_{N-i} = -\sum_{k=1}^{L'} c'_k \sum_{i=0}^{L} c_i s_{(N-k)-i}.$$

For $1 \le k \le L'$ we have $L \le N - L' \le N - k \le N - 1$, so the inner sum is the discrepancy of $(L, C)$ at $N - k$, which is 0 by (1). Hence $d = 0$, a contradiction. So $L' \ge N + 1 - L$. $\square$

**Corollary 2.** If $(L, C)$ is a shortest LFSR for $s_0, \ldots, s_{N-1}$ (so $L = L_N$) and it fails at $N$, then $L_{N+1} \ge \max(L_N, N + 1 - L_N)$.

*Proof.* $L_{N+1} \ge L_N$ always, and $L_{N+1} \ge N + 1 - L_N$ by Lemma 1. $\square$

**The update step.** Let $(L, C)$ generate $s_0, \ldots, s_{r-1}$ with discrepancy $d \ne 0$ at $r$. Let $(L_0, B)$ generate $s_0, \ldots, s_{r_0 - 1}$, where $r_0 < r$, with discrepancy $b \ne 0$ at $r_0$, and let $L = r_0 + 1 - L_0$ and $m = r - r_0$. Put

$$C^*(x) = C(x) - \frac{d}{b}\, x^m B(x), \qquad L^* = \max(L, r + 1 - L).$$

**Lemma 3.** $(L^*, C^*)$ is an LFSR that generates $s_0, \ldots, s_r$.

*Proof.* The constant term of $C^*$ is $c_0 = 1$, since $m \ge 1$. Its degree is at most $\max(L, m + L_0) = \max(L, r - r_0 + L_0) = \max(L, r + 1 - L) = L^*$. Let $L^* \le j \le r$. The coefficient of $x^i$ in $x^m B(x)$ is $b_{i-m}$, so

$$\sum_{i} c^*_i s_{j-i} = \sum_{i=0}^{L} c_i s_{j-i} - \frac{d}{b} \sum_{i=0}^{L_0} b_i s_{(j-m)-i}.$$

The first sum is 0 for $L \le j < r$ and $d$ for $j = r$. In the second sum, $j - m \ge r + 1 - L - m = r_0 + 1 - L = L_0$, so it is the discrepancy of $(L_0, B)$ at $j - m$. That is 0 for $j - m < r_0$, that is $j < r$, and $b$ for $j = r$. So the total is 0 for $j < r$ and $d - (d/b) b = 0$ for $j = r$. $\square$

**The start.** Before the first nonzero term, the algorithm has $L = 0$ and $C = 1$. While $s_0 = \cdots = s_{r-1} = 0$, the register $(0, 1)$ generates the prefix, and it is shortest. Let $s_r$ be the first nonzero term. Then $d = s_r$, $2L = 0 \le r$, and line L7 gives $C = 1 - s_r x^{m}$ with $m = r + 1$, since line L4 has added 1 to $m$ for each of the $r$ zero terms. Line L8 sets $L = r + 1$. Any register of length $L$ generates a prefix of length $L$, so $(r + 1, C)$ generates $s_0, \ldots, s_r$. It is shortest: a register of length $L' \le r$ would give $s_r = -\sum_{k=1}^{L'} c'_k s_{r-k} = 0$. After line L8, $B = 1$ is the register $(0, 1)$, which generates $s_0, \ldots, s_{r-1}$ and fails at $r$ with discrepancy $b = s_r$. Put $r_0 = r$ and $L_0 = 0$; then $L = r_0 + 1 - L_0$ and $m = 1 = (r + 1) - r_0$.

**Invariant.** After the first nonzero term, at the start of each step $r$ of line L2:

- (I1) $(L, C)$ generates $s_0, \ldots, s_{r-1}$ and $L = L_r$;
- (I2) there are $r_0 < r$ and $L_0 = L_{r_0}$ such that $(L_0, B)$ generates $s_0, \ldots, s_{r_0 - 1}$ with discrepancy $b \ne 0$ at $r_0$, $L = r_0 + 1 - L_0$, and $m = r - r_0$.

The start shows that (I1) and (I2) hold at step $r + 1$ after the first nonzero term $s_r$. Assume they hold at step $r$.

*Case $d = 0$ (line L4).* $(L, C)$ also generates $s_0, \ldots, s_r$, so $L_{r+1} \le L = L_r \le L_{r+1}$, and (I1) holds at $r + 1$. $B$, $b$, $r_0$ and $L$ do not change, and $m$ grows by 1, so (I2) holds.

*Case $d \ne 0$ and $2L > r$ (lines L10, L11).* Then $r + 1 - L \le L$, so $L^* = L$. By Lemma 3 with (I2), $(L, C^*)$ generates $s_0, \ldots, s_r$. So $L_{r+1} \le L = L_r \le L_{r+1}$, and (I1) holds. (I2) holds as in the first case.

*Case $d \ne 0$ and $2L \le r$ (lines L6 to L8).* Then $L^* = r + 1 - L$. By Lemma 3, $(L^*, C^*)$ generates $s_0, \ldots, s_r$, so $L_{r+1} \le r + 1 - L$. By (I1), $(L, C)$ is shortest for $s_0, \ldots, s_{r-1}$ and fails at $r$, so Corollary 2 gives $L_{r+1} \ge r + 1 - L$. So the new $L = r + 1 - L = L_{r+1}$, and (I1) holds. Line L8 sets $B$ to the old $C$, $b = d$, and $m = 1$. With $r_0 := r$ and $L_0 := L_r$ (the old $L$), the old register generates $s_0, \ldots, s_{r-1}$ with discrepancy $d \ne 0$ at $r$, the new $L$ is $r_0 + 1 - L_0$, and $m = (r + 1) - r_0$. So (I2) holds.

**Termination and result.** The loop of line L2 runs $n$ times, and each step does a bounded number of polynomial operations. If the sequence is all zero, the algorithm returns $(0, 1)$, which is shortest. Otherwise, after step $n - 1$, (I1) gives that $(L, C)$ generates $s_0, \ldots, s_{n-1}$ and $L = L_n$. Lemma 3 also shows $\deg C \le L$ at each step. So line L12 returns a shortest LFSR.

**The profile rule.** The three cases show $L_{r+1} = L_r$ when $d = 0$ and $L_{r+1} = \max(L_r, r + 1 - L_r)$ when $d \ne 0$. $\blacksquare$
