---
title: Honest pre-signatures pass pre-verification, adapt to valid BIP 340 signatures, and give back the witness
proves: [correctness]
status: full
---

Let $G$ be the base point of secp256k1, of prime order $n$. The public key $P = dG$ has an even y. BIP 340 verification of $(r, s)$ on $m$ under $x(P)$ accepts if and only if $sG - eP$ is a point with an even y and x coordinate $r$, where $e = H(r \| x(P) \| m) \bmod n$. For a point $R \ne \infty$ let $\epsilon(R) = 1$ if $R$ has an even y and $-1$ otherwise; then $\epsilon(R) R$ is the point with x coordinate $x(R)$ and an even y, because negation keeps x and flips the parity of y ($p$ is odd and no point of odd prime order has $y = 0$).

Fix $T = tG$, a message $m$ and the nonce $k$ of line L1, and let $\hat{R} = kG$, $R = \hat{R} + T$, $\epsilon = \epsilon(R)$ and $e = H(x(R) \| x(P) \| m)$. Assume $R \ne \infty$, which fails only if $k \equiv -t$, with probability $1/(n - 1)$ for random $k$.

**Lemma 1 (pre-verification accepts).** The output $(\hat{R}, s')$ of line L3 passes line L5.

*Proof.* Line L4 recomputes the same $R$, $\epsilon$ and $e$, since they depend only on $\hat{R}$, $T$, $P$ and $m$. Then $s'G = (\epsilon k + e d) G = \epsilon \hat{R} + eP$. $\square$

**Lemma 2 (adaptation gives a valid signature).** The output $(x(R), s)$ of line L6 passes BIP 340 verification.

*Proof.* $sG = s'G + \epsilon tG = \epsilon \hat{R} + eP + \epsilon T = \epsilon R + eP$ by Lemma 1. So $sG - eP = \epsilon R$, which has x coordinate $x(R)$ and an even y. The verifier's challenge is $H(x(R) \| x(P) \| m) = e$. $\square$

**Lemma 3 (extraction gives the witness).** For $s$ from line L6, line L7 returns $t$, and its check $tG = T$ passes.

*Proof.* $\epsilon(s - s') = \epsilon \cdot \epsilon t = \epsilon^2 t = t \bmod n$, since $\epsilon^2 = 1$. $\square$

**Lemma 4 (extraction from any valid signature).** Let $(\hat{R}, s')$ pass line L5, and let $(x(R), s)$ be any valid BIP 340 signature on $m$ under $P$ with the same $R = \hat{R} + T$. Then $\epsilon(s - s') G = T$, so line L7 returns a witness.

*Proof.* Validity gives $sG = \epsilon R + eP$, with the same $e$ because the challenge depends only on $x(R)$, $x(P)$ and $m$. Line L5 gives $s'G = \epsilon \hat{R} + eP$. Subtract: $(s - s')G = \epsilon (R - \hat{R}) = \epsilon T$. Multiply by $\epsilon$. $\square$

Lemma 4 is the reason for witness extractability: once a pre-signature has been checked, any valid signature with the same nonce point reveals a discrete logarithm of $T$, whoever made it. A valid signature on $m$ with a different nonce point is not covered; unforgeability rules it out in the security proof of Aumayr et al. $\blacksquare$
