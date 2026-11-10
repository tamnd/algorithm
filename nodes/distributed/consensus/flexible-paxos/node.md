---
tag: 4PEKRH
kind: algorithm
slug: flexible-paxos
name: Flexible Paxos
aliases:
- flexible quorums
- FPaxos
area: distributed/consensus
level: research
summary: Phase-one and phase-two quorums need only intersect each other, not each other within the phase.
solves: [consensus-problem]
model: asynchronous-model
complexity:
  vars: {n: the number of acceptors, l: the number of learners}
  time: {best: Θ(1)}
  messages: {best: Θ(n l)}
  space: {extra: Θ(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 2016
  people: [Heidi Howard, Dahlia Malkhi, Alexander Spiegelman]
  note: Presented at OPODIS 2016. Vertical Paxos (2009) had already used read and write quorums that only need to meet each other.
prereqs: [paxos, quorum, quorum-intersection]
see_also: [multi-paxos, fast-paxos, vertical-paxos, cheap-paxos, quorum-replication, byzantine-quorum-system]
sources:
  - paper: doi:10.4230/LIPIcs.OPODIS.2016.25
    title: Heidi Howard, Dahlia Malkhi and Alexander Spiegelman, Flexible Paxos, quorum intersection revisited, OPODIS 2016, LIPIcs 70, 25:1-25:14, 2016
    locator: the statement of the quorum intersection requirement for Multi-Paxos, its safety argument, and the examples with grid quorums and with simple counting quorums
  - paper: doi:10.1145/1582716.1582783
    title: Leslie Lamport, Dahlia Malkhi and Lidong Zhou, Vertical Paxos and primary-backup replication, PODC 2009, 312-313
    locator: the read quorums and write quorums of each ballot
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 2 (the invariant P2c, which uses only that a majority of phase 1 meets the majority that chose a value)
---

Flexible Paxos is [Paxos](/paxos/) with two kinds of [quorum](/quorum/): phase 1 quorums $Q_1$ and phase 2 quorums $Q_2$, where each $Q_1$ must meet each $Q_2$, but two $Q_1$ need not meet and two $Q_2$ need not meet. With quorums given by size, the rule is $|Q_1| + |Q_2| > n$. Because a stable leader runs phase 1 rarely and phase 2 for every command, a large $Q_1$ and a small $Q_2$ make the common case cheaper. The model is the one of Paxos: [asynchronous](/asynchronous-model/) messages and [crash failures](/crash-failure/).

## In plain words

Paxos uses a majority of the voters at both steps. A majority is used so that any two groups share a voter. Flexible Paxos asks where that shared voter is really needed.

The answer: only between the group that votes on a value and the group that a later leader asks about old votes. Two groups that vote on values never need to share a voter, because each leader asks first. Two groups that a leader asks never need to share a voter either.

So a system can ask a large group when a new leader starts, which is rare, and a small group for each command, which is frequent. With ten voters, a leader could ask nine of them once, and then need only two votes for each command.

## The problem

**Model.** As in Paxos: $n$ acceptors, proposers and learners, [asynchronous](/asynchronous-model/) timing, [crash failures](/crash-failure/) with stable storage, and messages that can be lost, duplicated and reordered. The goal is the [consensus problem](/consensus-problem/) with agreement and validity in every run, and termination when one proposer runs alone.

**Quorum systems.** Let $\mathcal{Q}_1$ and $\mathcal{Q}_2$ be two families of sets of acceptors. A value is *chosen* when every acceptor of some $Q_2 \in \mathcal{Q}_2$ has accepted it in the same ballot. The requirement is

$$\forall Q_1 \in \mathcal{Q}_1,\ \forall Q_2 \in \mathcal{Q}_2:\quad Q_1 \cap Q_2 \ne \emptyset.$$

If $\mathcal{Q}_1$ is all sets of at least $q_1$ acceptors and $\mathcal{Q}_2$ is all sets of at least $q_2$ acceptors, the requirement holds if and only if $q_1 + q_2 > n$. Two sets of sizes $q_1$ and $q_2$ can be disjoint exactly when $q_1 + q_2 \le n$.

## The algorithm

The code is that of Paxos, with the two quorum tests in place of the majority tests.

```pseudo id=main
PROPOSER p, with input x_p
L1  on start, or on a timeout:  b ← (r, p) with a fresh round r; send PREPARE(b) to all acceptors
L2  on PROMISE(b, vb, vv) from acceptor a, if b is current and p is in phase 1:  P ← P ∪ {(a, vb, vv)}
L3      if the senders in P include a phase 1 quorum then
L4          v ← the vv with the largest vb in P, or x_p if P reports no vote
L5          send ACCEPT(b, v) to all acceptors

ACCEPTOR a
L6  on PREPARE(b):  if b > promised then promised ← b; send PROMISE(b, vb, vv), else send NACK(promised)
L7  on ACCEPT(b, v):  if b ≥ promised then promised ← b; vb ← b; vv ← v; send ACCEPTED(b, v) to all learners, else send NACK(promised)

LEARNER
L8  on ACCEPTED(b, v):  when the senders for ballot b include a phase 2 quorum, learn v
```

**Counting quorums.** With $n$ acceptors, choose $q_2$ from 1 to $n$ and set $q_1 = n - q_2 + 1$. Majorities ($q_1 = q_2 = \lfloor n/2 \rfloor + 1$) are one choice among many.

**Grid quorums.** Place $n = r \cdot c$ acceptors in a grid with $r$ rows and $c$ columns. A phase 1 quorum is a full column ($r$ acceptors) and a phase 2 quorum is a full row ($c$ acceptors). Each row meets each column in one cell, so the requirement holds, though two rows never meet. With a $3 \times 3$ grid, phase 2 needs 3 of 9 acceptors, while a majority needs 5.

**In Multi-Paxos.** In [Multi-Paxos](/multi-paxos/) a leader runs phase 1 once for all slots, and then each command needs only one phase 2 quorum. The same requirement suffices there: each phase 1 quorum must meet each phase 2 quorum.

## Example

Four acceptors with $q_1 = q_2 = 2$, which breaks the rule since $2 + 2 = 4$ is not more than 4. Proposer $P_0$ has $x$ and $P_1$ has $y$, and the network splits $\{A_0, A_1\}$ from $\{A_2, A_3\}$.

| step | event | $A_0$ | $A_1$ | $A_2$ | $A_3$ |
|---|---|---|---|---|---|
| 1 | $P_0$ gets promises for $(1,0)$ from $A_0, A_1$: a phase 1 quorum with no votes | (1,0) | (1,0) | | |
| 2 | $P_1$ gets promises for $(1,1)$ from $A_2, A_3$: a phase 1 quorum with no votes | (1,0) | (1,0) | (1,1) | (1,1) |
| 3 | $P_0$ sends ACCEPT((1,0), $x$); $A_0, A_1$ accept: $x$ is chosen | $x$ | $x$ | (1,1) | (1,1) |
| 4 | $P_1$ sends ACCEPT((1,1), $y$); $A_2, A_3$ accept: $y$ is chosen | $x$ | $x$ | $y$ | $y$ |

With $q_1 = 3$ and $q_2 = 2$ instead, $P_1$ would need a promise from $A_0$ or $A_1$ in step 2, and it would see $x$ (or stop $A_0$ and $A_1$ from accepting $x$).

Now take five acceptors with $q_1 = 4$ and $q_2 = 2$. A leader finishes phase 1 with $A_0, \ldots, A_3$. Then $A_2$, $A_3$ and $A_4$ crash. The leader still gets $x$ chosen by $A_0$ and $A_1$, while Paxos with majorities would stop. But no new leader can finish phase 1 until two of the crashed acceptors return.

## Correctness

The safety proof of Paxos uses quorum intersection in only one place: the phase 1 quorum $S$ of a later ballot must share an acceptor with the quorum $C$ that chose a value in an earlier ballot. Here $S$ is a phase 1 quorum and $C$ is a phase 2 quorum, so the requirement $Q_1 \cap Q_2 \ne \emptyset$ is exactly what that step needs. The invariant P2c and the induction on ballots go through unchanged. The full proof is below.

The requirement is also necessary for safety in general: if some $Q_1$ and $Q_2$ are disjoint, the example above, with $Q_1$ and $Q_2$ in the roles of $\{A_2, A_3\}$ and $\{A_0, A_1\}$, chooses two values.

**Liveness.** A new leader needs a live phase 1 quorum, and each command needs a live phase 2 quorum. With counting quorums, a leader change survives $n - q_1 = q_2 - 1$ crashed acceptors, and the steady state survives $n - q_2$. With majorities both numbers are $\lceil n/2 \rceil - 1$.

## Complexity

The message counts are those of Paxos: $3n + nl$ messages per decision with all acceptors contacted, and $n + nl$ per command in the steady state of Multi-Paxos. The gain is in waiting and in load:

- **Latency.** A leader waits for the $q_2$-th fastest reply in phase 2, not for the $(\lfloor n/2 \rfloor + 1)$-th.
- **Load.** If the leader sends phase 2 messages only to a phase 2 quorum, each command loads $q_2$ acceptors, not a majority.
- **Fault tolerance.** The steady state and the leader change tolerate different numbers of crashes, as in the liveness paragraph.

| $n$ | $q_1$ | $q_2$ | crashes tolerated by a leader change | crashes tolerated in the steady state |
|---|---|---|---|---|
| 5 | 3 | 3 | 2 | 2 |
| 5 | 4 | 2 | 1 | 3 |
| 6 | 4 | 3 | 2 | 3 |
| 9 | 7 | 3 | 2 | 6 |
| 9 (3 × 3 grid) | a column | a row | at least 2 | at least 2 |

## Properties

- **Weaker requirement, same algorithm.** No message or rule changes. Only the quorum tests of lines L3 and L8 change.
- **Majorities are a special case.** With $q_1 = q_2 = \lfloor n/2 \rfloor + 1$ it is Paxos.
- **Even sizes.** With $n$ even, $q_1 = n/2 + 1$ and $q_2 = n/2$ saves one reply per command over a majority.
- **Safety does not depend on timing**, as in Paxos.

## Variants and improvements

- **[Vertical Paxos](/vertical-paxos/).** Each ballot has its own read quorums and write quorums, and a master changes the configuration.
- **[Cheap Paxos](/cheap-paxos/).** Uses a small fixed set of main acceptors as a quorum while all are up.
- **[Fast Paxos](/fast-paxos/).** Needs a stronger, three-way intersection for fast rounds.
- **Quorums per ballot.** Each ballot can use its own quorum system, as long as each phase 1 quorum of a ballot meets each phase 2 quorum of every smaller ballot. The proof below goes through with this weaker rule, because it compares a phase 1 quorum of ballot $b$ only with the phase 2 quorum of a smaller ballot $b_0$.

## When to use it

Use flexible quorums in a Multi-Paxos or [Raft](/raft/) style system with a stable leader, when the cost of phase 2 matters most and leader changes are rare. It helps most with many replicas, where a majority for each command is costly. It is a poor choice when leader changes are frequent or when the system must elect a new leader after many crashes.

## Pitfalls

- **Phase 2 quorums that meet only each other.** Line L3 must use phase 1 quorums that meet every phase 2 quorum. Small $q_1$ and $q_2$ with $q_1 + q_2 \le n$ give the split brain of the example.
- **Counting phase 1 quorums in phase 2.** Line L8 must test a phase 2 quorum. A learner that accepts any majority is correct only when majorities are phase 2 quorums.
- **Leader election with a small quorum.** In Raft style systems the vote for a leader is phase 1. Electing a leader with $q_2$ votes, because "a quorum is a quorum", breaks safety.
- **Forgetting the steady-state trade-off.** With $q_2$ small, a leader change needs nearly all acceptors. A cluster can then keep running but never recover from a leader crash.

## Implementations

## History

Howard, Malkhi and Spiegelman presented Flexible Paxos at OPODIS 2016, with an arXiv version in the same year. They observed that the Multi-Paxos safety argument needs only intersection between the quorums of the two phases. Vertical Paxos by Lamport, Malkhi and Zhou (2009) had already used separate read and write quorums for each ballot.

## References
