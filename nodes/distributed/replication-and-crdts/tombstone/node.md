---
tag: MG0079
kind: definition
slug: tombstone
name: Tombstone
aliases:
- deletion marker
area: distributed/replication-and-crdts
level: intro
summary: An entry that records a deletion so that merges do not bring the deleted item back; it can be removed only once every replica has seen it.
prereqs: [anti-entropy, last-writer-wins]
see_also: [death-certificates, two-phase-set, or-set, rga, read-repair, hinted-handoff, log-structured-merge-tree, version-vectors]
sources:
  - paper: doi:10.1145/41840.41841
    title: Alan Demers and others, Epidemic algorithms for replicated database maintenance, Proceedings of the 6th ACM Symposium on Principles of Distributed Computing (PODC), 1-12, 1987
    locator: the section on deletion and death certificates (a deleted item comes back under anti-entropy unless a death certificate replaces it; dormant death certificates and their removal)
  - url: https://cassandra.apache.org/doc/latest/cassandra/managing/operating/compaction/tombstones.html
    title: Apache Cassandra documentation, Tombstones
    locator: why deletes are writes, gc_grace_seconds and its default of 864000 seconds (10 days), zombie data when a node is down longer than the grace period, and the need to run repair within it
  - paper: "Gene T. J. Wuu and Arthur J. Bernstein, Efficient solutions to the replicated log and dictionary problems, Proceedings of the 3rd ACM Symposium on Principles of Distributed Computing (PODC), 1984"
    locator: the replicated dictionary with deletions, and the matrix of what each site knows that the others have seen, used to discard log entries that every site holds
---

## Definition

Consider a replicated store in which each replica maps keys to entries, and replicas exchange state and merge it, as in [anti-entropy](/anti-entropy/) or [read repair](/read-repair/). Each entry is a pair (stamp, value), and the merge of two entries for the same key keeps the one with the larger stamp, as in [last-writer-wins](/last-writer-wins/).

A **tombstone** for key $k$ is an entry $(s, \bot)$ for $k$, where $\bot$ is a special value that means "deleted". A delete of $k$ at a replica writes a tombstone with a new stamp $s$, in place of removing $k$. The tombstone takes part in merges like any other entry, so it beats every older write of $k$; a read that finds a tombstone returns "not found".

Without tombstones, a replica that has deleted $k$ has no entry for $k$, and a merge cannot tell "deleted here" from "never received here". The merge then copies the old value back from a replica that still holds it. This is **resurrection** of deleted data.

A tombstone $(s, \bot)$ for $k$ is **stable** when every replica holds an entry for $k$ with a stamp at least $s$, and no state or message that carries an older entry for $k$ is still on its way. A replica may **garbage collect** a stable tombstone, that is, remove it. Removing a tombstone that is not stable can resurrect the data it deleted.

The model is the [asynchronous model](/asynchronous-model/) with message passing and [crash-recovery](/crash-recovery/) failures: replicas can be down for a long time and come back with old state, which is the case that makes stability hard to know.

## Examples and non-examples

**Example: deletion without a tombstone.** Replicas $A$, $B$, $C$ all hold $x = v_1$ with stamp 1. $A$ deletes $x$ by removing it. Then $A$ and $B$ run an anti-entropy session. $B$ has $x$ and $A$ has nothing, so the merge copies $x = v_1$ to $A$. The delete is undone, and every later session spreads $x$ again.

**Example: the same run with a tombstone.** $A$ deletes $x$ by writing $(4, \bot)$. In the session with $B$, the tombstone's stamp 4 beats stamp 1, so $B$ now holds $(4, \bot)$. $C$ still has $x = v_1$ until its next session with $A$ or $B$, after which all three hold the tombstone, and every read of $x$ returns "not found".

**Example: removing a tombstone too early.** Five replicas hold $x$. Replica $R_1$ goes down at time 5. At time 8 another replica deletes $x$, and the tombstone reaches the other three live replicas. Each replica drops a tombstone 10 time units after the delete. At time 80 $R_1$ comes back, still holding $x = v_1$, and anti-entropy finds no entry for $x$ anywhere else. It copies $x$ to all replicas: the deleted value is back. Cassandra calls such values zombies. Its rule is that a tombstone is dropped at compaction after gc_grace_seconds, 864000 seconds (10 days) by default, and that repair must run on every node within that period; a node that is down longer must not rejoin with its old data.

**Example: removing a tombstone when it is stable.** Each replica tracks which replicas are known to hold the tombstone, and merges this set in each session. A replica drops the tombstone only when the set contains all replicas. In the run above, $R_1$ is missing from the set while it is down, so nobody drops the tombstone; when $R_1$ returns, it receives the tombstone, the set becomes complete, and then the replicas may drop it. No old copy of $x$ remains, so nothing can come back. Wuu and Bernstein (1984) used a matrix of such knowledge to discard entries of a replicated log once all sites had them.

**Example: CRDT tombstones.** The remove set of a [two-phase set](/two-phase-set/) is a set of tombstones: an element in it can never be added again. Sequence CRDTs such as [RGA](/rga/), [WOOT](/woot/) and [Treedoc](/treedoc/) keep deleted characters as hidden tombstones, because later inserts refer to them as positions.

**Non-example: a delete in a single-copy store.** With one copy and no merging, removing the key is enough; there is nothing that could bring it back.

**Non-example: a delete that wins by causality.** An [OR-set](/or-set/) removes exactly the add tags its replica has observed, so a concurrent add with a new tag survives, and the remove leaves no per-element marker. The tags of removed elements play the role of tombstones only in some implementations; the optimized OR-set uses version vectors in their place.

## Related definitions

- **Death certificate.** The term of Demers et al. (1987) for a tombstone spread by epidemic algorithms; they also keep *dormant* death certificates at a few sites after the others discard them, to stop late copies. See [death certificates](/death-certificates/).
- **Last-writer-wins.** The merge rule under which a tombstone with a larger stamp beats older writes; see [last-writer-wins](/last-writer-wins/). In Cassandra, a tombstone also wins over a write with the same timestamp.
- **Stability.** A tombstone, or an update in general, is stable when every replica has it. Detecting stability needs knowledge about all replicas, so a single replica that is down blocks garbage collection. Time-based rules such as gc_grace_seconds replace this knowledge by an assumption about how long a replica can stay away.
- **Compaction.** In stores built on a [log-structured merge tree](/log-structured-merge-tree/), a tombstone also hides older values in older files, and compaction removes both once the tombstone may go.
- **Hinted handoff and read repair.** Both carry tombstones like writes, so a delete reaches replicas that were down; see [hinted handoff](/hinted-handoff/) and [read repair](/read-repair/).

## References
