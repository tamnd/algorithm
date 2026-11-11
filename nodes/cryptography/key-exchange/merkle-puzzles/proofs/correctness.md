---
title: Alice and Bob agree with high probability, and the natural eavesdropper needs about NS/4 work
proves: [correctness]
status: full
---

We use the notation of the page. The marker $\mathrm{MAGIC}$ has $a$ bits and each identifier has $b$ bits. We model the puzzle cipher as follows: for each puzzle, the decryptions $D_r(P_j)$ under the keys $r \ne r_j$ are independent uniform strings, independent of everything else; this is the random oracle model for the keystream, which the toy cipher of the code follows with SHA-256. The decryption under $r_j$ gives the plaintext, since $D_{r_j}(E_{r_j}(M)) = M$ for an XOR keystream.

**Lemma 1 (Bob finds his puzzle).** Bob's loop in lines L6 and L7 returns $(\mathrm{id}_j, k_j)$ with probability at least $1 - S \cdot 2^{-a}$.

*Proof.* The loop tries $r = 0, 1, \dots, S - 1$ in order and $r_j$ is in this range, so it returns at $r_j$ at the latest, and the plaintext there is $\mathrm{MAGIC} \,\|\, \mathrm{id}_j \,\|\, k_j$. It returns a wrong pair only if some $r < r_j$ gives a decryption that begins with $\mathrm{MAGIC}$. For each such $r$ this has probability $2^{-a}$, and there are fewer than $S$ of them, so by the union bound the probability is at most $S \cdot 2^{-a}$. $\blacksquare$

**Lemma 2 (Alice finds the same key).** If the identifiers $\mathrm{id}_1, \dots, \mathrm{id}_N$ are distinct, then line L8 with $\mathrm{id} = \mathrm{id}_j$ gives $k = k_j$. The identifiers fail to be distinct with probability at most $\binom{N}{2} 2^{-b} < N^2 2^{-b - 1}$.

*Proof.* Line L3 stores $T[\mathrm{id}_i] \leftarrow k_i$ for each $i$. If the identifiers are distinct, no entry is overwritten, so $T[\mathrm{id}_j] = k_j$. Each of the $\binom{N}{2}$ pairs of uniform $b$-bit identifiers is equal with probability $2^{-b}$, and the union bound gives the second claim. $\blacksquare$

**Theorem 1 (agreement).** Alice and Bob end with the same key $k_j$ with probability at least $1 - S \cdot 2^{-a} - N^2 2^{-b - 1}$.

*Proof.* By Lemma 1, Bob holds $k_j$ and sends $\mathrm{id}_j$ unless the first bad event happens. By Lemma 2, Alice then gets $k_j$ unless the second bad event happens. The union bound gives the claim. In the code, $a = 64$, $b = 128$ and $N, S \le 2^{10}$, so the failure probability is below $2^{-50}$. $\blacksquare$

**Theorem 2 (the work of the honest parties).** Alice makes exactly $N$ cipher calls. Bob makes $r_j + 1$ calls, which is between 1 and $S$, and $(S + 1)/2$ on average.

*Proof.* Lines L1 to L3 encrypt once per puzzle. By Lemma 1 Bob stops at $r = r_j$ (in the good event), after $r_j + 1$ calls. Since $r_j$ is uniform on $\{0, \dots, S - 1\}$, the mean is $\frac{1}{S}\sum_{r=0}^{S-1}(r + 1) = (S + 1)/2$. $\blacksquare$

**Theorem 3 (the natural eavesdropper).** Eve sees the shuffled puzzles and $\mathrm{id}_j$, and opens the puzzles in a uniformly random order, each by Bob's loop, until she finds $\mathrm{id}_j$. Her expected number of cipher calls is $(N + 1)(S + 1)/4$.

*Proof.* Because Alice shuffles the puzzles and the identifiers are uniform and independent of the positions, the position of Bob's puzzle in Eve's order is uniform on $\{1, \dots, N\}$, so the number $J$ of puzzles she opens has mean $(N + 1)/2$. The puzzle keys $r_i$ are independent of the positions and of $J$, so by Theorem 2 each opened puzzle costs $(S + 1)/2$ calls on average. By Wald's identity (or by conditioning on $J$ and summing), her expected total is $\frac{N + 1}{2} \cdot \frac{S + 1}{2}$. $\blacksquare$

**Remark.** Theorem 3 is about one strategy. The general statement, that every eavesdropper needs about $N^2$ queries in the random oracle model when $S = N$, is the theorem of Biham, Goren and Ishai (2008) for their variant of the scheme, and the matching upper bound for every scheme is the theorem of Barak and Mahmoody (2009); we do not prove them here. $\blacksquare$
