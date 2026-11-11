---
title: scrypt computes RFC 7914, and less memory for ROMix costs proportionally more time
proves: [correctness]
status: full
---

We use the notation of the page. Write $H$ for BLOCKMIX, so line L4 computes $V_i = H^i(B)$ for $0 \le i < N$ and $X_0 = H^N(B)$, and line L5 computes $X_{t+1} = H(X_t \oplus V_{j_t})$ with $j_t = \mathrm{INTEGERIFY}(X_t) \bmod N$.

**Theorem 1 (the code computes scrypt).** Each function of the code computes the step of RFC 7914 with the same name: `salsa20_8` is Section 3, `block_mix` is Section 4, `ro_mix` is Section 5, and `scrypt` is Section 6.

*Proof.* `salsa20_8` applies, four times, the column quarter rounds on the index groups (0, 4, 8, 12), (5, 9, 13, 1), (10, 14, 2, 6), (15, 3, 7, 11) and then the row quarter rounds on (0, 1, 2, 3), (5, 6, 7, 4), (10, 11, 8, 9), (15, 12, 13, 14). For a group $(y_0, y_1, y_2, y_3)$ it sets $y_1 \mathrel{\oplus}= (y_0 + y_3) \lll 7$, $y_2 \mathrel{\oplus}= (y_1 + y_0) \lll 9$, $y_3 \mathrel{\oplus}= (y_2 + y_1) \lll 13$, $y_0 \mathrel{\oplus}= (y_3 + y_2) \lll 18$. Writing these out gives exactly the 32 lines of the C code of Section 3, in the same order, and the final addition of the input is the last loop of that code. The other functions follow the numbered steps of their sections with the same loop bounds and the same order of output chunks. $\blacksquare$

The tests confirm Theorem 1 on the vectors of Sections 8 to 12.

**Lemma 2 (the low memory trade-off).** Let an algorithm store $V_c$ for every multiple $c$ of $k$, and rebuild $V_j$ from $V_{j - (j \bmod k)}$ when line L5 needs it. Then it uses $\lceil N / k \rceil$ stored blocks and at most $2N + N(k - 1)$ calls to $H$, and it gives the same output as ROMix.

*Proof.* $H^{j \bmod k}(V_{j - (j \bmod k)}) = H^j(B) = V_j$, so every value read in line L5 is correct, and the output is the same. Line L4 costs $N$ calls. Each of the $N$ steps of line L5 costs one call plus $j_t \bmod k \le k - 1$ calls to rebuild $V_{j_t}$. If the indices are uniform, the expected extra cost is $N (k - 1) / 2$. $\square$

So an attacker can trade memory for time with a constant product: memory $N / k$ blocks and time about $N k / 2$ calls. The next result says it cannot do much better.

**Theorem 3 (Percival, 2009, Lemma 1 and Theorem 1, sketched).** Model $H$ as a random oracle on $k$-bit values. Let an algorithm keep an advice string of $kM$ bits about the chain, and then, for an index $x$ chosen uniformly from $0, \ldots, N - 1$, compute $H^x(B)$ with $M$ oracle calls in parallel per time unit. If the chain values are distinct and $N < 2^{k/8}$, its expected time is at least $N / (4M + 2) - 1/2$ (Lemma 1 of the paper). So the $N$ steps of line L5 take time $\Omega(N^2 / M)$, and space times time is $\Omega(N^2)$ (Theorem 1 of the paper).

*Sketch.* Since $H$ is a random oracle, $H^x(B)$ is unpredictable until $H$ has been queried at $H^{x-1}(B)$, so the only way to get it is to start from some chain value that can be read off the advice and apply $H$ to it. An advice string of $kM$ bits can fix only a small number of chain values, of order $M$, and from each one the algorithm moves forward at most one step per time unit. For a uniform $x$, the distance back to the nearest value the advice gives is then of order $N / M$ on average. Each step of line L5 needs a fresh index, because $j_t$ comes from the random oracle output $X_t$, which the algorithm cannot predict before it computes $X_t$. Summing over the $N$ steps gives the bound. Percival remarks that he believes the right bound is $N / (2M) - 1/2$, but that this is hard to prove. $\square$

**Remarks on the model.** Theorem 3 bounds the product of peak space and time for one evaluation. An attacker with many cores pays instead for the memory in use at every step, summed over the computation: the cumulative memory complexity (CMC). Alwen, Chen, Pietrzak, Reyzin and Tessaro (EUROCRYPT 2017) proved that the CMC of scrypt in the parallel random oracle model is $\Omega(N^2 w)$ for blocks of $w$ bits. Since the honest algorithm keeps about $N w$ bits for about $2N$ steps, the bound is tight up to a constant. Their proof is long and is not reproduced here.

**Theorem 4 (pseudorandom output).** If HMAC-SHA256 is a pseudorandom function keyed by $P$, then for a password of enough min-entropy the output of line L3 is indistinguishable from random for an adversary that cannot guess $P$. Line L3 is PBKDF2 with the key $P$, so this follows from the PBKDF2 result; see the [PBKDF2 page](/pbkdf2/). The memory hardness above concerns the cost of each guess, not this indistinguishability. $\blacksquare$
