---
tag: S2MVM5
kind: algorithm
slug: two-phase-commit
name: Two-phase commit
aliases:
- 2PC
area: distributed/consensus
level: core
summary: A coordinator asks every participant to prepare and vote, then sends commit if all voted yes and abort otherwise. It is always safe, but a participant blocks if the coordinator fails after the vote.
solves: [atomic-commit]
model: asynchronous-model
complexity:
  vars: {n: the number of participants}
  time: {best: Θ(1)}
  messages: {best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1978
  people: [Jim Gray, Butler Lampson, Howard Sturgis]
  note: Lampson and Sturgis described a two-phase commit for distributed storage in a Xerox PARC report of 1976, and Gray described the protocol and its logging rules in his notes on database operating systems of 1978.
prereqs: [atomic-commit, write-ahead-logging, crash-recovery, crash-failure]
see_also: [three-phase-commit, paxos-commit, acid-properties, two-phase-locking, group-commit, consensus-problem]
sources:
  - paper: doi:10.1007/3-540-08755-9_9
    title: Jim Gray, Notes on data base operating systems, in Operating Systems, an Advanced Course, Lecture Notes in Computer Science 60, Springer, 1978, pages 393 to 481
    locator: the part on recovery management, with the two-phase commit protocol and its log records
  - paper: "Butler W. Lampson and Howard E. Sturgis, Crash recovery in a distributed data storage system, Xerox Palo Alto Research Center, 1976"
    locator: the commit of a transaction that spans several storage servers
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 7 (distributed recovery, two-phase commit, the cooperative termination protocol, blocking)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 9 (atomic commit and two-phase commit, coordinator failure)
---

Two-phase commit (2PC) is a protocol for the [atomic commit](/atomic-commit/) problem: a transaction that touches several servers must commit on all of them or abort on all of them. In the first phase a coordinator asks every participant to prepare, and each participant votes yes or no. In the second phase the coordinator sends COMMIT if every vote was yes, and ABORT otherwise. The protocol is safe in the [asynchronous model](/asynchronous-model/) under any pattern of crashes, but it blocks: a participant that voted yes and then loses contact with the coordinator must wait, holding its locks, until the coordinator recovers.

## In plain words

A trip needs a flight, a hotel and a car, from three different companies. You want all three or none. So an organizer phones each company: "Can you hold this booking for me?" Each company either says "no" or puts the booking on hold, writes that down, and says "yes". Once a company says "yes", it must keep the hold until it hears back.

If all three said "yes", the organizer writes "go" in its notebook and calls everyone back with "go". If anyone said "no", it calls everyone with "cancel".

The weak point is the wait. If the organizer disappears after the companies said "yes", each company is stuck. It cannot cancel, because the organizer may have said "go" to someone. It cannot confirm, because the organizer may have said "cancel". It must wait for the organizer to come back.

## The problem

A transaction runs at $n$ participants $P_1, \ldots, P_n$ and one coordinator $C$. Each participant can vote yes (it can commit its part) or no. The protocol must give the [atomic commit](/atomic-commit/) properties: all processes that decide reach the same decision, commit only if every participant voted yes, and commit if every participant voted yes and nothing fails.

The model is asynchronous, with crash-recovery failures. Each process keeps a log on stable storage, as in [write-ahead logging](/write-ahead-logging/), and a crash loses everything else, including the messages it had not yet sent. A *forced* write returns only after the record is on stable storage. Timeouts exist, but a timeout does not prove that the other process crashed.

## The algorithm

```pseudo id=main
COORDINATOR C, with participants P1, ..., Pn
L1  send PREPARE to every participant; wait for the votes
L2  on YES from every participant: force-log COMMIT; decision ← commit
L3  on NO from any participant, or on a timeout: log ABORT; decision ← abort
L4  send the decision to every participant; when every ACK has arrived, log END
PARTICIPANT P
L5  on PREPARE, if P can commit: force-log PREPARED; send YES        ▷ P is now uncertain
L6  on PREPARE, if P cannot commit: log ABORT; abort; send NO
L7  on COMMIT or ABORT: force-log it; apply it and release the locks; send ACK
L8  on a timeout before P has voted: log ABORT; abort
L9  on a timeout while uncertain: send DECISION-REQUEST to every other process
ANY PROCESS Q, on DECISION-REQUEST from R                          ▷ cooperative termination
L10 if Q has decided then send the decision to R
L11 else if Q has not voted yes, or Q is the coordinator: log ABORT; abort; send ABORT to R
L12 else send UNCERTAIN to R                    ▷ if every answer is UNCERTAIN, R stays blocked
RECOVERY, from the log alone
L13 if the log has COMMIT or ABORT, apply it (the coordinator sends it again); else if Q is the coordinator or the log has no PREPARED: log ABORT; abort
L14 if the log has PREPARED and no decision: Q is uncertain; go to L9
```

**Phase 1 (voting).** The coordinator sends PREPARE. A participant that can commit its part makes the part durable, so that it can commit even after a crash, then forces a PREPARED record and votes yes. From this moment it is *uncertain*: it has given up its right to abort on its own. A participant that cannot commit aborts at once and votes no.

**Phase 2 (decision).** With yes from all, the coordinator forces COMMIT to its log. This write is the commit point of the transaction: it is committed even if the coordinator crashes the next instant. With a no or a timeout, the coordinator aborts. It then sends the decision, and each participant forces it, applies it, releases its locks and acknowledges. When all have acknowledged, the coordinator can forget the transaction.

**The two logging rules.** A participant forces PREPARED before it sends YES, so after a crash it knows that it may not abort on its own (line L14). The coordinator forces COMMIT before it sends it, so after a crash it never decides ABORT for a transaction that someone may have committed (line L13). The ABORT record need not be forced: a coordinator that recovers with no decision in its log aborts anyway. This is the presumed-abort rule.

**Termination (lines L9 to L12).** An uncertain participant that times out asks every other process. Any process that knows the decision tells it. A participant that has not voted yet may abort and say so, since then the coordinator cannot have decided COMMIT. If the coordinator is down and all reachable participants are uncertain, nobody can decide, and the participant stays blocked.

## Example

All three participants vote yes, and the coordinator crashes right after it forces COMMIT, before it sends it.

| step | event | log of C | logs of P1, P2, P3 | state of P1, P2, P3 |
|---|---|---|---|---|
| 1 | C sends PREPARE (line L1) | | | waiting |
| 2 | each Pi forces PREPARED and sends YES (line L5) | | PREPARED | uncertain |
| 3 | C gets three YES and forces COMMIT (line L2) | COMMIT | PREPARED | uncertain |
| 4 | C crashes before it sends COMMIT | COMMIT | PREPARED | uncertain |
| 5 | each Pi times out and asks the others (line L9); each answer is UNCERTAIN (line L12) | COMMIT | PREPARED | uncertain, blocked |
| 6 | C recovers, reads COMMIT and sends it again (line L13) | COMMIT | PREPARED, COMMIT | committed |

Between steps 4 and 6 the participants hold their locks, and no amount of waiting or asking helps. If they abort to free the locks, then in step 6 the coordinator commits and the transaction is half committed. If they commit, they are wrong in the run where the coordinator decided ABORT on a timeout in step 3 and crashed. The two runs look the same to every participant.

A second run: COMMIT reaches only P1, which commits and then crashes, and C crashes too. P2 and P3 are uncertain, and only P1 or C can tell them the answer. When P1 recovers, its log holds COMMIT, so it answers by line L10, and P2 and P3 commit.

## Correctness

The proof has three parts. *Safety:* every COMMIT decision comes from the coordinator's COMMIT, which needs yes from all, and a participant that voted yes has PREPARED in its log, so no rule lets it abort on its own; hence no process decides ABORT in a run where any process decides COMMIT. *Termination:* once every failed process has recovered and stays up, every process decides. *Blocking:* an uncertain participant cannot tell a run where the coordinator committed from one where it aborted, so it must wait while the coordinator is down and every other participant is uncertain. Safety holds with any delays and any number of crashes. The full proof is below.

## Complexity

Without failures, 2PC sends $4n$ messages: $n$ PREPARE, $n$ votes, $n$ decisions and $n$ ACKs. The ACKs are not on the critical path, so a participant learns the decision after 3 message delays: PREPARE, vote, decision. There are $n + 1$ forced writes before the decision is known (one PREPARED at each participant and the COMMIT of the coordinator), and $n$ more when the participants force the decision. The coordinator stores $n$ votes and $n$ ACK flags.

In practice the cost of 2PC is in the forced writes and in the locks held during the uncertain window, more than in the message count.

## Properties

- Safe in the asynchronous model with crash-recovery failures and any number of crashes.
- Blocking: one failure of the coordinator can stop the uncertain participants until it recovers.
- A participant that votes no, or that has not voted, can abort alone. A participant that votes yes cannot.
- The coordinator is a single point of decision: it alone moves a transaction to COMMIT.
- The commit point is the forced COMMIT record of the coordinator.

## Variants and improvements

- **Presumed abort and presumed commit.** The coordinator skips the forced write of one kind of decision and treats a missing record as that decision. Presumed abort, used above, saves writes and messages for aborted transactions. Presumed commit saves them for committed transactions at the cost of a forced record at the start.
- **Read-only participants.** A participant that wrote nothing votes "read only" and leaves the protocol at once, with no PREPARED record.
- **Linear 2PC.** The participants form a chain, and the vote and the decision pass along it. It uses fewer messages and more delays.
- **Coordinator on a replicated log.** If the coordinator's decision is itself stored with [Paxos](/paxos/) or [Raft](/raft/), the blocking window disappears as long as a majority of the coordinator replicas is up. [Paxos Commit](/paxos-commit/) goes further and runs one Paxos instance for each participant's vote.
- **Three-phase commit.** [Three-phase commit](/three-phase-commit/) adds a pre-commit round so that it never blocks under crash failures in a synchronous system, at the cost of safety under network partitions.

## When to use it

Use 2PC when a transaction writes data on several servers or resource managers that must agree, and when blocking during a rare coordinator failure is acceptable. Databases with partitioned data, XA transactions across a database and a message queue, and distributed transactions in cloud databases use it. If the coordinator cannot be made highly available, put its decision on a replicated log, or use a protocol such as Paxos Commit. If a transaction touches one server, use local commit instead: 2PC adds two rounds of messages and several forced writes.

## Pitfalls

- **Voting yes before the data is durable.** A participant that votes yes must be able to commit after any crash. It must force its changes and the PREPARED record first.
- **Aborting an uncertain participant on a timeout.** This breaks atomicity in the run of the example. Only a participant that has not voted may abort alone.
- **Sending COMMIT before forcing it.** If the coordinator crashes after it sends but before the write, it recovers, finds no decision, and aborts a transaction that some participant has committed.
- **Locks held while blocked.** An uncertain participant keeps its locks, so other transactions that need those rows also wait. Operators sometimes resolve such "in doubt" transactions by hand, which is safe only with the coordinator's log at hand.
- **Forgetting too early.** The coordinator may delete its record only after every participant has acknowledged. Otherwise a participant that asks later gets a wrong presumed answer.

## Implementations

## History

Lampson and Sturgis described the commit of a transaction across several storage servers in a 1976 report at Xerox PARC. Gray described the two-phase commit protocol and its log records in his 1978 notes on database operating systems. Bernstein, Hadzilacos and Goodman later gave the protocol with the cooperative termination protocol and the analysis of blocking in their 1987 book.

## References
