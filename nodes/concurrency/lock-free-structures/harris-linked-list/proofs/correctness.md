---
title: The Harris list is a linearizable lock-free set
proves: [correctness, linearizability, progress]
status: sketch
---

We use the pseudocode of the page and its model: asynchronous processes that may crash, atomic read, write and single-word CAS on marked pointers, sequential consistency, and nodes that are never freed. This is a proof sketch in the style of Harris's paper: the invariants are proved in full, and the linearization argument is given for each kind of operation, with some routine cases only outlined. The tests check the claims on all interleavings of small cases.

A node is *linked* after the CAS at L13 that puts it into the list. It is *reachable* if there is a path of `next` pointers from `head` to it. It is *marked* if the mark bit of its own `next` field is set.

**Lemma 1 (marks are final).** Once a node is marked, its `next` field never changes again.

*Proof.* The steps that write a `next` field are the CAS steps at L8, L13, L17 and L18, and the write of a new node's `next` at L12 before the node is linked. L8, L13 and L18 expect an unmarked value, so they fail on a marked field. L17 expects the unmarked `rNext`, so it also fails on a marked field. ∎

**Lemma 2 (only marked nodes leave).** A linked node that is not marked is reachable.

*Proof.* A node stops being reachable only by a successful CAS that changes some `left.next` from a pointer $a$ to a pointer $b$ and so cuts out the nodes from $a$ up to (not including) $b$. At L18 the cut node is `right`, which this process marked at L17. At L8 the cut nodes are the ones the search passed between `left` and `right`; for each of them the search read a marked `next`, and by Lemma 1 the chain from `leftNext` to `right` is still the same chain of marked nodes when the CAS succeeds, because the CAS checks that `left.next` is still `leftNext`. At L13, nothing is cut: the new node points to `right`, which was `left.next`. ∎

**Lemma 3 (order).** The keys along the reachable path from `head` strictly increase.

*Proof.* Unlinks at L8 and L18 remove nodes from the path, which keeps the order. An insert links $n$ with key $k$ between `left` and `right`, with `left.key` $< k <$ `right.key` (the search ensured `left.key` $< k \le$ `right.key`, and L11 ruled out equality), and only if `left.next` is still `right` and `left` is unmarked, so $n$ goes between two neighbours on the path. ∎

**The abstract set.** Define $S$ at a time as the keys of the linked unmarked nodes. By Lemma 2, they are all reachable, so by Lemma 3 they are distinct.

**Lemma 4 (what the search returns).** When a search returns (`left`, `right`), there was a time $\tau$ during the search at which `left` was unmarked, `left.next` = `right`, and `left.key` $< k \le$ `right.key`; and there was a time $\tau' \ge \tau$ during the search at which `right` was unmarked (or `right` = `tail`).

*Proof.* `leftNext` was read from `left.next` with the mark clear, so `left` was unmarked at that read. In phase 2, `leftNext` = `right` and $\tau$ is that read. In phase 3, $\tau$ is the successful CAS at L8. The key bounds come from the walk: `left` was passed with key $< k$ (or is `head`), and the walk stopped at `right` with key $\ge k$. The time $\tau'$ is the read at L7 or L9 that found `right.next` unmarked. ∎

**Theorem 1 (linearizability).** Each history is linearizable with respect to the sequential set.

*Proof sketch.* Choose the points:

- insert true: the CAS at L13. Before it, $k \notin S$: at $\tau'$ of its last search, `right` (key $\ne k$) followed `left` (key $< k$) with `left` unmarked, so no linked unmarked node had key $k$ at $\tau$; a node with key $k$ linked after $\tau$ would have been linked into the same gap, which changes `left.next` and makes this CAS fail. After the CAS, $k \in S$.
- delete true: the mark at L17. Before it, the node `right` with key $k$ is linked and unmarked, so $k \in S$; after it, $k \notin S$, because the keys are distinct (Lemma 3) and the only node with key $k$ is now marked.
- insert false and find true: the time $\tau'$ of the last search, when `right` with key $k$ is unmarked and linked, so $k \in S$.
- delete false and find false: the time $\tau$ of the last search, when `left` is unmarked and points to `right`, with `left.key` $< k <$ `right.key`. `left` is reachable (Lemma 2), so the path goes from `left` straight to `right`, and by Lemma 3 no reachable node has key $k$; so no linked unmarked node has key $k$, and $k \notin S$.

Each point is a step of the operation, or a time during it, and $S$ changes only at the points of successful inserts and deletes, by exactly what the sequential set does. So ordering the operations by their points gives a legal sequential history with the same results. ∎

**Theorem 2 (the naive list is not linearizable).** If delete unlinks the node with one CAS on its predecessor and never marks it, there is a run in which a completed insert is lost.

*Proof.* The list is `head` → 1 → 3. The deleter of 1 finds left = `head`, right = 1, reads `1.next` = 3. The inserter of 2 finds left = 1, right = 3 and swings `1.next` from 3 to the new node; it returns true. The deleter swings `head.next` from 1 to 3; it returns true. Now 2 is not reachable, and a find(2) returns false, although insert(2) completed before it and no delete(2) ran. The test `test_naive_list_loses_an_insert` replays this run. ∎

**Theorem 3 (progress).** The list is lock-free: in every infinite run in which processes take infinitely many steps, infinitely many operations complete. Alone, find and insert take at most $n + 4$ steps and delete at most $n + 6$, where $n$ is the number of nodes in the list.

*Proof sketch.* A search or an operation goes back to L1, L10 or L14 only after a failed CAS, or after it saw a mark on `right.next` or on `rNext`. A failed CAS on a word means that some other CAS on that word succeeded since the read. A new mark is a successful L17. So each restart is caused by a successful CAS of another process: a link (L13), a mark (L17) or an unlink (L8, L18). Each link and each mark ends its operation within a bounded number of steps of its owner, except for the cleanup search after a failed L18, which is itself charged in the same way. The number of unlinks is at most the number of marks. So if only finitely many operations completed, only finitely many successful CAS steps would happen, and every operation would finish its walk, which takes at most the number of nodes reachable from its position, and that number is finite since no new nodes are linked. The solo bounds follow by counting: one read per node passed, plus at most one CAS and one more read in the search, and at most two CAS steps and one read in insert and delete; the tests measure them. ∎
