---
title: BEA returns an order of the attributes in which each step is the best insertion, and the global affinity measure is the bond energy
proves: [correctness, termination, time.worst]
status: full
---

We use the line numbers of the pseudocode on the page. $AA$ is a symmetric $a \times a$ matrix with non-negative entries. For two columns $x$ and $y$, $\mathrm{bond}(x, y) = \sum_{z=1}^{a} AA(z, x) \, AA(z, y)$, and $\mathrm{bond}(x, y) = 0$ when $x$ or $y$ is the empty place $A_0$ or $A_{a+1}$ outside the order. For an order $c_1, \dots, c_m$ of some of the columns, with the rows in the same order, the global affinity measure is

$$AM(c_1, \dots, c_m) = \sum_{j=1}^{m} \big(\mathrm{bond}(c_j, c_{j-1}) + \mathrm{bond}(c_j, c_{j+1})\big) = 2 \sum_{j=1}^{m-1} \mathrm{bond}(c_j, c_{j+1}),$$

where the second form holds because each pair of neighbors is counted once from each side and the bonds with the empty places are 0.

**Lemma 1 (AM is the bond energy).** Let $B$ be the matrix $AA$ with its rows and its columns both put in the order $c_1, \dots, c_a$. The measure of effectiveness of McCormick, Schweitzer and White,

$$ME(B) = \tfrac{1}{2} \sum_{i, j} B_{ij} \, (B_{i, j-1} + B_{i, j+1} + B_{i-1, j} + B_{i+1, j}),$$

with $B_{ij} = 0$ outside the matrix, equals $AM(c_1, \dots, c_a)$.

*Proof.* The column part is $\sum_{i, j} B_{ij} (B_{i, j-1} + B_{i, j+1}) = \sum_j \sum_i B_{ij} B_{i, j+1} + \sum_j \sum_i B_{ij} B_{i, j-1}$. The inner sum $\sum_i B_{ij} B_{i, j+1}$ runs over all rows, so it does not depend on the order of the rows, and it equals $\mathrm{bond}(c_j, c_{j+1})$. Each of the two sums is $\sum_{j=1}^{a-1} \mathrm{bond}(c_j, c_{j+1})$, so the column part is $2 \sum_j \mathrm{bond}(c_j, c_{j+1})$. Because $AA$ is symmetric and the rows have the same order as the columns, $B$ is symmetric, so the row part $\sum_{i,j} B_{ij} (B_{i-1, j} + B_{i+1, j})$ equals the column part. Then $ME(B) = \tfrac{1}{2} \cdot 2 \cdot 2 \sum_j \mathrm{bond}(c_j, c_{j+1}) = AM$. $\square$

**Lemma 2 (contribution).** Let $c_1, \dots, c_m$ be an order and let $A_k$ be a column that is not in it. Put $A_k$ between $A_i$ and $A_j$, two neighbors of the order (or an empty place at an end). Then the new order has

$$AM_{\text{new}} - AM_{\text{old}} = \mathrm{cont}(A_i, A_k, A_j) = 2\,\mathrm{bond}(A_i, A_k) + 2\,\mathrm{bond}(A_k, A_j) - 2\,\mathrm{bond}(A_i, A_j).$$

*Proof.* By the second form of $AM$, the measure is twice the sum of the bonds of neighboring pairs. The insertion removes the neighbor pair $(A_i, A_j)$ and adds the pairs $(A_i, A_k)$ and $(A_k, A_j)$. All other neighbor pairs stay. If $A_i$ or $A_j$ is an empty place, its bonds are 0 and the formula still holds. $\square$

**Theorem 1 (correctness of the order).** BEA returns an order of all $a$ columns, and the matrix of line L6 is $AA$ with its rows and columns in that order. For each $k \ge 3$, the order after step $k$ has the largest $AM$ among all orders that insert $A_k$ into the order after step $k - 1$.

*Proof.* Line L1 places $A_1$ and $A_2$. For each $k$ from 3 to $a$, line L2 takes the column $A_k$, which is not placed yet. Lines L3 and L4 compute $\mathrm{cont}$ for each of the $k$ places of the current order of $k - 1$ columns, and line L5 inserts $A_k$ at a place with the largest value. By Lemma 2 the value at each place is the change of $AM$, and $AM_{\text{old}}$ is the same for all places, so the chosen order has the largest $AM$ among the $k$ candidates. Each column is inserted once, so the final order holds every column once. Line L6 orders the rows as the columns. $\square$

**Theorem 2 (no global guarantee).** BEA does not always return an order of largest $AM$.

*Proof.* Take $a = 4$ and three queries: $q_1$ uses $A_1$ and $A_2$ four times, $q_2$ uses $A_1$ and $A_4$ twice, and $q_3$ uses $A_1$ and $A_3$ once. The affinity matrix has the rows $(7, 4, 1, 2)$, $(4, 4, 0, 0)$, $(1, 0, 1, 0)$ and $(2, 0, 0, 2)$. The bonds needed are $\mathrm{bond}(A_1, A_2) = 44$, $\mathrm{bond}(A_1, A_3) = 8$, $\mathrm{bond}(A_1, A_4) = 18$, $\mathrm{bond}(A_2, A_3) = 4$, $\mathrm{bond}(A_2, A_4) = 8$ and $\mathrm{bond}(A_3, A_4) = 2$. BEA starts with $A_1 A_2$. For $A_3$ the contributions at the three places are $16$, $-64$ and $8$, so it gives $A_3 A_1 A_2$. For $A_4$ they are $4$, $24$, $-36$ and $16$, so it gives $A_3 A_4 A_1 A_2$ with $AM = 2(2 + 18 + 44) = 128$. The order $A_3 A_2 A_1 A_4$ has $AM = 2(4 + 44 + 18) = 132$. $\square$

**Remark (the exact problem).** By the second form of $AM$, an order of largest $AM$ is a path through all columns of largest total weight, where the weight of the pair $\{x, y\}$ is $2\,\mathrm{bond}(x, y)$. This is a maximum weight Hamiltonian path, a form of the [traveling salesman problem](/traveling-salesman-problem/), and the insertion of BEA is the cheapest insertion heuristic for it, run in a fixed order of the columns. The weights here are inner products of non-negative columns, so the general hardness of the traveling salesman problem does not by itself show that this special case is hard; the page makes no claim about that.

**Theorem 3 (running time).** With all bonds computed first, BEA takes $O(a^3)$ time and $O(a^2)$ space.

*Proof.* There are $a(a + 1)/2$ bonds, each a sum of $a$ products, so the table of bonds takes $O(a^3)$ time and $O(a^2)$ space. Step $k$ evaluates $k$ contributions, each with three lookups, and an insertion into a list of length $k - 1$ in $O(k)$ time. The sum over $k \le a$ is $O(a^2)$. Line L6 copies $a^2$ entries. The total is $O(a^3)$. Without the table, each contribution costs $O(a)$ and the steps cost $O(a^3)$ in total, which is the same bound. $\square$

**The split step.** For a split point $i$ of the order, let $TA$ be the first $i$ attributes and $BA$ the rest. $CTQ$ is the total frequency of the queries whose attributes all lie in $TA$, $CBQ$ the same for $BA$, and $COQ$ the total frequency of the other queries, which use both sides. A query with at least one attribute is in exactly one of the three groups, so $CTQ + CBQ + COQ$ is the total frequency. The step returns a split point with the largest $z = CTQ \cdot CBQ - COQ^2$. This is a rule: it prefers two fragments that both serve many queries alone and that few queries need together. It is not derived from a cost model, and it is not proved to minimize any cost.
