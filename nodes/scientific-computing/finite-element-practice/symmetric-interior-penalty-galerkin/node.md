---
tag: Z6FE5T
kind: algorithm
slug: symmetric-interior-penalty-galerkin
name: Symmetric interior penalty Galerkin method
aliases:
- SIPG
- interior penalty discontinuous Galerkin
area: scientific-computing/finite-element-practice
level: advanced
summary: A discontinuous Galerkin method for elliptic problems with symmetric consistency terms and a penalty on jumps that must exceed a known bound.
solves: [poisson-equation]
model: real-ram
complexity:
  vars: {m: the number of cells, k: the polynomial degree}
  time: {worst: "Θ(m^3 k^3)"}
  space: {extra: "Θ(m^2 k^2)"}
properties: {deterministic: true, consistent: true, symmetric_matrix: true, positive_definite_above_penalty_bound: true, locally_conservative: true}
history:
  year: 1982
  people: [Douglas N. Arnold, Mary F. Wheeler]
  note: Wheeler used interior penalties for continuous elements in 1978, and Arnold analyzed the symmetric interior penalty method with fully discontinuous elements in 1982, after the boundary penalty of Nitsche in 1971.
prereqs: [discontinuous-galerkin-method, nitsche-method, weak-formulation]
see_also: [discontinuous-galerkin-method, nitsche-method, hybridizable-discontinuous-galerkin, finite-element-method, poisson-equation, conjugate-gradient-method, hp-finite-element-method, cea-lemma]
sources:
  - paper: doi:10.1137/0719052
    title: Douglas N. Arnold, An interior penalty finite element method with discontinuous elements, SIAM Journal on Numerical Analysis 19(4) (1982) 742-760
    locator: the symmetric interior penalty method, its coercivity for a large enough penalty and the error estimates
  - paper: doi:10.1137/0715010
    title: Mary Fanett Wheeler, An elliptic collocation-finite element method with interior penalties, SIAM Journal on Numerical Analysis 15(1) (1978) 152-161
    locator: interior penalty terms on the jumps of the normal derivative
  - paper: doi:10.1137/S0036142901384162
    title: Douglas N. Arnold, Franco Brezzi, Bernardo Cockburn and L. Donatella Marini, Unified analysis of discontinuous Galerkin methods for elliptic problems, SIAM Journal on Numerical Analysis 39(5) (2002) 1749-1779
    locator: the flux formulation of SIPG, NIPG, IIPG, LDG and related methods, with their consistency, adjoint consistency and stability
  - book: isbn:9780898716566
    title: Béatrice Rivière, Discontinuous Galerkin Methods for Solving Elliptic and Parabolic Equations, SIAM Frontiers in Applied Mathematics 35, 2008
    locator: Chapter 1 (the one-dimensional problem with SIPG, NIPG and IIPG, the penalty bound and a code) and Chapter 2 (higher dimensions)
---

The symmetric interior penalty Galerkin method (SIPG) solves elliptic problems such as $-\Delta u = f$ with piecewise polynomials that may jump across the faces of the mesh. It starts from the [Galerkin method](/galerkin-method/) on each cell and adds three face terms: a consistency term with the average flux, a symmetric copy of it, and a penalty $\frac{\sigma}{h}[u][v]$ on the jumps. The result is a symmetric bilinear form that the exact solution satisfies, and it is positive definite when the penalty parameter $\sigma$ exceeds a bound that depends on the polynomial degree and the mesh. Boundary values enter weakly, as in [Nitsche's method](/nitsche-method/), and the method has the optimal orders $h^{k+1}$ in $L^2$ and $h^k$ in the broken energy norm.

## In plain words

Picture a curve built from separate pieces, one per interval, where the pieces do not have to meet at their ends. Each piece is a simple polynomial. The method asks every piece to obey the equation in its own interval, and at every meeting point it adds two kinds of terms. The first kind lets the slopes on the two sides talk to each other, so that the pieces act as one curve for a correct answer. The second kind is a spring that pulls the two ends together, and its strength is the penalty. If the spring is too weak, the system can have no single answer. If it is strong enough, the problem is well behaved, and the gaps that remain at the meeting points shrink as the pieces get shorter.

## The problem

**Input.** A domain $\Omega$ with a mesh $\mathcal{T}_h$, a source $f$, Dirichlet data $g$, a degree $k \ge 1$ and a penalty parameter $\sigma$. The reference code takes $\Omega = (0, 1)$, $-u'' = f$, $u(0) = g_0$, $u(1) = g_1$, and $m$ cells of width $h = 1/m$.

**Output.** $u_h$ in the broken space $V_h = \{v : v|_K \in \mathcal{P}_k(K) \text{ for all } K\}$ with $a_h(u_h, v) = l_h(v)$ for all $v \in V_h$, where

$$a_h(w, v) = \sum_K(\nabla w, \nabla v)_K - \sum_F\int_F\bigl(\{\nabla w\cdot n\}[v] + \{\nabla v\cdot n\}[w]\bigr) + \sum_F\frac{\sigma}{h_F}\int_F[w][v],$$

$$l_h(v) = (f, v) - \sum_{F \subset \partial\Omega}\int_F(\nabla v\cdot n)\,g + \sum_{F \subset \partial\Omega}\frac{\sigma}{h_F}\int_F g\,v.$$

On an interior face $[v]$ is the difference of the two traces and $\{\cdot\}$ the mean; on a boundary face $[v]$ is the trace and $\{\cdot\}$ the one-sided value. In 1D with the orientation of the code, $[v] = v(x^-) - v(x^+)$ inside, $[v] = v(1^-)$ at $x = 1$ and $[v] = -v(0^+)$ at $x = 0$.

## The algorithm

```pseudo id=main
SIPG(f, m, k, sigma, g0, g1)                   ▷ -u'' = f on (0, 1), degree k, m cells, h = 1/m
L1  for each cell K_j do                        ▷ local basis phi_r = xi^r, xi = (x - x_j)/h
L2      A[(j, r), (j, s)] += (phi_s', phi_r')_K = r s / (h (r + s - 1))     for r, s >= 1
L3      b[(j, r)] += (f, phi_r)_K by quadrature
L4  for each node x_e, e = 0 to m do            ▷ sides: (cell, end, weight of the mean, sign of the jump)
L5      for each pair of sides (trial, test): A[test, trial] += -{phi_s'}[phi_r] - {phi_r'}[phi_s] + (sigma/h)[phi_s][phi_r]
L6      if e = 0 or e = m then b[test] += -{phi_r'} [g] + (sigma/h) [g][phi_r]     ▷ [g] = -g0 at 0, g1 at 1
L7  c <- SOLVE(A, b)                            ▷ symmetric positive definite if sigma is above the bound
L8  return the coefficients c, k + 1 per cell
```

Lines L1 to L3 are the usual cell [assembly](/finite-element-assembly/), with no coupling between cells. Lines L4 and L5 couple the two cells that meet at a node: a node has two sides inside the domain and one side on the boundary, and the products of the mean and jump functionals of the sides give a block of size $(k+1) \times (k+1)$ for each pair. Line L6 puts the boundary data into the load, which is how the method imposes $u = g$ without fixing any unknown. A penalty of $\sigma > 2k^2$ is always enough in this 1D setting, and the code takes $\sigma = 2k^2 + 1$ by default.

## Example

Take $-u'' = 2$ with $u(0) = u(1) = 0$, so $u = x(1 - x)$, and $m = 2$, $k = 1$, $\sigma = 3$, $h = \frac12$. The unknowns are $(c_{0,0}, c_{0,1}, c_{1,0}, c_{1,1})$ with $u_h = c_{j,0} + c_{j,1}\xi$ on cell $j$. Each step adds the following to the matrix and the load:

| step | what it adds |
|---|---|
| L2, cell 0 and cell 1 | $(\phi_1', \phi_1')_K = 1/h = 2$ at $(0{,}1), (0{,}1)$ and at $(1{,}1), (1{,}1)$ |
| L3 | $b = (1, \tfrac12, 1, \tfrac12)$, since $\int_K 2\,d x = 1$ and $\int_K 2\xi\,d x = \tfrac12$ |
| L5, node $x = 0$ | one side (cell 0, left end); the penalty $\frac{\sigma}{h} = 6$ gives $6$ at $(0{,}0),(0{,}0)$, and the flux terms give $2$ at $(0{,}0),(0{,}1)$ and its mirror |
| L5, node $x = \frac12$ | two sides with weights $\frac12$; penalty block $6\,[\,\cdot\,][\,\cdot\,]$ and flux blocks between cells 0 and 1 |
| L5, node $x = 1$ | one side (cell 1, right end), the mirror image of node $0$ |
| L6 | nothing, because $g_0 = g_1 = 0$ |

The assembled system is

$$A = \begin{pmatrix} 12 & 7 & -6 & -1 \\ 7 & 6 & -5 & -1 \\ -6 & -5 & 12 & 5 \\ -1 & -1 & 5 & 4\end{pmatrix}, \qquad b = \begin{pmatrix} 1 \\ \tfrac12 \\ 1 \\ \tfrac12\end{pmatrix},$$

and line L7 gives $u_h = \frac18 + \frac18\xi$ on $(0, \frac12)$ and $u_h = \frac14 - \frac18\xi$ on $(\frac12, 1)$. The two pieces meet at $u_h(\frac12) = \frac14$, which is exact, but the boundary values are $u_h(0^+) = u_h(1^-) = \frac18$ in place of $0$. For this mesh $u_h(0^+) = \frac{1}{4(\sigma - 1)}$ exactly, so $\sigma = 10$ gives $\frac1{36}$ and $\sigma = 100$ gives $\frac1{396}$. A larger penalty pulls the boundary values toward the data, and the error still goes to zero as $h \to 0$ for any fixed $\sigma$ above the bound.

**Convergence (measurement).** For $u = \sin(\pi x)$ the reference code gives, at $m = 4, 8, 16, 32$:

| $k$ | $L^2$ errors | order | broken $H^1$ errors | order |
|---|---|---|---|---|
| 1 | $3.53 \times 10^{-2}$, $9.66 \times 10^{-3}$, $2.47 \times 10^{-3}$, $6.21 \times 10^{-4}$ | 1.99 | $0.531$, $0.255$, $0.126$, $0.0630$ | 1.00 |
| 2 | $1.44 \times 10^{-3}$, $1.67 \times 10^{-4}$, $2.01 \times 10^{-5}$, $2.47 \times 10^{-6}$ | 3.03 | $6.28 \times 10^{-2}$, $1.45 \times 10^{-2}$, $3.47 \times 10^{-3}$, $8.48 \times 10^{-4}$ | 2.03 |
| 3 | $8.49 \times 10^{-5}$, $5.52 \times 10^{-6}$, $3.48 \times 10^{-7}$, $2.18 \times 10^{-8}$ | 4.00 | $3.45 \times 10^{-3}$, $4.25 \times 10^{-4}$, $5.30 \times 10^{-5}$, $6.62 \times 10^{-6}$ | 3.00 |

The orders shown are those of the last refinement, and they match $k + 1$ and $k$.

## Correctness

The full proof is in [the correctness proof](proofs/correctness.md). It first shows that lines L1 to L6 compute the matrix of $a_h$ and the vector of $l_h$: at each node the mean and the jump are sums over the sides with the weights and signs of line L4, and line L5 expands their products. Integration by parts on each cell then shows consistency: for $u \in H^2$, the cell terms give $(f, v)$ plus $\sum_e u'(x_e)[v]_e$, which the first face term cancels, and the other terms reduce to the boundary data of $l_h$. The form is symmetric by construction. With the trace inverse inequality $p(z)^2 \le \frac{(n+1)^2}{h}\|p\|^2$ for polynomials of degree $n$, which follows from the Legendre basis, the face term is bounded by the cell terms, and for $\sigma > ck^2$ with $c = \frac32$ ($m \ge 2$) or $c = 2$ ($m = 1$) the form is bounded below by a positive multiple of $\sum_K\|v'\|_K^2 + \sum_e\frac1h[v]_e^2$. So the matrix is symmetric positive definite and the solution is unique. Polynomials of degree $k$ are reproduced exactly.

## Complexity

There are $N = m(k+1)$ unknowns. Line L2 does $\Theta(k^2)$ work per cell and line L3 does five evaluations of $f$ per basis function, so the cell loop costs $\Theta(mk^2)$. Each node has at most two sides and four side pairs, each a block of $(k+1)^2$ entries, so lines L4 to L6 cost $\Theta(mk^2)$. The matrix is block tridiagonal with blocks of size $k + 1$. The reference code stores it densely, which takes $\Theta(N^2) = \Theta(m^2k^2)$ memory, and solves it with Gaussian elimination in $\Theta(N^3) = \Theta(m^3k^3)$ time, the bound in the front matter. A block tridiagonal solver costs $\Theta(mk^3)$ time and $\Theta(mk^2)$ memory. In several dimensions, the matrix is sparse with one dense block per cell and one per pair of neighbors, and [conjugate gradients](/conjugate-gradient-method/) with a good preconditioner applies because the matrix is symmetric positive definite.

## Properties

- **Consistency and adjoint consistency (theorem).** The exact solution satisfies the discrete equations, and because the form is symmetric, the solution of the dual problem does too. The second fact gives the $L^2$ order $h^{k+1}$ by the Aubin-Nitsche argument.
- **Coercivity above a bound (theorem).** In 1D, $\sigma > \frac32k^2$ for $m \ge 2$ and $\sigma > 2k^2$ for $m = 1$ are sufficient. For $k = 1$ these bounds are sharp: the reference code finds the thresholds $1.5$ for $m = 2$ and $2$ for $m = 1$. For $k \ge 2$ the measured thresholds are smaller, for example about $4.43$ for $k = 2$ and $9.46$ for $k = 3$ at $m = 8$, against the sufficient bounds $6$ and $13.5$.
- **Optimal orders (theorem).** For $u \in H^{k+1}$, the broken energy error is $O(h^k)$ and the $L^2$ error is $O(h^{k+1})$, with constants that depend on $\sigma$ and the shape regularity.
- **Local conservation.** Testing with $v = 1$ on one cell gives a flux balance on that cell with the numerical flux $\{u_h'\} - \frac{\sigma}{h}[u_h]$.
- **Weak boundary values.** The discrete solution does not take the boundary values exactly, as the example shows.
- **More unknowns than continuous elements.** For degree $k$ there are $m(k+1)$ unknowns in place of $mk + 1$, and the gap is larger in several dimensions.

## Variants and improvements

- **NIPG and IIPG.** The nonsymmetric interior penalty method changes the sign of the term $\{\nabla v\cdot n\}[w]$, so the two flux terms cancel in $a_h(v, v)$ and the form is coercive for every $\sigma > 0$. It loses adjoint consistency, so the proved $L^2$ order is only $h^k$, and computations show the lost order for some degrees. The incomplete method drops that term. The alias "interior penalty discontinuous Galerkin" often refers to the whole family, not only to SIPG.
- **Explicit penalty bounds.** Shahbazi gave explicit values of $\sigma$ for simplices based on the sharp trace inverse inequality, and many codes use them in place of a guess.
- **Weighted averages.** For a coefficient $\kappa$ that jumps across faces, averages weighted by $\kappa$ and a penalty with the harmonic mean of $\kappa$ keep the method robust.
- **Local discontinuous Galerkin and Bassi-Rebay.** Use a lifting of the jumps in place of the penalty, which gives a stability parameter that does not need to be large.
- **[Hybridizable discontinuous Galerkin](/hybridizable-discontinuous-galerkin/).** Introduces a trace unknown on faces, which gives a smaller global system after local elimination.
- **Time-dependent and convection problems.** The SIPG form of the diffusion combines with upwind fluxes for the convection in the [discontinuous Galerkin method](/discontinuous-galerkin-method/).

## When to use it

Use SIPG when a discontinuous Galerkin code must also handle diffusion terms, when the mesh has hanging nodes or the degree changes from cell to cell as in [hp methods](/hp-finite-element-method/), or when local conservation matters. It keeps a symmetric positive definite matrix, which allows conjugate gradients and multigrid. Continuous elements have fewer unknowns for the same degree and need no penalty, so they are the cheaper choice for a smooth problem on a conforming mesh. If the choice of $\sigma$ is a problem, NIPG, LDG or HDG avoid a large penalty.

## Pitfalls

- **A penalty below the bound.** With $\sigma$ too small in line L5, the matrix is indefinite: for $k = 2$ and $m = 6$, $\sigma = 1$ makes the Cholesky factorization fail, and the solution can be wrong without any warning in a general solver. Use $\sigma$ above the bound for the degree, which grows like $k^2$.
- **Wrong scaling of the penalty.** The penalty is $\sigma/h$, not $\sigma$. A code that uses $\sigma$ alone in line L5 loses coercivity on fine meshes and the error stops decreasing.
- **Forgetting the boundary terms of the load.** Line L6 must add both $-\{\phi_r'\}[g]$ and $\frac{\sigma}{h}[g][\phi_r]$. With only the penalty part, the method is not consistent and the order drops.
- **Inconsistent jump signs.** The mean and jump in line L5 must use the same orientation on both sides of a face. A sign error in one side makes the matrix nonsymmetric and the method inconsistent.
- **Too large a penalty.** A huge $\sigma$ is safe for coercivity but increases the condition number in proportion to $\sigma$, which slows iterative solvers.

## Implementations

## History

Joachim Nitsche imposed Dirichlet data in 1971 with a symmetric boundary term and a penalty, which is SIPG restricted to the boundary. Garth Baker used interior penalties for fourth-order problems in 1977, Jim Douglas and Todd Dupont used them for continuous elements in 1976, and Mary Wheeler combined collocation with interior penalties in 1978. Douglas Arnold analyzed the method with fully discontinuous elements in 1982, and this is the SIPG method used today. Interest returned at the end of the 1990s with the nonsymmetric methods of Oden, Babuška and Baumann and of Rivière, Wheeler and Girault, and in 2002 Arnold, Brezzi, Cockburn and Marini put these methods and LDG into one framework of numerical fluxes.

## References
