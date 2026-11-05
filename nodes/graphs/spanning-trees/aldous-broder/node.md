---
tag: KAFQ9E
kind: algorithm
slug: aldous-broder
name: Aldous-Broder algorithm
aliases:
- Aldous-Broder random walk algorithm
area: graphs/spanning-trees
level: advanced
summary: Builds a uniform random spanning tree from the first-visit edges of a random walk.
solves: [uniform-spanning-tree-sampling]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {expected: O(m n)}
  space: {extra: O(n + m)}
properties: {deterministic: false, recursive: false}
prereqs: [spanning-tree, markov-chain, stationary-distribution, uniform-spanning-tree-sampling]
see_also: [wilson-algorithm, matrix-tree-theorem, counting-spanning-trees, randomized-algorithm, las-vegas-algorithm, breadth-first-search, spanning-forest, fundamental-cycle]
sources:
  - paper: doi:10.1109/SFCS.1989.63516
    title: "Andrei Z. Broder, Generating random spanning trees, Proceedings of the 30th Annual Symposium on Foundations of Computer Science (1989), 442-447"
    locator: the whole paper (the algorithm and its proof by the tree process of the walk)
  - paper: doi:10.1137/0403039
    title: "David J. Aldous, The random walk construction of uniform spanning trees and uniform labelled trees, SIAM Journal on Discrete Mathematics 3(4) (1990), 450-465"
    locator: the whole paper (the same construction, found independently)
  - book: isbn:9781107160156
    title: Russell Lyons and Yuval Peres, Probability on Trees and Networks, Cambridge University Press (2016)
    locator: Chapter 4, Uniform Spanning Trees (the Aldous-Broder algorithm and the Markov chain tree theorem)
  - paper: doi:10.1109/SFCS.1979.34
    title: "Romas Aleliunas, Richard M. Karp, Richard J. Lipton, László Lovász and Charles Rackoff, Random walks, universal traversal sequences, and the complexity of maze problems, Proceedings of the 20th Annual Symposium on Foundations of Computer Science (1979), 218-223"
    locator: the bound 2m(n - 1) on the expected cover time
---

The Aldous-Broder algorithm samples a [spanning tree](/spanning-tree/) of a connected undirected graph uniformly at random. It runs a simple random walk from any start vertex until the walk has visited every vertex, and for each vertex other than the start it keeps the edge by which the walk *first* entered it. These $n - 1$ first-entrance edges form a spanning tree, and each of the $\tau(G)$ spanning trees comes out with probability exactly $1 / \tau(G)$. Broder (1989) and Aldous (1990) found it independently. The running time is the cover time of the walk, which is at most $2m(n - 1)$ steps in expectation and can be that large. With edge weights as step probabilities, the same walk samples a tree with probability proportional to the product of its weights.

## In plain words

You want to pick one of all the possible connecting trees of a network, with every tree equally likely. Counting them all and picking one by number is slow.

Instead, walk through the network at random. Start at any point. At each step, take a link at random among the links at the point where you stand, and go to its other end. Each time you reach a point you have never seen, write down the link you just used. Stop when you have seen every point.

The links you wrote down connect all points without a loop, because each one leads to a new point. The surprising fact is that every possible tree is equally likely to be the result.

## The problem

The input is a finite undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a source of random bits. Parallel edges are allowed and are different edges. Self-loops are allowed: the walk may take them, but they are in no spanning tree.

- **Unweighted.** The output is a spanning tree $T$ with $\Pr[T = t] = 1 / \tau(G)$ for each spanning tree $t$, where $\tau(G)$ is the number of spanning trees.
- **Weighted.** Each edge has a weight $c_e > 0$, a *conductance*. The walk at $x$ takes edge $e$ with probability $c_e / c(x)$, where $c(x)$ is the sum of the weights at $x$. The output satisfies $\Pr[T = t] \propto \prod_{e \in t} c_e$. Weights of zero or less are not allowed; ties in weight are allowed and do not matter. The weights here are not edge costs, and the algorithm does not look for a minimum.
- **Disconnected graphs.** A walk cannot leave its component. The implementation runs one walk in each component, so the output is a [spanning forest](/spanning-forest/) that is uniform among the spanning forests with the components of $G$, since a uniform choice in each component is independent of the others.

## The algorithm

```pseudo id=main
ALDOUS-BRODER(G, r)
L1  x ← r
L2  mark x as visited; T ← ∅
L3  while some vertex is not visited do
L4      choose an edge e = (x, y) at x at random, with probability c_e / c(x)
L5      if y is not visited then
L6          mark y as visited
L7          T ← T ∪ {e}                ▷ the first-entrance edge of y
L8      x ← y
L9  return T
```

For the unweighted problem, $c_e = 1$ for each edge, so line L4 takes a uniformly random edge at $x$. The implementation counts the visited vertices of the component to test line L3 in $O(1)$ time, and keeps prefix sums of the weights at each vertex, so line L4 takes $O(\log \deg x)$ time with weights and could take $O(1)$ time without them.

## Example

The graph has the vertices $a$ to $f$ and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$; it has 55 spanning trees. One possible walk from $a$ is:

| step | move | new vertex? | edge kept |
|---|---|---|---|
| 1 | $a \to c$ | $c$ | $ac$ |
| 2 | $c \to b$ | $b$ | $bc$ |
| 3 | $b \to c$ | no | |
| 4 | $c \to a$ | no | |
| 5 | $a \to b$ | no | |
| 6 | $b \to d$ | $d$ | $bd$ |
| 7 | $d \to c$ | no | |
| 8 | $c \to e$ | $e$ | $ce$ |
| 9 | $e \to d$ | no | |
| 10 | $d \to f$ | $f$ | $df$ |

The walk stops after 10 steps, with the tree $\{ac, bc, bd, ce, df\}$. Each of the 55 trees has probability $1/55$ to be the result. The tests draw 11000 trees and check the counts against $200$ per tree with a chi-square statistic.

## Correctness

**Theorem.** Let $G$ be connected, with positive edge weights, and let $r$ be any vertex. With probability 1, ALDOUS-BRODER stops, and for each spanning tree $t$,

$$\Pr[T = t] = \frac{\prod_{e \in t} c_e}{\sum_{t'} \prod_{e \in t'} c_e},$$

which is $1 / \tau(G)$ when all weights are 1.

The output is a spanning tree because each kept edge joins a new vertex to the visited ones, so the kept edges form a tree on the visited set, and the loop ends when all $n$ vertices are visited. The walk on a finite connected graph visits every vertex with probability 1.

The distribution comes from a Markov chain on *rooted* spanning trees. Let the walk run forever in both directions from its stationary distribution, and at each time $k$ let $t_k$ be the tree, rooted at the current vertex $X_k$, made of the *last-exit* edge of each other vertex before time $k$. When the walk moves from $X_k$ to $X_{k+1}$, the tree changes by a fixed rule: the edge from $X_k$ to $X_{k+1}$ becomes the out-edge of $X_k$, and the old out-edge of $X_{k+1}$ is dropped. A short computation shows that the weight $\prod_{x \ne \rho} p(x, t(x))$, with $p$ the step probabilities and $t(x)$ the parent of $x$, is stationary for this chain. The time reversal of a reversible walk is the same walk, and reversal turns the last-exit edges of the past into the first-entrance edges of the future. So the first-entrance tree of a stationary walk has this law, and conditioning on the start vertex leaves a law proportional to $\prod_{e \in t} c_e$. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM with a source of uniform random numbers.

- **Steps.** The loop runs until the walk covers the graph. The expected cover time of a connected graph with $n$ vertices and $m$ edges, for the simple random walk, is at most $2m(n - 1)$ (Aleliunas et al., 1979). The proof: the expected time for the walk to cross an edge $uv$ and come back is at most $2m$, and a walk along a spanning tree in depth-first order crosses $n - 1$ edges twice each.
- **The bound is reached up to a constant.** On a path with $n$ vertices from one end, the expected cover time is $(n - 1)^2$, so $\Theta(n^2) = \Theta(mn)$. On the lollipop graph, a clique on about $2n/3$ vertices joined to a path, it is $\Theta(n^3)$ with $m = \Theta(n^2)$. On the complete graph it is only $\Theta(n \log n)$, by the coupon collector argument.
- **One step.** $O(1)$ unweighted and $O(\log \deg x)$ with weights.
- **Space.** $O(n + m)$ for the adjacency lists and the marks.

| claim | bound | case |
|---|---|---|
| steps | cover time, at most $2m(n - 1)$ expected | each connected graph |
| steps | $\Theta(mn)$ expected | path, lollipop |
| steps | $\Theta(n \log n)$ expected | complete graph |
| space | $O(n + m)$ | worst |

The running time is a random variable with no worst-case bound, so the algorithm is a [Las Vegas algorithm](/las-vegas-algorithm/): its output always has the right law, and only its time is random.

## Properties

- **Exact.** The law of the output is exactly uniform (or exactly proportional to the weight product), not an approximation, and the walk needs no mixing time.
- **Any start vertex.** The law does not depend on $r$.
- **Las Vegas.** The time is random; the expected time is the cover time.
- **Local and simple.** It needs only the ability to take a random step, so it works on graphs that are given implicitly.
- **Not deterministic.**

## Variants and improvements

- **[Wilson's algorithm](/wilson-algorithm/).** Loop-erased random walks give the same law in the expected *mean hitting time* of the walk, which is never more than the cover time and is often much less, for example $O(n)$ steps on the complete graph against $\Theta(n \log n)$.
- **Faster than the cover time.** Kelner and Mądry (2009) and later papers shortcut the walk in the parts already covered. An almost-linear time algorithm was given by Schild (2018).
- **Determinant methods.** With the [matrix-tree theorem](/matrix-tree-theorem/), one can decide each edge in turn, keeping it with probability $\tau(G / e) / \tau(G)$. This takes polynomial time with no randomness in the time.
- **Uniform labelled trees.** On the complete graph $K_n$, the algorithm gives a uniform labelled tree on $n$ vertices; Aldous used this to study the shape of random trees.

## When to use it

Use Aldous-Broder when you need exact uniform samples and the graph covers fast, such as an expander or a dense random graph, or when you need the simplest correct code, for example to test another sampler. Use [Wilson's algorithm](/wilson-algorithm/) by default, since it is never slower in expectation. Avoid it on graphs with a slow cover time, such as long paths or graphs with bottlenecks.

## Pitfalls

- **Keeping the last edge instead of the first.** The edge kept for $y$ is the edge of the *first* visit. If the code keeps, for each vertex, the edge of its last entrance before the walk stops, two vertices can keep the same edge, and the result need not be a spanning tree. On a triangle $a, b, c$ with an extra edge $cd$, and a walk from $d$, this happens in about one third of the runs.
- **A non-uniform step.** Line L4 must pick an edge, not a neighbor: with parallel edges, a neighbor joined by two edges must be twice as likely. Picking a uniform neighbor gives the wrong law on multigraphs.
- **Disconnected input.** A walk cannot reach other components, so the loop "until all vertices are visited" never ends. The implementation counts the vertices of the current component first.
- **A search with a random order is not uniform.** A depth-first search that visits the neighbors in random order produces a random spanning tree, but not a uniform one. On $K_4$ a depth-first search tree is always a path, so the 4 stars among the 16 spanning trees never appear.

## Implementations

## History

Broder (1989) and Aldous (1990) published the algorithm independently. Broder's proof uses the chain on rooted trees, which is closely tied to the Markov chain tree theorem; Aldous also used the construction to derive properties of random labelled trees. Wilson (1996) gave the faster loop-erased walk method.

## References
