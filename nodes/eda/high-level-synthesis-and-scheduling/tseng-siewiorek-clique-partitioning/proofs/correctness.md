---
title: Tseng-Siewiorek clique partitioning returns a maximal clique partition
proves: [correctness]
status: full
---

We use the notation of the page. $G = (V, E)$ has $n$ vertices. At any moment the supernodes have member sets $M(i)$ and neighbour sets $N(i)$, and $j \in N(i)$ exactly when $i \in N(j)$. Two sets $X, Y \subseteq V$ are *fully joined* when every $x \in X$ and every $y \in Y$ are adjacent in $G$.

**Lemma 1 (invariants).** Before each test of line L2:

1. the sets $M(i)$ partition $V$;
2. each $M(i)$ is a clique of $G$;
3. for two supernodes $i \ne j$, $j \in N(i)$ exactly when $M(i)$ and $M(j)$ are fully joined.

*Proof.* By induction on the number of merges. After L1, each $M(v) = \{v\}$, so (1) and (2) hold, and $N(v)$ is the set of neighbours of $v$ in $G$, which is (3) for single vertices.

Assume the claims before a merge of $i$ and $j$ with $j \in N(i)$. Line L5 replaces $M(i)$ and $M(j)$ by their union, so (1) still holds. By (2), $M(i)$ and $M(j)$ are cliques, and by (3) they are fully joined, so their union is a clique, and (2) holds. For (3), take another supernode $x$. By line L6, $x$ is a neighbour of the new supernode exactly when $x \in N(i) \cap N(j)$. By (3) before the merge, that is when $M(x)$ is fully joined to $M(i)$ and to $M(j)$, which is when it is fully joined to $M(i) \cup M(j)$. Line L6 removes $j$ from every neighbour set and adds the new supernode only to the sets of its new neighbours, so the adjacency between two supernodes other than the merged one is unchanged, and (3) holds for them by the assumption. $\square$

**Lemma 2 (termination).** The loop runs at most $n - 1$ times.

*Proof.* Each pass of the loop deletes one supernode $j$ and creates none, and there are $n$ supernodes after L1. When one supernode is left it has no neighbour, so the loop stops. A pass starts only when some supernode has a neighbour, so line L4 always finds a pair. $\square$

**Theorem 1 (valid and maximal).** The output is a partition of $V$ into cliques of $G$. No two output sets are fully joined, so no two of them can be replaced by their union to get a partition into fewer cliques.

*Proof.* By Lemma 2 the loop stops, and then no supernode has a neighbour. By Lemma 1 (1) and (2) the output sets partition $V$ into cliques. If two output sets $M(i)$ and $M(j)$ were fully joined, then by Lemma 1 (3) we would have $j \in N(i)$, and the loop would not have stopped. $\square$

By the [resource compatibility graph](/resource-compatibility-graph/) page, a partition of the compatibility graph into cliques is a valid binding, so the output is a valid binding with one unit, register or bus per output set.

**Theorem 2 (exact on unions of cliques).** If $G$ is a disjoint union of cliques $K_1, \ldots, K_c$, the output is $\{K_1, \ldots, K_c\}$, which has the fewest cliques.

*Proof.* Every clique of $G$ lies inside one $K_t$, since there are no edges between different $K_t$. So every partition into cliques has at least $c$ parts, one for each nonempty $K_t$ at least. By Lemma 1 (2), each output set is a clique and lies inside one $K_t$. If two output sets lay inside the same $K_t$, they would be fully joined, against Theorem 1. So each $K_t$ is exactly one output set. $\square$

**What is not claimed.** The number of output sets is not always the least. The page gives two graphs where it is not: a triangle with a pendant vertex on each corner, with 4 sets against 3, and an interval graph on 8 lifetimes of depth 4, with 5 sets against 4. On the interval graph, every order of breaking ties in line L4 gives 5 sets. These instances are checked in the tests of the implementation. $\blacksquare$
