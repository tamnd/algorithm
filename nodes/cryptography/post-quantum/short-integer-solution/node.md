---
tag: JRMD0G
kind: problem
slug: short-integer-solution
name: Short integer solution problem
aliases:
- SIS
area: cryptography/post-quantum
level: advanced
summary: Given a random matrix A mod q, find a short nonzero integer vector z with A z = 0 mod q. Ajtai 1996. As hard as worst-case SIVP; it gives collision-resistant hashing and signatures.
prereqs: [lattice-based-cryptography, shortest-independent-vectors-problem]
see_also: [ring-short-integer-solution, module-short-integer-solution, learning-with-errors, ajtai-worst-case-to-average-case-reduction, collision-resistance, gpv-signature, birthday-attack, dual-lattice]
sources:
  - paper: "Miklos Ajtai, Generating hard instances of lattice problems, STOC 1996, pages 99 to 108"
    locator: the one-way function f_A(x) = A x mod q on 0/1 vectors and the reduction from worst-case lattice problems
  - paper: "Daniele Micciancio and Oded Regev, Worst-case to average-case reductions based on Gaussian measures, SIAM Journal on Computing 37(1), pages 267 to 302, 2007"
    locator: the main reduction from SIVP and GapSVP to SIS with an approximation factor near n
  - paper: "Craig Gentry, Chris Peikert and Vinod Vaikuntanathan, Trapdoors for hard lattices and new cryptographic constructions, STOC 2008"
    locator: the SIS and ISIS reductions with a smaller modulus (q at least beta times a factor near the square root of n log n), and the trapdoor signatures built on ISIS
  - paper: "Chris Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4), 2016"
    locator: Section 4.1 (the definition of SIS, Theorem 4.1.2 on its worst-case hardness, and the hash function)
  - book: isbn:9783540887010
    title: Daniel J. Bernstein, Johannes Buchmann and Erik Dahmen (editors), Post-Quantum Cryptography, Springer, 2009
    locator: the chapter Lattice-based Cryptography by Daniele Micciancio and Oded Regev (the SIS hash function and the attack by lattice reduction on a subset of the columns)
---

The short integer solution problem (SIS) asks, for a random matrix $A \in \mathbb{Z}_q^{n \times m}$, for a nonzero integer vector $z$ of norm at most $\beta$ with $A z = 0 \bmod q$. Miklós Ajtai introduced it in 1996, together with the first proof that an average-case problem of this kind is as hard as worst-case [lattice](/lattice/) problems ([Ajtai's reduction](/ajtai-worst-case-to-average-case-reduction/)). It is the base of the lattice [hash functions](/cryptographic-hash-function/) and, in its [module form](/module-short-integer-solution/), of the signature standard ML-DSA. It is one of the two central problems of [lattice-based cryptography](/lattice-based-cryptography/); the other is [learning with errors](/learning-with-errors/).

**Notation.** $n$ is the number of rows (the security dimension), $m$ the number of columns, $q$ the modulus (not a number of queries), $\beta$ the norm bound, and $\|\cdot\|$ the Euclidean norm unless the text says $\|\cdot\|_\infty$. $\lambda$ is the security parameter; $\mathcal{A}$ is an adversary. Security statements are in the standard model.

## In plain words

You get a table of random numbers with a few rows and many columns. You must pick a combination of the columns, with small whole-number weights such as 1, 0 or minus 1 and not all zero, so that every row sums to a multiple of a fixed modulus.

If any weights are allowed, ordinary elimination finds a combination at once, but its weights are large numbers. The small weights make the task hard. A short answer always exists when there are enough columns, because there are more small combinations than possible sums, so two of them must give the same sums, and their difference is an answer. Finding one is the hard part. This is what makes the map from small combinations to sums a good hash function.

## Definition

**SIS$_{n,q,\beta,m}$.** Input: a uniformly random $A \in \mathbb{Z}_q^{n \times m}$. Output: $z \in \mathbb{Z}^m$ with

$$z \ne 0, \qquad \|z\| \le \beta, \qquad A z = 0 \pmod q.$$

The set of all $z \in \mathbb{Z}^m$ with $Az = 0 \bmod q$ is the $q$-ary lattice $\Lambda_q^\perp(A)$, so SIS asks for a short nonzero vector of $\Lambda_q^\perp(A)$: it is approximate [SVP](/shortest-vector-problem/) on a random lattice of this family. When the columns span $\mathbb{Z}_q^n$, $\Lambda_q^\perp(A)$ has dimension $m$ and volume $q^n$.

An adversary $\mathcal{A}$ solves SIS with advantage $\Pr[\mathcal{A}(A) \text{ outputs a valid } z]$ over the choice of $A$ and its coins. The **SIS assumption** for parameters $n(\lambda), q(\lambda), \beta(\lambda), m(\lambda)$ says that this advantage is negligible for every adversary that runs in time polynomial in $\lambda$.

**Conditions for a sensible instance.**

- If $\beta \ge q$, the vector $(q, 0, \ldots, 0)$ is a trivial solution.
- If $m > n \log_2 q$ and $\beta \ge \sqrt{m}$, a solution in $\{-1, 0, 1\}^m$ always exists. There are $2^m$ vectors in $\{0,1\}^m$ and only $q^n < 2^m$ values of $Ax \bmod q$, so two different $x, x'$ give the same value, and $z = x - x'$ is a solution.

## Variants

- **Inhomogeneous SIS (ISIS).** Given $A$ and a target $u \in \mathbb{Z}_q^n$, find a short $z$ with $A z = u \bmod q$. The GPV signature is a short ISIS solution for $u = H(\text{message})$.
- **Infinity norm.** The bound is on $\|z\|_\infty$. SIS$^\infty$ with bound 1 is the collision problem of Ajtai's hash.
- **Structured forms.** [Ring-SIS](/ring-short-integer-solution/) takes $A$ as a row of polynomials in $\mathbb{Z}_q[x]/(f)$; [Module-SIS](/module-short-integer-solution/) takes a small matrix of polynomials. Both save a factor near $n$ in key size, at the price of a reduction from a narrower class of lattices.
- **SelfTargetMSIS.** A variant in which the target depends on the solution through a hash function, used in the security proof of ML-DSA (see [Module-SIS](/module-short-integer-solution/)).

## Examples

**A tiny instance.** Take $n = 2$, $q = 11$, $m = 8$ and

$$A = \begin{pmatrix} 1 & 5 & 8 & 8 & 10 & 1 & 3 & 9 \\ 9 & 8 & 6 & 9 & 8 & 7 & 9 & 7 \end{pmatrix}.$$

There are $2^8 = 256$ vectors in $\{0,1\}^8$ and $11^2 = 121$ outputs, and $8 > 2 \log_2 11 \approx 6.92$. Random 0/1 vectors $x = (0,1,1,1,1,1,1,0)$ and $x' = (1,0,0,0,0,0,1,1)$ both give $Ax \bmod 11 = (2, 3)$; the search took 13 tries. The difference $z = (-1, 1, 1, 1, 1, 1, 0, -1)$ gives row sums $22$ and $22$, both $0 \bmod 11$, and $\|z\| = \sqrt 7 \approx 2.65$.

**Toy collisions.** With $n = 3$, $q = 101$, $m = 24$ there are $101^3 \approx 2^{19.97}$ outputs. Over 200 random instances the birthday search needed 1229 tries on average, near the predicted $\sqrt{\pi \cdot 101^3 / 2} \approx 1272$. With $n = 512$ and $q = 3329$ the output space has about $2^{5990}$ elements, and this search is hopeless.

**Non-example.** A nonzero $z$ with $Az = 0 \bmod q$ and no length bound is found by [Gaussian elimination mod q](/gaussian-elimination-modular/) in polynomial time: fix one free coordinate to 1 and solve for the pivots. The other entries are then spread over $\mathbb{Z}_q$, so $z$ is long. In 500 random toy instances with $q = 101$ the code found a kernel vector each time, and in 497 of them the vector had an entry above 1.

## Known algorithms

- **Birthday search.** Hash random short vectors until two collide; this takes about $q^{n/2}$ hash evaluations and as much memory. Merging lists that agree on parts of the output, as in the [BKW algorithm](/bkw-algorithm/), lowers the cost when $m$ is very large.
- **Lattice reduction.** Run [BKZ](/bkz-algorithm/) on a basis of $\Lambda_q^\perp(A')$ for a submatrix $A'$ of $d \le m$ columns. If BKZ reaches [root Hermite factor](/root-hermite-factor/) $\delta$, the shortest vector found has length about $\delta^d q^{n/d}$. Micciancio and Regev choose $d = \sqrt{n \log q / \log \delta}$, which gives length about $2^{2\sqrt{n \log q \log \delta}}$; the attack works when this is at most $\beta$. The cost of BKZ for the needed $\delta$ is then estimated as in the [core-SVP](/core-svp-hardness/) model.
- **No better quantum algorithm** is known than lattice reduction with quantum [sieving](/quantum-sieving/), which changes only the constant in the exponent.

The Python code with this page computes $f_A(x) = Ax \bmod q$, checks SIS solutions, finds kernel vectors by elimination, and turns a birthday collision into a SIS solution. It is for study only, is not constant time, and runs only on toy parameters. For hashing use SHA-2 or SHA-3 from a standard library; for lattice signatures use a FIPS 140 validated ML-DSA module.

## Bounds

- **Worst-case hardness.** Ajtai (1996) proved that for suitable $m, q = \mathrm{poly}(n)$, solving SIS on average is at least as hard as approximating SIVP and related problems within a polynomial factor in the worst case. Micciancio and Regev (2007) brought the factor down to about $n$ with Gaussian measures. Gentry, Peikert and Vaikuntanathan (2008) showed: for any $m = \mathrm{poly}(n)$, any $\beta = \mathrm{poly}(n)$ and any prime $q \ge \beta \cdot \omega(\sqrt{n \log n})$, solving SIS$_{n,q,\beta,m}$ with non-negligible probability is at least as hard as [SIVP](/shortest-independent-vectors-problem/)$_\gamma$ and [GapSVP](/gap-svp/)$_\gamma$ for $\gamma = \beta \cdot \tilde O(\sqrt{n})$, in the worst case.
- **The reductions are classical.** Unlike the LWE reduction, these reductions run on a classical computer.
- **Concrete hardness.** The reductions do not set parameters. Schemes size $n$, $q$ and $\beta$ from the BKZ cost above.
- **Upper bounds.** For $\beta = \mathrm{poly}(n)$ and $q = \mathrm{poly}(n)$, the attack by lattice reduction needs BKZ with a block size linear in $n$, so the best known algorithms take time $2^{\Theta(n)}$. For a bound $\beta$ that is large enough and exponential in $m$, LLL finds a solution in polynomial time.

## Reductions

- **SIS to collision-resistant hashing.** A collision $x \ne x'$ of $f_A$ on $\{0,1\}^m$ gives the SIS solution $x - x'$ with $\|x - x'\|_\infty \le 1$. So $f_A$ is [collision resistant](/collision-resistance/) under the SIS assumption with $\beta = \sqrt m$; this is a tight reduction with no loss.
- **ISIS and SIS.** A SIS solver gives an ISIS solver for the matrix $[A \mid -u]$ when the last coordinate of the solution is $\pm 1$.
- **SIS and LWE.** A short $v$ with $v^{\mathsf T} A = 0 \bmod q$ is a SIS solution for $A^{\mathsf T}$ and distinguishes LWE samples $(A, As + e)$ from uniform, because $\langle v, As + e \rangle = \langle v, e \rangle$ is small. This is the dual attack on [LWE](/learning-with-errors/).
- **To approximate SVP.** SIS is approximate SVP on $\Lambda_q^\perp(A)$, which is the [dual](/dual-lattice/) of the LWE lattice $\Lambda_q(A^{\mathsf T})$ scaled by $q$.

## Applications

- **Ajtai's hash function** $f_A(x) = Ax \bmod q$ on $\{0,1\}^m$, and its ring form SWIFFT (see [Ring-SIS](/ring-short-integer-solution/)).
- **Signatures.** [GPV hash-and-sign signatures](/gpv-signature/) with [trapdoors](/trapdoor-sampling-lattices/) (ISIS), the [Fiat-Shamir with aborts](/fiat-shamir-with-aborts/) signatures of Lyubashevsky, and [ML-DSA](/crystals-dilithium/) (Module-SIS).
- **Commitments and zero-knowledge proofs** with a binding property under SIS.

## References
