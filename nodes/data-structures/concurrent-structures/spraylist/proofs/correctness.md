---
title: The SprayList is a linearizable, lock-free relaxed priority queue
proves: [correctness, linearizability, progress]
status: full
---

We use the pseudocode of the page. Each read and each compare-and-swap (CAS) of a next reference with its mark bit, of a claimed flag, and of a counter is atomic. Keys are distinct (each insert adds a unique serial number). The specification is the relaxed priority queue on a multiset $Q$: insert$(x)$ adds $x$; delete-min removes and returns any item of $Q$, and returns EMPTY only if $Q$ is empty.

We use the facts about the lock-free skip list of Herlihy and Shavit that the skip list operations here are copied from: (S1) every level, followed from the head, is sorted by key; (S2) a reference is marked only by REMOVE of its own node, at line L17, and a marked reference never changes again; (S3) a node is unlinked from a level only by a CAS in FIND that requires its reference on that level to be marked; (S4) the CAS of line L14 links the new node on level 0 between two adjacent unmarked nodes, so it adds exactly this node to level 0. Here REMOVE is called only for a node that the same thread has claimed, so by (S2) and (S3):

**Lemma 1.** A node that is unlinked from level 0 was claimed before. A claimed node is never unclaimed.

*Proof.* REMOVE runs only after the caller's successful claim, at line L6 or line L10. A claimed flag is only set from false to true. $\square$

**The abstraction.** At each moment, $Q$ is the set of items of the nodes that are linked on level 0 and not claimed.

**Lemma 2 (claims).** At a successful claim of node $u$, $u$ is in $Q$ just before the step, and the step removes exactly $u$ from $Q$.

*Proof.* The thread reached $u$ by following references from the head, on level 0 or by a spray on higher levels, so $u$ had been linked on level 0 before it was reached: a node becomes visible only through the CAS of line L14, and line L16 links it on higher levels only after that. The flag of $u$ was false just before the CAS. By Lemma 1, $u$ was not unlinked, since it was not claimed. So $u$ is linked and unclaimed, in $Q$, and the CAS makes it claimed. No other node changes. $\square$

**Lemma 3 (the scan).** Suppose a delete-min reads $l = linked$ and then $s = started$ at line L8, finds no node to claim in line L10, and reads $started = s$ again at line L11 with $l = s$. Then $Q$ is empty at the moment of the last read.

*Proof.* Always $linked \le started$, since each insert increments $started$ before $linked$. At the moment of the first read of $started$, $linked \ge l = s = started$, so $linked = started$: every insert that had begun had already passed line L15, and so line L14. Since $started$ has the same value at the last read, no insert began between the two reads. So no CAS of line L14 happens in this interval, and no node is added to level 0. Let $u$ be any node that is linked on level 0 at the end of the interval. It was linked at the start too. If $u$ was ever claimed, it is still claimed (Lemma 1), and not in $Q$. Suppose $u$ was never claimed. Then $u$ is never unlinked from level 0 in the interval (Lemma 1), and its reference on level 0 is never marked. The scan of line L10 walks level 0 from the head, in increasing key order by (S1). When it reads the reference of a node $v$ with key smaller than that of $u$, that reference points to a node with key at most that of $u$: if $v$ is linked, because $u$ is linked and level 0 is sorted; if $v$ was unlinked, because its reference was frozen when it was marked (S2), at a moment when $v$ was linked and $u$ was linked too. So the scan cannot jump over $u$; it reaches $u$, finds it unclaimed and claims it, which contradicts the assumption. So every linked node is claimed, and $Q$ is empty. $\square$

**Theorem (linearizability).** Each history of the SprayList is linearizable with respect to the relaxed priority queue.

*Proof.* Choose the points: an insert at its successful CAS of line L14; a delete-min that returns an item at its successful claim; a delete-min that returns EMPTY at its last read of $started$ in line L11. Each is inside its call, and the order of the points respects real time; pending calls past their point are completed, the others removed.

$Q$ changes only at these points: by (S4) the CAS of line L14 adds the new, unclaimed node, so it adds the item to $Q$; by Lemma 2 a claim removes the claimed item from $Q$; other steps change neither the set of nodes on level 0 in a way that touches unclaimed nodes (Lemma 1) nor any claimed flag. A delete-min returns the item of the node it claimed, which was in $Q$ by Lemma 2. EMPTY is returned only when $Q$ is empty, by Lemma 3. Replaying the points in order gives a legal sequential history of the relaxed specification with the same results. $\square$

**Theorem (lock-freedom).** In every infinite execution in which some call is pending, infinitely many calls finish.

*Proof.* Suppose that from some moment $\tau$ no call finishes. Then from $\tau$ no claim succeeds after some point, since a claimer finishes its REMOVE and returns within finitely many steps unless REMOVE runs for ever, and REMOVE only fails to end if the CASes of its FIND fail for ever; in the lock-free skip list each failed CAS in FIND or in the CASes of insert is caused by a successful CAS of another thread on the same reference, which links or unlinks a node or marks a reference. Each successful linking CAS belongs to an insert, which then finishes its level 0 link and, after at most one link per level, returns; each successful mark belongs to a REMOVE, with at most one mark per level; each successful unlinking CAS removes a marked node from a level, and marked nodes are finite in number when no claim succeeds. So after some moment no CAS succeeds, every pending CAS of FIND, insert and REMOVE succeeds on its next try, and some insert or delete-min finishes. That leaves the case where only delete-mins without claims run after $\tau$: each one either claims a node, which is excluded, or reaches line L11. All inserts have finished, so $linked = started$ stays fixed, and the test of line L11 passes and the call returns EMPTY. Each case contradicts the assumption. $\blacksquare$
