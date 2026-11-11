---
title: YATA keeps every item between its origins, puts local inserts in place, and orders a shared gap by client id
proves: [invariant, correctness, termination]
status: full
---

**Scope.** This file proves three properties of the integrate loop of the main block: the origin invariant, local intent, and the conflict rule for items that share both origins. It does not prove convergence in general, for runs of items typed after other items in a gap; that rests on the ordering rules of the YATA paper and is checked by the seeded tests.

**Setting.** Each replica holds a list of items. An item $x$ has a unique id $(c, k)$ with client $c$, an origin $x.o$ and a right origin $x.r$, each an id or none. A local insert at visible index $i$ takes as $x.o$ the visible element $i - 1$ (or none) and as $x.r$ the item right after $x.o$ in the list, deleted or not (or none). An item is integrated at a replica only when its origins are present there, and at most once.

**Claim 1 (origin invariant).** At every replica and every time, every item $x$ in the list has $\mathrm{pos}(x.o) < \mathrm{pos}(x) < \mathrm{pos}(x.r)$, with $\mathrm{pos}(\text{none})$ read as $-1$ on the left and as the list length on the right.

*Proof.* By induction on integrations. Deletes change no positions. Consider the integration of $x$. Lines L1 and L2 set $\mathit{left} = \mathrm{pos}(x.o)$ and $\mathit{right} = \mathrm{pos}(x.r)$. By the hypothesis for $x.r$, if $x.o$ and $x.r$ are both present, $x.o$ is left of $x.r$; this holds because at the source $x.r$ is right after $x.o$, and the hypothesis keeps that order at every replica. In the loop, $\mathit{left}$ only changes to some $k$ with $\mathit{left} < k < \mathit{right}$. So line L10 puts $x$ at a position $p$ with $\mathrm{pos}(x.o) < p \le \mathrm{pos}(x.r)$; after the insertion $x.r$ moves to $\mathrm{pos}(x.r) + 1 > p$. For any other item $y$, inserting one element into the list keeps the relative order of $y$, $y.o$ and $y.r$. $\square$

**Claim 2 (local intent).** A local INSERT$(i, x)$ makes $x$ the $i$-th visible element at its source.

*Proof.* At the source, $x.r$ is the item right after $x.o$, so $\mathit{right} = \mathit{left} + 1$, the loop of line L3 does not run, and line L10 puts $x$ right after $x.o$. The items up to and including $x.o$ hold $i - 1$ visible elements, by the choice of $x.o$, so $x$ is the $i$-th. $\square$

**Claim 3 (the conflict rule).** Let $O$ and $R$ be two items, with $R$ right after $O$ at some time, and let $x_1, \ldots, x_m$ be items with origin $O$ and right origin $R$ and distinct client ids. Suppose that no other item is ever integrated between $O$ and $R$ at any replica. Then at every replica that has integrated a subset $S$ of the $x_j$, the items between $O$ and $R$ are $S$ in increasing client id order.

*Proof.* By induction on the number of integrated $x_j$. With none, $O$ is right before $R$, since nothing else is ever put between them. Assume the gap holds $S$ sorted by client id and integrate $x = x_j$. Every item $o$ in the gap has $o.o = O = x.o$, so only lines L4 to L6 apply. If $o$ has a smaller client id than $x$, line L5 moves $\mathit{left}$ to $o$. At the first $o$ with a larger client id, $o.r = R = x.r$, so line L6 stops the scan. Since the gap is sorted, $\mathit{left}$ ends at the last item with a smaller client id, or at $O$, and line L10 puts $x$ right after it. The gap is again sorted. Two different integration orders therefore give the same gap. $\square$

**Theorem.** Claims 1 to 3 hold for every run in the stated model. In particular, items inserted concurrently into the same gap converge to client id order at every replica, and every item keeps the neighbours its author saw on the correct sides.

*Proof.* Claims 1 to 3. $\square$

**Termination.** The loop of line L3 moves $k$ forward from $\mathit{left} + 1$ to at most $\mathit{right}$, a finite range. $\blacksquare$
