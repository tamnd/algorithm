---
tag: SJS6GY
kind: problem
slug: directed-feedback-vertex-set
name: Directed feedback vertex set
aliases:
- DFVS
area: complexity/parameterized-complexity
level: research
summary: "Delete at most k vertices of a digraph to make it acyclic. FPT in k, in O(4^k k! n^O(1)) by iterative compression and important separators (Chen et al. 2008); no polynomial kernel is known."
prereqs: [feedback-arc-set-problem, fixed-parameter-tractable, important-separators]
see_also: [iterative-compression, parameterized-feedback-vertex-set, feedback-vertex-set-problem, important-separators, parameterized-multicut, directed-acyclic-graph, parameterized-vertex-cover, karps-21-np-complete-problems]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 8, Finding cuts and separators (directed graphs and directed feedback vertex set)
  - paper: doi:10.1145/1411509.1411511
    title: "Jianer Chen, Yang Liu, Songjian Lu, Barry O'Sullivan and Igor Razgon, A fixed-parameter algorithm for the directed feedback vertex set problem, Journal of the ACM 55(5), article 21 (2008)"
    locator: O(4^k k! n^O(1)) algorithm by iterative compression and skew separators (conference version STOC 2008)
  - url: https://arxiv.org/abs/1609.04347
    title: Daniel Lokshtanov, M. S. Ramanujan and Saket Saurabh, A linear time parameterized algorithm for directed feedback vertex set, arXiv:1609.04347
    locator: abstract (O(k! 4^k k^5 (n + m)) time; conference version SODA 2018)
  - paper: doi:10.1145/2700209
    title: "Rajesh Chitnis, Marek Cygan, MohammadTaghi Hajiaghayi and Daniel Marx, Directed subset feedback vertex set is fixed-parameter tractable, ACM Transactions on Algorithms 11(4), 28 pages (2015)"
    locator: directed subset feedback vertex set is FPT in the solution size
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 85-103 (1972)"
    locator: feedback node set and feedback arc set are NP-complete
---

Directed feedback vertex set (DFVS) asks whether at most $k$ vertices of a directed graph can be deleted so that no directed cycle remains. With $k$ as the [parameter](/parameter/), it was for many years a main open problem whether the problem is [fixed-parameter tractable](/fixed-parameter-tractable/). In 2008 Chen, Liu, Lu, O'Sullivan and Razgon solved it with an $O(4^k k!\, n^{O(1)})$ algorithm. The algorithm combines [iterative compression](/iterative-compression/) with [important separators](/important-separators/). No polynomial kernel is known, and no $2^{O(k)} n^{O(1)}$ algorithm is known. This page gives the parameterized view; the [feedback arc set problem](/feedback-arc-set-problem/) page has the classical and approximation view.

## In plain words

A directed graph has arrows between points. A cycle is a way to follow arrows and come back to the start. You may remove at most $k$ points, and after that no cycle may remain, so the points can be put in a line where all arrows go forward.

In undirected graphs this is a well understood problem with simple branching rules. With arrows it is harder, because a cycle can be long and a vertex of low degree can still be on many cycles. The solution grows the graph one vertex at a time. At each step it has a solution that is one vertex too large, and it tries to make it smaller. For this it guesses the order of the old solution in the final line, and then it must cut all backward paths between them. Important separators do this cutting.

## Definition

- Instance: a directed graph $G$ with $n$ vertices and $m$ arcs, given by adjacency lists, and an integer $k \ge 0$.
- Parameter: $k$.
- Question: is there a set $S$ of at most $k$ vertices such that $G - S$ is a [directed acyclic graph](/directed-acyclic-graph/)?

## Variants

- **Directed feedback arc set (DFAS).** Delete at most $k$ arcs instead. The two problems are equivalent with the same $k$ (see Reductions), so every bound below holds for both.
- **Undirected feedback vertex set.** Delete vertices so that no undirected cycle remains. It has an $O^\ast(c^k)$ algorithm for a constant $c$, where $O^\ast$ hides polynomial factors, and a polynomial kernel. See [parameterized feedback vertex set](/parameterized-feedback-vertex-set/). The two problems differ: a directed acyclic graph can have undirected cycles, for example the arcs $1 \to 2$, $1 \to 3$, $2 \to 4$, $3 \to 4$.
- **Directed subset feedback vertex set.** Given also a set $T$ of vertices, delete at most $k$ vertices so that no directed cycle passes through $T$. Chitnis, Cygan, Hajiaghayi and Marx proved that it is FPT in $k$. Their algorithm uses the random sampling of important separators.
- **Weighted versions.** With integer vertex weights and $k$ the total weight, a vertex of weight $w$ can be replaced by $w$ copies with the same in-arcs and out-arcs. So the problem stays FPT in $k$.

## Examples

A scratch script solved DFVS by brute force on the digraph with vertices $1, \ldots, 6$ and the 9 arcs $1 \to 2$, $2 \to 3$, $3 \to 1$, $3 \to 4$, $4 \to 5$, $5 \to 6$, $6 \to 4$, $2 \to 5$, $5 \to 1$.

- The directed cycles include $1, 2, 3$ and $4, 5, 6$ and $1, 2, 5$. The least DFVS has 2 vertices, and there are 7 optimal solutions: $\{1, 4\}$, $\{1, 5\}$, $\{1, 6\}$, $\{2, 4\}$, $\{2, 5\}$, $\{2, 6\}$, $\{3, 5\}$.
- The least undirected feedback vertex set of the same graph, with arc directions ignored, also has 2 vertices, but there are only 5 optimal solutions. The sets $\{1, 6\}$ and $\{2, 6\}$ leave the undirected cycle $2, 3, 4, 5$, which is not a directed cycle.
- The least DFAS has 2 arcs, and there are 3 optimal solutions. Each one contains the arc $1 \to 2$, which is on the cycles $1, 2, 3$ and $1, 2, 5$.
- **One compression step.** The set $W = \{1, 4, 5\}$ is a DFVS of size 3. The script searched for a DFVS of size at most 2 that is disjoint from $W$ and found exactly one, $\{2, 6\}$. After deleting it, the arcs are $3 \to 1$, $3 \to 4$, $4 \to 5$, $5 \to 1$, so the vertices of $W$ appear in the order $4, 5, 1$.

## Known algorithms

- **Chen, Liu, Lu, O'Sullivan and Razgon (2008).** $O(4^k k!\, n^{O(1)})$ time, the first FPT algorithm. It uses iterative compression. Given a DFVS $W$ of size $k + 1$, it guesses the part $W'$ of $W$ that the new solution keeps and deletes the rest. Then it guesses the order $w_1, \ldots, w_\ell$ of $W'$ in a topological order of $G - S$. It splits each $w_i$ into a source $s_i$ with the out-arcs and a sink $t_i$ with the in-arcs. A set $S$ disjoint from $W'$ then works exactly when $G - S$ has no path from $s_i$ to $t_j$ for $j \le i$. This is the *skew multicut* problem, and a search tree over important separators solves it with at most $4^{k'}$ leaves for a budget $k'$. If $|W'| = \ell$, the budget is $\ell - 1$. So the total number of guesses with their leaves is $\sum_{\ell} \binom{k+1}{\ell} \ell!\, 4^{\ell - 1} \le (k + 1)!\, 4^{k} e^{1/4}$, and this gives the bound.
- **Lokshtanov, Ramanujan and Saurabh (2016, SODA 2018).** $O(k!\, 4^k k^5 (n + m))$ time, linear in the input size. The dependence on $k$ matches the earlier algorithm up to a factor $k$.

## Bounds

- **Classical complexity.** NP-complete under polynomial-time many-one reductions. Karp listed feedback node set and feedback arc set among his 21 NP-complete problems in 1972.
- **Lower bound in time.** DFVS has no $2^{o(k)} n^{O(1)}$ algorithm unless the exponential time hypothesis (ETH) fails. This follows from the reduction from vertex cover below. The gap between $2^{o(k)}$ and $4^k k!$ is open. In particular, no $2^{O(k)} n^{O(1)}$ algorithm is known.
- **Kernels.** Whether DFVS has a polynomial kernel in $k$ is open. No kernel lower bound is known either.

## Reductions

- **From vertex cover.** Given an undirected graph $H$, replace each edge $uv$ by the two arcs $u \to v$ and $v \to u$, and keep $k$. Each edge is now a directed 2-cycle, and every directed cycle uses an edge of $H$. So a vertex set hits all directed cycles exactly when it covers all edges. This is a parameterized reduction with $k' = k$ and linear size. The scratch script checked it on the graph with edges $12$, $23$, $31$, $34$, $45$: both optima are 3, and the five optimal solutions are the same sets.
- **From DFVS to DFAS.** Split each vertex $v$ into $v_{\mathrm{in}}$ and $v_{\mathrm{out}}$ with one arc $v_{\mathrm{in}} \to v_{\mathrm{out}}$. Each arc $u \to v$ becomes $u_{\mathrm{out}} \to v_{\mathrm{in}}$, repeated $k + 1$ times so that it is never worth deleting. Deleting the arc of $v$ is deleting $v$. On the example digraph above, the script found the least DFAS of the split graph to be 2, with the same 7 solutions.
- **From DFAS to DFVS.** Take the line digraph: one vertex per arc, and an arc from $a$ to $b$ when the head of $a$ is the tail of $b$. Directed cycles of the two graphs match, so a DFAS of size $k$ is a DFVS of size $k$ of the line digraph.

## Applications

Directed acyclic graphs are the structures that allow a topological order. So DFVS models the removal of a few items to break all circular dependencies. Examples are deadlock recovery in operating systems, the order of evaluation in circuits with feedback, and the order of tasks or the ranking of items from inconsistent comparisons. The algorithm for DFVS was also the model for later directed cut problems, such as directed multiway cut and directed subset feedback vertex set.

## References
