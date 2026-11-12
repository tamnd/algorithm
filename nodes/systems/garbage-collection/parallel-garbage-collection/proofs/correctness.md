---
title: Parallel marking with work stealing marks exactly the reachable cells, scans each once, and stops only when no work is left
proves: [correctness, termination]
status: full
---

We use the heap model and the template of the page. Each execution of lines L2 to L4, of lines L5 to L7, of line L9, and of one test at line L10 or L11 is one atomic step, and the steps of the $P$ workers interleave in any order. Before the workers start, every root is marked and pushed on exactly one deque. Let $R$ be the set of cells reachable from the roots, and $D = \bigcup_i D_i$ the cells in all deques.

**Lemma 1 (each cell enters a deque at most once).** A cell is pushed at line L4 only by the step whose TEST-AND-SET changes its mark from clear to set; a root is pushed once at the start, after its mark is set. Line L7 moves a cell from one deque to another, without a new push. So each cell is in at most one deque, at most once in the whole run, and it is scanned (popped at line L2) at most once. $\square$

**Lemma 2 (the marking invariant).** At the end of every step: (a) every marked cell is in $R$; (b) every marked cell is in $D$ or has been scanned; (c) every field of a scanned cell is nil or marked.

*Proof.* At the start only roots are marked, and all are in $D$. Line L4 marks $y$, a field of $x \in R$, so $y \in R$, and pushes $y$ in the same step. A pop at line L2 is followed in the same step by lines L3 and L4, which mark every field of $x$. Line L7 keeps the cell in $D$. No step clears a mark. $\square$

**Lemma 3 (the count).** At the end of every step, every worker whose deque is not empty is counted in *active*, and $\textit{active}$ equals the number of workers that are not in the offer state of lines L9 to L11.

*Proof.* A worker enters the offer state only at line L9, when its own deque is empty (the test at line L2 failed and no other deque was non-empty at line L5). In the offer state it pushes nothing, and no other worker pushes on its deque (pushes go to the worker's own deque). It leaves the offer state at line L10 and adds itself to *active* in the same step. $\square$

**Theorem.** (1) If any worker stops at line L11, then $D$ is empty, every worker is in the offer state, and the marked set is exactly $R$. (2) Each cell of $R$ is scanned exactly once. (3) Every fair run stops.

*Proof.* (1) A worker stops when $\textit{active} = 0$. By Lemma 3 every worker is then in the offer state and every deque is empty. By Lemma 2(b) every marked cell has been scanned, and by Lemma 2(c) the marked set is closed under the fields. It contains the roots, so it contains $R$, and by Lemma 2(a) it is exactly $R$. No worker can push again, since no worker leaves the offer state while $D$ is empty, so the result is final.

(2) By (1) and Lemma 2(b) every cell of $R$ is scanned, and by Lemma 1 at most once.

(3) Each scan step adds a cell to the scanned set, which by Lemma 1 has at most $|R|$ elements. A steal step does not scan, and an adversary can move one cell from thief to thief forever: with two workers and one cell, worker 1 steals it, then worker 0 steals it back, in every round. In the simulation the order of the workers in each round is random, so in each round that starts with $D$ not empty, a worker whose deque is not empty comes first in the order with probability at least $1/P$, and it then scans a cell. So with probability 1, $D$ becomes empty after finitely many rounds. (Real collectors avoid the livelock: the thief scans the stolen cell in the same step.) After that, every worker fails at line L5 and offers to stop, no worker comes back at line L10, *active* drops to 0, and every worker stops at its next test at line L11. $\blacksquare$

**The bound on time.** In a round, every worker that has work scans one cell. The rounds are at least $T_1/P$, since there are $T_1 = |R|$ scans, and at least $T_\infty$, since a cell at depth $d$ in the order of discovery can be pushed only after a cell at depth $d - 1$ was scanned. Work stealing with random victims comes within a constant factor of $T_1/P + T_\infty$ in expectation; see [work stealing](/work-stealing/).
