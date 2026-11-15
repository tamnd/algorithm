---
title: TAAT and its max_score variant return the exact top k
proves: [correctness]
status: full
---

The rank order $\prec$ is score descending, then docid ascending. For a finite set $S$ of (docid, score) pairs, $\mathrm{top}_k(S)$ is the first $\min(k, |S|)$ pairs of $S$ in this order. Let $M$ be the set of matching documents and $s(x)$ the score of $x$. The weights are exact numbers and at least 0.

**Lemma 1 (plain TAAT).** After the iteration $i$ of line L2, the map $A$ has an entry for $x$ if and only if one of the lists $1, \ldots, i$ contains $x$, and then $A[x]$ is the sum of the weights of terms $1, \ldots, i$ in $x$.

*Proof.* By induction on $i$. For $i = 0$ the map is empty and every sum is empty. In iteration $i$, line L3 visits each posting $(x, w)$ of list $i$ once, since the list has distinct docids. Line L4 adds $w$ to the old entry or creates the entry with $w$. Entries of documents not in list $i$ do not change. $\square$

**Theorem 1.** TAAT$(q, k)$ returns $\mathrm{top}_k(\{(x, s(x)) : x \in M\})$ in the order $\prec$.

*Proof.* By Lemma 1 with $i = m$, the entries of $A$ are exactly the pairs $(x, s(x))$ for $x \in M$. Line L5 selects the first $k$ of them by $\prec$. $\square$

**Lemma 2 (the max_score variant before the switch).** While or_mode is true at the start of iteration $i$, the map $A$ is as in Lemma 1 for the terms $1, \ldots, i-1$ in the order of line M1.

*Proof.* Line M5 is line L4. $\square$

**Lemma 3.** Let the switch happen in line M4 of iteration $i$, and let $R = U_i + \cdots + U_m$. Every document $x$ with no entry in $A$ at that time has $s(x) \le R$. At least $k$ documents have a final score greater than $R$.

*Proof.* By Lemma 2, $x$ has no entry exactly when none of the lists $1, \ldots, i-1$ contains $x$. So $s(x)$ is a sum of weights of terms in $\{i, \ldots, m\}$, and each weight of term $j$ is at most $U_j$, the largest weight of its list. Weights are at least 0, so $s(x) \le U_i + \cdots + U_m = R$. At the switch, $|A| \ge k$ and the $k$-th largest value in $A$ is greater than $R$, so at least $k$ entries are greater than $R$. Each entry is a partial sum of the final score of its document, and the remaining weights are at least 0, so these $k$ documents end with scores greater than $R$. $\square$

**Lemma 4.** After the switch no entry is created, and each entry that exists at the switch ends with the exact score of its document.

*Proof.* Line M6 only updates entries. For an entry $x$ and a later list $j$, line M6 finds $x$ in list $j$ if and only if list $j$ contains $x$, since the forward search looks for $x$ among the postings at or after the last position, and the docids of $A$ are visited in increasing order, so no posting of $x$ is passed. It then adds the weight of term $j$ in $x$. With Lemma 2, at the end $A[x]$ is the sum over all $m$ terms. $\square$

**Theorem 2.** TAAT-MAXSCORE$(q, k)$ returns $\mathrm{top}_k(\{(x, s(x)) : x \in M\})$ in the order $\prec$.

*Proof.* If there is no switch, the method is plain TAAT on a reordered query, and Theorem 1 applies, since the sum does not depend on the order of exact additions. Else let $E$ be the set of documents with an entry at the switch. By Lemma 4, the final map is $\{(x, s(x)) : x \in E\}$. Take $y \in M \setminus E$. By Lemma 3, $s(y) \le R$, and there are $k$ documents in $E$ with scores greater than $R$, so greater than $s(y)$. Each of them ranks before $y$ by $\prec$, whatever the docids, so $y$ is not in $\mathrm{top}_k(M)$. So $\mathrm{top}_k(M) = \mathrm{top}_k(E)$, which line M7 returns. $\blacksquare$

**Remark 1 (strictness).** Lemma 3 needs the $k$-th accumulator strictly greater than $R$. If it were only equal to $R$, a document $y$ without an entry could end with $s(y) = R$ and a docid smaller than that of the $k$-th document, and $y$ would rank before it.

**Remark 2 (floating point).** The variant adds the weights in the order of line M1, not in query order. With floating-point weights its sums can differ from those of an exhaustive scan in the last bit, so the scores agree only to a tolerance, and a near tie can break the other way. Lemma 3 also needs the computed sum $R$ to be at least every computed partial score that it bounds; this holds with exact arithmetic and is the reason the tests use integers and fractions.
