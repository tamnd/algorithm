---
tag: 0EEST3
kind: model
slug: nash-flows-over-time
name: Nash flows over time
aliases:
- Koch-Skutella dynamic equilibria
- dynamic Wardrop equilibrium
area: algorithmic-game-theory/inefficiency-of-equilibria
level: research
summary: "An equilibrium of a routing game with queues, in which particles enter over time and each takes a path that reaches the sink earliest."
prereqs: [wardrop-equilibrium, selfish-routing-model, max-flow-problem]
see_also: [price-of-anarchy, braess-paradox, min-cut-problem, min-cost-flow-problem, dijkstra, temporal-graph, kakutani-fixed-point-theorem, stackelberg-routing]
sources:
  - paper: "Ronald Koch and Martin Skutella, Nash equilibria and the price of anarchy for flows over time, Theory of Computing Systems 49(1) (2011); SAGT 2009"
    locator: "the model with the deterministic queue, earliest arrival labels, the characterization of Nash flows over time by thin flows with resetting, and their construction in phases"
  - paper: "William S. Vickrey, Congestion theory and transport investment, American Economic Review 59(2) (1969)"
    locator: the bottleneck model with a deterministic queue
  - paper: "Roberto Cominetti, Jose Correa and Omar Larre, Dynamic equilibria in fluid queueing networks, Operations Research 63(1) (2015)"
    locator: existence of dynamic equilibria for general inflow rates and uniqueness of the arrival times
  - paper: "Roberto Cominetti, Jose Correa and Neil Olver, Long-term behavior of dynamic equilibria in fluid queuing networks, Operations Research 70(1) (2022); IPCO 2017"
    locator: bounded queues and a steady state when the inflow rate is at most the capacity of a minimum cut
  - paper: doi:10.1145/3328526.3329593
    title: "Jose Correa, Andres Cristi and Tim Oosterwijk, On the price of anarchy for flows over time, EC 2019, 559-577; Mathematics of Operations Research"
    locator: "the bound e/(e - 1) when the inflow may be reduced, the value 4/3 on parallel links, and the monotonicity conjecture"
  - paper: "L. R. Ford and D. R. Fulkerson, Constructing maximal dynamic flows from static flows, Operations Research 6(3) (1958)"
    locator: flows over time and temporally repeated flows
---

A Nash flow over time is the equilibrium of a routing game in which time matters: traffic enters the network over time, edges take time to cross, and when too much traffic arrives at an edge it waits in a queue. Each tiny particle of traffic picks a path that gets it to the sink as early as possible, given the queues that the particles before it have built. The static [Wardrop equilibrium](/wardrop-equilibrium/) of the [selfish routing model](/selfish-routing-model/) has no time and no queues, only latency functions; this model replaces latency functions by queues that grow and shrink, and the main tool of Koch and Skutella (2009) describes the equilibrium by how fast arrival times change.

## The machine

**Network.** A directed graph $G = (V, E)$ with a source $s$ and a sink $t$. Each edge $e$ has a capacity $u_e > 0$, the largest rate at which flow can leave the edge, and a transit time $\tau_e \ge 0$.

**Inflow.** Flow enters at $s$ at a constant rate $r > 0$. Flow is a fluid of particles, and the particle that enters at time $\theta \ge 0$ is called particle $\theta$. Each particle is tiny, so this is a nonatomic game: its players are the particles.

**Queues.** Flow that enters edge $e$ first passes a queue at the tail of $e$, then travels for time $\tau_e$. The queue works first in, first out, and lets flow out at rate $u_e$ while it is not empty. Let $f^+_e(\xi)$ be the rate at which flow enters $e$ at time $\xi$, and $z_e(\xi)$ the amount of flow in its queue. The queue grows when the inflow is more than the capacity:

$$z_e'(\xi) = \begin{cases} f^+_e(\xi) - u_e & \text{if } z_e(\xi) > 0, \\ \max\{f^+_e(\xi) - u_e,\, 0\} & \text{if } z_e(\xi) = 0. \end{cases}$$

A particle that enters $e$ at time $\xi$ waits $z_e(\xi)/u_e$ and leaves $e$ at time $\xi + z_e(\xi)/u_e + \tau_e$. This is the deterministic queue of Vickrey's bottleneck model (1969).

**Costs and equilibrium notion.** This is a cost game. The cost of a particle is the time at which it reaches $t$. For each node $v$ let $\ell_v(\theta)$ be the earliest time at which particle $\theta$ can reach $v$, given the queues; these are the earliest arrival labels, with $\ell_s(\theta) = \theta$. A flow over time is a *Nash flow over time* if almost every particle $\theta$ uses a path on which it reaches each node $v$ of the path at time $\ell_v(\theta)$, that is, a shortest path given the queues. A particle that picks its path at random gains nothing: a mixed best response has its support inside the set of pure best responses, which here are the current shortest paths. So the model works with pure path choices.

**Existence.** Nash flows over time exist. Koch and Skutella constructed them for a constant inflow rate, and Cominetti, Correa and Larre (2015) proved existence for general inflow rates and showed that the labels $\ell_v(\theta)$ are the same in every equilibrium (theorems).

## What it counts

- The arrival time $\ell_t(\theta)$ of each particle, and the queues on the edges over time.
- The [price of anarchy](/price-of-anarchy/) for measures with time, for example the time at which a given amount of flow has reached $t$, compared with the best flow over time that sends the same amount.
- The long-run behavior: whether queues stay bounded and the flow reaches a steady state.

## Relation to other models

- **Static selfish routing.** In the [selfish routing model](/selfish-routing-model/) each edge has a latency function of its flow, and the equilibrium is a single flow. Here the delay on an edge is the waiting time in a queue, which depends on the whole history of the flow, not on the current flow alone.
- **Flows over time without selfishness.** Ford and Fulkerson (1958) introduced flows over time and showed that a maximum flow over time can be found by a [min-cost flow](/min-cost-flow-problem/) computation and repeated over time. Nash flows over time use the same network data, but the flow is chosen by the particles.
- **Paradoxes.** The analog of [Braess's paradox](/braess-paradox/) also occurs: adding an edge can make the arrival times later.
- **Dynamic traffic assignment.** In transport research, the same kind of model is studied as dynamic user equilibrium, with the bottleneck model of Vickrey as its basic edge.

## Known results in the model

Each item is a theorem unless it is marked as an open problem.

**Characterization by thin flows (Koch and Skutella).** Fix a particle $\theta$. An edge $e = (v, w)$ is *active* if it is on a shortest path, that is, $\ell_w(\theta) = \ell_v(\theta) + z_e/u_e + \tau_e$ at the time $\ell_v(\theta)$; it is *resetting* if it also has a positive queue then. Write $x_e(\theta)$ for the amount of flow from particles $0$ to $\theta$ that uses $e$. The derivatives $\ell'_v$ and $x'_e$ satisfy:

- $\ell'_s = 1$, and $x'$ is a static $s$-$t$ flow of value $r$ on the active edges;
- for a resetting edge $e = (v, w)$, the value $\rho_e = x'_e/u_e$;
- for an active edge without a queue, the value $\rho_e = \max\{\ell'_v,\ x'_e/u_e\}$;
- $\ell'_w = \min_e \rho_e$ over the active edges into $w$, with $\ell'_w = \rho_e$ if $x'_e > 0$.

A solution is a *thin flow with resetting*. Koch and Skutella proved that one exists on every network, with a fixed point argument ([Kakutani fixed point theorem](/kakutani-fixed-point-theorem/)), and that a Nash flow over time is built from a sequence of phases: in each phase the active and resetting edges are fixed, the labels grow linearly, and the phase ends when a new edge becomes active or a queue runs out.

**Long-term behavior (Cominetti, Correa and Olver).** If $r$ is at most the capacity of a minimum $s$-$t$ cut ([min cut](/min-cut-problem/)), then all queues stay bounded, and the Nash flow over time reaches a steady state in which the queues are constant. If $r$ is larger, some queues grow without bound.

**Price of anarchy (Correa, Cristi and Oosterwijk 2019).** Measure the time at which a given amount of flow has reached $t$ in the equilibrium, against the least such time over all flows over time. If the network designer may reduce the inflow rate, the price of anarchy is $e/(e - 1) \approx 1.582$, and on networks of parallel links it is $4/3$. This extends earlier work of Bhaskar, Fleischer and Anshelevich (2011).

**Open problem (Correa, Cristi and Oosterwijk, 2019; open in the journal version).** The monotonicity conjecture: in a Nash flow over time, the time at which a given amount of flow has reached $t$ does not increase when the inflow rate $r$ increases. If it holds, the price of anarchy above is $e/(e - 1)$ in general, without the change of inflow. The authors proved it for special classes of networks, such as chains of parallel paths.

### Example

Take two parallel edges from $s$ to $t$, both with capacity 1. Edge 1 has transit time 1 and edge 2 has transit time 2.

**Inflow rate $r = 3$.** At first only edge 1 is active. It receives flow at rate 3 and lets out flow at rate 1, so its queue is $z_1 = 2\theta$ and particle $\theta$ arrives at $\ell_t(\theta) = \theta + 2\theta + 1 = 1 + 3\theta$. Edge 2 offers the arrival time $\theta + 2$, and the two are equal at $\theta = 1/2$, when $\ell_t = 5/2$. From then on both edges are active, edge 1 is resetting and edge 2 has no queue. The thin flow conditions are

$$\ell'_t = x'_1 \quad\text{and}\quad \ell'_t = \max\{1,\ x'_2\}, \qquad x'_1 + x'_2 = 3.$$

If $x'_2 \le 1$, then $x'_1 = 1$ and the sum is at most 2, which is impossible. So $x'_1 = x'_2 = 3/2$ and $\ell'_t = 3/2$, that is, $\ell_t(\theta) = 5/2 + \frac{3}{2}(\theta - 1/2)$. Both queues grow at rate $1/2$ forever, as the inflow 3 exceeds the cut capacity 2. To check particle $\theta \ge 1/2$ on edge 2: the queue there is $\frac{1}{2}(\theta - 1/2)$, so it arrives at $\theta + \frac{1}{2}(\theta - 1/2) + 2 = \frac{3}{2}\theta + \frac{7}{4}$, the same as $\ell_t(\theta)$.

**Inflow rate $r = 3/2$.** Edge 1 alone gives $\ell_t(\theta) = \theta + \theta/2 + 1$, which reaches $\theta + 2$ at $\theta = 2$. Then the queue on edge 1 has size 1. From then on $x'_1 = 1$, so the queue stays at size 1, and $x'_2 = 1/2 \le 1$, so edge 2 never gets a queue. Both edges give the arrival time $\theta + 2$, and the flow is in a steady state, as the result of Cominetti, Correa and Olver says for an inflow rate below the cut capacity 2.

## References
