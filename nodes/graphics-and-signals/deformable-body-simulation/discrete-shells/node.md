---
tag: RG1SSM
kind: model
slug: discrete-shells
name: Discrete shells
aliases:
- discrete shell model
area: graphics-and-signals/deformable-body-simulation
level: advanced
summary: A thin shell model for triangle meshes. Membrane terms plus a bending energy that sums, over edges, the squared change of the bend angle times the rest edge length over a rest height.
prereqs: [surface-curvature, mass-spring-system]
see_also: [quadratic-bending-model, baraff-witkin-cloth, cloth-simulation, discrete-elastic-rods, elastically-deformable-models, newmark-beta-method, automatic-differentiation, cotangent-laplacian]
sources:
  - paper: doi:10.2312/SCA03/062-067
    title: "Eitan Grinspun, Anil N. Hirani, Mathieu Desbrun and Peter Schröder, Discrete shells, Eurographics/SIGGRAPH Symposium on Computer Animation (SCA 2003), 62-67, 2003"
    locator: "Section 2 (equations (1) to (3), the lumped masses, the damping force and the remark on Gaussian curvature), Section 3 (the curved rest shape, Newmark steps and automatic differentiation), Section 4 (beams, hats and paper) and the appendix (the tile height and the simplified energy)"
  - paper: doi:10.2312/SGP/SGP06/227-230
    title: "Miklós Bergou, Max Wardetzky, David Harmon, Denis Zorin and Eitan Grinspun, A quadratic bending model for inextensible surfaces, Eurographics Symposium on Geometry Processing (SGP 2006), 227-230, 2006"
    locator: "Section 2 (the edge based mean curvature vector is the linearization of the models of Grinspun et al. and others about a flat rest state)"
---

Discrete shells is a model of thin flexible objects, such as hats, leaves, paper and cans, on a triangle mesh. A *shell* differs from a *plate*: a plate is flat when it is at rest, and a shell has a curved rest shape. The model keeps the membrane energies of a cloth simulator and replaces its bending term by an energy in the change of the angle at each edge, measured against a rest mesh that can be curved. It differs from bending springs of a [mass-spring system](/mass-spring-system/), which cannot tell the sign of a fold, and from the [quadratic bending model](/quadratic-bending-model/), which is its linearization about a flat rest shape for isometric motion.

## The machine

The input is a 2-manifold triangle mesh with deformed positions $\mathbf x_i \in \mathbb R^3$ (m) and rest positions $\bar{\mathbf x}_i \in \mathbb R^3$ (m). The rest mesh does not have to be flat. A bar marks a rest quantity. For an edge $e$ the length is $|e|$. For a triangle the area is $A$. For an interior edge $e$ with the two triangles $t_0$ and $t_1$, the *bend angle* $\theta_e$ is the signed angle between the normals of $t_0$ and $t_1$, which is $\pi$ minus the dihedral angle; it is $0$ when the two triangles are flat. The rest heights of the two triangles over $e$ are $\bar h_0 = 2 \bar A_0 / |\bar e|$ and $\bar h_1 = 2 \bar A_1 / |\bar e|$, and

$$\bar h_e = \tfrac16 (\bar h_0 + \bar h_1),$$

which is a third of the average of the two heights (Section 2 and the appendix of the paper give the two forms of the same constant).

The energy is $W = k_L W_L + k_A W_A + k_B W_B$ (equation (3)) with

$$W_L = \sum_e \Big(1 - \frac{|e|}{|\bar e|}\Big)^2 |\bar e|, \qquad W_A = \sum_t \Big(1 - \frac{A_t}{\bar A_t}\Big)^2 \bar A_t, \qquad W_B = \sum_e (\theta_e - \bar\theta_e)^2 \, \frac{|\bar e|}{\bar h_e}$$

(equation (2) for $W_B$). $W_L$ and $W_A$ are the membrane terms of the reference code of the paper, and the authors say that any membrane model with small membrane strain will do. $W_L$ has the unit m, $W_A$ has m$^2$ and $W_B$ has no unit, so $k_L$ is in N, $k_A$ in N/m and the bending stiffness $k_B$ in J. The stiffnesses are set by the user.

The masses are lumped: vertex $i$ gets a third of the rest area of its triangles times the area density $\rho$ (kg/m$^2$). The motion is $\ddot{\mathbf x} = -M^{-1} \nabla W(\mathbf x)$, plus an optional damping force proportional to $(\dot\theta_e - \dot{\bar\theta}_e) \nabla\theta_e$ per edge. The paper steps this with the [Newmark method](/newmark-beta-method/) with $\beta = 1/4$ for production runs, $\beta = 0$ for debugging and $\gamma = 1/2$ for the least numerical damping, and takes the gradients and Hessians by [automatic differentiation](/automatic-differentiation/).

The bending term comes from the squared change of the mean curvature (equation (1)):

$$[\operatorname{Tr}(\varphi^* S) - \operatorname{Tr}(\bar S)]^2 = 4 (H \circ \varphi - \bar H)^2,$$

where $S$ is the shape operator and $H$ the mean curvature. The appendix cuts the rest surface into one diamond tile per edge, made of the edge and the barycenters of its two triangles. The integral of $H \circ \varphi - \bar H$ over a tile is $(\theta_e - \bar\theta_e) |\bar e|$ (the authors cite Cohen-Steiner and Morvan), and the tile has the area $(\bar A_0 + \bar A_1)/3 = |\bar e| \bar h_e$. So the mean of the difference over the tile is $(\theta_e - \bar\theta_e)/\bar h_e$. The authors then set the integral of the square equal to the area times the squared mean, which they state for fine meshes with no degenerate triangles. This gives the term of $W_B$, with the factor 4 put into $k_B$.

```pseudo id=main
DISCRETE-SHELL-ENERGY(x, xbar, mesh, kL, kA, kB)
L1  W <- 0
L2  for each edge e: W <- W + kL (1 - |e| / |ebar|)^2 |ebar|
L3  for each triangle t: W <- W + kA (1 - A_t / Abar_t)^2 Abar_t
L4  for each interior edge e = (x0, x1) with triangles (x0, x1, x2) and (x0, x1, x3):
L5      n0 <- (x1 - x0) x (x2 - x0), n1 <- (x3 - x0) x (x1 - x0)
L6      theta <- atan2((n0 x n1) . (x1 - x0) / |x1 - x0|, n0 . n1)
L7      thetabar <- the same angle on the rest mesh
L8      hbar <- (hbar_0 + hbar_1) / 6
L9      W <- W + kB (theta - thetabar)^2 |ebar| / hbar
L10 return W
```

The rest quantities $|\bar e|$, $\bar A_t$, $\bar\theta_e$ and $\bar h_e$ are computed once. The use of atan2 on L6 is a choice of this page that keeps the angle accurate near $0$ and near $\pm\pi$.

The standing assumptions are: the object is thin (the paper takes a width to thickness ratio above 100); the deformation is mostly isometric, so the membrane stiffness is high; the membrane and bending energies are separate, which the authors call a reasonable simplification for animation; and the mesh is fine and has no degenerate triangles, for the derivation of $W_B$.

## What it counts

The model gives the elastic energy $W$ (J), the internal forces $-\nabla W$ (N) and, with a time stepper, the motion of the shell. Each edge term depends on the four vertices of the two triangles of the edge, so one evaluation of $W$ or of $\nabla W$ costs $\Theta(|E| + |F|)$ time for $|E|$ edges and $|F|$ triangles, which is $O(n)$ for a mesh of $n$ vertices and bounded genus. The Hessian has a dense $12 \times 12$ block per interior edge and $9 \times 9$ per triangle, so it is sparse with $O(n)$ nonzeros, and it changes with $\mathbf x$ at every step. The paper gives no operation counts; its runs took from a few minutes to a few hours on a 2 GHz Pentium 4 (measured, the mesh sizes are not given).

## Relation to other models

- **Bending springs.** A [mass-spring system](/mass-spring-system/) resists bending by springs across the edges, which are coupled with stretch and see only the distance of the two far vertices. The paper notes that these springs are not sensitive to the sign of the dihedral angle, so they cannot hold a curved rest shape.
- **[Baraff-Witkin cloth](/baraff-witkin-cloth/).** Its bend condition is also a function of the angle between two triangle normals, but on a flat rest shape. The paper says that a cloth code of this kind becomes a shell code when the rest mesh is stored in 3D and $\bar\theta_e$ is computed from it; stored rest angles on a flat rest mesh only allow developable shapes.
- **[Elastically deformable models](/elastically-deformable-models/).** Terzopoulos et al. use the difference of the metric and curvature tensors of a smooth surface and discretize at the end. Discrete shells defines the energy on the triangle mesh directly; the authors place their model in that framework.
- **[Quadratic bending model](/quadratic-bending-model/).** For a flat rest shape and isometric motion, Bergou et al. show that the edge based mean curvature vector is the linearization of this model, and of the models of Bridson et al. (2003) and Cohen-Steiner and Morvan, about the flat state. Result 7 below gives the exact relation for one edge.
- **Bridson, Marino and Fedkiw (2003).** In the same proceedings they treat bending and wrinkles of cloth with a similar formula; the paper says so in Section 2.
- **[Discrete elastic rods](/discrete-elastic-rods/)** use the same discrete geometric approach for curves: a curvature on the mesh, a rest value and a squared difference.
- **Finite element shells.** Kirchhoff-Love shell elements, for example on subdivision surfaces, solve the continuum shell equations. The paper presents its model as a simpler path with the same kind of behaviour, not as a discretization with a convergence proof.

## Known results in the model

1. **Rigid motions and momentum (proved).** Each term of $W$ depends only on edge lengths, triangle areas and bend angles of $\mathbf x$, which do not change under a rigid motion. So the internal forces have zero sum and zero total torque, and they keep the linear and the angular momentum. The same holds for a rigid motion of the rest mesh.
2. **The rest shape is an equilibrium (proved).** Every term is a square that is zero at $\mathbf x = \bar{\mathbf x}$, so $W(\bar{\mathbf x}) = 0$ is the minimum and $\nabla W(\bar{\mathbf x}) = 0$. This holds for a curved rest shape too, which is the point of the model. If the rest angles $\bar\theta_e$ are changed so that no surface with the rest lengths has them, the rest state is no longer free of stress; the paper shows this with a sheet of paper creased on one half.
3. **The sign of a fold counts (proved).** $\theta_e$ is signed. An edge with rest angle $\bar\theta$ that is bent to $-\bar\theta$ has the bending energy $4 \bar\theta^2 k_B |\bar e| / \bar h_e$, not $0$. A spring between the two far vertices of a flat pair of triangles has the same length for the angles $\theta$ and $-\theta$, by the reflection in the plane of the other triangle.
4. **Scale (proved).** If $\mathbf x$ and $\bar{\mathbf x}$ are both scaled by $s > 0$, then $\theta_e$, $\bar\theta_e$ and $|\bar e| / \bar h_e$ do not change, so $W_B$ does not change. The smooth energy $\int H^2 \, dA$ has the same property. $W_L$ scales with $s$ and $W_A$ with $s^2$.
5. **Mean, not Gaussian, curvature (proved).** The determinant of the shape operator in place of the trace gives the Gaussian curvature. It depends only on the metric (Gauss's Theorema Egregium), so its change is zero under isometric deformation, which is pure bending, and an energy in it would not resist bending. The paper uses this argument to choose the mean curvature.
6. **The simplified energy (stated by the authors, with a measurement).** The term $(\theta_e - \bar\theta_e)^2 |\bar e|$, without $\bar h_e$, depends only on the shape and not on the triangulation. The appendix states that no discretization of equation (1) on piecewise planar surfaces can both depend only on the shape and converge under refinement, because the integral of the squared mean curvature of a polyhedral surface is in general unbounded. The paper gives this argument in two sentences and not as a full proof. In the hat runs on meshes with near uniform sampling, the simplified term gave results that the authors found satisfactory (measured, by visual comparison); they recommend equation (2) for meshes with nonuniform sampling.
7. **Relation to the quadratic bending model (proved).** Take a flat rest pair of triangles, and an isometric bend by the angle $\theta$ about the edge. The local energy of the [quadratic bending model](/quadratic-bending-model/) is then $\tfrac12 (2 \sin(\theta/2))^2 |\bar e| / \bar h_e$ (result 1 on that page). So it equals $\tfrac12 W_B$ for the edge, up to a relative error of $\theta^2/12$ to leading order, since $4 \sin^2(\theta/2) = \theta^2 - \theta^4/12 + O(\theta^6)$. A check on five random stencils gave the ratio $0.4999958$ at $\theta = 0.01$, which is $\tfrac12 (1 - \theta^2/12)$ to the printed digits.
8. **Beams, hats and paper (measured).** In the paper, a beam fixed at one end with the bending stiffnesses 100, 1000 and 10000 is more rigid for higher stiffness, and a beam with a V shaped cross section is more rigid than a flat beam with the same stiffness. A simulated hat dropped on a table was compared with video of a real hat and the brim bends in the same way; the comparison is visual. Plastic deformation is made by a change of the rest angles $\bar\theta_e$, which bends the rest shape without stretch; a change of $\bar{\mathbf x}$ itself could add membrane strain.

## References
