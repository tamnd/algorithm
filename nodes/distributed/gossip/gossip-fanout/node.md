---
tag: A3C4H2
kind: concept
slug: gossip-fanout
name: Gossip fanout
aliases:
- gossip degree
area: distributed/gossip
level: intro
summary: The fanout is the number of peers a node sends a message to. If each node forwards once to ln n + c random peers, all n nodes get it with probability tending to e^(-e^(-c)).
prereqs: [gossip-protocol, erdos-renyi-connectivity-threshold, giant-component]
see_also: [push-gossip, probabilistic-broadcast, bimodal-multicast, erdos-renyi-connectivity-threshold, epidemic-model, epidemic-threshold, lpbcast, peer-sampling-service]
sources:
  - paper: doi:10.1109/TPDS.2003.1189583
    title: Anne-Marie Kermarrec, Laurent Massoulié and Ayalvadi J. Ganesh, Probabilistic reliable dissemination in large-scale systems, IEEE Transactions on Parallel and Distributed Systems 14(3), 248-258, 2003
    locator: Section 2.1 (Algorithm 1, the fanout k), Section 3.1 (Theorem 1, p_n = (log n + c + o(1))/n gives success probability tending to exp(-exp(-c))), Section 3.2 (link and node failures, hierarchical gossip), Section 4.1 (the three regions of atomic broadcast)
  - paper: doi:10.1145/312203.312207
    title: Kenneth P. Birman, Mark Hayden, Oznur Ozkasap, Zhen Xiao, Mihai Budiu and Yaron Minsky, Bimodal multicast, ACM Transactions on Computer Systems 17(2), 41-88, 1999
    locator: Section 3 (the fanout of the gossip rounds), Appendix A (the bimodal delivery distribution as a function of the fanout)
  - paper: doi:10.1145/945506.945507
    title: Patrick Th. Eugster, Rachid Guerraoui, Sidath B. Handurukande, Petr Kouznetsov and Anne-Marie Kermarrec, Lightweight probabilistic broadcast, ACM Transactions on Computer Systems 21(4), 341-374, 2003
    locator: the analysis of lpbcast as a function of the fanout F and the view size l
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1.4 (the parameter k of rumor mongering and the residue s = e^{-m} for traffic m)
---

The fanout of a [gossip protocol](/gossip-protocol/) is the number of peers to which a node sends a message in one gossip step. It sets the trade-off between reliability and cost: each node sends about fanout messages per message spread, and the probability that some node is missed falls as the fanout grows. Kermarrec, Massoulié and Ganesh (2003) showed that there is a sharp threshold at $\ln n$: if each node forwards a new message once, to $\ln n + c$ random peers, the probability that all $n$ nodes receive it tends to $e^{-e^{-c}}$.

## In plain words

When somebody hears a piece of news, they pass it on to a few friends picked at random, and then they are done. The number of friends is the fanout. With a fanout of one, the news is a single chain that soon runs into people who already know, and it stops. With a fanout of two or three, it reaches most people. To reach every single person, the fanout must be about the natural logarithm of the number of people: about 7 for a thousand, about 14 for a million. A little more than that makes success almost certain; a little less makes it unlikely. The change from "some people are missed" to "nobody is missed" is sudden.

## The idea

### Notation and model

| Symbol | Meaning |
|---|---|
| $n$ | the number of nodes |
| $k$ | the fanout: the number of peers a node sends a message to in one step |
| $c$ | $k - \ln n$, the extra fanout above the threshold |
| $\varepsilon$ | the probability that a single message is lost |
| $f$ | the number of crashed nodes; $n' = n - f$ live nodes |
| $\pi$ | the fraction of nodes reached |

The model is asynchronous message passing with independent message loss and crash failures. Each node draws its targets uniformly at random from all nodes, or from a partial view kept by a [peer sampling service](/peer-sampling-service/). There is no round structure: a node forwards when it first receives the message.

### Two meanings of fanout

1. **Infect and die.** A node that receives a message for the first time sends it to $k$ random peers and never again (Algorithm 1 of Kermarrec et al.). The total cost is exactly $k$ messages per node reached, $kn$ at most. This is the meaning in [probabilistic broadcast](/probabilistic-broadcast/) and lpbcast.
2. **Per round.** Each informed node sends to $k$ random peers in every round, as in [push gossip](/push-gossip/) with fanout $k$. The informed set grows by a factor of up to $k + 1$ per round, and the end phase speeds up because an uninformed node is missed by all $k$ pushes of an informed node with probability about $1 - k/n$.

In bimodal multicast and in lpbcast, a node gossips for a bounded number of rounds with fanout $k$ in each, which lies between the two.

### The graph view

With infect and die, the message travels along a random directed graph in which each node has $k$ out-edges to random targets. The nodes reached are exactly the nodes reachable from the source in this graph. So the question "does every node get the message?" is the question "is every node reachable from the source?", a connectivity question about a random graph. Kermarrec et al. analyse the version in which each of the $n(n - 1)$ possible arcs is present independently with probability $p_n$, so that the fanout is binomial with mean $np_n$; their results hold also for a fixed fanout with the same mean.

### The threshold at ln n

**Theorem (Kermarrec, Massoulié and Ganesh 2003, Theorem 1).** In the directed random graph with $p_n = (\ln n + c + o(1))/n$ for a constant $c$, the probability that every node is reachable from the source tends to $e^{-e^{-c}}$ as $n \to \infty$.

The theorem is cited, not proved here. The reason for the double exponential is the same as for the [connectivity threshold of the Erdős-Rényi graph](/erdos-renyi-connectivity-threshold/). The main way to fail is a node with no in-arc from a reached node. A fixed node has in-degree about Poisson with mean $np_n = \ln n + c$, so it has no in-arc with probability about $e^{-\ln n - c} = e^{-c}/n$. The number of such nodes is then about Poisson with mean $e^{-c}$, and the probability that there is none is $e^{-e^{-c}}$. The proof shows that, apart from these isolated nodes, the reached set is everything with probability tending to 1.

| $c$ | $-1$ | $0$ | $1$ | $2$ | $3$ | $5$ |
|---|---|---|---|---|---|---|
| $e^{-e^{-c}}$ | 0.066 | 0.368 | 0.692 | 0.873 | 0.951 | 0.993 |

To reach everybody with probability $1 - \delta$ for a small $\delta$, take $c \approx \ln(1/\delta)$, so a fanout of $\ln n + \ln(1/\delta)$. The cost per node grows like $\ln n$, as for push.

### Constant fanout

With a constant fanout $k > 1$, the message does not reach everybody, but it reaches a fixed fraction $\pi$ of the nodes, the solution in $(0, 1)$ of
$$\pi = 1 - e^{-k\pi}.$$
The reason: a fixed node is not reached if none of its in-neighbors is reached, and it has about a Poisson number of in-neighbors with mean $k$, each reached with probability $\pi$. This is the equation of the [giant component](/giant-component/) of a random graph with mean degree $k$ and of the final size of an [SIR epidemic](/epidemic-model/) with $R_0 = k$. For $k = 2$, $3$ and $5$, $\pi \approx 0.797$, $0.941$ and $0.993$. For $k \le 1$, only $o(n)$ nodes are reached; this is the [epidemic threshold](/epidemic-threshold/).

Kermarrec et al. see three regions in their simulations (Section 4.1). For low fanouts, no broadcast reaches everybody and the fraction reached rises from 0 to almost 1. For intermediate fanouts, almost all nodes are reached in each broadcast, and the share of broadcasts that reach everybody rises from 0 to 1. For high fanouts, almost every broadcast reaches everybody.

### Failures

- **Lost messages.** If each message is lost independently with probability $\varepsilon$, a fanout $k$ acts as a fanout $k(1 - \varepsilon)$. Kermarrec et al. take $p_n = (\ln n + c + o(1))/((1 - \varepsilon)n)$, that is, a fanout of $(\ln n + c)/(1 - \varepsilon)$, and get the same limit $e^{-e^{-c}}$.
- **Crashed nodes.** If $f$ nodes crash and $n' = n - f$ stay up, messages sent to crashed nodes are lost, and the condition is on the live nodes: a fanout of $(n/n')(\ln n' + c)$ gives the limit $e^{-e^{-c}}$ for reaching all live nodes.
- **Hierarchy.** With $N$ clusters of $m$ nodes, an intra-cluster fanout of $\ln m + c_1$ and an inter-cluster fanout of $\ln N + c_2$ links per cluster give success with probability about $e^{-e^{-c_1}}$ inside each cluster and $e^{-e^{-c_2}}$ between clusters (Section 3.2).

## Examples

**Fanout around ln 1000.** With $n = 1000$, $\ln n \approx 6.91$. The push gossip implementation runs infect and die with fanout $k$ and 400 seeds:

| $k$ | $c = k - \ln n$ | $e^{-e^{-c}}$ | all reached, simulated |
|---|---|---|---|
| 6 | $-0.91$ | 0.084 | 0.063 |
| 7 | 0.09 | 0.402 | 0.403 |
| 8 | 1.09 | 0.715 | 0.730 |
| 9 | 2.09 | 0.884 | 0.895 |
| 10 | 3.09 | 0.956 | 0.965 |

The jump from 6% to 97% over a fanout change of 4 is the sharp threshold.

**Constant fanout.** With $n = 1000$ and 300 seeds, the mean fraction reached is 0.798, 0.941 and 0.993 for $k = 2$, 3 and 5, against $\pi = 0.797$, 0.941 and 0.993 from the equation. With a fixed fanout $k \ge 2$, the source itself sends to $k$ distinct nodes, so the spreading never dies out at the start; with a random fanout of mean $k$, it can.

**Rumor mongering.** In [rumor mongering](/rumor-mongering/), the parameter $k$ is a number of useless contacts, not a fanout, but the same trade-off appears: Demers et al. find that the fraction of sites missed is about $e^{-m}$ for a traffic of $m$ messages per site.

## Where it is used

- **Probabilistic broadcast.** lpbcast and the protocols of Eugster et al. choose the fanout from $n$ and the target reliability; see [probabilistic broadcast](/probabilistic-broadcast/) and [lpbcast](/lpbcast/).
- **Bimodal multicast.** The fanout of each gossip round decides whether the delivery distribution is bimodal; see [bimodal multicast](/bimodal-multicast/).
- **Membership.** The size of the partial view in [peer sampling](/peer-sampling-service/) is set to a small multiple of the fanout, so that targets can change between messages; SCAMP builds views of size about $(c + 1)\ln n$ for this reason.
- **Epidemic broadcast trees.** [Plumtree](/epidemic-broadcast-tree/) keeps a gossip overlay of fanout about $\ln n$ as a backup for its tree.

## References
