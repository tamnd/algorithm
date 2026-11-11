---
title: Correctness of the Lindén-Jonsson priority queue
proves: [correctness, linearizability, progress]
status: sketch
---

This is a sketch. It follows the pseudocode on the main page, with the line labels L1 to L35, in the model of that page: sequential consistency, atomic read, write, CAS and fetch-and-or (FAO) on one word, and no reuse of node addresses. Lindén and Jonsson give their own argument and a model check; the argument here is ours and is not a full proof.

## Terms

The *chain* is the sequence of nodes reached from head by bottom pointers. A node $y$ in the chain is *deleted* when the bottom pointer into $y$ is marked. The *prefix* is the set of deleted nodes in the chain. The abstract queue $Q$ is the multiset of keys of the nodes in the chain that are not deleted and are not sentinels.

## Invariants

**Lemma 1 (marks are permanent).** Once a bottom word $x.\mathit{next}[0]$ with $x \ne$ head is marked, it never changes again.

*Proof sketch.* The only steps that change a bottom word are the write at L11, the CAS at L12, the FAO at L23 and the CAS at L27. L11 writes the word of a node that is not yet in the chain. L12 expects an unmarked value. L27 acts on head only. The FAO leaves a marked word as it is. ∎

**Lemma 2 (marked prefix).** In every state, the marked bottom pointers of the chain come before all its unmarked ones.

*Proof sketch.* At the start no pointer is marked. An FAO at L23 by a delete-min that reached $x$ did so through a marked pointer into $x$ (the loop goes on only after a marked old value, and the first FAO is on head), or $x$ is head. So when it marks $x.\mathit{next}[0]$, all pointers before it in the chain are marked, by Lemma 1, provided $x$ is still in the chain. If $x$ was cut off by L27, then $x.\mathit{next}[0]$ is no longer a pointer of the chain, and the chain does not change. An insert at L12 changes an unmarked pointer to an unmarked pointer, so a marked pointer cannot follow it. The CAS at L27 replaces head's word with a marked pointer to a node $y$ that the winner reached by marked pointers; it removes a part of the prefix from the front, so the order is kept. ∎

**Lemma 3 (sorted).** The keys of the nodes that are not deleted are in non-decreasing order along the chain.

*Proof sketch.* An insert of $k$ links at L12 between preds[0] and succs[0], where LOCATE_PREDS stopped. The walk at level 0 passes nodes with key below $k$ and deleted nodes, and stops at a node with key at least $k$ that is not deleted. The CAS succeeds only if preds[0] still points to succs[0] with no mark, so no node came between them and succs[0] is still not deleted. The nodes before the new node that are not deleted have keys below $k$, or were inserted later in front of it with the same argument. Deleting a node and cutting the prefix do not change the order of the other nodes. ∎

**Lemma 4 (no lost node).** A node that an insert linked at L12 stays in the chain until a FAO deletes it.

*Proof sketch.* Only the CAS at L27 removes nodes from the chain, and it removes nodes before newhead only. Each of them was reached by the winner through marked pointers, so each has a marked incoming pointer: it is deleted. An insert can link a node only behind an unmarked pointer, so by Lemma 2 never between two deleted nodes. So the nodes before newhead were deleted when the winner walked past them and no insert added a node among them later. The CAS succeeds only if head's word is still obshead, so no other cut happened in between. ∎

This is the step that fails when the deletion flag is in the node: then the pointer of a deleted node is not marked, an insert can link behind it, and the cut removes the new node. The test `test_a_deletion_flag_in_the_node_loses_an_insert` shows this run.

## Theorem 1 (linearizability)

Take as linearization points: for insert, its successful CAS at L12; for a delete-min that returns $v$, its FAO at L23 whose old value was not marked; for a delete-min that returns EMPTY, its last read at L20, which saw a pointer to tail. Each point is inside its operation.

*Proof sketch.* At the point of an insert, its node enters the chain, after the prefix (it is linked behind an unmarked pointer) and not deleted, so $Q$ gains $k$. At the point of a delete-min, the FAO changes the first unmarked pointer of the chain to marked (Lemma 2, and the walker reached $x$ by marked pointers). The node behind it is the first node that is not deleted, so by Lemma 3 it has a least key of $Q$, and it leaves $Q$. This needs $x$ to be still in the chain at the FAO: if it was cut off, its pointer was marked before the cut (Lemma 4), so the FAO would have seen a mark. For EMPTY, the read sees that the node after the walker's $x$ is tail; $x$ is deleted or head, and every node between head and $x$ is deleted, so $Q$ is empty at that moment. The cut at L27 and RESTRUCTURE change no pointer that decides membership, by Lemma 4, so they do not change $Q$. So the order of the points gives a legal sequential history with the same results. ∎

The upper levels play no part in this argument. They are hints: LOCATE_PREDS uses them only to reach a point of the chain faster, and all decisions are made at level 0. A hint can point into a node that has been cut off; the walk then goes through marked pointers and continues in the chain, since a cut-off node's pointers still lead to the chain.

## Theorem 2 (lock-freedom)

*Proof sketch.* Suppose that from some point on, processes take infinitely many steps but no operation completes. An insert loops at L10 to L12 only after a failed CAS at L12, which means the word changed after it was read: an insert completed its L12 (then it finishes in a bounded number of further steps unless its upper level loop fails, and each failure of L16 again needs a change by another process), or an FAO marked it. The upper level loop ends after at most $t$ successful CAS steps or one failed check. A delete-min ends at its first FAO that sees an unmarked value; each FAO that sees a marked value moves it one node along the chain, and the chain before the first unmarked pointer is finite and grows only when an FAO that deletes a node succeeds, which completes a delete-min after a bounded number of steps (L25 to L29 and a RESTRUCTURE whose loops each end after a CAS that fails only when another process moved head). RESTRUCTURE's walks are finite because the prefix is finite. So some operation completes. ∎

The queue is not wait-free. A delete-min can walk forever if other delete-min operations keep deleting nodes in front of it.

## Theorem 3 (one write outside the head)

A delete-min changes at most one word outside head: the word its deciding FAO marks.

*Proof sketch.* Its other FAO steps see a marked value and leave the word as it is. Its CAS steps at L27 and L35 act on head words. It makes no other writes. ∎

The test `test_delete_min_writes_one_word_besides_the_head` checks this for each delete-min of a sequential run of 200 operations.
