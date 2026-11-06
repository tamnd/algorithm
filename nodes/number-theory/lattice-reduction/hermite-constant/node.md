---
tag: FJA1C5
kind: concept
slug: hermite-constant
name: Hermite constant
aliases:
- Hermite's constant
- gamma_n
area: number-theory/lattice-reduction
level: advanced
summary: Largest possible squared first minimum of a lattice normalized by its determinant, per dimension.
prereqs: [lattice, lattice-determinant, successive-minima]
see_also: [minkowski-theorem, gaussian-heuristic, root-hermite-factor, lll-approximation-guarantee, bkz-algorithm, hkz-reduction, lagrange-gauss-reduction, shortest-vector-problem]
sources:
  - book: isbn:9783642261640
    title: Phong Q. Nguyen and Brigitte Vallée (editors), The LLL Algorithm, Survey and Applications, Springer, 2010
    locator: Chapter 2, Phong Q. Nguyen, Hermite's constant and lattice algorithms (definition, known values, Hermite's and Mordell's inequalities, and their algorithmic versions)
  - book: isbn:9780387985855
    title: J. H. Conway and N. J. A. Sloane, Sphere Packings, Lattices and Groups, third edition, Springer, 1999
    locator: Chapter 1, Sphere packing and kissing numbers (the densest lattice packings, the centre density and the known optimal lattices)
  - paper: "H. Cohn and A. Kumar, Optimality and uniqueness of the Leech lattice among lattices, Annals of Mathematics 170(3) (2009)"
    locator: pages 1003 to 1050 (the value gamma_24 = 4)
  - book: isbn:9780792376880
    title: Daniele Micciancio and Shafi Goldwasser, Complexity of Lattice Problems, A Cryptographic Perspective, Kluwer, 2002
    locator: Chapter 1, Basics (Minkowski's first theorem and the resulting bound on the Hermite constant)
---

The Hermite constant $\gamma_n$ is the largest value of $\lambda_1(L)^2 / \det(L)^{2/n}$ over all [lattices](/lattice/) $L$ of rank $n$. It says how long the shortest vector of a lattice can be, relative to the volume. It grows linearly in $n$, its exact value is known only for $n \le 8$ and $n = 24$, and the approximation factors of reduction algorithms such as [LLL](/lll-algorithm/) and [BKZ](/bkz-algorithm/) are algorithmic versions of the classical bounds on it.

## In plain words

Take a grid of points in some number of dimensions and fix how much space each point occupies. The grid always has some point close to the centre point. The question is how far away the nearest one can be pushed if you design the grid as cleverly as possible.

The Hermite constant is the answer, one number per dimension. Spreading the neighbours far apart is the same as packing balls tightly, so the best grids are the best ball packings: the honeycomb in the plane, the stack of oranges in space, and special grids in 8 and 24 dimensions.

The constant matters for computation because it says what "short" means. An algorithm that finds a vector close to the best possible length for every grid has done as well as the geometry allows, and the classic proofs about the constant turn into algorithms.

## The idea

Notation is that of the other pages in this area: a lattice $L = L(B)$ of rank $n$ with basis rows $b_1, \ldots, b_n$, first minimum $\lambda_1(L)$, and [determinant](/lattice-determinant/) $\det(L)$.

**Definition.**

$$\gamma_n = \sup_{L \text{ of rank } n} \frac{\lambda_1(L)^2}{\det(L)^{2/n}}.$$

The ratio does not change when $L$ is scaled or rotated, and the supremum is a maximum, reached by some lattice. So $\lambda_1(L) \le \sqrt{\gamma_n}\, \det(L)^{1/n}$ for every rank-$n$ lattice, and the bound is tight. Some authors call $\sqrt{\gamma_n}$ the Hermite constant; this site uses $\gamma_n$, the convention of Conway and Sloane and of Nguyen.

**Packing form.** Balls of radius $\lambda_1/2$ around the lattice points do not overlap. Their density is $V_n (\lambda_1/2)^n / \det(L)$, with $V_n$ the volume of the unit ball, so maximizing $\gamma_n$ is the same as finding the densest lattice packing of balls in dimension $n$: the largest density is $V_n \gamma_n^{n/2} / 2^n$.

**Hermite's inequality.** $\gamma_n \le \gamma_2^{\,n-1} = (4/3)^{(n-1)/2}$.

*Proof.* By induction, with the stronger step $\gamma_n \le (\tfrac43 \gamma_{n-1})^{(n-1)/n}$. Let $v \in L$ have $\|v\| = \lambda_1$ and let $L'$ be the projection of $L$ orthogonally to $v$, a lattice of rank $n-1$ with $\det(L') = \det(L)/\lambda_1$. Take $w' \in L'$ with $\|w'\|^2 \le \gamma_{n-1} \det(L')^{2/(n-1)}$. A lift $w \in L$ of $w'$ can be chosen with component along $v$ of length at most $\lambda_1/2$, so $\|w\|^2 \le \|w'\|^2 + \lambda_1^2/4$. Since $w$ is a nonzero lattice vector, $\lambda_1^2 \le \|w\|^2$, which gives $\tfrac34 \lambda_1^2 \le \|w'\|^2 \le \gamma_{n-1} (\det(L)/\lambda_1)^{2/(n-1)}$. Collecting the powers of $\lambda_1$ gives $\lambda_1^{2n/(n-1)} \le \tfrac43 \gamma_{n-1} \det(L)^{2/(n-1)}$, which is the step. With $\gamma_{n-1} \le (4/3)^{(n-2)/2}$, the exponent of $4/3$ becomes $\tfrac{n-1}{n}(1 + \tfrac{n-2}{2}) = \tfrac{n-1}{2}$. $\square$

The proof is the analysis of LLL in disguise. LLL makes each projected pair nearly [Lagrange-reduced](/lagrange-gauss-reduction/) and gets $\|b_1\| \le (\tfrac43 + \varepsilon)^{(n-1)/4} \det(L)^{1/n}$: Hermite's bound, with $\gamma_2 = 2/\sqrt3$ replaced by $(4/3 + \varepsilon)^{1/2}$, in polynomial time.

**Mordell's inequality.** $\gamma_n \le \gamma_k^{(n-1)/(k-1)}$ for $2 \le k \le n$; for $k = n - 1$ this reads $\gamma_n^{n-2} \le \gamma_{n-1}^{n-1}$. Gama and Nguyen's slide reduction turns this into an algorithm that, using an SVP oracle in dimension $k$, finds $\|b_1\| \le ((1 + \varepsilon) \gamma_k)^{(n-1)/(2(k-1))} \det(L)^{1/n}$, the bound of Mordell's inequality up to the factor $1 + \varepsilon$.

**Growth.** Minkowski's theorem on convex bodies gives $\gamma_n \le 4 / V_n^{2/n} \le 1 + n/4$. The Minkowski-Hlawka theorem gives lattices with $\gamma_n \ge \tfrac{n}{2 \pi e}(1 + o(1))$, and the bound of Kabatiansky and Levenshtein gives $\gamma_n \le \tfrac{1.744\, n}{2 \pi e}(1 + o(1))$. So $\gamma_n = \Theta(n)$, and the [Gaussian heuristic](/gaussian-heuristic/) value $\tfrac{n}{2 \pi e}$ is a typical value, not the maximum.

## Examples

The known values, with the lattices that reach them:

| $n$ | $\gamma_n^n$ | $\gamma_n$ | lattice | proved by |
|---|---|---|---|---|
| 1 | 1 | 1 | $\mathbb{Z}$ | |
| 2 | $4/3$ | 1.1547 | $A_2$ (hexagonal) | Lagrange |
| 3 | 2 | 1.2599 | $A_3 = D_3$ (face-centred cubic) | Gauss |
| 4 | 4 | 1.4142 | $D_4$ | Korkine and Zolotarev |
| 5 | 8 | 1.5157 | $D_5$ | Korkine and Zolotarev |
| 6 | $64/3$ | 1.6654 | $E_6$ | Blichfeldt |
| 7 | 64 | 1.8114 | $E_7$ | Blichfeldt |
| 8 | 256 | 2 | $E_8$ | Blichfeldt |
| 24 | $4^{24}$ | 4 | Leech lattice | Cohn and Kumar (2009) |

- **Dimension 2.** For $A_2$ with rows $(1, 0)$, $(\tfrac12, \tfrac{\sqrt3}{2})$: $\lambda_1 = 1$, $\det = \tfrac{\sqrt3}{2}$, so $\lambda_1^2/\det = 2/\sqrt3$. The matching upper bound is the inequality $\lambda_1^2 \le \tfrac{2}{\sqrt3} \det(L)$ for a Lagrange-reduced basis.
- **Dimension 3.** For $D_3$ with basis $(1, -1, 0), (0, 1, -1), (1, 1, 0)$: $\lambda_1^2 = 2$, $\det = 2$, so $\lambda_1^2 / \det^{2/3} = 2^{1/3}$ and $\gamma_3^3 = 2$.
- **Dimension 4.** $D_4$ has $\lambda_1^2 = 2$ and $\det = 2$, so $\gamma_4 = 2/\sqrt2 = \sqrt2$.
- **Dimension 8.** $E_8$ is unimodular with $\lambda_1^2 = 2$, so $\gamma_8 = 2$. Hermite's bound gives only $(4/3)^{7/2} \approx 2.74$.
- **A lattice far from the maximum.** $\mathbb{Z}^n$ gives ratio 1 in every dimension, while $\gamma_n$ grows like $n/(2 \pi e)$.

## Where it is used

- **Approximation factors.** The output guarantee of [LLL](/lll-approximation-guarantee/) is stated as a Hermite factor $\|b_1\| / \det(L)^{1/n}$, and the observed behaviour of reduction algorithms is measured by the [root Hermite factor](/root-hermite-factor/), the $n$-th root of that ratio.
- **Block reduction.** The analysis of [BKZ](/bkz-algorithm/) and slide reduction bounds the output by powers of $\gamma_\beta$ for the block size $\beta$, such as $\|b_1\| \le ((1 + \varepsilon) \gamma_\beta)^{(n-\beta)/(\beta-1)} \lambda_1$ for slide reduction.
- **[HKZ reduction](/hkz-reduction/).** The bounds on HKZ-reduced bases, and the cost analysis of [Kannan's enumeration](/kannan-enumeration/), use $\gamma_k$ for every $k \le n$.
- **Hermite SVP.** The problem "find a nonzero $v$ with $\|v\| \le \gamma \det(L)^{1/n}$" is called HSVP; any factor $\gamma \ge \sqrt{\gamma_n}$ makes it always solvable.
- **Sphere packing.** The values in the table are the densest lattice packings; the Leech lattice and $E_8$ are also the densest packings among all packings in their dimensions (Viazovska and coauthors, 2016).
- **Minkowski's theorems.** [Minkowski's first theorem](/minkowski-theorem/) is the bound $\gamma_n \le 4/V_n^{2/n}$; the [second theorem](/minkowski-second-theorem/) extends it to the product of the successive minima.

## References
