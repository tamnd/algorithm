---
tag: KZJ4DM
kind: algorithm
slug: pocs-partial-fourier
name: POCS partial Fourier reconstruction
aliases:
- Haacke POCS reconstruction
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: Rebuilds an MR image from partial k-space by alternate projections onto the images with a low resolution phase and onto the images that agree with the measured samples.
solves: [partial-fourier-reconstruction]
model: real-ram
complexity:
  vars: {n: "the side of an n x n image (the number of samples along the partial axis), with n a power of two and an FFT", K: the number of iterations}
  time: {worst: O(K n^2 log n)}
  space: {extra: O(n^2)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1991
  people: [E. Mark Haacke, E. D. Lindskog, W. Lin]
  note: Haacke, Lindskog and Lin made partial Fourier reconstruction iterative, with a phase constraint in the image and a data constraint in k-space, and showed that it recovers local phase better than one-step methods.
prereqs: [partial-fourier-reconstruction, discrete-fourier-transform]
see_also: [homodyne-reconstruction, k-space, error-reduction-algorithm, gerchberg-saxton-algorithm, convex-set, parseval-theorem, landweber-iteration, compressed-sensing-mri]
sources:
  - paper: doi:10.1016/0022-2364(91)90253-P
    title: E. M. Haacke, E. D. Lindskog and W. Lin, A fast, iterative, partial-Fourier technique capable of local phase recovery, Journal of Magnetic Resonance 92(1), 1991, 126 to 145
    locator: the iteration between the phase constraint in the image and the measured data in k-space (general locator; section numbers not confirmed)
  - book: isbn:9780120928613
    title: Matt A. Bernstein, Kevin F. King and Xiaohong Joe Zhou, Handbook of MRI Pulse Sequences, Elsevier Academic Press, 2004
    locator: Section 13.4, Partial Fourier Reconstruction
---

POCS partial Fourier reconstruction rebuilds an MR image from a little more than half of [k-space](/k-space/), the case of [partial Fourier reconstruction](/partial-fourier-reconstruction/). It alternates two steps. The first step gives every pixel the phase of a low resolution image made from the band that is measured on both sides of the center. The second step puts the measured samples back into the k-space of the current image. Each step is the projection onto a convex set, so the name is projections onto convex sets (POCS). Haacke, Lindskog and Lin published the method in 1991. The iterates converge for any phase estimate, and for a real image with a constant phase the error halves at each iteration. Both facts are proved on this page.

## In plain words

The picture we want is made of real numbers, but the scanner adds a slowly changing tilt to each value. The scan measures only a little more than half of the frequency description of the picture. A blurry picture made from the frequencies near the middle shows the tilt well.

The method then repeats two steps. First, it makes every pixel point in the direction of that tilt, and it keeps only the part of the value that points that way. Second, it puts back the frequencies that the scanner measured, because the first step changed them. Each step moves the picture to the nearest picture that obeys one rule. Repeating the two steps brings the picture closer to one that obeys both rules.

## The problem

The input is one line of [k-space](/k-space/) data of even length $n$ along the phase encoding axis, in DFT order with frequencies $-n/2, \ldots, n/2 - 1$, and the number $k_0$ with $0 \le k_0 < n/2 - 1$. The data are $y_f = (F_u x)(f)$ for $f \in S = \{-n/2, \ldots, k_0\}$, where $F_u = n^{-1/2} F$ is the unitary DFT. The model is $x = e^{i\varphi}\rho$ with $\rho$ real and $\varphi$ smooth. The output is a complex image $\hat x$ whose acquired samples equal $y$ and whose phase is the reference phase. For an $n_1 \times n_2$ image with partial phase encoding, an inverse DFT along the fully sampled readout axis first gives one such line per image column.

## The algorithm

The two sets are $C_1 = \{\rho p : \rho \in \mathbb{R}^n\}$, the images with the reference phase $p$, and $C_2$, the images whose samples on $S$ equal $y$.

```pseudo id=main
POCS-PF(y, n, k0, K)                  ▷ y known for f = -n/2 .. k0
L1  p <- unit phase of F_u^H (T y)     ▷ T: triangle window on |f| <= k0
L2  x <- F_u^H (y on S, 0 elsewhere)   ▷ the zero filled image
L3  repeat K times
L4      x_j <- Re(conj(p_j) x_j) p_j for each pixel j   ▷ project onto C1
L5      X <- F_u x
L6      X(f) <- y(f) for each f in S                     ▷ project onto C2
L7      x <- F_u^H X
L8  return x
```

Line L1 makes the reference phase from the band $|f| \le k_0$, which is measured on both sides, with the window $T(f) = 1 - |f|/(k_0+1)$. Where the low resolution image is zero, $p_j = 1$. Line L2 starts from the zero filled image. Line L4 keeps, at each pixel, the component of $x_j$ along $p_j$; this is the nearest image with the phase $p$. Lines L5 to L7 replace the acquired samples by the data and keep the estimate of the missing samples; because $F_u$ is unitary, this is the nearest image that agrees with the data. The magnitude image $|\hat x|$ or the real part $\operatorname{Re}(\overline{p} \hat x)$ is the result.

## Example

Take $n = 8$, $k_0 = 1$, the real profile $\rho = [0, 0, 4, 4, 4, 0, 0, 0]$ and the constant phase $0.5$ rad, so $x = e^{0.5i}\rho$. The scan acquires $f = -4, \ldots, 1$ and misses $f = 2, 3$. The reference phase of line L1 is $e^{0.5i}$ at every pixel. The table gives the relative error $\|x_t - x\| / \|x\|$ after $t$ iterations, rounded.

| iteration $t$ | 0 | 1 | 2 | 3 | 5 | 10 | 20 |
|---|---|---|---|---|---|---|---|
| relative error | 0.22094 | 0.11047 | 0.05524 | 0.02762 | 0.00690 | 0.00022 | $2 \times 10^{-7}$ |

Iteration 0 is the zero filled image of line L2. The error halves at each step, as the theorem below says. With the signed profile $\rho = [0, 0, 4, 4, -2, 0, 0, 0]$ and the same phase, the errors are 0.516, 0.258, 0.129 and so on, and POCS again converges to $x$. [Homodyne reconstruction](/homodyne-reconstruction/) returns the sign of the smoothed image times $\rho$, so it can give the wrong sign in such a case.

## Correctness

Line L4 is the orthogonal projection onto $C_1$, a real linear subspace of $\mathbb{C}^n$ seen as $\mathbb{R}^{2n}$. Lines L5 to L7 are the orthogonal projection onto $C_2$, an affine subspace. The key invariant is that for every $z \in C_1 \cap C_2$, the distance $\|x_t - z\|$ never grows. The [proof](proofs/correctness.md) shows three theorems.

- If $C_1 \cap C_2$ is not empty, the iterates converge to the point of the intersection nearest to the zero filled image, at a geometric rate.
- If the intersection is empty, for example with noise, the iterates still converge, to a point of $C_2$ whose distance to $C_1$ is the distance between the sets.
- For a real image with a constant phase and $p_j = \pm e^{i\varphi_0}$, the intersection is the true image, and the error halves exactly at each iteration.

These are theorems about the sets. When the phase of the image varies, the set $C_1$ is built from an estimated phase, so the limit is the nearest image of the model, not the true image.

## Complexity

Each iteration costs one DFT and one inverse DFT of length $n$ and $O(n)$ other operations. With an FFT and $n$ a power of two this is $O(n \log n)$ per line, and $O(K n^2 \log n)$ for $K$ iterations on an $n \times n$ image, in the [real RAM](/real-ram/). The method stores the hybrid data and the image, $O(n^2)$ numbers. Line L1 costs one more inverse DFT per line.

## Properties

- **Convergence.** The iterates converge for any unit phase $p$ (theorem). The rate is geometric, with a constant that depends on the angle between the two sets.
- **Exact rate for a constant phase.** The error halves at each iteration (theorem). Ten iterations reduce it by a factor of about 1000.
- **Signed images.** For a constant phase, the limit is the true image even when $\rho$ has both signs (theorem). The sign of $\rho$ is relative to $p$.
- **Smooth phase.** On a $16 \times 16$ modified Shepp-Logan phantom with the phase $0.4 + 0.5x - 0.6y + 0.2xy$ rad on $[-1, 1]^2$ and 12 of 16 phase encoding lines, the relative magnitude error was 0.156 after 1 iteration, 0.046 after 5 and 0.0455 after 30, against 0.333 for the zero filled magnitude (measurement with the code of this page). Homodyne gave 0.094 on the same data.
- **Data consistency.** The output agrees with the measured samples exactly, because line L6 is the last step that changes them.

## Variants and improvements

- **Magnitude with the reference phase.** Many descriptions replace $x_j$ by $|x_j| p_j$ in line L4. That map is not a projection onto a convex set, and the convergence theorems do not cover it. It gives a nonnegative magnitude by construction.
- **Smooth transition.** Some implementations blend the estimated and the measured samples near the edge $f = k_0$ to reduce ringing.
- **Two-dimensional partial Fourier.** The same iteration works when both axes are partial; the data step then uses a 2D DFT.
- **Combination with other constraints.** The phase constraint can join the coil sensitivity constraint of [SENSE](/sense/) or a sparsity term as in [compressed sensing MRI](/compressed-sensing-mri/).
- **Relatives in phase retrieval.** The [error reduction algorithm](/error-reduction-algorithm/) and the [Gerchberg-Saxton algorithm](/gerchberg-saxton-algorithm/) also alternate between an image constraint and a Fourier constraint, but their Fourier set is not convex.

## When to use it

Use POCS for partial Fourier data when the phase varies inside the image and homodyne is not accurate enough, when the image has both signs, or when the output must agree with the data. It costs several times more than [homodyne reconstruction](/homodyne-reconstruction/), but 5 to 10 iterations are often enough. As with any partial Fourier method, the phase must be smooth enough for the central band to show it.

## Pitfalls

- **Phase from the wrong samples.** If line L1 uses all acquired samples, not a symmetric band, the reference phase is wrong even for a constant phase, and the limit is not the true image.
- **Data step that changes the missing samples.** If line L6 also sets the missing samples to zero, every iteration returns the zero filled image.
- **No unitary scale.** If line L5 and line L7 use DFTs with scales that do not cancel, line L7 does not invert line L5, and the data step is not a projection.
- **Too many iterations on noisy data.** With noise the sets do not meet. The iterates converge, but late iterations change little and can make the noise at the edge of the band more visible.
- **Phase zeros.** Where the low resolution image is zero, line L1 has no phase; the code uses 1 there.

## Implementations

## History

Margosian, Schmitt and Purdy (1986) and Feinberg and colleagues (1986) showed that half of k-space with a phase correction gives a full image. Noll, Nishimura and Macovski (1991) gave the one-step homodyne method. In the same year Haacke, Lindskog and Lin published the iterative method in the Journal of Magnetic Resonance, with the phase constraint in the image domain and the data constraint in k-space. The idea of alternate projections onto convex sets goes back to von Neumann for two subspaces.

## References
