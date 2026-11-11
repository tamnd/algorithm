---
tag: BQWX41
kind: concept
slug: replicated-log
name: Replicated log
aliases:
- Log replication
- replicated log
- replicated op log
- replicated write-ahead log
area: distributed/replication-and-crdts
level: core
summary: The numbered sequence of commands that replicas agree on, with a committed prefix and an apply index; consensus fills its slots and snapshots bound its length.
prereqs: [state-machine-replication, consensus-problem, total-order-broadcast]
see_also: [replicated-state-machine, multi-paxos, raft, viewstamped-replication, zab, log-compaction, active-replication, write-ahead-logging]
sources:
  - url: https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro
    title: Diego Ongaro and John Ousterhout, In search of an understandable consensus algorithm, USENIX ATC 2014, 305-319
    locator: Figure 2 (commitIndex, lastApplied, the AppendEntries receiver rules), Section 5.3 (log replication, the Log Matching Property), Section 5.4.2 (committing entries from previous terms) and Section 7 (log compaction)
  - paper: "Leslie Lamport, Paxos made simple, ACM SIGACT News 32(4), 51-58, 2001"
    locator: Section 3 (implementing a state machine, gaps in the sequence of instances filled with no-op commands)
  - paper: doi:10.1145/2673577
    title: Robbert van Renesse and Deniz Altinbuken, Paxos made moderately complex, ACM Computing Surveys 47(3), article 42, 2015
    locator: the replica, with its slot_in and slot_out indexes and the invariants on decided slots
  - paper: doi:10.1145/98163.98167
    title: Fred B. Schneider, Implementing fault-tolerant services using the state machine approach, a tutorial, ACM Computing Surveys 22(4), 299-319, 1990
    locator: Section 3 (the requirements Agreement and Order, and when a request is stable)
---

A replicated log is the data structure at the core of [state machine replication](/state-machine-replication/): a sequence of numbered slots, each holding one command, that all replicas agree on slot by slot. Each replica keeps two indexes on it, the end of the committed prefix and the end of the applied prefix, and runs the committed commands on its state machine in slot order. A consensus protocol such as [Multi-Paxos](/multi-paxos/) or [Raft](/raft/) decides what goes into each slot. State machine replication is the approach (same commands, same order, same state); the replicated log is the object that carries the order, with its own rules for gaps, overwrites, commitment and truncation.

## In plain words

Think of a shared notebook with numbered lines. Each line holds one instruction, such as "add 5 to the balance". Several computers each keep a copy of the notebook. A line is final once enough computers have agreed on it. After that, nobody may change it.

Each computer reads its notebook from the top and carries out the instructions in order. It keeps a bookmark at the last line it has carried out. It may only move the bookmark onto a line that is final, and it may never skip a line. If line 5 is still open while line 6 is final, the computer waits at line 4.

A notebook cannot grow forever. So a computer can write down the result of all lines up to some point, and then tear those pages out.

## The idea

### Slots, entries and the two indexes

A log is a map from slot numbers $1, 2, 3, \ldots$ to entries. In Raft an entry is a pair (term, command). In Multi-Paxos an entry is the value voted for or chosen in that slot, with its ballot. A replica keeps:

- the **commit index** $c$: every slot $1, \ldots, c$ holds a committed entry, that is, an entry that a quorum has accepted in a way that no later leader can change (Raft calls it commitIndex; in Paxos the entry is *chosen*);
- the **apply index** $a$: the state machine has applied slots $1, \ldots, a$ (Raft calls it lastApplied).

The rules are $a \le c$, and the apply loop is: while $a < c$, set $a \leftarrow a + 1$ and apply the command of slot $a$. By the theorem of [state machine replication](/state-machine-replication/), two replicas with the same apply index are in the same state, because the committed prefix is the same at all replicas. Safety of the log means exactly this: **no two replicas commit different entries in the same slot**.

The slots after $c$ are not stable. A replica may hold entries there that a new leader later overwrites. A replica must never apply them and never answer a client from them.

### How Multi-Paxos fills the log

[Multi-Paxos](/multi-paxos/) runs one instance of [Paxos](/paxos/) for each slot. A leader may propose in many slots at once, so slots can be chosen out of order, and a replica can know slot 6 while slot 5 is still open. That open slot is a **gap**. The commit index is the end of the longest chosen prefix, so a gap blocks the apply loop. When a new leader takes over, it runs phase 1 for all open slots. For a slot where some acceptor reports a vote, the leader must propose the reported value. For a slot with no reported vote below the highest known slot, it proposes a **no-op**, a command that leaves the state unchanged. Lamport (2001, Section 3) describes this filling of gaps. After that the prefix is complete and the replicas can apply past the old gap.

### How Raft fills the log

[Raft](/raft/) fills slots strictly in order from one leader. The AppendEntries message carries the index and the term of the entry just before the new ones (prevLogIndex and prevLogTerm). A follower accepts only if its own log holds an entry at prevLogIndex with that term. If an existing entry conflicts with a new one (same index, different term), the follower deletes it and all entries after it, then appends the new ones. Then it sets its commit index to the minimum of the leader's commit index and the index of the last new entry. This check gives the **Log Matching Property**: if two logs hold an entry with the same index and term, the entries are equal and the logs are equal in all earlier slots (Ongaro and Ousterhout, Section 5.3). So Raft logs have no gaps, and a follower's log is always a prefix of the leader's log after a successful AppendEntries.

The leader commits an entry of its current term when a majority holds it. It never commits an entry of an older term by counting replicas; that entry becomes committed only as part of the prefix of a newer committed entry (Section 5.4.2). The paper shows, in its Figure 8, a run in which counting replicas for an old entry would let a committed entry be overwritten.

### Compaction and snapshots

The log grows with every command. A replica that has applied slots $1, \ldots, a$ can save the state $s_a$ with the index $a$ and the term of slot $a$, and delete those slots. This is [log compaction](/log-compaction/). It is safe for the replica itself, because by the theorem of state machine replication $s_a$ is all that the deleted prefix determines. A follower that lags behind the start of the leader's log can no longer receive the missing entries, so the leader sends the snapshot instead (InstallSnapshot in Raft, Section 7). The saved index and term let the next AppendEntries consistency check work at the boundary.

### Log and approach, kept apart

[State machine replication](/state-machine-replication/) is the approach: deterministic replicas, same commands, same order. [Active replication](/active-replication/) and [primary-backup replication](/primary-backup-replication/) are two ways to run it. The replicated log is the structure through which consensus protocols deliver the order, and the questions on this page (gaps, overwrites of uncommitted slots, the commit rule, compaction) belong to the log, not to the approach. The page [replicated state machine](/replicated-state-machine/) gives the consensus view of the same pairing.

## Examples

**A gap in Multi-Paxos.** A replica knows that slots 1 to 4 and slot 6 are chosen, with the commands add 1, add 2, double, add 4 and add 6, on a counter that starts at 0. Its commit index is 4. It applies slots 1 to 4 and holds $((0 + 1 + 2) \cdot 2) + 4 = 10$. Slot 6 waits, because slot 5 is a gap. A new leader runs phase 1, learns of no vote in slot 5, and gets a no-op chosen there. The commit index jumps to 6, the replica applies the no-op and then add 6, and holds 16.

**A conflict in Raft.** The leader's log has the terms $[1, 1, 2, 3, 3]$ in slots 1 to 5. A follower has the terms $[1, 1, 2, 2, 2, 2]$, where slots 4 to 6 come from an old leader of term 2 and were never committed. The leader sends AppendEntries with prevLogIndex 4 and prevLogTerm 3. The follower's slot 4 has term 2, so it rejects. The leader moves back one slot and sends prevLogIndex 3, prevLogTerm 2, and its entries 4 and 5. The follower's slot 3 matches. Its slot 4 conflicts (term 2 against term 3), so it deletes slots 4 to 6 and appends the two entries. Both logs now read $[1, 1, 2, 3, 3]$.

**A snapshot.** A replica has applied 9 commands and saves (index 9, term $t_9$, state $s_9$). It deletes slots 1 to 9. A new replica installs this snapshot and then receives slots 10 onward with prevLogIndex 9 and prevLogTerm $t_9$. After applying them it is in the same state as a replica that applied all slots from the start.

## Where it is used

- **Consensus-based replication.** [Multi-Paxos](/multi-paxos/), [Raft](/raft/), [Viewstamped Replication](/viewstamped-replication/) (the op log with op numbers and a commit number) and [Zab](/zab/) are all protocols for filling a replicated log.
- **Primary-backup with a log.** A primary can ship its write-ahead log to the backups, so the backups replay the same records; see [primary-backup replication](/primary-backup-replication/) and [write-ahead logging](/write-ahead-logging/).
- **Recovery.** A replica that restarts loads its last snapshot, then replays its log from the saved index; this needs the log and snapshot to be on stable storage before a vote is sent.
- **Reconfiguration.** Raft and other protocols put configuration changes into the log as entries, so the members agree on when a change takes effect; see [cluster reconfiguration](/cluster-reconfiguration/).
- **Shared logs as a service.** Some systems offer one replicated log to many applications, which each read it and build their own state.

## References
