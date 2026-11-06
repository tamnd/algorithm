---
tag: F2T6WS
kind: problem
slug: gap-svp
name: GapSVP
aliases:
- gap shortest vector problem
- GapSVP_gamma
- decisional approximate SVP
area: number-theory/lattice-reduction
level: advanced
summary: Decide whether lambda_1 is below one threshold or above gamma times that threshold.
prereqs: [shortest-vector-problem, approximate-svp]
see_also: [dual-lattice, svp-randomized-np-hardness, co-np, learning-with-errors, unique-svp, bounded-distance-decoding, ajtai-worst-case-to-average-case-reduction, closest-vector-problem]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1 (promise problems GapSVP and GapCVP), Chapter 4 (hardness of GapSVP) and Chapter 9, Interactive proof systems (GapSVP in coAM)
  - paper: "D. Aharonov and O. Regev, Lattice problems in NP intersect coNP, Journal of the ACM 52(5) (2005)"
    locator: pages 749 to 765 (GapSVP and GapCVP with factor sqrt(n) are in coNP)
  - paper: "O. Goldreich and S. Goldwasser, On the limits of nonapproximability of lattice problems, Journal of Computer and System Sciences 60(3) (2000)"
    locator: pages 540 to 563 (GapSVP and GapCVP with factor sqrt(n / log n) are in coAM)
  - paper: "O. Regev, On lattices, learning with errors, random linear codes, and cryptography, Journal of the ACM 56(6) (2009)"
    locator: the main theorem (a quantum reduction from worst-case GapSVP and SIVP to LWE)
---

GapSVP$_\gamma$ is the decision version of the [approximate shortest vector problem](/approximate-svp/): given a basis of a [lattice](/lattice/) $L$ and a number $r$, answer YES if $\lambda_1(L) \le r$ and NO if $\lambda_1(L) > \gamma r$. When $\lambda_1$ lies in the gap between $r$ and $\gamma r$, any answer is accepted. It is the form in which the hardness of lattice problems is usually proved, both NP-hardness for small $\gamma$ and the worst-case assumptions behind [learning with errors](/learning-with-errors/) for polynomial $\gamma$.

## In plain words

Instead of asking for a short step in a grid, ask a yes-or-no question: is there a step shorter than a given length? To make the question easier, add slack. You must say yes when a step shorter than the length exists, and no when even the given length times the slack has no step. If the truth lies in between, either answer counts.

A wider slack makes the question easier. With a huge slack a quick tidying of the grid answers it. With a slack of about the square root of the number of dimensions, there are short proofs for both answers, which makes it unlikely that the question is among the hardest problems in its class. With a slack close to one it is as hard as the hardest of them.

## Definition

Notation is that of the other pages in this area: basis rows $b_1, \ldots, b_n$, $L = L(B)$ of rank $n$, first minimum $\lambda_1(L)$, [dual lattice](/dual-lattice/) $L^\times$.

**GapSVP$_\gamma$.** A promise problem with factor $\gamma = \gamma(n) \ge 1$. An instance is a pair $(B, r)$ with $B$ a rational basis and $r > 0$ rational.

- YES instances: $\lambda_1(L(B)) \le r$.
- NO instances: $\lambda_1(L(B)) > \gamma r$.

An algorithm solves GapSVP$_\gamma$ if it answers correctly on every YES and every NO instance; on other instances it may answer anything. For $\gamma = 1$ the gap is empty and the problem is the exact decision version of the [shortest vector problem](/shortest-vector-problem/).

Many authors use $\lambda_1 \le 1$ against $\lambda_1 > \gamma$ after scaling, or squared lengths so that all data stay rational.

## Variants

- **GapCVP$_\gamma$.** Given $(B, t, r)$, decide $\operatorname{dist}(t, L) \le r$ against $\operatorname{dist}(t, L) > \gamma r$; the decision form of the [closest vector problem](/closest-vector-problem/).
- **GapSVP in other norms.** In $\ell_\infty$, van Emde Boas proved the exact problem NP-hard under deterministic reductions.
- **Decisional unique SVP.** The YES and NO cases are restricted further by a gap between $\lambda_1$ and $\lambda_2$; see [unique SVP](/unique-svp/).
- **GapSVP with the Hermite normalization.** Compare $\lambda_1$ with $\det(L)^{1/n}$ instead of a given $r$; this is HSVP in decision form.
- **Average-case versions.** Distinguishing a lattice with a planted short vector from a random one is the decision form of LWE and NTRU problems.

## Examples

- **The promise.** The lattice with rows $(2, 0)$ and $(1, 2)$ has $\lambda_1 = 2$. Take $\gamma = 2$. The instance $r = 2$ is a YES instance. The instance $r = 0.9$ is a NO instance, since $2 > 1.8$. The instance $r = 1$ is neither: $\lambda_1 = 2$ is not more than $\gamma r = 2$, so it lies in the gap and either answer is correct.
- **A YES certificate.** A nonzero lattice vector of length at most $r$, given by its integer coefficients, proves a YES instance. So GapSVP$_\gamma$ is in NP for every $\gamma \ge 1$.
- **A NO certificate for $\gamma = n$.** If $\lambda_1(L) > n r$, then by Banaszczyk's transference theorem $\lambda_n(L^\times) \le n / \lambda_1(L) < 1/r$, so there are $n$ independent dual vectors of length less than $1/r$. Conversely, given $n$ independent dual vectors $y_1, \ldots, y_n$ of length less than $1/r$: every $v \in L \setminus \{0\}$ has a nonzero integer product with some $y_j$, so $1 \le |\langle v, y_j \rangle| \le \|v\| \|y_j\| < \|v\| / r$, and $\lambda_1(L) > r$. The certificate can be checked in polynomial time, so GapSVP$_n$ is in NP $\cap$ [coNP](/co-np/). Aharonov and Regev improved the factor to $\sqrt n$ with a certificate built from the Gaussian function on the dual.
- **Answering with a reduced basis.** For $L$ given by $(4, 4), (9, 10)$ and $r = 0.9$, $\gamma = 2$: [Lagrange-Gauss reduction](/lagrange-gauss-reduction/) returns $(2, 0)$, of length $2 > \gamma r = 1.8$, so the answer is NO, which is correct.

## Known algorithms

- **From search to decision.** Any algorithm for $\gamma$-SVP solves GapSVP$_\gamma$: compute $v \ne 0$ with $\|v\| \le \gamma \lambda_1$, and answer YES if and only if $\|v\| \le \gamma r$. On a YES instance $\|v\| \le \gamma \lambda_1 \le \gamma r$; on a NO instance $\|v\| \ge \lambda_1 > \gamma r$. So [LLL](/lll-algorithm/) solves GapSVP$_{2^{(n-1)/2}}$ in polynomial time, and [BKZ](/bkz-algorithm/) and slide reduction trade time for smaller factors as described on the [approximate SVP](/approximate-svp/) page.
- **Exact algorithms.** [Enumeration](/lattice-enumeration/) in time $n^{n/(2e) + o(n)}$ and sieving in time $2^{O(n)}$ solve the exact problem; the best proved single exponential algorithms run in time $2^{n + o(n)}$.
- **Lower bounds from Gram-Schmidt.** For any basis, $\lambda_1 \ge \min_i \|b_i^*\|$. After LLL, $\min_i \|b_i^*\| \ge 2^{-(n-1)/2} \|b_1\| \ge 2^{-(n-1)/2} \lambda_1$, so on a NO instance with $\gamma \ge 2^{(n-1)/2}$ this lower bound already exceeds $r$ and certifies the answer.

## Bounds

All hardness results below are for the $\ell_2$ norm and use randomized reductions.

- **Exact.** GapSVP$_1$ is NP-hard (Ajtai, 1998; see [SVP NP-hardness](/svp-randomized-np-hardness/)).
- **Constant factors.** GapSVP$_\gamma$ is NP-hard for every $\gamma < \sqrt 2$ (Micciancio, 2001) and for every constant $\gamma$ (Khot, 2005).
- **Almost polynomial factors.** GapSVP$_\gamma$ with $\gamma = 2^{(\log n)^{1 - \varepsilon}}$ is not in randomized polynomial time unless NP is in randomized quasi-polynomial time (Haviv and Regev, 2012).
- **Upper limits.** GapSVP$_{\sqrt{n / \log n}}$ is in NP $\cap$ coAM (Goldreich and Goldwasser, 2000), and GapSVP$_{\sqrt n}$ is in NP $\cap$ coNP (Aharonov and Regev, 2005). If GapSVP were NP-hard for these factors, the [polynomial hierarchy](/polynomial-hierarchy/) would collapse.
- **Cryptographic factors.** For $\gamma = \operatorname{poly}(n)$ larger than $\sqrt n$, no NP-hardness is expected and no algorithm faster than $2^{\Theta(n)}$ is known. This is the regime of [worst-case to average-case reductions](/ajtai-worst-case-to-average-case-reduction/).

## Reductions

- **GapSVP$_\gamma$ to GapCVP$_\gamma$.** The reduction of Goldreich, Micciancio, Safra and Seifert, with the same factor and rank.
- **GapSVP to SIVP.** By transference, an SIVP$_\gamma$ oracle on $L^\times$ solves GapSVP$_{n\gamma}$ on $L$.
- **To LWE.** Regev (2005) gave a quantum reduction from worst-case GapSVP$_\gamma$ and SIVP$_\gamma$ with $\gamma = \tilde O(n / \alpha)$ to [LWE](/learning-with-errors/) with error rate $\alpha$. Peikert (2009) made the reduction from GapSVP classical, at first with an exponential modulus; Brakerski, Langlois, Peikert, Regev and Stehlé (2013) brought the modulus down to polynomial.
- **To SIS.** Ajtai's reduction and its refinements map worst-case GapSVP and SIVP with polynomial factors to the average-case [SIS](/short-integer-solution/) problem.
- **uSVP, BDD and GapSVP.** Lyubashevsky and Micciancio (2009) showed that [unique SVP](/unique-svp/) and [BDD](/bounded-distance-decoding/) are equivalent up to a factor about 2 in the parameters, and reduced GapSVP, with a factor larger by about $\sqrt{n / \log n}$, to both.

## Applications

- **Hardness assumptions.** The security of LWE-based encryption, signatures and fully homomorphic encryption is stated as the worst-case hardness of GapSVP$_\gamma$ or SIVP$_\gamma$ for a polynomial $\gamma$.
- **Proof systems.** The coAM protocol of Goldreich and Goldwasser is a statistical zero-knowledge proof that a lattice has no short vector; it is a standard example of a natural problem in SZK.
- **Limits of hardness.** The NP $\cap$ coNP result is the main reason to believe that lattice cryptography with polynomial factors does not rest on NP-hard problems.

## References
