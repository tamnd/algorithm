---
tag: RR48F0
kind: problem
slug: failure-detection
name: Failure detection
aliases:
- crash failure detection
- practical failure detection
area: distributed/gossip
level: core
summary: Decide from heartbeats or probes which processes have crashed, trading detection time against wrong suspicions and message cost, since asynchrony makes some false suspicions unavoidable.
prereqs: [failure-detector, crash-failure]
see_also: [failure-detector, swim, phi-accrual-failure-detector, eventually-perfect-failure-detector, membership-management, churn, partial-synchrony, raft]
sources:
  - paper: doi:10.1109/TC.2002.1004315
    title: Wei Chen, Sam Toueg and Marcos K. Aguilera, On the quality of service of failure detectors, IEEE Transactions on Computers 51(5), 2002
    locator: pages 561 to 580 (the primary metrics detection time, mistake recurrence time and mistake duration, the derived metrics, the detector NFD-S with freshness points, and its configuration from QoS requirements)
  - paper: "Robbert van Renesse, Yaron Minsky and Mark Hayden, A gossip-style failure detection service, IFIP International Conference on Distributed Systems Platforms (Middleware), 1998"
    locator: gossip of heartbeat counters with the timeouts T_fail and T_cleanup
  - paper: "Indranil Gupta, Tushar D. Chandra and Germán S. Goldszmidt, On scalable and efficient distributed failure detectors, ACM Symposium on Principles of Distributed Computing (PODC), 2001"
    locator: the lower bound on network load for a given detection time and false positive rate in a group of n processes
---

Failure detection is the problem of deciding, at each process, which other processes have crashed, from the messages that they send or fail to send. In an asynchronous system a slow process cannot be told apart from a crashed one, so every practical detector makes some wrong suspicions, and the task is to balance three costs: how fast a crash is detected, how often and how long a live process is wrongly suspected, and how many messages the detector sends. Chen, Toueg and Aguilera (2002) gave the standard metrics for this balance. The abstract classes of detectors used in consensus are on the page [failure detector](/failure-detector/); this page is about building and tuning real ones.

## In plain words

You call a friend every day at noon. One day the friend does not answer. Maybe the friend is ill, maybe the phone line is bad, maybe the friend is just busy. You cannot know for sure.

You still have to decide when to start worrying. If you worry after five minutes, you find real trouble fast, but you often worry for nothing. If you wait a whole day, you rarely worry for nothing, but real trouble waits a long time. Calling more often helps, but costs more calls.

A failure detector makes this choice for computers. It watches regular messages from other computers and decides when to say: that one has probably stopped.

## Definition

A monitor $p$ watches a process $q$. At each time, the detector at $p$ outputs *trust* or *suspect* for $q$. Process $q$ may crash at some time and then takes no more steps; messages may be delayed or lost. The detector should satisfy, at least eventually:

- **Completeness.** If $q$ crashes, $p$ eventually suspects $q$ forever.
- **Accuracy.** If $q$ does not crash, $p$ does not suspect it, or suspects it only rarely and briefly.

Chen, Toueg and Aguilera measure the quality of service with three primary metrics, all random variables over a run:

- **Detection time $T_D$.** The time from the crash of $q$ until $p$ starts to suspect $q$ forever.
- **Mistake recurrence time $T_{MR}$.** The time between two consecutive wrong suspicions of a live $q$, from the start of one to the start of the next.
- **Mistake duration $T_M$.** The time it takes to correct a wrong suspicion.

Derived metrics follow from these: the average mistake rate $\lambda_M = 1 / \mathbb{E}[T_{MR}]$; the good period duration $T_G$, from the end of one mistake to the start of the next, with $\mathbb{E}[T_{MR}] = \mathbb{E}[T_M] + \mathbb{E}[T_G]$; and the query accuracy probability $P_A = 1 - \mathbb{E}[T_M] / \mathbb{E}[T_{MR}]$, the probability that the output is right at a random time while $q$ is live. A requirement is then an upper bound on $T_D$, a lower bound on $T_{MR}$ and an upper bound on $T_M$, and the detector must meet it with the least message rate.

## Variants

- **Heartbeats (push).** $q$ sends a message every $\eta$ time units, and $p$ suspects $q$ when a heartbeat is late by more than a timeout.
- **Probes (pull).** $p$ pings $q$ and waits for an answer. This lets $p$ choose whom to check, as in [SWIM](/swim/), and gives a direct round trip measure.
- **Fixed or adaptive timeouts.** A fixed timeout is simple but does not follow changes of the delay. Adaptive detectors estimate the next arrival time from recent arrivals and add a safety margin.
- **Binary or accrual output.** An accrual detector outputs a suspicion level instead of trust or suspect, and each application chooses its own threshold, as in the [phi accrual failure detector](/phi-accrual-failure-detector/).
- **One monitor or a group.** In a group of $n$ processes, all-to-all heartbeats cost $\Theta(n^2)$ messages per period. Gossip of heartbeat counters and random probing reduce the cost per process to a constant or $O(\log n)$.
- **Crash-stop or crash-recovery.** If processes can recover, the detector must also tell an old suspicion from a new incarnation, for example with incarnation numbers.

## Examples

**Freshness points.** In the NFD-S detector of Chen, Toueg and Aguilera, with synchronized clocks, $q$ sends heartbeat $m_i$ at time $\sigma_i = i \eta$. The monitor sets freshness points $\tau_i = \sigma_i + \delta$, and during $[\tau_i, \tau_{i+1})$ it trusts $q$ only if it has received some $m_j$ with $j \ge i$. If $q$ crashes after sending $m_i$, it is suspected forever from $\tau_{i+1}$ on, so $T_D \le \eta + \delta$.

**A rough tuning.** Take $\eta = 1$ s and $\delta = 0.5$ s, with loss probability 0.01 and a delay above 0.5 s in 0.1 percent of the messages. When $\delta \le \eta$, a suspicion starts at $\tau_i$ when $m_i$ is lost or late, probability $p \approx 0.011$, after a trusted period, probability about $1 - p$. So about $p(1 - p) \approx 0.0109$ of the freshness points start a mistake, $\mathbb{E}[T_{MR}] \approx 92$ s, and a mistake lasts about one period, until a later heartbeat arrives. The detection time is at most 1.5 s. Doubling $\delta$ to 1 s, when it is above the delay tail, removes the late messages from $p$ but not the losses, and raises $T_D$ to 2 s.

**Gossip-style detection.** In the service of van Renesse, Minsky and Hayden (1998), every member keeps a table of heartbeat counters for all members, increases its own counter, and gossips the table to a random member. A member whose counter has not increased for $T_{fail}$ is suspected, and its entry is removed after $T_{cleanup}$.

**Random probing.** [SWIM](/swim/) pings one random member per period and asks $k$ others to ping it if the direct ping fails. The expected time until some member probes a crashed one is $e / (e - 1)$ periods, whatever the group size.

## Known algorithms

| Detector | Idea | Main parameters |
|---|---|---|
| Fixed timeout | suspect after a fixed silence | heartbeat period, timeout |
| NFD-S, NFD-E (Chen, Toueg, Aguilera 2002) | freshness points, with estimated arrival times when clocks are not synchronized | $\eta$, $\delta$ or a safety margin $\alpha$ |
| Bertier, Marin and Sens (2002) | Chen's estimate plus a dynamic margin like the TCP round trip estimator | gain factors |
| [Phi accrual](/phi-accrual-failure-detector/) (Hayashibara et al. 2004) | suspicion level $-\log_{10}$ of the late probability | window, threshold $\Phi$ |
| Gossip-style (van Renesse et al. 1998) | gossip of heartbeat counters | gossip period, $T_{fail}$, $T_{cleanup}$ |
| [SWIM](/swim/) (Das, Gupta, Motivala 2002) | random ping and indirect ping, suspicion | period, $k$, suspicion timeout |

## Bounds

- **No perfect detector in asynchrony.** Without bounds on delays, no detector can be both complete and always accurate; that would decide the crash of a slow process, against [FLP impossibility](/flp-impossibility/). Practical detectors are eventually accurate only under [partial synchrony](/partial-synchrony/), which makes them [eventually perfect](/eventually-perfect-failure-detector/).
- **Detection time.** With heartbeats every $\eta$ and a delay that can reach $d$, a detector that never suspects a live process in a synchronous period needs a detection time of at least about $\eta + d$ in the worst case; the period sets the floor.
- **Optimality of NFD-S.** Chen, Toueg and Aguilera show that, in their probabilistic model and among detectors that send heartbeats at the same rate and meet the same detection time bound, NFD-S gives the best query accuracy probability.
- **Load in a group.** Gupta, Chandra and Goldszmidt (2001) give a lower bound on the network load of any detector for a group of $n$ processes in terms of the detection time and the false positive probability, and show that all-to-all and gossip heartbeating are far from it as $n$ grows, while randomized probing is within a constant factor.

## Reductions

- **Consensus.** Failure detectors are the oracles that make consensus solvable in asynchronous systems: the [eventually perfect](/eventually-perfect-failure-detector/) class suffices for [Chandra-Toueg consensus](/chandra-toueg-consensus/), and [Omega](/omega-failure-detector/) is the [weakest for consensus](/weakest-failure-detector-consensus/). An eventually accurate practical detector gives Omega by electing the smallest trusted process.
- **Membership.** A membership service is a failure detector plus a way to spread its decisions; [SWIM](/swim/) is built this way, and see [membership management](/membership-management/).
- **Leader leases.** The election timeout of [Raft](/raft/) and the leader leases of [Paxos](/paxos/) systems are heartbeat failure detectors of the leader.

## Applications

- **Cluster membership.** Consul and Nomad (through Serf and memberlist) use SWIM; Cassandra and Akka use phi accrual detectors over gossip or heartbeats.
- **Consensus and replication.** Raft and Paxos based systems detect a failed leader by missed heartbeats and start an election.
- **Peer-to-peer systems.** Under [churn](/churn/), overlays detect departed neighbours by failed contacts or timeouts, often as part of the membership protocol.
- **Cloud monitoring.** Health checks of load balancers and orchestrators are pull detectors with fixed timeouts and a number of failed checks before a node is removed.

## References
