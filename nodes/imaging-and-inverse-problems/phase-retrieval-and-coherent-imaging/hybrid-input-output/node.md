---
tag: 5WGXT1
kind: algorithm
slug: hybrid-input-output
name: Hybrid input-output algorithm
aliases:
- HIO
- Fienup HIO
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: "Fienup's phase retrieval iteration: keep the magnitude-projected image on the support and push the old iterate away from it elsewhere. It escapes stagnation but has no convergence proof."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of iterations}
  time: {worst: O(K N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 1982
  people: [James R. Fienup]
  note: Fienup defined the input-output algorithms, among them hybrid input-output, in his 1982 comparison of phase retrieval algorithms.
prereqs: [error-reduction-algorithm, phase-retrieval]
see_also: [difference-map, raar, shrinkwrap, coherent-diffraction-imaging, oversampling-in-phase-retrieval, phase-retrieval-ambiguities, convex-feasibility-problem, fixed-point-iteration]
sources:
  - paper: doi:10.1364/AO.21.002758
    title: J. R. Fienup, Phase retrieval algorithms, a comparison, Applied Optics 21(15), 1982, 2758 to 2769
    locator: the section on the input-output algorithms, with the hybrid input-output update, and the comparison with error reduction
  - paper: doi:10.1364/OL.3.000027
    title: J. R. Fienup, Reconstruction of an object from the modulus of its Fourier transform, Optics Letters 3(1), 1978, 27 to 29
    locator: the iterative method with object domain constraints
  - paper: doi:10.1364/JOSAA.19.001334
    title: Heinz H. Bauschke, Patrick L. Combettes and D. Russell Luke, Phase retrieval, error reduction algorithm, and Fienup variants, a view from convex optimization, Journal of the Optical Society of America A 19(7), 2002, 1334 to 1345
    locator: HIO with the support constraint and beta = 1 as the Douglas-Rachford algorithm
  - paper: doi:10.1103/PhysRevB.68.140101
    title: S. Marchesini, H. He, H. N. Chapman, S. P. Hau-Riege, A. Noy, M. R. Howells, U. Weierstall and J. C. H. Spence, X-ray image reconstruction from a diffraction pattern alone, Physical Review B 68(14), 2003, 140101
    locator: HIO with beta = 0.9 inside the shrinkwrap method
---

The hybrid input-output algorithm (HIO) solves the [phase retrieval](/phase-retrieval/) problem with a known support. Like [error reduction](/error-reduction-algorithm/), it first puts the measured Fourier magnitude on the current image. Then it keeps the result on the support, but at the pixels that break the object constraint it does not set zero: it takes the old value and subtracts $\beta$ times the new one. This feedback pushes the iterate away from the stagnation points of error reduction. Fienup (1982) introduced it, and it is still a standard method in [coherent diffraction imaging](/coherent-diffraction-imaging/). Its error is not monotone and there is no convergence proof, but every fixed point of HIO gives a solution.

## In plain words

Error reduction cleans up a guess by erasing everything outside the box where the object must be. This often gets stuck: the guess stops changing, but it is still wrong.

HIO changes the clean-up step. Inside the box, it keeps the new guess as it is. Outside the box, the new guess should be zero but is not. HIO does not erase it. It looks at how much stuff is there, and it moves the old guess in the opposite direction by almost the same amount. The next round then has a strong push to remove that stuff.

This push lets the guess climb out of places where error reduction gets stuck. The price is that the error can go up for a while. In practice HIO finds the object much more often.

## The problem

The input is an $n_1 \times n_2$ array of Fourier magnitudes $A_u = |F_u|$ of an unknown image $f$ with $N = n_1 n_2$ pixels, a support mask $S$ that holds every nonzero pixel of $f$, and maybe the knowledge that $f$ is real and nonnegative. The output is an image that is zero off $S$, nonnegative if required, and whose DFT has magnitude $A$. At best it equals $f$ up to the [trivial ambiguities](/phase-retrieval-ambiguities/). The DFT is unnormalized forward with $1/N$ on the inverse.

## The algorithm

```pseudo id=main
HIO(A, S, g₀, K, β)
L1  g ← g₀
L2  for k ← 1 to K do
L3      G ← DFT(g)
L4      G′_u ← A_u · G_u / |G_u| for each u            ▷ A_u when G_u = 0
L5      g′ ← IDFT(G′)
L6      for each pixel r do
L7          if r ∈ S and g′(r) ≥ 0 then g(r) ← g′(r)  ▷ test g′(r) ≥ 0 only with nonnegativity
L8          else g(r) ← g(r) − β · g′(r)
L9  return P_S(g′)
```

Lines L3 to L5 are the magnitude projection $g' = P_M g$, the same as in error reduction. With nonnegativity the image is real, and $g'$ means the real part of the inverse DFT. The output of line L9 is $g'$ with the object constraint put on. The iterate $g$ itself is not the answer: off the support it holds the accumulated feedback.

The progress of HIO is usually tracked by the object error $E_0(g') = \|g' - P_S g'\|$, the part of $g'$ that breaks the object constraint. It is zero exactly when $g'$ is a solution.

## Example

Use the same object as on the error reduction page: the $4 \times 4$ nonnegative block

$$f = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 3 & 1 & 0 \\ 2 & 1 & 4 & 1 \\ 0 & 1 & 0 & 2 \end{pmatrix}$$

in the corner of an $8 \times 8$ frame, with the $4 \times 4$ support and nonnegativity. From the random start of seed 1, error reduction stops at the Fourier error 0.617. HIO with $\beta = 0.9$ from the same start gives these object errors $E_0(g'_k)$ (measurements of the implementation):

| iteration $k$ | 0 | 1 | 2 | 5 | 10 | 20 | 50 | 100 | 200 | 299 |
|---|---|---|---|---|---|---|---|---|---|---|
| $E_0$ | 6.22 | 5.59 | 3.44 | 1.13 | 0.483 | 0.0374 | 0.0210 | 0.0269 | 0.0100 | 0.00635 |

The error goes up between iterations 50 and 100: HIO is not monotone. After 300 iterations, 20 iterations of error reduction bring the Fourier error to $2.8 \times 10^{-5}$. The result is not $f$ but its twin $f(3 - i, 3 - j)$, the object turned by 180 degrees. It has the same Fourier magnitude and fits in the same support, so it is an equally good answer (a conjugate reversal followed by a shift). The start of seed 2 also gives the twin.

## Correctness

There is no proof that HIO converges, and its error can go up. Three facts are proved:

- **Solutions are fixed points.** If $f$ fits the magnitude and the object constraint, one HIO step leaves it unchanged.
- **Fixed points give solutions.** If $H(g) = g$, then at every pixel outside the set of line L7, $g(r) = g(r) - \beta g'(r)$, so $g'(r) = 0$. So $g'$ is zero off the support and nonnegative on it, and $g'$ is a solution. This is the difference from error reduction, whose fixed points can be stagnation points with a positive error.
- **Douglas-Rachford.** With a support constraint only and $\beta = 1$, the step is $x + P_S(2P_M x - x) - P_M x$, the Douglas-Rachford iteration for the two sets (Bauschke, Combettes and Luke 2002). The convergence theory of Douglas-Rachford needs convex sets, and the magnitude set is not convex, so this does not give convergence.

The proofs are below.

## Complexity

Each iteration does one forward and one inverse 2D DFT and $O(N)$ other work. With a [fast Fourier transform](/fast-fourier-transform/) this is $O(N \log N)$ per iteration and $O(K N \log N)$ in total. The extra space is $O(N)$ for $G$, $g'$ and $g$. There is no bound on the number of iterations; typical runs use some hundreds to some thousands.

## Properties

- **Not monotone.** The error can go up. Do not stop at the first increase.
- **Fixed points are solutions** in the sense of Theorem 2 of the proof.
- **Feedback.** The value $\beta$ sets the strength of the push. Common values are between 0.5 and 1. The value 0.9 (used, for example, by Marchesini et al. 2003) is a tuned choice, not a result.
- **Ambiguities remain.** A run can end at the object, its twin, or a shift of either that fits the support.

## Variants and improvements

- **Input-output and output-output.** Fienup (1982) also defined two other steps. The basic input-output step keeps the old value $g(r)$ at the pixels of line L7 and uses $g(r) - \beta g'(r)$ elsewhere. The output-output step uses $g'(r)$ at the pixels of line L7 and $g'(r) - \beta g'(r)$ elsewhere. HIO mixes the two, which gives its name. HIO worked best in his tests.
- **HIO then error reduction.** Run HIO to get near a solution, then a few error reduction steps, which reduce the error and never increase it.
- **[Difference map](/difference-map/).** Elser's family of iterations; one choice of its parameters gives HIO exactly.
- **[RAAR](/raar/).** A relaxation of the $\beta = 1$ case that behaves better with noisy data.
- **[Shrinkwrap](/shrinkwrap/).** HIO with a support that is updated during the run.
- **Many starts.** Run HIO from many random starts, and keep or average the results with the smallest error.

## When to use it

Use HIO for phase retrieval from one far-field intensity with a support, as in [coherent diffraction imaging](/coherent-diffraction-imaging/) and crystallography of small objects. Start with HIO, end with error reduction, and run several starts. Make sure the data are [oversampled](/oversampling-in-phase-retrieval/), or the support constraint is too weak. With noisy data, compare with RAAR, which is less likely to wander.

## Pitfalls

- **Returning $g$ instead of $g'$.** The iterate $g$ holds feedback off the support. The estimate is $P_S(g')$.
- **Stopping at an increase.** The error is not monotone, so an increase is not a sign of failure.
- **Nonnegativity for a complex object.** The test $g'(r) \ge 0$ in line L7 is for a real object. For a complex object, use the support test alone.
- **A twin that lives inside the support.** For a centrally symmetric support, the twin is always a valid answer, and a run can mix the object and its twin into one stagnation pattern. A support that is not centrally symmetric breaks this tie.
- **Comparing with the truth.** Align the result for shift, twin and global phase first.

## Implementations

## History

Fienup (1978) reconstructed an object from the modulus of its Fourier transform with an iterative method and object domain constraints. In his 1982 comparison he defined error reduction, the gradient methods and the input-output algorithms, among them hybrid input-output, and found that HIO worked best in his tests. Bauschke, Combettes and Luke (2002) showed that HIO for the support constraint with $\beta = 1$ is the Douglas-Rachford algorithm of convex optimization. Elser (2003) and Luke (2005) built the difference map and RAAR on this view.

## References
