---
title: ChaCha20-Poly1305 decryption accepts exactly the outputs of encryption and releases nothing on failure
proves: [correctness]
status: full
---

Fix a key $K$. Write $\mathrm{CB}(j, N)$ for $\mathrm{CHACHA20\text{-}BLOCK}(K, j, N)$, lines L1 to L4, and $\mathrm{KS}(N, \ell)$ for the first $\ell$ bytes of $\mathrm{CB}(1, N) \| \mathrm{CB}(2, N) \| \cdots$. Write $\mathrm{otk}(N)$ for the first 32 bytes of $\mathrm{CB}(0, N)$, and $\mathrm{enc}(A, C) = A \| \mathrm{pad16}(A) \| C \| \mathrm{pad16}(C) \| \mathrm{le64}(|A|) \| \mathrm{le64}(|C|)$. Then $\mathrm{Enc}(N, A, P) = (C, T)$ with $C = P \oplus \mathrm{KS}(N, |P|)$ and $T = \mathrm{POLY1305}(\mathrm{otk}(N), \mathrm{enc}(A, C))$, lines L5 to L9, and $\mathrm{Dec}(N, A, C, T)$ is lines L10 to L13. All these maps are deterministic functions of their inputs and $K$. We take inputs within the limits of RFC 8439, Section 2.8: $|P| \le (2^{32} - 1) \cdot 64$ and $|A| < 2^{64}$, so the block counter never wraps and the two lengths fit in 64 bits.

**Lemma 1 (completeness).** For all $N$, $A$, $P$ within the limits, $\mathrm{Dec}(N, A, \mathrm{Enc}(N, A, P)) = P$.

*Proof.* Let $(C, T) = \mathrm{Enc}(N, A, P)$. L10 computes $\mathrm{otk}(N)$, the same value as L5, because $\mathrm{CB}$ is deterministic. L11 computes $T' = \mathrm{POLY1305}(\mathrm{otk}(N), \mathrm{enc}(A, C))$, the same expression as L8, so $T' = T$. The comparison at L12 reads equal strings and does not return. L13 returns $C \oplus \mathrm{KS}(N, |C|)$. Since $|C| = |P|$, this is $P \oplus \mathrm{KS}(N, |P|) \oplus \mathrm{KS}(N, |P|) = P$. $\square$

**Lemma 2 (the MAC input is injective).** If $\mathrm{enc}(A, C) = \mathrm{enc}(A', C')$, then $A = A'$ and $C = C'$.

*Proof.* Let $M = \mathrm{enc}(A, C)$. Its length is $|A| + \mathrm{pad}(|A|) + |C| + \mathrm{pad}(|C|) + 16$, a multiple of 16. Its last 16 bytes are $\mathrm{le64}(|A|) \| \mathrm{le64}(|C|)$, and $\mathrm{le64}$ is injective on $[0, 2^{64})$, so $M$ fixes $|A|$ and $|C|$. Then $A$ is the first $|A|$ bytes of $M$, and $C$ is the $|C|$ bytes that start at offset $|A| + \mathrm{pad}(|A|)$, where $\mathrm{pad}(x) = (-x) \bmod 16$. So $(A, C)$ is a function of $M$, and two pairs with the same $M$ are equal. $\square$

Lemma 2 is why the lengths block is needed. Without it, for any $X$ with $|X|$ a multiple of 16, the pairs $(X, \varepsilon)$ and $(\varepsilon, X)$ give the same string $X$, so a tag for one would be a tag for the other.

**Lemma 3 (canonical verification).** If $\mathrm{Dec}(N, A, C, T)$ returns a string $P$, then $(C, T) = \mathrm{Enc}(N, A, P)$.

*Proof.* $\mathrm{Dec}$ returns a string only at L13, so the condition $T' \ne T$ at L12 was false, which means $T = T' = \mathrm{POLY1305}(\mathrm{otk}(N), \mathrm{enc}(A, C))$. The output is $P = C \oplus \mathrm{KS}(N, |C|)$, so $|P| = |C|$ and $P \oplus \mathrm{KS}(N, |P|) = C$, because XOR with a fixed string is its own inverse. So the ciphertext part of $\mathrm{Enc}(N, A, P)$ is $C$, and its tag is $\mathrm{POLY1305}(\mathrm{otk}(N), \mathrm{enc}(A, C)) = T$. $\square$

By Lemmas 1 and 3, $\mathrm{Dec}$ accepts $(N, A, C, T)$ exactly when $(C, T)$ is an output of $\mathrm{Enc}$ on $(N, A)$, and the plaintext it returns is the unique $P$ with $\mathrm{Enc}(N, A, P) = (C, T)$: it is unique because $C$ fixes $P$ through the XOR. So an accepted tuple that the sender never produced is a forgery in the sense of integrity of ciphertexts.

**Lemma 4 (no release on failure).** On every input that $\mathrm{Dec}$ rejects, its output is the constant FAIL, and no byte of the key stream $\mathrm{KS}$ is computed.

*Proof.* The only return point other than L13 is L12, which returns the constant FAIL. Lines L10 to L12 use only $\mathrm{CB}(0, N)$, $A$, $C$ and $T$; the key stream blocks $\mathrm{CB}(1, N), \mathrm{CB}(2, N), \ldots$ appear only at L13, which is not reached. So no plaintext exists on this path, and the output depends on nothing but the accept bit. $\square$

As on the CCM page, this lemma speaks of output values, not of timing. The comparison at L12 has no early exit, but the Python big integers of Poly1305 are not constant time, so the study code claims no constant time.

**Corollary (the decryption oracle can be simulated).** For an adversary that gets $(C_i, T_i) = \mathrm{Enc}(N_i, A_i, P_i)$ and asks $\mathrm{Dec}$ on tuples not among the $(N_i, A_i, C_i, T_i)$, Lemmas 3 and 4 show that every answer is FAIL until the first accepted query, and the first accepted query is a forgery. So replacing $\mathrm{Dec}$ by the oracle that always says FAIL changes the view only on the event of a forgery. Together with IND-CPA privacy of $\mathrm{Enc}$, this is the step that gives IND-CCA security, as on the page on authenticated encryption. The probability of the forgery event is then bounded by the PRF advantage against ChaCha20 plus the Poly1305 term of Procter's analysis; that bound is not part of this correctness proof. $\blacksquare$
