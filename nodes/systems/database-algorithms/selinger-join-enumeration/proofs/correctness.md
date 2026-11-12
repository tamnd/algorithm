---
title: The System R dynamic program finds the cheapest left-deep plan
proves: [correctness]
status: full
---

**Setting.** The relations are $R_1, \ldots, R_n$. Each $R_i$ has a set $\mathrm{cols}(R_i)$ of join column classes, and its access paths produce either no order or an order on a class of $\mathrm{cols}(R_i)$. A join step takes a plan $P$ for a set $L$, with output order $o$, and a relation $R_j \notin L$, and uses a method $m$. Its added cost $g(L, o, j, m)$ and its output order $h(o, m)$ are given by the cost model, with these properties, which hold for the methods of the page:

- (P1) $g$ depends on $o$ only through the test $o = k$ for the class $k$ of a merge join, and $k$ is then a class shared by $R_j$ and some relation of $L$.
- (P2) $h(o, m)$ is $o$ (nested loop and index nested loop), none (hash join) or the class $k$ of a merge join.
- (P3) The size of a result depends only on its set of relations, so a plan's cost is the cost of its left input plus $g$.

A left-deep plan of a set $S$ is an access path of one relation followed by join steps that add the other relations of $S$ one at a time; if cross products are off, each step must share a class between $R_j$ and the set already joined. The *interesting orders* of $S$ are $I(S) = \{k : k \in \mathrm{cols}(R_a) \cap \mathrm{cols}(R_b),\ R_a \in S,\ R_b \notin S\}$, plus the required order $r$ if the query has one. The *label* of a plan $P$ of $S$ with output order $o$ is $\lambda(P) = o$ if $o \in I(S)$ and none otherwise. Line A1 stores each plan under its label.

**Lemma 1.** Every order produced by a plan of $L$ is a class of some relation of $L$. If a plan $P$ of $L$ has an order $o \notin I(L)$, then for every $R_j \notin L$, the order $o$ is not in $I(L \cup \{R_j\})$, and $o \ne r$.

*Proof.* Access paths order on a class of their own relation, and a merge join orders on a class shared with a relation of $L$; nested loops keep the order of their input. So $o$ is a class of some relation of $L$. If $o \notin I(L)$, then $o \ne r$ and no relation outside $L$ has the class $o$. In particular $R_j$ does not have it, so no relation outside $L \cup \{R_j\}$ has it and no relation of $L \cup \{R_j\}$ meets one outside with it. So $o \notin I(L \cup \{R_j\})$. $\square$

**Lemma 2 (labels are enough).** Let $P$ and $P'$ be plans of the same set $L$ with the same label. Then every join step $(R_j, m)$ adds the same cost to both, and the two results have the same label. The cost of a final sort is the same for both.

*Proof.* If the orders are equal, there is nothing to prove. Otherwise both orders are outside $I(L)$ or one is none, so the common label is none. By (P1), $g$ can differ only for a merge join on a class $k$ that $R_j$ shares with $L$; then $k \in I(L)$ because $R_j \notin L$, so neither order equals $k$ and both pay the same. By (P2), the output orders are equal, or both are the inputs' orders; in the second case, by Lemma 1, neither is in $I(L \cup \{R_j\})$ (a none order has label none trivially), so both labels are none. The final sort is needed when the order is not $r$; since $r \in I(S)$ for every $S$ by definition, the test $o = r$ has the same answer for both plans. $\square$

**Theorem.** After the iteration of line L2 for the size $s$, for every set $S$ with $|S| \le s$ and every label $\ell$, the entry $\mathrm{best}[S, \ell]$ (if any) is a left-deep plan of $S$ with label $\ell$, and no left-deep plan of $S$ with label $\ell$ is cheaper. So line L10 returns a cheapest left-deep plan for all $n$ relations, including the cost of a final sort.

*Proof.* Each stored plan is built by lines L1 or L9 from an access path or from a stored plan and a valid join step, so it is a left-deep plan of $S$, and line A1 stores it under its label. Line A2 keeps the cheapest one per label. It remains to show that no plan is cheaper.

For $|S| = 1$, line L1 tries every access path of the relation. Assume the claim for all sets of size less than $s$, and let $Q$ be a left-deep plan of $S$, $|S| = s$, with label $\ell$. Its last step joins a plan $P$ of $L = S - \{R_j\}$ with $R_j$ by a method $m$; if cross products are off, $R_j$ shares a class with $L$, so line L6 does not skip $R_j$. Let $\ell'$ be the label of $P$. By the induction hypothesis, $\mathrm{best}[L, \ell']$ exists and costs at most as much as $P$. By Lemma 2 and (P3), joining it with $R_j$ by $m$ costs at most $\mathrm{cost}(Q)$ and gives a plan with label $\ell$. Lines L7 to L9 try exactly this step, so line A2 stores under $\ell$ a plan that costs at most $\mathrm{cost}(Q)$.

For line L10, take a cheapest complete plan $Q$, with the final sort if its order is not $r$. Its label is some $\ell$, and $\mathrm{best}[\{R_1, \ldots, R_n\}, \ell]$ costs at most as much; by Lemma 2 it needs a final sort exactly when $Q$ does. So the cheapest value that line L10 computes is at most $\mathrm{cost}(Q)$, and it is the cost of a real plan. $\blacksquare$

**Remark.** Without labels (one plan per set), Lemma 2 fails: a plan in a useful order can lose to a cheaper unordered plan for the same set and then be missing when a merge join or the final ORDER BY needs it. The example on the page shows a factor of almost 2.
