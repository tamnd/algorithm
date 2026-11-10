---
tag: DSVH0K
kind: algorithm
slug: three-phase-commit
name: Three-phase commit
aliases:
- 3PC
area: distributed/consensus
level: advanced
summary: Two-phase commit with an extra pre-commit round. It does not block under crash failures in a synchronous system with exact failure detection, but it is unsafe under partitions.
solves: [atomic-commit]
model: synchronous-model
complexity:
  vars: {n: the number of participants, f: the number of crashed processes}
  time: {best: Θ(1), worst: O(f)}
  messages: {best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1981
  people: [Dale Skeen]
  note: Skeen gave the theorem that characterizes non-blocking commit protocols and derived three-phase commit from it in a SIGMOD paper of 1981.
prereqs: [two-phase-commit, atomic-commit, synchronous-model, crash-failure]
see_also: [paxos-commit, split-brain, failure-detector, partial-synchrony, consensus-problem, cap-theorem]
sources:
  - paper: doi:10.1145/582318.582339
    title: Dale Skeen, Nonblocking commit protocols, Proceedings of the ACM SIGMOD International Conference on Management of Data, 1981, pages 133 to 142
    locator: the fundamental nonblocking theorem (concurrency sets), its corollary for protocols that are synchronous within one state transition, and the three-phase protocol derived from it
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 7 (three-phase commit and its termination protocol)
  - paper: "Jim Gray and Leslie Lamport, Consensus on transaction commit, ACM Transactions on Database Systems 31(1), 2006"
    locator: the discussion of three-phase commit and of the need for a reliable failure detector
---

Three-phase commit (3PC) is a protocol for the [atomic commit](/atomic-commit/) problem that adds a *pre-commit* round between the vote and the commit of [two-phase commit](/two-phase-commit/). Skeen (1981) derived it from a theorem: a commit protocol is non-blocking when no state of a process can coexist with both a commit and an abort elsewhere, and no state that is not yet committable can coexist with a commit. The pre-commit state removes the uncertain state of 2PC that breaks this rule, so the live processes can always finish on their own. This holds with [crash failures](/crash-failure/) in a [synchronous system](/synchronous-model/) with exact failure detection; with network partitions, 3PC can commit on one side and abort on the other.

## In plain words

Two-phase commit has a bad moment. A participant has said "yes" and waits. The organizer vanishes. The participant cannot tell whether the organizer said "go" or "cancel" to someone else, so it must wait.

Three-phase commit adds a warning step. After everyone says "yes", the organizer first tells everyone "get ready to go". Only when all have heard this does it say "go". So nobody says "go" while anyone still waits without the warning.

Now the survivors can finish without the organizer. They compare notes. If someone already cancelled, all cancel. If someone already went, all go. If someone heard "get ready", nobody can have cancelled, so all go. If nobody heard "get ready", nobody can have gone, so all cancel.

This works only when a silent process has truly stopped. If the network splits, each half thinks the other stopped, and the halves can decide differently.

## The problem

A transaction runs at $n$ participants and a coordinator. Each participant votes yes or no. The goal is [atomic commit](/atomic-commit/) with one more property, non-blocking: every process that does not crash eventually decides, whatever the other processes do.

The model is the one of Skeen's result. It is the [synchronous model](/synchronous-model/): processes run in lock-step rounds, and a message sent in one round arrives in the next. Processes fail only by crashing. The failure detector is exact: one round after a process crashes, every live process knows it. The network does not lose messages and does not partition. These assumptions matter: no protocol is non-blocking in an [asynchronous](/asynchronous-model/) system (see [atomic commit](/atomic-commit/)).

## The algorithm

Each process is in one of five states: q (initial), w (voted yes, waiting), p (pre-committed), c (committed) and a (aborted). The leader is the coordinator at the start, and at all times the live process with the smallest id.

```pseudo id=main
COORDINATOR
L1  state ← w; send VOTE-REQ to all participants
L2  PARTICIPANT, on VOTE-REQ: if it votes yes then state ← w, send YES; else state ← a, send NO
L3  COORDINATOR, one round trip later: if YES came from all then state ← p, send PRE-COMMIT to all; else state ← a, send ABORT to all
L4  PARTICIPANT, on PRE-COMMIT: state ← p; send ACK
L5  COORDINATOR, one round trip later: state ← c; send COMMIT to all       ▷ missing ACKs come from crashed processes
L6  PARTICIPANT, on COMMIT: state ← c; on ABORT: state ← a
TERMINATION, when the failure detector reports that the leader crashed
L7  the new leader is the live process with the smallest id; if it has decided, it sends its decision to all
L8  else it sends STATE-REQ to all, and each live process answers with its state (one round trip)
L9  if some state is a then state ← a, send ABORT
L10 else if some state is c then state ← c, send COMMIT
L11 else if no state is p then state ← a, send ABORT
L12 else state ← p, send PRE-COMMIT; one round trip later state ← c, send COMMIT
```

**The pre-commit state.** In 2PC, a participant in w can coexist with a process that committed and also with one that aborted, so it cannot decide alone. In 3PC, the coordinator commits (line L5) only after every live participant has entered p (line L4), and the protocol is synchronous, so the states of two processes are never more than one transition apart. This gives the concurrency sets:

| state of a live process | states that other live processes can be in at the same time |
|---|---|
| q | q, w, a |
| w | q, w, p, a |
| p | w, p, c |
| c | p, c |
| a | q, w, a |

No set has both c and a. The set of w has no c, and the set of p has no a. These are the two conditions of Skeen's theorem, so a survivor can always pick a decision that agrees with every possible state of the crashed processes. A crashed process keeps its last state, so a process that crashed in w can sit next to live processes that commit. That is harmless, because it decides nothing while it is down.

**Termination (lines L7 to L12).** If the leader crashes, the next leader collects the states of the live processes and applies the rules in order. A state a or c anywhere fixes the decision. With a p and no c or a, no process can have aborted (the set of p), so the leader commits, but it first moves the others to p (line L12), so that the table stays true if it crashes too. With no p, no process can have committed (the set of w), so the leader aborts. If the new leader crashes, the next one starts again.

**Recovery.** A process that recovers after a crash cannot decide alone if its log says w or p, since the others may have decided either way while it was down. It must ask the processes that stayed up.

## Example

Three participants vote yes and nothing fails: the states go from w (round 0) to p (round 2) to c (round 4).

The run below shows why the model matters. All vote yes. In round 2 the coordinator C sends PRE-COMMIT, but a partition starts in that round and splits $\{C, P_1\}$ from $\{P_2, P_3\}$. Each side sees the other side as crashed.

| round | C | $P_1$ | $P_2$ | $P_3$ | event |
|---|---|---|---|---|---|
| 0 | w | q | q | q | C sends VOTE-REQ |
| 1 | w | w | w | w | all vote yes |
| 2 | p | w | w | w | C sends PRE-COMMIT; only $P_1$ gets it. $P_2$ thinks C crashed, becomes leader and sends STATE-REQ |
| 3 | p | p | w | w | $P_1$ sends ACK; $P_3$ answers w |
| 4 | c | p | a | a | C commits (it sees $P_2$ and $P_3$ as crashed). $P_2$ sees only w, so line L11 aborts |
| 5 | c | c | a | a | final: one side committed, the other aborted |

Each side followed the rules exactly. The failure detector was wrong: $P_2$ and $P_3$ were alive. No commit protocol avoids this: with a partition, a non-blocking protocol must let each side decide, and the two sides cannot know what the other decided.

## Correctness

The proof is a sketch. In each round all live processes agree on one leader, the live process with the smallest id, so at most one process sends decision messages at a time. A new leader collects states only after the decision messages of the crashed leader have arrived, so the states it sees are current and differ by at most one transition. By induction on the rounds, a process in c forces every live process to p or c, and a process in a forbids any live process in p or c. Each termination rule then agrees with every state that a crashed process can be in. Each leader that does not crash finishes within 5 rounds, so the live processes decide after a number of rounds linear in the number of crashes. The proof sketch is below.

## Complexity

Without failures, 3PC takes 5 message delays and $5n$ messages: VOTE-REQ, the votes, PRE-COMMIT, the ACKs and COMMIT, one per participant each. That is one round trip more than 2PC. Each leader crash adds a termination run of at most 5 rounds (STATE-REQ, the states, PRE-COMMIT, the ACKs and COMMIT) and up to $4n$ messages, so with $f$ crashes the decision comes within $O(f)$ rounds.

## Properties

- Non-blocking with crash failures, in a synchronous system with an exact failure detector and no partitions.
- Safe in that model for any number of crashes, as long as the processes that crash do not recover during the protocol.
- Not safe when the failure detector can be wrong: under partitions, or in an asynchronous or partially synchronous network with timeouts.
- One more round trip than 2PC in the common case.

## Variants and improvements

- **Quorum-based 3PC.** A group of processes may decide only with a [quorum](/quorum/) of processes in the right states, so that two sides of a partition cannot both decide. This makes the protocol safe under partitions, but the side without a quorum blocks.
- **Consensus-based commit.** [Paxos Commit](/paxos-commit/) of Gray and Lamport runs one [Paxos](/paxos/) instance for each participant's vote. It is safe in the [asynchronous model](/asynchronous-model/) and does not block while a majority of acceptors is up, which is what 3PC tries to give.
- **Two-phase commit with a replicated coordinator.** Storing the coordinator's decision on [Raft](/raft/) or [Multi-Paxos](/multi-paxos/) has the same effect in practice, and many systems take this route instead of 3PC.

## When to use it

3PC is mostly of historical and teaching value. Its guarantee needs an exact failure detector and no partitions, which real networks do not give, and under a partition it can lose atomicity, which is worse than the blocking of 2PC. Use it only where the timing assumptions hold, for example within one machine with a hardware-backed failure detector. For a commit that is safe and does not block while a majority is up, use 2PC on a replicated coordinator or [Paxos Commit](/paxos-commit/).

## Pitfalls

- **Treating a timeout as a crash.** This is the partition run above. A timeout says that a process is slow or unreachable, not that it stopped.
- **Committing without moving the others to p first.** In line L12, a termination leader that commits at once can crash after the commit and before anyone else hears, and the next leader, which sees only w, aborts. The pre-commit round is needed in the termination protocol too.
- **A recovered process that decides alone.** A process that recovers in w or p must ask. In w it cannot abort alone, because the survivors may have committed.
- **Counting 3PC as consensus.** 3PC decides commit or abort given the votes; it does not make processes in an asynchronous system agree, and it does not escape the [FLP impossibility](/flp-impossibility/) result.

## Implementations

## History

Dale Skeen studied which commit protocols can avoid blocking. In his 1981 SIGMOD paper he defined the concurrency set of a local state, proved that a protocol is non-blocking if and only if no concurrency set holds both a commit and an abort state and no noncommittable state has a commit state in its concurrency set, and derived the three-phase protocol as the smallest change to 2PC that meets these conditions. Bernstein, Hadzilacos and Goodman presented 3PC with its termination and recovery protocols in their 1987 book. Gray and Lamport later used the consensus view to give Paxos Commit, which needs no exact failure detector.

## References
