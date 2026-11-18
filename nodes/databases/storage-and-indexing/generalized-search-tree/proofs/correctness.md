---
title: A GiST search returns every matching record, and insert and delete keep the tree properties
proves: [correctness]
status: full
---

We use the notation of the page. A key is a predicate on the key domain. For a key $p$ and a record key $k$, "$p$ covers $k$" means that $p$ holds for $k$. The extension must satisfy these contracts, which are the contracts of the paper:

- (C1) If $p$ covers some $k$ that satisfies the query $q$, then Consistent$(p, q)$ is true.
- (C2) Union$(P)$ covers every record key that some key of $P$ covers.
- (C3) Compress$(p)$ covers every record key that $p$ covers, and Decompress$(p)$ covers every record key that $p$ covers.
- (C4) PickSplit on $M + 1$ entries returns two sets of at least $m$ entries each.

The interval and rectangle extensions of the code satisfy these: Consistent is the exact overlap or intersection test, so (C1) holds; Union is the smallest covering interval or box; Compress is the identity, or rounds a box outward, which only makes it larger; the sorted halves have $\lfloor (M+1)/2 \rfloor \ge m$ entries, and the quadratic split gives the rest of the entries to a group as soon as that group needs them to reach $m$.

**Invariant.** (P1) Every node other than the root has between $m$ and $M$ entries; an inner root has at least two. (P2) Every leaf entry $(p, rid)$ has a key $p$ that covers the key of record $rid$. (P3) Every index entry $(p, ptr)$ has $p = $ Compress(Union(the decompressed keys of $ptr$)). (P4) All leaves are at the same depth.

**Lemma 1 (cover).** If (P2) and (P3) hold, then every key on the path from the root to the leaf entry of a record $r$ covers the key of $r$.

*Proof.* By induction from the leaf up. The leaf entry covers $r$ by (P2). If an entry of node $v$ covers $r$, then the key of $v$ in its parent is Compress(Union(...)) of a set that includes that entry, so it covers $r$ by (C2) and (C3). $\square$

**Claim 1 (search).** If the invariant holds, SEARCH$(root, q)$ outputs every record whose key satisfies $q$, and with an exact extension it outputs no other record. The recheck in `search` makes the result exact for a lossy extension.

*Proof.* Let $r$ satisfy $q$. By Lemma 1 every key on the path to $r$ covers the key of $r$, which satisfies $q$, so by (C1) Consistent is true on the decompressed key at every step of the path. So L3 descends along the path and L5 outputs $r$. If Compress and Decompress are the identity, the leaf key is the exact key of $r$, and Consistent is the exact test, so L5 outputs only matches. If they are lossy, L5 may output extra records, and the recheck removes exactly the records whose stored key does not satisfy $q$. $\square$

**Claim 2 (insert).** INSERT keeps the invariant.

*Proof.* CHOOSE-SUBTREE descends to a leaf, and L7 adds a leaf entry with Compress(key), which covers the key by (C3), so (P2) holds. If the leaf has $M + 1$ entries, L13 and L14 split it into two nodes with at least $m$ and at most $M + 1 - m \le M$ entries each, by (C4), which gives (P1) for both. Both are at the depth of the old leaf, so (P4) holds. L15 and L16 set the parent keys of both nodes to Compress(Union(...)) of their entries, which is (P3). The parent now has one more entry, and the same argument applies to it if it overflows. The walk upward (L9) recomputes the key of every node on the path, so (P3) holds for every entry whose subtree changed, and the other entries are unchanged. If the root splits, the new root has the two halves as entries, with keys as in (P3); every leaf is now one level deeper, so (P4) still holds. $\square$

**Claim 3 (delete).** DELETE keeps the invariant and removes exactly the record $rid$.

*Proof.* By Lemma 1 and (C1), the search for the leaf at L17 with the exact key of $rid$ reaches the leaf entry of $rid$, because Consistent$(p, k)$ is true when $p$ covers $k$. Removing the entry keeps (P2) for the others. Walking up, a node with fewer than $m$ entries is removed from its parent, and the records in its subtree are kept; a node that stays has its key recomputed (L19), which keeps (P3). Removing whole subtrees does not change the depth of any leaf that stays, so (P4) holds. If the root is an inner node with one entry, its child becomes the root, and every leaf depth drops by one. Every kept record is inserted again by INSERT, which keeps the invariant by Claim 2, and so every record other than $rid$ is in the tree at the end. $\square$

**Termination.** CHOOSE-SUBTREE and SEARCH go down one level per call, and the height is finite. The walk upward in INSERT and DELETE goes up one level per step. Each reinsertion in DELETE is an INSERT, which does not reinsert anything, so DELETE ends.

The tests check the invariant with `check` (the fill bounds, the leaf depths, (P2), (P3) and the cover of Lemma 1) during random inserts and deletes, and compare every search with a scan of all records for both extensions, with exact and with lossy keys.
