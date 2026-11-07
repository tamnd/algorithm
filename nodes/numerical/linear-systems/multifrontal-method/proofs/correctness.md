---
title: The multifrontal method computes the Cholesky factor, the update matrices it needs are on top of the stack, and Liu's child order minimizes the stack peak
proves: [correctness, termination]
status: full
---

Setting. $A \in \mathbb{R}^{n \times n}$ is symmetric positive definite, already permuted, and $A = L L^T$. In exact arithmetic, write $\mathcal{S}_j = \{i > j : l_{ij} \ne 0\}$ for the structure of column $j$; the implementation computes the symbolic structure, which can only be larger, and the argument below holds for it word for word. The elimination tree has $\mathrm{parent}(j) = \min \mathcal{S}_j$, or none when $\mathcal{S}_j = \emptyset$. $T[j]$ is the subtree rooted at $j$, $I_j = \{j\} \cup \mathcal{S}_j$, and line numbers refer to the pseudocode of the page.

**Lemma 1 (structure inheritance).** If $j < p < i$ and $l_{pj} \ne 0$, $l_{ij} \ne 0$, then $l_{ip} \ne 0$ (symbolically). Consequently $\mathcal{S}_j \setminus \{p\} \subseteq \mathcal{S}_p$ for $p = \mathrm{parent}(j)$, and if $l_{jk} \ne 0$ with $k < j$, then $j$ is an ancestor of $k$.

*Proof.* In the elimination graph model ([fill-in](/fill-in/)), when $j$ is eliminated its later neighbours $p$ and $i$ are joined, so $l_{ip} \ne 0$ when $p$ is eliminated. Applying this with $p = \min \mathcal{S}_j$ gives the inclusion. For the last claim, follow parents from $k$: each step goes to the smallest element of the current structure, and by the inclusion, $j$ stays in the structure until it is reached, since the parents increase and stay at most $j$. $\square$

**Lemma 2 (symbolic recurrence).** $\mathcal{S}_j = \big(\{i > j : a_{ij} \ne 0\} \cup \bigcup_{c \text{ child of } j} \mathcal{S}_c\big) \setminus \{j\}$.

*Proof.* "$\supseteq$": $a_{ij} \ne 0$ gives $l_{ij} \ne 0$ symbolically, and Lemma 1 gives $\mathcal{S}_c \setminus \{j\} \subseteq \mathcal{S}_j$. "$\subseteq$": a later neighbour $i$ of $j$ at its elimination is either an original neighbour, or was joined to $j$ when some $k < j$ with $i, j \in \mathcal{S}_k$ was eliminated. By Lemma 1, $k$ is a descendant of $j$. Let $c$ be the child of $j$ on the path. Repeated use of Lemma 1 along the path from $k$ to $c$ keeps $i$, which exceeds every vertex of the path, in the structures, so $i \in \mathcal{S}_c$. $\square$

`column_structures` applies this recurrence in increasing $j$; children have smaller indices, so their structures are complete when used. `elimination_tree` is Liu's algorithm, and the tests check $\mathrm{parent}(j) = \min \mathcal{S}_j$ against an exact factorization.

**Lemma 3 (the stack discipline).** In a postorder, processing the subtree $T[c]$ of a non-root $c$ leaves the stack as it was plus one item, the update matrix $U_c$ on top. Hence, when $j$ is processed, the top $|\mathrm{children}(j)|$ items are exactly the update matrices of its children.

*Proof.* Induction on the height of $c$. Its children's subtrees each add one item by induction. Lines L6 and L7 pop exactly these items, and line L10 pushes $U_c$, which is nonempty because $\mathrm{parent}(c) \in \mathcal{S}_c$. Roots push nothing. $\square$

**Theorem 1 (correctness).** For every $j$, the update matrix is
$$U_j = -\sum_{k \in T[j]} \ell_k \ell_k^T \Big|_{\mathcal{S}_j \times \mathcal{S}_j}, \qquad \ell_k = L(\mathcal{S}_j, k),$$
and line L8 computes column $j$ of $L$ exactly.

*Proof.* Induction along the postorder. Lines L4 to L7 build
$$F_j = \begin{pmatrix} a_{jj} & a_{\mathcal{S}_j, j}^T \\ a_{\mathcal{S}_j, j} & 0 \end{pmatrix} \oplus \bigoplus_{c} U_c,$$
where $\oplus$ is extend-add: entries are added at matching global indices. This is well defined because $\mathcal{S}_c \subseteq I_j$ by Lemma 1. By the induction hypothesis, the first column of $F_j$ is $a_{ij} - \sum_{k \in T[j] \setminus \{j\}} l_{ik} l_{jk}$ for $i \in I_j$. Cholesky requires $l_{ij} l_{jj} = a_{ij} - \sum_{k < j} l_{ik} l_{jk}$, and by Lemma 1 the nonzero terms have $l_{jk} \ne 0$, hence $k \in T[j]$. So the two sums agree, and $l_{jj} = \sqrt{F_{11}}$ and $l_{ij} = F_{i1}/l_{jj}$ are correct. Line L9 subtracts $\ell_j \ell_j^T$ from the trailing block, which gives the formula for $U_j$. The children's contributions restricted to $\mathcal{S}_j$ cover every $k \in T[j]$, because for each such $k$ the rows of $L(:, k)$ beyond $j$ lie in $\mathcal{S}_j$ by Lemma 1 applied along the path. $\square$

The $LDL^T$ mode is the same argument with $F_{11} = d_j$, $l_{ij} = F_{i1}/d_j$ and update $F_{22} - F_{\cdot 1} F_{\cdot 1}^T/d_j$. In rational arithmetic it agrees exactly with the dense $LDL^T$, which the tests check.

**Termination.** The loop at line L3 visits each of the $n$ columns once, and every inner loop is over finite index sets.

**Lemma 4 (stack storage; Liu).** Let $u_c$ be the storage of $U_c$, let $f_j$ be the storage of the front $F_j$, and let the children $c_1, \ldots, c_t$ of $j$ be visited in this order. Then the peak storage over the processing of $T[j]$ is
$$\mathrm{peak}(j) = \max\Big(\max_{1 \le s \le t}\big(\textstyle\sum_{r < s} u_{c_r} + \mathrm{peak}(c_s)\big),\ \textstyle\sum_{r \le t} u_{c_r} + f_j\Big).$$
Ordering the children by decreasing $\mathrm{peak}(c) - u_c$ minimizes $\mathrm{peak}(j)$ over all orders.

*Proof.* The recurrence follows from Lemma 3. During $T[c_s]$, the updates of $c_1, \ldots, c_{s-1}$ wait on the stack. At $j$, all children's updates and the front coexist; the code allocates the front before popping. For optimality, compare two adjacent children $x$ before $y$ with prefix $S$. The terms are $\max(S + p_x,\ S + u_x + p_y)$ against $\max(S + p_y,\ S + u_y + p_x)$ for the swapped order. If $p_x - u_x \ge p_y - u_y$, then $S + u_x + p_y \le S + u_y + p_x$ and $S + p_x \le S + u_y + p_x$, so $x$ first is no worse, and no other term changes. Bubble-sorting any order into the decreasing order therefore never increases the peak. Since $\mathrm{peak}(j)$ is nondecreasing in each $\mathrm{peak}(c)$, choosing the best order bottom up gives the least peak over all postorders. $\square$

The tests check the recurrence against the measured peak and the optimality against brute force over all child orders on small trees.

**Floating point.** Each computed entry of $L$ is $a_{ij}$ minus the products $\hat l_{ik}\hat l_{jk}$, summed in an order fixed by the tree and the extend-adds, and then divided by $\hat l_{jj}$. The standard analysis of Cholesky (Higham, Chapter 10) bounds every summation order by the same $\gamma$, so if the factorization runs to completion, $A + \Delta A = \hat L \hat L^T$ with $|\Delta A| \le \gamma_{n+1} |\hat L||\hat L^T|$. The tests check this elementwise with exact rational residuals.
