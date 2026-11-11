---
tag: 4YZXDV
kind: problem
slug: ring-learning-with-errors
name: Ring learning with errors
aliases:
- Ring-LWE
- RLWE
area: cryptography/post-quantum
level: advanced
summary: LWE over a polynomial ring such as Z_q[x]/(x^n + 1). Given a and b = a s + e with small s and e, find s or tell b from uniform. Keys of size n, products in O(n log n) by NTT.
prereqs: [learning-with-errors, number-theoretic-transform, polynomial-ring]
see_also: [ring-lwe-hardness, module-learning-with-errors, ring-short-integer-solution, ntru-problem, newhope, homomorphic-encryption, polynomial-multiplication, learning-with-rounding]
sources:
  - paper: "Vadim Lyubashevsky, Chris Peikert and Oded Regev, On ideal lattices and learning with errors over rings, Journal of the ACM 60(6), Article 43, 2013"
    locator: Section 3 (the ring R = O_K, its dual, and the definition of the Ring-LWE distribution and problems), Theorem 3.6 (main theorem), Section 5 (search to decision for cyclotomic rings), Section 8 (the cryptosystem)
  - paper: "Vadim Lyubashevsky, Chris Peikert and Oded Regev, On ideal lattices and learning with errors over rings, EUROCRYPT 2010, LNCS 6110, pages 1 to 23"
    locator: the conference version that introduced Ring-LWE
  - paper: "Chris Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4), pages 283 to 424, 2016"
    locator: Section 4.4 (Ring-LWE, its definitions, hardness and relation to NTRU)
  - url: "https://doi.org/10.6028/NIST.FIPS.203"
    title: NIST, FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard, August 2024
    locator: Section 4.3 (the number theoretic transform over Z_3329[x]/(x^256 + 1))
---

Ring learning with errors (Ring-LWE) is [learning with errors](/learning-with-errors/) in which the secret, the random values and the errors are elements of a [polynomial ring](/polynomial-ring/) such as $R_q = \mathbb{Z}_q[x]/(x^n + 1)$. Lyubashevsky, Peikert and Regev defined it in 2010 and proved it as hard as worst-case problems on ideal lattices for quantum algorithms (see [Ring-LWE hardness](/ring-lwe-hardness/)). One ring sample replaces $n$ plain LWE samples, so keys shrink from about $n^2$ to $n$ numbers, and the [number theoretic transform](/number-theoretic-transform/) multiplies two ring elements in $O(n \log n)$ operations.

**Notation.** $n$ is the ring degree, a power of 2 unless the text says otherwise, and $q$ the modulus, a prime (not a number of queries). $R = \mathbb{Z}[x]/(x^n + 1)$ and $R_q = R / qR$. Elements are polynomials of degree below $n$, written as coefficient vectors. $\chi$ is an error distribution on $R$ with small coefficients. $\lambda$ is the security parameter and $\mathcal{A}$ an adversary. Security statements are in the standard model.

## In plain words

Plain LWE hides a secret behind many random equations, and each equation needs its own long row of random numbers. Ring-LWE builds all those rows from a single row: each new row is the previous one shifted by one place, with the number that falls off the end coming back in front with its sign flipped. One short list of random numbers then stands for a whole square table.

This saves space, and a fast transform, related to the one used for fast multiplication of big numbers, does the arithmetic quickly. The cost is extra structure. The hardness proof now rests on lattices with the same kind of symmetry, which are less studied than general lattices. So far no attack uses this structure to break the schemes.

## Definition

**The ring.** For $n$ a power of 2, the polynomial $x^n + 1$ is the $2n$-th cyclotomic polynomial, so it is irreducible over $\mathbb{Q}$ and $R = \mathbb{Z}[x]/(x^n+1)$ is the ring of integers of the cyclotomic field $\mathbb{Q}(\zeta_{2n})$. Multiplication by $x$ shifts the coefficients up by one place and maps the top coefficient $c$ to $-c$ at the bottom (since $x^n = -1$). The product $a \cdot s$ is therefore $\mathrm{Rot}(a)\, s$ for the $n \times n$ negacyclic matrix $\mathrm{Rot}(a)$ whose column $j$ is $x^j a$.

**The distribution.** For $s \in R_q$, the Ring-LWE distribution $A_{s,\chi}$ draws $a \in R_q$ uniformly and $e \leftarrow \chi$, and outputs $(a, b = a \cdot s + e) \in R_q \times R_q$.

**Search Ring-LWE.** Given $\ell$ independent samples from $A_{s,\chi}$, find $s$.

**Decision Ring-LWE.** Tell $\ell$ samples from $A_{s,\chi}$ for a uniform $s$ from $\ell$ uniform pairs in $R_q \times R_q$. The advantage of $\mathcal{A}$ is $\bigl|\Pr[\mathcal{A}(\{(a_i, a_i s + e_i)\}) = 1] - \Pr[\mathcal{A}(\{(a_i, u_i)\}) = 1]\bigr|$, and the Ring-LWE assumption says it is negligible for every adversary that runs in time polynomial in $\lambda$.

**The general form.** LPR define the problem for any number field $K$ with ring of integers $R$: the secret lies in $R_q^\vee = R^\vee / qR^\vee$ for the dual ideal $R^\vee$, and the error is a Gaussian in the canonical embedding of $K$. For $n$ a power of 2, $R^\vee = n^{-1} R$ and the canonical embedding is $\sqrt n$ times an isometry of the coefficient vector. After scaling by $n$, the problem becomes the form above with a spherical Gaussian on the coefficients. For other cyclotomic rings this simple form is not equivalent, and the dual matters.

**The NTT.** If $q$ is a prime with $q \equiv 1 \pmod{2n}$, then $\mathbb{Z}_q$ has a primitive $2n$-th root of unity $\psi$, and $x^n + 1 = \prod_{i=0}^{n-1} (x - \psi^{2i+1}) \bmod q$. By the [Chinese remainder theorem](/chinese-remainder-theorem/), $R_q \cong \mathbb{Z}_q^n$ through evaluation at the $n$ roots $\psi^{2i+1}$. The negacyclic NTT computes this map with $\tfrac n2 \log_2 n$ butterflies, so a product in $R_q$ costs two forward transforms, $n$ multiplications and one inverse transform, $O(n \log n)$ operations in $\mathbb{Z}_q$ against $n^2$ for the schoolbook method.

## Variants

- **Normal form.** The secret is drawn from $\chi$ instead of uniformly; this is as hard, by the same argument as for LWE, and all schemes use it.
- **Other rings.** Any cyclotomic ring $\mathbb{Z}[x]/(\Phi_m(x))$, with the dual ideal as above, or rings such as $\mathbb{Z}[x]/(x^p - x - 1)$ in [NTRU Prime](/ntru-prime/). Moduli with $q \not\equiv 1 \pmod{2n}$, such as $3329$ for $n = 256$, give a partial NTT (see [Module-LWE](/module-learning-with-errors/)).
- **Module-LWE.** A vector of $k$ ring elements as the secret; rank $k = 1$ is Ring-LWE. See [Module-LWE](/module-learning-with-errors/).
- **Ring-LWR.** Deterministic rounding instead of random errors; see [learning with rounding](/learning-with-rounding/).
- **Number of samples.** Schemes give out one or two samples. The LPR theorem also covers a bounded number $\ell$ of samples with a slightly wider error.

## Examples

**A small ring.** Take $n = 4$ and $q = 17$, so $17 \equiv 1 \pmod 8$. The element $\psi = 9$ has $9^4 \equiv -1 \pmod{17}$, so it is a primitive 8th root of unity, and the roots of $x^4 + 1$ mod 17 are $9, 15, 8, 2$ (the odd powers of 9). Let

$$a = 1 + 2x - x^3, \qquad s = 1 - x^2 + x^3, \qquad e = 1 - x^3.$$

The product in $\mathbb{Z}[x]$ is $1 + 2x - x^2 - 2x^3 + 2x^4 + x^5 - x^6$, and $x^4 = -1$ turns it into $a s = -1 + x - 2x^3$, so

$$b = a s + e = x - 3x^3 \equiv x + 14 x^3 \pmod{17}.$$

The NTT values of $a$ at $(9, 8, 15, 2)$, in the bit-reversed order the code uses, are $(4, 15, 5, 14)$, and those of $s$ are $(3, 7, 6, 5)$. Their pointwise products are $(12, 3, 13, 2)$, which are the values of $a s$ at the same points: for instance $a s$ at $9$ is $-1 + 9 - 2 \cdot 9^3 \equiv 12 \pmod{17}$.

**As plain LWE.** The same sample is four LWE samples $\mathrm{Rot}(a)\, s + e$ with the matrix

$$\mathrm{Rot}(a) = \begin{pmatrix} 1 & 1 & 0 & -2 \\ 2 & 1 & 1 & 0 \\ 0 & 2 & 1 & 1 \\ -1 & 0 & 2 & 1 \end{pmatrix},$$

whose column $j$ is $x^j a \bmod (x^4 + 1)$.

**Real sizes.** NewHope used $n = 1024$ and $q = 12289 \equiv 1 \pmod{2048}$. The code multiplies with $n = 256$ and $q = 7681$ or $12289$ and checks each NTT product against the schoolbook product.

**Non-example: the ring $x^n - 1$.** With $f = x^n - 1$, evaluation at $1$ is a ring map to $\mathbb{Z}_q$. It sends a sample to $b(1) = a(1) s(1) + e(1) \bmod q$, and $e(1)$ is a sum of $n$ small numbers, of size about $\sqrt n$ times the error width. If $q$ is much larger, the pairs $(a(1), b(1))$ are one-dimensional LWE with a small error, which leaks $s(1)$ and distinguishes the samples from uniform. A ring with a small-degree factor of this kind is unsafe; $x^n + 1$ is irreducible over $\mathbb{Q}$ and avoids this problem.

## Known algorithms

- **Generic LWE attacks.** Through $\mathrm{Rot}(a)$, Ring-LWE with $\ell$ samples is LWE in dimension $n$ with $\ell n$ samples, and the primal and dual lattice attacks apply unchanged. Their costs are estimated in the [core-SVP](/core-svp-hardness/) model. For the cyclotomic rings and parameters in use, no attack is known that does much better by using the ring structure.
- **Attacks on ideal lattices.** There are quantum algorithms that find short vectors in ideal lattices for some approximation factors faster than for general lattices. They do not solve Ring-LWE as used in schemes; see [Ring-LWE hardness](/ring-lwe-hardness/).
- **Many samples.** [Arora-Ge](/arora-ge-algorithm/) and [BKW](/bkw-algorithm/) need many samples and do not apply when a scheme gives out one or two.

The Python code with this page samples Ring-LWE, multiplies in $R_q$ by schoolbook and by its own negacyclic NTT, and writes a sample as $n$ LWE samples. It is for study only and is not constant time. Real systems should use a FIPS 140 validated ML-KEM module.

## Bounds

- **Hardness (Lyubashevsky, Peikert and Regev).** For the $m$-th cyclotomic ring of degree $n = \varphi(m)$, a prime $q \equiv 1 \pmod m$ of polynomial size, and error rate $\alpha$ with $\alpha q \ge \omega(\sqrt{\log n})$, decision Ring-LWE is at least as hard as quantum approximation of SVP on ideal lattices of $K$ to within $\tilde O(\sqrt n/\alpha)$ in the worst case. The error in this theorem comes from a family of elliptical Gaussians; for a bounded number of samples a spherical Gaussian of a somewhat larger width also works. The exact statement is on [Ring-LWE hardness](/ring-lwe-hardness/).
- **Upper bounds.** The best known algorithms for the parameters in use are the lattice attacks on the LWE form, of time $2^{\Theta(n)}$.
- **Concrete security** comes from attack estimates, not from the reduction.

## Reductions

- **Ring-LWE to LWE.** Every Ring-LWE instance is an LWE instance with structured $A$, so an LWE solver for arbitrary $A$ solves Ring-LWE. The converse is not known: the hardness of LWE does not imply that of Ring-LWE.
- **Search to decision.** For cyclotomic rings and $q \equiv 1 \pmod m$, search reduces to decision (LPR, Section 5). The proof uses the field automorphisms to move the error between the $n$ factors of $R_q$.
- **To Module-LWE.** Ring-LWE is Module-LWE of rank 1 (see [Module-LWE](/module-learning-with-errors/)).
- **Relation to NTRU.** An NTRU public key $h = g/f$ resembles a Ring-LWE sample with $a = h$ and the secret $f$; see the [NTRU problem](/ntru-problem/).

## Applications

- **Encryption.** In the LPR scheme the public key is $(a, b = a s + e)$. To encrypt a message $\mu \in \{0,1\}^n$, pick small $r, e_1, e_2$ and send $u = a r + e_1$ and $v = b r + e_2 + \lfloor q/2 \rceil \mu$. Decryption computes $v - u s = e r + e_2 - e_1 s + \lfloor q/2 \rceil \mu$ and rounds each coefficient.
- **Key exchange.** [NewHope](/newhope/) used Ring-LWE with $n = 1024$; [ML-KEM](/crystals-kyber/) uses Module-LWE over $n = 256$.
- **Fully homomorphic encryption.** The BGV, BFV and CKKS schemes for [homomorphic encryption](/homomorphic-encryption/) work over cyclotomic rings and rest on Ring-LWE.
- **Signatures** with [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/) use the ring forms of LWE and SIS.

## References
