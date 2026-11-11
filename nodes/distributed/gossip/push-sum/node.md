---
tag: X9WP5N
kind: algorithm
slug: push-sum
name: Push-sum protocol
aliases:
- Kempe-Dobra-Gehrke push-sum
area: distributed/gossip
level: advanced
summary: Each node keeps a sum and a weight, pushes half of both to a random node each round, and estimates the average as sum over weight.
solves: [distributed-averaging]
model: synchronous-model
complexity:
  vars: {n: the number of nodes, ε: the relative error, δ: the failure probability}
  time: {rounds: O(log n + log(1/ε) + log(1/δ))}
  space: {extra: O(1)}
properties: {deterministic: false, recursive: false}
prereqs: [distributed-averaging, push-gossip, markov-inequality]
see_also: [gossip-averaging, gossip-aggregation, push-rumor-spreading-time, random-phone-call-model, network-size-estimation, averaging-convergence-spectral-gap]
sources:
  - paper: doi:10.1109/SFCS.2003.1238221
    title: David Kempe, Alin Dobra and Johannes Gehrke, Gossip-based computation of aggregate information, 44th IEEE Symposium on Foundations of Computer Science (FOCS), 2003
    locator: pages 482 to 491; Algorithm 1 (Push-Sum), Section 2 (contributions, the potential function, Lemma 2.3 and Theorem 2.1 on the diffusion speed of uniform gossip), Section 2.4 (practical considerations), Theorem 3.1 (convergence of Push-Sum)
  - paper: doi:10.1109/TIT.2006.874516
    title: Stephen Boyd, Arpita Ghosh, Balaji Prabhakar and Devavrat Shah, Randomized gossip algorithms, IEEE Transactions on Information Theory 52(6), 2006
    locator: pages 2508 to 2530 (two way pairwise averaging, for comparison)
  - paper: "Alan M. Frieze and Geoffrey R. Grimmett, The shortest-path problem for graphs with random arc-lengths, Discrete Applied Mathematics 10(1), 1985"
    locator: Theorem 5.2, as used by Kempe et al. for the push rumor spreading time that bounds the weights from below
---

Push-sum, from Kempe, Dobra and Gehrke (2003), solves [distributed averaging](/distributed-averaging/) with one way messages: each node holds a pair $(s, w)$, and in each round it keeps half of the pair and sends the other half to a node chosen uniformly at random. The ratio $s/w$ at every node converges to the average, and with probability at least $1 - \delta$ every ratio is within relative error $\varepsilon$ after $O(\log n + \log(1/\varepsilon) + \log(1/\delta))$ rounds. The sums and the weights are both conserved, which is what makes the ratio right. Unlike [randomized gossip averaging](/gossip-averaging/), no exchange has to be atomic or two way, and unlike [push-pull aggregation](/gossip-aggregation/), a node never waits for a reply.

## In plain words

Every computer holds a number and a weight, and all weights start at one. In each round, a computer splits both its number and its weight in half. It keeps one half and sends the other half to a computer picked at random. Then it adds up everything that arrived.

Nothing is lost or created, so the total of the numbers and the total of the weights never change. Each computer's best guess of the average is its number divided by its weight. A computer that received many halves has a big number and a big weight, and the division corrects for that.

The halves spread through the network like a rumor, and they get mixed more evenly at each round. After a number of rounds that grows only with the logarithm of the network size, every guess is very close to the true average.

## The problem

There are $n$ nodes, and node $i$ holds $x_i \in \mathbb{R}$. Every node must approximate $\bar x = \frac1n \sum_j x_j$.

**Model.** Computation is in synchronous rounds, in the uniform gossip model: in each round, each node can send messages to any node whose address it knows, and the analysis lets each node choose a target uniformly from all $n$ nodes, itself included, independent of everything else. This is the [random phone call model](/random-phone-call-model/) with push only. There are no failures and no message loss in the analysis. Costs are rounds and messages; a node sends one message per round.

**Output.** At round $t$, node $i$ outputs an estimate $s_{t,i} / w_{t,i}$. The relative error of node $i$ is $|s_{t,i}/w_{t,i} - \bar x| / |\bar x|$.

## The algorithm

```pseudo id=main
PUSH-SUM(x_i)                                 ▷ the code of node i
L1  s ← x_i; w ← 1
L2  for each round t = 0, 1, 2, …
L3      choose a target f uniformly at random from the n nodes
L4      send (s/2, w/2) to f and send (s/2, w/2) to i itself
L5      let (ŝ_r, ŵ_r) be all pairs sent to i in this round
L6      s ← Σ_r ŝ_r; w ← Σ_r ŵ_r
L7      output s / w as the estimate of the average
```

Line L4 to itself is a local step, not a message. Line L5 gets at least one pair, the one that node $i$ sent to itself, so $w > 0$ at every time.

**Theorem 3.1 (Kempe, Dobra and Gehrke 2003).** With probability at least $1 - \delta$, there is a time $t_0 = O(\log n + \log \frac1\varepsilon + \log \frac1\delta)$ such that for all times $t \ge t_0$ and all nodes $i$,

$$\Big| \frac{s_{t,i}}{w_{t,i}} - \frac1n \sum_j x_j \Big| \le \varepsilon \cdot \frac1n \sum_j |x_j|.$$

So the relative error is at most $\varepsilon \sum_j |x_j| / |\sum_j x_j|$, which is $\varepsilon$ when all $x_j$ have the same sign.

## Example

Take $n = 3$ and $x = (6, 0, 0)$, so $\bar x = 2$. The column "targets" lists $f$ for nodes 1, 2 and 3.

| round | targets | $s$ | $w$ | estimates $s/w$ | largest error |
|---|---|---|---|---|---|
| 0 | | (6, 0, 0) | (1, 1, 1) | (6, 0, 0) | 4 |
| 1 | (2, 3, 1) | (3, 3, 0) | (1, 1, 1) | (3, 3, 0) | 2 |
| 2 | (3, 3, 1) | (3/2, 3/2, 3) | (1, 1/2, 3/2) | (3/2, 3, 2) | 1 |
| 3 | (1, 1, 2) | (9/4, 9/4, 3/2) | (5/4, 1, 3/4) | (9/5, 9/4, 2) | 1/4 |
| 4 | (2, 3, 3) | (9/8, 9/4, 21/8) | (5/8, 9/8, 5/4) | (9/5, 2, 21/10) | 1/5 |

In round 2 node 3 gets two pairs and node 2 gets none, so the weights stop being equal. The sums of $s$ stay 6 and the sums of $w$ stay 3 in every row. Node 3's value 3 alone would be a bad estimate, but $3 / \frac32 = 2$ is exact.

## Correctness

The full proof is below. It has five parts.

- **Mass conservation.** Each node splits its pair into two equal halves, and every half is received by exactly one node. So $\sum_i s_{t,i} = \sum_i x_i$ and $\sum_i w_{t,i} = n$ for all $t$.
- **Contributions.** Write $s_{t,i} = \sum_j v_{t,i,j} x_j$, where $v_{t,i}$ is the vector of shares of the inputs at node $i$. The vectors follow the same updates, so $w_{t,i} = \sum_j v_{t,i,j}$, and $s/w$ is a weighted average of the inputs with weights $v_{t,i,j} / w_{t,i}$.
- **Potential.** Let $\Phi_t = \sum_{i,j} (v_{t,i,j} - w_{t,i}/n)^2$. Then $\Phi_0 = n - 1$ and $\mathbb{E}[\Phi_{t+1} \mid \Phi_t] = (\frac12 - \frac1{4n}) \Phi_t$, because the cross terms cancel by mass conservation. So $\mathbb{E}[\Phi_t] \le (n-1) 2^{-t}$.
- **Weights.** In each round a node passes at least half of its weight to itself and half to its target. Following the push rumor from the heaviest node, all weights are at least $2^{-\tau}$ after $\tau$ rounds, where $\tau$ is a bound on the [push rumor spreading time](/push-rumor-spreading-time/).
- **Ratios.** $|v_{t,i,j}/w_{t,i} - 1/n| \le 2^{\tau} \sqrt{\Phi_t}$. [Markov's inequality](/markov-inequality/) and a union bound give the theorem at one time $t$. Each new ratio vector is a convex combination of old ones, so the largest error never grows after that.

Kempe et al. prove in their Lemma 2.3 that the potential drops to less than half in expectation; the exact factor for targets drawn from all $n$ nodes is $\frac12 - \frac1{4n}$.

## Complexity

- **Rounds.** $O(\log n + \log(1/\varepsilon) + \log(1/\delta))$ with probability at least $1 - \delta$. The proof below gives the explicit value $t = 3\log_2 n + 2\log_2(1/\varepsilon) + \log_2(2/\delta) + 2\tau$ with $\tau = 4\log_2 n + \log_2(2/\delta)$, the choice of Kempe et al.
- **Messages.** One message of two numbers per node per round, so $n$ messages per round.
- **Message size.** Kempe et al. show that messages at round $t$ need $O(t + \max_j \mathrm{bits}(x_j))$ bits with exact arithmetic, because each round halves the shares.
- **Local space.** Two numbers per node.

The explicit bound is loose. Over 30 seeded runs with inputs uniform in $[0, 100]$, the mean number of rounds until every node has relative error at most $\varepsilon$ was:

| $n$ | $\varepsilon = 10^{-2}$ | $\varepsilon = 10^{-4}$ | explicit bound, $\varepsilon = 10^{-4}$, $\delta = 0.1$ |
|---|---|---|---|
| 16 | 15.3 | 26.2 | 85 |
| 64 | 16.8 | 29.6 | 107 |
| 256 | 18.8 | 31.7 | 129 |
| 1024 | 20.1 | 32.8 | 151 |

Each factor 4 in $n$ adds about 2 rounds, and each factor 100 in $1/\varepsilon$ adds about 13 rounds, which fits $\log_2 n + \log_2(1/\varepsilon)$ with small constants.

## Properties

- **Randomized.** The only random choice is the target in line L3.
- **One way.** No node waits for a reply, and no exchange must be atomic. A message can arrive in the next round in any order.
- **Exact invariant.** Mass conservation holds in every run, not only in expectation.
- **Monotone error.** The largest distance of an estimate from $\bar x$ never increases.
- **Generic.** The same rule computes any linear aggregate: start with $w_i = 1$ at one node and $0$ elsewhere to get sums, or with $w_i = 1$ only at nodes that match a predicate.

## Variants and improvements

- **Sums and counts.** With $w = 1$ at one node and $w = 0$ at the others, $s/w$ converges to $\sum_j x_j$ at every node. With $x_j = 1$ everywhere and that weight rule, it gives $n$, as in [network size estimation](/network-size-estimation/).
- **Push-vector.** Each node sends a vector of shares in place of one number. Kempe et al. use it to analyse the protocol and to build sketches, sampling and quantile computation on top of push-sum.
- **Other graphs.** On a general graph a node sends to a random neighbour. Kempe et al. relate the speed to the mixing of the random walk; the ratio is still exact in the limit, because only column sums of the matrix matter.
- **Asynchronous use.** Kempe et al. note that nodes can follow their own clocks and that a query can start at one node and spread; mass is still conserved, but the speed analysis changes.
- **Push-pull averaging.** If two nodes can exchange atomically, both can keep the mean, which halves the variance faster; this is [gossip aggregation](/gossip-aggregation/).

## When to use it

Use push-sum when messages are one way or replies are costly, for example over datagrams, when the network lets any node reach a random node, and when an approximate average or sum is enough. It is the standard choice in analyses of aggregation in the uniform gossip model. If links can lose messages, add acknowledgements or resend lost halves to the sender, because a lost message removes mass.

## Pitfalls

- **Lost messages bias the result.** A lost pair removes part of the total $s$ and $w$, and the estimates converge to a ratio of what is left, not to $\bar x$. A crashed node takes its mass with it in the same way.
- **Reading $s$ alone.** The estimate is $s/w$. Before the weights mix, $s$ alone can be far from $\bar x$, as node 3 in round 2 of the example shows.
- **Mixed signs.** The guarantee is relative to $\frac1n\sum_j |x_j|$. If the inputs nearly cancel, the relative error to $\bar x$ itself can be large.
- **Floating point.** Shares halve every round, so after many rounds tiny values lose precision. This matters only for very long runs; use exact arithmetic or restart.
- **Skipping the self half.** If a node sends all of its mass away, a node with no incoming message has $w = 0$ and no estimate.

## Implementations

## History

Kempe, Dobra and Gehrke presented push-sum at FOCS 2003, with the potential function proof and with push-vector protocols for sums, random samples and quantiles. The bound on the weights uses the push rumor spreading time of Frieze and Grimmett (1985). Boyd, Ghosh, Prabhakar and Shah (2006) analysed the two way, pairwise version on arbitrary graphs.

## References
