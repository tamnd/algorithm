---
title: Clustal returns a valid alignment, and each merge is optimal for its profile score
proves: [correctness]
status: full
---

A *valid alignment* of sequences $(S_r)_{r \in R}$ is a set of rows of equal length over $\Sigma \cup \{-\}$ such that row $r$ with its gaps removed equals $S_r$ and no column consists of gaps only. For a node $v$ of the guide tree $T$, let $R(v)$ be the set of leaves below $v$.

We prove three claims: (1) for every node $v$, $P[v]$ is a valid alignment of $(S_r)_{r \in R(v)}$; (2) PROFILE-ALIGN returns an alignment of its two profiles with the largest total column score $\sum \mathrm{col}$ among all alignments that keep each profile as a block; (3) for $k = 2$ the output is an optimal global alignment of the two sequences.

**Block alignments.** Let $X$ have rows $X_1, \ldots, X_a$ of length $m$ and $Y$ have rows $Y_1, \ldots, Y_b$ of length $n$. A *block alignment* of $X$ and $Y$ is a sequence of columns, each of one of three kinds: $(X[\cdot][i], Y[\cdot][j])$, $(X[\cdot][i], -^b)$ or $(-^a, Y[\cdot][j])$, in which the columns of $X$ appear in order $1, \ldots, m$ once each, and the columns of $Y$ in order $1, \ldots, n$ once each. Block alignments correspond one to one to paths from $(0, 0)$ to $(m, n)$ in the grid with steps $(1, 1)$, $(1, 0)$ and $(0, 1)$, exactly as pairwise alignments of two strings of lengths $m$ and $n$ do, with the column of $X$ in place of a letter.

**Claim (2).** Let $F[i][j]$ be the largest total of $\mathrm{col}$ over block alignments of the first $i$ columns of $X$ and the first $j$ columns of $Y$. The last column of such a block alignment is of one of the three kinds, and removing it leaves a block alignment of the prefixes $(i-1, j-1)$, $(i-1, j)$ or $(i, j-1)$. The score is additive over columns, so

$$F[i][j] = \max\big(F[i-1][j-1] + \mathrm{col}(X_i, Y_j),\ F[i-1][j] + \mathrm{col}(X_i, -^b),\ F[i][j-1] + \mathrm{col}(-^a, Y_j)\big),$$

with $F[0][0] = 0$ and the boundary rows filled by the only possible steps. This is the recurrence of PROFILE-ALIGN. By induction on $i + j$ every entry is correct. The traceback follows, from $(m, n)$, a step whose term equals the current entry, so it rebuilds a path of total $F[m][n]$, which is the largest total.

**Claim (1).** By induction over the postorder of line L6. For a leaf $v$, $P[v]$ is the one-row alignment of $S_v$; it is valid because a sequence alone has no gaps. Let $v$ have children $u, u'$, and assume $P[u]$ and $P[u']$ are valid. PROFILE-ALIGN returns a block alignment $N$ of $X = P[u]$ and $Y = P[u']$. Each row of $X$ appears in $N$ with its symbols in their order and gaps added (the columns of the third kind), so it still spells its sequence; the same holds for $Y$. The rows of $N$ have equal length, the number of columns. A column of the first or second kind contains a column of $X$, which has a letter because $X$ is valid; a column of the third kind contains a column of $Y$, which has a letter. So $N$ has no column of gaps only, and $P[v] = N$ is a valid alignment of $(S_r)_{r \in R(v)}$, since $R(v) = R(u) \cup R(u')$. Line L8 reorders rows, which keeps validity. With $v$ the root, $R(v)$ is all of $\{1, \ldots, k\}$.

**Claim (3).** For $k = 2$ the tree has one internal node, the root, with the two leaves as children. Both profiles have one row, with weights $w_1$ and $w_2$ (or 1 and 1 when the weights are 0). Then

$$\mathrm{col}(x, y) = \frac{w_1 w_2\, s(x, y)}{w_1 w_2} = s(x, y)$$

for single symbols, including a gap against a letter. Block alignments of two one-row profiles are exactly the pairwise alignments of the two sequences, so by Claim (2) the output maximizes $\sum_p s(A_1[p], A_2[p])$, the global alignment score. $\blacksquare$
