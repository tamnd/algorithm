---
tag: 2Y9DFJ
kind: problem
slug: module-short-integer-solution
name: Module short integer solution problem
aliases:
- Module-SIS
area: cryptography/post-quantum
level: advanced
summary: SIS over a module. Given a k x l matrix A over Z_q[x]/(x^n + 1), find a short nonzero z with A z = 0. With SelfTargetMSIS, it underlies the unforgeability of ML-DSA.
prereqs: [ring-short-integer-solution]
see_also: [short-integer-solution, module-learning-with-errors, crystals-dilithium, quantum-random-oracle-model, fiat-shamir-with-aborts, core-svp-hardness, bkz-algorithm, lattice-based-cryptography]
sources:
  - paper: "Adeline Langlois and Damien Stehle, Worst-case to average-case reductions for module lattices, Designs, Codes and Cryptography 75(3), 2015"
    locator: the definitions of Module-SIS and Module-LWE and the reduction from worst-case problems on module lattices to Module-SIS
  - paper: "Eike Kiltz, Vadim Lyubashevsky and Christian Schaffner, A concrete treatment of Fiat-Shamir signatures in the quantum random-oracle model, EUROCRYPT 2018, LNCS 10822"
    locator: the SelfTargetMSIS problem and the security proof of Dilithium in the quantum random oracle model
  - url: "https://pq-crystals.org/dilithium/data/dilithium-specification-round3-20210208.pdf"
    title: Shi Bai, Leo Ducas, Eike Kiltz, Tancrede Lepoint, Vadim Lyubashevsky, Peter Schwabe, Gregor Seiler and Damien Stehle, CRYSTALS-Dilithium algorithm specifications and supporting documentation, version 3.1, 2021
    locator: the security section, with the MLWE, MSIS and SelfTargetMSIS assumptions and the concrete attack estimates
  - url: "https://doi.org/10.6028/NIST.FIPS.204"
    title: NIST, FIPS 204, Module-Lattice-Based Digital Signature Standard, 2024
    locator: Table 1, the ML-DSA parameter sets (q, k, l)
---

The module short integer solution problem (Module-SIS, MSIS) asks for a short nonzero vector $z$ of polynomials with $Az = 0$, where $A$ is a random $k \times \ell$ matrix over $R_q = \mathbb{Z}_q[x]/(x^n + 1)$. It sits between [SIS](/short-integer-solution/), the case $n = 1$, and [Ring-SIS](/ring-short-integer-solution/), the case $k = 1$. Langlois and Stehlé (2015) proved it as hard as worst-case problems on module lattices. Together with a hashed variant, SelfTargetMSIS, it is the assumption behind the unforgeability of ML-DSA ([CRYSTALS-Dilithium](/crystals-dilithium/)).

**Notation.** $n$ is the ring degree, $q$ the modulus (not a number of queries), $k$ and $\ell$ the numbers of rows and columns of $A$, and $\beta$ the bound on the solution. $R = \mathbb{Z}[x]/(x^n + 1)$ and $R_q = R/qR$. For $z \in R^\ell$, $\|z\|_\infty$ is the largest absolute value of a coefficient and $\|z\|$ the Euclidean norm of all $\ell n$ coefficients. $H$ is a hash function, modeled as a random oracle, and $\mu$ is a message. $\lambda$ is the security parameter.

## In plain words

Take a small table whose entries are not numbers but short lists of numbers that are multiplied in a special wrapped way. The task is to find a small combination of the columns, with only tiny multipliers, that adds up to zero.

With one row, this is the ring version of the problem. With lists of length one, it is the plain version. Using a few rows of medium-length lists lets designers change the security level by adding rows and columns, while the fast multiplication code stays the same.

## Definition

Fix $n$ (a power of 2), $q$, $k$, $\ell$ and $\beta$.

**Module-SIS$_{n,q,k,\ell,\beta}$.** Given $A$ drawn uniformly from $R_q^{k \times \ell}$, find $z \in R^\ell$ with

$$Az \equiv 0 \pmod{q}, \qquad z \ne 0, \qquad \|z\| \le \beta.$$

ML-DSA uses the infinity norm, $\|z\|_\infty \le \beta$. Often $A$ is given in the form $[A' \mid I_k]$; this is the same problem up to a change of the basis of $R_q^k$ when the right $k \times k$ block of $A$ is invertible.

**As SIS.** Replace each entry $a_{ij}$ by its $n \times n$ negacyclic matrix $\mathrm{Rot}(a_{ij})$, whose column $t$ holds the coefficients of $x^t a_{ij}$. The result is an ordinary SIS matrix of size $kn \times \ell n$, and $z$ becomes a vector of $\ell n$ integers.

**SelfTargetMSIS.** Kiltz, Lyubashevsky and Schaffner (2018) define a variant with a hash function $H$ into the set of challenge polynomials: given a uniform matrix $A$, find a message $\mu$ and a short vector $y$ whose last entry is a challenge $c$, such that $H(\mu, A y) = c$. The target of the hash is part of the solution itself, which gives the name.

## Variants

- **Inhomogeneous Module-SIS.** Find short $z$ with $Az = t$ for a given $t$.
- **Norms.** The Euclidean norm matches the reductions; the infinity norm matches the rejection step of ML-DSA, which bounds each coefficient of a signature.
- **Rank and degree.** For a fixed lattice dimension $\ell n$, a smaller $n$ and larger $k, \ell$ give less algebraic structure and larger keys. ML-DSA fixes $n = 256$ and changes $(k, \ell)$ between security levels.

## Examples

**A toy instance.** Take $n = 2$, so $R_5 = \mathbb{Z}_5[x]/(x^2 + 1)$ and $x^2 = -1$, with $k = 2$, $\ell = 3$ and

$$A = \begin{pmatrix} 2 + 2x & 1 + x & 1 + x \\ 1 + x & 4x & 1 + 2x \end{pmatrix}.$$

The vector $z = (x, -x, -x)$ is a solution with $\|z\|_\infty = 1$ and $\|z\| = \sqrt{3}$. Row 1 gives $(2x - 2) + (1 - x) + (1 - x) = 0$. Row 2 gives $(x - 1) + 4 + (2 - x) = 5 \equiv 0$. As an SIS matrix over $\mathbb{Z}_5$, $A$ is the $4 \times 6$ matrix with rows $(2,3,1,4,1,4)$, $(2,2,1,1,1,1)$, $(1,4,0,1,1,3)$ and $(1,1,4,0,2,1)$, and $z$ is $(0,1,0,-1,0,-1)$.

**A long solution is easy.** For $A = [A' \mid I_k]$ and any $w \in R^\ell$, $z = (w, -A'w \bmod q)$ solves $Az = 0$. Its second part is close to uniform in $R_q^k$, so it is long. Short solutions are the hard part.

**ML-DSA shapes.** FIPS 204 uses $n = 256$, $q = 8380417 = 2^{23} - 2^{13} + 1$, and $(k, \ell) = (4, 4)$, $(6, 5)$ and $(8, 7)$ for ML-DSA-44, ML-DSA-65 and ML-DSA-87.

## Known algorithms

- **Lattice reduction.** As for SIS, an attacker picks a subset of the $\ell n$ columns and runs [BKZ](/bkz-algorithm/) on the $q$-ary lattice $\{z : Az \equiv 0\}$ to find a short vector. The Dilithium specification estimates the block size this needs for its infinity-norm bound and converts it to a cost with the [core-SVP](/core-svp-hardness/) model. No known attack gains more than small factors from the module structure for the ML-DSA parameters.
- **Birthday search.** Hash random binary $z$ until two collide. The output space has $q^{kn}$ elements, so this takes about $q^{kn/2}$ tries.

The Python code with this page generates instances, checks candidate solutions, writes $A$ as a SIS matrix, and finds solutions on toy sizes by a birthday search. It is for study only and not constant time, and the solver runs only on toy parameters. For ML-DSA use a FIPS 140 validated module or a maintained library such as liboqs.

## Bounds

- **Worst-case hardness.** Langlois and Stehlé (2015) prove that for $q$ a large enough polynomial in $n$ and a large enough $\ell$, solving Module-SIS on average is at least as hard as approximating SIVP to within a polynomial factor in the worst case on module lattices of rank $k$ over $R$.
- **Existence.** If $2^\ell > q^k$, two binary inputs collide, so a solution with $\|z\|_\infty \le 1$ exists.
- **No concrete bound.** As for SIS, the reduction does not set parameters. ML-DSA's parameters come from attack estimates.

## Reductions

- **Special cases.** $n = 1$ gives SIS and $k = 1$ gives Ring-SIS.
- **To SIS.** By the rotation matrices above, any SIS algorithm solves Module-SIS in dimension $\ell n$.
- **To SelfTargetMSIS.** In the classical random oracle model a forking-lemma argument turns a SelfTargetMSIS solver into a Module-SIS solver, with a loss. In the quantum random oracle model no such argument is known, so the proof of Kiltz, Lyubashevsky and Schaffner uses SelfTargetMSIS as an assumption of its own.

## Applications

- **ML-DSA.** The security proof of Kiltz, Lyubashevsky and Schaffner, in the [quantum random oracle model](/quantum-random-oracle-model/), shows that ML-DSA is unforgeable if Module-LWE and SelfTargetMSIS are hard; strong unforgeability also uses Module-SIS. The Module-LWE part hides the secret key; the SIS parts say that a forger must find a short vector of the form above. See [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/) for the signing method.
- **Hash functions and commitments.** $z \mapsto Az$ on short inputs is a collision-resistant compression function and a binding commitment under Module-SIS.

## References
