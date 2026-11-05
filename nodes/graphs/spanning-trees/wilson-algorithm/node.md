---
tag: XQWGT5
kind: algorithm
slug: wilson-algorithm
name: Wilson's algorithm
aliases:
- loop-erased random walk algorithm
area: graphs/spanning-trees
level: advanced
summary: Builds a uniform random spanning tree from loop-erased random walks.
solves: [uniform-spanning-tree-sampling]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: O(m n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [spanning-tree, uniform-spanning-tree-sampling, markov-chain, stationary-distribution]
see_also: [aldous-broder, matrix-tree-theorem, counting-spanning-trees, coupling-from-the-past, las-vegas-algorithm, spanning-forest, randomized-algorithm, laplacian-matrix]
sources:
  - paper: doi:10.1145/237814.237880
    title: David Bruce Wilson, Generating random spanning trees more quickly than the cover time, Proceedings of the 28th Annual ACM Symposium on Theory of Computing (1996), 296-303
    locator: the whole paper (the algorithm RandomTreeWithRoot, the cycle popping proof, and the expected running time)
  - book: isbn:9781107160156
    title: Russell Lyons and Yuval Peres, Probability on Trees and Networks, Cambridge University Press (2016)
    locator: Chapter 4, Uniform Spanning Trees (Section 4.1, Generating uniform spanning trees, Wilson's method with stacks and cycle popping)
---

Wilson's algorithm samples a [spanning tree](/spanning-tree/) of a connected undirected graph uniformly at random. It fixes a root, and then, for each vertex not yet in the tree, runs a random walk until the walk hits the tree, erases the loops of that walk, and adds the loop-free path to the tree. Each of the $\tau(G)$ spanning trees comes out with probability exactly $1/\tau(G)$, and with edge weights as step probabilities the same method samples a tree with probability proportional to the product of its weights. Wilson (1996) showed that the expected number of steps is the expected commute time between the root and a random vertex, which is $O(mn)$. With a root drawn from the stationary distribution this is twice the mean hitting time of the walk, which is always less than the cover time that the [Aldous-Broder algorithm](/aldous-broder/) needs.

## In plain words

You want one of all the connecting trees of a network, with every tree equally likely.

Start with one point as the tree. Pick a point that is not in the tree yet and walk at random from it, one link at a time, until you reach the tree. Your route may cross itself. Each time it comes back to a point it has already passed, cut off the loop it just made, so the route stays a simple path. When you reach the tree, add the whole path to the tree. Then pick another point that is not in the tree and do the same. When every point is in the tree, stop.

The surprising fact is that every tree is equally likely, and the work is often much less than a walk that must visit every point.

## The problem

The input is a finite undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a source of random bits. Parallel edges are allowed and are different edges. Self-loops are allowed: a walk may take one, but loop erasure always removes it.

- **Unweighted.** The output is a spanning tree $T$ with $\Pr[T = t] = 1 / \tau(G)$ for each spanning tree $t$, where $\tau(G)$ is the number of spanning trees.
- **Weighted.** Each edge has a weight $c_e > 0$, a *conductance*. The walk at $x$ takes edge $e$ with probability $c_e / c(x)$, where $c(x)$ is the sum of the weights at $x$, with a self-loop counted twice. The output satisfies $\Pr[T = t] \propto \prod_{e \in t} c_e$. Weights of zero or less are not allowed. Ties in weight are allowed and do not matter: equal weights give equal factors. The weights are not costs, and the algorithm does not look for a minimum.
- **Disconnected graphs.** A walk cannot leave its component, so the graph need not be connected if each component has its own root. The implementation takes the smallest vertex of each component as its root, so the output is a [spanning forest](/spanning-forest/) that is uniform among the spanning forests with the components of $G$.

## The algorithm

```pseudo id=main
WILSON(G, r)
L1  InTree[r] ← true; InTree[x] ← false for each x ≠ r; T ← ∅
L2  for each vertex i, in any order do
L3      u ← i
L4      while not InTree[u] do                          ▷ walk until the tree is hit
L5          Next[u] ← an edge at u, chosen at random with probability c_e / c(u)
L6          u ← the other end of Next[u]
L7      u ← i
L8      while not InTree[u] do                          ▷ follow the loop-erased path
L9          InTree[u] ← true
L10         T ← T ∪ {Next[u]}
L11         u ← the other end of Next[u]
L12 return T
```

The loop erasure is hidden in line L5. When the walk comes back to a vertex $u$, it takes a new step out of $u$ and overwrites $\text{Next}[u]$, so the steps of the loop are forgotten. After the walk hits the tree, following $\text{Next}$ from $i$ traces the *loop-erased* walk: the path that remains when each loop is cut off at the moment it closes. Lines L8 to L11 add that path to the tree. A vertex that the walk visited but that is not on the loop-erased path keeps $\text{InTree}$ false and gets its own walk later.

## Example

The graph has the vertices $a$ to $f$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$. It has 55 spanning trees. Take the root $r = a$ and the order $b, c, d, e, f$. One possible run:

| start | walk | $\text{Next}$ at the end of the walk | path added | edges added |
|---|---|---|---|---|
| $b$ | $b \to c \to b \to a$ | $b{:}\,ab$, $c{:}\,bc$ | $b, a$ | $ab$ |
| $c$ | $c \to b$ | $c{:}\,bc$ | $c, b$ | $bc$ |
| $d$ | $d \to c$ | $d{:}\,cd$ | $d, c$ | $cd$ |
| $e$ | $e \to f \to e \to d$ | $e{:}\,de$, $f{:}\,ef$ | $e, d$ | $de$ |
| $f$ | $f \to e$ | $f{:}\,ef$ | $f, e$ | $ef$ |

The first walk closes the loop $b \to c \to b$, and the second step out of $b$ overwrites $\text{Next}[b]$, so the loop is erased. The vertex $c$ was visited but is not on the path from $b$, so it is not added and gets its own walk. The result is the path $\{ab, bc, cd, de, ef\}$. Each of the 55 trees has probability $1/55$ to be the result. The tests replay this run with fixed random numbers, and draw 11000 trees and compare the counts with $200$ per tree by a chi-square statistic.

## Correctness

**Theorem.** Let $G$ be connected, with positive edge weights, and let $r$ be any vertex. With probability 1, WILSON stops, and for each spanning tree $t$,

$$\Pr[T = t] = \frac{\prod_{e \in t} c_e}{\sum_{t'} \prod_{e \in t'} c_e},$$

which is $1/\tau(G)$ when all weights are 1. The law does not depend on $r$ or on the order of the vertices in line L2.

**Termination and shape.** A random walk on a finite connected graph hits each given vertex with probability 1, so each walk of lines L4 to L6 ends. Line L8 starts at a vertex not in the tree and follows $\text{Next}$ to the tree, through vertices of the loop-erased path, which are distinct. So each pass adds a path that touches the old tree only at its end, and $T$ stays a tree that contains $r$. Every vertex $i$ is in the tree after its pass, so the final $T$ is a spanning tree.

**The law, by cycle popping.** Give each vertex $x \ne r$ an infinite stack of independent random edges at $x$, each chosen with probability $c_e / c(x)$, and let line L5 read the next entry of the stack of $u$. The top entries form a graph in which each vertex $x \ne r$ has one arrow out. Either the arrows form a spanning tree directed to $r$, or they contain a directed cycle. *Popping* a cycle removes the top entry of each vertex on it. The run of the algorithm pops cycles, one each time a walk closes a loop, until no cycle is left, and it returns the tree of the arrows on top. Two facts finish the proof. First, for fixed stacks, the set of cycles popped and the final tree do not depend on the order of popping, since two cycles visible at one time share no vertex. Second, the event "these cycles are popped and the tree $t$ is left" asks for given values in disjoint sets of stack entries, so its probability is a product: a factor for the cycles, times $\prod_{x \ne r} c_{t(x)} / c(x)$ for the tree. The set of possible popped cycles does not depend on $t$, so summing over them gives $\Pr[T = t] \propto \prod_{e \in t} c_e$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM with a source of uniform random numbers.

- **Steps.** Let $\pi(x) = c(x) / \sum_y c(y)$ be the stationary distribution of the walk and $H(x, y)$ the expected time for the walk from $x$ to hit $y$. Wilson proved that the expected number of steps in line L5 is
$$\sum_{x \in V} \pi(x)\, \big( H(x, r) + H(r, x) \big),$$
the expected commute time between $r$ and a vertex drawn from $\pi$.
- **Worst case.** The commute time between two vertices of a connected unweighted graph is at most $2m(n - 1)$, since it equals $2m$ times the effective resistance between them, which is at most the length of a path between them. So the expected number of steps is at most $2m(n - 1) = O(mn)$.
- **Fast cases.** On the complete graph $K_n$, the commute time between two vertices is $2(n - 1)$, so Wilson takes $O(n)$ steps, while a walk that covers $K_n$ takes $\Theta(n \log n)$ steps. On the example graph with root $a$, the formula gives about 13.8 steps.
- **Lines L7 to L11.** Each vertex enters the tree once, so they cost $O(n)$ in total.
- **One step.** $O(1)$ unweighted and $O(\log \deg x)$ with weights, by binary search in the prefix sums of the weights at $x$.
- **Space.** $O(n + m)$.

| claim | bound | case |
|---|---|---|
| steps | expected commute time between $r$ and a $\pi$-random vertex | each connected graph |
| steps | at most $2m(n - 1)$ expected | each connected unweighted graph |
| steps | $O(n)$ expected | complete graph |
| space | $O(n + m)$ | worst |

The running time is a random variable with no worst-case bound, so the algorithm is a [Las Vegas algorithm](/las-vegas-algorithm/): its output always has the right law, and only its time is random.

## Properties

- **Exact.** The law is exactly uniform, or exactly proportional to the weight product, not an approximation.
- **Any root and any order.** The law of the output depends on neither, but the running time depends on the root.
- **Compared with Aldous-Broder.** With a root drawn from $\pi$, the expected number of steps is $2\tau$, where $\tau = \sum_{x, y} \pi(x) \pi(y) H(x, y)$ is the mean hitting time. Wilson noted that $\tau$ is always less than the cover time, and on many graphs it is much less.
- **Directed graphs.** The same procedure, with the walk on the directed graph, samples a random arborescence directed to $r$ with probability proportional to the product of the step probabilities. In a directed graph the law then depends on $r$.
- **Not deterministic.**

## Variants and improvements

- **Random root.** Choose $r$ from $\pi$. The law of the tree as an edge set is the same.
- **Unknown root, directed graphs.** For a random arborescence with a root drawn in proportion to a given weight, Wilson adds a new absorbing vertex and runs the walk with a small chance to stop at each step, halving that chance until the result has one root.
- **Rooted spanning forests.** With an extra absorbing vertex joined to every vertex, the same method samples random rooted forests, a tool in fast Laplacian and sampling algorithms.
- **Faster algorithms.** Kelner and Mądry (2009) and later papers shortcut random walks with electrical flows, and Schild (2018) reached almost-linear time.
- **Mazes.** On a grid graph, the algorithm gives a uniformly random perfect maze.

## When to use it

Use Wilson's algorithm by default for exact uniform spanning trees of graphs with up to millions of edges: it is short, needs only random steps, and its expected time, within a factor 2 of the mean hitting time, is usually far below the cover time of Aldous-Broder. Use the determinant method when the time must be bounded in the worst case. For very large graphs with a slow walk, such as long paths or graphs with bottlenecks, the expected time can reach $\Theta(mn)$.

## Pitfalls

- **Adding the walk instead of the loop-erased path.** Adding every edge the walk used creates cycles. Adding the loop-free path built in a different way, for example by erasing loops in a different order, can change the law. The erasure must cut each loop at the moment it closes, which overwriting $\text{Next}$ does.
- **A non-uniform step.** Line L5 must pick an edge, not a neighbor. With parallel edges, a neighbor joined by two edges must be twice as likely. A self-loop has two ends at $u$ and counts twice in $c(u)$.
- **Disconnected input.** A walk in a component without the root never ends. The implementation gives each component its own root.
- **Running out of the tree check.** The test in line L4 must be on the tree, not on the vertices the current walk has seen. A walk that stops at its own past is not loop erasure.

## Implementations

## History

Broder (1989) and Aldous (1990) gave the cover-time algorithm. Wilson (1996) introduced the loop-erased walk method and the cycle popping proof, and Propp and Wilson used the same ideas for exact sampling with coupling from the past. Loop-erased random walks were studied earlier by Lawler in probability, and Pemantle had shown in 1991 that the path between two vertices in a uniform spanning tree has the law of a loop-erased random walk.

## References
