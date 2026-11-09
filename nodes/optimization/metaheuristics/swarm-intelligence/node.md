---
tag: WEYMQ2
kind: concept
slug: swarm-intelligence
name: Swarm intelligence
aliases:
- swarm algorithms
- collective intelligence
area: optimization/metaheuristics
level: intro
summary: Collective problem solving by many simple agents with local rules and no central control. In optimization it names methods such as ant colony optimization and particle swarm optimization.
prereqs: [population-based-search]
see_also: [ant-colony-optimization, particle-swarm-optimization, artificial-bee-colony, evolutionary-computation, intensification-and-diversification, firefly-algorithm, bat-algorithm, cuckoo-search]
sources:
  - book: isbn:9780195131598
    title: Eric Bonabeau, Marco Dorigo and Guy Theraulaz, Swarm Intelligence, From Natural to Artificial Systems, Oxford University Press, 1999
    locator: Chapter 1 (self-organization, stigmergy and positive feedback) and Chapter 2 (foraging and the double bridge experiment)
  - book: isbn:9780262042192
    title: Marco Dorigo and Thomas Stützle, Ant Colony Optimization, MIT Press, 2004
    locator: Chapter 1, From real to artificial ants (the double bridge experiments and the choice model)
  - book: isbn:9781558605954
    title: James Kennedy, Russell C. Eberhart and Yuhui Shi, Swarm Intelligence, Morgan Kaufmann, 2001
    locator: Part 2 (the particle swarm and its social metaphor)
  - paper: S. Goss, S. Aron, J.-L. Deneubourg and J. M. Pasteels, Self-organized shortcuts in the Argentine ant, Naturwissenschaften 76, 1989
    title: Self-organized shortcuts in the Argentine ant
    locator: pages 579 to 581
  - paper: doi:10.1145/37402.37406
    title: Craig W. Reynolds, Flocks, herds and schools, a distributed behavioral model, Computer Graphics 21(4) (SIGGRAPH 1987)
    locator: pages 25 to 34 (the three steering rules of the boids)
  - paper: doi:10.1111/itor.12001
    title: Kenneth Sörensen, Metaheuristics, the metaphor exposed, International Transactions in Operational Research 22(1), 2015
    locator: pages 3 to 18
---

Swarm intelligence is the collective behavior of many simple agents that follow local rules, interact with each other or with their environment, and have no central control, yet together solve a problem that no single agent solves. The term comes from robotics (Beni and Wang, 1989). In optimization it names [population-based](/population-based-search/) methods modeled on such behavior, mainly [ant colony optimization](/ant-colony-optimization/), modeled on the foraging of ants, and [particle swarm optimization](/particle-swarm-optimization/), modeled on flocks. Many later methods use other animal metaphors. Several of them have been shown to reuse the operators of older methods under new names.

## In plain words

One ant is not smart, but a colony finds short paths between its nest and food. Each ant leaves a scent on its path and tends to follow paths with more scent. Ants on a short path come back sooner, so the short path gets scent faster, and more ants take it. No ant knows the map. The colony finds the path through many small local actions.

Optimization methods copy this style. Many simple agents each build or move a candidate solution. They share information, directly or through marks in a common memory. Good information grows stronger and old information fades. The best solution found by any agent is the answer.

## The idea

Bonabeau, Dorigo and Theraulaz describe four ingredients of self-organization in insect societies, which appear again in the algorithms.

- **Positive feedback.** A choice that worked is made more likely: more pheromone on a short path, or a stronger pull toward the best point found.
- **Negative feedback.** Some force stops the feedback from locking the system: pheromone evaporates, or particles keep a random part in their moves.
- **Randomness.** Agents choose at random, with probabilities set by the feedback, so they can find new options.
- **Many interactions.** The result comes from many agents and many local contacts, not from one agent.

**Stigmergy.** In ant colonies, agents interact through the environment: an ant changes the pheromone on a path, and other ants react to that change later. The biologist Grassé called this stigmergy. [Ant colony optimization](/ant-colony-optimization/) uses it directly: the ants write to a shared pheromone matrix, and the next ants read it.

**Direct sharing.** In a particle swarm, each particle knows the best point found by itself and by its neighbors, and moves toward them. The neighbor graph, called the topology, sets how fast information spreads. With a fully connected graph, all particles follow one global best, which spreads information fast but can cause a [premature convergence](/premature-convergence/). A ring spreads it slowly and keeps more diversity.

**The main methods.**

| method | agents | shared information | the new candidate |
|---|---|---|---|
| [ant colony optimization](/ant-colony-optimization/) | ants that build solutions step by step | pheromone on solution parts | a solution built at random with probabilities from pheromone and heuristic values |
| [particle swarm optimization](/particle-swarm-optimization/) | particles with a position and a velocity | personal and neighborhood best points | the old position plus a velocity pulled toward the best points |
| [artificial bee colony](/artificial-bee-colony/) | food sources and bees | the fitness of each source | a source moved along the difference to another source |

**The metaphor problem.** Since about 2005, many methods have been published under new animal metaphors, among them the [firefly algorithm](/firefly-algorithm/), [cuckoo search](/cuckoo-search/) and the [bat algorithm](/bat-algorithm/). Sörensen (2015) argued that a new metaphor often hides an operator that an existing method already has, and that methods should be described in the standard terms of optimization. Camacho-Villalón, Dorigo and Stützle analysed several of these methods and showed that the firefly and bat algorithms are forms of particle swarm optimization and that cuckoo search is a $(\mu + \lambda)$ [evolution strategy](/evolution-strategies/) with the recombination of [differential evolution](/differential-evolution/). The pages of these methods give the reductions.

## Examples

**The double bridge.** In the experiments of Deneubourg and coworkers, a nest and a food source are joined by two branches. In the model that fits these experiments, if $A_1$ and $A_2$ ants have already used branches 1 and 2, the next ant takes branch 1 with probability
$$P_1 = \frac{(k + A_1)^h}{(k + A_1)^h + (k + A_2)^h},$$
with fitted values about $k = 20$ and $h = 2$. With $A_1 = A_2 = 0$, $P_1 = 1/2$. With $A_1 = 30$ and $A_2 = 10$, $P_1 = 50^2/(50^2 + 30^2) = 2500/3400 \approx 0.735$. A small early lead grows, which is the positive feedback. If one branch is shorter, ants on it return first and add to its count first, so the lead usually goes to the short branch.

**Pheromone in ant colony optimization.** After each iteration, every pheromone value is multiplied by $1 - \rho$, the evaporation, and the edges of good tours get a deposit. With $\rho = 0.1$ and no deposit, a value of 1 drops to $0.9^{10} \approx 0.35$ after 10 iterations. So an edge that stops being used loses its weight, which is the negative feedback.

**One particle move.** A particle at $x = 0$ with velocity $v = 0$, personal best $p = 1$ and global best $g = 3$ in one dimension, with $c_1 = c_2 = 1.5$ and random factors $r_1 = 0.5$ and $r_2 = 0.2$, gets the velocity $0 + 1.5 \cdot 0.5 \cdot (1 - 0) + 1.5 \cdot 0.2 \cdot (3 - 0) = 0.75 + 0.9 = 1.65$ and moves to $x = 1.65$. It is pulled toward both best points.

## Where it is used

- In combinatorial optimization, with [ant colony optimization](/ant-colony-optimization/) for routing, the [traveling salesman problem](/traveling-salesman-problem/), the [quadratic assignment problem](/quadratic-assignment-problem/) and scheduling.
- In continuous black-box optimization and in the training of small models, with [particle swarm optimization](/particle-swarm-optimization/).
- In swarm robotics, where many simple robots coordinate by local rules, which is the field where the term started.
- In network routing, where ant-based methods such as AntNet spread routing information through the network.
- In computer graphics, where the boids of Reynolds (1987) simulate flocks with three local rules: separation, alignment and cohesion.

## References
