---
tag: 7KQWVZ
kind: technique
slug: multipole-to-local-translation
name: Multipole-to-local translation
aliases:
- M2L translation
- M2L operator
area: scientific-computing/n-body-and-particle-methods
level: advanced
summary: "Converts the multipole expansion of a far cell into a local Taylor expansion about a target cell; it is the costliest step of the fast multipole method."
prereqs: [multipole-expansion, multipole-truncation-error-bound, binomial-coefficient]
see_also: [fast-multipole-method, adaptive-fast-multipole-method, kernel-independent-fast-multipole-method, black-box-fast-multipole-method, fast-fourier-transform, singular-value-decomposition, quadtree, octree]
sources:
  - paper: doi:10.1016/0021-9991(87)90140-9
    title: "Leslie Greengard and Vladimir Rokhlin, A fast algorithm for particle simulations, Journal of Computational Physics 73(2), 1987, 325-348"
    locator: the conversion of a multipole expansion into a local expansion in 2D and its error bound
  - url: https://math.nyu.edu/~greengar/shortcourse_fmm.pdf
    title: "Rick Beatson and Leslie Greengard, A short course on fast multipole methods, in Wavelets, Multilevel Methods and Elliptic PDEs, Oxford University Press, 1997"
    locator: "Lemma 4.7, formulas (4.18) to (4.20); Section 5 for the 3D interaction list of 189 boxes and the faster 3D translations"
  - book: isbn:9780262071109
    title: Leslie Greengard, The Rapid Evaluation of Potential Fields in Particle Systems, MIT Press, 1988
    locator: the 3D translation operators in spherical harmonics
---

The multipole-to-local (M2L) translation takes the [multipole expansion](/multipole-expansion/) of the charges in one box and gives a local expansion, a Taylor series, of their field about the center of a second box that is well separated from the first. It is the step of the [fast multipole method](/fast-multipole-method/) that connects the two trees: the upward pass builds the multipole expansions, M2L turns them into local expansions, and the downward pass moves the local expansions down to the particles. In 2D, with $p$ terms, one M2L costs $O(p^2)$, and each box takes part in up to 27 of them, against 4 multipole shifts and 4 local shifts. In 3D the interaction list has 189 boxes and a direct M2L costs $O(p^4)$, so most work on faster FMMs is work on faster M2L.

## In plain words

A far group of charges can be described in two ways. The first way is centered on the group: it says how the group pulls on any point far from it. The second way is centered on a region where you want the pull: it says how all far charges pull on points in that region.

The M2L step changes the first description into the second one. It takes the short list of numbers for a source box and gives a short list of numbers for a target box. Many source boxes can then add their lists into one list for the target box. After that, the particles of the target box need only this one list to feel all the sources, instead of one sum for each source box.

## When it applies

M2L applies when the field of the sources has a convergent multipole expansion outside a disk (or ball) that holds them, and the target region is a disk (or ball) that lies far enough outside it. In 2D, for charges in the disk of radius $R$ about $z_0$ and targets in the disk of radius $R$ about $0$, Lemma 4.7 of Beatson and Greengard needs $|z_0| > (c + 1) R$ with $c > 1$. In the uniform FMM, two boxes of side $w$ in each other's interaction list have centers at least $2w$ apart and radius $R = w / \sqrt{2}$, so $c = 2\sqrt{2} - 1 \approx 1.83$. It does not apply to near neighbours: there, the series does not converge in the whole target box.

The kernel must have a separable expansion: the logarithm and $1/r$ (Laplace), the Helmholtz and Yukawa kernels with Bessel functions, and in a weaker sense any smooth kernel through interpolation or equivalent densities.

## The template

For the 2D logarithmic kernel in complex form, the source expansion about $z_0$ is

$$\phi(z) = a_0 \log(z - z_0) + \sum_{k=1}^{p} \frac{a_k}{(z - z_0)^k}, \qquad a_0 = \sum_i q_i, \quad a_k = -\sum_i \frac{q_i (z_i - z_0)^k}{k}.$$

1. **Expand each term about the target center.** Move the target center to $0$. For $|z| < |z_0|$, write $\log(z - z_0) = \log(-z_0) - \sum_{l \ge 1} \frac{1}{l} \left( \frac{z}{z_0} \right)^l$ and $(z - z_0)^{-k} = (-z_0)^{-k} \sum_{l \ge 0} \binom{l + k - 1}{k - 1} \left( \frac{z}{z_0} \right)^l$.
2. **Collect the powers of $z$.** This gives $\phi(z) = \sum_{l \ge 0} b_l z^l$ with
$$b_0 = a_0 \log(-z_0) + \sum_{k=1}^{p} (-1)^k \frac{a_k}{z_0^k}, \qquad b_l = -\frac{a_0}{l z_0^l} + \frac{1}{z_0^l} \sum_{k=1}^{p} (-1)^k \frac{a_k}{z_0^k} \binom{l + k - 1}{k - 1} \quad (l \ge 1).$$
3. **Truncate.** Keep $b_0, \ldots, b_p$. The error inside the target disk is less than $A \frac{4e(p + c)(c + 1) + c^2}{c (c - 1)} (1/c)^{p+1}$ with $A = \sum |q_i|$ (Lemma 4.7, formula (4.20)). It decays like $(1/c)^p$, the same rate as the [truncation bound](/multipole-truncation-error-bound/) with $r / R$ replaced by $1 / c$.
4. **Add.** M2L is linear in the $a_k$, so the local expansions from all boxes of the interaction list add into one set of $b_l$ per target box.
5. **Precompute.** In a uniform tree, the M2L operator depends only on the offset of the two boxes in units of the side. In 2D there are $7^2 - 3^2 = 40$ offsets. With coefficients scaled by the box size, $a_k / w^k$ and $b_l w^l$, the matrices are the same at every level, apart from a $\log w$ term in $b_0$.

The cost of one translation by step 2 is $p^2$ multiplications. The matrix $\binom{l + k - 1}{k - 1} = \frac{(l + k - 1)!}{l! \, (k - 1)!}$ is a Hankel matrix in $l + k$ between two diagonal scalings, so an FFT gives the product in $O(p \log p)$.

## Classic examples

**One charge at the center of the source box.** Take $q = 1$ at $z_0 = 2$, so $a_0 = 1$ and $a_k = 0$ for $k \ge 1$. Then $b_0 = \log(-2)$, with real part $\log 2 = 0.693147$, and $b_l = -1/(l \, 2^l)$: $b_1 = -0.5$, $b_2 = -0.125$, $b_3 = -0.041667$. At $z = 0.5$ the exact potential is $\log|0.5 - 2| = \log 1.5 = 0.405465$. The local series with $p = 2$ gives $0.693147 - 0.25 - 0.03125 = 0.411897$, an error of $6.4 \times 10^{-3}$. With $p = 4$ and $p = 8$ the errors are $2.5 \times 10^{-4}$ and $5.5 \times 10^{-7}$, close to the factor $|z| / |z_0| = 1/4$ per term. This case can be checked by hand.

**Two charges in an FMM box.** Take $q_1 = 1$ at $2.3 + 0.2\mathrm{i}$ and $q_2 = -0.5$ at $1.8 - 0.3\mathrm{i}$, in the box of side 1 about $z_0 = 2$, and the target box of side 1 about $0$, so $c = 2\sqrt{2} - 1$. The multipole coefficients for $p = 2$ are $a_0 = 0.5$, $a_1 = -0.4 - 0.35\mathrm{i}$ and $a_2 = -0.0375 - 0.03\mathrm{i}$, and M2L gives $b_1 = -0.159375 + 0.08\mathrm{i}$ and $b_2 = -0.019531 + 0.038125\mathrm{i}$. At $z = 0.3 + 0.4\mathrm{i}$ the exact potential is $0.446133$. The errors are:

| $p$ | multipole series at $z$ | local series after M2L | bound (4.20) |
|---|---|---|---|
| 2 | $3.1 \times 10^{-3}$ | $3.5 \times 10^{-3}$ | 19.6 |
| 4 | $5.1 \times 10^{-6}$ | $1.7 \times 10^{-4}$ | 8.9 |
| 8 | $4.2 \times 10^{-8}$ | $4.0 \times 10^{-7}$ | 1.3 |
| 16 | $1.1 \times 10^{-14}$ | $9.1 \times 10^{-12}$ | $1.9 \times 10^{-2}$ |

These were computed with the implementation of the [fast multipole method](/fast-multipole-method/) page. The local series is less accurate than the multipole series at the same point, because it must also converge in the whole target disk. The bound is far above the measured error, but it falls at the right rate.

**The interaction list.** In the 2D FMM, a box at level $l \ge 2$ receives M2L translations from the children of its parent's near neighbours that do not touch it: 27 boxes for an interior box. In 3D the same rule gives $6^3 - 3^3 = 189$ boxes.

## Variations

- **3D spherical harmonics.** A $p$-term 3D expansion has $(p + 1)^2$ coefficients, and the direct M2L costs $O(p^4)$ (Greengard 1988).
- **Rotations.** Rotate the frame so that the translation is along the $z$ axis, translate along the axis, and rotate back. Each step costs $O(p^3)$.
- **Plane waves.** The newer 3D FMM of Greengard and Rokhlin converts multipole expansions to exponential (plane-wave) expansions, for which translation is diagonal. Beatson and Greengard (Section 5) state that this replaces $189 p^4$ operations per box with about $3 p^3 + 189 p^2$.
- **FFT.** The Toeplitz or Hankel structure of the operator, in 2D and on a regular grid of equivalent points in 3D, gives $O(p \log p)$ per translation; the [kernel-independent FMM](/kernel-independent-fast-multipole-method/) uses FFTs for its M2L.
- **Low rank compression.** The [black-box FMM](/black-box-fast-multipole-method/) stores the M2L operator between Chebyshev nodes and compresses it with the [singular value decomposition](/singular-value-decomposition/).
- **Adaptive trees.** In the [adaptive FMM](/adaptive-fast-multipole-method/), M2L is used for the V list of boxes of the same size. Boxes of different sizes use direct multipole evaluation (W list) or direct local expansions of the charges (X list) instead.

## Pitfalls

- **Wrong sign of the offset.** The formulas need $z_0$ as the source center minus the target center. With the other sign, the series is that of a box at the mirror position and is wrong without any error message.
- **Translating near neighbours.** The local series converges only for $|z| < |z_0| - R$. If $|z_0| \le 2R$, it can diverge on part of the target box. Use the interaction list exactly.
- **Overflow and underflow.** For large $p$, the powers $z_0^{-k}$ and the binomial coefficients become very large or very small. Use scaled coefficients.
- **The branch of $\log(-z_0)$.** Only the real part is the potential. If the imaginary part is used, the branch cuts of all boxes must agree.
- **Trusting the bound as an estimate.** The bound (4.20) is many orders of magnitude above the actual error for small $p$. Choose $p$ from measurements against direct summation, or from a sharper bound.
- **Unequal truncation.** Keeping $p$ terms in the multipole expansion but fewer in the local expansion (or the reverse) wastes work, since the error is set by the smaller order.

## Exercises

1. Derive the formula for $b_l$ in step 2 from the binomial series of $(1 - z/z_0)^{-k}$.
2. Show that the M2L operator for the scaled coefficients $\tilde a_k = a_k / w^k$ and $\tilde b_l = b_l w^l$ depends only on $z_0 / w$, except for the term $a_0 \log w$ in $b_0$.
3. For one unit charge at $z_0 = 2$, show that the error of the $p$-term local series at $z = 0.5$ is $\sum_{l > p} 4^{-l} / l$, and compare it with the numbers above.
4. Count the 2D interaction list of a box in a corner of the unit square at level 2, and at level 3.
5. Write the M2L operator as $D_1 H D_2$ with diagonal $D_1$, $D_2$ and a Hankel matrix $H$, and explain how an FFT computes $H a$ in $O(p \log p)$.

## References
