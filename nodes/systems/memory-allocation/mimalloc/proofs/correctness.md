---
title: mimalloc keeps each block in one place, frees only empty pages, and enters the slow path regularly
proves: [correctness]
status: full
---

We prove the claims for MALLOC (L1 to L3), FREE (L4 to L8) and GENERIC (L9 to L14) of the page. Fix a page $q$ with block set $B$ and owner thread $o$. Let $H$ be the set of blocks of $q$ that are handed out, that is, returned by MALLOC and not yet passed to FREE.

**Invariant.** At every moment:

- (I1) $B$ is the disjoint union of $H$, free, local_free and thread_free;
- (I2) thread_freed $= |$thread_free$|$;
- (I3) used $= |H| + |$thread_free$|$.

Hence used − thread_freed $= |H|$, the number of live blocks of $q$.

*Proof.* A fresh page (L14) has all of $B$ on free, and used = thread_freed = 0. We check each line that touches $q$.

- L3 moves one block from free to $H$ and adds 1 to used: (I1) and (I3) hold.
- L6 moves a block from $H$ to local_free and subtracts 1 from used: (I3) holds, since $|H|$ fell by 1.
- L8 moves a block from $H$ to thread_free and adds 1 to thread_freed. used is unchanged, and $|H| + |$thread_free$|$ is unchanged. (I2) holds.
- L11 moves local_free and all of thread_free to free and subtracts $m = |$thread_free$|$ from used and thread_freed. Both sides of (I2) become 0 less the same $m$; in (I3), $|$thread_free$|$ falls by $m$ and used by $m$.

The pushes at L8 are atomic, and the take at L11 is an atomic swap with the empty list, so each block pushed by another thread is either in the list that L11 took or in the list left behind, never in both and never lost. The atomic increment of thread_freed at L8 happens after the push. So between the two steps of one remote free, thread_freed can be one less than $|$thread_free$|$, never more. In that window, used − thread_freed is one more than $|H|$, which only delays the freeing of a page, never makes it early. $\square$

**Theorem 1 (no double handout).** MALLOC never returns a block that is handed out, and the page freed at L7 or L12 has no live block.

*Proof.* MALLOC returns a block popped from free at L3, and by (I1) free is disjoint from $H$. The page is freed only when used − thread_freed $= 0$, and by the invariant, or the window argument above, this means $|H| = 0$. Only the owner frees a page and only the owner pops at L3, so no pop can happen in a page that is being freed. $\square$

**Theorem 2 (no atomics on the owner's fast paths).** A MALLOC that ends at L3 without GENERIC, and a FREE by the owner of the segment, execute no atomic operation.

*Proof.* L1 to L3 and L4 to L7 read and write only the heap of the thread and the fields free, local_free and used of a page owned by the thread. No other thread writes these fields: other threads write only thread_free and thread_freed (L8). So plain reads and writes suffice. $\square$

**Theorem 3 (the heartbeat).** Let $C$ be the number of blocks of a page of size class $c$. Between two calls of GENERIC for class $c$ in thread $t$, thread $t$ makes at most $C$ calls of MALLOC for class $c$ that end at L3.

*Proof.* The direct page of class $c$ changes only inside GENERIC (L13, L14) or when it is freed, after which the direct entry is an empty page and the next MALLOC goes to GENERIC. While the direct page stays the same, no line except L11 adds a block to its free list: L6 and L8 push on the other two lists. So free only shrinks between two calls of GENERIC, and each fast MALLOC removes one block. A list of at most $C$ blocks allows at most $C$ pops. $\square$

Since deferred_free is called at L9 on each call of GENERIC, Theorem 3 means a thread that keeps allocating in one size class calls deferred_free at least once every $C + 1$ allocations. The tests of the model check (I1) to (I3), Theorems 1 and 2, and the bound of Theorem 3 after every call on random traces with several threads. $\blacksquare$
