---
tag: R9M66X
kind: algorithm
slug: tree-center-leaf-peeling
name: Tree center by leaf peeling
aliases:
- onion peeling
area: graphs/tree-algorithms
level: intro
summary: Repeatedly delete all leaves; the last one or two remaining nodes are the center.
solves: [tree-center]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, weighted: false}
prereqs: [tree-center, tree-edge-count, eccentricity]
see_also: [tree-diameter-double-sweep, tree-diameter, kahns-algorithm, centroid, tree-isomorphism, ahu-algorithm, degeneracy-ordering, rerooting-technique]
sources:
  - paper: Camille Jordan, Sur les assemblages de lignes, Journal für die reine und angewandte Mathematik 70, 185 to 190 (1869)
    locator: the centre of a tree, found by removing the extreme vertices step by step until one vertex or one edge remains
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.1 (Basic properties of trees), Jordan's theorem on the centre and its proof by deleting all leaves
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.4 (Enumeration of trees), the use of the centroid and centre to root a free tree when counting free trees
---

Leaf peeling finds the [centre of a tree](/tree-center/) by deleting all leaves at once, again and again, until one or two vertices are left. Those vertices are the centre, and the number of rounds gives the radius and the diameter. The method works on an unweighted free tree, uses only degree counters and lists, and runs in $\Theta(n)$ time. It is the same queue discipline as [Kahn's algorithm](/kahns-algorithm/) for topological sorting, applied to leaves instead of sources, and its proof is Jordan's proof that the centre is one vertex or two adjacent vertices.

## In plain words

Look at a tree and remove every leaf, every node that has only one neighbour, all at the same time. What is left is still a tree. Do it again with the new leaves. The tree shrinks from all its tips toward the middle, like peeling an onion.

Stop when one or two nodes are left. These are the centre: the nodes whose farthest node is the closest. The reason is that removing all leaves makes every remaining node exactly one step closer to its farthest node, so the order of the nodes by their worst distance does not change.

To do it fast, keep for each node the number of neighbours it still has. When a leaf is removed, its neighbour loses one. A node whose count drops to one becomes a leaf of the next round.

## The problem

The input is a free tree with the vertices $0, \ldots, n-1$, $n \ge 1$, given as $n - 1$ edges. It is not rooted and not weighted: the distance is the number of edges. The output is the centre, the set of vertices of smallest [eccentricity](/eccentricity/), sorted, and the number $k$ of peeling rounds. For $n \ge 2$ the radius is $k$ if the centre has one vertex and $k + 1$ if it has two, and the diameter is $2k + |{\rm centre}| - 1$. This is the [tree center](/tree-center/) problem.

## The algorithm

```pseudo id=main
LEAF-PEEL(n, adj)                        ▷ adj[v]: the neighbours of v in the tree
L1  if n ≤ 2 then return all vertices
L2  for each vertex v do deg[v] ← |adj[v]|
L3  L ← the list of v with deg[v] = 1;  left ← n
L4  while left > 2 do
L5      left ← left − |L|
L6      L′ ← an empty list
L7      for each u in L do
L8          deg[u] ← 0                   ▷ u is removed
L9          for each v in adj[u] with deg[v] > 0 do
L10             deg[v] ← deg[v] − 1
L11             if deg[v] = 1 then append v to L′
L12     L ← L′
L13 return L
```

The counter $\mathrm{deg}[v]$ is the degree of $v$ in the tree that is left, and $0$ for a removed vertex. Each round removes the list $L$ of the current leaves. Line L9 finds the one neighbour of $u$ that is still present. A vertex whose degree falls to 1 at line L11 is a leaf of the next tree. When the loop stops, $L$ holds exactly the one or two vertices that are left.

## Example

Take the tree with the edges $01, 02, 13, 14, 25, 46, 47$.

```
          0
        /   \
       1     2
      / \     \
     3   4     5
        / \
       6   7
```

| round | leaves removed ($L$) | degree changes | left after | next leaves ($L'$) |
|---|---|---|---|---|
| start | | $\mathrm{deg} = 2, 3, 2, 1, 3, 1, 1, 1$ | 8 | $3, 5, 6, 7$ |
| 1 | $3, 5, 6, 7$ | $1{:}\,3 \to 2$, $2{:}\,2 \to 1$, $4{:}\,3 \to 2 \to 1$ | 4 | $2, 4$ |
| 2 | $2, 4$ | $0{:}\,2 \to 1$, $1{:}\,2 \to 1$ | 2 | $0, 1$ |

Two vertices are left after $k = 2$ rounds, so the centre is $\{0, 1\}$, the radius is $k + 1 = 3$, and the diameter is $2k + 1 = 5$. The eccentricities of $0, \ldots, 7$ are $3, 3, 4, 4, 4, 5, 5, 5$, which agrees.

The small cases: for $n = 1$ and $n = 2$, line L1 returns all vertices. On the path $0, \ldots, n-1$, each round removes the two ends; for odd $n$ the centre is $\{(n-1)/2\}$ after $(n-1)/2$ rounds, and for even $n$ it is $\{n/2 - 1, n/2\}$ after $n/2 - 1$ rounds. On a star with $n \ge 3$, the first round removes the $n - 1$ leaves, the centre's counter goes down to 1 and then to 0, and the result is the centre alone after one round.

## Correctness

Let $T$ be a tree with at least 3 vertices and $T'$ the tree left after removing all its leaves. Two facts carry the proof. First, $T'$ is a tree, and its distances are those of $T$, because no path between two non-leaves passes through a leaf. Second, for each vertex $v$ of $T'$, $\mathrm{ecc}_{T'}(v) = \mathrm{ecc}_T(v) - 1$: a farthest vertex from $v$ in $T$ is a leaf, its neighbour toward $v$ is in $T'$ at one step less, and each vertex of $T'$ has a neighbour one step farther from $v$. So each round lowers every remaining eccentricity by one, the vertices of smallest eccentricity stay the same, and the loop stops with the one or two vertices that are left, which are the centre of the last tree and so of $T$. The counters keep the degree of the remaining tree, and $L'$ is exactly its leaf list. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model with adjacency lists.

- Each vertex enters a list $L$ at most once, because it is appended only when its counter reaches 1 for the first time, at line L3 or L11, and it is removed in the next round.
- When a vertex $u$ is removed, line L9 reads its adjacency list once. The total over all vertices is $\sum_u \deg u = 2(n - 1)$, by the [tree edge count](/tree-edge-count/).
- Line L5 and line L12 take $O(1)$ time each per round, and there are at most $n/2$ rounds.

So the time is $\Theta(n)$ in every case, and the extra space is $\Theta(n)$ for the counters and the lists.

## Properties

- **Deterministic and not recursive.** Only counters and lists are used, so a path of $10^5$ vertices is safe in any language.
- **Unweighted.** The proof uses that each edge has length 1. On a weighted tree, a round removes leaves at different distances, and the method can return the wrong vertex.
- **Radius and diameter.** With $k$ rounds and $c$ vertices left, the radius is $k + c - 1$ and the diameter is $2k + c - 1$, for $n \ge 2$.
- **Layers.** The rounds split the vertices into layers. A leaf that hangs next to the centre is removed in round 1, so the round of a vertex is not a function of its eccentricity alone.

## Variants and improvements

- **Queue form.** Put the first leaves in a FIFO queue with the round number $0$, and push each new leaf with the round number of the leaf that freed it, plus one. The last one or two vertices pushed are the centre. This is a breadth-first search that starts from all leaves at once, as in [multi-source BFS](/multi-source-bfs/).
- **Double sweep.** The [double sweep](/tree-diameter-double-sweep/) finds a diametral path, and its middle is the centre. It also works with non-negative weights.
- **Centroid.** The [centroid](/centroid/) is a different centre, defined by subtree sizes and not by distances. It is found from [subtree sizes](/subtree-sizes/), not by rounds of leaf removal.
- **$k$-cores of a tree and degeneracy.** Removing all vertices of degree at most 1 is the first step of the [degeneracy ordering](/degeneracy-ordering/) of any graph. On a tree it removes everything, which shows that a tree is 1-degenerate.

## When to use it

Use leaf peeling for the centre of an unweighted tree when a short program without recursion is wanted and the tree is given as an edge list. It needs no distance arrays. It is also the natural method when you want the layers, for example to process a tree from the outside in. On a weighted tree, use the double sweep and take the vertices nearest to the midpoint of the diametral path.

## Pitfalls

- **Removing leaves one at a time.** If line L11 adds a new leaf to the current list $L$ instead of $L'$, the rounds mix, and the last vertex left can be any vertex of a longest path, not the centre. The new leaves must wait for the next round.
- **Wrong stopping test.** The loop must stop when at most 2 vertices are left (line L4). Stopping when $L$ is empty removes the centre too.
- **Small trees.** For $n = 1$ the single vertex has degree 0 and is never a leaf, and for $n = 2$ both vertices are leaves at once. Line L1 handles both.
- **Weights.** On a weighted tree, peeling by rounds ignores the lengths and can return a vertex that is not the centre. Use the double sweep there.

## Implementations

## History

Jordan's paper of 1869 on assemblages of lines proves that the centre of a tree is a vertex or an edge by taking away the extreme vertices step by step, which is this algorithm. West gives the same proof in the first section of the chapter on trees. Knuth uses the centre and the centroid of a free tree to root it in a canonical way in the section on the enumeration of trees.

## References
