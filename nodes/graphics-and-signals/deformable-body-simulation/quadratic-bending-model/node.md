---
tag: CKV49R
kind: model
slug: quadratic-bending-model
name: Quadratic bending model
aliases:
- Bergou-Wardetzky bending
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: Under isometric deformation of a flat rest mesh, the bending energy is a quadratic form in the positions with a constant matrix of cotangent weights. Otherwise it is an approximation.
prereqs: [cotangent-laplacian, discrete-shells]
see_also: [baraff-witkin-cloth, cloth-simulation, mass-spring-system, fast-mass-spring, implicit-fairing, finite-element-method, backward-euler-method, surface-curvature]
sources:
  - paper: doi:10.2312/SGP/SGP06/227-230
    title: "Miklós Bergou, Max Wardetzky, David Harmon, Denis Zorin and Eitan Grinspun, A quadratic bending model for inextensible surfaces, Eurographics Symposium on Geometry Processing (SGP 2006), 227-230, 2006"
    locator: "Section 1 (the smooth energy and the central observation), Section 2 (the three conditions, Q = L^T M^-1 L, Crouzeix-Raviart elements and the local matrix of an interior edge), Section 3 (forces, Rayleigh damping, the test setup and the measured speedups) and Table 1"
  - paper: doi:10.2312/SCA03/062-067
    title: "Eitan Grinspun, Anil N. Hirani, Mathieu Desbrun and Peter Schröder, Discrete shells, Eurographics/SIGGRAPH Symposium on Computer Animation (SCA 2003), 62-67, 2003"
    locator: "Section 2, equation (2) (the hinge energy with the tile height, used here for comparison)"
---

The quadratic bending model, also called the isometric bending model, is a bending energy for nearly inextensible triangle meshes such as cloth. Its hypotheses are that the mesh deforms isometrically, so that every edge keeps its rest length, and that the rest shape is flat. Under these hypotheses the bending energy is $\tfrac12 \mathbf x^{\mathsf T} Q \mathbf x$ for a constant matrix $Q$ of cotangent weights, so the forces are linear in the positions and the Hessian never changes. A real simulation only keeps the edge lengths near their rest values through stiff membrane forces, so in practice the model is an approximation. It differs from [discrete shells](/discrete-shells/), which is nonlinear in the positions and allows a curved rest shape, and from the vertex based [cotangent Laplacian](/cotangent-laplacian/), whose linear elements it replaces by edge based elements.

## The machine

**The smooth model.** For a surface $S$ with mean curvature $H$, Section 1 of the paper takes the bending energy

$$E_b(S) = \frac12 \int_S H^2 \, dA = \frac12 \int_S \langle \Delta \mathbf x, \Delta \mathbf x \rangle \, dA,$$

where $\mathbf x$ is the embedding of the surface and $\Delta$ is its Laplace-Beltrami operator, so that $\Delta \mathbf x$ is the mean curvature normal. $\Delta$ depends only on the metric of $S$, and an isometric deformation does not change the metric. So for isometric deformations $\Delta$ is a fixed linear operator and $E_b$ is quadratic in $\mathbf x$. The paper calls this the *central observation*.

**The discrete model.** The positions are $\mathbf x = (\mathbf x_0, \dots, \mathbf x_{n-1}) \in \mathbb R^{3n}$ (m). A mesh deforms isometrically if all its edge lengths stay the same. Section 2 asks for an energy that is (i) quadratic in $\mathbf x$ under isometric deformation, (ii) invariant under rigid motions and (iii) invariant under a uniform scaling, and writes it as

$$E_b(\mathbf x) = \frac12 \mathbf x^{\mathsf T} Q \mathbf x = \frac12 \sum_{i, j} Q_{ij} \langle \mathbf x_i, \mathbf x_j \rangle, \qquad Q = L^{\mathsf T} M^{-1} L,$$

where $Q$ depends only on the rest mesh, $L$ is a discrete Laplacian with $\sum_j L_{ij} = 0$ and $M$ is a symmetric positive definite mass matrix that scales with the square of the length. $Q$ acts on each of the three coordinates in the same way. For cloth the paper uses the nonconforming Crouzeix-Raviart elements, whose degrees of freedom sit on the edges, and gives $Q$ as a sum of local $4 \times 4$ matrices, one per interior edge.

Label the stencil of the interior edge $e_0 = (\mathbf x_0, \mathbf x_1)$ as follows. Its triangles are $t_0 = (\mathbf x_0, \mathbf x_1, \mathbf x_2)$ and $t_1 = (\mathbf x_0, \mathbf x_1, \mathbf x_3)$ with rest areas $A_0$ and $A_1$. The other edges are $e_1 = \mathbf x_0 \mathbf x_2$, $e_2 = \mathbf x_0 \mathbf x_3$, $e_3 = \mathbf x_1 \mathbf x_2$ and $e_4 = \mathbf x_1 \mathbf x_3$, and $c_{jk}$ is the cotangent of the rest angle between $e_j$ and $e_k$. So $c_{01}$ and $c_{02}$ are at $\mathbf x_0$, and $c_{03}$ and $c_{04}$ are at $\mathbf x_1$. Then

$$K_0 = (c_{03} + c_{04},\ c_{01} + c_{02},\ -c_{01} - c_{03},\ -c_{02} - c_{04}), \qquad Q(e_0) = \frac{3}{A_0 + A_1} K_0^{\mathsf T} K_0,$$

and the local energy is $\tfrac12 (\mathbf x_0, \mathbf x_1, \mathbf x_2, \mathbf x_3) \, Q(e_0) \, (\mathbf x_0, \mathbf x_1, \mathbf x_2, \mathbf x_3)^{\mathsf T}$. A scratch check of this page confirmed the labelling: with it, $K_0$ applied to the four points of a flat stencil gives $0$.

The elastic bending force is $-\nabla E_b = -Q \mathbf x$. The paper adds Rayleigh damping $-(\alpha_1 M + \alpha_2 \nabla^2 E)\mathbf v$, whose bending part $-\alpha_2 Q \mathbf v$ is also precomputed. The energy is multiplied by a bending stiffness as in any bending model, and the paper found no need to change the material parameters when it switched from a nonlinear hinge model to this one.

```pseudo id=main
ASSEMBLE-BENDING-MATRIX(rest mesh)
L1  Q <- the zero n by n sparse matrix
L2  for each interior edge e0 = (x0, x1) with triangles (x0, x1, x2) and (x0, x1, x3):
L3      c01, c02 <- cot of the rest angles at x0 in the two triangles
L4      c03, c04 <- cot of the rest angles at x1 in the two triangles
L5      K <- (c03 + c04, c01 + c02, -c01 - c03, -c02 - c04)
L6      add 3 / (A0 + A1) K^T K to the rows and columns of x0, x1, x2, x3 in Q
L7  return Q
BENDING-FORCE(Q, x)
L8  return -Q x, for each coordinate separately
```

The standing assumptions are: the deformation is isometric, which an in-plane model with high stiffness keeps close to true (the paper treats the in-plane model as a penalty that enforces isometry); the rest shape is flat; and no rest triangle is degenerate, so the cotangents are finite. Boundary edges have no term.

## What it counts

The model gives the bending energy $E_b$ (J), the bending forces $-Q\mathbf x$ (N) and the constant bending Hessian $Q$. The assembly visits each interior edge once and costs $\Theta(|E|)$ time, once per simulation. $Q_{ij}$ is nonzero only if the vertices $i$ and $j$ lie in a common stencil, so $Q$ has at most $16 |E|$ nonzero entries, and one force evaluation is a sparse product in $O(|E|)$ time. A nonlinear hinge model also costs $O(|E|)$ per evaluation, with a larger constant, and must rebuild its Hessian at every Newton step.

The paper measured the gain (measured, hardware not given in the text): over two solvers, two scenes (cloth draped on a sphere and a flag in wind), regular and irregular meshes, and 400 to 25600 vertices, the simulation was typically two to three times faster than with a nonlinear hinge, and the bending force computation seven to eleven times faster. The overall gain depends on the share of the bending forces in the total cost.

## Relation to other models

- **[Discrete shells](/discrete-shells/)** sums $(\theta_e - \bar\theta_e)^2 |\bar e| / \bar h_e$ over the edges, with the bend angle $\theta_e$. It is nonlinear in $\mathbf x$, allows a curved rest shape, and needs a new Hessian at every step. For a flat rest shape and isometric motion, result 1 below shows that the quadratic model is the same energy with $\theta_e^2$ replaced by $4 \sin^2(\theta_e/2)$, times $\tfrac12$. The paper states that its edge based $L\mathbf x$ is the linearization about the flat rest state of the models of Bridson et al. (2003), Cohen-Steiner and Morvan, and Grinspun et al.
- **[Cotangent Laplacian](/cotangent-laplacian/).** The paper names the usual linear (Lagrange) elements as one possible basis, which gives the vertex based cotangent Laplacian. It prefers the edge based Crouzeix-Raviart elements for cloth, because there the bending happens about the edges.
- **[Baraff-Witkin cloth](/baraff-witkin-cloth/)** and bending springs of a [mass-spring system](/mass-spring-system/) give bending forces that are nonlinear in $\mathbf x$. The paper notes that some models are linearized at every step instead, and that this loses the invariance under rigid motions; the quadratic model keeps it (result 2).
- **[Fast mass-spring simulation](/fast-mass-spring/)** and [implicit fairing](/implicit-fairing/) also gain speed from a constant matrix that is set up once. Here the matrix is exact only under the hypotheses above.
- **Willmore flow.** The paper also uses the model for the fairing of surfaces, where isometry is a poor assumption; it reports that the model is still effective inside inexact Newton methods. The details are in a longer report by the same authors, which this page has not checked.

## Known results in the model

Let $\bar h_e = (\bar h_0 + \bar h_1)/6$ for the rest heights $\bar h_k = 2 A_k / |\bar e|$ of the two triangles over $e$, as on the discrete shells page, and let $\theta_e$ be the bend angle of $e$ in $\mathbf x$.

1. **The exact energy under the hypotheses (proved).** If the rest mesh is flat and $\mathbf x$ is an isometric deformation of it, then
   $$E_b(\mathbf x) = \sum_e \tfrac12 \big(2 \sin(\theta_e / 2)\big)^2 \, \frac{|\bar e|}{\bar h_e}.$$
   *Proof.* Take a triangle $(\mathbf a, \mathbf b, \mathbf c)$ with angles $\alpha$ at $\mathbf a$ and $\beta$ at $\mathbf b$, and put it in its own plane with $\mathbf a = (0, 0)$, $\mathbf b = (l, 0)$ and $\mathbf c = (p, h)$, $h > 0$. Then $\cot\alpha = p/h$, $\cot\beta = (l - p)/h$, and $\cot\beta \, \mathbf a + \cot\alpha \, \mathbf b - (\cot\alpha + \cot\beta)\, \mathbf c = (0, -l) = -l\, \mathbf u$, where $\mathbf u$ is the unit vector in the plane of the triangle that is normal to the edge and points to $\mathbf c$. The entries of $K_0$ are the sum of this expression for $t_0$ and for $t_1$, so $K_0 \mathbf x = -|e| (\mathbf u_0 + \mathbf u_1)$. An isometric deformation keeps all the angles of the triangles, so the cotangents of the deformed mesh are the rest cotangents and the formula holds for $\mathbf x$. The angle between $\mathbf u_0$ and $-\mathbf u_1$ is the bend angle $\theta_e$, so $|\mathbf u_0 + \mathbf u_1| = 2 \sin(|\theta_e| / 2)$. With $|e| = |\bar e|$ and $A_0 + A_1 = |\bar e| (\bar h_0 + \bar h_1)/2$, the local energy is $\tfrac12 \cdot 3 \cdot 4 |\bar e|^2 \sin^2(\theta_e/2) / (A_0 + A_1) = \tfrac12 (2\sin(\theta_e/2))^2 |\bar e| / \bar h_e$. $\square$
   So under the hypotheses the model is the [discrete shells](/discrete-shells/) energy with a flat rest shape, with $\theta_e^2$ replaced by $4 \sin^2(\theta_e/2) = \theta_e^2 - \theta_e^4/12 + O(\theta_e^6)$ and a factor $\tfrac12$. A scratch check with a hinge bend of $\theta = 2.5$ rad on random stencils, after a random rigid motion, matched the formula to 15 digits.
2. **Rigid motions and momentum (proved).** The entries of $K_0$ sum to $0$, so $\sum_j Q_{ij} = 0$ and a translation does not change $E_b$; a rotation $R$ keeps every $\langle \mathbf x_i, \mathbf x_j \rangle$. The forces $\mathbf f_i = -\sum_j Q_{ij} \mathbf x_j$ have the sum $-\sum_j (\sum_i Q_{ij}) \mathbf x_j = 0$, and the total torque $-\sum_{i,j} Q_{ij}\, \mathbf x_i \times \mathbf x_j$ is $0$ because $Q$ is symmetric. So the bending forces keep the linear and the angular momentum. Section 2 of the paper states that condition (ii) holds if and only if $\sum_i Q_{ij} = \sum_j Q_{ij} = 0$, with the proof in the longer report; this page proves only the direction it uses.
3. **Positive semidefinite, with the affine maps in the kernel (proved).** $Q$ is a sum of matrices $c K_0^{\mathsf T} K_0$ with $c > 0$, so $E_b \ge 0$. For a flat rest stencil, the proof of result 1 gives $K_0 \bar{\mathbf x} = 0$, and $K_0 (A \bar{\mathbf x} + \mathbf t) = A K_0 \bar{\mathbf x} + \mathbf t \sum_k K_{0,k} = 0$ for any linear map $A$ and shift $\mathbf t$. So every affine image of the flat rest mesh has zero bending energy, including in-plane stretch and shear. A scratch check found an energy below $10^{-28}$ for a random affine map.
4. **In-plane changes that are not affine give energy (proved).** Move only $\mathbf x_3$ of a flat stencil by $\boldsymbol\delta$ in the plane. Then $K_0 \mathbf x = -(c_{02} + c_{04}) \boldsymbol\delta \neq 0$ and $E_b > 0$, although nothing bends. This is the cost of the isometry hypothesis: the model relies on the in-plane forces to keep such changes small.
5. **A curved rest shape is not an equilibrium (proved).** If the rest mesh has an edge with a bend angle $\bar\theta \ne 0$ and $Q$ is built from its rest angles and areas, then by the proof of result 1 that edge gives $K_0 \bar{\mathbf x} \ne 0$, so $\bar{\mathbf x}^{\mathsf T} Q \bar{\mathbf x} > 0$ and the force $-Q \bar{\mathbf x}$ is not zero, so the rest shape is not at rest in the model. So the flat rest shape is a real hypothesis; the paper says that the extension to curved rest shapes and to anisotropy is in its longer report.
6. **Scale (proved).** If the rest mesh is scaled by $s > 0$, the cotangents and $K_0$ do not change and $A_0 + A_1$ scales by $s^2$, so $Q$ scales by $1/s^2$, which is condition (iii). The energy of the scaled positions $s\mathbf x$ is then the same as that of $\mathbf x$.
7. **Large bends (proved).** By result 1 the energy per edge is at most $2 |\bar e| / \bar h_e$, reached when the two triangles fold onto each other ($\theta_e = \pi$). At that angle the ratio $4 \sin^2(\theta/2) / \theta^2$ is $4/\pi^2 \approx 0.405$, so the model is softer than a hinge energy in $\theta^2$ for sharp folds. It has no jump at $\theta = \pm\pi$, because it is a polynomial in $\mathbf x$.
8. **Same look, less time (measured).** In the paper, cloth draped on a sphere and a flag in wind looked qualitatively the same with this model and with a nonlinear hinge model, with the same material parameters, and the runs were faster as given under "What it counts". The test framework used an implicit solver in the manner of Baraff and Witkin and explicit Euler, linear finite elements for the in-plane forces, k-DOP trees for collision detection and the collision response of Bridson et al. (2002).

## References
