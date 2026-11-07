---
title: Correctness of structured Gaussian elimination
proves: [correctness, termination]
status: full
---

We prove that STRUCTURED-GE returns a solution of $A x = c$ when one exists and reports "inconsistent" otherwise, and that it terminates. Notation is as on the main page: during the loop each column is in exactly one of $L$ (light), $H$ (heavy), $E$ (eliminated by a pivot) or $F$ (free, removed on line L3), and each row is active or set aside as a pivot row. We write rows together with their right-hand sides, so a row operation also acts on $c$.

**Termination.** Each pass of the loop removes one column from $L$, on line L3, L4, L5 or L6, and moves it to $F$, $E$, $E$ or $H$. So the loop runs at most $n$ times, and every pass, the dense solve and the back-substitution are finite.

**Invariant.** At the start of each pass of the loop:

1. (*Equivalence*) The system $S$ made of the active rows and the pivot rows set aside has the same solutions as $A x = c$.
2. (*Cleared columns*) No active row has a nonzero entry in a column of $E \cup F$.
3. (*Shape of pivot rows*) Each pivot $(r, j)$ in $P$ has $a_{rj} \ne 0$ in the stored row $r$, and every other column $k$ with $a_{rk} \ne 0$ in that stored row is in $H$ or $F$, or is in $E$ through a pivot appended to $P$ after $(r, j)$, or is still in $L$.

*Initialization.* At the start, $S$ is $A x = c$, $E = F = \emptyset$ and $P$ is empty.

*Maintenance.* Consider one pass.

- Line L3: column $j$ has weight $0$, so no active row meets it, and part 2 holds with $j \in F$. Part 3 still holds, since $F$ is allowed in pivot rows. Nothing else changes.
- Line L4: column $j$ has weight $1$, with its only active entry in row $r$. Setting row $r$ aside changes neither $S$ nor any active row, so part 1 holds. No active row meets $j$ any more, so part 2 holds. For part 3, the new pivot $(r, j)$ has $a_{rj} \ne 0$; the other entries of row $r$ are not in $E \cup F$ by part 2 (row $r$ was active), so they are in $H$ or in $L$. Older pivots are unaffected, except that a column of $L$ appearing in an older pivot row has now moved to $E$ through a pivot appended after it, which is allowed.
- Line L5: row $r$ has exactly one entry in $L$, in column $j$, and by part 2 none in $E \cup F$, so its nonzero entries are $a_{rj}$ and entries in $H$. Each active row $i$ with $a_{ij} \ne 0$ is replaced by row $i$ minus $(a_{ij} / a_{rj})$ times row $r$. This is an invertible operation on $S$, since row $r$ stays in $S$ as a pivot row, so part 1 holds. The new row $i$ has a zero in column $j$, and its other entries change only in columns of $H$, so it still has no entry in $E \cup F$: part 2 holds with $j \in E$. Part 3 holds for $(r, j)$ because its other entries are in $H$, and for older pivots as in the case of line L4.
- Line L6: a column moves from $L$ to $H$. Parts 1 and 2 are unchanged, and part 3 still holds because $H$ only grows.

**After the loop.** $L = \emptyset$, so by part 2 every active row has its nonzero entries in $H$ only. By part 3, each stored pivot row $(r, j)$ has its other nonzero entries in $H$, in $F$, or in columns pivoted after $(r, j)$.

**Inconsistent systems.** If line L7 finds the active rows, restricted to $H$, inconsistent, then no assignment of the heavy unknowns satisfies them. Since these rows involve no other unknowns, no $x$ satisfies them, so $S$ has no solution, and by part 1 neither has $A x = c$. The report is correct.

**Consistent case.** Otherwise line L7 gives values $x_k$ for $k \in H$ satisfying all active rows. Free unknowns keep the value $0$ and appear in no active row. Line L8 processes the pivots from the last to the first. When $(r, j)$ is processed, every unknown $k \ne j$ with $a_{rk} \ne 0$ in row $r$ is in $H$ or $F$, whose values are fixed, or was pivoted after $(r, j)$ and has therefore already received its value; its value does not change later, because each unknown is the column of exactly one pivot. Since $a_{rj} \ne 0$, setting $x_j = (c_r - \sum_{k \ne j} a_{rk} x_k) / a_{rj}$ makes row $r$ hold, and it stays true because none of its unknowns changes afterwards. Unknowns in $H$ and $F$ are never assigned on line L8, because the columns of pivots are in $E$. So at the end every active row and every pivot row holds: $x$ solves $S$, and by part 1 it solves $A x = c$. $\blacksquare$
