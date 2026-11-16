---
tag: 5WYD2H
kind: problem
slug: multi-robot-task-allocation
name: Multi-robot task allocation
aliases:
- MRTA
area: robotics/multi-robot-systems
level: core
summary: Assign tasks to robots to optimize the team utility, under Gerkey and Mataric's taxonomy of single or multi task and robot types.
prereqs: [multi-robot-system, assignment-problem]
see_also: [market-based-task-allocation, contract-net-protocol, consensus-based-bundle-algorithm, hungarian-algorithm, generalized-assignment-problem, unrelated-machine-scheduling, set-cover, vehicle-routing-problem]
sources:
  - paper: doi:10.1177/0278364904045564
    title: Brian P. Gerkey and Maja J. Mataric, A formal analysis and taxonomy of task allocation in multi-robot systems, International Journal of Robotics Research 23(9), 2004
    locator: pages 939 to 954 (the three axes ST or MT, SR or MR, IA or TA, and the link of each class to a known optimization problem)
  - paper: doi:10.1177/0278364913496484
    title: G. Ayorkor Korsah, Anthony Stentz and M. Bernardine Dias, A comprehensive taxonomy for multi-robot task allocation, International Journal of Robotics Research 32(12), 2013
    locator: pages 1495 to 1512 (the iTax taxonomy with the degree of interdependence of utilities)
  - paper: doi:10.1109/JPROC.2006.876939
    title: M. Bernardine Dias, Robert Zlot, Nidhi Kalra and Anthony Stentz, Market-based multirobot coordination, a survey and analysis, Proceedings of the IEEE 94(7), 2006
    locator: pages 1257 to 1270 (market methods for task allocation)
---

Multi-robot task allocation (MRTA) asks which robot should do which task, so that the team gets the most value or pays the least cost. Gerkey and Matarić (2004) sorted its forms along three axes, and the simplest form, one task per robot and one robot per task with no planning ahead, is the [assignment problem](/assignment-problem/). This page is the problem; [market-based task allocation](/market-based-task-allocation/), the [contract net protocol](/contract-net-protocol/) and the [consensus-based bundle algorithm](/consensus-based-bundle-algorithm/) are methods that solve it, usually without a central computer and without a guarantee of optimality.

## In plain words

A team of robots has a list of jobs: visit places, carry boxes, watch an area. Each robot is good at some jobs and bad at others, and each job takes some time or energy. Task allocation decides who does what.

If each robot does one job and each job needs one robot, the best answer can be found quickly. It gets hard when a robot must plan a whole list of jobs in order, when a job needs several robots at once, or when the value of one job depends on who does the others. Then teams use quick rules, such as auctions, that give a good answer but not always the best one.

## Definition

There are $r$ robots and $t$ tasks. For each robot $i$ and task $j$ (or each set of robots and set of tasks), a *utility* says how much the team gains, or a *cost* says how much it pays, in units such as seconds, meters or joules. An allocation gives tasks to robots under the rules of the class below, and the goal is to maximize the total utility, or to minimize the total cost.

Gerkey and Matarić (2004) use three axes:

- **ST or MT.** Single-task robots do one task at a time; multi-task robots can do several at once.
- **SR or MR.** Single-robot tasks need one robot; multi-robot tasks need a team.
- **IA or TA.** Instantaneous assignment uses only the tasks known now and plans nothing ahead; time-extended assignment also plans which tasks each robot does later, in a schedule.

**Basic case (ST-SR-IA).** Given an $r \times t$ utility matrix $U$, find a matching between robots and tasks that maximizes the sum of $U_{ij}$ over matched pairs.

When the robots must decide without a central computer, the problem also has a communication model: a graph that says which robots can talk, whether messages are synchronous or asynchronous, and how many messages or rounds a method may use. These are part of the method, not of the problem, and each method page states them.

## Variants

- **ST-SR-TA.** Each robot gets a schedule of tasks. Gerkey and Matarić relate it to scheduling on [unrelated machines](/unrelated-machine-scheduling/); with travel between task places it becomes a [vehicle routing problem](/vehicle-routing-problem/).
- **ST-MR-IA.** Tasks need teams of robots, so the problem is to split the robots into coalitions. Gerkey and Matarić relate it to set partitioning, a relative of [set cover](/set-cover/).
- **MT-SR and MT-MR.** Robots that can do several tasks at once lead to problems of the same kind with the roles of robots and tasks swapped.
- **Capacities.** If robot $i$ can take several tasks up to a budget, the IA case becomes the [generalized assignment problem](/generalized-assignment-problem/).
- **Interrelated utilities.** Korsah, Stentz and Dias (2013) add a fourth axis: no dependencies, dependencies within one robot's schedule, dependencies across schedules, and complex dependencies where the way a task is split into subtasks is also chosen.
- **Online.** Tasks appear over time, and the allocation must be made without knowing future tasks.

## Examples

**One task per robot.** Three robots and two tasks, with costs in seconds:

| | task 0 | task 1 |
|---|---|---|
| robot 0 | 1 | 2 |
| robot 1 | 10 | 3 |
| robot 2 | 1.5 | 2.5 |

There are 6 ways to give the two tasks to two different robots. The cheapest gives task 0 to robot 0 and task 1 to robot 2, total 3.5 s. A greedy auction that awards both tasks at once, as the [contract net protocol](/contract-net-protocol/) does with its full window, gives task 1 to robot 1 and pays 4 s.

**Bundles.** Three robots on a line of radio links, two tasks, each robot one task at most, and utilities $(10, 9)$, $(4, 6)$, $(8, 1)$. The best allocation is robot 0 to task 1 and robot 2 to task 0, value 17. The greedy allocation that the [consensus-based bundle algorithm](/consensus-based-bundle-algorithm/) reaches is robot 0 to task 0 and robot 1 to task 1, value 16.

**Teams.** Moving a heavy box needs two robots at once. Every task of this kind is a coalition choice, and choosing coalitions for many such tasks is the ST-MR-IA class.

## Known algorithms

- **[Hungarian algorithm](/hungarian-algorithm/).** Solves ST-SR-IA exactly in $O(n^3)$ time with $n = \max(r, t)$, on one computer that knows all utilities (theorem).
- **[Auction algorithm](/auction-algorithm/).** Bertsekas's price auction solves ST-SR-IA within $\varepsilon$ of the optimum per task, with bids that can be sent as messages.
- **[Contract net protocol](/contract-net-protocol/).** Managers announce tasks and award them to the best bid; greedy, fast, no cost bound.
- **[Market-based task allocation](/market-based-task-allocation/).** Single-item, sequential and combinatorial auctions, and trading between robots.
- **[Consensus-based bundle algorithm](/consensus-based-bundle-algorithm/).** Robots build bundles greedily and agree on winners over a connected graph; at least half of the optimum under diminishing marginal gain (theorem).
- **Integer programming and heuristics.** For the TA and MR classes, mixed integer programs, routing heuristics and coalition formation heuristics are used.

## Bounds

- **ST-SR-IA is polynomial (theorem).** It is a maximum weight bipartite matching, solved by the Hungarian algorithm.
- **Greedy for utilities (theorem).** Taking the largest remaining utility first gives at least half of the best total utility, since greedy is a $1/2$ approximation for [maximum weight matching](/maximum-weight-matching/).
- **Greedy for costs (theorem).** Taking the smallest remaining cost first has no constant factor bound: with costs $1, 2$ for robot 0 and $2, M$ for robot 1, greedy pays $1 + M$ while the best pays 4.
- **Harder classes.** The classes that Gerkey and Matarić relate to set partitioning, scheduling on unrelated machines and vehicle routing contain these problems, which are [NP-hard](/np-hard/), so no polynomial-time exact method is expected unless P = NP. Which of their classes are NP-hard in each exact form is stated in the paper; the locator here is general.

## Reductions

- ST-SR-IA is the [assignment problem](/assignment-problem/), and so a [maximum weight matching](/maximum-weight-matching/) in a bipartite graph.
- ST-SR-IA with budgets is the [generalized assignment problem](/generalized-assignment-problem/).
- ST-SR-TA with fixed task durations is a scheduling problem on [unrelated machines](/unrelated-machine-scheduling/).
- ST-MR-IA is a set partitioning problem over all coalitions of robots.
- The bundle score of CBBA with diminishing marginal gain is a [submodular function](/submodular-function/), and the rule "one robot per task" is a partition [matroid](/matroid/).

## Applications

Warehouse robots that pick shelves, delivery and inspection drones, search and rescue teams that split areas, planetary rovers that share science targets, and robot soccer teams that pick roles all solve task allocation, often many times per minute as tasks appear and robots finish.

## References
