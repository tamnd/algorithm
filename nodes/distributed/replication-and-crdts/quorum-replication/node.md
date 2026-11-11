---
tag: TKDEFR
kind: algorithm
slug: quorum-replication
name: Quorum replication
aliases:
- quorum consensus
- weighted voting
- Gifford weighted voting
area: distributed/replication-and-crdts
level: core
summary: Reads and writes each contact a quorum of replicas, any read quorum meets any write quorum, and version tags pick the newest value; ABD makes this an atomic register.
model: asynchronous-model
complexity:
  vars: {n: the number of servers}
  messages: {worst: Θ(n)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false}
history:
  year: 1979
  people: [David K. Gifford, Robert H. Thomas, Hagit Attiya, Amotz Bar-Noy, Danny Dolev]
  note: Gifford (1979) gave weighted voting with version numbers, and Thomas (1979) majority consensus. Attiya, Bar-Noy and Dolev (1995) built an atomic register from majorities with a two phase read.
prereqs: [quorum, linearizability, crash-failure, asynchronous-model]
see_also: [quorum-intersection, leaderless-replication, dynamo-style-replication, read-repair, byzantine-quorum-system, primary-backup-replication, sloppy-quorum, flexible-paxos]
sources:
  - paper: doi:10.1145/800215.806583
    title: David K. Gifford, Weighted voting for replicated data, Proceedings of the 7th ACM Symposium on Operating Systems Principles (SOSP), 150-162, 1979
    locator: the description of votes per copy, read and write quorums with r + w greater than the total number of votes, and version numbers
  - paper: doi:10.1145/320071.320076
    title: Robert H. Thomas, A majority consensus approach to concurrency control for multiple copy databases, ACM Transactions on Database Systems 4(2), 180-209, 1979
    locator: the voting rule in which a majority of database copies must accept an update, with timestamps on the data
  - paper: doi:10.1145/200836.200869
    title: Hagit Attiya, Amotz Bar-Noy and Danny Dolev, Sharing memory robustly in message-passing systems, Journal of the ACM 42(1), 124-142, 1995
    locator: the emulation of a single-writer atomic register with majorities, the read that writes back before it returns, and the impossibility when half or more of the processors can fail
  - book: isbn:9780201107159
    title: Philip A. Bernstein, Vassos Hadzilacos and Nathan Goodman, Concurrency Control and Recovery in Database Systems, Addison-Wesley, 1987
    locator: Chapter 8 (replicated data, quorum consensus with the conditions 2w > v and r + w > v)
  - paper: doi:10.1145/78969.78972
    title: Maurice P. Herlihy and Jeannette M. Wing, Linearizability, a correctness condition for concurrent objects, ACM Transactions on Programming Languages and Systems 12(3), 463-492, 1990
    locator: Section 2 (the definition of linearizability)
---

Quorum replication stores a copy of a data item on each of $n$ servers and lets every read and every write contact only a **quorum** of them, chosen so that every read quorum meets every write quorum. Each copy carries a version tag, and a read keeps the value with the largest tag, so it sees the most recent completed write. Gifford (1979) gave the general form, weighted voting, where each copy has some votes and a read needs $r$ votes and a write $w$ votes, with $r + w$ greater than the total; Thomas (1979) used majorities. Attiya, Bar-Noy and Dolev (ABD, 1995) showed that majorities are enough to build a [linearizable](/linearizability/) register in the [asynchronous model](/asynchronous-model/) when fewer than half the servers crash, provided that a read writes back the value it found before it returns. Unlike [primary-backup replication](/primary-backup-replication/), no server is special and no failure detector is needed: a crashed server simply does not answer, and the quorum is made of others.

## In plain words

Five people each keep a copy of one number. To change the number, you must tell at least three of them, and each of them writes the new number with a counter that is one more than the last counter you saw. To read the number, you must ask at least three of them, and you take the number with the biggest counter.

Any group of three meets any other group of three in at least one person. So the people you ask always include someone who heard about the last change.

There is one more step when you read. Before you report what you found, you tell three people about it. Then nobody who reads after you can find an older number than you did.

## The problem

Clients share one read/write register, replicated on $n$ servers. Each operation must look as if it happened at one moment between its call and its return, so the history is [linearizable](/linearizability/). The model is the [asynchronous model](/asynchronous-model/) with reliable links and [crash failures](/crash-failure/) of servers and clients. The algorithm must not wait for a crashed server, so an operation can wait only for a quorum.

A quorum system for this problem is a set of read quorums and a set of write quorums such that every read quorum meets every write quorum; see [quorum intersection](/quorum-intersection/). With weighted voting, server $i$ has $v_i$ votes, $V = \sum_i v_i$, a read quorum is a set of servers with at least $r$ votes, a write quorum one with at least $w$ votes, and $r + w > V$. Majorities are the case $v_i = 1$ and $r = w = \lfloor n/2 \rfloor + 1$.

## The algorithm

Each server stores a pair (tag, value), with the initial tag $(0, \bot)$. A tag is a pair (ts, id) of a timestamp and a client id, ordered first by ts and then by id. The following is the multi-writer form of ABD.

```pseudo id=main
WRITE(v)                                   ▷ at client c
L1  send QUERY to all servers; wait for (tag, value) replies from a read quorum
L2  t ← (largest ts among the replies + 1, c)
L3  send STORE(t, v) to all servers; wait for acks from a write quorum

READ()                                     ▷ at any client
L4  send QUERY to all servers; wait for (tag, value) replies from a read quorum
L5  (t, v) ← the reply with the largest tag
L6  send STORE(t, v) to all servers; wait for acks from a write quorum    ▷ write back
L7  return v

SERVER, on STORE(t, v)
L8  if t > tag then (tag, value) ← (t, v)
L9  send an ack
```

A server answers QUERY with its current pair. Lines L1 and L2 give the write a tag larger than that of every write that completed before it started, because its read quorum meets the write quorum of each such write. Line L3 makes the new pair known to a write quorum. Lines L4 and L5 find the newest pair that any read quorum can see. Line L6 is the step that turns a regular register into an atomic one: before the read returns $v$, a write quorum holds a tag at least $t$, so a later read cannot return an older value. Line L8 keeps the tag at each server from going down.

With a single writer, the writer keeps its own counter and skips lines L1 and L2, so a write takes one round trip. Gifford's weighted voting is lines L1 to L5 with one difference: the version number has no client id, and a read returns at L5 without the write back. In Gifford's setting, writes run inside transactions with locks, so a write quorum lock gives the order of writes and a read has no concurrent writer.

## Example

**Why the read must write back.** Three servers $S_0, S_1, S_2$ with majorities, a single writer, and the initial value $\bot$.

1. The writer starts write(1) with tag 1. Its STORE reaches $S_0$ at once, but the messages to $S_1$ and $S_2$ are slow, so the write is still running.
2. Reader A queries $S_0$ and $S_1$. It gets (1, 1) and (0, $\bot$), takes 1, and, with the write back, stores (1, 1) at $S_0$ and $S_1$. It returns 1.
3. After A has returned, reader B queries $S_1$ and $S_2$. $S_1$ now holds (1, 1), so B returns 1.

The history is linearizable: put write(1) before both reads. Without line L6, step 2 leaves $S_1$ at (0, $\bot$), and B gets (0, $\bot$) from both $S_1$ and $S_2$ and returns $\bot$. Then A returned the new value and B, which started after A ended, returned the old one. No order of the three operations explains that, so the history is not linearizable. This pattern is called a new-old inversion.

**Weighted voting.** Three copies have 2, 1 and 1 votes, so $V = 4$. Take $r = 2$ and $w = 3$. Then $r + w = 5 > 4$ and $2w = 6 > 4$. A read can use the heavy copy alone. A write needs the heavy copy and one light copy, or both light copies and the heavy copy. If the heavy copy fails, reads still work with the two light copies, but writes stop. Votes let a designer move cost and availability between reads and writes.

**A quorum that is too small.** With $N = 3$, $W = 2$ and $R = 1$, so that $R + W = N$, a write of 1 goes to $S_0$ and $S_1$, and a later read asks only $S_2$. It returns the old value although the write completed before it.

## Correctness

**Theorem.** In the asynchronous model with reliable links, let every read quorum meet every write quorum, and let some read quorum and some write quorum stay free of crashed servers. Then every operation of a correct client completes, and every history of the multi-writer algorithm is linearizable. With majorities, this needs $n \ge 2f + 1$ to tolerate $f$ crashed servers, and ABD prove that no emulation of a register is possible when $n \le 2f$.

The proof assigns to each completed operation $o$ a tag $\tau(o)$: for a write, the tag it chose at L2; for a read, the tag it found at L5. Two facts carry the proof.

1. **Monotone tags.** If $o_1$ completes before $o_2$ starts, then $\tau(o_2) \ge \tau(o_1)$, and $\tau(o_2) > \tau(o_1)$ if $o_2$ is a write. When $o_1$ returns, a write quorum $Q_w$ holds a tag at least $\tau(o_1)$ (L3 or L6), and server tags never go down (L8). The query of $o_2$ gets replies from a read quorum $Q_r$, which meets $Q_w$, so it sees a tag at least $\tau(o_1)$. A write then adds 1 to the timestamp.
2. **Unique write tags.** Two writes by different clients differ in the id. Two writes by one client are sequential, so by fact 1 the later one has a larger tag.

Order the operations by tag, and put the write with tag $t$ before all reads with tag $t$; order reads with the same tag by their start times. By fact 1 this order respects real time, and each read with tag $t$ returns the value of the unique write with tag $t$, which is the last write before it in the order. The full proof, with pending operations, is in the proof file. Liveness holds because each phase waits only for a quorum, and a quorum of correct servers exists. The impossibility for $n \le 2f$ is a partition argument: split the servers into two groups of at most $f$; a writer that hears only from one group and a reader that hears only from the other cannot be told apart from runs in which the other group has crashed.

## Complexity

- **Messages.** Each phase sends one message to each of the $n$ servers and gets up to $n$ replies, so an operation costs $2n$ messages per phase and $4n$ in all for a read or a multi-writer write; a single-writer write costs $2n$. This is $\Theta(n)$.
- **Time.** A read and a multi-writer write take two round trips (four message delays); a single-writer write takes one round trip. No phase waits for a timeout.
- **Space.** Each server stores one value and one tag. The tag holds a counter that grows without bound.
- **Load.** Each operation touches a quorum, about $n/2$ servers with majorities. Other quorum systems lower the load; see [quorum intersection](/quorum-intersection/).

## Properties

- **No leader, no failure detector.** Any client can run any operation at any time, and crashes of up to the tolerated number of servers do not slow it down.
- **Atomic register.** With the write back, the register is linearizable. Without it, it is only a regular register: each read returns the value of the last completed write or of a concurrent write, but two reads can see an inversion.
- **Only registers.** Quorums with tags give read/write registers. They do not give read-modify-write operations such as compare-and-swap; those need consensus.
- **Trade off by sizes.** A small read quorum makes reads cheap and writes expensive, and the reverse.

## Variants and improvements

- **Single writer and multi-writer.** ABD (1995) give the single-writer form. The multi-writer form with the query phase in the write is due to Lynch and Shvartsman (1997).
- **Weighted voting.** Gifford assigns votes per copy. Copies with zero votes, which he calls weak representatives, serve as caches.
- **Byzantine quorums.** With Byzantine servers, quorums must meet in more than one correct server; see [Byzantine quorum system](/byzantine-quorum-system/).
- **Fast reads.** A read can skip the write back when all servers in its quorum already hold the largest tag, because then a write quorum already holds it.
- **Leaderless stores.** Systems in the style of [Dynamo](/dynamo-style-replication/) use $N$, $R$ and $W$ in the same way, but most do not write back on every read and allow [sloppy quorums](/sloppy-quorum/), so they do not give linearizability; see [leaderless replication](/leaderless-replication/) and [read repair](/read-repair/).

## When to use it

Use quorum replication for a register or a key-value store that must stay available while a minority of servers fail, with no failover step and no leader. It gives linearizable reads and writes at the price of two round trips. Use [primary-backup replication](/primary-backup-replication/) or a consensus protocol when the service needs operations other than read and write, such as increments or transactions.

## Pitfalls

- **Reads without write back.** Wrong: return the newest value from the read quorum at once. Right: write it back to a write quorum first (L6), or check that the quorum already agrees. The example shows the inversion that results.
- **Version numbers without writer ids.** Wrong: two concurrent writers both pick version 1 and store different values. Right: break ties with the client id, or require $2w > V$ and lock a write quorum so that writes are ordered, as in Gifford's scheme.
- **Quorums that do not meet.** Wrong: $r + w \le V$. A read can miss the last write.
- **Waiting for all replies.** Wrong: wait for every server. Right: wait only for a quorum, or one crashed server blocks every operation.
- **Using the counter of the local server.** Wrong: a client takes the timestamp from one server. Right: take the largest over a read quorum (L1, L2).

## Implementations

The Python code runs servers and clients in a discrete event simulator with seeded delays and crash times, in three modes: multi-writer ABD, single-writer ABD and Gifford voting with plain version numbers. A switch turns the write back off. The module includes a small Wing and Gong style search that decides whether a short register history is linearizable.

## History

Thomas (1979) proposed majority consensus for multiple copy databases: a majority of copies must approve an update, and timestamps order the updates. Gifford (1979) generalized this to weighted voting with read and write quorums and version numbers. Bernstein, Hadzilacos and Goodman (1987) present both as quorum consensus. Attiya, Bar-Noy and Dolev (1995) moved the idea from databases to distributed computing: they emulated a shared atomic register in an asynchronous message-passing system with majorities, added the write back that makes reads atomic, and proved that a majority of correct processors is necessary. Lynch and Shvartsman (1997) gave the multi-writer form with a query phase in the write.

## References
