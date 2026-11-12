---
title: FROM-TREE returns the splits of a tree, and TO-TREE rebuilds the unique tree of a compatible split system
proves: [correctness]
status: full
---

Let $X = \{x_0, \ldots, x_{n-1}\}$ with $n \ge 3$ and $r = x_0$. For a split $A \mid B$, its *cluster* is the part that does not hold $r$; the system stores the cluster as a mask. We identify a mask with the set of taxa whose bits are set.

## FROM-TREE

Let $T$ be an unrooted phylogenetic $X$-tree, and hang it from the leaf $r$: the parent of a vertex $v \ne r$ is its neighbour on the path to $r$, which is the vertex from which breadth-first search first reached $v$. Write $L(v)$ for the set of taxa below $v$, that is, the taxa $y$ whose path to $r$ passes through $v$.

**Claim.** After line L4 for $v$, `below[v]` is $L(v) \setminus \{r\}$.

*Proof.* Breadth-first search reaches each child of $v$ after $v$, so in reverse order each child comes before $v$. We use induction along the reverse order. The taxa below $v$ are $v$ itself if $v$ is a taxon, together with the taxa below the children of $v$. The children of $v$ are the neighbours $u \ne$ `parent[v]`. Line L3 handles $v$ itself, and line L4 forms the union over the children, whose values are correct by induction. $\square$

For $v \ne r$, deleting the edge from $v$ to its parent leaves two subtrees. The one with $v$ holds exactly the vertices below $v$, and the other holds $r$. So the split of this edge is $L(v) \mid X \setminus L(v)$, and its cluster is $L(v)$, which does not hold $r$. Each edge of $T$ is the edge from some $v \ne r$ to its parent, so line L5 adds the cluster of every edge, and nothing else. Hence FROM-TREE returns $\Sigma(T)$.

## TO-TREE

Let $\mathcal{H}$ be the set $H$ of line L8, with the clusters in the order of line L9. Every member is a nonempty subset of $X \setminus \{r\}$, and $top = X \setminus \{r\}$ is the first. Two clusters $C, D$ *cross* if $C \cap D \ne \emptyset$, $C \not\subseteq D$ and $D \not\subseteq C$. By the lemma on the page of splits, two splits are compatible exactly when their clusters do not cross. The trivial splits never cross anything, so $\Sigma$ is compatible exactly when no two members of $\mathcal{H}$ cross.

**Invariant.** Suppose that the loop has processed the clusters $C_1, \ldots, C_t$ (in order) without an error. Then (a) no two of $C_1, \ldots, C_t$ cross, and (b) for each taxon $y \ne r$, `deepest[y]` is the smallest of $C_1, \ldots, C_t$ that holds $y$.

The smallest one is well defined under (a): $C_1 = top$ holds $y$, and the clusters that hold $y$ pairwise meet, so they are nested and form a chain.

*Proof.* For $t = 1$, $C_1 = top$, and line L17 sets `deepest[y]` to $top$ for every $y$; (a) is empty. Assume the invariant after $t$ steps and process $C = C_{t+1}$, with $C \ne top$. Every earlier cluster $D$ has at least as many elements as $C$ and $D \ne C$.

*Case 1: some earlier $D$ crosses $C$.* Pick $y \in C \cap D$ and $z \in C \setminus D$. By (b), `deepest[y]` is a cluster that holds $y$ and is contained in $D$, since $D$ holds $y$ and the clusters holding $y$ form a chain with `deepest[y]` the smallest. On the other hand, `deepest[z]` holds $z \notin D$, so it is not contained in $D$. So `deepest[y]` $\ne$ `deepest[z]`, and whichever taxon line L14 picks, line L15 finds a taxon of $C$ with a different value and raises the error.

*Case 2: no earlier cluster crosses $C$.* Let $D$ be an earlier cluster that meets $C$. It does not cross $C$, so $D \subseteq C$ or $C \subseteq D$. If $D \subseteq C$, then $|D| \ge |C|$ gives $D = C$, which is impossible. So $C \subsetneq D$. Hence, for every $y \in C$, the earlier clusters that hold $y$ are exactly the earlier clusters that contain $C$, and these do not depend on $y$. By (b) all taxa of $C$ have the same value $P$ of `deepest`, the smallest earlier cluster that contains $C$, so line L15 raises no error. After line L17, (a) holds for $C_1, \ldots, C_{t+1}$, and for $y \in C$ the new value $C$ is the smallest cluster that holds $y$, since all others that hold $y$ contain $C$ strictly. For $y \notin C$ nothing changes, and $C$ does not hold $y$, so (b) holds. $\square$

**The error is raised exactly when $\Sigma$ is not compatible.** If $\Sigma$ is compatible, no two clusters cross, Case 1 never occurs, and the loop ends without error. If $\Sigma$ is not compatible, take the first cluster $C$ in the order that crosses an earlier one. All steps before it are in Case 2, so the invariant holds when $C$ is processed, and by Case 1 line L15 raises the error at $C$, unless an error was raised even earlier. In both cases TO-TREE reports an error.

**The tree is correct.** Assume $\Sigma$ is compatible. By Case 2, each cluster $C \ne top$ is joined to $v(P)$, where $P$ is the smallest member of $\mathcal{H}$ that strictly contains $C$: every member that contains $C$ strictly has more elements, so it comes earlier in the order. And $top$ is joined to $r$. This is exactly the tree built in the proof of the splits-equivalence theorem on the page of splits, with the clusters $\mathcal{H}$ and the reference taxon $r$: one vertex for each cluster, an edge from each cluster to its parent, the singletons as the leaves $x \ne r$, and the leaf $r$ joined to $X \setminus \{r\}$. That proof shows that the result is an unrooted phylogenetic $X$-tree whose split set is the set of splits with clusters in $\mathcal{H}$, which is $\Sigma$ together with all trivial splits, and that no other tree has this split set. $\square$

**Running time.** Line L9 sorts $k + n$ masks. Lines L15 and L17 each visit the taxa of $C$ once, so the loop costs $O\bigl(\sum_{C \in \mathcal{H}} |C|\bigr) = O(n (k + n))$. For a compatible system $k \le 2n - 3$, and the total is $O(n^2)$.
