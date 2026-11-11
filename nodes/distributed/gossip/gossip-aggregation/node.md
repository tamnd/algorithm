---
tag: 2FN2GA
kind: problem
slug: gossip-aggregation
name: Gossip-based aggregation
aliases:
- gossip aggregate computation
area: distributed/gossip
level: advanced
summary: Every node of a large dynamic network must learn an aggregate of all node values, such as the mean, the maximum or the network size, by gossip with random peers.
prereqs: [distributed-averaging, gossip-protocol, push-pull-gossip, peer-sampling-service]
see_also: [distributed-averaging, gossip-averaging, push-sum, network-size-estimation, peer-sampling-service, push-pull-gossip, churn, anti-entropy]
sources:
  - paper: doi:10.1145/1082469.1082470
    title: Márk Jelasity, Alberto Montresor and Ozalp Babaoglu, Gossip-based aggregation in large dynamic networks, ACM Transactions on Computer Systems 23(3), 2005
    locator: pages 219 to 252 (the push-pull averaging protocol, the pair selectors GETPAIR_PM, GETPAIR_RAND and GETPAIR_DISTR, the convergence factor E(2^-phi), epochs and restarts, COUNT by a leader with value 1, and derived aggregates)
  - paper: doi:10.1109/SFCS.2003.1238221
    title: David Kempe, Alin Dobra and Johannes Gehrke, Gossip-based computation of aggregate information, 44th IEEE Symposium on Foundations of Computer Science (FOCS), 2003
    locator: push-sum for sums and averages, and the reduction of other aggregates to sums
---

Gossip-based aggregation is the problem in which every node of a large network holds a value and every node must learn a global function of all values, such as the mean, the sum, the maximum or the number of nodes, by repeated exchanges with random peers. There is no central server and no spanning tree, and nodes may join, leave or crash while the computation runs. The standard solution, by Jelasity, Montresor and Babaoglu (2005), is push-pull averaging over a [peer sampling service](/peer-sampling-service/): in each exchange two nodes replace their values by the mean of the two. With a uniform random peer, the variance of the values falls by a factor of about $1/(2\sqrt e) \approx 0.303$ in each cycle.

## In plain words

Imagine a hall with thousands of people. Each person holds a number on a card. Everyone wants to know the average of all the cards, but nobody can see the whole hall.

At each bell, every person walks up to one random other person. The two compare cards, and both write the average of their two numbers on their cards. The total of all cards does not change, but the cards become more alike. After a few dozen bells, every card shows almost the same number, and that number is the average.

The same idea gives other answers. To find the largest number, the two people both keep the larger card. To count the people in the hall, one person starts with a one and all others start with a zero. The average then becomes one divided by the number of people.

## Definition

**Model.** There are $n$ nodes, and $n$ is large and unknown. Each node can reach a peer chosen by a [peer sampling service](/peer-sampling-service/), which in the ideal case returns a uniform random live node. Time is divided into cycles of equal length $\delta$. Nodes may crash and new nodes may join at any time, which is [churn](/churn/). Messages may be lost.

**Input and output.** Node $i$ holds a value $x_i$. For a fixed aggregate function $F$, every node must keep an estimate $\hat F_i$ that is close to $F(x_1, \ldots, x_n)$ for the current set of nodes, and the estimate must follow the true value when the values or the membership change. The quality measures are the number of cycles to reach a given accuracy, the number of messages per node per cycle, and the error under churn and message loss.

**Push-pull averaging.** Every node keeps a current value $a_i$, which starts at $x_i$. An exchange between nodes $i$ and $j$ is atomic and sets

$$a_i, a_j \leftarrow \mathrm{UPDATE}(a_i, a_j),$$

where $\mathrm{UPDATE}(a, b) = (a + b)/2$ for the mean. The exchange keeps $\sum_i a_i$, so the mean of the $a_i$ stays $\bar x$. A cycle is a sequence of exchanges, and a pair selector GETPAIR chooses the pairs. Let $\sigma_k^2$ be the empirical variance of the values after cycle $k$. The *convergence factor* is $\rho = \mathbb{E}(\sigma_{k+1}^2) / \mathbb{E}(\sigma_k^2)$.

**Theorem (Jelasity, Montresor and Babaoglu 2005).** Suppose that the two values chosen by each call of GETPAIR are uncorrelated random variables. Let $\phi$ be the number of exchanges in which a fixed node takes part during one cycle. Then

$$\rho = \mathbb{E}\big(2^{-\phi}\big).$$

*Why the formula holds.* An exchange replaces two uncorrelated deviations $e$ and $e'$ from the mean by their average, whose expected square is $(\mathbb{E} e^2 + \mathbb{E} e'^2)/4$. Each exchange that a node takes part in therefore halves the share of the old variance that the node carries, and averaging over the random number of exchanges gives $\mathbb{E}(2^{-\phi})$.

The three pair selectors of the paper give three values of $\phi$. The probability generating function of a Poisson variable with mean $\lambda$ is $\mathbb{E} z^X = e^{\lambda(z - 1)}$, so for $z = \frac12$ it is $e^{-\lambda/2}$.

| Selector | Pairs in one cycle | $\phi$ for large $n$ | $\rho = \mathbb{E}(2^{-\phi})$ |
|---|---|---|---|
| GETPAIR_PM | two random perfect matchings | exactly 2 | $1/4$ |
| GETPAIR_RAND | $n$ uniform random pairs | Poisson with mean 2 | $1/e \approx 0.368$ |
| GETPAIR_DISTR | each node starts one exchange with a uniform peer | $1 +$ Poisson with mean 1 | $1/(2\sqrt e) \approx 0.303$ |

GETPAIR_DISTR is the practical protocol: each node runs an active thread that, once per cycle, picks a peer and sends its value, and a passive thread that answers. The assumption of uncorrelated values does not hold exactly, because values that met recently are equal, but for large $n$ the measured factors match the formula (see Examples).

## Variants

- **The aggregate.** With $\mathrm{UPDATE}(a, b) = \max(a, b)$ or $\min(a, b)$ the protocol is [push-pull gossip](/push-pull-gossip/) of the extreme value, and it is exact after $O(\log n)$ cycles. With the mean, it converges only in the limit.
- **Derived aggregates.** The mean of $f(x_i)$ for any function $f$ gives generalized means: the geometric mean is $\exp$ of the mean of $\ln x_i$, and the power mean of order $p$ is the $p$-th root of the mean of $x_i^p$. Two means run side by side give the variance as the mean of $x_i^2$ minus the square of the mean of $x_i$. The sum is the mean times $n$, and the product is the geometric mean to the power $n$, with $n$ from COUNT.
- **COUNT.** One node, the leader, starts with $a = 1$ and all other nodes start with $a = 0$. The mean is $1/n$, so each node estimates the size as $1/a_i$. This is one method of [network size estimation](/network-size-estimation/).
- **Synchronous rounds or asynchronous exchanges.** The analysis treats a cycle as a sequence of atomic exchanges. In a real deployment, cycles of different nodes overlap, and an exchange must be made atomic or its loss must be detected.
- **Push only.** [Push-sum](/push-sum/) needs only one-way messages, at the cost of a weight per node, and has a proof of $O(\log n + \log \frac1\varepsilon + \log \frac1\delta)$ rounds.
- **Fixed graphs.** On a fixed graph with neighbour exchanges, the problem is [distributed averaging](/distributed-averaging/) and its pairwise random version is [randomized gossip averaging](/gossip-averaging/), whose rate is set by a spectral gap.

## Examples

**Four nodes with perfect matchings.** Start with values $(8, 0, 0, 0)$, so the mean is 2 and $\sigma^2 = 16$ (the empirical variance with divisor $n - 1$). The first matching pairs nodes 1 and 2 and nodes 3 and 4: the values become $(4, 4, 0, 0)$. The second matching pairs nodes 1 and 3 and nodes 2 and 4: the values become $(2, 2, 2, 2)$. Here the variance fell to 0 in one cycle, which is better than the expected factor $1/4$, because these two matchings happened to mix the values perfectly.

**Measured factors.** The implementation runs each selector on $n = 10{,}000$ nodes with independent uniform values on $[0, 1)$, for 10 cycles and 3 seeds, and reports the geometric mean of $\sigma_{k+1}^2 / \sigma_k^2$.

| Selector | Measured $\rho$ | Formula |
|---|---|---|
| GETPAIR_PM | 0.2488 | 0.2500 |
| GETPAIR_RAND | 0.3658 | 0.3679 |
| GETPAIR_DISTR | 0.3034 | 0.3033 |

**COUNT with churn.** Start with $5000$ nodes and run epochs of 30 cycles of GETPAIR_DISTR. In each cycle, each member crashes with probability $c$ and takes its value with it, and the same number of new nodes join and wait for the next epoch. The median estimate $1/a_i$ at the end of each of 3 epochs, with seed 1:

| $c$ | Members at the end of each epoch | Median estimate |
|---|---|---|
| 0 | 5000, 5000, 5000 | 5000.00, 5000.00, 5000.00 |
| 0.001 | 4870, 4857, 4814 | 4977, 4983, 4984 |
| 0.01 | 3700, 3708, 3669 | 4850, 4913, 4813 |

Without churn the estimate is exact to six digits. With churn the estimate lies between the size at the start and at the end of the epoch, and the restart at the next epoch removes the error that crashes caused.

## Known algorithms

- **Push-pull averaging** (Jelasity, Montresor and Babaoglu 2005). One exchange per node per cycle with a peer from the [peer sampling service](/peer-sampling-service/), two messages per exchange. The variance falls by about $0.303$ per cycle, so the number of cycles to reduce the standard deviation by a factor $\varepsilon$ is about $\ln(1/\varepsilon) / \ln(\sqrt{2\sqrt e}) \approx 1.68 \ln(1/\varepsilon)$, independent of $n$ once the start variance is fixed.
- **Epochs and restarts.** The protocol is restarted every $\gamma$ cycles with fresh values, and every message carries an epoch number. A node that receives a message of a later epoch drops its state and joins that epoch. A new node waits for the next epoch before it takes part. So the estimate never depends on values older than one epoch, and the error that crashes and losses add is bounded by what happens in one epoch.
- **Several instances.** For COUNT, the crash of the leader early in an epoch loses most of the mass. The paper runs several instances at the same time, with leaders that elect themselves at random with a probability scaled by the previous size estimate, and combines their results.
- **[Push-sum](/push-sum/)** (Kempe, Dobra and Gehrke 2003). Push only, with a pair $(s, w)$ per node. It computes sums and averages, and other aggregates by reduction to sums.
- **Extreme values.** UPDATE equal to max or min, which is rumor spreading of the extreme value.

## Bounds

- **Upper bound for the mean.** By the theorem, after $k$ cycles of GETPAIR_DISTR, $\mathbb{E}\sigma_k^2 \approx (2\sqrt e)^{-k} \sigma_0^2$, under the assumption of uncorrelated pairs. Push-sum has a full proof of $O(\log n + \log \frac1\varepsilon + \log \frac1\delta)$ rounds for relative error $\varepsilon$ with probability $1 - \delta$.
- **Lower bound.** Any aggregate that depends on every input needs at least as many rounds as spreading one value to all nodes. In the [random phone call model](/random-phone-call-model/) that is $\Omega(\log n)$ rounds, because the set of nodes that the value has reached grows by at most a constant factor per round in expectation (see [rumor spreading](/rumor-spreading-problem/)).
- **Messages.** Push-pull averaging sends $2n$ messages per cycle. Each message carries a constant number of values.

## Reductions

- **Mean to sum and count.** The sum is $n \bar x$, so a sum needs both the mean and COUNT. Push-sum avoids COUNT: start with weight 1 at one node and 0 at the others, and the ratio $s/w$ converges to the sum.
- **COUNT to mean.** COUNT is averaging of the indicator of the leader.
- **Maximum to rumor spreading.** Gossip of the maximum, with one node holding 1 and the others 0, is the same process as [push-pull rumor spreading](/push-pull-gossip/).
- **Variance and higher moments to means.** Each moment is the mean of a power of the values, so it costs one more averaging instance.

## Applications

- **Size estimation** of peer to peer networks, used to set parameters that depend on $n$, such as the fanout of [gossip](/gossip-protocol/) or the view size of a [peer sampling service](/peer-sampling-service/).
- **Load balancing**, where each node compares its load with the mean load.
- **Monitoring** of large systems: the mean and the maximum load, the free storage, or the number of nodes that run a given software version.
- **Distributed learning**, where nodes average models or gradients without a parameter server.

## References
