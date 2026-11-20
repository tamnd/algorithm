---
tag: CRHCPN
kind: algorithm
slug: difference-map
name: Difference map
aliases:
- Elser difference map
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: "Find a point in the intersection of two sets, such as a support set and a Fourier magnitude set, by a fixed point map built from both projections. With gamma_S = -1 and gamma_M = 1/beta it is HIO."
solves: [phase-retrieval]
model: real-ram
complexity:
  vars: {N: the number of pixels, K: the number of iterations}
  time: {worst: O(K N log N)}
  space: {extra: O(N)}
properties: {deterministic: true, online: false, in_place: false, exact: false}
history:
  year: 2003
  people: [Veit Elser]
  note: Elser introduced the difference map for phase retrieval with a support, as a family of fixed point maps that contains Fienup's hybrid input-output.
prereqs: [hybrid-input-output, phase-retrieval]
see_also: [raar, error-reduction-algorithm, shrinkwrap, convex-feasibility-problem, fixed-point-iteration, coherent-diffraction-imaging, charge-flipping, crystallographic-phase-problem]
sources:
  - paper: doi:10.1364/JOSAA.20.000040
    title: Veit Elser, Phase retrieval by iterated projections, Journal of the Optical Society of America A 20(1), 2003, 40 to 55
    locator: the definition of the difference map with the estimates f_1 and f_2, the choice gamma_1 = -1/beta and gamma_2 = 1/beta, the read-out of the solution at a fixed point, and the relation to HIO (preprint arXiv math/0111080)
  - paper: doi:10.1088/0266-5611/21/1/004
    title: D. Russell Luke, Relaxed averaged alternating reflections for diffraction imaging, Inverse Problems 21(1), 2005, 37 to 50
    locator: the statement that HIO for the support constraint is the difference map with gamma_1 = -1 and gamma_2 = 1/beta (preprint arXiv math/0405208)
  - paper: doi:10.1364/JOSAA.19.001334
    title: Heinz H. Bauschke, Patrick L. Combettes and D. Russell Luke, Phase retrieval, error reduction algorithm, and Fienup variants, a view from convex optimization, Journal of the Optical Society of America A 19(7), 2002, 1334 to 1345
    locator: HIO with beta = 1 as the Douglas-Rachford algorithm
---

The difference map is a fixed point iteration for [phase retrieval](/phase-retrieval/) and other problems of the form "find a point in two sets at once". It uses only the two projections: here $P_S$ onto the images that fit the support, and $P_M$ onto the images whose Fourier transform has the measured magnitude. Elser (2003) built it so that every fixed point gives a solution through a simple read-out, unlike the fixed points of error reduction. It is a family with parameters $\beta$, $\gamma_S$ and $\gamma_M$. The choice $\gamma_S = -1$, $\gamma_M = 1/\beta$ gives Fienup's [hybrid input-output](/hybrid-input-output/) with feedback $\beta$; Elser's own choice is $\gamma_S = -1/\beta$, $\gamma_M = 1/\beta$, and the two agree at $\beta = 1$.

## In plain words

You look for a picture that obeys two rules: it must fit in a box, and its diffraction pattern must have the measured brightness. For each rule there is an easy repair: the nearest picture that obeys that rule.

The difference map makes two estimates from the current guess. One estimate first moves the guess a little with the box repair, then repairs the brightness. The other estimate does the same in the other order. If both rules can be met, a good guess makes the two estimates agree. So the map moves the guess by the difference between the two estimates.

When the guess stops moving, the two estimates agree, and that common picture obeys both rules. The guess itself is only a tool to get there.

## The problem

The input is the Fourier magnitude $A$ of an unknown image with $N$ pixels, a support mask $S$, and maybe nonnegativity. The output is an image in both sets $C$ (the images that fit the support and the sign) and $M$ (the images whose DFT has magnitude $A$). The method needs only the two maps $P_S$ and $P_M$, each a nearest point map onto its set. $P_M$ is the magnitude step of [error reduction](/error-reduction-algorithm/).

## The algorithm

```pseudo id=main
DIFFERENCE-MAP(A, S, x₀, K, β, γ_S, γ_M)
L1  x ← x₀
L2  for k ← 1 to K do
L3      f_S ← (1 + γ_S) · P_S(x) − γ_S · x
L4      f_M ← (1 + γ_M) · P_M(x) − γ_M · x
L5      x ← x + β · (P_S(f_M) − P_M(f_S))
L6  return P_M(f_S)
```

Lines L3 and L4 make the two estimates. Line L5 moves $x$ by $\beta$ times the difference of the projected estimates. Line L6 is the read-out: at a fixed point, $P_M(f_S)$ and $P_S(f_M)$ are equal, and the common value is a solution. Each step calls $P_M$ twice and $P_S$ twice. In Elser's notation the support constraint is $\pi_1$ and the magnitude constraint is $\pi_2$; changing the sign of $\beta$ exchanges the roles of the two sets.

The parameters:

- Elser's choice is $\gamma_S = -1/\beta$ and $\gamma_M = 1/\beta$. The value of $\beta$ is tuned to the problem.
- With $\gamma_S = -1$, $\gamma_M = 1/\beta$ and a support constraint only, line L3 gives $f_S = x$, and the step is HIO with feedback $\beta$ (Luke 2005 states this; the proof below checks it).
- With $\beta = 1$, $\gamma_S = -1$ and $\gamma_M = 1$, it is the Douglas-Rachford step $x + P_S(2P_M x - x) - P_M x$.

## Example

Use the $4 \times 4$ nonnegative object of the error reduction and HIO pages,

$$f = \begin{pmatrix} 1 & 2 & 0 & 1 \\ 0 & 3 & 1 & 0 \\ 2 & 1 & 4 & 1 \\ 0 & 1 & 0 & 2 \end{pmatrix},$$

in the corner of an $8 \times 8$ frame, with the $4 \times 4$ support and nonnegativity. Take $\beta = 0.9$, $\gamma_S = -1/0.9$ and $\gamma_M = 1/0.9$, and the random start of seed 1, from which error reduction stops at the error 0.617. The gap $\|P_S(f_M) - P_M(f_S)\|$ at step $k$ (measurements of the implementation):

| step $k$ | 0 | 1 | 2 | 5 | 10 | 20 | 50 | 100 | 150 | 200 | 249 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gap | 6.3 | 5.9 | 4.5 | 1.4 | 0.55 | 0.079 | 0.0011 | 1.1e-6 | 0.095 | 1.5e-5 | 1.7e-8 |

The gap falls to $10^{-6}$, jumps back up to $0.095$ near step 150, and then falls again to $10^{-8}$. The read-out is the twin $f(3 - i, 3 - j)$ of the object to within $3 \times 10^{-8}$; the twin has the same Fourier magnitude and fits the same support. Seeds 2 and 3 also reach a gap below $10^{-6}$ within 250 steps.

## Correctness

Three facts are proved below.

- **Fixed points give solutions.** If $D(x) = x$ and $\beta \ne 0$, then $P_S(f_M(x)) = P_M(f_S(x))$. The left side is in the support set and the right side is in the magnitude set, so the common image is in both.
- **Solutions are fixed points.** For a solution $z$, both projections leave $z$ unchanged, so $f_S(z) = f_M(z) = z$ and $D(z) = z$, for all parameters.
- **HIO is a special case.** With $\gamma_S = -1$, $\gamma_M = 1/\beta$ and a linear support projection, $D(x) = x + (\beta + 1)P_S P_M x - P_S x - \beta P_M x$. This is $P_M x$ on the support and $x - \beta P_M x$ off it: the HIO step.

There is no theorem that the iteration reaches a fixed point. The magnitude set is not convex. The gap is not monotone, as the example shows.

## Complexity

Each step does two magnitude projections, each one forward and one inverse 2D DFT, and $O(N)$ other work. With a [fast Fourier transform](/fast-fourier-transform/) that is $O(N \log N)$ per step and $O(K N \log N)$ in total, about twice the cost of an HIO step. In the HIO case $\gamma_S = -1$ one projection is not needed, because $f_S = x$. The extra space is $O(N)$.

## Properties

- **Fixed points are solutions** (through the read-out), for every choice of the parameters.
- **Not monotone.** The gap can grow for a while.
- **Symmetric in the two sets.** Changing the sign of $\beta$ swaps their roles.
- **Generic.** It needs only the two projections, so it applies to any problem that splits into two constraint sets with easy projections.

## Variants and improvements

- **[Hybrid input-output](/hybrid-input-output/).** The case $\gamma_S = -1$, $\gamma_M = 1/\beta$.
- **Douglas-Rachford.** The case $\beta = 1$, $\gamma_S = -1$, $\gamma_M = 1$.
- **[RAAR](/raar/).** Luke's relaxation of the Douglas-Rachford step, made for noisy and inconsistent data.
- **Many sets.** A problem with several constraints can be written as two sets in a product space: one set is the product of all constraint sets, and the other set holds the tuples whose copies are all equal. Then the difference map applies as it is.
- **[Shrinkwrap](/shrinkwrap/).** The support can be updated during the run, as with HIO.

## When to use it

Use the difference map when HIO stagnates or when you want one code for several constraint pairs. In phase retrieval with a support it is a direct alternative to HIO and RAAR; which works best depends on the data, and it is usual to try more than one. Read the answer from $P_M(f_S)$, not from $x$.

## Pitfalls

- **Reading $x$.** The iterate $x$ is not the answer. Use the read-out of line L6.
- **Mixed conventions.** Papers swap the names of the two sets, the sign of $\beta$, and the signs of the $\gamma$. Check the HIO special case on your own code before you trust a parameter value from a paper.
- **Stopping on a small gap.** The gap can be small for a short time and then grow, as in the example. Stop on a small gap that stays small, or check the read-out against the data.
- **Nonnegativity breaks linearity.** With a sign constraint, $P_S$ is not linear, and the HIO identity holds only approximately.

## Implementations

## History

Elser (2003) proposed the difference map in a paper on phase retrieval by iterated projections, with a preprint in 2001. He showed that at $\beta = 1$ it reproduces Fienup's HIO with feedback 1, and chose $\gamma_S = -1/\beta$ and $\gamma_M = 1/\beta$. Bauschke, Combettes and Luke (2002) had shown that HIO with $\beta = 1$ is Douglas-Rachford. Luke (2005) placed the difference map, HIO and his RAAR in one framework of reflections.

## References
