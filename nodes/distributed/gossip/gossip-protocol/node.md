---
tag: RX1KJ5
kind: concept
slug: gossip-protocol
name: Gossip protocol
aliases:
- epidemic protocol
- epidemic algorithm
area: distributed/gossip
level: intro
summary: A gossip protocol has each process talk, round after round, with a few peers chosen at random. Information then reaches all n processes in O(log n) rounds with a small, even load.
prereqs: [randomized-algorithm, flooding, broadcast-problem]
see_also: [random-phone-call-model, rumor-spreading-problem, push-pull-gossip, anti-entropy, rumor-mongering, epidemic-model, gossip-averaging, peer-sampling-service]
sources:
  - paper: doi:10.1145/41840.41841
    title: Alan Demers, Dan Greene, Carl Hauser, Wes Irish, John Larson, Scott Shenker, Howard Sturgis, Dan Swinehart and Doug Terry, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: Section 1 (direct mail, anti-entropy and rumor mongering; push, pull and push-pull), Section 1.4 (complex epidemics), Section 2 (deletion and death certificates), Section 3 (spatial distributions)
  - paper: doi:10.1145/1317379.1317381
    title: Anne-Marie Kermarrec and Maarten van Steen, Gossiping in distributed systems, ACM SIGOPS Operating Systems Review 41(5), 2-7, 2007
    locator: the general framework of a gossip protocol (peer selection, data exchanged, data processing) and the survey of applications
  - paper: doi:10.1109/SFCS.2000.892324
    title: Richard Karp, Christian Schindelhauer, Scott Shenker and Berthold Vöcking, Randomized rumor spreading, Proceedings of the 41st IEEE Symposium on Foundations of Computer Science (FOCS), 565-574, 2000
    locator: Section 1 (the random phone call model, push and pull), Sections 2 and 3 (push-pull in log3 n + O(log log n) rounds with O(n log log n) transmissions), Section 4 (the lower bound for address-oblivious algorithms)
  - paper: doi:10.1145/1275517.1275520
    title: Márk Jelasity, Spyros Voulgaris, Rachid Guerraoui, Anne-Marie Kermarrec and Maarten van Steen, Gossip-based peer sampling, ACM Transactions on Computer Systems 25(3), 2007
    locator: the peer sampling service and its gossip-based implementations
  - paper: doi:10.1145/312203.312207
    title: Kenneth P. Birman, Mark Hayden, Oznur Ozkasap, Zhen Xiao, Mihai Budiu and Yaron Minsky, Bimodal multicast, ACM Transactions on Computer Systems 17(2), 41-88, 1999
    locator: Section 3 (the protocol), Appendix A (the analysis of the gossip stage)
---

A gossip protocol, also called an epidemic protocol, is a distributed algorithm in which every process repeatedly picks one or a few other processes at random and exchanges information with them. Because the set of informed processes roughly doubles in each round, a piece of information reaches all $n$ processes in $O(\log n)$ rounds, while each process sends only a constant number of messages per round. Gossip replaces the fixed structure of [flooding](/flooding/) or a [spanning tree](/distributed-spanning-tree/) with randomness, which makes it robust to crashes, lost messages and changes in membership. Demers et al. (1987) introduced it for replicated databases, and Karp et al. (2000) gave the standard model for its analysis, the [random phone call model](/random-phone-call-model/).

## In plain words

Think of how a rumor moves through an office. Nobody sends a memo to everyone. Each person who knows the rumor tells one colleague at random, every few minutes. At first one person knows, then two, then four, and soon almost the whole office knows. Nobody has to know who works there, nobody does much work, and if some people are away or some conversations fail, the rumor still gets through by another path.

A gossip protocol does the same with computers. In each round, every computer calls a random partner and the two compare what they know. The same pattern can spread a message, repair copies of a database, compute an average, keep a list of live members, or detect failed machines. It is not exact: a protocol gives a high probability of success, not a certainty, and it sends some messages that turn out to be useless.

## The idea

### Notation and model

| Symbol | Meaning |
|---|---|
| $n$ | the number of processes (nodes) |
| $f$ | the number of processes that crash |
| $m$ | the number of links of the overlay graph, when there is one |
| $D$ | the diameter of the overlay graph |
| $\Delta$ | the maximum degree of the overlay graph |
| $k$ | the fanout: the number of partners a process contacts per round |

The analysis almost always uses synchronous rounds: in each round, every process chooses its partners and the messages of the round arrive before the next round. Real systems run in the [asynchronous model](/asynchronous-model/) with a local timer per process, and the rounds are only approximate. Failures are [crash failures](/crash-failure/) or [crash-recovery](/crash-recovery/), and messages can be lost; gossip is not designed for Byzantine processes. Communication is point to point, and any process can send to any process whose address it knows. On the complete graph, partners are uniform over all processes. On an overlay graph, they are uniform over the neighbors.

### The three design choices

Kermarrec and van Steen (2007) describe a gossip protocol by three choices.

1. **Peer selection.** Which processes a process contacts. The usual choice is uniform at random from all processes, which needs a list of all members. Large systems use a [peer sampling service](/peer-sampling-service/) that keeps a small random view at each process. Some protocols prefer nearby peers (the spatial distributions of Demers et al.) or fixed neighbors in an overlay.
2. **Data exchanged.** What the two processes send. It can be one new message (a rumor), a summary of the whole state (a digest or a [Merkle tree](/merkle-tree/)), a number to be averaged, or a list of peers.
3. **Data processing.** What a process does with what it receives. It can store a new message and forward it later, merge two states and keep the newer entries, replace two values by their mean, or merge two peer lists and keep a random part.

Two more choices complete the design. The *direction* of a contact is [push](/push-gossip/) (the caller sends), [pull](/pull-gossip/) (the caller asks and the callee answers), or [push-pull](/push-pull-gossip/) (both). The *stopping rule* is how a process decides that a message is old: after a fixed number of rounds, after a number of useless contacts as in [rumor mongering](/rumor-mongering/), or never, as in [anti-entropy](/anti-entropy/).

### Why it is fast and why it is robust

Suppose $i$ processes are informed and each pushes to one random partner. While $i$ is small, almost every partner is new, so the number of informed processes about doubles per round, and $\log_2 n$ rounds bring it close to $n$. The last processes are found more slowly by push: [Frieze and Grimmett (1985) and Pittel (1987)](/push-rumor-spreading-time/) proved that push needs $\log_2 n + \ln n + O(1)$ rounds. Pull finishes the last processes much faster, and push-pull needs only $\log_3 n + O(\log \log n)$ rounds (Karp et al. 2000).

The load is even: each process sends a constant number of messages per round, so no process is a bottleneck, unlike the source of a direct broadcast, which sends $n - 1$ messages. Partners are random, so a crashed process or a lost message removes one path out of many, and the protocol keeps working with a slightly higher round count. The price is redundancy: push sends about $n \ln n$ messages in total, while a tree needs $n - 1$, and the guarantees hold [with high probability](/high-probability-bounds/), not always.

### Two families

Demers et al. (1987) named the two families that still organize the area.

- **Simple epidemics** (anti-entropy). Every process takes part in every round and compares its whole state with a random partner. Every update reaches every process with probability 1, but the cost per round is high.
- **Complex epidemics** (rumor mongering). Only processes with a hot update take part, and they stop after some useless contacts. The cost is low, but some processes can miss the update, so the two are combined.

In the language of epidemiology, which the area borrows, a process is susceptible, infective or removed; see [the SIR epidemic model](/epidemic-model/).

### A map of the area

| Goal | Pages |
|---|---|
| Model and analysis | [random phone call model](/random-phone-call-model/), [rumor spreading problem](/rumor-spreading-problem/), [push rumor spreading time](/push-rumor-spreading-time/), [message lower bound](/rumor-spreading-message-lower-bound/), [graph conductance](/graph-conductance/), [conductance bound](/conductance-rumor-spreading-bound/), [epidemic model](/epidemic-model/), [epidemic threshold](/epidemic-threshold/) |
| Spreading one message | [push gossip](/push-gossip/), [pull gossip](/pull-gossip/), [push-pull gossip](/push-pull-gossip/), [gossip fanout](/gossip-fanout/), [rumor mongering](/rumor-mongering/) |
| Broadcast of a stream | [probabilistic broadcast](/probabilistic-broadcast/), [bimodal multicast](/bimodal-multicast/), [lpbcast](/lpbcast/), [epidemic broadcast trees](/epidemic-broadcast-tree/) |
| Replicated state | [anti-entropy](/anti-entropy/), [Scuttlebutt reconciliation](/scuttlebutt-reconciliation/), [death certificates](/death-certificates/) |
| Aggregation | [distributed averaging](/distributed-averaging/), [gossip averaging](/gossip-averaging/), [push-sum](/push-sum/), [gossip aggregation](/gossip-aggregation/), [network size estimation](/network-size-estimation/) |
| Membership and overlays | [peer sampling service](/peer-sampling-service/), [random peer sampling](/random-peer-sampling/), [Newscast](/newscast/), [Cyclon](/cyclon/), [SCAMP](/scamp/), [HyParView](/hyparview/), [membership management](/membership-management/), [churn](/churn/) |
| Failure detection | [failure detection](/failure-detection/), [SWIM](/swim/), [phi accrual failure detector](/phi-accrual-failure-detector/) |

## Examples

**Push, pull and push-pull on 1024 processes.** One process starts with a rumor, and the simulator of the push, pull and push-pull pages runs the random phone call model with seed 7. Under push, the number of informed processes after each round is 1, 2, 4, 8, 16, 31, 60, 115, 215, 370, 577, 754, 889, 973, 1006, 1015, 1021, 1024. The first ten rounds are close to doubling. The last 51 processes take five rounds, because a process that is not yet informed is found only when an informed process happens to call it. The run takes 17 rounds and 7057 messages; $\log_2 1024 + \ln 1024 \approx 16.9$. Under push-pull with the same seed the counts are 1, 3, 10, 34, 94, 256, 585, 928, 1020, 1024: 9 rounds and 5857 rumor transmissions. Under pull the run takes 12 rounds and 3383 transmissions.

**Averaging.** Each process holds a number. In each round, a random pair of processes replaces both of its numbers by their mean. The sum never changes, and every value converges to the mean of all values, at a rate set by the [spectral gap](/spectral-gap/) of the contact graph. This is [gossip averaging](/gossip-averaging/), the same communication pattern with a different data processing step.

**A non-example.** [Flooding](/flooding/) also spreads a message to everybody, but each process sends to all its neighbors once, and the order is fixed by the graph. There is no random choice and no repetition, so it uses $2m$ messages and $D$ rounds, and a single lost message on a bridge stops it. A spanning tree broadcast is cheaper still, with $n - 1$ messages, and more fragile.

## Where it is used

- **Replicated databases.** The Clearinghouse name service at Xerox used anti-entropy and rumor mongering (Demers et al. 1987). Dynamo-style stores repair replicas by anti-entropy with Merkle trees; see [Dynamo-style replication](/dynamo-style-replication/).
- **Membership and failure detection.** Cluster managers spread membership lists and suspicions by gossip; [SWIM](/swim/) is the best known protocol.
- **Reliable broadcast at scale.** [Bimodal multicast](/bimodal-multicast/) repairs an unreliable multicast by gossip. [Plumtree](/epidemic-broadcast-tree/) builds a broadcast tree out of a gossip overlay and repairs it by gossip.
- **Aggregation in sensor and peer-to-peer networks.** Sums, averages, counts and the size of the network are computed by [gossip aggregation](/gossip-aggregation/).
- **Reconciliation of cluster state.** [Scuttlebutt](/scuttlebutt-reconciliation/) spreads per-node key-value state with bounded messages.

## References
