---
title: Mark-and-sweep frees exactly the unreachable cells and keeps the reachable ones intact
proves: [correctness, termination]
status: full
---

**Setting.** The heap has the cells $0, \ldots, n-1$. Each cell has $k$ fields, and each field holds an address or nil. Write $\rho$ for the multiset of root values when COLLECT starts, and $R$ for the set of cells reachable from the non-nil roots: the least set that holds each non-nil root and holds $y$ whenever it holds $x$ and some field of $x$ is $y \ne$ nil. We assume two facts that the mutator and the allocator keep: (A1) no mark bit is set when COLLECT starts, and (A2) no field of a cell in $R$ and no root points to a cell on the free list. The claim is that after COLLECT returns: (C1) the free list holds each cell of $\{0, \ldots, n-1\} \setminus R$ exactly once and no other cell; (C2) every field of every cell of $R$ has the value it had at the start; (C3) no mark bit is set.

**Lemma 1 (the mark phase).** When the loop of line L3 exits, the set $M$ of marked cells equals $R$. The loop runs at most $n$ times.

*Proof.* Consider these three statements at the test of line L3:

- (I1) $M \subseteq R$;
- (I2) every non-nil root is in $M$;
- (I3) for each cell $x \in M$ that is not on $W$, every non-nil field of $x$ is in $M$.

*Initialization.* By (A1), $M$ is empty before line L2. Line L2 marks each non-nil root and pushes it, so after line L2, $M$ is the set of non-nil roots, which is a subset of $R$, and every marked cell is on $W$. So (I1), (I2) and (I3) hold.

*Maintenance.* An iteration pops a cell $x$ at line L4. The cell $x$ is marked, because a cell is pushed only at the moment it is marked. Lines L5 and L6 visit each field $y$ of $x$. If $y \ne$ nil and $y$ is unmarked, line L6 marks $y$ and pushes it. Since $x \in R$ by (I1) and $y$ is a field of $x$, $y \in R$, so (I1) holds. Marks are only set in this phase, so (I2) holds. After the iteration, every non-nil field of $x$ is marked, which gives (I3) for $x$; a cell $y$ that became marked is on $W$, so (I3) asks nothing of it; for the other cells, the iteration only adds marks, so (I3) still holds.

*Termination.* A cell is pushed only when it changes from unmarked to marked, and no mark is cleared in this phase. So each cell is pushed at most once, there are at most $n$ pushes, and so at most $n$ pops. Each iteration pops one entry, so the loop runs at most $n$ times.

*At exit.* $W$ is empty, so by (I3) $M$ is closed under fields, and by (I2) it holds every non-nil root. $R$ is the least set with these two properties, so $R \subseteq M$. With (I1), $M = R$. $\square$

**Lemma 2 (the sweep).** For $j = n, n-1, \ldots, 0$, let $S_j$ be the state after the loop of line L8 has handled the addresses $n-1$ down to $j$ (so $S_n$ is the state after line L7, and $S_0$ the state at the end). In $S_j$: the free list holds exactly the cells of $[j, n) \setminus R$, each one time, linked in increasing order of address; the cells of $[j, n) \cap R$ are unmarked and their fields are unchanged.

*Proof.* *Initialization.* Line L7 makes the list empty, and $[n, n)$ is empty, so $S_n$ satisfies the invariant. *Maintenance.* Assume $S_{a+1}$ satisfies it, and consider the iteration for $a$. By Lemma 1, the cell $a$ is marked exactly when $a \in R$. If $a \in R$, line L9 clears its mark and does not touch its fields or the list. If $a \notin R$, line L10 overwrites its fields with a link to the old head and makes $a$ the new head. The address $a$ is smaller than all addresses already on the list, so the list stays in increasing order and holds $a$ one time. Line L10 writes only to the cell $a \notin R$, so no field of a cell of $R$ changes. So $S_a$ satisfies the invariant. *Termination.* The loop runs $n$ times, and $S_0$ satisfies the invariant for the full range $[0, n)$. $\square$

**Theorem.** COLLECT terminates and (C1), (C2) and (C3) hold.

*Proof.* The mark loop terminates by Lemma 1, and the sweep loop runs $n$ times. The mark phase writes only mark bits. So the fields of the cells of $R$ are unchanged after the mark phase, and by Lemma 2 they are unchanged after the sweep, which is (C2). Lemma 2 at the end of the sweep gives (C1) and shows that the marks of the cells of $R$ are clear. The cells outside $R$ are never marked, by Lemma 1, so (C3) holds. $\square$

**Corollary (allocation).** If ALLOCATE returns a cell $a$, then $a$ is not reachable from the roots at the moment of the call. If the free list was empty, line L11 runs COLLECT, and by (C1) the new free list holds only unreachable cells. If it was not empty, its cells are unreachable by (A2). In both cases line L13 takes the head of the list, which is unreachable, and clears its fields. If line L12 fails, (C1) says that every cell is reachable, so the heap is full of live data. $\blacksquare$
