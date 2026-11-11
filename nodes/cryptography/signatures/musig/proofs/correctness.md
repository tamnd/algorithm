---
title: Honest MuSig2 partial signatures pass their check and sum to a valid BIP 340 signature under the aggregate key
proves: [correctness]
status: full
---

Let $G$ be the base point of secp256k1, of prime order $n$. For a point $X \ne \infty$ write $\bar{X}$ for the point with the same x coordinate and an even y, so $\bar{X} = X$ or $\bar{X} = -X$. BIP 340 verification of $(r, s)$ on $m$ under the x-only key $x(\bar{Q})$ accepts if and only if $sG - e\bar{Q}$ is a point with an even y and x coordinate $r$, where $e = H(r \| x(Q) \| m) \bmod n$.

Fix honest signers $i = 1, \dots, u$ with secrets $d_i$, keys $P_i = d_i G$ and coefficients $a_i$ from lines L1 and L2, so line L3 gives $Q = \sum_i a_i P_i = (\sum_i a_i d_i) G$. Assume $Q \ne \infty$ (KeyAgg fails otherwise).

**Lemma 1 (the sign factors).** Let $g = 1$ if $Q$ has an even y and $g = n - 1$ otherwise. Then $\bar{Q} = gQ$. Let $\epsilon = 1$ if $R$ has an even y and $\epsilon = -1$ otherwise. Then $\bar{R} = \epsilon R$.

*Proof.* Negating a point keeps x and replaces y by $p - y$, which has the other parity because $p$ is odd and $y \ne 0$ (no point of odd prime order has $y = 0$). Multiplying by $n - 1 \equiv -1$ negates. $\square$

**Lemma 2 (each partial signature passes line L10).** For each $i$, $s_i G = \epsilon (R_{i,1} + b R_{i,2}) + e a_i g P_i$.

*Proof.* After line L8 the nonces are $\epsilon k_{i,1}$ and $\epsilon k_{i,2}$ (as residues mod $n$). Line L9 gives $s_i = \epsilon k_{i,1} + b \epsilon k_{i,2} + e a_i g d_i$. Multiply by $G$ and use $k_{i,j} G = R_{i,j}$ and $d_i G = P_i$. $\square$

**Lemma 3 (the sum verifies).** The output $(x(R), s)$ of line L11 passes BIP 340 verification under $x(Q)$ on $m$.

*Proof.* Every signer computes the same $b$, $R$, $e$ and $g$, because lines L6 and L7 use only the public values $R_1$, $R_2$, $Q$ and $m$, and line L5 gives every signer the same $R_1$ and $R_2$. Summing Lemma 2 over $i$,

$$sG = \epsilon \sum_i (R_{i,1} + b R_{i,2}) + e g \sum_i a_i P_i = \epsilon (R_1 + b R_2) + e g Q = \epsilon R + e \bar{Q} = \bar{R} + e \bar{Q},$$

using line L5, line L6 ($R = R_1 + b R_2$), line L3 and Lemma 1. So $sG - e\bar{Q} = \bar{R}$, which has an even y and x coordinate $x(R)$. The challenge in verification is $H(x(R) \| x(Q) \| m)$, which equals the $e$ of line L7. Hence verification accepts. (If $R_1 + b R_2 = \infty$, BIP 327 sets $R = G$; this happens with negligible probability for honest random nonces and is not needed here.) $\square$

**Lemma 4 (rogue keys do not cancel).** Let $P_1$ be honest and let an adversary choose $P_2$ after it sees $P_1$. If the adversary could output $\beta$ with $Q = \beta G$ for $Q = a_1 P_1 + a_2 P_2$, it would know $d_1 = a_1^{-1}(\beta - a_2 d_2)$ whenever it also knew $d_2$; in general it must fix $P_2$ before it learns $a_1 = H(L \| pk_1)$, which depends on $P_2$ through $L$.

*Proof sketch.* This is the reason for the hash of the full list in line L1, not a full security proof. The security proof of MuSig2 in the random oracle model programs $H$ at the coefficient query and rewinds the adversary with a different $a_1$; from two forgeries with different $a_1$ for the same list it extracts $d_1$. The details are in Nick, Ruffing and Seurin (2021). $\blacksquare$
