---
tag: QP641E
kind: concept
slug: log-compaction
name: Log compaction and snapshotting
aliases:
- snapshotting
area: distributed/consensus
level: advanced
summary: A replica replaces the committed prefix of its replicated log by a snapshot of the state that the prefix produces, so the log stays small. A lagging follower gets the snapshot instead of the entries.
prereqs: [replicated-log, replicated-state-machine, raft]
see_also: [raft, multi-paxos, checkpointing, write-ahead-logging, log-structured-merge-tree, cluster-reconfiguration, chandy-lamport-snapshot, crash-recovery]
sources:
  - url: https://raft.github.io/raft.pdf
    title: Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm (extended version), 2014
    locator: Section 7 (log compaction), Figure 12 (a snapshot replaces the committed entries) and Figure 13 (the InstallSnapshot RPC)
  - paper: "Diego Ongaro, Consensus: bridging theory and practice, PhD thesis, Stanford University, 2014"
    locator: Chapter 5 (log compaction, including snapshots of memory-based and disk-based state machines and incremental cleaning)
  - paper: doi:10.1145/1281100.1281103
    title: Tushar D. Chandra, Robert Griesemer and Joshua Redstone, Paxos made live, an engineering perspective, Proceedings of the 26th ACM Symposium on Principles of Distributed Computing (PODC), 2007
    locator: the section on snapshots, which the replicas of Chubby take on their own and use to truncate the Paxos log
---

Log compaction is the step that keeps the [replicated log](/replicated-log/) of a [replicated state machine](/replicated-state-machine/) from growing without bound. A replica takes a snapshot of its state after it has applied the entries up to some index, writes the snapshot to stable storage, and discards those entries. The snapshot records the index and term of the last entry it replaces, so that the log consistency checks still work at its boundary. A follower that is so far behind that the leader has discarded the entries it needs gets the snapshot instead, through the InstallSnapshot call of [Raft](/raft/).

## In plain words

A bank keeps a list of every deposit and withdrawal. After years, the list is very long, and a new branch that wants a copy must read it all. So at the end of each month the bank writes down the balance of each account and throws away the older lines. The balance sheet says "this is the state after line 9000". To rebuild, read the balance sheet and then the lines after 9000.

Only finished lines may go into the balance sheet. A line that might still be undone must stay in the list.

If a branch is so far behind that the lines it needs are gone, the bank sends it the balance sheet first, and then the newer lines.

## The idea

**The state machine view.** A replica applies commands $c_1, c_2, \ldots$ of the log, in order, to a deterministic state machine that starts in state $s_0$. After applying entries 1 to $i$, its state is $s_i = \delta(\ldots\delta(\delta(s_0, c_1), c_2)\ldots, c_i)$. Since $\delta$ is deterministic, $s_i$ holds all the information that a replica needs about the prefix $c_1 \ldots c_i$. So the replica can store

$$\text{snapshot} = (s_i,\ \text{lastIncludedIndex} = i,\ \text{lastIncludedTerm} = \text{term of entry } i,\ \text{configuration at } i)$$

and delete entries 1 to $i$. Recovery loads the snapshot and replays the entries after $i$, which gives the same state as replaying the full log. The configuration is in the snapshot because [cluster reconfiguration](/cluster-reconfiguration/) stores membership in log entries, and the replica must not lose it.

**Why the term is kept.** In Raft, the AppendEntries consistency check for entry $i+1$ compares the index and term of entry $i$. After compaction, entry $i$ is gone, so the replica uses lastIncludedIndex and lastIncludedTerm for that check. Without them, the [log matching](/raft/) argument would have no base at the boundary.

**The safety condition.** A replica may put into a snapshot only entries that are committed and that it has applied. The reason is that committed entries never change: every replica that applies an entry at index $j$ applies the same command (the state machine safety property). So the snapshots of all replicas are states $s_i$ of one and the same sequence, possibly at different $i$, and a snapshot from one replica can replace the log prefix of another. An entry that is not yet committed can still be overwritten by a new leader; a snapshot that included it would hold a state that the cluster never agrees on, and no later message could undo it.

**InstallSnapshot.** Each Raft server compacts on its own. When the leader must send entry $j$ to a follower (its nextIndex for that follower is $j$) and the leader has already compacted past $j$, it sends its snapshot instead, in chunks. Figure 13 of the Raft paper gives the rules. The follower:

1. Replies at once if the term of the call is less than its own current term.
2. Writes the chunks, and acts when the last chunk arrives.
3. If it has a log entry with the same index and term as the last included entry of the snapshot, it keeps the entries after it, and stops. Its own state machine may be behind; it may load the snapshot or keep applying entries.
4. Otherwise it discards its whole log and resets its state machine to the snapshot.

**Why step 4 is safe.** Let the snapshot cover index $i$ with term $T$, and suppose that the follower's entry at $i$ is missing or has a term other than $T$. Assume that some entry of the follower at an index $j > i$ is committed. Then, by leader completeness, the leader has the same entry at $j$, and by log matching the two logs agree at every index up to $j$, including $i$. This contradicts the assumption. So no entry that step 4 discards is committed. In step 3, log matching says that the follower's log up to $i$ equals the leader's, so the snapshot replaces exactly the prefix that it describes.

**When and how to snapshot.** A common policy is to snapshot when the log is some factor larger than the last snapshot, so that the cost of writing snapshots, amortized over the entries, stays bounded. Writing a large snapshot takes time, so implementations use copy-on-write (for example a fork of the process, or persistent data structures) and let the replica keep serving. A state machine that already lives on disk, such as a [log-structured merge tree](/log-structured-merge-tree/), can compact in increments instead of writing one full snapshot.

## Examples

A key-value store has this committed log in Raft, with commitIndex = 4 and lastApplied = 4.

| index | term | command |
|---|---|---|
| 1 | 1 | x ← 3 |
| 2 | 1 | y ← 1 |
| 3 | 1 | y ← 9 |
| 4 | 2 | x ← 2 |
| 5 | 3 | z ← 0 (not committed) |

The leader takes a snapshot at index 4: state $\{x: 2, y: 9\}$, lastIncludedIndex = 4, lastIncludedTerm = 2. Its log now holds only entry 5. Entry 5 must stay in the log: it is not committed, and a later leader could replace it.

A follower that crashed after index 2 comes back. The leader's nextIndex for it is 3, but the leader's first entry is now 5, so it sends InstallSnapshot with the state above. The follower's entry at index 4 does not exist, so it discards its log (entries 1 and 2, which the snapshot covers anyway), loads $\{x: 2, y: 9\}$, and sets its last index to 4. The next AppendEntries, for entry 5, checks the previous entry (index 4, term 2) against the values from the snapshot, and succeeds.

**Non-example.** A replica that snapshots at index 5 above, before entry 5 is committed, keeps $z = 0$ in its state. If a new leader then replaces entry 5 by a different command, the replica has no log entry left to overwrite, and its state differs from the others for good.

**A different meaning.** In Apache Kafka, log compaction means keeping only the last record for each key in a topic. That is compaction of a message log by key, not a snapshot of a state machine.

## Where it is used

- **Raft implementations.** etcd, Consul and other Raft systems take snapshots on each server and send them to followers that are far behind or new.
- **Paxos systems.** Chubby's replicas take snapshots of the database and truncate the Paxos log (Chandra, Griesemer and Redstone, 2007).
- **Databases.** [Checkpointing](/checkpointing/) in a database with [write-ahead logging](/write-ahead-logging/) is the same idea on one machine: after a checkpoint, [crash recovery](/crash-recovery/) can ignore the older part of the log.
- **Adding a replica.** A new server in a [reconfiguration](/cluster-reconfiguration/) catches up by loading a snapshot and then the newer entries.

## References
