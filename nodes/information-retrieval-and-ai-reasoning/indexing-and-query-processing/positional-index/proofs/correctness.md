---
title: The positional index stores, for each term, exactly its documents and its positions, in order
proves: [correctness]
status: full
---

The collection is a sequence of documents $d_1 < d_2 < \cdots < d_N$ added in this order, and document $d$ is the token sequence $t^d_0, \ldots, t^d_{L_d - 1}$. For a term $w$, let $D(w) = (d : w \text{ occurs in } d)$ in increasing order, and for a document $d$ let $\mathrm{Pos}(w, d) = (i : t^d_i = w)$ in increasing order. The index stores, for each term $w$ that it has seen, an array $ids(w)$ and an array $pos(w)$ of the same length.

**Invariant (P).** After the first $j$ documents are added, for every term $w$: $ids(w)$ is $D(w)$ restricted to $d_1, \ldots, d_j$, and $pos(w)[p] = \mathrm{Pos}(w, ids(w)[p])$ for each index $p$. A term with no occurrence in these documents has no entry.

**Lemma 1.** ADD-DOCUMENT keeps (P), and it raises an error, with no change to the lists, if the new id is not greater than the last one.

*Proof.* Line L1 checks the order before any change. Let $d = d_{j+1}$ be greater than every id added before, and let (P) hold for the first $j$ documents. We show by induction on $i$ that after the token $t^d_i$ is handled, for every term $w$:

- if $w$ occurs in $t^d_0, \ldots, t^d_i$, then $ids(w)$ is $D(w)$ restricted to $d_1, \ldots, d_j$, followed by $d$, and the last entry of $pos(w)$ is $(i' \le i : t^d_{i'} = w)$;
- else $ids(w)$ and $pos(w)$ are as before the call.

Before the first token, the second case holds for every term. Let $w = t^d_i$. Line L3 finds or creates the lists of $w$. If $w$ did not occur in $t^d_0, \ldots, t^d_{i-1}$, then the last id of $ids(w)$, if there is one, is an earlier document, so it is less than $d$ and not equal to it. Line L4 appends $d$ with an empty position list, and line L5 appends $i$, which gives the list $(i)$. If $w$ did occur, the last id is $d$, line L4 does nothing, and line L5 appends $i$ to the last position list. Since $i$ is greater than every position of that list, the list stays increasing and equals $(i' \le i : t^d_{i'} = w)$. Other terms do not change.

After the last token, every term of $d$ has $d$ appended once, at the end, with the full position list $\mathrm{Pos}(w, d)$. Since $d$ is greater than every earlier id, $ids(w)$ stays strictly increasing and is $D(w)$ restricted to $d_1, \ldots, d_{j+1}$. Terms that do not occur in $d$ do not change. So (P) holds for $j + 1$ documents. $\square$

**Lemma 2.** POSITIONS$(w, d)$ returns $\mathrm{Pos}(w, d)$, which is the empty list when $w$ does not occur in $d$.

*Proof.* If $w$ has no entry, then by (P) it occurs in no document, and line L6 returns the empty list. Else line L7 finds the least index $p$ with $p = |ids(w)|$ or $ids(w)[p] \ge d$, by binary search on the strictly increasing array $ids(w)$. If $ids(w)[p] = d$, then $d \in D(w)$, and by (P) line L8 returns $\mathrm{Pos}(w, d)$. Else $d$ is not in $ids(w)$, because every id before index $p$ is less than $d$ and every id from $p$ on is greater, so $w$ does not occur in $d$ and line L9 returns the empty list. $\square$

**Theorem.** After the documents $d_1 < \cdots < d_N$ are added, POSTINGS$(w) = D(w)$, POSITIONS$(w, d) = \mathrm{Pos}(w, d)$, $\mathrm{df}(w) = |D(w)|$, $\mathrm{tf}(w, d) = |\mathrm{Pos}(w, d)|$ and $\mathrm{cf}(w) = \sum_d |\mathrm{Pos}(w, d)|$.

*Proof.* (P) holds with no documents, because no term has an entry. By Lemma 1 and induction on $j$, it holds after all $N$ documents. The claims on POSTINGS and on the counts follow from (P), and the claim on POSITIONS is Lemma 2. $\blacksquare$

**Space.** Each token $t^d_i$ adds exactly one position, at line L5, and each pair of a term and a document that holds it adds exactly one id, at line L4. With $T = \sum_d L_d$ tokens, the index holds $T$ positions and at most $T$ ids, plus one dictionary entry for each distinct term, at most $T$ of them. So the space is $\Theta(T)$ words for a collection with $T \ge 1$.

**Time.** Line L3 is one lookup in a hash table, $O(1)$ expected, and lines L4 and L5 are $O(1)$ amortized appends. So ADD-DOCUMENT costs $O(L_d)$ expected, and the whole build costs $O(T)$ expected. POSITIONS makes $O(\log |D(w)|)$ comparisons in line L7 and copies $|\mathrm{Pos}(w, d)|$ positions. $\blacksquare$
