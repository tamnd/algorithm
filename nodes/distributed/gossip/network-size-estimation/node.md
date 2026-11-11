---
tag: RJGWTH
kind: problem
slug: network-size-estimation
name: Network size estimation
aliases:
- gossip counting
- population estimation
area: distributed/gossip
level: advanced
summary: Every node of a decentralized network must estimate the number of nodes n, by gossip or by random walks, without a central counter and while nodes join and leave.
prereqs: [gossip-aggregation, distributed-averaging, markov-chain, stationary-distribution, order-statistic]
see_also: [gossip-aggregation, push-sum, hyperloglog, kmv-sketch, distinct-elements-problem, random-peer-sampling, birthday-paradox, churn]
sources:
  - paper: doi:10.1145/1082469.1082470
    title: Márk Jelasity, Alberto Montresor and Ozalp Babaoglu, Gossip-based aggregation in large dynamic networks, ACM Transactions on Computer Systems 23(3), 2005
    locator: COUNT by push-pull averaging with one leader at value 1, and epochs with restarts
  - paper: "Laurent Massoulié, Erwan Le Merrer, Anne-Marie Kermarrec and Ayalvadi Ganesh, Peer counting and sampling in overlay networks: random walk methods, 25th ACM Symposium on Principles of Distributed Computing (PODC), 2006"
    locator: the Random Tour estimator, the continuous time random walk sampler, and the Sample and Collide estimator C_l^2 / (2 l)
  - paper: "Damon Mosk-Aoyama and Devavrat Shah, Computing separable functions via gossip, 25th ACM Symposium on Principles of Distributed Computing (PODC), 2006"
    locator: sums estimated from the minima of exponential random variables, spread by gossip
  - paper: "Ziv Bar-Yossef, T. S. Jayram, Ravi Kumar, D. Sivakumar and Luca Trevisan, Counting distinct elements in a data stream, RANDOM 2002"
    locator: the estimator from the k-th smallest hash value
  - paper: "Philippe Flajolet, Éric Fusy, Olivier Gandouet and Frédéric Meunier, HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm, Conference on Analysis of Algorithms (AofA), 2007"
    locator: the HyperLogLog estimator and its relative standard error 1.04 / sqrt(m)
---

Network size estimation is the problem in which every node of a decentralized network, such as a peer to peer overlay, must estimate the number of nodes $n$. No node knows the full membership, there is no central counter, and nodes join and leave all the time. The main methods either compute an aggregate whose value depends on $n$, by [gossip aggregation](/gossip-aggregation/), or measure the network with random walks. Typical uses are to set parameters that grow with $n$, such as a [gossip fanout](/gossip-fanout/) of about $\ln n$.

## In plain words

You stand inside a very large crowd and want to know how many people are in it. You cannot see everyone, and people come and go.

One way is to share a small fact with your neighbours again and again. If one person starts with the number one and everyone else with zero, and people keep averaging their numbers in pairs, everyone ends with one divided by the crowd size.

A second way is a lottery. Each person draws a random ticket, and the crowd passes on only the smallest tickets. In a big crowd the smallest tickets are very small, so their size tells how big the crowd is.

A third way is to walk at random and count how often you meet someone you met before. Repeats come sooner in a small crowd than in a big crowd.

## Definition

**Model.** The nodes form a connected undirected overlay graph $G$ with $n$ nodes, $m$ edges and degrees $d_v$. A node knows its own neighbours, and possibly can reach uniform random peers through a [peer sampling service](/peer-sampling-service/). Time is in rounds or cycles. Nodes may crash and join, which is [churn](/churn/).

**Output.** Each node $v$ outputs an estimate $\hat n_v$. An estimator is *unbiased* if $\mathbb{E} \hat n = n$. Its quality is the relative error $|\hat n / n - 1|$, or the relative standard deviation $\sqrt{\mathrm{Var}\, \hat n} / n$. The cost measures are the number of rounds until every node has an estimate, the total number of messages, and the size of each message.

**Unbiased estimators used below.**

*Averaging.* If one node holds $1$ and all other nodes hold $0$, the mean is $1/n$. Any [distributed averaging](/distributed-averaging/) method then gives $\hat n_v = 1/a_v \to n$.

*The $k$-th minimum.* Each node draws $U_v$ uniform on $(0, 1)$, independently. Let $U_{(k)}$ be the $k$-th smallest of the $n$ values, with $k \ge 2$. Then

$$\hat n = \frac{k - 1}{U_{(k)}}, \qquad \mathbb{E} \hat n = n, \qquad \mathrm{Var}\, \hat n = \frac{n (n - k + 1)}{k - 2} \quad (k \ge 3).$$

*Proof.* $U_{(k)}$ has the Beta$(k, n - k + 1)$ density, so $\mathbb{E}[U_{(k)}^{-1}] = B(k - 1, n - k + 1) / B(k, n - k + 1) = n / (k - 1)$, from $B(a - 1, b)/B(a, b) = (a + b - 1)/(a - 1)$. In the same way $\mathbb{E}[U_{(k)}^{-2}] = n(n - 1)/((k - 1)(k - 2))$, and the variance follows. $\square$

So the relative standard deviation is about $1/\sqrt{k - 2}$. The set of the $k$ smallest values is a merge of sets that keeps the $k$ smallest, so gossip spreads it like a maximum.

*Exponential minima.* Each node draws $k$ independent Exp(1) values. The minimum of $n$ independent Exp(1) values is Exp($n$). Let $S$ be the sum of the $k$ coordinate minima, which has the Gamma$(k, n)$ law. Then $\hat n = (k - 1)/S$ has mean $n$ and variance $n^2/(k - 2)$, from $\mathbb{E}[S^{-1}] = n/(k - 1)$ and $\mathbb{E}[S^{-2}] = n^2/((k - 1)(k - 2))$.

*Random tour.* A simple random walk on $G$ starts at node $i$ and stops when it first returns to $i$. It adds $1/d_v$ at every visit, including the start. With $T$ the length of the tour,

$$\hat n = d_i \sum_{t = 0}^{T - 1} \frac{1}{d_{X_t}}, \qquad \mathbb{E} \hat n = n.$$

*Proof.* The walk has the [stationary distribution](/stationary-distribution/) $\pi_v = d_v / 2m$, so the expected return time to $i$ is $1/\pi_i = 2m/d_i$. By the renewal reward argument, the expected sum of $f(X_t)$ over one tour is $(1/\pi_i) \sum_v \pi_v f(v)$. For $f(v) = 1/d_v$ this is $(2m/d_i) \cdot n / 2m = n / d_i$. $\square$

## Variants

- **Static or dynamic.** In a dynamic network the estimate must follow $n$ as it changes. Gossip methods run in epochs and restart (see [gossip aggregation](/gossip-aggregation/)). Random walk methods start a new walk.
- **All nodes or one node.** Gossip methods give an estimate at every node. Random walk methods give an estimate at the node that started the walk, and it must then spread the result.
- **Exact or approximate.** In a static network averaging COUNT converges to $n$ exactly. All other methods have a random error that more effort reduces.
- **Distinct items instead of nodes.** If nodes hold sets of items, the same sketches estimate the number of distinct items in the union. This is the [distinct elements problem](/distinct-elements-problem/) in a distributed setting.

## Examples

All numbers come from the implementation, with fixed seeds.

| Method | Setting | Result |
|---|---|---|
| Averaging COUNT | $n = 1000$, 40 cycles of push-pull | every node within $10^{-3}$ of 1000 |
| $k$-th minimum | $n = 1000$, $k = 20$, 2000 trials | mean 1008.4, standard error 5.3 |
| Exponential minima | $n = 1000$, $k = 20$, 20000 trials | mean 998.4, standard error 1.6 |
| Random tour | $n = 200$, degrees from 3 to 10, 2000 tours | mean 208.1, standard error 6.0 |
| Sample and collide | $n = 2000$, $l = 20$, timer 10, 30 runs | mean 2103 |
| HyperLogLog by gossip | $n = 2000$, $m = 64$ registers, 15 cycles | 2099.5 and 2038.5 for two seeds |

The relative standard deviation of one $k$-th minimum estimate with $k = 20$ is about $1/\sqrt{18} \approx 0.24$, so one run alone is not precise. The averages over many trials show that the estimators have no bias. For HyperLogLog with $m = 64$ the relative standard error is $1.04/8 = 0.13$, and both runs are well inside it. After 15 cycles all nodes hold the same merged sketch, so all nodes report the same value.

Sample and collide with a timer of $0.5$ instead of $10$ gives a mean of about 53 on a graph with 200 nodes. The walk does not mix, the samples stay near the start node, and repeats come too early. The timer must be long compared with the mixing time.

## Known algorithms

| Method | Messages | Rounds | Accuracy | Notes |
|---|---|---|---|---|
| Averaging COUNT (Jelasity, Montresor and Babaoglu 2005) | $2n$ per cycle | $O(\log n + \log \frac1\varepsilon)$ cycles | exact in the limit | a crash early in an epoch loses mass |
| $k$-th minimum by gossip | $2n$ per cycle, $k$ numbers each | $O(\log n)$ cycles | relative deviation $\approx 1/\sqrt{k}$ | merge is idempotent, so duplicates do no harm |
| Exponential minima (Mosk-Aoyama and Shah 2006) | $2n$ per cycle, $k$ numbers each | $O(\log n)$ cycles | relative deviation $\approx 1/\sqrt{k}$ | also gives sums of positive values |
| Random tour (Massoulié et al. 2006) | $2m / d_i$ expected | one walk | unbiased, high variance | no gossip needed |
| Sample and collide (Massoulié et al. 2006) | $\approx \sqrt{2 n l}$ samples, each a walk of length $T$ | sequential | relative deviation $\approx 1/\sqrt{l}$ | needs a mixing sampler |
| HyperLogLog by gossip | $2n$ per cycle, $m$ small registers each | $O(\log n)$ cycles | $1.04/\sqrt{m}$ | merge by register maximum |

**Averaging COUNT.** One node, chosen as leader, starts with 1, and the rest start with 0. Push-pull averaging runs for an epoch, and every node outputs $1/a_v$. Without failures the estimate is exact in the limit. A crash removes the value of the crashed node from the total, so the estimate grows. The crash of the leader in the first cycle loses almost all of the mass. Jelasity, Montresor and Babaoglu run several instances with different leaders and restart in epochs.

**Minimum based sketches.** In the $k$-th minimum method, each node keeps the $k$ smallest values that it has seen, and two nodes in an exchange both keep the $k$ smallest of the union. The merge is idempotent and commutative, so a value that arrives twice changes nothing, and the protocol is as robust as [rumor spreading](/rumor-spreading-problem/). The exponential variant keeps the minimum of each of $k$ coordinates. A crashed node keeps its values in the sketch until the next epoch, so the estimate follows departures only by restart.

**Random tour.** The tour visits on average $2m/d_i$ nodes, which is $\Theta(n)$ messages for bounded degrees, and the estimate has a large variance, so many tours are averaged. The method needs only the neighbour lists.

**Sample and collide.** A continuous time random walk stays at node $v$ for an exponential time with rate $d_v$ and then moves to a uniform neighbour. Its stationary distribution is uniform on the nodes, whatever the degrees. A sample is the node at which a timer of length $T$ runs out. Samples are taken until $l$ of them repeat an earlier sample. If $C_l$ samples were needed, the estimate is $C_l^2 / (2l)$, from the [birthday paradox](/birthday-paradox/): after $C$ uniform samples about $C^2 / (2n)$ pairs collide. The estimate is asymptotically unbiased as $n$ grows. For finite $n$ it is a little high, because a sample can only repeat one of the distinct earlier samples, and by a short calculation the relative bias is about $C_l / (3n)$, which is about 5 percent for $n = 2000$ and $l = 20$.

**HyperLogLog by gossip.** Each node hashes its identifier into a [HyperLogLog](/hyperloglog/) sketch with $m$ registers. The sketch of a union is the register-wise maximum of the sketches, so gossip with UPDATE equal to the register-wise maximum gives every node the sketch of the whole network after $O(\log n)$ cycles. The registers hold small integers, so a message has about $5m$ to $6m$ bits.

## Bounds

- **Time.** Every estimate that depends on all nodes needs information from all nodes to reach the estimating node. In the [random phone call model](/random-phone-call-model/) that takes $\Omega(\log n)$ rounds, and the gossip methods above match it up to constants.
- **Accuracy against message size.** A sketch that can be merged gives a streaming algorithm for distinct elements: feed the items one at a time and merge each into the sketch. So the known streaming lower bound of $\Omega(1/\varepsilon^2)$ bits for relative error $\varepsilon$ with constant probability also bounds the size of any mergeable sketch of the node set. HyperLogLog is close to this bound.
- **Random walks.** A random tour needs $2m/d_i$ steps in expectation, which is $\Theta(n)$ for bounded degree. Sample and collide needs about $\sqrt{2nl}$ samples, each costing a walk whose length depends on the mixing time.

## Reductions

- **Size estimation to averaging.** COUNT is the average of the indicator of one node.
- **Size estimation to distinct elements.** The node identifiers are the items, and gossip computes the sketch of the union.
- **Size estimation to the maximum.** The $k$-th minimum and exponential minima methods reduce to gossip of a minimum, which reduces to [rumor spreading](/rumor-spreading-problem/).
- **Sums to size estimation.** Mosk-Aoyama and Shah draw Exp($y_v$) values at node $v$ for a positive value $y_v$. The minimum is then Exp($\sum_v y_v$), and the same estimator gives the sum.

## Applications

- **Parameters of gossip protocols.** The fanout of [probabilistic broadcast](/probabilistic-broadcast/), the view size of [SCAMP](/scamp/) and the piggyback count of [SWIM](/swim/) grow with $\log n$.
- **Overlay maintenance.** Structured overlays such as [Chord](/chord/) estimate $n$ to size their routing tables.
- **Monitoring** of peer to peer systems, where the number of users is itself the quantity of interest.

## References
