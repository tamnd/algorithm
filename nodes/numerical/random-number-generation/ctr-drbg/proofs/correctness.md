---
title: CTR_DRBG generate encrypts consecutive counters under one key, never repeats a counter within a call, and leaves the specified new state
proves: [correctness]
status: full
---

We use the pseudocode of the page with AES and a full-width counter, $\mathit{blocklen} = 128$, $\mathit{seedlen} = \mathit{keylen} + 128$, and $u = \lceil \mathit{seedlen} / 128 \rceil$, which is 2 for AES-128 and 3 for AES-192 and AES-256. Assume $c \le \mathit{reseed\_interval}$ and $n \le 2^{19}$, and let $m = \lceil n / 128 \rceil$. Write $E_K$ for AES encryption under $K$ and read $V$ as an integer modulo $2^{128}$.

**Lemma 1 (Update).** $\mathrm{UPDATE}(d, K, V)$ encrypts the $u$ counters $V+1, \ldots, V+u$ under $K$, and returns $(K^+, V^+)$ with $K^+ \| V^+ = \mathrm{left}_{\mathit{seedlen}}(E_K(V+1) \| \cdots \| E_K(V+u)) \oplus d$.

*Proof.* The loop in Update increments $V$ before each encryption and stops when at least $\mathit{seedlen}$ bits are collected, which takes $u$ passes. The split is by definition. $\square$

**Lemma 2 (output).** Let $(K', V')$ be the state after line L2, and let $a'$ be the value of $a$ after line L2 ($\mathit{seedlen}$ bits in every branch). The loop L4 and L5 runs exactly $m$ times, and on exit $W = E_{K'}(V'+1) \| \cdots \| E_{K'}(V'+m)$ and the counter is $V'+m$.

*Proof.* By induction on the number $j$ of passes: after $j$ passes the counter is $V'+j$ and $W$ is the concatenation of the first $j$ encryptions, with $|W| = 128 j$. The key does not change in the loop. The condition $|W| < n$ holds exactly for $j < m$. $\square$

**Lemma 3 (new state).** After lines L6 and L7 the state is $(K'', V'', c+1)$ with $K'' \| V'' = \mathrm{left}_{\mathit{seedlen}}(E_{K'}(V'+m+1) \| \cdots \| E_{K'}(V'+m+u)) \oplus a'$.

*Proof.* Lemma 1 applied at line L6 to the state $(K', V'+m)$ and data $a'$. $\square$

**Lemma 4 (distinct counters).** The $m + u$ counters encrypted under $K'$ in one call, $V'+1, \ldots, V'+m+u$, are pairwise distinct, so the $m + u$ encrypted blocks are pairwise distinct.

*Proof.* $m + u \le 2^{12} + 3 < 2^{128}$, so these are distinct residues modulo $2^{128}$, and $E_{K'}$ is a permutation. $\square$

Lemma 4 is the structural fact behind the security argument: under the PRP assumption the $m$ output blocks and the $u$ blocks that form the next state are $m + u$ distinct pseudorandom blocks, and the next state is computed only from the $u$ blocks that are never output.

**Theorem.** CTR-DRBG-GENERATE returns the leftmost $n$ bits of $E_{K'}(V'+1) \| \cdots \| E_{K'}(V'+m)$ and leaves the state $(K'', V'', c+1)$ of Lemma 3. This is the generate process of SP 800-90A Rev. 1, Section 10.2.1.5.1 (without the derivation function) and 10.2.1.5.2 (with it), with $\mathit{ctr\_len} = \mathit{blocklen}$. Line L1 rejects the call exactly when $c$ exceeds the reseed interval.

*Proof.* Lemmas 2 and 3, and line L8. In the specification, empty additional input is replaced by $0^{\mathit{seedlen}}$ and no Update is done at the start, which is the else branch of line L2; nonempty input is transformed once (by Block_Cipher_df or by zero padding) and the same value is used in both Updates, as at lines L2 and L6. $\square$

**Remark (prediction resistance).** With prediction resistance requested, the implementation first reseeds with the fresh entropy and $a$ and then runs the theorem's computation with empty additional input, as in SP 800-90A, Section 9.3.1. The CAVP vectors with prediction resistance in the tests check this composition. $\blacksquare$
