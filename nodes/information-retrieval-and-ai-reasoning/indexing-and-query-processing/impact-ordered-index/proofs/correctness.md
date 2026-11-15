---
title: Score-at-a-time evaluation is exact without a stop and order-exact with the safe stop
proves: [correctness]
status: full
---

All statements are about the impact scores: $s(x)$ is the sum of the impacts of the query terms in $x$, and $M$ is the set of documents that contain a query term. Whether the impact ranking agrees with a ranking by real weights depends on the quantizer and is not claimed here. The rank order $\prec$ is score descending, then docid ascending, and $\mathrm{top}_k(S)$ is the first $\min(k, |S|)$ pairs of a set $S$ in this order. The impacts are positive integers, so all sums are exact.

**Lemma 1 (partial sums).** After any number of segments of $G$ have been read in full, $A[x]$ exists if and only if a read segment contains $x$, and then $A[x]$ is the sum of the impacts of the read segments that contain $x$. Each term contributes at most one read segment to this sum.

*Proof.* Line L6 adds $a$ once for each docid of a read segment. The segments of one term are disjoint, so $x$ is in at most one segment of each term, and that segment carries the impact of the term in $x$. $\square$

**Theorem 1 (stop none).** SAAT$(q, k, \mathit{none})$ returns $\mathrm{top}_k(\{(x, s(x)) : x \in M\})$ in the order $\prec$.

*Proof.* All segments of the query terms are read. By Lemma 1, $A$ maps each $x \in M$ to the sum of the impacts of all query terms in $x$, which is $s(x)$, and has no other entries. Line L7 selects the top $k$ by $\prec$. $\square$

**Lemma 2 (the remaining gain).** At the test of line L4, let $r$ be the sum, over the query terms, of the impact of the next unread segment of the term, or 0 if the term has none left. Then each document $x$ has $A[x] \le s(x) \le A[x] + r$, with $A[x] = 0$ if $x$ has no entry.

*Proof.* The lower bound is Lemma 1, since impacts are positive. For the upper bound, the impacts of $x$ that are not yet added come from unread segments, at most one for each term. The segments of a term come in decreasing order of impact, and $G$ reads the segments of each term in this order, so each unread segment of a term has an impact at most the impact of its next unread segment. Summing over the terms gives at most $r$. $\square$

**Theorem 2 (stop safe).** Let SAAT$(q, k, \mathit{safe})$ return the list $(x_1, b_1), \ldots, (x_j, b_j)$, and let SAAT$(q, k, \mathit{none})$ return $(y_1, s_1), \ldots, (y_{j'}, s_{j'})$. Then $j = j'$, $x_i = y_i$ for each $i$, and $b_i \le s(x_i) = s_i$.

*Proof.* If line L4 never breaks, the run is the run of stop none, and Theorem 1 applies with $b_i = s_i$.

Otherwise let the break happen with the accumulators $A$ and gain $r$. The test needs $|A| \ge k$, so $j = k$; also $|M| \ge |A| \ge k$, so $j' = k$. Let $a_1 \ge \cdots \ge a_k$ be the $k$ best accumulators, by $\prec$, of the documents $x_1, \ldots, x_k$, and let $a_{k+1}$ be the next one, or 0. The test says $a_i > a_{i+1} + r$ for $i < k$ and $a_k > \max(a_{k+1}, 0) + r$.

For $i < k$, Lemma 2 gives $s(x_i) \ge a_i > a_{i+1} + r \ge s(x_{i+1})$. So $s(x_1) > s(x_2) > \cdots > s(x_k)$.

Let $z$ be any other document of $M$. Either it has an entry, which is at most $a_{k+1}$, or it has none, and then its entry is taken as 0. In both cases $s(z) \le \max(a_{k+1}, 0) + r < a_k \le s(x_k)$.

So $x_1, \ldots, x_k$ are the $k$ documents of highest true score, all with distinct scores, and every other document has a strictly lower score. The tie rule is never needed, and $\mathrm{top}_k(M)$ is $x_1, \ldots, x_k$ in this order, which is the output of stop none by Theorem 1. The returned scores are $b_i = a_i \le s(x_i)$ by Lemma 2. $\blacksquare$

**Proposition 3 (stop budget).** Each pair $(x, b)$ returned by SAAT$(q, k, \mathit{budget})$ has $b \le s(x)$, and with a budget of at least the total length $T$ of the query lists, the output equals that of stop none.

*Proof.* The accumulators are partial sums of the read postings, so $b \le s(x)$ as in Lemma 2. A budget of at least $T$ never breaks the loop, so the run is that of stop none. $\square$

No more is claimed for the budget stop. With a smaller budget the returned set can differ from the true top $k$, as the toy example on the page shows.

**Remark (strictness).** Theorem 2 needs strict gaps. With $a_k = a_{k+1} + r$, the document $z$ of $a_{k+1}$ could end with $s(z) = s(x_k)$ and a smaller docid, and it would then rank before $x_k$.

**Remark (real weights).** With real weights in place of integer impacts, Lemma 2 still holds in exact arithmetic. In floating point, the sums $A[x]$ are added in impact order, not in query order, so they can differ in the last bit from the scores of a docid-ordered scan.
