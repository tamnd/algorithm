---
title: The Mikami-Tabuchi line search returns a valid path, finds one whenever one exists, and runs in time linear in the grid, but its path need not be shortest
proves: [correctness, completeness, termination, running time, not exact]
status: full
---

Let $G$ be the graph of free cells, with an edge between cells that share a side. A *run* is a maximal set of free cells that are consecutive in one row (a horizontal run) or in one column (a vertical run). Every free cell lies in exactly one horizontal run and one vertical run. The probe from $b$ in orientation $o$ returns the run of orientation $o$ that contains $b$. Fix one side $X$, with origin $x$ (that is, $s$ or $t$), and say that a cell is *covered by $X$* when it has a base point $\mathrm{base}_X$.

**Lemma 1 (lines are drawn once).** Side $X$ draws each run at most once.

*Proof.* When $X$ draws the run $R$ of orientation $o$ from a base $b$, every cell of $R$ is marked as having a line of orientation $o$ from $X$. Any later pair $(b', o)$ with $b' \in R$ is skipped by line L6, and a pair $(b', o)$ with $b' \notin R$ gives a different run. $\square$

**Lemma 2 (base chains).** For every cell $c$ covered by $X$, following $\mathrm{base}_X$ from $c$ reaches $x$, and the cells passed between $c$ and its base point, and so on, form a walk from $c$ to $x$ in $G$.

*Proof.* The origin has itself as base. Any other covered cell $c$ got $\mathrm{base}_X(c) = b$ on line L9 from a run that contains both $c$ and $b$, so the cells of the run between them are free and form a straight walk. The base $b$ was covered before $c$. So following bases goes strictly back in the order of covering and ends at $x$. $\square$

**Theorem 1 (valid path).** When line L10 finds a cell $c$ covered by both sides, the walk from $s$ to $c$ by the bases of side $S$, followed by the walk from $c$ to $t$ by the bases of side $T$, is a walk from $s$ to $t$ in $G$. Cutting out the part between two visits of the same cell, as long as a cell repeats, leaves a simple path from $s$ to $t$.

*Proof.* By Lemma 2 for each side. Cutting a closed part of a walk keeps a walk with the same ends, and each cut makes it shorter, so the process stops with a walk in which no cell repeats. $\square$

**Lemma 3 (closure).** Suppose the loop of line L2 ends with no meeting. Then the set $K_X$ of cells covered by $X$ is the connected component of $x$ in $G$.

*Proof.* Every covered cell is joined to $x$ by Lemma 2, so $K_X$ lies in the component of $x$. For the other direction, let $c \in K_X$ and let $d$ be a free neighbor of $c$. The cells $c$ and $d$ lie in one run $R$, of orientation $o$ say. Consider the moment $c$ was covered. If $c = x$, the pair $(x, o)$ was in the first list. Otherwise $c$ was covered by a line of the other orientation $o'$ through it, and line L11 added $(c, o)$ to the next list, since the orientation added is the other one of the line. Either way the pair $(c, o)$ is handled in a later round, unless the loop stops first, which it does not, because a list only becomes empty after all its pairs are handled. When it is handled, either $X$ draws the run $R$ now, or line L6 skips it because $X$ has already drawn a line of orientation $o$ through $c$, which is $R$. In both cases $d \in R$ is covered. So $K_X$ is closed under free neighbors, and it contains $x$, so it contains the whole component. $\square$
**Theorem 2 (completeness).** If $t$ is reachable from $s$, the search stops on line L10 with a path. If $t$ is not reachable, it returns "no path".

*Proof.* Suppose $t$ is reachable and the loop ends with no meeting. By Lemma 3, side $S$ covers the component of $s$, which contains $t$. But $t$ is covered by side $T$ from the start, so the first time side $S$ covered $t$, line L10 found a cell covered by both sides and stopped. This is a contradiction. If $t$ is not reachable, no cell is covered by both sides, since a common cell would join $s$ and $t$ by Lemma 2. The loop ends because by Lemma 1 each side draws finitely many lines, each pair is added at most once per newly covered cell, and the lists then become empty. $\square$

**Running time.** By Lemma 1 each side draws each run at most once. The runs of one orientation partition the free cells, so the total length of all runs is at most $2MN$, and drawing a run takes time in proportion to its length. Each covered cell adds one pair to a list, so the lists have $O(MN)$ pairs in total, and each skipped pair costs $O(1)$. The cutting of loops takes time in proportion to the length of the walk, which is $O(MN)$: each segment of a base chain lies in the run that covered its cell, these runs are distinct by Lemma 1, and their total length is at most $2MN$ for each side. So the time is $O(MN)$, and the base points take $O(MN)$ space. $\square$

**Proposition (not exact).** The path found need not be shortest.

*Proof.* Take the 3 by 3 grid with rows `...`, `...` and `.#.`, $s = (2, 2)$ and $t = (2, 0)$. At level 0 the horizontal probe from $s$ is blocked at once, the vertical probe covers column 2, and side $T$ covers column 0 in the same way. At level 1 side $S$ first draws the horizontal line of $(0, 2)$, the top row. Its first cell, $(0, 0)$, is covered by side $T$, so the search stops. The path goes up column 2, along the top row and down column 0, with 6 steps. The path $(2,2), (1,2), (1,1), (1,0), (2,0)$ has 4 steps. $\square$
