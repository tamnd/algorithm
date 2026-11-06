---
tag: 7YAXKD
kind: problem
slug: bounded-distance-decoding
name: Bounded distance decoding
aliases:
- BDD
- BDD problem
- Bounded distance decoding problem
- Bounded-distance decoding
- bounded distance decoding
- unique decoding
- BDD_alpha
area: number-theory/lattice-reduction
level: advanced
summary: CVP promised that the target is within a small distance of the lattice.
prereqs: [closest-vector-problem, shortest-vector-problem]
see_also: [babai-nearest-plane, babai-rounding, unique-svp, learning-with-errors, gap-svp, covering-radius, fincke-pohst-enumeration, lattice-based-cryptography]
sources:
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 18, Sections 18.1 to 18.3 (nearest plane, rounding and the embedding technique for targets close to the lattice)
  - paper: "Y.-K. Liu, V. Lyubashevsky and D. Micciancio, On bounded distance decoding for general lattices, APPROX-RANDOM 2006, LNCS 4110"
    locator: NP-hardness of BDD for alpha above 1/sqrt(2), and the version with preprocessing
  - paper: "V. Lyubashevsky and D. Micciancio, On bounded distance decoding, unique shortest vectors, and the minimum distance problem, CRYPTO 2009, LNCS 5677"
    locator: the reductions between BDD, unique SVP and GapSVP
  - paper: "O. Regev, On lattices, learning with errors, random linear codes, and cryptography, Journal of the ACM 56(6) (2009)"
    locator: LWE as an average-case BDD problem on q-ary lattices, and the use of a BDD oracle in the reduction
---

Bounded distance decoding $\text{BDD}_\alpha$ is the [closest vector problem](/closest-vector-problem/) with a promise: the target $t$ is within distance $\alpha \lambda_1(L)$ of the [lattice](/lattice/), and the task is to find the lattice vector that close to it. For $\alpha < 1/2$ that vector is unique, so BDD is the lattice analogue of unique decoding of an error-correcting code. Decryption in [lattice-based cryptography](/lattice-based-cryptography/) is BDD with a good basis, and [learning with errors](/learning-with-errors/) is BDD on a random lattice without one.

## In plain words

A message is sent as a grid point, and the channel adds a little noise, so the receiver gets a point near the grid but not on it. The noise is smaller than a quarter of the gap between grid points. The receiver must find the grid point that was sent.

Because the noise is small, there is only one grid point close enough, so the answer is well defined. Finding it is easy when the receiver knows a tidy description of the grid: round off and read the answer. With only a skewed description, the same rounding lands on a wrong point, and fixing that is as hard as other hard grid problems. This gap between the tidy and the skewed description is what lattice encryption uses: the tidy one is the secret key.

## Definition

Notation is that of the other pages in this area: basis rows $b_1, \ldots, b_n$, $L = L(B)$ of rank $n$, Gram-Schmidt vectors $b_i^*$, first minimum $\lambda_1$, and $\operatorname{dist}(t, L) = \min_{v \in L} \|t - v\|$.

**$\text{BDD}_\alpha$.** For a function $\alpha = \alpha(n) > 0$:

- Input: a basis $B$ and a target $t \in \operatorname{span}(L)$ with $\operatorname{dist}(t, L) \le \alpha \lambda_1(L)$.
- Output: a vector $v \in L$ with $\|t - v\| \le \alpha \lambda_1(L)$.

Inputs that violate the promise may get any answer. The parameter $\alpha$ is the relative decoding distance; a smaller $\alpha$ is an easier problem.

**Uniqueness.** If $\alpha < \tfrac12$, the answer is unique. Two lattice vectors $v \ne v'$ within $\alpha \lambda_1$ of $t$ would satisfy $\|v - v'\| \le 2 \alpha \lambda_1 < \lambda_1$, which is impossible for a nonzero lattice vector. For $\alpha \ge \tfrac12$ several answers can exist and the problem is a form of list decoding.

**Absolute version.** Some authors give a radius $d$ with $d < \lambda_1/2$ instead of $\alpha$, so that the promise is $\operatorname{dist}(t, L) \le d$.

## Variants

- **BDD with preprocessing (BDDP).** The lattice is fixed in advance and arbitrary polynomial-size advice about it may be computed without time limit; then targets arrive. This models decryption with a precomputed trapdoor.
- **Search LWE.** Given $A \in \mathbb{Z}_q^{m \times k}$ and $b = A s + e \bmod q$ with a short random $e$, find $s$. It is BDD on the q-ary lattice $\Lambda_q(A) = \{A z + q w\}$ with target $b$, averaged over random $A$ and Gaussian $e$, where the error is typically much shorter than $\lambda_1$.
- **Decision BDD.** Distinguish a target close to the lattice from a uniformly random one; decision LWE is its average-case form.
- **Other norms.** BDD in $\ell_p$ norms, and BDD for lattices from codes (Construction A), where it connects to decoding of linear codes.
- **Gap version.** GapCVP$'$ restricts CVP by both a distance promise and a gap; it sits between BDD and GapCVP.

## Examples

Take the lattice with rows $(2, 0)$ and $(1, 2)$, so $\lambda_1 = 2$, and $\alpha = \tfrac14$, so the promise radius is $\tfrac12$.

- **A good basis decodes.** The target $t = (0.7, 2.3)$ is at distance $\sqrt{0.18} \approx 0.424 \le 0.5$ from $(1, 2)$, so it satisfies the promise. With the basis $(2, 0), (1, 2)$, whose Gram-Schmidt vectors are $(2, 0)$ and $(0, 2)$, [Babai's nearest plane method](/babai-nearest-plane/) computes the coefficient $2.3/2 = 1.15$, rounds it to 1, subtracts $(1, 2)$, then computes $-0.3/2 = -0.15$ and rounds it to 0. It returns $(1, 2)$, the right answer.
- **A bad basis fails.** The basis $(4, 4), (9, 10)$ generates the same lattice. Its Gram-Schmidt vectors are $(4, 4)$ and $(-\tfrac12, \tfrac12)$, with squared lengths $32$ and $\tfrac12$. Nearest plane computes the coefficient $\tfrac85$ along the short vector $(-\tfrac12, \tfrac12)$ and rounds it to 2, and then $-\tfrac{35}{8}$, which it rounds to $-4$. It returns $(2, 4)$, at squared distance $4.58$ from $t$. The error $(-0.3, 0.3)$ points along the very short Gram-Schmidt vector, so the method guesses the wrong line.
- **Unique answer.** Since $\alpha = \tfrac14 < \tfrac12$, no other lattice vector is within $\tfrac12$ of $t$. The next closest is $(-1, 2)$, at distance $\sqrt{2.98} \approx 1.73$.

## Known algorithms

All methods below take a basis with rational entries and use exact arithmetic, or floating point of proved sufficient precision.

- **Nearest plane.** [Babai's nearest plane method](/babai-nearest-plane/) returns the unique answer whenever $\operatorname{dist}(t, L) < \tfrac12 \min_i \|b_i^*\|$. After [LLL](/lll-algorithm/) with $\delta = 3/4$, $\min_i \|b_i^*\| \ge 2^{-(n-1)/2} \lambda_1$, so LLL plus nearest plane solves $\text{BDD}_\alpha$ for $\alpha < 2^{-(n+1)/2}$ in polynomial time. Stronger reduction, such as [BKZ](/bkz-algorithm/), makes $\min_i \|b_i^*\|$ larger and $\alpha$ larger.
- **Rounding.** [Babai rounding](/babai-rounding/) decodes when $\operatorname{dist}(t, L) \cdot \|d_i\| < \tfrac12$ for every row $d_i$ of the [dual basis](/dual-lattice/); it is faster and easier to run in parallel, with a smaller radius.
- **Embedding.** Kannan's embedding puts $t$ as an extra basis vector $(t, M)$; when $t$ is close to $L$, the vector $(t - v, M)$ is an unusually short vector of the new lattice, found by [unique SVP](/unique-svp/) methods. This is the main attack on LWE in practice.
- **Enumeration and sieving.** [Fincke-Pohst enumeration](/fincke-pohst-enumeration/) with radius $\alpha \lambda_1$ solves BDD exactly; its cost is much lower than for full CVP because the radius is small. Sieving with preprocessing is used for batches of targets.
- **With preprocessing.** The algorithm of Aharonov and Regev, as analysed by Liu, Lyubashevsky and Micciancio, solves BDDP for $\alpha = O(\sqrt{\log n / n})$ in polynomial time.

## Bounds

- **NP-hardness.** Liu, Lyubashevsky and Micciancio proved that $\text{BDD}_\alpha$ is NP-hard under randomized reductions for $\alpha > 1/\sqrt 2$, and gave a hardness result for the version with preprocessing at a larger $\alpha$. For $\alpha < 1/2$, the regime of unique decoding, no NP-hardness is known for small $\alpha$.
- **Average case.** LWE with polynomial modulus and Gaussian error of width $\alpha q$ is as hard as worst-case GapSVP and SIVP with factor $\tilde O(n / \alpha)$, quantumly (Regev) and, for GapSVP, classically (Peikert; Brakerski and coauthors).

## Reductions

- **BDD and unique SVP.** Lyubashevsky and Micciancio (2009) showed $\text{BDD}_{1/(2\gamma)} \le \text{uSVP}_\gamma \le \text{BDD}_{1/\gamma}$, up to small polynomial factors, through the embedding technique.
- **GapSVP to BDD.** GapSVP with a factor larger by about $\sqrt{n / \log n}$ reduces to BDD (Lyubashevsky and Micciancio; Peikert).
- **BDD to CVP.** Trivial: a CVP algorithm solves BDD. The converse fails: CVP allows targets as far as the [covering radius](/covering-radius/), which is at least $\lambda_n/2$.
- **Inside Regev's reduction.** A BDD oracle on $L^\times$ is used with a quantum step to sample discrete Gaussians on $L$ of smaller width, which gives the worst-case to average-case link for LWE.

## Applications

- **Decryption.** In the GGH, LWE and Regev cryptosystems, a ciphertext is a lattice point plus a short error, and the secret key is a short basis (a trapdoor) that decodes it by rounding or nearest plane. Security is the hardness of BDD without the trapdoor.
- **Communication.** Decoding lattice codes and MIMO detection are BDD problems in practice; sphere decoding is Fincke-Pohst enumeration in a small radius.
- **Cryptanalysis.** The primal attack on LWE and NTRU is BDD through embedding, and the cost estimates use BKZ with the [Gaussian heuristic](/gaussian-heuristic/).
- **Number theory.** Some instances of the hidden number problem and of attacks on DSA with partially known nonces are BDD on structured lattices.

## References
