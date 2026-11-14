---
tag: KESX1E
kind: algorithm
slug: electrostatics-based-placement
name: Electrostatics-based placement
aliases:
- ePlace
area: eda/partitioning-floorplanning-and-placement
level: research
summary: Lu and coauthors' placement that models cells as charges, computes the density penalty as electric potential by FFT and minimizes with Nesterov's method.
solves: [placement-problem]
model: real-ram
complexity:
  vars: {n: the number of movable cells, P: the number of pins, M: the number of bins on each side of the grid, k: the number of iterations}
  time: {worst: "O(k (P + n + M^2 log M))", average: "O(k (P + n + M^2 log M))", best: "O(P + n + M^2 log M)"}
  space: {extra: "O(P + n + M^2)"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 2014
  people: [Jingwei Lu, Pengwen Chen, Chin-Chih Chang, Lu Sha, Dennis Jen-Hsin Huang, Chin-Chi Teng, Chung-Kuan Cheng]
  note: ePlace was presented at DAC 2014 and in the journal ACM TODAES in 2015; RePlAce (2019) added local density control and routability and made the method a widely used open-source placer.
prereqs: [analytical-placement, log-sum-exp-wirelength, poisson-equation, discrete-cosine-transform, nesterov-accelerated-gradient]
see_also: [force-directed-placement, simpl-placement, fast-fourier-transform, preconditioning, placement-legalization, detailed-placement, heat-equation, quadratic-placement]
sources:
  - paper: doi:10.1145/2699873
    title: Jingwei Lu, Pengwen Chen, Chin-Chih Chang, Lu Sha, Dennis Jen-Hsin Huang, Chin-Chi Teng and Chung-Kuan Cheng, ePlace, electrostatics-based placement using fast Fourier transform and Nesterov's method, ACM Transactions on Design Automation of Electronic Systems 20(2), article 17, 2015
    locator: the electrostatic density model, the spectral solution of Poisson's equation, Nesterov's method with a Lipschitz step estimate, and the preconditioner
  - paper: doi:10.1145/2593069.2593133
    title: Jingwei Lu, Pengwen Chen, Chin-Chih Chang, Lu Sha, Dennis Jen-Hsin Huang, Chin-Chi Teng and Chung-Kuan Cheng, ePlace, electrostatics based placement using Nesterov's method, Proceedings of the 51st Design Automation Conference (DAC), 2014
    locator: the conference version of the method
  - paper: doi:10.1109/TCAD.2018.2859220
    title: Chung-Kuan Cheng, Andrew B. Kahng, Ilgweon Kang and Lutong Wang, RePlAce, advancing solution quality and routability validation in global placement, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 38(9), 1717 to 1730, 2019
    locator: the extension of ePlace with local density functions and routability-driven cell inflation
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 4, Global and Detailed Placement (analytical global placement with a density penalty; general locator)
---

Electrostatics-based placement is a global placer for the [placement problem](/placement-problem/) in chip design. It treats each cell as a positive electric charge equal to its area. Crowded regions then have a high electric potential, and the electric field pushes the cells out of them. The density penalty is the potential energy of the system, found by solving [Poisson's equation](/poisson-equation/) on a grid of bins with cosine and sine transforms, computed by the [fast Fourier transform](/fast-fourier-transform/). The placer minimizes a smooth wirelength plus $\lambda$ times this energy by [Nesterov's method](/nesterov-accelerated-gradient/) with a diagonal preconditioner, and raises $\lambda$ until the overflow is small. ePlace (Lu and coauthors, 2014 and 2015) introduced the method, and RePlAce extended it. It is an [analytical placement](/analytical-placement/) method: a heuristic with a smooth objective, whose output is still to be legalized.

## In plain words

Think of every part of the circuit as a small charged ball. Balls with the same charge push each other away, and the push is strongest where many balls are packed together. The wires act like rubber bands that pull connected balls together.

The placer lets both forces act, a little at a time, and makes the push stronger step by step. In the end the balls are spread fairly evenly over the board, and the bands still keep connected balls near each other. A short cleanup step then puts each ball on an exact spot.

## The problem

The input is a netlist with $n$ movable cells of widths $W_i$ and heights $H_i$, fixed pads, nets $e$ with weights $w_e$, and $P$ pins, with every pin at the center of its cell. The region is the square $[0, MB] \times [0, MB]$, cut into $M \times M$ bins of side $B$. The output is a position for each cell in the region, with a small wirelength and a small overflow

$$ \tau = \frac{\sum_{\text{bins } b} \max(0, \rho_b - 1) B^2}{\sum_i W_i H_i}, $$

where $\rho_b$ is the cell area inside bin $b$ divided by $B^2$. Overlap is allowed in the output; the legalizer removes it.

**Electrostatics.** Let $\rho$ be the density on the grid, and $t = x / B$ the coordinate in bin units. The potential $\psi$ solves

$$ -\nabla^2 \psi = \rho - \bar\rho, \qquad \frac{\partial \psi}{\partial \mathbf{n}} = 0 \text{ on the border}, \qquad \int \psi = 0, $$

where $\bar\rho$ is the mean density, which must be removed for a solution to exist with this border condition. The field is $\xi = -\nabla \psi$. With $\omega_u = \pi u / M$ and the cosine coefficients $a_{uv}$ of $\rho$ (a 2D [discrete cosine transform](/discrete-cosine-transform/), with $a_{00} = \bar\rho$),

$$ \psi = \sum_{(u, v) \ne (0, 0)} \frac{a_{uv}}{\omega_u^2 + \omega_v^2} \cos(\omega_u t_x) \cos(\omega_v t_y), \qquad \xi_x = \frac1B \sum_{(u, v) \ne (0, 0)} \frac{a_{uv} \, \omega_u}{\omega_u^2 + \omega_v^2} \sin(\omega_u t_x) \cos(\omega_v t_y), $$

and $\xi_y$ in the same way. Every term has a zero normal derivative on the border, because $\sin(\omega_u t) = 0$ at $t = 0$ and $t = M$.

**Objective.** With the [log-sum-exp wirelength](/log-sum-exp-wirelength/) $W_\gamma$ and the energy $N = \frac12 \sum_i q_i \psi(x_i, y_i)$ with $q_i = W_i H_i$, minimize $f = W_\gamma + \lambda N$. ePlace takes the gradient of $N$ for cell $i$ as $-q_i \xi(x_i, y_i)$, the force on a charge in a field, and ignores the change of the field caused by the cell itself.

## The algorithm

```pseudo id=main
EPLACE(cells, nets, pads, M × M bins, γ, target τ*)
L1  put the cells near the center of the region (v ← u ← start)
L2  λ ← Σ|∇W_γ| / Σ q_i |ξ_i| at the start; a ← 1
L3  repeat
L4      ρ ← bin densities of the cells at v
L5      a_uv ← DCT of ρ; ψ, ξ ← potential and field from a_uv / (ω_u² + ω_v²)
L6      g_i ← (∇_i W_γ(v) − λ q_i ξ(v_i)) / (|E_i| + λ q_i)       ▷ preconditioned gradient
L7      α ← |v − v_prev| / |g − g_prev|                            ▷ inverse Lipschitz estimate
L8      u_new ← clamp(v − α g) to the region
L9      a_new ← (1 + √(4a² + 1)) / 2; v ← clamp(u_new + (a − 1)/a_new · (u_new − u)); u ← u_new; a ← a_new
L10     λ ← 1.1 λ
L11 until τ(v) ≤ τ*
L12 return u
```

Line L5 is the electrostatic step. The forward transform is a DCT, and the potential and the two field components are inverse transforms of the same coefficients with cosines and sines. With the FFT each costs $O(M^2 \log M)$. In line L6, $|E_i|$ is the number of nets of cell $i$; ePlace divides by this approximate diagonal of the Hessian so that cells of very different sizes move at similar speeds. Line L7 is the step of ePlace: the inverse of a local estimate of the Lipschitz constant of the gradient, from the last two points. Line L9 is Nesterov's update: $u$ is the main sequence and $v$ the look-ahead point. ePlace changes $\lambda$ by a factor near 1 that depends on the change of HPWL in the last step; the implementation here uses the fixed factor 1.1.

## Example

**Potential of one full bin.** A grid of $2 \times 2$ bins of side 1 has all cell area in bin $(0, 0)$: $\rho = 2$ there and 0 in the other three bins, so $\bar\rho = \frac12$. Then $\omega_1 = \pi / 2$, and the coefficients are $a_{00} = \frac12$, $a_{10} = a_{01} = \frac{\sqrt2}{2}$ and $a_{11} = 1$. At the bin centers:

| bin | $\rho$ | $\psi$ | $\xi_x$ | $\xi_y$ |
| --- | --- | --- | --- | --- |
| $(0, 0)$ | 2 | $\frac{5}{\pi^2} \approx 0.5066$ | $\frac{3}{2\pi} \approx 0.4775$ | $\frac{3}{2\pi}$ |
| $(1, 0)$ | 0 | $-\frac{1}{\pi^2} \approx -0.1013$ | $\frac{3}{2\pi}$ | $\frac{1}{2\pi} \approx 0.1592$ |
| $(0, 1)$ | 0 | $-\frac{1}{\pi^2}$ | $\frac{1}{2\pi}$ | $\frac{3}{2\pi}$ |
| $(1, 1)$ | 0 | $-\frac{3}{\pi^2} \approx -0.3040$ | $\frac{1}{2\pi}$ | $\frac{1}{2\pi}$ |

For example $\psi(0, 0) = \frac{a_{10}}{\omega_1^2} \cdot \frac{\sqrt2}{2} + \frac{a_{01}}{\omega_1^2} \cdot \frac{\sqrt2}{2} + \frac{a_{11}}{2 \omega_1^2} \cdot \frac12 = \frac{2}{\pi^2} + \frac{2}{\pi^2} + \frac{1}{\pi^2}$. The potential is highest in the full bin and lowest in the far corner, and the field points from the full bin toward the empty ones in every bin. The four potentials sum to 0, and the energy is $N = \frac12 \cdot 2 \cdot \frac{5}{\pi^2} = \frac{5}{\pi^2}$. The tests check these values against the direct sums.

**A run.** On 5 random netlists of 16 unit cells in an $8 \times 8$ region with unit bins (seed 14, all cells started within 0.1 of the center), the overflow starts at 0.75 and falls below the target 0.1 in 16 to 22 iterations. With 32 cells it starts at 0.875 and needs 25 to 95 iterations.

## Correctness

The electrostatic part is exact: the coefficients $a_{uv}$ reproduce $\rho$ at the bin centers, the series $\psi$ solves Poisson's equation with the border condition for the cosine interpolant of $\rho - \bar\rho$, and $\xi$ is $-\nabla \psi$. See the [proof](proofs/correctness.md). The tests check the transform against the direct formula, the Poisson equation by finite differences at the bin centers, the field by finite differences of $\psi$, and the gradient of $W_\gamma$ by finite differences.

The optimization has no such guarantee. Nesterov's method reaches error $O(1/k^2)$ for a convex function with a Lipschitz gradient and a fixed step, but $N$ is not convex, $\lambda$ changes at every step, and the step of line L7 is an estimate. So the placer is a heuristic: it stops when the overflow is small, not at a proved optimum.

## Complexity

- **Wirelength.** The value and the gradient of $W_\gamma$ cost $O(P)$.
- **Density.** With no cell larger than a few bins, line L4 costs $O(n + M^2)$.
- **Transforms.** One DCT and three inverse transforms by the FFT, $O(M^2 \log M)$. The implementation here uses separable direct sums, $O(M^3)$, which is simpler and fast enough for small grids.
- **Field at the cells and the update.** $O(n)$.

So $k$ iterations cost $O(k (P + n + M^2 \log M))$ time and $O(P + n + M^2)$ space. With about one bin per cell, $M^2 \approx n$, and the transforms cost $O(n \log n)$ per iteration.

## Properties

**What is proved.**

- The coefficients $a_{uv}$ give back $\rho$ exactly at the bin centers, and $a_{00}$ is the mean density.
- The series $\psi$ solves $-\nabla^2 \psi = \rho - \bar\rho$ for the cosine interpolant of $\rho$, with a zero normal derivative on the border, and $\xi = -\nabla \psi$. A uniform density gives $\psi = 0$ and no field.
- The method stops after the iteration limit, and each iteration costs the time above.

**What is measured.** The numbers in the example come from the implementation on toy inputs, not from benchmarks. ePlace was measured on the ISPD 2005 and 2006 benchmarks against the placers of its time, and RePlAce on the same suites and on routability benchmarks; both report smaller HPWL than the earlier analytical placers at the same target density. See those papers for the numbers. None of those results has a proof.

## Variants and improvements

- **Weighted average wirelength.** ePlace uses the weighted average model instead of LSE (see the [log-sum-exp wirelength](/log-sum-exp-wirelength/) page). It is closer to HPWL for the same $\gamma$.
- **Smoothing $\gamma$ with the overflow.** ePlace ties $\gamma$ to the overflow, large at the start and small at the end, so the wirelength gets sharper as the cells spread.
- **Mixed size.** ePlace-MS places macros and standard cells together, with the macros as large charges, and then fixes the macros before the cells are finished.
- **RePlAce.** Adds a local density per bin, so the penalty adapts to the region, and routability-driven inflation of cells in congested regions.
- **GPU placers.** DREAMPlace runs the same model as a deep learning toolkit on a GPU, with the transforms and gradients as batched operations.
- **Other density penalties.** Earlier analytical placers, such as NTUplace3, use a bell-shaped smoothing of the bin density instead of a potential. [Force-directed placement](/force-directed-placement/) in Kraftwerk also uses a potential from Poisson's equation, but with a quadratic wirelength and a linear solve.

## When to use it

Use an electrostatics-based placer for large standard cell and mixed-size designs when you want the best wirelength from global placement and can afford a few hundred gradient iterations. The density penalty is global, so it spreads cells smoothly over the whole region, and the cost per iteration is near linear. For a quick placement, a quadratic placer such as [SimPL](/simpl-placement/) is simpler and often faster. The output must still go through [legalization](/placement-legalization/) and [detailed placement](/detailed-placement/).

## Pitfalls

- **Forgetting to remove the mean.** With zero normal derivative on the border, Poisson's equation has a solution only if the source has zero mean. Drop the term $(0, 0)$.
- **The wrong transform.** The border condition calls for a cosine series. A plain FFT of $\rho$ assumes a periodic region, where a cell at the right edge pushes cells at the left edge.
- **A grid too coarse.** If a bin is much larger than a cell, the density inside a bin is flat and cells in the same bin feel no force from each other.
- **The step without a bound.** The estimate of line L7 can be very large when the gradient barely changes; ePlace backtracks if the estimate is not consistent. The implementation here caps $\alpha$ at one bin.
- **Exponent overflow.** Use the shift by the maximum in $W_\gamma$, as on the log-sum-exp page.

## Implementations

## History

Lu, Chen, Chang, Sha, Huang, Teng and Cheng presented ePlace at DAC 2014 and in ACM TODAES in 2015. The electrostatic analogy of density was older: Kraftwerk (1998) used Poisson's equation for its spreading forces. The new parts of ePlace were the global charge model with a spectral solver, Nesterov's method with a Lipschitz step estimate, and the preconditioner. ePlace-MS (2015) handled mixed-size designs, and RePlAce (Cheng, Kahng, Kang and Wang, 2019) added local density control and routability; RePlAce became the global placer of the OpenROAD flow.

## References
