---
tag: 97JH7N
kind: technique
slug: hinted-handoff
name: Hinted handoff
aliases:
- hinted handoff
area: distributed/replication-and-crdts
level: advanced
summary: When a replica cannot be reached, another node stores the write with a hint that names that replica, and sends the write to it when it is reachable again.
prereqs: [leaderless-replication, failure-detector]
see_also: [sloppy-quorum, dynamo-style-replication, read-repair, anti-entropy, tombstone, crash-recovery, write-ahead-logging, eventual-consistency]
sources:
  - paper: doi:10.1145/1294261.1294281
    title: Giuseppe DeCandia, Deniz Hastorun, Madan Jampani, Gunavardhan Kakulapati, Avinash Lakshman, Alex Pilchin, Swaminathan Sivasubramanian, Peter Vosshall and Werner Vogels, Dynamo, Amazon's highly available key-value store, Proceedings of the 21st ACM Symposium on Operating Systems Principles (SOSP), 205-220, 2007
    locator: Section 4.6 (hinted replicas kept in a separate local database, scanned periodically and delivered when the intended node recovers) and Section 4.7 (anti-entropy for the case where hinted replicas become unavailable)
  - url: https://cassandra.apache.org/doc/latest/cassandra/managing/operating/hints.html
    title: Apache Cassandra documentation, Hints
    locator: hints as a best-effort repair at write time, stored at the coordinator and replayed when the replica returns, max_hint_window (default 3 hours), and why hints do not replace anti-entropy repair
  - book: isbn:9781449373320
    title: Martin Kleppmann, Designing Data-Intensive Applications, O'Reilly, 2017
    locator: Chapter 5, the section Sloppy Quorums and Hinted Handoff
---

Hinted handoff is a repair technique for replicated stores. When a write is meant for a replica that cannot be reached, another node stores the write together with a **hint**, a record that names the intended replica. The node holding the hint checks from time to time whether that replica is reachable again, and when it is, it sends the write there and deletes the hint. In Dynamo the stand-in is one of the nodes of a [sloppy quorum](/sloppy-quorum/), and the hinted copy counts toward the write quorum (DeCandia et al. 2007, Section 4.6). In Cassandra the coordinator itself keeps the hint. In both, hinted handoff shortens the time a returning replica stays stale, but it is best effort: it does not by itself guarantee that replicas converge, so stores also run [anti-entropy](/anti-entropy/).

## In plain words

You have a letter for a friend who is away. Your neighbor takes it and puts a note on it: "for Sam". Each day the neighbor looks to see if Sam is home. When Sam is back, the neighbor gives the letter to Sam and throws the note away.

This works well when Sam is away for a short time. If the neighbor loses the letter, or Sam is away for months and the neighbor gives up, Sam never gets it. So you need another way to catch up as well, such as Sam comparing notes with the other friends who got the same letter.

## When it applies

- Data is replicated on a fixed set of home replicas per key, as in [leaderless replication](/leaderless-replication/) and [Dynamo-style replication](/dynamo-style-replication/).
- The model is the [asynchronous model](/asynchronous-model/) with message passing and [crash-recovery](/crash-recovery/) failures: a replica can be down or cut off for a while and then come back with the state it had.
- Some node can detect, by a [failure detector](/failure-detector/) or a timeout, that a replica did not take a write, and later that the replica is reachable again.
- Writes are idempotent or carry versions, so a write that arrives late, twice, or after a newer write does no harm. This is the case for version merges with [vector clocks](/vector-clocks/) and for [last-writer-wins](/last-writer-wins/).

## The template

The holes are in capitals. HOLDER(write, home) chooses the node that keeps the hint, REACHABLE(home) is the holder's current view, DELIVER sends the data and waits for the home's ack, and EXPIRE is the rule for giving up on a hint.

```pseudo id=main
ON-WRITE-MISS(write, home)                       ▷ the write could not reach home
L1  h ← HOLDER(write, home)                       ▷ a sloppy-quorum stand-in, or the coordinator itself
L2  h stores (home, key, version) durably in its hint store, apart from its own data

HANDOFF, periodically at a holder h
L3  for each hint (home, key, version) at h do
L4      if EXPIRE(hint) then drop the hint                 ▷ anti-entropy must now repair home
L5      else if REACHABLE(home) then
L6          DELIVER(home, key, version); on ack, drop the hint
L7          if h is not a home of key, drop h's copy of key unless a newer local write needs it
```

**What it guarantees.** Suppose the holder does not lose its hint store, the hint does not expire, and the home is eventually reachable from the holder for long enough. Then the home eventually receives the version and merges it, so the home holds that version or a newer one from then on. If line L6 delivers the same hint twice, for example because the ack was lost, the merge makes the second delivery harmless.

**What it does not guarantee.**

- It does not repair writes that no node recorded as missed: a home that acked a write and then lost its disk, or a write that failed at a node no one noticed.
- It does not survive the loss of the holder. A hint lives on one node; if that node fails for good before line L6, the home never gets the write from this path.
- It does not keep reads fresh. Until line L6 runs, reads that go to the home return old data; with a sloppy quorum they can miss a successful write.
- It does not wait forever. Real stores expire hints (line L4) after a window, to bound the space used for a node that may never return.

These gaps are why Dynamo also runs Merkle tree [anti-entropy](/anti-entropy/) between replicas (Section 4.7), and why the Cassandra documentation says that hints do not replace repair.

**Example.** Nodes A to E, $N = 3$, $R = W = 2$, and a key whose homes are B, A and C. A partition separates {B, D, E} from {A, C}. A write on the first side is stored at B, at D with the hint "for A" and at E with the hint "for C". While the partition lasts, A and C are not reachable from D or E, so lines L5 to L7 do nothing. When it heals, D sends the version to A and E sends it to C; both drop their hints and their copies, and the three homes hold the new value. If D had crashed for good before the partition healed, A would get the value only through [read repair](/read-repair/) or anti-entropy.

## Classic examples

- **Dynamo.** The stand-in from the [sloppy quorum](/sloppy-quorum/) keeps hinted replicas in a separate local database that it scans periodically; when it sees that the intended node has recovered, it sends the replica and may delete its copy (DeCandia et al. 2007, Section 4.6). See [Dynamo-style replication](/dynamo-style-replication/).
- **Cassandra.** The coordinator of a write stores a hint for each replica that did not respond, and replays it when the failure detector reports that the replica is back. Hints are generated for a failed replica only during the first max_hint_window after it fails, 3 hours by default; a replica that is down longer misses later writes, and repair must bring it up to date.
- **Deletes.** A delete is sent as a [tombstone](/tombstone/), and a tombstone travels through hints like any write, so a replica that was down also learns of the deletion.
- **Leaderless stores in general.** Kleppmann (2017, Chapter 5) presents hinted handoff together with sloppy quorums as the way Dynamo-style stores keep writes available, with [read repair](/read-repair/) and anti-entropy as the other two repair paths; see [leaderless replication](/leaderless-replication/).

## Variations

- **Hint at the coordinator or at a stand-in.** A stand-in from the ring spreads the hints of a failed node over many nodes, and its copy can count for the write quorum. A hint at the coordinator is simpler and keeps the replica set fixed, but does not add availability.
- **Hint the data or only the key.** A hint can carry the full version, or only the key, in which case the holder reads its current version at delivery time. The second form uses less space but needs the holder to hold the key.
- **Throttled replay.** Delivery is rate limited so that a returning node is not overloaded by a backlog of hints from every other node.
- **Expiry.** Hints expire after a window, or when the total hint store passes a size limit. An expired hint turns into work for anti-entropy.
- **Hints for whole ranges.** When a node is down long, it is often cheaper to stream the key range from other replicas than to replay many hints. This is the step from hinted handoff to anti-entropy.

## Pitfalls

- **Hints as the only repair.** Wrong: run without anti-entropy because hints exist. Right: hints are lost with their holder and expire, so a long outage leaves replicas stale for good.
- **Hints in memory.** Wrong: keep hints only in memory. Right: a holder that restarts then forgets every pending hint; store them durably, as with a [write-ahead log](/write-ahead-logging/).
- **Expiry versus deletes.** Wrong: let a hinted tombstone expire and then let replicas drop tombstones after a grace period. Right: if the home misses the tombstone and all other replicas drop it, the old value comes back from the home; run repair within the tombstone grace period.
- **Replay storms.** Wrong: replay all hints at full speed when a node returns. Right: throttle, or the returning node falls over again.
- **Stand-in copies left behind.** Wrong: leave the stand-in's copy in place after handoff. Right: drop it, or it takes space and can return stale data to reads that reach it later.

## Exercises

1. Show that delivering a hint twice, or delivering two hints for the same key in either order, leaves the home in the same state when versions are merged as in [Dynamo-style replication](/dynamo-style-replication/).
2. Give a run in which every hint is delivered but a home still misses a write. Which repair path fixes it?
3. A node is down for time $t$. Writes to its keys arrive at rate $\lambda$, and each hint takes $s$ bytes. Estimate the hint space used across the cluster, and the replay time at a throttle of $b$ bytes per second.

## References
