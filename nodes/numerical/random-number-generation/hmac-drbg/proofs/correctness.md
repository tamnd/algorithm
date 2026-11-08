---
title: HMAC_DRBG generate returns the HMAC chain from the updated state and leaves the specified new state
proves: [correctness]
status: full
---

We use the pseudocode of the page and the definition of Update given there. Assume $c \le \mathit{reseed\_interval}$ and $n \le 2^{19}$, and let $m = \lceil n / \mathit{outlen} \rceil$.

**Lemma 1 (Update).** For empty data, Update performs exactly one round: $K_1 = \mathrm{HMAC}(K, V \| \texttt{00})$ and $V_1 = \mathrm{HMAC}(K_1, V)$. For nonempty $d$, it performs two rounds, the second with separator $\texttt{01}$.

*Proof.* Steps 1 to 3 of Update, with the early stop at step 2. $\square$

**Lemma 2 (output chain).** Let $(K', V')$ be the state after line L2: $(K', V') = (K, V)$ if $a$ is empty and $\mathrm{UPDATE}(a, K, V)$ otherwise. Then the loop L4 and L5 runs exactly $m$ times, and on exit $W = V_1 \| \cdots \| V_m$ with $V_0 = V'$ and $V_j = \mathrm{HMAC}(K', V_{j-1})$, and the current value is $V_m$.

*Proof.* By induction on the number $j$ of passes: after $j$ passes the value is $V_j$ and $W = V_1 \| \cdots \| V_j$, with $|W| = j \cdot \mathit{outlen}$. The key is not changed inside the loop. The loop condition $|W| < n$ holds exactly for $j < m$. $\square$

**Lemma 3 (new state).** After line L6 the state is $\mathrm{UPDATE}(a, K', V_m)$, and after L7 the counter is $c + 1$. In particular the new key is $\mathrm{HMAC}(K', V_m \| \texttt{00} \| a)$ followed, if $a$ is nonempty, by a second round.

*Proof.* Direct from lines L6 and L7 and Lemma 1. $\square$

**Lemma 4 (distinct HMAC inputs under $K'$).** The inputs to $\mathrm{HMAC}(K', \cdot)$ in one call are $V_0, \ldots, V_{m-1}$ (each $\mathit{outlen}$ bits) and $V_m \| \texttt{00} \| a$ (at least $\mathit{outlen} + 8$ bits). The last differs from all the others by length. The first $m$ are pairwise distinct unless the chain $V_j$ repeats.

*Proof.* Immediate from Lemmas 2 and 3. A repeat $V_i = V_j$ with $i < j \le m - 1$ is the only way two of the first $m$ inputs coincide. $\square$

Lemma 4 is the structural fact behind the security argument: if $\mathrm{HMAC}(K', \cdot)$ is replaced by a random function, each $V_j$ is uniform and independent of the earlier ones as long as no input repeats, so a repeat occurs with probability at most $\binom{m}{2} 2^{-\mathit{outlen}}$.

**Theorem.** HMAC-DRBG-GENERATE returns the leftmost $n$ bits of $V_1 \| \cdots \| V_m$ and leaves the state $(\mathrm{UPDATE}(a, K', V_m), c + 1)$, which is the generate process of SP 800-90A Rev. 1, Section 10.1.2.5. Line L1 rejects the call exactly when $c$ exceeds the reseed interval.

*Proof.* Lemmas 2 and 3, and line L8. $\square$

**Remark (RFC 6979).** In RFC 6979, Section 3.2, steps b to f are Instantiate with entropy input $\mathrm{int2octets}(x)$ and nonce $\mathrm{bits2octets}(h)$ (both of length $\lceil \mathit{qlen}/8 \rceil$ bytes), with no personalization string. Step h computes $T$ by the loop of lines L4 and L5 and, when the candidate is rejected, sets $K \leftarrow \mathrm{HMAC}(K, V \| \texttt{00})$ and $V \leftarrow \mathrm{HMAC}(K, V)$, which is the empty-data Update of line L6 by Lemma 1. So the successive candidates are the leftmost $\mathit{qlen}$ bits of successive generate calls of $\lceil \mathit{qlen}/8 \rceil$ bytes, as in the implementation. The test vectors of Appendix A.2.5 confirm this. $\blacksquare$
