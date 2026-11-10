---
tag: RNQ60T
kind: concept
slug: omega-failure-detector
name: Omega (leader) failure detector
aliases:
- Ω
- eventual leader detector
area: distributed/consensus
level: advanced
summary: Eventually outputs the same correct leader at all correct processes.
prereqs: [failure-detector]
see_also: [weakest-failure-detector-consensus, eventually-perfect-failure-detector, chandra-toueg-consensus, paxos, raft, leader-lease, partial-synchrony, flp-impossibility]
sources:
  - paper: doi:10.1145/234533.234549
    title: Tushar Deepak Chandra, Vassos Hadzilacos and Sam Toueg, The weakest failure detector for solving consensus, Journal of the ACM 43(4), 1996
    locator: pages 685 to 722 (the definition of Omega, and the proof that Omega, so also diamond-W, is the weakest failure detector for consensus with a majority of correct processes)
  - paper: "Francis C. Chu, Reducing Ω to ◊W, Information Processing Letters 67(6), 1998"
    locator: the direct reduction from diamond-W to Omega
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (the classes diamond-S and diamond-W, and the reduction from weak to strong completeness)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 2 (eventual leader election, and its implementation from an eventually perfect detector) and Chapter 5 (consensus with an eventual leader)
---

$\Omega$ is the [failure detector](/failure-detector/) that outputs one process, the trusted leader, at each process, with the promise that eventually all correct processes trust the same correct process for ever. Chandra, Hadzilacos and Toueg (1996) defined it and proved that it is the [weakest failure detector for consensus](/weakest-failure-detector-consensus/) when a majority of processes is correct. It is equivalent to $\Diamond\mathcal{W}$, the weakest of the eight classes of Chandra and Toueg. Leader based protocols such as [Paxos](/paxos/) and [Raft](/raft/) use exactly this guarantee for liveness.

## In plain words

Each computer has a helper that names one computer as the leader. For a while the helpers may name different leaders, or a leader that has stopped. But from some point on, every working computer's helper names the same working computer, and keeps naming it.

Nobody is told when that point has come. So an algorithm that uses the leader must stay correct while the leaders differ, and it may only make progress once they agree.

This promise is small, but it is enough for a group with a working majority to agree on a value, and nothing smaller is enough.

## The idea

### Definition

There are $n$ processes, and a process is correct if it never crashes. The module of $\Omega$ at process $p$ outputs at each time $t$ one process $\mathit{leader}_p(t)$. The only promise is this.

- **Eventual leadership.** There is a correct process $\ell$ and a time $T$ such that $\mathit{leader}_p(t) = \ell$ for every correct process $p$ and every $t \ge T$.

Before $T$ the outputs can be anything: different at different processes, crashed processes, or changing at every query. A process cannot tell whether $T$ has passed.

### $\Omega$ gives $\Diamond\mathcal{S}$

Let each process $p$ output the set of suspects $\Pi \setminus \{\mathit{leader}_p\}$, where $\Pi$ is the set of all processes. After time $T$, every correct process suspects every process except $\ell$. So every crashed process is permanently suspected by every correct process, which is strong completeness, and the correct process $\ell$ is never suspected, which is eventual weak accuracy. So $\Omega$ is at least as strong as $\Diamond\mathcal{S}$, and so also as $\Diamond\mathcal{W}$. The reduction needs no messages.

### $\Diamond\mathcal{W}$ gives $\Omega$

The converse is harder, because $\Diamond\mathcal{S}$ lets different correct processes suspect different correct processes for ever, so "the smallest process that I do not suspect" can differ between processes. Chandra, Hadzilacos and Toueg get the converse as a corollary of their weakest detector theorem. Chu (1998) gives a direct reduction. One simple reduction uses accusation counters.

1. First turn $\Diamond\mathcal{W}$ into $\Diamond\mathcal{S}$ with the Chandra-Toueg reduction from weak to strong completeness.
2. Each process $p$ keeps a counter $a_p[q]$ for each $q$, and adds 1 to $a_p[q]$ at each query in which its module suspects $q$. It sends its vector $a_p$ to all, again and again.
3. Each process keeps the largest vector it has received from each $s$, and computes $A[q] = \sum_s a_s[q]$. It outputs as its leader the $q$ with the smallest pair $(A[q], q)$.

*Proof.* Let $B$ be the set of processes $q$ for which the true total $\sum_s a_s[q]$ stays bounded. A crashed process is suspected for ever by every correct process, at each of infinitely many queries, so its total is unbounded. The eventually trusted process $\ell$ of $\Diamond\mathcal{S}$ is suspected only finitely often, so $\ell \in B$. So $B$ is non-empty and has only correct processes. Each counter of a process in $B$ stops at a final value, and every correct process eventually receives every final value, also from crashed senders, whose finitely many messages all arrive. So every correct process eventually computes the same final $A[q]$ for each $q \in B$. For $q \notin B$, some correct sender increases $a_s[q]$ for ever and keeps sending it, so $A[q]$ grows past every bound at every correct process. There are finitely many processes, so eventually every correct process outputs the same $q \in B$, the one with the smallest pair $(A[q], q)$, and that process is correct. $\blacksquare$

So $\Omega \cong \Diamond\mathcal{S} \cong \Diamond\mathcal{W}$.

### Consensus with $\Omega$

With $n > 2f$, a leader based algorithm solves consensus with $\Omega$. It is the [Chandra-Toueg algorithm](/chandra-toueg-consensus/) with the rotating coordinator replaced by "the process that $\Omega$ names". A process that thinks it is the leader starts a new round with a higher number, collects estimates with timestamps from a majority, proposes the one with the largest timestamp, and decides when a majority adopts it. Safety comes from majority intersection and timestamps alone. Once $\Omega$ is stable, only $\ell$ starts rounds, and its next round succeeds. This is the structure of single decree [Paxos](/paxos/), with ballots in place of rounds.

## Examples

- **From $\Diamond\mathcal{P}$.** If the module is an [eventually perfect detector](/eventually-perfect-failure-detector/), let each process output the smallest identifier that it does not suspect. Once $\Diamond\mathcal{P}$ is exact at all correct processes, this is the smallest correct identifier everywhere. So heartbeats with growing timeouts in the [partial synchrony](/partial-synchrony/) model give $\Omega$.
- **Non-example: the smallest unsuspected process with $\Diamond\mathcal{S}$.** Take $n = 3$ with $p_1$ correct. A $\Diamond\mathcal{S}$ history may have $p_2$ suspect $p_1$ for ever, while $p_3$ suspects nobody and nobody ever suspects $p_3$; this meets eventual weak accuracy with $\ell = p_3$. Then $p_2$ picks $p_2$ and $p_3$ picks $p_1$, and the two never agree. This is why the counters above are needed.
- **Election timeouts.** In [Raft](/raft/), a follower that hears nothing from the leader for a random timeout starts an election. If the network is eventually timely and timeouts are long enough, one leader is eventually elected and stays, which is the $\Omega$ guarantee. While several processes think they are leaders, Raft stays safe by terms and majority votes.
- **Non-example: a fixed leader.** Always naming $p_1$ is $\Omega$ only in runs where $p_1$ is correct. It fails the definition in a run where $p_1$ crashes.

## Where it is used

- **Paxos and its relatives.** [Paxos](/paxos/), [Multi-Paxos](/multi-paxos/), [Raft](/raft/), [Zab](/zab/) and [Viewstamped Replication](/viewstamped-replication/) are safe with any leader output and live once an $\Omega$ like leader is stable. A [leader lease](/leader-lease/) adds timing assumptions on top so that the leader can serve reads alone.
- **The theory of consensus.** $\Omega$ is the weakest detector for consensus with a majority of correct processes. Without a majority, consensus needs $\Omega$ together with the quorum detector $\Sigma$, as shown on the [weakest failure detector](/weakest-failure-detector-consensus/) page.
- **Separating timing from logic.** An algorithm written against $\Omega$ runs in any system where $\Omega$ can be built, for example a partially synchronous system or one where only some links are eventually timely.

## References
