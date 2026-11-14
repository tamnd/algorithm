---
title: The method of means and medians has depth the ceiling of log2 n, runs in O(n log n) time and gives the H-tree on a full grid
proves: [correctness, depth, complexity, grid case]
status: full
---

**Model.** The input is a list of $n \ge 1$ sinks $p_1, \dots, p_n$ in the plane. The split order on axis $a$ (0 for $x$, 1 for $y$) compares $(p_i[a], p_i[1 - a], i)$, which is a total order. For a set $S$ split on axis $a$, the *low half* is the first $\lfloor |S|/2 \rfloor$ sinks of $S$ in this order and the *high half* is the rest. The tree has a node for each set that arises, placed at the centre of mass $c(S) = \frac{1}{|S|} \sum_{i \in S} p_i$, and an edge from the node of each set to the nodes of its two halves, of length the L1 distance between them. The root set is all sinks, split on $x$, and the axis alternates with the depth.

**Lemma 1 (the output is a routing tree).** Each sink is a leaf at its own point, each set of at least two sinks has two nonempty halves that partition it, and every root-to-sink path ends at a distinct sink.

*Proof.* For $|S| \ge 2$, both $\lfloor |S|/2 \rfloor \ge 1$ and $|S| - \lfloor |S|/2 \rfloor \ge 1$, and the halves partition $S$ by definition. Sets shrink strictly, so the recursion ends at sets of size 1, whose centre of mass is the sink itself. The leaves are the singletons of a partition of all sinks, so each sink is reached by exactly one path. $\square$

**Lemma 2 (the linear split is correct).** Let $X$ and $Y$ be the sinks of $S$ sorted in the order on axis 0 and on axis 1. Let $L$ be the first $\lfloor |S|/2 \rfloor$ entries of the list for the split axis. Then the entries of $X$ in $L$, in their order in $X$, are the low half sorted on axis 0, and the same holds for $Y$ and for the high half.

*Proof.* $L$ is the low half by its definition. A sublist of a sorted list, kept in order, is sorted. $\square$

**Theorem 1 (depth).** The tree has depth exactly $\lceil \log_2 n \rceil$.

*Proof.* Let $h(n)$ be the depth for $n$ sinks. Then $h(1) = 0$ and $h(n) = 1 + h(\lceil n/2 \rceil)$ for $n \ge 2$, since the high half is the larger and $h$ is nondecreasing (by induction, as $\lceil n/2 \rceil$ is nondecreasing in $n$). If $2^{j - 1} < n \le 2^j$ with $j \ge 1$, then $2^{j - 2} < \lceil n/2 \rceil \le 2^{j - 1}$ (for $j = 1$, $\lceil n/2 \rceil = 1$). By induction $h(n) = 1 + (j - 1) = j = \lceil \log_2 n \rceil$. $\square$

**Theorem 2 (time).** With the two lists sorted once at the start, the algorithm runs in $O(n \log n)$ time.

*Proof.* The two sorts take $O(n \log n)$. At a set $S$, the centre of mass takes $O(|S|)$ arithmetic operations, and by Lemma 2 the four lists of the halves are made by one pass over each list of $S$ with a mark on the sinks of $L$, in $O(|S|)$ time. The sets at one depth are disjoint, so each depth costs $O(n)$, and by Theorem 1 there are $\lceil \log_2 n \rceil + 1$ depths. $\square$

**Theorem 3 (full grid).** Let $n = 4^k$ sinks be the centres of the cells of a $2^k \times 2^k$ grid on a square of side $D$. Then every root-to-sink path has length $D (1 - 2^{-k})$, so the skew under linear delay is zero, and the total wire length is $\frac{3}{2} D (2^k - 1)$. These are the values of the H-tree on the same sinks.

*Proof.* By induction on $k$. For $k = 0$ the tree is one sink, with length 0 and wire 0. Let $k \ge 1$ and put the square at $[0, D]^2$. The order on axis 0 lists the sinks column by column, so the low half of size $4^k / 2$ is the left $2^{k - 1}$ columns. Its centre of mass is $(D/4, D/2)$ by symmetry, at distance $D/4$ from the root at $(D/2, D/2)$; the right half is the mirror. Each half is split on axis 1, and the low half of the left half is its lower $2^{k - 1}$ rows, a $2^{k - 1} \times 2^{k - 1}$ grid on the square $[0, D/2]^2$, with centre $(D/4, D/4)$ at distance $D/4$ from $(D/4, D/2)$. The other three quarters are the same up to symmetry. So two levels add $D/4 + D/4 = D/2$ to every path and $2 \cdot D/4 + 4 \cdot D/4 = \frac{3}{2} D$ to the wire, and leave four copies of the problem with $k - 1$ and side $D/2$, whose next split is again on axis 0. The path length is $D/2 + (D/2)(1 - 2^{-(k-1)}) = D (1 - 2^{-k})$, and the wire is $\frac{3}{2} D + 4 \cdot \frac{3}{2} \frac{D}{2} (2^{k - 1} - 1) = \frac{3}{2} D (2^k - 1)$. $\square$

**Remark (no zero skew in general).** The sinks $(0, 6)$, $(0, 7)$, $(2, 3)$ and $(8, 6)$ give path lengths 4, 4, 8 and 8, as computed on the page, so Theorem 3 does not extend to arbitrary sinks.
