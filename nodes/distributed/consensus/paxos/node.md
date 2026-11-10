---
tag: 7W88GQ
kind: algorithm
slug: paxos
name: Paxos
aliases:
- Synod protocol
- single-decree Paxos
- basic Paxos
area: distributed/consensus
level: core
summary: Two-phase protocol with proposers, acceptors and learners that decides one value safely under asynchrony.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of acceptors, l: the number of learners}
  time: {best: Θ(1)}
  messages: {best: Θ(n l)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1998
  people: [Leslie Lamport]
  note: Lamport described the algorithm in The Part-Time Parliament, submitted in 1990 and published in 1998, and again in Paxos Made Simple in 2001.
prereqs: [consensus-problem, asynchronous-model, crash-failure, quorum, ballot-number]
see_also: [multi-paxos, raft, viewstamped-replication, fast-paxos, flexible-paxos, flp-impossibility, omega-failure-detector, chandra-toueg-consensus]
sources:
  - paper: doi:10.1145/279227.279229
    title: Leslie Lamport, The part-time parliament, ACM Transactions on Computer Systems 16(2), 133-169, 1998
    locator: Section 2 (the Synod protocol and the conditions B1 to B3) and Section 3 (the multi-decree parliament)
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 2 (the consensus algorithm, the properties P1, P1a, P2, P2a, P2b, P2c and the two phases) and Section 3 (state machines)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 5 (consensus) and Chapter 6 (consensus variants), the leader-driven consensus algorithms with the epoch abstraction
  - paper: doi:10.1145/2673577
    title: Robbert van Renesse and Deniz Altinbuken, Paxos made moderately complex, ACM Computing Surveys 47(3), article 42, 2015
    locator: the single-decree core (acceptors, leaders, scouts and commanders) and the invariants
---

Paxos is an algorithm for the [consensus problem](/consensus-problem/) among processes that can crash, in the [asynchronous model](/asynchronous-model/). Proposers suggest values, acceptors vote on them in numbered ballots, and learners find out which value won. Any two majorities of acceptors share an acceptor, and a proposer must re-propose the latest value that such an acceptor reports, so at most one value is ever chosen, whatever the delays, losses and crashes. Paxos cannot guarantee that a value is chosen, which agrees with the [FLP impossibility](/flp-impossibility/) result, but it decides as soon as one leader runs alone for a while.

## In plain words

A group must pick one value, but members can stop, and letters can be slow or get lost. Some members suggest values. The others vote.

A suggester first sends a ticket with a number, larger than any number it has used. Each voter promises to ignore all older tickets, and it tells the suggester the last value it voted for, with that value's ticket number. When more than half of the voters reply, the suggester asks them to vote. It does not ask for its own value when someone reported an earlier vote. It asks for the reported value with the largest ticket number.

When more than half of the voters vote for the same value under the same ticket, that value is chosen. Two different halves always share a voter, and that shared voter carries the chosen value forward to every later ticket.

## The problem

**Model.** There are $n$ acceptors, any number of proposers and $l$ learners. The timing is [asynchronous](/asynchronous-model/): there is no bound on message delays or on relative speeds. Processes fail by [crashing](/crash-failure/). An acceptor may restart: it keeps its state on stable storage. Messages can be lost, duplicated and delivered out of order, but they are not corrupted. There are no [Byzantine](/byzantine-failure-model/) faults. We write $f$ for the number of acceptors that are crashed at a time; Lamport does not name it.

**Properties.** Each proposer $p$ has an input value $x_p$. A value is *chosen* when a majority of acceptors have accepted it in the same ballot. Paxos guarantees these [consensus properties](/consensus-properties/):

- **Validity** (in the form of Lamport): only a value that some proposer proposed can be chosen.
- **Agreement**: at most one value is chosen, and a learner learns a value only if it is chosen.
- **Termination** (liveness, not guaranteed in general): if one proposer runs as the only leader, a majority of acceptors is up and messages arrive within a bound, then each live learner learns the value.

The two safety properties hold in every run, with no timing assumption and with any number of crashes. Termination needs more, as the section on liveness explains.

## The algorithm

A [ballot number](/ballot-number/) $b$ is a pair $(r, p)$ of a round $r$ and a proposer id $p$, compared first by $r$ and then by $p$. So two proposers never use the same ballot. Here $\bot$ means "none", and a majority is any set of at least $\lfloor n/2 \rfloor + 1$ acceptors (a [quorum](/quorum/)).

```pseudo id=main
PROPOSER p, with input x_p
L1  on start, or on a timeout:
L2      b ← (r, p), with r larger than each round that p has seen; P ← ∅
L3      send PREPARE(b) to all acceptors                          ▷ phase 1a
L4  on PROMISE(b, vb, vv) from acceptor a, if b is the current ballot and p is in phase 1:
L5      P ← P ∪ {(a, vb, vv)}
L6      if |P| ≥ ⌊n/2⌋ + 1 then
L7          if some promise in P has vb ≠ ⊥ then v ← the vv with the largest vb in P
L8          else v ← x_p
L9          send ACCEPT(b, v) to all acceptors                    ▷ phase 2a

ACCEPTOR a, with promised, vb, vv on stable storage (all ⊥ at the start)
L10 on PREPARE(b) from p:  if promised = ⊥ or b > promised then
L11     promised ← b; send PROMISE(b, vb, vv) to p                 ▷ phase 1b
L12 else send NACK(promised) to p
L13 on ACCEPT(b, v) from p:  if promised = ⊥ or b ≥ promised then
L14     promised ← b; vb ← b; vv ← v; send ACCEPTED(b, v) to all learners   ▷ phase 2b
L15 else send NACK(promised) to p

LEARNER
L16 on ACCEPTED(b, v) from acceptor a:  add a to S[b]
L17     if |S[b]| ≥ ⌊n/2⌋ + 1 then learn v
```

**Phase 1 (prepare and promise).** A proposer picks a fresh ballot $b$ and sends PREPARE($b$). An acceptor that has not promised a larger ballot promises $b$. The promise means: "I will not accept any ballot smaller than $b$". With the promise, the acceptor reports its last vote $(vb, vv)$, the largest ballot in which it accepted a value and that value.

**Phase 2 (accept and accepted).** With promises from a majority, the proposer picks the value. If some promise reports a vote, it must take the value of the vote with the largest ballot (line L7). Only if no acceptor of the majority has voted may it take its own input (line L8). Then it sends ACCEPT($b$, $v$). An acceptor accepts unless it has promised a larger ballot, and it tells the learners.

A NACK carries the larger ballot that the acceptor has promised. The proposer uses it in line L2 to pick a larger round next time. Each handler is safe to run twice on the same message, so duplicates do no harm. A lost message only stops progress, and a timeout starts a new ballot.

## Example

Three acceptors $A_0, A_1, A_2$, so a majority has two. Proposer $P_0$ has input $x$ and proposer $P_1$ has input $y$. The entries show (promised, last vote) of each acceptor; a vote is a pair of ballot and value.

| step | event | $A_0$ | $A_1$ | $A_2$ |
|---|---|---|---|---|
| 0 | start | ⊥, ⊥ | ⊥, ⊥ | ⊥, ⊥ |
| 1 | $P_0$ sends PREPARE((1,0)); the copy to $A_2$ is lost | (1,0), ⊥ | (1,0), ⊥ | ⊥, ⊥ |
| 2 | $P_0$ has 2 promises with no vote, so $v = x$; ACCEPT((1,0), $x$) reaches $A_0$ and $A_1$ | (1,0), ((1,0), $x$) | (1,0), ((1,0), $x$) | ⊥, ⊥ |
| 3 | $x$ is now chosen: 2 of 3 acceptors accepted it in ballot (1,0) | | | |
| 4 | $P_1$ sends PREPARE((1,1)); it reaches $A_1$ and $A_2$ | (1,0), ((1,0), $x$) | (1,1), ((1,0), $x$) | (1,1), ⊥ |
| 5 | $P_1$ gets the promises ((1,0), $x$) from $A_1$ and ⊥ from $A_2$; line L7 gives $v = x$, not $y$ | | | |
| 6 | ACCEPT((1,1), $x$) reaches $A_1$ and $A_2$ | (1,0), ((1,0), $x$) | (1,1), ((1,1), $x$) | (1,1), ((1,1), $x$) |
| 7 | the late ACCEPT((1,0), $x$) reaches $A_2$; $(1,0) < (1,1)$, so $A_2$ sends a NACK | | | |

Each learner gets ACCEPTED from two acceptors in ballot (1,0) or (1,1), and learns $x$. The promise of $A_1$ in step 4 is the shared acceptor of the two majorities $\{A_0, A_1\}$ and $\{A_1, A_2\}$. If $P_1$ broke line L7 and proposed its own $y$, the acceptors $A_1$ and $A_2$ would accept $y$ in ballot (1,1), and both $x$ and $y$ would be chosen.

## Correctness

The safety proof rests on one invariant, the form P2c of Paxos Made Simple:

> If ACCEPT($b$, $v$) is sent, then there is a majority $S$ of acceptors such that either (a) no acceptor in $S$ has accepted a ballot smaller than $b$, or (b) $v$ is the value of the largest ballot smaller than $b$ that the acceptors of $S$ have accepted.

Lines L4 to L8 keep it: $S$ is the set of acceptors whose promises the proposer used, and a promise for $b$ stops its acceptor from accepting any smaller ballot later. From P2c, strong induction on the ballot shows: if $v$ is chosen in ballot $b_0$, then each ACCEPT with a ballot larger than $b_0$ carries $v$. So all chosen values are equal. Validity holds because each value in an ACCEPT is either an input (line L8) or a value from an earlier ACCEPT (line L7). The full proof is below.

### Liveness

Paxos does not always terminate, and no deterministic algorithm can in this model ([FLP](/flp-impossibility/)). The simplest bad run has two dueling proposers. $P_0$ finishes phase 1 with ballot 1. $P_1$ finishes phase 1 with ballot 2 before the ACCEPT of $P_0$ arrives, so that ACCEPT fails. $P_0$ then starts ballot 3, which makes the ACCEPT of $P_1$ fail, and so on. No value is ever chosen, but safety holds the whole time.

The fix is a distinguished leader: only one process acts as proposer. An [Ω failure detector](/omega-failure-detector/) gives exactly this: eventually all correct processes trust the same correct leader. Assume [partial synchrony](/partial-synchrony/) (after an unknown time GST, each message arrives within $\delta$), a majority of acceptors that stay up, and a leader that, after GST, is the only proposer and uses timeouts larger than $4\delta$. Then the leader's first ballot that is larger than all ballots used before finishes both phases, and the value is chosen within $4\delta$ of the start of that ballot. A NACK tells the leader a larger round, so it needs at most one failed ballot after GST to find a large enough round.

## Complexity

The costs are for one ballot with no failures and one proposer, counted in message delays (the time unit of the asynchronous model when each message takes one unit).

- **Message delays.** PREPARE, PROMISE, ACCEPT, ACCEPTED: 4 delays from the start of the ballot until the learners learn. If a client sends its value to the proposer, the client's message adds one delay. When phase 1 is already done, 2 delays remain: ACCEPT and ACCEPTED. [Multi-Paxos](/multi-paxos/) uses this to do phase 1 once for many values.
- **Messages.** $n$ PREPARE, $n$ PROMISE, $n$ ACCEPT and $n \cdot l$ ACCEPTED, so $3n + nl = \Theta(nl)$. With $n = 3$ and $l = 2$ this is 15 messages, and with $n = l = 5$ it is 40. The proposer can send phase 1 and phase 2 messages to a majority only, but then the loss of one acceptor stops the ballot.
- **Stable storage.** Each acceptor writes to stable storage before it sends a PROMISE or an ACCEPTED, so there are two writes on the critical path.
- **State.** Each acceptor keeps three items: promised, vb and vv. So the space is $\Theta(1)$ ballots and values per acceptor.
- **Fault tolerance.** Safety holds with any number of crashes. Progress needs a majority of acceptors that are up, so $n = 2f + 1$ acceptors tolerate $f$ crashed acceptors.

In the worst case the number of ballots has no bound, as the dueling run above shows.

## Properties

- **Safe under asynchrony.** No timing assumption is needed for agreement and validity. Timeouts only affect progress.
- **Crash-recovery.** An acceptor that restarts with its stable state is the same as a slow acceptor.
- **Roles are logical.** In practice each server is proposer, acceptor and learner at the same time.
- **Not Byzantine tolerant.** One acceptor that lies about its last vote can break agreement. [PBFT](/pbft/) solves the Byzantine case with $n \ge 3f + 1$.

## Variants and improvements

- **[Multi-Paxos](/multi-paxos/).** A sequence of instances with a stable leader. Phase 1 runs once for all future slots, so each value costs only phase 2. This is the usual way to build a [replicated state machine](/replicated-state-machine/).
- **[Fast Paxos](/fast-paxos/).** Clients send values straight to acceptors, which saves one message delay but needs larger quorums.
- **[Flexible Paxos](/flexible-paxos/).** Phase 1 quorums need only intersect phase 2 quorums, so phase 2 quorums can be small.
- **[Cheap Paxos](/cheap-paxos/).** $f + 1$ main processors and $f$ auxiliary ones that work only after a failure.
- **[Generalized Paxos](/generalized-paxos/) and [EPaxos](/epaxos/).** Commands that commute need no order.
- **[Vertical Paxos](/vertical-paxos/).** An external master changes the set of acceptors from ballot to ballot.
- **[Mencius](/mencius/).** Leaders take turns on pre-assigned slots, for wide area networks.
- **[Paxos Commit](/paxos-commit/).** One Paxos instance per resource manager makes atomic commit non-blocking.
- **[Raft](/raft/), [Viewstamped Replication](/viewstamped-replication/) and [Zab](/zab/).** Leader-based protocols with the same quorum and ballot core, with a different way to elect the leader and repair logs.

## When to use it

Use Paxos when a group of servers must agree on a value despite crashes and an unreliable network, and when it is more important never to disagree than always to respond. Typical uses are a lock service, the choice of a primary, and configuration data. For a sequence of values use Multi-Paxos or Raft, not one Paxos instance per value with a fresh phase 1. If processes can lie, use a Byzantine protocol. If all processes are reliable and the network is synchronous, a simpler protocol such as [FloodSet](/floodset/) is enough.

## Pitfalls

- **Own value instead of the reported value.** Line L8 must run only when no promise reports a vote. A proposer that always sends its input breaks agreement, as in the example. A test with that change finds two chosen values on random schedules.
- **The first vote instead of the largest one.** Line L7 must take the vote with the largest ballot. An older vote may belong to a ballot whose value was never chosen, while a later ballot did choose a value.
- **Strict test in phase 2.** Line L13 uses $b \ge$ promised, because the acceptor has promised exactly $b$ to this proposer in phase 1. With $b >$ promised no ballot could ever finish.
- **Reused ballots.** Two proposers with the same ballot can send two values in one ballot. Use pairs (round, id), as in line L2.
- **State not on stable storage.** An acceptor that forgets its promise after a restart can accept a smaller ballot. Write promised, vb and vv before line L11 and line L14 send their replies.
- **A learner that counts messages, not acceptors.** With duplicate messages, line L16 must count distinct acceptors per ballot. It must also not add votes of different ballots together.

## Implementations

## History

Lamport described the algorithm as the Synod protocol of a fictional Greek parliament in The Part-Time Parliament. He submitted it in 1990, and it appeared in ACM Transactions on Computer Systems in 1998. Paxos Made Simple (2001) gave the same algorithm in plain terms, with the derivation from P1 to P2c. Oki and Liskov published [Viewstamped Replication](/viewstamped-replication/) in 1988, a replication protocol with an equivalent core. Later work turned Paxos into the textbook basis for replicated services, with Chubby, Spanner and ZooKeeper as well known users of Paxos-like protocols.

## References
