---
tag: QE5Z2N
kind: model
slug: load-balancing-game
name: Load balancing game
aliases:
- KP model
- Koutsoupias-Papadimitriou model
- selfish load balancing
area: algorithmic-game-theory/inefficiency-of-equilibria
level: core
summary: "Selfish jobs choose machines to minimize their own load, and the social cost is the makespan. It is the first model of the price of anarchy."
prereqs: [normal-form-game, mixed-strategy, pure-nash-equilibrium, makespan]
see_also: [price-of-anarchy-of-load-balancing, atomic-congestion-game, list-scheduling, makespan-minimization, selfish-routing-model, price-of-stability, truthful-scheduling-unrelated-machines, balls-into-bins]
sources:
  - paper: doi:10.1007/3-540-49116-3_38
    title: "Elias Koutsoupias and Christos Papadimitriou, Worst-case equilibria, STACS 1999, Lecture Notes in Computer Science 1563, 404-413"
    locator: "the model of selfish traffic on parallel links, the coordination ratio of the expected makespan, and the bound 3/2 for two identical links"
  - book: isbn:9780521872829
    title: "Noam Nisan, Tim Roughgarden, Eva Tardos and Vijay V. Vazirani (eds.), Algorithmic Game Theory, Cambridge University Press, 2007"
    locator: "Chapter 20, Berthold Vocking, Selfish load balancing (the model, the existence of pure equilibria, and the price of anarchy bounds)"
  - paper: "Dimitris Fotakis, Spyros Kontogiannis, Elias Koutsoupias, Marios Mavronicolas and Paul Spirakis, The structure and complexity of Nash equilibria for a selfish routing game, ICALP 2002; Theoretical Computer Science 410(36) (2009)"
    locator: "a greedy algorithm that computes a pure equilibrium on related links, and the hardness of computing the best and the worst pure equilibrium"
  - paper: "Eyal Even-Dar, Alex Kesselman and Yishay Mansour, Convergence time to Nash equilibria, ICALP 2003"
    locator: the number of steps of best and better response dynamics in load balancing games
  - paper: doi:10.1145/1186810.1186814
    title: "Artur Czumaj and Berthold Vocking, Tight bounds for worst-case equilibria, ACM Transactions on Algorithms 3(1) (2007), Article 4; SODA 2002"
    locator: the tight bounds on the price of anarchy for identical and related machines
---

The load balancing game is the model in which Koutsoupias and Papadimitriou first measured the [price of anarchy](/price-of-anarchy/), in 1999. Jobs are players, each job chooses a machine, and each job wants its machine to finish early. The social cost is the makespan, the finishing time of the busiest machine. This page defines the model and lists what is known about its equilibria; the page [price of anarchy of load balancing](/price-of-anarchy-of-load-balancing/) states and proves the bounds on how bad the equilibria can be.

Throughout, $m$ is the number of machines and $n$ is the number of jobs, which are the players. This is a cost game: each job minimizes its cost.

## The machine

**Machines and jobs.** There are $m$ machines $1, \dots, m$ and $n$ jobs $1, \dots, n$. Four machine environments are studied, the same as in scheduling ([machine environments](/machine-environments/)):

| environment | data | time of job $j$ on machine $i$ |
|---|---|---|
| identical | weights $w_j > 0$ | $w_j$ |
| related | weights $w_j$, speeds $v_i > 0$ | $w_j / v_i$ |
| restricted assignment | weights $w_j$, allowed sets $M_j$ | $w_j$ if $i \in M_j$, else not allowed |
| unrelated | times $p_{ij} > 0$ | $p_{ij}$ |

**Pure strategies.** Job $j$ chooses one machine $a_j$. A profile $a = (a_1, \dots, a_n)$ is a schedule. The load of machine $i$ is $L_i(a) = \sum_{j : a_j = i} p_{ij}$, with $p_{ij} = w_j / v_i$ for related machines and $p_{ij} = w_j$ for identical ones. The cost of job $j$ is the load of its machine, $c_j(a) = L_{a_j}(a)$: all jobs on a machine finish together, at the end. A pure Nash equilibrium is a schedule in which no job can move to a machine whose load, with the job added, is smaller:

$$L_{a_j}(a) \le L_k(a) + p_{kj} \quad \text{for every job } j \text{ and every machine } k \ne a_j.$$

**Mixed strategies.** Job $j$ chooses machine $i$ with probability $q_j(i)$, independently of the other jobs. Its expected cost on machine $i$ is

$$c_j(i, q_{-j}) = p_{ij} + \sum_{k \ne j} q_k(i)\, p_{ik}.$$

A mixed profile is a Nash equilibrium if every machine with $q_j(i) > 0$ minimizes $c_j(i, q_{-j})$ over $i$. A mixed best response has its support inside the set of pure best responses, so it is enough to check the $m$ pure choices of each job.

**Social cost.** The social cost of a schedule is the makespan $\max_i L_i(a)$. For a mixed profile it is the expected makespan $\mathbb{E}[\max_i L_i]$, the expectation of a maximum, which is not the maximum of the expected loads.

## What it counts

The model measures the loss caused by selfish choice:

- the price of anarchy, the largest ratio of the makespan of an equilibrium to the optimal makespan, for pure or for mixed equilibria (Koutsoupias and Papadimitriou called it the coordination ratio);
- the [price of stability](/price-of-stability/), the same ratio for the best equilibrium;
- the time to compute a pure equilibrium, and the number of moves that selfish jobs make before they reach one.

The optimum is the optimum of [makespan minimization](/makespan-minimization/) on the same machines, which is [NP-hard](/np-hard/) even for 2 identical machines.

## Relation to other models

- **Congestion games.** A load balancing game is a weighted [atomic congestion game](/atomic-congestion-game/) in which each strategy is a single resource and the cost of a resource is its load. With unit weights it is a singleton congestion game with $c_i(x) = x/v_i$. But the social cost here is the maximum cost, not the sum, so the results for the sum, such as the bound $5/2$ of the [smoothness framework](/smoothness-framework/), do not apply.
- **Selfish routing.** Koutsoupias and Papadimitriou phrased the model as traffic on $m$ parallel links from a source to a sink. If the jobs are many and tiny, the model becomes the nonatomic [selfish routing model](/selfish-routing-model/) on parallel links with linear latencies $\ell_i(x) = x/v_i$. There every Wardrop equilibrium balances the loads, so its makespan is optimal; the loss in the atomic model comes from the size of the jobs.
- **Scheduling.** A pure equilibrium on identical machines is a schedule that no single move of one job improves for that job. Such schedules are local optima of [makespan minimization](/makespan-minimization/) for the move of one job. [List scheduling](/list-scheduling/) can end in a schedule that is not an equilibrium, but [longest processing time first](/longest-processing-time-first/) always ends in one (below).
- **Mechanism design.** In [truthful scheduling on unrelated machines](/truthful-scheduling-unrelated-machines/) the machines are the selfish agents and the jobs are assigned by a mechanism. Here the jobs are the agents.

## Known results in the model

Each item below is a theorem unless it says otherwise.

**Pure equilibria exist in all four environments.** Sort the loads of a schedule in decreasing order and call it the load vector. Suppose job $j$ moves from machine $h$ to machine $k$ and gains, so $L_k + p_{kj} < L_h$. Machine $h$ loses load, and the new load of $k$ is below the old load of $h$. Both changed entries are below the old $L_h$, and no other entry changes. So the load vector decreases in lexicographic order. There are finitely many schedules, so every sequence of improving moves is finite and ends in a pure equilibrium (the game has the [finite improvement property](/finite-improvement-property/)).

**Longest processing time first gives a pure equilibrium on identical machines.** Sort the jobs by $w_1 \ge w_2 \ge \dots \ge w_n$ and put each one on a machine of least load. Take any job $j$ on machine $h$, and let $k$ be the last job put on $h$. Then $w_k \le w_j$, and when $k$ was placed, $h$ had the least load, so $L_h - w_k$ is at most the final load $L_i$ of every machine $i$. So $L_h \le L_i + w_k \le L_i + w_j$, and job $j$ does not gain by a move. The algorithm takes $O(n \log n + n \log m)$ time. Fotakis and coauthors (2002) gave a greedy algorithm of the same kind for related machines.

**The price of stability is 1.** Start from an optimal schedule and let jobs make improving moves. By the lexicographic argument, the largest load never increases, so the final equilibrium is also optimal. This holds in all four environments.

**The best and the worst equilibria are hard to compute.** By the previous result, the best pure equilibrium has the optimal makespan, so computing it is as hard as [makespan minimization](/makespan-minimization/). For 2 identical machines, the [partition problem](/partition-problem/) reduces to deciding whether the optimal makespan is half the total weight. Fotakis and coauthors also proved that computing the worst pure equilibrium is NP-hard.

**Improving moves of unit jobs on identical machines.** With $w_j = 1$, the potential $\Phi = \sum_i L_i^2$ is at most $n^2$. A move from $h$ to $k$ with $L_k + 1 < L_h$ changes it by $2(L_k + 1 - L_h) \le -2$, because the loads are integers. So at most $n^2/2$ improving moves occur, in any order. Even-Dar, Kesselman and Mansour (2003) studied the number of moves for weighted jobs and other environments.

**Price of anarchy.** The bounds below are proved or cited on [price of anarchy of load balancing](/price-of-anarchy-of-load-balancing/).

| environment | pure equilibria | mixed equilibria |
|---|---|---|
| identical | $2 - 2/(m + 1)$ | $\Theta(\log m / \log \log m)$ |
| related | $\Theta(\log m / \log \log m)$ | $\Theta(\log m / \log \log \log m)$ |
| unrelated | unbounded | unbounded |

For unrelated machines, take 2 machines and 2 jobs with $p_{11} = \varepsilon$, $p_{21} = 1$, $p_{12} = 1$ and $p_{22} = \varepsilon$, for a small $\varepsilon > 0$. The schedule with job 1 on machine 2 and job 2 on machine 1 has makespan 1. Each job would pay $1 + \varepsilon$ after a move, so it is an equilibrium. The optimum puts each job on its fast machine, with makespan $\varepsilon$, so the ratio $1/\varepsilon$ is unbounded.

### Example

Take $m = 2$ identical machines and jobs of weights $2, 2, 1, 1$.

| schedule | loads | equilibrium? | makespan |
|---|---|---|---|
| $\{2, 1\}, \{2, 1\}$ | 3, 3 | yes | 3 |
| $\{2, 2\}, \{1, 1\}$ | 4, 2 | yes | 4 |
| $\{2, 2, 1\}, \{1\}$ | 5, 1 | no | 5 |

In the second schedule, a job of weight 2 that moves pays $2 + 2 = 4$, no less than now, and a job of weight 1 that moves pays $4 + 1 = 5$. So it is an equilibrium, with makespan 4 against the optimum 3, the ratio $4/3 = 2 - 2/3$. In the third schedule, a unit job on the first machine pays 5 and would pay $1 + 1 = 2$ after a move.

Now take 2 identical machines and 2 unit jobs, each of which picks a machine with probability $1/2$. A job pays $1 + 1/2$ on either machine, so this mixed profile is an equilibrium. The makespan is 2 with probability $1/2$ and 1 with probability $1/2$, so the expected makespan is $3/2$, while the optimum and every pure equilibrium have makespan 1. Koutsoupias and Papadimitriou proved that $3/2$ is the worst ratio for 2 identical machines.

## References
