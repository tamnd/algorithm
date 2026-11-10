---
tag: PG2BGV
kind: model
slug: partial-synchrony
name: Partial synchrony model
aliases:
- Dwork-Lynch-Stockmeyer model
area: distributed/consensus
level: advanced
summary: Timing bounds exist but hold only after an unknown global stabilization time.
history:
  year: 1988
  people: [Cynthia Dwork, Nancy Lynch, Larry Stockmeyer]
  note: Dwork, Lynch and Stockmeyer defined partial synchrony and gave consensus algorithms with optimal resilience for it in the Journal of the ACM in 1988, after a PODC 1984 version.
prereqs: [asynchronous-model, synchronous-model]
see_also: [flp-impossibility, eventually-perfect-failure-detector, chandra-toueg-consensus, paxos, pbft, byzantine-resilience-bound, failure-detector, clock-synchronization]
sources:
  - paper: doi:10.1145/42282.42283
    title: Cynthia Dwork, Nancy Lynch and Larry Stockmeyer, Consensus in the presence of partial synchrony, Journal of the ACM 35(2), 1988
    locator: pages 288 to 323 (the two forms of partial synchrony, with unknown bounds or with known bounds after GST, the round based algorithms, and the resilience bounds for crash, omission and Byzantine faults)
  - paper: doi:10.1145/226643.226647
    title: Tushar Deepak Chandra and Sam Toueg, Unreliable failure detectors for reliable distributed systems, Journal of the ACM 43(2), 1996
    locator: pages 225 to 267 (diamond-P built with timeouts in a partially synchronous system, and the need for a majority with diamond-P)
  - book: isbn:9781558603486
    title: Nancy A. Lynch, Distributed Algorithms, Morgan Kaufmann, 1996
    locator: Chapters 23 to 25 (partially synchronous system models, mutual exclusion and consensus with timing bounds)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luis Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 2 (eventually synchronous systems and the failure detectors they allow)
---

The partial synchrony model of Dwork, Lynch and Stockmeyer (1988) lies between the [synchronous](/synchronous-model/) and the [asynchronous model](/asynchronous-model/). Bounds on message delay and on relative process speed exist, but either they are not known, or they are known and hold only after an unknown global stabilization time, GST. An algorithm for this model must be safe in every execution, as in the asynchronous model, and must terminate once the system behaves well. [Consensus](/consensus-problem/) with crash failures is solvable here exactly when $n > 2f$, and with Byzantine failures exactly when $n > 3f$.

## The machine

**Processes and links.** There are $n$ processes on a complete network, of which at most $f$ may be faulty. Time is real time, which the processes cannot read directly. Each process has a local clock or counts its own steps.

**Two timing bounds.** Let $\Delta$ bound the time from the sending of a message to its delivery, and let $\Phi$ bound the relative speed of processes: in any interval in which some process takes $\Phi + 1$ steps, every correct process takes at least one step. In the synchronous model both bounds hold from the start and are known. In the asynchronous model, neither exists.

**The two forms of partial synchrony.** Dwork, Lynch and Stockmeyer define two forms, and show that the same results hold in both.

- **Unknown bounds.** $\Delta$ and $\Phi$ exist and hold in the whole execution, but the processes do not know them. An algorithm cannot wait for a fixed time, because any fixed time may be too short.
- **Known bounds after GST.** $\Delta$ and $\Phi$ are known, but they are only guaranteed to hold from an unknown time GST on. Before GST, messages can be delayed arbitrarily and processes can be arbitrarily slow. In DLS's formal model, messages sent before GST may also be lost. Many later papers assume reliable links instead, with every message sent at time $s$ delivered by $\max(s, \mathrm{GST}) + \Delta$, and call this the *eventually synchronous* model.

A third form, used by Chandra and Toueg, combines them: the bounds are unknown and hold only after GST.

**Rounds in DLS.** DLS run their algorithms in rounds, with each process using its clock to decide when a round ends. Before GST, messages of a round can miss their round, and a round can fail. After GST, with round lengths large enough, every message of a round arrives in that round. In the unknown bounds form, round lengths grow over time, so that eventually they are longer than the unknown $\Delta$.

## What it counts

- **Safety in all executions.** Agreement and validity must hold in every execution, also before GST, or when the bounds are never reached. This is the asynchronous model's demand.
- **Termination after stabilization.** Each correct process must decide in every execution that satisfies the timing assumptions. The cost is measured as the time, or the number of rounds, from GST to the last decision, in units of $\Delta$ and $\Phi$.
- **Messages.** The number of messages per round, and in total after GST.

An algorithm with these properties is often called *indulgent*: the timing assumptions are used only for liveness, never for safety.

## Relation to other models

- **Asynchronous model.** With reliable links, every partially synchronous execution is also an asynchronous one, so an algorithm that is correct in the asynchronous model is correct here. The converse fails: consensus is solvable here and not there. Each finite prefix of an asynchronous execution is also a prefix of a partially synchronous one, with GST after it. So an algorithm here cannot use timing for safety, only for termination.
- **Synchronous model.** It is the case GST $= 0$ with known bounds.
- **Failure detectors.** Heartbeats with timeouts that grow after each mistake build an [eventually perfect failure detector](/eventually-perfect-failure-detector/) $\Diamond\mathcal{P}$ in this model, and so also [$\Omega$](/omega-failure-detector/). So an algorithm written for the asynchronous model with $\Diamond\mathcal{S}$ or $\Omega$, such as the [Chandra-Toueg algorithm](/chandra-toueg-consensus/) or [Paxos](/paxos/), runs here with no oracle.
- **Clocks.** The processes need only to measure local time intervals, not to agree on the time. [Clock synchronization](/clock-synchronization/) is a separate problem.

## Known results in the model

**Crash failures need and suffice with $n > 2f$.**

*Necessity.* Assume $n \le 2f$ and an algorithm that solves consensus. Split the processes into groups $A$ and $B$ of at most $f$ each. In execution $\alpha$, the processes of $B$ crash at the start and all of $A$ has input 0; this is a legal execution with GST $= 0$, so $A$ decides, and by validity it decides 0, by some time $t_A$. In execution $\beta$, $A$ crashes at the start, all of $B$ has input 1, and $B$ decides 1 by some time $t_B$. Now take execution $\gamma$ with no crash, inputs 0 in $A$ and 1 in $B$, and GST later than $\max(t_A, t_B)$, with every message between $A$ and $B$ delayed until after GST. Up to time $t_A$, the processes of $A$ cannot tell $\gamma$ from $\alpha$, so they decide 0; in the same way $B$ decides 1. This breaks agreement, so $n > 2f$ is necessary.

*Sufficiency.* With $n > 2f$, DLS give a round based algorithm with rotating coordinators and locks. Another route is to build $\Diamond\mathcal{P}$ with growing timeouts and run the Chandra-Toueg algorithm, whose safety does not depend on the detector.

**Byzantine failures need and suffice with $n > 3f$.** DLS show that $n > 3f$ is necessary and sufficient for Byzantine faults in partial synchrony, matching the [Byzantine resilience bound](/byzantine-resilience-bound/) of the synchronous model. Practical protocols such as [PBFT](/pbft/) use this model: safe always, live after GST, with $n = 3f + 1$.

**Summary of crash resilience for consensus.**

| model | crashes tolerated |
|---|---|
| [synchronous](/synchronous-model/) | any $f < n$ |
| partial synchrony | $n > 2f$ |
| [asynchronous](/asynchronous-model/), deterministic | none, by [FLP](/flp-impossibility/) |

The gap between the synchronous and the partially synchronous rows comes from the necessity argument above: in a synchronous system the silence of $B$ for one round proves that $B$ crashed, while before GST it proves nothing.

## References
