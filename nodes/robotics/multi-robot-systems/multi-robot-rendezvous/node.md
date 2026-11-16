---
tag: FR36DY
kind: problem
slug: multi-robot-rendezvous
name: Multi-robot rendezvous
aliases:
- gathering problem
area: robotics/multi-robot-systems
level: core
summary: Make all robots meet at one point that is not given in advance, using only local sensing or communication.
prereqs: [multi-robot-system, graph]
see_also: [ando-circumcenter-algorithm, laplacian-consensus-protocol, connectivity-maintenance, formation-control, distributed-averaging, minimum-enclosing-circle, synchronous-model, consensus-problem]
sources:
  - paper: doi:10.1109/70.795787
    title: Hideki Ando, Yoshinobu Oasa, Ichiro Suzuki and Masafumi Yamashita, Distributed memoryless point convergence algorithm for mobile robots with limited visibility, IEEE Transactions on Robotics and Automation 15(5), 1999
    locator: pages 818 to 828 (point convergence for oblivious robots with limited visibility)
  - paper: doi:10.1137/040620552
    title: Jie Lin, A. Stephen Morse and Brian D. O. Anderson, The multi-agent rendezvous problem, Part 1, The synchronous case, SIAM Journal on Control and Optimization 46(6), 2007
    locator: pages 2096 to 2119
  - paper: doi:10.1137/040620564
    title: Jie Lin, A. Stephen Morse and Brian D. O. Anderson, The multi-agent rendezvous problem, Part 2, The asynchronous case, SIAM Journal on Control and Optimization 46(6), 2007
    locator: pages 2120 to 2147
  - paper: doi:10.1109/TAC.2006.878713
    title: Jorge Cortes, Sonia Martinez and Francesco Bullo, Robust rendezvous for mobile autonomous agents via proximity graphs in arbitrary dimensions, IEEE Transactions on Automatic Control 51(8), 2006
    locator: pages 1289 to 1298
  - paper: doi:10.1109/TAC.2007.908304
    title: Sonia Martinez, Francesco Bullo, Jorge Cortes and Emilio Frazzoli, On synchronous robotic networks, Part II, Time complexity of rendezvous and deployment algorithms, IEEE Transactions on Automatic Control 52(12), 2007
    locator: pages 2214 to 2226
  - book: isbn:9780691141954
    title: Francesco Bullo, Jorge Cortes and Sonia Martinez, Distributed Control of Robotic Networks, Princeton University Press, 2009
    locator: Chapter 4, Connectivity maintenance and rendezvous
---

Multi-robot rendezvous is the problem of bringing $r$ robots to one common point when no robot knows the point in advance and each robot senses or hears only some of the others. The point is not given; it comes out of the interaction, so the robots must agree on it while they move. When the interaction graph is fixed and connected, the [Laplacian consensus protocol](/laplacian-consensus-protocol/) on the positions solves it. When the graph comes from distances, as for robots with a limited sensing range, the motion itself can break the links and split the group, and the problem is to meet and keep the group connected at the same time.

## In plain words

Some robots are spread over a field, and they must all come to the same spot. Nobody tells them where. Each robot sees only the robots near it.

If the robots simply move toward their neighbors, they come together, as long as the links between them stay. But a robot at the edge of the group can lose sight of its only neighbor when that neighbor is pulled the other way. Then the lone robot stops, and the group never meets.

Good methods let each robot move toward its neighbors but never so far that it loses one of them. Then the group stays in one piece and shrinks to a point.

## Definition

**Robots.** There are $r$ robots with positions $p_1, \dots, p_r \in \mathbb{R}^d$, usually $d = 2$, and simple dynamics $\dot p_i = u_i$, or $p_i(k+1) = p_i(k) + u_i(k)$ in rounds.

**Information.** Robot $i$ knows the relative positions $p_j - p_i$ of its neighbors $j \in N_i$. The neighbors are either given by a fixed graph, or by a radius $V$, with $N_i = \{ j : \lVert p_j - p_i \rVert \le V \}$, which changes as the robots move. Robots may have no identifiers, no common frame and no memory of past rounds.

**Goal.** Asymptotic rendezvous asks that there is a point $p^\ast$ with $p_i(t) \to p^\ast$ for every $i$. The $\varepsilon$-rendezvous version asks that all robots come within distance $\varepsilon$ of their mean, and exact rendezvous asks that all robots reach the same point in finite time and stay there. A solution must reach the goal from every start in a stated class, usually every start whose graph is connected.

## Variants

- **Fixed graph or distance graph.** On a fixed connected graph the problem is consensus on each coordinate. On a distance graph a solution must also keep the graph connected, which is [connectivity maintenance](/connectivity-maintenance/).
- **Timing.** All robots act in common rounds in the [synchronous model](/synchronous-model/); in the semi-synchronous model a subset acts in each round; in the [asynchronous model](/asynchronous-model/) robots can act on old observations. Lin, Morse and Anderson (2007) treat the synchronous and the asynchronous case in two papers.
- **Gathering.** In distributed computing, the gathering problem asks oblivious robots, which work in look, compute and move cycles, to meet at one point in finite time. This is a stronger goal than convergence, and the answers depend strongly on the timing model, on the visibility and on what the robots share.
- **Meeting point.** Some tasks fix the meeting point by the start, such as the average of the start positions; consensus on a balanced graph reaches the average, while circumcenter methods reach a point that depends on the shape of the group.
- **Robot dynamics.** Robots with nonholonomic constraints, such as unicycles, need laws that also handle the heading.
- **Two robots.** Rendezvous of two agents on a graph or a line, who search for each other, is a different problem in search theory.

## Examples

**Fixed graph.** Three robots on a line at $0$, $3$ and $6$ with the fixed path graph $1 - 2 - 3$ and the protocol $\dot p = -L p$ meet at the average $3$, with the gap shrinking as $e^{-t}$; see the [Laplacian consensus protocol](/laplacian-consensus-protocol/).

**Distance graph, consensus breaks the group.** Let $V = 1$ and five robots on a line at $0$, $1$, $1.9$, $1.9$ and $1.9$. The robot at $0$ sees only the robot at $1$, and the robot at $1$ sees all others. One round of the sampled consensus step $p_i \leftarrow p_i + 0.2 \sum_{j \in N_i} (p_j - p_i)$ moves the robot at $1$ by $0.2 (-1 + 3 \cdot 0.9) = 0.34$ to $1.34$, because three neighbors pull it right and only one pulls it left. The robot at $0$ moves to $0.2$. Now they are $1.14$ apart, the link is lost, and the robot at $0.2$ sees nobody and never moves again. The other four see each other, so they meet at their average $(1.34 + 3 \cdot 1.72) / 4 = 1.625$.

**Distance graph, circumcenter step keeps it.** With [Ando's circumcenter algorithm](/ando-circumcenter-algorithm/) and the same start, the robots move to $0.5$, $0.95$ and three times $1.45$, the centers of the smallest intervals around the robots they see. No link is lost, every robot now sees every other robot, and in the next round all five meet at $0.975$.

## Known algorithms

- [Laplacian consensus protocol](/laplacian-consensus-protocol/): each robot moves toward its neighbors; solves rendezvous on a fixed connected graph, or on a changing graph that stays connected often enough, and meets at the average on balanced graphs.
- [Ando's circumcenter algorithm](/ando-circumcenter-algorithm/): each robot moves toward the center of the smallest enclosing circle of the robots it sees, inside disks that keep every link; solves rendezvous for oblivious robots with limited visibility.
- Circumcenter laws in any dimension and with other proximity graphs (Cortés, Martínez and Bullo 2006).
- Consensus with weights that grow without bound as a link nears the sensing radius, which keeps the links; see [connectivity maintenance](/connectivity-maintenance/).

## Bounds

- **Rate on a fixed graph.** The consensus protocol shrinks the distance to the meeting point at the rate $e^{-\lambda_2 t}$, where $\lambda_2$ is the second smallest eigenvalue of the Laplacian; on a path of $r$ robots this is about $\pi^2 / r^2$.
- **Rounds of the circumcenter algorithm.** On a line, the synchronous circumcenter algorithm needs $\Theta(r)$ rounds (Martínez, Bullo, Cortés and Frazzoli 2007).
- **Contraction.** Every law that moves each robot into the convex hull of the robots it sees, including the two above, never increases the diameter of the group; this is a common first step of the proofs.
- **Connectivity is needed.** Robots in two groups that see nothing of each other can never meet, because no law can use information the robots do not have.

## Reductions

- **To consensus.** On a fixed graph, rendezvous in $\mathbb{R}^d$ is $d$ copies of the agreement problem of [distributed averaging](/distributed-averaging/), one per coordinate.
- **From formation control.** Displacement-based [formation control](/formation-control/) with target offsets $c_i$ is rendezvous for the shifted positions $p_i - c_i$, so rendezvous is the formation with all offsets zero.
- **Not the fault-tolerant consensus.** The [consensus problem](/consensus-problem/) of distributed computing asks processes to decide on one value in finite time while some of them fail. Rendezvous assumes no faults and usually reaches agreement only in the limit.

## Applications

Rendezvous is used to gather robots after a mission, to bring robots together before a formation starts, to meet for recharging or for the exchange of data, and as a step in other tasks, where robots must first agree on a common reference point. It is also the simplest test case for laws that must keep a sensing graph connected.

## References
