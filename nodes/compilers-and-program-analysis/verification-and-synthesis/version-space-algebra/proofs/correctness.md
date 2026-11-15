---
title: BUILD, INTERSECT and COUNT give exactly the consistent programs and their number
proves: [correctness]
status: full
---

**Setting.** Programs are the trees of the language $E \to x \mid y \mid 1 \mid 2 \mid E + E \mid E - E \mid E \times E$. The size $|P|$ of a program is its number of nodes. Two programs are equal when their trees are equal. The set $R(n)$ represented by a node $n$ is defined by $R(\mathrm{LEAF}(A)) = A$, $R(\mathrm{UNION}(k_1, \ldots, k_r)) = R(k_1) \cup \cdots \cup R(k_r)$ and $R(\mathrm{JOIN}(\mathit{op}, a, b)) = \{ \mathit{op}(p, q) : p \in R(a), q \in R(b) \}$. EMPTY is the union with no kids, so $R(\mathrm{EMPTY}) = \emptyset$. A node is *disjoint* when every union node below it, itself included, has kids with pairwise disjoint sets. Line numbers refer to the pseudocode on the page.

## Lemma 1: the values

**Claim.** After line L6, for each odd $s \le S$, $\mathit{vals}[s] = \{ [\![P]\!](i) : |P| = s \}$, and for each $v$, $\mathit{how}[s][v]$ holds exactly the tuples $(\mathit{op}, s_1, a, b)$ with $s_1 + s_2 = s - 1$, $a \in \mathit{vals}[s_1]$, $b \in \mathit{vals}[s_2]$ and $\mathit{op}(a, b) = v$.

**Proof.** By induction on $s$. For $s = 1$ the programs are the terminals, and line L1 puts each one under its value. For $s \ge 3$, a program of size $s$ is $\mathit{op}(p, q)$ with $|p| + |q| = s - 1$, and its value is $\mathit{op}([\![p]\!](i), [\![q]\!](i))$. By the hypothesis, the values of $p$ and $q$ range exactly over $\mathit{vals}[|p|]$ and $\mathit{vals}[|q|]$, and line L4 tries every split, every pair of values and every operator. So the keys of $\mathit{how}[s]$ are exactly the values of programs of size $s$. $\square$

## Lemma 2: BUILD

**Claim.** For each odd $s \le S$ and each $v \in \mathit{vals}[s]$, NODE$(s, v)$ is not EMPTY, it is disjoint, and
$$R(\mathrm{NODE}(s, v)) = \{ P : |P| = s,\ [\![P]\!](i) = v \}.$$

**Proof.** By induction on $s$. For $s = 1$, line L8 returns the leaf of the terminals with value $v$, and the set is not empty because $v \in \mathit{vals}[1]$.

For $s \ge 3$, take a program $P = \mathit{op}(p, q)$ of size $s$ with value $v$. Let $s_1 = |p|$, $a = [\![p]\!](i)$ and $b = [\![q]\!](i)$. By Lemma 1 the tuple $(\mathit{op}, s_1, a, b)$ is in $\mathit{how}[s][v]$, and by the hypothesis $p \in R(\mathrm{NODE}(s_1, a))$ and $q \in R(\mathrm{NODE}(s - 1 - s_1, b))$. So $P$ is in the set of the join that line L9 builds for this tuple. In the other direction, each join of line L9 holds programs $\mathit{op}(p, q)$ with $|p| = s_1$, $|q| = s - 1 - s_1$, $[\![p]\!](i) = a$ and $[\![q]\!](i) = b$. Such a program has size $s$ and value $\mathit{op}(a, b) = v$. The kids of the join are not EMPTY by the hypothesis, so the join is not EMPTY, and $\mathit{how}[s][v]$ is not empty by Lemma 1.

Disjointness: two different tuples of $\mathit{how}[s][v]$ differ in the operator, in $s_1$, or in $a$ or $b$. Programs from the two joins then differ in the root symbol, in the size of the left subtree, or in the value of one subtree. In each case they are different trees. The kids are disjoint by the hypothesis. $\square$

**Corollary.** BUILD$(i, o, S)$ represents exactly the programs of size at most $S$ with output $o$ on $i$. Line L7 joins the nodes of different sizes, whose sets are disjoint. If no program has output $o$, the union has no kids and BUILD returns EMPTY.

## Lemma 3: INTERSECT

**Claim.** For all nodes $a$ and $b$, $R(\mathrm{INTERSECT}(a, b)) = R(a) \cap R(b)$. If $a$ and $b$ are disjoint, the result is disjoint.

**Proof.** By induction on the sum of the heights of $a$ and $b$ in their DAGs. The memo table returns a result computed earlier for the same pair, so it does not change the result.

- Line L10: one set is empty.
- Line L11: $R(a) \cap R(b) = \bigcup_j (R(k_j) \cap R(b))$, and each $k_j$ is lower than $a$. Each new kid is a subset of $R(k_j)$, so the kids stay pairwise disjoint.
- Line L12: the same with the roles swapped. The new kids are subsets of the pairwise disjoint sets $R(k_j)$, so they are disjoint.
- Line L13: both sets are explicit.
- Line L14: a tree $\mathit{op}(p, q)$ is in both sets if and only if $p \in R(a_1) \cap R(b_1)$ and $q \in R(a_2) \cap R(b_2)$, because two trees with the same root are equal exactly when their subtrees are equal.
- Line L15: a leaf holds only terminals and a join only compound trees, and two joins with different operators hold trees with different roots. So the intersection is empty.

Unions are made only at lines L11 and L12, and their kids are disjoint, as shown. Other unions in the result come from recursive calls, and they are disjoint by the hypothesis. $\square$

The recursion stops: each call goes down at least one edge in $a$ or in $b$, and the DAGs have no cycles.

## Lemma 4: COUNT

**Claim.** For a disjoint node $n$, COUNT$(n) = |R(n)|$.

**Proof.** By induction on the height. A leaf has $|A|$ programs. The kids of a disjoint union have disjoint sets, so the size of the union is the sum. For a join, the map $(p, q) \mapsto \mathit{op}(p, q)$ from $R(a) \times R(b)$ is one to one, so the size is the product. $\square$

## Theorem

For examples $(i_1, o_1), \ldots, (i_k, o_k)$ and a size bound $S$, the node
$$\mathrm{INTERSECT}(\ldots \mathrm{INTERSECT}(\mathrm{BUILD}(i_1, o_1, S), \mathrm{BUILD}(i_2, o_2, S)) \ldots, \mathrm{BUILD}(i_k, o_k, S))$$
represents exactly the programs of size at most $S$ that are consistent with all $k$ examples, and COUNT gives their number.

**Proof.** By the corollary of Lemma 2, each BUILD represents the programs consistent with its example. By Lemma 3, applied $k - 1$ times, the result represents the intersection of these sets, and it is disjoint. Lemma 4 gives the count. $\square$

## Size of the structure

**Claim.** Let $d$ be the largest $|\mathit{vals}[s]|$. BUILD makes at most $\frac{S+1}{2} d$ nodes of the form NODE$(s, v)$, and at most $3 \bigl(\frac{S+1}{2}\bigr)^2 d^2$ join nodes. A chain of $k$ joins over one leaf with two terminals represents $2^{k+1}$ programs with $k + 1$ nodes.

**Proof.** There is one NODE$(s, v)$ for each odd $s$ and each $v \in \mathit{vals}[s]$, by the memo table. Each join comes from one tuple of $\mathit{how}$, and there are at most $\frac{S+1}{2}$ splits, $d^2$ pairs of values and 3 operators for each odd $s$. For the chain, let $L$ be the leaf $\{x, y\}$, $J_0 = L$ and $J_{t} = \mathrm{JOIN}(+, L, J_{t-1})$. Then $|R(J_t)| = 2 \cdot |R(J_{t-1})|$ by Lemma 4, so $|R(J_k)| = 2^{k+1}$, and the DAG has the nodes $L, J_1, \ldots, J_k$. $\square$
