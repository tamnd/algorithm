---
title: The PAES archive is non-dominated and bounded, and without the bound it equals the front of all points evaluated
proves: [correctness]
status: full
---

All objectives are minimized, $M$ is the archive bound, and line numbers refer to the `pseudo id=main` block of the PAES page. We write $a \preceq b$ when $a$ weakly dominates $b$. PAES is a heuristic; the statements below are about its archive and its current solution, not about reaching the Pareto front of a problem.

## The archive

**Lemma 1.** Lines L11 to L14 keep the archive mutually non-dominated, with distinct images and at most $M$ members.

*Proof.* Line L11 rejects $m$ if a member weakly dominates it, so an added $m$ is not dominated by a member and has a new image. Line L12 removes the members that $m$ dominates, so after the addition no member dominates another. Line L13 adds only when $\lvert A \rvert < M$, and line L14 removes one member for the one it adds. $\square$

**Lemma 2.** Let $A$ be the set of non-dominated images of a finite set $S$, one member per image, and let $\lvert A \rvert < M$ after line L12. Then after lines L11 to L13 the images of $A$ are the non-dominated images of $S \cup \{f(m)\}$.

*Proof.* If a member $a$ has $a \preceq f(m)$, line L11 returns. Then $f(m)$ is dominated by or equal to $a$, every image that $f(m)$ dominates is dominated by $a$ too, and so the non-dominated images of $S \cup \{f(m)\}$ are those of $S$. Otherwise no point $z \in S$ dominates $f(m)$: if one did, some non-dominated image $w$ of $S$ would have $w \preceq z$, and that $w$, a member of $A$, would dominate $f(m)$. So $f(m)$ is non-dominated in $S \cup \{f(m)\}$, and the other non-dominated images are those of $S$ that $f(m)$ does not dominate. Lines L12 and L13 make exactly this set. $\square$

**Theorem 3.** If the archive never holds $M$ members when line L13 runs, then after each step the images of $A$ are exactly the non-dominated images of all points evaluated so far.

*Proof.* By induction on the steps. At the start $A = \{c\}$ and $c$ is the only point evaluated. In a step, let $S$ be the points evaluated before it. If line L4 discards $m$, then $f(c)$ dominates $f(m)$ and $c$ is in $S$, so $f(m)$ is not non-dominated in $S \cup \{f(m)\}$, and every image that $f(m)$ dominates is dominated by $f(c)$; the non-dominated images do not change, and neither does $A$. Line L6 is the same with an archive member in place of $c$. In the other branches lines L5 and L8 call lines L11 to L13, and Lemma 2 applies. $\square$

With the bound, a member removed by line L14 no longer blocks the points that it dominates, so a later archive can hold a point that an earlier member dominated.

## The current solution

**Lemma 4.** The current solution never moves to a point that it dominates.

*Proof.* The current solution changes only in line L5, where $f(m)$ dominates $f(c)$, and in line L9, which line L4 does not let run when $f(c)$ dominates $f(m)$. $\square$

## Crowding

**Lemma 5.** When line L14 replaces a member, the removed member is in a most crowded cell, and in the grid of that step the largest cell count does not grow.

*Proof.* Let $t$ be the largest count and $k < t$ the count of the cell of $m$. The removal lowers one cell of count $t$ to $t - 1$, and the addition raises the cell of $m$ to $k + 1 \le t$. If the two cells are the same, which needs $k = t$, the rule does not fire. No other count changes. $\square$

The grid moves when the range of the archive changes, so the largest count can grow from one step to the next.

## The output

**Lemma 6.** Line L10 returns a nonempty set of mutually non-dominated solutions with at most $M$ members.

*Proof.* The archive starts with $c$. If line L12 removes a member, then $\lvert A \rvert < M$ after it, and line L13 adds $m$. Line L14 removes a member only when it adds $m$. So the archive never becomes empty. The rest is Lemma 1. $\square$
