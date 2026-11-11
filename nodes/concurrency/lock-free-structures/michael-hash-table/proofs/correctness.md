---
title: The Michael hash table is a linearizable lock-free set with safe memory reclamation
proves: [correctness, linearizability, progress]
status: sketch
---

We use the pseudocode and the model of the page: $p$ asynchronous processes that may crash, atomic read, write and single-word CAS, sequential consistency, and memory that is reused as soon as it is freed. This is a proof sketch. The memory safety argument is given in full; the linearization argument for one bucket follows the proof for the Harris list, and only the steps that differ are given. The tests check the claims on all interleavings of small cases.

**Lemma 1 (buckets are independent).** An operation on key $k$ reads and writes only `bucket[h(k)]`, nodes reachable from it at some time, nodes it allocates itself, the hazard pointers, and the nodes it frees in a scan.

*Proof.* FIND starts at `bucket[h(k)]` and follows only `next` fields. INSERT and DELETE use the words FIND returns. A scan reads only hazard pointers and frees only nodes of its own retired list. ∎

**Lemma 2 (validated protection).** Suppose a process sets a hazard pointer to a node $x$ at time $t_1$ and then reads at time $t_2 > t_1$ a word that shows $x$ still reachable (`prev` = $(x, 0)$ at L3 or L9, or `cur.next` = `(x, cmark)` at L7 with `cur` protected and reachable). Then $x$ is not freed from $t_1$ until the process changes that hazard pointer.

*Proof.* A node is retired only after it is unlinked (L13 and L22 retire `cur` after the CAS that removed it), and an unlinked node never becomes reachable again (a new link at L18 points only to a new node, and the unlink CAS steps point past `cur` to its frozen successor). At $t_2$, $x$ was reachable, so it was not yet retired, so any scan that frees $x$ starts its reads of the hazard pointers (R3) after $t_2 > t_1$. Such a scan reads the hazard pointer that holds $x$ and keeps $x$. ∎

For L7 we also need `cur` to be reachable at the second read; that is given by L9 of the same iteration, which reads `prev` = `(cur, 0)` after L7, and by the fact that a node that is not reachable at a time is not reachable at any earlier time after it was first unlinked. If L9 fails, FIND drops `next` and starts over, so it never uses `next` without the check.

**Lemma 3 (no use after free).** A process never reads or writes a freed node, and every CAS that compares against a node address compares against a node that has not been freed since the process protected it.

*Proof.* Every node that FIND reads (`cur` at L5, L7, L8) or uses as `prev` is protected by `hp1` or `hp2` and was validated as in Lemma 2. INSERT and DELETE use `prev`, `cur` and `next` just after FIND returns, while the three hazard pointers still hold them. So by Lemma 2 none of them is freed, and an address in an expected value of a CAS still names the same node. ∎

Lemma 3 is what rules out the [ABA problem](/aba-problem/): a CAS at L13, L18 or L22 that expects `(cur, 0)` cannot succeed against a different node at the same address, because `cur` has not been freed.

**Lemma 4 (the list invariants).** In each bucket, (a) a marked `next` field never changes; (b) only marked nodes are unlinked; (c) the reachable keys strictly increase.

*Proof.* As for the Harris list. (a) Every CAS on a `next` field expects an unmarked value. (b) L13 unlinks `cur` after it read `cur.next` marked; L22 unlinks `cur` after its own mark at L21. Each of them unlinks exactly one node, the one between `prev` and `next`, because `next` is the frozen successor of the marked `cur`. (c) L18 links $k$ between `prev`'s node, with key $< k$ (or the bucket head), and `cur`, with key $> k$ (or null), and only if `prev` still points, unmarked, to `cur`. By Lemma 3 these are the same nodes that FIND saw. ∎

**Theorem 1 (linearizability).** Every history of the table is linearizable with respect to the sequential set.

*Proof sketch.* By Lemma 1, the operations on bucket $i$ form a history of one list, and the set of the table is the disjoint union of the sets of the lists. Linearizability is local (Herlihy and Wing 1990): a history is linearizable if its restriction to each object is. For one list, choose the points of the page: a successful insert at L18; a successful delete at L21; an operation that finds $k$ at the L5 read that returned `cur.next` unmarked, when `cur`, with key $k$, is reachable (confirmed by L9 after L5, and `cur` cannot become reachable again once unlinked, so it was reachable at L5) and unmarked; an operation that does not find $k$ at the last L9 (or L3 when the list is empty), when `prev` holds `(cur, 0)` with the node of `prev` reachable and unmarked, and `cur.key` $> k$ or `cur` = null, so by Lemma 4(c) no reachable node has key $k$. At each point the abstract set agrees with the result, and the set changes only at the points of successful inserts and deletes. ∎

**Theorem 2 (progress).** The table is lock-free. Alone, an operation on a bucket of $b$ nodes takes at most $7b + 3 + 3p + R$ steps.

*Proof sketch.* A FIND goes back to L1 only when a word it reads again has changed (L3, L7, L9) or when its CAS at L13 fails. Each of these means that some other process did a successful CAS on a `next` field or a bucket word in the meantime: a link, a mark or an unlink. INSERT and DELETE retry only after such a CAS of another process, too. Each operation does at most one link or one mark, and the number of unlinks is at most the number of marks. So in an infinite run where only finitely many operations complete, there are only finitely many successful CAS steps, and after the last one every FIND runs without restarts and ends after a finite walk. The scan is a loop of $3p$ reads and at most $R$ frees, so it always ends. The solo bound comes from counting the steps of the pseudocode, as on the page. ∎

**Theorem 3 (bounded garbage).** Each process has at most $3p + R - 1$ retired nodes that are not freed, except during a scan, when it may have one more.

*Proof.* After a scan, the nodes kept are in the set $H$ of hazard pointer values that the scan read, so there are at most $3p$ of them. After that, a process adds at most $R - 1$ nodes without scanning; the next one starts a scan. ∎
