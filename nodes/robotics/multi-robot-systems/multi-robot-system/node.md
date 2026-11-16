---
tag: PXR4C7
kind: concept
slug: multi-robot-system
name: Multi-robot system
aliases:
- robot team
area: robotics/multi-robot-systems
level: intro
summary: A group of robots that share a task, with centralized, decentralized or distributed decisions over limited sensing and communication.
prereqs: [graph]
see_also: [swarm-robotics, formation-control, multi-robot-rendezvous, coverage-control, connectivity-maintenance, multi-robot-task-allocation, multi-agent-pathfinding, laplacian-consensus-protocol]
sources:
  - paper: doi:10.1023/A:1008855018923
    title: Y. Uny Cao, Alex S. Fukunaga and Andrew B. Kahng, Cooperative mobile robotics, antecedents and directions, Autonomous Robots 4(1), 1997
    locator: pages 7 to 27 (survey of group architectures, resource conflicts, origins of cooperation, learning, and geometric problems)
  - paper: doi:10.1177/0278364904045564
    title: Brian P. Gerkey and Maja J. Mataric, A formal analysis and taxonomy of task allocation in multi-robot systems, International Journal of Robotics Research 23(9), 2004
    locator: pages 939 to 954 (taxonomy of task allocation problems for robot teams)
  - book: isbn:9780691141954
    title: Francesco Bullo, Jorge Cortes and Sonia Martinez, Distributed Control of Robotic Networks, Princeton University Press, 2009
    locator: Chapter 3, Robotic network models and complexity notions
  - book: isbn:9780691140612
    title: Mehran Mesbahi and Magnus Egerstedt, Graph Theoretic Methods in Multiagent Networks, Princeton University Press, 2010
    locator: Chapter 3, The Agreement Protocol, Part I, and Chapter 6, Formation Control
---

A multi-robot system is a group of two or more robots that work on a common task, such as moving in a formation, covering an area, exploring a building or carrying an object. Each robot senses, decides and acts on its own body, and the robots share information by sensing each other or by messages over links of limited range. The main design question is where the decisions are made: in one central computer, in each robot with full information, or in each robot with only local information. The links between the robots form a [graph](/graph/), and many methods for robot teams are statements about this graph and how it changes as the robots move.

## In plain words

One robot can do a lot, but some jobs are too big, too spread out or too risky for one machine. A team of robots can watch a large field, search a building faster, or carry a heavy box together.

A team also brings new problems. The robots must not hit each other. They must decide who does what. They can usually talk only to robots that are close, and messages can be lost. Each robot sees only part of the world.

There are two main styles. In one style, a central computer collects everything and gives orders, which is simple but fragile. In the other style, each robot decides from what it sees and hears nearby, which keeps working when some robots fail.

## The idea

**Parts of the model.** A multi-robot system is described by four parts.

- **The robots.** Each robot $i$ has a state $x_i$, such as a position or a pose, and dynamics $\dot x_i = f_i(x_i, u_i)$, for example a single integrator $\dot p_i = u_i$ or a [unicycle](/unicycle-model/).
- **The interaction graph.** Robot $i$ can sense or hear robot $j$ when $(i, j)$ is an edge. The graph is often a disk graph, with an edge when $\lVert p_i - p_j \rVert \le R$, so it changes with the positions.
- **The control law.** Each robot computes $u_i$ from its own state and the information it gets over its edges.
- **The task.** A goal on the states of all robots, such as agreement, a shape, a cover of a region, or an assignment of jobs.

**Centralized, decentralized and distributed.** A centralized system has one planner that knows all states and computes all inputs. It can find good plans, as in [multi-agent pathfinding](/multi-agent-pathfinding/), but it needs reliable communication with every robot and fails with the planner. A decentralized system lets each robot decide, possibly with global information. A distributed law uses only information from neighbors in the graph, so the cost per robot does not grow with the size of the team. The [Laplacian consensus protocol](/laplacian-consensus-protocol/) is the basic distributed law: each robot moves its state toward its neighbors, and on a connected graph all states agree.

**Timing.** In the synchronous model all robots sense and act in common rounds. In asynchronous models robots act at their own times, on possibly old information. Proofs for one timing model need not hold for the other.

**Homogeneous and heterogeneous teams.** Teams of identical robots are easy to scale and to replace. Teams of robots with different sensors or bodies, such as ground and aerial robots, need [task allocation](/multi-robot-task-allocation/) to match jobs to robots.

**Swarms.** A [swarm](/swarm-robotics/) is a large team of simple, identical robots with local rules and no central control, where the group behavior comes from many local interactions.

## Examples

- **Rendezvous.** Robots that see only nearby robots must meet at one point; see [multi-robot rendezvous](/multi-robot-rendezvous/) and [Ando's circumcenter algorithm](/ando-circumcenter-algorithm/).
- **Formations.** Robots hold a shape while they move, from target offsets, distances or a leader; see [formation control](/formation-control/).
- **Coverage.** Robots spread over a region so that every point is near a robot; see [coverage control](/coverage-control/) and the [distributed Lloyd coverage algorithm](/cortes-coverage-algorithm/).
- **Connectivity.** Robots move while their communication graph stays connected; see [connectivity maintenance](/connectivity-maintenance/).
- **Task allocation.** Robots bid for jobs, as in the [auction algorithm](/auction-algorithm/), or a central solver uses the [Hungarian algorithm](/hungarian-algorithm/).
- **Path planning for many robots.** A planner finds paths without collisions for all robots at once; see [multi-agent pathfinding](/multi-agent-pathfinding/).
- **Mapping.** Robots build one map together; see [multi-robot SLAM](/multi-robot-slam/).
- **Flocks.** The [boids](/boids/) rules give group motion from three local rules.

## Where it is used

Multi-robot systems are used in warehouses, where many mobile robots move shelves under a central planner; in agriculture and environmental monitoring, where teams of ground, aerial or marine robots cover large areas; in search and rescue and in exploration, where teams map a building or a cave faster than one robot; in formations of aircraft, satellites and vehicles; and in research on swarms of small robots. The theory of distributed control for these systems links robotics with graph theory, with control, and with distributed computing.

## References
