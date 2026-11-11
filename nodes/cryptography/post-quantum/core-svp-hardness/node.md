---
tag: AEJ0J4
kind: definition
slug: core-svp-hardness
name: Core-SVP hardness
aliases:
- core-SVP model
- bit-security estimate for lattice schemes
area: cryptography/post-quantum
level: advanced
summary: A conservative cost model for lattice attacks. Find the BKZ block size b that breaks the scheme, then count only one SVP call, 2^(0.292 b) classical or 2^(0.265 b) quantum.
prereqs: [bkz-algorithm, learning-with-errors, gaussian-heuristic]
see_also: [lattice-sieving, quantum-sieving, root-hermite-factor, unique-svp, dual-lattice, crystals-kyber, crystals-dilithium, module-learning-with-errors]
sources:
  - paper: "Erdem Alkim, Leo Ducas, Thomas Poppelmann and Peter Schwabe, Post-quantum key exchange, a new hope, USENIX Security 2016"
    locator: Section 6, the core-SVP methodology, the primal attack with the GSA success condition, and the dual attack with 2^(0.2075 b) vectors per sieve
  - paper: "Anja Becker, Leo Ducas, Nicolas Gama and Thijs Laarhoven, New directions in nearest neighbor searching with applications to lattice sieving, SODA 2016"
    locator: the sieve with heuristic time (3/2)^(b/2 + o(b)) = 2^(0.292 b + o(b))
  - paper: "Thijs Laarhoven, Search problems in cryptography, from fingerprinting to lattice sieving, PhD thesis, Eindhoven University of Technology, 2015"
    locator: the quantum sieve with Grover search and heuristic time 2^(0.265 b + o(b))
  - url: "https://pq-crystals.org/kyber/data/kyber-specification-round3-20210131.pdf"
    title: Roberto Avanzi, Joppe Bos, Leo Ducas, Eike Kiltz, Tancrede Lepoint, Vadim Lyubashevsky, John M. Schanck, Peter Schwabe, Gregor Seiler and Damien Stehle, CRYSTALS-Kyber algorithm specifications and supporting documentation, version 3.01, 2021
    locator: Sections 5.1.1 to 5.1.4 (the core-SVP analysis, Eq. (9), the dual attack), Section 5.2 (beyond core-SVP), and Table 4
  - paper: "Martin R. Albrecht, Rachel Player and Sam Scott, On the concrete hardness of learning with errors, Journal of Mathematical Cryptology 9(3), 2015"
    locator: the survey of attacks on LWE and the estimator that computes their costs in several cost models
---

Core-SVP hardness is a simple, conservative way to give a lattice-based scheme a bit-security figure. One finds the smallest block size $b$ with which [BKZ](/bkz-algorithm/) makes the best known lattice attack succeed, and then counts only the cost of a single call to an SVP solver in dimension $b$: $2^{0.292 b}$ classically and $2^{0.265 b}$ on a quantum computer. Alkim, Ducas, Pöppelmann and Schwabe (ADPS) introduced the model for NewHope in 2016, and it became the common yardstick of the lattice candidates in the NIST process, including Kyber (ML-KEM) and Dilithium (ML-DSA).

**Notation.** $n$ is the dimension of the LWE secret (for Module-LWE of rank $k$ over a ring of degree 256, $n = 256k$), $q$ the modulus (not a number of queries), $m$ the number of LWE samples used, and $\varsigma$ the standard deviation of each secret and error coefficient. $b$ is the BKZ block size, $d$ the dimension of the attack lattice, and $\delta = \delta(b)$ the root Hermite factor that BKZ-$b$ reaches. $\varepsilon$ is a distinguishing advantage, $\ell$ the length of a dual vector, and $\lambda$ a security level in bits.

## Definition

**Block size to root Hermite factor.** BKZ-$b$ is modeled as reaching

$$\delta(b) = \left( (\pi b)^{1/b} \cdot \frac{b}{2\pi e} \right)^{1/(2(b-1))}.$$

**Primal attack.** From $m$ samples $(A, As + e)$ build the lattice $\{x \in \mathbb{Z}^{m+n+1} : (A \mid I_m \mid -b)\,x \equiv 0 \pmod q\}$ of dimension $d = m + n + 1$ and volume $q^m$. It contains the short vector $v = (s, e, 1)$. Under the geometric series assumption (GSA), BKZ-$b$ returns a basis with Gram-Schmidt norms $\|b_i^*\| = \delta^{d - 2i - 1} \mathrm{Vol}^{1/d}$. The projection of $v$ onto the last $b$ Gram-Schmidt directions has expected length $\varsigma \sqrt{b}$, and BKZ finds $v$ when this is below $\|b^*_{d-b}\|$:

$$\varsigma \sqrt{b} \le \delta^{2b - d - 1} \cdot q^{m/d}.$$

The primal block size $b_{\mathrm{primal}}$ is the smallest $b$ for which some allowed $m$ satisfies this condition.

**Dual attack.** BKZ-$b$ on the lattice $\{(x, y) \in \mathbb{Z}^m \times \mathbb{Z}^n : A^{\mathsf T} x \equiv y\}$, of dimension $d = m + n$ and volume $q^n$, gives a vector of length $\ell = \delta^{d-1} q^{n/d}$. Its inner product with the samples is Gaussian of width $\ell \varsigma$ for LWE and uniform otherwise, which gives an advantage $\varepsilon = 4 \exp(-2\pi^2 \tau^2)$ with $\tau = \ell\varsigma/q$. ADPS assume a sieve gives $2^{0.2075 b}$ such vectors, and that about $1/\varepsilon^2$ vectors are needed, so the attack is repeated $R = \max(1, 1/(2^{0.2075 b} \varepsilon^2))$ times.

**Core-SVP hardness.** With $b$ the block size of the cheapest attack,

$$\text{classical: } 0.292\, b \text{ bits}, \qquad \text{quantum: } 0.265\, b \text{ bits},$$

times $R$ for the dual attack. The constant 0.292 is the exponent of the classical sieve of Becker, Ducas, Gama and Laarhoven (2016), $(3/2)^{b/2} \approx 2^{0.292 b}$. The constant 0.265 is that of Laarhoven's quantum sieve with Grover search (2015). Both drop the $o(b)$ terms.

**Why it is conservative.** The model counts one SVP call, although BKZ makes many; it drops all lower-order terms of the sieve; it works in the RAM model, in which access to exponential memory is free; and in the dual attack it takes every sieve output to be as short as the shortest. The GSA is slightly optimistic for the attacker. The result is meant as a lower bound on the cost of known attacks, not as a prediction. The Kyber round 3 specification calls the method informative but too coarse for accurate estimates and adds a refined analysis in its Section 5.2.

## Examples and non-examples

**Kyber round 3, Table 4 (primal attack only).**

| | Kyber512 | Kyber768 | Kyber1024 |
|---|---|---|---|
| lattice dimension $d$ | 1003 | 1424 | 1885 |
| block size $b$ | 403 | 625 | 877 |
| core-SVP classical | 118 | 182 | 256 |
| core-SVP quantum | 107 | 165 | 232 |

The bit figures agree with $0.292 b$ and $0.265 b$ to within 1; for example $0.292 \cdot 403 = 117.7$ and $0.265 \cdot 625 = 165.6$. For Kyber512 the figure 118 is for the public keys; the ciphertexts reach 112 bits from the LWE noise alone and 118 only when the rounding noise of compression is also counted, a weak form of the [LWR](/learning-with-rounding/) assumption.

**Recomputing Kyber512.** Take $n = 512$, $q = 3329$, $\varsigma = \sqrt{3/2}$ (the centered binomial distribution with $\eta_1 = 3$), and $m \le 768$. The calculator with this page finds $b = 406$ at $m = 486$, so $d = 999$. There $\delta(406) \approx 1.003941$, the left side of the condition is $\varsigma\sqrt{406} \approx 24.678$, and the right side is $\delta^{-188} \cdot 3329^{486/999} \approx 24.683$, so the condition holds. For $b = 405$ the right side is about 24.459, below $\varsigma \sqrt{405} \approx 24.648$, and no $m \le 768$ works. The resulting costs are $0.292 \cdot 406 \approx 118.6$ and $0.265 \cdot 406 \approx 107.6$ bits. For Kyber768 ($n = 768$, $\eta_1 = 2$) and Kyber1024 ($n = 1024$, $\eta_1 = 2$) it finds $b = 624$ and $b = 874$. These are within 1% of Table 4 but not equal to it, because the Kyber scripts model the noise and the success probability in more detail than the plain formula. The tests check this agreement within 1% in $b$ and 1 bit in cost.

The Python code is for study only. It is a rough model, not a tool for choosing parameters; for that use the lattice estimator of Albrecht, Player and Scott and its successors. The code does no cryptography, so constant time does not apply to it.

**Refined estimates.** Section 5.2 of the Kyber specification counts more than one SVP call, uses dimensions for free, and reports block sizes 413, 637 and 894, with lattice dimensions 1025, 1467 and 1918. It also gives smaller sieving dimensions $b' = 375$, $586$ and $829$. These figures are outside the core-SVP model.

**Non-example: a bound from a reduction.** The worst-case to average-case reductions for LWE, such as [Regev's theorem](/regev-lwe-hardness/), give no bit-security figure. Core-SVP is an estimate of the cost of known attacks, not a proof.

**Non-example: algebraic and combinatorial attacks.** The [Arora-Ge](/arora-ge-algorithm/) and [BKW](/bkw-algorithm/) attacks are not lattice reduction and fall outside the model. For the noise widths and sample counts of Kyber they cost more than the lattice attacks, so the model ignores them.

## Related definitions

- **Root Hermite factor.** The quantity $\delta$ above; see [root Hermite factor](/root-hermite-factor/).
- **Unique-SVP.** The primal attack is a [unique-SVP](/unique-svp/) attack. Older analyses used the success condition $\lambda_2/\lambda_1 \ge \tau \delta^d$ of Gama and Nguyen; the ADPS condition based on projections is more conservative.
- **Sieving costs.** The constants come from [lattice sieving](/lattice-sieving/) and [quantum sieving](/quantum-sieving/). Enumeration has a cost that grows faster than exponentially and is not used in the model.
- **Lattice estimator.** The estimator of Albrecht, Player and Scott computes the cost of many attacks, including the primal, dual, hybrid, Arora-Ge and BKW attacks, in several cost models, of which core-SVP is one.
- **NIST security levels.** Kyber maps the core-SVP figures and the refined gate counts to the NIST categories, defined by the cost of key search on AES and of collision search on a 256-bit or 384-bit hash function.

## References
