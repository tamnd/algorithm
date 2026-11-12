---
title: CLIQUE finds every dense unit and describes each cluster exactly
proves: [correctness]
status: full
---

We use the pseudocode of the page. $D$ has $N$ points in the attributes $1, \ldots, d$. Line L1 gives each point one interval index per attribute. A $k$-dimensional unit is a set $u = \{(a_1, i_1), \ldots, (a_k, i_k)\}$ with $a_1 < \cdots < a_k$, written as a tuple in this order; $\mathrm{pts}(u)$ is the set of points whose interval in $a_j$ is $i_j$ for each $j$. The unit is dense if $|\mathrm{pts}(u)| > \tau N$. Let $\mathcal{D}_k$ be the set of all dense $k$-dimensional units.

**Lemma 1 (downward closure).** If $u$ is dense and $\emptyset \ne w \subset u$, then $w$ is dense.

*Proof.* A point of $u$ matches every pair of $u$, so it matches every pair of $w$: $\mathrm{pts}(u) \subseteq \mathrm{pts}(w)$. Hence $|\mathrm{pts}(w)| \ge |\mathrm{pts}(u)| > \tau N$. $\square$

**Lemma 2 (the candidates).** Let $k \ge 2$ and suppose $U_{k-1} = \mathcal{D}_{k-1}$. After lines L4 and L5, $C_k$ is the set of $k$-dimensional units all of whose $(k-1)$-element subsets are in $U_{k-1}$.

*Proof.* ($\subseteq$) Line L4 joins $u = (p_1, \ldots, p_{k-2}, (a, i))$ and $v = (p_1, \ldots, p_{k-2}, (a', i'))$ with $a < a'$. The attributes of $p_1, \ldots, p_{k-2}$ are smaller than $a$ because $u$ is sorted, so $c = (p_1, \ldots, p_{k-2}, (a, i), (a', i'))$ is a $k$-dimensional unit with distinct, sorted attributes. Line L5 removes $c$ unless all its $(k-1)$-subsets are in $U_{k-1}$.

($\supseteq$) Let $c = (q_1, \ldots, q_k)$ be a $k$-dimensional unit whose $(k-1)$-subsets are all in $U_{k-1}$. Then $u = (q_1, \ldots, q_{k-2}, q_{k-1})$ and $v = (q_1, \ldots, q_{k-2}, q_k)$ are in $U_{k-1}$, they agree on the first $k - 2$ pairs, and the attribute of $q_{k-1}$ is smaller than that of $q_k$. So line L4 forms $c$ from $u$ and $v$, and line L5 keeps it. $\square$

**Theorem 1 (all dense units).** For each $k \ge 1$ that the loop reaches, $U_k = \mathcal{D}_k$. The loop stops after at most $d$ iterations, and then $U_1 \cup U_2 \cup \cdots$ is the set of all dense units of all $2^d - 1$ subspaces.

*Proof.* Induction on $k$. Line L2 counts every 1-dimensional unit that holds a point (the others hold none and are not dense), so $U_1 = \mathcal{D}_1$. Suppose $U_{k-1} = \mathcal{D}_{k-1}$. If $c \in \mathcal{D}_k$, all its $(k-1)$-subsets are dense by Lemma 1, so they are in $U_{k-1}$, and $c \in C_k$ by Lemma 2. Line L6 counts each candidate exactly and keeps the dense ones, so $U_k = C_k \cap \mathcal{D}_k = \mathcal{D}_k$.

A unit has at most $d$ pairs, so $\mathcal{D}_{d+1} = \emptyset$ and the loop stops with some $U_{k-1} = \emptyset$, $k \le d + 1$. At that point $\mathcal{D}_{k-1} = \emptyset$, and by Lemma 1 no unit of dimension $k - 1$ or more is dense (each has a dense $(k-1)$-subset otherwise). So the levels found contain every dense unit. $\square$

**Lemma 3 (clusters).** Line L8 returns the connected components of the graph on the dense units of $S$ in which two units are adjacent iff they share a common face.

*Proof.* Two units of $S$ share a face iff they differ in exactly one attribute and their intervals there differ by 1. The search of the implementation starts from each unseen unit, pushes it, and, for each popped unit, pushes each of its at most $2|S|$ face neighbors that is dense and unseen. This is a graph search with an explicit stack, so each component is found exactly once. $\square$

Now fix a cluster $K$, a set of dense units of $S = \{a_1 < \cdots < a_k\}$. A region $R = \prod_j [\ell_j, h_j]$ is the set of units with interval in $[\ell_j, h_j]$ in attribute $a_j$; it *fits* if $R \subseteq K$.

**Lemma 4 (maximal regions).** The region $R$ that line L9 grows from a unit $s \in K$ fits, contains $s$, and is maximal: no region obtained by moving one bound of $R$ out by one interval fits.

*Proof.* The region starts as $\{s\}$, which fits. Each extension is accepted only if the extended region fits, so $R$ fits and contains $s$. Let $R^{(j)}$ be the region just after attribute $a_j$ is done. Attribute $a_j$ stopped growing up at $h_j$ because a region $F$ was refused: $F$ has the range $[s_j, h_j + 1]$ in $a_j$ (with $s_j$ the interval of $s$) and the ranges at that moment in the other attributes. The region $E_j^{\uparrow}$, equal to $R^{(j)}$ with $h_j$ replaced by $h_j + 1$, contains $F$ (the downward growth only lowers $\ell_j$), so some unit $z \in E_j^{\uparrow} \setminus K$. The later steps only widen the ranges of $a_{j+1}, \ldots, a_k$ and leave the range of $a_1, \ldots, a_j$ as it is. So the final $R$ with $h_j$ replaced by $h_j + 1$ contains $E_j^{\uparrow}$, hence $z$, and does not fit. The same argument works for the lower bound $\ell_j$, using the region at the moment the downward growth of $a_j$ stopped, which already has the final $h_j$. $\square$

**Lemma 5 (the cover).** After line L9 the regions cover $K$ exactly. After line L10 they still cover $K$ exactly, and no remaining region is covered by the union of the others.

*Proof.* Each region lies in $K$ by Lemma 4. Line L9 visits every unit of $K$; a unit that is not yet covered starts a region that contains it. So the union is $K$.

Line L10 looks at the regions in increasing order of size and removes a region if all its units lie in the union of the other regions still kept. A removal keeps the union equal to $K$, because the units of the removed region are still covered. Removals only shrink the union of "the others" for every remaining region, so a region that was not covered by the others when it was checked is not covered later either. Hence no remaining region is redundant at the end. $\square$

**Theorem 2 (the descriptions).** For each cluster $K$, the DNF output by line L10 is satisfied by a point iff the point lies in a unit of $K$.

*Proof.* A term $\bigwedge_j (\text{value of } a_j \text{ in the intervals } \ell_j, \ldots, h_j)$ is satisfied iff the point's unit in $S$ lies in the region $\prod_j [\ell_j, h_j]$. The disjunction is satisfied iff the unit lies in the union of the regions, which is $K$ by Lemma 5. $\square$

**Remark (not a minimum cover).** Lemma 5 gives an irredundant cover by maximal regions, not one with the fewest regions; the staircase example on the page needs two regions, and the greedy step first builds three. Finding a cover with the fewest regions is NP-hard in general, so CLIQUE uses this greedy rule.
