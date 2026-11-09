---
title: Pareto local search terminates on a finite space and returns a Pareto local optimum set, which is the whole front under a complete neighbourhood
proves: [correctness]
status: full
---

All objectives are minimized, $p$ is the number of objectives, and $y = f(x)$ is the image of $x$. The search space $X$ is finite, each solution $x$ has a finite neighbour set $\mathcal{N}(x)$, and line numbers refer to the `pseudo id=main` block of the Pareto local search page. We write $a \preceq b$ when $a$ weakly dominates $b$ (each coordinate of $a$ is at most that of $b$) and $a \prec b$ when $a$ dominates $b$. Call an image $y$ *covered* by the archive $A$ when some member $a \in A$ has $f(a) \preceq y$.

## Invariants

**Lemma 1.** At all times:

1. no member of $A$ dominates another, and no two members have the same image;
2. once an image is covered, it stays covered;
3. the images of $A$ are exactly the non-dominated images among the start and all neighbours evaluated so far.

*Proof.* (1) Line L5 adds $x'$ only when no member weakly dominates $f(x')$, so $f(x')$ is not equal to and not dominated by any member; line L6 removes the members that $f(x')$ dominates before it adds $x'$. (2) A member $a$ leaves $A$ only in line L6, when a new member $x'$ with $f(x') \prec f(a)$ enters. If $f(a) \preceq y$, then $f(x') \preceq y$, so $y$ is still covered. (3) This is the induction for an elitist archive. If a member weakly dominates the new image, the set of non-dominated images does not change. Otherwise no evaluated image dominates the new image. Every evaluated image is covered from the moment it is evaluated, because line L5 either finds it covered or adds it, and by (2) it stays covered. So a dominator $s$ of the new image $y$ would have a member $a$ with $f(a) \preceq s \prec y$, and $a$ would weakly dominate $y$. So the new image is non-dominated, and the old images it dominates are exactly the members that line L6 removes. $\square$

## Termination

**Theorem 2.** On a finite space, each image enters $A$ at most once, the loop of lines L2 to L7 runs at most $\lvert f(X) \rvert$ times, and the search stops.

*Proof.* An image that is in $A$ is covered, and by Lemma 1(2) it stays covered for the rest of the run. Line L5 rejects every solution whose image is covered. So after an image enters $A$ once, no solution with that image enters again. Hence the number of entries, the start included, is at most $\lvert f(X) \rvert$. Each pass of the loop marks one unvisited member visited in line L7, and a visited member is never unmarked, so each entry gives at most one pass. The loop stops when no member is unvisited, after at most $\lvert f(X) \rvert$ passes, each of which scans the finite set $\mathcal{N}(x)$. $\square$

## What the result is

Paquete, Chiarandini and Stützle call a set $S$ of solutions a *Pareto local optimum set* when no member of $S$ dominates another and no neighbour of a member of $S$ dominates a member of $S$.

**Theorem 3.** When the search stops, every neighbour of every member of $A$ has a covered image, and $A$ is a Pareto local optimum set.

*Proof.* Let $x \in A$. It was visited, because the loop stops only when every member is visited. During the visit, each $x' \in \mathcal{N}(x)$ was either rejected by line L5 because it was covered, or added, so covered by itself. By Lemma 1(2) it is still covered. Now suppose a neighbour $x'$ of a member dominates a member $a$. A member $b$ covers $x'$, so $f(b) \preceq f(x') \prec f(a)$ and $b$ dominates $a$, against Lemma 1(1). $\square$

A Pareto local optimum set need not be the front. On the path $a - b - c$ with $f(a) = (1, 1)$, $f(b) = (2, 2)$ and $f(c) = (0, 0)$, the search from $a$ rejects $b$ and stops with $A = \{a\}$, while the only Pareto-optimal image is $(0, 0)$.

**Corollary 4 (complete neighbourhood).** If $\mathcal{N}(x) = X$ for every $x$, the images of the final archive are exactly the Pareto front of $f(X)$, one solution per image.

*Proof.* The start was visited in the first pass, so every $z \in X$ was evaluated. By Lemma 1(3) the images of $A$ are the non-dominated images of all of $f(X)$, which is the front, and by Lemma 1(1) each appears once. $\square$

**Theorem 5 (connected efficient set).** Suppose that the start is efficient, that no two efficient solutions have the same image, and that the efficient solutions form a connected subgraph of the neighbour graph. Then the final archive is exactly the set of efficient solutions.

*Proof.* An efficient solution $z$ never leaves $A$ once it enters, because line L6 removes only dominated images. If $z$ is evaluated while it is not in $A$, line L5 adds it: a member $a$ with $f(a) \preceq f(z)$ would have $f(a) = f(z)$ because $f(z)$ is non-dominated, so $a$ would be efficient with the same image, and $a = z$ by hypothesis. So every efficient solution that is evaluated enters $A$, stays there and is visited, and then all its neighbours are evaluated. Starting from the efficient start, induction along paths in the connected subgraph shows that every efficient solution is evaluated, so all of them are in $A$. Every member of $A$ is efficient, because a member with a dominated image $f(a) \succ f(z)$, $z$ efficient, would be dominated by the member $z$, against Lemma 1(1). $\square$

The hypotheses matter. Ehrgott and Klamroth showed that the efficient set of some combinatorial problems is not connected under natural neighbourhoods, and the trap above shows that a dominated start can stop the search before it meets the front.
