---
tag: 5TRQGX
kind: algorithm
slug: multi-paxos
name: Multi-Paxos
aliases:
- multi-decree Paxos
area: distributed/consensus
level: advanced
summary: Runs Paxos over a log of slots with a stable leader to skip phase one.
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
  note: The multi-decree parliament of The Part-Time Parliament runs phase 1 once for all future decrees. Paxos Made Simple (2001) gives the same idea for a state machine.
prereqs: [paxos, ballot-number, replicated-state-machine, quorum]
see_also: [raft, viewstamped-replication, leader-lease, mencius, epaxos, flexible-paxos, log-compaction, cluster-reconfiguration]
sources:
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 3 (implementing a state machine, the gaps filled with no-op commands)
  - paper: doi:10.1145/279227.279229
    title: Leslie Lamport, The part-time parliament, ACM Transactions on Computer Systems 16(2), 133-169, 1998
    locator: Section 3 (the multi-decree parliament)
  - paper: doi:10.1145/1281100.1281103
    title: Tushar D. Chandra, Robert Griesemer and Joshua Redstone, Paxos made live, an engineering perspective, PODC 2007, 398-407
    locator: the sections on Multi-Paxos and on master leases
  - paper: doi:10.1145/2673577
    title: Robbert van Renesse and Deniz Altinbuken, Paxos made moderately complex, ACM Computing Surveys 47(3), article 42, 2015
    locator: the leader, scout and commander processes and the slot invariants
---

Multi-Paxos runs a sequence of [Paxos](/paxos/) instances, one for each slot of a log, to build a [replicated state machine](/replicated-state-machine/). A stable leader runs phase 1 once, with one [ballot number](/ballot-number/), for all slots at the same time. After that each new command needs only phase 2, so it is chosen two message delays after the leader sends it. The model is the one of Paxos: [asynchronous](/asynchronous-model/) messages and [crash failures](/crash-failure/), with safety in every run and progress when one leader runs alone.

## In plain words

A group keeps a numbered list of commands, the log, and all members must agree on the command in each position. One member acts as the leader.

When a member becomes leader, it asks a majority once: "promise to ignore leaders older than me, and tell me everything you have voted for in each position". For each position where someone reported a vote, the leader re-proposes the reported value with the newest ticket. For each empty position below the last reported one, it proposes a "do nothing" command, so the log has no holes. After this single round of questions, the leader assigns each new command to the next free position and asks the members to vote. A majority of votes chooses the command.

Each member runs the commands in position order, and it waits when a position is not decided yet.

## The problem

**Model.** There are $n$ acceptors, some processes that can act as leader, and $l$ learners. The model is the [asynchronous model](/asynchronous-model/) with [crash failures](/crash-failure/). Acceptors keep their state on stable storage. Messages can be lost, duplicated and reordered.

**Goal.** Choose a value for each slot $s = 0, 1, 2, \ldots$ of a log. The values are client commands or the special command no-op. For each slot $s$:

- **Agreement**: at most one value is chosen for slot $s$.
- **Validity**: a chosen value is a submitted command or no-op.
- **Liveness** (with a stable leader, see below): each command that a stable leader receives is chosen in some slot.

Each learner applies the chosen values in slot order. Agreement in each slot makes all applied logs prefixes of one log, which is the [total order broadcast](/total-order-broadcast/) that a replicated state machine needs.

## The algorithm

A leader $p$ has a ballot $b$, a flag *active*, and the next free slot *next*. An acceptor has one value *promised* for all slots and a map *accepted* from slots to (ballot, value) pairs.

```pseudo id=main
LEADER p
L1  on start, or on a timeout:  b ← (r, p), with r larger than each round that p has seen; active ← false
L2      send PREPARE(b) to all acceptors                             ▷ phase 1 for all slots
L3  on PROMISE(b, accepted_a) from a majority Q of acceptors:
L4      for each slot s reported in Q:  best[s] ← the reported value with the largest ballot in s
L5      for each slot s < top, where top is 1 + the largest reported slot (0 if none):  send ACCEPT(b, s, best[s], or no-op if s has no report)
L6      active ← true; next ← top
L7  on command c, if active:  s ← next; next ← next + 1
L8      send ACCEPT(b, s, c) to all acceptors                         ▷ phase 2 only

ACCEPTOR a
L9  on PREPARE(b):  if promised = ⊥ or b > promised then
L10     promised ← b; send PROMISE(b, accepted) to the leader       ▷ else NACK(promised)
L11 on ACCEPT(b, s, v):  if promised = ⊥ or b ≥ promised then
L12     promised ← b; accepted[s] ← (b, v); send ACCEPTED(b, s, v) to all learners   ▷ else NACK(promised)

LEARNER
L13 on ACCEPTED(b, s, v) from a majority of acceptors (counted per b and s):  learned[s] ← v
L14     while learned[k] is set, where k is the number of applied commands:  apply learned[k]
```

**Phase 1 for all slots.** A promise for ballot $b$ covers every slot, including slots that no one has used yet. So a single PREPARE and one PROMISE from each acceptor of a majority prepare an unbounded number of Paxos instances. The PROMISE carries the last vote of the acceptor in each slot.

**Recovery of the old slots.** For each slot with a reported vote, the leader must re-propose the value with the largest ballot in that slot (line L4). This is the rule of Paxos, applied slot by slot. A slot below *top* with no report in $Q$ is a gap: no value can have been chosen there, so the leader fills it with no-op (line L5). Without the no-op, the learners could never apply any slot after the gap.

**Steady state.** While the leader keeps its ballot, each command costs one ACCEPT round (lines L7 and L8). The leader can send many ACCEPT messages without waiting, and acceptors accept them in any order.

**Leader change.** A NACK with a larger ballot tells a leader that it is deposed. Any process can then start a new ballot after a timeout. Each new leader runs line L1 again. Clients retry commands that they do not see applied, so a command can appear in two slots. A state machine that must run each command once keeps a table of the last request id per client.

## Example

Three acceptors $A_0, A_1, A_2$ and two leaders. Leader $L_0$ runs phase 1 with ballot $(1,0)$ and becomes active. It sends three commands $a, b, c$ to slots 0, 1 and 2.

| step | event | $A_0$ | $A_1$ | $A_2$ |
|---|---|---|---|---|
| 1 | ACCEPT($(1,0)$, 0, $a$) reaches all acceptors | 0: $a$ | 0: $a$ | 0: $a$ |
| 2 | slot 1 is lost; ACCEPT($(1,0)$, 2, $c$) reaches only $A_2$ | 0: $a$ | 0: $a$ | 0: $a$, 2: $c$ |
| 3 | $L_0$ crashes; $L_1$ sends PREPARE($(1,1)$); $A_1$ and $A_2$ promise | | | |
| 4 | $L_1$ gets slot 0 → $a$ and slot 2 → $c$; top = 3; slot 1 has no report | | | |
| 5 | $L_1$ sends ACCEPT($(1,1)$, $s$, ·) for $a$, no-op and $c$ | 0: $a$, 1: no-op, 2: $c$ | same | same |

Slot 0 was already chosen in step 1, and it keeps $a$. Slot 2 had only one vote, so $c$ was not chosen, but $L_1$ may keep it. Slot 1 becomes no-op. All learners apply $a$, no-op, $c$, and the next command of $L_1$ goes to slot 3.

## Correctness

Each slot $s$ is one run of single-decree Paxos. Phase 1 for ballot $b$ is shared by all slots: a promise for $b$ is a promise for $b$ in each slot, and the report of acceptor $a$ for slot $s$ is its last vote in slot $s$. Lines L4 and L5 pick the value of slot $s$ exactly as Paxos does. A slot with no report from the majority $Q$ falls under case (a) of the invariant P2c, where any value is allowed, so no-op is safe there. A leader sends at most one value per slot in each ballot, because lines L5 and L7 use disjoint slots and *next* only grows. So the proof of [Paxos](/paxos/) applies to each slot, and at most one value is chosen per slot. The full proof is below.

**Liveness.** Progress needs a single leader after some time, as in Paxos. With [partial synchrony](/partial-synchrony/), an [Ω failure detector](/omega-failure-detector/) for the leader choice, a majority of acceptors up, and retransmission of lost messages, each command that the stable leader receives is chosen. Two leaders that keep deposing each other can stop progress forever, but they cannot break agreement.

## Complexity

All costs are for the steady state with a stable leader and no failures.

- **Message delays.** 2 from the leader to the learners: ACCEPT and ACCEPTED. Seen by a client that sends its command to the leader and gets the reply from the leader, which is also a learner, the cost is 4 delays: request, ACCEPT, ACCEPTED, reply. Single-decree Paxos with a fresh phase 1 needs 4 delays from the proposer to the learners.
- **Messages per command.** $n$ ACCEPT and $n l$ ACCEPTED, so $n + nl = \Theta(nl)$. With $n = 3$ and $l = 3$ this is 12. When the leader is the only learner and tells the others later, it is $2n$.
- **Stable storage.** One write per acceptor per command, before it sends ACCEPTED. Batching many commands in one write is common.
- **Leader change.** One phase 1 round trip, plus one ACCEPT round for the slots that the old leader left open. The PROMISE messages carry all votes, so a real system cuts the log with [log compaction](/log-compaction/) and sends votes only from the first slot that the leader does not know as chosen.
- **Leader load.** All commands pass through the leader, so it limits throughput. [Mencius](/mencius/) and [EPaxos](/epaxos/) spread this load.

## Properties

- **Safe under asynchrony.** Agreement per slot holds in every run, as in Paxos.
- **Pipelined.** The leader can have many slots in phase 2 at the same time. Commands are chosen out of order but applied in slot order.
- **No-ops close gaps.** A new leader turns each hole into a no-op, so learners never wait forever on an empty slot.
- **Reads.** A read must also be ordered. Either it goes through a slot like a write, or the leader holds a [leader lease](/leader-lease/) and answers from its local state.

## Variants and improvements

- **[Raft](/raft/).** The same core with a stronger rule for the leader: only an acceptor with a log that is as up to date as a majority can become leader, so the new leader never needs to fetch old values. Its logs have no gaps.
- **[Viewstamped Replication](/viewstamped-replication/) and [Zab](/zab/).** Leader-based protocols with a view change that moves the most recent log to the new leader.
- **[Flexible Paxos](/flexible-paxos/).** Phase 1 runs rarely, so a large phase 1 quorum and a small phase 2 quorum make the steady state cheaper.
- **[Leader lease](/leader-lease/).** Local reads at the leader without a round of messages.
- **[Cluster reconfiguration](/cluster-reconfiguration/).** A command in the log changes the set of acceptors for later slots.
- **[Mencius](/mencius/).** Each server leads a fixed share of the slots.

## When to use it

Use Multi-Paxos to replicate a log or a state machine across a small group of servers, three or five in practice, when the system must stay correct under any timing and stay available while a majority is up. A single leader is simple and fast in one data center. In a wide area network, with clients near different servers, a leaderless or rotating protocol such as [EPaxos](/epaxos/) or [Mencius](/mencius/) can give lower latency.

## Pitfalls

- **Phase 1 for one slot only.** Line L2 must cover all slots. A PROMISE that reports only some slots lets a new leader overwrite a chosen value in a slot it did not ask about.
- **Gaps left open.** Without the no-op of line L5, a slot with no chosen value blocks line L14 at every learner forever.
- **Reusing a slot.** Line L7 must give each command a fresh slot. Two values in the same slot in one ballot break agreement.
- **Learners that apply out of order.** Line L14 applies slot $k$ only after all slots before it. Commands are chosen out of order, but the state machine must see them in slot order.
- **Reads from a deposed leader.** An old leader that answers reads from its state without a lease, or after its lease ends, can return stale data. Line L1 of a new leader does not stop the old one.
- **Logs that grow forever.** The PROMISE of line L10 sends all votes. Without a snapshot and [log compaction](/log-compaction/), leader changes get slower over time.

## Implementations

## History

Lamport's Part-Time Parliament (submitted in 1990, published in 1998) has a multi-decree parliament in which a president runs the first phase once for all future decrees. Paxos Made Simple (2001) gave the same construction for a state machine, with no-ops for gaps. The name Multi-Paxos came into wide use later. Chandra, Griesemer and Redstone described the engineering of a Multi-Paxos system for Chubby at Google in 2007, with master leases, snapshots and group membership.

## References
