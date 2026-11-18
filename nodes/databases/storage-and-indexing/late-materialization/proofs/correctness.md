---
title: Late materialization returns the same records, in the same order, as early materialization, and reads the number of values given on the page
proves: [correctness]
status: full
---

We use the notation of the page. A table has columns of length $N$; record $i$ is the $i$-th value of every column. A query has predicates $p_1, \ldots, p_m$, each of the form $c \mathbin{\theta} v$ on one column $c$, and output columns $o_1, \ldots, o_r$. A predicate holds on record $i$ only if the value is not NULL and the comparison is true. Let $Q$ be the sorted list of the records on which every predicate holds.

**Lemma 1.** After iteration $m'$ of the loop at lines L2 and L3, $P$ is the sorted list of the records on which $p_1, \ldots, p_{m'}$ all hold.

*Proof.* By induction on $m'$. Before the loop, line L1 sets $P$ to all records in order, which is the claim for $m' = 0$. Line L3 keeps, in their order, exactly the records of $P$ on which $p_{m'}$ holds. A sublist of a sorted list is sorted, and a record is kept if and only if it satisfies $p_1, \ldots, p_{m'-1}$ (by induction) and $p_{m'}$. $\square$

**Theorem 1.** LATE returns the list $(o_1[i], \ldots, o_r[i])$ for $i \in Q$, in increasing order of $i$. EARLY returns the same list. So both compute, as a bag, the projection on $o_1, \ldots, o_r$ of the selection of the table by $p_1 \wedge \ldots \wedge p_m$.

*Proof.* By Lemma 1 with $m' = m$, $P = Q$ after the loop. Lines L4 and L5 build, for each output column, the list of its values at the positions of $Q$, in the order of $Q$. Line L6 takes the $x$-th entry of each list, which are values of the same record $Q[x]$. EARLY visits the records in increasing order (line L7), reads the values of record $i$ from every column the query uses (line L8), and outputs the projection exactly when every predicate holds (line L9), that is, for $i \in Q$ in increasing order. The two lists are equal, and each record of the selection appears once in each, which is the bag semantics of selection and projection. $\square$

The order of the predicates does not change $Q$, since a conjunction does not depend on the order of its terms, so any order gives the same result.

**Theorem 2 (values read).** Let $P_{m'}$ be the list after iteration $m'$, so $|P_0| = N$ and $P_m = Q$. LATE reads

$$\sum_{m'=1}^{m} |P_{m'-1}| + r \lvert Q \rvert$$

values, EARLY reads $N u$ values, where $u$ is the number of distinct columns among the predicates and the outputs, and the bitmap variant reads $N m + r \lvert Q \rvert$.

*Proof.* Iteration $m'$ of line L3 reads column $c$ of predicate $p_{m'}$ once at each position of $P_{m'-1}$. Lines L4 and L5 read each output column at each position of $Q$. EARLY reads, for each of the $N$ records, one value of each of the $u$ columns. The bitmap variant scans each predicate column completely and then reads the outputs at $Q$. $\square$

Since $|P_{m'}|$ does not increase with $m'$, LATE reads at most $N m + r \lvert Q \rvert$ values, the cost of the bitmap variant. For two predicates the cost is $N + |P_1| + r \lvert Q \rvert$, so the predicate that keeps fewer records should come first. For more predicates the best order also depends on how the predicates are correlated, and the most selective one first is a heuristic. When $m = 1$ and the output columns differ from the predicate column, LATE reads $N + r \lvert Q \rvert$ against $N(1 + r)$ for EARLY, so it wins whenever $\lvert Q \rvert < N$. It can read more than EARLY when an output column is also a predicate column and most records qualify, because it then reads that column twice.
