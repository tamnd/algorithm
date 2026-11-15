---
title: MaxScore returns the exact top k under the tie rule
proves: [correctness]
status: full
---

The rank order $\prec$ is score descending, then docid ascending, and $\mathrm{top}_k(S)$ is the first $\min(k, |S|)$ pairs of a set $S$ in this order. Let $M$ be the set of matching documents and $s(x)$ the score of $x$. A pass is one run of lines L5 to L12, or L5 to L10 when line L10 stops it. The candidate of a pass is the $d$ of line L6. The cursors are numbered in the order of line L1, so $P_i$ is the bound sum of cursors $1, \ldots, i$.

**The three conditions.**

> **(C1)** Each weight is at least 0, $U_i$ is at least every weight of list $i$, and the sums are computed exactly, or in an arithmetic in which a sum of numbers each at most its partner is at most the sum of the partners.
>
> **(C2)** The heap replaces its least entry only on a strictly greater score, and documents are offered in increasing docid order.
>
> **(C3)** Each document left out has a score of at most the current threshold $\theta$.

(C1) is an assumption; (C2) and (C3) are proved below.

**Lemma 1 (the split).** The value $e$ never decreases. After line L5 of each pass, $e \ge 1$ implies that the heap is full and $P_e \le \theta$.

*Proof.* Line L5 only increases $e$, and only when the heap is full and $P_{e+1} \le \theta$. Once the heap is full it stays full, and $\theta$ never decreases, so $P_e \le \theta$ stays true. $\square$

**Lemma 2 (the cursors).** Let $d^-$ be the candidate of the previous pass, or $-\infty$ before the first pass. At the start of each pass:

> **(M1)** each cursor $e+1, \ldots, m$ is at the first posting of its list with docid greater than $d^-$;
>
> **(M2)** each cursor $1, \ldots, e$ is at a posting with docid at most the first docid of its list that is greater than $d^-$.

*Proof.* At the start every cursor is at the first posting of its list, so (M1) and (M2) hold. Assume them at the start of a pass with candidate $d$. Line L5 moves some cursors from the essential to the nonessential group, and (M1) for a cursor implies (M2) for it, so both still hold. By (M1), each essential cursor is at a docid greater than $d^-$, and $d$ is the least of them, so $d > d^-$. Line L8 moves each essential cursor at $d$ to the next posting, which is the first posting greater than $d$. The other essential cursors are already at docids greater than $d$, and since they were at the first posting greater than $d^-$ and $d > d^-$, they are at the first posting greater than $d$. So (M1) holds with $d$ in place of $d^-$. A nonessential cursor is either left alone, and then by (M2) it is at most the first docid greater than $d^-$, which is at most the first docid greater than $d$; or line L11 moves it to the first docid at least $d$, which is at most the first docid greater than $d$. In both cases (M2) holds with $d$. $\square$

**Lemma 3 (candidates and their scores).** The candidates are strictly increasing. Each candidate $d$ that reaches line L12 is offered with $s = s(d)$.

*Proof.* The order is the step $d > d^-$ in the proof of Lemma 2. For the score: by (M1), an essential list contains $d$ if and only if its cursor is at $d$, so line L8 adds the weights of exactly the essential terms that $d$ contains. For a nonessential cursor $i$, (M2) says that it has not passed any docid greater than $d^-$, and $d > d^-$, so line L11 finds $d$ if and only if list $i$ contains $d$. If line L10 never stops, every nonessential term is probed, and $s = s(d)$. $\square$

**Lemma 4 (documents left out).** If a matching document $y$ is never offered, then at some time the heap holds $k$ documents, each with a score at least $s(y)$ and a docid less than $y$.

*Proof.* There are two cases.

Case A: $y$ is a candidate, and line L10 stops it at index $i$. At that time $s$ is the sum of the weights in $y$ of the essential terms and of the nonessential terms $i+1, \ldots, e$, by Lemma 3. The terms $1, \ldots, i$ contribute at most $U_1 + \cdots + U_i = P_i$ by (C1). So $s(y) \le s + P_i \le \theta$. Since $i \le e$ and $e \ge 1$, the heap is full by Lemma 1.

Case B: $y$ is never a candidate. Take the first pass whose candidate $d$ is greater than $y$, or, if there is none, the pass that ends in line L7 with $d = \infty$. Let $d^-$ be the candidate before it; then $d^- < y$, since the candidates are increasing, none of them is $y$, and $d$ is the first one above $y$. Suppose an essential list of this pass contains $y$. By (M1) its cursor is at the first posting greater than $d^-$, which is at most $y$, so $d \le y$, which is false. So $y$ is only in the lists $1, \ldots, e$ of this pass, and $s(y) \le P_e \le \theta$ by (C1) and Lemma 1. Since $y$ matches, $e \ge 1$, so the heap is full.

In both cases the heap is full and each entry has a score at least $\theta \ge s(y)$. Each entry was offered in an earlier pass, so its docid is an earlier candidate, which is less than $y$ in case A by Lemma 3 and at most $d^- < y$ in case B. $\square$

**Theorem.** Under (C1), MAXSCORE$(q, k)$ returns $\mathrm{top}_k(\{(x, s(x)) : x \in M\})$ in the order $\prec$.

*Proof.* Let $S$ be the set of offered documents with their scores. By Lemma 3 they are offered in increasing docid order with exact scores, so by Lemma 1 of the DAAT proof, the heap rule, the final heap is $\mathrm{top}_k(S)$. By Lemma 4 each $y \in M \setminus S$ ranks after $k$ members of $S$, so $\mathrm{top}_k(M) = \mathrm{top}_k(S)$. Line L7 returns it in the order $\prec$. $\blacksquare$

**Termination.** In each pass the essential cursor at $d$ moves one posting in line L8, so there are at most $T$ passes. Line L5 and the loop of line L9 do at most $m$ steps each.

**Remark (ties).** Both line L5 and line L10 use $\le \theta$. A document left out with score exactly $\theta$ ranks after the $k$ heap entries, because they have smaller docids. This needs the increasing order of the candidates and the strict replacement in the heap.

**Remark (floating point).** Line L10 compares $s + P_i$, a sum in one order, with $\theta$, a score summed in another order. With floating-point weights the bound can come out a little below the true score, and a document of the top $k$ can be dropped. With integer or fraction weights, as in the tests, this cannot happen.
