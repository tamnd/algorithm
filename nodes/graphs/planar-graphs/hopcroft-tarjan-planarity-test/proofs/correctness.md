---
title: Correctness of the Hopcroft-Tarjan planarity test
proves: [correctness, termination]
status: full
---

The proof follows the segment formulation of Mehlhorn. Line numbers refer to the pseudocode on the main page.

## Reduction to one block

**Lines L1 and L2.** A simple planar graph with $n \ge 3$ vertices has at most $3n - 6$ edges ([planar edge bound](/planar-edge-bound/)), so line L1 never rejects a planar graph. A graph is planar if and only if each of its biconnected components is planar: one direction holds because subgraphs of planar graphs are planar; for the other, embeddings of the blocks can be glued at cut vertices, one block at a time, by putting the block on the outer face of its cut vertex in the drawing so far. A block with at most 4 vertices is a subgraph of $K_4$, which is planar. So it suffices to show that lines L3 to L6 accept a biconnected graph $B$ with $k \ge 5$ vertices exactly when $B$ is planar.

## The palm tree

Fix the DFS of line L3; vertices are their preorder numbers, and $T(v)$ is the subtree of $v$. In an undirected DFS every non-tree edge joins a vertex and one of its ancestors, so it becomes a back arc $v \to w$ with $w$ a proper ancestor of $v$ that is not its parent.

**Fact 1.** In a biconnected graph with at least 3 vertices, vertex 0 has the single child 1, every vertex $v \ge 1$ has an arc other than the arc from its parent, and $\mathrm{lowpt}_1(c) < p$ for every tree arc $p \to c$ with $p \ne 0$.

*Proof.* A root with two children is a cut vertex. A vertex $v \ge 1$ of degree 1 would make its neighbour a cut vertex. If $\mathrm{lowpt}_1(c) \ge p$ for $p \ne 0$, then no back arc leaves $T(c)$ above $p$, and $p$ separates $T(c)$ from $0$. $\square$

**Fact 2 (spines).** After the sort of line L5, the first arc out of every vertex $v \ge 1$ goes to a child $c$ with $\mathrm{lowpt}_1(c) = \mathrm{lowpt}_1(v)$, or is a back arc to $\mathrm{lowpt}_1(v)$. So line L8 is well defined, the spine of $x \to y$ ends with a back arc $w_k \to w_0$ where $w_0 = \mathrm{lowpt}_1(y)$, every vertex on the spine has $\mathrm{lowpt}_1 = w_0$, and $w_0 < x$ unless $x = 0$.

*Proof.* $\mathrm{lowpt}_1(v)$ is the minimum of $v$, of the ends of back arcs out of $v$, and of $\mathrm{lowpt}_1(c)$ over the children. The cost of an arc is $2w$ or $2w + 1$ where $w$ is the end of the back arc or $\mathrm{lowpt}_1(c)$, so the arc of least cost reaches the minimum of these, which is below $v$ by Fact 1. The walk goes down the tree, so it ends; it ends at a back arc. The last statement is Fact 1. $\square$

**Segments and their attachments.** For a tree arc $e = x \to y$, $S(e)$ is $T(y)$ with the arc $e$ and all back arcs out of $T(y)$; its attachments $\mathrm{Att}(e)$ are the ends of those back arcs that are smaller than $y$. For a back arc $e = v \to w$, $S(e)$ is the arc and $\mathrm{Att}(e) = \{w\}$. Every attachment of $S(x \to y)$ lies on the tree path from $w_0$ to $x$, the *stem* $P(e)$, because it is an ancestor of $y$ and at least $\mathrm{lowpt}_1(y) = w_0$. Let $G(e) = S(e) \cup P(e)$.

**Definition.** $S(e)$ is *strongly planar* if $G(e)$ has a planar embedding in which every edge and vertex of $P(e)$ lies on the boundary of the outer face. For $e = 0 \to 1$, $S(e)$ is all of $B$ and $P(e)$ is the single vertex 0, so $B$ is planar if and only if $S(0 \to 1)$ is strongly planar (any face can be made the outer face).

## Decomposition along the spine

Fix a tree arc $e = x \to y$ with spine $w_1, \ldots, w_k$ and closing back arc $w_k \to w_0$. Let $C$ be the cycle formed by the stem, the arc $e$, the spine and the arc $w_k \to w_0$. Call the arcs out of spine vertices that are not on $C$ the *emanating arcs* $e_1, \ldots, e_r$, with segments $S_i = S(e_i)$.

**Fact 3.** $G(e) = C \cup S_1 \cup \cdots \cup S_r$, two different $S_i$ meet only in vertices of $C$, and every $S_i$ meets $C$ exactly in its base (the spine vertex it leaves) and its attachments. So the $S_i$ are the bridges of $C$ in $G(e)$.

*Proof.* The subtrees of the children of spine vertices that are not on the spine are disjoint and disjoint from $C$, and each back arc from them ends at an ancestor at least $w_0$ (by Fact 2 applied to the child, $\mathrm{lowpt}_1 \ge w_0$), which lies on $C$. Each tree-arc segment is connected through its subtree. $\square$

Two bridges $S_i$ and $S_j$ *conflict* if their contact sets with $C$ (base and attachments) have 3 vertices in common, or contain 4 vertices $u_1, u_2, u_3, u_4$ in this cyclic order on $C$ with $u_1, u_3$ in one set and $u_2, u_4$ in the other. This is the classical overlap relation of bridges, and the following facts are the standard bridge lemma.

**Fact 4.** In a planar embedding of $C \cup S_i \cup S_j$ in which $S_i$ and $S_j$ are on the same side of $C$, they do not conflict.

*Proof.* By the [Jordan curve theorem](/jordan-curve-theorem/), $C$ bounds a disc on that side, and $S_i$ and $S_j$ are drawn inside it. In the alternating case, $S_i$ contains a path from $u_1$ to $u_3$ through the disc, which cuts the disc into two parts, with $u_2$ and $u_4$ on different boundary arcs; a path in $S_j$ from $u_2$ to $u_4$ would have to cross it. In the case of 3 common vertices $a, b, c$, each bridge contains a vertex joined to $a, b, c$ by internally disjoint paths (a subdivided claw); two such claws inside a disc with the same 3 ends on the boundary must cross, since the first claw cuts the disc into three regions and no region has all of $a, b, c$ on its boundary. $\square$

**Fact 5.** Suppose bridges $S_1, \ldots, S_q$ pairwise do not conflict, and each $C \cup S_i$ has a planar embedding with $S_i$ inside $C$. Then $C \cup S_1 \cup \cdots \cup S_q$ has a planar embedding with all of them inside $C$.

*Proof.* Induction on $q$. Embed $C \cup S_1 \cup \cdots \cup S_{q-1}$ with all bridges inside. The faces inside $C$ are bounded by arcs of $C$ and paths through bridges. Because $S_q$ conflicts with no $S_i$, all contact vertices of $S_q$ lie on the boundary of one of these faces: if they did not, two of them would be separated by some $S_i$, which gives an alternating quadruple, or all three regions around a branch vertex of $S_i$ would be needed, which gives 3 common contact vertices. This face is a disc whose boundary meets $C$ in an arc that contains all contact vertices of $S_q$ in their order along $C$, so the embedding of $S_q$ inside $C$ can be copied into it, after a homeomorphism of discs that matches the contact vertices. $\square$

**Lemma 1 (decomposition).** $S(e)$ is strongly planar if and only if

1. every $S_i$ is strongly planar, and
2. the bridges $S_1, \ldots, S_r$ can be split into two classes $L$ and $R$ with no conflict inside a class, such that every bridge with an attachment $a$ with $w_0 < a < x$ is in $L$.

*Proof.* (Only if.) Take an embedding of $G(e)$ with the stem on the outer face. By Fact 3 and the Jordan curve theorem, each bridge is drawn inside or outside $C$; let $R$ be the bridges on the side of $C$ that contains the outer face and $L$ the others. By Fact 4 there is no conflict inside a class. A bridge in $R$ with an attachment $a$ strictly inside the stem contains a path from $a$ to its base, which lies off the stem; with $C$, this path cuts the side of $C$ that holds the outer face so that the stem edges before $a$ and after $a$ are on the boundaries of different faces, which contradicts the choice of the embedding. So such bridges are in $L$. For condition 1, restrict the embedding to $C \cup S_i$: the side of $C$ without $S_i$ is a face with all of $C$ on its boundary, so the stem of $S_i$, which is a subpath of $C$ from its lowest attachment to its base, is on the boundary of one face, and $G(e_i)$ is a subgraph whose stem is still on that face.

(If.) For each $S_i$, take an embedding of $G(e_i)$ with its stem $P_i$ on the outer face. The rest of $C$ is a path between the two ends of $P_i$ that avoids $S_i$; draw it in the outer face, close to the boundary, which gives an embedding of $C \cup S_i$ with $S_i$ on one side, and by a reflection on either side. Apply Fact 5 to $L$ inside $C$ and to $R$ outside $C$ (outside is a disc on the sphere). The stem has no attachment from $R$ in its interior, so after the bridges of $R$ are drawn, all stem edges still border one face outside $C$; make it the outer face. $\square$

**Conflicts along the spine.** By Fact 3 and the order of numbers along $C$ (the stem and spine are a tree path with increasing numbers, closed by the arc from $w_k$ to $w_0$), conflict has a simple form. Say $S_j$ is handled after $S_i$ by line L11, so the base $b_j$ of $S_j$ is at most the base $b_i$ of $S_i$. Let $a_j = \min \mathrm{Att}(S_j)$.

**Lemma 2.** $S_i$ and $S_j$ conflict if and only if $S_i$ has an attachment $c$ with $a_j < c < b_j$.

*Proof.* (If.) If $b_j < b_i$, the four vertices $a_j < c < b_j < b_i$ alternate, with $a_j, b_j$ in $S_j$ and $c, b_i$ in $S_i$. If $b_j = b_i = v$, then $S_i$ came first in the sort, so $\mathrm{lowpt}_1$ of $S_i$ is at most $a_j$. If it is smaller, the vertices $\mathrm{lowpt}_1(S_i) < a_j < c < v$ alternate. If it equals $a_j$, then $S_i$ has the attachment $c$ strictly between $a_j$ and $v$, so its cost is odd, and $S_j$, which comes later with the same $\mathrm{lowpt}_1$, has odd cost too: it has an attachment $d$ with $a_j < d < v$. If $c = d$, the common vertices $a_j, c, v$ are three; otherwise $a_j, \min(c, d), \max(c, d), v$ alternate between the two bridges. (A back arc counts as a segment with even cost, which comes first in its bucket.)

(Only if.) Suppose every attachment of $S_i$ is at most $a_j$ or at least $b_j$. All contact vertices of $S_j$ lie in the interval $[a_j, b_j]$ of $C$, and all contact vertices of $S_i$ lie outside the open interval $(a_j, b_j)$. Then two vertices of $S_i$ never separate two vertices of $S_j$ on $C$, and the only possible common vertices are $a_j$ and $b_j$. So they do not conflict. $\square$

## The stack of blocks

Consider one call SEGMENT$(x, y)$. Say that a bridge is *seen* once line L13 has handled it, and that its *live* attachments are those below the current vertex $w$ of line L10. Line L14 removes, when the walk moves from $w$ to its parent, exactly the attachments equal to the parent, so the lists on $S$ hold exactly the live attachments of seen bridges, if each list is sorted with the largest first (removal at the heads then removes all copies of the parent).

**Invariant.** Before and after each call of ADD-BLOCK:

- (a) every list on $S$ is sorted with the largest first;
- (b) each block holds the live attachments of a set of seen bridges, split into left and right lists by a 2-colouring with no conflict inside a colour, and the sets of the blocks are the connected components of the conflict graph of the seen bridges that still have live attachments;
- (c) every attachment in a block is at most every attachment in every block above it.

*Proof that ADD-BLOCK keeps it.* Let the new bridge be $S_j$ with list $A$, sorted by induction (for a back arc, $A$ has one element). Its minimum is $a_j$. While $S$ is not empty, look at the top block $T$ and let $\mu$ be the minimum of the current left list of $B$.

First, $\mu = a_j$ as long as the left list of $B$ has only taken left lists that are empty or have all entries at most $a_j$; and by (c) every entry of a block below $T$ is at most every entry of $T$. So if the loop has combined a block with a nonempty left list, then $\mu$ is the minimum of that list, and every remaining block has all entries at most $\mu$, so the loop ends at line L22 in the next round. Hence the comparisons with $\mu$ give the same result as comparisons with $a_j$ for every block that is compared while it matters.

By Lemma 2, $S_j$ conflicts with a seen bridge exactly when that bridge has a live attachment above $a_j$. (Attachments that are not live are at least the current vertex $w = b_j$, and cannot lie in $(a_j, b_j)$.) So $S_j$ conflicts with some bridge on the left of $T$ if and only if the head of the left list of $T$ exceeds $a_j$, and the same on the right.

- If both sides of $T$ have such a bridge, the component of $T$ with $S_j$ has an odd cycle: a path inside the component between two bridges of different colours has odd length, and $S_j$ closes it with two edges. The conflict graph is not bipartite, and lines L19 and L20 fail. By Lemma 1, $S(e)$ is not strongly planar, and failing is correct.
- If only the left side conflicts, line L19 swaps the sides of $T$, which is another valid colouring of the same component.
- If the right side conflicts after this, $T$ joins the component of $S_j$ on the side opposite to $S_j$, and line L21 merges it: the left lists contain $S_j$ and the non-conflicting colour of $T$, the right lists the conflicting colour. The concatenations stay sorted, because the left list of $T$ has all entries at most $\mu$ (otherwise line L20 would have failed) and the right list of $B$ comes from blocks above $T$, whose entries are at least those of $T$ by (c).
- If neither side conflicts, then by (c) no lower block conflicts either, because all their entries are at most the entries of $T$, which are at most $a_j$. The loop ends.

The pushed block holds $S_j$ and every component that conflicts with it, so (b) holds. Its entries are at least $\mu$, and everything below it is at most $\mu$, so (c) holds. Line L14 removes only heads and pops empty blocks, which keeps (a), (b) and (c): a bridge without live attachments conflicts with no later bridge by Lemma 2. $\square$

**Lemma 3.** Assume that every recursive call made by SEGMENT$(x, y)$ returns the attachments of its segment below its base, sorted, when the segment is strongly planar, and fails otherwise. Then SEGMENT$(x, y)$ does the same for $S(x \to y)$.

*Proof.* If some $S_i$ is not strongly planar, a recursive call fails, and by Lemma 1 so does $S(e)$. Otherwise, by the invariant, line L13 fails exactly when the conflict graph of the bridges is not bipartite; the conflicts are those of Lemma 2, and a bridge whose attachments have all left the lists conflicts with no later bridge, so dropping it changes nothing. If the loop of L10 ends, the conflict graph is bipartite, and the blocks on $S$ are the components of the bridges that still have attachments below $x$; the colouring of each component can be chosen independently, up to a swap. A bridge with an attachment strictly between $w_0$ and $x$ is a bridge with a live entry above $w_0$ at the end. Condition 2 of Lemma 1 can be met if and only if no component has such bridges in both colours, which is the test of line L15. So line L15 fails exactly when $S(e)$ is not strongly planar.

When it does not fail, line L16 returns the attachments of $S(e)$ below $x$: in each block, the list with no entry above $w_0$ contains only copies of $w_0$, since all live entries are at least $w_0$, so taking the other list loses only copies of $w_0$, and $w_0$ is appended when $w_0 \ne x$. The result is sorted by (a) and (c). The bridges whose attachments all left the lists contribute attachments at least $x$, which are not attachments of $S(e)$ below $x$. $\square$

**Theorem.** HT-PLANAR returns true if and only if $G$ is planar.

*Proof.* By induction on the size of the subtree of $y$, Lemma 3 holds for every call; the innermost calls have only back arcs as bridges, where the hypothesis on recursive calls is empty. For the call SEGMENT$(0, 1)$, the segment is the whole block, so line L6 fails exactly when the block is not planar. With the reduction to blocks, the algorithm returns true exactly when every block, and so the graph, is planar. $\square$

## Termination

The search, the low points and the sort are finite loops. Each tree arc starts at most one call of SEGMENT, and each call walks a finite spine. Each round of the loop in ADD-BLOCK either pops a block or leaves the loop, and each block is pushed once. Line L14 deletes list entries, which were created once each. So the algorithm stops, in $O(n + m)$ steps by the count on the main page. $\blacksquare$
