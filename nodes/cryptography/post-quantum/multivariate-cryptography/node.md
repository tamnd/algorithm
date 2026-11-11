---
tag: V5Q3SF
kind: concept
slug: multivariate-cryptography
name: Multivariate cryptography
aliases:
- multivariate public-key cryptography
- MPKC
area: cryptography/post-quantum
level: intro
summary: Public-key schemes whose public key is a system of quadratic polynomials over a finite field with a hidden easy structure. UOV and its variants are in the NIST signature process.
prereqs: [digital-signature]
see_also: [multivariate-quadratic-problem, unbalanced-oil-and-vinegar, rainbow-signature, hidden-field-equations, xl-algorithm, f4-algorithm, code-based-cryptography, post-quantum-cryptography]
sources:
  - paper: "Tsutomu Matsumoto and Hideki Imai, Public quadratic polynomial-tuples for efficient signature-verification and message-encryption, Eurocrypt 1988, LNCS 330, pages 419 to 453"
    locator: the whole paper (the C* scheme, the first scheme with the trapdoor shape T, F, S)
  - paper: "Jacques Patarin, Hidden fields equations (HFE) and isomorphisms of polynomials (IP): two new families of asymmetric algorithms, Eurocrypt 1996, LNCS 1070, pages 33 to 48"
    locator: the whole paper (HFE, the big field family)
  - paper: "Aviad Kipnis, Jacques Patarin and Louis Goubin, Unbalanced oil and vinegar signature schemes, Eurocrypt 1999, LNCS 1592, pages 206 to 222"
    locator: the whole paper (UOV, the small field family)
  - paper: "Jintai Ding and Dieter Schmidt, Rainbow, a new multivariable polynomial signature scheme, ACNS 2005, LNCS 3531, pages 164 to 175"
    locator: the whole paper (Rainbow, several layers of oil and vinegar)
  - paper: "Ward Beullens, Breaking Rainbow takes a weekend on a laptop, Crypto 2022, LNCS 13508, pages 464 to 479"
    locator: the whole paper (key recovery for the Rainbow security level 1 parameters in about 53 hours on a laptop; also IACR ePrint 2022/214)
  - paper: "Chengdong Tao, Albrecht Petzoldt and Jintai Ding, Efficient key recovery for all HFE signature variants, Crypto 2021, LNCS 12825, pages 70 to 93"
    locator: the whole paper (the attack that broke GeMSS)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Multivariate public key cryptography by Jintai Ding and Bo-Yin Yang (the trapdoor shape, the big field and small field families, and the attacks)
  - url: "https://doi.org/10.6028/NIST.IR.8610"
    title: NIST IR 8610, Status Report on the Second Round of the Additional Digital Signature Schemes for the NIST Post-Quantum Cryptography Standardization Process, May 2026
    locator: Section 1 (the multivariate candidates are all variants of UOV, and the attacks of the second round), Sections 3.11 to 3.14 (UOV, MAYO, QR-UOV and SNOVA)
---

Multivariate cryptography builds public-key schemes, mostly [digital signatures](/digital-signature/), from systems of quadratic polynomials in many variables over a small finite field. The public key is a map $\mathcal{P} : \mathbb{F}_q^n \to \mathbb{F}_q^m$ given by $m$ quadratic polynomials. Anyone can evaluate it, but finding a preimage of a given value is the [multivariate quadratic problem](/multivariate-quadratic-problem/), which is NP-hard in general. The owner of the secret key knows a hidden structure that makes preimages easy. The idea goes back to C* by Matsumoto and Imai (1988). Many schemes have been broken, but the oil and vinegar family, from 1997 and 1999, stands. No quantum algorithm is known that solves these systems much faster than a square root of the classical cost, so this is a branch of [post-quantum cryptography](/post-quantum-cryptography/).

**Notation.** $\mathbb{F}_q$ is a finite field with $q$ elements, $n$ is the number of variables and $m$ the number of polynomials. $\mathcal{P} = (p_1, \ldots, p_m)$ is the public map, $\mathcal{F}$ the central map, and $S$, $T$ invertible affine maps of $\mathbb{F}_q^n$ and $\mathbb{F}_q^m$. $\mathcal{H}$ is a hash function onto $\mathbb{F}_q^m$. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. **Security model.** The signature schemes aim at existential unforgeability under chosen message attack (EUF-CMA) in the random oracle model. That needs two assumptions: preimages of $\mathcal{P}$ are hard to find (an MQ instance), and $\mathcal{P}$ cannot be told apart from a random quadratic map well enough to recover $\mathcal{F}$, $S$ or $T$.

## In plain words

Write down a few hundred quadratic equations in a few hundred unknowns, with all arithmetic done modulo a small prime or in a small field. Checking a proposed solution is fast: put the numbers in and evaluate. Finding a solution from scratch is very hard, even for computers built for algebra.

The trick is to start from a special system that is easy to solve, for example one where fixing some unknowns makes the rest linear. Then mix the unknowns and the equations with secret linear changes, so that the published system looks random. A signer undoes the mixing, solves the easy system, and mixes back. A verifier only evaluates the published polynomials.

## The idea

**The trapdoor shape.** Almost all schemes use

$$\mathcal{P} = T \circ \mathcal{F} \circ S,$$

where the central map $\mathcal{F}$ is quadratic and easy to invert, and $S$ and $T$ hide its structure. The public key is the list of coefficients of $\mathcal{P}$, about $m \binom{n+2}{2}$ field elements. To sign a message $M$, compute $y = \mathcal{H}(M)$, then $y' = T^{-1}(y)$, a preimage $x'$ with $\mathcal{F}(x') = y'$, and $x = S^{-1}(x')$. To verify, check $\mathcal{P}(x) = \mathcal{H}(M)$. Signatures need $n \ge m$, so that every $y$ has preimages; encryption needs $m \ge n$, so that the preimage is unique.

**Big field schemes.** Identify $\mathbb{F}_q^n$ with the extension field $\mathbb{F}_{q^n}$. A map such as $X \mapsto X^{q^\theta + 1}$ is quadratic over $\mathbb{F}_q$ in the coordinates of $X$. C* uses this monomial; [HFE](/hidden-field-equations/) uses a polynomial of low degree in $X$, which the owner inverts with a root finding algorithm. Patarin broke C* in 1995, and key recovery attacks broke HFE and its signature variants, the last being GeMSS in 2021.

**Small field schemes.** In [oil and vinegar](/unbalanced-oil-and-vinegar/) the central polynomials have no products of two oil variables. Fixing the vinegar variables at random makes $\mathcal{F}$ a linear system in the oil variables, which the signer solves. [Rainbow](/rainbow-signature/) stacks several oil and vinegar layers to get smaller keys.

**Attacks.** Generic attacks solve the public system: exhaustive search, [linearization and XL](/xl-algorithm/), and Gröbner basis algorithms such as [F4](/f4-algorithm/) and F5. Structural attacks find the hidden $\mathcal{F}$, $S$ and $T$: linear algebra on the shape of the central map (the Kipnis-Shamir attack on balanced oil and vinegar), rank attacks (MinRank), and differential attacks. A scheme needs parameters that resist both.

## Examples

**A central polynomial over $\mathbb{F}_7$.** Take $f(v, o) = v o + 3 v^2$ with vinegar $v$ and oil $o$. There is no $o^2$ term. To find a preimage of 5, fix $v = 1$; then $f = o + 3$, a linear equation, and $o = 2$ gives $f(1, 2) = 2 + 3 = 5$. A real scheme has $m$ such polynomials, $v$ vinegar and $m$ oil variables, and the signer solves an $m \times m$ linear system.

**The status in 2026.**

- Rainbow was a finalist of round 3 of the NIST process for post-quantum signatures. Beullens broke it in 2022: his attack recovered a security level 1 key in about 53 hours on a laptop.
- GeMSS, an HFE variant and an alternate in the same round, fell to the key recovery attack of Tao, Petzoldt and Ding (Crypto 2021).
- In October 2024 NIST moved 14 schemes to the second round of its process for additional signatures. Four of them, UOV, MAYO, QR-UOV and SNOVA, are variants of UOV.
- In May 2026 NIST moved all four to the third round (NIST IR 8610). New attacks in round 2, among them the wedge attack on fields of characteristic 2, put some parameter sets of UOV, MAYO and SNOVA below their targets. No proposed parameter set of QR-UOV was broken.

**Sizes.** UOV gives signatures as small as 96 bytes at NIST security category 1 with very fast verification, but its expanded public key is over 200 kilobytes (NIST IR 8610). MAYO, QR-UOV and SNOVA add structure to make the key smaller.

## Where it is used

- **Signatures for special uses.** Short signatures with very fast verification but large public keys, for example where the key is stored once and many signatures are checked. No multivariate scheme is in a NIST standard yet; use a reviewed library and a NIST standard signature, such as [ML-DSA](/crystals-dilithium/), for general use.
- **Encryption.** Multivariate encryption has a poor record: C*, HFE and many others were broken. No multivariate encryption scheme is a NIST candidate.
- **MQ without a trapdoor.** MQ is also the base of schemes with no hidden structure: the identification scheme of Sakumoto, Shirai and Hiwatari, MQDSS, and the NIST round 3 candidate MQOM, which uses MPC in the head. These rest only on the hardness of random MQ instances.
- **Cryptanalysis.** The same Gröbner basis and XL tools are used in algebraic attacks on block ciphers and stream ciphers.

## References
