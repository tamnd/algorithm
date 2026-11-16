---
tag: 5MESC6
kind: problem
slug: connectivity-maintenance
name: Connectivity maintenance
aliases:
- connectivity preservation
area: robotics/multi-robot-systems
level: research
summary: Control a team of robots so that its communication graph, which depends on the positions, stays connected while the team does its task.
prereqs: [multi-robot-system, laplacian-matrix]
see_also: [multi-robot-rendezvous, ando-circumcenter-algorithm, laplacian-consensus-protocol, matrix-tree-theorem, courant-fischer-theorem, semidefinite-programming, control-barrier-function, random-geometric-graph]
sources:
  - paper: doi:10.1109/TRO.2007.900642
    title: Michael M. Zavlanos and George J. Pappas, Potential fields for maintaining connectivity of mobile networks, IEEE Transactions on Robotics 23(4), 2007
    locator: pages 812 to 816 (a potential on the determinant of the projected Laplacian, centralized)
  - paper: doi:10.1109/TRO.2007.900638
    title: Meng Ji and Magnus Egerstedt, Distributed coordination control of multiagent systems while preserving connectedness, IEEE Transactions on Robotics 23(4), 2007
    locator: pages 693 to 703 (edge tension potentials that keep the links, with hysteresis in the graph)
  - paper: "Michael M. Zavlanos and George J. Pappas, Distributed connectivity control of mobile networks, IEEE Transactions on Robotics 24(6), 2008"
    locator: pages 1416 to 1428 (distributed control that lets links be added and removed)
  - paper: doi:10.1109/JPROC.2011.2157884
    title: Michael M. Zavlanos, Magnus B. Egerstedt and George J. Pappas, Graph-theoretic connectivity control of mobile robot networks, Proceedings of the IEEE 99(9), 2011
    locator: pages 1525 to 1540 (survey of local and global methods)
  - book: isbn:9780691141954
    title: Francesco Bullo, Jorge Cortes and Sonia Martinez, Distributed Control of Robotic Networks, Princeton University Press, 2009
    locator: Chapter 4, Connectivity maintenance and rendezvous
---

Connectivity maintenance is the problem of moving a team of robots while its communication graph stays connected. Two robots can talk when they are within a range $\rho$, so the graph $G(p)$ changes with the positions $p$, and a law that is good for the task, such as moving toward a goal or spreading out, can break the links and cut the team into parts that cannot coordinate again. A solution adds a constraint or a correcting term to the task law so that the graph stays connected for all time. Local methods keep every link that exists at the start; global methods allow links to break as long as the graph as a whole stays connected, usually measured by the second smallest eigenvalue $\lambda_2$ of the [Laplacian matrix](/laplacian-matrix/).

## In plain words

Robots in a team pass messages to each other, but each radio reaches only so far. If two robots drive too far apart, their link drops. If too many links drop, the team splits into groups that cannot hear each other, and the groups cannot work together any more.

There are two ways to prevent this. The simple way is that no robot ever lets go of a partner it starts with. This is safe but strict, because the team can never change its shape much.

The flexible way is that a link may drop as long as every robot can still reach every other robot through some chain of links. That needs a measure of how well the whole team is joined, and robots must keep this measure above zero.

## Definition

**Robots and graph.** There are $r$ robots with positions $p_1, \dots, p_r$ and dynamics $\dot p_i = u_i$. The graph $G(p)$ has an edge $\{i, j\}$ when $\lVert p_i - p_j \rVert \le \rho$. A weighted version uses weights $w_{ij} = f(\lVert p_i - p_j \rVert)$ with a smooth function $f$ that is positive below $\rho$ and zero from $\rho$ on, and the weighted Laplacian $L(p)$.

**Task.** A task law $u_i^{\text{task}}$, such as a step toward a goal, a coverage law or a formation law.

**Goal.** Given that $G(p(0))$ is connected, find inputs $u_i$, close to the task law and computed from local information when possible, such that $G(p(t))$ is connected for all $t \ge 0$.

**The algebraic test.** A graph is connected if and only if $\lambda_2(L) > 0$. Let $P$ be an $r \times (r - 1)$ matrix whose columns are orthonormal and orthogonal to $\mathbf 1$. Then $P^T L P$ has the eigenvalues $\lambda_2, \dots, \lambda_r$, so the graph is connected if and only if $\det(P^T L P) > 0$. By the [matrix-tree theorem](/matrix-tree-theorem/) this determinant is $r$ times the weighted number of spanning trees.

## Variants

- **Local, edge preserving.** Keep every initial link: $\lVert p_i(t) - p_j(t) \rVert \le \rho$ for all initial edges. Each robot needs only its neighbors, but the team keeps a fixed tree of constraints. Edges may be added and then kept, as in the hysteresis of Ji and Egerstedt (2007).
- **Global, algebraic.** Keep $\lambda_2(L(p)) > 0$ or $\det(P^T L P) > 0$, and allow links to break. Zavlanos and Pappas (2007) used a potential on the determinant, which needs the whole graph; their later work (2008) made such control distributed.
- **Robust connectivity.** Keep $\lambda_2 \ge \lambda_{\min} > 0$, or keep the graph $k$-connected, so that the team survives the loss of a robot or a link.
- **Intermittent connectivity.** The graph may be disconnected at times, as long as the robots meet often enough to share information.
- **Line of sight and real radios.** Obstacles and signal fading make the range depend on the place, and links are then modeled with probabilities or measured signal strength.

## Examples

**The weighted path of three robots.** Let robot 2 be linked to robot 1 with weight $a$ and to robot 3 with weight $b$. The Laplacian has eigenvalues $0$ and $(a + b) \pm \sqrt{a^2 - a b + b^2}$, so $\lambda_2 = a + b - \sqrt{a^2 - ab + b^2}$, and $\det(P^T L P) = \lambda_2 \lambda_3 = 3ab$, which is $r = 3$ times the weight $ab$ of the one spanning tree. With $a = 1$, the value $\lambda_2$ is $1$ for $b = 1$, $0.634$ for $b = 0.5$, $0.146$ for $b = 0.1$, and $0$ for $b = 0$. As robot 3 drifts toward the range limit and $b$ fades, $\lambda_2$ falls smoothly to zero, which gives a global method a warning before the link is lost.

**A task law that cuts the team.** Five robots with $\rho = 1$ stand on a line at $0$, $1$, $1.9$, $1.9$ and $1.9$. One step of the consensus law $p_i \leftarrow p_i + 0.2 \sum_{j \in N_i} (p_j - p_i)$ moves the robot at $1$ to $1.34$ and the robot at $0$ to $0.2$, so their link of length $1.14$ is lost and the robot at $0.2$ is cut off for good. [Ando's circumcenter algorithm](/ando-circumcenter-algorithm/), which moves each robot only within disks of radius $\rho / 2$ around the midpoints of its links, keeps all links, and the five robots meet; see [multi-robot rendezvous](/multi-robot-rendezvous/).

## Known algorithms

- **Constraint disks.** Each pair of linked robots stays in the disk of radius $\rho / 2$ around their midpoint, as in [Ando's circumcenter algorithm](/ando-circumcenter-algorithm/). This keeps every link in the synchronous and the semi-synchronous model.
- **Edge tension potentials.** Ji and Egerstedt (2007) add to the consensus law weights that grow without bound as a link approaches the range $\rho$, so that the gradient flow never lets a link reach the range.
- **Determinant potential.** Zavlanos and Pappas (2007) add the gradient of a potential that grows without bound as $\det(P^T L(p) P)$ goes to zero; this keeps the graph connected while links may change, but it needs global information.
- **Distributed link deletion.** Zavlanos and Pappas (2008) let robots decide together which links can be removed without breaking connectivity, and keep the others with local potentials.
- **Barrier functions and optimization.** A [control barrier function](/control-barrier-function/) on the length of each link, or on an estimate of $\lambda_2$, gives a [quadratic program](/quadratic-programming/) per step that changes the task input as little as possible.

## Bounds

- **Concavity of $\lambda_2$.** By the [Courant-Fischer theorem](/courant-fischer-theorem/), $\lambda_2(L) = \min \{ x^T L x : \lVert x \rVert = 1, \mathbf 1^T x = 0 \}$, a minimum of functions that are linear in $L$. So $\lambda_2$ is a concave function of $L$, and of the edge weights, since $L$ is linear in them. Maximizing $\lambda_2$ over weights in a convex set is a convex problem and can be written as a [semidefinite program](/semidefinite-programming/).
- **Cost of the test.** Checking that a graph is connected takes $O(r + m)$ time with [breadth-first search](/breadth-first-search/), while computing $\lambda_2$ of a dense Laplacian takes $O(r^3)$ time with a standard eigenvalue method. A robot that knows only its neighbors cannot decide alone whether the whole graph is connected; global methods must estimate $\lambda_2$ by distributed iterations.
- **Local is conservative.** Keeping every initial link is sufficient for connectivity but not necessary. It keeps a connected spanning subgraph fixed, which limits the shapes the team can take.

## Reductions

- **A constraint added to other problems.** [Rendezvous](/multi-robot-rendezvous/) with a distance graph, [formation control](/formation-control/) with limited sensing, [coverage control](/coverage-control/) and exploration all need connectivity maintenance as a side constraint.
- **Weighted connectivity and spanning trees.** The test $\det(P^T L P) > 0$ is a test for a spanning tree with positive weight, by the matrix-tree theorem.

## Applications

Connectivity maintenance is used in teams of ground and aerial robots that must report to a base or share a map, in mobile sensor networks, in convoys and swarms where robots relay messages for each other, and in search and exploration, where a chain of robots keeps a link back to the operator.

## References
