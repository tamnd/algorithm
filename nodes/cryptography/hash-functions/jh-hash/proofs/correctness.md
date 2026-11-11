---
title: E8 is a bijection, L has branch number 3, and F8 is invertible for each block
proves: [correctness]
status: full
---

We use the notation of the page: $F_8(H, m) = E_8(H \oplus (m \| 0^{512})) \oplus (0^{512} \| m)$, the round $R_8$ made of the S-box layer, the map $L$ and the permutation $P_8$, and the padding of Section 6.1.

**Lemma 1 (the layers are bijections).** $S_0$ and $S_1$ are permutations of $\{0, \dots, 15\}$, $L$ is a bijection of pairs of 4-bit elements, and $P_8$, the grouping and the de-grouping are permutations of positions. So $R_8(\cdot, C)$ is a bijection for each constant $C$, and $E_8$ is a bijection of $\{0,1\}^{1024}$.

*Proof.* The tables of Section 4.1 list each of the 16 values once. $L(A, B) = (5 \bullet A + 2 \bullet B, 2 \bullet A + B)$ is linear over $\mathrm{GF}(2^4)$ with matrix $\begin{pmatrix} 5 & 2 \\ 2 & 1 \end{pmatrix}$, whose determinant is $5 \bullet 1 + 2 \bullet 2 = 5 \oplus 4 = 1 \ne 0$, so it is invertible. $\pi_8$, $P'_8$ and $\phi_8$ each send the index set $\{0, \dots, 255\}$ onto itself one to one: $\pi_8$ and $\phi_8$ are products of disjoint swaps, and $P'_8$ sends the even index $2i$ to $i$ and the odd index $2i + 1$ to $i + 128$. The grouping sends bit $i + 256k$ to place $k$ of element $2i$ and bit $i + 128 + 256k$ to place $k$ of element $2i + 1$, for $0 \le i < 128$ and $0 \le k < 4$, with place 0 the most significant bit; this covers each of the 1024 bits once. A composition of bijections is a bijection. $\square$

**Lemma 2 (branch number of $L$).** If $(A, B) \ne (0, 0)$ and $(C, D) = L(A, B)$, then at least 3 of $A, B, C, D$ are nonzero.

*Proof.* If $A = 0$ and $B \ne 0$, then $C = 2 \bullet B \ne 0$ and $D = B \ne 0$. If $B = 0$ and $A \ne 0$, then $C = 5 \bullet A \ne 0$ and $D = 2 \bullet A \ne 0$, because $\mathrm{GF}(2^4)$ has no zero divisors. If both are nonzero, then $(C, D) \ne (0, 0)$ by Lemma 1, so at least one of $C, D$ is nonzero. In each case at least 3 elements are nonzero. $\square$

So $L$ is an MDS map, and a difference in one element of a pair spreads to both elements of the output. This is the property that the differential analysis of Section 9.3 uses to count active S-boxes.

**Lemma 3 ($F_8$ is invertible in the state).** For each block $m$, the map $H \mapsto F_8(H, m)$ is a bijection, with inverse $H' \mapsto E_8^{-1}(H' \oplus (0^{512} \| m)) \oplus (m \| 0^{512})$.

*Proof.* Substitute: $E_8^{-1}(F_8(H, m) \oplus (0^{512} \| m)) = E_8^{-1}(E_8(H \oplus (m \| 0^{512}))) = H \oplus (m \| 0^{512})$, and XOR with $m \| 0^{512}$ gives $H$. The inverse of $E_8$ exists by Lemma 1. $\square$

**Corollary (why there is no Merkle-Damgård reduction).** Given any $H'$ and any $m$, Lemma 3 gives the $H$ with $F_8(H, m) = H'$. So pseudo-preimages of $F_8$ cost one call of $E_8^{-1}$, and two different blocks $m \ne m'$ with the same target $H'$ give a pseudo-collision $(H, m) \ne (H_*, m')$. The collision resistance of JH therefore cannot follow from the collision resistance of $F_8$, as it does for the [Merkle-Damgård construction](/merkle-damgard-construction/). It rests on the fixed IV and on modeling $E_8$ as an ideal permutation, where the indifferentiability results cited on the page apply. Those results are bounds on the mode, not a reduction to a property of the real $E_8$, so no tight concrete reduction is claimed.

**Lemma 4 (padding is injective).** For byte strings $M \ne M'$, the padded strings differ.

*Proof.* The last 128 bits of the padded string hold $N$, the length of $M$ in bits. If the lengths differ, these fields differ. If the lengths are equal, the padded strings have the same length and begin with $M$ and $M'$, which differ. $\square$

**Theorem (the code is JH).** The code agrees with the official short-message known-answer tests for JH-256 and JH-512 and with the round constants $C_0$, $C_1$, $C_2$, $C_{40}$ and $C_{41}$ of Appendix A.1. The constants test the S-boxes, $L$ and $P_6$ through 41 rounds of $R_6$; the known answers test the grouping, $P_8$, $F_8$, the padding, the IV and the truncation. $\blacksquare$
