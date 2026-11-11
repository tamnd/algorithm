---
tag: KNPHFP
kind: problem
slug: membership-management
name: Membership management
aliases:
- group membership by gossip
- partial view maintenance
- gossip membership
area: distributed/gossip
level: advanced
summary: Keep each node's view of the group, full or partial, up to date as nodes join, leave or fail, so that the views form a connected, random-looking overlay for gossip.
prereqs: [peer-sampling-service, failure-detection, churn]
see_also: [peer-sampling-service, random-peer-sampling, scamp, cyclon, newscast, hyparview, lpbcast, swim]
sources:
  - paper: doi:10.1145/1275517.1275520
    title: Márk Jelasity, Spyros Voulgaris, Rachid Guerraoui, Anne-Marie Kermarrec and Maarten van Steen, Gossip-based peer sampling, ACM Transactions on Computer Systems 25(3), 2007
    locator: Sections 2 and 3 (the peer sampling service and the framework of partial view protocols with the view selection, peer selection and propagation policies)
  - paper: "Ayalvadi J. Ganesh, Anne-Marie Kermarrec and Laurent Massoulié, Peer-to-peer membership management for gossip-based protocols, IEEE Transactions on Computers 52(2), 2003"
    locator: the problem of partial view membership for gossip, and the SCAMP protocol with views of mean size (c + 1) log n
  - paper: "David Liben-Nowell, Hari Balakrishnan and David Karger, Analysis of the evolution of peer-to-peer systems, 21st ACM Symposium on Principles of Distributed Computing (PODC), 2002"
    locator: the lower bound of Omega(log n) notifications per node per half-life for staying connected under churn
---

Membership management is the problem of keeping, at every node of a large group, a view of the other members that stays useful while nodes join, leave and crash. A view can list all members, as in [SWIM](/swim/), or only a small *partial view* of a few dozen nodes, as in [SCAMP](/scamp/), [Cyclon](/cyclon/), [Newscast](/newscast/), [HyParView](/hyparview/) and [lpbcast](/lpbcast/). The views together form a directed overlay graph, and a [gossip protocol](/gossip-protocol/) works only if this graph stays connected, has a small diameter and looks random. This page is a map of these protocols and of what they guarantee.

## In plain words

In a big club, nobody can know all members. Each member keeps a short list of names to call when there is news.

The lists must stay good. New members must get on some lists. Members who leave must drop off the lists. Every member must be on about as many lists as the others, so that nobody is forgotten and nobody gets all the calls. The lists must also mix the club well, so that news from any member can reach everyone in a few steps.

Membership management is the set of rules that members follow to keep their lists like this, by talking only to the members on their own lists.

## Definition

There are $n$ nodes, and $n$ changes over time. Each live node $p$ keeps a view $V_p$, a set of node identifiers, possibly with ages or other data. The views define the directed graph with an arc from $p$ to each $q \in V_p$. A membership protocol tells each node how to join, how to leave, and how to update its view by exchanges with nodes in its view. It should keep, under joins, leaves, crashes and message loss:

- **Small views.** $|V_p|$ is $O(\log n)$ or a constant $c$, so that a node needs no global knowledge.
- **Connectivity.** The graph of live nodes stays connected, also after many nodes crash at once.
- **Balance.** In-degrees are close to the mean, so that load and the chance of being reached are the same for all nodes.
- **Randomness.** Views look like uniform random samples of the live nodes, which is the [peer sampling service](/peer-sampling-service/) contract, with the [random peer sampling](/random-peer-sampling/) problem as the ideal.
- **Freshness.** Entries of departed nodes leave the views quickly, and new nodes enter views quickly.

Full membership is the special case $V_p$ = all live nodes. Then the problem is to agree, at least eventually, on the set of live nodes, which needs [failure detection](/failure-detection/) and a way to spread its decisions.

## Variants

- **Full or partial views.** Full views give direct addressing and $O(n)$ state per node; they suit clusters of up to some thousands of nodes. Partial views give $O(\log n)$ or constant state and suit very large or open systems.
- **Reactive or cyclic.** Reactive protocols, like [SCAMP](/scamp/) and the active view of [HyParView](/hyparview/), change views only on joins, leaves and detected failures. Cyclic protocols, like [Cyclon](/cyclon/) and [Newscast](/newscast/), exchange view entries with a peer every cycle, which keeps views random and removes dead entries by ageing.
- **Fixed or growing view size.** Cyclon, Newscast and HyParView use a fixed size. In SCAMP the mean view size grows like $(c + 1) \ln n$ without any node knowing $n$.
- **Membership inside the payload.** In [lpbcast](/lpbcast/), membership data rides on the broadcast messages, so the same gossip both spreads events and updates views.
- **Symmetric views.** HyParView keeps its active view symmetric, so a link is a TCP connection that both ends watch; most others keep directed views.
- **Crash or churn.** Some protocols are tuned for a large crash at one time, others for steady [churn](/churn/).

## Examples

- **SCAMP join.** A new node subscribes at a contact, which forwards the subscription to all nodes in its view and to $c$ extra random ones; each copy is kept with a probability that falls with the view size of the receiver. The expected number of arcs grows by $c + 1$ per join, so the mean view size is $(c + 1) H_n \approx (c + 1) \ln n$. For $n = 1000$ and $c = 1$ this is about 15.
- **Cyclon shuffle.** Every cycle a node picks the oldest entry in its view, sends it a few random entries with a fresh entry for itself, and both nodes swap entries. The in-degree stays close to the view size, and a dead entry is found within at most view-size cycles.
- **HyParView repair.** Each node keeps an active view of 5 and a passive view of 30. When an active neighbour fails, the node promotes a passive entry. In the measurements on the [HyParView](/hyparview/) page with 1000 nodes, after 80 percent of them crashed, all 200 survivors formed one component again after one repair round.
- **SWIM full membership.** Every member probes a random member each period, and joins, suspicions and confirmed failures ride on the probe messages, so every member eventually knows the same live set.

## Known algorithms

| Protocol | View | Main mechanism | Strength |
|---|---|---|---|
| [SCAMP](/scamp/) (Ganesh, Kermarrec, Massoulié 2001) | partial, mean $(c + 1) \ln n$ | probabilistic forwarding of subscriptions, leases | view size adapts to $n$ with no knowledge of $n$ |
| [lpbcast](/lpbcast/) (Eugster et al. 2003) | partial, fixed $l$ | subscriptions and unsubscriptions on the gossip messages | membership at no extra message cost |
| [Newscast](/newscast/) (Jelasity et al.) | partial, fixed $c$ | push-pull exchange, keep the freshest entries | very fresh views, fast removal of dead entries |
| [Cyclon](/cyclon/) (Voulgaris, Gavidia, van Steen 2005) | partial, fixed $c$ | shuffle with the oldest neighbour | balanced in-degrees, low clustering |
| [HyParView](/hyparview/) (Leitão, Pereira, Rodrigues 2007) | active 5, passive 30 | symmetric active view over TCP, passive view by shuffles | survives very large crashes |
| [SWIM](/swim/) (Das, Gupta, Motivala 2002) | full | random probing, suspicion, piggybacked dissemination | constant load per member, used in production |
| Gossip-style heartbeats (van Renesse et al. 1998) | full | gossip of heartbeat counters | simple; load grows with $n$ |

The [peer sampling service](/peer-sampling-service/) page describes the common framework of the cyclic protocols, and its policies for view selection, peer selection and propagation.

## Bounds

- **View size for connectivity.** If each node keeps $k$ uniform random out-neighbours and nodes fail independently, the graph of survivors stays connected with high probability only if $k$ is of order $\log n$, as in the [Erdős-Rényi connectivity threshold](/erdos-renyi-connectivity-threshold/). This is the reason for the $(c + 1) \ln n$ views of SCAMP and for fanouts of order $\ln n$ in [gossip](/gossip-fanout/).
- **Maintenance under churn.** Liben-Nowell, Balakrishnan and Karger show that a system that stays connected must notify each node of $\Omega(\log n)$ other nodes per half-life, see [churn](/churn/).
- **Dead entries.** Under a churn rate $c$ per cycle, an entry of age $A$ points to a departed node with probability about $c A$, so a protocol that bounds entry ages bounds the fraction of dead entries.
- **Full membership load.** Keeping full views needs at least one message about each join or failure at each member, so the total traffic per event is $\Omega(n)$; SWIM attains $O(n)$ messages per event by piggybacking on its probes, spread over $O(\log n)$ periods.

## Reductions

- **Membership from peer sampling.** A [peer sampling service](/peer-sampling-service/) that returns near uniform samples gives a partial view: the view is the last samples. Most partial view protocols are built this way.
- **Membership from failure detection.** Full membership is [failure detection](/failure-detection/) plus dissemination of its decisions, as in SWIM.
- **Broadcast from membership.** [Probabilistic broadcast](/probabilistic-broadcast/), [rumor mongering](/rumor-mongering/), [bimodal multicast](/bimodal-multicast/) and [epidemic broadcast trees](/epidemic-broadcast-tree/) all choose gossip targets from the membership views, and their reliability depends on the connectivity and randomness of the views.

## Applications

- **Cluster managers.** Consul, Nomad and Serf use SWIM through the memberlist library; Cassandra keeps full membership by gossip with a phi accrual detector.
- **Peer-to-peer overlays.** Unstructured overlays use partial views as their neighbour sets, and structured ones like [Chord](/chord/) and [Kademlia](/kademlia/) use gossip membership to bootstrap and to repair routing tables.
- **Gossip broadcast and aggregation.** [Gossip aggregation](/gossip-aggregation/) and [network size estimation](/network-size-estimation/) need random peers from the membership layer in every round.
- **Epidemic dissemination at scale.** Plumtree builds its broadcast tree over the HyParView active view, and uses the passive view to repair it.

## References
