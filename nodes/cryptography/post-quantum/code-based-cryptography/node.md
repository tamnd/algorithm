---
tag: G31QDK
kind: concept
slug: code-based-cryptography
name: Code-based cryptography
aliases:
- coding-theoretic cryptography
area: cryptography/post-quantum
level: intro
summary: Public-key cryptography whose security rests on the hardness of decoding random linear codes. It includes McEliece (1978), BIKE and HQC, which NIST selected in March 2025.
prereqs: [linear-code, parity-check-matrix, public-key-encryption]
see_also: [syndrome-decoding-problem, information-set-decoding, mceliece-cryptosystem, niederreiter-cryptosystem, bike, hqc, post-quantum-cryptography, learning-parity-with-noise]
sources:
  - paper: "Robert J. McEliece, A public-key cryptosystem based on algebraic coding theory, DSN Progress Report 42-44, Jet Propulsion Laboratory, pages 114 to 116, 1978"
    locator: the whole report (the first code-based public-key scheme, with binary Goppa codes)
  - paper: "Elwyn R. Berlekamp, Robert J. McEliece and Henk C. A. van Tilborg, On the inherent intractability of certain coding problems, IEEE Transactions on Information Theory 24(3), pages 384 to 386, 1978"
    locator: the whole paper (decoding a general linear code is NP-complete)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Code-based cryptography by Raphael Overbeck and Nicolas Sendrier (McEliece, Niederreiter, the attacks, and the choice of codes)
  - url: "https://doi.org/10.6028/NIST.IR.8545"
    title: NIST IR 8545, Status Report on the Fourth Round of the NIST Post-Quantum Cryptography Standardization Process, March 2025
    locator: Section 2.3 (HQC selected, BIKE and Classic McEliece not selected, the ISO process for Classic McEliece), Section 3 (the three schemes), Tables 6 to 8 (key and ciphertext sizes)
  - paper: "Rafael Misoczki, Jean-Pierre Tillich, Nicolas Sendrier and Paulo S. L. M. Barreto, MDPC-McEliece: new McEliece variants from moderate density parity-check codes, ISIT 2013, pages 2069 to 2073"
    locator: the whole paper (quasi-cyclic MDPC codes, the base of BIKE)
  - paper: "Carlos Aguilar Melchor, Olivier Blazy, Jean-Christophe Deneuville, Philippe Gaborit and Gilles Zemor, Efficient encryption from random quasi-cyclic codes, IEEE Transactions on Information Theory 64(5), pages 3927 to 3943, 2018"
    locator: the whole paper (the HQC construction with a public decodable code and a random quasi-cyclic code)
  - paper: "Vladimir M. Sidelnikov and Sergey O. Shestakov, On insecurity of cryptosystems based on generalized Reed-Solomon codes, Discrete Mathematics and Applications 2(4), pages 439 to 444, 1992"
    locator: the whole paper (a key recovery attack on Niederreiter with generalized Reed-Solomon codes)
  - url: "https://doi.org/10.6028/NIST.IR.8610"
    title: NIST IR 8610, Status Report on the Second Round of the Additional Digital Signature Schemes for the NIST Post-Quantum Cryptography Standardization Process, May 2026
    locator: the introduction (the 14 round 2 candidates and the 9 candidates of the third round)
---

Code-based cryptography is public-key cryptography whose security rests on the hardness of decoding a [linear code](/linear-code/) that looks random. The core hard problem is the [syndrome decoding problem](/syndrome-decoding-problem/): given a [parity check matrix](/parity-check-matrix/) $H$, a syndrome $s$ and a weight $w$, find $e$ with $He = s$ and weight $w$. The secret key is a code with a fast decoder, and the public key is a disguised form of it that looks like a random code. Robert McEliece proposed the first scheme in 1978, and it is still unbroken with its original choice of codes. No quantum algorithm is known that decodes random codes much faster than a square root of the classical cost, so code-based schemes are a main branch of [post-quantum cryptography](/post-quantum-cryptography/). In March 2025 NIST selected the code-based KEM [HQC](/hqc/) for standardization.

**Notation.** All codes are binary unless stated. A code has length $n$, dimension $k$ and $r = n - k$, $G \in \mathbb{F}_2^{k \times n}$ is a [generator matrix](/generator-matrix/), $H \in \mathbb{F}_2^{r \times n}$ is a parity check matrix, and $t$ or $w$ is the number of errors. $\lambda$ is the security parameter, $\mathcal{A}$ an adversary and $\mathrm{Adv}$ its advantage. The schemes on this page aim at IND-CCA2 security as KEMs, in the random oracle model or its quantum version; their one-way security rests on syndrome decoding and on the indistinguishability of the public code from a random code.

## In plain words

Error-correcting codes add redundancy to a message so that the receiver can fix a few flipped bits. For some codes, fixing the bits is fast. For a code chosen at random, nobody knows a fast way, and the work grows exponentially.

Code-based cryptography uses this gap. The owner picks a code with a fast decoder, then scrambles its description so that it looks random, and publishes the scrambled form. To send a secret, anyone encodes it and adds a few random errors on purpose. Only the owner, who knows the hidden structure, can remove the errors.

The price is size. The public keys of the classic schemes are large, about a quarter of a megabyte for the smallest Classic McEliece set. Newer schemes use codes with cyclic structure to shrink the keys to a few kilobytes.

## The idea

**Codes and syndromes.** A binary linear code $C$ of length $n$ and dimension $k$ is the row space of a generator matrix $G$, or the kernel of a parity check matrix $H$. A received word $y = c + e$ with $c \in C$ has [syndrome](/syndrome/) $Hy = He$, which depends only on the error. A code with minimum distance $d$ can correct up to $\lfloor (d-1)/2 \rfloor$ errors, but finding them is a hard problem in general: the decision version of syndrome decoding is [NP-complete](/np-complete/) (Berlekamp, McEliece and van Tilborg 1978).

**The two hard problems.** A code-based scheme is secure if both of these hold.

- *Decoding is hard.* Syndrome decoding of a random code with the scheme's $n$, $k$ and $w$ costs about $2^\lambda$ operations for the best attacks, which are [information set decoding](/information-set-decoding/) algorithms.
- *The public code looks random.* No efficient algorithm tells the public code apart from a random code, and no algorithm recovers the hidden decoder. This is a separate assumption, and the attacks on many proposed codes broke it rather than the decoding problem.

**The McEliece family.** In [McEliece](/mceliece-cryptosystem/) the private key is a binary [Goppa code](/goppa-code/) with an efficient decoder for $t$ errors, and the public key is a generator matrix of the same code in a scrambled basis and order. A ciphertext is $c = mG' + e$ with a random error $e$ of weight $t$. The [Niederreiter](/niederreiter-cryptosystem/) form publishes a parity check matrix instead, and the ciphertext is the syndrome $He$; it has the same security and shorter ciphertexts. Classic McEliece is a KEM in the Niederreiter form.

**The quasi-cyclic schemes.** A quasi-cyclic matrix is made of circulant blocks, so one row of each block describes it. This shrinks the keys from hundreds of kilobytes to a few kilobytes. [BIKE](/bike/) uses quasi-cyclic moderate density parity check (MDPC) codes with a bit flipping decoder, and its secret is the sparse parity check matrix. [HQC](/hqc/) is built differently: the decodable code is public (a concatenation of Reed-Muller and Reed-Solomon codes), and the secret is a pair of sparse vectors in a quasi-cyclic structure, much like a Diffie-Hellman exchange with noise. Both decoders fail with a small probability, which must be very small for IND-CCA2 security.

**Structure that broke.** Many codes with more structure have been proposed to shrink the keys, and several were broken by algebraic attacks on the second assumption. Sidelnikov and Shestakov (1992) broke Niederreiter with generalized Reed-Solomon codes. Faugère, Otmani, Perret and Tillich (2010) broke several quasi-cyclic and quasi-dyadic variants of McEliece. Binary Goppa codes with the parameters of Classic McEliece, the MDPC codes of BIKE and the random quasi-cyclic codes of HQC have no known structural attack.

## Examples

Sizes in bytes from NIST IR 8545 (Tables 6 to 8), for the round 4 versions at NIST security category 1:

| scheme | parameter set | public key | secret key | ciphertext |
|---|---|---|---|---|
| Classic McEliece | mceliece348864 ($n = 3488$, $t = 64$, $m = 12$) | 261120 | 6492 | 96 |
| BIKE | Level 1 ($r = 12323$, $w = 142$, $t = 134$) | 1541 | 281 | 1573 |
| HQC | hqc-128 ($n = 17669$) | 2249 | 40 | 4497 |

Classic McEliece has the largest public keys and the smallest ciphertexts of all the NIST candidates. BIKE and HQC have keys of a few kilobytes, much smaller than McEliece but larger than the lattice scheme ML-KEM. The HQC secret key is small because it is stored as a seed.

## Where it is used

- **NIST standardization.** NIST selected HQC in March 2025 as a second KEM next to ML-KEM, based on a different hard problem (NIST IR 8545). BIKE and Classic McEliece were in round 4 and were not selected. NIST chose HQC over BIKE because the analysis of the decoding failure rate of HQC is more mature. Classic McEliece is under consideration for standardization by ISO (it was proposed for ISO/IEC 18033-2), and NIST says it may consider a standard based on the ISO standard after that work ends.
- **Signatures.** Code-based identification schemes start with Stern (1993). In the NIST process for additional signatures, CROSS, LESS and SDitH were among the 14 round 2 candidates (October 2024), and SDitH is in the third round that NIST announced in May 2026 (NIST IR 8610).
- **Other uses.** Pseudorandom generators, and the [LPN](/learning-parity-with-noise/) based protocols for light devices.
- **Use a vetted library.** For real systems, use a vetted implementation, for example a FIPS 140 validated module once a standard exists, not a study implementation.

## References
