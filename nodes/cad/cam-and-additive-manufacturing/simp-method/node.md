---
tag: KDKEWF
kind: algorithm
slug: simp-method
name: SIMP method
aliases:
- solid isotropic material with penalization
area: cad/cam-and-additive-manufacturing
level: advanced
summary: Gives each element a density between 0 and 1 and a stiffness that grows as a power of it, so intermediate densities are penalized, and updates by optimality criteria.
solves: [topology-optimization]
model: real-ram
complexity:
  vars: {n: number of elements, h: number of elements across the short side, r: filter radius in elements, k: number of iterations}
  time: {worst: "O(k n (h^2 + r^2))"}
  space: {extra: "O(n (h + r^2))"}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1989
  people: [Martin P. Bendsøe]
  note: Bendsøe proposed the power law for the stiffness of a density in 1989. Sigmund published the 99 line code with the optimality criteria update and the sensitivity filter in 2001.
prereqs: [topology-optimization, finite-element-method]
see_also: [level-set-topology-optimization, kkt-conditions, lagrange-multiplier, bisection-method, projected-gradient-descent, cholesky-decomposition, sparse-linear-systems, support-structure-generation]
sources:
  - paper: doi:10.1007/BF01650949
    title: Martin P. Bendsøe, Optimal shape design as a material distribution problem, Structural Optimization 1(4), 1989, 193 to 202
    locator: the density of each point with the stiffness given as a power of the density, which penalizes intermediate densities
  - paper: doi:10.1007/s001580050176
    title: Ole Sigmund, A 99 line topology optimization code written in Matlab, Structural and Multidisciplinary Optimization 21(2), 2001, 120 to 127
    locator: the MBB beam problem, the optimality criteria update with move limit 0.2 and damping 1/2, the bisection on the multiplier and the mesh-independency filter
  - book: isbn:978-3-540-42992-0
    title: Martin P. Bendsøe and Ole Sigmund, Topology Optimization, Theory, Methods and Applications, Springer, 2003
    locator: the chapter on the minimum compliance problem (the SIMP interpolation, the optimality criteria method, checkerboards and filters)
---

The SIMP method (solid isotropic material with penalization) is the most used method for [topology optimization](/topology-optimization/). It divides the design domain into finite elements and gives each element $e$ a density $x_e$ between a small $x_{\min}$ and 1. The Young's modulus of the element is $x_e^p E_0$ with a power $p > 1$, usually $p = 3$. Because of the power, a gray element with $x_e = 1/2$ costs half the material of a solid one but gives only $1/8$ of its stiffness, so the optimizer is pushed toward densities near 0 or 1. Each iteration solves the [finite element](/finite-element-method/) model, computes the derivative of the compliance with respect to every density, smooths these derivatives with a filter, and updates all densities at once with the optimality criteria rule, with a bisection on the [Lagrange multiplier](/lagrange-multiplier/) of the volume bound. Bendsøe (1989) proposed the power law, and the 99 line code of Sigmund (2001) made the method a standard. SIMP finds a local optimum of a penalized problem. It does not give the global optimum of the 0/1 problem, and this page shows a small case where it does not.

## In plain words

Cut the space that the part may fill into many small squares. Each square gets a dial from almost empty to full. A full square is stiff, and a square that is half full is much less than half as stiff. So half full squares are a bad deal, and the method learns to avoid them.

Now repeat a few dozen times. Compute how the part bends under the load. Find out which squares do the most work. Turn those dials up and the others down, but keep the total material fixed. Smooth the result a little, so that tiny patterns do not appear. At the end, the full squares show a structure of bars and holes that carries the load well.

## The problem

The domain is a grid of $n = n_x n_y$ unit square elements with bilinear (Q4) plane stress elements. The element stiffness matrix for $E = 1$ is $k_0$, an $8 \times 8$ matrix that depends on Poisson's ratio $\nu$. Given a load vector $f$, supports that remove all rigid body motions, a volume fraction $v$ and a power $p \ge 1$, the method looks for densities $x = (x_e)$ that solve

$$\min_x\ c(x) = f^{\mathsf T} u(x) \quad\text{subject to}\quad K(x)\, u = f,\quad \sum_e x_e \le v\, n,\quad x_{\min} \le x_e \le 1,$$

with $K(x) = \sum_e x_e^p K_e$, where $K_e$ is $k_0$ placed at the degrees of freedom of element $e$. The compliance $c$ is the work done by the load, and a small compliance is a stiff structure. The lower bound $x_{\min} = 10^{-3}$ keeps $K(x)$ positive definite.

**The sensitivity.** Differentiate $K u = f$: $K\,\partial u = -(\partial K)\,u$. Then $\partial c = f^{\mathsf T} \partial u = -u^{\mathsf T} (\partial K)\, u$, so

$$\frac{\partial c}{\partial x_e} = -p\, x_e^{p-1}\, u_e^{\mathsf T} k_0\, u_e \le 0,$$

where $u_e$ holds the 8 displacements of element $e$. More material never makes the structure softer. No extra linear solve is needed, because compliance is self-adjoint.

## The algorithm

The filter uses the weights $H_{ef} = \max(0, r - \operatorname{dist}(e, f))$ between the centers of the elements, with $r$ the filter radius $r_{\min}$ in element widths. The update uses a move limit $m = 0.2$ and a damping power $\eta = 1/2$.

```pseudo id=main
SIMP(grid, f, supports, v, p, r)
L1  x_e ← v for every element e
L2  for it = 1 to maxit do
L3      solve K(x) u = f; c ← fᵀu             ▷ banded LDLᵀ factorization
L4      record c
L5      dc_e ← −p x_e^(p−1) u_eᵀ k₀ u_e
L6      dc_e ← Σ_f H_ef x_f dc_f / (x_e Σ_f H_ef)   ▷ sensitivity filter
L7      x' ← OC(x, dc)
L8      change ← max_e |x'_e − x_e|
L9      x ← x'; if change < tol then stop
L10 return x

OC(x, dc)                             ▷ V = v n
L11 l1 ← 0; l2 ← 1
L12 while Σ TRIAL(l2) > V do (l1, l2) ← (l2, 2 l2)
L13 repeat at most 100 times
L14     λ ← (l1 + l2) / 2
L15     if Σ TRIAL(λ) > V then l1 ← λ else l2 ← λ
L16     if l2 − l1 ≤ tol_λ · l2 then stop
L17 return TRIAL(l2)

TRIAL(λ)
L18 x'_e ← max(x_min, x_e − m, min(1, x_e + m, x_e (−dc_e / λ)^η)) for every e
```

The rule of line L18 comes from the optimality condition. At an optimum with $x_{\min} < x_e < 1$, the [KKT conditions](/kkt-conditions/) say $-\partial c / \partial x_e = \lambda$: every element that is not at a bound does the same work per unit of material. So $B_e = -dc_e / \lambda$ should be 1. If $B_e > 1$ the element is worth more than it costs and its density grows, and if $B_e < 1$ it shrinks. The power $\eta$ and the move limit make the steps small enough to be stable.

The volume of TRIAL$(\lambda)$ never increases with $\lambda$. Line L12 doubles $l_2$ until the trial design meets the volume bound, and lines L13 to L16 are a [bisection](/bisection-method/) that keeps $l_2$ feasible. The result is the trial design at $l_2$, so it always meets the bound. The stop test of line L16 is relative, because the scale of $dc$, and so of $\lambda$, changes with the load and the mesh. The code of Sigmund (2001) starts with $l_2 = 10^5$ and uses an absolute tolerance, which works for his scaling only.

**The filter.** Line L6 is the mesh-independency filter of Sigmund (2001). It replaces each sensitivity by a weighted average over the elements within distance $r$. With $r \le 1$ only the element itself has a positive weight and the filter does nothing. The filter is a heuristic: the filtered values are not the derivatives of any function that the method minimizes.

## Example

**The half MBB beam.** This is the test case of Sigmund (2001). A beam on two supports carries a load at the middle of its top edge. By symmetry only the left half is modeled: the left edge cannot move in $x$, the bottom right corner rests on a roller, and a unit load points down at the top left corner. With $24 \times 8$ elements, $v = 1/2$, $p = 3$, $r = 1.5$ and $\nu = 0.3$, the code of this page stops after 41 iterations, when no density changes by more than 0.01. The elements with $x_e > 1/2$ are:

```
#################.......
#####......#######......
..###........##..##.....
...###......##....###...
....###...###......###..
.....###.###.........##.
###########..........###
########################
```

The top and bottom rows are the flanges of a truss, and the diagonals carry the shear to the roller at the right.

| iteration | 1 | 2 | 3 | 4 | 5 | 6 | 41 |
|---|---|---|---|---|---|---|---|
| compliance | 975.83 | 585.85 | 427.58 | 366.15 | 347.62 | 338.64 | 264.72 |

The run takes about 0.6 s in pure Python.

**What the filter does.** On a $30 \times 10$ half MBB beam with $v = 1/2$ and at most 100 iterations, the test counts the $2 \times 2$ blocks of elements that form a checkerboard (solid and void on the diagonals):

| filter radius $r$ | iterations | final compliance | checkerboard blocks |
|---|---|---|---|
| 0.9 (no filter) | 100 | 190.9 | 51 |
| 1.5 | 72 | 225.6 | 0 |
| 2.0 | 35 | 265.0 | 0 |

Without the filter the compliance is lowest, but the design is full of checkerboards. They are an error of the Q4 element, which makes a checkerboard look stiffer than it is. They are not a better structure. A larger radius gives thicker members and a larger compliance. These are measurements on this one case.

**Against brute force.** A $5 \times 2$ cantilever is clamped on the left edge and loaded down at the bottom right corner. There are $\binom{10}{5} = 252$ designs with 5 solid elements and 5 elements at $x_{\min}$. The test computes all of them: the best is the bottom row of 5 elements, with compliance 347.38. Every other design has a compliance above $10^9$, because its solid elements do not form a stiff path from the load to the clamp, and only the elements at $x_{\min}$ hold it. SIMP with $p = 3$, $r = 1.5$ and the same volume stops at a gray design with compliance about 388, about 12% worse. SIMP with $p = 1$ and no filter reaches about 107. That value is lower than every 0/1 design, as it must be, because with $p = 1$ the problem is convex and the 0/1 designs are feasible points of it.

## Correctness

SIMP is a heuristic for the 0/1 problem, and the statements that can be proved are about the steps. With $x_{\min} < v \le 1$ and supports that remove the rigid body motions, every iterate satisfies $x_{\min} \le x_e \le 1$ and $\sum_e x_e \le v n$. The stiffness matrix is positive definite, because every element has a stiffness of at least $x_{\min}^p$, so line L3 is defined. The sensitivities are at most 0, the filter keeps that sign, and the volume of TRIAL$(\lambda)$ decreases with $\lambda$. So line L12 stops, the bisection keeps a feasible $l_2$, and OC returns a feasible design. The main loop stops after at most maxit iterations.

If the update has a fixed point and $r \le 1$, the fixed point satisfies the KKT conditions of the penalized problem: $-\partial c/\partial x_e = \lambda$ where $x_{\min} < x_e < 1$, at most $\lambda$ where $x_e = x_{\min}$, and at least $\lambda$ where $x_e = 1$. For $p = 1$ the compliance is a convex function of $x$, so such a point is a global minimum. For $p > 1$ it is only a stationary point. With the filter the fixed point satisfies the same conditions for the filtered values, which are not true derivatives. The full proof is below. The convergence of the iterates themselves is not proved here, and the code stops on a tolerance.

## Complexity

Number the nodes along the short side, with $h$ elements across it. Then the stiffness matrix has a half bandwidth of $2h + 5$, and the banded LDLᵀ factorization of about $2n$ unknowns takes $O(n h^2)$ time and $O(n h)$ space. The filter has $O(r^2)$ weights per element. The OC update calls TRIAL $O(\log \lambda + 100)$ times at $O(n)$ each. So one iteration takes $O(n(h^2 + r^2))$ time, and $k$ iterations take $O(k\, n (h^2 + r^2))$.

The number of iterations is not bounded by a formula. It is measured: 41 on the $24 \times 8$ beam above. Large models replace the direct solver by an iterative one, such as the [conjugate gradient method](/conjugate-gradient-method/) with a [multigrid](/multigrid-method/) preconditioner, and the solve is then most of the cost.

## Properties

- **Feasible iterates.** Every design meets the volume bound and the box bounds.
- **Monotone sensitivities.** More material in any element never increases the compliance.
- **Convex for $p = 1$.** The compliance $f^{\mathsf T} K(x)^{-1} f$ is convex when $K$ is linear in $x$. Then the method solves a convex problem, but the optimum is gray.
- **Local for $p > 1$.** The penalized problem has many local minima, and the result depends on $p$, $r$, the start and the mesh.
- **Not exact.** The answer is a density field that is close to 0/1, not a proved optimum, and the final design is a threshold of it.
- **Simple.** The OC update needs one solve per iteration and no line search.

## Variants and improvements

- **Modified SIMP.** Use $E = E_{\min} + x_e^p (E_0 - E_{\min})$ with $0 \le x_e \le 1$ and a small $E_{\min}$. Void elements then have an exact density 0. The 88 line code of Andreassen and coauthors (2011) uses this form.
- **Density filter.** Filter the densities instead of the sensitivities, and use the filtered density in the model. Then the sensitivities are exact derivatives of a well defined problem.
- **Projection.** A smooth Heaviside step on the filtered densities gives crisp 0/1 designs with a minimum member size.
- **Continuation.** Start with $p = 1$ and increase $p$ slowly, which often finds better local optima.
- **Other updates.** The OC rule needs sensitivities of one sign and one constraint. For several constraints, or sensitivities that change sign as in compliant mechanisms, the method of moving asymptotes of Svanberg (1987) is the usual choice.
- **The choice of $p$.** Bendsøe and Sigmund relate the power to the bounds on composite materials of Hashin and Shtrikman, so that every gray density has a physical meaning. In 2D with $\nu = 1/3$ this asks for $p \ge 3$.
- **Manufacturing constraints.** Overhang limits for additive manufacturing (see [support structure generation](/support-structure-generation/)), minimum and maximum member sizes, and symmetry.

## When to use it

Use SIMP for minimum compliance and similar problems on a fixed mesh, when a density field is a good model and the result will be turned into a part afterwards. It is easy to code, robust, and fast enough for large 3D models with an iterative solver. If a crisp boundary is needed during the optimization, for example for loads that follow the surface, consider [level set topology optimization](/level-set-topology-optimization/), which moves a boundary instead of densities.

## Pitfalls

- **No filter.** Without a filter or a projection, the result has checkerboards and depends on the mesh: a finer mesh gives finer members. The $30 \times 10$ case above shows 51 checkerboard blocks.
- **A zero lower bound.** With $x_{\min} = 0$ in the classic form, $K(x)$ can be singular, and the filter divides by $x_e$.
- **An absolute bisection tolerance.** The multiplier scales with the compliance. A fixed interval and an absolute tolerance can stop too early or never reach the right value.
- **Reading gray as material.** The final design has gray elements. A threshold at $1/2$ can change the compliance much, so compute the compliance of the 0/1 design that is built.
- **Trusting the optimum.** The brute force case above shows a SIMP result 12% worse than the best 0/1 design of the same volume. On large meshes there is no way to check this.
- **Wrong sign.** Compliance sensitivities are at most 0. Code that uses $+$ in line L5 moves material away from where it is needed.

## Implementations

## History

Bendsøe and Kikuchi (1988) started material distribution methods with a homogenization model of microstructures with holes. Bendsøe (1989) proposed the simpler model of this page, a density with a stiffness that is a power of it. The name SIMP came into use a few years later, in work by Rozvany, Zhou and coauthors. Sigmund (2001) published a complete Matlab code of 99 lines, with the MBB beam, the optimality criteria update and the sensitivity filter. That code made the method the common start for teaching and research, and the 88 line code of Andreassen, Clausen, Schevenels, Lazarov and Sigmund (2011) made it faster. Commercial tools for design for additive manufacturing use density methods of this kind.

## References
