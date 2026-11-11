---
title: The X448 ladder computes the u-coordinate of kP, and two honest parties agree
proves: [correctness]
status: full
---

We use the notation of the page. $p = 2^{448} - 2^{224} - 1$ is prime, $A = 156326$, $a_{24} = (A - 2)/4 = 39081$, and $E : v^2 = f(u)$ with $f(u) = u^3 + Au^2 + u$. Since $A^2 - 4$ is not a square modulo $p$, the only root of $f$ is $u = 0$, and $T_0 = (0, 0)$ is the only point of order 2. For $P \ne O$ write $x(P)$ for its $u$-coordinate, and let $x(O)$ be the projective value $(1 : 0)$.

The proof for [X25519](/x25519/) uses only these facts: $p$ is an odd prime, $A \ne \pm 2$, $A^2 - 4$ is a non-square (so $T_0$ is the only point with $x = 0$), $a_{24} = (A - 2)/4$, the clamped scalar has a fixed top bit and is less than $2^b$ for the number $b$ of ladder steps, and the base point has odd prime order $\ell$ that does not divide the clamped scalar. We restate the steps and check each fact for X448.

**Lemma 1 (doubling).** If $P \ne O$ and $2P \ne O$, then $x(2P) = (x^2 - 1)^2 / (4x(x^2 + Ax + 1))$ with $x = x(P)$.

*Proof.* The tangent law gives $x(2P) = \lambda^2 - A - 2x$ with $\lambda = (3x^2 + 2Ax + 1)/(2y)$ and $y^2 = f(x) \ne 0$. The numerator of $\lambda^2 - A - 2x$ over $4f(x)$ is $(3x^2 + 2Ax + 1)^2 - 4(A + 2x)(x^3 + Ax^2 + x) = (x^2 - 1)^2$, an identity in $\mathbb{Z}[x, A]$ that holds for every $A$. $\blacksquare$

**Lemma 2 (differential addition).** If $P, Q, P \pm Q \ne O$ and $x(P) \ne x(Q)$, then $x(P + Q)\,x(P - Q) = (x(P)x(Q) - 1)^2 / (x(P) - x(Q))^2$.

*Proof.* With $a = x(P)$, $b = x(Q)$, $\sigma = a + b$ and $\pi = ab$, the chord law gives $(a - b)^2 x(P \pm Q) = g \mp 2y_Py_Q$ with $g = \sigma(\pi + 1) + 2A\pi$, and $g^2 - 4f(a)f(b) = (\sigma^2 - 4\pi)(\pi - 1)^2$. These are identities in $\mathbb{Z}[a, b, A]$, proved in full on the X25519 proof page, so they hold for $A = 156326$. Dividing by $(a - b)^4 = (\sigma^2 - 4\pi)^2$ gives the claim. $\blacksquare$

**Lemma 3 (the step).** Let the slots hold $x(R) = (X_2 : Z_2)$ and $x(S) = (X_3 : Z_3)$ with $x(S - R) = x_1 \notin \{0, \infty\}$. LADDER-STEP returns $Z_2' = 4X_2Z_2(X_2^2 + AX_2Z_2 + Z_2^2)$, $X_2' = (X_2^2 - Z_2^2)^2$, $X_3' = 4(X_2X_3 - Z_2Z_3)^2$ and $Z_3' = 4x_1(X_3Z_2 - X_2Z_3)^2$. Then $(X_2' : Z_2') = x(2R)$ in every case, and $(X_3' : Z_3') = x(R + S)$ in every case that occurs when $R$ and $S$ lie in a group of odd order.

*Proof.* The four expressions follow from $E = A_2^2 - B_2^2 = 4X_2Z_2$, $A_2^2 + a_{24}E = X_2^2 + (2 + 4a_{24})X_2Z_2 + Z_2^2$ with $2 + 4a_{24} = A$, $DA + CB = 2(X_2X_3 - Z_2Z_3)$ and $DA - CB = 2(X_3Z_2 - X_2Z_3)$. With these, Lemmas 1 and 2 give the generic cases. The special cases are the same as for X25519: $R = O$ or $S = O$ give the other point back, because $x_1$ is then the $u$-coordinate of the other point; $2R = O$ or $R + S = O$ give $Z' = 0$ with $X' \ne 0$, because a point with $x = \pm 1$ has $x^2 + Ax + 1 = 2 \pm A \ne 0$ and doubles to $T_0$, so it has order 4 and does not lie in a group of odd order. $\blacksquare$

**Lemma 4 (ladder invariant).** Let $P$ have odd prime order $r$ and $x_1 = x(P)$. After the iteration for bit $t$, with the lazy swap undone, the slots hold $x(m_tP)$ and $x((m_t + 1)P)$, where $m_t = \lfloor k / 2^t \rfloor$.

*Proof.* At the start, $m = 0$ and the slots hold $(1 : 0) = x(O)$ and $(x_1 : 1) = x(P)$ with $\mathrm{swap} = 0$. Line L6 sets $\mathrm{swap} = s \oplus k_t$, where $s$ records whether the slots are in swapped order, so after line L7 the first slot holds $R_{k_t}$ and the second $R_{1 - k_t}$. LADDER-STEP doubles the first and adds the two; the result is $x((2m + k_t)P)$ in the first slot and $x((2m + 1)P)$ in the second, which is the pair for $m_t = 2m + k_t$ in the order recorded by line L8. The difference of the two points is always $P$, so $x_1$ is the right difference. Since $r$ is odd, $P \ne T_0$ and $x_1 \ne 0$; by Lemma 3 every step is correct. $\blacksquare$

**Theorem 1 (the output).** For a point $P$ of odd prime order with $u$-coordinate $u$, X448$(k, u)$ returns the encoding of $x(kP)$, or of 0 if $kP = O$.

*Proof.* The loop reads bits 447 down to 0 of the clamped $k < 2^{448}$, so $m_0 = k$, and line L10 undoes the last swap. By Lemma 4 the first slot is $(X : Z) = x(kP)$. Line L11 returns $X \cdot Z^{p - 2} = X/Z$ by Fermat's little theorem when $Z \ne 0$, and 0 when $Z = 0$. $\blacksquare$

**Theorem 2 (agreement).** For the base point $P_0$ ($u = 5$, of prime order $\ell$) and clamped private keys $a$ and $b$, X448$(a, $X448$(b, 5)) = $ X448$(b, $X448$(a, 5))$, and the value is 0 only in the case described below.

*Proof.* By Theorem 1, Bob's public key is $x(bP_0)$. If $bP_0 \ne O$, it is the $u$-coordinate of $\pm bP_0$, a point of order $\ell$, and since $x(a(-Q)) = x(aQ)$, Theorem 1 gives Alice's output $x(a(bP_0)) = x((ab)P_0)$. In the same way Bob's output is $x(b(aP_0)) = x((ab)P_0)$, by commutativity of scalar multiplication. So the outputs are equal.

The value is 0 only if $\ell \mid ab$. Clamping gives $a = 4a'$ with $2^{445} \le a' < 2^{446}$, and $\ell = 2^{446} - c$ with $0 < c < 2^{224}$, so $2^{445} < \ell < 2^{446} < 2\ell$. Since $\ell$ is an odd prime, $\ell \mid a$ exactly when $a' = \ell$, the only multiple of $\ell$ in that range. So the output is nonzero unless $a' = \ell$ or $b' = \ell$, one value out of $2^{445}$ for each key; if this happens, both outputs are 0 and are still equal. $\blacksquare$

**Remark (twist and small order).** A $u$ that is not on $E$ is the $u$-coordinate of a point on the quadratic twist, and Lemmas 1 to 3 hold there with the same proofs, since the twist constant cancels in the chord and tangent law. Points of order dividing 4 are mapped to $O$ by the clamped scalar, a multiple of 4, so the output is all zero. $\blacksquare$
