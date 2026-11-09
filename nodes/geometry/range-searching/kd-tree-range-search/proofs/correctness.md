---
title: kd-tree range search reports exactly the points in the box and searches O(n^(1/2)) nodes
proves: [correctness, termination, complexity]
status: full
---

**Setting.** $P = (p_0, \dots, p_{n-1})$ is a list of $n \ge 1$ points in the plane (repeats allowed). The tree $T$ is the leaf-based kd-tree of the page: a node at even depth orders its $m$ points by the composite key $X(p_i) = (x_i, y_i, i)$, a node at odd depth by $Y(p_i) = (y_i, x_i, i)$, both lexicographic, and gives the first $\lceil m/2 \rceil$ points to the left child and the rest to the right child; a node with one point is a leaf. Every node $v$ stores $\mathrm{box}(v)$, the smallest closed axis-parallel rectangle that contains the points of its subtree $S(v)$. The query box is $R = [x_1, x_2] \times [y_1, y_2]$, closed, with $x_1 \le x_2$ and $y_1 \le y_2$ (otherwise the code returns at once, and $P \cap R = \emptyset$).

**Claim.** SEARCH-KD-TREE(root, $R$) terminates, reports each index $i$ with $p_i \in R$ exactly once and no other, and the number of nodes on which it is called is $O(\sqrt{n})$.

**Step 1 (tests of lines L4 and L5).** For closed intervals, $[a, b] \subseteq [c, e]$ if and only if $c \le a$ and $b \le e$, and $[a, b] \cap [c, e] \ne \emptyset$ if and only if $a \le e$ and $c \le b$. A product of two intervals is inside, or meets, another product if and only if this holds on both axes. So lines L4 and L5 compute exactly $\mathrm{box}(c) \subseteq R$ and $\mathrm{box}(c) \cap R \ne \emptyset$.

**Step 2 (correctness).** We show by induction on the height of $v$: a call SEARCH-KD-TREE$(v, R)$ reports each $i \in S(v)$ with $p_i \in R$ exactly once and no other index.

If $v$ is a leaf, $S(v) = \{i\}$ and line L2 reports $i$ if and only if $p_i \in R$.

Otherwise $S(v)$ is the disjoint union of $S(c)$ over the two children. Take a child $c$.

- If $\mathrm{box}(c) \subseteq R$, then every point of $S(c)$ lies in its bounding box, hence in $R$, and REPORT-SUBTREE$(c)$ reports each leaf of the subtree once, that is each index of $S(c)$ once.
- If $\mathrm{box}(c) \cap R = \emptyset$, no point of $S(c)$ lies in $R$, and nothing is reported, which is right.
- Otherwise the call on $c$ reports the right indices of $S(c)$ by induction.

The children have disjoint index sets, so each index of $S(v) \cap \{i : p_i \in R\}$ is reported once. Applied to the root, the claim of correctness follows.

**Step 3 (termination).** Every call is on a child of the node of the calling frame, so the calls follow distinct root-to-node paths in a finite tree. The build terminates because a node with $m \ge 2$ points gives $\lceil m/2 \rceil \ge 1$ and $\lfloor m/2 \rfloor \ge 1$ points to its children, both fewer than $m$.

**Step 4 (composite coordinates).** Map each point to $p'_i = (X(p_i), Y(p_i))$ and order each axis lexicographically. All first coordinates of the $p'_i$ are distinct, and so are all second coordinates. Let $A_1 = (x_1, -\infty, -\infty)$, $A_2 = (x_2, +\infty, +\infty)$, $B_1 = (y_1, -\infty, -\infty)$, $B_2 = (y_2, +\infty, +\infty)$, where $\pm\infty$ compare below and above every number. Then $x_1 \le x_i \le x_2$ if and only if $A_1 < X(p_i) < A_2$, and likewise for $y$. The values $A_1, A_2, B_1, B_2$ differ from every coordinate of every $p'_i$. Let $\mathrm{box}'(v)$ be the bounding box of $\{p'_i : i \in S(v)\}$, which is $[X_{\min}, X_{\max}] \times [Y_{\min}, Y_{\max}]$, and $R' = [A_1, A_2] \times [B_1, B_2]$. The first component of $X_{\min}$ is $x_{\min}$ of $\mathrm{box}(v)$, and so on. Hence by Step 1, $\mathrm{box}(v) \subseteq R$ if and only if $\mathrm{box}'(v) \subseteq R'$, and $\mathrm{box}(v) \cap R \ne \emptyset$ if and only if $\mathrm{box}'(v) \cap R' \ne \emptyset$. So the search on $P$ with $R$ makes the same decisions as the search on $P'$ with $R'$, where all coordinates are distinct.

**Step 5 (regions).** In the composite space define the region $\rho(v)$ as in de Berg et al.: $\rho(\text{root})$ is the whole plane; if $v$ splits by the first axis and $s$ is the largest first coordinate in its left child, then $\rho(\text{left}) = \rho(v) \cap \{X \le s\}$ and $\rho(\text{right}) = \rho(v) \cap \{X > s\}$, and the same with the second axis at odd depth. By induction, $\{p'_i : i \in S(v)\} \subseteq \rho(v)$, and so $\mathrm{box}'(v) \subseteq \rho(v)$ because $\rho(v)$ is a product of intervals.

**Step 6 (searched nodes cross a side line).** Let $v$ be a node other than the root on which the search is called. Then $\mathrm{box}'(v) \cap R' \ne \emptyset$ and $\mathrm{box}'(v) \not\subseteq R'$. So on some axis, say the first, the interval $[X_{\min}, X_{\max}]$ meets $[A_1, A_2]$ but is not inside it: $X_{\min} < A_1 \le X_{\max}$ or $X_{\min} \le A_2 < X_{\max}$. Since $A_1, A_2$ are not coordinates of points, $X_{\min} < A_j < X_{\max}$ for $j = 1$ or $j = 2$. So the vertical line $\ell_j = \{X = A_j\}$ meets $\mathrm{box}'(v)$, hence meets $\rho(v)$. The same holds with horizontal lines $\{Y = B_j\}$ on the second axis. So every searched node other than the root has a region that meets one of the four lines $\{X = A_1\}$, $\{X = A_2\}$, $\{Y = B_1\}$, $\{Y = B_2\}$, none of which passes through a point $p'_i$.

**Step 7 (counting regions met by a line).** Let $\ell$ be a vertical line $\{X = A\}$ with $A$ different from all first coordinates. For $m \ge 1$ let $Q(m)$ be the largest number of nodes whose region meets $\ell$, taken over all subtrees with at most $m$ points whose root splits by the first axis. The two children of such a root $u$ have regions on opposite sides of a vertical line $X = s$ with $s \ne A$, so $\ell$ meets the region of at most one child. That child splits by the second axis, and $\ell$ may meet the regions of both its children, the grandchildren of $u$. The grandchildren split by the first axis again and hold at most $\lceil \lceil m/2 \rceil / 2 \rceil = \lceil m/4 \rceil$ points each. Counting $u$, the child, and the nodes below the two grandchildren,
$$Q(m) \le 2 + 2\,Q(\lceil m/4 \rceil) \quad (m \ge 2), \qquad Q(1) = 1 .$$
(For $m \le 3$ the grandchildren are absent or leaves, and the bound still holds.) Let $j \ge 0$ be the least integer with $m \le 4^j$. Unrolling $j$ times, using that $Q$ does not decrease in $m$ by its definition, gives $Q(m) \le 2(1 + 2 + \dots + 2^{j-1}) + 2^j Q(1) = 3 \cdot 2^j - 2$. Since $4^{j-1} < m$ when $j \ge 1$, we have $2^j < 2\sqrt{m}$, so $Q(m) < 6\sqrt{m}$ for all $m \ge 1$.

The root of the whole tree splits by the first axis, so a vertical side line meets fewer than $6\sqrt{n}$ regions. A horizontal side line meets the root region and possibly both children, whose subtrees split by the second axis first and hold at most $\lceil n/2 \rceil$ points; by the same argument with the axes exchanged, it meets fewer than $1 + 2 \cdot 6\sqrt{\lceil n/2 \rceil}$ regions in total.

**Step 8 (total cost).** By Steps 6 and 7, the number of searched nodes is at most $1 + 2 \cdot 6\sqrt{n} + 2(1 + 12\sqrt{\lceil n/2 \rceil}) = O(\sqrt{n})$. Each searched node costs $O(1)$ comparisons. REPORT-SUBTREE on a subtree with $j$ leaves visits its $2j - 1$ nodes, and the reported subtrees are disjoint, with $k$ leaves in all, so they cost $O(k)$. The query takes $O(\sqrt{n} + k)$ time. $\blacksquare$
