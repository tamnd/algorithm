---
tag: H8SH4G
kind: algorithm
slug: kuhn-algorithm
name: Kuhn's algorithm
aliases:
- Kuhn's augmenting path algorithm
- Kuhn's matching algorithm
area: graphs/matching
level: core
summary: Finds maximum bipartite matching by repeated DFS for augmenting paths, in O(VE) time.
solves: [bipartite-matching]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(n m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: true}
history:
  year: 1955
  people: [Harold W. Kuhn]
  note: Kuhn's 1955 paper on the Hungarian method finds a maximum matching of the zero entries of a matrix by augmenting paths, after Kőnig and Egerváry.
prereqs: [bipartite-graph, augmenting-path, depth-first-search]
see_also: [hopcroft-karp, hungarian-algorithm, berge-lemma, konig-theorem, hall-theorem, edmonds-blossom, ford-fulkerson, maximal-matching]
sources:
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 3.2, Algorithms and applications (the augmenting path algorithm for bipartite graphs and its proof)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Section 7.5, A first application, the bipartite matching problem (the O(mn) bound by augmenting paths)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency, Springer
    locator: Chapter 16, Cardinality bipartite matching and vertex cover (the matching augmenting algorithm and its O(nm) bound)
  - paper: doi:10.1002/nav.3800020109
    title: Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2(1-2), 83 to 97 (1955)
    locator: the first part (a maximum set of independent zeros by an augmenting labeling)
---

Kuhn's algorithm finds a [maximum matching](/bipartite-matching/) in a [bipartite graph](/bipartite-graph/) without weights. For each vertex of the left side in turn, it runs one [depth-first search](/depth-first-search/) for an [augmenting path](/augmenting-path/) that starts there, and flips the path when it finds one. One pass over the left side is enough, so the time is $O(nm)$ on a graph with $n$ vertices and $m$ edges. It is the shortest correct matching code and the base of the faster [Hopcroft-Karp algorithm](/hopcroft-karp/) and of the [Hungarian algorithm](/hungarian-algorithm/).

## In plain words

Workers stand on the left and jobs on the right. Take the workers one at a time. A new worker looks at the jobs they can do. If a job is free, the worker takes it. If a job is taken, the worker asks its current holder to move to another job that the holder can do, and that holder may ask a third worker in the same way. If this chain of requests ends at a free job, everyone on the chain moves one step and the new worker gets a job. If no chain works, the new worker stays without a job, and the algorithm goes on to the next worker.

Each job is asked about at most once for each new worker, so one round is fast. A worker who stays without a job never gets one later, so one round per worker is enough.

## The problem

The input is a [bipartite graph](/bipartite-graph/) $G = (L \cup R, E)$, without weights, where each edge joins a vertex of $L$ to a vertex of $R$. Parallel edges are allowed; they do not change the answer. The output is a matching $M$ of largest size, given as the mate of each vertex of $L$ (nil for an exposed vertex). Write $n = |L| + |R|$ and $m = |E|$. The graph can be empty, and it does not need a perfect matching. For a general graph, with odd cycles, use [Edmonds' blossom algorithm](/edmonds-blossom/) instead.

## The algorithm

```pseudo id=main
KUHN(L, R, Adj)                            ▷ Adj[x] lists the neighbours of x ∈ L
L1  for each u ∈ L do mate_L[u] ← nil;  for each v ∈ R do mate_R[v] ← nil
L2  for each u ∈ L do
L3      visited[v] ← false for each v ∈ R
L4      TRY(u)
L5  return mate_L

TRY(x)                                     ▷ look for an augmenting path from x ∈ L
L6  for each v ∈ Adj[x] do
L7      if not visited[v] then
L8          visited[v] ← true
L9          if mate_R[v] = nil or TRY(mate_R[v]) then
L10             mate_R[v] ← x, mate_L[x] ← v
L11             return true
L12 return false
```

TRY$(x)$ walks an alternating path: from a left vertex $x$ along an edge not in $M$ to a right vertex $v$, then, if $v$ is matched, along the matching edge to $\text{mate}_R[v]$, and so on. When it reaches an exposed right vertex, the calls return true one by one, and line L10 rematches each left vertex on the path to the right vertex after it. This is the augmentation $M \oplus P$. The array `visited` lives for one call of line L4: a right vertex that led to a failure once in this round will fail again, because the matching does not change until the round succeeds.

## Example

The left vertices are $1, 2, 3, 4$ and the right vertices are $a, b, c, d$. The neighbour lists, in scan order, are $1: a, b$; $2: a, c$; $3: a$; $4: c, d$.

| round | search | result | matching after the round | visited |
|---|---|---|---|---|
| $u = 1$ | $a$ is free | $1a$ | $\{1a\}$ | $a$ |
| $u = 2$ | $a$ is held by 1; TRY(1): $b$ is free | path $2\,a\,1\,b$ | $\{1b, 2a\}$ | $a, b$ |
| $u = 3$ | $a$ is held by 2; TRY(2): $c$ is free | path $3\,a\,2\,c$ | $\{1b, 2c, 3a\}$ | $a, c$ |
| $u = 4$ | $c$ is held by 2; TRY(2): $a$ is held by 3; TRY(3) fails; TRY(2) fails; then $d$ is free | $4d$ | $\{1b, 2c, 3a, 4d\}$ | $a, c, d$ |

The result is a perfect matching. In round 4 the first branch fails: vertex 3 has no other neighbour, so the chain $4\,c\,2\,a\,3$ ends with no free vertex.

**A graph with no perfect matching.** Change the lists to $1: a, b$; $2: a$; $3: a$; $4: c, d$. Rounds 1 and 2 give $\{1b, 2a\}$. In round 3, $a$ is held by 2, and TRY(2) fails because $a$ is already visited; vertex 3 stays exposed. Round 4 gives $4c$. The result has size 3. The left set $\{2, 3\}$ has only the neighbour $a$, so by [Hall's theorem](/hall-theorem/) no matching covers both, and 3 is the maximum.

## Correctness

The algorithm returns a maximum matching. Two facts give this. First, when TRY$(u)$ is called with a fresh `visited` array, it returns true exactly when $M$ has an augmenting path from $u$, and then it augments along one. Second, if $M$ has no augmenting path from an exposed vertex $u$, then no later matching $M \oplus P$ has one either. So after the round of $u$, either $u$ is matched and stays matched, or no augmenting path will ever start at $u$. At the end no augmenting path starts at any exposed left vertex, and every augmenting path of a bipartite graph has one end in $L$, so $M$ has no augmenting path and is maximum by [Berge's lemma](/berge-lemma/). The full proof is below.

## Complexity

The model is the [word RAM](/word-ram/) with adjacency lists.

- **One round.** In one round, each right vertex is marked at most once (lines L7 and L8), and TRY is called on $u$ and on the mate of each newly marked vertex, so on each left vertex at most once, because mates are distinct. Each call scans the list of its vertex once. So a round takes $O(|L| + |R| + m)$ time, with the reset of line L3.
- **Total.** There are $|L|$ rounds, so the time is $O(|L| (n + m)) = O(nm)$ when there are no isolated vertices.
- **Resets.** Line L3 costs $\Theta(|R|)$ per round, so $\Theta(|L| \cdot |R|)$ in total even when each search is short. A round number stored in each mark ("visited in round $k$") removes this cost.
- **Space.** $\Theta(n)$ for the mates, the marks and the recursion stack, besides the input. The recursion can be $|L|$ deep, so an implementation in a language with a small stack should use an explicit stack.

## Properties

- **Bipartite only.** The proof of the first fact uses that an alternating walk never comes back to a vertex of the other side; in a graph with odd cycles this fails.
- **Greedy and incremental.** After round $k$, $M$ is a maximum matching of the subgraph induced by the first $k$ left vertices and all of $R$. So the algorithm also answers "add one left vertex" queries in $O(n + m)$ each.
- **Certificate.** In the last failed search from $u$, the visited right vertices $Z$ and the left vertices reached form a set $S$ with $N(S) = Z$ and $|S| = |Z| + 1$, which violates Hall's condition. Running the search from all exposed left vertices at the end gives a minimum vertex cover, as in the proof of [Kőnig's theorem](/konig-theorem/).
- **Deterministic.** The result depends on the order of $L$ and of the lists; its size does not.

## Variants and improvements

- **Greedy start.** Begin with a [maximal matching](/maximal-matching/) found by one scan. It already has at least half the maximum size, which removes many rounds in practice.
- **Do not reset `visited` after a failure.** Keep the marks of a failed round for the next rounds until the next success. A failed search does not change $M$, so the marked vertices are still dead ends. This keeps the worst case and often runs much faster.
- **[Hopcroft-Karp](/hopcroft-karp/).** Find a maximal set of vertex-disjoint shortest augmenting paths in each phase, with one BFS and one DFS. Only $O(\sqrt n)$ phases are needed, so the time is $O(m \sqrt n)$.
- **As a flow.** Kuhn's algorithm is [Ford-Fulkerson](/ford-fulkerson/) on the unit network $s \to L \to R \to t$, with each DFS as one search for an augmenting path in the residual graph.
- **Weighted.** The [Hungarian algorithm](/hungarian-algorithm/) keeps vertex potentials and searches for augmenting paths only along tight edges.

## When to use it

Use Kuhn's algorithm for bipartite graphs with up to some thousands of vertices, in contests and in short scripts. It is about fifteen lines, and with a greedy start it is often as fast as Hopcroft-Karp on random inputs. For large or adversarial graphs, use [Hopcroft-Karp](/hopcroft-karp/), whose worst case is $O(m \sqrt n)$. For a general graph, use [Edmonds' blossom algorithm](/edmonds-blossom/). For weights, use the [Hungarian algorithm](/hungarian-algorithm/).

## Pitfalls

- **Forgetting to reset the marks after a success.** Line L3 must clear `visited` before each round that follows a success, because line L10 has changed the mates and an old dead end can now lead somewhere. With the lists $1: a, b$ and $2: a$, round 1 marks $a$ and matches $1a$. If the marks are kept, round 2 sees $a$ as visited and fails, so the result has size 1, while $\{1b, 2a\}$ has size 2.
- **Marking after the call.** Line L8 must mark $v$ before the recursive call of line L9. If the mark is set only after TRY returns, the search can reach $v$ again from deeper on the same path and call TRY on the same left vertex again, without end.
- **Using it on a general graph.** In a graph with an odd cycle, the same search can miss an augmenting path that enters the cycle on one side and leaves on the other. The answer can then be too small. A [blossom](/blossom/) must be contracted, as in Edmonds' algorithm.
- **Deep recursion.** An augmenting path can have $2|L| - 1$ edges. In Python or Java the recursive TRY overflows the stack for some thousands of vertices; use an explicit stack.

## Implementations

The Python version takes the sizes of the two sides and the neighbour lists of the left vertices, and returns the mate of each left vertex. TRY runs on an explicit stack, and the flip of line L10 walks the stack from top to bottom.

## History

Dénes Kőnig proved in 1931 that the size of a maximum matching of a bipartite graph equals the size of a least vertex cover, and Jenő Egerváry gave a weighted form the same year. Harold Kuhn turned their proofs into an algorithm in his 1955 paper on the Hungarian method: its first part finds a largest set of independent zeros of a matrix, that is, a maximum matching of a bipartite graph, by growing alternating paths. Hopcroft and Karp reduced the worst case to $O(m \sqrt n)$ in 1973.

## References
