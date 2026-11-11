---
tag: 42KE82
kind: definition
slug: bilinear-diffie-hellman
name: Bilinear Diffie-Hellman assumption
aliases:
- BDH
area: cryptography/public-key
level: research
summary: "The assumption that, given P, aP, bP and cP in a pairing group, no efficient algorithm computes e(P,P)^(abc). Boneh-Franklin IBE rests on it; DBDH is its decisional form."
prereqs: [bilinear-pairing, computational-diffie-hellman]
see_also: [decisional-diffie-hellman, boneh-franklin-ibe, identity-based-encryption, miller-algorithm, menezes-okamoto-vanstone-reduction, generic-group-model, bls-signature, attribute-based-encryption]
sources:
  - paper: "Dan Boneh and Matthew Franklin, Identity-based encryption from the Weil pairing, Crypto 2001, LNCS 2139, pages 213 to 229"
    locator: the definition of the BDH problem, the BDH parameter generator and the BDH assumption, and the remark that BDH is no harder than CDH in either group
  - paper: "Dan Boneh and Matthew Franklin, Identity-based encryption from the Weil pairing, SIAM Journal on Computing 32(3), 2003, pages 586 to 615"
    locator: the section on bilinear maps and the BDH assumption (the full version)
  - paper: "Antoine Joux, A one round protocol for tripartite Diffie-Hellman, ANTS-IV, LNCS 1838, 2000, pages 385 to 393"
    locator: the three-party key e(P,P)^(abc), whose security is the BDH problem
  - paper: "Antoine Joux and Kim Nguyen, Separating decision Diffie-Hellman from computational Diffie-Hellman in cryptographic groups, Journal of Cryptology 16(4), 2003, pages 239 to 247"
    locator: the use of the Weil and Tate pairings with a distortion map to decide DDH on supersingular curves, where CDH is still believed hard
  - paper: "Dan Boneh and Xavier Boyen, Efficient selective-ID secure identity based encryption without random oracles, Eurocrypt 2004, LNCS 3027, pages 223 to 238"
    locator: the decisional BDH assumption and the q-BDHI assumption, and the two schemes built on them
  - paper: "Dan Boneh and Xavier Boyen, Short signatures without random oracles, Eurocrypt 2004, LNCS 3027, pages 56 to 73"
    locator: the q-SDH assumption and its lower bound in the generic group model
  - paper: "Dan Boneh, Xavier Boyen and Eu-Jin Goh, Hierarchical identity based encryption with constant size ciphertext, Eurocrypt 2005, LNCS 3494, pages 440 to 456"
    locator: the appendix with a general generic group bound for Diffie-Hellman type problems in bilinear groups
  - paper: "Jung Hee Cheon, Security analysis of the strong Diffie-Hellman problem, Eurocrypt 2006, LNCS 4004, pages 1 to 11"
    locator: the algorithm that recovers x from P, xP and x^d P when d divides r - 1, and the variant for d dividing r + 1
---

The bilinear Diffie-Hellman (BDH) assumption says that, in a group with a [bilinear pairing](/bilinear-pairing/) $e$, nobody can compute $e(P, P)^{abc}$ from $P$, $aP$, $bP$ and $cP$ in reasonable time. Antoine Joux's one-round three-party key exchange of 2000 gives exactly this value as the shared key, and Dan Boneh and Matthew Franklin named the problem and stated the assumption in 2001 for their [identity-based encryption](/boneh-franklin-ibe/). The assumption is needed because a pairing makes the [decisional Diffie-Hellman problem](/decisional-diffie-hellman/) easy in the source group, so the usual DDH assumption fails there. BDH and its decisional form DBDH became the base assumptions of pairing-based cryptography. Later schemes use stronger assumptions with $q$ powers of a secret, such as q-SDH and q-BDHI, and these lose some security to Cheon's attack.

**Notation.** $\kappa$ is the security parameter. A **BDH parameter generator** $\mathcal{G}(\kappa)$ outputs a prime $r$ of about $2\kappa$ binary digits, groups $\mathbb{G}_1 = \langle P \rangle$ (written additively) and $\mathbb{G}_T$ (written multiplicatively) of order $r$, and a symmetric pairing $e : \mathbb{G}_1 \times \mathbb{G}_1 \to \mathbb{G}_T$ that is bilinear, non-degenerate and efficiently computable. $g = e(P, P)$ generates $\mathbb{G}_T$. $\mathcal{A}$ is an adversary and $\mathrm{Adv}$ its advantage. "X $\le$ Y" means that X is no harder than Y: an algorithm for Y gives one for X with a polynomial overhead.

## Definition

**BDH problem.** Given $(P, aP, bP, cP)$ for uniform $a, b, c \in \mathbb{Z}_r^*$, compute $e(P, P)^{abc}$.

**BDH assumption.** For every probabilistic polynomial time $\mathcal{A}$,

$$\mathrm{Adv}^{\mathrm{bdh}}(\mathcal{A}) = \Pr\bigl[\mathcal{A}(P, aP, bP, cP) = e(P, P)^{abc}\bigr]$$

is a negligible function of $\kappa$. The probability is over the output of $\mathcal{G}(\kappa)$, the choice of $a, b, c$ and the coins of $\mathcal{A}$.

**Decisional BDH (DBDH) assumption.** For every probabilistic polynomial time $\mathcal{A}$, with $z$ uniform in $\mathbb{Z}_r$,

$$\mathrm{Adv}^{\mathrm{dbdh}}(\mathcal{A}) = \Bigl|\Pr\bigl[\mathcal{A}(P, aP, bP, cP, g^{abc}) = 1\bigr] - \Pr\bigl[\mathcal{A}(P, aP, bP, cP, g^{z}) = 1\bigr]\Bigr|$$

is negligible. Under DBDH, $g^{abc}$ is a pseudorandom element of $\mathbb{G}_T$, so it can mask a message, as in the [Boneh-Boyen](/identity-based-encryption/) and [attribute-based](/attribute-based-encryption/) schemes. Under BDH alone, a scheme must hash $g^{abc}$ in the [random oracle model](/random-oracle-model/) to get a pseudorandom key, as [Boneh-Franklin IBE](/boneh-franklin-ibe/) does.

Asymmetric pairings $e : \mathbb{G}_1 \times \mathbb{G}_2 \to \mathbb{G}_T$ of Type 3 have no efficient map between $\mathbb{G}_1$ and $\mathbb{G}_2$, so the problem has several forms, with some of the inputs in $\mathbb{G}_1$ and some in $\mathbb{G}_2$. A scheme on such curves must state the form its proof uses.

### Relations to other problems

**Theorem.** In the setting above:

1. BDH $\le$ CDH in $\mathbb{G}_1$.
2. BDH $\le$ CDH in $\mathbb{G}_T$.
3. DBDH $\le$ BDH.
4. CDH in $\mathbb{G}_1$ $\le$ DL in $\mathbb{G}_1$ $\le$ DL in $\mathbb{G}_T$.
5. DDH in $\mathbb{G}_1$ can be decided in polynomial time.

*Proof.* (1) A CDH solver in $\mathbb{G}_1$ maps $(aP, bP)$ to $abP$, and then $e(abP, cP) = g^{abc}$. (2) The values $g$, $e(aP, bP) = g^{ab}$ and $e(P, cP) = g^{c}$ are a CDH instance in $\mathbb{G}_T$ with base $g$, and its answer is $g^{abc}$. (3) Compute $g^{abc}$ with the BDH solver and compare it with the fifth input. (4) The first step is the usual one for [CDH](/computational-diffie-hellman/). For the second, given $Q = xP$, compute $g$ and $e(P, Q) = g^x$, and take the discrete logarithm in $\mathbb{G}_T$; since $e$ is non-degenerate and $r$ is prime, $g \ne 1$ generates $\mathbb{G}_T$, so the answer is $x \bmod r$. This is the [MOV reduction](/menezes-okamoto-vanstone-reduction/). (5) For $(P, aP, bP, cP)$, test whether $e(aP, bP) = e(P, cP)$. The two sides are $g^{ab}$ and $g^c$, and $g$ has order $r$, so they are equal if and only if $c \equiv ab \pmod r$. $\square$

No reduction in the other direction is known in general, so BDH may be easier than CDH in either group. A group like $\mathbb{G}_1$, in which DDH is easy but CDH is believed hard, is called a **gap Diffie-Hellman group**. [BLS signatures](/bls-signature/) use this gap: the pairing checks a DH tuple, and forging a signature is a CDH problem.

**Random self-reduction.** Given $(P, aP, bP, cP)$, pick uniform $s, t, u \in \mathbb{Z}_r^*$ and form $(P, saP, tbP, ucP)$, a uniform instance. If $Z$ answers it, $Z^{(stu)^{-1} \bmod r}$ answers the first instance. So BDH is as hard on average as for each fixed $P$.

**Generic lower bound.** In the generic model of a bilinear group, an algorithm that solves BDH or DBDH with constant probability needs about $\sqrt{r}$ group operations. Boneh, Boyen and Goh give a general bound of this form for a large class of Diffie-Hellman type problems. Real pairing groups are not generic: the best attacks take discrete logarithms either in $\mathbb{G}_1$, with [Pollard rho](/pollard-rho-discrete-logarithm/) in about $\sqrt{r}$ steps, or in $\mathbb{G}_T \subset \mathbb{F}_{p^k}^*$, with the number field sieve. So $r$ and $p^k$ must both be large; see [bilinear pairing](/bilinear-pairing/) for the sizes.

### Assumptions with $q$ powers

Many later schemes give out $xP, x^2P, \ldots, x^qP$ for a secret $x$, where $q$ grows with the number of keys or signatures.

- **q-SDH** (strong Diffie-Hellman, Boneh and Boyen 2004). Given $(P, xP, x^2P, \ldots, x^qP)$, output a pair $(c, \frac{1}{x + c}P)$ for any $c \in \mathbb{Z}_r$ with $x + c \ne 0$. It is the assumption behind the Boneh-Boyen short signatures. Boneh and Boyen prove that a generic algorithm needs about $\sqrt{r/q}$ group operations.
- **q-BDHI** (bilinear Diffie-Hellman inversion, Boneh and Boyen 2004). Given $(P, xP, x^2P, \ldots, x^qP)$, compute $e(P, P)^{1/x}$. Its decisional form is the assumption of the second selective-ID scheme of Boneh and Boyen.

For $q = 1$, q-BDHI is close to BDH. As $q$ grows, the problems give the adversary more information, and they get easier.

**Cheon's attack (Eurocrypt 2006).** Let $d$ divide $r - 1$. Given $P$, $xP$ and $x^dP$, Cheon recovers $x$ with $O\bigl(\log r \cdot (\sqrt{(r-1)/d} + \sqrt{d})\bigr)$ group operations. The idea: write $x = \zeta^k$ for a generator $\zeta$ of $\mathbb{Z}_r^*$. Then $x^d$ lies in the subgroup of order $(r-1)/d$, so a [baby-step giant-step](/baby-step-giant-step/) search on the multiples of $P$ finds $k \bmod (r-1)/d$; a second search of size $\sqrt{d}$ finds the rest of $k$. A similar method works when $d$ divides $r + 1$ and $x^iP$ is known for $i \le 2d$. A q-SDH or q-BDHI instance with $q \ge d$ gives these inputs, and $x$ solves both problems. For $d \approx q$ the cost falls from about $\sqrt{r}$ to about $\sqrt{r/q}$, so a scheme that gives out $2^{40}$ powers can lose up to 20 binary digits of security if $r - 1$ has a divisor of that size. The defenses are to choose $r$ so that $r - 1$ and $r + 1$ have no divisors of the sizes that matter, or to make $r$ larger.

## Examples and non-examples

**A hand-sized instance.** Take the curve $y^2 = x^3 + x$ over $\mathbb{F}_{59}$ with $r = 5$ and the pairing $e(A, B) = t_5(A, \phi(B))$ with the distortion map $\phi(x, y) = (-x, iy)$, computed with [Miller's algorithm](/miller-algorithm/). The point $G = (35, 31)$ has order 5, with $2G = (25, 29)$, $3G = (25, 30)$ and $4G = (35, 28)$. The pairing gives $g = e(G, G) = 42 + 19i$ in $\mathbb{F}_{59^2}$, and

| $k$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $g^k$ | $42 + 19i$ | $46 + 3i$ | $46 + 56i$ | $42 + 40i$ | $1$ |

For $a = 2$, $b = 3$, $c = 4$ the instance is $(G, (25, 29), (25, 30), (35, 28))$, and $abc = 24 \equiv 4 \pmod 5$, so the answer is $g^4 = 42 + 40i$. In a group of order 5 a search over four values gives $a$, and then $e(bG, cG)^a = (46 + 3i)^2 = 42 + 40i$. The problem is hard only when $r$ and the field $\mathbb{F}_{p^k}$ are large.

**DDH is easy in the same group.** For $(G, 2G, 3G, D)$ the tuple is a DH tuple when $D = 6G = G$. The test of part (5) gives $e(2G, 3G) = g^6 = g = e(G, G)$, so it accepts $D = G$, and $e(G, 2G) = g^2 \ne g$, so it rejects $D = 2G$. This is why pairing schemes cannot use the DDH assumption in $\mathbb{G}_1$ and use DBDH in its place.

**Joux's three-party key exchange.** Three parties publish $aP$, $bP$ and $cP$. Each one computes the same key from its own secret and the two other public values, for example $e(bP, cP)^a = g^{abc}$. An eavesdropper sees a BDH instance. If the parties use $g^{abc}$ directly as a group element key, they need DBDH; if they hash it, BDH in the random oracle model is enough.

**The code with this page.** The Python file builds BDH and DBDH instances on a toy curve with a 128-binary-digit $p$ and $r = 2^{63} + 29$, runs the reductions of parts (1) and (2) against simulated oracles, and decides DDH in $\mathbb{G}_1$ with the pairing. The toy curve is not secure: the discrete logarithm in $\mathbb{F}_{p^2}$ of 256 binary digits is within reach. The code is for study only and is not constant time; real pairing code should use a maintained library such as blst or MCL for BLS12-381. BDH is an assumption and has no official test vectors, so the tests check the hand-sized instance above and the algebra with fixed seeds.

**Non-example: a degenerate map.** On the same curve without the distortion map, the reduced Tate pairing of two points of $E(\mathbb{F}_p)[r]$ is always 1. The "answer" $e(P, P)^{abc}$ is then 1 for every instance, and the problem is trivial. Non-degeneracy is part of the setting for a reason.

**Non-example: a small target field.** If $p^k$ is small enough for the number field sieve, part (4) gives $a$ from $e(P, aP)$, and BDH falls. Supersingular curves over prime fields have $k \le 2$, so they need a very large $p$ for the same security; this is one reason why practice moved to curves such as BLS12-381 with $k = 12$.

## Related definitions

- **[Computational Diffie-Hellman](/computational-diffie-hellman/)** and **[decisional Diffie-Hellman](/decisional-diffie-hellman/)** are the one-group problems. BDH is no harder than CDH in either group, and a symmetric pairing makes DDH in $\mathbb{G}_1$ easy.
- **[Bilinear pairing](/bilinear-pairing/)** gives the setting; **[Miller's algorithm](/miller-algorithm/)** computes it.
- **[Discrete logarithm problem](/discrete-logarithm-problem/)**: BDH is no harder than the discrete logarithm in $\mathbb{G}_1$ or in $\mathbb{G}_T$, through the [MOV reduction](/menezes-okamoto-vanstone-reduction/).
- **[Generic group model](/generic-group-model/)**: the model in which the lower bounds for BDH, DBDH and q-SDH hold.
- **[Identity-based encryption](/identity-based-encryption/)**: [Boneh-Franklin IBE](/boneh-franklin-ibe/) is IND-ID-CCA secure under BDH in the random oracle model, and the Boneh-Boyen schemes use DBDH and decisional q-BDHI without random oracles.
- **[Attribute-based encryption](/attribute-based-encryption/)**: the first KP-ABE scheme of Goyal, Pandey, Sahai and Waters is secure under DBDH.

## References
