---
tag: 2NTKNP
kind: problem
slug: closest-vector-problem
name: Closest vector problem
aliases:
- CVP
- bounded lattice decoding
- nearest lattice point problem
- integer least squares
area: number-theory/lattice-reduction
level: intro
summary: Given a lattice and a target point, find the lattice vector nearest to the target.
prereqs: [lattice, lattice-basis, gram-schmidt-orthogonalization]
see_also: [shortest-vector-problem, bounded-distance-decoding, babai-nearest-plane, fincke-pohst-enumeration, cvp-np-hardness, covering-radius, voronoi-cell, lattice-based-cryptography]
sources:
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1 (definitions of CVP and its variants), Chapter 2 (Babai's nearest plane algorithm), Chapter 3, Closest vector problem (NP-hardness and inapproximability), and Chapter 4 (the reduction from SVP to CVP)
  - book: isbn:9781107013926
    title: Steven D. Galbraith, Mathematics of Public Key Cryptography, Cambridge University Press, 2012
    locator: Chapter 18, Algorithms for the closest and shortest vector problems (Sections 18.1 to 18.4, nearest plane, rounding, the embedding technique and enumeration)
  - paper: "L. Babai, On Lovász' lattice reduction and the nearest lattice point problem, Combinatorica 6(1) (1986)"
    locator: pages 1 to 13 (the rounding off and nearest plane methods and their approximation factors)
  - paper: "O. Goldreich, D. Micciancio, S. Safra and J.-P. Seifert, Approximating shortest lattice vectors is not harder than approximating closest lattice vectors, Information Processing Letters 71(2) (1999)"
    locator: pages 55 to 61 (the reduction from SVP to CVP that keeps the approximation factor)
  - paper: "D. Micciancio and P. Voulgaris, A deterministic single exponential time algorithm for most lattice problems based on Voronoi cell computations, SIAM Journal on Computing 42(3) (2013)"
    locator: pages 1364 to 1391 (CVP in time 2^(2n) times a polynomial)
  - paper: "D. Aggarwal, D. Dadush and N. Stephens-Davidowitz, Solving the closest vector problem in 2^n time, the discrete Gaussian strikes again, FOCS 2015"
    locator: the main theorem (randomized exact CVP in time 2^(n + o(n)))
  - paper: "I. Dinur, G. Kindler, R. Raz and S. Safra, Approximating CVP to within almost-polynomial factors is NP-hard, Combinatorica 23(2) (2003)"
    locator: pages 205 to 243
---

The closest vector problem (CVP) asks, for a [lattice](/lattice/) given by a [basis](/lattice-basis/) and a target point $t$, for a lattice vector $v$ that minimizes the distance $\|t - v\|$. It is the lattice form of the least squares problem with integer unknowns, and of decoding a noisy point to the nearest codeword. CVP is [NP-hard](/cvp-np-hardness/) even to approximate within a factor $n^{c / \log \log n}$, and the best exact algorithms take time exponential in the dimension $n$. Polynomial-time algorithms such as [Babai's nearest plane method](/babai-nearest-plane/) give a factor $2^{O(n)}$, and the promise version [bounded distance decoding](/bounded-distance-decoding/) is the problem behind decryption in [lattice-based cryptography](/lattice-based-cryptography/).

## In plain words

Think of a grid of points that is skewed, like the corners of tiles laid at an angle. Someone gives you an arbitrary point, not on the grid. You must name the grid point nearest to it.

On a square grid the answer is easy: round each coordinate. On a skewed grid described by long, nearly parallel arrows, rounding in terms of those arrows can land far from the right point. In two or three dimensions you can draw the picture and check a few neighbours. In hundreds of dimensions the number of neighbours to check is astronomically large, and no fast method is known. This hardness protects several modern encryption schemes.

## Definition

**Notation.** The basis vectors $b_1, \ldots, b_n \in \mathbb{R}^m$ are the rows of $B$, $L = L(B) = \{x B : x \in \mathbb{Z}^n\}$, and $\|\cdot\|$ is the Euclidean norm unless a page says otherwise. For a point $t \in \mathbb{R}^m$,

$$\operatorname{dist}(t, L) = \min_{v \in L} \|t - v\|.$$

The minimum exists because only finitely many lattice points lie in any ball. For computation the entries of $B$ and $t$ are integers or rationals, and the input size is the total number of binary digits of $B$ and $t$.

**Search CVP.** *Input:* $B$ and $t$. *Output:* $v \in L(B)$ with $\|t - v\| = \operatorname{dist}(t, L)$. The answer can be returned as $v$ or as its coefficient vector $x \in \mathbb{Z}^n$. It need not be unique: for $L = \mathbb{Z}$ and $t = 1/2$ both $0$ and $1$ are closest.

If $t$ is not in $\operatorname{span}(L)$, write $t = t_\parallel + t_\perp$ with $t_\perp$ orthogonal to the span. Then $\|t - v\|^2 = \|t_\parallel - v\|^2 + \|t_\perp\|^2$ for every $v \in L$, so the problem on $t$ and on $t_\parallel$ has the same solutions. Many texts therefore assume $t \in \operatorname{span}(L)$.

## Variants

- **Optimization.** Output the number $\operatorname{dist}(t, L)$, or its square, which is rational for rational input.
- **Decision.** Given also $r > 0$, decide whether $\operatorname{dist}(t, L) \le r$. Search reduces to decision in polynomial time, so the versions are equivalent up to polynomial factors.
- **Approximate CVP ($\gamma$-CVP).** For $\gamma \ge 1$, output $v \in L$ with $\|t - v\| \le \gamma \operatorname{dist}(t, L)$.
- **GapCVP$_\gamma$.** A promise problem: given $(B, t, r)$, answer YES if $\operatorname{dist}(t, L) \le r$ and NO if $\operatorname{dist}(t, L) > \gamma r$; other inputs may get any answer. This is the version used in hardness proofs, like [GapSVP](/gap-svp/).
- **[Bounded distance decoding](/bounded-distance-decoding/) (BDD$_\alpha$).** The target is promised to satisfy $\operatorname{dist}(t, L) < \alpha \lambda_1(L)$ with $\alpha < 1/2$, so the closest vector is unique.
- **CVP with preprocessing (CVPP).** The lattice is fixed in advance and an algorithm may compute advice of polynomial size about it, without time limit; then it receives targets. CVPP is still NP-hard (Micciancio 2001; Feige and Micciancio 2004).
- **Other norms.** CVP in the $\ell_p$ norms, in particular $\ell_\infty$, has the same flavour; van Emde Boas proved NP-hardness for $\ell_\infty$ as well.
- **The shortest vector problem.** [SVP](/shortest-vector-problem/) is CVP with target $0$ in which the answer $v = 0$ is forbidden. It is no harder than CVP (see Reductions).

## Examples

**The integer grid.** For $L = \mathbb{Z}^m$ the closest vector to $t$ is obtained by rounding each coordinate: $v_k = \lceil t_k \rfloor$. For $t = (0.6, 1.4)$, $v = (1, 1)$ and $\operatorname{dist} = (0.16 + 0.16)^{1/2} \approx 0.566$.

**A good and a bad basis.** Let $L$ have the basis rows $b_1 = (2, 0)$ and $b_2 = (1, 2)$, so $\det L = 4$, and let $t = (1/2, 5/2)$.

- In this basis the coefficients of $t$ are $x = t B^{-1} = (-3/8, 5/4)$. Rounding gives $(0, 1)$, the vector $(1, 2)$, at squared distance $1/4 + 1/4 = 1/2$. A search over all coefficient vectors in a large enough box confirms that $(1, 2)$ is the closest lattice vector.
- The rows $c_1 = (4, 4) = b_1 + 2 b_2$ and $c_2 = (9, 10) = 2 b_1 + 5 b_2$ are another basis of the same lattice, since $\det \begin{pmatrix} 1 & 2 \\ 2 & 5 \end{pmatrix} = 1$. In this basis the coefficients of $t$ are $(-35/8, 2)$. Rounding gives $(-4, 2)$, the vector $-4 c_1 + 2 c_2 = (2, 4)$, at squared distance $9/4 + 9/4 = 9/2$: nine times the optimum.

This is why CVP algorithms first [reduce](/lattice-basis-reduction/) the basis.

**A non-unique answer.** For $L = \mathbb{Z}^2$ and $t = (1/2, 1/2)$, the four points $(0, 0)$, $(1, 0)$, $(0, 1)$ and $(1, 1)$ are all at distance $\sqrt{2}/2$, which is the [covering radius](/covering-radius/) of $\mathbb{Z}^2$.

## Known algorithms

Here $n$ is the rank, and costs are arithmetic operations on numbers whose size is polynomial in the input size, unless stated otherwise.

- **[Babai rounding](/babai-rounding/).** Round the coefficients of $t$ in an [LLL-reduced](/lll-reduction/) basis. Polynomial time; Babai proved the factor $1 + 2n (9/2)^{n/2}$ for LLL with $\delta = 3/4$.
- **[Babai's nearest plane](/babai-nearest-plane/).** Fix the coefficients one at a time along the [Gram-Schmidt](/gram-schmidt-orthogonalization/) directions. Polynomial time, factor $2^{n/2}$ for an LLL-reduced basis with $\delta = 3/4$. With a [BKZ-reduced](/bkz-algorithm/) basis of block size $\beta$ the factor drops to about $\beta^{O(n/\beta)}$, at a cost of $2^{O(\beta)}$ per SVP call in the block.
- **Enumeration.** [Fincke-Pohst](/fincke-pohst-enumeration/) and [Schnorr-Euchner](/schnorr-euchner-enumeration/) enumeration list the lattice points in a ball around $t$ and solve CVP exactly. On an LLL-reduced basis the time is $2^{O(n^2)}$; with Kannan's preprocessing it is $n^{O(n)}$, and Hanrot and Stehlé showed $n^{n/2 + o(n)}$ for CVP.
- **The embedding technique (Kannan).** Put $t$ as an extra row: the lattice generated by $(b_i, 0)$ and $(t, M)$ often has $(t - v, M)$ as a shortest vector when $t$ is close to $L$, so one SVP call solves the instance. This is a heuristic in general and a reduction for BDD instances with a small enough distance.
- **Voronoi cell algorithm.** Micciancio and Voulgaris solve CVP exactly and deterministically in time $2^{2n}$ times a polynomial and space $2^n$ times a polynomial, by computing the [Voronoi cell](/voronoi-cell/) of the lattice.
- **Discrete Gaussian sampling.** Aggarwal, Dadush and Stephens-Davidowitz solve CVP exactly in randomized time $2^{n + o(n)}$, the fastest proved bound known.
- **Sieving.** [Lattice sieves](/lattice-sieving/) adapted to CVP solve approximate CVP heuristically in single exponential time and memory, and they are the fastest method in practice in high dimension.

## Bounds

- **Exact CVP is NP-hard.** Van Emde Boas proved it in 1981 by a reduction from [subset sum](/subset-sum-problem/); see [NP-hardness of CVP](/cvp-np-hardness/). The decision version is in [NP](/np/): a lattice vector with its coefficients is a certificate, and its distance can be checked in exact arithmetic.
- **Hardness of approximation.** Arora, Babai, Stern and Sweedyk (1997) proved that $\gamma$-CVP is NP-hard for every constant $\gamma$, and quasi-NP-hard within $2^{\log^{1 - \varepsilon} n}$. Dinur, Kindler, Raz and Safra (2003) proved NP-hardness within $n^{c / \log \log n}$ for some constant $c > 0$, under deterministic reductions.
- **Limits of hardness.** GapCVP$_{\sqrt{n / \log n}}$ is in [NP](/np/) $\cap$ coAM (Goldreich and Goldwasser, 2000), and GapCVP$_{\sqrt n}$ is in NP $\cap$ [coNP](/co-np/) (Aharonov and Regev, 2005). So GapCVP within these factors is not NP-hard unless the polynomial hierarchy collapses (for the coAM result) or NP = coNP.
- **Fine-grained lower bounds.** Under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/), CVP in the $\ell_p$ norm has no $2^{(1 - \varepsilon) n}$-time algorithm for any $\varepsilon > 0$ when $p$ is not an even integer (Bennett, Golovnev and Stephens-Davidowitz, 2017). For the Euclidean norm only weaker conditional bounds are known.
- **Upper bounds.** Exact CVP is solvable in randomized time $2^{n + o(n)}$ and deterministic time $2^{2n + o(n)}$ (see above).

## Reductions

- **SVP to CVP, keeping the factor.** Goldreich, Micciancio, Safra and Seifert (1999). For $i = 1, \ldots, n$, let $B^{(i)}$ be $B$ with $b_i$ replaced by $2 b_i$, and let $v_i$ be a $\gamma$-approximate closest vector to $b_i$ in $L(B^{(i)})$. Output the shortest of the vectors $b_i - v_i$.

  *Proof.* Each $b_i - v_i$ is in $L$, and it is nonzero, because its coefficient on $b_i$ is odd. Let $s = \sum_j c_j b_j$ be a shortest nonzero vector of $L$. Not all $c_j$ are even, since otherwise $s/2$ would be a shorter nonzero lattice vector. Take $i$ with $c_i$ odd. Then $b_i - s = (1 - c_i) b_i - \sum_{j \ne i} c_j b_j$ has an even coefficient on $b_i$, so $b_i - s \in L(B^{(i)})$ and $\operatorname{dist}(b_i, L(B^{(i)})) \le \|s\|$. Hence $\|b_i - v_i\| \le \gamma \lambda_1(L)$. The reduction makes $n$ calls, so $\gamma$-SVP is no harder than $\gamma$-CVP. $\square$
- **CVP to SVP.** No reduction that keeps the factor is known. The embedding technique above reduces BDD to the [unique SVP](/unique-svp/) problem (Lyubashevsky and Micciancio, 2009), and Kannan showed that CVP reduces to SVP if one accepts a loss in the approximation factor.
- **Subset sum to CVP.** The NP-hardness proof maps a subset sum instance $(a_1, \ldots, a_n, s)$ to a lattice and a target such that a solution of the subset sum gives a lattice vector at a known small distance; see [NP-hardness of CVP](/cvp-np-hardness/).
- **Search to decision.** With a decision oracle, one can find the coefficients of a closest vector one bit at a time on a shrinking chain of lattices, in polynomially many calls.

## Applications

- **Decryption and attacks in lattice cryptography.** Decrypting a [learning with errors](/learning-with-errors/) ciphertext, or attacking it with a reduced basis, is a BDD instance. The [GPV signature](/gpv-signature/) signs by sampling a lattice vector near a hash target with a secret short basis.
- **Communications.** Maximum likelihood detection for multiple-antenna channels and lattice codes is CVP; the "sphere decoder" used there is [Fincke-Pohst enumeration](/fincke-pohst-enumeration/).
- **Integer least squares.** Resolving the integer ambiguities of carrier-phase satellite positioning is CVP in the norm of a covariance matrix.
- **Cryptanalysis.** Recovering a secret from approximations of it, as in the hidden number problem and attacks on DSA with partly known nonces, is solved by nearest plane or embedding on a reduced basis.
- **Integer programming in fixed dimension.** [Lenstra's algorithm](/lenstra-algorithm/) uses reduced bases and nearest-point steps to decide integer feasibility in polynomial time for fixed $n$.

## References
