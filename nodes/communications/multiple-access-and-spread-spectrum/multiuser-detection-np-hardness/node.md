---
tag: SQ5MB1
kind: theorem
slug: multiuser-detection-np-hardness
name: NP-hardness of optimum multiuser detection
aliases:
- Verdu complexity theorem
area: communications/multiple-access-and-spread-spectrum
level: advanced
summary: "Finding the jointly most likely bits of K synchronous CDMA users from their matched filter outputs is NP-hard in K, as Verdú showed in 1989."
prereqs: [optimum-multiuser-detector, maximum-cut, np-hard]
see_also: [optimum-multiuser-detector, maximum-cut, polynomial-time-reduction, np-complete, semidefinite-relaxation-detection, mimo-detection, fincke-pohst-enumeration, decorrelating-detector]
sources:
  - paper: doi:10.1007/BF01553893
    title: "Sergio Verdú, Computational complexity of optimum multiuser detection, Algorithmica 4, 1989"
    locator: "the statement that optimum multiuser detection for synchronous CDMA is NP-hard in the number of users"
  - book: isbn:9780716710455
    title: "Michael R. Garey and David S. Johnson, Computers and Intractability: A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979"
    locator: "Appendix A2.2, problem ND16, Max Cut"
  - paper: doi:10.1109/18.705573
    title: "C. Sankaran and Anthony Ephremides, Solving a class of optimum multiuser detection problems with polynomial complexity, IEEE Transactions on Information Theory 44(5), 1998"
    locator: "pp. 1958 to 1961 (the case of nonpositive crosscorrelations, solved as a minimum cut problem)"
  - book: isbn:9780521593731
    title: "Sergio Verdú, Multiuser Detection, Cambridge University Press, 1998"
    locator: "Chapter 4, Optimum multiuser detection"
---

The [optimum multiuser detector](/optimum-multiuser-detector/) chooses the bits of all $K$ users that best explain the received signal. Verdú showed in 1989 that this choice is NP-hard in $K$: unless P equals NP, no algorithm finds it in time polynomial in the number of users for every set of crosscorrelations. The reason is that the likelihood is a quadratic function of $K$ binary variables, and every such function with a positive definite matrix can occur. This page proves the result by a reduction from [maximum cut](/maximum-cut/), a standard argument for this kind of problem, and does not claim to follow the steps of Verdú's paper. The theorem explains why the field built cheaper detectors, such as the [decorrelator](/decorrelating-detector/), and why the exponential cost of the optimum detector is in $K$ and not in the length of the message.

## Statement

There are $K$ synchronous users with unit-norm signatures $s_1, \ldots, s_K$, amplitudes $A_1, \ldots, A_K > 0$ and bits $b \in \{-1, +1\}^K$. The receiver sees $y = S A b + w$ with white Gaussian noise $w$, and the matched filter outputs $z = S^\top y$ are a sufficient statistic. Let $R = S^\top S$ and $A = \mathrm{diag}(A_k)$. The maximum likelihood decision maximizes

$$\Omega(b) = 2\, b^\top A z - b^\top A R A b.$$

**Decision problem (MUD).** Given a rational symmetric positive definite $K \times K$ matrix $R$ with unit diagonal, rational amplitudes $A_k > 0$, a rational vector $z$ and a rational threshold $t$, is there a $b \in \{-1, +1\}^K$ with $\Omega(b) \ge t$?

**Theorem.** MUD is NP-complete. So finding a maximizer of $\Omega$ is NP-hard, measured in $K$.

Every such $R$ is the crosscorrelation matrix of real unit-norm signatures with $N = K$ chips, for example the columns of its Cholesky factor, so the hard inputs are real CDMA systems.

## In plain words

The best detector has to try combinations of the users' bits, and the number of combinations doubles with each new user. This theorem says that, in the worst case, there is no clever way around that. If someone found a fast method for the best detector that works for every set of codes, the same method would also solve a famous hard graph problem quickly, and with it a large family of other hard problems. Most researchers believe that is impossible. So for many users, receivers use simpler detectors that are good but not always the best.

## Proof

**MUD is in NP.** A certificate is a vector $b$. Computing $\Omega(b)$ takes $O(K^2)$ rational operations on numbers of polynomial size, and comparing with $t$ is easy.

**Reduction.** MAX-CUT asks, for a graph on vertices $1, \ldots, K$ with nonnegative integer weights $w_{ij} = w_{ji}$ and an integer $c$, whether some split of the vertices into two sides cuts edges of total weight at least $c$. It is NP-complete (Garey and Johnson, ND16). Given such an instance, let $W$ be the weight matrix with zero diagonal, and let

$$D = 1 + \max_i \sum_j w_{ij}, \qquad R = I + \frac{1}{D} W, \qquad A = I, \qquad z = 0.$$

**$R$ is a valid input.** It is rational and symmetric with unit diagonal. Each row has off-diagonal sum $\sum_j w_{ij} / D < 1$, so $R$ is strictly diagonally dominant with a positive diagonal. By the Gershgorin circle theorem, every eigenvalue is greater than 0, so $R$ is positive definite.

**The objective is the cut.** Encode a split by $b_i = +1$ on one side and $b_i = -1$ on the other. An edge $\{i, j\}$ is cut when $b_i b_j = -1$, so

$$\mathrm{cut}(b) = \sum_{i < j} w_{ij} \frac{1 - b_i b_j}{2} = \frac{1}{2} \sum_{i < j} w_{ij} - \frac{1}{4} b^\top W b.$$

With $A = I$ and $z = 0$,

$$\Omega(b) = -b^\top R b = -K - \frac{1}{D}\, b^\top W b = -K - \frac{1}{D} \Big( 2 \sum_{i < j} w_{ij} - 4\, \mathrm{cut}(b) \Big).$$

So $\Omega(b)$ is an increasing affine function of $\mathrm{cut}(b)$. Set

$$t = -K - \frac{1}{D} \Big( 2 \sum_{i < j} w_{ij} - 4c \Big).$$

Then $\Omega(b) \ge t$ if and only if $\mathrm{cut}(b) \ge c$, so the MUD instance is a yes instance exactly when the MAX-CUT instance is. All numbers have size polynomial in the input, and the map takes $O(K^2)$ arithmetic steps. Hence MUD is NP-hard, and with the first part, NP-complete. A maximizer of $\Omega$ gives a maximum cut, so the search problem is NP-hard too. $\square$

**Example.** The triangle with unit weights has $D = 3$, and $R$ has $1/3$ in every off-diagonal entry. If all three bits are equal, $b^\top R b = 3 + 2 = 5$ and the cut is 0. If one bit differs, $b^\top R b = 3 - 2/3 = 7/3$ and the cut is 2. The largest $\Omega$ is $-7/3$, at the maximum cut.

## Consequences

- **No fast optimum detector for all codes.** Unless P equals NP, no algorithm runs in time polynomial in $K$ and returns the maximum likelihood bits for every $R$. The $O(2^K)$ per bit of the [optimum detector](/optimum-multiuser-detector/) cannot be reduced to a polynomial in general.
- **Suboptimal detectors.** The result is the main reason for linear detectors and cancellation methods: the [decorrelator](/decorrelating-detector/), the [MMSE detector](/mmse-multiuser-detector/), [successive](/successive-interference-cancellation/) and [parallel](/parallel-interference-cancellation/) interference cancellation, all polynomial in $K$.
- **Relaxations and search.** Since the problem contains maximum cut, the methods for maximum cut apply. [Semidefinite relaxation](/semidefinite-relaxation-detection/) relaxes the bits to a positive semidefinite matrix. Enumeration methods such as [Fincke-Pohst](/fincke-pohst-enumeration/) search a sphere and are exact, with a running time that is exponential in the worst case.
- **MIMO detection.** Maximum likelihood detection of a binary vector through a real matrix channel has the same form, so the same reduction shows that [MIMO detection](/mimo-detection/) is NP-hard in the number of transmit antennas.

## Tightness

- **Fixed number of users.** For each fixed $K$, the problem is easy: trying all $2^K$ vectors costs $O(2^K K^2)$, and the Viterbi form of the optimum detector handles asynchronous frames of any length in time linear in the frame length. The hardness is in $K$ only.
- **Special crosscorrelations.** When every crosscorrelation is nonpositive, $R_{ij} \le 0$ for $i \ne j$, maximizing $\Omega$ becomes a minimum cut problem and is solvable in polynomial time (Sankaran and Ephremides). The reduction above needs positive crosscorrelations, which is consistent with this.
- **Worst case only.** The theorem is about the worst choice of $R$ and $z$. It says nothing about the average over the noise, and many practical systems with small correlations are solved well by suboptimal detectors.
- **Signature alphabet.** The proof uses real signatures. It does not show that the problem stays NP-hard when the chips must be $\pm 1/\sqrt N$, as in most practical systems, and this page does not settle that case.

## History

Verdú derived the optimum multiuser detector for asynchronous Gaussian CDMA in 1983 and 1986 and found that its cost grows as $2^K$. In a paper in Algorithmica in 1989, he showed that this growth is not a weakness of his algorithm: optimum multiuser detection is NP-hard in the number of users. The result moved the research of the late 1980s and the 1990s toward linear and decision-driven detectors with polynomial cost. In 1998 Sankaran and Ephremides identified a class of crosscorrelation matrices for which the problem is a minimum cut problem and is solvable in polynomial time.

## References
