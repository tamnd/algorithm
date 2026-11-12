---
title: MAFFT returns a valid alignment, and each merge is optimal among the merges through its anchors
proves: [correctness]
status: full
---

A *valid alignment* of sequences $(S_r)_{r \in R}$ is a set of rows of equal length over $\Sigma \cup \{-\}$ such that row $r$ with its gaps removed equals $S_r$, and no column consists of gaps only. Let $X$ have columns $X_1, \ldots, X_m$ and $Y$ have columns $Y_1, \ldots, Y_n$. A *block alignment* of $X$ and $Y$ is a sequence of columns, each of the form $(X_i, Y_j)$, $(X_i, \text{gaps})$ or $(\text{gaps}, Y_j)$, in which $X_1, \ldots, X_m$ appear once each in order, and so do $Y_1, \ldots, Y_n$. It *matches* $(i, j)$ if it has the column $(X_i, Y_j)$. Its score is the sum of $\mathrm{col}$ over its columns, where $\mathrm{col}$ is the average pair score between the two parts of a column.

We prove: (1) the anchors $(i_1, j_1), \ldots, (i_r, j_r)$ of line L10 satisfy $i_1 < \cdots < i_r$ and $j_1 < \cdots < j_r$; (2) GROUP-ALIGN returns a block alignment of $X$ and $Y$ that matches every anchor and has the largest score among all such block alignments; (3) the output of MAFFT-FFT-NS-2 is a valid alignment of the input.

**Claim (1).** A segment $(i, j, \lambda)$ covers the column pairs $(i + t, j + t)$ for $0 \le t < \lambda$, and its center is $(i + \lfloor \lambda/2 \rfloor, j + \lfloor \lambda/2 \rfloor)$, which is one of them because $0 \le \lfloor \lambda/2 \rfloor < \lambda$ for $\lambda \ge 1$. The chain of line L9 orders its segments so that each next segment $(i', j', \lambda')$ satisfies $i + \lambda \le i'$ and $j + \lambda \le j'$. Then the first coordinate of the center of the earlier segment is at most $i + \lambda - 1 < i'$, which is at most the first coordinate of the center of the later one; the same holds for the second coordinate.

**Claim (2).** Put $(i_0, j_0) = (0, 0)$ and $(i_{r+1}, j_{r+1}) = (m + 1, n + 1)$, and call region $t$ the columns $X_{i_t + 1}, \ldots, X_{i_{t+1} - 1}$ and $Y_{j_t + 1}, \ldots, Y_{j_{t+1} - 1}$, for $t = 0, \ldots, r$. By Claim (1) the regions are well defined and cover every column that is not an anchor.

Let $B$ be a block alignment that matches every anchor. Cut $B$ just before and just after each anchor column $(X_{i_t}, Y_{j_t})$. Because the columns of $X$ appear in order, the columns of $B$ strictly between the anchor columns $t$ and $t+1$ use exactly the columns of $X$ with index between $i_t$ and $i_{t+1}$, and the same for $Y$. So that piece of $B$ is a block alignment of region $t$. Conversely, any choice of one block alignment $B_t$ per region, joined in order with the anchor columns between them, is a block alignment of $X$ and $Y$ that matches every anchor. This is a bijection between the block alignments through the anchors and the tuples $(B_0, \ldots, B_r)$, and

$$\mathrm{score}(B) = \sum_{t=0}^{r} \mathrm{score}(B_t) + \sum_{t=1}^{r} \mathrm{col}(X_{i_t}, Y_{j_t}).$$

The second sum does not depend on $B$, so $B$ has the largest score if and only if each $B_t$ has the largest score among block alignments of region $t$. Line L11 computes each $B_t$ by the profile dynamic program. Its table entry $F[a][b]$ is the best score of a block alignment of the first $a$ columns and the first $b$ columns of the region; the last column of such an alignment is one of the three kinds, and removing it leaves a block alignment of a shorter prefix pair, so

$$F[a][b] = \max\big(F[a-1][b-1] + \mathrm{col}(X'_a, Y'_b),\ F[a-1][b] + \mathrm{col}(X'_a, \text{gaps}),\ F[a][b-1] + \mathrm{col}(\text{gaps}, Y'_b)\big),$$

and induction on $a + b$ shows that every entry is correct. The traceback follows terms equal to the current entry from the last cell to $F[0][0]$, so it returns a block alignment with the best score. Line L12 joins the pieces and the anchor columns in order, which is the optimal $B$.

**Claim (3).** A block alignment $N$ of a valid alignment $X$ of $(S_r)_{r \in R_X}$ and a valid alignment $Y$ of $(S_r)_{r \in R_Y}$, with $R_X \cap R_Y = \emptyset$, is a valid alignment of $(S_r)_{r \in R_X \cup R_Y}$. Indeed, each row of $X$ appears in $N$ with its symbols in order and gaps inserted, so it still spells its sequence; the same holds for $Y$; the rows of $N$ all have one symbol per column; and every column of $N$ contains a column of $X$ or of $Y$, which has a letter. PROGRESSIVE starts at the leaves with the one-row alignment of each sequence, which is valid, and at each internal node applies GROUP-ALIGN to the alignments of its two children, whose leaf sets are disjoint. By Claim (2) the result is a block alignment, so by induction over the tree, the alignment at the root is a valid alignment of all $k$ sequences. This holds for both passes, lines L3 and L5, whatever the trees are. Line L6 only reorders rows.

For two single sequences with no anchors, Claim (2) says that the merge is a best block alignment of two one-row groups, which is an optimal pairwise alignment, because $\mathrm{col}(a, b) = s(a, b)$. $\blacksquare$
