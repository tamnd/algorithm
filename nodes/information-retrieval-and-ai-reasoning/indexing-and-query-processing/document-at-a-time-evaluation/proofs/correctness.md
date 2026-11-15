---
title: DAAT returns the exact top k under the tie rule
proves: [correctness]
status: full
---

Write $\prec$ for the rank order of this area: $(s, d) \prec (s', d')$, read "ranks before", if $s > s'$, or $s = s'$ and $d < d'$. It is a strict total order on pairs with distinct docids. For a finite set $S$ of pairs, $\mathrm{top}_k(S)$ is the set of the first $\min(k, |S|)$ pairs of $S$ in this order. The weights are exact numbers (integers, fractions or reals); the remark at the end covers floating point.

**Lemma 1 (the heap rule).** Let $S$ be a set of pairs whose docids are all less than $d$, and let $H = \mathrm{top}_k(S)$. Offer $(s, d)$ by line L8. Then the new heap is $\mathrm{top}_k(S \cup \{(s, d)\})$.

*Proof.* If $|H| < k$, then $|S| = |H| < k$, so $|S \cup \{(s,d)\}| \le k$ and its top $k$ is all of it, which is $H$ plus the new pair. Line L8 inserts the pair.

Else $|H| = k$. Let $(s_0, d_0)$ be the last pair of $H$ in the order $\prec$; it has the least score in $H$ and, among pairs of that score, the largest docid, which is how the heap orders its entries. Since $d > d_0$, the new pair ranks before $(s_0, d_0)$ if and only if $s > s_0$. If $s > s_0$, then the new pair ranks before $(s_0, d_0)$, and every pair of $S \setminus H$ ranks after $(s_0, d_0)$, so the first $k$ pairs of $S \cup \{(s,d)\}$ are $H \setminus \{(s_0, d_0)\}$ plus $(s, d)$. Line L8 makes exactly this replacement. If $s \le s_0$, then $(s, d)$ ranks after $(s_0, d_0)$, so $H$ is still the top $k$, and line L8 leaves $H$ unchanged. $\square$

**Invariant.** Let $M$ be the set of matching documents, and for each document $x$ let $s(x)$ be its score. Before each test of line L4:

> **(D1)** Each cursor $c_i$ is at the first posting of list $i$ whose docid is at least $d$, and $d = \min_i c_i.\mathit{docid}$.
>
> **(D2)** $H = \mathrm{top}_k(\{(s(x), x) : x \in M, x < d\})$.

*Initialization.* Line L1 puts each cursor at the start of its list, so (D1) holds with $d$ from line L3. No document is less than the least docid of all lists, so the set in (D2) is empty, and $H$ is empty.

*Maintenance.* Assume (D1) and (D2) and $d < \infty$. In lines L6 and L7, a list $i$ contains $d$ if and only if its cursor is at $d$, by (D1): the cursor is at the first posting with docid at least $d$, and that posting has docid $d$ exactly when the list contains $d$. So line L7 adds the weight of each query term that $d$ contains and no other weight, and $s = s(d)$ after the loop. The document $d$ matches, since some cursor is at $d$. Line L7 moves each cursor at $d$ one step, so after line L6 each cursor is at the first posting with docid greater than $d$. Let $d'$ be the value from line L9. No list has a posting with docid strictly between $d$ and $d'$, so no document strictly between them matches. By Lemma 1, after line L8, $H = \mathrm{top}_k(\{(s(x), x) : x \in M, x \le d\})$, which is the set of (D2) for $d'$. Each cursor is at the first posting with docid greater than $d$, which is the first with docid at least $d'$, so (D1) holds for $d'$.

*Termination.* Each iteration moves at least one cursor one step, and there are $T$ postings, so the loop runs at most $T$ times.

**Theorem.** DAAT$(q, k)$ returns $\mathrm{top}_k(\{(s(x), x) : x \in M\})$ in the order $\prec$: the exact top $k$ with the tie rule of score descending, then docid ascending.

*Proof.* At the end $d = \infty$, so by (D2) $H$ is the top $k$ of all matching documents. Line L10 sorts it by $\prec$. $\blacksquare$

**Remark (floating point).** With floating-point weights the theorem holds for the scores computed in query order, which is the order of line L7 and of the exhaustive reference scan. The two methods then compute the same sums, bit for bit, and so return the same ranking. A method that adds the same weights in another order can get a sum that differs in the last bit, and then a near tie can break the other way.
