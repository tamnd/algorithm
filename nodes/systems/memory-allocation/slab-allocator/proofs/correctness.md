---
title: A slab cache hands out only free built objects, grows only when every slab is full, and reaps exactly the wholly free slabs
proves: [correctness, termination]
status: full
---

**Setting.** A cache has object size $s$ and page size $P \ge s$, so a slab holds $p = \lfloor P / s \rfloor \ge 1$ objects. A slab made at page base $B$ with color $c$ has the objects $B + c + j s$ for $0 \le j < p$; line L11 picks $c$ with $c + p s \le P$, so all objects lie in the page and do not overlap. Let $\mathcal{S}$ be the set of slabs of the cache. For a slab $S$, let $F(S)$ be its free list and $U(S)$ the set of its objects that the program holds. The program frees only objects that it holds.

**Invariant (I).** For every slab $S \in \mathcal{S}$:

1. $F(S)$ has no repeat, $F(S)$ and $U(S)$ are disjoint, and $F(S) \cup U(S)$ is the set of all $p$ objects of $S$;
2. the count of $S$ equals $|U(S)|$;
3. $S$ is in exactly one group: full if the count is $p$, wholly free if it is 0, and partial otherwise;
4. the constructor has run exactly once on each object of $S$, and the destructor has not run on it;

and no object outside the slabs of $\mathcal{S}$ is held by the program.

**Lemma 1 (grow).** If (I) holds and CACHE-GROW gets a page, then (I) holds after it, with one more slab in the wholly free group.

*Proof.* The page was not in use, so the new slab overlaps no other slab. Line L12 runs the constructor once on each of its $p$ objects and puts all of them on the free list. So $F = $ all objects, $U = \emptyset$, the count is 0, and the slab is in the wholly free group. The other slabs do not change. $\square$

**Lemma 2 (alloc).** If (I) holds before SLAB-ALLOC, then (I) holds after it. A returned object was not held by the program, and the constructor has run on it. CACHE-GROW runs only when no slab of the cache has a free object.

*Proof.* By (I.1) to (I.3), a slab has a free object exactly when its count is less than $p$, that is, when it is partial or wholly free. Lines L1 and L2 look for such a slab, and line L3 runs only when there is none. If CACHE-GROW runs and gets a page, Lemma 1 gives a slab with $p \ge 1$ free objects. Line L4 pops an object $o$ from $F(S)$; by (I.1) it is not in $U(S)$, and by (I.4) it is built. The object moves from $F(S)$ to $U(S)$, and the count grows by 1, so (I.1) and (I.2) hold. Line L5 puts $S$ in the group of its new count, so (I.3) holds. No constructor or destructor runs, except in CACHE-GROW, so (I.4) holds. If no page is left, the call returns FAIL and nothing changes. $\square$

**Lemma 3 (free).** If (I) holds and the program frees an object $o$ that it holds, then (I) holds after SLAB-FREE$(o)$, and $o$ is still built.

*Proof.* By the last part of (I), $o$ belongs to a slab $S \in \mathcal{S}$, and line L7 finds it, because the objects of $S$ lie in its page. By (I.1), $o \in U(S)$ and $o \notin F(S)$, so after line L8, $F(S)$ has no repeat, and the two sets still cover all objects of $S$. The count drops by 1, and line L9 puts $S$ in its group. No destructor runs, so $o$ stays built. $\square$

**Lemma 4 (reap).** If (I) holds, CACHE-REAP gives back exactly the slabs whose count is 0, and (I) holds after it.

*Proof.* By (I.3), the wholly free group holds exactly the slabs with count 0, and by (I.2) these are the slabs with $U(S) = \emptyset$. Line L13 runs the destructor once on each of their objects and removes them from $\mathcal{S}$. No held object was in them, so the last part of (I) holds. The other slabs do not change. $\square$

**Theorem.** Starting from a cache with no slab, for any sequence of calls in which the program frees only objects that it holds:

1. SLAB-ALLOC never returns an object that the program holds, and every object it returns is built;
2. a new slab is made only when every slab of the cache is full, so a freed object is reused before the cache takes a new page;
3. the constructor runs exactly $p$ times per slab made, and the destructor exactly $p$ times per slab reaped;
4. CACHE-REAP gives back a slab exactly when none of its objects is held;
5. each call ends: SLAB-ALLOC and SLAB-FREE do a constant number of list operations plus at most one CACHE-GROW, which runs $p$ constructors, and CACHE-REAP runs $p$ destructors per slab it gives back.

*Proof.* (I) holds at the start, with $\mathcal{S}$ empty. By Lemmas 2, 3 and 4 and induction on the number of calls, (I) holds before each call. Then (1) and (2) are Lemma 2, (3) follows from (I.4) and Lemmas 1 and 4, (4) is Lemma 4, and (5) follows from the lines, none of which loops more than $p$ times. $\blacksquare$
