---
title: Baker's collector keeps the mutator's view, and with S at least L + ceil(L/k) no allocation fails
proves: [correctness, complexity]
status: full
---

We use the heap model and the procedures of the page. A *cycle* is the time from one flip to the next; the first cycle starts with an empty to-space and no flip. At every moment at most $L$ cells are reachable from the registers. Each mutator operation, with its barrier, is one atomic step.

**Lemma 1 (to-space invariant).** At the end of every step, every register holds nil or a to-space address.

*Proof.* At the start all registers are nil. A flip (lines L1 and L2) changes to-space and then replaces each register by EVACUATE of it, which returns nil or a to-space address (lines L3 to L7). LOAD returns EVACUATE of a field (line L8). ALLOCATE returns $\textit{top}$, which is in to-space (lines L17 and L18). Copying a register into another, clearing a register, and a store do not create a new register value. $\square$

**Lemma 2 (only gray cells hold from-space addresses).** At the end of every step, a to-space cell outside $[\textit{scan}, \textit{copy})$ has no field with a from-space address. No from-space cell is written after the flip that starts the cycle.

*Proof.* A cell below $\textit{scan}$ was scanned at line L10, which evacuates every field; after that, only stores and line L8 change its fields. A cell at or above $\textit{top}$ starts with nil fields at line L17. A store writes a register value, which is in to-space by Lemma 1, and line L8 writes an evacuated value. So these cells never get a from-space value. For the second claim: the mutator writes only fields of cells that it holds in registers, which are in to-space by Lemma 1, and the collector reads from-space cells at line L5 but writes only their forwarding address. $\square$

**Lemma 3 (the view is kept).** Define the *view* of an address $a$ as $a$ itself if $a$ is in to-space or has no forwarding address, and its forwarding address otherwise. Name each cell by its identity: a copy made at line L5 has the identity of the cell it copies. Then the graph of identities reachable from the registers, with each field read through the view, is the same after each collector action as before it.

*Proof.* Line L4 makes each from-space cell copied at most once in a cycle, and line L6 records the copy. Line L5 gives the copy the same fields, and from-space cells do not change afterward (Lemma 2), so the fields of a copy and of its original agree up to the view. EVACUATE replaces an address by its view, which has the same identity. So lines L2, L8 and L10 replace addresses only by addresses of the same identity, and lines L1 and L17 touch no reachable cell. $\square$

So the mutator, which only reads through LOAD, sees each operation give the same result, by identity, as with no collector.

**Lemma 4 (at most $L$ copies per cycle).** Every cell copied in a cycle was reachable at the flip that starts it. So a cycle copies at most $L$ cells.

*Proof.* Line L5 copies a cell $a$ only when EVACUATE gets a from-space address $a$. This happens at line L2, where $a$ is a root at the flip, or at line L8 or L10, where $a$ is a field of a to-space cell. By Lemma 2 that cell is gray, so it is a copy of a from-space cell $a'$, and by Lemma 2 again its from-space fields are those of $a'$ at the flip. By induction on the order of copies, $a'$ was reachable at the flip, so $a$ was too. $\square$

**Lemma 5 (safe flip).** If $\textit{scan} = \textit{copy}$ at the end of a step after the first flip of a cycle, then no from-space address is reachable, and no cell is copied in the rest of the cycle.

*Proof.* With no gray cell, Lemma 1 and Lemma 2 say that no register and no to-space field holds a from-space address. So the reachable cells are all in to-space, and EVACUATE gets a from-space address only from a register or a field, which does not happen. $\square$

Lemma 5 is what makes the flip at line L14 correct: line L13 allows a flip only when $\textit{scan} = \textit{copy}$, so the old from-space holds no reachable cell when it becomes the new to-space.

**Theorem.** If $S \ge L + \lceil L/k \rceil$, then line L13 and line L16 never fail, and line L5 always finds $\textit{copy} < \textit{top}$.

*Proof.* Fix a cycle, and let $c \le L$ be the number of cells that it copies (Lemma 4). Number the allocations of the cycle $1, 2, \ldots$, where allocation 1 is the one that flips. Before allocation $j$ has taken its cell, to-space holds at most $c$ copies and $j - 1$ new cells.

An allocation that ends with a gray cell left has scanned exactly $k$ cells, since line L9 stops early only when $\textit{scan} = \textit{copy}$. The scans of the cycle are distinct cells among the $c$ copies. So if allocation $j$ ends with a gray cell left, then $jk$ scans are done and $jk < c$, so $j < c/k$. Hence the first allocation that ends with no gray cell is number $j^* \le \lceil c/k \rceil \le \lceil L/k \rceil$, and by Lemma 5 no cell is copied after it.

Up to and during allocation $j^*$, to-space holds at most $c + j^* - 1 \le L + \lceil L/k \rceil - 1 < S$ cells before the new cell is taken. So each copy at line L5 finds room, the test at line L12 is false (except at the flip of allocation 1, where to-space is new), line L16 does not fail, and allocation $j^*$ gets its cell. After allocation $j^*$ nothing is copied, so line L5 is not reached, line L9 does no work, and line L16 is false whenever line L12 was false. When to-space fills at last, $\textit{scan} = \textit{copy}$, so line L13 does not fail and the flip starts the next cycle. In the first cycle nothing is copied at all. $\blacksquare$

**The pause.** Each allocation scans at most $k$ cells (line L9), each scan evacuates $p$ fields, and each evacuation copies at most $p$ words. A load evacuates one field. A flip evacuates $r$ roots. All of these are independent of $S$ and $L$.

**The bound is sufficient, not tight.** The proof charges every copy to the scan and assumes the worst order. A FIFO queue of 16 live cells with $k = 1$ runs with $S = 30$ and fails with $S = 29$, against the bound of 32.
