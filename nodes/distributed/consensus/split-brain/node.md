---
tag: Z2JAHA
kind: concept
slug: split-brain
name: Split brain
area: distributed/consensus
level: intro
summary: Two parts of a system each believe they are the leader and act on their own, which can corrupt shared data. Quorums, leases and fencing tokens prevent it.
prereqs: [failure-detector, quorum, crash-failure]
see_also: [leader-lease, quorum, raft, primary-backup-replication, cap-theorem, three-phase-commit, clock-drift, view-change]
sources:
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 8, the sections on process pauses, on the truth defined by the majority, and on fencing tokens
  - paper: doi:10.1145/74850.74870
    title: Cary G. Gray and David R. Cheriton, Leases, an efficient fault-tolerant mechanism for distributed file cache consistency, Proceedings of the 12th ACM Symposium on Operating Systems Principles (SOSP), 1989
    locator: the definition of a lease and the effect of clock drift on lease safety
  - paper: "Mike Burrows, The Chubby lock service for loosely-coupled distributed systems, Proceedings of the 7th USENIX Symposium on Operating Systems Design and Implementation (OSDI), 2006"
    locator: the section on sequencers, which a lock holder passes to servers so that they can reject requests from an old holder
  - url: https://raft.github.io/raft.pdf
    title: Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm (extended version), 2014
    locator: Section 5.1 (terms, and a server that rejects a request with a stale term) and Section 5.2 (at most one leader per term)
---

Split brain is a failure in which two parts of a system each believe that they are in charge, for example two servers that both act as the primary of a database, and both accept writes. The writes of one side then overwrite or contradict the writes of the other. It comes from a network partition, a long process pause or a wrong clock, because a node that cannot hear the leader cannot tell whether the leader stopped or is only cut off. The standard fixes are a [quorum](/quorum/) rule for who may lead, a time-bounded [lease](/leader-lease/), and a fencing token that the shared resource itself checks.

## In plain words

A shop has two managers on duty, and only one may sign checks. The phone line between them breaks. Each one thinks the other went home, so both sign checks from the same account, and the account goes empty.

A rule of "the person with the key signs" helps: there is one key. But a manager can fall asleep with the key, the key office gives a new key to someone else, and the sleeper wakes up and signs with the old key.

The bank can stop this. Each key has a number, and each new key has a bigger number. The bank remembers the biggest number it has seen and refuses any check signed with a smaller one.

## The idea

**What goes wrong.** A system has one leader (a primary, a lock holder, a master), and the others watch it with timeouts. A timeout does not prove a crash. There are three common causes of a false one:

- **Network partition.** The leader runs, but its messages do not reach the others. They elect a new leader, and the old one, still connected to some clients, keeps serving them.
- **Process pause.** The leader stops for many seconds, from a garbage collection pause, a suspended virtual machine, or a swap to disk. The others elect a new leader. The old leader then resumes in the middle of its work, with no sign that time has passed.
- **Clock jumps and drift.** The leader decides from its own clock that its lease is still valid, but its clock is slow or jumped back, and the lease ran out by the clock of the lock service.

Each case gives two nodes that act as leader at the same time. In a [primary-backup](/primary-backup-replication/) database both accept writes; in a lock service both think they hold the lock; in a commit protocol each side of a partition decides on its own, which is why [three-phase commit](/three-phase-commit/) can commit on one side and abort on the other.

**Fix 1: quorums.** A leader needs the votes of a majority, and two majorities share a member, so two leaders of the same election cannot both be chosen. [Raft](/raft/) and [Paxos](/paxos/) number the elections (terms or ballots), and each server votes at most once per number. The side of a partition without a majority cannot elect a leader and stops, which is the price that the [CAP theorem](/cap-theorem/) predicts. A quorum alone does not stop an old leader that has not yet learned that a new term began: it can still answer reads from its own state. Raft stops its writes because they need a majority, and a majority has moved to the new term.

**Fix 2: leases.** A lease is a lock with an expiry time (Gray and Cheriton, 1989). The holder may act only until the lease expires, and the service grants no new lease before then. A lease is safe only if clocks run at nearly the same rate: the holder must stop early by a margin larger than the possible [clock drift](/clock-drift/). It is not safe under a process pause, since the holder can check the lease, pause, and act after the lease ends.

**Fix 3: fencing tokens.** Each time the lock service grants the lock, it also gives a token: a number that is larger than every token it gave before. The holder attaches the token to every request it sends to the shared resource. The resource stores the largest token it has accepted and rejects any request with a smaller one. Chubby calls the token a sequencer; in Raft the term number plays this role.

```pseudo id=main
L1  LOCK SERVICE, on grant to client c: token ← token + 1; return (token, expiry)
L2  STORAGE, on write(t, v): if t < maxToken then reject
L3  else maxToken ← max(maxToken, t); apply v
L4  CLIENT: if it does not believe it holds a lease then request one
L5  CLIENT: while it believes it holds a lease with token t: send write(t, v)
```

**Claim.** Assume that the lock service gives strictly increasing tokens (line L1) and that the storage runs lines L2 and L3 as one atomic step. Then the sequence of writes that the storage accepts has non-decreasing tokens. So once a write of the holder with token $t$ is accepted, no later write from any holder with a smaller token is accepted.

*Proof.* Let $w_1, w_2, \ldots$ be the accepted writes in the order the storage applies them, with tokens $t_1, t_2, \ldots$, and let $M_i$ be the value of maxToken just after $w_i$. Line L3 sets $M_i = \max(M_{i-1}, t_i)$, so $M_i \ge t_i$ and $M$ never decreases. Write $w_{i+1}$ was accepted, so line L2 did not reject it: $t_{i+1} \ge M_i \ge t_i$. $\square$

Since tokens follow the order of the grants, the storage sees the holders in grant order, as if each lease ended before the next began: the writes of an old holder can come before the first write of a newer holder, never after it. This does not need clocks to agree or pauses to be short. It does need every resource that the holder touches to check the token; a resource that ignores it is still open to the stale holder.

## Examples

**The stale write.** This is the run in the tests.

| time | event | storage maxToken | result |
|---|---|---|---|
| 0 | client 1 gets the lease with token 33, until time 10 | 0 | |
| 1 | client 1 starts a long pause | 0 | |
| 10 | the lease of client 1 expires | 0 | |
| 12 | client 2 gets the lease with token 34 | 0 | |
| 13 | client 2 writes "new" with token 34 | 34 | accepted |
| 20 | client 1 wakes, still believes it holds the lease, writes "stale" with token 33 | 34 | rejected, since $33 < 34$ |

Without the check in line L2, the storage accepts "stale", which overwrites the newer value. In the seeded simulation of the implementation, with three clients, random pauses and some slow clocks, 185 of 300 runs without fencing accept a write with a smaller token than an earlier write, and no run with fencing does.

**Two primaries.** A database runs a primary and a backup, and the backup takes over when heartbeats stop. A partition cuts the heartbeats but not the clients. Both servers now accept writes, and the two copies diverge; when the partition heals, one side's writes must be thrown away. Replication by a majority quorum, as in [Raft](/raft/), avoids this: the side without a majority cannot commit.

**Non-example.** Two servers that both answer reads from their copy of a value, during a partition, give stale reads but do not corrupt data. Whether that counts as split brain depends on the consistency the system promises; under [linearizability](/linearizability/) it is a violation.

## Where it is used

- **Consensus protocols.** [Raft](/raft/) terms, Paxos ballots and [view](/view-change/) numbers in [Viewstamped Replication](/viewstamped-replication/) are fencing tokens: a server rejects any message with a smaller number than the one it has seen.
- **Lock services.** Chubby gives sequencers. ZooKeeper's zxid of the node that holds a lock can serve as a token in the same way.
- **Leader leases.** A [leader lease](/leader-lease/) lets a leader serve reads without a round of messages, which is safe only with bounded clock drift.
- **Clusters with shared disks.** High-availability clusters cut the old node from the disk or turn its power off before a new node takes over. This is fencing done by the resource, without tokens.

## References
