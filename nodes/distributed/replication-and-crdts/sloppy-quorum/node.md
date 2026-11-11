---
tag: X1134J
kind: technique
slug: sloppy-quorum
name: Sloppy quorum
aliases:
- sloppy quorums
area: distributed/replication-and-crdts
level: advanced
summary: Reads and writes go to the first N healthy nodes on the ring, not to the fixed N home replicas. Writes stay available, but R + W > N no longer makes reads and writes meet.
prereqs: [quorum-replication, quorum-intersection, consistent-hashing]
see_also: [dynamo-style-replication, hinted-handoff, leaderless-replication, read-repair, anti-entropy, eventual-consistency, cap-theorem, split-brain]
sources:
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall and Werner Vogels, Dynamo, Amazon's highly available key-value store, Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP), 205-220, 2007
    locator: Section 4.6 (handling temporary failures, the sloppy quorum on the first N healthy nodes of the preference list, and the hinted replica), and Section 4.5 (R, W and R + W > N)
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, the sections Limitations of Quorum Consistency and Sloppy Quorums and Hinted Handoff
---

A sloppy quorum is a way to keep a replicated key-value store writable when some replicas of a key cannot be reached. Each key has a fixed set of $N$ home replicas, and a strict quorum system sends a request only to them: a write needs $W$ acks from home nodes, a read needs $R$ replies from home nodes, and $R + W > N$ makes every read quorum meet every write quorum (see [quorum intersection](/quorum-intersection/)). A **sloppy quorum** sends the request to the first $N$ *healthy* nodes in a fixed order that starts with the homes, for example the walk of a [consistent hashing](/consistent-hashing/) ring. A node outside the home set that takes a write is a stand-in; it keeps a hint that names the home it replaces and returns the data later by [hinted handoff](/hinted-handoff/). The result is that a write succeeds whenever any $W$ nodes are reachable, and the price is that $R + W > N$ no longer gives intersection, so a read can miss a write that succeeded. Amazon's Dynamo introduced the technique (DeCandia et al. 2007, Section 4.6); see [Dynamo-style replication](/dynamo-style-replication/).

## In plain words

Each item has three keepers. A normal rule says: a change counts once two of the three keepers have it, and a reader asks two of the three. Two groups of two out of three always share a keeper, so the reader always finds the change.

A sloppy rule says: if a keeper is away, give the change to the next person in line, with a note that says whose copy it is. Now a change still counts with any two people, so changes are almost never refused.

But the two people who took the change and the two people a reader asks can now be different people. The reader can then get the old version. The notes fix this later, when the keepers are back.

## When it applies

- The store is replicated without a leader, as in [leaderless replication](/leaderless-replication/), and it uses read and write quorums of sizes $R$ and $W$ over $N$ replicas per key.
- The model is the [asynchronous model](/asynchronous-model/) with message passing, [crash-recovery](/crash-recovery/) failures and network partitions. Nodes are trusted, so there are no Byzantine faults.
- There are more nodes in the cluster than replicas of a key, so healthy nodes outside the home set exist.
- The application values write availability over fresh reads: it accepts [eventual consistency](/eventual-consistency/) and stale reads during failures. In the terms of the [CAP theorem](/cap-theorem/), it chooses availability.
- A repair path exists that moves data from stand-ins to homes: hinted handoff, and as a backup [anti-entropy](/anti-entropy/).

## The template

The holes are written in capitals. HOMES(key) gives the $N$ home replicas, ORDER(key) is a fixed list of all nodes that starts with HOMES(key), HEALTHY(x) is the coordinator's current view of node $x$, from a [failure detector](/failure-detector/) or from timeouts, and STORE and HANDOFF are the local store and the repair path.

```pseudo id=main
SLOPPY-WRITE(key, value)
L1  P ← HOMES(key)                                        ▷ for a ring: the first N distinct nodes clockwise
L2  T ← the first N nodes x of ORDER(key) with HEALTHY(x)
L3  pair each x in T \ P with a different node of P \ T; x will keep the hint "for that home"
L4  send (key, value, hint) to every node of T; each node does STORE, and keeps the hint if it has one
L5  succeed when W nodes of T have acked

SLOPPY-READ(key)
L6  compute T as in lines L1 and L2; ask every node of T; wait for R replies
L7  return the newest version, or all concurrent versions, of the replies

REPAIR, at a node that holds hints
L8  when the home named in a hint is HEALTHY, HANDOFF the hinted data to it and drop the hint
```

When every home is healthy, $T = P$ and the technique behaves like a strict quorum. When at least $N$ nodes are healthy, $T$ and $P$ both have $N$ elements, so $T \setminus P$ and $P \setminus T$ have the same size in line L3, and every stand-in gets one home. With fewer healthy nodes, $T$ is smaller and some homes get no stand-in.

**Why intersection fails.** With a strict quorum the write set $Q_w$ and the read set $Q_r$ are both subsets of $P$, and $|Q_r| + |Q_w| > N = |P|$ forces a common node. With a sloppy quorum, $Q_w \subseteq T_w$ and $Q_r \subseteq T_r$, where $T_w$ and $T_r$ are computed from two views of which nodes are healthy. Both are subsets of the whole cluster of $n$ nodes, so $Q_w$ and $Q_r$ can be disjoint whenever $R + W \le n$ and the two views differ. Nothing in lines L1 to L7 relates the two views.

**Counterexample.** Five nodes A to E, $N = 3$, $R = W = 2$, and a key with the ring order B, A, C, D, E, so $P = \{B, A, C\}$. A partition splits {B, D, E} from {A, C}.

1. A client on the first side writes. Its coordinator sees B, D, E as healthy, so $T_w = \{B, D, E\}$, D keeps the hint "for A" and E the hint "for C". All three store the value, and the write succeeds with $W = 2$. A strict quorum would have $T_w = \{B\}$ and would fail.
2. A client on the second side reads. Its coordinator sees only A and C, so $T_r = \{A, C\}$, and both return the old value. The read succeeds with $R = 2$ and returns the old value, although $R + W = 4 > 3 = N$ and the write succeeded before the read started.
3. The partition heals. D sends the value to A, E sends it to C, and both drop their hints. From now on every read returns the new value.

**What is still true.** Each write is stored at $W$ nodes, so it survives up to $W - 1$ crashes that lose data. Once the hints reach their homes, the homes hold every write, and the store converges by the same argument as for any merge of versions; see the correctness section of [Dynamo-style replication](/dynamo-style-replication/).

**Availability.** Suppose each node is up independently with probability $1 - p$ and the coordinator can reach every node that is up. A strict write succeeds when at least $W$ of the $N$ homes are up, which has probability $\sum_{i \ge W} \binom{N}{i} (1-p)^i p^{N-i}$. A sloppy write succeeds when at least $W$ of all $n$ nodes are up, which has the same formula with $n$ in place of $N$. For $N = 3$, $W = 2$, $n = 10$ and $p = 0.1$, the strict write fails with probability $3p^2(1-p) + p^3 = 0.028$, and the sloppy one with probability about $10^{-8}$.

## Classic examples

- **Dynamo.** The original use: every get and put goes to the first $N$ healthy nodes of the preference list, a hinted replica is stored in a separate local database at the stand-in, and a periodic task hands it back (DeCandia et al. 2007, Section 4.6). Dynamo uses it so that the shopping cart accepts writes during node failures and data center outages. See [Dynamo-style replication](/dynamo-style-replication/).
- **Hinted handoff.** The repair half of the technique, which moves the data from the stand-ins to the homes. See [hinted handoff](/hinted-handoff/).
- **Strict versus sloppy quorums.** The ABD style register of [quorum replication](/quorum-replication/) uses strict quorums only; it is the case where the technique is not allowed, because the proof of linearizability rests on intersection.
- **Leaderless stores in practice.** Kleppmann (2017, Chapter 5) describes sloppy quorums as optional in Dynamo-style stores: Riak enables them by default, while Cassandra and Voldemort disable them by default. See [leaderless replication](/leaderless-replication/).

## Variations

- **Count only home acks.** Send to the stand-ins, but let the write succeed only when $W$ *home* nodes have acked. This is a strict quorum with extra copies: the stand-ins add durability and help repair, but not availability.
- **A separate primary quorum.** Let the client ask for at least $W' \le W$ acks from home nodes in addition to the $W$ acks from anyone. With $W' + R > N$ for reads that only use homes, reads again meet writes.
- **Write availability with one copy.** Accept a write once a single node anywhere has stored it or a hint for it. This is the most available form, and the least durable: one crash can lose the write.
- **Reads from homes only.** Make reads strict and writes sloppy. Reads can then fail during failures, but a read that succeeds still can miss a write stored only at stand-ins; intersection needs both sides to use homes.
- **Wider fallback.** Choose stand-ins in other racks or data centers, so that one outage does not take the homes and the stand-ins at once.

## Pitfalls

- **Treating R + W > N as a promise.** Wrong: tell users that $R + W > N$ gives fresh reads. Right: with sloppy quorums it gives nothing while the cluster is split or nodes are failing; the counterexample above has $R + W = 4 > 3$ and a stale read.
- **Stale reads without a partition.** Wrong: assume that stale reads need a network partition. Right: a home that was down and comes back before its hints arrive is again in $T$ and answers with old data. For example, with A down a write goes to B, C and D (for A), and C and D ack while the copy for B is still on its way; A comes back, and a read that gets its replies from A and B returns the old value.
- **Hints that never return.** Wrong: rely on the stand-in to deliver every hint. Right: a stand-in can crash or drop old hints, so a home can stay stale for good unless [anti-entropy](/anti-entropy/) also runs.
- **Too many stand-ins in one place.** Wrong: take the next nodes on the ring as stand-ins without regard to placement. Right: if they are in the same rack as the failed homes, one outage removes both.
- **Siblings.** Wrong: assume that writes on both sides of a partition are ordered. Right: they are concurrent; the store must keep both, as with [vector clocks](/vector-clocks/), or lose one, as with [last-writer-wins](/last-writer-wins/).

## Exercises

1. Show that if $R + W > n$, a sloppy read set and a sloppy write set always share a node, whatever the two views are. Why is this condition of little use in practice?
2. In the counterexample, find the smallest change to $R$ or $W$ that makes the read on the side {A, C} fail instead of returning the old value.
3. With $N = 3$, $W = 2$ and $p = 0.05$, compute the probability that a strict write fails and the probability that a sloppy write fails for $n = 6$.
4. Give a run with no partition and no crash, only with wrong suspicions by the failure detector, in which a sloppy read misses a successful write.

## References
