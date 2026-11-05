---
tag: DNDY29
kind: technique
slug: rerooting-technique
name: Rerooting technique
aliases:
- rerooting DP
area: graphs/tree-algorithms
level: advanced
summary: Compute a quantity for every node as root by reusing DP values from neighbors.
prereqs: [tree-dynamic-programming, rooted-tree, subtree-sizes]
see_also: [tree-center, tree-diameter, eccentricity, centroid, prefix-sums, monoid, tree-hashing, euler-tour-technique]
sources:
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook (free PDF edition)
    locator: Chapter 14, Tree algorithms, Section 14.3 (All longest paths, the maximum length of a path from every node, with one pass down and one pass up)
---

The rerooting technique computes a [tree dynamic program](/tree-dynamic-programming/) once for every possible root of a free tree, in $\Theta(n)$ total time and not $\Theta(n^2)$. It roots the tree once, computes the usual bottom-up value of each subtree in a first pass, and then, in a second pass from the root down, computes for each vertex the value of the part of the tree above it. The answer for a vertex as root combines the values of all its neighbouring parts. Standard uses are all [eccentricities](/eccentricity/), the sum of the distances from every vertex, and the [tree hash](/tree-hashing/) of the tree rooted at each vertex.

## In plain words

You can solve a problem on a tree when you pick one node as the top: each node collects a summary from each child and passes its own summary up. Now you want the answer with each node as the top in turn. Doing the whole job again for each node is slow.

The trick is to see that a node with a different top only gets one new branch: the part of the tree that used to be above it. So you do the normal upward pass once. Then you walk down from the top, and each node tells each child a summary of everything that is not in the child's own branch. With the summaries from below and the one from above, each node has all the branches around it, and so its answer.

## When it applies

- The tree is free, not rooted, with the vertices numbered $0, \ldots, n-1$ and given as a list of $n - 1$ edges. The technique fixes an arbitrary root $r$ only as a tool; the answers do not depend on it. The tree may be weighted, on the vertices or on the edges, if the dynamic program uses the weights.
- A quantity $F(v)$ is wanted for every vertex $v$, where $F(v)$ is the result of a bottom-up dynamic program on the tree rooted at $v$.
- At each vertex the dynamic program merges the values of the neighbouring parts with an operation $\oplus$ that is associative and commutative and has an identity $e$, that is, a commutative [monoid](/monoid/). The order of the children must not matter.
- The value that a part sends across an edge, and the final value of a vertex, are $O(1)$ functions of the merged value.

## The template

Write $N(v)$ for the neighbours of $v$. For an edge $\{u, v\}$, the part $T_{u \setminus v}$ is the component of $u$ after the edge is removed, rooted at $u$. It is the subtree of $u$ in every rooting in which $v$ is the parent of $u$. The dynamic program has three holes.

- $\oplus$ and $e$: merge the contributions of several parts.
- $\mathrm{LIFT}(x)$: turn the value $x$ of the part $T_{u \setminus v}$ into its contribution at $v$, across the edge.
- $\mathrm{FINISH}(v, y)$: turn the merged contributions $y$ of some parts at $v$ into the value of $v$ with these parts below it.

So the value of a part satisfies $\mathrm{val}(T_{u \setminus v}) = \mathrm{FINISH}(u, \bigoplus_{w \in N(u), w \ne v} \mathrm{LIFT}(\mathrm{val}(T_{w \setminus u})))$, and the wanted answer is $F(v) = \mathrm{FINISH}(v, \bigoplus_{w \in N(v)} \mathrm{LIFT}(\mathrm{val}(T_{w \setminus v})))$.

Root the tree at $r$ and let $p(v)$ be the parent of $v$. Then $\mathit{down}[v] = \mathrm{val}(T_{v \setminus p(v)})$ is the value of the subtree of $v$, and $\mathit{up}[v] = \mathrm{val}(T_{p(v) \setminus v})$ is the value of the part above $v$, seen from $v$.

```pseudo id=main
REROOT(tree, r)
L1  order ← the vertices in BFS order from r; p ← the parents
L2  for v in order, from the last to the first do
L3      down[v] ← FINISH(v, ⊕ of LIFT(down[c]) over the children c of v)
L4  for v in order, from the first to the last do
L5      top ← LIFT(up[v]) if v ≠ r, else e
L6      let c_1, …, c_k be the children of v, and a_i ← LIFT(down[c_i])
L7      pre[0] ← e; pre[i] ← pre[i − 1] ⊕ a_i for i = 1, …, k
L8      suf[k + 1] ← e; suf[i] ← a_i ⊕ suf[i + 1] for i = k, …, 1
L9      F[v] ← FINISH(v, top ⊕ pre[k])
L10     for i ← 1 to k do
L11         up[c_i] ← FINISH(v, top ⊕ pre[i − 1] ⊕ suf[i + 1])
L12 return F
```

**Why it is right.** Line L1 puts each vertex after its parent. The backward scan of line L2 reaches each vertex after all its children, so line L3 applies the defining equation with $v$'s parent left out, and gives $\mathit{down}[v] = \mathrm{val}(T_{v \setminus p(v)})$ by induction on the height, as on [subtree sizes](/subtree-sizes/). The forward scan of line L4 reaches $v$ after $p(v)$, so $\mathit{up}[v]$ is already set when $v \ne r$. The neighbours of $v$ are its children and, if $v \ne r$, its parent. Line L9 merges the contributions of all of them, so it is the definition of $F(v)$. Line L11 merges the contributions of all neighbours of $v$ except $c_i$: the parent through $\mathit{top}$ and the other children through the prefix and the suffix. This is the defining equation of $\mathrm{val}(T_{v \setminus c_i}) = \mathit{up}[c_i]$. Commutativity lets the order of the merged terms change.

**Cost.** Each vertex is handled once in each pass. At a vertex with $k$ children, lines L6 to L11 take $O(k + 1)$ operations, and the sum of $k + 1$ over all vertices is $2n - 1$. So the time is $\Theta(n)$ when $\oplus$, LIFT and FINISH take $O(1)$, and the space is $\Theta(n)$. Both passes are loops over an order, with no recursion, which matters for a path of $10^5$ vertices.

**When $\oplus$ has an inverse.** If $\oplus$ is a group operation, such as $+$ on numbers or on pairs, line L11 can be $\mathrm{FINISH}(v, \mathit{all} \ominus a_i)$ with $\mathit{all} = \mathit{top} \oplus \mathrm{pre}[k]$, and the prefix and suffix arrays are not needed. For $\max$ there is no inverse, and the usual short form keeps the two largest contributions at $v$: the best one leaving out $c_i$ is the largest, or the second largest when $c_i$ gives the largest.

### Example

Take the tree on $\{0, \ldots, 7\}$ with the edges $01, 02, 13, 14, 25, 46, 47$, rooted at $r = 0$, so $p = [-1, 0, 0, 1, 1, 2, 4, 4]$. The tree is not weighted. Find every [eccentricity](/eccentricity/), the largest distance from a vertex.

The value of a part is its height seen from its top vertex. So $\oplus = \max$ with $e = -\infty$, $\mathrm{LIFT}(h) = h + 1$ (one more edge), and $\mathrm{FINISH}(v, y) = \max(y, 0)$ (a part with only $v$ has height $0$).

| $v$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $\mathit{down}[v]$, the height of the subtree | 3 | 2 | 1 | 0 | 1 | 0 | 0 | 0 |
| $\mathit{up}[v]$, the height of the part above | none | 2 | 3 | 3 | 3 | 4 | 4 | 4 |
| $F(v) = \mathrm{ecc}(v)$ | 3 | 3 | 4 | 4 | 4 | 5 | 5 | 5 |

For instance at $v = 1$: $\mathit{top} = \mathrm{LIFT}(\mathit{up}[1]) = 3$, the children $3, 4$ give $a = (1, 2)$, so $F(1) = \max(3, 1, 2) = 3$. For the child $3$, the other contributions are $3$ and $2$, so $\mathit{up}[3] = 3$: the farthest vertex from $1$ outside the subtree of $3$ is at distance $3$. The minimum of $F$ is $3$ at $\{0, 1\}$, the [centre](/tree-center/), and the maximum is $5$, the [diameter](/tree-diameter/).

The same pass with the sum of the distances: a part has the value $(c, s)$, its number of vertices and the sum of their distances to its top vertex. Take $\oplus$ the sum of pairs, $e = (0, 0)$, $\mathrm{LIFT}(c, s) = (c, s + c)$ (every vertex of the part is one edge farther), and $\mathrm{FINISH}(v, (c, s)) = (c + 1, s)$ (add $v$ itself). The second entry of $F$ is then $14, 12, 18, 18, 14, 24, 20, 20$ for $v = 0, \ldots, 7$. Their sum is $140$, twice the sum $70$ over unordered pairs. The smallest sum, $12$, is at $1$, the [centroid](/centroid/).

The small cases. On a single vertex, $F(0) = \mathrm{FINISH}(0, e)$, and the second pass does nothing. On the path $0, 1, \ldots, n-1$ rooted at $0$, $\mathit{down}[v] = n - 1 - v$ and $\mathit{up}[v] = v - 1$ for the heights, so $\mathrm{ecc}(v) = \max(v, n - 1 - v)$. On the star with centre $0$, each leaf has $\mathit{down} = 0$ and $\mathit{up} = 1$ when $n \ge 3$, so its eccentricity is $2$, and the centre has eccentricity $1$.

## Classic examples

- **All eccentricities.** The example above, $\Theta(n)$ time. With non-negative edge weights, LIFT adds the weight of the edge, and the values stay correct.
- **Sum of the distances from each vertex.** The pair form above. With the inverse of $+$ it has the short form $S(c) = S(v) + n - 2 s(c)$ for a child $c$ of $v$, where $s$ are the [subtree sizes](/subtree-sizes/): moving the root along the edge brings $s(c)$ vertices one step closer and takes $n - s(c)$ one step farther.
- **Number of vertices at distance at most $k$, or the farthest vertex of each colour.** The value is a short vector, and $\oplus$ works entry by entry.
- **Rooted hash of every root.** A [tree hash](/tree-hashing/) that merges the child hashes with a commutative operation gives, by rerooting, the hash of the tree rooted at each vertex, so all roots can be compared in $\Theta(n)$ time.
- **Counting orientations or labellings with a root.** For example, the number of ways to delete vertices one at a time so that the remaining ones stay connected, ending at $v$, for each $v$. The value is a pair of a count and a size, and the merge multiplies counts by binomial coefficients.

## Variations

- **Edge answers.** The pair $(\mathit{down}[c], \mathit{up}[c])$ gives the values of the two sides of the edge $\{c, p(c)\}$. So the technique also answers questions for every edge, such as the best edge to cut.
- **Non-commutative merges.** If the children are ordered and $\oplus$ is only associative, the prefix and suffix still work, but the parent's contribution must be put in its correct place in the order, which depends on the problem.
- **Merges that cost more than $O(1)$.** When a value is a list or a polynomial, the prefix and suffix at a vertex of degree $k$ cost $O(k)$ merges, so the time is $O(n)$ merges in total. Small-to-large merging, as in [DSU on tree](/dsu-on-tree/), helps when the values are sets.
- **Dynamic trees.** When the tree changes, a rerooting value for one root at a time is kept by top trees or link-cut trees, which move the root with an evert operation.

## Pitfalls

- **Recomputing for each root.** Running the full dynamic program from every vertex costs $\Theta(n^2)$. On a path of $10^5$ vertices that is $10^{10}$ steps.
- **Subtracting a maximum.** $\max$ has no inverse. Taking "the best of all minus the child" fails when the child gives the best value. Use the prefix and suffix, or the two largest values.
- **Forgetting the parent's part.** At the root, $\mathit{top} = e$. At every other vertex, the part above must be merged both into $F(v)$ and into each $\mathit{up}[c]$. Leaving it out gives the values of the subtrees only.
- **LIFT applied twice or not at all.** $\mathit{down}$ and $\mathit{up}$ store values of parts, not contributions. Each is lifted exactly once when it crosses an edge.
- **Deep recursion.** A recursive first pass overflows the Python call stack on a path of $10^5$ vertices. Use the BFS order of line L1, as in the template.

## Exercises

1. Use rerooting to find, for every vertex $v$, the number of vertices at distance exactly $2$ from $v$. Check your answer on the star.
2. For a tree with positive edge weights, compute for each vertex the sum of the weighted distances to all others, in $O(n)$ time, with the short form $S(c) = S(v) + w(v, c)(n - 2 s(c))$. Prove the formula.
3. Show that the vertex with the smallest sum of distances is a [centroid](/centroid/) vertex, using the short form of the sum.
4. Give a version of lines L7 to L11 that uses $O(1)$ extra space at each vertex for $\oplus = \max$, by keeping the two largest contributions and the child that gives the largest.

## References
