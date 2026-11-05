---
tag: 425Q3K
kind: concept
slug: discovery-and-finish-times
name: Discovery and finish times
aliases:
- pre and post numbers
- DFS timestamps
area: graphs/traversal
level: core
summary: Timestamps recording when DFS first reaches and finally leaves each vertex.
prereqs: [depth-first-search]
see_also: [parenthesis-theorem, white-path-theorem, edge-classification, dfs-forest, depth-first-orders, topological-sort, kosaraju-sharir, low-link]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.3, Depth-first search (the timestamps d and f, the parenthesis theorem and the corollary on nesting of descendants' intervals)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Chapter 3, Decompositions of graphs (Section 3.2, the previsit and postvisit orderings, and Section 3.3, Depth-first search in directed graphs)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.2, Directed graphs (the class DepthFirstOrder, with preorder and postorder)
---

The discovery time $d[u]$ and the finish time $f[u]$ of a vertex $u$ are the two moments, on one clock, when [depth-first search](/depth-first-search/) first reaches $u$ and when it has finished all work below $u$. The two times give each vertex an interval $[d[u], f[u]]$. These intervals nest like brackets, and from them one reads in $O(1)$ time whether one vertex is an ancestor of another, the type of each edge, and a [topological ordering](/topological-ordering/) of a directed acyclic graph.

## In plain words

Depth-first search walks into the graph and later walks back out. Give it a clock that ticks once at each such event. When the search arrives at a vertex for the first time, write the clock value on the vertex. This is the discovery time. When the search has explored everything it can reach from that vertex and leaves it for good, write the clock value again. This is the finish time.

Each vertex now has a start and an end, like a meeting in a calendar. Two such meetings never overlap in part. One lies fully inside the other, or they do not touch at all. A meeting inside another one means that the inner vertex was explored from the outer one. This simple picture explains many uses of depth-first search.

## The idea

In the procedure DFS of the [depth-first search](/depth-first-search/) page, a global counter $time$ starts at 0. Line L5 increases it and stores it in $d[u]$ when $u$ turns from white to gray. Line L10 increases it and stores it in $f[u]$ when $u$ turns from gray to black. On a graph with $n$ vertices:

- the $2n$ values $d[u]$ and $f[u]$ are the numbers $1, 2, \ldots, 2n$, each used one time;
- $d[u] < f[u]$ for each $u$;
- at time $t$, the vertex $u$ is white if $t < d[u]$, gray if $d[u] \le t < f[u]$, and black if $t \ge f[u]$.

So the colours of the search are a function of the times, and an algorithm can keep the times instead of the colours.

**Nesting.** The [parenthesis theorem](/parenthesis-theorem/) says that for any two vertices $u \ne v$, either the intervals $[d[u], f[u]]$ and $[d[v], f[v]]$ are disjoint, or one contains the other, and $[d[v], f[v]] \subset [d[u], f[u]]$ holds exactly when $v$ is a proper descendant of $u$ in the [depth-first forest](/dfs-forest/). This gives an ancestor test in $O(1)$ time:

$$u \text{ is an ancestor of } v \iff d[u] \le d[v] \text{ and } f[v] \le f[u].$$

**Size of a subtree.** The interval of $u$ holds exactly the $2 s_u$ times of the $s_u$ descendants of $u$, $u$ included, because each descendant's interval lies inside it and each other vertex's interval is disjoint from it. The interval has $f[u] - d[u] + 1$ integers, so

$$s_u = \frac{f[u] - d[u] + 1}{2}.$$

**Edges.** For an edge $(u, v)$ of a directed graph, the times give its type in the classification of [edge classification](/edge-classification/): tree or forward edge if $d[u] < d[v] < f[v] < f[u]$, back edge if $d[v] \le d[u] < f[u] \le f[v]$, cross edge if $f[v] < d[u]$. The fourth order, $f[u] < d[v]$, never occurs for an edge: when $u$ finishes, $v$ has been seen.

**Two counters.** Some books use two separate counters: the *preorder number* $\mathrm{pre}[u] \in \{1, \ldots, n\}$ counts only discoveries, and the *postorder number* $\mathrm{post}[u] \in \{1, \ldots, n\}$ counts only finishes. Dasgupta, Papadimitriou and Vazirani use one shared clock and call the values pre and post. With two counters, $\mathrm{pre}$ and $\mathrm{post}$ each give the same order of the vertices as $d$ and $f$, but a discovery cannot be compared with a finish, so the ancestor test needs both orders: $u$ is an ancestor of $v$ if and only if $\mathrm{pre}[u] \le \mathrm{pre}[v]$ and $\mathrm{post}[v] \le \mathrm{post}[u]$. The lists of vertices sorted by these numbers are the [depth-first orders](/depth-first-orders/).

## Examples

Run DFS on the directed graph with vertices 0 to 6 and the adjacency lists $0: 1, 3, 2$; $1: 2$; $2: 0$; $3: 2, 4$; $4$: none; $5: 4, 6$; $6: 5$. The roots are tried in the order 0 to 6.

| $u$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| $d[u]$ | 1 | 2 | 3 | 6 | 7 | 11 | 12 |
| $f[u]$ | 10 | 5 | 4 | 9 | 8 | 14 | 13 |
| subtree size $(f - d + 1)/2$ | 5 | 2 | 1 | 2 | 1 | 2 | 1 |

Read in time order, the events form the bracket word

$$(_0\ (_1\ (_2\ )_2\ )_1\ (_3\ (_4\ )_4\ )_3\ )_0\ (_5\ (_6\ )_6\ )_5$$

with the times 1 to 14.

- **Ancestor tests.** $[7, 8] \subset [1, 10]$, so 4 is a descendant of 0. The intervals $[2, 5]$ and $[6, 9]$ are disjoint, so neither of 1 and 3 is an ancestor of the other.
- **Edge types.** The edge $2 \to 0$ has $d[0] = 1 \le d[2] = 3 < f[2] = 4 \le f[0] = 10$, so it is a back edge. The edge $3 \to 2$ has $f[2] = 4 < d[3] = 6$, so it is a cross edge. The edge $0 \to 2$ has $[3, 4] \subset [1, 10]$ and is not a tree edge, so it is a forward edge.
- **Two counters.** The preorder numbers are $0{:}1, 1{:}2, 2{:}3, 3{:}4, 4{:}5, 5{:}6, 6{:}7$, and the postorder numbers are $2{:}1, 1{:}2, 4{:}3, 3{:}4, 0{:}5, 6{:}6, 5{:}7$.
- **Decreasing finish time.** Sorted by decreasing $f$, the vertices are $5, 6, 0, 3, 4, 1, 2$. This graph has the cycle $0, 1, 2$, so this order is not a topological ordering: the edge $2 \to 0$ goes backwards. For a graph without cycles the same sort gives a [topological sort](/topological-sort/).

## Where it is used

- **[Topological sort](/topological-sort/).** In a directed acyclic graph, each edge $(u, v)$ has $f[v] < f[u]$, so the vertices in decreasing order of $f$ form a topological ordering.
- **[Cycle detection](/cycle-detection/).** A directed graph has a cycle if and only if some edge $(u, v)$ has $d[v] \le d[u] < f[u] \le f[v]$, a back edge.
- **Strong components.** The [Kosaraju-Sharir algorithm](/kosaraju-sharir/) runs a second DFS on the [transpose graph](/transpose-graph/) in decreasing order of the finish times of the first DFS.
- **Low links.** [Tarjan's algorithm](/tarjan-scc/), [articulation points](/articulation-point/) and [bridges](/bridge-finding/) compare discovery times through the [low-link](/low-link/) value.
- **Ancestor queries on trees.** The [Euler tour technique](/euler-tour-technique/) uses the same intervals to answer "is $u$ an ancestor of $v$" and subtree queries on a rooted tree in $O(1)$ time after a linear-time pass.
- **The [white-path theorem](/white-path-theorem/).** It describes the descendants of $u$ by the state of the search at the moment $d[u]$.

## References
