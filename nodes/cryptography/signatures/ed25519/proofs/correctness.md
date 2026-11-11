---
title: Honest Ed25519 signatures pass both the cofactored and the cofactorless check
proves: [correctness]
status: full
---

Let $E$ be the curve $-x^2 + y^2 = 1 + d x^2 y^2$ over $\mathbb{F}_p$, $p = 2^{255} - 19$, with the base point $B$ of prime order $L$. For integers $u, v$, $[u]B = [v]B$ if and only if $u \equiv v \pmod L$.

**Lemma 1 (the encoding is decoded back).** For every point $P = (x, y)$ of $E$, decoding $\mathrm{ENC}(P)$ returns $P$.

*Proof.* $\mathrm{ENC}(P)$ stores $y \in [0, p-1]$ and the low binary digit of $x$. Since $p < 2^{255}$, $y$ fits in 255 binary digits and the decoder reads back $y < p$, so its range check passes. On $E$, $x^2 (d y^2 + 1) = y^2 - 1$. The value $d y^2 + 1$ is not zero, because $d$ is not a square mod $p$ and so $-1/d$ is not a square either ($-1$ is a square mod $p$ since $p \equiv 1 \pmod 4$). So $x^2 = (y^2 - 1)/(d y^2 + 1)$ is fixed by $y$, and the two square roots $x$ and $p - x$ have different low digits when $x \ne 0$, because $p$ is odd. The stored digit picks $x$. If $x = 0$, the stored digit is 0 and the decoder returns $x = 0$. $\square$

**Lemma 2 (honest signatures verify).** Let $(\mathrm{ENC}(R), S)$ be the output of lines L4 to L8 for the key of lines L1 to L3 and a message $M$. Then line L11 returns true in both forms, cofactored and cofactorless.

*Proof.* By Lemma 1, line L9 decodes $A$ and $R$ to the points $A = [a]B$ and $R = [r]B$, and $S < L$ because line L7 reduces mod $L$. So line L9 does not reject. Line L10 hashes the same bytes as line L6, so it gets the same $k$. By line L7, $S \equiv r + k a \pmod L$, so

$$[S]B = [r]B + [k]([a]B) = R + [k]A.$$

This is the cofactorless equation. Multiplying both sides by 8 gives $[8][S]B = [8]R + [8][k]A$, the cofactored equation. $\square$

**Lemma 3 (the two checks differ only by a small order point).** For any decoded $A$, $R$ and any $S$, $k$, let $D = [S]B - R - [k]A$. The cofactorless check passes if and only if $D = O$. The cofactored check passes if and only if $[8]D = O$, that is, if $D$ is in the subgroup of order dividing 8.

*Proof.* Scalar multiplication by 8 is a group homomorphism, so $[8][S]B - [8]R - [8][k]A = [8]D$. The rest is the definition of the two checks. $\square$

For the key $A' = [a]B + T$ with $T$ of order 8 and a signature made with $a$ as in lines L4 to L8, $D = [S]B - R - [k][a]B - [k]T = -[k]T$. So the cofactored check always passes, and the cofactorless one passes if and only if $8$ divides $k$, as the tests show. $\blacksquare$
