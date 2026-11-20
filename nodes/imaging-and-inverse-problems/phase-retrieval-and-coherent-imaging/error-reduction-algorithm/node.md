---
tag: HKZC9V
kind: algorithm
slug: error-reduction-algorithm
name: Error reduction algorithm
aliases:
- Fienup error reduction
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: "Alternate between the measured Fourier magnitude and a support (and nonnegativity) constraint. The error never grows, but the iteration often stops short of a solution."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of iterations}
  time: {worst: O(K N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1978
  people: [James R. Fienup]
  note: Fienup adapted the Gerchberg-Saxton iteration to one intensity measurement and an object constraint, and in 1982 proved that its error does not increase.
prereqs: [gerchberg-saxton-algorithm, phase-retrieval, discrete-fourier-transform]
see_also: [hybrid-input-output, shrinkwrap, oversampling-in-phase-retrieval, phase-retrieval-ambiguities, projected-gradient-descent, convex-feasibility-problem, griffin-lim-algorithm, coherent-diffraction-imaging]
sources:
  - paper: doi:10.1364/AO.21.002758
    title: J. R. Fienup, Phase retrieval algorithms, a comparison, Applied Optics 21(15), 1982, 2758 to 2769
    locator: the section on the error-reduction algorithm (the error does not increase) and the section on gradient search methods (error reduction as steepest descent)
  - paper: doi:10.1364/OL.3.000027
    title: J. R. Fienup, Reconstruction of an object from the modulus of its Fourier transform, Optics Letters 3(1), 1978, 27 to 29
    locator: the iterative method with object domain constraints
  - paper: "R. W. Gerchberg and W. O. Saxton, A practical algorithm for the determination of phase from image and diffraction plane pictures, Optik 35(2), 1972, pages 237 to 246"
    locator: the iteration between two planes with known magnitudes
  - paper: doi:10.1109/MSP.2014.2352673
    title: Yoav Shechtman, Yonina C. Eldar, Oren Cohen, Henry N. Chapman, Jianwei Miao and Mordechai Segev, Phase retrieval with application to optical imaging, a contemporary overview, IEEE Signal Processing Magazine 32(3), 2015, 87 to 109
    locator: the section on alternating projection algorithms
---

The error reduction algorithm solves the [phase retrieval](/phase-retrieval/) problem with a known support. It alternates two projections: it puts the measured Fourier magnitude on the current image and keeps the phase, then it sets the image to zero off the support (and, if the object is known to be nonnegative, clips it there). Fienup (1982) showed that the Fourier error never grows from one iteration to the next, and that each iteration is a steepest descent step with unit step on the squared error. The error can stop at a positive value, so error reduction often stagnates before it finds a solution. The [hybrid input-output](/hybrid-input-output/) algorithm was made to get past this.

## In plain words

You have a picture that you cannot see. You know how bright each spot of its diffraction pattern is, and you know that the object fits inside a small box. You want the picture back.

Start with any guess. Compute its diffraction pattern. The brightness is wrong, so replace it with the measured brightness and keep the rest. Go back to a picture. Now the picture has some stuff outside the box, and maybe some negative values. Remove them. That is one round.

Each round fixes one rule and breaks the other a little. The amount by which the two rules disagree can never grow. But it can stop shrinking before it gets to zero. Then the guess is stuck, and more rounds do not help.

## The problem

The input is an $n_1 \times n_2$ array of magnitudes $A_u = |F_u|$, where $F$ is the DFT of an unknown image $f$ with $N = n_1 n_2$ pixels, and a support mask $S$ that holds every nonzero pixel of $f$. Sometimes $f$ is also known to be real and nonnegative. The output is an image $g$ that is zero off $S$ (and nonnegative, if required) and whose DFT has magnitude $A$. Such an image is equal to $f$ at best up to the [trivial ambiguities](/phase-retrieval-ambiguities/). The DFT is unnormalized forward with $1/N$ on the inverse. Errors use the unitary DFT, so they are distances between images.

## The algorithm

```pseudo id=main
ERROR-REDUCTION(A, S, g₀, K)
L1  g ← P_S(g₀)
L2  for k ← 1 to K do
L3      G ← DFT(g)
L4      G′_u ← A_u · G_u / |G_u| for each frequency u      ▷ A_u when G_u = 0
L5      g′ ← IDFT(G′)
L6      g ← P_S(g′)
L7  return g
```

$P_S(g')$ keeps $g'(r)$ on the support and sets $0$ off it. With nonnegativity it sets $\max(\operatorname{Re} g'(r), 0)$ on the support. Lines L3 to L5 together are the magnitude projection $P_M$: the nearest image whose DFT has magnitude $A$. Line L6 is the nearest image that satisfies the object constraint. Line L1 starts inside the constraint set, which the proof needs.

The Fourier error of an image is

$$E_F(g)^2 = \frac{1}{N} \sum_u \bigl(|G_u| - A_u\bigr)^2 = \|g - P_M g\|^2 .$$

The object error of $g'$ is $E_0(g')^2 = \|g' - P_S g'\|^2$, the energy that line L6 removes.

## Example

The object is a $4 \times 4$ nonnegative block in the corner of an $8 \times 8$ frame:

$$f = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 3 & 1 & 0 \\ 2 & 1 & 4 & 1 \\ 0 & 1 & 0 & 2 \end{pmatrix}.$$

The support $S$ is the $4 \times 4$ block, so the oversampling ratio is $64 / 16 = 4$. The start is a random image with entries in $[0, 1]$, with nonnegativity on. These are measurements of the implementation with two fixed seeds:

| iteration $k$ | 0 | 1 | 2 | 5 | 10 | 50 | 100 | 200 | 500 |
|---|---|---|---|---|---|---|---|---|---|
| $E_F$, seed 1 | 4.899 | 1.858 | 1.347 | 0.972 | 0.892 | 0.620 | 0.617 | 0.617 | 0.617 |
| $E_F$, seed 2 | 4.481 | 1.698 | 1.283 | 0.882 | 0.749 | 0.586 | 0.472 | 0.435 | 0.227 |

The error never grows. In the first run it stops at 0.617 after about 100 iterations and does not move again: this is stagnation at a point that is not a solution. In the second run it is still falling slowly at 500 iterations. The large drop in the first iterations, then a long slow tail, is the typical behavior.

## Correctness

Let $g_k$ be the image after $k$ passes and $g'_k = P_M g_k$. Both projections are nearest point maps: $P_M$ by a per-frequency argument and Parseval's identity, $P_S$ by a per-pixel argument. Since $g'_k$ has the right magnitude and $g_k$ satisfies the object constraint,

$$E_F(g_{k+1}) \le \|g_{k+1} - g'_k\| = E_0(g'_k) \le \|g'_k - g_k\| = E_F(g_k).$$

So the error does not increase. This is a theorem. It does not say that the error goes to zero: the set of images with magnitude $A$ is not convex, and the iterates can stop at a point that is not a solution. Where no DFT entry is zero, $B(g) = \frac{1}{2}E_F(g)^2$ has the gradient $g - P_M g$, so line L5 is the step $g - \nabla B(g)$ and line L6 projects it. This is Fienup's steepest descent view. The full proof is below.

## Complexity

Each iteration does one forward and one inverse 2D DFT and $O(N)$ other work. With a [fast Fourier transform](/fast-fourier-transform/) the cost is $O(N \log N)$ per iteration, so $O(K N \log N)$ in total. With the direct sum it is $O(N(n_1 + n_2))$ per iteration for the row and column transforms. The extra space is $O(N)$ for $G$ and $g'$. The number of iterations $K$ has no useful bound, because the method can stagnate.

## Properties

- **Monotone.** $E_F(g_{k+1}) \le E_0(g'_k) \le E_F(g_k)$ at every step (a theorem).
- **Fixed points.** Every solution is a fixed point. The converse is false: stagnation points are fixed points too.
- **Local.** It is a descent method on a nonconvex function, so the result depends on the start.
- **Ambiguities remain.** A result can be a shift (if the support allows it), a conjugate reversal or a global phase factor of the object. Compare results only up to these.

## Variants and improvements

- **[Gerchberg-Saxton](/gerchberg-saxton-algorithm/).** The same alternation with a known magnitude in both planes instead of a support.
- **[Hybrid input-output](/hybrid-input-output/).** Off the support, it pushes the iterate away from the constraint violation instead of setting it to zero. It escapes most stagnation points, but it has no monotone error and no convergence proof.
- **[Difference map](/difference-map/) and [RAAR](/raar/).** Fixed point iterations built from the same two projections that are less likely to stagnate.
- **[Shrinkwrap](/shrinkwrap/).** Starts with a loose support and makes it smaller during the run.
- **Gradient methods.** The steepest descent view leads to conjugate gradient and other descent methods on the same error. Fienup compared them in 1982.

## When to use it

Use error reduction as a baseline, and as a final polish: a common recipe runs hybrid input-output for some hundreds of iterations and ends with some error reduction iterations, which reduce the error and never increase it. Do not use it alone from a random start on a hard problem, because it stagnates.

## Pitfalls

- **Starting outside the constraint set.** The proof needs $g_0$ in the constraint set. Line L1 makes sure of this.
- **Errors in different units.** With the unnormalized DFT, the Fourier sum is $N$ times the object domain sum. Use the factor $1/N$ when you compare $E_F$ and $E_0$.
- **Taking a monotone error as success.** A small, flat error is not a solution. Check it against the noise level, and try several starts.
- **A support that is too tight or too loose.** A support that misses part of the object has no solution. A support that is much too large gives too few constraints for uniqueness; see [oversampling](/oversampling-in-phase-retrieval/).
- **Comparing with the truth.** Align the result for shift, conjugate reversal and global phase before you compute an error against the true object.

## Implementations

## History

Gerchberg and Saxton (1972) described the alternation between two planes with known magnitudes. Fienup (1978) used the same idea with one Fourier magnitude and constraints in the object domain, such as a support and nonnegativity. In his 1982 comparison of phase retrieval algorithms, Fienup called this method error reduction, proved that its error does not increase, showed that it is a form of steepest descent, and proposed the input-output algorithms, among them hybrid input-output.

## References
