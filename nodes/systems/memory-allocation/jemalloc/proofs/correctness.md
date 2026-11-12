---
title: The jemalloc model gives out disjoint objects and frees them into the right run
proves: [correctness]
status: full
---

We prove the claims for the model of the page: MALLOC (L1 to L7), FREE (L8 to L13), BUDDY-ALLOC (L14) and BUDDY-FREE (L15). A chunk has $P = 2^9$ pages of 4 KiB and starts at a multiple of the chunk size. For a run $r$ we write $r.\mathit{used}$ for the number of set bits of its bitmap and $r.n$ for its number of regions.

**Invariant B (buddy blocks).** For each chunk $k$ owned by arena $a$: (B1) the runs in $k$ and the free blocks of $a$ in $k$ are disjoint and their union is the $P$ pages of $k$; (B2) a block or run of order $o$ starts at a page that is a multiple of $2^o$; (B3) if $(k, q)$ is a free block of order $o$, then $(k, q \oplus 2^o)$ is not a free block of order $o$; (B4) the page map of $k$ maps each page of a run to that run and each free page to nothing; (B5) no free block is a whole chunk.

**Invariant R (runs).** For each small run $r$ of class $c$ in arena $a$: (R1) the header and the $r.n$ regions fit in the run; (R2) bit $i$ is set exactly when the program holds the object at $r.\mathit{start} + r.\mathit{header} + i c$; (R3) $r$ is in exactly one of three states: current for $(a, c)$; non-full, with $0 < r.\mathit{used} < r.n$, not current and out of QINIT; or full and not current; (R4) if $r.\mathit{used} = 0$ then $r$ is current and in QINIT.

**Invariant H (huge).** The huge tree maps bases $k$ to sizes $s$; the ranges $[k, k + s)$ are disjoint, are made of whole chunks, and contain no chunk that an arena owns.

All three hold at the start, when nothing is mapped.

**Lemma 1 (buddy).** BUDDY-ALLOC and BUDDY-FREE keep B, and BUDDY-ALLOC returns a run of $2^j \ge k$ pages that was free.

*Proof.* L14 takes a free block of order $o \ge j$, or maps a new chunk, which is one free block of order 9 and keeps (B1) to (B4). Splitting a block of order $o$ at a multiple of $2^o$ gives two halves at multiples of $2^{o-1}$, which are buddies of each other. The upper half becomes free, and the lower half is split again or becomes the run, so (B1) and (B2) hold. The new free half has as buddy the lower half, which is in use, so (B3) holds for it. Each smaller free block put back in the loop has the same property. The page map is set for the pages of the run, so (B4) holds, and (B5) holds since the whole block of order 9 was split or $j = 9$, which does not happen because large classes are at most half a chunk. L15 frees a run of order $o$, clears its pages in the page map and merges it with its buddy while the buddy is free at the same order. The merged block starts at the smaller of the two starts, which is a multiple of $2^{o+1}$, so (B2) holds. The loop stops when the buddy is not free at this order, so (B3) holds for the result; no other free block changed. If the result is the whole chunk, the chunk leaves the arena, which gives (B5). $\square$

**Lemma 2 (small malloc).** L5 to L7 keep R and return an object that the program does not hold, inside one run, aligned to $\min(c, 16)$.

*Proof.* L5 keeps the current run if it is not full. Otherwise the old current run is full and becomes "full and not current", and a new run is taken from the non-full runs, which leaves that state, or from BUDDY-ALLOC, with an empty bitmap and in QINIT. Either way the new current run has a 0 bit, so L6 finds the lowest one, $i < r.n$. By (R2) region $i$ is not held, and setting the bit keeps (R2). After L6, $r.\mathit{used} > 0$, and $r$ leaves QINIT once a quarter of its regions are in use. The header size is a multiple of 16 and every class below 16 is a power of two, so the address at L7 is aligned. By (R1) the region lies inside the run. $\square$

**Lemma 3 (small free).** If the program frees an object $p$ that it holds and that MALLOC gave out in a small run, then L8 to L13 find that run and keep R.

*Proof.* The run lies in one chunk, which starts at a multiple of the chunk size, so L8 finds it; by H the chunk is not in the huge tree. By (B4) the page map gives the run, and the run's arena is the one that owns the chunk. L12 computes the region index, and by (R2) its bit is set, so clearing it keeps (R2). If the run is now empty and out of QINIT, L13 removes it from its state and frees it, which by Lemma 1 keeps B; no region of it is held, so (R2) holds for nothing. If the run was full and is not current, it becomes non-full: its count is $r.n - 1 > 0$ and it is out of QINIT, since it was full. In all other cases the state does not change, and the conditions of (R3) and (R4) still hold: a non-full run that does not become empty stays non-full, and a run in QINIT is current by (R4) applied before the call, or because only a current run can be in QINIT. That last fact holds because a run leaves the current state only when it is full, at L5, and a full run is out of QINIT. $\square$

**Lemma 4 (large and huge).** L2, L4, L9 and L11 keep B and H.

*Proof.* A large object is a run of its own from Lemma 1, and L11 finds it by (B4) and frees it with Lemma 1. A huge object gets new chunks that no arena owns and no huge entry uses, so H holds. L9 finds the base in the tree and gives the chunks back. $\square$

**Theorem.** In every sequence of calls on the model where the program frees only objects it holds, B, R and H hold after each call. So no two live objects overlap, each live object lies inside the chunk, run or huge range that its address gives, and every free reaches the arena that gave the object out.

*Proof.* Induction on the calls, by Lemmas 1 to 4. Live small objects are distinct regions of runs (R2), runs are disjoint page ranges (B1), large objects are whole runs, and huge objects are whole chunks outside all arenas (H), so no two live objects overlap. $\square$

The tests of the model check B, R and H and the disjointness of live objects on random traces with several threads, all three groups of size classes and one, two or four processors. They also check that each small malloc returns the lowest free region of the current run of the caller's arena, and that after all objects are freed only empty runs in QINIT remain. $\blacksquare$
