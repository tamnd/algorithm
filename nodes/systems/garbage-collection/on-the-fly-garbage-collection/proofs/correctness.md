---
title: The handshake collector never frees a cell that some thread can reach
proves: [correctness]
status: full
---

We use the heap model, the concurrency model and the procedures of the page. Steps are atomic; a store is two steps, line L11 and then lines L12 to L14; a thread answers a post (lines L9 and L10) only between two of its operations. A cell is *gray* if it is on $W$, *black* if it is marked and not on $W$, and *white* if it is not marked. SHADE turns a white cell gray. Let $t_0$ be the moment the collector posts async.

**Lemma 1 (no black cell before the trace).** Until every thread has answered async, no cell is black.

*Proof.* Cells become black only at line L3, which runs after line L2 has seen every answer to async. A cell allocated black at line L15 needs $\textit{status}_m = $ async and the flag *marking*, so it is allocated after $t_0$ by a thread that has answered async. It has nil fields, so we treat it as gray with nothing to scan; this changes no argument below. $\square$

**Lemma 2 (every deletion after $t_0$ is shaded).** Each store whose second step runs after $t_0$ shades the old value of the field.

*Proof.* Let thread $m$ do the store. If $\textit{status}_m$ is sync1 or sync2, line L12 shades the old value. Otherwise $\textit{status}_m$ is async. Before $t_0$ every thread answered sync1 and sync2 (line L2), so a thread whose status is async after $t_0$ has answered the post of $t_0$. It answered at a safe point, so the whole store, with its first step at line L11, came after that answer and after $t_0$. Then *marking* was true at line L11, and line L13 shades the old value. $\square$

Lemma 2 is where the sync statuses matter. If the collector posts async with no sync status before it, a thread whose status is async from the previous cycle can read the flag before $t_0$ and write after it with no shade. The example on the page is such a schedule.

**Definitions.** At a moment after $t_0$, let $A$ be the set of threads that have answered async. The *domain* is the set of cells reachable from the registers of the threads in $A$ or from a marked cell. A white cell $z$ is *protected* if some path of fields leads from a gray cell to $z$ through white cells only.

**Invariant K.** From $t_0$ until the trace ends, every white cell in the domain is protected.

*Proof.* At $t_0$, $A$ is empty and by Lemma 1 every marked cell is gray. A white cell $z$ in the domain is reachable from a gray cell; on such a path, the last marked cell is gray, and the rest of the path is white. So $z$ is protected.

We check each kind of step.

- *Shading of a cell $y$* (by line L4, L10, L12 or L13). This only turns white cells gray, which keeps every protecting path or shortens it. New cells may join the domain: those reachable from $y$. Let $z$ be such a cell and white, and take a path from $y$ to $z$. If no cell after $y$ on it is marked, it is a protecting path from the gray $y$. Otherwise let $c$ be the last marked cell on the path. If $c$ is gray, the rest of the path protects $z$. If $c$ is black, then $z$ was reachable from the marked cell $c$ before the step, so $z$ was in the domain and protected, and still is.
- *Scan of a gray $x$* (lines L3 and L4). The scan shades the fields of $x$, as above, and then $x$ turns black. A protecting path that started at $x$ continues with a field of $x$, which is now marked; if that cell is gray, the rest of the path protects $z$, and if it was black already the path did not start at $x$. The domain does not grow, since the cells reachable from $x$ were in it.
- *An answer by thread $m$* (lines L9 and L10). The registers of $m$ are shaded, which is the first case. Then $m$ joins $A$; the cells it reaches are reachable from its registers, which are now marked, so they were in the domain already.
- *A load by thread $m$.* If $m \in A$, the new register value is a field of a cell in the domain, so the domain does not grow. If $m \notin A$, its registers are not part of the definition of the domain.
- *A register clear.* The domain does not grow.
- *An allocation.* A thread in $A$ allocates a black cell with nil fields, and the domain gains no white cell. A thread not in $A$ allocates a white cell into its own register, outside the domain.
- *A store $x.f \leftarrow y$ by thread $m$, second step.* Two things change. The edge from $x$ to the old value $o$ is removed; a protecting path that used this edge is cut, but by Lemma 2 the barrier shaded $o$ first, so the part of the path after $o$ is a protecting path from the gray $o$. The edge from $x$ to $y$ is added. If $m \in A$, then $y$ is in a register of $m$ and in the domain already. If $m \notin A$, then $\textit{status}_m$ is sync2 (every thread answered sync2 before $t_0$ and has not answered async), and line L12 shades $y$, which is the first case. $\square$

**Lemma 3 (the trace marks every reachable cell).** When the trace ends at line L5, every cell reachable from the registers of any thread is marked.

*Proof.* The trace runs after every thread has answered async, so $A$ holds all threads and the domain contains every reachable cell. The trace ends when $W$ is empty, so there is no gray cell and no white cell is protected. By Invariant K, no white cell is in the domain. $\square$

**Theorem.** The sweep frees no cell that is reachable at the time it is freed, or later.

*Proof.* After line L5 the flag *marking* is false, and SHADE does nothing, so no stale mark is set during the sweep. Line L7 frees a cell $s$ only if it is unmarked when the sweep reaches it. A cell allocated during the sweep at an address not yet swept is marked at line L15, and a cell allocated behind the sweep pointer is not visited. So $s$ existed at the end of the trace, and by Lemma 3 it was unreachable then. Threads get new references only by loads from cells they reach and by allocation, so $s$ stays unreachable until it is freed, and it is reachable afterwards only as a newly allocated cell. $\blacksquare$

**Remark on the second sync status.** The proof uses only that every thread answered some sync status before $t_0$, and the exhaustive test of the implementation also finds no loss with sync1 and async alone. The published protocol has both sync1 and sync2, and its proof treats a finer interleaving of the barrier than the one used here. This model does not show a role for the second status.
