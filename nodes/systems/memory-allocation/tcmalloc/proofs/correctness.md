---
title: The tcmalloc model keeps every object in one place and the page heap consistent
proves: [correctness]
status: full
---

We prove the claims for the model of the page: MALLOC (L1 to L6), FREE (L7 to L10), SCAVENGE (L11), CENTRAL-INSERT (L12) and the page heap (L13, L14). The heap is the page range $[0, N)$.

**Invariant P (page heap).** (P1) The spans tile $[0, N)$: they are disjoint runs of pages whose union is $[0, N)$. (P2) The pagemap maps every page to the span that contains it. (P3) No two free spans are adjacent. (P4) The set of free spans is exactly the set of spans marked free.

**Invariant O (objects).** For each span $s$ of a small class $c$, with $C = \mathit{PAGE}/c$ objects: (O1) each object of $s$ is in exactly one of three places: the free list of $s$, the list of class $c$ of one thread cache, or held by the program; (O2) $s.\mathit{refcount}$ is the number of objects of $s$ in the last two places, and it is at least 1; (O3) $s$ is in central$[c]$ exactly when its free list is not empty.

**Invariant C (caches).** Every list $L$ has $L.\mathit{max} \ge 1$ and $L.\mathit{low} \le \mathrm{length}(L)$, and the recorded size of each cache is the sum of the sizes of its objects.

The model does not keep $\mathrm{length}(L) \le L.\mathit{max}$, and neither does tcmalloc. $L.\mathit{max}$ is a target, not a bound. When L9 lowers it by $b(c)$ after a release of $b(c)$ objects, the length can be $L.\mathit{max} + 1$. When L11 lowers it, the length can stay above it. The next free that finds the list too long releases a batch.

All three hold for the empty heap.

**Lemma 1 (page heap).** PAGEHEAP-ALLOC and PAGEHEAP-FREE keep P, and ALLOC returns a span of at least $k$ pages that was free.

*Proof.* ALLOC (L13) either finds a free span of at least $k$ pages, or first appends a free span of $\max(k, 16)$ pages at the end of the heap, maps its pages, and merges it with a free span before it, which keeps (P1) to (P4) and gives a span that fits. It then splits off the last pages of the chosen span as a new free span, mapped page by page, and marks the first $k$ pages used. The free remainder is adjacent to the used part and to the old neighbor after the chosen span, which was not free by (P3). FREE (L14) marks $s$ free and merges it with the span before it if that span is free, which it finds through the pagemap entry of page $s.\mathit{start} - 1$, and then with the span after it. After the merges both neighbors of the result are used or absent, so (P3) holds; the merged pages are remapped, so (P2) holds. $\square$

**Lemma 2 (central lists).** CENTRAL-REMOVE and CENTRAL-INSERT keep O.

*Proof.* A new span from L4 has all $C$ objects on its free list and refcount 0. Each object taken moves from the free list of its span to the caller, which puts it in a cache list or returns it to the program, and adds 1 to the refcount; a span whose list becomes empty leaves central$[c]$. At L12, each object comes from a cache list and goes to the free list of the span that the pagemap gives for its page, which by (P2) is its own span; the refcount drops by 1, and a span that had an empty list joins central$[c]$. When the refcount reaches 0, no object of the span is in a cache or in the program, by (O2), so the span can go to the page heap; it leaves central$[c]$ first. $\square$

**Lemma 3 (thread caches).** MALLOC, FREE and SCAVENGE keep C and O.

*Proof.* L3 moves an object from a cache list to the program, and lowers $L.\mathit{low}$ if needed. L4 runs only when $L$ is empty and takes $k = \min(L.\mathit{max}, b(c)) \ge 1$ objects; L6 returns one and pushes the other $k - 1$. L5 only raises $L.\mathit{max}$. L8 moves an object from the program to a cache list; if the list is then longer than $L.\mathit{max}$, L9 moves $\min(\mathrm{length}(L), b(c)) \ge 1$ objects to central. The maximum then grows by 1, or stays, or after more than three overflows drops by $b(c)$. The value of $L.\mathit{max}$ is always in $\{1, \dots, b(c)\}$ or a multiple of $b(c)$: slow start adds 1 up to $b(c)$, L5 rounds down to a multiple of $b(c)$, and L9 and L11 subtract $b(c)$ or set $b(c)$. A drop in L9 happens only when $L.\mathit{max} > b(c)$, so then $L.\mathit{max} \ge 2b(c)$ and it stays at least $b(c)$. L11 moves $\max(1, \lfloor L.\mathit{low}/2 \rfloor) \le L.\mathit{low} \le \mathrm{length}(L)$ objects, only when $L.\mathit{low} > 0$, and lowers the maximum to no less than $b(c) \ge 2$. Each removal from a list lowers $L.\mathit{low}$ to the new length if needed, and L11 sets it to the length. Every move between a cache and central is a move between two of the three places of (O1), done by Lemma 2 on the central side, and the cache size changes by $c$ per object. $\square$

**Theorem.** In every sequence of calls on the model, invariants P, O and C hold after each call. Hence no object is handed to the program twice while it is held, a span returns to the page heap only when none of its objects is held or cached, and every address that the program frees is mapped to the span and class it came from.

*Proof.* Induction on the calls, by Lemmas 1 to 3. A small object returned by MALLOC came from a cache list or a span free list, so by (O1) the program did not hold it. A large object is a whole span taken by Lemma 1 from the free spans, so it is disjoint from every other span. $\square$

The tests of the model check P, O and C after every call on random traces with several threads, large and small sizes and small cache limits, and check that after all objects are freed and all caches are drained the page heap is one free span. $\blacksquare$
