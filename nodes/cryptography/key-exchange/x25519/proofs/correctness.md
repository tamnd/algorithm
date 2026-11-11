---
title: The X25519 ladder computes the u-coordinate of kP, and two honest parties agree
proves: [correctness]
status: full
---

We use the notation of the page. $p = 2^{255} - 19$ is prime, $A = 486662$, and $A^2 - 4$ is not a square in $\mathbb{F}_p$, so $E : v^2 = u^3 + Au^2 + u$ is an elliptic curve whose only point with $u = 0$ other than $O$ is $T_0 = (0, 0)$, of order 2. For a point $P = (u, v) \ne O$ write $x(P) = u$, and put $x(O) = \infty$, represented projectively by $(1 : 0)$. We write $(X : Z)$ for the projective value $X/Z$; two pairs that differ by a nonzero factor are the same value. Since $x(-P) = x(P)$, $x$ determines a point up to sign.

**Lemma 1 (doubling).** If $P \ne O$ and $2P \ne O$, then $x(2P) = \dfrac{(x^2 - 1)^2}{4x(x^2 + Ax + 1)}$ with $x = x(P)$.

*Proof.* The tangent at $P = (x, y)$ has slope $\lambda = (3x^2 + 2Ax + 1)/(2y)$, and for $y^2 = x^3 + Ax^2 + x$ the group law gives $x(2P) = \lambda^2 - A - 2x$. Since $2P \ne O$, $y \ne 0$, and

$$x(2P) = \frac{(3x^2 + 2Ax + 1)^2 - 4(A + 2x)(x^3 + Ax^2 + x)}{4(x^3 + Ax^2 + x)}.$$

Expanding, the numerator is $9x^4 + 12Ax^3 + (4A^2 + 6)x^2 + 4Ax + 1 - (8x^4 + 12Ax^3 + 4A^2x^2 + 8x^2 + 4Ax) = x^4 - 2x^2 + 1 = (x^2 - 1)^2$. $\blacksquare$

**Lemma 2 (differential addition).** If $P, Q, P + Q, P - Q$ are all different from $O$ and $x(P) \ne x(Q)$, then $x(P + Q)\, x(P - Q) = \dfrac{(x(P)x(Q) - 1)^2}{(x(P) - x(Q))^2}$.

*Proof.* Write $P = (a, y_P)$ and $Q = (b, y_Q)$, with $f(t) = t^3 + At^2 + t$, so $y_P^2 = f(a)$ and $y_Q^2 = f(b)$. The chord law gives $x(P \pm Q) = \lambda_\pm^2 - A - a - b$ with $\lambda_\pm = (y_P \mp y_Q)/(a - b)$. Put $\sigma = a + b$, $\pi = ab$, $s = \sigma + A$ and $c = 2y_Py_Q$. Then $(a - b)^2 x(P \pm Q) = f(a) + f(b) \mp c - s(a - b)^2 = g \mp c$, where $g = f(a) + f(b) - s(a - b)^2$. So the product is $(g^2 - c^2)/(a - b)^4$ with $c^2 = 4f(a)f(b)$. A direct computation, using $a^3 + b^3 = \sigma^3 - 3\sigma\pi$, $a^2 + b^2 = \sigma^2 - 2\pi$ and $(a - b)^2 = \sigma^2 - 4\pi$, gives

$$g = (\sigma^3 - 3\sigma\pi + A\sigma^2 - 2A\pi + \sigma) - (\sigma^3 - 4\sigma\pi + A\sigma^2 - 4A\pi) = \sigma(\pi + 1) + 2A\pi,$$

and $4f(a)f(b) = 4\pi(\pi^2 + A\sigma\pi + A^2\pi + \sigma^2 - 2\pi + A\sigma + 1)$. Then

$$g^2 - 4f(a)f(b) = \sigma^2(\pi + 1)^2 - 4\pi\sigma^2 + 4A\sigma\pi(\pi + 1) - 4A\sigma\pi(\pi + 1) + 4A^2\pi^2 - 4A^2\pi^2 - 4\pi(\pi - 1)^2 = (\sigma^2 - 4\pi)(\pi - 1)^2.$$

Since $\sigma^2 - 4\pi = (a - b)^2$, the product is $(ab - 1)^2/(a - b)^2$. $\blacksquare$

**Lemma 3 (the step formulas).** Let $(X_2 : Z_2) = x(R)$, $(X_3 : Z_3) = x(S)$ and $x_1 = x(S - R) \notin \{0, \infty\}$, and let LADDER-STEP return $(X_2', Z_2', X_3', Z_3')$. Then:
(a) $(X_2' : Z_2') = x(2R)$, for every $R$, with the convention $x(O) = (1 : 0)$ and $(X_2' : Z_2') = (1 : 0)$ when $2R = O$;
(b) $(X_3' : Z_3') = x(R + S)$ when $R, S \ne O$ and $x(R) \ne x(S)$;
(c) $(X_3' : Z_3') = x(R + S)$ when exactly one of $R$, $S$ is $O$.

*Proof.* With $A_2 = X_2 + Z_2$ and $B_2 = X_2 - Z_2$, we have $A_2^2 B_2^2 = (X_2^2 - Z_2^2)^2$ and $E = A_2^2 - B_2^2 = 4X_2Z_2$, so

$$Z_2' = 4X_2Z_2\big((X_2 + Z_2)^2 + (A - 2)X_2Z_2\big) = 4X_2Z_2(X_2^2 + AX_2Z_2 + Z_2^2),$$

using $a_{24} = (A - 2)/4$. If $Z_2 \ne 0$ and $2R \ne O$, dividing by $Z_2^4$ gives Lemma 1. If $R = O$, then $(X_2', Z_2') = (X_2^4, 0)$, which is $(1 : 0)$. If $R \ne O$ and $2R = O$, then $R = T_0$ (so $X_2 = 0$, and $Z_2' = 0$, $X_2' = Z_2^4 \ne 0$) or $R$ has $x^2 + Ax + 1 = 0$ (so $Z_2' = 0$, and $X_2' \ne 0$ since $x = \pm 1$ would make $x^2 + Ax + 1 = 2 \pm A \ne 0$). This proves (a).

For the addition, $DA + CB = (X_3 - Z_3)(X_2 + Z_2) + (X_3 + Z_3)(X_2 - Z_2) = 2(X_2X_3 - Z_2Z_3)$ and $DA - CB = 2(X_3Z_2 - X_2Z_3)$. So $X_3' = 4(X_2X_3 - Z_2Z_3)^2$ and $Z_3' = 4x_1(X_3Z_2 - X_2Z_3)^2$. In case (b), divide by $4Z_2^2Z_3^2$; since $x(R) \ne x(S)$, $X_3Z_2 - X_2Z_3 \ne 0$, and Lemma 2 with $x(S - R) = x_1$ gives $X_3'/Z_3' = x(R + S)$ when $R + S \ne O$. The value $R + S = O$ would give $x(R) = x(-R) = x(S)$, which is excluded. In case (c), say $R = O$, so $(X_2, Z_2) = (\mu, 0)$ with $\mu \ne 0$ and $S - R = S$, so $x(S) = x_1$. Then $X_3' = 4\mu^2X_3^2$ and $Z_3' = 4x_1\mu^2Z_3^2$, which is $(X_3^2 : x_1Z_3^2) = (x_1 : 1) = x(S) = x(R + S)$, because $X_3/Z_3 = x_1$. The case $S = O$ is the same with the roles of the slots swapped. $\blacksquare$

**Lemma 4 (ladder invariant).** Let $P \in E(\mathbb{F}_p)$ have odd prime order $r$, let $x_1 = x(P)$, and let $k$ be the clamped scalar. Write $m_t = \lfloor k / 2^t \rfloor$. After the iteration for bit $t$, with the lazy swap undone (that is, after swapping the slots once more if $\mathrm{swap} = 1$), the slots hold $x(m_tP)$ and $x((m_t + 1)P)$, in that order.

*Proof.* Before the loop, $m = 0$ and the slots are $(1 : 0) = x(O)$ and $(x_1 : 1) = x(P)$, with $\mathrm{swap} = 0$.

The lazy swap. Let $s$ be the value of $\mathrm{swap}$ before line L6. By induction, the true pair $(R_0, R_1) = (x(mP), x((m + 1)P))$ sits in the slots $(x_2, x_3)$ if $s = 0$ and in $(x_3, x_2)$ if $s = 1$. Line L6 sets $\mathrm{swap} = s \oplus k_t$, and line L7 swaps exactly when that is 1. So after line L7 the slots hold $(R_0, R_1)$ if $k_t = 0$ and $(R_1, R_0)$ if $k_t = 1$. LADDER-STEP doubles the first slot and adds the two. If $k_t = 0$ the slots become $(x(2mP), x((2m + 1)P))$; if $k_t = 1$ they become $(x((2m + 2)P), x((2m + 1)P))$, which is the pair $(x((2m + 1)P), x((2m + 2)P))$ in swapped order. Line L8 sets $\mathrm{swap} = k_t$, which records exactly this order. Since $m_t = 2m + k_t$, the invariant holds again. Line L10 undoes the last swap.

Each step uses $x_1 = x(R_1 - R_0) = x(P)$, because the difference of the two points is always $P$. Since $r$ is odd, $P \ne T_0$, so $x_1 \ne 0$, and $x_1 \ne \infty$ because $P \ne O$.

The doubling is correct in every case by Lemma 3(a). For the addition of $R = m'P$ and $S = (m' + 1)P$: if one of them is $O$, Lemma 3(c) applies. Otherwise $x(R) = x(S)$ would mean $S = \pm R$; $S = R$ gives $P = O$, and $S = -R$ gives $(2m' + 1)P = O$. If neither holds, Lemma 3(b) applies. If $(2m' + 1)P = O$, the true sum is $O$. Here $R, S \ne O$ and $x(R) = x(S) = \xi$, so $X_3Z_2 - X_2Z_3 = 0$ and $Z_3' = 0$, while $X_2X_3 - Z_2Z_3 = Z_2Z_3(\xi^2 - 1)$. If $\xi = \pm 1$, then $x^2 + Ax + 1 = 2 \pm A \ne 0$ at $\xi$, so Lemma 1 gives $x(2R) = 0$, that is $2R = T_0$, and $R$ has order 4; this is impossible, since $R \ne O$ lies in the group generated by $P$, of odd order $r$. So $X_3' \ne 0$, and the result is $(1 : 0) = x(O)$, which is again correct. $\blacksquare$

**Theorem 1 (the output).** For a point $P$ of odd prime order $r$ with $u$-coordinate $u$, X25519$(k, u)$ returns the encoding of $x(kP)$ if $kP \ne O$, and the encoding of 0 if $kP = O$.

*Proof.* The loop processes bits 254 down to 0, so at the end $m_0 = k$ (bit 255 is 0 after clamping), and by Lemma 4 the first slot is $(X : Z) = x(kP)$ after line L10. If $Z \ne 0$, line L11 computes $X \cdot Z^{p - 2} = X/Z$ by Fermat's little theorem. If $Z = 0$, then $Z^{p - 2} = 0$ and the output is 0. $\blacksquare$

**Theorem 2 (agreement).** Let $P_0$ be the base point, of prime order $\ell$, and let $a$ and $b$ be the clamped private keys of Alice and Bob. Then X25519$(a, $X25519$(b, 9)) = $ X25519$(b, $X25519$(a, 9))$.

*Proof.* Clamping makes $a = 8a'$ with $2^{251} \le a' < 2^{252}$, so $a' < \ell$ and $\ell \nmid a'$; since $\ell$ is odd, $\ell \nmid a$, and likewise $\ell \nmid b$. By Theorem 1, Bob's public key is $x(bP_0)$ with $bP_0 \ne O$, and $bP_0$ again has order $\ell$. The $u$-coordinate $x(bP_0)$ is shared by $bP_0$ and $-bP_0$, and $x(a(-Q)) = x(-(aQ)) = x(aQ)$, so the choice of sign does not matter. By Theorem 1 again, Alice's output is $x(a(bP_0)) = x((ab)P_0)$, and Bob's is $x(b(aP_0)) = x((ab)P_0)$, since scalar multiplication in a commutative group satisfies $a(bQ) = (ab)Q = b(aQ)$. As $\ell \nmid ab$, this point is not $O$, so both outputs are the same nonzero 32-byte string. $\blacksquare$

**Remark (inputs that are not honest).** For a $u$ that is not the coordinate of a point of $E$, the same formulas compute on the quadratic twist $E' : B'y^2 = f(x)$, with $B'$ a non-square, whose $x$-coordinates are the other elements of $\mathbb{F}_p$; Lemmas 1 to 3 hold there with the same proofs, because in the chord and tangent law $B'\lambda^2$ has the denominator $B'y^2 = f(x)$, so $B'$ cancels. For points whose order divides 8, clamping makes $k$ a multiple of 8, so $kP = O$ and the output is 0; this is the all-zero output that RFC 7748, Section 6.1, lets a protocol reject. $\blacksquare$
