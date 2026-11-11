---
tag: XT34ZK
kind: theorem
slug: regev-lwe-hardness
name: Regev's LWE hardness reduction
aliases:
- Regev's reduction
- quantum reduction from GapSVP to LWE
area: cryptography/post-quantum
level: advanced
summary: "If LWE with alpha q > 2 sqrt(n) is easy, a quantum algorithm approximates GapSVP and SIVP within O~(n/alpha) in the worst case. Peikert and BLPRS later gave classical forms for GapSVP."
prereqs: [learning-with-errors, gap-svp, shortest-independent-vectors-problem, bounded-distance-decoding]
see_also: [ring-lwe-hardness, ajtai-worst-case-to-average-case-reduction, regev-encryption, core-svp-hardness, gaussian-sampling-over-lattices, quantum-fourier-transform, dual-lattice, search-to-decision-reduction]
sources:
  - paper: "Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, Journal of the ACM 56(6), Article 34, 2009"
    locator: Theorem 1.1, Section 3 (Theorem 3.1, Lemma 3.2 bootstrapping, Lemma 3.3 iterative step, Lemma 3.4 classical part, Lemma 3.14 quantum part), Section 4 (Lemmas 4.1 to 4.3)
  - paper: "Oded Regev, On lattices, learning with errors, random linear codes, and cryptography, STOC 2005, pages 84 to 93"
    locator: the conference version
  - paper: "Chris Peikert, Public-key cryptosystems from the worst-case shortest vector problem, STOC 2009, pages 333 to 342"
    locator: Definition 2.7 (zeta-to-gamma GapSVP) and Theorem 3.1 (the classical reduction to LWE with an exponential modulus)
  - paper: "Zvika Brakerski, Adeline Langlois, Chris Peikert, Oded Regev and Damien Stehle, Classical hardness of learning with errors, STOC 2013, pages 575 to 584"
    locator: Theorem 1.1, Theorem 3.1 and Corollaries 3.2 and 3.4 (modulus switching and the trade-off between dimension and modulus), Theorem 4.1 (LWE with binary secret)
  - paper: "Chris Peikert, A decade of lattice cryptography, Foundations and Trends in Theoretical Computer Science 10(4), pages 283 to 424, 2016"
    locator: Section 4.2.2 (Theorem 4.2.4 and the outline of the quantum reduction) and Section 4.2.4 (classical hardness)
  - paper: "Dorit Aharonov and Oded Regev, Lattice problems in NP intersect coNP, Journal of the ACM 52(5), 2005"
    locator: the main theorem (GapSVP and GapCVP with factor sqrt(n) are in NP and coNP)
---

Regev's reduction is the theorem that an efficient algorithm for [learning with errors](/learning-with-errors/) gives an efficient quantum algorithm for worst-case approximate [GapSVP](/gap-svp/) and [SIVP](/shortest-independent-vectors-problem/) with polynomial factors. Oded Regev proved it in 2005, and it is the reason LWE is trusted as a base for [lattice-based cryptography](/lattice-based-cryptography/). Peikert (2009) and Brakerski, Langlois, Peikert, Regev and Stehlé (2013) gave classical reductions for GapSVP. None of these results gives concrete parameters.

**Notation.** $n$ is the lattice dimension, $q$ the LWE modulus (Regev writes $p$; here $q$ is a modulus, not a number of queries), $\alpha \in (0,1)$ the error rate, $L \subset \mathbb{R}^n$ a full-rank lattice and $L^*$ its [dual](/dual-lattice/). For $r > 0$, $\rho_r(x) = \exp(-\pi \|x\|^2 / r^2)$, and the discrete Gaussian $D_{L,r}$ gives $x \in L$ probability $\rho_r(x) / \rho_r(L)$. The smoothing parameter $\eta_\varepsilon(L)$ is the least $s > 0$ with $\rho_{1/s}(L^* \setminus \{0\}) \le \varepsilon$. $\Psi_\alpha$ is the normal distribution of standard deviation $\alpha / \sqrt{2\pi}$ reduced mod 1, and $\bar\Psi_\alpha$ its discretization on $\mathbb{Z}_q$ (multiply by $q$ and round). LWE$_{q,\chi}$ is [learning with errors](/learning-with-errors/) in dimension $n$ with modulus $q$ and error $\chi$. DGS$_\gamma$ is the problem: given a basis of $L$ and $r \ge \gamma(L)$, output a sample from $D_{L,r}$.

## Statement

**Theorem (Regev 2009, Theorem 1.1).** Let $n, q$ be integers and $\alpha \in (0,1)$ with $\alpha q > 2\sqrt{n}$. If there is an efficient (polynomial-time) algorithm that solves LWE$_{q, \bar\Psi_\alpha}$, then there is an efficient quantum algorithm that approximates the worst-case problems [GapSVP](/gap-svp/) and [SIVP](/shortest-independent-vectors-problem/) in dimension $n$ to within a factor $\tilde O(n/\alpha)$.

**Main step (Regev 2009, Theorem 3.1).** Let $\varepsilon(n)$ be negligible, $q(n) \ge 2$ an integer and $\alpha(n) \in (0,1)$ with $\alpha q > 2\sqrt{n}$. Assume an oracle $W$ that solves search LWE$_{q,\Psi_\alpha}$ from a polynomial number of samples. Then there is an efficient quantum algorithm for DGS$_{\sqrt{2n} \cdot \eta_\varepsilon(L)/\alpha}$.

DGS with this width gives SIVP within $\tilde O(n/\alpha)$, because $\eta_\varepsilon(L) \le \omega(\sqrt{\log n}) \cdot \lambda_n(L)$ for negligible $\varepsilon$ and $n$ independent samples of $D_{L,r}$ have length at most $r\sqrt n$ with high probability. Regev's Section 3.3 gives the step from DGS to GapSVP. The discretization step (Lemma 4.3) moves from $\Psi_\alpha$ to $\bar\Psi_\alpha$, and for a prime $q \le \mathrm{poly}(n)$ Lemma 4.2 extends the result to decision-LWE.

**Classical form for GapSVP (Peikert 2009, Theorem 3.1).** Let $\alpha \in (0,1)$, $\gamma \ge n / (\alpha \sqrt{\log n})$, $\zeta \ge \gamma$ and $q \ge \zeta \cdot \omega(\sqrt{\log n / n})$. There is a probabilistic polynomial-time classical reduction from the worst-case problem $\zeta$-to-$\gamma$-GapSVP to search LWE$_{q,\Psi_\alpha}$ with $\mathrm{poly}(n)$ samples. Here $\zeta$-to-$\gamma$-GapSVP is GapSVP$_\gamma$ restricted to instances with $\lambda_1(L) \le \zeta$ and a basis with $\min_i \|\tilde b_i\| \ge 1$; for $\zeta \ge 2^{n/2}$ it equals GapSVP$_\gamma$, since LLL produces such a basis. So for $q \ge 2^{n/2}$, LWE is classically as hard as GapSVP$_{\tilde O(n/\alpha)}$. This form covers GapSVP only, not SIVP.

**Classical form with a small modulus (Brakerski, Langlois, Peikert, Regev and Stehlé 2013, Theorem 1.1, informal).** Solving $n$-dimensional LWE with a modulus $q = \mathrm{poly}(n)$ implies an equally efficient solution to a worst-case lattice problem (GapSVP) in dimension $\sqrt{n}$.

## In plain words

The theorem says: anyone who can solve random noisy equations of the LWE kind can, with a quantum computer, find short vectors in every lattice, even in the hardest ones. So an attack on LWE in general would also solve lattice problems that experts have studied for decades without success.

The proof uses the LWE solver many times. It starts with long random lattice vectors, which are easy to make, and uses the solver and a quantum step to make shorter and shorter random vectors, until they are short enough to answer the lattice question. Later work removed the quantum step for one of the two lattice problems, at the price of a larger modulus or a smaller lattice dimension. None of the proofs gives a key size.

## Proof

This is an outline of Regev's proof, with the lemma numbers of the journal version. The complete proof is Section 3 of Regev 2009.

**Plan.** Let $L$ be the input lattice. Set $r_i = r \cdot (\alpha q / \sqrt{n})^i$ for $i = 0, 1, \ldots, 3n$, where $r = \sqrt{2n} \cdot \eta_\varepsilon(L) / \alpha$ is the target width. Because $\alpha q > 2\sqrt n$, the ratio $\alpha q / \sqrt n$ is above 2, so $r_{3n} > 2^{3n} r$.

**Step 1: bootstrapping (Lemma 3.2).** For $r' > 2^{2n} \lambda_n(L)$, samples from $D_{L,r'}$ can be computed classically: run [LLL](/lll-algorithm/) to get a basis of length at most $2^n \lambda_n(L)$, draw a continuous Gaussian point, and reduce it modulo the basis. Regev shows that $r_{3n}$ is at least this large, with a transference bound that relates $\eta_\varepsilon(L)$ to $\lambda_n(L)$, so the algorithm gets $n^c$ samples from $D_{L, r_{3n}}$ for any fixed $c$.

**Step 2: the iterative step (Lemma 3.3).** Given $n^c$ samples from $D_{L, r'}$ with $r' > \sqrt 2\, q\, \eta_\varepsilon(L)$, the step outputs one sample from $D_{L, r' \sqrt n / (\alpha q)}$. Repeated $n^c$ times, it turns samples at width $r_i$ into samples at width $r_{i-1}$. It has two parts.

*Classical part (Lemma 3.4): samples and the LWE oracle solve BDD on the dual.* The input is a point $x$ at distance at most $d = \alpha q / (\sqrt 2\, r')$ from the dual lattice $L^*$; the goal is the nearest $v \in L^*$. Here the LWE samples are in Regev's continuous form, $(a, \langle a, s \rangle / q + e \bmod 1)$ with $e \leftarrow \Psi_\alpha$. For each sample $y \leftarrow D_{L,r'}$, with $L$ also the basis matrix, form

$$a = L^{-1} y \bmod q, \qquad b = \langle x, y \rangle / q \bmod 1.$$

Since $r' > \sqrt 2\, q\, \eta_\varepsilon(L)$, the vector $y \bmod qL$ is close to uniform, so $a$ is close to uniform in $\mathbb{Z}_q^n$. Write $x = v + u$ with $v \in L^*$ and $\|u\| \le d$. The number $\langle v, y \rangle$ is an integer, equal to $\langle (L^*)^{-1} v, L^{-1} y \rangle$, so $\langle v, y \rangle / q \bmod 1$ equals $\langle s, a \rangle / q \bmod 1$ for the secret $s = (L^*)^{-1} v \bmod q$. The rest, $\langle u, y \rangle / q$, is close to a Gaussian of parameter at most $\|u\| r' / q \le \alpha / \sqrt 2$; the reduction adds its own Gaussian noise so that the total error is close to $\Psi_\alpha$. So $(a, b)$ are LWE samples, the oracle returns $s$, and a standard step recovers $v$ from $v \bmod qL^*$ by repeating the method on a point closer to the lattice. The output is a classical algorithm for BDD on $L^*$ with distance $\alpha q / (\sqrt 2\, r')$, written CVP$_{L^*, d}$ in the paper.

*Quantum part (Lemma 3.14): a BDD solver on the dual gives narrower Gaussian samples.* Assume a CVP$_{L^*, d}$ oracle with $d < \lambda_1(L^*)/2$. The quantum algorithm prepares a superposition $\sum_z \rho_{d/\sqrt n}(z) |z\rangle$ over a fine grid of short offsets $z$, which have norm below $d$ with high probability. It computes $x = z \bmod L^*$ (reduction to a fundamental region) into a second register. From $x$ alone, the BDD oracle finds the nearest dual lattice point $v$, and $z = x - v$, so the algorithm can erase the first register. Erasure works because the oracle answers every point of the superposition correctly; this is the step with no known classical analog. The state that remains is a periodic Gaussian $\sum_{x} \sum_{v \in L^*} \rho_{d/\sqrt n}(x - v) |x\rangle$ over the fundamental region. Its [quantum Fourier transform](/quantum-fourier-transform/) is close to $\sum_{y \in L} \rho_{\sqrt n / d}(y) |y\rangle$, and a measurement gives a sample from $D_{L, \sqrt n / (\sqrt 2\, d)}$ (the factor $\sqrt 2$ comes from squaring the amplitudes).

With $d = \alpha q / (\sqrt 2\, r')$, the output width is $\sqrt n / (\sqrt 2\, d) = r' \sqrt n / (\alpha q)$, which is Lemma 3.3.

**Step 3: end.** Apply Step 2 for $i = 3n, 3n - 1, \ldots, 1$. Each round needs its input width to be at least about $\sqrt 2\, q\, \eta_\varepsilon(L)$, and the choice of $r$ makes this hold for every $i \ge 1$: $r_1 = r \alpha q / \sqrt n = \sqrt 2\, q\, \eta_\varepsilon(L)$, and the $r_i$ increase with $i$. The last round gives samples from $D_{L, r_0} = D_{L,r}$. The number of oracle calls and the running time are polynomial in $n$, and the errors per round are negligible, so the total error is negligible. This proves Theorem 3.1.

**Why the classical reductions avoid the quantum step.** Peikert's reduction does not iterate. With $q \ge 2^{n/2}$, the samples from Step 1 are already narrow enough relative to $q$ that one run of the classical part gives a BDD solver on $L^*$ with a large distance, and a known classical argument turns such a BDD solver into a decision procedure for GapSVP. SIVP needs short vectors of $L$ itself, which only the iteration provides, so it stays quantum. The 2013 result reduces LWE with modulus $2^{\Theta(n)}$ in dimension $k$ first to LWE with a binary secret in dimension about $k \log_2 q$ (Theorem 4.1), then switches the modulus down to $\mathrm{poly}(n)$ (Corollary 3.2), at the cost of a small increase of the error. Together with Peikert 2009 this gives hardness for polynomial $q$ in dimension $n \approx k^2$, which is the $\sqrt n$ in its Theorem 1.1.

## Consequences

- **LWE-based cryptography is sound in principle.** [Regev encryption](/regev-encryption/), and every scheme proved secure from decision-LWE, is secure unless GapSVP and SIVP with polynomial factors have efficient quantum algorithms.
- **Average case from worst case.** Every LWE instance with uniform $A$ is as hard as the worst lattice of dimension $n$. A key generator does not need special care to avoid weak instances.
- **Search and decision.** With Regev's Lemma 4.2 for prime $q \le \mathrm{poly}(n)$, and later results for other moduli (Peikert's survey, Section 4.2.2), the hardness carries over to decision-LWE, which is what encryption needs.
- **The ring and module versions** follow the same plan on ideal and module lattices (see [Ring-LWE hardness](/ring-lwe-hardness/)).

## Tightness

- **The factor is polynomial, and such problems are not NP-hard unless the hierarchy collapses.** For $\alpha = 1/\mathrm{poly}(n)$, the factor $\tilde O(n/\alpha)$ is at least $\sqrt n$. Aharonov and Regev showed that GapSVP$_{\sqrt n}$ lies in NP $\cap$ coNP, so the theorem does not make LWE NP-hard. Its value is the decades of failed attempts to solve these worst-case problems fast.
- **The width condition is needed.** For error width $\alpha q = n^{\varepsilon}$ with $\varepsilon < 1/2$, the [Arora-Ge algorithm](/arora-ge-algorithm/) solves LWE in time $2^{\tilde O(n^{2\varepsilon})}$, which is subexponential. So no reduction of this kind can hold far below $\alpha q \approx \sqrt n$ unless the worst-case problems are subexponential too.
- **No concrete parameters.** The reduction calls the oracle a polynomial number of times, loses a polynomial factor in the approximation, and goes to a different problem (SIVP or GapSVP with factor $\tilde O(n/\alpha)$) whose concrete cost is itself not known exactly. It does not tell how large $n$ must be for 128-bit security. The schemes in use also take errors far narrower than the theorem asks: ML-KEM samples errors with standard deviation about 1, a width near 2.5, while $2\sqrt n$ is about 55 for $n = 768$. Concrete parameters come from the cost of the best known attacks, in the [core-SVP](/core-svp-hardness/) model.
- **The classical forms are weaker.** Peikert's form needs an exponential modulus; the 2013 form for polynomial $q$ loses a quadratic factor in the dimension, and the authors list the removal of this loss as an open question.

## History

Regev introduced LWE and proved the quantum reduction at STOC 2005, with the journal version in 2009. Peikert gave the first classical reduction, for GapSVP with an exponential modulus, at STOC 2009. Brakerski, Langlois, Peikert, Regev and Stehlé brought the classical reduction to polynomial moduli at STOC 2013, with modulus switching and a reduction to LWE with binary secrets. Lyubashevsky, Peikert and Regev carried the quantum reduction over to ideal lattices for Ring-LWE in 2010.

## References
