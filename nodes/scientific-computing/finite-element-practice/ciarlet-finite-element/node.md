---
tag: QGHDNE
kind: definition
slug: ciarlet-finite-element
name: Ciarlet finite element
aliases:
- finite element triple
area: scientific-computing/finite-element-practice
level: core
summary: A finite element as a triple of a cell, a space of shape functions and a set of degrees of freedom that determines each shape function uniquely.
prereqs: [lagrange-finite-element, sobolev-space]
see_also: [raviart-thomas-element, nedelec-element, taylor-hood-element, isoparametric-mapping, finite-element-assembly, bramble-hilbert-lemma, hermite-interpolation, virtual-element-method]
sources:
  - book: isbn:9780898715149
    title: Philippe G. Ciarlet, The Finite Element Method for Elliptic Problems, SIAM Classics in Applied Mathematics 40, 2002
    locator: Chapter 2, Section 2.3 (the general definition of a finite element and affine families)
  - book: isbn:9780387759333
    title: Susanne C. Brenner and L. Ridgway Scott, The Mathematical Theory of Finite Element Methods, third edition, Springer, 2008
    locator: Chapter 3, Section 3.1 (the definition of a finite element, nodal basis and local interpolant) and the rest of Chapter 3 (examples and affine equivalence)
  - book: isbn:9780387205748
    title: Alexandre Ern and Jean-Luc Guermond, Theory and Practice of Finite Elements, Applied Mathematical Sciences 159, Springer, 2004
    locator: Chapter 1 (finite element interpolation, Lagrange and Hermite elements, H(div) and H(curl) elements)
---

A Ciarlet finite element is a triple $(K, \mathcal{P}, \mathcal{N})$ of a cell $K$, a finite-dimensional space $\mathcal{P}$ of shape functions on $K$, and a set $\mathcal{N}$ of linear functionals, the degrees of freedom, that is a basis of the dual space of $\mathcal{P}$. The last condition means that the degrees of freedom fix each shape function uniquely, so they define a nodal basis and a local interpolant. The definition covers the [Lagrange elements](/lagrange-finite-element/) as well as the [Raviart-Thomas](/raviart-thomas-element/), [Nédélec](/nedelec-element/) and Hermite elements, and the choice of degrees of freedom on the faces decides how the global space is glued together.

## Definition

**Finite element (Ciarlet).** A finite element is a triple $(K, \mathcal{P}, \mathcal{N})$ with:

1. $K \subset \mathbb{R}^d$ a closed bounded set with nonempty interior and a Lipschitz boundary, the *cell* or *element domain*;
2. $\mathcal{P}$ a space of functions on $K$ of finite dimension $n$, the *shape functions*;
3. $\mathcal{N} = \{N_1, \ldots, N_n\}$ a basis of the dual space $\mathcal{P}'$, the *degrees of freedom* or *nodal variables*.

Since $\dim\mathcal{P} = n$, condition 3 holds if and only if the triple is *unisolvent*: for $v \in \mathcal{P}$, $N_i(v) = 0$ for all $i$ implies $v = 0$. This is the condition that you check in practice.

**Nodal basis.** The basis $\phi_1, \ldots, \phi_n$ of $\mathcal{P}$ dual to $\mathcal{N}$ is defined by $N_i(\phi_j) = \delta_{ij}$. Unisolvence makes it exist and be unique: write $\phi_j$ in any basis of $\mathcal{P}$, and the conditions become a square linear system with a nonsingular matrix.

**Local interpolant.** For a function $v$ smooth enough that every $N_i(v)$ is defined, $I_K v = \sum_{i=1}^n N_i(v)\,\phi_i$. Then $N_i(I_K v) = N_i(v)$ for every $i$, and $I_K p = p$ for every $p \in \mathcal{P}$, so $I_K$ is a projection onto $\mathcal{P}$.

**Affine equivalence.** Two elements $(\hat K, \hat{\mathcal{P}}, \hat{\mathcal{N}})$ and $(K, \mathcal{P}, \mathcal{N})$ are affine equivalent if an affine map $F_K(\hat x) = B_K\hat x + b_K$ maps $\hat K$ onto $K$, $\mathcal{P} = \{\hat p \circ F_K^{-1} : \hat p \in \hat{\mathcal{P}}\}$, and $N_i(v) = \hat N_i(v \circ F_K)$. Then $\phi_i = \hat\phi_i \circ F_K^{-1}$, so a code computes the basis once on the reference cell $\hat K$. The scaling proof of the [Bramble-Hilbert](/bramble-hilbert-lemma/) interpolation estimate uses this equivalence. A non-affine $F_K$ gives [isoparametric elements](/isoparametric-mapping/).

**Global space.** A mesh $\mathcal{T}_h$ with one element on each cell defines the global space of functions whose restriction to each $K$ is in its $\mathcal{P}$. Degrees of freedom that sit on a shared face are identified, and this makes a trace of the function continuous across the face. Values on the face give $H^1$ conformity, normal components give $H(\mathrm{div})$ conformity, and tangential components give $H(\mathrm{curl})$ conformity. [Finite element assembly](/finite-element-assembly/) uses this identification as its local-to-global map.

## Examples and non-examples

**The P1 triangle.** $K$ is a triangle with vertices $a_1, a_2, a_3$, $\mathcal{P} = \mathcal{P}_1$ (dimension 3), and $N_i(v) = v(a_i)$. A linear function that vanishes at three points that are not collinear is zero, so the triple is unisolvent. The nodal basis is the barycentric coordinates $\lambda_i$. On the reference triangle with vertices $(0,0)$, $(1,0)$, $(0,1)$ they are $1 - x - y$, $x$ and $y$, and the interpolant of $v = x^2$ is $I_K v = x$.

**The P2 triangle.** $\mathcal{P} = \mathcal{P}_2$ (dimension 6), with values at the three vertices and the three edge midpoints. If $v \in \mathcal{P}_2$ vanishes at the three nodes of an edge, its restriction to that edge is a quadratic in one variable with three zeros, so it is zero there and $v = \lambda_1 w$ for the barycentric coordinate $\lambda_1$ that vanishes on that edge and some $w \in \mathcal{P}_1$. Doing the same for the other two edges gives $v = c\lambda_1\lambda_2\lambda_3$, which has degree 3 unless $c = 0$. So the triple is unisolvent.

**Cubic Hermite in one dimension.** $K = [0, 1]$, $\mathcal{P} = \mathcal{P}_3$, and $\mathcal{N} = \{v(0), v'(0), v(1), v'(1)\}$. The nodal basis is $1 - 3x^2 + 2x^3$, $x - 2x^2 + x^3$, $3x^2 - 2x^3$ and $x^3 - x^2$. For the first one: its value is $1$ at $0$ and $0$ at $1$, and its derivative $-6x + 6x^2$ is $0$ at both ends. Shared values and slopes make the global space $C^1$, as beams need. This is [Hermite interpolation](/hermite-interpolation/) as a finite element.

**Crouzeix-Raviart.** $\mathcal{P} = \mathcal{P}_1$ on a triangle with values at the three edge midpoints. The midpoints are not collinear, so the triple is unisolvent. Neighbors agree only at the midpoint of the shared edge, so the global space is not in $H^1$: the element is nonconforming.

**Raviart-Thomas of lowest order.** $\mathcal{P} = \{a + c\,x : a \in \mathbb{R}^2, c \in \mathbb{R}\}$ on a triangle (dimension 3), with $N_e(v) = \int_e v\cdot n_e\,ds$ for the three edges $e$. Shared normal fluxes give $H(\mathrm{div})$ conformity. See [Raviart-Thomas element](/raviart-thomas-element/).

**Non-example: collinear nodes.** $\mathcal{P}_1$ on a triangle with values at $a_1$, $a_2$ and the midpoint of the edge $a_1a_2$ is not unisolvent: the barycentric coordinate $\lambda_3$ vanishes at all three points.

**Non-example: nodes on a conic.** $\mathcal{P}_2$ on the reference triangle with values at $(0,0)$, $(\tfrac13, 0)$, $(\tfrac23, 0)$, $(1, 0)$, $(0, \tfrac12)$ and $(0, 1)$ has the right count, 6, but $v = xy$ vanishes at all six points. Six points on the pair of lines $xy = 0$ cannot determine a quadratic.

**Non-example: wrong count.** Vertex values on a quadrilateral give four functionals, but $\mathcal{P}_1$ has dimension 3. The bilinear space $\mathcal{Q}_1 = \operatorname{span}\{1, x, y, xy\}$ matches them and gives the Q1 element.

## Related definitions

- **[Lagrange finite element](/lagrange-finite-element/).** All degrees of freedom are point values. It is the most common instance and gives continuous piecewise polynomials.
- **[Raviart-Thomas](/raviart-thomas-element/) and [Nédélec](/nedelec-element/) elements.** Degrees of freedom are normal or tangential moments on faces, for $H(\mathrm{div})$ and $H(\mathrm{curl})$.
- **[Taylor-Hood element](/taylor-hood-element/).** Not one triple but a pair: $\mathcal{P}_2$ Lagrange velocities with $\mathcal{P}_1$ Lagrange pressures, chosen to satisfy the [inf-sup condition](/inf-sup-condition/) for Stokes flow.
- **Interpolation equivalence.** A weaker relation than affine equivalence, $I_K v \circ F_K = \hat I(v \circ F_K)$, which holds for Hermite elements whose derivative degrees of freedom do not map one to one.
- **[Virtual element method](/virtual-element-method/).** Keeps the degrees of freedom but leaves $\mathcal{P}$ implicit on general polygons, so the shape functions are never computed.

## References
