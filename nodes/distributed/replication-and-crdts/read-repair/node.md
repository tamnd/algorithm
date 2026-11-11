---
tag: EK4GBG
kind: technique
slug: read-repair
name: Read repair
aliases:
- read-time repair
area: distributed/replication-and-crdts
level: intro
summary: A read that gets replies from several replicas finds the newest version and writes it back to the replicas that sent an older one, either before it returns or in the background.
prereqs: [leaderless-replication, quorum-replication]
see_also: [anti-entropy, hinted-handoff, dynamo-style-replication, sloppy-quorum, tombstone, last-writer-wins, monotonic-reads, eventual-consistency]
sources:
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall and Werner Vogels, Dynamo, Amazon's highly available key-value store, Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP), 205-220, 2007
    locator: Section 5 (the coordinator of a read waits for late responses and updates the nodes that returned stale versions, called read repair) and Section 4.5 (get and put with R and W)
  - url: https://cassandra.apache.org/doc/latest/cassandra/managing/operating/read_repair.html
    title: Apache Cassandra documentation, Read repair
    locator: blocking read repair, the read_repair table option with BLOCKING and NONE, monotonic quorum reads against partition level write atomicity, the removal of background read repair (read_repair_chance) in 4.0, and why read repair does not replace other repair
  - paper: doi:10.1145/200836.200869
    title: Hagit Attiya, Amotz Bar-Noy and Danny Dolev, Sharing memory robustly in message-passing systems, Journal of the ACM 42(1), 124-142, 1995
    locator: the read protocol, in which a reader writes the value it found back to a majority before it returns
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, the section Read repair and anti-entropy
---

Read repair is a repair technique for replicated stores in which reads fix stale replicas. A read asks several replicas of a key for their versions, as a quorum read does. When the replies differ, the coordinator of the read picks the newest version, or merges concurrent versions, returns the result, and sends it to each replica that replied with an older version. The write back can be **blocking**, done before the read returns, or **background**, done after it. Blocking repair makes reads monotonic, and in the ABD register of [quorum replication](/quorum-replication/) it is what makes reads linearizable. Background repair only speeds up convergence. Either way, read repair touches only keys that are read and replicas that are asked, so a store also needs [anti-entropy](/anti-entropy/) for the rest. Dynamo uses it (DeCandia et al. 2007, Section 5), and Cassandra runs it as blocking repair.

## In plain words

You ask three friends what time the meeting is. Two say 10, and one says 9 because she missed the change. You go with 10, the newest answer, and you tell the third friend that it is 10 now.

Next time she answers right. But you only fixed the friend you asked, and only about this one meeting. Friends you did not ask, and meetings you did not ask about, can still be out of date.

## When it applies

- Data is stored on several replicas per key, and reads already ask more than one replica, as in [leaderless replication](/leaderless-replication/) and [Dynamo-style replication](/dynamo-style-replication/).
- Versions can be compared or merged: a timestamp as in [last-writer-wins](/last-writer-wins/), a tag as in quorum replication, or [vector clocks](/vector-clocks/) with a merge of siblings.
- Writing a version to a replica is safe at any time: a replica keeps the newer of what it has and what it receives, so a late or repeated repair does no harm.
- The model is the [asynchronous model](/asynchronous-model/) with message passing and [crash-recovery](/crash-recovery/) failures: replicas miss writes while they are down or slow, and come back with old data.

## The template

The holes are in capitals. ASK(key) is the set of replicas the read contacts, and WAIT is how many replies it waits for. NEWEST merges the replies into the result, MODE is blocking or background, and ACKS is how many replicas must hold the result before a blocking read returns.

```pseudo id=main
READ-WITH-REPAIR(key)
L1  send a read for key to every replica in ASK(key)
L2  wait for WAIT replies; let V be the versions they carry
L3  v ← NEWEST(V)                                   ▷ the largest stamp, or the merge of concurrent versions
L4  S ← the repliers whose version is older than v or differs from v
L5  if MODE = blocking then
L6      send v to S, and wait until ACKS replicas in all hold v (the repliers that already had it count)
L7      return v
L8  else
L9      return v, then send v to S and to replicas whose replies arrive late
```

A replica that receives $v$ stores it only if $v$ is newer than its own version, or merges it with its own versions.

**Example.** Replicas A, B and C hold $x = v_1$ with stamp 1, and $N = 3$, $R = W = 2$. A write of $v_2$ with stamp 2 reaches only B before its coordinator crashes, so the write fails, but B holds $v_2$.

- *No repair.* Read 1 gets replies from A and B and returns $v_2$. Read 2 starts later, gets replies from A and C, and returns $v_1$. A client that runs both reads sees the value go back in time.
- *Background repair.* Read 1 returns $v_2$ and then sends it to A. If read 2 reaches A after the repair, it returns $v_2$; if it reaches A before, it still returns $v_1$.
- *Blocking repair with ACKS = 2.* Read 1 sends $v_2$ to A and waits for the ack before it returns. Now A and B hold $v_2$. Every set of two replicas contains A or B, so read 2 and every later read return $v_2$ or a newer version.

**Why blocking repair makes reads monotonic.** Assume strict quorums, $R + W > N$, ACKS $= W$, and that replicas never lose data. When a blocking read returns $v$, at least $W$ replicas hold $v$ or a newer version. A later read waits for $R$ replies, and $R + W > N$ forces one of them to come from such a replica, so line L3 returns $v$ or a newer version. This is the second phase of the ABD read (Attiya, Bar-Noy and Dolev 1995), and with it the quorum register is linearizable; the full proof is on [quorum replication](/quorum-replication/).

**What it cannot do.** A replica is repaired only for keys that some read asks it about. A key that is never read stays stale on every replica that missed it, however long the store runs. A replica outside ASK(key), or whose reply comes too late for a blocking read and is ignored in background mode, is not repaired either. So read repair cannot guarantee convergence alone.

## Classic examples

- **Dynamo.** The coordinator of a get waits a little after it has $R$ replies to collect late ones, and updates the nodes that returned stale versions; the paper notes that this relieves the anti-entropy protocol (DeCandia et al. 2007, Section 5). See [Dynamo-style replication](/dynamo-style-replication/).
- **Quorum registers.** The ABD read phase writes the value with the largest tag back to a majority before it returns, which is blocking read repair with ACKS equal to a majority. See [quorum replication](/quorum-replication/).
- **Cassandra.** Read repair is blocking by default: a read that finds differences waits until the repair writes reach the consistency level. The table option read_repair set to NONE turns the write back off. The documentation describes the trade off: blocking repair gives monotonic quorum reads, but repairs only the rows that the read covers, so it can expose a part of a batch write that failed; NONE keeps such writes atomic at the partition level, but reads can go back in time. Background read repair with a probability per read was removed in version 4.0.
- **Deletes.** A [tombstone](/tombstone/) is a version like any other, so read repair spreads deletions to replicas that missed them.
- **The repair trio.** In [leaderless replication](/leaderless-replication/), read repair works with [hinted handoff](/hinted-handoff/), which repairs replicas that were known to miss writes, and [anti-entropy](/anti-entropy/), which compares whole replicas in the background.

## Variations

- **Blocking or background.** Blocking costs one more round trip on reads that find a difference and gives monotonic reads. Background repair adds no latency and only speeds up convergence.
- **Repair by probability.** Repair only a fraction of reads, or compare all replicas on only a fraction of reads, to bound the load. Older Cassandra versions did this with read_repair_chance.
- **Digest reads.** Ask one replica for the data and the others only for a hash of it. Fetch full data only when the hashes differ. This saves bandwidth when replicas usually agree.
- **Repair all replicas.** Send the result to every replica of the key, not only to the repliers. This repairs more, at the cost of a write to every replica on each repaired read.
- **Merge, not pick.** With [vector clocks](/vector-clocks/), NEWEST keeps all concurrent versions, and the repair sends every sibling, so that replicas converge on the same set.

## Pitfalls

- **Read repair as the only repair.** Wrong: rely on reads to fix every replica. Right: cold keys are never read, so they stay stale on replicas that missed a write. Run anti-entropy as well.
- **Background repair and monotonic reads.** Wrong: expect two reads in a row to never go back in time with background repair. Right: only blocking repair to a write quorum gives this.
- **Comparing with wall clock stamps.** Wrong: pick the newest version by the timestamps of writers whose clocks disagree. Right: with [clock skew](/clock-skew/), the "newest" version can be an older write, and repair then spreads the wrong value; see [last-writer-wins](/last-writer-wins/).
- **Repairs that undo deletes.** Wrong: let replicas drop tombstones before repair has reached every replica. Right: a replica that still holds the old value then wins the comparison, since no tombstone is left to beat it, and read repair spreads the deleted value back.
- **Load on hot keys.** Wrong: repair on every read of a key that is read very often. Right: concurrent reads of the same stale key all send the same repair; let one do it, or use digest reads and probability.

## Exercises

1. In the example, give a run with background repair in which read 2 returns $v_1$ although read 1 returned $v_2$ and finished before read 2 started.
2. Show that blocking repair with ACKS $= W$ and $R + W > N$ makes every later read return a version at least as new as an earlier read, and show that ACKS $= W - 1$ is not enough.
3. A store has $10^6$ keys, each read with probability $q$ per day. One replica misses all writes for an hour. What fraction of its stale keys does read repair fix in a week, as a function of $q$?

## References
