---
tag: 7NBZ21
kind: algorithm
slug: swim
name: SWIM
aliases:
- Scalable Weakly-consistent Infection-style process group Membership
- SWIM protocol
- Scalable Weakly-consistent Infection-style Process Group Membership Protocol
area: distributed/gossip
level: advanced
summary: Membership protocol that probes one random member per period, directly and through k others, and spreads joins, suspicions and failures by piggybacking them on its own probe messages.
solves: [failure-detection, membership-management]
model: asynchronous-model
complexity:
  vars: {n: the number of members, k: the number of indirect probes}
  rounds: {expected: O(log n)}
  space: {extra: O(n)}
properties: {deterministic: false, recursive: false}
prereqs: [failure-detection, gossip-protocol, crash-failure]
see_also: [failure-detection, phi-accrual-failure-detector, failure-detector, membership-management, gossip-protocol, rumor-mongering, churn, hyparview]
sources:
  - paper: doi:10.1109/DSN.2002.1028914
    title: Abhinandan Das, Indranil Gupta and Ashish Motivala, SWIM, scalable weakly-consistent infection-style process group membership protocol, International Conference on Dependable Systems and Networks (DSN), 2002
    locator: Section 3.1 (ping, ping-req and the expected first detection time e/(e - 1) periods), Section 4.1 (infection-style dissemination by piggybacking, lambda log n retransmissions), Section 4.2 (suspicion with Alive, Suspect and Confirm and incarnation numbers), Section 4.3 (round-robin probe order, at most 2n - 1 periods), Section 5 (evaluation)
  - paper: "Indranil Gupta, Tushar D. Chandra and Germán S. Goldszmidt, On scalable and efficient distributed failure detectors, ACM Symposium on Principles of Distributed Computing (PODC), 2001"
    locator: the scale-independent detection time and false positive rate that SWIM's detector is built to meet
  - paper: "Armon Dadgar, James Phillips and Jon Currey, Lifeguard: local health awareness for more accurate failure detection, arXiv:1707.00788, 2018"
    locator: the extensions of SWIM in HashiCorp memberlist (local health multiplier, dynamic suspicion timeout, buddy system)
---

SWIM (Scalable Weakly-consistent Infection-style process group Membership) is a membership protocol, from Das, Gupta and Motivala (2002), that splits the job into a failure detector and a dissemination component. Once per protocol period each member pings one target; if no ack comes, it asks $k$ other members to ping the target for it. Membership changes do not use extra messages: they ride on the pings and acks, each change for about $\lambda \log n$ messages, so they spread like an epidemic. A suspicion step with incarnation numbers lets a slow but live member refute a false accusation, and a round-robin probe order bounds the time until every member probes a crashed one.

## In plain words

Each member of a group keeps a list of all members. Once every second or so, it calls one of them and asks: are you there? If the answer does not come, it asks a few other members to try the same call. A member that answers through any of them is fine.

If nobody gets an answer, the member is not declared dead at once. It is first marked as suspected, and this news travels to the others. If the suspected member hears it, it says: I am still here, and this is my newer version number. If no such answer comes in time, the member is declared dead.

All this news travels as small notes stuck onto the calls that members make anyway, so the group needs no extra messages.

## The problem

A [failure detector](/failure-detector/) that has every member send heartbeats to every other member costs $O(n^2)$ messages per period, and a detector that sends all heartbeats to a few central members makes those members a bottleneck. [Failure detection](/failure-detection/) in a large group should have a detection time and a false positive rate that do not grow with $n$, a constant message load per member, and a way to tell every member about each change. See [membership management](/membership-management/).

## The algorithm

Each member $M_i$ keeps a list of members with a state (Alive, Suspect or Faulty) and an incarnation number for each, and a buffer of recent updates. The protocol period $T'$ is at least three round trip times. Each update is sent at most $\lambda \log n$ times.

```pseudo id=main
SWIM-PERIOD(M_i), once per period T'
L1  M_j ← the next member in the probe list of M_i
L2  send ping to M_j; if an ack comes back within the timeout, stop
L3  send ping-req(M_j) to k random members; each of them pings M_j and relays the ack to M_i
L4  if no ack has come by the end of the period: disseminate Suspect(M_j, inc_j) (basic SWIM: declare M_j faulty at once)
ON-UPDATE(u) at M_i
L5  if u is Suspect(M_i, inc) about M_i itself: inc_i ← inc + 1 and disseminate Alive(M_i, inc_i)
L6  else apply u if it overrides the current entry: Confirm overrides all; Alive(j, a) overrides Suspect(j, b) and Alive(j, b) when a > b; Suspect(j, a) overrides Suspect(j, b) when a > b and Alive(j, b) when a ≥ b
L7  when a Suspect entry is older than the suspicion timeout, it becomes Confirm(M_j), which is disseminated
DISSEMINATION
L8  every ping, ping-req and ack carries a few updates from the buffer, those sent the fewest times first; an update leaves the buffer after λ log n sends
L9  the probe list is a random permutation of the members; at its end it is shuffled again, and a new member is put at a random place
```

A member joins by contacting a known member, and its Alive update is disseminated like any other. A member that leaves on purpose disseminates its own departure.

## Example

**Why $e/(e - 1)$.** Suppose each of the $n - 1$ live members picks its target uniformly among its $n - 1$ others. A crashed member $M$ is missed by one member with probability $1 - 1/(n - 1)$, so it is missed by all of them in a period with probability

$$\left(1 - \frac{1}{n - 1}\right)^{n - 1} \longrightarrow e^{-1}.$$

The period of first detection is geometric with success probability $p = 1 - (1 - 1/(n - 1))^{n - 1}$, so its mean is $1/p$, which tends to $1/(1 - e^{-1}) = e/(e - 1) \approx 1.582$ periods. If only a fraction $q_f$ of members is live, the success probability is about $1 - e^{-q_f}$, so the detection time is still independent of $n$. Das, Gupta and Motivala measured first detection times that match this value in their prototype.

**Simulation.** With 30 members and no message loss, 800 crashes gave a mean first detection of 1.590 periods with uniform targets and 1.568 periods with the round-robin order, against $1/p = 1.566$ for $n = 30$. With 20 members and the round-robin order, every live member probed the crashed member within 35 periods, below the bound $2n - 1 = 39$.

**False positives under loss.** A probe of a live member fails if the ping or its ack is lost, probability $1 - q^2$ when each message arrives with probability $q$, and all $k$ indirect paths fail, each with probability $1 - q^4$. With $q = 0.95$ and $k = 3$ that is $0.0975 \times 0.1855^3 \approx 6 \times 10^{-4}$ per probe. Eight runs of 40 members for 200 periods each:

| loss | basic SWIM, false Faulty entries | with suspicion, false suspicions | with suspicion, false Faulty entries |
|---|---|---|---|
| 3 % | 234 | 7 | 0 |
| 5 % | 1138 | 29 | 0 |
| 8 % | 7732 | 212 | 117 |

A false Faulty entry counts every member that marks a live member faulty, so one false failure that reaches the whole group counts about 39. With suspicion, every false suspicion at 3 and 5 percent loss was refuted before the timeout of 7 periods. At 8 percent loss the refutation sometimes came too late; a longer timeout trades detection time for accuracy.

## Correctness

The proved claims are: with uniform targets and no loss, the expected first detection time is $1/(1 - (1 - 1/(n - 1))^{n - 1})$ periods, which tends to $e/(e - 1)$; with the round-robin order, every live member probes a crashed member within $2n - 1$ periods; a crashed member is never refuted, so with reliable delivery of updates it is eventually confirmed by everyone (completeness); and a live member that learns of its own suspicion produces an Alive update that overrides the suspicion at every member that receives it. The full proof is below.

Accuracy is probabilistic. A live member can be confirmed faulty if its refutation does not reach a suspecting member before the timeout, as the table shows at 8 percent loss.

## Complexity

- **Detection time.** $e/(e - 1)$ periods in expectation to the first failed probe, and at most $2n - 1$ periods at each member with round-robin.
- **Dissemination time.** An update is sent $\lambda \log n$ times, and spreads like a push epidemic, so it reaches all members in $O(\log n)$ periods with high probability. The suspicion timeout is set to a multiple of $\log n$ periods for this reason.
- **Message load.** A member sends one ping and gets one ack per period, plus at most $4k$ messages when the direct ping fails. It receives about one ping per period. The load does not grow with $n$.
- **Space.** A full membership list, $O(n)$ per member.

## Properties

- **Scale-independent detection.** The expected detection time and the false positive probability per period do not depend on $n$.
- **Indirect probing.** A probe fails only if the direct path and all $k$ indirect paths fail, which tolerates a congested link between two members.
- **Weak consistency.** Members can disagree for a while about who is alive; updates converge with high probability.
- **No extra dissemination traffic.** Updates use the probe messages, so the load is the same with or without membership changes.

## Variants and improvements

- **Lifeguard.** Dadgar, Phillips and Currey (2018) added a local health multiplier, so a member that is itself slow stretches its timeouts; a suspicion timeout that starts long and shrinks as independent suspicions arrive; and a buddy system that tells a suspected member at once. These cut false positives a lot in HashiCorp's measurements.
- **HashiCorp memberlist and Serf.** The Go library memberlist implements SWIM with suspicion and Lifeguard, adds gossip of updates on a separate short interval to a few random members, and periodic full state exchange over TCP. Its default LAN settings probe every second, use 3 indirect checks, a retransmit limit of $4 \lceil \log_{10}(n + 1) \rceil$ and a suspicion timeout of $4 \log_{10} n$ probe intervals. Serf, and through it Consul and Nomad, build on memberlist.
- **[Phi accrual failure detection](/phi-accrual-failure-detector/)** replaces the binary probe outcome with a suspicion level from heartbeat history; it is used in systems that send heartbeats along fixed links instead of random probes.

## When to use it

Use SWIM for membership of a cluster of tens to thousands of nodes that all need a full member list, such as service discovery, cluster managers and distributed databases. It needs no central node and its load per node is constant. If each node needs only a small partial view, use a [peer sampling service](/peer-sampling-service/) or [HyParView](/hyparview/) instead.

## Pitfalls

- **Period too short.** The period must cover a ping, a ping-req and the relayed ack, at least three round trip times; otherwise live members fail probes.
- **No suspicion.** Basic SWIM declares a member faulty after one failed probe, which gives many false positives under message loss, as the table shows.
- **Suspicion timeout too short.** The timeout must let the Suspect update reach the suspected member and its Alive answer come back, about two dissemination times.
- **Slow members as accusers.** A member with a busy CPU or a slow network misses acks and suspects healthy members; Lifeguard was made for this case.
- **Network partitions.** Each side confirms the other side faulty, and the groups must be merged again by a full state exchange or a rejoin.

## Implementations

## History

Gupta, Chandra and Goldszmidt (PODC 2001) gave the requirements for a scalable failure detector, a detection time and a false positive rate independent of the group size, and showed a randomized detector that meets them. Das, Gupta and Motivala built SWIM on it at Cornell and presented it at DSN 2002, with suspicion, infection-style dissemination and the round-robin order, and a prototype measured on a cluster of up to 55 machines. HashiCorp's memberlist made SWIM widely used, and in 2018 HashiCorp published Lifeguard, its extensions for more accurate detection.

## References
