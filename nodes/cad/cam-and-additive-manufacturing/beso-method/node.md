---
tag: 0GMFJK
kind: algorithm
slug: beso-method
name: Bidirectional evolutionary structural optimization
aliases:
- BESO
- evolutionary structural optimization
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Ranks elements by strain energy density and lowers the volume step by step, removing the weakest solid elements and adding back void ones, so the design stays 0/1 at every iteration.
solves: [topology-optimization]
model: real-ram
complexity:
  vars: {n: number of elements, s: time of one finite element solve, k: number of iterations}
  time: {worst: O(k (s + n log n))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1998
  people: [Osvaldo M. Querin, Grant P. Steven, Yi Min Xie, Xiaodong Huang]
  note: Xie and Steven proposed the one-way removal method in 1993. Querin, Steven and Xie made it bidirectional in 1998, and Huang and Xie gave the form with a filter and history averaging in 2007.
prereqs: [topology-optimization, finite-element-method]
see_also: [simp-method, density-filtering, level-set-topology-optimization, knapsack-problem, fractional-knapsack, greedy-algorithm, homogenization-method, gaussian-elimination]
sources:
  - paper: doi:10.1016/0045-7949(93)90035-C
    title: Y. M. Xie and G. P. Steven, A simple evolutionary procedure for structural optimization, Computers and Structures 49(5), 1993, 885 to 896
    locator: the removal of the elements with the lowest stress, step by step, until the design reaches a steady state
  - paper: doi:10.1108/02644409810244129
    title: O. M. Querin, G. P. Steven and Y. M. Xie, Evolutionary structural optimisation (ESO) using a bidirectional algorithm, Engineering Computations 15(8), 1998, 1031 to 1048
    locator: adding elements next to the most stressed regions as well as removing the least stressed ones
  - paper: doi:10.1016/j.finel.2007.06.006
    title: X. Huang and Y. M. Xie, Convergent and mesh-independent solutions for the bi-directional evolutionary structural optimization method, Finite Elements in Analysis and Design 43(14), 2007, 1039 to 1049
    locator: the sensitivity numbers, the mesh-independency filter, the averaging with the previous iteration, the evolutionary volume ratio and the stop rule on the compliance
  - book: isbn:978-0-470-74653-0
    title: Xiaodong Huang and Yi Min Xie, Evolutionary Topology Optimization of Continuum Structures, Methods and Applications, Wiley, 2010
    locator: the soft-kill BESO with a material interpolation scheme and the admission ratio (general locator)
  - paper: doi:10.1007/s001580050170
    title: M. Zhou and G. I. N. Rozvany, On the validity of ESO type methods in topology optimization, Structural and Multidisciplinary Optimization 21(1), 2001, 80 to 83
    locator: a small example where the element removal of ESO gives a highly nonoptimal design
---

Bidirectional evolutionary structural optimization (BESO) is a method for [topology optimization](/topology-optimization/) that keeps every element either solid or void. It starts from the full design domain and lowers the volume by a small ratio at each iteration. After each [finite element](/finite-element-method/) solve, it gives every element a sensitivity number, the strain energy per unit volume, and keeps the elements with the highest numbers up to the current target volume. Solid elements with low numbers are removed, and void elements with high numbers come back, which is the "bidirectional" part. The older method of Xie and Steven (1993) only removed elements. Querin, Steven and Xie (1998) added the reverse step, and Huang and Xie (2007) added a filter and an average with the previous iteration, which make the results stable on fine meshes. BESO is simple and gives crisp designs, but it has no general proof of convergence or of optimality. This page proves what holds for a network of bars: the sensitivity is the derivative of the compliance, the method is optimal for parallel bars with equal areas, and it is a greedy knapsack rule, worse than the optimum by any factor, when the areas differ.

## In plain words

Start with a solid block. Push on it and see which small pieces work hard and which hardly work at all. Remove a few of the lazy pieces, so the block gets a little lighter. Push again. Some pieces that were removed may now be needed, so put the most useful of them back.

Repeat until the block has the target weight and stops changing. What is left is a frame of members that carry the load. At every step each piece is either fully there or fully gone, so the result needs no rounding at the end.

## The problem

The design domain is divided into $n$ elements, and element $e$ has the volume $v_e$ and the variable $x_e \in \{x_{\min}, 1\}$. The stiffness of the structure is $K(x) = \sum_e x_e^p K_e$, where $K_e$ is the element matrix of the solid material and $p \ge 1$. A void element keeps the small stiffness $x_{\min}^p K_e$, which is the soft-kill form, so the solve is always defined. The goal is

$$\min_x\ c(x) = f^{\mathsf T} u \quad\text{subject to}\quad K(x) u = f,\quad \sum_e x_e v_e \le V^*,\quad x_e \in \{x_{\min}, 1\}.$$

**The sensitivity number.** As on the [SIMP page](/simp-method/), $\partial c / \partial x_e = -p\, x_e^{p-1} u_e^{\mathsf T} k_e u_e$. BESO uses

$$\alpha_e = \frac{1}{2}\, \frac{x_e^{p-1}\, u_e^{\mathsf T} k_e u_e}{v_e} = -\frac{1}{2p\,v_e} \frac{\partial c}{\partial x_e}.$$

For a solid element this is its strain energy per unit volume. For a void element it is $x_{\min}^{p-1}$ times that of the solid element with the same displacements. With $x_{\min} = 10^{-3}$ and $p = 3$ the factor is $10^{-6}$. A void element ranks high only when its displacements are very large, which is what happens when the remaining solid parts lose their connection.

## The algorithm

```pseudo id=main
BESO(mesh, f, V*, ER, p, x_min, AR_max, τ, N)
L1  x_e ← 1 for every element; V ← Σ v_e
L2  for k = 1 to maxit do
L3      solve K(x) u = f; C_k ← fᵀu
L4      if V = V* and k > 2N and |Σ_{last N} C − Σ_{previous N} C| ≤ τ Σ_{last N} C then stop
L5      α_e ← ½ x_e^(p−1) u_eᵀ k_e u_e / v_e      ▷ filtered on a continuum mesh
L6      if k > 1 then α_e ← (α_e + α_e^prev) / 2;  α^prev ← α
L7      V ← max(V*, V (1 − ER))
L8      S ← the longest prefix of the elements sorted by decreasing α with Σ_{e∈S} v_e ≤ V
L9      if more than AR_max·n elements of S are void then
            keep the best AR_max·n of those voids, then fill with solid elements by α up to V
L10     x_e ← 1 for e in S and x_min for the other elements
L11 return x
```

Line L7 is the volume schedule: the target falls by the evolutionary ratio ER (often 1% to 2%) per iteration until it reaches $V^*$. Line L8 is the threshold of Huang and Xie: the solid set is the elements whose sensitivity is above a level, chosen so that the volume meets the target. Line L9 is the admission limit: when too many voids would turn solid at once, only the best of them do, which keeps the design from jumping. Line L6 averages each number with its value from the previous iteration. Huang and Xie (2007) found that this stops the design from oscillating between two states. On a continuum mesh, line L5 also smooths the numbers over a radius $r_{\min}$, with the cone weights of the sensitivity filter of the [SIMP page](/simp-method/). The filter also gives void elements a number from their solid neighbors, so material grows next to stressed regions. Line L4 stops when the compliance over the last $N$ iterations (often 5) differs from the $N$ before by a relative amount of at most $\tau$.

## Example

The test structure is a set of parallel bars between a wall and a rigid plate, with a unit load on the plate and $E = 1$. Every bar stretches by the same $\delta = F / \sum_e x_e^p A_e / L_e$, so by line L5 a solid bar has $\alpha_e = \delta^2 / (2 L_e^2)$, whatever its area.

**Equal areas.** Six bars of area 1 have the lengths 1 to 6, so the total volume is 21. Take $V^* = 10$, ER $= 1/10$, $p = 3$ and $x_{\min} = 1/1000$. The shorter a bar, the higher its number, so line L8 keeps the shortest bars that fit:

| iteration | target $V$ | solid bars (lengths) | volume | compliance |
|---|---|---|---|---|
| 0 | 21 | 1, 2, 3, 4, 5, 6 | 21 | 0.4082 |
| 1 | 18.9 | 1, 2, 3, 4, 5 | 15 | 0.4380 |
| 2, 3 | 17.01, 15.31 | 1, 2, 3, 4, 5 | 15 | 0.4380 |
| 4 to 7 | 13.78 down to 10.04 | 1, 2, 3, 4 | 10 | 0.4800 |
| 8 to 13 | 10 | 1, 2, 3, 4 | 10 | 0.4800 |

The compliance of the full design is $1/(1 + 1/2 + \dots + 1/6) = 20/49 \approx 0.4082$, and that of the final design is $1/(1 + 1/2 + 1/3 + 1/4) = 12/25 = 0.48$, plus a term of order $10^{-9}$ from the void bars. The run stops after 14 solves, when the compliance has not changed over two windows of 5. The volume falls in jumps, not smoothly, because a bar is either in or out: at iteration 1 the target is 18.9 but the design has volume 15. Brute force over all $2^6$ designs confirms that $\{1, 2, 3, 4\}$ is the best design with volume at most 10.

**Unequal areas.** Two bars: bar 1 with $L = 1$, $A = 1$ (stiffness 1, volume 1), and bar 2 with $L = 1.1$, $A = 10$ (stiffness $100/11 \approx 9.09$, volume 11). The target is $V^* = 11$ and ER $= 1/50$. Bar 1 has the higher number, $\delta^2/2$ against $\delta^2/2.42$. At the first target, 11.76, both bars together have volume 12, so line L8 keeps bar 1 alone. Bar 2 is now void, its number is a factor $10^{-6}$ smaller, and it never returns. BESO ends with compliance about 1.0. The best design is bar 2 alone, with compliance $11/100 = 0.11$. BESO is 9.09 times softer than the optimum.

**Random networks.** On 100 random networks of 4 nodes on a line (the wall at the first node, a unit load at the last, a chain of 3 bars of area 1 and 4 to 7 more bars between random node pairs with areas 1 to 3, seed 3, $V^*$ half the total volume), BESO matched the brute force optimum within $10^{-6}$ on 28 networks and came within 10% on 43. The median ratio was 1.17 and the worst 3.0. These are measurements on small discrete examples, where the jumps of the volume are large, and they say nothing about fine continuum meshes.

## Correctness

What is proved for the method as stated: every design after the first meets the current target volume, the targets reach $V^*$ after $\lceil \ln(V^*/V_0)/\ln(1 - \text{ER}) \rceil$ iterations, and the loop stops after maxit iterations. The sensitivity is $-\frac{1}{2p v_e}$ times the derivative of the compliance, by differentiating $K u = f$. So line L8 ranks the elements by the first order gain per unit volume.

For parallel bars with equal areas and distinct lengths, the method is optimal. By induction the solid set is always a prefix of the bars sorted by length, and a removed bar never fits again, because the targets only fall. So BESO ends at the longest prefix that fits in $V^*$. Any feasible set with $s$ bars has at least the total length of the $s$ shortest bars, so $s$ is at most the length of that prefix, and its stiffness $\sum 1/L_e$ is at most that of the prefix. With unequal areas the problem is a [0/1 knapsack](/knapsack-problem/) with value $A_e/L_e$ and weight $A_e L_e$, and BESO takes the bars in the order of value per weight. That rule is optimal for the [fractional knapsack](/fractional-knapsack/), not for the 0/1 one, and the two bar example shows a gap that grows without bound as the second area grows.

**What is not proved.** BESO has no general proof of convergence. The averaging and the stop rule are measured to work well, but the 0/1 iterates can cycle, and nothing bounds the gap to the optimum. Zhou and Rozvany (2001) gave a small example where the element removal of the earlier ESO method gives a highly nonoptimal design. The full proofs of the statements above are in [the correctness proof](proofs/correctness.md).

**What the tests check.** The solver against the closed forms for bars in parallel and in series, the sensitivity against an exact central difference of the compliance, the equal area case and random equal area cases against brute force, the knapsack counterexample, and the volume and feasibility on random networks.

## Complexity

Each iteration does one finite element solve, of time $s$, then computes $n$ sensitivity numbers, filters them in $O(n r^2)$ time on a 2D grid with filter radius $r$, and sorts them in $O(n \log n)$. With a [bisection](/bisection-method/) on the threshold instead of a sort, the selection is $O(n)$ per step of the bisection. So $k$ iterations take $O(k(s + n \log n))$, and the solve is most of the time on real meshes. The space is $O(n)$ for the numbers and the design, plus the solver.

The number of iterations is at least $\lceil \ln(V^*/V_0) / \ln(1 - \text{ER}) \rceil$ to reach the volume, which is 35 for $V^*/V_0 = 1/2$ and ER $= 2\%$, plus at least $2N$ to pass the stop test. On the random networks above the runs took 36 to 47 solves. No formula bounds the number of iterations after the target is reached; the code stops at maxit.

## Properties

- **0/1 designs.** Every iterate is solid or void, so there is no gray material to round at the end.
- **Feasible volume.** Every design after the first meets the current target.
- **First order ranking.** The sensitivity number is the derivative of the compliance per unit volume, scaled by a positive constant.
- **Heuristic.** It has no general proof of convergence and no bound on the gap to the optimum.
- **Volume in jumps.** On coarse meshes the volume can fall well below the target in one step.
- **Deterministic.** With a fixed tie rule the result depends only on the input and the parameters.

## Variants and improvements

- **ESO.** The one-way method of Xie and Steven (1993) only removes elements, by a stress or energy criterion. A removed element cannot return, which is the weakness that Zhou and Rozvany (2001) showed.
- **Hard kill.** Void elements are deleted from the mesh instead of kept at $x_{\min}$. The solve is smaller, but a void element has no displacement, so its number must come from the filter.
- **Soft kill with interpolation.** Huang and Xie use $x_{\min}$ and the power $p$ as in SIMP, which gives void elements a defined number and lets the method treat several materials.
- **Other objectives.** Natural frequencies, displacement constraints and several load cases change the sensitivity number, not the selection.
- **Filters.** The mesh-independency filter is the same as the sensitivity filter of SIMP. See [density filtering](/density-filtering/) for the filter on the densities and its properties.

## When to use it

Use BESO when a crisp 0/1 design is needed at every iteration, for example when the next step of the work reads the layout directly, or when the analysis code can only switch elements on and off. It is easy to add to an existing finite element code, because it needs only element energies. For problems with several constraints or a need for a certificate of optimality, a gradient method on a relaxed problem, such as [SIMP](/simp-method/) with a general optimizer, is the safer choice.

## Pitfalls

- **Claiming convergence.** The stop rule says that the compliance stopped changing. It does not prove a local optimum.
- **An admission limit of zero.** A limit of AR_max times $n$, rounded down, is 0 on a small model, and then no void element can ever return. The code of this page uses at least 1.
- **No averaging.** Without line L6 the design often flips between two states on fine meshes.
- **A large ER.** Large volume steps remove members that later turn out to be needed, and on coarse meshes the volume jumps far below the target.
- **Disconnected designs.** If the solid set loses its path from the load to the supports, the soft-kill solve still works, but the compliance is huge. With hard kill the matrix becomes singular.
- **Reading the volume as the target.** The final volume is at most $V^*$ and can be smaller, as the 6 bar example shows at iteration 1.

## Implementations

## History

Xie and Steven (1993) proposed evolutionary structural optimization: remove the least stressed elements, a few at a time, until the design stops changing. Querin, Steven and Xie (1998) made it bidirectional by adding elements near the most stressed regions. Zhou and Rozvany (2001) showed with a small example that the removal rule can give a design far from the optimum, which started a debate on the method. Huang and Xie (2007) gave the form used today: sensitivity numbers from the compliance, a mesh-independency filter, an average with the previous iteration and a stop rule on the compliance. Their 2010 book collects the soft-kill form with material interpolation and many applications.

## References
