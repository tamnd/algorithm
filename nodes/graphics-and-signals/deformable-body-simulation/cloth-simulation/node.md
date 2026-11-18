---
tag: 6XGTZ1
kind: problem
slug: cloth-simulation
name: Cloth simulation
aliases:
- cloth animation
area: graphics-and-signals/deformable-body-simulation
level: core
summary: Compute the motion of a sheet or garment that stretches little, bends easily, and collides with bodies and with itself. Stiff stretch against soft bending makes explicit steps small.
model: real-ram
prereqs: [mass-spring-system]
see_also: [baraff-witkin-cloth, provot-strain-limiting, fast-mass-spring, discrete-shells, robust-cloth-collision, position-based-dynamics, projective-dynamics, continuous-collision-detection]
sources:
  - book: isbn:9781568810904
    title: "Donald H. House and David E. Breen (editors), Cloth Modeling and Animation, A K Peters, 2000"
    locator: the whole book (models of cloth, their parameters and their numerics; general locator)
  - paper: doi:10.20380/GI1995.17
    title: "Xavier Provot, Deformation constraints in a mass-spring model to describe rigid cloth behavior, Graphics Interface 95, 147-154, 1995"
    locator: "Section 3 (the super-elastic effect: springs stretched past 100%) and Section 4 (the critical stiffness for a given time step)"
  - paper: doi:10.1145/280814.280821
    title: "David Baraff and Andrew Witkin, Large steps in cloth simulation, Proceedings of SIGGRAPH 98, 43-54, 1998"
    locator: "Section 1 (why explicit methods need small steps for stiff stretch) and Section 8 (running times per frame as the mesh grows)"
  - paper: doi:10.1145/566654.566623
    title: "Robert Bridson, Ronald Fedkiw and John Anderson, Robust treatment of collisions, contact and friction for cloth animation, ACM Transactions on Graphics 21(3), 594-603, 2002"
    locator: "Section 5 (the split of internal dynamics and collision processing in one time step) and Sections 6 and 7 (proximity, collisions, friction and impact zones)"
  - url: http://www.cs.columbia.edu/cg/pdfs/9-QuadBend.pdf
    title: "Miklós Bergou, Max Wardetzky, David Harmon, Denis Zorin and Eitan Grinspun, A quadratic bending model for inextensible surfaces, Eurographics Symposium on Geometry Processing 2006"
    locator: "Section 1 (stretching stiffness exceeds bending stiffness by four or more orders of magnitude) and Section 3 (cloth as nearly inextensible)"
---

Cloth simulation asks for the motion of a thin sheet, such as a garment, a flag or a curtain, under gravity, wind and contact. Cloth hardly stretches, bends with almost no effort, and touches the body under it and itself in many places at once. These three facts make the problem hard: the stiff stretch forces limit explicit time steps, the soft bending makes fine folds, and the contacts must never let the sheet pass through anything. This page states the problem and lists the methods; each method has its own page, starting with the [mass-spring system](/mass-spring-system/).

## In plain words

A piece of cloth is cut into many small triangles or a grid of points. The computer must move every point from one frame to the next so that the cloth falls, swings and folds as real cloth does.

Cloth resists being pulled longer very strongly, but it folds very easily. A simple computer step that takes small forward guesses must use tiny time steps, or the strong pull makes the points shake and fly apart. Methods that solve for the next state as a whole can take large steps, but each step costs more.

The cloth must also never pass through the body that wears it or through itself. Points move in jumps from one frame to the next, so a check only at the end of a step can miss a crossing. Good methods check the whole path of each point during the step.

## Definition

**Input.** A triangle mesh (or a grid) of the cloth with $n$ vertices and $m$ triangles or springs. Each vertex has a mass, a rest position in the flat pattern (material coordinates $(u, v)$), a current position $\mathbf x_i$ and a velocity $\mathbf v_i$. An elastic model for stretch, shear and bending, and a damping model. External forces such as gravity $(0, -9.81, 0)$ m/s$^2$ and wind. Obstacles given as moving meshes, a list of pinned vertices, a cloth thickness $h$, a friction coefficient $\mu$, a time step $\Delta t$ and a number of frames.

**Output.** The positions of all vertices at each frame, such that:

- the motion approximates the solution of $M \ddot{\mathbf x} = \mathbf f(\mathbf x, \dot{\mathbf x}) + \mathbf f_{\text{ext}}$ for the chosen elastic and damping forces;
- the cloth does not intersect itself or the obstacles, and in the stronger form stays at least $h$ away from them;
- contacts obey a friction law, usually [Coulomb friction](/coulomb-friction-law/) on the relative tangential velocity.

**Cost model.** The real RAM. The cost is given per time step and per solver iteration, in $n$ vertices, $m$ elements, $c$ contacts, $k$ iterations and $s$ substeps. An iteration count is a measurement unless a method states a convergence bound.

The goal of graphics is a plausible motion at the frame rate, not an accurate answer for one fabric. The output is judged by eye, and the parameters are tuned. Measured fabric parameters exist, but they are not part of the problem here.

## Variants

- **Explicit or implicit time stepping.** Explicit methods cost little per step but need steps below the stability limit of the stiffest spring. Implicit methods solve a large system per step and can take steps of a frame or more.
- **Stretch as a force or as a constraint.** Most models treat stretch as a stiff elastic force. Others treat the cloth as inextensible or limit the strain to a few percent ([Provot's strain limiting](/provot-strain-limiting/)).
- **Bending model.** Bending springs, or an energy in the dihedral angles ([discrete shells](/discrete-shells/), [quadratic bending model](/quadratic-bending-model/)).
- **With or without self-collision.** A flag in the wind can skip self-collision. A garment cannot.
- **Real time or offline.** Games use a few iterations of a position solver per frame and accept errors. Film uses implicit solvers and robust collision handling, and spends seconds per frame.

## Examples

**The step limit under refinement.** Take a grid with particles of mass $m = 10^{-3}$ kg and stretch springs of $k = 10^3$ N/m. One particle on one spring has $\omega = \sqrt{k/m} = 10^3$ rad/s, so [symplectic Euler](/symplectic-euler-method/) needs $\Delta t < 2/\omega = 2$ ms, and a network needs less. Halve the grid spacing for the same cloth. Each particle now carries a quarter of the mass, while a stretch spring keeps the same stiffness, so $\omega$ doubles and the step limit halves to at most 1 ms. There are four times as many particles and twice as many steps, so one second of motion costs eight times as much. In general an explicit 2D cloth of $n$ particles costs $\Theta(n^{3/2})$ per second of motion.

**Stretch against bending.** Bergou et al. (2006) state that for inextensible plates and shells, which they take cloth to be, the stretching stiffness is greater than the bending stiffness by four or more orders of magnitude. The bending forces then decide the shape of the folds, while the stretch forces decide the step size.

**Super-elasticity.** Provot (1995) hung a 17 by 17 grid of springs by two corners. With a stiffness low enough for his time step, the springs near the corners stretched by more than 100%, while woven cloth stretches by about 10% at most. A stiffer spring would need a smaller step; his fix was to limit the strain after each step.

## Known algorithms

Internal forces and time stepping:

- [Mass-spring system](/mass-spring-system/) with explicit [symplectic Euler](/symplectic-euler-method/) steps. Cheap per step, limited by the stiffest spring.
- [Provot's strain limiting](/provot-strain-limiting/) (1995). Explicit steps with soft springs, then a pass that shortens springs stretched past a limit.
- [Baraff-Witkin cloth](/baraff-witkin-cloth/) (1998). Stretch, shear and bend conditions on triangles, and one linearized [backward Euler](/backward-euler-method/) step solved by a filtered [conjugate gradient method](/conjugate-gradient-method/).
- [Fast mass-spring simulation](/fast-mass-spring/) (2013) and [projective dynamics](/projective-dynamics/) (2014). Backward Euler as a minimization, solved by local steps and a global solve with a constant matrix.
- [Position-based dynamics](/position-based-dynamics/), [extended position-based dynamics](/extended-position-based-dynamics/) and [small steps](/small-steps-physics/). Constraint projection on positions, the usual choice in games.
- [Vertex block descent](/vertex-block-descent/) and [optimization time integration](/optimization-time-integration/). Backward Euler by descent on the incremental potential.
- Finite elements: [St. Venant-Kirchhoff](/st-venant-kirchhoff-model/) membranes and [corotational FEM](/corotational-fem/).

Bending:

- [Discrete shells](/discrete-shells/) (2003): an energy in the change of the dihedral angle of each edge.
- [Quadratic bending model](/quadratic-bending-model/) (2006): a constant quadratic form for nearly inextensible cloth with a flat rest shape.

Collisions and friction:

- [Robust cloth collision](/robust-cloth-collision/) (Bridson, Fedkiw and Anderson 2002): repulsion forces, [elementary CCD tests](/elementary-ccd-tests/) on the linear paths, Coulomb friction, and [impact zones](/impact-zones/) as the last resort.
- [Incremental potential contact](/incremental-potential-contact/): a barrier energy with a CCD-filtered line search.
- Broad phase: [bounding volume hierarchies](/bounding-volume-hierarchy/) refit each step, or [spatial hashing](/spatial-hashing/).

## Bounds

- **Lower bound per step.** Any method must read and write every vertex, so a step costs $\Omega(n)$.
- **Explicit methods.** $\Theta(n + m)$ per step, with a step limit that shrinks like the grid spacing, so $\Theta(n^{3/2})$ per second of a 2D cloth (see the example). This is a bound in the model above, for a fixed material.
- **Implicit methods.** One sparse linear solve per step. With $k$ conjugate gradient iterations it costs $O(k (n + m))$. Baraff and Witkin (1998, Section 8) measured times per frame that grow slightly better than $O(n^{1.5})$ on their scenes; that is a measurement. With a constant matrix, as in fast mass-spring, a sparse Cholesky factor is computed once, and each solve costs the size of the factor.
- **Collisions.** With a bounding volume hierarchy, a broad phase query is $O(n)$ in the worst case and much less in practice; the number of close pairs $c$ is observed, not bounded. Robust handling by iterated CCD and impact zones has no useful worst case bound on the number of iterations; the impact zones make it end, because the zones only grow.

## Reductions

- One step of backward Euler reduces to the minimization of the incremental potential $\frac{1}{2\Delta t^2} (\mathbf x - \mathbf y)^\top M (\mathbf x - \mathbf y) + E(\mathbf x)$ with $\mathbf y = \mathbf x_n + \Delta t \, \mathbf v_n + \Delta t^2 M^{-1} \mathbf f_{\text{ext}}$. Fast mass-spring, projective dynamics, vertex block descent and IPC all start from this form.
- One linearized step reduces to a sparse symmetric linear system, solved by the [conjugate gradient method](/conjugate-gradient-method/) or by [Cholesky decomposition](/cholesky-decomposition/).
- Intersection-free motion reduces to [continuous collision detection](/continuous-collision-detection/): for each vertex-triangle and edge-edge pair, find the first time in the step when the four points are coplanar and close.
- Frictional contact can be written as a complementarity problem ([linear complementarity problem](/linear-complementarity-problem/) after linearization); cloth methods in graphics usually solve it approximately by impulses.

## Applications

Clothing of characters in film and games, flags, curtains and sails in scenes, and the virtual try-on and design of garments, where the pattern pieces are simulated before the fabric is cut.

## References
