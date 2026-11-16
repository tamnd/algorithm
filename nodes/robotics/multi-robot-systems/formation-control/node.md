---
tag: KRRR23
kind: problem
slug: formation-control
name: Formation control
aliases:
- formation keeping
area: robotics/multi-robot-systems
level: core
summary: Drive a group of robots to a desired geometric shape and keep it while the group moves, using only what each robot senses about its neighbors.
prereqs: [multi-robot-system, graph]
see_also: [distance-based-formation-control, leader-follower-formation-control, laplacian-consensus-protocol, rigidity-matrix, laman-theorem, multi-robot-rendezvous, connectivity-maintenance, boids]
sources:
  - paper: doi:10.1016/j.automatica.2014.10.022
    title: Kwang-Kyo Oh, Myoung-Chul Park and Hyo-Sung Ahn, A survey of multi-agent formation control, Automatica 53, 2015
    locator: pages 424 to 440 (the classification into position-based, displacement-based and distance-based control by sensed and controlled variables)
  - book: isbn:9780691140612
    title: Mehran Mesbahi and Magnus Egerstedt, Graph Theoretic Methods in Multiagent Networks, Princeton University Press, 2010
    locator: Chapter 6, Formation Control (Section 6.3 shape-based control and Section 6.4 relative state-based control)
  - paper: doi:10.1109/70.976023
    title: Jaydev P. Desai, James P. Ostrowski and Vijay Kumar, Modeling and control of formations of nonholonomic mobile robots, IEEE Transactions on Robotics and Automation 17(6), 2001
    locator: pages 905 to 908 (leader-follower control with separation and bearing, and with two separations)
  - paper: doi:10.1109/70.736776
    title: Tucker Balch and Ronald C. Arkin, Behavior-based formation control for multirobot teams, IEEE Transactions on Robotics and Automation 14(6), 1998
    locator: pages 926 to 939 (line, column, diamond and wedge formations kept by motor schemas)
  - paper: doi:10.1023/A:1008814708459
    title: M. Anthony Lewis and Kar-Han Tan, High precision formation control of mobile robots using virtual structures, Autonomous Robots 4(4), 1997
    locator: pages 387 to 403 (the virtual structure approach)
---

Formation control is the problem of moving a group of robots so that their positions form a given shape, and of keeping that shape while the group travels. The shape is given by target positions, by target offsets between neighbors, by target distances or by target bearings, and each kind needs different sensing. A robot usually sees only a few neighbors, so the problem is set on a sensing graph, and the question is which shapes a given graph and given measurements can hold, and with which control law.

## In plain words

A group of robots must fly or drive in a set pattern, such as a line, a V or a square. Nobody steers the group as a whole. Each robot sees only some of the others and must adjust its own motion so that, together, the pattern appears and stays.

What a robot can measure decides how hard this is. If every robot knows where it is on a map, each one just drives to its own spot. If robots share a compass but have no map, they can agree on spots relative to each other. If they have no compass at all and only know how far their neighbors are, they need enough of these distance links to lock the shape, like the bars of a stiff truss.

## Definition

**The model.** There are $r$ robots with positions $p_i \in \mathbb{R}^n$, usually $n = 2$, in meters. The basic model is the single integrator $\dot p_i = u_i$. Wheeled robots are often [unicycles](/unicycle-model/), with $\dot x = v \cos\theta$, $\dot y = v \sin\theta$ and $\dot\theta = \omega$. A fixed graph $G = (V, E)$ says which robots sense or talk to which; it can be directed, as in leader-follower control, or undirected.

**The target.** A target formation is a set $\mathcal{F}$ of configurations, given in one of these ways:

- *Position-based*: target points $p_i^*$ in a common frame, so $\mathcal{F} = \{p^*\}$.
- *Displacement-based*: target offsets $p_j^* - p_i^*$ on the edges, in a common orientation, so $\mathcal{F}$ is the set of translates of $p^*$.
- *Distance-based*: target distances $d_{ij}$ on the edges, so $\mathcal{F}$ is the set of configurations with $\lVert p_i - p_j \rVert = d_{ij}$ for every edge.
- *Bearing-based*: target unit directions on the edges.

**The question.** Find control laws $u_i$ that use only the measurements of robot $i$ about its neighbors, such that $p(t) \to \mathcal{F}$, ideally from every start, and such that $p(t)$ stays near $\mathcal{F}$ when the group moves as a whole. *Formation acquisition* is the convergence part, and *formation keeping* is the part that holds the shape during motion.

**What each kind needs.** Oh, Park and Ahn (2015) sort the methods by what the robots sense and what they control. Position-based control needs global positions. Displacement-based control needs relative positions and a common orientation, and a graph with a spanning tree. Distance-based control needs only relative positions in local frames, but the graph must make the target framework rigid.

## Variants

- **Leader-follower.** Each follower keeps a distance and a bearing, or two distances, to one or two leaders, and the graph is a directed tree or a directed acyclic graph. See [leader-follower formation control](/leader-follower-formation-control/).
- **Virtual structure.** The formation is a rigid body with its own pose. Each robot tracks its point on the body, and the body moves along a path (Lewis and Tan 1997).
- **Behavior-based.** Each robot mixes behaviors such as keep the formation, avoid obstacles and move to the goal, as in Balch and Arkin (1998). This works in practice but has no convergence proof.
- **Moving formations.** The whole shape follows a reference path or velocity, often given to a leader or to all robots.
- **Scale and orientation.** Some targets fix the shape up to scale, for example by bearings, and some fix it up to rotation, for example by distances.

## Examples

**Displacement-based by consensus.** Three robots in the plane share a compass. The target offsets come from the points $c_1 = (0, 0)$, $c_2 = (1, 0)$ and $c_3 = (0, 1)$ in meters, and the graph is the path 1 - 2 - 3. Each robot runs the [Laplacian consensus protocol](/laplacian-consensus-protocol/) on $q_i = p_i - c_i$. From $p_1 = (0, 0)$, $p_2 = (3, 1)$, $p_3 = (1, 4)$, the values $q_i$ are $(0, 0)$, $(2, 1)$ and $(1, 3)$, whose average is $(1, 4/3)$. On an undirected connected graph the average is invariant and the $q_i$ converge to it, so the robots end at $(1, 1.3333)$, $(2, 1.3333)$ and $(1, 2.3333)$: the target shape, shifted to keep the average of $q$.

**Distance-based needs rigidity.** Four robots must form a unit square using only distances. The four sides alone are not enough: a rhombus with unit sides satisfies them, and in the plane a rigid framework with 4 points needs at least $2 \cdot 4 - 3 = 5$ edges, by the counting condition of the [Laman theorem](/laman-theorem/). The four sides plus one diagonal of length $\sqrt 2$ m fix the square up to congruence. The [distance-based formation control](/distance-based-formation-control/) page shows a run where the four sides reach length 1 but the shape ends as a rhombus with diagonals 1.6168 m and 1.1772 m.

## Known algorithms

- [Laplacian consensus protocol](/laplacian-consensus-protocol/) on $p_i - c_i$: displacement-based, global convergence on a connected graph, needs a common orientation.
- [Distance-based formation control](/distance-based-formation-control/): gradient of the squared distance errors, local convergence for infinitesimally rigid targets.
- [Leader-follower formation control](/leader-follower-formation-control/): feedback linearization of the separation and bearing of each follower to its leader.
- Virtual structures (Lewis and Tan 1997) and behavior-based schemes (Balch and Arkin 1998), the latter as a heuristic.
- [Boids](/boids/) give loose flocks, not fixed shapes, and are not a formation controller.

## Bounds

- **Sensing graphs.** Displacement-based consensus needs at least $r - 1$ edges, a spanning tree. Distance-based control in the plane needs a rigid framework, which has at least $2r - 3$ edges; in space it needs at least $3r - 6$ edges for $r \ge 3$. These counts are necessary, and by the Laman theorem the planar count condition on all subgraphs is also sufficient for generic positions.
- **Convergence.** Displacement-based consensus converges from every start. The distance gradient law converges only locally in general, because it has equilibria with wrong shapes, such as collinear ones.
- **Rate.** For displacement-based consensus the error decays as $e^{-\lambda_2 t}$, with $\lambda_2$ the second smallest eigenvalue of the Laplacian.

## Reductions

- Displacement-based formation control reduces to consensus: with $q_i = p_i - c_i$, the target set is $\{q_1 = \dots = q_r\}$, so any agreement protocol solves it.
- A distance specification is a framework, and asking whether it can be realized at all is the [distance geometry problem](/distance-geometry-problem/). Whether it fixes the shape locally is a question of [infinitesimal rigidity](/infinitesimal-rigidity/), decided by the rank of the [rigidity matrix](/rigidity-matrix/), and whether it fixes the shape uniquely is a question of [global rigidity](/global-rigidity/).
- [Rendezvous](/multi-robot-rendezvous/) is the special case where all target offsets are zero.

## Applications

Formations are used for groups of mobile robots that carry a sensor array or a load together, for aerial vehicles that fly in a fixed pattern, for satellites that keep a fixed geometry for measurements, and for road vehicles that drive in a platoon at fixed gaps. In each case the choice between the variants depends on what the vehicles can measure: global positions, a common heading, or only the relative positions of their neighbors.

## References
