---
title: Each compare-and-swap keeps the Bw-tree a correct B-link structure, so its operations are linearizable
proves: [correctness]
status: full
---

We use the notation of the page and the code. The mapping table $M$ maps a pid to the head of a chain. The *page* of a pid is its chain read at one instant. Its bounds $(low, high, right)$ are those of the newest split delta in the chain, or of the base page if there is none, and its *content* is `logical(h)`: the base, with the deltas applied from the oldest to the newest, restricted to $[low, high)$. A page is *reachable* if a walk from the root along child pointers and right links reaches it.

The only writes to shared state are CAS operations on single slots of $M$, and the setup of a new pid before it is reachable. A CAS $(pid, h, n)$ succeeds only if $M[pid]$ is still $h$, so the new head $n$ is computed from the page as it is at the instant of the CAS. We show that the following invariant holds after every successful CAS. Since it holds for the initial tree (one empty leaf root with the range $(-\infty, \infty)$), it holds at every instant.

**Invariant.**

- (B1) The reachable pages of each level, read from the page with $low = -\infty$ along the right links, have the ranges $[low, high)$ of a partition of $(-\infty, \infty)$, in increasing order. The root is the only page of the top level.
- (B2) For an inner page at level $\ell + 1$ and a key $k$ in its range, `inner_route` returns a pid of a page at level $\ell$ whose $low$ is at most $k$.
- (B3) The key set of the tree is the union of the contents of the reachable leaves, and each key is in the content of the leaf whose range holds it.
- (B4) The $low$ of a page never changes after it is reachable, and its $high$ never increases.

**Lemma 1 (find).** If the invariant holds at each instant, `_find(k, level)` returns a pid and a head $h$ such that, at the instant $h$ was read, $h$ was the head of a reachable page at that level whose range held $k$.

*Proof.* The walk starts at the root, whose range is $(-\infty, \infty)$. At any page it reads, it holds the property "the page is reachable, at the current level, and $low \le k$". This holds at the root. If $k \ge high$, the walk moves to $right$, whose $low$ is $high \le k$ by (B1), at the same level, and reachable. If $low \le k < high$ and the level is the wanted one, the walk returns it. If it is higher, by (B2) the child has $low \le k$ and is one level down. By (B4), the property "low ≤ k" stays true after the read. By (B1), the pages to the right of a page with $low \le k$ include the page whose range holds $k$, and in a finite run there are finitely many pages, so the walk ends. $\square$

**Lemma 2 (each CAS keeps the invariant).**

*Insert, update or delete delta (L5).* The CAS puts a delta in front of the head $h$ of a leaf whose range holds $k$ (Lemma 1, and the CAS validates that the page has not changed since). It changes only the state of $k$ in the content, and no bounds, so (B1), (B2) and (B4) are kept, and (B3) holds with $k$ added or removed.

*Consolidation (L15).* The new base page is `logical(h)`: the same bounds and the same content. The CAS validates $h$, so nothing changes logically.

*Split (L16 and L17).* The new page $Q$ gets the keys of the content of $h$ that are $\ge sep$, the range $[sep, high)$ and the right link of $h$, and it is not reachable before the CAS. The CAS puts a split delta $(sep, Q)$ on $h$, which sets the range of $P$ to $[low, sep)$ and its right link to $Q$. Because the CAS validates $h$, the content of $Q$ is exactly the part of the content of $P$ in $[sep, high)$ at that instant. So the level now has $[low, sep)$, $[sep, high)$ and then the old right neighbour, which is (B1). The contents together are unchanged, so (B3) holds. $P$ keeps its $low$ and its $high$ falls, which is (B4). The new page is not the root, and the root never gets a split delta (it splits by a root split), so the top level still has one page.

*Index term (L20).* The delta adds the entry $(sep \to Q)$ to a parent at level $\ell + 1$, with $Q$ at level $\ell$ (the level check of L19) and $Q.low = sep$. `inner_route` returns $Q$ only for $sep \le k$, so (B2) holds. No bounds or contents change.

*Root split.* The CAS replaces the root head $h$ by a new base page one level up, with the two entries $(-\infty \to L)$ and $(sep \to R)$. $L$ and $R$ were built from the content of $h$, with the ranges $[-\infty, sep)$ and $[sep, \infty)$ and the link $L \to R$, and they were not reachable before. The CAS validates $h$, so their contents are exactly that of the old root. The old top level becomes the level of $L$ and $R$, which is (B1). (B2) holds for the new root, and the pages below are unchanged. $\square$

**Theorem (linearizability).** Every operation of the code is linearizable with respect to a map from keys to values.

*Proof.* Take as the linearization point of an update its successful CAS at L5; of a delete of an absent key, the read of the leaf head that `_find` returns; and of a lookup, the same read. By Lemma 1, at that instant the head is that of the reachable leaf whose range holds $k$, and by (B3) the state of $k$ in its content is the state of $k$ in the map. The result of the operation (the old value, or the value found) is computed from that head, so it is the value of $k$ at the linearization point. Each linearization point lies between the start and the end of its operation. The changes of structure (consolidation, split, index term, root split) do not change the map, by Lemma 2. $\square$

**Lock-freedom.** A CAS fails only because another CAS on the same pid has succeeded in the meantime. So while some operation retries, others make progress. A single operation can retry without bound, so the structure is lock-free, not wait-free.

**Help along.** The correctness above does not need the index term of a split to be posted: a search that reaches $P$ for a key $\ge sep$ follows the right link (Lemma 1). Posting it, by the thread that made the split or by any thread that took the side link, only makes later searches shorter.

The tests compare sequential runs with a Python dict, check that every concurrent run of three threads with four operations each on shared keys has a linear order that respects real time and matches a dict (by a search over all orders), check concurrent writers with disjoint keys and readers of fixed keys, and stop a split after its split delta to show that a later reader posts the index term.
