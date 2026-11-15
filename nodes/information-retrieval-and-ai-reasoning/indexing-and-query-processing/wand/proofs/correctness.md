---
title: WAND with F = 1 returns the exact top k under the tie rule
proves: [correctness]
status: full
---

The rank order $\prec$ is score descending, then docid ascending, and $\mathrm{top}_k(S)$ is the first $\min(k, |S|)$ pairs of a set $S$ in this order. Let $M$ be the set of matching documents and $s(x)$ the score of $x$. A step is one pass through lines L4 to L12. We say that list $i$ still holds $x$ if list $i$ contains $x$ and $c_i.\mathit{docid} \le x$.

**The three conditions.** The proof uses exactly these.

> **(C1)** Each weight is at least 0, and for every list $i$ and posting $(x, w)$ of it, $w \le U_i$. Sums of bounds and sums of weights are computed exactly, or in an arithmetic in which a sum of numbers each at most its partner is at most the sum of the partners. Floating-point sums in different orders do not have this property.
>
> **(C2)** The heap replaces its least entry only on a strictly greater score, and documents are offered to it in increasing docid order.
>
> **(C3)** $F = 1$: each document that is skipped has a score of at most the current threshold $\theta$.

(C2) and (C3) are proved below from the code, given $F = 1$; (C1) is an assumption on the index and the arithmetic.

**Lemma 1 (bound of a prefix).** At the start of a step, let $p$ be the value of line L5, or $p = m + 1$ if there is none. Every document $x$ with $x < c_p.\mathit{docid}$ (with $c_{m+1}.\mathit{docid} = \infty$) has at most $U_1 + \cdots + U_{p-1}$ as the sum of the weights of the lists that still hold it, and this sum is at most $\theta$.

*Proof.* A list that still holds $x$ has $c_i.\mathit{docid} \le x < c_p.\mathit{docid}$, so its cursor is one of $c_1, \ldots, c_{p-1}$ in the sorted order. Each of its weights in $x$ is at most its bound by (C1), and weights are at least 0. If $p - 1 \ge 1$, the least index $p$ of line L5 means that the sum $U_1 + \cdots + U_{p-1}$ is not greater than $\theta$, or else $p - 1$ would qualify (cursors $c_1, \ldots, c_{p-1}$ are not at $\infty$, since they are less than $c_p.\mathit{docid}$). If $p = 1$ the sum is empty. $\square$

**Lemma 2 (the pivots do not decrease).** Let $d$ be the pivot of a step. In each later step the pivot is at least $d$, and after a step that scores $d$ every later pivot is greater than $d$.

*Proof.* Consider the step with pivot $d$ and index $p$. Before it, the cursors with docid less than $d$ are among $c_1, \ldots, c_{p-1}$, and by the choice of $p$ their bounds sum to at most $\theta$. The step moves cursors only forward. In line L12 the moved cursor goes to a docid at least $d$. In line L9, all the cursors at $d$ move forward, and since $c_1.\mathit{docid} = d$ no cursor is less than $d$. So after the step, the cursors with docid less than $d$ are a subset of the old $c_1, \ldots, c_{p-1}$, and after a scoring step there are none at $d$ or below. The threshold never decreases, since the heap only gets better. In the next sort these cursors form a prefix, every shorter prefix has a smaller or equal bound sum since bounds are at least 0, and the whole prefix sums to at most the old $\theta$, so to at most the new one. So line L5 cannot pick a cursor with docid less than $d$, and after a scoring step it cannot pick one at $d$ or less. Induction on the steps gives the claim for all later steps. $\square$

**Lemma 3 (exact scores, increasing order).** Each document scored in line L9 gets its exact score $s(d)$, and the documents are scored in strictly increasing docid order.

*Proof.* The order follows from Lemma 2. For the score: in line L8, $c_1.\mathit{docid} = d$ is the least docid, so no cursor is before $d$. Let list $i$ contain $d$. Its cursor has not passed $d$: a cursor moves past a docid only in line L9, past the pivot of that step, which is less than $d$ by Lemma 2, or in line L12 to the first docid at least the pivot of that step, which is at most $d$ by Lemma 2. So $c_i.\mathit{docid} = d$, and line L9 adds its weight. No other list contributes. $\square$

**Lemma 4 (skipped documents).** Call a matching document $y$ skipped if it is never scored. Then at some point of the run the heap holds $k$ documents, each with a score at least $s(y)$ and a docid less than $y$.

*Proof.* Let $y$ be skipped. Since $y$ is never scored, the run ends with some list that contains $y$ having its cursor past $y$, or with no pivot while some list still holds $y$.

Case A: a cursor first moves past $y$ in line L12 of some step with pivot $d$ and index $p$. Then $y < d$, since the cursor goes to the first docid at least $d$, and it was at a docid at most $y$. So $y < c_p.\mathit{docid}$, and by Lemma 1 the lists that still hold $y$ at the start of this step have weights summing to at most $\theta$. Every list that contains $y$ still holds it at that time: a cursor moves past $y$ for the first time in this step, and line L9 never moves a cursor past $y$ without scoring $y$, which does not happen. So $s(y) \le \theta$. If $|H| < k$, then $\theta = -\infty$ and line L5 picks $p = 1$, so $c_1.\mathit{docid} = d$ and line L12 is not reached. So the heap is full, each entry has a score at least $\theta \ge s(y)$, and each entry was scored before this step, at a docid less than $y$: every scored docid $z$ was the least cursor docid at its time, and the cursor that moves past $y$ in this step was at a docid at most $y$ after $z$ was scored, so $z$ was less than that docid, which is at most $y$. If $z = y$ then $y$ was scored, so $z < y$.

Case B: the run ends in line L6 while some list still holds $y$. Then $p = m + 1$ in Lemma 1, and $s(y) \le \theta$ as in case A. If $|H| < k$ then $\theta = -\infty$ and line L5 picks $c_1$ whenever a cursor is not at $\infty$; so $|H| = k$. Every entry was scored at a docid less than the least cursor docid, which is at most $y$, so less than $y$. $\square$

In both cases the condition $s(y) \le \theta$ is (C3).

**Theorem.** With $F = 1$ and (C1), WAND$(q, k)$ returns $\mathrm{top}_k(\{(x, s(x)) : x \in M\})$ in the order $\prec$.

*Proof.* Let $S$ be the set of scored documents with their scores. By Lemma 3 they are offered in increasing docid order with exact scores, so by Lemma 1 of the DAAT proof (the heap rule, which uses the strict replacement of (C2)) the final heap is $\mathrm{top}_k(S)$. Take a skipped $y$. By Lemma 4, $S$ holds $k$ documents with a score at least $s(y)$ and a smaller docid; each of them ranks before $y$ by $\prec$. So $y \notin \mathrm{top}_k(M)$, and every element of $\mathrm{top}_k(M)$ is in $S$. Since $S \subseteq M$, $\mathrm{top}_k(M) = \mathrm{top}_k(S)$. $\blacksquare$

**Termination.** Line L9 moves at least one cursor, and line L12 moves $c_j$ from a docid less than $d$ to one at least $d$. Each step moves a cursor past at least one posting, so there are at most $T$ steps.

**Remark (the threshold factor).** With $F > 1$, Lemma 1 gives only $s(y) \le F\theta$ for a skipped document, and a document with $\theta < s(y) \le F\theta$ can be skipped although it belongs to the top $k$. The example on the page, with lists a = (d1 1, d2 1) and b = (d2 1), $k = 1$ and $F = 2$, returns d1 in place of d2. The method is then approximate.

**Remark (ties).** Lemma 4 uses $s(y) \le \theta$, not $s(y) < \theta$. A skipped document with $s(y) = \theta$ is still correctly left out, because all heap entries have smaller docids and win the tie. This needs the docid order of (C2); a method that scored documents out of docid order would need the strict test $s(y) < \theta$ to skip.
