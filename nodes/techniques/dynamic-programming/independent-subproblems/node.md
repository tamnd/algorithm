---
tag: XN1R75
kind: concept
slug: independent-subproblems
name: Independent subproblems
area: techniques/dynamic-programming
level: core
summary: Subproblems that share no resources, which is required for optimal substructure to apply in dynamic programming.
prereqs: [optimal-substructure, cut-and-paste-argument]
see_also: [overlapping-subproblems, principle-of-optimality, longest-path-problem, held-karp-algorithm, tree-dynamic-programming, bitmask-dp, knapsack-dynamic-programming, matrix-chain-multiplication]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 14.3, Elements of dynamic programming (the discussion of unweighted shortest and longest simple paths, and of independent and overlapping subproblems)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 6.7, Independent sets in trees
  - paper: doi:10.1137/0110015
    title: Michael Held and Richard M. Karp, A dynamic programming approach to sequencing problems, Journal of the Society for Industrial and Applied Mathematics 10(1), 1962
    locator: pp. 196 to 210
---

The subproblems of one decomposition are independent when the solution of one of them does not restrict the solutions of the others: any optimal solutions of the parts can be put together, and the result is a feasible solution of the whole. CLRS phrases it as subproblems that do not share resources. Independence is the half of [optimal substructure](/optimal-substructure/) that makes the recurrence an upper bound on the optimum, and its failure is why the longest simple path problem has no simple DP. The usual fix is to move the shared resource into the subproblem, which often makes the number of subproblems much larger.

## In plain words

Suppose a job splits into two smaller jobs, and you solve each one as well as you can. If the two best answers fit together without a clash, the parts are independent. Then the best whole is the best first part next to the best second part.

Sometimes they clash. Two parts of a trip may both want to pass through the same town when the trip may not repeat a town. Two parts of a packing may both want the same space. Then the two best answers cannot be used together, and adding their scores gives a number that no real answer reaches.

When this happens, describe each part with more detail: say which towns are still free, or how much space is left. With that detail the parts no longer clash, but there are more parts to solve.

## The idea

### The definition

Take an instance $I$, a choice $k$ that splits it into subinstances $I_1, \ldots, I_m$, and a rule that combines solutions $X_j \in \mathcal{F}(I_j)$ into $\mathrm{comb}_k(X_1, \ldots, X_m)$. Let $\mathcal{G}_k \subseteq \mathcal{F}(I_1) \times \cdots \times \mathcal{F}(I_m)$ be the set of tuples whose combination is feasible for $I$. The subproblems $I_1, \ldots, I_m$ are **independent** for the choice $k$ when

$$ \mathcal{G}_k = \mathcal{F}(I_1) \times \cdots \times \mathcal{F}(I_m), $$

that is, every tuple of feasible parts combines into a feasible whole. They are *dependent* when some tuple of feasible parts combines into something infeasible. This is the closure condition in the definition of [optimal substructure](/optimal-substructure/).

### Why the recurrence needs it

Let the cost be additive: $c(\mathrm{comb}_k(X_1, \ldots, X_m)) = w_k + \sum_j c(X_j)$. The best solution of $I$ that uses the choice $k$ has cost

$$ \min_{(X_1, \ldots, X_m) \in \mathcal{G}_k} \Bigl( w_k + \sum_j c(X_j) \Bigr). $$

**Claim.** If the subproblems are independent for $k$, this equals $w_k + \sum_j \mathrm{OPT}(I_j)$. If they are dependent, it is at least that, and it can be strictly larger.

**Proof.** If $\mathcal{G}_k$ is the full product, the minimum of a sum of terms that each depend on one coordinate is the sum of the minima: choose each $X_j$ optimal for $I_j$, which is allowed since the product has no constraint between coordinates, and no tuple does better since each term is at least $\mathrm{OPT}(I_j)$. If $\mathcal{G}_k$ is a subset of the product, the minimum over a subset is at least the minimum over the product. It is strictly larger when every tuple of optimal parts lies outside $\mathcal{G}_k$, as in the examples below. ∎

So with dependent subproblems, the formula $w_k + \sum_j \mathrm{OPT}(I_j)$ is not the value of any solution. For a minimization it is too small, and for a maximization it is too large. The recurrence then reports a value that no feasible solution achieves.

### Independence and overlap

The two words describe different relations, and a DP needs both. Independence is a relation among the sibling subproblems of *one* choice: they must not compete for a resource. [Overlap](/overlapping-subproblems/) is a relation across the whole recursion: the same subproblem appears under *different* choices or different parents, so storing its answer saves work. CLRS points out that the two are not in conflict: the subproblems of one choice are distinct and independent, while the same subproblem can be reached through many choices.

### How to restore independence

When parts compete for a resource, put the state of the resource into the subproblem. The choice then also decides how the resource is shared, and each part gets its own share.

- **Capacity.** In the [0/1 knapsack](/knapsack-dynamic-programming/), "the best subset of items $1, \ldots, i$" is not a well-posed subproblem, because the item $i + 1$ and the first $i$ items compete for the capacity. The subproblem "the best subset of items $1, \ldots, i$ with capacity $w$" fixes the share of each part. The number of subproblems grows by the factor $W + 1$.
- **Used elements.** For paths that may not repeat a vertex, the subproblem must record which vertices are used. The [Held-Karp algorithm](/held-karp-algorithm/) uses the state (set of visited vertices, last vertex), which gives $O(n 2^n)$ subproblems instead of $n$. This is the pattern of [bitmask DP](/bitmask-dp/).
- **The interface.** In a tree, two subtrees of a vertex $v$ meet only at $v$. Once the subproblem fixes what happens at $v$, the subtrees are independent. This is the pattern of [tree DP](/tree-dynamic-programming/).

## Examples

### Shortest paths: independent

Split a shortest path from $u$ to $v$ at a vertex $w$ into a path from $u$ to $w$ and a path from $w$ to $v$. Any walk from $u$ to $w$ followed by any walk from $w$ to $v$ is a walk from $u$ to $v$, so the parts are independent when the solutions are walks. When there is no negative cycle, a shortest walk can be taken to be a simple path, because removing a cycle does not increase its weight. CLRS Section 14.3 makes the matching argument for simple paths in an unweighted graph: if the two shortest parts shared a vertex other than $w$, the whole path would contain a cycle and would not be shortest.

### Longest simple paths: dependent

Take the complete graph on the four vertices $a, b, c, d$, with unit edge lengths. The longest simple path from $a$ to $b$ has 3 edges, for example $a, c, d, b$. The longest simple path from $b$ to $d$ also has 3 edges, for example $b, a, c, d$. The recurrence "longest from $a$ to $d$ through $b$ = longest from $a$ to $b$ + longest from $b$ to $d$" gives $3 + 3 = 6$. But a simple path in a graph with 4 vertices has at most 3 edges, and the true longest simple path from $a$ to $d$ has 3 edges. Each longest part uses all four vertices, so the parts compete for $c$ and $d$, and every pair of longest parts combines into a walk that repeats a vertex. CLRS Section 14.3 shows the same failure on another graph with four vertices.

### Matrix chains and rod cutting: independent

In [matrix-chain multiplication](/matrix-chain-multiplication/), the split at $k$ gives the ranges $A_i \cdots A_k$ and $A_{k+1} \cdots A_j$. They share no matrix, and any parenthesization of the left range together with any parenthesization of the right range is a parenthesization of $A_i \cdots A_j$. In [rod cutting](/rod-cutting-problem/), the first piece and the rest of the rod are disjoint, and any cutting of the rest can follow any first piece. In [longest common subsequence](/longest-common-subsequence/), each choice leaves only one subproblem, so there is nothing to compete with.

### Independent sets in a tree: dependent until the state is refined

Take the tree with root $r$ of weight 5, its children $x$ of weight 6 and $y$ of weight 2, and the children $x_1$ of weight 3 and $x_2$ of weight 4 of $x$. An independent set has no two adjacent vertices. The best independent set of the subtree of $x$ is $\{x_1, x_2\}$, of weight 7, and the best of the subtree of $y$ is $\{y\}$, of weight 2. If $r$ is taken, adding these gives $5 + 7 + 2 = 14$, but $\{r, x_1, x_2, y\}$ is not independent, because $r$ and $y$ are adjacent. The subtrees are not independent of the choice at $r$.

With two values for each vertex $v$, the best set of the subtree of $v$ that contains $v$ and the best one that does not, the subproblems become independent. For the leaves, the values are $(3, 0)$, $(4, 0)$ and $(2, 0)$. For $x$, they are $(6 + 0 + 0, \max(3, 0) + \max(4, 0)) = (6, 7)$. For $r$, they are $(5 + 7 + 0, \max(6, 7) + \max(2, 0)) = (12, 9)$. The optimum is 12, with the set $\{r, x_1, x_2\}$. This is the algorithm of Dasgupta, Papadimitriou and Vazirani, Section 6.7.

## Where it is used

- **Checking a recurrence.** Before you trust a DP recurrence, take optimal solutions of the parts of one choice and check that they combine into a feasible whole. If they may not, the recurrence is wrong.
- **Designing the state.** Most DP states are the smallest data that makes the parts of each choice independent: the remaining capacity in a [knapsack](/knapsack-problem/), the last item in a sequence problem, the status of a vertex in [tree DP](/tree-dynamic-programming/), the set of used vertices in [bitmask DP](/bitmask-dp/), or the profile of a boundary in [broken-profile DP](/broken-profile-dp/).
- **Explaining hardness.** The [longest path problem](/longest-path-problem/) on general graphs has no known polynomial algorithm. Its natural subproblems are dependent, and restoring independence needs a record of the used vertices, which is exponential. In a [directed acyclic graph](/directed-acyclic-graph/), two parts of a path cannot share a vertex, so the subproblems are independent and the [longest path in a DAG](/dag-longest-path/) takes linear time.
- **Greedy proofs.** The subproblem that remains after a greedy choice must be independent of that choice, or the [cut-and-paste argument](/cut-and-paste-argument/) for optimal substructure fails at the paste.

## References
