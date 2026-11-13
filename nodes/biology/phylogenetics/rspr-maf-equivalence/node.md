---
tag: J6TD60
kind: theorem
slug: rspr-maf-equivalence
name: rSPR distance equals maximum agreement forest size
area: biology/phylogenetics
level: research
summary: For rooted binary trees, the rSPR distance equals the size of a maximum agreement forest minus one, once a leaf rho is added above both roots (Bordewich and Semple 2005).
prereqs: [spr-distance, maximum-agreement-forest]
see_also: [subtree-prune-and-regraft, tree-bisection-and-reconnection, maximum-agreement-subtree, phylogenetic-network, fixed-parameter-tractable, np-hard]
sources:
  - paper: doi:10.1007/s00026-004-0229-z
    title: M. Bordewich and C. Semple, On the computational complexity of the rooted subtree prune and regraft distance, Annals of Combinatorics 8, 2005, 409-423
    locator: the root leaf convention and the theorem that the rSPR distance equals the maximum agreement forest size minus one, with its proof
  - paper: doi:10.1007/s00026-001-8006-8
    title: B. L. Allen and M. Steel, Subtree transfer operations and their induced metrics on evolutionary trees, Annals of Combinatorics 5, 2001, 1-15
    locator: the unrooted analogue for TBR, and the example that refutes the same claim for unrooted SPR
  - paper: doi:10.1016/S0166-218X(96)00062-5
    title: J. Hein, T. Jiang, L. Wang and K. Zhang, On the complexity of comparing evolutionary trees, Discrete Applied Mathematics 71, 1996, 153-169
    locator: the first definition of agreement forests and the original claim for unrooted subtree transfer
  - paper: doi:10.1137/110845045
    title: C. Whidden, R. G. Beiko and N. Zeh, Fixed-parameter algorithms for maximum agreement forests, SIAM Journal on Computing 42(4), 2013, 1431-1466
    locator: the agreement forest algorithms that compute the rSPR distance through this theorem
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 2, restrictions, rearrangement operations and agreement forests
---

The rooted subtree prune-and-regraft distance between two rooted binary [phylogenetic trees](/phylogenetic-tree/) equals the least number of pieces in a rooted [maximum agreement forest](/maximum-agreement-forest/) minus one. The forest must be taken after a new leaf $\rho$ is joined above the root of both trees. Bordewich and Semple proved this in 2005. It turns the [SPR distance](/spr-distance/), which counts moves, into a static cutting problem, and nearly all exact and approximate rSPR algorithms are built on it. Without $\rho$ the equality is false, and for unrooted SPR no such equality holds at all.

## Statement

Let $X$ be a finite set of labels, and let $T_1$ and $T_2$ be rooted binary phylogenetic trees on $X$. For a rooted tree $T$, the tree $T^\rho$ has a new root whose two children are the root of $T$ and a new leaf $\rho \notin X$. For $L \subseteq X \cup \{\rho\}$, the restriction $T^\rho|L$ is the smallest subtree that connects $L$, with nodes of degree 2 suppressed. The subgraph $T^\rho(L)$ is the same subtree before suppression.

A *rooted agreement forest* of $T_1$ and $T_2$ is a partition $F = \{L_\rho, L_1, \ldots, L_k\}$ of $X \cup \{\rho\}$, with $\rho \in L_\rho$, such that

1. $T_1^\rho|L = T_2^\rho|L$ as rooted leaf-labelled trees, for every block $L \in F$, and
2. the subgraphs $T_1^\rho(L)$ for $L \in F$ are pairwise vertex-disjoint, and so are the subgraphs $T_2^\rho(L)$.

Write $m(T_1, T_2)$ for the least number of blocks of a rooted agreement forest.

**Theorem** (Bordewich and Semple 2005). For all rooted binary phylogenetic trees $T_1$ and $T_2$ on $X$,

$$d_{\mathrm{rSPR}}(T_1, T_2) = m(T_1, T_2) - 1.$$

## In plain words

Instead of counting moves, you can count cuts. Add one extra leaf at the very top of both trees, to pin down where the root is. Then cut the first tree into pieces so that each piece looks the same in the second tree, and the pieces do not overlap in either tree.

The theorem says that the fewest cuts you need is the same as the fewest moves. Each move cuts one branch and glues it somewhere else, so a list of moves tells you where to cut. In the other direction, a set of cuts tells you which branches to move, and one move per cut is enough.

The extra top leaf is not a detail. Without it, a tree can be cut into matching pieces too cheaply, because the pieces ignore where the root sits.

## Proof

For a rooted tree, name each vertex by its cluster, the set of leaves below it. Then a vertex $u$ lies in $T(L)$ if and only if the cluster of $u$ meets $L$ and lies inside the cluster of the lowest common ancestor of $L$. The proof has two lemmas and two inequalities.

**Lemma 1.** Let $F$ be an agreement forest with at least two blocks. Then some block $L_j \ne L_\rho$ is a cluster of $T_1$.

*Proof.* Among the blocks other than $L_\rho$, choose $L_j$ whose lowest common ancestor $x_j$ in $T_1$ has an inclusion-minimal cluster. Suppose a leaf $\ell \in L_y$, $y \ne j$, lies below $x_j$. If $y = \rho$, the path from $\ell$ to $\rho$ lies in $T_1^\rho(L_\rho)$ and passes through $x_j$, which lies in $T_1^\rho(L_j)$. This breaks condition 2. If $y \ne \rho$, the lowest common ancestor $x_y$ of $L_y$ is an ancestor of $\ell$, so $x_y$ and $x_j$ are comparable. By the choice of $j$, $x_y$ is not strictly below $x_j$, and $x_y \ne x_j$ by condition 2. So $x_y$ is strictly above $x_j$, and the path from $\ell$ up to $x_y$ passes through $x_j$, which again breaks condition 2. So the leaves below $x_j$ are exactly $L_j$. $\square$

**Lemma 2.** Let $F$ be an agreement forest and $L_j \ne L_\rho$ a block. Let $v$ be the lowest common ancestor of $L_j$ in $T_2^\rho$. Walk from $v$ toward $\rho$, and let $w$ be the first vertex after $v$ that lies in a piece $T_2^\rho(L_h)$. Then $w$ exists, and one of the following holds.

- (a) $w = \rho$ and $L_h = \{\rho\}$. Then $T_2^\rho|(L_j \cup \{\rho\})$ is $T_2|L_j$ with $\rho$ as the sibling of its root.
- (b) $w$ is a vertex of $T_2$, and $A = w \cap L_h$ is a cluster of $T_2^\rho|L_h$ with $\emptyset \ne A \ne L_h$ and $\rho \notin A$. Then $T_2^\rho|(L_h \cup L_j)$ is $T_2^\rho|L_h$ with $T_2|L_j$ joined on the edge above $A$.

In both cases $T_2^\rho(L_h \cup L_j)$ lies inside $T_2^\rho(L_h) \cup T_2^\rho(L_j)$ together with the inner vertices of the path from $v$ to $w$, and those inner vertices lie in no piece.

*Proof.* The walk ends at $\rho \in T_2^\rho(L_\rho)$, so $w$ exists. Let $r$ be the root of $T_2^\rho$ and $c$ the root of $T_2$. If $w = r$, then $h = \rho$ and $L_\rho$ has a leaf $x \in X$. The path from $x$ to $\rho$ passes through $c$, so $c \in T_2^\rho(L_\rho)$. But $c$ comes before $r$ on the walk, or $c = v$, which lies in $T_2^\rho(L_j)$. Both contradict the choice of $w$ or condition 2. So $w \ne r$. If $w = \rho$, then $r$ lies in no piece. Since $r$ lies on the path from $\rho$ to any other leaf, $L_\rho = \{\rho\}$, and case (a) holds. Otherwise $w$ is a strict ancestor of $v$ in $T_2$. Let $c'$ be its child on the walk. If $c'$ had a leaf of $L_h$ below it, then $c'$ would lie in $T_2^\rho(L_h)$, because $c' \subseteq w$ and $w$ lies inside the cluster of the lowest common ancestor of $L_h$. But $c'$ is $v$ or an earlier vertex of the walk. So all leaves of $L_h$ below $w$ lie below its other child, and $A = w \cap L_h$ is not empty because $w$ lies in the piece. If $A = L_h$, then $w$ would be the lowest common ancestor of $L_h$, whose two children both have leaves of $L_h$ below them, and $c'$ has none. So $A \ne L_h$. As $w \subseteq X$, $\rho \notin A$. The clusters of $T_2^\rho|(L_h \cup L_j)$ are the sets $C \cap (L_h \cup L_j)$. The vertex $c'$ gives the cluster $L_j$ and $w$ gives $A \cup L_j$, so $L_j$ hangs on the edge above $A$. The union of the two pieces and the path is connected and holds all the leaves, so it contains $T_2^\rho(L_h \cup L_j)$. By the choice of $w$, the inner vertices of the path lie in no piece. $\square$

**Part 1: $d_{\mathrm{rSPR}} \le m - 1$.** Induction on the number of blocks $m$ of an agreement forest $F$. If $m = 1$, condition 1 for the block $X \cup \{\rho\}$ gives $T_1 = T_2$. Let $m \ge 2$. If $T_1 = T_2$ there is nothing to show. Otherwise take $L_j$ from Lemma 1. It is not $X$, since $L_j = X$ would give $T_1 = T_1|X = T_2|X = T_2$. Prune the subtree on $L_j$ from $T_1$, which leaves a tree $R$ on $X - L_j$. Take $w$, $h$ and $A$ from Lemma 2. In case (a), regraft $L_j$ above the root of $R$. In case (b), let $q$ be the lowest common ancestor of $A$ in $R$, and regraft $L_j$ on the edge above $q$, or above the root if $q$ is the root of $R$. Call the result $T_1'$. This is one rSPR move. Let $F'$ be $F$ with $L_j$ and $L_h$ merged. Then $F'$ is an agreement forest of $T_1'$ and $T_2$, for these reasons.

- *Condition 1.* A block $L$ other than the merged one misses $L_j$, and moving the subtree on $L_j$ does not change the restriction to $L$. So $T_1'^\rho|L = T_1^\rho|L = T_2^\rho|L$. For the merged block, note that $A$ is a cluster of $T_1^\rho|L_h = T_2^\rho|L_h$, so some cluster of $R$ meets $L_h$ in exactly $A$, and therefore $q \cap L_h = A$. In $T_1'$ the parent of $L_j$ has the cluster $q \cup L_j$. So $T_1'^\rho|(L_h \cup L_j)$ is $T_1^\rho|L_h$ with $T_1|L_j$ on the edge above $A$, which is $T_2^\rho|(L_h \cup L_j)$ by Lemma 2. Case (a) is the same with $\rho$ as the sibling.
- *Condition 2 in $T_2$.* By Lemma 2, the new piece only adds vertices that lie in no other piece.
- *Condition 2 in $T_1'$.* The pieces of the other blocks are those of $T_1$, with the parent of the pruned subtree suppressed if it lay on one of them. In case (b), $q$ meets $L_h$ and is not the lowest common ancestor of $L_h$, because $q \cap L_h = A \ne L_h$. So the edge above $q$ in $R^\rho$ is an edge of the piece of $L_h$. The new vertex on it touches no other piece. In case (a), the new vertex and the root of $T_1'^\rho$ lie above every piece whose leaves are in $X$, and the only other piece through the root would hold $\rho$.

So $F'$ has $m - 1$ blocks, and by induction $d_{\mathrm{rSPR}}(T_1', T_2) \le m - 2$. With the first move, $d_{\mathrm{rSPR}}(T_1, T_2) \le m - 1$.

**Part 2: $m - 1 \le d_{\mathrm{rSPR}}$.** Induction on $d = d_{\mathrm{rSPR}}(T_1, T_2)$. If $d = 0$, the single block $X \cup \{\rho\}$ is an agreement forest. Let $d \ge 1$, and let the first move of a shortest sequence prune the subtree with leaf set $P$ from $T_1$ and give $T_1'$, with $d(T_1', T_2) = d - 1$. By induction there is an agreement forest $F'$ of $T_1'$ and $T_2$ with at most $d$ blocks. Let $e'$ be the edge above $P$ in $T_1'^\rho$. A block that meets both $P$ and its complement has its piece crossing $e'$, and by condition 2 at most one block $L^*$ does so. Replace $L^*$ by $L^* \cap P$ and $L^* - P$, and call the result $F$. It has at most $d + 1$ blocks, and $\rho$ is still in one of them.

- *Condition 1.* Every block of $F$ lies inside $P$ or inside $(X \cup \{\rho\}) - P$. The move does not change the restriction of $T^\rho$ to either side, so $T_1^\rho|L = T_1'^\rho|L$. For a part of $L^*$, restrict $T_1'^\rho|L^* = T_2^\rho|L^*$ further.
- *Condition 2 in $T_2$.* The set $L^* \cap P$ is a cluster of $T_1'^\rho|L^* = T_2^\rho|L^*$. So in $T_2^\rho$ no leaf of $L^* - P$ lies below the lowest common ancestor of $L^* \cap P$. The pieces of the two parts are then disjoint subgraphs of the piece of $L^*$, which misses all other pieces.
- *Condition 2 in $T_1$.* Delete the edge above $P$ in $T_1^\rho$ and the edge $e'$ in $T_1'^\rho$. In both cases the two components are subdivisions of $T_1^\rho|P$ and of $T_1^\rho|((X \cup \{\rho\}) - P)$. Vertex-disjoint pieces stay vertex-disjoint when an edge is subdivided or a degree-2 vertex is suppressed. Blocks on different sides lie in different components.

So $m(T_1, T_2) \le d + 1$. The two parts give the theorem. $\square$

Both parts are constructive. Part 1 turns any agreement forest with $m$ blocks into $m - 1$ explicit moves, and Part 2 turns any sequence of $d$ moves into a forest with at most $d + 1$ blocks. The implementation for this page codes both steps and checks them against a breadth-first search over all trees with up to 5 leaves and a sample with 6 leaves.

## Consequences

- **Algorithms.** Every algorithm for rooted maximum agreement forests computes $d_{\mathrm{rSPR}}$. This includes the $O(2.42^k n)$ branching algorithm and the linear-time 3-approximation of Whidden, Beiko and Zeh.
- **Hardness.** The rSPR distance and the rooted agreement forest problem have the same complexity. Bordewich and Semple proved NP-hardness and a [kernel](/kernelization/) with $O(k)$ leaves through the forest form.
- **Approximation.** An algorithm that finds a forest within a factor $c$ of the least number of cuts gives the rSPR distance within the same factor $c$.
- **Agreement subtrees.** A maximum agreement subtree on $S$ gives a forest with block $S \cup \{\rho\}$ and singletons, so $d_{\mathrm{rSPR}} \le n - |S|$.
- **Unrooted bound.** Removing $\rho$ and forgetting the roots turns a rooted agreement forest into an unrooted one of at most the same size (one less if $\{\rho\}$ is a block by itself). So the TBR distance of the unrooted trees is at most $d_{\mathrm{rSPR}}$.
- **Networks.** The hybridization number of two trees is the least size of an *acyclic* agreement forest minus one, where acyclic is an extra condition on the order of the blocks in the two trees. Every acyclic forest is a forest, so $d_{\mathrm{rSPR}}$ is a lower bound for the hybridization number.

## Tightness

- **The leaf $\rho$ is needed.** Let $T_1 = ((a,(b,c)),d)$ and $T_2 = (((a,d),b),c)$. Without $\rho$, the blocks $\{a, d\}$ and $\{b, c\}$ form an agreement forest of the two trees, which would give distance 1. A breadth-first search shows $d_{\mathrm{rSPR}} = 2$. With $\rho$, every forest with 2 blocks fails, and $\{\{a\}, \{b\}, \{c, d, \rho\}\}$ is a maximum agreement forest. Forests without $\rho$ only give the lower bound $m_0 - 1 \le d_{\mathrm{rSPR}}$.
- **No unrooted SPR version.** For unrooted trees, the agreement forest size minus one is the TBR distance, not the uSPR distance. The trees $((A,B),C,(D,(E,F)))$ and $((A,C),B,(F,(D,E)))$ have an agreement forest $\{\{A,B,C\},\{D,E,F\}\}$ and TBR distance 1, but uSPR distance 2.
- **Binary trees.** Lemma 2 uses that each vertex has two children. For trees with multifurcations, the usual forms of the theorem replace equality of restrictions by compatibility.
- **Not a network count.** The forest of the theorem may be cyclic. Then the hybridization number of the two trees is larger than $d_{\mathrm{rSPR}}$.

## History

Hein, Jiang, Wang and Zhang introduced agreement forests in 1996 and stated that their size minus one gives the unrooted subtree transfer (SPR) distance. Allen and Steel showed in 2001 that the unrooted agreement forest counts TBR moves instead, and gave pairs of trees for which the uSPR distance is larger. Bordewich and Semple then treated the rooted case. They added the leaf $\rho$, proved the equality of this page in their 2005 paper, and used it to prove that the rSPR distance is NP-hard and fixed-parameter tractable. The later branching algorithms of Whidden, Beiko and Zeh, and the acyclic forests of Baroni, Grünewald, Moulton and Semple for hybridization, build on the same form.

## References
