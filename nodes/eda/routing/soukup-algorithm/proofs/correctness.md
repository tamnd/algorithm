---
title: Soukup's router reaches each cell once and finds a path whenever one exists, but the path need not be shortest
proves: [correctness, completeness, termination, running time, not exact]
status: full
---

Let $G$ be the graph of free cells, with an edge between cells that share a side. Let $C$ be the set of cells reachable from $s$ in $G$. Call a cell *reached* once line L1 or line L9 marks it.

**Lemma 1 (each cell once).** A cell is marked at most once, and it is put at most once on a stack or in a wave. The parent links form a tree on the reached cells, rooted at $s$.

*Proof.* Line L8 only looks at cells that are not reached, and line L9 marks them at once. After that the cell is never chosen again by line L8. A cell enters a stack (line L11) or the next wave (line L12) only right after it is marked, so at most once. The parent of a cell is set once, to a cell that was reached before it, so following parents strictly goes back in the order of marking and ends at $s$. $\square$

**Lemma 2 (every reached cell is popped).** If the search does not stop on line L10, every reached cell is popped exactly once on line L7.

*Proof.* The source is popped, as the first cell of the first wave. Any other reached cell went either on a stack or into the list next. A stack is emptied by the loop of line L6 before the loop of line L4 moves on, so every cell pushed on it is popped. Every cell of next becomes a cell of the following wave on line L13 and is pushed on line L5 when its turn comes, and popped. The loop of line L2 only ends when a wave is empty, so no list next is left unprocessed. $\square$

**Lemma 3 (closure).** If the search ends on line L14, the set of reached cells is $C$.

*Proof.* Reached cells are in $C$, since each is a neighbor of an earlier reached cell. For the other direction, let $u$ be reached and $v$ a free neighbor of $u$. By Lemma 2, $u$ is popped, and at that time line L8 either marks $v$ or finds it already reached. So the reached set is closed under free neighbors and contains $s$. Every cell of $C$ is joined to $s$ by a path, and induction along the path shows that it is reached. $\square$

**Theorem (completeness and validity).** If $t \in C$, the router returns a path from $s$ to $t$. If $t \notin C$, it returns "no path".

*Proof.* If $t \in C$ and the search reached line L14, Lemma 3 would say that $t$ is reached. But $t$ is checked on line L10 right when it is marked, so the search would have stopped there. So the search stops on line L10. By Lemma 1 the parent links of $t$ lead to $s$, and each link joins neighbors, so they give a path. If $t \notin C$, it is never marked, and since each cell is popped at most once the search ends, on line L14. $\square$

**Running time.** By Lemma 1 and Lemma 2 each cell is pushed and popped at most once, and each pop looks at 4 neighbors. The sorting on line L11 handles at most 4 cells. So the time is $O(MN)$. The marks, parents, stack and waves take $O(MN)$ space. $\square$

**Proposition (not exact).** There are grids where the path found is longer than the shortest path.

*Proof.* Take the 5 by 2 grid with the blocked cell $(1, 0)$, $s = (4, 1)$ and $t = (0, 0)$, with neighbors tried up, right, down, left. Both $(3, 1)$ and $(4, 0)$ are toward $t$. The cell $(4, 0)$ is pushed last and popped first, and the run goes up to $(2, 0)$, which marks $(2, 1)$ with parent $(2, 0)$. When $(3, 1)$ is popped, $(2, 1)$ is already reached. So the path to $t$ goes through $(4, 0), (3, 0), (2, 0), (2, 1), (1, 1), (0, 1)$ and has 7 steps, while the path $(4,1), (3,1), (2,1), (1,1), (0,1), (0,0)$ has 5. $\square$
