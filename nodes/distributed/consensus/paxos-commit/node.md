---
tag: KZW5JY
kind: algorithm
slug: paxos-commit
name: Paxos Commit
area: distributed/consensus
level: research
summary: Non-blocking atomic commit where each participant's decision is replicated with Paxos.
solves: [atomic-commit]
model: asynchronous-model
complexity:
  vars: {N: the number of resource managers, F: the number of acceptor failures tolerated}
  time: {best: Θ(1)}
  messages: {best: Θ(N F)}
  space: {extra: Θ(N)}
properties: {deterministic: true, recursive: false}
history:
  year: 2006
  people: [Jim Gray, Leslie Lamport]
  note: Published in ACM Transactions on Database Systems in 2006, after a Microsoft Research report of 2003.
prereqs: [paxos, two-phase-commit, atomic-commit]
see_also: [two-phase-commit, three-phase-commit, atomic-commit, paxos, multi-paxos, fast-paxos, consensus-problem]
sources:
  - paper: doi:10.1145/1132863.1132867
    title: Jim Gray and Leslie Lamport, Consensus on transaction commit, ACM Transactions on Database Systems 31(1), 133-160, 2006
    locator: the Paxos Commit algorithm with one Paxos instance per resource manager and ballot 0 owned by the resource manager, the cost table that compares it with Two-Phase Commit, the remark that Two-Phase Commit is the case F = 0, and the Faster Paxos Commit variant
  - paper: "Jim Gray and Leslie Lamport, Consensus on transaction commit, Microsoft Research technical report MSR-TR-2003-96, 2004"
    locator: the TLA+ specifications of the transaction commit problem, Two-Phase Commit and Paxos Commit in the appendix
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, December 2001"
    locator: Section 2 (the two phases of a single Paxos instance)
---

Paxos Commit solves [atomic commit](/atomic-commit/) without blocking. Each of the $N$ resource managers (RMs) of a transaction votes *Prepared* or *Aborted*, and the vote is not sent to one coordinator, as in [Two-Phase Commit](/two-phase-commit/), but is chosen by its own instance of [Paxos](/paxos/), run by $2F + 1$ acceptors. The transaction commits if every instance chooses Prepared, and aborts otherwise. If the leader fails, another leader finishes the instances, so the protocol makes progress as long as a majority of the acceptors and one leader are up. Gray and Lamport showed that Two-Phase Commit is the special case $F = 0$. The model is [asynchronous](/asynchronous-model/) with [crash failures](/crash-failure/).

## In plain words

A transaction touches several databases. Each one must say "ready" or "no", and all must then do the same thing: commit everywhere or abort everywhere.

In Two-Phase Commit, every database sends its answer to one coordinator. If the coordinator crashes at the wrong moment, the databases that said "ready" must wait for it, with their data locked.

Paxos Commit sends each answer to a small group of record keepers instead. A majority of them must write it down. If the coordinator crashes, a new one reads the answers from a majority of the record keepers. A database whose answer no one recorded is treated as "no", and the transaction aborts. Nobody waits for a crashed coordinator.

## The problem

**Model.** $N$ RMs, $2F + 1$ acceptors, and one or more leaders, with asynchronous messages that may be delayed, reordered and duplicated, and crash failures. Each process has stable storage.

**Goal.** The [atomic commit](/atomic-commit/) problem: every RM that decides reaches the same outcome (agreement), commit is possible only if every RM voted Prepared (validity), and if all vote Prepared and nothing fails, the outcome is commit (non-triviality). In addition, the protocol must not block: if at most $F$ acceptors fail and some leader is alive and eventually alone, every live RM decides.

**Instances.** There is one Paxos instance per RM. In instance $r$, ballot 0 belongs to RM $r$, so RM $r$ can send its phase 2a message at once, without a phase 1. Higher ballots belong to leaders.

## The algorithm

```pseudo id=main
L1  the first RM sends BeginCommit to the leader
L2  leader, on BeginCommit:  send Prepare to every other RM
L3  RM r, on Prepare (the first RM at once):  choose Prepared or Aborted; write it to storage; send 2a(r, ballot 0, vote) to F + 1 acceptors
L4  acceptor, on 2a(r, b, v):  if b is not below its promise, accept (b, v) in instance r
L5  acceptor, once it has accepted ballot 0 in every instance:  send one 2b with all N votes to the leader
L6  leader:  instance r has chosen v when F + 1 acceptors report v at the same ballot for r
L7  leader:  if every instance chose Prepared, decide Commit; if some instance chose Aborted, decide Abort; send the outcome to all RMs

RECOVERY, by a leader whose timeout fires
L8  choose a ballot b > 0 above every ballot it knows; send 1a(b) to all acceptors
L9  acceptor, on 1a(b) with b above its promise:  promise b; reply 1b(b, its accepted (ballot, value) for each instance)
L10 leader, on 1b from F + 1 acceptors:  for each instance, the value with the highest ballot, or Aborted if none
L11 send 2a(b, those values) to all acceptors; acceptors accept (L4) and reply 2b to the leader, who goes on at L6

L12 RM, on the outcome:  commit or abort, and remember the outcome
```

**Normal case** (lines L1 to L7). The leader asks the RMs to vote, each RM sends its vote straight to the acceptors as a ballot-0 accept message, and the acceptors report to the leader. The vote is chosen once $F + 1$ acceptors have it. Five message delays pass from the first RM's request to the outcome.

**Recovery** (lines L8 to L11). A new leader runs phase 1 of Paxos for all instances at once. For an instance where an acceptor reports a vote, it must keep the vote with the highest ballot; for an instance with no vote, it proposes Aborted. This is the only value a leader may propose on its own: a leader never invents a Prepared vote.

**Two-Phase Commit as a special case.** With $F = 0$ there is one acceptor. Put it on the leader's node: its 2b message becomes local, and the first RM's BeginCommit can travel with its 2a message. What remains is Prepare, the votes and the outcome: the $3N - 1$ messages of Two-Phase Commit, and the acceptor is the coordinator's stable storage. With one acceptor, its failure blocks the protocol, as in Two-Phase Commit.

## Example

$N = 3$ RMs, $F = 1$, acceptors $A_1, A_2, A_3$, leaders $L$ and $L'$.

| step | event | instances |
|---|---|---|
| 1 | RM1 writes Prepared, sends 2a(1, 0, Prepared) to $A_1, A_2$ and BeginCommit to $L$ | |
| 2 | $L$ sends Prepare to RM2 and RM3 | |
| 3 | RM2 votes Prepared, sends 2a to $A_1, A_2$ | |
| 4 | $L$ crashes; RM3 has not voted yet and also crashes before it votes | |
| 5 | $A_1$ and $A_2$ hold votes for instances 1 and 2, none for 3; nothing is chosen for 3 | 1: Prepared, 2: Prepared |
| 6 | $L'$ times out, sends 1a($b = (1, L')$) | |
| 7 | $A_2$ and $A_3$ promise: $A_2$ reports Prepared for 1 and 2, $A_3$ reports nothing | |
| 8 | $L'$ proposes Prepared for 1 and 2 (found in phase 1), Aborted for 3 (none found) | |
| 9 | $A_1, A_2, A_3$ accept; $L'$ gets 2b from two of them | 1: Prepared, 2: Prepared, 3: Aborted |
| 10 | $L'$ decides Abort and sends it to RM1 and RM2, which release their locks | |

In Two-Phase Commit, RM1 and RM2 would wait for $L$ to come back. Here the vote of RM1 and RM2 is safe with the acceptors, and the missing vote of RM3 is replaced by Aborted.

## Correctness

- **One value per instance.** Each instance is a Paxos instance. Ballot 0 is used only by its RM, which sends one vote, and phase 1 at a higher ballot reads every vote that could have been chosen. So each instance chooses at most one value.
- **Agreement.** Every leader decides from the chosen values only (line L7), so every leader that decides, and every RM that hears from one, reaches the same outcome.
- **Validity.** A leader proposes Prepared for instance $r$ only if it found Prepared in phase 1, so by induction only RM $r$ can be the source of Prepared in instance $r$. Commit needs Prepared chosen in every instance.
- **Non-blocking.** With $F + 1$ live acceptors and one live leader that is eventually alone, line L8 runs, phase 1 ends, and every instance chooses a value.

The full proof is below.

## Complexity

The cost in the normal case, with one leader, as in the comparison of Gray and Lamport:

| | Two-Phase Commit | Paxos Commit |
|---|---|---|
| message delays | 4 | 5 |
| messages | $3N - 1$ | $(N + 1)(F + 3) - 2$ |
| stable-storage writes | $N + 1$ | $N + F + 1$ |

The [Two-Phase Commit](/two-phase-commit/) page counts $4n$ messages and 3 delays: it starts at the coordinator's PREPARE and counts the ACKs. The message count adds up as $1$ BeginCommit, $N - 1$ Prepare, $N(F + 1)$ messages 2a, $F + 1$ messages 2b and $N$ outcomes. The tests check this sum for $N \le 6$ and $F \le 3$. A recovery costs two more round trips between the leader and the acceptors.

## Properties

- **Non-blocking.** Survives $F$ acceptor failures and any number of leader failures, as long as one leader is up.
- **Same write delay as Two-Phase Commit.** An RM writes its vote, and the acceptors write theirs in parallel, so two writes lie on the critical path in both protocols.
- **No consensus on the outcome.** There is no separate agreement on Commit or Abort: the outcome is a function of $N$ chosen votes.
- **Abort on doubt.** A missing vote becomes Aborted, so failures can abort a transaction that could have committed.

## Variants and improvements

- **Faster Paxos Commit.** The acceptors send their 2b messages to the RMs as well as to the leader, so an RM learns the outcome one message delay earlier, at the cost of about $N F$ more messages.
- **Co-location.** Placing acceptors on RM nodes makes some messages local, and the paper counts the cost of that case.
- **[Three-Phase Commit](/three-phase-commit/).** Also avoids blocking, but needs a synchronous model to be correct; Paxos Commit is safe in an asynchronous one.
- **[Two-Phase Commit](/two-phase-commit/).** The case $F = 0$.

## When to use it

Use Paxos Commit for distributed transactions where a blocked coordinator is too costly, for example when locks are held across data centers. If the commit coordinator is already replicated, for example a Multi-Paxos group, Two-Phase Commit on top of it gives a similar guarantee. If no failure must ever abort a ready transaction, Paxos Commit is not enough: it aborts on doubt.

## Pitfalls

- **A leader that proposes Prepared.** Line L10 may propose Prepared only when phase 1 found it. A leader that guesses Prepared for a slow RM can commit a transaction that this RM aborts.
- **Skipping phase 1 in recovery.** Line L10 must read the votes. The tests show that a leader that proposes Aborted for every instance without phase 1 can abort after another leader has committed.
- **Deciding from a minority.** Line L6 needs $F + 1$ acceptors with the same ballot. One acceptor's vote may be overwritten by a later ballot.
- **Voting before writing.** Line L3 writes the vote to stable storage first. An RM that restarts without its vote may send another one.
- **$F = 0$ in production.** With one acceptor the protocol blocks when it fails; the tests show this, as for Two-Phase Commit.

## Implementations

## History

[Two-Phase Commit](/two-phase-commit/) dates from the 1970s, and its blocking problem led Skeen to [Three-Phase Commit](/three-phase-commit/) in 1981, which needs synchrony. Gray and Lamport wrote "Consensus on transaction commit" as a Microsoft Research report in 2003 and published it in ACM Transactions on Database Systems in 2006. They showed that one Paxos instance per RM gives a non-blocking protocol with the same stable-storage delay as Two-Phase Commit, and that Two-Phase Commit is its case with one acceptor.

## References
