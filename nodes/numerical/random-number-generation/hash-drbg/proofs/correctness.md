---
title: Hash_DRBG generate returns the hashes of consecutive counter values and performs the specified state update, with distinct hash inputs
proves: [correctness]
status: full
---

We use the pseudocode of the page. Let $N = 2^{\mathit{seedlen}}$, let $\mathrm{Hash}$ have output length $\mathit{outlen}$, and identify an integer in $[0, N)$ with its $\mathit{seedlen}$-bit big-endian string. Assume $c \le \mathit{reseed\_interval}$ and $n \le 2^{19}$.

**Lemma 1 (additional input).** After line L2, $V' = V$ if $a$ is empty, and $V' = (V + \mathrm{Hash}(\texttt{02} \| V \| a)) \bmod N$ otherwise, where $\mathrm{Hash}$ outputs are read as integers.

*Proof.* Direct from line L2. $\square$

**Lemma 2 (output).** Let $m = \lceil n / \mathit{outlen} \rceil$. The loop L4 and L5 runs exactly $m$ times, and on exit $W = \mathrm{Hash}(V') \| \mathrm{Hash}(V' + 1) \| \cdots \| \mathrm{Hash}(V' + m - 1)$, with the arguments reduced modulo $N$.

*Proof.* By induction on the number $j$ of completed passes: after $j$ passes, $|W| = j \cdot \mathit{outlen}$ and $\mathit{data} = (V' + j) \bmod N$, and $W$ is the concatenation of the first $j$ hashes. Line L3 gives $j = 0$. A pass appends $\mathrm{Hash}(V' + j)$ and increments $\mathit{data}$. The loop condition $|W| < n$ holds exactly for $j \cdot \mathit{outlen} < n$, that is, for $j < m$. $\square$

**Lemma 3 (distinct inputs).** The $m$ hash inputs of Lemma 2 are pairwise distinct strings, and each differs from the inputs $\texttt{02} \| V \| a$ (if any) and $\texttt{03} \| V'$ of the same call.

*Proof.* $m \le n \le 2^{19} < N$ (as $\mathit{seedlen} \ge 440$), so $V', V'+1, \ldots, V'+m-1$ are distinct residues modulo $N$, hence distinct $\mathit{seedlen}$-bit strings. The other two inputs have length at least $\mathit{seedlen} + 8$ bits, so they differ from every output input by length. $\square$

**Lemma 4 (update).** After lines L6 to L8, $V'' = (V' + \mathrm{Hash}(\texttt{03} \| V') + C + c) \bmod N$, $C$ is unchanged, and the counter is $c + 1$.

*Proof.* Line L6 reads $V$, which equals $V'$ at that point: line L3 copied $V$ into $\mathit{data}$, and only $\mathit{data}$ changed in the loop. Lines L7 and L8 apply the update. $\square$

**Theorem.** HASH-DRBG-GENERATE returns the leftmost $n$ bits of $\mathrm{Hash}(V') \| \cdots \| \mathrm{Hash}(V' + m - 1)$ and leaves the state $(V'', C, c + 1)$, which is the generate process of SP 800-90A Rev. 1, Section 10.1.1.4. Line L1 rejects the call exactly when $c$ exceeds the reseed interval.

*Proof.* Lemmas 1, 2 and 4, and line L9. $\square$

**Remark (prediction resistance).** With prediction resistance requested, the implementation calls reseed with the fresh entropy and $a$, which sets $V \leftarrow \mathrm{Hash\_df}(\texttt{01} \| V \| e \| a)$, $C \leftarrow \mathrm{Hash\_df}(\texttt{00} \| V)$ and $c \leftarrow 1$, and then runs the theorem's computation with empty additional input, as in SP 800-90A, Section 9.3.1. The CAVP vector with prediction resistance in the tests checks this composition. $\blacksquare$
