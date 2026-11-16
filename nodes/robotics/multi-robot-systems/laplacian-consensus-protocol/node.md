---
tag: GHGHQ7
kind: algorithm
slug: laplacian-consensus-protocol
name: Laplacian consensus protocol
aliases:
- Olfati-Saber-Murray consensus
area: robotics/multi-robot-systems
level: core
summary: Each agent moves its state toward its neighbors by x' = -L x, which converges to the average on a connected undirected graph.
solves: [distributed-averaging]
model: real-ram
complexity:
  vars: {r: the number of agents, m: the number of edges, k: the number of rounds}
  time: {per_round: O(r + m), total: O(k (r + m))}
  messages: {per_round: O(m)}
  space: {extra: O(r)}
properties: {deterministic: true, randomized: false, online: true}
history:
  year: 2004
  people: [Reza Olfati-Saber, Richard M. Murray]
  note: Olfati-Saber and Murray stated the protocol x' = -L x for networks of agents with fixed and switching directed graphs and time delays, after Jadbabaie, Lin and Morse had analyzed the nearest-neighbor heading rule of Vicsek in 2003.
prereqs: [laplacian-matrix, eigenvalue]
see_also: [distributed-averaging, gossip-averaging, averaging-convergence-spectral-gap, perron-frobenius-theorem, multi-robot-rendezvous, formation-control, consensus-problem, boids]
sources:
  - paper: doi:10.1109/TAC.2004.834113
    title: Reza Olfati-Saber and Richard M. Murray, Consensus problems in networks of agents with switching topology and time-delays, IEEE Transactions on Automatic Control 49(9), 2004
    locator: pages 1520 to 1533 (the protocol, average consensus on balanced and strongly connected digraphs, switching topology and delays)
  - paper: doi:10.1109/TAC.2003.812781
    title: Ali Jadbabaie, Jie Lin and A. Stephen Morse, Coordination of groups of mobile autonomous agents using nearest neighbor rules, IEEE Transactions on Automatic Control 48(6), 2003
    locator: pages 988 to 1001 (agreement of headings when the union of the graphs over bounded intervals is connected)
  - paper: doi:10.1109/TAC.2005.846556
    title: Wei Ren and Randal W. Beard, Consensus seeking in multiagent systems under dynamically changing interaction topologies, IEEE Transactions on Automatic Control 50(5), 2005
    locator: pages 655 to 661 (consensus on directed graphs that have a spanning tree)
  - paper: doi:10.1109/JPROC.2006.887293
    title: Reza Olfati-Saber, J. Alex Fax and Richard M. Murray, Consensus and cooperation in networked multi-agent systems, Proceedings of the IEEE 95(1), 2007
    locator: pages 215 to 233 (survey of the continuous and discrete protocols and their convergence rates)
  - book: isbn:9780691140612
    title: Mehran Mesbahi and Magnus Egerstedt, Graph Theoretic Methods in Multiagent Networks, Princeton University Press, 2010
    locator: Chapter 3, The Agreement Protocol, Part I (Section 3.1 for undirected and Section 3.2 for directed graphs)
---

The Laplacian consensus protocol lets $r$ agents that talk only to their neighbors agree on a common value. Each agent $i$ holds a number $x_i$ and changes it at the rate $\dot x_i = \sum_{j} a_{ij} (x_j - x_i)$, the weighted sum of its differences to its neighbors. For the whole group this is $\dot x = -L x$, where $L = D - A$ is the [Laplacian matrix](/laplacian-matrix/) of the communication graph. On a fixed, connected, undirected graph every $x_i$ converges to the average of the initial values, and the slowest part of the error decays as $e^{-\lambda_2 t}$, where $\lambda_2$ is the second smallest eigenvalue of $L$. The sampled form $x(k+1) = (I - \varepsilon L) x(k)$ is the same idea in rounds, and it is one standard solution of [distributed averaging](/distributed-averaging/).

## In plain words

Some robots each hold a number, for example a guess of a heading or of a meeting time. No robot sees all the others. Each robot can only read the numbers of the robots near it.

Each robot repeats one small step. It looks at how far each neighbor is above or below its own number, adds up these gaps, and moves its own number a small part of the way in that direction. When the links go both ways with the same weight, what one robot gains its neighbor loses, so the total stays the same. The gaps shrink at every step, so all robots end at the same number, which is the mean of the start values.

If the links go one way only, the robots still agree when the network is well joined, but the common value can favor some robots over others.

## The problem

**The model.** There are $r$ agents, numbered $1$ to $r$, and a graph $G = (V, E)$ with $m$ edges. A weight $a_{ij} > 0$ means that agent $i$ reads the state of agent $j$; this is the convention of Olfati-Saber and Murray, with the neighbors $N_i = \{j : (i, j) \in E\}$. The graph is undirected when $a_{ij} = a_{ji}$, and directed otherwise. $D$ is the diagonal matrix of the weighted in-degrees $d_i = \sum_j a_{ij}$, and $\Delta = \max_i d_i$. The main case on this page is a fixed graph. In the sampled protocol the time is synchronous: in each round every agent reads the current states of its neighbors, and all agents update at the same time.

**Input.** The graph with its weights, the initial states $x(0) \in \mathbb{R}^r$, a step $\varepsilon$ with $0 < \varepsilon < 1/\Delta$, and a number $K$ of rounds. For vector states, such as positions in the plane, the protocol runs on each coordinate separately.

**Output.** The states $x(K)$. The goal is *agreement*, $x_i = x_j$ for all $i, j$, and on an undirected connected graph, *average consensus*, $x_i \to \bar x = \frac1r \sum_j x_j(0)$.

**How it differs from close pages.** [Distributed averaging](/distributed-averaging/) is the problem; this protocol is one solution, with the weight matrix $W = I - \varepsilon L$. [Gossip averaging](/gossip-averaging/) solves the same problem with random pairwise exchanges instead of synchronous rounds. The [consensus problem](/consensus-problem/) of distributed computing is a different problem: processes must decide on one of the proposed values in finite time while some of them crash or lie, and results such as [FLP impossibility](/flp-impossibility/) and protocols such as [Paxos](/paxos/) belong to it. The Laplacian protocol assumes no faults and reaches agreement only in the limit.

## The algorithm

```pseudo id=main
CONSENSUS(G, a, x(0), ε, K)
L1  each agent i learns its neighbors N_i and the weights a_ij
L2  for k = 0 to K - 1 do
L3      for each agent i, in parallel, do
L4          u_i ← Σ_{j ∈ N_i} a_ij (x_j(k) - x_i(k))     ▷ only the states of neighbors
L5          x_i(k+1) ← x_i(k) + ε u_i
L6      all agents switch to the new states at the same time
L7  return x(K)
```

Line L4 is the control input of the continuous protocol $\dot x_i = u_i$, and lines L4 and L5 together are one step of the explicit Euler method with step $\varepsilon$. In matrix form a round is $x(k+1) = (I - \varepsilon L) x(k)$. The condition $\varepsilon < 1/\Delta$ makes every diagonal entry $1 - \varepsilon d_i$ of $I - \varepsilon L$ positive, so each new state is a convex combination of the old states of the agent and its neighbors. The implementation also has a version that integrates $\dot x = -L x$ with the classic fourth order Runge-Kutta method and a fixed step, and a version that uses a different edge set in each round.

## Example

**Path of three agents.** Agents 1, 2 and 3 form the path 1 - 2 - 3 with unit weights. Then

$$L = \begin{pmatrix} 1 & -1 & 0 \\ -1 & 2 & -1 \\ 0 & -1 & 1 \end{pmatrix},$$

with eigenvalues 0, 1 and 3 and eigenvectors $(1, 1, 1)$, $(1, 0, -1)$ and $(1, -2, 1)$. The start $x(0) = (0, 3, 6)$ has the average 3, and its error $(-3, 0, 3)$ is an eigenvector of the eigenvalue 1. So the continuous protocol gives exactly $x(t) = (3 - 3 e^{-t}, 3, 3 + 3 e^{-t})$, and the sampled protocol with $\varepsilon = 1/4$ multiplies the error by $1 - 1/4 = 3/4$ in each round: $x(1) = (0.75, 3, 5.25)$, $x(2) = (1.3125, 3, 4.6875)$.

**Two modes.** The start $x(0) = (0, 0, 9)$ also has the average 3. Its error $(-3, -3, 6)$ is $-4.5 (1, 0, -1) + 1.5 (1, -2, 1)$, so

$$x(t) = 3 \cdot \mathbf 1 - 4.5 e^{-t} (1, 0, -1) + 1.5 e^{-3t} (1, -2, 1).$$

| $t$ (s) | $x_1$ | $x_2$ | $x_3$ |
|---|---|---|---|
| 0 | 0 | 0 | 9 |
| 0.5 | 0.6053 | 2.3306 | 6.0641 |
| 1 | 1.4192 | 2.8506 | 4.7301 |
| 2 | 2.3947 | 2.9926 | 3.6127 |
| 4 | 2.9176 | 3.0000 | 3.0824 |

The fast mode $e^{-3t}$ is gone after about one second. After that the middle agent sits near 3 and the two end agents approach 3 from both sides at the rate $e^{-t}$ of $\lambda_2 = 1$. The sampled protocol with $\varepsilon = 1/4$ gives $x(1) = (0, 2.25, 6.75)$, $x(2) = (0.5625, 2.8125, 5.625)$ and $x(4) = (1.5820, 2.9883, 4.4297)$, and the sum stays 9 in every round.

**One-way links.** On the directed chain where agent 2 reads agent 1 and agent 3 reads agent 2, agent 1 reads nobody. With $x(0) = (5, -1, 2)$ and $\varepsilon = 1/2$, the rounds give $(5, 2, 0.5)$, $(5, 3.5, 1.25)$, $(5, 4.25, 2.375)$, and all agents converge to 5, the value of the root. The average 2 is not reached, because the graph is not balanced.

## Correctness

The [proof](proofs/correctness/) shows that $L \mathbf 1 = 0$, so agreement is an equilibrium, and that on an undirected graph the sum $\mathbf 1^T x$ never changes. With the identity $x^T L x = \sum_{\{i,j\}} a_{ij} (x_i - x_j)^2$, the error $e = x - \bar x \mathbf 1$ of the continuous protocol obeys $\lVert e(t) \rVert \le e^{-\lambda_2 t} \lVert e(0) \rVert$ on a connected graph. For the sampled protocol with $0 < \varepsilon < 1/\Delta$, the error shrinks by the factor $\rho = \max(|1 - \varepsilon \lambda_2|, |1 - \varepsilon \lambda_r|) < 1$ per round, because the [Gershgorin circle theorem](/gershgorin-circle-theorem/) gives $\lambda_r \le 2 \Delta$. On a strongly connected directed graph, $I - \varepsilon L$ is a primitive stochastic matrix, and the [Perron-Frobenius theorem](/perron-frobenius-theorem/) gives the limit $(w^T x(0)) \mathbf 1$, where $w$ is the positive left kernel vector of $L$ with $\mathbf 1^T w = 1$. This is the average for every start if and only if the graph is balanced.

## Complexity

- **Per round.** Agent $i$ reads $|N_i|$ states and does $O(|N_i|)$ arithmetic. A round costs $O(r + m)$ operations in total, in the [real RAM](/real-ram/) model, and $O(m)$ messages, one state per edge and direction. Each agent stores $O(1)$ numbers besides its neighbor list.
- **Rounds, proved.** On a connected undirected graph, $K$ rounds reduce the error by the factor $\rho^K$ (Theorem 2 of the proof). To reduce it by a factor $\delta$ takes $K = \lceil \ln(1/\delta) / \ln(1/\rho) \rceil$ rounds. With $\varepsilon = 1/(2\Delta)$, $\rho = 1 - \lambda_2 / (2 \Delta)$ (Lemma 4 of the proof), so $K$ is about $2 \Delta \ln(1/\delta) / \lambda_2$. On the path of $r$ agents, $\lambda_2 = 2 - 2 \cos(\pi / r)$, which is about $\pi^2 / r^2$, so the path needs $\Theta(r^2 \log(1/\delta))$ rounds. On the complete graph, $\lambda_2 = r$ and $\Delta = r - 1$, so a constant number of rounds per factor suffices.
- **Continuous time.** The error decays as $e^{-\lambda_2 t}$, and this rate is attained by an eigenvector of $\lambda_2$. Better connected graphs have larger $\lambda_2$ and converge faster.

## Properties

- **Distributed.** Each agent uses only the states of its neighbors and its own weights. No agent needs $r$, the graph or an identifier.
- **Average preserving** on undirected and on balanced directed graphs, because $\mathbf 1^T L = 0$.
- **Linear and time invariant** on a fixed graph, so the solution is $x(t) = e^{-L t} x(0)$, and the [matrix exponential](/matrix-exponential/) gives exact values.
- **Asymptotic, not finite time.** The states agree only in the limit. Agents that must stop need a tolerance.
- **No fault tolerance.** One agent that keeps a fixed value pulls every agent to that value, as the root does in the directed example.
- **Deterministic.** The same graph and start always give the same states.

## Variants and improvements

- **Switching graphs.** If the graph changes over time, agreement still holds when the union of the graphs over every interval of bounded length is connected (Jadbabaie, Lin and Morse 2003), or, for directed graphs, has a rooted spanning tree (Ren and Beard 2005).
- **Directed graphs.** Agreement holds when the graph has a rooted spanning tree. The limit is the average only on balanced graphs (Olfati-Saber and Murray 2004).
- **Time delays.** With a delay $\tau$ in every link, the continuous protocol on a fixed undirected graph still converges if $\tau < \pi / (2 \lambda_r)$ (Olfati-Saber and Murray 2004).
- **Optimal weights.** For the sampled protocol, the weights that make $\rho$ smallest are the solution of a semidefinite program (Xiao and Boyd 2004), see [distributed averaging](/distributed-averaging/).
- **Second order consensus and flocking.** Agents with double integrator dynamics run the protocol on the velocities and a related rule on the positions, which gives velocity agreement as in [boids](/boids/).
- **Leader following.** One agent with fixed state and a graph with a rooted spanning tree make all agents converge to the leader, as in the directed example.

## When to use it

Use the protocol when agents must agree on one number or vector, such as a heading, a speed, a clock offset or the center of the group, and each agent can talk only to its neighbors. It is the building block of [rendezvous](/multi-robot-rendezvous/) for agents that stay connected and of displacement-based [formation control](/formation-control/), where agents agree on $x_i - c_i$ for given offsets $c_i$. Use [gossip averaging](/gossip-averaging/) when links fire at random times, and use a fault tolerant agreement protocol when agents can crash or lie.

## Pitfalls

- **Step size.** The sampled protocol needs $\varepsilon < 1/\Delta$ for the convex combination, and diverges when $\varepsilon \lambda_r > 2$. On the path of three agents with $\varepsilon = 0.9$, the mode $(1, -2, 1)$ is multiplied by $1 - 2.7 = -1.7$ in each round.
- **Direction of the edges.** Some texts write $a_{ij} > 0$ when $j$ reads $i$. Then $L$ is the transpose, and the condition on the graph changes from in-degrees to out-degrees. State the convention.
- **Directed graphs do not average.** On an unbalanced directed graph the limit is a weighted average, and on a graph without a rooted spanning tree there is no agreement at all.
- **Disconnected graphs.** Each connected component agrees on its own average. The protocol cannot detect that the graph is disconnected.
- **Moving robots.** When the states are positions and the graph depends on distances, the motion can break edges. The protocol alone does not keep the graph connected; see [connectivity maintenance](/connectivity-maintenance/).
- **Not the fault tolerant consensus.** The name is the same as the [consensus problem](/consensus-problem/) of distributed computing, but the guarantees are not.

## Implementations

## History

In 2003 Jadbabaie, Lin and Morse proved that the nearest neighbor heading rule from the flocking model of Vicsek et al. (1995) reaches agreement when the graph is connected often enough. In 2004 Olfati-Saber and Murray stated the protocol $\dot x = -L x$ for networks of agents, proved average consensus on balanced directed graphs, and treated switching graphs and delays. Ren and Beard extended the results to directed graphs with a spanning tree in 2005. The survey of Olfati-Saber, Fax and Murray (2007) and the book of Mesbahi and Egerstedt (2010) give the theory in one place.

## References
