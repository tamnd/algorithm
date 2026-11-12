---
title: Gusfield's algorithm returns a perfect phylogeny exactly when one exists
proves: [correctness, termination]
status: full
---

**Notation.** $M$ is an $n \times m$ matrix with entries in $\{0, 1\}$. For a column $c$, let $O_c = \{\, i : M[i][c] = 1 \,\}$ be the set of rows with a 1 in $c$. A *rooted perfect phylogeny* for $M$ (with the all-zero ancestor) is a rooted tree $T$ with these properties. Each column $c$ with $O_c \neq \emptyset$ labels exactly one edge of $T$, and an all-zero column labels no edge. Each row $i$ is attached as a leaf below some node $v_i$ of $T$. For each row $i$, the labels on the path from the root to $v_i$ are exactly the columns $c$ with $M[i][c] = 1$. Nodes with one child are allowed.

A family of sets is *laminar* if every two of its sets are disjoint or nested.

**Lemma 1 (a phylogeny forces nesting).** If $M$ has a rooted perfect phylogeny, then the sets $O_c$ with $O_c \neq \emptyset$ form a laminar family.

*Proof.* Let column $c$ label the edge from $u$ to its child $w$. A row $i$ crosses this edge on its root path if and only if $v_i$ is $w$ or below $w$. So $O_c$ is the set of rows attached in the subtree of $w$. Two subtrees of a rooted tree are disjoint or one contains the other. $\square$

**Lemma 2 (the sort).** After line L1, the columns are in non-increasing order of the integer $\mathrm{val}(c) = \sum_{i=1}^{n} M[i][c] \, 2^{n-i}$, where row 1 is the most significant digit. Hence, after line L2, the classes $C_1, \ldots, C_k$ have pairwise distinct sets $O_1, \ldots, O_k$, all nonempty, and $O_a \supsetneq O_b$ implies $a < b$.

*Proof.* Line L1 is a least significant digit [radix sort](/radix-sort/) with base 2: one stable pass per row, from row $n$ to row 1, and each pass puts the columns with a 1 in that row before the columns with a 0. After the passes for rows $n, n-1, \ldots, r$, the columns are in non-increasing order of the number formed by rows $r, \ldots, n$, by the standard induction for LSD radix sort (stability keeps the order of the later digits among columns that tie on row $r$). So at the end the order is non-increasing in $\mathrm{val}$. Two columns with the same value are equal, and equal columns are adjacent in this order, so line L2 merges each group of equal nonzero columns into one class and drops the zero columns. If $O_a \supsetneq O_b$, then $\mathrm{val}(a) > \mathrm{val}(b)$, because $a$ has every 1 of $b$ and at least one more. So class $a$ comes first. $\square$

For a row $i$ and a class $j$ with $i \in O_j$, let $\mathrm{prev}_i(j)$ be the largest $j' < j$ with $i \in O_{j'}$, or $0$ if there is none.

**Lemma 3 (the loop).** In the iteration of line L4 for row $i$, when line L7 finds $i \in O_j$, the variable $last$ equals $\mathrm{prev}_i(j)$. The algorithm reaches line L12 if and only if, for each class $j$, all rows $i \in O_j$ give the same value $\mathrm{prev}_i(j)$. In that case $parent[j]$ is this common value $p(j)$, and $p(j) < j$.

*Proof.* Line L5 sets $last = 0$, and line L10 sets $last = j$ each time the scan meets a class that contains $i$. So at line L7 the variable holds the last class before $j$ that contains $i$, or 0. The first row of $O_j$ that the loop meets sets $parent[j]$ at line L8. Each later row of $O_j$ is compared with it at line L9, and the run stops with no phylogeny on the first difference. Every class is nonempty, so every $parent[j]$ is set when line L12 is reached. $\square$

**Lemma 4 (nesting implies success).** If $O_1, \ldots, O_k$ is laminar, then the algorithm reaches line L12.

*Proof.* Fix $j$ and a row $i \in O_j$. Let $j' < j$ with $i \in O_{j'}$. The sets $O_{j'}$ and $O_j$ meet in $i$, so they are nested. They are distinct, and $O_{j'} \subsetneq O_j$ would give $j < j'$ by Lemma 2. So $O_j \subsetneq O_{j'}$. This shows that $\{\, j' < j : i \in O_{j'} \,\} = \{\, j' < j : O_j \subsetneq O_{j'} \,\}$. The right side does not depend on $i$, so neither does its maximum $\mathrm{prev}_i(j)$. Lemma 3 completes the proof. $\square$

**Lemma 5 (success implies nesting).** If the algorithm reaches line L12, then for every $j$ and every $j' < j$ with $O_{j'} \cap O_j \neq \emptyset$, we have $O_j \subseteq O_{j'}$. In particular, $O_1, \ldots, O_k$ is laminar.

*Proof.* Put $O_0 = \{1, \ldots, n\}$. First, $O_j \subseteq O_{p(j)}$ for each $j$: every $i \in O_j$ has $\mathrm{prev}_i(j) = p(j)$, and if $p(j) \ge 1$ this means $i \in O_{p(j)}$.

Now use strong induction on $j$. Let $j' < j$ and $i \in O_{j'} \cap O_j$. Write $p = p(j) = \mathrm{prev}_i(j)$. Since $i \in O_{j'}$ and $j' < j$, the definition of $\mathrm{prev}$ gives $p \ge j'$. If $p = j'$, then $O_j \subseteq O_p = O_{j'}$. If $p > j'$, then $p \ge 1$, $O_j \subseteq O_p$, and $i \in O_{j'} \cap O_p$ with $j' < p < j$. The induction hypothesis for $p$ gives $O_p \subseteq O_{j'}$, so $O_j \subseteq O_{j'}$. $\square$

**Lemma 6 (the output).** If the algorithm reaches line L12, the tree it returns is a rooted perfect phylogeny for $M$.

*Proof.* The nodes are $0, 1, \ldots, k$ and the edges are $p(j) \to j$. Since $p(j) < j$, following parents from any node strictly decreases the index and ends at 0, so the graph is a tree rooted at 0. Row $i$ is attached below $\mathrm{leaf}[i]$, the last class that contains $i$ (or 0). Let $j_1 < j_2 < \cdots < j_t$ be the classes that contain $i$. Then $\mathrm{leaf}[i] = j_t$ and $p(j_s) = \mathrm{prev}_i(j_s) = j_{s-1}$, with $j_0 = 0$. So the root path of row $i$ passes exactly the edges into $j_1, \ldots, j_t$, whose labels are exactly the columns $c$ with $M[i][c] = 1$. Each nonzero column is in exactly one class, so it labels exactly one edge, and the zero columns label none. $\square$

**Theorem.** GUSFIELD-PERFECT-PHYLOGENY$(M)$ always stops. It returns a tree if and only if $M$ has a rooted perfect phylogeny, and the tree it returns is one.

*Proof.* Every loop has a fixed number of steps, so the algorithm stops. If $M$ has a rooted perfect phylogeny, the sets $O_j$ are laminar by Lemma 1, so the algorithm reaches line L12 by Lemma 4. Whenever it reaches line L12, the tree is a perfect phylogeny by Lemma 6. If $M$ has none, the algorithm cannot reach line L12, because the tree would be one; so it returns NO PHYLOGENY at line L9. $\blacksquare$

**Corollary (the pair test).** $M$ has a rooted perfect phylogeny if and only if no two columns $a, b$ contain all three of the pairs $(0,1)$, $(1,0)$ and $(1,1)$ in the same rows.

*Proof.* By Lemmas 1, 4 and 6, a phylogeny exists if and only if the nonempty sets $O_c$ are laminar. Two sets $O_a, O_b$ are disjoint exactly when no row shows $(1,1)$, and nested exactly when no row shows $(1,0)$ or no row shows $(0,1)$. $\square$

**The unrooted problem.** An *unrooted perfect phylogeny* for $M$ is a tree whose nodes carry vectors in $\{0,1\}^m$, in which each row of $M$ is the vector of some node and each column changes its value on at most one edge. Let $M'$ be $M$ with every column $c$ complemented where $M[1][c] = 1$, so that row 1 of $M'$ is all zero. Complementing a column does not change the edge on which it changes, so $M$ and $M'$ have the same unrooted phylogenies. Root such a tree for $M'$ at the node of row 1. That node is all zero, so for each column the nodes with value 1 are exactly the nodes below its change edge, and the tree, with its change edges as labels, is a rooted perfect phylogeny for $M'$. Conversely, a rooted perfect phylogeny for $M'$, with each node labeled by the columns on its root path, is an unrooted one. So the unrooted problem for $M$ is the rooted problem for $M'$, and the corollary for $M'$ becomes the four-gamete test for $M$: row 1 of $M'$ shows $(0,0)$ in every pair of columns. $\square$
