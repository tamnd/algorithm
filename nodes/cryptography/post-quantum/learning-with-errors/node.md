---
tag: 91A2EW
kind: problem
slug: learning-with-errors
name: Learning with errors
aliases:
- LWE
- learning with errors problem
area: cryptography/post-quantum
level: advanced
summary: Recover a secret s, or tell samples apart from uniform, given random a and b = <a, s> + e mod q with a small error e. Regev 2005. The base of most lattice encryption.
prereqs: [lattice-based-cryptography, bounded-distance-decoding, gaussian-elimination]
see_also: [regev-lwe-hardness, ring-learning-with-errors, module-learning-with-errors, learning-with-rounding, core-svp-hardness, arora-ge-algorithm, bkw-algorithm, regev-encryption]
sources:
  - paper: "Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, Journal of the ACM 56(6), Article 34, 2009"
    locator: Section 1 (the definition of LWE and Theorem 1.1), Section 4 (Lemma 4.1 average case to worst case over s, Lemma 4.2 decision to search for a prime modulus of polynomial size)
  - paper: "Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, STOC 2005, pages 84 to 93"
    locator: the conference version that introduced the problem
  - paper: "Benny Applebaum, David Cash, Chris Peikert and Amit Sahai, Fast cryptographic primitives and circular-secure encryption based on hard learning problems, CRYPTO 2009, LNCS 5677"
    locator: the transformation to a secret drawn from the error distribution (the normal form)
  - paper: "Chris Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4), 2016"
    locator: Section 4.2 (definitions of search and decision LWE, Theorem 4.2.4, and the list of search to decision results for other moduli in Section 4.2.2)
  - paper: "Martin R. Albrecht, Rachel Player and Sam Scott, On the concrete hardness of learning with errors, Journal of Mathematical Cryptology 9(3), pages 169 to 203, 2015"
    locator: the survey of the primal, dual, algebraic and combinatorial attacks and their costs
  - paper: "Richard Lindner and Chris Peikert, Better key sizes (and attacks) for LWE-based encryption, CT-RSA 2011, LNCS 6558"
    locator: the decoding form of the primal attack (BKZ followed by a nearest plane step)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Lattice-based Cryptography by Daniele Micciancio and Oded Regev (LWE, the dual distinguishing attack, and parameter choice)
---

Learning with errors (LWE) is the problem of finding a secret vector $s \in \mathbb{Z}_q^n$ from random linear equations $b_i = \langle a_i, s \rangle + e_i \bmod q$ whose right sides carry a small random error $e_i$, or of telling such equations apart from uniform ones. Oded Regev defined it in 2005 and proved that it is as hard as worst-case [lattice](/lattice/) problems for quantum algorithms (see [Regev's reduction](/regev-lwe-hardness/)). Without the errors, [Gaussian elimination](/gaussian-elimination/) solves it in polynomial time; with them, the best known algorithms take time exponential in $n$ for the parameters in use. It is the base of most of [lattice-based cryptography](/lattice-based-cryptography/), through its [ring](/ring-learning-with-errors/) and [module](/module-learning-with-errors/) forms also of ML-KEM.

**Notation.** $n$ is the dimension, $q \ge 2$ the modulus (here $q$ is a modulus, not a number of queries), $m$ the number of samples, $\chi$ the error distribution on $\mathbb{Z}$, and $\alpha \in (0,1)$ the error rate. $\langle a, s \rangle$ is the inner product mod $q$, and $\lambda$ is the security parameter, to which $n$ grows polynomially. $\mathcal{A}$ is an adversary and $\mathrm{Adv}$ its advantage. All statements are in the standard model.

## In plain words

Pick a secret list of numbers. Make many random equations: each one multiplies random numbers with the secret, adds them up, and takes the remainder by a fixed modulus. Before you publish an equation, add a small random error to its right side, such as 1, 0 or minus 1.

Without the errors, a student solves the equations by elimination. With them, elimination fails: each step adds and multiplies equations, and the small errors grow until they hide everything. The errors also make each equation look like random numbers. The problem asks you to find the secret, or only to tell such equations apart from random ones. No fast method is known, even for a quantum computer, and good evidence says that none exists.

## Definition

Fix $n$, $q$ and a distribution $\chi$ on $\mathbb{Z}$. For $s \in \mathbb{Z}_q^n$, the **LWE distribution** $A_{s,\chi}$ on $\mathbb{Z}_q^n \times \mathbb{Z}_q$ draws $a \in \mathbb{Z}_q^n$ uniformly and $e \leftarrow \chi$, and outputs

$$(a,\; b = \langle a, s \rangle + e \bmod q).$$

With $m$ samples in the rows of a matrix $A \in \mathbb{Z}_q^{m \times n}$, this is $b = A s + e \bmod q$ with $e \leftarrow \chi^m$.

**The error distribution.** Regev uses $\bar\Psi_\alpha$: draw a real normal value of mean 0 and standard deviation $\alpha q / \sqrt{2\pi}$, round it to the nearest integer, and reduce mod $q$. The number $\alpha q$ is the *width*; the density of the real normal value is proportional to $\exp(-\pi x^2 / (\alpha q)^2)$. Other common choices are the discrete Gaussian $D_{\mathbb{Z}, \alpha q}$, the uniform distribution on a small interval $[-B, B]$, and the centered binomial distribution of ML-KEM.

**Search-LWE$_{n,q,\chi,m}$.** Input: $m$ independent samples from $A_{s,\chi}$, for a secret $s$ (uniform in $\mathbb{Z}_q^n$, or arbitrary). Output: $s$.

**Decision-LWE$_{n,q,\chi,m}$.** Input: $m$ samples, either all from $A_{s,\chi}$ for one uniform $s$, or all uniform in $\mathbb{Z}_q^n \times \mathbb{Z}_q$. Output: a bit. The advantage of $\mathcal{A}$ is

$$\mathrm{Adv}^{\mathrm{lwe}}(\mathcal{A}) = \bigl|\Pr[\mathcal{A}((A, As + e)) = 1] - \Pr[\mathcal{A}((A, u)) = 1]\bigr|,$$

with $u$ uniform in $\mathbb{Z}_q^m$. The **LWE assumption** for a family of parameters $n(\lambda), q(\lambda), \chi(\lambda), m(\lambda)$ says that every adversary that runs in time polynomial in $\lambda$ has negligible advantage.

The secret is unique with high probability once $m$ is somewhat larger than $n$ and the error is small compared to $q$. A typical setting for the theory is $q = \mathrm{poly}(n)$, $\alpha q > 2\sqrt{n}$ and $m = \mathrm{poly}(n)$.

## Variants

- **Normal form.** The secret is drawn from $\chi^n$ instead of uniformly. Applebaum, Cash, Peikert and Sahai (2009) showed that this form is as hard as the uniform one: take $n$ samples $(A_1, b_1)$ with $A_1$ invertible, and map each other sample $(a, b)$ to $(-a^{\mathsf T} A_1^{-1},\; b - a^{\mathsf T} A_1^{-1} b_1)$. The result is LWE with secret $e_1$, the error of the first $n$ samples, and it costs $n$ samples. Most schemes, including ML-KEM, use a short secret for this reason.
- **Bounded and binary errors.** $\chi$ is uniform on $\{-B, \ldots, B\}$ or on $\{0, 1\}$. With few samples these forms are still hard; with many samples the [Arora-Ge algorithm](/arora-ge-algorithm/) solves them.
- **Learning parity with noise.** The case $q = 2$ with Bernoulli errors is [learning parity with noise](/learning-parity-with-noise/), the problem behind code-based schemes.
- **Structured forms.** [Ring-LWE](/ring-learning-with-errors/) and [Module-LWE](/module-learning-with-errors/) replace $\mathbb{Z}_q^n$ by a polynomial ring or a module over it, which saves a factor near $n$ in key size.
- **Deterministic errors.** [Learning with rounding](/learning-with-rounding/) rounds $\langle a, s \rangle$ instead of adding random noise.
- **Few samples and many secrets.** Schemes often fix $m$ near $n$ (one public key) and use the matrix form with several secrets at once, $B = AS + E$; a hybrid argument shows that each extra secret loses at most the advantage of one more LWE instance.

## Examples

**A toy instance.** Take $n = 3$, $q = 13$, the secret $s = (2, 5, 11)$ and errors in $\{-1, 0, 1\}$. Six samples:

| $a_i$ | $\langle a_i, s \rangle \bmod 13$ | $e_i$ | $b_i$ |
|---|---|---|---|
| $(7, 2, 11)$ | 2 | 0 | 2 |
| $(9, 4, 3)$ | 6 | 1 | 7 |
| $(11, 6, 12)$ | 2 | 1 | 3 |
| $(11, 12, 4)$ | 9 | 1 | 10 |
| $(8, 3, 10)$ | 11 | $-1$ | 10 |
| $(11, 7, 5)$ | 8 | 0 | 8 |

Elimination on the first three rows, with the errors ignored, gives $(6, 7, 1)$, which is wrong. The number of secrets in $\mathbb{Z}_{13}^3$ that fit the first $k$ samples with an error in $\{-1, 0, 1\}$ is 507, 117, 27, 8, 1 and 1 for $k = 1, \ldots, 6$. Each sample keeps about $3/13$ of the candidates, so here five samples fix $s$. In real dimensions this count cannot be done, because there are $q^n$ candidates.

**Without errors.** If every $e_i = 0$, three of these samples with an invertible $3 \times 3$ matrix give $s$ by elimination mod 13. The code finds $s = (2, 5, 11)$ from $b_i - e_i$.

**A toy lattice attack.** For $n = 10$, $q = 97$, $m = 22$ and $\alpha q = 2.5$ (standard deviation about 1), the error vector together with one more coordinate, $(e, 1)$, has norm about 5.0. It lies in a lattice of dimension 23 whose [Gaussian heuristic](/gaussian-heuristic/) length is about 12.6. That gap is large enough for [LLL](/lll-algorithm/): the primal attack below recovers $s$ in each of 20 random trials, and also for $n = 16$, $q = 257$, $m = 32$. These parameters are toy sizes. ML-KEM uses an LWE dimension of 512 to 1024 over $\mathbb{Z}_{3329}$, where LLL is far from enough.

**Non-example.** If $q$ is large and the error is 0, or if the error is so wide that $\chi$ mod $q$ is close to uniform, the problem is not LWE in a useful sense: the first is easy, and the second has no unique solution and carries no information about $s$.

## Known algorithms

**Exhaustive search.** Try every secret, $q^n$ of them (or the support of $\chi$ to the power $n$ in normal form), and keep the one with small residuals $b_i - \langle a_i, s \rangle$.

**Primal attack.** The vector $b$ is close to the $q$-ary lattice $\Lambda_q(A) = \{A x \bmod q\} + q\mathbb{Z}^m$, at distance $\|e\|$. So search-LWE is an instance of [bounded distance decoding](/bounded-distance-decoding/). Kannan's embedding adds $b$ as one more basis row; then $(e, 1)$ is an unusually short vector, and [unique-SVP](/unique-svp/) methods find it with [BKZ](/bkz-algorithm/) of a large enough block size. Lindner and Peikert (2011) use BKZ and then a nearest plane step instead. The block size that the attack needs, and so its cost, is the subject of [core-SVP hardness](/core-svp-hardness/).

```pseudo id=main
PRIMAL-ATTACK(A, b, q, B)               ▷ A in Z_q^(m×n), b = A s + e, |e_i| ≤ B
L1  reorder the samples so that the first n rows A_1 are invertible mod q
L2  C ← A_2 · A_1^(−1) mod q             ▷ Λ_q(A) = {(v, C v mod q)}
L3  rows (e_i, column i of C, 0) for i < n; rows (0, q·e_j, 0) for j < m − n
L4  last row (b, 1)                     ▷ (e, 1) lies in this lattice of dimension m + 1
L5  R ← LLL(rows)
L6  for each row r of R whose last entry is ±1 do
L7      e ← ±(r without its last entry)
L8      s ← A_1^(−1) (b_1 − e_1) mod q
L9      if |b_i − ⟨a_i, s⟩| ≤ B for every i then return s
L10 return FAIL
```

Line L3 is the Hermite normal form of $\Lambda_q(A)$, so the basis is square and LLL needs no step to remove dependent rows. Line L9 checks the answer, so the attack never returns a wrong secret; it can only fail.

**Dual attack.** Find a short $v \in \mathbb{Z}^m$ with $v^{\mathsf T} A = 0 \bmod q$, a vector of the [dual](/dual-lattice/) $q$-ary lattice and a solution of [SIS](/short-integer-solution/) on $A^{\mathsf T}$. Then $\langle v, b \rangle = \langle v, e \rangle \bmod q$ is small when $b$ is an LWE vector and uniform when $b$ is uniform. Many such $v$ give a distinguisher for decision-LWE. Its cost is also measured in the core-SVP model.

**Algebraic attack.** If the error takes only a few values, each sample gives a polynomial equation in $s$, and [Arora and Ge](/arora-ge-algorithm/) solve the system by linearization. With error width about $n^{\varepsilon}$ the time is $2^{\tilde O(n^{2\varepsilon})}$. This is subexponential only for $\varepsilon < 1/2$, which is why the hardness theorem asks for $\alpha q > 2\sqrt{n}$. It needs about $n^{|E|}$ samples, far more than a scheme gives out.

**Combinatorial attack.** The [BKW algorithm](/bkw-algorithm/) adds and subtracts samples that agree on blocks of coordinates until only a few coordinates are left. It needs exponentially many samples and much memory.

**Quantum algorithms.** No quantum algorithm is known that solves LWE much faster than the classical ones. The known gain is generic: [Grover search](/grover-search/) inside lattice sieving, which lowers the exponent constant of the core-SVP estimate from 0.292 to 0.265.

The Python code with this page samples LWE, solves the case without error by elimination, runs the primal attack with its own LLL, and runs the search to decision reduction below. It is for study only, is not constant time, and works only on toy parameters. Real systems must use a validated implementation of a standard such as FIPS 203 (ML-KEM), for example a FIPS 140 validated module.

## Bounds

- **Upper bounds.** For $q = \mathrm{poly}(n)$ and $\alpha q = \Theta(\sqrt n)$, lattice reduction and BKW solve LWE in time $2^{O(n)}$. For error width $n^{\varepsilon}$ with $\varepsilon < 1/2$, Arora-Ge gives $2^{\tilde O(n^{2\varepsilon})}$ with enough samples.
- **Hardness.** For $\alpha q > 2\sqrt{n}$, solving LWE is at least as hard as quantum approximation of GapSVP and SIVP to within $\tilde O(n/\alpha)$ in the worst case (Regev). Classical reductions exist for GapSVP (Peikert 2009 for exponential $q$; Brakerski, Langlois, Peikert, Regev and Stehlé 2013 for polynomial $q$). The exact statements are on the page [Regev's LWE hardness reduction](/regev-lwe-hardness/).
- **Concrete security.** The reductions are not tight enough to set parameters. Schemes choose $n$, $q$ and $\chi$ from the cost of the best known attacks, in the [core-SVP](/core-svp-hardness/) model or with the lattice estimator of Albrecht, Player and Scott.

## Reductions

- **Decision to search (Regev, Lemma 4.2).** For a prime $q \le \mathrm{poly}(n)$, an oracle that tells $A_{s,\chi}$ from uniform for every $s$ gives $s$. To test a guess $k$ for $s_1$, map each sample $(a, b)$ to $(a + \ell e_1, b + \ell k)$ with a fresh uniform $\ell \in \mathbb{Z}_q$. If $k = s_1$ the new samples come from $A_{s,\chi}$; if not, $b$ gains the term $\ell (k - s_1)$, which is uniform because $k - s_1$ is invertible. At most $nq$ calls give $s$. Later work extended the equivalence to other moduli, including composite and exponentially large ones (Peikert's survey, Section 4.2.2, lists them). The code runs this reduction with a brute-force decision oracle on $n = 2$, $q = 13$.
- **Worst case to average case over $s$ (Regev, Lemma 4.1).** Add $\langle a, t \rangle$ to $b$ for a uniform $t$: samples for $s$ become samples for the uniform secret $s + t$.
- **Normal form.** Uniform secret to short secret, as in Variants.
- **From worst-case lattice problems.** GapSVP and SIVP reduce to LWE; see [Regev's reduction](/regev-lwe-hardness/).
- **To lattice problems.** Search-LWE reduces to [BDD](/bounded-distance-decoding/) on $\Lambda_q(A)$, and decision-LWE reduces to finding short vectors in the dual lattice, which is [SIS](/short-integer-solution/) on $A^{\mathsf T}$.
- **To and from structured forms.** LWE is Module-LWE of rank $n$ over $\mathbb{Z}$, and Ring-LWE is its rank 1 case over a ring.

## Applications

- **Public-key encryption.** [Regev encryption](/regev-encryption/) (IND-CPA under decision-LWE) and its descendants [FrodoKEM](/frodokem/) (plain LWE) and [ML-KEM](/crystals-kyber/) (Module-LWE).
- **Signatures and trapdoors.** [GPV signatures](/gpv-signature/) and [lattice trapdoors](/trapdoor-sampling-lattices/) rest on SIS and LWE together.
- **Fully homomorphic encryption.** The second and third generation [homomorphic](/homomorphic-encryption/) schemes rest on LWE and Ring-LWE.
- **Pseudorandom functions.** Through [learning with rounding](/learning-with-rounding/).
- **Learning theory.** LWE is a hard learning problem in the sense of [PAC learning](/pac-learning/): it generalizes learning parities with noise to larger moduli.

## References
