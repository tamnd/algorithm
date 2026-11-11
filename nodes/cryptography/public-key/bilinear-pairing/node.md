---
tag: VJKYK9
kind: definition
slug: bilinear-pairing
name: Bilinear pairing
aliases:
area: cryptography/public-key
level: advanced
summary: "A map e from G1 x G2 to GT, groups of prime order r, that is bilinear, non-degenerate and efficient. Built from the Weil or Tate pairing on elliptic curves; the base of IBE, BLS and SNARKs."
prereqs: [cyclic-group, elliptic-curve-cryptography]
see_also: [miller-algorithm, bilinear-diffie-hellman, menezes-okamoto-vanstone-reduction, bls-signature, boneh-franklin-ibe, decisional-diffie-hellman, finite-field-discrete-logarithm-problem, number-field-sieve-discrete-logarithm]
sources:
  - paper: "Steven D. Galbraith, Kenneth G. Paterson and Nigel P. Smart, Pairings for cryptographers, Discrete Applied Mathematics 156(16), 2008, pages 3113 to 3121"
    locator: the Types 1, 2 and 3 of pairings and what each type allows (hashing to G2, a homomorphism from G2 to G1, short elements)
  - paper: "Alfred J. Menezes, Tatsuaki Okamoto and Scott A. Vanstone, Reducing elliptic curve logarithms to logarithms in a finite field, IEEE Transactions on Information Theory 39(5), 1993, pages 1639 to 1646"
    locator: the use of the Weil pairing to move the discrete logarithm from E(F_p) to F_(p^k), and the small embedding degree of supersingular curves
  - paper: "Antoine Joux, A one round protocol for tripartite Diffie-Hellman, ANTS-IV, LNCS 1838, 2000, pages 385 to 393"
    locator: the first constructive use of a pairing, with a distortion map on a supersingular curve
  - paper: "Dan Boneh and Matthew Franklin, Identity-based encryption from the Weil pairing, Crypto 2001, LNCS 2139, pages 213 to 229"
    locator: the abstract bilinear map, the distortion map on y^2 = x^3 + 1, and the modified Weil pairing
  - paper: "Paulo S. L. M. Barreto and Michael Naehrig, Pairing-friendly elliptic curves of prime order, SAC 2005, LNCS 3897, pages 319 to 331"
    locator: the BN family with embedding degree 12
  - paper: "Taechan Kim and Razvan Barbulescu, Extended tower number field sieve, a new complexity for the medium prime case, Crypto 2016, LNCS 9814, pages 543 to 571"
    locator: the exTNFS algorithm for discrete logarithms in F_(p^k) for composite k, which lowers the security of pairing groups
  - paper: "Razvan Barbulescu and Sylvain Duquesne, Updating key size estimations for pairings, Journal of Cryptology 32, 2019"
    locator: the estimate of about 100 bits of security for BN254 after exTNFS, and new key sizes for BN, BLS12 and other families
  - url: "https://datatracker.ietf.org/doc/draft-irtf-cfrg-pairing-friendly-curves/"
    title: Yumi Sakemi, Tetsutaro Kobayashi, Tsunekazu Saito and Riad S. Wahby, Pairing-friendly curves, IRTF CFRG Internet-Draft
    locator: the parameters of BLS12-381 and BN462, and the security estimates for BN254 and BLS12-381
  - book: isbn:9781420071467
    title: Lawrence C. Washington, Elliptic Curves, Number Theory and Cryptography, second edition, Chapman and Hall/CRC, 2008
    locator: Chapter 11 (divisors, the Weil pairing and the Tate-Lichtenbaum pairing) and Section 5.3 (the MOV attack)
---

A bilinear pairing is a map $e : \mathbb{G}_1 \times \mathbb{G}_2 \to \mathbb{G}_T$ between groups of the same prime order $r$ that is linear in each argument, does not collapse to 1, and is fast to compute. On elliptic curves it comes from the Weil or Tate pairing, computed with [Miller's algorithm](/miller-algorithm/). Menezes, Okamoto and Vanstone used it in 1993 to attack curves with small embedding degree. From 2000 on, Joux's three-party key exchange, [Boneh-Franklin identity-based encryption](/boneh-franklin-ibe/) and [BLS signatures](/bls-signature/) used it to build schemes. Today pairings also run in aggregate signatures, [attribute-based encryption](/attribute-based-encryption/) and succinct zero-knowledge proofs.

**Notation.** $r$ is a prime. $\mathbb{G}_1$ and $\mathbb{G}_2$ are written additively with generators $P$ and $Q$, and $\mathbb{G}_T$ multiplicatively. $E$ is an elliptic curve over $\mathbb{F}_p$, $E[r]$ its points of order dividing $r$, and $\mu_r$ the $r$-th roots of unity in $\overline{\mathbb{F}}_p$. $\psi$ is a map between groups.

## Definition

A **bilinear pairing** (or bilinear map) is a map $e : \mathbb{G}_1 \times \mathbb{G}_2 \to \mathbb{G}_T$, where the three groups are cyclic of prime order $r$, with these properties:

1. **Bilinear.** $e(P_1 + P_2, Q) = e(P_1, Q)\,e(P_2, Q)$ and $e(P, Q_1 + Q_2) = e(P, Q_1)\,e(P, Q_2)$ for all points. It follows that $e(aP, bQ) = e(P, Q)^{ab}$ for all integers $a$ and $b$.
2. **Non-degenerate.** If $P$ generates $\mathbb{G}_1$ and $Q$ generates $\mathbb{G}_2$, then $e(P, Q)$ generates $\mathbb{G}_T$, that is, $e(P, Q) \ne 1$.
3. **Computable.** There is a polynomial time algorithm for $e$.

For cryptography the discrete logarithm problems in $\mathbb{G}_1$, $\mathbb{G}_2$ and $\mathbb{G}_T$ must also be hard. If $\mathbb{G}_1 = \mathbb{G}_2$ the pairing is **symmetric**.

### Types

Galbraith, Paterson and Smart (2008) sort pairings on curves by how $\mathbb{G}_1$ and $\mathbb{G}_2$ relate:

- **Type 1**: $\mathbb{G}_1 = \mathbb{G}_2$, a symmetric pairing. It comes from supersingular curves with a distortion map. The embedding degree is at most 2 over prime fields of large characteristic, so the groups are large for their security.
- **Type 2**: $\mathbb{G}_1 \ne \mathbb{G}_2$, and there is an efficient homomorphism $\psi : \mathbb{G}_2 \to \mathbb{G}_1$ (the trace), but no known way to hash into $\mathbb{G}_2$.
- **Type 3**: $\mathbb{G}_1 \ne \mathbb{G}_2$ and no efficient homomorphism is known in either direction, but hashing into $\mathbb{G}_2$ is possible. All the curves in use today (BN, BLS12) are Type 3.

Proofs written for Type 1 often use $e(P, P)$ or the symmetric structure, and must be checked again for Type 3.

### Pairings on elliptic curves

Let $E/\mathbb{F}_p$ have a subgroup of prime order $r$ with $r \nmid p$. The **embedding degree** $k$ is the smallest integer with $r \mid p^k - 1$. Then $\mu_r \subset \mathbb{F}_{p^k}^*$ and, when $k > 1$, all of $E[r] \cong \mathbb{Z}_r \times \mathbb{Z}_r$ is defined over $\mathbb{F}_{p^k}$.

- The **Weil pairing** $e_r : E[r] \times E[r] \to \mu_r$ is $e_r(P, Q) = (-1)^r f_{r,P}(Q) / f_{r,Q}(P)$, where $f_{r,P}$ is a function with divisor $r(P) - r(\mathcal{O})$. It is bilinear, alternating ($e_r(P, P) = 1$) and non-degenerate on $E[r]$.
- The **reduced Tate pairing** $t_r : E(\mathbb{F}_{p^k})[r] \times E(\mathbb{F}_{p^k}) / rE(\mathbb{F}_{p^k}) \to \mu_r$ is $t_r(P, Q) = f_{r,P}(Q)^{(p^k - 1)/r}$, computed by one Miller loop and one final exponentiation. It costs about half of the Weil pairing and is the base of the ate and optimal ate pairings used in practice.

Because $e_r(P, P) = 1$, a pairing on one cyclic group needs a second, independent point. A **distortion map** is an endomorphism $\phi$ of $E$ that sends $P \in E(\mathbb{F}_p)[r]$ outside the group generated by $P$. Then $e(P, Q) = t_r(P, \phi(Q))$ is a symmetric, non-degenerate pairing on $\langle P \rangle$.

### Security and the size of the groups

A pairing moves discrete logarithms: if $Q = xP$ then $e(Q, P) = e(P, P)^x$. So the [elliptic curve discrete logarithm](/elliptic-curve-discrete-logarithm-problem/) in $\mathbb{G}_1$ is no harder than the [discrete logarithm](/finite-field-discrete-logarithm-problem/) in $\mathbb{F}_{p^k}^*$. This is the [MOV reduction](/menezes-okamoto-vanstone-reduction/): it breaks curves with small $k$ that were chosen without care, and for pairing-friendly curves it fixes how large $p^k$ must be. In 2016 Kim and Barbulescu's extended tower number field sieve (exTNFS) made discrete logarithms in $\mathbb{F}_{p^k}$ cheaper when $k$ is composite. Barbulescu and Duquesne (2019) then estimated the curve BN254, designed for 128 bits, at about 100 bits of security. The newer curve BLS12-381 was chosen in 2017 to target about 128 bits after these attacks.

## Examples and non-examples

**The toy curve of the code.** $E : y^2 = x^3 + x$ over $\mathbb{F}_p$ with $p \equiv 3 \pmod 4$ is supersingular with $\#E(\mathbb{F}_p) = p + 1$. For a prime $r \mid p + 1$, the embedding degree is 2, $\mathbb{F}_{p^2} = \mathbb{F}_p[i]$ with $i^2 = -1$, and $\phi(x, y) = (-x, iy)$ is a distortion map: it maps $E(\mathbb{F}_p)$ to points with $x \in \mathbb{F}_p$ and $y \in i\mathbb{F}_p$. The pairing $e(P, Q) = t_r(P, \phi(Q))$ is a Type 1 pairing with $\mathbb{G}_T = \mu_r \subset \mathbb{F}_{p^2}^*$. The code uses a 128-binary-digit $p$ and $r = 2^{63} + 29$. That gives a discrete logarithm problem in $\mathbb{F}_{p^2}$ of only 256 binary digits, so it is not secure. The code is for study only and is not constant time. For real use, take a maintained library for BLS12-381, such as blst or MCL. There are no official test vectors for this toy curve, so the tests check the hand-sized case below, bilinearity and non-degeneracy with fixed seeds.

**A hand-sized case.** Take $p = 11$. Then $\#E(\mathbb{F}_{11}) = 12$, $r = 3$, and the points of order 3 are $G = (5, 3)$ and $2G = (5, 8)$. The tangent at $G$ has slope $\lambda = (3 \cdot 25 + 1)/(2 \cdot 3) = 9$ in $\mathbb{F}_{11}$, and $\phi(G) = (-5, 3i) = (6, 3i)$. The Miller loop for $r = 3$ is one tangent line (the next line, through $2G$ and $G$, is vertical and is dropped because its value lies in $\mathbb{F}_{11}$):

| step | computation | value |
|---|---|---|
| line | $y - 3 - 9(x - 5)$ at $\phi(G) = (6, 3i)$: $3i - 3 - 9$ | $f = 10 + 3i$ |
| $f^{p-1}$ | $\bar{f}/f = (10 - 3i)/(10 + 3i)$ | $8 + 5i$ |
| $(\cdot)^{(p+1)/r}$ | $(8 + 5i)^4$ | $e(G, G) = 5 + 3i$ |

Then $(5 + 3i)^2 = 5 + 8i = e(G, 2G) = e(2G, G)$, $(5 + 3i)^3 = 1$, and $e(2G, 2G) = (5 + 3i)^4 = 5 + 3i$, as bilinearity says.

**BN254 and BLS12-381.** Barreto-Naehrig curves have prime order, $k = 12$, and a sextic twist that puts $\mathbb{G}_2$ on a curve over $\mathbb{F}_{p^2}$. BN254 (a 254-binary-digit $p$) is in the Ethereum precompiles. BLS12-381 has a 381-binary-digit $p$, a 255-binary-digit $r$ and $k = 12$. It is used in Zcash, Ethereum consensus and the [BLS signatures](/bls-signature/) of the CFRG drafts.

**Non-example: a trivial bilinear map.** Let $\mathbb{G}_1 = \mathbb{G}_2 = (\mathbb{Z}_r, +)$, $\mathbb{G}_T = \langle g \rangle$, and $e(a, b) = g^{ab}$. This map is bilinear, non-degenerate and computable, but the discrete logarithm in $\mathbb{G}_1$ is trivial, so it is useless for cryptography.

**Non-example: a curve with large embedding degree.** For a random curve, such as the curves of ECDSA, $k$ is about as large as $r$. The Weil pairing still exists, but its values lie in $\mathbb{F}_{p^k}$ with $k$ of hundreds of binary digits, so it is not computable. This is good for those curves: the MOV reduction does not apply.

**Non-example: the Tate pairing without a distortion map on a Type 1 curve.** For $P, Q \in E(\mathbb{F}_p)[r]$ with $k = 2$, every line value lies in $\mathbb{F}_p$, so $f_{r,P}(Q)^{(p^2-1)/r} = 1$, since $p - 1$ divides the exponent. The distortion map is what makes the pairing non-degenerate.

## Related definitions

- **[Miller's algorithm](/miller-algorithm/)** computes $f_{r,P}$ at a point in $O(\log r)$ steps, and so the Weil and Tate pairings.
- **[Bilinear Diffie-Hellman](/bilinear-diffie-hellman/)** is the hardness assumption most pairing schemes use. With a Type 1 pairing, [DDH](/decisional-diffie-hellman/) is easy in $\mathbb{G}_1$: $(P, aP, bP, cP)$ is a DH tuple if and only if $e(aP, bP) = e(P, cP)$.
- **[Identity-based encryption](/identity-based-encryption/)**, [BLS signatures](/bls-signature/), [aggregate signatures](/aggregate-signature/) and [attribute-based encryption](/attribute-based-encryption/) are the main constructions.
- **Multilinear maps** would extend $e$ to more than two arguments. Candidate constructions since 2013 have been attacked, and none is in use.

## References
