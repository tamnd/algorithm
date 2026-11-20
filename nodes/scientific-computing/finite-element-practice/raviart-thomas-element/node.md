---
tag: 1KM42C
kind: definition
slug: raviart-thomas-element
name: Raviart-Thomas element
aliases:
- RT element
area: scientific-computing/finite-element-practice
level: advanced
summary: A vector element with continuous normal components across faces, conforming in H(div), used for fluxes in mixed methods.
prereqs: [mixed-finite-element-method, ciarlet-finite-element, sobolev-space]
see_also: [mixed-finite-element-method, nedelec-element, inf-sup-condition, ciarlet-finite-element, taylor-hood-element, hybridizable-discontinuous-galerkin, finite-volume-method, static-condensation]
sources:
  - paper: doi:10.1007/BFb0064470
    title: P.-A. Raviart and J.-M. Thomas, A mixed finite element method for 2-nd order elliptic problems, in Mathematical Aspects of Finite Element Methods, Lecture Notes in Mathematics 606, Springer, 1977, 292-315
    locator: the definition of the flux spaces of degree k on triangles and rectangles, their degrees of freedom and the error estimates of the mixed method
  - paper: doi:10.1007/BF01396415
    title: J. C. Nédélec, Mixed finite elements in R^3, Numerische Mathematik 35(3) (1980) 315-341
    locator: the H(div) conforming elements on tetrahedra and cubes, the three-dimensional form of the Raviart-Thomas spaces
  - paper: doi:10.1007/BF01389710
    title: Franco Brezzi, Jim Douglas Jr. and L. D. Marini, Two families of mixed finite elements for second order elliptic problems, Numerische Mathematik 47(2) (1985) 217-235
    locator: the Brezzi-Douglas-Marini flux spaces with full polynomials of degree k
  - book: isbn:9783642365188
    title: Daniele Boffi, Franco Brezzi and Michel Fortin, Mixed Finite Element Methods and Applications, Springer Series in Computational Mathematics 44, Springer, 2013
    locator: Chapter 2 (function spaces and finite element approximations, the H(div) conforming elements) and Chapter 7 (mixed methods for elliptic problems)
  - paper: doi:10.1017/S0962492906210018
    title: Douglas N. Arnold, Richard S. Falk and Ragnar Winther, Finite element exterior calculus, homological techniques, and applications, Acta Numerica 15 (2006) 1-155
    locator: the trimmed polynomial spaces of differential forms and the discrete de Rham sequence that contains the Raviart-Thomas and Nédélec spaces
---

The Raviart-Thomas element is a [finite element](/ciarlet-finite-element/) for vector fields whose normal component is continuous across the faces of the mesh, while the tangential component can jump. The global space lies in $H(\mathrm{div})$, the space of vector fields whose divergence is square integrable, and the degrees of freedom are fluxes through the faces. It is the standard space for the flux $\sigma = -\kappa\nabla u$ in the [mixed method](/mixed-finite-element-method/) for the Poisson problem and for Darcy flow, because the divergence of the space is exactly the piecewise polynomial space of the potential, which gives local conservation on each cell.

## Definition

Let $K \subset \mathbb{R}^d$ be a triangle ($d = 2$) or a tetrahedron ($d = 3$), let $P_k(K)$ be the polynomials of degree at most $k$ and let $\tilde P_k(K)$ be the homogeneous polynomials of degree exactly $k$. The **Raviart-Thomas space of index $k \ge 0$** is

$$\mathrm{RT}_k(K) = P_k(K)^d + x\,\tilde P_k(K).$$

Its dimension is $(k + 1)(k + 3)$ in 2D and $(k + 1)(k + 2)(k + 4)/2$ in 3D. As a Ciarlet triple $(K, \mathrm{RT}_k(K), \Sigma)$, the degrees of freedom $\Sigma$ are, for a face $F$ with unit normal $n_F$,

$$v \mapsto \int_F (v\cdot n_F)\,q\,ds \quad (q \in P_k(F)), \qquad v \mapsto \int_K v\cdot q\,dx \quad (q \in P_{k-1}(K)^d),$$

where the second set is empty for $k = 0$. These degrees of freedom are unisolvent: they determine $v \in \mathrm{RT}_k(K)$ uniquely (theorem). In 2D their number is $3(k + 1) + k(k + 1) = (k + 1)(k + 3)$. On a mesh $\mathcal{T}_h$ each face gets one fixed normal, and the face degrees of freedom are shared by the two cells next to the face. The global space is

$$\mathrm{RT}_k(\mathcal{T}_h) = \{v \in H(\mathrm{div}; \Omega) : v|_K \in \mathrm{RT}_k(K) \text{ for all } K\},$$

and a piecewise $\mathrm{RT}_k$ field is in $H(\mathrm{div})$ exactly when its normal component is continuous across every interior face (theorem).

**Properties (theorem).**

- For $v \in \mathrm{RT}_k(K)$, $\nabla\cdot v \in P_k(K)$ and $v\cdot n_F \in P_k(F)$ on each face. The divergence maps $\mathrm{RT}_k(\mathcal{T}_h)$ onto the discontinuous piecewise polynomials of degree $k$.
- Let $\Pi_h$ be the interpolation defined by the degrees of freedom and $P_h$ the $L^2$ projection onto the discontinuous polynomials of degree $k$. Then $\nabla\cdot(\Pi_h v) = P_h(\nabla\cdot v)$. This commuting diagram makes $\Pi_h$ a Fortin operator, so the pair $\mathrm{RT}_k$ with discontinuous $P_k$ satisfies the [Babuška-Brezzi conditions](/inf-sup-condition/) uniformly on shape-regular meshes.
- For the mixed Poisson problem with a smooth solution, $\|\sigma - \sigma_h\|_{L^2} \le Ch^{k+1}|\sigma|_{H^{k+1}}$ and $\|u - u_h\|_{L^2} \le Ch^{k+1}(|\sigma|_{H^{k+1}} + |u|_{H^{k+1}})$.
- Fields on a general cell come from the reference cell by the contravariant Piola map $v(x) = \frac{1}{\det J}J\hat v(\hat x)$, with $J$ the Jacobian of the affine map $\hat x \mapsto x$. This map keeps the normal fluxes through the faces.

## Examples and non-examples

**Example: the lowest order space $\mathrm{RT}_0$.** For $k = 0$ the space is $\{a + bx : a \in \mathbb{R}^d, b \in \mathbb{R}\}$, with dimension $d + 1$ and one degree of freedom per face, the total flux through it. On a cell with vertices $P_1, \dots, P_{d+1}$, let $F_i$ be the face opposite $P_i$ with outward normal. The basis function

$$\phi_i(x) = \frac{x - P_i}{d\,|K|}$$

has total flux $1$ through $F_i$ and flux $0$ through the other faces, and $\nabla\cdot\phi_i = 1/|K|$. The reason: $x - P_i$ is tangent to every face that contains $P_i$, and on $F_i$ the normal component of $x - P_i$ is constant and equal to the height of $K$ over $F_i$, which is $d\,|K|/|F_i|$. Some codes use $|F_i|\,\phi_i$ instead, whose normal component on $F_i$ is $1$. Both choices span the same space.

**Example: the reference triangle, by hand.** Let $K$ have the vertices $(0, 0)$, $(1, 0)$ and $(0, 1)$, so $|K| = 1/2$. Use the total flux through each edge as the degree of freedom, so $\phi_i = (x - P_i)/(2|K|) = x - P_i$ for this triangle.

- For $P = (0, 0)$, $\phi = (x, y)$. On the hypotenuse $x + y = 1$, the outward normal is $(1, 1)/\sqrt2$, so $\phi\cdot n = 1/\sqrt2$, and the edge length $\sqrt2$ gives the flux $1$. On the edge $y = 0$, $\phi\cdot n = -y = 0$, and on $x = 0$, $\phi\cdot n = -x = 0$. The divergence is $2$, which equals the total flux $1$ divided by $|K|$.
- For $P = (1, 0)$, $\phi = (x - 1, y)$. On the edge $x = 0$ with outward normal $(-1, 0)$, $\phi\cdot n = 1 - x = 1$, so the flux is $1$.
- The constant field $v = (1, 0)$ has the fluxes $1$ through the hypotenuse, $-1$ through the edge $x = 0$ and $0$ through the edge $y = 0$. So its interpolant is $(x, y) - (x - 1, y) = (1, 0) = v$, as it must be, because constants are in $\mathrm{RT}_0$.

**Example: rectangles.** On a rectangle the lowest order space is $\{(a + bx, c + dy)\}$, with the four edge fluxes as degrees of freedom. Its divergence $b + d$ is constant.

**Non-example: piecewise constant vector fields.** A field that is constant on each triangle is in $L^2$, but its normal component jumps across edges in general, so it is not in $H(\mathrm{div})$. The space $\mathrm{RT}_0$ adds the term $bx$ so that the normal component on each edge is constant and can be matched across the edge.

**Non-example: $P_1^2$ with only edge fluxes.** The full linear fields have dimension 6 in 2D, and the three edge fluxes do not determine them. The Brezzi-Douglas-Marini element below uses two moments per edge to fix this.

**Non-example: continuous Lagrange vector fields.** A continuous piecewise linear field is in $H(\mathrm{div})$, but it also has a continuous tangential component. When the coefficient $\kappa$ jumps across an interface, the exact flux $-\kappa\nabla u$ has a continuous normal component and a tangential component that jumps, so a continuous field cannot follow it near the interface.

## Related definitions

- **Brezzi-Douglas-Marini element $\mathrm{BDM}_k$**, $k \ge 1$: the full space $P_k(K)^d$ with normal moments of degree $k$ on the faces. It is $H(\mathrm{div})$ conforming, with divergence in $P_{k-1}$, so it is paired with discontinuous $P_{k-1}$. It has dimension $(k + 1)(k + 2)$ in 2D, fewer than $\mathrm{RT}_k$, and its flux error in $L^2$ is also $O(h^{k+1})$, but its divergence and its potential are one order less accurate.
- **[Nédélec element](/nedelec-element/).** The $H(\mathrm{curl})$ conforming counterpart, with continuous tangential components. In 2D the Nédélec space of the first kind is the Raviart-Thomas space rotated by 90 degrees.
- **Hybridization.** Making the $\mathrm{RT}_k$ space fully discontinuous and enforcing normal continuity with a multiplier on the faces gives a positive definite system for the face unknowns, through [static condensation](/static-condensation/). [HDG](/hybridizable-discontinuous-galerkin/) methods use the same structure.
- **Finite volumes.** $\mathrm{RT}_0$ with piecewise constant potential is conservative on each cell, like a cell-centered [finite volume method](/finite-volume-method/). The two are closely related on some meshes.
- **Finite element exterior calculus.** In the notation of Arnold, Falk and Winther, $\mathrm{RT}_k = \mathcal{P}_{k+1}^-\Lambda^{d-1}$, the trimmed polynomial $(d-1)$-forms. In the discrete de Rham sequence it sits between the Nédélec space, which the curl maps into it, and the discontinuous space, onto which the divergence maps it.

## References
