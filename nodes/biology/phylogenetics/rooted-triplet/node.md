---
tag: H3ZK37
kind: definition
slug: rooted-triplet
name: Rooted triplet
aliases:
- rooted triple
- three-taxon statement
area: biology/phylogenetics
level: core
summary: The rooted shape ab|c that a rooted tree gives to three taxa, saying a and b share an ancestor not shared with c. A rooted tree is fixed by its triplets, and BUILD tests if triplets fit one tree.
prereqs: [rooted-and-unrooted-trees, lowest-common-ancestor]
see_also: [quartet, splits-of-a-tree, supertree, maximum-rooted-triplet-consistency, tree-comparison, connected-components, consensus-tree]
sources:
  - paper: doi:10.1137/0210030
    title: Alfred V. Aho, Yehoshua Sagiv, Thomas G. Szymanski and Jeffrey D. Ullman, Inferring a tree from lowest common ancestors with an application to the optimization of relational expressions, SIAM Journal on Computing 10(3), 1981, 405-421
    locator: the algorithm BUILD and the graph on the leaves used to split them at the root
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 6 (rooted triples displayed by a rooted tree, and the algorithm BUILD)
---

A rooted triplet is the rooted shape of a tree on three taxa: $ab \mid c$ says that $a$ and $b$ have a common ancestor that is not an ancestor of $c$. A rooted [phylogenetic tree](/phylogenetic-tree/) displays at most one of the three triplets $ab \mid c$, $ac \mid b$ and $bc \mid a$ on each set of three taxa, and exactly one if it is binary. A rooted tree is determined by the triplets it displays. The algorithm BUILD of Aho, Sagiv, Szymanski and Ullman (1981) decides in polynomial time whether a set of triplets is displayed by one tree, and builds such a tree if it exists.

## Definition

Let $X$ be a set of taxa. A *rooted triplet* on $X$ is written $ab \mid c$, or $((a,b),c)$ in [Newick format](/newick-format/), for three distinct taxa $a, b, c \in X$. The order of $a$ and $b$ has no meaning: $ab \mid c$ and $ba \mid c$ are the same triplet.

**Displayed triplets.** Let $T$ be a rooted phylogenetic $X$-tree and $\operatorname{lca}(x, y)$ the [lowest common ancestor](/lowest-common-ancestor/) of the leaves $x$ and $y$. $T$ *displays* $ab \mid c$ if $\operatorname{lca}(a, b)$ is a proper descendant of $\operatorname{lca}(a, c)$. Equivalently, some cluster of $T$ holds $a$ and $b$ but not $c$. The set of triplets that $T$ displays is $R(T)$.

The three lowest common ancestors of $a$, $b$ and $c$ are on one path to the root, and at least two of them are equal. If $\operatorname{lca}(a, b)$ is strictly lower, then $\operatorname{lca}(a, c) = \operatorname{lca}(b, c)$, and $T$ displays $ab \mid c$ and neither of the other two triplets. If all three are equal, $T$ displays none of them; the restriction of $T$ to $\{a, b, c\}$ is then the *fan* $(a, b, c)$, a root with three children. A binary tree has no fans, so it displays exactly one triplet on each set of three taxa and $|R(T)| = \binom{n}{3}$.

**Triplets and quartets.** Add a new taxon $\rho$ joined to the root of $T$, and unroot. Then $T$ displays $ab \mid c$ if and only if the unrooted tree displays the [quartet](/quartet/) $ab \mid c\rho$. This is how results about quartets and triplets move from one setting to the other.

### Rooted trees are determined by their triplets

**Theorem.** Let $T$ be a rooted phylogenetic $X$-tree and $C \subseteq X$ with $2 \le |C| < |X|$. Then $C$ is a cluster of $T$ if and only if $T$ displays $aa' \mid c$ for all distinct $a, a' \in C$ and all $c \in X \setminus C$. So $R(T)$ determines the clusters of $T$, and the clusters determine $T$: two rooted phylogenetic $X$-trees with the same triplets are equal.

*Proof.* If $C$ is the cluster of a vertex $v$, then for $a, a' \in C$ and $c \notin C$ the vertex $\operatorname{lca}(a, a')$ is $v$ or below it, and $\operatorname{lca}(a, c)$ is strictly above $v$. So $T$ displays $aa' \mid c$.

Conversely, assume that $T$ displays all these triplets, and let $v$ be the lowest common ancestor of all of $C$. The cluster of $v$ contains $C$. Since $|C| \ge 2$, the taxa of $C$ are not all below one child of $v$, so some $a, a' \in C$ are below different children of $v$, and $\operatorname{lca}(a, a') = v$. Suppose the cluster of $v$ holds some $c \notin C$. Then $c$ is below a child of $v$, and at least one of $a, a'$, say $a'$, is below a different child, so $\operatorname{lca}(a', c) = v = \operatorname{lca}(a, a')$, and $T$ does not display $aa' \mid c$. This contradicts the assumption, so the cluster of $v$ is $C$.

The clusters of a rooted phylogenetic tree form a hierarchy (any two are disjoint or nested), and the tree is the Hasse diagram of the hierarchy, in the same way as in the proof of the [splits-equivalence theorem](/splits-of-a-tree/). So the clusters determine the tree. $\square$

### BUILD: is a set of triplets displayed by one tree?

Let $R$ be a set of triplets on $X$. For $S \subseteq X$, the *Aho graph* $[R, S]$ has the vertex set $S$ and an edge $\{a, b\}$ for each triplet $ab \mid c \in R$ with $a, b, c \in S$.

```pseudo id=build
BUILD(R, S)
L1  if |S| = 1 then return the leaf labeled by the element of S
L2  compute the connected components S_1, ..., S_k of the Aho graph [R, S]
L3  if k = 1 then return "no tree displays R"
L4  for i ← 1 to k
L5      T_i ← BUILD(R, S_i); if T_i is "no tree" then return "no tree displays R"
L6  return a new root with the children T_1, ..., T_k
```

**Why it works.** Suppose some tree $T$ on $S$ displays every triplet of $R$ with all three taxa in $S$, and let $C_1, \ldots, C_m$ be the clusters of the children of the root of $T$, with $m \ge 2$. For a triplet $ab \mid c$, the vertex $\operatorname{lca}(a, b)$ is below the root, so $a$ and $b$ are in the same $C_j$. So each edge of the Aho graph lies inside one $C_j$, each component lies inside one $C_j$, and there are at least $m \ge 2$ components. So BUILD never stops at L3 when a tree exists; by induction it does not stop at L5 either, since the restriction of $T$ to $S_i$ displays the triplets inside $S_i$. In the other direction, let BUILD return a tree and let $ab \mid c \in R$ with $a, b, c \in S$. The edge $\{a, b\}$ puts $a$ and $b$ in one component $S_i$. If $c \notin S_i$, the tree displays $ab \mid c$ at this root. If $c \in S_i$, the triplet is handled inside $T_i$, by induction. So the returned tree displays all of $R$.

**Cost.** Each call computes [connected components](/connected-components/) in $O(|S| + |R|)$ time, and the calls on one level of the recursion work on disjoint sets $S_i$. There are at most $n - 1$ levels, so the whole run takes $O(n (n + |R|))$ time for $n = |X|$. Faster versions exist that keep the Aho graph under edge deletions instead of building it again on each level.

A consistent set $R$ is often displayed by many trees, and BUILD returns one of them. For example, $\{ab \mid c\}$ on $\{a, b, c, d\}$ gives $((a,b),c,d)$, but $((a,b,d),c)$ also displays it, and this second tree does not have the cluster $\{a, b\}$. When no tree displays $R$, finding a tree that displays the most triplets of $R$ is NP-hard; this is [maximum rooted triplet consistency](/maximum-rooted-triplet-consistency/). BUILD is also the core of many [supertree](/supertree/) methods, which combine rooted trees on overlapping taxon sets.

## Examples and non-examples

**All triplets of a tree.** The rooted tree $((a,b),(c,(d,e)))$ is binary, so it displays $\binom{5}{3} = 10$ triplets:
$$ab \mid c,\; ab \mid d,\; ab \mid e,\; cd \mid a,\; cd \mid b,\; ce \mid a,\; ce \mid b,\; de \mid a,\; de \mid b,\; de \mid c.$$
The tree $((a,c),(b,(d,e)))$ shares only $de \mid a$, $de \mid b$ and $de \mid c$ with it, so the two trees differ on $10 - 3 = 7$ of the 10 sets of three taxa. This count is their *triplet distance*.

**BUILD on a consistent set.** Let $R = \{ab \mid c,\ cd \mid b,\ de \mid c\}$ and $S = \{a, b, c, d, e\}$. The Aho graph has the edges $ab$, $cd$ and $de$, so its components are $\{a, b\}$ and $\{c, d, e\}$. Inside $\{a, b\}$ there is no triplet, and the components are $\{a\}$ and $\{b\}$. Inside $\{c, d, e\}$ only $de \mid c$ applies, with the edge $de$, and the components are $\{c\}$ and $\{d, e\}$. BUILD returns $((a,b),(c,(d,e)))$, which displays all three triplets. Three triplets already fix this binary tree on five taxa, although it displays ten.

**BUILD on an inconsistent set.** Let $R = \{ab \mid c,\ bc \mid a\}$. The Aho graph on $\{a, b, c\}$ has the edges $ab$ and $bc$, so it is connected and BUILD stops at L3. Indeed, a tree that displays $ab \mid c$ has a cluster with $a$ and $b$ but not $c$, and a tree that displays $bc \mid a$ has a cluster with $b$ and $c$ but not $a$. These two clusters meet in $b$ and neither contains the other, so they cannot both be clusters of one tree.

**A fan.** The tree $(a, b, (c, d))$ displays $cd \mid a$ and $cd \mid b$, and nothing on $\{a, b, c\}$, $\{a, b, d\}$. So $|R(T)| = 2 < 4 = \binom{4}{3}$.

**Non-example: an unrooted tree.** An unrooted tree does not display triplets: the unrooted tree $ab \mid cd$ is the rooting $((a,b),(c,d))$ with $ab \mid c$, but it is also the rooting $(a,(b,(c,d)))$ with $bc \mid a$. Use [quartets](/quartet/) for unrooted trees.

## Related definitions

- [Quartets](/quartet/) are the unrooted analog, and the [splits](/splits-of-a-tree/) of an unrooted tree play the part of the clusters of a rooted tree.
- The triplet distance between two rooted trees counts the sets of three taxa on which they display different triplets; see [tree comparison](/tree-comparison/).
- [Maximum rooted triplet consistency](/maximum-rooted-triplet-consistency/) asks for a tree that displays as many triplets of a set as possible.
- [Supertree](/supertree/) methods merge rooted trees on overlapping taxon sets, many of them through BUILD on the union of their triplets.
- Aho, Sagiv, Szymanski and Ullman designed BUILD for a database problem, and the same question, whether constraints on lowest common ancestors fit one tree, appears in phylogenetics under the name of triplet compatibility.

## References
