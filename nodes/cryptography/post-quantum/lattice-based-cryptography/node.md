---
tag: 6EV6NN
kind: concept
slug: lattice-based-cryptography
name: Lattice-based cryptography
aliases:
- lattice cryptography
area: cryptography/post-quantum
level: intro
summary: Cryptography whose security rests on hard lattice problems such as LWE, SIS and NTRU. It has worst-case hardness proofs, resists known quantum attacks, and is the base of ML-KEM and ML-DSA.
prereqs: [lattice, shortest-vector-problem]
see_also: [learning-with-errors, short-integer-solution, ntru-problem, core-svp-hardness, post-quantum-cryptography, crystals-kyber, crystals-dilithium, falcon]
sources:
  - paper: "Chris Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4), 2016"
    locator: Section 2 (lattices and the worst-case problems), Section 3 (early schemes, including Ajtai's function and NTRU), Section 4 (SIS, LWE, Ring-SIS and Ring-LWE with their reductions)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Lattice-based Cryptography by Daniele Micciancio and Oded Regev
  - paper: "Miklos Ajtai, Generating hard instances of lattice problems, STOC 1996, pages 99 to 108"
    locator: the first worst-case to average-case reduction for a lattice problem (the one-way function behind SIS)
  - paper: "Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, Journal of the ACM 56(6), Article 34, 2009"
    locator: Section 1 (the LWE problem, its quantum hardness, and the public-key scheme)
  - url: "https://doi.org/10.6028/NIST.FIPS.203"
    title: NIST, FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, August 2024
    locator: the introduction and the overview of ML-KEM (security based on the Module-LWE problem)
  - url: "https://doi.org/10.6028/NIST.FIPS.204"
    title: NIST, FIPS 204, Module-Lattice-Based Digital Signature Standard, August 2024
    locator: the introduction and the overview of ML-DSA (security based on Module-LWE and Module-SIS)
  - url: "https://falcon-sign.info/"
    title: Pierre-Alain Fouque and others, Falcon, Fast-Fourier Lattice-based Compact Signatures over NTRU, specification version 1.2, 2020
    locator: the design rationale (NTRU lattices and the GPV hash-and-sign framework)
  - url: "https://csrc.nist.gov/projects/post-quantum-cryptography"
    title: NIST, Post-Quantum Cryptography project page
    locator: the status of FN-DSA (FIPS 206), the standard planned from Falcon
---

Lattice-based cryptography is the part of [post-quantum cryptography](/post-quantum-cryptography/) whose security rests on the hardness of problems about [lattices](/lattice/), mostly through the average-case problems [learning with errors](/learning-with-errors/) (LWE), the [short integer solution](/short-integer-solution/) problem (SIS) and the [NTRU problem](/ntru-problem/). Many of its schemes have proofs that break them only if a worst-case lattice problem is easy, and no quantum algorithm is known that solves these problems much faster than classical ones. It is the base of the NIST standards ML-KEM ([CRYSTALS-Kyber](/crystals-kyber/)) and ML-DSA ([CRYSTALS-Dilithium](/crystals-dilithium/)), and of the coming FN-DSA ([Falcon](/falcon/)).

**Notation.** $n$ is the lattice or problem dimension, $q$ a modulus (not a number of queries), $\lambda_1(L)$ the length of a shortest nonzero vector of a lattice $L$, $\gamma \ge 1$ an approximation factor, and $\lambda$ the security parameter.

## In plain words

A lattice is a regular grid of points in a space with many dimensions, made by adding whole-number multiples of a few base arrows. The same grid has many sets of base arrows. Some are short and nearly at right angles; others are long and almost parallel. With a good set, it is easy to find the grid point nearest to a given point. With a bad set, the task seems very hard when there are hundreds of dimensions.

Lattice cryptography gives out a bad description of a grid, or a point near the grid, and keeps the good description or the hidden offset secret. Breaking the scheme means solving a grid problem that has resisted decades of study. Quantum computers break RSA and elliptic curves because those rest on hidden repeating patterns, and no such pattern is known in lattice problems.

## The idea

**Lattices and bases.** A lattice is a set $L = \{\sum_{i=1}^{n} z_i b_i : z_i \in \mathbb{Z}\}$ for linearly independent vectors $b_1, \ldots, b_n \in \mathbb{R}^n$, the [basis](/lattice-basis/). Two bases $B$ and $B'$ give the same lattice exactly when $B' = U B$ for an integer matrix $U$ with $\det U = \pm 1$. All bases have the same $|\det B|$, the volume of the lattice. Short, nearly orthogonal bases are "good"; [LLL](/lll-algorithm/) and [BKZ](/bkz-algorithm/) turn a bad basis into a better one, but in high dimension they reach only an approximation factor that is exponential in $n$ (LLL) or that costs time exponential in the block size (BKZ).

**The hard problems.** The schemes rest on a few worst-case problems:

- [SVP](/shortest-vector-problem/): find a nonzero vector of length $\lambda_1(L)$. The approximate form asks for length at most $\gamma \lambda_1(L)$.
- [GapSVP](/gap-svp/)$_\gamma$: decide whether $\lambda_1(L) \le 1$ or $\lambda_1(L) > \gamma$.
- [SIVP](/shortest-independent-vectors-problem/)$_\gamma$: find $n$ linearly independent lattice vectors, each of length at most $\gamma \lambda_n(L)$.
- [BDD](/bounded-distance-decoding/): given a target point within a known small distance of the lattice, find the nearest lattice point.

For the factors $\gamma = \mathrm{poly}(n)$ that cryptography uses, these problems are not known to be NP-hard, but the best known algorithms, classical and quantum, take time $2^{\Theta(n)}$ ([lattice sieving](/lattice-sieving/) and [enumeration](/lattice-enumeration/) inside BKZ).

**Worst case to average case.** A scheme needs random instances that are hard, not only some hard instances. Ajtai (1996) proved that solving a random instance of what is now called SIS gives a solution to approximate SIVP on *every* lattice of a smaller dimension (see [Ajtai's reduction](/ajtai-worst-case-to-average-case-reduction/)). Regev (2005) proved the same kind of result for LWE, with a quantum reduction (see [Regev's reduction](/regev-lwe-hardness/)). So a key generator that picks a random instance is as safe as the hardest lattice of the class. No such result is known for factoring or discrete logarithms.

**SIS and LWE.** The two average-case problems are dual to each other:

- [SIS](/short-integer-solution/): given a random $A \in \mathbb{Z}_q^{n \times m}$, find a short nonzero $z \in \mathbb{Z}^m$ with $A z = 0 \bmod q$. It gives [collision-resistant](/collision-resistance/) hash functions and signatures.
- [LWE](/learning-with-errors/): given $A$ and $b = A s + e \bmod q$ with a small error $e$, find $s$, or tell $b$ from uniform. It gives public-key encryption, key exchange and [fully homomorphic encryption](/homomorphic-encryption/).

**Ring and module forms.** A random $n \times n$ matrix costs $n^2$ numbers. The ring forms ([Ring-SIS](/ring-short-integer-solution/), [Ring-LWE](/ring-learning-with-errors/)) replace it by one element of $R_q = \mathbb{Z}_q[x]/(x^n + 1)$, which costs $n$ numbers and multiplies in $O(n \log n)$ time with the [number theoretic transform](/number-theoretic-transform/). The module forms ([Module-SIS](/module-short-integer-solution/), [Module-LWE](/module-learning-with-errors/)) use a small $k \times \ell$ matrix of ring elements, which lets one ring serve several security levels. Their hardness proofs go to problems on special lattices (ideal and module lattices), which are less studied than general lattices (see [Ring-LWE hardness](/ring-lwe-hardness/)). [Learning with rounding](/learning-with-rounding/) replaces the random error by rounding.

**Why lattices resist Shor.** [Shor's algorithm](/shor-algorithm/) finds the period of a function on a finite abelian group with the [quantum Fourier transform](/quantum-fourier-transform/), and this breaks factoring and discrete logarithms. No reduction is known from lattice problems with polynomial factors to such a period-finding problem. The best known quantum algorithms for SVP are sieves that use [Grover search](/grover-search/) as a subroutine, and they lower the exponent only by a constant factor: $2^{0.265 n}$ heuristic time against $2^{0.292 n}$ classically. This is a statement about the known algorithms, not a proof. For some approximation factors on ideal lattices there are quantum algorithms that do better (see [Ring-LWE hardness](/ring-lwe-hardness/)); they do not break the schemes in use.

**From proofs to parameters.** The reductions show that the problems are sound to build on, but their losses are too large to fix key sizes. Designers choose parameters from the cost of the best known attacks, in the [core-SVP](/core-svp-hardness/) model or with a lattice estimator.

## Examples

**A good and a bad basis.** The rows $(5, 1)$ and $(-1, 4)$ form a good basis of a lattice of volume $21$. With $U = \begin{pmatrix} 7 & 2 \\ 3 & 1 \end{pmatrix}$, $\det U = 1$, the rows $(33, 15)$ and $(14, 7)$ form a bad basis of the same lattice ($33 \cdot 7 - 15 \cdot 14 = 21$). The shortest nonzero vectors are $\pm(-1, 4)$, of length $\sqrt{17}$. For the target $t = (10.3, 13.9)$, write $t$ in each basis and round the coefficients (Babai's rounding method). The good basis gives the point $(12, 15)$ at distance about $2.02$, which is the closest lattice point. The bad basis gives $(-2, 8)$ at distance about $13.64$. In dimension 2 a bad basis is easy to repair; in dimension 500 it is not, and this gap is what the schemes use.

**A toy LWE instance.** The page [learning with errors](/learning-with-errors/) solves an LWE instance of dimension 3 by counting candidates and a dimension 16 instance with LLL. Real schemes use dimension 512 or more, where these methods fail.

**Non-example.** The knapsack scheme of [Merkle and Hellman](/merkle-hellman-knapsack/) also rests on a problem about short vectors ([subset sum](/subset-sum-problem/)), but its instances have a hidden structure and lattice reduction breaks them. It has no worst-case hardness proof, so it does not count as lattice-based cryptography in the modern sense.

## Where it is used

**The standards and the problems under them.**

| Standard | Scheme | Type | Security rests on |
|---|---|---|---|
| FIPS 203, ML-KEM (2024) | [CRYSTALS-Kyber](/crystals-kyber/) | key encapsulation | Module-LWE |
| FIPS 204, ML-DSA (2024) | [CRYSTALS-Dilithium](/crystals-dilithium/) | signature | Module-LWE (key recovery), Module-SIS (forgery), and SelfTargetMSIS in the [QROM](/quantum-random-oracle-model/) proof |
| FIPS 206, FN-DSA (planned) | [Falcon](/falcon/) | signature | the NTRU problem (key recovery) and SIS over NTRU lattices (forgery), in the GPV hash-and-sign framework |

FN-DSA has no public draft standard as of November 2026. NIST submitted the draft for internal approval in August 2025, and the date of the final standard is not known.

**Other schemes.** [Regev encryption](/regev-encryption/) (LWE) is the template for most encryption schemes. [FrodoKEM](/frodokem/) uses plain LWE without ring structure. [Saber](/saber/) uses Module-LWR. [NewHope](/newhope/) used Ring-LWE. [NTRU encryption](/ntru-encrypt/) and [NTRU Prime](/ntru-prime/) use NTRU-type rings. [GPV signatures](/gpv-signature/) use [lattice trapdoors](/trapdoor-sampling-lattices/), and Dilithium uses [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/).

**Beyond encryption and signatures.** The practical [fully homomorphic encryption](/gentry-fully-homomorphic-encryption/) schemes rest on LWE and Ring-LWE. Lattices also give identity-based and attribute-based encryption and [pseudorandom functions](/pseudorandom-function/).

**Attacks and parameters.** The concrete security of all these schemes comes from the cost of lattice reduction on the primal and dual lattices of the instance, estimated in the [core-SVP](/core-svp-hardness/) model. With many samples, the [Arora-Ge](/arora-ge-algorithm/) and [BKW](/bkw-algorithm/) algorithms also apply; the schemes give out too few samples for them.

## References
