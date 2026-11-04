---
title: Little's algorithm returns a shortest tour
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. A *tour* is a set $T$ of $n \ge 2$ arcs that forms one cycle through all $n$ cities, and $\mathrm{cost}(T) = \sum_{(u, v) \in T} c_{uv}$, which is $\infty$ if $T$ has a forbidden arc. Let $z^*$ be the least cost of a tour, or $\infty$ if every tour has a forbidden arc. For a node $(lb, M, S)$, let $R$ and $K$ be the rows and columns of $M$: the cities with no arc of $S$ out of them, and the cities with no arc of $S$ into them. The node *stands for* the set $\mathcal{T}(lb, M, S)$ of tours $T$ with $S \subseteq T$ and $M_{uv} < \infty$ for every $(u, v) \in T \setminus S$.

**Claim 1 (cost identity).** For every node that the algorithm makes and every $T \in \mathcal{T}(lb, M, S)$, $\mathrm{cost}(T) = lb + \sum_{(u, v) \in T \setminus S} M_{uv}$, and $M_{uv} \ge 0$ for all entries.

*Proof.* Before line L1 reduces it, $M = C$ with $\infty$ on the diagonal, and $lb = 0$, $S = \emptyset$; the identity holds, as no tour uses a diagonal arc. We show that each operation keeps the identity and $M \ge 0$, for every tour that the node still stands for after the operation.

- *Row reduction by $h$, the smallest entry of row $u \in R$.* A tour $T$ in the set uses exactly one arc out of $u$, and since $u \in R$ it is not in $S$, so its end is a column in $K$. The sum in the identity loses $h$ and $lb$ gains $h$. The new row has smallest entry 0. If $h = \infty$, the set is empty, and REDUCE returns $\infty$.
- *Column reduction.* The same, with arcs into a city of $K$.
- *Setting an entry to $\infty$ (lines L10 and L12).* The set of tours shrinks; the identity holds for the tours that remain, as the other entries do not change.
- *Fixing $(i, j)$ with $M_{ij} = 0$ (line L11).* For a tour $T \supseteq S \cup \{(i, j)\}$, the term $M_{ij} = 0$ moves from the sum to $S''$, and the other terms of $T \setminus S''$ lie in rows $R \setminus \{i\}$ and columns $K \setminus \{j\}$, which $M''$ keeps.

Each node is made from its parent by these operations, so the claim holds by induction. $\square$

**Claim 2 (bound and leaves).** For every node, every $T \in \mathcal{T}(lb, M, S)$ has $\mathrm{cost}(T) \ge lb$. If $|S| = n$ at line L6, then $S$ is a tour and $\mathrm{cost}(S) = lb$.

*Proof.* The first part follows from Claim 1, as $M \ge 0$. For the second, arcs are added only at line L11, with $i \in R$ and $j \in K$, so $S$ has at most one arc out of each city and at most one into each city. If $S$ has no cycle, it is a set of disjoint paths, where a city with no arc of $S$ counts as a path with no arcs. The end $e$ of a path has no arc out, so $e \in R$, and its start $s$ has no arc in, so $s \in K$.

We show the invariant: for every path $s \to \cdots \to e$ of $S$ with fewer than $n - 1$ arcs, $M_{es} = \infty$. For a path with no arcs this is the diagonal entry, which line L1 sets to $\infty$. Reductions do not change entries equal to $\infty$, and line L10 only adds one, so the invariant passes to the exclude child. In the include child, $i$ is the end of its path and $j$ the start of its path, and these two paths join into the path through $(i, j)$, for which line L12 sets $M''_{es} = \infty$ when it has fewer than $n - 1$ arcs. Every other path keeps its ends, which are not $i$ and not $j$, so its entry is in a row and a column that $M''$ keeps.

Now suppose that adding $(i, j)$ at line L11 closes a cycle. Then $j$ is the start and $i$ the end of the same path $P$, and the cycle has $|P| + 1$ arcs. If $|P| + 1 < n$, the invariant gives $M_{ij} = \infty$, so $(i, j)$ is not a zero, a contradiction. So the only cycle $S$ can contain has $n$ arcs and is a tour. When $|S| = n$, the $n$ arcs with one out of each city and one into each city cannot all lie on paths, so $S$ is this tour; it lies in $\mathcal{T}(lb, M, S)$ with an empty sum, and Claim 1 gives $\mathrm{cost}(S) = lb$. $\square$

**Claim 3 (children split the parent).** Let a node $N = (lb, M, S)$ with $|S| < n$ be split at lines L8 to L14 on $(i, j)$. Every $T \in \mathcal{T}(N)$ lies in the set of the exclude child $N'$ or of the include child $N''$, with the bounds $lb + \theta(i, j)$ and $lb + h$ that lines L10 and L13 compute, whether or not the child is inserted.

*Proof.* If $(i, j) \notin T$, then $T$ uses no arc with $M'_{uv} = \infty$, so $T \in \mathcal{T}(N')$; the reduction of row $i$ subtracts $\min_{k \ne j} M_{ik}$, since $M'_{ij} = \infty$ and the other entries of row $i$ are those of $M$, and then column $j$ has smallest entry $\min_{k \ne i} M_{kj}$, so the bound is $lb + \theta(i, j)$. If $(i, j) \in T$, then $T \supseteq S''$. If $|S''| < n - 1$, the arc $(e, s)$ of line L12 together with the path $s \to \cdots \to e$ of $S''$ makes a cycle of fewer than $n$ arcs, which $T$ cannot contain, so $T$ does not use $(e, s)$ and $T \in \mathcal{T}(N'')$. $\square$

**Claim 4 (invariant).** At the start of each iteration of line L3, every tour $T$ with $\mathrm{cost}(T) < z$ lies in the set of some live node.

*Proof.* At the start, the root stands for all tours of finite cost, and it is inserted unless its bound is $\infty$, in which case no tour has finite cost. Suppose that the claim holds at the start of an iteration that takes $N$ and does not break, and let $\mathrm{cost}(T) < z$ at the end of the iteration. As $z$ only decreases, $\mathrm{cost}(T) < z$ held at the start, and $T$ was in the set of a live node. If that node is not $N$, it is still live. If it is $N$ and $|S| = n$, then $T = S$ and line L7 sets $z = \mathrm{cost}(S)$, which contradicts $\mathrm{cost}(T) < z$. Otherwise, by Claim 3, $T$ is in the set of a child with bound $b \le \mathrm{cost}(T) < z$ by Claim 2; then the test at line L9 or line L14 passes and the child is inserted. $\square$

**Claim 5 (termination).** The loop runs finitely often. *Proof.* Each child either has one more arc in $S$ (include) or one more entry equal to $\infty$ among the entries of its rows and columns (exclude, since $M_{ij} = 0$ becomes $\infty$). Along any path of the tree, the number of fixed arcs is at most $n$, and between two include steps the number of finite entries, at most $n^2$, falls by at least one at each exclude step. So every path has length at most $n + n^3$, the tree is binary, and it is finite. $\square$

**Theorem.** LITTLE$(C)$ returns $(z^*, T)$ for a tour $T$ of cost $z^*$ if $z^* < \infty$, and $(\infty, \text{NIL})$ otherwise.

*Proof.* By Claim 5 the loop ends. By Claim 2, $z$ is $\infty$ or the cost of the tour $best$, so $z \ge z^*$. When the loop ends, either $H$ is empty, or the node taken has $lb \ge z$ and, as $H$ is a min-priority queue, every live node has bound at least $z$. In both cases, Claim 4 and Claim 2 show that no tour has cost below $z$: such a tour would lie in a live node with bound at most its cost, below $z$. So $z \le z^*$, hence $z = z^*$. If $z^* < \infty$, then $best$ is a tour of cost $z^*$; if $z^* = \infty$, line L7 never runs, since a leaf has finite bound only if its tour has finite cost, and inserted nodes have bound below $z = \infty$; so $best = \text{NIL}$. $\blacksquare$
