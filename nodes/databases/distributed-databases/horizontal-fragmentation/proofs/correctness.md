---
title: Minterm fragments are complete and disjoint, also with NULLs, and derived fragments follow their owner
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode on the page. A relation $R$ is a bag: each row has a count. A simple predicate $p$ maps each row to TRUE, FALSE or UNKNOWN, as in SQL, where a comparison with NULL is UNKNOWN. For a list $p_1, \dots, p_k$ and a sign vector $m \in \{+, -\}^k$, the minterm $m$ holds on a row $t$ when, for each $i$, $p_i(t)$ is TRUE if $m_i = +$ and $p_i(t)$ is not TRUE (FALSE or UNKNOWN) if $m_i = -$. Line L2 sets $R_m = \sigma_m(R)$, with the counts of $R$.

**Theorem 1.** The minterm fragments of lines L1 to L3 are disjoint, complete, and their bag union (line L6) is $R$, with the same count for every row.

*Proof.* For a row $t$, define $m(t)$ by $m(t)_i = +$ exactly when $p_i(t)$ is TRUE. Then $t$ satisfies $m(t)$. If $t$ satisfies a minterm $m$, then for each $i$, $m_i = +$ exactly when $p_i(t)$ is TRUE, so $m = m(t)$. So every row satisfies exactly one minterm: it is in exactly one fragment (disjointness) and in at least one (completeness). Each fragment keeps the count of each of its rows, so the bag union has the count of $R$ for each row. Line L3 drops only empty fragments, which add nothing to the union. $\square$

**The form with NOT.** If the minterm uses $\lnot p_i$ for $m_i = -$, with the SQL rule that $\lnot$ UNKNOWN is UNKNOWN and that a selection keeps only TRUE rows, then a row $t$ with $p_i(t)$ UNKNOWN for some $i$ satisfies no minterm. The fragments are still disjoint, but their union is $\sigma_{\text{no } p_i \text{ is UNKNOWN}}(R)$, a proper sub-bag of $R$ whenever such a row exists. The two forms agree when no predicate can be UNKNOWN on the data, for example when the attributes they use are declared NOT NULL.

**Derived fragments.** Let $S$ be a member relation and $R$ its owner, with common attributes $J$, and let $R_m$ be fragments of $R$. Line L5 sets $S_m = S \ltimes R_m$: the rows of $S$, with their counts, that agree on $J$ with some row of $R_m$ and have no NULL in $J$.

**Theorem 2.** Let the fragments $R_m$ of the owner be complete and disjoint.

1. A row of $S$ is in some $S_m$ exactly when it joins with some row of $R$. So the derived fragments are complete exactly when $S \ltimes R = S$, which holds when every row of $S$ has a non-null value of $J$ that appears in $R$ (referential integrity from $S$ to $R$).
2. If $J$ is a key of $R$, the derived fragments are disjoint.
3. Under both conditions, the bag union of the $S_m$ is $S$.

*Proof.* (1) A row $s$ of $S$ is in $S_m$ when it joins with a row of $R_m$. Every row of $R$ is in some $R_m$ and every row of an $R_m$ is in $R$, so $s$ is in some $S_m$ exactly when it joins with a row of $R$. (2) If $J$ is a key of $R$, then a row $s$ joins with at most one row $r$ of $R$, the one with $r[J] = s[J]$. That row is in exactly one fragment, so $s$ is in exactly one $S_m$. (3) By (1) and (2) each row of $S$ is in exactly one $S_m$, with its count. $\square$

Both conditions are needed. If a value of $J$ appears in two rows of $R$ that lie in different fragments, a row of $S$ with that value is in both derived fragments, and the bag union counts it twice. If a row of $S$ has a NULL in $J$, or a value that is not in $R$, it is in no fragment. The tests check both failures.

**Reconstruction is a query.** By Theorem 1, $R = \bigcup_m R_m$ with bag union, so any query on $R$ can be answered from the fragments. A query with a selection $\sigma_q$ needs only the fragments whose minterm is consistent with $q$: if $m$ and $q$ cannot both be TRUE on any row, then $\sigma_q(R_m)$ is empty. This is the reason to fragment by the predicates of the workload.
