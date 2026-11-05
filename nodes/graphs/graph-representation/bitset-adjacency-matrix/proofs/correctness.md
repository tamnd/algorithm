---
title: The operations of a bitset adjacency matrix keep the invariant and store the edge set of the graph type
proves: [correctness, termination]
status: full
---

Write $W = \lceil n/w \rceil$ and $\beta(u, v)$ for bit $v \bmod w$ of the word $R[u][\lfloor v/w \rfloor]$, with bit 0 the least significant. For $0 \le v < n$ the map $v \mapsto (\lfloor v/w \rfloor, v \bmod w)$ is one-to-one onto the non-padding positions of a row, so the rows define an $n \times n$ 0-1 matrix $A$ with $A[u][v] = \beta(u, v)$. The structure stands for the graph whose [adjacency matrix](/adjacency-matrix/) is $A$. Invariant (B) is (B1), all padding bits are 0, and (B2), $A$ is symmetric with a zero diagonal when the graph is undirected; (B2) is the invariant (M) of the adjacency matrix.

**Lemma 1 (single bits).** For $0 \le b < w$ and a word $x$: $x \text{ OR } 2^b$ has bit $b$ set and all other bits as in $x$; $x \text{ AND NOT } 2^b$ has bit $b$ clear and all other bits as in $x$; and $(x \gg b) \text{ AND } 1$ is bit $b$ of $x$.

*Proof.* The word $2^b$ has only bit $b$ set, and OR and AND act bit by bit. Shifting right by $b$ moves bit $b$ to position 0, and AND with 1 keeps only position 0. $\square$

**Lemma 2 (lowest bits).** For a word $x \neq 0$ with lowest set bit $b$, the word $x \text{ AND } (x - 1)$ equals $x$ with bit $b$ cleared, and $x \text{ AND } (-x) = 2^b$.

*Proof.* The bits of $x$ below $b$ are 0. Subtracting 1 turns bit $b$ to 0, the bits below $b$ to 1, and leaves the bits above $b$ unchanged, so the AND keeps the bits above $b$ and clears bit $b$ and the bits below it, which were 0. In two's complement $-x = \text{NOT } x + 1$, which has bit $b$ set, the bits below $b$ zero, and the bits above $b$ inverted, so the AND is $2^b$. $\square$

**Theorem.** Assume that before an operation (B) holds and $A$ is the adjacency matrix of the graph that the [graph](/graph/) type prescribes. Then after the operation the same holds for the new graph, each query returns the answer of the graph type, and each operation stops.

*Proof.* *NEW (line L1)* makes all words zero, so $A = 0$, which is the empty graph, and (B) holds.

*ADD-EDGE and REMOVE-EDGE (lines L2 to L5).* By Lemma 1 each line changes exactly the bit $\beta(u, v)$, or $\beta(v, u)$, and no other bit. These bits are not padding bits since $u, v < n$, so (B1) holds. On the matrix $A$, the lines are exactly lines L2 to L5 of the adjacency matrix, whose proof shows that $A$ becomes the matrix of the new graph and that (B2) holds.

*ADJACENT (line L6)* returns $\beta(u, v) = A[u][v]$ by Lemma 1, which is the right answer by the adjacency matrix proof.

*NEIGHBORS (lines L7 to L11).* Fix a word $j$. By Lemma 2, each pass of the loop of lines L9 to L11 outputs $jw + b$ for the lowest set bit $b$ of $x$ and then clears that bit. So the passes output the set bits of $R[u][j]$ in increasing order, each once, and the loop stops after as many passes as $R[u][j]$ has set bits. By (B1) the outputs are below $n$, and they are exactly the $v$ with $\lfloor v/w \rfloor = j$ and $A[u][v] = 1$. Over $j = 0, \ldots, W - 1$ in order, the output is the set $\{v : A[u][v] = 1\}$ in increasing order, which is the set of (out-)neighbours of $u$.

*DEGREE and COMMON (lines L12 and L13).* POPCOUNT of a word counts its set bits. By (B1) the set bits of row $u$ are exactly the positions of its neighbours, so line L12 returns the degree. The AND of word $j$ of rows $u$ and $v$ has bit $b$ set exactly when both rows have it, so the sum in line L13 is $|\{x : A[u][x] = A[v][x] = 1\}| = |N(u) \cap N(v)|$.

*ADD-VERTEX (lines L14 and L15).* If $n$ is a multiple of $w$, the old rows have no padding and exactly $W$ words, and the new column $n$ is bit 0 of a new word, which line L14 appends as zero. Otherwise column $n$ is a padding bit of the last word, which is 0 by (B1). Either way the new column of $A$ is zero, and line L15 adds a zero row of the right length. So the old cells of $A$ keep their values, the new vertex has no edges, all padding bits are still 0, and $A$ stays symmetric with zero diagonal when it was. The loops of lines L1, L14 and L15 run over finitely many words, so they stop.

By induction on the number of operations, starting with NEW, (B) holds and $A$ is the matrix of the current graph after each operation, so each query answers for the current edge set. $\blacksquare$
