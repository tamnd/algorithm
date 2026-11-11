---
tag: AE1DRR
kind: problem
slug: decisional-diffie-hellman
name: Decisional Diffie-Hellman problem
aliases:
- DDH
- DDH problem
- Decisional Diffie-Hellman assumption
- decisional Diffie-Hellman
area: cryptography/public-key
level: advanced
summary: Tell (g^x, g^y, g^(xy)) apart from (g^x, g^y, g^z) with z random. Easy in Z_p^* and on pairing curves, believed hard in prime order subgroups. ElGamal security rests on it.
prereqs: [computational-diffie-hellman, legendre-symbol]
see_also: [elgamal-encryption, cramer-shoup-cryptosystem, diffie-hellman, bilinear-pairing, safe-prime, shoup-generic-lower-bound, computational-indistinguishability, quadratic-residuosity-problem]
sources:
  - paper: "Dan Boneh, The decision Diffie-Hellman problem, ANTS-III, LNCS 1423, pages 48 to 63, 1998"
    locator: the survey of DDH, the groups where it fails and its applications
  - paper: "Moni Naor and Omer Reingold, Number-theoretic constructions of efficient pseudo-random functions, FOCS 1997, pages 458 to 467"
    locator: the random self-reduction of DDH and the pseudorandom function built on it
  - paper: doi:10.1007/3-540-69053-0_18
    title: Victor Shoup, Lower bounds for discrete logarithms and related problems, EUROCRYPT 1997, Lecture Notes in Computer Science 1233
    locator: pages 256 to 266, the generic lower bound for the decision problem
  - paper: "Antoine Joux and Kim Nguyen, Separating decision Diffie-Hellman from computational Diffie-Hellman in cryptographic groups, Journal of Cryptology 16(4), pages 239 to 247, 2003"
    locator: the pairing groups where DDH is easy and CDH is believed hard
  - paper: "Ronald Cramer and Victor Shoup, A practical public key cryptosystem provably secure against adaptive chosen ciphertext attack, CRYPTO 1998, LNCS 1462, pages 13 to 25"
    locator: the use of DDH in a prime order subgroup of Z_p^*
  - paper: "Yiannis Tsiounis and Moti Yung, On the security of ElGamal based encryption, PKC 1998, LNCS 1431, pages 117 to 134"
    locator: the equivalence of DDH and the semantic security of ElGamal
  - book: isbn:9780815354369
    title: Jonathan Katz and Yehuda Lindell, Introduction to Modern Cryptography, third edition, CRC Press, 2020
    locator: Chapter 9, the section on cryptographic assumptions in cyclic groups (the DDH experiment and the quadratic residue attack)
  - url: "https://toc.cryptobook.us/"
    title: Dan Boneh and Victor Shoup, A Graduate Course in Applied Cryptography, version 0.6, 2023
    locator: Chapter 10, the section on the decisional Diffie-Hellman assumption and its random self-reduction
---

The decisional Diffie-Hellman problem (DDH) asks to tell a Diffie-Hellman triple $(g^x, g^y, g^{xy})$ apart from a triple $(g^x, g^y, g^z)$ with $z$ random. The DDH assumption says that no efficient algorithm can do this in a given group. It is stronger than the [computational Diffie-Hellman](/computational-diffie-hellman/) assumption, and it is exactly what [ElGamal encryption](/elgamal-encryption/) needs for [IND-CPA security](/ind-cpa-security/). DDH fails in the full group $\mathbb{Z}_p^*$, because of the [Legendre symbol](/legendre-symbol/), and in groups with a pairing; it is believed to hold in prime order subgroups of $\mathbb{Z}_p^*$ and of most elliptic curves.

**Notation.** $G = \langle g \rangle$ is a cyclic group of order $q$; $q$ is a prime unless stated otherwise. $\lambda$ is the security parameter, $\mathcal{A}$ is an adversary that runs in time $t$, and $\mathrm{Adv}$ is its advantage. A *DH triple* is $(g^x, g^y, g^{xy})$. All results are in the standard model, except the generic bound, which is in the [generic group model](/generic-group-model/).

## In plain words

Two people do a Diffie-Hellman exchange in public, and an eavesdropper sees the two public values. Someone then shows the eavesdropper a third value: either the real shared key or a random element of the group. The problem asks the eavesdropper to say which one it is.

If the eavesdropper could compute the key, it could compare and win. But it may also win with less: one bit of the key that it can predict is enough. In some groups such a bit exists, and that breaks every scheme that needs the key to look random. In well-chosen groups no such bit is known, and the key looks like a random element to anyone without a secret number.

## Definition

**Input.** A description of $G$ and $g$, and a triple $(X, Y, Z) \in G^3$, where $X = g^x$ and $Y = g^y$ for uniform $x, y \in \mathbb{Z}_q$, and either $Z = g^{xy}$ or $Z = g^z$ for a uniform $z \in \mathbb{Z}_q$.

**Output.** A bit: 1 for "DH triple", 0 for "random triple".

**Advantage.**

$$\mathrm{Adv}^{\mathrm{ddh}}_G(\mathcal{A}) = \bigl|\Pr[\mathcal{A}(g, g^x, g^y, g^{xy}) = 1] - \Pr[\mathcal{A}(g, g^x, g^y, g^z) = 1]\bigr|.$$

**The DDH assumption.** For a family of groups indexed by $\lambda$, $\mathrm{Adv}^{\mathrm{ddh}}_G(\mathcal{A})$ is negligible in $\lambda$ for every adversary that runs in time polynomial in $\lambda$. In words: the two distributions of triples are [computationally indistinguishable](/computational-indistinguishability/).

## Variants

- **Multi-instance DDH.** Distinguish $(g^{x_i}, g^{y_j}, g^{x_i y_j})_{i,j}$ from random. The random self-reduction below shows that it is equivalent to DDH, with a tight reduction.
- **Hashed DDH and oracle DH.** Distinguish $H(g^{xy})$ from a random string, possibly with an oracle for $H(U^x)$ on $U \ne g^y$. This is the oracle Diffie-Hellman assumption of DHIES and [ECIES](/ecies/).
- **Decisional bilinear DH.** In a pairing group, DDH itself is easy, and the decisional problem moves to $e(g, g)^{xyz}$; see [bilinear Diffie-Hellman](/bilinear-diffie-hellman/).
- **Decision linear and matrix DDH.** Weaker assumptions that survive a symmetric pairing, used in pairing-based schemes.
- **DDH in groups of composite order.** In $\mathbb{Z}_n^*$ for an RSA modulus $n$, a subgroup decision problem appears; see the [quadratic residuosity problem](/quadratic-residuosity-problem/) for the closely related case of squares.

## Examples

**The full group $\mathbb{Z}_{23}^*$ fails.** $g = 5$ generates $\mathbb{Z}_{23}^*$, of order 22. An element $g^k$ is a square modulo 23 exactly when $k$ is even, and $xy$ is even exactly when $x$ or $y$ is even. So the [Legendre symbol](/legendre-symbol/) of $g^{xy}$ follows from those of $g^x$ and $g^y$. The test file enumerates all $22^3$ triples: on DH triples the distinguisher below says 1 every time, on random triples exactly half the time.

| triple | $x, y, z$ | squares? $(X, Y, Z)$ | rule $Z$ square iff $X$ or $Y$ square | answer |
|---|---|---|---|---|
| $(5^3, 5^5, 5^{15}) = (10, 20, 19)$ | $3, 5, 15$ | no, no, no | predicts no | 1 (correct) |
| $(5^3, 5^5, 5^{4}) = (10, 20, 4)$ | $3, 5, 4$ | no, no, yes | predicts no | 0 (correct) |
| $(5^3, 5^5, 5^{7}) = (10, 20, 17)$ | $3, 5, 7$ | no, no, no | predicts no | 1 (wrong) |

**The subgroup of squares works.** For the safe prime $p = 23 = 2 \cdot 11 + 1$, take $g = 4$, which generates the squares, a group of prime order 11. Every element is a square, so the Legendre symbol is always $+1$ and says nothing.

## Known algorithms

The obvious algorithm solves CDH and compares. Faster algorithms exist only when the group has extra structure.

**The Legendre distinguisher.** Let $g$ generate $\mathbb{Z}_p^*$, so $p - 1$ is even.

```pseudo id=main
LEGENDRE-DDH(p, X, Y, Z)              ▷ X = g^x, Y = g^y, g a generator of Z_p^*
L1  ex ← [X is a square mod p]        ▷ by Euler: X^((p−1)/2) = 1; true iff x is even
L2  ey ← [Y is a square mod p]
L3  ez ← [Z is a square mod p]
L4  return 1 if ez = (ex or ey) else 0
```

On a DH triple, $Z = g^{xy}$ is a square iff $xy$ is even iff $x$ or $y$ is even, so the output is always 1. On a random triple, $z$ is independent of $x$ and $y$, so $ez$ is a fair coin and the output is 1 with probability $\tfrac12$. The advantage is $\tfrac12$, at the cost of three exponentiations.

**Small factors of the group order.** The same idea works for every small prime $\ell$ that divides the order $n$ of $G$: raise $X$, $Y$, $Z$ to the power $n / \ell$, solve the three discrete logarithms in the subgroup of order $\ell$, and test the product rule there. This is why $G$ must have prime order (or a cofactor that is removed).

**Pairings.** If there is an efficiently computable bilinear map $e: G \times G \to G_T$ with $e(g, g) \ne 1$, then $(X, Y, Z)$ is a DH triple iff $e(X, Y) = e(g, Z)$. This makes DDH easy on supersingular curves and on other curves with small embedding degree, while CDH is still believed hard there (Joux and Nguyen, 2003). See [bilinear pairing](/bilinear-pairing/) and the [MOV reduction](/menezes-okamoto-vanstone-reduction/).

**Groups where DDH is believed hard.** The subgroup of squares of $\mathbb{Z}_p^*$ for a [safe prime](/safe-prime/) $p$; a subgroup of prime order $q$ of $\mathbb{Z}_p^*$ with $q \mid p - 1$; the prime order group of an elliptic curve with large embedding degree, such as P-256. In these groups the best known attack is to compute discrete logarithms.

## Bounds

**Generic lower bound.** In the generic group model, an algorithm that makes $m$ group operations in a group of prime order $q$ has DDH advantage $O(m^2 / q)$ (Shoup, 1997). So advantage $\varepsilon$ needs $\Omega((\varepsilon q)^{1/2})$ operations. The Legendre and pairing attacks are not generic: they use the representation of $\mathbb{Z}_p^*$ or of the curve.

**Upper bound.** DDH is never harder than CDH, so it falls to the [discrete logarithm](/discrete-logarithm-problem/) algorithms: $O(q^{1/2})$ operations by Pollard rho, and polynomial time on a quantum computer.

## Reductions

- **DDH $\le$ CDH $\le$ DL.** An algorithm for the discrete logarithm computes $g^{xy}$; an algorithm for CDH decides DDH. So the DDH assumption implies the CDH assumption, which implies the DL assumption.
- **CDH $\not\le$ DDH in general.** The pairing groups above have easy DDH and, as far as is known, hard CDH. No group is known where the converse gap occurs.
- **Random self-reducibility (Naor and Reingold, 1997).** In a group of prime order $q$, choose $a \in \{1, \ldots, q - 1\}$ and $b, c \in \mathbb{Z}_q$ uniform, and map

$$X' = X^a g^b, \quad Y' = Y g^c, \quad Z' = Z^a Y^b X^{ac} g^{bc}.$$

Then $x' = ax + b$, $y' = y + c$ and $z' - x'y' = a(z - xy)$. If $z = xy$, the output is a uniform DH triple. If $z \ne xy$, it is uniform among the triples with $z' \ne x'y'$, which is within statistical distance $1/q$ of a uniform triple. So a distinguisher that works on a fraction of the instances works on all of them, its advantage can be amplified by repetition, and many independent instances can be made from one. The test file checks the exact distribution for $q = 11$ by enumeration.

- **IND-CPA of ElGamal $\equiv$ DDH.** The reduction from DDH is tight: $\mathrm{Adv}^{\mathrm{ind\text{-}cpa}} = 2 \mathrm{Adv}^{\mathrm{ddh}}$ (proof on the [ElGamal](/elgamal-encryption/) page), and the converse also holds (Tsiounis and Yung, 1998).
- **DDH in $\mathbb{Z}_p^*$ and quadratic residuosity.** The Legendre attack is the case $\ell = 2$ of the small factor attack. Modulo a composite $N$ the analogous question, whether an element is a square, is the [quadratic residuosity problem](/quadratic-residuosity-problem/), which is hard without the factors of $N$.

## Applications

- **[ElGamal encryption](/elgamal-encryption/).** IND-CPA secure exactly when DDH holds.
- **[Cramer-Shoup](/cramer-shoup-cryptosystem/).** IND-CCA secure in the standard model under DDH and a target collision resistant hash.
- **Pseudorandom functions and generators.** The Naor-Reingold function $f(x_1 \ldots x_n) = g^{a_0 \prod_{x_i = 1} a_i}$ is a pseudorandom function under DDH. The map $(x, y) \mapsto (g^x, g^y, g^{xy})$ is a [pseudorandom generator](/pseudorandom-generator/) on group elements.
- **[Diffie-Hellman key exchange](/diffie-hellman/).** DDH says that the exchanged key is indistinguishable from a random group element, which a key derivation can then extract.
- **Voting and mix networks.** Rerandomized ElGamal ciphertexts are unlinkable under DDH.

The Python code next to this page implements the Legendre distinguisher and the random self-reduction. It is for study only and not constant time.

## References
