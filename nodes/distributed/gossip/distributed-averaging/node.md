---
tag: XNYGXK
kind: problem
slug: distributed-averaging
name: Distributed averaging
aliases:
- average consensus
- gossip averaging problem
area: distributed/gossip
level: core
summary: Every node of a network holds a number, and all nodes must learn the average of the numbers by talking only to their neighbours.
prereqs: [graph, synchronous-model, transition-matrix, eigenvalue]
see_also: [gossip-averaging, averaging-convergence-spectral-gap, push-sum, gossip-aggregation, network-size-estimation, spectral-gap, mixing-time, metropolis-hastings]
sources:
  - paper: doi:10.1016/j.sysconle.2004.02.022
    title: Lin Xiao and Stephen Boyd, Fast linear iterations for distributed averaging, Systems and Control Letters 53(1), 2004
    locator: pages 65 to 78 (the convergence condition for x(t+1) = W x(t), the asymptotic convergence factor, and the optimal symmetric weights as a semidefinite program)
  - paper: doi:10.1109/TIT.2006.874516
    title: Stephen Boyd, Arpita Ghosh, Balaji Prabhakar and Devavrat Shah, Randomized gossip algorithms, IEEE Transactions on Information Theory 52(6), 2006
    locator: pages 2508 to 2530 (the randomized pairwise version of the problem and its averaging time)
  - paper: "Lin Xiao, Stephen Boyd and Sanjay Lall, A scheme for robust distributed sensor fusion based on average consensus, Fourth International Symposium on Information Processing in Sensor Networks (IPSN), 2005"
    locator: the Metropolis-Hastings weights, which a node computes from its own degree and the degrees of its neighbours
---

Distributed averaging is the problem in which each node $i$ of a connected [graph](/graph/) holds a real number $x_i(0)$, and every node must compute the average $\bar x = \frac1n \sum_i x_i(0)$ while it exchanges messages only with its neighbours. The standard solution is a linear iteration $x(t+1) = W x(t)$ with a doubly stochastic weight matrix $W$ that follows the edges of the graph. The values converge to $\bar x$ exactly when $W$ has a [spectral gap](/spectral-gap/), and the second largest eigenvalue modulus (SLEM) of $W$ sets the rate. The problem is the base of [gossip averaging](/gossip-averaging/), [push-sum](/push-sum/) and [gossip aggregation](/gossip-aggregation/).

## In plain words

A group of sensors each measures a temperature. No sensor sees the whole network, and there is no central server. Each sensor can only talk to the sensors next to it. All of them must agree on the mean temperature.

Each sensor repeats one simple step: it replaces its number by a weighted mix of its own number and the numbers of its neighbours. If the mix weights are chosen well, the total of all numbers never changes, and the numbers get closer to each other at each step. After enough steps every sensor holds a number very close to the mean.

How fast this happens depends on the shape of the network. A well connected network mixes fast. A long chain or ring mixes slowly, because a change at one end needs many steps to reach the other end.

## Definition

**Model.** The network is a connected undirected graph $G = (V, E)$ with $n = |V|$ nodes and $m = |E|$ edges, and $d_i$ is the degree of node $i$. Computation is in the [synchronous model](/synchronous-model/): in each round every node sends a message to each neighbour, receives the messages of its neighbours, and updates its state. There are no failures. The cost measures are the number of rounds and the number of messages.

**Input and output.** Node $i$ starts with $x_i(0) \in \mathbb{R}$. Let $\mathbf 1$ be the all ones vector and $\bar x = \frac1n \mathbf 1^T x(0)$. An algorithm solves *exact* averaging if every node outputs $\bar x$, and *asymptotic* averaging if $x_i(t) \to \bar x$ for all $i$ as $t \to \infty$. The $\varepsilon$-averaging time is the least $t$ with $\|x(t) - \bar x \mathbf 1\|_2 \le \varepsilon \|x(0) - \bar x \mathbf 1\|_2$ for all inputs.

**Linear iterations.** A linear iteration fixes a real $n \times n$ matrix $W$ with $W_{ij} = 0$ whenever $i \ne j$ and $\{i, j\} \notin E$, and runs

$$x(t+1) = W x(t), \qquad \text{so} \qquad x_i(t+1) = W_{ii} x_i(t) + \sum_{j : \{i,j\} \in E} W_{ij} x_j(t).$$

Let $J = \frac1n \mathbf 1 \mathbf 1^T$, the projection onto the constant vectors.

**Theorem (Xiao and Boyd 2004).** $\lim_{t \to \infty} W^t = J$, that is, the iteration solves asymptotic averaging for every input, if and only if

$$\mathbf 1^T W = \mathbf 1^T, \qquad W \mathbf 1 = \mathbf 1, \qquad \rho(W - J) < 1,$$

where $\rho$ is the [spectral radius](/spectral-radius/).

*Proof.* Suppose the three conditions hold. From $W\mathbf 1 = \mathbf 1$ and $\mathbf 1^T W = \mathbf 1^T$ we get $WJ = JW = J$, and $J^2 = J$. By induction on $t$, $(W - J)^t = W^t - J$ for $t \ge 1$: the case $t = 1$ is clear, and $(W^t - J)(W - J) = W^{t+1} - W^t J - JW + J^2 = W^{t+1} - J - J + J$. A matrix power $A^t$ tends to $0$ if and only if $\rho(A) < 1$, so $W^t - J \to 0$. Conversely, suppose $W^t \to J$. Then $JW = \lim W^{t+1} = J$ and $WJ = J$ in the same way. Multiplying $JW = J$ on the left by $\mathbf 1^T$ gives $\mathbf 1^T W = \mathbf 1^T$, and multiplying $WJ = J$ on the right by $\mathbf 1$ gives $W \mathbf 1 = \mathbf 1$. Then the identity above holds again, so $(W - J)^t = W^t - J \to 0$, and $\rho(W - J) < 1$. $\square$

**The rate for symmetric weights.** Let $W$ be symmetric with $W \mathbf 1 = \mathbf 1$, and let $1 = \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_n$ be its eigenvalues, with $\mathbf 1$ the eigenvector of $\lambda_1$. The eigenvalues of $W - J$ are $0, \lambda_2, \ldots, \lambda_n$, so $\rho(W - J) = \max(\lambda_2, -\lambda_n)$, the SLEM. The error $e(t) = x(t) - \bar x \mathbf 1$ satisfies $e(t+1) = (W - J) e(t)$, because $\mathbf 1^T x(t)$ stays the same. A symmetric matrix has operator 2-norm equal to its spectral radius, so

$$\|e(t)\|_2 \le \mathrm{SLEM}(W)^t \, \|e(0)\|_2,$$

with equality in the limit for an input that has a component on the eigenvector of the extreme eigenvalue. Hence the $\varepsilon$-averaging time is $\lceil \ln(1/\varepsilon) / \ln(1/\mathrm{SLEM}(W)) \rceil$ rounds.

**Metropolis weights.** Set $W_{ij} = 1/(1 + \max(d_i, d_j))$ for each edge $\{i, j\}$, and $W_{ii} = 1 - \sum_{j \ne i} W_{ij}$. Each node computes its row from its own degree and the degrees of its neighbours, with no global knowledge. The matrix is symmetric, so its columns also sum to 1. Each diagonal entry is positive, because $\sum_{j \ne i} W_{ij} \le d_i / (1 + d_i) < 1$. On a connected graph the matrix is irreducible, and the positive diagonal makes it aperiodic, so by the [Perron-Frobenius theorem](/perron-frobenius-theorem/) the eigenvalue 1 is simple and every other eigenvalue has modulus below 1. So the Metropolis iteration solves asymptotic averaging on every connected graph. These are the weights of the [Metropolis-Hastings](/metropolis-hastings/) chain with the uniform distribution as target.

**Optimal weights.** For a fixed graph, the symmetric $W$ with the smallest SLEM solves

$$\text{minimize } s \quad \text{subject to} \quad -sI \preceq W - J \preceq sI, \quad W = W^T, \quad W\mathbf 1 = \mathbf 1, \quad W_{ij} = 0 \text{ for } i \ne j, \{i,j\} \notin E.$$

This is a [semidefinite program](/semidefinite-programming/), because the SLEM of a symmetric matrix is a convex function of its entries. Xiao and Boyd solve it centrally and also give a distributed subgradient method. The optimal weights may be negative.

## Variants

- **Randomized pairwise averaging.** At each step one random edge wakes up and its two end nodes replace their values by their mean. This is [randomized gossip averaging](/gossip-averaging/), with its own matrix $\bar W$ and averaging time.
- **Directed or one way links.** With only $W \mathbf 1 = \mathbf 1$ or only $\mathbf 1^T W = \mathbf 1^T$ the iteration converges to a weighted average. [Push-sum](/push-sum/) keeps a sum and a weight per node and outputs their ratio, which gives the true average with column stochastic $W$.
- **Unstructured overlays.** In a peer to peer system each node picks a random peer in each cycle. [Gossip-based aggregation](/gossip-aggregation/) runs push-pull averaging this way and adds restarts for churn.
- **Continuous time.** The flow $\dot x = -Lx$, with $L$ the [Laplacian matrix](/laplacian-matrix/) of the graph, converges to $\bar x \mathbf 1$ at the rate set by the second smallest eigenvalue of $L$.
- **Other aggregates.** Averaging the indicator of one node gives $1/n$, which is the base of [network size estimation](/network-size-estimation/). Averaging $x_i^2$ next to $x_i$ gives the variance.

## Examples

**The cycle.** Take the cycle $C_{10}$. Every degree is 2, so the Metropolis weights are $W_{ii} = W_{i,i\pm1} = \frac13$. The matrix is circulant with eigenvalues $(1 + 2\cos(2\pi k/10))/3$ for $k = 0, \ldots, 9$. The SLEM is the value for $k = 1$, $(1 + 2\cos(\pi/5))/3 = 0.8727$; the value for $k = 5$ is $-\frac13$. Start with $x(0) = (1, 0, \ldots, 0)$, so $\bar x = 0.1$:

| round $t$ | $x_1(t)$ | $x_2(t)$ | $x_3(t)$ | $\lVert x(t) - \bar x \mathbf 1 \rVert_2$ |
|---|---|---|---|---|
| 0 | 1 | 0 | 0 | 0.9487 |
| 1 | 0.3333 | 0.3333 | 0 | 0.4830 |
| 2 | 0.3333 | 0.2222 | 0.1111 | 0.3668 |
| 10 | 0.1517 | 0.1416 | 0.1155 | 0.1146 |
| 20 | 0.1131 | 0.1106 | 0.1041 | 0.0293 |
| 30 | 0.1034 | 0.1027 | 0.1010 | 0.0075 |

From round 20 to round 30 the error shrinks by the factor $0.0075/0.0293 = 0.256$, and $0.8727^{10} = 0.256$, the SLEM to the tenth power. On the $4 \times 4$ grid the Metropolis SLEM is $0.8686$.

**A non-example.** On the cycle $C_6$ take $W = A/2$, where $A$ is the adjacency matrix, so each node takes the mean of its two neighbours and ignores its own value. $W$ is symmetric and doubly stochastic, but the cycle is bipartite and $W$ has the eigenvalue $-1$ with eigenvector $(1, -1, 1, -1, 1, -1)$. So $\rho(W - J) = 1$, and the input $(1, 0, 1, 0, 1, 0)$ flips to $(0, 1, 0, 1, 0, 1)$ and back for ever. Any positive weight on the diagonal removes the problem.

**Cycle rate in general.** For Metropolis on $C_n$, $1 - \mathrm{SLEM} = \frac23(1 - \cos(2\pi/n)) \sim 4\pi^2/(3n^2)$ for large $n$. So the iteration needs $\Theta(n^2 \log(1/\varepsilon))$ rounds on a cycle. On the [complete graph](/complete-graph/) the matrix $W = J$ is allowed, its SLEM is 0, and one round is enough.

## Known algorithms

| algorithm | model | result |
|---|---|---|
| Linear iteration, Metropolis weights | synchronous, fixed graph, local degrees only | asymptotic, rate SLEM$(W)$ per round |
| Linear iteration, optimal weights (Xiao and Boyd 2004) | synchronous, weights found by an SDP | asymptotic, smallest SLEM over symmetric $W$ on $G$ |
| [Randomized gossip averaging](/gossip-averaging/) (Boyd et al. 2006) | asynchronous, one random edge per clock tick | asymptotic, time set by $\lambda_2(\bar W)$ |
| [Push-sum](/push-sum/) (Kempe, Dobra and Gehrke 2003) | synchronous rounds, uniform random targets | relative error $\varepsilon$ in $O(\log n + \log 1/\varepsilon + \log 1/\delta)$ rounds |
| [Push-pull aggregation](/gossip-aggregation/) (Jelasity, Montresor and Babaoglu 2005) | cycles on a peer sampling overlay | variance falls by about $1/(2\sqrt e)$ per cycle |
| [Convergecast](/convergecast/) on a spanning tree, then broadcast | synchronous, needs a tree | exact, $O(D)$ rounds, fragile under failures |

## Bounds

- **Locality lower bound.** After $t$ rounds of any algorithm, the state of node $i$ depends only on the inputs within distance $t$ of $i$. Changing an input at distance more than $t$ by $\Delta$ moves $\bar x$ by $\Delta/n$ and leaves node $i$ unchanged, so one of the two inputs has error at least $\Delta/(2n)$ at $i$. So no algorithm reaches a small error at every node before round $\max_i \mathrm{ecc}(i) \ge D/2$, where $D$ is the diameter.
- **Linear iterations.** For a symmetric $W$ the number of rounds is $\lceil \ln(1/\varepsilon) / \ln(1/\mathrm{SLEM}) \rceil$ in the worst case over inputs, as shown above. A small spectral gap $1 - \mathrm{SLEM}$ gives about $\ln(1/\varepsilon)/(1 - \mathrm{SLEM})$ rounds.
- **Messages.** Each round of a linear iteration sends $2m$ messages, one in each direction of each edge.

## Reductions

- **To Markov chains.** A symmetric stochastic $W$ is the [transition matrix](/transition-matrix/) of a reversible chain with the uniform [stationary distribution](/stationary-distribution/), and $x(t) = W^t x(0)$. So the averaging time of the iteration is, up to constants and the factor $\log(1/\varepsilon)$, the [mixing time](/mixing-time/) of the chain, and fast averaging is the same task as fast mixing on $G$.
- **Sum and count.** If $n$ is known, the sum is $n \bar x$. If one node starts with 1 and the rest with 0, the average is $1/n$, so averaging solves [network size estimation](/network-size-estimation/).
- **Linear functions.** Any $\sum_i c_i x_i(0)$ with known $c_i$ reduces to averaging $n c_i x_i(0)$.

## Applications

- Fusion of sensor readings in a wireless sensor network with no base station, often modelled as a [random geometric graph](/random-geometric-graph/).
- Load balancing, where each node holds a load and the loads should become equal.
- Distributed estimation and distributed [gradient descent](/gradient-descent/), where nodes average their local estimates or gradients at each step.
- [Clock synchronization](/clock-synchronization/) by averaging clock offsets with neighbours.
- Monitoring of large peer to peer systems, where [gossip aggregation](/gossip-aggregation/) gives the mean load, the number of nodes or the largest value.

## References
