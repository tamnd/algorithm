---
tag: S5R1H6
kind: algorithm
slug: distributed-pagerank
name: Distributed PageRank
aliases:
- distributed random walk PageRank
area: distributed/distributed-graph-algorithms
level: research
summary: Each node starts short random walks that stop with the reset chance ε, and counts the walks that visit it. In CONGEST this estimates all PageRank values in O(log n / ε) rounds.
model: congest-model
complexity:
  vars: {n: the number of nodes, m: the number of arcs, ε: the reset probability}
  time: {worst: O(log n / ε)}
  messages: {worst: O(m log n / ε)}
prereqs: [pagerank, congest-model, markov-chain, geometric-distribution]
see_also: [pagerank, power-iteration, personalized-pagerank, iterative-mapreduce, pregel-model, chernoff-bound, median-trick, congested-clique-model]
sources:
  - paper: doi:10.1007/978-3-642-35668-1_2
    title: Atish Das Sarma, Anisur Rahaman Molla, Gopal Pandurangan and Eli Upfal, Fast distributed PageRank computation, ICDCN 2013, LNCS 7730
    locator: pages 11 to 26, the walk algorithm in O(log n / ε) rounds on any graph and the faster O((log n)^(1/2) / ε) algorithm for undirected graphs; arXiv 1208.3071
  - paper: "Atish Das Sarma, Anisur Rahaman Molla, Gopal Pandurangan and Eli Upfal, Fast distributed PageRank computation, Theoretical Computer Science 561, 2015"
    locator: pages 113 to 121, the journal version
  - paper: "Lawrence Page, Sergey Brin, Rajeev Motwani and Terry Winograd, The PageRank citation ranking: bringing order to the web, Stanford technical report, 1999"
    locator: the definition of PageRank with the random surfer and the reset probability
  - paper: "Konstantin Avrachenkov, Nelly Litvak, Danil Nemirovsky and Natalia Osipova, Monte Carlo methods in PageRank computation: when one iteration is sufficient, SIAM Journal on Numerical Analysis 45(2), 2007"
    locator: the estimator that counts all visits of short walks from every node (the complete path estimator), in the sequential setting
  - paper: "Atish Das Sarma, Danupon Nanongkai, Gopal Pandurangan and Prasad Tetali, Distributed random walks, Journal of the ACM 60(1), 2013"
    locator: the stitching of short walks into a long walk, which the faster undirected algorithm uses
---

Distributed PageRank computes the [PageRank](/pagerank/) of each node of a network, where the network is the link graph itself. Each node runs a small program and talks only to its neighbours. The algorithm of Das Sarma, Molla, Pandurangan and Upfal (ICDCN 2013) uses the random surfer directly. Each node starts $K$ walk tokens. In each round, each token stops with the reset probability $\epsilon$, or moves to a random out-neighbour. Each node counts how many tokens visit it, and its count, times $\epsilon / (nK)$, is an unbiased estimate of its PageRank. The tokens are all alike, so a node sends one number on each link in each round, and the run fits the [CONGEST model](/congest-model/). It takes $O(\log n / \epsilon)$ rounds on any graph. On undirected graphs, the same paper joins short walks into long ones and gets $O(\sqrt{\log n} / \epsilon)$ rounds.

This page is about the walk algorithm in a message-passing network. The definition of PageRank and the sequential power method are on [PageRank](/pagerank/) and [power iteration](/power-iteration/). The batch form, where a cluster runs one iteration of the PageRank equation in each MapReduce job, is on [iterative MapReduce](/iterative-mapreduce/).

## In plain words

Imagine many people who walk on the web. Each starts on some page, and at each step either stops (with a small chance $\epsilon$, say 15%) or clicks a random link. A page that many walkers visit is important. That is PageRank.

Here the pages are computers, and the links are cables. Each computer starts some walkers and passes them on. A walker carries no name, so a computer only has to tell each neighbour how many walkers it sends. Walks are short, about $1/\epsilon$ steps on average, so after a few dozen rounds all walkers have stopped. Each computer then counts its visitors, and that count gives its PageRank. More walkers give a smaller error.

## The problem

**Input.** A directed graph $G = (V, E)$ with $n$ nodes and $m$ arcs, in which each node has at least one out-arc, and a reset probability $\epsilon \in (0, 1)$. Each node knows its out-arcs and $n$. Messages can travel in both directions of each arc.

**PageRank.** The vector $\pi$ with

$$
\pi(v) = \frac{\epsilon}{n} + (1 - \epsilon) \sum_{u \to v} \frac{\pi(u)}{\text{outdeg}(u)} .
$$

This is the stationary distribution of the walk that, at each step, jumps to a uniform node with probability $\epsilon$ and otherwise follows a uniform out-arc. Note that $\pi(v) \ge \epsilon / n$ for each $v$.

**Output.** Each node $v$ outputs $\tilde{\pi}(v)$ with $|\tilde{\pi}(v) - \pi(v)| \le \delta \pi(v)$, for all nodes at once, with probability at least $1 - 2/n$.

## The algorithm

Every node runs the same code. A round has a send step and a receive step.

```pseudo id=main
WALK-PAGERANK at node v, with K walks per node and R rounds
L1  count ← K; visits ← K
L2  for round r ← 1 to R do
L3      for each of the count tokens: with chance ε it stops, else pick a uniform out-arc
L4      send to each out-neighbour u the number of tokens that picked the arc to u
L5      count ← the sum of the numbers received; visits ← visits + count
L6  output π̃(v) = ε · visits / (n K)
```

The parameters are $R = \lceil \ln(n^2 K) / \epsilon \rceil$ and $K = \lceil 10 \ln(2 n^2) / (\epsilon \delta^2) \rceil$ for $0 < \delta \le 1$. A count is at most $nK$, so each message has $O(\log n)$ bits when $\epsilon$ and $\delta$ are at least $1 / \text{poly}(n)$. A node with no token in a round sends nothing.

## Example

Take the 4 nodes with the arcs $0 \to 1$, $1 \to 2$, $2 \to 0$, $2 \to 3$, $3 \to 0$, and $\epsilon = 0.2$. Power iteration gives $\pi = (0.2871, 0.2797, 0.2737, 0.1595)$. Node 3 has the lowest rank, since only node 2 links to it, and node 2 splits its rank between two arcs.

Run the algorithm with $K = 1000$, so that 4000 walks start. The run has $R = \lceil \ln(16000) / 0.2 \rceil = 49$ rounds. In one run of the implementation (seed 7), the visit counts are $(5732, 5564, 5464, 3186)$. The estimate of node 0 is $0.2 \cdot 5732 / 4000 = 0.2866$, and all four estimates are $(0.2866, 0.2782, 0.2732, 0.1593)$, each within 1% of $\pi$. The run sends 163 messages, the largest count needs 10 bits, and no token is alive at the end.

The expected number of visits to node 0 is $nK\pi(0)/\epsilon = 4000 \cdot 0.2871 / 0.2 = 5742$, and the run got 5732.

## Correctness

The full proof is in [the correctness proof](proofs/correctness). Its three parts:

1. **Unbiased.** Let $\zeta(v)$ be the number of visits to $v$ over all walks, with no limit on the length. A walk from $u$ makes $t$ steps without stopping and ends at $v$ with probability $((1 - \epsilon) P)^t[u, v]$, where $P$ is the walk matrix. So $\mathbb{E}[\zeta(v)] = K \mathbf{1}^\top (I - (1 - \epsilon) P)^{-1} e_v$, and the PageRank equation says that this is $nK \pi(v) / \epsilon$.
2. **Concentrated.** A walk that visits $v$ comes back to $v$ before it stops with a fixed probability $r(v) \le 1 - \epsilon$, so the visits of one walk are 0, or 1 plus a [geometric](/geometric-distribution/) number. The walks are independent. A [Chernoff](/chernoff-bound/) style bound on this sum gives $\Pr[|\zeta(v) - \mu| \ge \delta\mu] \le 2 e^{-(1 - r(v)) \delta^2 \mu / 10}$, with $\mu = \mathbb{E}[\zeta(v)] \ge K$.
3. **Truncation.** A token lives more than $R$ rounds with probability $(1 - \epsilon)^R \le 1 / (n^2 K)$. So with probability at least $1 - 1/n$, no token is alive after round $R$, and the counts of the run are the full counts $\zeta(v)$.

With the stated $K$, each node fails with probability at most $1/n^2$, and the union bound over the nodes and the truncation gives the result with probability at least $1 - 2/n$. Each claim is checked by the tests against power iteration.

## Complexity

| measure | bound |
|---|---|
| rounds | $R = \lceil \ln(n^2 K) / \epsilon \rceil = O(\log n / \epsilon)$ |
| messages | at most $m R = O(m \log n / \epsilon)$ |
| message size | $O(\log(nK)) = O(\log n)$ bits |
| local work | $O(K/\epsilon)$ token steps per node on average |
| memory per node | two counters and one counter per out-arc |

The number of tokens, $nK$, does not change the number of rounds, only the size of the counts. The rounds do not depend on the diameter. A walk has about $1/\epsilon$ steps, and the bound needs only that all $nK$ walks end.

## Properties

- **Randomized and Monte Carlo.** The output is close with high probability, not always.
- **One message per arc per round.** A message is an integer count, not a real number, so there is no rounding error in the communication.
- **No global step.** No tree, no leader and no synchronizing step are needed, except that all nodes know $n$ and stop after $R$ rounds.
- **The relative error is the same for all nodes.** Since $\mu \ge K$ for each node, nodes with small PageRank get the same relative error bound as nodes with large PageRank.

## Variants and improvements

- **Undirected graphs, $O(\sqrt{\log n} / \epsilon)$ rounds.** *Sketch.* Das Sarma et al. first let each node prepare short walks in parallel, and then make each long walk by joining short walks, as in the distributed random walks of Das Sarma, Nanongkai, Pandurangan and Tetali. Undirected links let a token go back along a short walk. See the paper for the parameters.
- **Distributed power iteration.** Each node sends $(1 - \epsilon)\pi_t(u)/\text{outdeg}(u)$ to its out-neighbours, rounded to $O(\log n)$ bits. The error in the $\ell_1$ norm shrinks by the factor $1 - \epsilon$ in each round, and $\pi(v) \ge \epsilon/n$, so $O(\log(n/\delta)/\epsilon)$ rounds give relative error $\delta$. This is deterministic and has the same round bound as the walk algorithm. The walk algorithm has integer messages and an error bound with no rounding analysis, and its walks can be joined, which gives the faster undirected bound.
- **[Personalized PageRank](/personalized-pagerank/).** Start the walks only at the source node. The same estimator then gives the personalized vector.
- **The end point estimator.** Count only where each walk stops. This is also unbiased, but it uses each walk once, so it needs more walks for the same error.

## When to use it

- The graph is a real network of machines, and each machine is a node with its links, for example a peer-to-peer network that ranks its peers.
- Messages must be small, and the graph is large, so a node cannot hold real numbers for its many neighbours at full precision.
- Only an estimate with relative error $\delta$ is needed, not many digits.

For a graph that sits in a cluster as data, use [iterative MapReduce](/iterative-mapreduce/) or a [Pregel](/pregel-model/) system. For one machine, use [power iteration](/power-iteration/).

## Pitfalls

- **Nodes with no out-arc.** The walk stops there, and the estimate is then of another vector. Add a self loop, or let the walk jump, which needs a global step.
- **Too few walks.** The error bound grows as $1/\sqrt{K}$. With $K$ fixed and $n$ large, some nodes will be far off. Use $K = \Theta(\log n / (\epsilon \delta^2))$ for the bound on all nodes.
- **Stopping too early.** With $R$ less than about $\ln(nK)/\epsilon$, some walks are cut short, and all estimates are too low.
- **Wrong normalization.** The estimate is $\epsilon \cdot \text{visits} / (nK)$, and the visits count the start. Without the start, the sum of the estimates is $1 - \epsilon$, not 1.
- **Correlated randomness.** Each token must use fresh random choices. If a node sends all its tokens on the same arc, the estimate is wrong.

## Implementations

## History

Page, Brin, Motwani and Winograd defined PageRank in a 1999 report, with the random surfer that the walk algorithm uses. Monte Carlo estimators that count the visits of short walks were studied for sequential PageRank, for example by Avrachenkov, Litvak, Nemirovsky and Osipova (SIAM J. Numer. Anal. 2007). Das Sarma, Molla, Pandurangan and Upfal gave the distributed algorithm and its analysis in CONGEST at ICDCN 2013, with the journal version in Theoretical Computer Science in 2015. They called these the first fully distributed algorithms for PageRank with a proven run time. Their faster undirected algorithm uses the stitching of short walks from the work on distributed random walks by Das Sarma, Nanongkai, Pandurangan and Tetali (JACM 2013).

## References
