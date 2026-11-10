---
tag: S0DYB3
kind: concept
slug: eventually-perfect-failure-detector
name: Eventually perfect failure detector
aliases:
- diamond-P
- ◊P
area: distributed/consensus
level: advanced
summary: Eventually suspects exactly the crashed processes.
prereqs: [failure-detector, partial-synchrony]
see_also: [omega-failure-detector, chandra-toueg-consensus, weakest-failure-detector-consensus, phi-accrual-failure-detector, swim, failure-detection, flp-impossibility, crash-failure]
sources:
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (the definition of the class diamond-P by strong completeness and eventual strong accuracy, and its implementation with timeouts in a partially synchronous system)
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: pages 288 to 323 (the two models of partial synchrony, with unknown bounds or with known bounds after an unknown global stabilization time)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 2 (the eventually perfect failure detector, built with heartbeats and a timeout that grows after each false suspicion)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapter 21, Section 21.4 (failure detectors in asynchronous networks)
---

An eventually perfect failure detector, written $\Diamond\mathcal{P}$, is a [failure detector](/failure-detector/) that can make mistakes for a while but, after some unknown time, suspects exactly the processes that have crashed. It is the class defined by strong completeness and eventual strong accuracy in Chandra and Toueg (1996). It cannot be built in the pure [asynchronous model](/asynchronous-model/), but heartbeats with timeouts that grow after each mistake build it in the [partial synchrony](/partial-synchrony/) model. It is strong enough for [consensus](/consensus-problem/) with a majority of correct processes.

## In plain words

Each computer sends a short "I am alive" note to the others at a fixed rate. If the notes from a computer stop for too long, the others start to suspect that it has stopped.

When the network is slow, a working computer can be suspected by mistake. When its next note arrives, the others trust it again and agree to wait a little longer next time.

Once the network settles, the notes from a working computer always come within some fixed time, which nobody knows. Each mistake makes the wait longer, so after a few mistakes the wait is long enough and the mistakes stop. A computer that has really stopped sends no more notes, so it stays suspected for ever.

## The idea

### Definition

A failure detector module at each process $p$ outputs a set $\mathit{suspected}_p(t)$ of processes at each time $t$. A *correct* process is one that never crashes. The class $\Diamond\mathcal{P}$ is defined by two properties.

- **Strong completeness.** There is a time after which every crashed process is in $\mathit{suspected}_p$ of every correct process $p$, for ever.
- **Eventual strong accuracy.** There is a time after which no correct process is in $\mathit{suspected}_p$ of any correct process $p$.

Only finitely many processes crash, so together they say that there is a time $T$ after which $\mathit{suspected}_p(t)$ is exactly the set of crashed processes at every correct $p$. Before $T$ the output can be wrong in both ways. The *perfect* detector $\mathcal{P}$ has strong completeness and *strong accuracy*: it never suspects a process before that process crashes. $\Diamond\mathcal{P}$ is the eventual form of $\mathcal{P}$, and it is stronger than $\Diamond\mathcal{S}$, which needs only one correct process that is eventually trusted by all.

### Why it needs timing

In the asynchronous model, a crashed process cannot be told apart from a slow one in finite time. If some algorithm built $\Diamond\mathcal{P}$ there, then the [Chandra-Toueg algorithm](/chandra-toueg-consensus/) would solve consensus with one crash in the asynchronous model, which the [FLP impossibility](/flp-impossibility/) rules out. So any construction needs a timing assumption, and partial synchrony is the weakest usual one.

### The construction with growing timeouts

Assume the partial synchrony model of Dwork, Lynch and Stockmeyer with a global stabilization time GST: after GST, every correct process sends a heartbeat every $\eta$ time units, and a message sent at time $s$ arrives by $\max(s, \mathrm{GST}) + \Delta$. The values of GST and $\Delta$ are not known to the processes. Process $p$ runs this for each other process $q$:

```
HEARTBEAT-DIAMOND-P at process p
  every η time units: send (heartbeat) to all
  for each q ≠ p: last[q] ← 0; T[q] ← T0; q is trusted
  when (heartbeat) arrives from q:
      last[q] ← now
      if q is suspected then trust q; T[q] ← T[q] + 1
  when now − last[q] > T[q] and q is trusted: suspect q
```

**Claim.** This module is in $\Diamond\mathcal{P}$.

*Step 1, the gap after GST.* Let $q$ be correct and $u \ge \mathrm{GST} + \eta + \Delta$. Let $s$ be the last time at or before $u - \Delta$ when $q$ sends a heartbeat. Then $s \ge \mathrm{GST}$ and $s > u - \Delta - \eta$. The heartbeat arrives at $p$ by $s + \Delta \le u$. So at every time $u \ge \mathrm{GST} + \eta + \Delta$, the last heartbeat from $q$ arrived less than $\eta + \Delta$ ago.

*Step 2, eventual strong accuracy.* Let $p$ and $q$ be correct. Every suspicion of $q$ by $p$ ends, because $q$ sends heartbeats for ever and each arrives. Each end of a suspicion raises $T[q]$ by 1. A suspicion that starts at a time $u \ge \mathrm{GST} + \eta + \Delta$ needs $u - \mathit{last}[q] > T[q]$, so by step 1 it needs $T[q] < \eta + \Delta$. So at most $\eta + \Delta - T_0$ suspicions of $q$ by $p$ start after $\mathrm{GST} + \eta + \Delta$. Before that time only finitely many start, because each needs a silence longer than $T_0$. So $p$ makes finitely many mistakes about $q$, and after the last one ends, $p$ trusts $q$ for ever. There are finitely many pairs, so there is a time after which no correct process suspects a correct process.

*Step 3, strong completeness.* Let $q$ crash. It sent finitely many heartbeats, and they all arrive by some time $a$. At time $a + T[q] + 1$ at the latest, every correct $p$ suspects $q$. After that no heartbeat from $q$ arrives, so nothing makes $p$ trust $q$ again. $\blacksquare$

The bound in step 2 is on the *number* of mistakes, not on *when* they happen. With random delays, a gap close to $\eta + \Delta$ is rare, so the last mistakes can come long after GST.

### Known bounds and unknown bounds

Dwork, Lynch and Stockmeyer define two forms of partial synchrony. If $\eta$ and $\Delta$ are known and hold after an unknown GST, a fixed timeout $T \ge \eta + \Delta$ already gives $\Diamond\mathcal{P}$, by step 1. If the bounds hold from the start but are unknown, no fixed timeout is safe, because the true $\Delta$ may be larger than any value chosen in advance. The growing timeout covers both forms, which is why it is the standard construction. Instead of adding 1, the module can double $T[q]$; this reaches a large enough value after fewer mistakes, but it can make the detection of a real crash much slower.

## Examples

**The construction in a simulation.** Take $n = 5$ processes, heartbeats every $\eta = 4$ ticks and delays after GST in $[1, \Delta]$ with $\Delta = 6$ ticks, with $T_0 = 1$. With whole ticks the largest gap is $\eta + \Delta - 1 = 9$ ticks, so a timeout of $\eta + \Delta - 2 = 8$ is enough, and each pair makes at most $8 - T_0 = 7$ mistakes after $\mathrm{GST} + \eta + \Delta$. Over 30 seeded runs with GST at tick 200, uniform random delays and no crash, the mean number of mistakes after tick 210 was 63.7 over all 20 pairs, and the largest was 78, below the bound of 140. The last mistake ended a mean of 815 ticks after GST, and once 1498 ticks after GST: the bound on the number of mistakes says nothing about their time. In 80 seeded test runs with up to two crashes, each correct process ended by suspecting exactly the crashed ones.

**Non-example: a fixed timeout that is too small.** Keep $T = \eta + \Delta - 3 = 7$ fixed. An adversary that gives the heartbeats the delays $1, \Delta, \eta + 1, 1, \Delta, \eta + 1, \ldots$ makes a gap of 9 ticks in every third period, so each correct process is suspected again every 12 ticks, for ever: 300 mistakes over 12 pairs in the last 300 ticks of a run. The same adversary against the growing timeout with $T_0 = 7$ causes at most one mistake per pair after GST, and none at the end.

**From $\Diamond\mathcal{P}$ to $\Omega$.** Let each process output as its leader the smallest identifier that it does not suspect. After the time when the detector is exact at all correct processes, this is the smallest correct identifier at every correct process. So $\Diamond\mathcal{P}$ gives the [$\Omega$ detector](/omega-failure-detector/), which is the [weakest failure detector for consensus](/weakest-failure-detector-consensus/). The converse is false: $\Omega$ says nothing about which other processes are alive.

**Non-example: a detector that trusts everybody.** A module that never suspects anyone has strong accuracy but not completeness. It is in no class of Chandra and Toueg, and with it a process can wait for ever for a message from a crashed coordinator.

## Where it is used

- **Consensus.** $\Diamond\mathcal{P}$ is in $\Diamond\mathcal{S}$, so the [Chandra-Toueg algorithm](/chandra-toueg-consensus/) solves consensus with it when $n > 2f$. With $\Diamond\mathcal{P}$ the bound $n > 2f$ is still necessary.
- **Leader election.** Through the reduction above, it gives the leader that [Paxos](/paxos/) and [Raft](/raft/) style protocols need for liveness. Raft's election timeouts play a similar role.
- **Group membership and monitoring.** Practical detectors such as the [phi accrual detector](/phi-accrual-failure-detector/) and [SWIM](/swim/) are tuned heartbeat schemes. They aim at $\Diamond\mathcal{P}$ behaviour in a network that is mostly well behaved, and expose the trade off between fast detection and few mistakes that the timeout controls.

## References
