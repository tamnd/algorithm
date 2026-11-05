---
title: Flood fill recolours exactly the region of the seed
proves: [correctness, termination]
status: full
---

Let $A$ be the grid before the call, $o = A[s]$ the old colour and $c$ the new colour. Let $W$ be the region of $s$: the cells reached from $s$ by a sequence of neighbouring cells that all have colour $o$ in $A$. Write $A'$ for the grid during the run. If $o = c$, line L2 returns at once, and the grid is unchanged, which is correct because recolouring $W$ with $o$ changes nothing. From now on $o \ne c$.

**Invariant.** At the start of each iteration of the loop of line L5, and when the loop ends:

1. each cell $p$ with $A'[p] \ne A[p]$ is in $W$ and has $A'[p] = c$;
2. each cell of $W$ either still has $A'[p] = o$ or has $A'[p] = c$;
3. each cell on the stack has $A'[p] = c$, and each cell that has been recoloured is on the stack now or has been popped before.

*Initialization.* After lines L3 and L4, only $s$ is changed, $s \in W$, and $s$ is on the stack. All three parts hold.

*Maintenance.* An iteration pops $p$ and, for each neighbour $q$ of $p$ with $A'[q] = o$, sets $A'[q] = c$ and pushes $q$. By part 3, $A'[p] = c \ne o$, so $p$ was recoloured, and by part 1, $p \in W$. A neighbour $q$ with $A'[q] = o$ was not changed, because changed cells have colour $c \ne o$, so $A[q] = o$. Then $q$ is a neighbour of a cell of $W$ and has colour $o$ in $A$, so $q \in W$. Recolouring it to $c$ keeps parts 1 and 2, and pushing it keeps part 3.

**Termination.** Each push follows a change of one cell from $o$ to $c$, and a cell of colour $c$ never has colour $o$ again, so at most $|W|$ cells are pushed. Each iteration pops one cell, so the loop runs at most $|W|$ times, and each iteration does at most 4 tests.

**Lemma.** When the loop ends, every cell of $W$ has colour $c$.

*Proof.* Assume a cell of $W$ still has colour $o$. Take a sequence $s = p_0, p_1, \ldots, p_j$ of neighbouring cells of colour $o$ in $A$ that ends at such a cell, and let $p_i$ be its first cell with $A'[p_i] = o$ at the end. Then $i \ge 1$, because $s$ was recoloured at line L3. The cell $p_{i-1}$ has colour $c$ at the end, by the choice of $i$ and part 2. By part 3, it was pushed, and since the stack is empty at the end, it was popped. When it was popped, its neighbour $p_i$ was tested at line L8. Colours only change from $o$ to $c$, and $p_i$ has colour $o$ at the end, so it had colour $o$ at that test. Then line L9 recoloured it, which contradicts $A'[p_i] = o$ at the end. $\square$

**Theorem.** FLOOD-FILL$(A, s, c)$ terminates, and afterwards each cell of $W$ has colour $c$ and each other cell has its colour in $A$.

*Proof.* Termination was shown above. By the lemma, all cells of $W$ have colour $c$. By part 1, each cell whose colour changed is in $W$, so each cell outside $W$ has its old colour. $\blacksquare$
