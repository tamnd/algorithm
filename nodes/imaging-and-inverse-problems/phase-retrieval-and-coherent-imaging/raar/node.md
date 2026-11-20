---
tag: MJJXEG
kind: algorithm
slug: raar
name: Relaxed averaged alternating reflections
aliases:
- RAAR
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: "Phase retrieval by a step that mixes the Douglas-Rachford reflection step with the magnitude projection. For convex sets that meet, its fixed points are exactly the solutions."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of iterations}
  time: {worst: O(K N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2005
  people: [D. Russell Luke]
  note: Luke introduced RAAR as a relaxation of the Douglas-Rachford (HIO with beta = 1) step, made for diffraction data that is noisy or does not fit the constraints exactly.
prereqs: [hybrid-input-output, phase-retrieval]
see_also: [difference-map, error-reduction-algorithm, shrinkwrap, convex-feasibility-problem, proximal-operator, fixed-point-iteration, coherent-diffraction-imaging, ptychography]
sources:
  - paper: doi:10.1088/0266-5611/21/1/004
    title: D. Russell Luke, Relaxed averaged alternating reflections for diffraction imaging, Inverse Problems 21(1), 2005, 37 to 50
    locator: the definition of the RAAR map as a relaxation of the averaged alternating reflections, its pointwise form for a support constraint, and the analysis of its fixed points for convex sets (preprint arXiv math/0405208)
  - paper: doi:10.1364/JOSAA.19.001334
    title: Heinz H. Bauschke, Patrick L. Combettes and D. Russell Luke, Phase retrieval, error reduction algorithm, and Fienup variants, a view from convex optimization, Journal of the Optical Society of America A 19(7), 2002, 1334 to 1345
    locator: HIO with beta = 1 as the Douglas-Rachford algorithm, and the projection and reflection notation
---

Relaxed averaged alternating reflections (RAAR) is a fixed point iteration for [phase retrieval](/phase-retrieval/) and other problems of the form "find a point in two sets at once". Luke (2005) built it from the Douglas-Rachford step, which is [hybrid input-output](/hybrid-input-output/) with $\beta = 1$. Each step takes the average $\beta$ of the Douglas-Rachford step and $1 - \beta$ of the plain magnitude projection. For two convex sets that meet, the fixed points of RAAR are exactly the points in both sets, and the iterates converge. For phase retrieval the magnitude set is not convex, and RAAR is a heuristic that often escapes the stagnation of error reduction.

## In plain words

You look for a picture that obeys two rules: it must fit in a box, and its diffraction pattern must have the measured brightness. For each rule there is an easy repair: the nearest picture that obeys that rule.

A reflection goes past the repaired picture by the same distance again, like a mirror. One method reflects through the first rule, reflects through the second rule, and then goes half way back to the start. That method can drift when the data has noise. RAAR mixes it with the plain brightness repair. The mix keeps the drift small, and for simple rules the method stops only at a picture that obeys both rules.

## The problem

The input is the Fourier magnitude $A$ of an unknown image with $N$ pixels, a support mask $S$, and maybe nonnegativity. The output is an image in both sets $C$ (the images that fit the support and the sign) and $M$ (the images whose DFT has magnitude $A$). The method uses two nearest point maps: $P_S$ onto $C$ and $P_M$ onto $M$. $P_M$ is the magnitude step of [error reduction](/error-reduction-algorithm/). A reflection is $R = 2P - I$: it maps $x$ to the point on the other side of $P x$.

## The algorithm

```pseudo id=main
RAAR(A, S, x₀, K, β)
L1  x ← x₀
L2  for k ← 1 to K do
L3      p ← P_M(x)
L4      r ← 2p − x
L5      q ← P_S(r)
L6      x ← (β/2) · (2q − r + x) + (1 − β) · p
L7  return P_M(x)
```

Line L4 is the reflection $R_M x$, and $2q - r$ is $R_S R_M x$. So line L6 is

$$V(x) = \tfrac{\beta}{2}\bigl(R_S R_M x + x\bigr) + (1 - \beta) P_M x .$$

The first term is the Douglas-Rachford step, the average of $x$ and its double reflection. At $\beta = 1$ RAAR is that step, which is HIO with $\beta = 1$. Line L7 returns $P_M x$, which has the measured magnitude; the iterate $x$ itself is not the answer.

For a support without nonnegativity, $P_S$ keeps the values on $S$ and sets the rest to zero, and the step has a simple pointwise form, with $p = P_M x$:

- on $S$: the new value is $p$;
- off $S$: the new value is $\beta x + (1 - 2\beta) p$.

HIO gives $x - \beta p$ off $S$. The value of $\beta$ is tuned to the problem.

## Example

Use the $4 \times 4$ nonnegative object of the error reduction, HIO and difference map pages,

$$f = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 3 & 1 & 0 \\ 2 & 1 & 4 & 1 \\ 0 & 1 & 0 & 2 \end{pmatrix},$$

in the corner of an $8 \times 8$ frame, with the $4 \times 4$ support and nonnegativity. Start from the random image of seed 1, from which error reduction stops at the error 0.617. Take $\beta = 0.95$. The distance from the estimate $P_M x$ to the object set, $\|P_M x - P_S P_M x\|$, at step $k$ (measurements of the implementation):

| step $k$ | 0 | 1 | 2 | 5 | 10 | 20 | 50 | 100 | 150 | 200 | 250 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| distance | 6.2 | 5.6 | 3.4 | 1.1 | 0.26 | 0.04 | 7.9e-4 | 1.2e-5 | 2.6e-7 | 4.5e-9 | 1e-10 |

The estimate is the twin $f(3 - i, 3 - j)$ to within $3.2 \times 10^{-10}$. The twin has the same Fourier magnitude and fits the same support.

The value of $\beta$ matters. Over the random starts of seeds 1, 2 and 3, with 300 steps:

| $\beta$ | 0.5 | 0.7 | 0.8 | 0.9 | 0.95 |
|---|---|---|---|---|---|
| starts that reach a solution | 0 of 3 | 1 of 3 | 2 of 3 | 2 of 3 | 3 of 3 |

With $\beta = 0.5$ every start stagnates, as error reduction does. These numbers hold for this small example only.

## Correctness

The proof page proves these facts for two closed convex sets $A$ and $B$ in place of $C$ and $M$.

- **Firmly nonexpansive.** The reflections are nonexpansive, so the Douglas-Rachford step is firmly nonexpansive, and so is its convex combination with $P_B$.
- **Fixed points are solutions.** For $0 < \beta < 1$ and $A \cap B$ nonempty, $V(x) = x$ holds exactly for $x \in A \cap B$. At $\beta = 1$ only $P_B x$ is a solution, which is why the read-out is $P_M x$.
- **Convergence.** If $V$ has a fixed point, the distance from $x_k$ to each fixed point never grows, and $x_k$ converges to a fixed point.

$M$ is not convex, so none of this applies to phase retrieval. There, a fixed point need not give a solution, and there is no convergence proof. The example shows that RAAR can still find a solution where error reduction stagnates.

## Complexity

Each step does one magnitude projection, which is one forward and one inverse 2D DFT, and $O(N)$ other work. With a [fast Fourier transform](/fast-fourier-transform/) that is $O(N \log N)$ per step and $O(K N \log N)$ in total, the same as HIO and about half the cost of a step of the [difference map](/difference-map/) with Elser's parameters. The extra space is $O(N)$.

## Properties

- **Firmly nonexpansive** for convex sets, for every $\beta$ in $(0, 1]$.
- **Fixed points are solutions** for convex sets that meet and $\beta < 1$.
- **Not monotone** for phase retrieval. The error can grow for a while.
- **Generic.** It needs only the two nearest point maps.

## Variants and improvements

- **Douglas-Rachford and HIO.** The case $\beta = 1$.
- **[Difference map](/difference-map/).** Another family of fixed point maps built from the two projections; with suitable parameters it also contains HIO.
- **[Shrinkwrap](/shrinkwrap/).** The support can be updated during the run.
- **Many sets.** As with the difference map, several constraints can be written as two sets in a product space.
- **[Ptychography](/ptychography/).** Projection methods of the same kind are used with many overlapping measurements.

## When to use it

Use RAAR in place of HIO when the data is noisy, when the support is only roughly known, or when HIO does not settle. It costs the same per step. Try several values of $\beta$ and several starts, and read the answer from $P_M x$.

## Pitfalls

- **Reading $x$.** The iterate $x$ is not the answer. Use $P_M x$, or the result of a few steps of error reduction from it.
- **A small $\beta$.** With $\beta = 0.5$, every start in the example stagnates, as error reduction does.
- **Convex theory for a nonconvex problem.** The fixed point and convergence results hold for convex sets. They do not apply to the magnitude set.
- **Mixed conventions.** Papers swap the names of the two sets. Check the case $\beta = 1$ against HIO on your own code.

## Implementations

## History

The Douglas-Rachford method comes from the numerical solution of heat flow problems in the 1950s and was later studied as a splitting method for monotone operators. Bauschke, Combettes and Luke (2002) showed that Fienup's HIO with $\beta = 1$ is the Douglas-Rachford method for phase retrieval. Luke (2005) proposed RAAR as a relaxation of this method. He studied the fixed points for convex sets, also for sets that do not meet, where the Douglas-Rachford method has no fixed points.

## References
