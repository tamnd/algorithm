---
tag: F7BSD0
kind: problem
slug: setup-planning
name: Setup planning
aliases:
- setup minimization
area: cad/manufacturing-process-planning
level: core
summary: Group the machining features of a part into setups, each a fixed orientation on the machine, so few setups are needed and tolerances between features hold.
prereqs: [accessibility-cone, set-cover]
see_also: [feature-recognition, fixture-planning, operation-sequencing, computer-aided-process-planning, greedy-set-cover, hitting-set, tolerance-stack-up, manufacturability-analysis]
sources:
  - paper: doi:10.1016/0278-6125(96)82335-1
    title: Sanjay E. Sarma and Paul K. Wright, Algorithms for the minimization of setups and tool changes in simply fixturable components in milling, Journal of Manufacturing Systems 15(2), 1996, 95 to 112
    locator: the graph model of the feasible plans of a part whose fixturing can be ignored, the choice of an access face for each feature, and the algorithms that minimize setups and then tool changes
  - paper: doi:10.1016/s0736-5845(98)00031-3
    title: Hong-Chao Zhang and Enhao Lin, A hybrid-graph approach for automated setup planning in CAPP, Robotics and Computer-Integrated Manufacturing 15(1), 1999, 89 to 100
    locator: the graph of features with the tolerance and datum relations between them, used to group features into setups
  - paper: doi:10.1080/0020754031000153351
    title: S. H. Huang and N. Xu, Automatic set-up planning for metal cutting, an integrated methodology, International Journal of Production Research 41(18), 2003, 4339 to 4356
    locator: setup planning that groups features by approach direction and by tolerance requirements, and selects the datum of each setup
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum, 1972, 85 to 103
    locator: the NP-completeness of set cover, the source problem of the reduction on this page
---

Setup planning groups the machining features of a part into setups. A setup is one way of holding the part on the machine: a fixed orientation, a fixture and a datum, with the part not moved until all its features are cut. Each setup costs time to load, align and fix the part, and each move of the part to a new setup adds a positioning error. So the aim is to use few setups, and to make features whose relative position has a tight tolerance in the same setup. A feature can be made in a setup only if the tool can reach it from the spindle direction of that setup. Setup planning differs from [fixture planning](/fixture-planning/) in scope: setup planning decides which features are made in which orientation, and fixture planning decides how the part is held in one of those setups. This page states the problem, shows that its combinatorial core is [set cover](/set-cover/), and so that it is NP-hard.

## In plain words

A three-axis milling machine cuts only from above. To cut a hole in the side of a block, the operator must stop, turn the block, clamp it again and find its position again. Each turn takes time, and each new clamping moves the part a little, so two features cut in different setups are less precisely placed relative to each other than two features cut in the same one.

So a planner asks, for each feature, from which sides a tool can reach it. A hole in the top face can be drilled only from above. A slot that runs across an edge can be cut from above or from the side. The planner picks as few sides as possible so that a tool reaches every feature, and keeps features that must line up closely in the same setup.

## Definition

There is no standard formal statement of setup planning. The following version captures the parts of it that the cited work shares: access, setup count and tolerance.

**Input.**
- A set $F = \{f_1, \dots, f_m\}$ of machining features, from [feature recognition](/feature-recognition/) on the part model.
- A finite set $S$ of candidate setups. For a three-axis machine, a setup is an orientation of the part, given by the direction $d_s$ of the tool relative to the part, often one of the six directions $\pm x, \pm y, \pm z$ of a prismatic part.
- For each feature $f$, the set $C(f) \subseteq S$ of setups in which a tool can reach and cut $f$. Geometrically, $s \in C(f)$ when $d_s$ is in the [accessibility cone](/accessibility-cone/) of $f$ and the tool and holder do not collide with the part.
- A set $T$ of tolerance relations: pairs $(f, g)$ with a tolerance $t_{fg}$ on their relative position, and a model of the error. In the simplest model, two features made in the same setup have a relative error of at most $e_1$, and two features made in different setups have a relative error of at most $e_2 > e_1$, where $e_2 - e_1$ is the error of moving the part.
- A precedence relation on $F$: $f \prec g$ when $f$ must be cut before $g$, for example because $f$ is the datum of $g$ or because $g$ is cut into a face that $f$ makes.

**Output.** An assignment $\sigma : F \to S$ and an order of the setups used, such that

1. $\sigma(f) \in C(f)$ for every feature $f$ (access);
2. $\sigma(f) = \sigma(g)$ for every $(f, g) \in T$ with $t_{fg} < e_2$ (tolerance);
3. if $f \prec g$ and $\sigma(f) \ne \sigma(g)$, then the setup $\sigma(f)$ comes before the setup $\sigma(g)$ (precedence).

**Objective.** Minimize the number $\lvert \sigma(F) \rvert$ of setups used.

A tight tolerance makes a hard constraint in this model. Other versions make it a cost: a penalty for each tolerance pair split across two setups, added to the setup count with a weight.

## Variants

- **Fixed directions.** Three-axis machining of prismatic parts with the six directions $\pm x, \pm y, \pm z$. Then $\lvert S \rvert = 6$.
- **Indexing tables and five-axis machines.** A rotary table or a five-axis head gives more tool directions per setup. Then a setup is a set of directions, and a feature can be made in a setup if its accessibility cone meets that set.
- **Simply fixturable parts.** Sarma and Wright (1996) study parts that a universal fixture can hold in any orientation, so fixturing does not limit the plan, and minimize the setups and then the tool changes.
- **Setups with datums.** Each setup also picks a datum, the faces that locate the part in the fixture, and a tolerance is measured from the datum. Zhang and Lin (1999) and Huang and Xu (2003) build a graph of the tolerance and datum relations between features and use it to group features.
- **Joint setup and fixture planning.** Each setup must also have a valid fixture, so a setup is feasible only if [fixture planning](/fixture-planning/) succeeds for it.
- **Weighted objective.** Minimize total time: setup time, plus tool change time, plus a penalty for split tolerance pairs. This joins setup planning with [operation sequencing](/operation-sequencing/).

## Examples

**Six features and three directions.** A block has six features. The candidate setups are $+z$ (tool from the top), $-z$ (tool from the bottom) and $+x$ (tool from one side).

| feature | description | $C(f)$ |
|---|---|---|
| $f_1, f_2$ | slots in the top face that run out through the $+x$ side | $\{+z, +x\}$ |
| $f_3$ | a blind hole in the top face | $\{+z\}$ |
| $f_4, f_5$ | slots in the bottom face that run out through the $+x$ side | $\{-z, +x\}$ |
| $f_6$ | a blind hole in the bottom face | $\{-z\}$ |

- *No tolerance relation.* The setups $\{+z, -z\}$ reach every feature, and one setup cannot, since $f_3$ needs $+z$ and $f_6$ needs $-z$. So the minimum is 2. The rule "pick the setup that reaches the most features first" picks $+x$, which reaches four features, and then still needs $+z$ for $f_3$ and $-z$ for $f_6$: 3 setups. This is the greedy rule of set cover, and the example shows that it is not optimal.
- *A tight tolerance.* Now the top slot $f_1$ and the bottom slot $f_4$ must line up within $t = 0.01$ mm, and assume that moving the part adds an error of $0.05$ mm, so $t < e_2$. Then $f_1$ and $f_4$ need one setup in $C(f_1) \cap C(f_4) = \{+x\}$. With $f_3$ in $+z$ and $f_6$ in $-z$, the minimum is now 3. The tolerance costs one setup.

The example has three candidate setups, so a check of all $2^3 - 1 = 7$ nonempty subsets finds both minima.

## Known algorithms

- **Search over subsets.** For $\lvert S \rvert = k$ candidate setups, try the subsets of $S$ in order of size and test each in $O(k m + \lvert T \rvert)$ time. This takes $O(2^k (k m + \lvert T \rvert))$ time, which is fast for the six directions of three-axis machining.
- **Greedy set cover.** Pick the setup that reaches the most unassigned features, and repeat. By the reduction below, this is [greedy set cover](/greedy-set-cover/), with its approximation guarantee. Many rule-based planners use this rule, with ties broken by datums and tolerances.
- **Graph methods.** Sarma and Wright (1996) model all feasible plans of a simply fixturable part as one graph and search it for plans with few setups and then few tool changes. Zhang and Lin (1999) group features with a graph of tolerance and datum relations.
- **Integer programming and metaheuristics.** A 0-1 variable for each pair of a feature and a setup, and one for each setup used, give an integer program. Later papers also use genetic algorithms and particle swarm methods for larger weighted versions.

There are no standard benchmarks for setup planning. Papers test their methods on example parts of their own, so their results cannot be compared from paper to paper.

## Bounds

**NP-hardness.** The decision version, "is there a plan with at most $k$ setups", is NP-complete when $S$ and the sets $C(f)$ are part of the input. It is in NP, since a plan is checked in polynomial time. For hardness, reduce from set cover, which is NP-complete (Karp 1972): map each element to a feature, each set to a setup, and let $C(f)$ be the sets that contain the element of $f$, with no tolerance or precedence relation. Then plans with $k$ setups are exactly set covers with $k$ sets.

The reduction keeps the objective value, so the approximation limits of [set cover](/set-cover/) carry over to this combinatorial version.

**What the reduction does not show.** The reduction needs arbitrary access sets $C(f)$. The cited sources do not show that every set system arises from the accessibility cones of the features of a real part on a given machine. With a constant number of candidate setups, such as six, the search over subsets is polynomial in $m$. So the hardness concerns machines and parts with many candidate setups.

## Reductions

- **From set cover.** As above. The reduction also works from [hitting set](/hitting-set/), which is the same problem with the roles of elements and sets swapped: choose setups (elements) that hit every set $C(f)$.
- **To set cover, with tolerances.** Join the features of each tight tolerance pair, and take the connected components of these pairs. A component $K$ must go to one setup, in $\bigcap_{f \in K} C(f)$. Replace each component by one feature with this access set. If some intersection is empty, there is no plan. Otherwise, with no precedence relation, a plan is a set cover of the components. Precedence adds a test that the chosen setups can be ordered with no cycle among the precedence pairs that cross setups.

## Applications

- **Process planning.** Setup planning is one step of [computer-aided process planning](/computer-aided-process-planning/), after the processes are chosen and before the operations are ordered and the fixtures are designed.
- **Design feedback.** The minimum number of setups is a measure of [manufacturability](/manufacturability-analysis/): a feature that forces an extra setup is a candidate for a change in the design.
- **Tolerance analysis.** The assignment of features to setups decides which tolerances depend on the error of moving the part, so it feeds the [tolerance stack-up](/tolerance-stack-up/) of the plan.

## References
