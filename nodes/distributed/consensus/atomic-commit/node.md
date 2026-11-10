---
tag: JN1ENY
kind: problem
slug: atomic-commit
name: Atomic commit problem
aliases:
- atomic commitment
- non-blocking atomic commit
area: distributed/consensus
level: core
summary: The processes of a distributed transaction vote, and they must all commit or all abort. Commit is allowed only if all voted yes, and is required if all voted yes and nothing failed.
prereqs: [consensus-problem, crash-failure, asynchronous-model, acid-properties]
see_also: [two-phase-commit, three-phase-commit, paxos-commit, consensus-problem, flp-impossibility, failure-detector, two-generals-problem, write-ahead-logging]
sources:
  - paper: doi:10.1145/582318.582339
    title: Dale Skeen, Nonblocking commit protocols, Proceedings of the ACM SIGMOD International Conference on Management of Data, 1981, pages 133 to 142
    locator: the definition of a nonblocking protocol, the fundamental nonblocking theorem with concurrency sets, and its corollary for protocols that are synchronous within one state transition
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 7 (the atomic commitment problem, its conditions, blocking, two-phase and three-phase commit)
  - book: isbn:9783642152597
    title: Christian Cachin, Rachid Guerraoui and Luís Rodrigues, Introduction to Reliable and Secure Distributed Programming, second edition, Springer, 2011
    locator: Chapter 6 (non-blocking atomic commit, and the algorithm from consensus and a perfect failure detector)
  - paper: "Jim Gray and Leslie Lamport, Consensus on transaction commit, ACM Transactions on Database Systems 31(1), 2006"
    locator: the statement of the transaction commit problem and Paxos Commit
---

The atomic commit problem asks the processes of a distributed transaction to agree to commit it or to abort it: each process votes yes or no, all processes that decide must reach the same decision, commit is allowed only if every vote is yes, and commit is required if every vote is yes and nothing fails. It is the "all or nothing" of the [ACID properties](/acid-properties/) when a transaction spans several servers. [Two-phase commit](/two-phase-commit/) solves it but can block when its coordinator fails, and the non-blocking form asks that every process that stays up decides. No protocol solves the non-blocking form in the [asynchronous model](/asynchronous-model/) with even one crash, while [three-phase commit](/three-phase-commit/) solves it with crash failures in a [synchronous system](/synchronous-model/) (Skeen, 1981).

## In plain words

A money transfer takes 100 from an account at one bank and adds 100 to an account at another bank. Both changes must happen, or neither. Each bank first checks its part and says "yes, I can do it" or "no". The banks then must all do it or all drop it.

The rules are simple. If anyone says "no", nobody may do it. If everyone says "yes" and nothing goes wrong, everyone must do it. And no two banks may end up with different outcomes.

The hard case is a bank that stops answering. Has it crashed, or is its network just slow? If the others cannot tell, they cannot safely decide either way, so they may have to wait.

## Definition

There are $n$ processes $p_1, \ldots, p_n$, the participants of one transaction. One of them may also act as coordinator. Each process $p_i$ starts with a vote $v_i \in \{\text{yes}, \text{no}\}$, and may decide commit or abort. A protocol solves **atomic commit** if every run satisfies:

- **Agreement.** No two processes decide differently. This applies to every process, including one that decides and later crashes.
- **Integrity.** A process decides at most once and does not change its decision.
- **Commit validity.** If some process decides commit, then every vote is yes.
- **Non-triviality.** If every vote is yes and no process fails, then every process decides commit.
- **Termination.** If all failures are repaired and no new failures happen for long enough, every process decides.

These conditions follow the book of Bernstein, Hadzilacos and Goodman. Commit validity and agreement are safety. Termination of this weak form is what [two-phase commit](/two-phase-commit/) gives.

**Non-blocking atomic commit (NBAC)** replaces termination by a stronger property:

- **Non-blocking termination.** Every process that does not crash eventually decides, whatever the other processes do.

In the form of Cachin, Guerraoui and Rodrigues, non-triviality reads: a process may decide abort only if some process voted no or some process crashed.

In non-triviality, "no failure" must also cover a slow process in a model where slowness and crashes look the same. The impossibility below rests on exactly this point.

## Variants

- **Blocking and non-blocking.** As above. In the blocking form a process may wait until a failed process recovers.
- **Crash-stop and crash-recovery.** With recovery, a process must log its vote and its decision on stable storage before it acts on them, as in [write-ahead logging](/write-ahead-logging/).
- **Presumed abort and presumed commit.** Variants of the protocol in which a missing record means abort or commit. These change the cost, not the problem.
- **Byzantine atomic commit.** Some participants may lie about their votes. It needs Byzantine agreement on the decision.
- **Commit with partitions.** The network can split into groups. A protocol that never decides differently in two groups must block in some group: see [split-brain](/split-brain/).

## Examples

**Bank transfer.** Bank A votes yes (the account has 150, so the debit of 100 is possible). Bank B votes yes. With no failure, both commit: A ends with 50, B with its old balance plus 100. If A has only 80, A votes no, and both abort.

**A run of two-phase commit that blocks.** All participants vote yes. The coordinator records commit, then crashes before it sends anything. Each participant voted yes and knows nothing more, so the blocking form allows it to wait until the coordinator recovers, and the non-blocking form requires it to decide, which it cannot do safely. See the example on the [two-phase commit](/two-phase-commit/) page.

**Non-examples.** A protocol where each participant commits once it has voted yes breaks agreement when another participant votes no. A protocol where every participant aborts on any timeout breaks agreement in the run above: the coordinator recovers and commits.

## Known algorithms

- **[Two-phase commit](/two-phase-commit/)** (Gray 1978, Lampson and Sturgis 1976). Safe in the asynchronous model with crash-recovery failures. Blocking.
- **[Three-phase commit](/three-phase-commit/)** (Skeen 1981). Non-blocking with crash failures in a synchronous system with an exact failure detector. Not safe under partitions.
- **NBAC from consensus and a perfect failure detector** (Cachin, Guerraoui and Rodrigues). Each process sends its vote to all, waits until it has a vote or a crash report from every process, and proposes commit to a uniform [consensus](/consensus-problem/) if it has yes from all, else abort. It decides what consensus decides.
- **[Paxos Commit](/paxos-commit/)** (Gray and Lamport 2006). Each participant's vote is decided by a [Paxos](/paxos/) instance with $2F + 1$ acceptors. It is always safe, and it decides when at most $F$ acceptors fail and the system behaves synchronously for long enough. With $F = 0$ it is two-phase commit.

## Bounds

### No non-blocking protocol in the asynchronous model

**Theorem.** In the asynchronous model, no protocol solves non-blocking atomic commit if one process may crash.

*Proof.* Assume a protocol solves it, and take $n \ge 2$ processes. Fix a process $p$.

- **Run $R_1$.** Every process except $p$ votes yes, $p$ votes no, and $p$ crashes at the start, before it sends any message. By non-blocking termination, every other process decides by some finite time $T$. By commit validity it cannot decide commit, since $p$ voted no. So every process other than $p$ decides abort by time $T$.
- **Run $R_2$.** Every process votes yes, including $p$, and no process crashes. The process $p$ is slow: it takes no step before time $T$, and the messages it sends later arrive after time $T$. The other processes behave as in $R_1$. The asynchronous model allows this run.

Until time $T$, every process other than $p$ receives the same messages in $R_1$ and in $R_2$, so it takes the same steps and decides abort by time $T$ in $R_2$ too. But in $R_2$ every vote is yes and no process fails, so non-triviality requires commit. This is a contradiction. $\square$

The proof uses only that a crashed process and a slow process look the same. It does not need the [FLP impossibility](/flp-impossibility/) result. With a perfect failure detector, $R_1$ and $R_2$ differ, because in $R_2$ the detector never reports $p$, and the problem becomes solvable (previous section).

### The synchronous case: Skeen's theorem

Skeen (1981) gives an exact condition. For a protocol given as one finite state automaton for each process, the **concurrency set** of a local state $s$ is the set of local states that other processes can be in while some process is in $s$. A state is **committable** if a process in it knows that every process voted yes. Skeen's fundamental nonblocking theorem says that a protocol is non-blocking if and only if both conditions hold:

1. no local state has a concurrency set that holds both an abort state and a commit state, and
2. no noncommittable state has a concurrency set that holds a commit state.

For protocols that are synchronous within one state transition (no process is more than one transition ahead of another), the concurrency sets are given by the adjacent states, and the corollary reads: no local state is adjacent to both a commit and an abort state, and no noncommittable state is adjacent to a commit state. The wait state of two-phase commit breaks condition 1, and three-phase commit adds a committable pre-commit state between wait and commit to meet both conditions. This page cites the theorem and does not prove it.

### Partitions

With network partitions, a non-blocking protocol must let each group decide without hearing from the other, and then two groups can decide differently. The run on the [three-phase commit](/three-phase-commit/) page shows this for 3PC.

## Reductions

**Consensus with a perfect failure detector solves NBAC.** Let $\mathcal P$ be a perfect failure detector (it eventually reports every crashed process and never reports a live one). Each process sends its vote to all, waits until for each process it has the vote or a report from $\mathcal P$, and proposes commit if it has yes from all $n$ processes, else abort. It decides the output of a uniform consensus.

*Proof.* Agreement and integrity come from uniform consensus. Termination: by completeness of $\mathcal P$, each correct process stops waiting, and consensus terminates. Commit validity: commit is decided only if some process proposed it (validity of consensus), and that process received yes from all. Non-triviality in the form of Cachin et al.: abort is proposed only if some vote is no or $\mathcal P$ reported some process, and by accuracy of $\mathcal P$ that process crashed. $\square$

The theorem of the previous section shows that a failure detector that can be wrong forever is not enough: with no accurate information about crashes, $R_1$ and $R_2$ look the same.

**Relation to consensus.** Consensus asks for agreement on any proposed value and allows any outcome; atomic commit fixes the outcome by the votes, and commit validity and non-triviality depend on all $n$ votes. So an atomic commit protocol must hear from every process, while consensus needs only a majority in the crash model.

## Applications

- **Distributed transactions.** Databases that split data across servers commit a transaction with [two-phase commit](/two-phase-commit/), often with the coordinator's decision on a replicated log.
- **XA and resource managers.** A transaction manager runs two-phase commit across a database and a message queue.
- **Sharded databases over consensus.** Each shard is a [Raft](/raft/) or [Paxos](/paxos/) group, and two-phase commit runs between the groups. Each group stays up while a majority of its replicas is up, so the coordinator does not block on one machine.
- **Locking.** Atomic commit works with [two-phase locking](/two-phase-locking/): a participant holds its locks from its yes vote to the decision.

## References
