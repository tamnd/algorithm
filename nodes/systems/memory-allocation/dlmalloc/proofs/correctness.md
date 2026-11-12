---
title: The dlmalloc model keeps its heap invariants and returns disjoint blocks
proves: [correctness]
status: full
---

We prove the claims for the model of the page: MALLOC on lines L1 to L11 and FREE on lines L12 to L18. The arena is the address range $[0, T)$, where $T$ is the end of top. A chunk is a pair (address, size). We call a chunk *binned* if it lies in a small bin or a tree bin.

**Invariant.** Between calls, all of the following hold.

- (I1) *Tiling.* Starting at address 0 and adding sizes from the heads reaches top, and top ends at $T$. Every chunk other than top has a size that is a multiple of 8 and at least 16.
- (I2) *Boundary tags.* For each chunk $c$ after the first, PINUSE$(c)$ equals CINUSE of the chunk just before $c$. Every free chunk other than top has a footer equal to its size, stored at its end.
- (I3) *No adjacent free chunks.* No two free chunks are next to each other. In particular the chunk before top is in use.
- (I4) *Bins.* Every free chunk other than top and dv is binned exactly once, in the bin for its size. dv and top are not binned. Every binned chunk is free.
- (I5) *Live set.* The chunks in use in the arena, together with the mapped chunks, are exactly the blocks returned by MALLOC and not yet freed.

All five hold for the empty arena, where top has size 0 and there are no other chunks.

**Lemma 1 (split).** Let $c = (a, s)$ be a free chunk that is not binned, with $s \ge nb$, $nb \ge 16$ and $nb$ a multiple of 8. The split marks $[a, a + nb)$ in use, or all of $c$ if $s - nb < 16$, and marks the rest $(a + nb, s - nb)$ free with a footer. After it, (I1) and (I2) hold, and the only new free chunk is the rest.

*Proof.* Both parts have sizes that are multiples of 8, and the rest has at least 16 bytes when it exists, so (I1) holds. The split writes the head of the used part, the head and footer of the rest, sets PINUSE of the rest to 1, and sets PINUSE of the chunk after $c$ to the state of the last part. The chunk before $c$ is unchanged, and PINUSE$(a)$ keeps its value. So (I2) holds. $\square$

**Lemma 2 (MALLOC).** If the invariant holds before MALLOC$(r)$, it holds after, and the returned chunk has at least $nb \ge r + 4$ bytes and was free before the call.

*Proof.* $nb$ from line L1 is at least $r + 4$. Each way out of MALLOC takes a free chunk that is not binned at the moment of the split (a binned chunk is first removed from its bin), and splits it by Lemma 1. So the returned chunk was free, has at least $nb$ bytes, and is disjoint from all chunks in use, which gives (I5). It remains to check (I3) and (I4).

*Line L3.* A chunk of size $nb$ or $nb + 8$ is removed from its bin and used whole (a rest of 8 bytes is below 16). No free chunk is created. A free chunk became used, so no two free chunks become adjacent.

*Line L5.* A binned chunk is removed and split. Its rest is free. The chunk after the rest is the old successor of the chunk, which was not free by (I3), so the rest has no free successor; its predecessor is the used part. The old dv, which is free and not binned, is put into its bin, and the rest becomes dv. So (I3) and (I4) hold.

*Line L7.* As in L5, but the rest goes into its bin and dv does not change.

*Line L8.* dv is split. Its rest, if any, is the new dv and stays unbinned. If there is no rest, dv becomes empty.

*Line L9.* top is split. The used part lies just before the new top, so the chunk before top is in use, which (I3) needs. The new top is not binned.

*Line L10.* A new mapping is outside the arena. Nothing in the arena changes.

*Line L11.* Top grows at its end. The chunk before top does not change. Then the loop returns to line L9, which succeeds because top now has more than $nb$ bytes. $\square$

**Lemma 3 (FREE).** If the invariant holds before FREE$(p)$ for a block $p$ that is live, it holds after.

*Proof.* If $p$ is mapped (line L12), only the mapping is removed. Otherwise $p$ is a chunk in use in the arena. We show that the chunk built by lines L13 to L16 is a maximal run of free memory, and that it is put in exactly one place.

*Backward (line L13).* By (I2), PINUSE$(p) = 0$ exactly when the chunk $q$ before $p$ is free, and then the footer just before $p$ gives the size of $q$, so $q$ is found. By (I3), the chunk before $q$ is in use. If $q$ is binned it is removed from its bin; if $q$ is dv it is not binned, by (I4), and stays dv. The merged chunk starts at $q$.

*Forward.* Let $n$ be the chunk after the merged chunk. There are three cases. If $n$ is top (line L14), the merged chunk joins top. If it was dv, dv is cleared, so that dv is not inside top. Now the chunk before top is the chunk before the merged chunk, which is in use by (I3) or by PINUSE. If $n$ is dv (line L15), the merged chunk joins dv; it cannot also start with dv, because two free chunks are never adjacent. If $n$ is another free chunk (line L16), it is binned by (I4), so it is removed from its bin and joined. In every case the chunk after the merged chunk is now in use, because by (I3) the chunk after a free chunk is in use.

*Placement (lines L17 and L18).* The new footer and the PINUSE bit of the next chunk are written, so (I2) holds. If the merged chunk starts at dv, it is dv with a new size and is not binned (line L17). Otherwise it is put into the bin of its size (line L18). Every chunk that was joined has been removed from its bin, so (I4) holds. Both neighbors of the merged chunk are in use, so (I3) holds. The freed block is no longer in use, which gives (I5). $\square$

**Theorem.** In every sequence of MALLOC and FREE calls on the model, each call keeps (I1) to (I5). Hence the blocks that are live at any moment are pairwise disjoint, each has at least as many bytes as was asked plus the head word, and no block is returned twice while it is live.

*Proof.* Induction on the number of calls, with Lemmas 2 and 3. Disjointness follows from (I1) and (I5): the chunks tile the arena, and each mapping is a separate range. $\square$

**Choice rules.** Two properties of the policy follow from the order of the lines. (a) For a small request, if a chunk of size $nb$ or $nb + 8$ is binned, line L3 returns one of them. (b) If a large request is served from a tree bin (line L7), it gets a binned chunk of the smallest size at least $nb$, because the search scans the tree bins from the bin of $nb$ upward and, inside a bin, by increasing size, and every larger tree bin holds only larger sizes. The same scan gives the smallest binned chunk at line L5. These are the two rules that the randomized tests check after every call, together with (I1) to (I5). $\blacksquare$
