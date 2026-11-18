---
title: Both forms of the heap file keep their free space structure exact, and their operations have the stated page I/O costs
proves: [correctness]
status: full
---

We use the notation of the page. The data pages are $0, \ldots, N - 1$. Each page $q$ is a slotted page with free space $free(q)$, and a record $r$ fits in $q$ when $|r| + 4 \le free(q)$. We treat the slotted page as correct (see its own page): inside one page, `insert`, `get` and `delete` behave as a map from slots to records, and a slot keeps its record until that record is deleted. Let $M$ be the abstract map from record ids to records.

## The page directory form

**Invariant D.** (a) The directory pages hold, in order, exactly one entry for each data page, in page id order. (b) Every directory page except the last has $D$ entries. (c) The entry of page $q$ is $(q, free(q))$.

By (a) and (b), the entry of page $q$ is entry $q \bmod D$ of directory page $\lfloor q / D \rfloor$, and there are $\max(1, \lceil N / D \rceil)$ directory pages.

**Lemma 1.** DIR-INSERT keeps Invariant D, returns a record id not in $M$, and adds $r$ under that id. If $q^\ast$ is the least page id with $|r| + 4 \le free(q^\ast)$, the record goes to $q^\ast$, at a cost of $\lfloor q^\ast / D \rfloor + 2$ reads and 2 writes. If there is no such page, the record goes to the new page $N$, at a cost of $\max(1, \lceil N / D \rceil)$ reads and 2 writes, or 3 if the last directory page had $D$ entries.

*Proof.* Lines L1 to L4 visit the entries in page id order, by (a), and stop at the first entry whose free value is at least $|r| + 4$. By (c) the value is $free(q)$, so the loop stops at $q^\ast$. The record fits in $q^\ast$, and the slotted page returns a slot $s$ that no live record of $q^\ast$ uses, so $(q^\ast, s) \notin M$. Line L7 writes the new free space, which restores (c) for $q^\ast$; no other entry changes. The reads are the directory pages $0$ to $\lfloor q^\ast / D \rfloor$ and the page $q^\ast$, and the writes are $q^\ast$ and its directory page.

If the loop finds no page, every directory page was read. Line L9 makes page $N$, which is empty, so the record fits (a record larger than an empty page is rejected before the insert). Lines L11 to L13 append the entry $(N, free(N))$ after the entry of $N - 1$, in a new directory page if the last one was full. This keeps (a), (b) and (c). The writes are page $N$ and the last directory page, plus the old last page when a new directory page is linked to it. $\square$

**Lemma 2.** A delete of $(q, s) \in M$ keeps Invariant D, removes $(q, s)$ from $M$, and costs 2 reads and 2 writes.

*Proof.* The delete reads page $q$, frees slot $s$ and writes $q$. It then reads directory page $\lfloor q / D \rfloor$, sets the entry of $q$ to the new $free(q)$, and writes the page. Only the entry of $q$ changes, and it becomes exact. $\square$

**Lemma 3.** If Invariant D holds, DIR-SCAN outputs each pair of $M$ exactly once and reads $N + \max(1, \lceil N / D \rceil)$ pages.

*Proof.* Lines L15 to L18 read every directory page once and, by (a), every data page once. Line L19 lists the live slots of each page once. Every record id $(q, s)$ in $M$ has $q < N$ and $s$ live in $q$, so it is output once, and nothing else is output. $\square$

## The linked list form

**Invariant L.** (a) Every data page is on exactly one of the two lists, and the lists are doubly linked: if $q'$ follows $q$ then $prev(q') = q$, and the head has no predecessor. (b) A page is on the full list if and only if $free(q) < m$.

**Lemma 4.** LIST-INSERT keeps Invariant L, and adds $r$ under a new record id. If the first page of the free list, in list order, in which $r$ fits is the $k$-th one, the record goes there. If that page stays on the free list, the cost is $k + 1$ reads and 1 write. If there is no such page, the cost is at most $F + 2$ reads and 3 writes, where $F$ is the length of the free list.

*Proof.* Lines L22 to L30 read the header and then the pages of the free list in order, and stop at the first page $q$ where $r$ fits. The slotted page gives a new slot. If $free(q)$ is still at least $m$, the lists do not change and (b) still holds for $q$. The pages read are the header and the first $k$ pages of the list, and the only write is $q$. If $free(q)$ drops below $m$, line L28 unlinks $q$ (its predecessor, or the header, and its successor change their pointers) and pushes it at the head of the full list (the old head and the header change). Each changed page is written once, and each list stays doubly linked. Now $q$ is on the full list and $free(q) < m$, so (b) holds.

If no page of the free list fits, all $F$ pages were read. Line L31 makes a new page with the record in it, and line L32 pushes it on the list that (b) calls for. The new reads are at most the old head of that list (which may already have been read, as the head of the free list), and the writes are the new page, the old head and the header. $\square$

**Lemma 5.** A delete keeps Invariant L. It costs 1 read and 1 write, or at most 5 reads and 5 writes when the page moves from the full list to the free list.

*Proof.* The delete reads page $q$, frees the slot and writes $q$. Its free space grows. A page on the free list stays there, which (b) allows. A page on the full list that now has $free(q) \ge m$ is unlinked from the full list and pushed on the free list, as in Lemma 4; this reads and writes at most the page, its two old neighbors, the old head of the free list and the header. $\square$

**Lemma 6.** If Invariant L holds, a scan that reads the header and walks both lists outputs each pair of $M$ once and reads $N + 1$ pages.

*Proof.* By (a), the two walks together visit each data page exactly once, and they stop at the ends of the lists. The rest is as in Lemma 3. $\square$

## Summary

**Theorem.** Starting from an empty file, after any sequence of `insert`, `delete`, `get` and `scan`, both forms keep their invariant; `get(q, s)` returns $M((q, s))$ with one read; `scan` outputs $M$; and the page I/O of each operation is the one in the table of the page.

*Proof.* The empty directory form has one empty directory page and no data pages, which satisfies Invariant D; the empty list form has an empty header, which satisfies Invariant L. Lemmas 1 to 6 show that each operation keeps the invariant and changes $M$ as its specification says. A record id $(q, s)$ stays in $M$ until its delete, since no operation moves a record to another page or another slot, so `get` reads page $q$ once and finds the record in slot $s$. $\square$

The I/O counts assume that an operation reads each page it needs once and writes each page it changes once, which holds when it can keep the two or three pages it uses in buffer frames for its duration. The implementation counts I/O in exactly this way, and the tests compare its counts with the formulas of Lemmas 1 to 6 on random sequences.
