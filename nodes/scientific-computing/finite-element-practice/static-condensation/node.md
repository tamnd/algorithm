---
tag: G6BEQJ
kind: technique
slug: static-condensation
name: Static condensation
area: scientific-computing/finite-element-practice
level: core
summary: Eliminates the interior degrees of freedom of each element before assembly by a Schur complement, leaving a smaller system on element boundaries.
prereqs: [finite-element-assembly, schur-complement]
see_also: [hybridizable-discontinuous-galerkin, hp-finite-element-method, spectral-element-method, domain-decomposition, gaussian-elimination, cholesky-decomposition, sparse-linear-systems, mixed-finite-element-method]
sources:
  - paper: doi:10.1002/nme.1620080115
    title: Edward L. Wilson, The static condensation algorithm, International Journal for Numerical Methods in Engineering 8(1) (1974) 198-203
    locator: the element level elimination of internal unknowns and its operation count
  - paper: doi:10.2514/3.2874
    title: Robert J. Guyan, Reduction of stiffness and mass matrices, AIAA Journal 3(2) (1965) 380
    locator: elimination of unloaded coordinates from the stiffness, and its use for the mass
  - book: isbn:9780198528692
    title: George Em Karniadakis and Spencer J. Sherwin, Spectral/hp Element Methods for Computational Fluid Dynamics, 2nd edition, Oxford University Press (2005)
    locator: static condensation of the interior modes and the boundary system for high degree elements
---

Static condensation solves a finite element system in two levels. Each element has interior unknowns, which belong to that element only, and boundary unknowns, which it shares with its neighbors. Because the interior unknowns of one element do not couple to any other element, they can be eliminated element by element before assembly: the element matrix is replaced by its [Schur complement](/schur-complement/) $S = K_{BB} - K_{BI}K_{II}^{-1}K_{IB}$ on the boundary unknowns. The global system then has only the boundary unknowns. After it is solved, each element recovers its interior values from its own small system. The result is exactly the solution of the full system, because static condensation is block Gaussian elimination in a good order. It is not an approximation. For high degree elements most unknowns are interior, so the global system becomes much smaller.

## In plain words

Some unknowns live inside one element and talk only to the other unknowns of the same element. You can solve for them in terms of the unknowns on the element's edges before you build the big system. Each element then gives a smaller matrix that only connects edge unknowns. You build and solve the big system for the edge unknowns only. At the end, go back to each element and compute its inside unknowns from the edge values you now know. Nothing is lost: the answer is the same as when you solve the whole system at once. It is just a way to do the elimination in pieces.

## When it applies

- **The interior unknowns are private.** An unknown can be condensed on element $K$ only if no other element uses it. This holds for the interior nodes or bubble functions of $H^1$ elements, for the cell unknowns of [hybridized mixed](/mixed-finite-element-method/) and [HDG](/hybridizable-discontinuous-galerkin/) methods, and for the interior of a subdomain in [domain decomposition](/domain-decomposition/).
- **The interior block is invertible.** $K_{II}$ must be nonsingular. For a symmetric positive definite element matrix it is: a principal submatrix of an SPD matrix is SPD. For a singular element matrix, like a pure Neumann element stiffness, the interior block is still SPD as long as the interior functions do not include a constant.
- **A linear static problem.** For $KU = F$ the method is exact. For a dynamic problem $M\ddot U + KU = F$ the interior unknowns have inertia too, and eliminating them with the stiffness alone, as Guyan did, is an approximation.

## The template

```pseudo id=main
CONDENSE(K, F, I)                                      ▷ one element; I = its interior local unknowns
L1  B <- the local unknowns that are not in I
L2  factor K_II = L L^T; X_K <- K_II^{-1} K_IB; X_F <- K_II^{-1} F_I
L3  S <- K_BB - K_BI X_K; g <- F_B - K_BI X_F            ▷ the Schur complement and the condensed load
L4  return S, g, X_K, X_F

SOLVE-CONDENSED(elements)
L5  for each element: (S, g, X_K, X_F) <- CONDENSE(K, F, I); add S and g into the global boundary system
L6  apply the boundary conditions and solve the global boundary system for u_B
L7  for each element: u_I <- X_F - X_K u_B               ▷ local recovery
L8  return u
```

**Why it is exact.** Write the full system with all interior unknowns first:
$$\begin{pmatrix} K_{II} & K_{IB} \\ K_{BI} & K_{BB}\end{pmatrix}\begin{pmatrix} u_I \\ u_B\end{pmatrix} = \begin{pmatrix} F_I \\ F_B\end{pmatrix}.$$
The first block row gives $u_I = K_{II}^{-1}(F_I - K_{IB}u_B)$. Put it into the second row: $(K_{BB} - K_{BI}K_{II}^{-1}K_{IB})u_B = F_B - K_{BI}K_{II}^{-1}F_I$. Because the interior unknowns of different elements do not couple, the global $K_{II}$ is block diagonal with one block per element. So its inverse is the block diagonal of the element inverses, and the global Schur complement is the sum of the element Schur complements, assembled like ordinary element matrices. Line L5 does exactly that, and line L7 is the first block row.

**Energy view.** For an SPD element matrix, $u_B^{\mathsf T}Su_B = \min_{u_I}(u_I, u_B)^{\mathsf T}K(u_I, u_B)$, and the minimizer is the recovered $u_I$ when the load is 0. So $S$ is SPD, and the condensed element is the stiffest response of the element to given boundary values.

## Classic examples

**The P2 element in 1D condenses to P1.** For $-u'' = 1$, the P2 element on $[x_L, x_R]$ of length $h$ with unknowns (left, right, middle) has
$$K = \frac{1}{3h}\begin{pmatrix} 7 & 1 & -8 \\ 1 & 7 & -8 \\ -8 & -8 & 16\end{pmatrix}, \qquad F = h\begin{pmatrix}\tfrac16 \\ \tfrac16 \\ \tfrac23\end{pmatrix}.$$
Condense the middle unknown. $K_{II} = 16/(3h)$ and $K_{BI} = -8/(3h)$ for both ends, so $K_{BI}K_{II}^{-1}K_{IB}$ has all four entries $\tfrac{64}{9h^2}\cdot\tfrac{3h}{16} = \tfrac{4}{3h}$, and
$$S = \frac{1}{3h}\begin{pmatrix} 3 & -3 \\ -3 & 3\end{pmatrix} = \frac1h\begin{pmatrix} 1 & -1 \\ -1 & 1\end{pmatrix}, \qquad g = \frac h6 + \frac{8}{3h}\cdot\frac{3h}{16}\cdot\frac{2h}{3} = \frac h2.$$
That is the P1 element matrix with the P1 load. So the vertex values of P2 are the P1 vertex values, which in 1D are exact. The recovery gives $u_{\text{mid}} = \tfrac12(u_L + u_R) + \tfrac{h^2}{8}$, which is the exact value of the quadratic solution at the midpoint. The test file checks this, and it checks that the condensed solve and the full solve agree on P2 meshes and on chains of random SPD elements.

**High degree quadrilaterals.** A $\mathcal{Q}_p$ element has $(p+1)^2$ unknowns, of which $(p-1)^2$ are interior and $4p$ are on the boundary. For $p = 8$ that is 49 interior and 32 boundary unknowns out of 81. In the [hp finite element method](/hp-finite-element-method/) and the [spectral element method](/spectral-element-method/), condensation removes most of the unknowns from the global system, and the boundary system has a much smaller bandwidth.

**Hybridization.** In HDG and hybridized mixed methods, all cell unknowns are interior, and the only global unknowns are on the faces. Condensation is what makes these methods competitive: the global system is a sparse system for a single face function.

**Substructuring.** Treat a whole subdomain as one element. Its interior is condensed, and the interface problem with the Schur complement is the starting point of the iterative substructuring methods of domain decomposition.

## Variations

- **Condense, then solve iteratively.** The Schur complement system is better conditioned than the full system for many problems, and it can be solved by the [conjugate gradient method](/conjugate-gradient-method/) without forming $S$, using one interior solve per element in each product.
- **Static condensation in parallel.** The condensation of all elements is independent, so it runs in parallel with no communication.
- **Recursive condensation.** Condense the element interiors, then group elements into patches and condense the patch interiors, and so on. This is the nested dissection idea, and it is how multifrontal direct solvers work.
- **Guyan reduction.** Apply the transformation $u_I = -K_{II}^{-1}K_{IB}u_B$ also to the mass matrix. This gives a smaller eigenvalue problem that is accurate for the low frequencies, but it is no longer exact.
- **Condensation of a nonlinear problem.** In Newton's method, condense the tangent matrix in each step. The interior residual must then be part of the condensed load.

## Pitfalls

- **Shared unknowns.** Condensing an unknown that another element also uses gives a wrong answer. The interior set must be private to the element.
- **Do not form the inverse.** Compute $K_{II}^{-1}K_{IB}$ with one Cholesky factorization and several triangular solves, as the code does. An explicit inverse costs more and loses accuracy.
- **Storage for the recovery.** The recovery needs $X_K$ and $X_F$, or the factorization of $K_{II}$, for every element. Keep them, or recompute the element matrices after the global solve.
- **Fill in the boundary system.** The Schur complement of an element is dense on its boundary unknowns. For a low degree element with few interior unknowns, this can make the global matrix denser than it was, with little gain. Use condensation when the interior is large.
- **Dynamics.** The Schur complement of the stiffness alone does not give the right inertia. Do not treat Guyan reduction as exact.
- **Boundary conditions on interior unknowns.** If a Dirichlet condition fixes an interior unknown, move it to the right side before condensation.

## Exercises

1. Show that $S$ is symmetric positive definite when $K$ is. *Answer:* for $u_B \ne 0$, let $u_I = -K_{II}^{-1}K_{IB}u_B$. Then $(u_I, u_B)^{\mathsf T}K(u_I, u_B) = u_B^{\mathsf T}Su_B$, and the left side is positive because $(u_I, u_B) \ne 0$.
2. Count the operations of condensing one element with $i$ interior and $b$ boundary unknowns by Cholesky. *Answer:* $i^3/3$ for the factorization, $2i^2b$ for the $b$ solves, and $2ib^2$ for $K_{BI}X_K$, so $O(i^3 + i^2b + ib^2)$.
3. For the 1D P2 element with the load $f$ constant, find the recovered midpoint value. *Answer:* $u_{\text{mid}} = \tfrac12(u_L + u_R) + fh^2/8$.
4. Why does condensation of all unknowns except one give the exact value of that unknown? *Answer:* it is Gaussian elimination of all other unknowns, and the last equation is $S\,u = g$ with a $1 \times 1$ Schur complement.

## References
