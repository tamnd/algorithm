---
tag: T239X1
kind: concept
slug: churn
name: Churn
aliases:
- node churn
- membership churn
area: distributed/gossip
level: advanced
summary: The continual arrival and departure of nodes in a large distributed system, measured by session lengths and the half-life, which every gossip and overlay protocol must tolerate.
prereqs: [crash-failure, geometric-distribution]
see_also: [membership-management, peer-sampling-service, failure-detection, cyclon, newscast, gossip-aggregation, chord, kademlia]
sources:
  - paper: doi:10.1145/1177080.1177105
    title: Daniel Stutzbach and Reza Rejaie, Understanding churn in peer-to-peer networks, 6th ACM SIGCOMM Conference on Internet Measurement (IMC), 2006
    locator: pages 189 to 202 (measurement of session lengths, uptimes and inter-arrival times in Gnutella, BitTorrent and Kad, the biases of measurement methods, and the fit of session lengths by Weibull and log-normal distributions)
  - paper: "David Liben-Nowell, Hari Balakrishnan and David Karger, Analysis of the evolution of peer-to-peer systems, 21st ACM Symposium on Principles of Distributed Computing (PODC), 2002"
    locator: pages 233 to 242 (the doubling time, the halving time and the half-life, and the lower bound of Omega(log n) notifications per node per half-life for staying connected)
---

Churn is the continual arrival and departure of nodes in a large distributed system, such as a peer-to-peer network or a big cluster, so that the set of members is never fixed. Its rate is described by the distribution of session lengths, the time from a node's arrival to its departure, and by the half-life of Liben-Nowell, Balakrishnan and Karger (2002), the time in which the system replaces half of its members. Every membership, gossip and overlay protocol must repair itself at least as fast as churn breaks it.

## In plain words

Think of a busy train station. People come in and go out all the time, and after an hour most of the people in the hall are new. A list of the people in the hall goes out of date quickly.

In a large computer network, machines join and leave in the same way. Some stay for days, many leave after a few minutes. A machine's list of other machines slowly fills with machines that are gone.

Churn is the name for this coming and going. A system that wants to stay connected must update its lists faster than the lists go out of date.

## The idea

**Sessions.** Each node alternates between online sessions and offline periods. Churn is described by the session length distribution, the uptime distribution of the nodes online at a given moment, and the arrival process. A crash and a planned departure look the same to the other nodes unless the leaver says goodbye, so models of churn treat departures as [crash failures](/crash-failure/) in the worst case.

**Simple model.** Many simulations, including those on the pages of [Newscast](/newscast/), [Cyclon](/cyclon/) and [gossip aggregation](/gossip-aggregation/), replace a fraction $c$ of the nodes in each cycle by new nodes. A node then leaves after a number of cycles that follows a [geometric distribution](/geometric-distribution/) with mean $1/c$, and the group size stays fixed. In continuous time, the same model has exponential session lengths with rate $\lambda$.

**Half-life.** Liben-Nowell, Balakrishnan and Karger define, for a system with $N$ live nodes at time $t$, the *doubling time* as the time from $t$ until $N$ new nodes have arrived, and the *halving time* as the time from $t$ until half of the $N$ nodes live at $t$ have left. The half-life is the smaller of the two, taken over all $t$. In the exponential model with a stable size, nodes arrive at rate $N \lambda$, so the doubling time is $1/\lambda$, and a node is still live after time $s$ with probability $e^{-\lambda s}$, so the halving time is $\ln 2 / \lambda$. The half-life is $\ln 2 / \lambda$, which is $\ln 2$ times the mean session length.

**Lower bound.** Liben-Nowell, Balakrishnan and Karger show that a peer-to-peer system that stays connected with high probability in every half-life must notify every node of $\Omega(\log N)$ other nodes per half-life. Otherwise some node has, with good probability, only neighbours that all leave within the half-life. They show that Chord with a suitable maintenance protocol uses $O(\log^2 N)$ messages per node per half-life, close to the bound.

**What measurements show.** Stutzbach and Rejaie (2006) measured churn in Gnutella, BitTorrent and Kad, with care for the biases of snapshot measurements, which miss short sessions and overweight long ones. They found that session lengths are not exponential: they are better fit by Weibull or log-normal distributions, with many short sessions and a long tail. Nodes that have been up for a long time are more likely to stay, so the set of long-lived nodes is a stable core. A node's past session lengths predict its next session length well.

**Effect on protocols.** A view entry of age $A$ cycles points to a departed node with probability about $1 - (1 - c)^A \approx c A$ in the simple model. So the fraction of dead entries is about $c$ times the mean age of entries, and protocols that keep entries fresh lose fewer of them. Under 1 percent churn per cycle, Newscast keeps about 1.3 percent dead entries because its entries are young, while Cyclon keeps about 10 percent because an entry can stay up to the cache size in cycles. Aggregation protocols lose mass with each departure, so a count under churn drifts during an epoch and must restart often.

## Examples

- **Exponential sessions.** If the mean session is 60 minutes, $\lambda = 1/60$ per minute and the half-life is $60 \ln 2 \approx 42$ minutes. In 42 minutes the system must have repaired itself, and every node must have learned about $\Omega(\log N)$ new nodes.
- **Cycle model.** With $c = 0.01$ per cycle and one exchange per node per cycle, the mean session is 100 cycles and the half-life is about 69 cycles, so a peer sampling service that replaces dead entries within a few cycles keeps up easily.
- **Heavy-tailed sessions.** With a Weibull session law of shape below 1, most sessions are very short, so most departures come from new nodes. A protocol that prefers neighbours with a long uptime, as Kademlia does when it keeps old contacts in its buckets, keeps fewer dead links than one that chooses uniformly.

## Where it is used

- **Peer sampling and membership.** [Peer sampling services](/peer-sampling-service/) and [membership management](/membership-management/) protocols are measured by how many dead entries they keep under churn and how fast they remove them.
- **Failure detection.** Under churn, a [failure detector](/failure-detection/) must tell crashes from departures and must not spend its budget on nodes that already left.
- **Distributed hash tables.** [Chord](/chord/) and [Kademlia](/kademlia/) run stabilization and bucket refresh to keep routing tables correct within a half-life.
- **Aggregation.** [Gossip aggregation](/gossip-aggregation/) restarts in epochs so that churn during one epoch does not spoil the result for long.

## References
