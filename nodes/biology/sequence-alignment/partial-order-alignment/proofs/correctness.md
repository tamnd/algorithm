---
title: Partial order alignment finds the best path alignment at each step and returns a valid multiple alignment
proves: [correctness]
status: full
---

A *valid alignment* of $S_1, \ldots, S_k$ is a list of rows of equal length over $\Sigma \cup \{-\}$ such that row $r$ with its gaps removed equals $S_r$, and no column consists of gaps only. A *full path* of the graph $G$ is a path $v_1 \to \cdots \to v_p$ along edges of $G$ in which $v_1$ has no predecessors and $v_p$ has no successors. An alignment of a sequence $y$ with a full path is a pairwise alignment of $y$ with the string $\mathrm{base}(v_1) \cdots \mathrm{base}(v_p)$, scored with $s$ for two letters and $g$ for a letter against a gap.

We prove: (1) ALIGN returns, for a nonempty graph, an alignment of $y$ with a full path of largest score, and for the empty graph the alignment of $y$ against gaps only; (2) after each fusion the graph keeps invariants I1 to I3 below; (3) the output is a valid alignment of the input; (4) for $k = 2$ the output is an optimal pairwise alignment.

The invariants, for the sequences added so far:

- **I1.** The path of $S_r$ is a list of nodes whose letters spell $S_r$, and each two consecutive nodes of it are joined by an edge.
- **I2.** The columns have a linear order, and every edge goes from a column to a strictly later column.
- **I3.** Every node lies on the path of at least one sequence.

**Claim (1).** For the empty graph the only alignment puts every letter against a gap, which is what ALIGN returns. Otherwise, by I2 the nodes, listed column by column, are in topological order, so every predecessor of $v$ is filled before $v$. For a node $v$ and $0 \le j \le |y|$, let $H^*[v][j]$ be the best score of an alignment of $y_1 \ldots y_j$ with a path that ends at $v$ and starts at a node without predecessors. The last column of such an alignment is one of three kinds: $v$ against $y_j$, $v$ against a gap, or $y_j$ against a gap. In the third case, removing the column leaves an alignment of $y_1 \ldots y_{j-1}$ with the same path, so the best value is $H^*[v][j-1] + g$. In the first two cases, removing the column leaves an alignment of $y_1 \ldots y_{j-1}$ or $y_1 \ldots y_j$ with the path before $v$. If $v$ has predecessors, that path ends at one of them, $u$, and the best value is $H^*[u][j-1] + s(v, y_j)$ or $H^*[u][j] + g$. If $v$ has no predecessors, the path before $v$ is empty, and the best alignment of $y_1 \ldots y_i$ with the empty path is $i \cdot g$, the start row. Conversely, every term of the recurrence is the score of such an alignment. The score is a sum over columns, so $H^*$ satisfies the recurrence of line L3, and by induction over the order of the cells (topological order of $v$, then increasing $j$), $H = H^*$. A full path ends at a node without successors, so line L4 takes the best full path alignment. The traceback follows, from each cell, a term that attains its value, so it rebuilds an alignment with that score along edges of $G$.

**Claim (2).** All three invariants hold for the empty graph. Suppose they hold before $S_r$ is added, and let the alignment from ALIGN list the pairs in path order. Let $w_1, \ldots, w_q$ be the nodes that fusion assigns to the letters of $S_r$, in order.

I1. Each letter $y_j$ gets one node $w$ with $\mathrm{base}(w) = y_j$: line L5 picks or creates a node with letter $y_j$, and line L6 creates one. Line L7 adds the edges $w_i \to w_{i+1}$. So I1 holds for $S_r$, and it still holds for the earlier sequences, because fusion removes no node or edge.

I2. Write $c(w)$ for the column of $w$, and $\prec$ for the column order. We show $c(w_i) \prec c(w_{i+1})$ for every new edge. Walk along the pairs and keep the column $\ell$ of the last node met, whether it was matched, against a gap or inserted. Path nodes of the graph come in the order of a path in $G$, so by I2 their columns strictly increase. A node from line L5 sits in the column of its path node. A node from line L6 sits in a new column placed right after $\ell$, and so before the column of every later path node, because those columns come strictly after $\ell$; and a later inserted node gets a column right after this new one. So, along the pairs, the columns met strictly increase, and the edge $w_i \to w_{i+1}$ goes forward. Old edges keep their columns, and inserting a new column into the order does not change the order of the old ones.

I3. Every new node is a node $w_i$ of $S_r$, and old nodes keep their paths.

**Claim (3).** Line L8 writes, in row $r$ and column $c$, the letter of the node of $S_r$ in $c$, or a gap. This is well defined: by I2 and I1 the columns of $w_1, \ldots, w_q$ strictly increase, so $S_r$ has at most one node in each column. Reading row $r$ from left to right then gives the letters of $w_1, \ldots, w_q$ in order, which by I1 spell $S_r$. All rows have one entry per column, so they have equal length. Every column was created for a node, and by I3 that node lies on the path of some sequence, whose row has a letter there; so no column consists of gaps only.

**Claim (4).** For $k = 2$ the graph of $S_1$ is a chain $v_1 \to \cdots \to v_m$, and its only full path spells $S_1$. By Claim (1), ALIGN returns an optimal pairwise alignment of $S_2$ with $S_1$. Fusion maps it to columns one to one: a pair $(v_i, y_j)$ puts $y_j$ in the column of $v_i$, a pair $(v_i, -)$ leaves row 2 empty in that column, and an inserted $y_j$ gets its own column, placed between the columns of its neighbors on the path, with a gap in row 1. So the two output rows are exactly that alignment, and their score is the optimum. $\blacksquare$
