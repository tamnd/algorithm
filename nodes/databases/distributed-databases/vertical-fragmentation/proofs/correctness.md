---
title: Vertical fragments that keep a key are joined back to the relation without loss
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode on the page. $R$ is a bag of rows over the attributes $U$, and $K \subseteq U$. The groups $G_1, \dots, G_n$ cover $U \setminus K$. Line L2 sets $F_i = \pi_{K \cup G_i}(R)$, a bag projection that keeps the counts, and lines L3 to L5 compute $F_1 \bowtie \dots \bowtie F_n$ on the common attributes, where a NULL matches nothing, and put the columns back in the order of $U$.

$K$ is a *key of the instance* $R$ if no row has a NULL in $K$ and no two rows, and no two copies of one row, agree on $K$. So $R$ is a set, and the map $t \mapsto t[K]$ is one to one on it.

**Theorem 1.** If the fragmentation is complete ($K \cup G_1 \cup \dots \cup G_n = U$) and $K$ is a key of the instance $R$, the join of the fragments is $R$, with every count equal to 1.

*Proof.* Each $F_i$ has one row $t[K \cup G_i]$ for each row $t$ of $R$, with count 1, because two rows of $R$ that agree on $K$ are equal. Two fragments $F_i$ and $F_j$ have the common attributes $K \cup (G_i \cap G_j)$, which hold $K$.

*Every row of $R$ is in the join.* For a row $t$ of $R$, the rows $t[K \cup G_i]$ agree with each other on all their common attributes, since they come from one row, and their $K$ values have no NULL. So they join, and their join is $t$, because the groups cover $U$.

*No other row is in the join.* A row $u$ of the join comes from rows $f_i \in F_i$ that agree on $K$ and have no NULL there. Each $f_i$ is $t_i[K \cup G_i]$ for a row $t_i$ of $R$, and the $t_i$ agree on $K$, so they are one row $t$. Then $u$ agrees with $t$ on every $G_i$ and on $K$, so $u = t$.

*Counts.* Each fragment row has count 1, and by the two parts above, each row $t$ of $R$ arises from exactly one combination of fragment rows. So $t$ has count 1 in the join, as in $R$. $\square$

The proof uses completeness only to get every attribute back. Disjointness of the groups is not needed for reconstruction; it only saves storage and makes an update touch fewer fragments. When the groups overlap, the shared attribute values agree because they come from one row.

**Without a key the join can add rows.** Let $R(A, B, C) = \{(0, 0, 0), (0, 1, 1)\}$, with fragments $\pi_{A, B}(R)$ and $\pi_{A, C}(R)$. Here $A$ is not a key. The join on $A$ has four rows, $(0, b, c)$ for $b, c \in \{0, 1\}$, so it is a proper superset of $R$. In general every row of $R$ is in the join with at least its count, since the projections keep the counts and the row joins with itself; the join can only add rows or copies. This is the case of a lossy decomposition on the page [lossless-join decomposition](/lossless-join-decomposition/).

**A NULL in $K$ loses the row.** If a row has a NULL in $K$, its pieces never match, so it is missing from the join. A key must therefore be NOT NULL.

**Tuple identifiers.** If $R$ has no key, for example because it is a bag with duplicate rows, give each copy of each row a distinct identifier $tid$. The relation $R'$ over $\{tid\} \cup U$ has the key $tid$, so by Theorem 1 the fragments of $R'$ join back to $R'$, and $\pi_U(R')$ with bag projection is $R$ again. The tests check Theorem 1, the lossy case, the NULL case and the identifiers on random relations.
