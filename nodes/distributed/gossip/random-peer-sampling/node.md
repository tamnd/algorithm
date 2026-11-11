---
tag: F8JAYE
kind: problem
slug: random-peer-sampling
name: Random peer sampling
aliases:
- peer sampling
area: distributed/gossip
level: advanced
summary: Each node of a large dynamic network must be able to draw peers that are close to independent uniform samples of the live nodes, while it knows only a few other nodes.
prereqs: [markov-chain, stationary-distribution, mixing-time]
see_also: [peer-sampling-service, newscast, cyclon, membership-management, metropolis-hastings, random-walk-metropolis, mixing-time, network-size-estimation]
sources:
  - paper: doi:10.1145/1275517.1275520
    title: Márk Jelasity, Spyros Voulgaris, Rachid Guerraoui, Anne-Marie Kermarrec and Maarten van Steen, Gossip-based peer sampling, ACM Transactions on Computer Systems 25(3), article 8, 2007
    locator: the uniform ideal, and the measures used to compare gossip-based solutions (in-degree distribution, clustering, path length, removal of dead links)
  - paper: "Daniel Stutzbach, Reza Rejaie, Nick Duffield, Subhabrata Sen and Walter Willinger, On unbiased sampling for unstructured peer-to-peer networks, ACM Internet Measurement Conference (IMC), 2006"
    locator: the bias of the simple random walk toward high degree peers, and the Metropolis-Hastings random walk that removes it
  - paper: "Laurent Massoulié, Erwan Le Merrer, Anne-Marie Kermarrec and Ayalvadi Ganesh, Peer counting and sampling in overlay networks: random walk methods, 25th ACM Symposium on Principles of Distributed Computing (PODC), 2006"
    locator: the continuous time random walk sampler with a timer
---

Random peer sampling is the problem in which every node of a large network, which knows only a few other nodes, must be able to draw peers that are close to independent uniform samples of all live nodes. It is the problem under almost every [gossip protocol](/gossip-protocol/), whose analysis assumes that a node can call a uniform random peer. There are two families of solutions: gossip protocols that keep a small random view at every node, such as [Newscast](/newscast/) and [Cyclon](/cyclon/), and random walks on the overlay, such as the [Metropolis-Hastings](/metropolis-hastings/) walk. The interface that the solutions offer is the [peer sampling service](/peer-sampling-service/).

## In plain words

Gossip works best when each computer talks to someone chosen completely at random from the whole group. But a computer in a group of millions only knows a few dozen others.

There are two ways around this. In the first, every computer keeps a short list of names and often swaps names with others, so each list keeps looking like a random handful of the group. In the second, a message walks from computer to computer for a while, and the computer where it stops is the sample.

A plain walk has a bias: it stops more often at computers with many links. A small change fixes this. Before the walk moves to a computer with more links, it flips a coin and sometimes stays where it is. Then every computer is equally likely to be the stopping point.

## Definition

**Model.** The live nodes at time $t$ form a set $V_t$ of size $n_t$. Each node $p$ keeps a local state, typically a view of $c$ node descriptors with $c \ll n$, and can send messages to the nodes that it knows. Nodes join through a contact node and may leave or crash at any time ([churn](/churn/)). The views define a directed overlay graph, with an edge from $p$ to $q$ when $q$ is in the view of $p$.

**The uniform ideal.** At any time, a request at node $p$ returns a node $q \ne p$ of $V_t$ with probability $1/(n_t - 1)$, independently of all other requests at $p$ and at other nodes.

**Measures of quality.** No protocol with $c \ll n$ meets the ideal, so the solutions are compared by:

- *bias across nodes:* how far the probability that $q$ is returned is from $1/(n - 1)$. If a request at a uniform node returns a uniform descriptor of its view, then node $q$ is returned with probability $\mathrm{indeg}(q) / (nc)$, where $\mathrm{indeg}(q)$ is the number of views that contain $q$. So the bias is exactly the spread of the in-degrees, and the ideal needs all in-degrees equal to $c$;
- *correlation over time:* how often requests at one node return the same nodes, and how fast the view of a node changes;
- *correlation across nodes:* how much the views of nearby nodes overlap, measured by the [clustering coefficient](/clustering-coefficient/) of the overlay;
- *membership:* how fast a new node appears in views, and how fast the descriptors of crashed nodes disappear;
- *connectivity:* whether the overlay stays connected under churn and large failures;
- *cost:* messages per node per cycle, and their size.

**Random walks.** Let $G$ be the undirected overlay with degrees $d_v$. A simple random walk moves from $i$ to a uniform neighbour. By detailed balance, $d_i \cdot \frac1{d_i} = d_j \cdot \frac1{d_j}$, so its stationary law is $\pi_v = d_v / 2m$, which favours nodes of high degree. The Metropolis-Hastings walk proposes a uniform neighbour $j$ of $i$ and moves to it with probability $\min(1, d_i / d_j)$, and otherwise stays at $i$. For $j \ne i$ its transition probability is

$$P(i, j) = \frac1{d_i} \min\Big(1, \frac{d_i}{d_j}\Big) = \min\Big(\frac1{d_i}, \frac1{d_j}\Big) = P(j, i).$$

A symmetric stochastic matrix is doubly stochastic, so the uniform law is stationary. If $G$ is connected and the walk is aperiodic, for example lazy, the law of the walk after $t$ steps tends to the uniform law, at a rate set by its [mixing time](/mixing-time/).

## Variants

- **Static or dynamic.** In a static network, a random walk of length well above the mixing time gives a sample. In a dynamic network the views must also follow joins and crashes.
- **Many samples or one.** A gossip view gives many samples at once but they are correlated. A walk gives one sample per walk and costs one message per step.
- **Biased sampling.** Some uses want samples proportional to a weight, such as capacity. The Metropolis-Hastings walk with acceptance $\min(1, w_j d_i / (w_i d_j))$ samples in proportion to $w$.
- **Byzantine nodes.** Malicious nodes can push their own descriptors into many views and take over the samples. Protocols for this setting limit how many descriptors one push can insert and mix pushes, pulls and history samples.
- **Locality.** Some systems want samples that are close in latency, not uniform. That is a different goal, served by topology construction protocols.

## Examples

**Bias of a plain walk.** On a graph with 60 nodes, built by preferential attachment with degrees from 2 to 18, the degree-proportional law is at total variation distance 0.286 from uniform. The implementation computes the exact law of a lazy walk from node 0 after $t$ steps:

| $t$ | simple walk, distance to $d_v / 2m$ | Metropolis-Hastings walk, distance to uniform |
|---|---|---|
| 5 | 0.299 | 0.514 |
| 20 | 0.027 | 0.193 |
| 50 | 0.0009 | 0.050 |
| 100 | below $10^{-4}$ | 0.0082 |
| 200 | below $10^{-4}$ | 0.0003 |

The simple walk converges fast, but to the wrong law. The Metropolis-Hastings walk converges to the uniform law, but more slowly, because it often rejects moves into the high degree hubs. After 3 steps the Metropolis-Hastings walk is still at node 0 with probability 0.213, against $1/60 \approx 0.017$ for a uniform sample.

**Bias of a view.** In an overlay where each of $n = 1000$ nodes keeps $c = 20$ descriptors, a node that appears in 40 views is returned twice as often as the ideal, and a node in 5 views a quarter as often. Cyclon keeps the in-degrees close to $c$; Newscast does not (see their pages).

## Known algorithms

| algorithm | idea | bias across nodes | dead descriptors |
|---|---|---|---|
| [Newscast](/newscast/) | push-pull of views with timestamps, keep the freshest | high spread of in-degree | removed quickly |
| [Cyclon](/cyclon/) | swap a few descriptors with the oldest neighbour | small spread of in-degree | removed within about $c$ cycles |
| generic framework of Jelasity et al. | peer selection, view selection with $H$ and $S$, propagation | depends on $S$ | depends on $H$ |
| [SCAMP](/scamp/) | subscriptions forwarded at random, view size about $(c + 1)\ln n$ | moderate | lease and resubscription |
| [lpbcast](/lpbcast/) | membership changes piggybacked on gossip messages | moderate | by unsubscription |
| Metropolis-Hastings walk | random walk with acceptance $\min(1, d_i/d_j)$ | uniform in the limit | the walk must avoid dead links |
| continuous time walk (Massoulié et al.) | stay an Exp($d_v$) time at $v$, stop when a timer runs out | uniform in the limit | as above |

## Bounds

- **Walk length.** A walk sample is only close to uniform after a number of steps of the order of the mixing time of the walk. On an expander overlay this is $O(\log n)$ steps. On a poorly connected overlay it can be much larger, and a short walk stays near its start.
- **Correlation of a fixed view.** Any $c + 1$ samples drawn from one view of size $c$ contain a repeat, so independence fails for more than $c$ samples per refresh (see the [peer sampling service](/peer-sampling-service/)).
- **Cost of fresh samples.** Each fresh walk sample costs one message per step, so $k$ walk samples cost about $k$ times the mixing time in messages, while a gossip view refreshes $c/2$ descriptors with two messages.

## Reductions

- **Gossip to peer sampling.** [Push](/push-gossip/), [pull](/pull-gossip/) and [push-pull gossip](/push-pull-gossip/), [gossip averaging](/gossip-aggregation/) and [probabilistic broadcast](/probabilistic-broadcast/) all call getPeer, and their analyses assume the uniform ideal.
- **Size estimation to sampling.** Sample and collide estimates $n$ from repeats among uniform samples (see [network size estimation](/network-size-estimation/)).
- **Peer sampling to Markov chain sampling.** A walk sampler is a [Markov chain](/markov-chain/) on the overlay whose stationary law is the target law, and [random walk Metropolis](/random-walk-metropolis/) is the general recipe.

## Applications

- **Gossip dissemination and aggregation**, which need a random peer in each round.
- **Overlay construction**, where a random overlay is the start point for structured overlays and for locality based topologies.
- **Measurement** of peer to peer networks, where unbiased samples of peers estimate the distribution of properties such as degree, uptime or files shared.
- **Load balancing**, where tasks go to random peers.

## References
