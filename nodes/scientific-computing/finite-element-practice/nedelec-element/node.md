---
tag: EAY989
kind: definition
slug: nedelec-element
name: Nedelec edge element
aliases:
- edge element
- Whitney element
area: scientific-computing/finite-element-practice
level: advanced
summary: A vector element with continuous tangential components across faces, conforming in H(curl), used for Maxwell's equations.
prereqs: [raviart-thomas-element, ciarlet-finite-element]
see_also: [raviart-thomas-element, mixed-finite-element-method, ciarlet-finite-element, yee-fdtd-scheme, perfectly-matched-layer, helmholtz-hodge-decomposition, lagrange-finite-element, inf-sup-condition]
sources:
  - paper: doi:10.1007/BF01396415
    title: J. C. Nédélec, Mixed finite elements in R^3, Numerische Mathematik 35(3) (1980) 315-341
    locator: the H(curl) conforming spaces of the first kind on tetrahedra and cubes, their degrees of freedom on edges, faces and cells, and their unisolvence
  - paper: doi:10.1007/BF01389668
    title: J. C. Nédélec, A new family of mixed finite elements in R^3, Numerische Mathematik 50(1) (1986) 57-81
    locator: the second family of H(curl) and H(div) conforming spaces with full polynomials of degree k
  - paper: doi:10.1049/ip-a-1.1988.0077
    title: "A. Bossavit, Whitney forms: a class of finite elements for three-dimensional computations in electromagnetism, IEE Proceedings A 135(8) (1988)"
    locator: the identification of the lowest order Nédélec space with the Whitney 1-forms and their use for eddy current and Maxwell problems
  - book: isbn:9780198508885
    title: Peter Monk, Finite Element Methods for Maxwell's Equations, Oxford University Press, 2003
    locator: Chapter 5 (finite elements on tetrahedra) and Chapter 6 (finite elements on hexahedra)
  - book: isbn:9783642365188
    title: Daniele Boffi, Franco Brezzi and Michel Fortin, Mixed Finite Element Methods and Applications, Springer Series in Computational Mathematics 44, Springer, 2013
    locator: Chapter 2 (the H(curl) conforming elements) and Chapter 11 (mixed finite elements for electromagnetic problems)
  - paper: doi:10.1017/S0962492906210018
    title: Douglas N. Arnold, Richard S. Falk and Ragnar Winther, Finite element exterior calculus, homological techniques, and applications, Acta Numerica 15 (2006) 1-155
    locator: the two families of polynomial differential forms, the Whitney forms as the lowest order case and the commuting projections of the discrete de Rham sequence
---

The Nédélec element is a [finite element](/ciarlet-finite-element/) for vector fields whose tangential component is continuous across the faces of the mesh, while the normal component can jump. The global space lies in $H(\mathrm{curl})$, the space of vector fields whose curl is square integrable, and the lowest order degrees of freedom are the integrals of the tangential component along the edges. It is the standard space for the electric field in finite element methods for Maxwell's equations. The tangential component of the electric field is continuous across a material interface and the normal component jumps, which is exactly the continuity of the space, and continuous nodal elements in place of it can give spurious solutions.

## Definition

Let $K \subset \mathbb{R}^3$ be a tetrahedron, let $P_k(K)$ be the polynomials of degree at most $k$ and let $\tilde P_k(K)$ be the homogeneous polynomials of degree exactly $k$. The **Nédélec space of the first kind of order $k \ge 1$** is

$$N_k(K) = P_{k-1}(K)^3 \oplus S_k(K), \qquad S_k(K) = \{p \in \tilde P_k(K)^3 : p(x)\cdot x = 0\}.$$

Its dimension is $k(k + 2)(k + 3)/2$, and $k(k + 2)$ for the same construction in 2D. The degrees of freedom, for the edges $e$ with unit tangent $t_e$, the faces $F$ with unit normal $n_F$, and the cell $K$, are

$$\int_e (v\cdot t_e)\,q\,ds \ (q \in P_{k-1}(e)), \qquad \int_F (v\times n_F)\cdot q\,dA \ (q \in P_{k-2}(F)^2 \text{ tangent to } F), \qquad \int_K v\cdot q\,dx \ (q \in P_{k-3}(K)^3),$$

where a set is empty when the degree is negative. They are unisolvent (theorem, Nédélec 1980). On a mesh each edge gets one fixed direction and each face one fixed normal, and the degrees of freedom on a shared edge or face are shared by all the cells that contain it. The global space is

$$N_k(\mathcal{T}_h) = \{v \in H(\mathrm{curl}; \Omega) : v|_K \in N_k(K) \text{ for all } K\},$$

and a piecewise $N_k$ field is in $H(\mathrm{curl})$ exactly when its tangential component is continuous across every interior face (theorem).

**Properties (theorem).**

- For $k = 1$, $N_1(K) = \{a + b\times x : a, b \in \mathbb{R}^3\}$, with dimension 6 and one degree of freedom per edge, the circulation $\int_e v\cdot t_e\,ds$.
- The gradients of the continuous Lagrange functions of degree $k$ lie in $N_k(\mathcal{T}_h)$, and the curls of $N_k(\mathcal{T}_h)$ lie in the [Raviart-Thomas space](/raviart-thomas-element/) $\mathrm{RT}_{k-1}(\mathcal{T}_h)$. On a contractible domain the sequence Lagrange, then Nédélec, then Raviart-Thomas, then discontinuous, linked by grad, curl and div, is exact, and the interpolation operators commute with these maps. This discrete de Rham sequence is the reason why the space has no spurious modes for the Maxwell eigenvalue problem.
- For a smooth field, the interpolation error is $\|E - \Pi_h E\|_{H(\mathrm{curl})} \le Ch^k(|E|_{H^k} + |\nabla\times E|_{H^k})$ on a shape-regular family of meshes.
- Fields on a general cell come from the reference cell by the covariant Piola map $v(x) = J^{-\mathsf T}\hat v(\hat x)$, which keeps the tangential components along edges.

## Examples and non-examples

**Example: Whitney forms.** For $k = 1$, the basis function of the edge from the vertex $P_i$ to the vertex $P_j$ is the Whitney 1-form

$$w_{ij} = \lambda_i\nabla\lambda_j - \lambda_j\nabla\lambda_i,$$

where $\lambda_i$ are the barycentric coordinates. Its circulation is $1$ along the edge from $P_i$ to $P_j$ and $0$ along all other edges, and $\nabla\times w_{ij} = 2\nabla\lambda_i\times\nabla\lambda_j$ is constant on the cell.

**Example: the reference triangle, by hand.** The same construction works in 2D with the scalar curl $\partial_xv_2 - \partial_yv_1$. Let $K$ have the vertices $P_0 = (0, 0)$, $P_1 = (1, 0)$ and $P_2 = (0, 1)$, so $\lambda_0 = 1 - x - y$, $\lambda_1 = x$ and $\lambda_2 = y$.

- $w_{12} = x\,(0, 1) - y\,(1, 0) = (-y, x)$. On the edge from $(1, 0)$ to $(0, 1)$ the unit tangent is $(-1, 1)/\sqrt2$, so $w_{12}\cdot t = (x + y)/\sqrt2 = 1/\sqrt2$, and the length $\sqrt2$ gives the circulation $1$. On the edge $y = 0$, $w_{12}\cdot(1, 0) = -y = 0$, and on the edge $x = 0$, $w_{12}\cdot(0, 1) = x = 0$. The curl is $1 - (-1) = 2$, which is the circulation $1$ divided by the area $1/2$, as Stokes' theorem requires.
- $w_{01} = (1 - y, x)$ and $w_{02} = (y, 1 - x)$, by the same formula.
- The gradient of the Lagrange function $\lambda_1 = x$ is $(1, 0)$. The differences of its vertex values along the edges $P_0P_1$, $P_0P_2$ and $P_1P_2$ are $1$, $0$ and $-1$, and indeed $w_{01} - w_{12} = (1 - y, x) - (-y, x) = (1, 0)$. So the discrete gradient is the edge-vertex incidence matrix, one case of the exact sequence above.

**Example: hexahedra.** On a cube the lowest order space has one unknown per edge, 12 in total, and the $x$ component of a field is a function of $y$ and $z$ only, linear in each, with similar forms for the other components.

**Non-example: continuous nodal vector fields.** Continuous piecewise linear vector fields are in $H(\mathrm{curl})$, but they also force a continuous normal component. At an interface between two materials the normal component of the electric field jumps, so these fields cannot follow it. For the Maxwell eigenvalue problem, nodal elements can produce spurious eigenvalues on some meshes, while the Nédélec spaces give the correct spectrum (theorem, see Boffi, Brezzi and Fortin, Chapter 11).

**Non-example: the Raviart-Thomas space in 3D.** It has a continuous normal component, not a continuous tangential one, so it is in $H(\mathrm{div})$ and not in $H(\mathrm{curl})$. It is the right space for the magnetic flux density, not for the electric field.

## Related definitions

- **Nédélec spaces of the second kind** (Nédélec 1986): the full space $P_k(K)^3$ with tangential moments, dimension $(k + 1)(k + 2)(k + 3)/2$. They are more accurate in $L^2$ for the same curl accuracy.
- **[Raviart-Thomas element](/raviart-thomas-element/):** the $H(\mathrm{div})$ counterpart. In 2D the Nédélec space of the first kind is the Raviart-Thomas space rotated by 90 degrees.
- **[Yee scheme](/yee-fdtd-scheme/):** on a uniform brick mesh, the lowest order Nédélec unknowns sit at the same places as the electric field components of the Yee grid, the tangential components along the edges, and with a lumped mass matrix the two methods are closely related.
- **[Perfectly matched layer](/perfectly-matched-layer/):** absorbing layers for wave problems on unbounded domains, often used with Nédélec spaces.
- **[Helmholtz-Hodge decomposition](/helmholtz-hodge-decomposition/):** the split of a field into a gradient and a divergence-free part. Its discrete form on the Nédélec space separates the large kernel of the curl, the gradients of Lagrange functions, which a solver for the curl-curl problem must handle, for example with a multiplier or a special multigrid smoother.
- **Finite element exterior calculus.** In the notation of Arnold, Falk and Winther, $N_k = \mathcal{P}_k^-\Lambda^1$ (first kind) and the second kind is $\mathcal{P}_k\Lambda^1$.

## References
