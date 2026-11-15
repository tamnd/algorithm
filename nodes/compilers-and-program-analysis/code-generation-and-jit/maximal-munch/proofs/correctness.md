---
title: Maximal munch gives a valid tiling with no two tiles that combine
proves: [correctness]
status: full
---

We use the pseudocode of the page. A pattern is a tree whose leaves can be holes. A hole stands for an operand in a register, and every other node of the pattern is an operator, an immediate constant or a variable in memory. When a pattern $p$ matches at a node $v$ of the tree $T$, it *covers* the nodes of $T$ that sit under the non-hole nodes of $p$, and its holes sit on nodes $h_1, \ldots, h_q$. The size $|p|$ is the number of nodes that $p$ covers. A *tiling* of $T_v$ is a pattern that matches at $v$ and a tiling of $T_{h_t}$ for each hole $h_t$.

We assume that the table is *complete*: for each kind of node there is a pattern of size 1 that matches it, with a hole for each child. The table of the page has LI, LD, ADD, MUL and LDR, so it is complete.

**Lemma 1 (termination and validity).** For each node $v$, MUNCH$(v)$ stops and emits a tiling of $T_v$. Each node of $T_v$ is covered by exactly one tile of it, and each tile comes after the tiles of its holes in the code.

*Proof.* By induction on the size of $T_v$. By completeness, at least one pattern matches at $v$, so line L3 chooses a pattern $p$ with $|p| \ge 1$. The pattern $p$ covers $v$ and the nodes under its non-hole nodes. Its holes $h_1, \ldots, h_q$ are proper descendants of $v$, and their subtrees are disjoint and disjoint from the nodes that $p$ covers. Each node of $T_v$ is either covered by $p$ or lies in exactly one subtree $T_{h_t}$. Line L5 calls MUNCH on each $T_{h_t}$, which is smaller than $T_v$. By induction, each call stops and covers each node of $T_{h_t}$ exactly once. Line L6 emits $p$ after these calls, so its operands are in registers when it runs. $\square$

Lemma 1 also shows that the code computes the value of $T$: the instruction of a tile computes the value of the covered part of the tree from the values of its holes, and by induction these values are in the registers that line L5 returns.

**Lemma 2 (no two tiles combine).** Let $p$ be the tile at a node $v$, and let $p'$ be the tile at one of its holes $h$. No pattern of the table matches at $v$ and covers exactly the nodes that $p$ and $p'$ cover together.

*Proof.* Suppose that a pattern $p''$ matches at $v$ and covers the union. The two sets are disjoint and $|p'| \ge 1$, so $|p''| = |p| + |p'| > |p|$. When MUNCH$(v)$ ran line L3, $p''$ also matched at $v$, and line L3 keeps a pattern of the largest size. So the size of the chosen pattern is at least $|p''| > |p|$. This contradicts the choice of $p$. $\square$

**Theorem.** Maximal munch emits a valid tiling of $T$. In this tiling, no two adjacent tiles can be replaced by one tile of the table, so in particular by one tile of lower cost. So the tiling is *optimal* in the sense of Appel.

*Proof.* Lemma 1 and Lemma 2. Two tiles are adjacent when one sits on a hole of the other, and this is the case of Lemma 2. $\blacksquare$

**The tiling need not be optimum.** Take $T = \mathrm{MEM}(\mathrm{ADD}(\mathrm{MUL}(a, b), c))$ with the table of the page. At the root, LDR has size 1, LDO does not match, and LDX has size 2, so MUNCH picks LDX. Then it tiles MUL$(a, b)$ with MUL and the three variables with LD. The cost is $3 + 3 + 3 \cdot 3 = 15$. The tiling LDR, MADD and three LD costs $3 + 2 + 9 = 14$. The tiles LDX and MUL of the munch tiling do not combine into any pattern, so Lemma 2 is not violated. The local property does not give the least total cost.

**Time.** Line L2 tries each pattern at each node where MUNCH runs, and a match takes time proportional to the size of the pattern. MUNCH runs once for each tile, and each tile covers at least one node. So the time is $O(n \cdot P \cdot m)$ for $n$ nodes, $P$ patterns and patterns of at most $m$ nodes. For a fixed table this is linear in $n$.
