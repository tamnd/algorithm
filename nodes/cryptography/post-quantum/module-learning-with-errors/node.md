---
tag: 4H2DFX
kind: problem
slug: module-learning-with-errors
name: Module learning with errors
aliases:
- Module-LWE
- MLWE
area: cryptography/post-quantum
level: advanced
summary: LWE with a k x k matrix of ring elements, between LWE (n = 1) and Ring-LWE (k = 1). Given A and t = A s + e over Z_q[x]/(x^n + 1), find s. The base of ML-KEM and ML-DSA.
prereqs: [ring-learning-with-errors]
see_also: [learning-with-errors, module-short-integer-solution, crystals-kyber, crystals-dilithium, saber, number-theoretic-transform, ring-lwe-hardness, core-svp-hardness]
sources:
  - paper: "Zvika Brakerski, Craig Gentry and Vinod Vaikuntanathan, (Leveled) fully homomorphic encryption without bootstrapping, ITCS 2012"
    locator: the General LWE (GLWE) problem, which contains LWE and Ring-LWE as special cases
  - paper: "Adeline Langlois and Damien Stehle, Worst-case to average-case reductions for module lattices, Designs, Codes and Cryptography 75(3), pages 565 to 599, 2015"
    locator: the definitions of Module-LWE and Module-SIS and their reductions from worst-case problems on module lattices
  - url: "https://doi.org/10.6028/NIST.FIPS.203"
    title: NIST, FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, August 2024
    locator: Section 4.3 and Algorithms 9 to 12 (NTT, inverse NTT, MultiplyNTTs, BaseCaseMultiply), Algorithm 8 (SamplePolyCBD), Section 8 (parameter sets), Appendix A (the zeta tables)
  - url: "https://doi.org/10.6028/NIST.FIPS.204"
    title: NIST, FIPS 204, Module-Lattice-Based Digital Signature Standard, August 2024
    locator: the parameter sets of ML-DSA (q = 8380417, n = 256, and the matrix sizes k x l)
  - url: "https://pq-crystals.org/kyber/data/kyber-specification-round3-20210131.pdf"
    title: Roberto Avanzi and others, CRYSTALS-Kyber Algorithm Specifications and Supporting Documentation, version 3.01, January 31, 2021
    locator: Section 4 (the Module-LWE assumption behind Kyber) and Section 5 (attacks on Module-LWE)
---

Module learning with errors (Module-LWE) is [learning with errors](/learning-with-errors/) in which the secret is a vector of $k$ elements of a polynomial ring $R_q = \mathbb{Z}_q[x]/(x^n + 1)$ and the public matrix has entries in $R_q$. With $k = 1$ it is [Ring-LWE](/ring-learning-with-errors/), and with $n = 1$ it is plain LWE. Brakerski, Gentry and Vaikuntanathan (2012) and Langlois and Stehlé (2015) introduced it, and it is the problem under the NIST standards ML-KEM ([CRYSTALS-Kyber](/crystals-kyber/)) and ML-DSA ([CRYSTALS-Dilithium](/crystals-dilithium/)).

**Notation.** $n$ is the ring degree, $k$ the module rank, $q$ the modulus (a prime here; not a number of queries), $R_q = \mathbb{Z}_q[x]/(x^n + 1)$, and $\chi$ a distribution on $R$ with small coefficients. Bold letters are not used: $A \in R_q^{m \times k}$ is a matrix and $s \in R_q^k$ a vector. $\circ$ is the coefficient-wise product in the NTT domain. $\lambda$ is the security parameter and $\mathcal{A}$ an adversary. Security statements are in the standard model.

## In plain words

Ring-LWE uses one large shifted table to save space; plain LWE uses one large random table. Module-LWE takes a middle path: a small grid of blocks, for example two by two or three by three, where each block is a shifted table of fixed size.

The block size stays the same, so one fast multiplication routine serves all security levels; a scheme gets more security by using a larger grid of blocks. The structure is weaker than in the ring case, because the blocks are independent, so the problem sits closer to plain LWE. That is why the main standards chose it.

## Definition

**Module-LWE.** Fix $n$, $q$, $k$, a number of samples $m$ (counted in ring elements) and $\chi$. For a secret $s \in R_q^k$, the distribution outputs

$$(A,\; t = A s + e) \in R_q^{m \times k} \times R_q^m, \qquad A \text{ uniform},\; e \leftarrow \chi^m.$$

**Search Module-LWE:** given $(A, t)$, find $s$. **Decision Module-LWE:** tell $(A, t)$ from $(A, u)$ with $u$ uniform in $R_q^m$. The advantage of $\mathcal{A}$ is $|\Pr[\mathcal{A}(A, As + e) = 1] - \Pr[\mathcal{A}(A, u) = 1]|$, and the Module-LWE assumption says it is negligible for every adversary that runs in time polynomial in $\lambda$. In the schemes, $s \leftarrow \chi^k$ (normal form) and $m = k$.

**As plain LWE.** Replace each entry $a_{ij}$ of $A$ by its $n \times n$ negacyclic matrix $\mathrm{Rot}(a_{ij})$. Then $t = As + e$ is LWE in dimension $kn$ with $mn$ samples and a structured matrix made of $m \times k$ blocks.

**Special cases.** $k = 1$ gives Ring-LWE in degree $n$. $n = 1$ (so $R = \mathbb{Z}$) gives LWE in dimension $k$.

**The NTT of ML-KEM.** For $q = 3329$ and $n = 256$, $q - 1 = 2^8 \cdot 13$, so $\mathbb{Z}_q$ has a primitive 256-th root of unity $\zeta = 17$ but no 512-th root. Then $x^{256} + 1$ does not split into linear factors mod $q$; it splits into 128 quadratic factors:

$$x^{256} + 1 = \prod_{i=0}^{127} \bigl(x^2 - \zeta^{2\,\mathrm{BitRev}_7(i) + 1}\bigr) \pmod{3329}.$$

FIPS 203 computes this map with a 7-layer [NTT](/number-theoretic-transform/) (Algorithm 9): in each layer, with a fixed $\zeta^{\mathrm{BitRev}_7(i)}$ per block, the butterfly is $t \leftarrow \zeta f_{j+\ell}$, $f_{j+\ell} \leftarrow f_j - t$, $f_j \leftarrow f_j + t$, for block lengths $\ell = 128, 64, \ldots, 2$. The result is 128 polynomials of degree at most 1. MultiplyNTTs (Algorithm 11) multiplies them pairwise with BaseCaseMultiply (Algorithm 12):

$$(a_0 + a_1 X)(b_0 + b_1 X) \bmod (X^2 - \gamma) = (a_0 b_0 + a_1 b_1 \gamma) + (a_0 b_1 + a_1 b_0) X,$$

with $\gamma = \zeta^{2\,\mathrm{BitRev}_7(i) + 1}$. The inverse (Algorithm 10) runs the layers in reverse with Gentleman-Sande butterflies and multiplies by $3303 = 128^{-1} \bmod 3329$. A product in $R_q$ costs $3 \cdot 7 \cdot 128$ butterflies and 128 base multiplications.

## Variants

- **Module-LWR.** Rounding instead of random errors; [Saber](/saber/) uses it with $q = 2^{13}$ and $p = 2^{10}$ (see [learning with rounding](/learning-with-rounding/)).
- **Rectangular matrices.** ML-DSA uses $A \in R_q^{k \times \ell}$ with $k \ne \ell$; the public key is $t = A s_1 + s_2$ with $s_1 \in R_q^\ell$ and $s_2 \in R_q^k$, both with coefficients uniform in $[-\eta, \eta]$.
- **Other rings.** The definition works over any ring of integers of a number field; Langlois and Stehlé state it in that generality.
- **Module-SIS.** The SIS analog, used for ML-DSA's unforgeability; see [Module-SIS](/module-short-integer-solution/).

## Examples

**A toy instance.** Take $n = 4$, $q = 17$ and $k = 2$, so $R_q = \mathbb{Z}_{17}[x]/(x^4 + 1)$. Let

$$A = \begin{pmatrix} 3 + 5x^2 + x^3 & -1 + 2x + 7x^3 \\ 4 + 9x + x^2 & 11x^2 + 6x^3 \end{pmatrix}, \quad s = \begin{pmatrix} 1 - x^2 \\ x + x^2 - x^3 \end{pmatrix}, \quad e = \begin{pmatrix} x - x^3 \\ 1 \end{pmatrix}.$$

For instance $(3 + 5x^2 + x^3)(1 - x^2) = 3 + 2x^2 + x^3 - 5x^4 - x^5$, and $x^4 = -1$ turns it into $8 + x + 2x^2 + x^3$. Summing the products in each row and adding $e$ gives

$$t = A s + e = \begin{pmatrix} 3 + 11x + 10x^2 + 3x^3 \\ 6 + 14x + 3x^2 + 2x^3 \end{pmatrix} \pmod{17}.$$

As plain LWE this is an $8 \times 8$ system made of four $4 \times 4$ negacyclic blocks.

**ML-KEM parameters (FIPS 203, Section 8).** All three sets use $n = 256$ and $q = 3329$; the Module-LWE instance of the key has rank $k$ and errors from the centered binomial distribution $\mathrm{CBD}_\eta$, whose coefficients lie in $[-\eta, \eta]$ with variance $\eta/2$.

| Set | $k$ | $\eta_1$ | $\eta_2$ | LWE dimension $kn$ |
|---|---|---|---|---|
| ML-KEM-512 | 2 | 3 | 2 | 512 |
| ML-KEM-768 | 3 | 2 | 2 | 768 |
| ML-KEM-1024 | 4 | 2 | 2 | 1024 |

The public key holds $t$, that is $kn$ coefficients of 12 bits, plus a 32-byte seed from which $A$ is expanded; for ML-KEM-768 that is $768 \cdot 12 / 8 + 32 = 1184$ bytes.

**ML-DSA parameters.** ML-DSA uses $n = 256$, $q = 8380417 = 2^{23} - 2^{13} + 1$ and $(k, \ell) = (4, 4), (6, 5), (8, 7)$. Since $q \equiv 1 \pmod{512}$, its ring splits completely and it uses a full 8-layer NTT with $\zeta = 1753$.

**A check of the NTT.** In $R_q$, $x^{128} \cdot x^{128} = x^{256} = -1$. The FIPS 203 NTT gives the same: the inverse NTT of MultiplyNTTs applied to the NTT of $x^{128}$ twice is the constant polynomial $3328$.

## Known algorithms

- **Lattice attacks on the LWE form.** The primal and dual attacks treat the instance as LWE in dimension $kn$ with $mn$ samples. Their cost, estimated in the [core-SVP](/core-svp-hardness/) model, sets the parameters of ML-KEM and ML-DSA. The Kyber round 3 specification (Section 5) bases its estimates on these attacks, which do not use the module structure.
- **Few samples rule out other attacks.** A key gives only $kn$ LWE samples, plus $n$ more if the ciphertext is counted, so [BKW](/bkw-algorithm/) and the linearization of [Arora-Ge](/arora-ge-algorithm/), which need far more samples, do not apply.
- **Structure.** No analog for module lattices of rank $k \ge 2$ is known of the quantum attacks on ideal lattices described under [Ring-LWE hardness](/ring-lwe-hardness/).

The Python code with this page implements Algorithms 8 to 12 of FIPS 203 and samples Module-LWE instances in the style of ML-KEM key generation, but draws $A$ and the noise from Python's random module instead of SHAKE. It checks every NTT product against the schoolbook product. It is not ML-KEM, is for study only, and is not constant time; real systems must use a FIPS 140 validated ML-KEM module. Scheme details belong to [CRYSTALS-Kyber](/crystals-kyber/).

## Bounds

- **Worst-case hardness (Langlois and Stehlé 2015).** Module-LWE of rank $k$ over a ring of degree $n$, with a polynomial modulus and a Gaussian error of suitable width, is at least as hard as quantum approximation of SIVP on module lattices of rank $k$ over that ring, with a polynomial factor, in the worst case. For $k = 1$ these are ideal lattices (the LPR theorem); for growing $k$ the class grows toward general lattices.
- **Concrete hardness.** As for LWE and Ring-LWE, the reduction does not fix parameters. The best known attacks on the parameter sets in use take time exponential in $kn$, and the cost estimates use $kn$ as the LWE dimension.

## Reductions

- **To LWE.** Module-LWE is LWE with a block-structured matrix, so an LWE solver for arbitrary matrices solves it.
- **To Ring-LWE.** Rank 1 Module-LWE is Ring-LWE. Conversely, no general reduction is known that makes rank $k$ Module-LWE as easy as Ring-LWE.
- **Duality with Module-SIS.** A short vector $v \in R^m$ with $v^{\mathsf T} A = 0$, a Module-SIS solution for $A^{\mathsf T}$, gives the dual attack, as for plain LWE.

## Applications

- **ML-KEM (FIPS 203).** Key encapsulation from Module-LWE, with the [Fujisaki-Okamoto transform](/fujisaki-okamoto-transform/) for IND-CCA2 security; see [CRYSTALS-Kyber](/crystals-kyber/).
- **ML-DSA (FIPS 204).** Signatures; key recovery is Module-LWE, forgery is Module-SIS and SelfTargetMSIS; see [CRYSTALS-Dilithium](/crystals-dilithium/).
- **Saber.** A NIST round 3 finalist on Module-LWR; see [Saber](/saber/).
- **Homomorphic encryption.** The GLWE problem of BGV covers both the LWE and the Ring-LWE forms of [homomorphic encryption](/homomorphic-encryption/).

## References
