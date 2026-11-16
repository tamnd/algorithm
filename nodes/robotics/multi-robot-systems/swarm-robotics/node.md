---
tag: V6TYQS
kind: concept
slug: swarm-robotics
name: Swarm robotics
aliases:
- robot swarm
area: robotics/multi-robot-systems
level: core
summary: Many simple robots with local sensing and simple rules, whose useful group behavior comes from their interactions without central control.
prereqs: [multi-robot-system]
see_also: [boids, swarm-intelligence, ant-colony-optimization, particle-swarm-optimization, cellular-automaton, multi-robot-system, laplacian-consensus-protocol, coverage-control]
sources:
  - paper: doi:10.1007/978-3-540-30552-1_2
    title: Erol Sahin, Swarm robotics, from sources of inspiration to domains of application, in Swarm Robotics, Lecture Notes in Computer Science, Springer, 2005
    locator: pages 10 to 20 (the definition of swarm robotics and its criteria)
  - paper: doi:10.1007/s11721-012-0075-2
    title: Manuele Brambilla, Eliseo Ferrante, Mauro Birattari and Marco Dorigo, Swarm robotics, a review from the swarm engineering perspective, Swarm Intelligence 7(1), 2013
    locator: pages 1 to 41 (taxonomy of design and analysis methods and of collective behaviors)
  - paper: doi:10.1126/science.1254295
    title: Michael Rubenstein, Alejandro Cornejo and Radhika Nagpal, Programmable self-assembly in a thousand-robot swarm, Science 345(6198), 2014
    locator: pages 795 to 799 (a swarm of 1024 robots that form given two-dimensional shapes)
  - paper: doi:10.1145/37402.37406
    title: Craig W. Reynolds, Flocks, herds, and schools, a distributed behavioral model, Computer Graphics 21(4), Proceedings of SIGGRAPH 1987
    locator: pages 25 to 34 (flocking from local rules)
---

Swarm robotics is the study and design of large groups of simple robots that act without central control, each with local sensing, local communication and simple rules, so that a useful behavior of the whole group comes out of the many local interactions. It takes its ideas from social insects, flocks of birds and schools of fish, and it aims at three properties: robustness, because no robot is essential; scalability, because each robot deals only with its neighbors; and flexibility, because the same rules work in many settings. It is the robotic side of [swarm intelligence](/swarm-intelligence/), and the hard part is design: to find local rules for each robot that give a wanted behavior of the group, and to show that they do.

## In plain words

Think of ants. One ant is small and knows little. It follows a few simple habits, such as following a scent and leaving one where it walks. Yet the colony finds short paths to food, builds nests and moves house.

A robot swarm copies this idea. It uses many small, cheap robots. Each one sees only what is near it, talks only to its neighbors, and follows a few rules. Nobody is in charge.

If one robot breaks, the others go on. If more robots join, the rules stay the same. The difficult part is to choose the rules, because what one robot does is easy to see, but what the whole crowd does is hard to predict.

## The idea

**Criteria.** Şahin (2005) lists the features that set a swarm apart from other robot teams: many robots, few kinds of robots, robots that are simple or not efficient alone for the task, and robots with only local sensing and communication. A team of a few specialized robots under a central planner is a [multi-robot system](/multi-robot-system/), but not a swarm.

**Emergence from local rules.** Each robot runs the same controller, a map from what it senses nearby to what it does. The group behavior, such as a flock, a cluster or a shape, is not written in any one controller. It comes from many interactions, often with positive feedback, where a pattern attracts more robots to it, and negative feedback, which limits the growth.

**Kinds of interaction.** Robots interact directly, by sensing or messaging their neighbors, or indirectly through the environment, by changing it and reacting to the changes of others, as ants do with scent; this indirect form is called stigmergy.

**Design methods.** Brambilla et al. (2013) separate behavior-based design, where a person writes and tunes the rules by trial in simulation, from automatic design, where an evolutionary or learning method searches for the rules. Analysis uses simulation, models of the rates at which robots switch between behaviors, and, for the simplest rules, proofs from control theory, such as the convergence of the [Laplacian consensus protocol](/laplacian-consensus-protocol/).

**Limits.** A swarm is slow to give guarantees: local rules can split the group, stall, or fail in a new environment, and a behavior that works in simulation can fail on hardware. Swarms also trade speed for robustness, because no robot holds a global plan.

## Examples

- **Flocking.** The [boids](/boids/) rules of separation, alignment and cohesion give a flock that moves as one, without a leader.
- **Aggregation and rendezvous.** Robots gather in one place, for example by moving toward their neighbors; see [multi-robot rendezvous](/multi-robot-rendezvous/).
- **Dispersion and coverage.** Robots spread over an area to watch it, as in [coverage control](/coverage-control/).
- **Foraging and path formation.** Robots search for items and bring them home, and find short paths with signals left in the environment, the robotic form of the idea behind [ant colony optimization](/ant-colony-optimization/).
- **Self-assembly into shapes.** Rubenstein, Cornejo and Nagpal (2014) made 1024 small robots form given two-dimensional shapes, using only local communication, a few seed robots and the measured distances to neighbors.
- **Collective decisions.** Robots choose together between options, such as two sites, by local voting or by consensus.

## Where it is used

Swarm robotics is used mostly in research, with platforms of small robots in the laboratory, and it is studied for tasks where many cheap robots and robustness matter more than speed: environmental monitoring, search over large areas, agriculture, and the inspection of large structures. Its ideas also feed into optimization methods, such as [particle swarm optimization](/particle-swarm-optimization/), and into models of collective motion in biology and physics.

## References
