---
title: Correctness of J-PAKE
proves: [correctness]
status: full
---

We prove that honest Schnorr proofs verify, that two honest parties with the same password compute the same $K$, and that with different passwords they compute the same $K$ only with probability $1/q$. Notation is that of the page: $g$ has prime order $q$ in $\mathbb{Z}_p^*$, all exponents are taken modulo $q$, Alice holds $x_1, x_2$ and Bob holds $x_3, x_4$, with $x_2, x_4 \ne 0$.

**Lemma 1 (Schnorr completeness).** If $X = h^x$ and the prover follows lines L8 to L10, the check of line L11 passes.

*Proof.* The verifier computes the same $c$ as the prover, since line L9 hashes the same items. Then $h^r X^c = h^{v - xc} h^{xc} = h^v = V$, because $h$ has order dividing $q$ and $r \equiv v - xc \pmod q$. The values $X = h^x$ and $V = h^v$ are powers of an element of the subgroup, so they lie in the subgroup. $\square$

**Lemma 2 (honest checks pass).** In an honest run, every proof verifies and the check $G_4 \ne 1$ of line L3 passes.

*Proof.* Each proof is made for the base and exponent that the sender used: $G_i = g^{x_i}$ with base $g$; $A = (G_1 G_3 G_4)^{x_2 s}$ with base $G_1 G_3 G_4$, and $B = (G_1 G_2 G_3)^{x_4 s}$ with base $G_1 G_2 G_3$. The receiver forms the same base from the values it holds. By Lemma 1 all proofs verify. $G_4 = g^{x_4}$ with $x_4 \in [1, q)$, and $g$ has order $q$, so $G_4 \ne 1$. $\square$

**Lemma 3 (agreement).** If both parties use the same $s$, both compute $K = g^{(x_1 + x_3) x_2 x_4 s}$.

*Proof.* We have $G_1 G_3 G_4 = g^{x_1 + x_3 + x_4}$ and $G_1 G_2 G_3 = g^{x_1 + x_2 + x_3}$, so $A = g^{(x_1 + x_3 + x_4) x_2 s}$ and $B = g^{(x_1 + x_2 + x_3) x_4 s}$. Alice computes $G_4^{x_2 s} = g^{x_2 x_4 s}$ and
$$B \cdot g^{-x_2 x_4 s} = g^{(x_1 + x_2 + x_3) x_4 s - x_2 x_4 s} = g^{(x_1 + x_3) x_4 s},$$
then raises it to $x_2$ and gets $g^{(x_1 + x_3) x_2 x_4 s}$. Bob computes $G_2^{x_4 s} = g^{x_2 x_4 s}$ and
$$A \cdot g^{-x_2 x_4 s} = g^{(x_1 + x_3 + x_4) x_2 s - x_2 x_4 s} = g^{(x_1 + x_3) x_2 s},$$
then raises it to $x_4$ and gets the same value. $\square$

**Lemma 4 (different passwords).** If Alice uses $s$ and Bob uses $s' \ne s \pmod q$, then $K_A = K_B$ if and only if $x_1 + x_2 + x_3 + x_4 \equiv 0 \pmod q$, and this has probability $1/q$ over Alice's uniform $x_1$.

*Proof.* Now $A = g^{(x_1 + x_3 + x_4) x_2 s}$ and $B = g^{(x_1 + x_2 + x_3) x_4 s'}$. Alice computes
$$K_A = \left(g^{(x_1 + x_2 + x_3) x_4 s' - x_2 x_4 s}\right)^{x_2} = g^{x_2 x_4 \left((x_1 + x_3) s' + x_2 (s' - s)\right)},$$
and Bob computes
$$K_B = \left(g^{(x_1 + x_3 + x_4) x_2 s - x_2 x_4 s'}\right)^{x_4} = g^{x_2 x_4 \left((x_1 + x_3) s + x_4 (s - s')\right)}.$$
Since $g$ has order $q$ and $x_2 x_4 \not\equiv 0$, $K_A = K_B$ if and only if $(x_1 + x_3) s' + x_2 (s' - s) \equiv (x_1 + x_3) s + x_4 (s - s')$, that is, $(s' - s)(x_1 + x_2 + x_3 + x_4) \equiv 0 \pmod q$. As $s' - s \not\equiv 0$ and $q$ is prime, this holds if and only if $x_1 + x_2 + x_3 + x_4 \equiv 0$. For any fixed $x_2, x_3, x_4$, exactly one value of $x_1 \in [0, q)$ satisfies it. $\square$

**Theorem.** In an honest run with the same password, J-PAKE never aborts and both parties derive the same key. With different passwords, the keys from line L7 agree with probability at most $1/q$ plus the probability of a collision of the KDF.

*Proof.* Lemma 2 shows that no check aborts, and Lemma 3 gives equal $K$, so line L7 gives equal keys. Lemma 4 bounds the probability of equal $K$ for different passwords; different values of $K$ give equal keys only by a collision of the KDF. $\blacksquare$
