---
title: BasicIdent and FullIdent decrypt every honest ciphertext
proves: [correctness]
status: full
---

Let $e : \mathbb{G}_1 \times \mathbb{G}_1 \to \mathbb{G}_T$ be a bilinear map on a group $\mathbb{G}_1 = \langle P \rangle$ of prime order $q$: $e(aA, bB) = e(A, B)^{ab}$ for all $A, B \in \mathbb{G}_1$ and all integers $a, b$. Let $s$ be the master key, $P_{\mathrm{pub}} = sP$, $Q = H_1(\mathsf{ID})$ and $d = sQ$, as in lines L1 to L5.

**Lemma.** For every $r \in \mathbb{Z}_q^*$, $e(d, rP) = e(Q, P_{\mathrm{pub}})^r$.

*Proof.* By bilinearity, $e(d, rP) = e(sQ, rP) = e(Q, P)^{sr}$, and $e(Q, P_{\mathrm{pub}})^r = e(Q, sP)^r = (e(Q, P)^s)^r = e(Q, P)^{sr}$. $\square$

**Theorem 1 (BasicIdent).** For every message $M \in \{0,1\}^n$ and every $r$ of line L6, BASIC-DECRYPT$(d, \text{BASIC-ENCRYPT}(\mathsf{params}, \mathsf{ID}, M)) = M$.

*Proof.* Lines L7 and L8 give $U = rP$ and $V = M \oplus H_2(g^r)$ with $g = e(Q, P_{\mathrm{pub}})$. By the lemma, $e(d, U) = g^r$, so line L9 returns $V \oplus H_2(g^r) = M \oplus H_2(g^r) \oplus H_2(g^r) = M$, because $x \oplus y \oplus y = x$ for strings of the same length. $\blacksquare$

**Theorem 2 (FullIdent).** For every $M \in \{0,1\}^n$ and every $\sigma$ of line L10, FULL-DECRYPT$(d, \text{FULL-ENCRYPT}(\mathsf{params}, \mathsf{ID}, M)) = M$.

*Proof.* Lines L10 to L12 give $r = H_3(\sigma, M) \in \mathbb{Z}_q^*$, $U = rP$, $V = \sigma \oplus H_2(g^r)$ and $W = M \oplus H_4(\sigma)$.

Line L13 accepts $U$: it is a multiple of $P$, so it lies in $\mathbb{G}_1$, and it is not $\mathcal{O}$, because $P$ has prime order $q$ and $0 < r < q$.

Line L14 computes $V \oplus H_2(e(d, U))$. By the lemma, $e(d, U) = g^r$, so this value is $\sigma$. Then $W \oplus H_4(\sigma) = M \oplus H_4(\sigma) \oplus H_4(\sigma) = M$.

Line L15 recomputes $H_3(\sigma, M) = r$, the same value as in line L10, since $H_3$ is a function. So $H_3(\sigma, M) \cdot P = rP = U$, the check passes, and line L16 returns $M$. $\blacksquare$

Neither proof uses the security assumptions; correctness needs only bilinearity, the fact that $P$ has order $q$, and that the hash functions are deterministic.
