---
tag: Q1YWWQ
kind: concept
slug: depth-first-orders
name: Depth-first orders (preorder, postorder, reverse postorder)
aliases:
- Depth-first orders
area: graphs/traversal
level: core
summary: Three orderings of vertices recorded during depth-first search of a digraph, used for topological sort and strong components.
prereqs: [depth-first-search, discovery-and-finish-times]
see_also: [topological-sort, kosaraju-sharir, parenthesis-theorem, preorder-traversal, postorder-traversal, dfs-forest, edge-classification, strongly-connected-components]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (the class DepthFirstOrder with preorder, postorder and reverse postorder, topological sort and the Kosaraju-Sharir algorithm)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.4, Topological sort, and Section 20.5, Strongly connected components (decreasing finish times)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Section 3.3 (directed acyclic graphs and the post numbers) and Section 3.4 (the vertex with the highest post number lies in a source strongly connected component)
---

The depth-first orders of a [depth-first search](/depth-first-search/) are three lists of the vertices: the *preorder* lists each vertex when DFS discovers it, the *postorder* lists each vertex when DFS finishes it, and the *reverse postorder* is the postorder read backwards. They are the vertices sorted by the [discovery and finish times](/discovery-and-finish-times/), and one DFS gives all three in $\Theta(n + m)$ time. In a directed acyclic graph, the reverse postorder is a [topological ordering](/topological-ordering/), and in any directed graph its first vertex lies in a source strong component, which is the key fact of the [Kosaraju-Sharir](/kosaraju-sharir/) algorithm.

## In plain words

Depth-first search goes into a vertex, explores below it, and comes back out. It can write the vertex on a list at the moment it goes in, or at the moment it comes out.

The first list is the preorder. A vertex comes before everything that the search finds below it.

The second list is the postorder. A vertex comes after everything below it. So the last vertex to be left is at the end.

Read the second list from the end and you get the reverse postorder. Here each vertex comes before everything below it, and also before the vertices that the search had already finished when it arrived. When the graph has no loops, this puts each vertex before every vertex that it points to.

## The idea

Run DFS$(G)$ on a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, with the times $d$ and $f$ of the [depth-first search](/depth-first-search/) page. Append $u$ to a list *pre* at line L5, when $u$ turns gray, and append $u$ to a list *post* at line L10, when $u$ turns black. Then

- *pre* is the list of the vertices in increasing order of $d$;
- *post* is the list of the vertices in increasing order of $f$;
- the reverse postorder, *post* read from the end, is the list in decreasing order of $f$.

Each list costs $O(1)$ time per vertex on top of the DFS. The reverse postorder can be built without a reversal: push each finished vertex on a [stack](/stack/), or put it at the front of a [linked list](/linked-list/).

**Subtrees are blocks.** By the [parenthesis theorem](/parenthesis-theorem/), the descendants of $u$ in the [depth-first forest](/dfs-forest/) are exactly the vertices whose intervals lie inside $[d[u], f[u]]$. So in *pre* they form a contiguous block that starts with $u$, and in *post* a contiguous block that ends with $u$. For a rooted tree, these are the [preorder](/preorder-traversal/) and [postorder](/postorder-traversal/) traversals.

**Edges in the reverse postorder.** For an edge $(u, v)$, the [edge classification](/edge-classification/) gives $f[v] < f[u]$ for tree, forward and cross edges, and $f[u] \le f[v]$ for back edges. So in the reverse postorder, an edge goes forward, from earlier to later, exactly when it is not a back edge.

**Proposition 1 (topological order).** If $G$ is acyclic, its reverse postorder is a topological ordering: for each edge $(u, v)$, $u$ comes before $v$.

*Proof.* Let $(u, v)$ be an edge. If it were a back edge, then $v$ would be an ancestor of $u$, the tree path from $v$ to $u$ with the edge $(u, v)$ would be a cycle, and $G$ would not be acyclic. So $(u, v)$ is a tree, forward or cross edge, and $f[v] < f[u]$. In decreasing order of $f$, $u$ is before $v$. $\square$

**Proposition 2 (source component).** Let $C$ and $C'$ be two different strongly connected components of $G$ with an edge from a vertex of $C$ to a vertex of $C'$. Then the largest finish time in $C$ is larger than the largest finish time in $C'$. So the first vertex of the reverse postorder lies in a component that no edge enters.

*Proof.* Let $x$ be the first vertex of $C \cup C'$ that DFS discovers. Just before $d[x]$, all of $C \cup C'$ is white. If $x \in C$, then $x$ reaches each vertex of $C$ inside $C$, and each vertex of $C'$ through the edge from $C$ to $C'$, by paths in $C \cup C'$, which are white. By the [white-path theorem](/white-path-theorem/), all of $C \cup C'$ are descendants of $x$, so $f[x]$ is the largest finish time in $C \cup C'$, and it is in $C$. If $x \in C'$, then by the same theorem all of $C'$ are descendants of $x$, so they finish by $f[x]$. No vertex of $C$ is reachable from $C'$, because then $C$ and $C'$ would be one component. So no vertex of $C$ is a descendant of $x$, and each vertex $y$ of $C$ is white at $f[x]$: it was white at $d[x]$, and if it were discovered during the interval of $x$, the parenthesis theorem would make it a descendant. So $f[y] > f[x]$ for each $y \in C$. In both cases the largest finish time of $C$ is larger.

For the second claim, let $v$ be the vertex with the largest $f$, and $C$ its component. If an edge entered $C$ from a component $C'$, the first claim would give a vertex of $C'$ with a larger $f$ than $v$. $\square$

**Preorder is not topological.** Preorder puts $u$ before its descendants, but a cross edge can go from a later branch into an earlier one. On the acyclic graph with the edges $0 \to 1$ and $2 \to 1$, DFS with the roots $0, 1, 2$ gives the preorder $0, 1, 2$, and the edge $2 \to 1$ goes backwards. The reverse postorder is $2, 0, 1$, which is topological. The reverse of the preorder is not the postorder either: here it is $2, 1, 0$, while the postorder is $1, 0, 2$.

## Examples

Run DFS on the directed graph with vertices 0 to 6 and the lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$, with roots tried in the order 0 to 6. The times are $d = (1, 2, 3, 6, 7, 11, 12)$ and $f = (10, 5, 4, 9, 8, 14, 13)$.

| order | list |
|---|---|
| preorder | 0, 1, 2, 3, 4, 5, 6 |
| postorder | 2, 1, 4, 3, 0, 6, 5 |
| reverse postorder | 5, 6, 0, 3, 4, 1, 2 |

The subtree of 3 is $\{3, 4\}$, a block in each list. The graph has the cycles $0, 1, 2$ and $5, 6$, so no list is topological: in the reverse postorder, the back edges $2 \to 0$ and $6 \to 5$ go backwards, and all other edges go forwards. The strong components are $\{0, 1, 2\}$, $\{3\}$, $\{4\}$ and $\{5, 6\}$. The first vertex, 5, lies in $\{5, 6\}$, and no edge enters that component, as Proposition 2 says.

Remove the edges $2 \to 0$ and $6 \to 5$. The graph is now acyclic, and DFS gives the same tree edges and the same times, because the removed edges led to gray vertices. So the reverse postorder $5, 6, 0, 3, 4, 1, 2$ is a topological ordering: each of the edges $0 \to 1$, $0 \to 3$, $0 \to 2$, $1 \to 2$, $3 \to 2$, $3 \to 4$, $5 \to 4$, $5 \to 6$ goes forward in it.

## Where it is used

- **[Topological sort](/topological-sort/).** The reverse postorder of a DFS of a directed acyclic graph, by Proposition 1.
- **[Kosaraju-Sharir](/kosaraju-sharir/).** The first pass computes the reverse postorder of $G$. The second pass runs DFS on the [transpose graph](/transpose-graph/) and tries the roots in that order. By Proposition 2, each tree of the second pass is one [strong component](/strongly-connected-components/).
- **[Cycle detection](/cycle-detection/).** A directed graph is acyclic exactly when its reverse postorder has no backward edge, which a scan of the edges checks in $O(n + m)$ time.
- **Tree traversals.** On a rooted tree with its children in order, the preorder and postorder of DFS from the root are the [preorder](/preorder-traversal/) and [postorder](/postorder-traversal/) traversals.
- **[Euler tour technique](/euler-tour-technique/).** Subtrees are contiguous blocks of the preorder, so subtree queries become range queries on an array.

## References
