---
title: The column dynamic program returns an optimal weighted MEC solution
proves: [correctness]
status: full
---

**Setting.** There are $n$ fragments and $m$ columns. Fragment $i$ has an allele $F_i(j) \in \{0, 1\}$ and a weight $w_i(j) \ge 0$ at each column $j$ in its set of defined columns $J_i$; the other columns are holes. A fragment with $J_i \ne \emptyset$ is *active* at every column from $\min J_i$ to $\max J_i$, and $A(j)$ is the set of fragments active at column $j$. A *bipartition* of a set $X$ is a pair $(R, S)$ with $R \cup S = X$ and $R \cap S = \emptyset$. For a set $Y$, the *restriction* of $(R, S)$ to $Y$ is $(R \cap Y, S \cap Y)$.

For a set $X$ of fragments, a column $j$ and an allele $a$, let $W_j(X, a) = \sum_{i \in X,\ j \in J_i,\ F_i(j) \ne a} w_i(j)$, the cost to set column $j$ of every fragment in $X$ to $a$. The weighted MEC problem asks for a bipartition $(R, S)$ of all fragments and two haplotypes $h_1, h_2 \in \{0, 1\}^m$ that minimize

$$\mathrm{cost}(R, S, h_1, h_2) = \sum_{j=1}^{m} \bigl(W_j(R, h_1(j)) + W_j(S, h_2(j))\bigr).$$

In the all-heterozygous form, $h_2$ must be the complement of $h_1$. The value is the same as $\min_{h_1, h_2} \sum_i \min(d_i(h_1), d_i(h_2))$, where $d_i(h)$ is the weight of the entries of fragment $i$ that differ from $h$, because for fixed haplotypes the best bipartition puts each fragment on the side of the closer haplotype. This second form is what the tests compute by brute force.

The algorithm computes, at lines L4 and L5,

$$\Delta(j, (R, S)) = \min_a W_j(R, a) + \min_a W_j(S, a)$$

for each bipartition $(R, S)$ of $A(j)$, or $\min_a \bigl(W_j(R, a) + W_j(S, 1 - a)\bigr)$ in the all-heterozygous form.

**Lemma 1 (one bipartition).** Fix a bipartition $(R, S)$ of all fragments. Then $\min_{h_1, h_2} \mathrm{cost}(R, S, h_1, h_2) = \sum_j \Delta(j, (R \cap A(j), S \cap A(j)))$, and the minimum is reached by taking $h_1(j)$ and $h_2(j)$ as the alleles that give the two minima of $\Delta$.

*Proof.* The cost is a sum over columns, and the term of column $j$ depends only on $h_1(j)$ and $h_2(j)$. So the minimum over $(h_1, h_2)$ is the sum over $j$ of the minimum over $(h_1(j), h_2(j))$. In the free form the two choices are independent and give $\min_a W_j(R, a) + \min_a W_j(S, a)$. In the all-heterozygous form there is one choice $a = h_1(j)$, which gives the second formula. A fragment with an entry at column $j$ has $\min J_i \le j \le \max J_i$, so it is in $A(j)$. Fragments outside $A(j)$ add 0 to $W_j$, so $W_j(R, a) = W_j(R \cap A(j), a)$, and the same holds for $S$. $\square$

**Lemma 2 (consistent sequences).** Call a sequence $B_1, \ldots, B_m$, with $B_j$ a bipartition of $A(j)$, *consistent* when $B_j$ and $B_{j+1}$ have the same restriction to $A(j) \cap A(j+1)$ for each $j < m$. The restrictions of a bipartition of all fragments to the sets $A(j)$ form a consistent sequence, and each consistent sequence comes from a bipartition of all fragments in this way.

*Proof.* The first claim is clear, because two restrictions of one bipartition agree on every common fragment. For the second claim, take a consistent sequence. A fragment $i$ with $J_i \ne \emptyset$ is in $A(j)$ exactly for $j$ in the interval $[\min J_i, \max J_i]$. For two adjacent columns $j, j+1$ of that interval, $i$ is in $A(j) \cap A(j+1)$, so consistency puts $i$ on the same side in $B_j$ and $B_{j+1}$. By induction along the interval, $i$ is on the same side in every $B_j$ that contains it. Put $i$ on that side. Put each fragment with no entries on either side; it is in no $A(j)$. The restrictions of this bipartition are the given sequence. $\square$

The interval property is the reason for the definition of *active*: a paired read with a long gap between its mates stays in $A(j)$ over the gap, so the sequence cannot move it from one side to the other there.

By Lemmas 1 and 2, the optimum of weighted MEC is $\min \sum_j \Delta(j, B_j)$ over consistent sequences.

**Lemma 3 (table invariant).** After line L7 for column $j$, for each bipartition $B$ of $A(j)$, $C(j, B) = \min \sum_{l=1}^{j} \Delta(l, B_l)$ over the sequences $B_1, \ldots, B_j$ that are consistent up to $j$ and have $B_j = B$. After line L8, $\bar C(j, B')$ is the minimum of $C(j, B)$ over the bipartitions $B$ of $A(j)$ whose restriction to $A(j) \cap A(j+1)$ is $B'$, and $D(j, B')$ is a $B$ that reaches it.

*Proof.* By induction on $j$. For $j = 1$, the only sequence is $B_1 = B$, and line L6 sets $C(1, B) = \Delta(1, B)$. For $j > 1$, a sequence consistent up to $j$ with $B_j = B$ is a sequence consistent up to $j - 1$ whose last element $B_{j-1}$ has the same restriction to $A(j-1) \cap A(j)$ as $B$, followed by $B$. The cost is $\Delta(j, B)$ plus the cost of the first part. The least cost of the first part, over all choices, is $\min C(j-1, B_{j-1})$ over those $B_{j-1}$, by the induction hypothesis, and this is $\bar C(j-1, B')$ with $B'$ the restriction of $B$ to $A(j-1) \cap A(j)$. Line L7 adds these two numbers. The claim on $\bar C$ and $D$ is the definition of line L8: the code visits each $B$, maps it to its restriction, and keeps the smallest value and the first $B$ that gives it. $\square$

**Theorem.** Line L9 finds the optimal weighted MEC cost $C^* = \min_B C(m, B)$. Lines L10 and L11 return a bipartition of the fragments and haplotypes $h_1, h_2$ with $\mathrm{cost}(R, S, h_1, h_2) = C^*$, and the MEC value of $(h_1, h_2)$, with each fragment on its closer haplotype, is also $C^*$.

*Proof.* By Lemma 3 with $j = m$ and the remark after Lemma 2, $C^*$ is the optimum. Line L10 sets $B^*_m$ to a minimizer and then $B^*_j = D(j, B^*_{j+1} \cap A(j))$ for $j = m - 1$ down to 1. By Lemma 3, $B^*_j$ has the same restriction to $A(j) \cap A(j+1)$ as $B^*_{j+1}$, so the sequence is consistent, and $C(j+1, B^*_{j+1}) = \Delta(j+1, B^*_{j+1}) + C(j, B^*_j)$. Summing these equations gives $\sum_j \Delta(j, B^*_j) = C(m, B^*_m) = C^*$. By Lemma 2 the sequence comes from a bipartition $(R, S)$ of all fragments, which is the returned `side`. Line L11 takes for each column the alleles that reach the minima in $\Delta(j, B^*_j)$, so by Lemma 1, $\mathrm{cost}(R, S, h_1, h_2) = C^*$. Last, the MEC value of $(h_1, h_2)$ moves each fragment to its closer haplotype, so it is at most $C^*$, and it is at least $C^*$ because $C^*$ is the optimum. $\square$

**Cost.** Let $c = \max_j |A(j)|$. Line L1 costs $O(n + \sum_i (\max J_i - \min J_i + 1))$. For each column, the code computes the subset sums $W_j(\cdot, 0)$ and $W_j(\cdot, 1)$ over the $2^{|A(j)|}$ masks, each from a mask with one bit less, in $O(2^{|A(j)|})$ time. Then $\Delta$, the projection of each mask to the intersection, $C$ and $\bar C$ also take $O(2^{|A(j)|})$ time. So the time is $O(2^c m)$ plus the cost of line L1, and the back pointers take $O(2^c m)$ space. Because $(R, S)$ and $(S, R)$ have the same $\Delta$ and the same $C$, an implementation can keep one of each two masks, which gives the bound $O(2^{c-1} m)$ of Patterson et al. (2015). The code keeps both.
