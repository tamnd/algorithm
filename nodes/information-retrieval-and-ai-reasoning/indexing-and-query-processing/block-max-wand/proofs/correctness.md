---
title: Block-max WAND returns the exact top k under the tie rule
proves: [correctness]
status: full
---

The rank order $\prec$ is score descending, then docid ascending, and $\mathrm{top}_k(S)$ is the first $\min(k, |S|)$ pairs of a set $S$ in this order. Let $M$ be the set of matching documents and $s(x)$ the score of $x$. A step is one pass through lines L4 to L16. In a step, $d$ is the pivot, $p_0$ is the index found in line L5 and $p \ge p_0$ the index after line L8. A step is a pass step if the test of line L10 is true and a skip step if it is false; a skip step has the range $[d, n)$ of line L15. List $i$ still holds $x$ if list $i$ contains $x$ and $c_i.\mathit{docid} \le x$.

**The three conditions.**

> **(C1)** Each weight is at least 0. For every list $i$, $U_i$ is at least every weight of list $i$, and each block max is at least every weight of its block. Sums are computed exactly, or in an arithmetic in which a sum of numbers each at most its partner is at most the sum of the partners.
>
> **(C2)** The heap replaces its least entry only on a strictly greater score, and documents are offered in increasing docid order.
>
> **(C3)** Each document that is skipped has a score of at most the current threshold $\theta$.

(C1) is an assumption; (C2) and (C3) are proved below.

**Lemma 1 (after a step).** At the start of a step, every cursor with docid less than $d$ is among $c_1, \ldots, c_{p_0 - 1}$, and the bounds of these cursors sum to at most $\theta$. After a step that scores $d$, no cursor is at $d$ or below. After a skip step, every cursor is at $n$ or later, and $n > d$.

*Proof.* The first claim is the choice of $p_0$ in line L5, as in Lemma 1 of the WAND proof. Line L11 moves every cursor at $d$ past $d$, and no cursor is below $d$ since $c_1.\mathit{docid} = d$. In a skip step, each cursor of the prefix has, after line L9, a block with last docid at least $d$, or no block left, in which case its last docid is $\infty$; and if $p < m$, then $c_{p+1}.\mathit{docid} > d$ by line L8. So $n > d$. Line L16 moves $c_1, \ldots, c_p$ to $n$ or later, and $c_{p+1}, \ldots, c_m$ are at $c_{p+1}.\mathit{docid} \ge n$ or later. $\square$

**Lemma 2 (the pivots do not decrease).** The pivot of each step is at least the pivot $d$ of every earlier step. It is greater than $d$ if that earlier step scored $d$, and at least $n$ if that earlier step was a skip step.

*Proof.* Every step moves cursors only forward, and $\theta$ never decreases. After a step of line L13, the cursors with docid less than $d$ are a subset of the old $c_1, \ldots, c_{p_0-1}$: they form a prefix of the next sorted order, and their bounds sum to at most the old $\theta$, so to at most the new one, so line L5 does not pick them. After a scoring step or a skip step, Lemma 1 puts all cursors above $d$, or at $n$ or later. Induction on the steps gives the claim. $\square$

**Lemma 3 (moves that pass a document).** Let list $i$ contain $x$, and let a step move $c_i$ from a docid at most $x$ to one greater than $x$. Then either the step scores $x = d$, or $x < d$, or the step is a skip step with $d \le x < n$.

*Proof.* Line L11 moves a cursor at $d$ to the next posting of its list, which passes a posting of $x$ only if $x = d$. Line L13 moves to the first docid at least $d$, which passes $x$ only if $x < d$. Line L16 moves to the first docid at least $n$, which passes $x$ only if $x < n$, so either $x < d$ or $d \le x < n$. $\square$

**Lemma 4 (exact scores).** Each document scored in line L11 gets its exact score, and the scored documents are in strictly increasing docid order.

*Proof.* The order follows from Lemma 2. Let $d$ be scored, and let list $i$ contain $d$. Suppose that $c_i.\mathit{docid} > d$ at this time. Then an earlier step with pivot $d'$ moved $c_i$ past $d$. By Lemma 3, either it scored $d' = d$, or $d < d'$, or it was a skip step with $d' \le d < n'$. By Lemma 2 each case makes every later pivot greater than $d$, which is false for the current step. So $c_i.\mathit{docid} \le d$, and since $d = c_1.\mathit{docid}$ is the least cursor docid, $c_i.\mathit{docid} = d$. Line L11 adds the weight of every list that contains $d$, and no other weight. $\square$

**Lemma 5 (skipped documents).** If a matching document $y$ is never scored, then at some point the heap holds $k$ documents, each with a score at least $s(y)$ and a docid less than $y$.

*Proof.* If some step moves a cursor of a list that contains $y$ past $y$, take the first such step, with pivot $d$. Before it, every list that contains $y$ still holds $y$. By Lemma 3, and since $y$ is not scored, there are two cases.

Case A: $y < d$. The lists that still hold $y$ have cursors at most $y < d$, so by Lemma 1 they are among $c_1, \ldots, c_{p_0-1}$, and $s(y)$ is at most the sum of their bounds, which is at most $\theta$. If $\theta = -\infty$, then $p_0 = 1$ and no cursor is below $d$, which is false for the cursor that moves past $y$; so $\theta > -\infty$.

Case B: a skip step with $d \le y < n$. Since $B$ is a finite number, a skip step needs $\theta > -\infty$. Each list that contains $y$ has its cursor at most $y < n$, while $c_{p+1}, \ldots, c_m$ are at $n$ or later, so the list is one of $c_1, \ldots, c_p$. After line L9 its block is the first block with last docid at least $d$, and by line L15 that last docid is at least $n - 1 \ge y$. The block before it ends below $d \le y$. So the posting of $y$ lies in this block, and its weight is at most the block max by (C1). With weights at least 0, $s(y) \le B \le \theta$.

If no step moves such a cursor past $y$, the run ends in line L6 with every list that contains $y$ still holding it. No index qualifies in line L5, so the bounds of all cursors before $\infty$ sum to at most $\theta$, and $s(y) \le \theta$. If $|H| < k$, then $\theta = -\infty$ and line L5 would pick $c_1$; so $\theta > -\infty$.

In every case the heap is full, and each entry has a score at least $\theta \ge s(y)$. Each entry $z$ was scored in an earlier step, after which no cursor was at $z$ or below by Lemma 1. In each case some cursor is at most $y$ at the time, so $z < y$. $\square$

**Theorem.** Under (C1), BLOCK-MAX-WAND$(q, k)$ returns $\mathrm{top}_k(\{(x, s(x)) : x \in M\})$ in the order $\prec$.

*Proof.* Let $S$ be the set of scored documents with their scores. By Lemma 4 they are offered in increasing docid order with exact scores, so by Lemma 1 of the DAAT proof, the heap rule, the final heap is $\mathrm{top}_k(S)$. Each $y \in M \setminus S$ ranks after $k$ members of $S$ by Lemma 5, so $\mathrm{top}_k(M) = \mathrm{top}_k(S)$. $\blacksquare$

**Termination.** A pass step moves at least one cursor past at least one posting, as in WAND. A skip step moves $c_p$, which is at $d$, to $n > d$ or later. So there are at most $T$ steps.

**Remark (ties and strictness).** Lemma 5 uses $s(y) \le \theta$, not $s(y) < \theta$. A skipped document with $s(y) = \theta$ is correctly left out, because all heap entries have smaller docids. This needs the docid order of (C2) and the strict test $B > \theta$ in line L10.

**Remark (moving one cursor).** Many implementations move only one cursor of the prefix to $n$ in line L16. The same block bound shows that every document in $[d, n)$ has a score of at most $\theta$; the order argument of Lemma 2 changes, since other cursors of the prefix stay below $n$. This version is not proved here.
