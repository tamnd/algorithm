---
tag: W2E44J
kind: algorithm
slug: distance-based-formation-control
name: Distance-based formation control
aliases:
- gradient formation control
area: robotics/multi-robot-systems
level: research
summary: Each robot follows the gradient of the squared errors of its distances to neighbors, which converges locally when the target framework is infinitesimally rigid.
solves: [formation-control]
model: real-ram
complexity:
  vars: {r: the number of robots, m: the number of edges, k: the number of integration steps}
  time: {per_step: O(r + m), total: O(k (r + m))}
  space: {extra: O(r + m)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 2009
  people: [Laura Krick, Mireille E. Broucke, Bruce A. Francis]
  note: Krick, Broucke and Francis proved in 2009 that the gradient law of the squared distance errors makes an infinitesimally rigid target formation locally asymptotically stable, with a center manifold argument.
prereqs: [formation-control, rigidity-matrix, infinitesimal-rigidity]
see_also: [laman-theorem, generic-rigidity, bar-and-joint-framework, leader-follower-formation-control, laplacian-consensus-protocol, distance-geometry-problem, lasalle-invariance-principle, gradient-descent]
sources:
  - paper: doi:10.1080/00207170802108441
    title: Laura Krick, Mireille E. Broucke and Bruce A. Francis, Stabilisation of infinitesimally rigid formations of multi-robot networks, International Journal of Control 82(3), 2009
    locator: pages 423 to 439 (the gradient law, the invariance of the centroid and of the collinear set, and local asymptotic stability of infinitesimally rigid targets by center manifold theory)
  - paper: doi:10.1016/j.automatica.2014.10.022
    title: Kwang-Kyo Oh, Myoung-Chul Park and Hyo-Sung Ahn, A survey of multi-agent formation control, Automatica 53, 2015
    locator: pages 424 to 440 (the distance-based class of formation control and its sensing and interaction requirements)
  - paper: doi:10.1109/TAC.2010.2053735
    title: Florian Dörfler and Bruce Francis, Geometric analysis of the formation problem for autonomous robots, IEEE Transactions on Automatic Control 55(10), 2010
    locator: pages 2379 to 2384 (the triangle formation, its incorrect equilibria, and convergence from every start that is not collinear)
  - book: isbn:9780691140612
    title: Mehran Mesbahi and Magnus Egerstedt, Graph Theoretic Methods in Multiagent Networks, Princeton University Press, 2010
    locator: Chapter 6, Formation Control (Section 6.3 on shape-based control), and Chapter 7, Section 7.4 (formation control revisited with weighted graphs)
---

Distance-based formation control turns a [bar-and-joint framework](/bar-and-joint-framework/) into a control law. The robots are the joints, the graph edges are the bars, and each bar has a target length $d_{ij}$. Each robot moves down the gradient of $V = \frac14 \sum_{\{i,j\}} (\lVert p_i - p_j \rVert^2 - d_{ij}^2)^2$, so $\dot p = -R(p)^T e$, where $R$ is the [rigidity matrix](/rigidity-matrix/) and $e$ is the vector of squared length errors. The robots need only the relative positions of their neighbors, in their own frames, and no common frame. If the target framework is [infinitesimally rigid](/infinitesimal-rigidity/), the target shape is locally exponentially stable: from every start close to it, the robots converge to a congruent copy. A generic framework in the plane whose graph contains a spanning [Laman graph](/laman-theorem/) is infinitesimally rigid, so the graph theory of rigidity tells which sensing graphs can hold a shape. Convergence is only local, and the law has other equilibria, for example collinear ones.

## In plain words

Picture a few robots joined by invisible elastic bands of chosen lengths. Each robot can see its band partners, but it has no compass and no map. If a band is longer than its target, the two robots pull toward each other. If it is too short, they push apart. Each robot adds up the pulls and pushes on its bands and moves in that direction.

If enough bands are used, so that the bands alone fix the shape, the robots settle into that shape. The shape can end up shifted or turned, because no robot knows where north is. With too few bands, the group can settle into a bent version of the shape. A bad start, such as all robots in one straight line, can also trap the group in a wrong shape.

## The problem

**The model.** There are $r$ robots in the plane with positions $p_i \in \mathbb{R}^2$ (in meters) and the single integrator model $\dot p_i = u_i$. A fixed, undirected, connected graph $G = (V, E)$ with $m$ edges says which robots sense each other. Robot $i$ measures $z_{ij} = p_i - p_j$ for each neighbor $j$, in its own frame; the law needs no common orientation, because it is equivariant under rotations. Time is continuous, and all robots act at the same time. Unicycle robots can use the law after [feedback linearization](/feedback-linearization/) of a point ahead of the wheel axle, as Krick, Broucke and Francis do.

**Input.** The graph, a target distance $d_{ij} > 0$ for each edge, which must be realizable, and the initial positions $p(0)$.

**Output.** A trajectory $p(t)$ with $\lVert p_i(t) - p_j(t) \rVert \to d_{ij}$ on every edge. When the target framework is rigid, this fixes the shape up to a translation, a rotation and possibly a reflection.

**How it differs from close pages.** [Formation control](/formation-control/) is the problem, with several kinds of specification. In displacement-based control the robots know a common orientation and run the [Laplacian consensus protocol](/laplacian-consensus-protocol/) on $p_i - c_i$, which converges globally but needs a compass. In [leader-follower formation control](/leader-follower-formation-control/) each follower tracks one or two leaders, and the graph is a tree. The distance-based law needs no compass, but it needs rigidity and gives only local convergence. The [distance geometry problem](/distance-geometry-problem/) asks for positions with given distances as a computation; this law solves it by a physical gradient flow, one robot per point.

## The algorithm

```pseudo id=main
DISTANCE-FORMATION(G, d, p(0), T, h)
L1  each robot i learns its neighbors N_i and the target distances d_ij
L2  for each step of length h until time T do
L3      for each robot i, in parallel, do
L4          u_i ← 0
L5          for each neighbor j ∈ N_i do
L6              z ← p_i - p_j                  ▷ relative position, sensed by robot i
L7              e ← ‖z‖² - d_ij²               ▷ squared distance error of the edge
L8              u_i ← u_i - e z
L9      move every robot with ṗ_i = u_i for time h
L10 return p
```

Lines L4 to L8 compute $u = -\nabla V = -R(p)^T e(p)$. Krick, Broucke and Francis use $\frac12 \lVert e \rVert^2$ as the potential, which is $2V$; this only rescales time. Line L9 stands for the motion of the robots. The implementation integrates it with the classic fourth order Runge-Kutta method and a fixed step $h$, and it has a function that computes the rank of $R$ to test infinitesimal rigidity.

## Example

**One evaluation by hand.** Three robots stand at $p_1 = (0, 0)$, $p_2 = (1.2, 0.1)$ and $p_3 = (0.4, 0.8)$, with the triangle graph and all target distances 1 m. The squared errors are $e_{12} = 1.45 - 1 = 0.45$, $e_{23} = 1.13 - 1 = 0.13$ and $e_{13} = 0.8 - 1 = -0.2$, so $V = (0.2025 + 0.0169 + 0.04)/4 = 0.06485$. Robot 1 gets

$$u_1 = -0.45 (p_1 - p_2) + 0.2 (p_1 - p_3) = (0.54, 0.045) + (-0.08, -0.16) = (0.46, -0.115),$$

which moves it toward robot 2, whose edge is too long, and away from robot 3, whose edge is too short. The three inputs are $(0.46, -0.115)$, $(-0.644, 0.046)$ and $(0.184, 0.069)$, and they sum to zero, so the centroid does not move.

**The run.** With RK4 and $h = 0.005$ s:

| $t$ (s) | $V$ | $\lVert p_1 - p_2 \rVert$ | $\lVert p_2 - p_3 \rVert$ | $\lVert p_1 - p_3 \rVert$ |
|---|---|---|---|---|
| 0 | 0.06485 | 1.2042 | 1.0630 | 0.8944 |
| 0.5 | 0.0021619 | 1.0307 | 0.9989 | 0.9649 |
| 1 | 0.00010922 | 1.0070 | 0.9998 | 0.9923 |
| 2 | 2.7069e-7 | 1.0004 | 1.0000 | 0.9996 |
| 4 | 1.6632e-12 | 1.0000 | 1.0000 | 1.0000 |

The robots end at $(0.0853, -0.0641)$, $(1.0727, 0.0940)$ and $(0.4420, 0.8701)$, a unit equilateral triangle that is turned with respect to the axes and has the start centroid $(0.5333, 0.3)$. Between $t = 2$ and $t = 4$, $V$ drops by a factor of about $1.6 \times 10^5$, close to $e^{-12}$. This matches the linearization: at the unit equilateral triangle the matrix $2 R R^T$ has the eigenvalues 6, 3 and 3, so the slowest error mode decays as $e^{-3t}$ and $V$ as $e^{-6t}$.

**A wrong equilibrium.** From the collinear start $(0, 0)$, $(1, 0)$, $(3, 0)$ the robots stay on the line, as the proof shows. They stop at $(0.8294, 0)$, $(1.2073, 0)$ and $(1.9633, 0)$, with distances 0.3780, 0.7559 and 1.1339 and $V = 0.25$. Here $\nabla V = 0$, but the shape is wrong.

**A flexible graph.** With only the four sides of a square, all of length 1, the framework is not rigid: $R$ has rank 4, less than $2 \cdot 4 - 3 = 5$. From $(0, 0)$, $(1.1, 0)$, $(1.5, 0.9)$, $(0.3, 1)$ all four sides reach length 1, but the robots stop in a rhombus with diagonals 1.6168 and 1.1772 instead of $\sqrt 2 = 1.4142$. Adding one diagonal with target $\sqrt 2$ gives rank 5, and then starts near the square converge to the square.

## Correctness

The [proof](proofs/correctness/) shows that the law is the gradient flow $\dot p = -\nabla V$, so $\dot V = -\lVert \nabla V \rVert^2 \le 0$. The inputs sum to zero, so the centroid is fixed, and the law commutes with rotations and translations. With a connected graph the trajectories stay bounded, and by the [LaSalle invariance principle](/lasalle-invariance-principle/) they approach the set of equilibria. The collinear set is invariant, which gives wrong equilibria. The main step is a local gradient inequality $\lVert \nabla V \rVert^2 \ge c V$ near an infinitesimally rigid target, proved from the rank of $R$ and the [Asimow-Roth theorem](/asimow-roth-theorem/). It gives $V(t) \le V(0) e^{-c t}$ and a finite path length, so starts close to the target converge to a congruent copy of it.

## Complexity

- **Per step.** Robot $i$ does $O(|N_i|)$ work in lines L4 to L8, so one evaluation of all inputs costs $O(r + m)$ in the [real RAM](/real-ram/) model, and an RK4 step costs four evaluations. No messages are sent: each robot senses the relative positions $z_{ij}$.
- **Rate, proved locally.** Near an infinitesimally rigid target, $V$ decays exponentially. The rate $c$ depends on the smallest positive singular value of $R$ at the target, so a nearly flexible target, where $R$ is close to losing rank, converges slowly.
- **Global behavior.** There is no bound on the time from an arbitrary start, and some starts do not reach the target at all.

## Properties

- **Needs only relative positions in local frames.** The law commutes with rotations, so each robot can use its own orientation.
- **Gradient system.** $V$ never increases, and the centroid never moves.
- **Local convergence.** It is proved for infinitesimally rigid targets in the plane by Krick, Broucke and Francis, and by the proof on this site.
- **Not global.** Other equilibria exist, among them configurations on a line for the triangle.
- **Shape up to congruence.** The final formation can be any translated and turned copy of the target, or its mirror image. A target that is rigid but not [globally rigid](/global-rigidity/) also has other realizations with the same edge lengths that are not congruent to it, and a start far from the target can end in one of them.
- **Deterministic and distributed.** Each robot uses only its own edges.

## Variants and improvements

- **Other potentials.** Any potential $\sum \gamma(\lVert z_{ij} \rVert^2 - d_{ij}^2)$ with $\gamma \ge 0$, $\gamma(0) = 0$ and $\gamma'(0) = 0$ gives a law with the same structure. The square of the error is the most common choice. Oh, Park and Ahn (2015) list the forms used in the literature.
- **Triangle and global results.** For three robots, Dörfler and Francis (2010) show that every start that is not collinear converges to the target triangle.
- **Unicycles.** Feedback linearization of a point at a small distance ahead of the axle turns a [unicycle](/unicycle-model/) into a single integrator, and the law applies to that point.
- **Bearing and displacement laws.** If the robots share a compass, displacement-based control with the Laplacian converges globally. Bearing-based laws use directions instead of distances.
- **Moving formations.** Adding a common velocity to every $u_i$ moves the whole formation while the gradient term holds the shape.

## When to use it

Use the distance law when the robots can measure the relative positions of their neighbors, as with cameras or range sensors, but do not share a compass or a global frame, and when they start close to the target shape. Pick the sensing graph from rigidity theory: a minimally rigid graph built by a [Henneberg construction](/henneberg-construction/) has $2r - 3$ edges in the plane and is generically infinitesimally rigid. Use displacement-based consensus when the robots share an orientation, and leader-follower control when a tree of pairs is enough.

## Pitfalls

- **Rigidity is required.** A graph that is not rigid, like the four sides of a square, reaches the right edge lengths in a wrong shape. Check the rank of $R$ at the target, not only the edge count.
- **Non-generic targets.** A target that has the right graph but a special position, such as three robots on a line, is not infinitesimally rigid, and the local theorem does not apply.
- **Wrong equilibria.** A start on a line, or near some other wrong equilibrium, can stop at a wrong shape. Start near the target or use a law with a global result for the case at hand.
- **Mirror images.** Distances do not fix the handedness of a shape. From a start far from the target, the robots can converge to its mirror image.
- **Inconsistent distances.** If the targets are not realizable, $V$ cannot reach 0, and the robots stop at a compromise. Some robots can also drift if the measured distances are biased.

## Implementations

## History

Krick, Broucke and Francis (2009) gave the local stability theorem for infinitesimally rigid targets, with a center manifold argument and a link to the rigidity theory of frameworks. Dörfler and Francis (2010) analyzed the triangle in detail and its wrong equilibria. The survey of Oh, Park and Ahn (2015) classifies formation control into position-based, displacement-based and distance-based methods by what the robots sense and control.

## References
