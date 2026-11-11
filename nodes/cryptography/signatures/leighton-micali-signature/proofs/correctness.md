---
title: LMS and HSS signatures verify
proves: [correctness]
status: full
---

**Setting.** We use the notation of RFC 8554. $I$ is the 16-byte key identifier, $q$ the leaf number, $p$ the number of chains, and $w$ the number of bits per digit. The chain step $j$ of chain $i$ of leaf $q$ is $s_{q,i,j}(t) = H(I \| u32(q) \| u16(i) \| u8(j) \| t)$ (line L5). For $a \le b$ write $S_{q,i}[a, b)$ for the steps $a, a+1, \ldots, b - 1$ applied in that order. The one-time public value of chain $i$ is $y_i = S_{q,i}[0, 2^w - 1)(x_i)$, and the one-time public key hash is $K_q = H(I \| u32(q) \| u16(D\_PBLC) \| y_0 \| \ldots \| y_{p-1})$. The tree nodes are $T[r]$ for $r = 1, \ldots, 2^{h+1} - 1$: $T[2^h + q] = H(I \| u32(2^h+q) \| u16(D\_LEAF) \| K_q)$ and $T[r] = H(I \| u32(r) \| u16(D\_INTR) \| T[2r] \| T[2r+1])$ for $r < 2^h$.

**Lemma 1 (LM-OTS).** For every message and every $C$, the value $K_c$ of line L14, computed from an honest LM-OTS signature of leaf $q$, equals $K_q$.

*Proof.* Signer and verifier compute the same $Q$ and the same digits $a_0, \ldots, a_{p-1}$, because lines L2 and L3 depend only on $I, q, C$ and the message, and $C$ is in the signature. Each digit is below $2^w$, because coef returns $w$ bits. The signature has $y'_i = S_{q,i}[0, a_i)(x_i)$ (line L4), and line L13 computes $z_i = S_{q,i}[a_i, 2^w - 1)(y'_i)$. Applying steps $0, \ldots, a_i - 1$ and then $a_i, \ldots, 2^w - 2$ is applying steps $0, \ldots, 2^w - 2$, so $z_i = y_i$. Then line L14 hashes the same string as $K_q$. $\square$

**Lemma 2 (the path).** Let $r_0 = 2^h + q$ and $t_0 = T[r_0]$. For $i = 0, \ldots, h-1$ let $r_{i+1} = \lfloor r_i / 2 \rfloor$, and let $t_{i+1}$ be the value of line L16: $H(I \| u32(r_{i+1}) \| u16(D\_INTR) \| path_i \| t_i)$ if $r_i$ is odd, and the same with $t_i \| path_i$ if $r_i$ is even, where $path_i = T[r_i \oplus 1]$ (line L9). Then $t_i = T[r_i]$ for all $i$, and $t_h = T[1]$.

*Proof.* By induction on $i$. The case $i = 0$ is the definition. Assume $t_i = T[r_i]$. If $r_i$ is even, $r_i = 2 r_{i+1}$ and $r_i \oplus 1 = 2r_{i+1} + 1$, so $t_{i+1} = H(I \| u32(r_{i+1}) \| u16(D\_INTR) \| T[2r_{i+1}] \| T[2r_{i+1}+1]) = T[r_{i+1}]$. If $r_i$ is odd, $r_i = 2r_{i+1} + 1$ and $r_i \oplus 1 = 2 r_{i+1}$, and the same equation holds with the arguments in the same order. After $h$ steps, $r_h = \lfloor (2^h + q) / 2^h \rfloor = 1$, because $0 \le q < 2^h$. $\square$

**Theorem 3 (LMS correctness).** An honest LMS signature with leaf $q < 2^h$ passes LMS verification against the public key $(lmstype, otstype, I, T[1])$.

*Proof.* The signature has the format that line L11 checks: the types are the ones of the public key, and the lengths follow from them. Line L7 makes sure that $q < 2^h$. By Lemma 1, line L14 gives $K_q$, so line L15 gives $T[2^h + q]$. By Lemma 2, the loop of line L16 ends with $T[1]$, and line L17 accepts. $\square$

**Theorem 4 (HSS correctness).** An honest HSS signature with $L$ levels passes HSS verification.

*Proof.* The signer sends $N_{spk} = L - 1$ signed public keys, so line L18 passes. The tree of level $i$ signed the public key of level $i + 1$ honestly, so by Theorem 3 each check in line L19 passes, and the key used next is the public key of level $i + 1$. The last tree signed the message, and line L20 accepts by Theorem 3. $\square$

**Remarks on security.** The RFC does not prove security. Katz (2016) analyzed the proposed standard and proved its security with a tight bound in the random oracle model; the domain separation of the hash inputs (Section 9.1 of the RFC: the leaf number $q$, the chain number $i$, the step $j$ and the constants $D\_PBLC$, $D\_MESG$, $D\_LEAF$, $D\_INTR$ give distinct inputs) is what makes each hash call a fresh random oracle query. The randomizer $C$ in line L1 means that a forger must find a second message for a hash it did not choose, so collisions of SHA-256 alone do not break the scheme. As with every Merkle scheme, security holds only if no leaf signs two messages.
