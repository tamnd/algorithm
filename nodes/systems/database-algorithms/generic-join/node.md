---
tag: 5SQ32K
kind: algorithm
slug: generic-join
name: Generic join
aliases:
- GenericJoin
area: systems/database-algorithms
level: research
summary: "Join many relations one attribute at a time: intersect the candidate values from each relation, loop over the smallest set; the time is within the AGM bound."
solves: [multiway-join]
model: word-ram
complexity:
  vars: {n: the total number of input tuples, k: the number of attributes, r: the number of relations, a: the AGM bound of the instance}
  time: {worst: O(k n log n + k r a log n), expected: O(k n + k r a)}
  space: {extra: O(k n)}
properties: {deterministic: true, recursive: true, online: false}
prereqs: [agm-bound, trie, hash-table, relational-join]
see_also: [leapfrog-triejoin, multiway-join, yannakakis-algorithm, hash-join, sorted-array-intersection, triangle-listing-by-degree, hypercube-shares-join, hypergraph]
sources:
  - paper: doi:10.1145/2590989.2590991
    title: Hung Q. Ngo, Christopher Ré and Atri Rudra, Skew strikes back, new developments in the theory of join algorithms, SIGMOD Record 42(4), 5 to 16 (2013)
    locator: the section on worst-case optimal algorithms (Algorithm Generic-Join, its analysis by the query decomposition lemma, and the skewed triangle example)
  - paper: doi:10.1145/3180143
    title: Hung Q. Ngo, Ely Porat, Christopher Ré and Atri Rudra, Worst-case optimal join algorithms, Journal of the ACM 65(3), Article 16 (2018); first in PODS 2012, 37 to 48
    locator: the NPRR algorithm and the proof that it runs in time within the AGM bound
  - paper: doi:10.1137/110859440
    title: Albert Atserias, Martin Grohe and Dániel Marx, Size bounds and query plans for relational joins, SIAM Journal on Computing 42(4), 1737 to 1767 (2013)
    locator: the output size bound that generic join meets
  - paper: doi:10.5441/002/icdt.2014.13
    title: Todd L. Veldhuizen, Leapfrog triejoin, a simple, worst-case optimal join algorithm, ICDT 2014, 96 to 106
    locator: leapfrog triejoin, an instance of the same attribute-at-a-time scheme with sorted tries
---

Generic join computes a [multiway join](/multiway-join/) one attribute at a time instead of one relation at a time. For the next attribute in a fixed order, it takes from each relation that holds the attribute the set of values that agree with the bound attributes, loops over the smallest of these sets, and keeps a value if every other set holds it. Ngo, Ré and Rudra (2013) proved that the work at each attribute is at most the [AGM bound](/agm-bound/), so the running time is $O(\text{AGM})$ up to factors in the query size and, with sorted data, a log factor. On the triangle query with $N$ tuples per relation it takes $O(N^{3/2})$ time, while every plan of pairwise joins can take $\Theta(N^2)$.

## In plain words

You want all triples of people A, B and C such that A knows B, B knows C and A knows C. A usual plan first finds all pairs of friendships A-B and B-C, and then checks A-C. If one person knows everyone, that middle list is huge, even if few triangles exist.

Generic join picks A first, then B, then C. For each choice of A, it lists the people B that A knows, and keeps those who know someone at all. For each A and B, the candidates for C are the friends of B and the friends of A. It walks the shorter of the two lists and checks each name in the other list. Walking the shorter list is what keeps the work small even when some people have huge lists.

## The problem

The input is a join query with hypergraph $H = (V, E)$ (each relation $R_e$ has attribute set $e$), the relations as sets of tuples, and an order $v_1, \ldots, v_k$ of the attributes. The output is the natural join $Q(D) = \{ t : t[e] \in R_e \text{ for each } e \}$, as tuples over $v_1, \ldots, v_k$. This is the [multiway join](/multiway-join/) problem for a full conjunctive query. The cost model is the word RAM with hash tables, or with sorted arrays and binary search; $n$ is the total input size, $r = |E|$, and $\text{AGM}(Q, D) = \min_x \prod_e |R_e|^{x_e}$ over the fractional edge covers $x$ of $H$.

## The algorithm

Each relation is stored as a [trie](/trie/) whose levels follow the global order: the root's children are the values of the first attribute of the relation, and so on. For a prefix $t$ over $v_1, \ldots, v_{i-1}$ and an edge $e \ni v_i$, the node of $R_e$ reached by $t$ restricted to $e$ has as keys the set $R_e[t]$ of values of $v_i$ that agree with $t$.

```pseudo id=main
GENERIC-JOIN(H, R, v_1 .. v_k)               ▷ tries of all R_e are built
L1  S ← a stack holding (1, the empty tuple)
    while S is not empty do
        (i, t) ← POP(S)
L2      if i > k then output t; continue
L3      for each edge e ∋ v_i do C_e ← R_e[t]      ▷ keys of a trie node
L4      e* ← an edge e ∋ v_i with the smallest |C_e|
L5      for each a ∈ C_{e*} do
L6          if a ∈ C_e for every other edge e ∋ v_i then
L7              PUSH(S, (i + 1, t extended by v_i = a))
```

Relations that do not hold $v_i$ play no part at level $i$. The intersection at line L6 is computed in time proportional to the smallest set, by hash lookups or by binary search in the other sets; that is the only rule that matters for the bound.

## Example

The triangle query $R(A, B) \bowtie S(B, C) \bowtie T(A, C)$ with the order $A, B, C$:

- $R = \{(1,1), (1,2), (2,1), (2,3)\}$, $S = \{(1,2), (2,3), (3,1), (1,3)\}$, $T = \{(1,2), (1,3), (2,3), (2,1)\}$.

| level | prefix | candidate sets | loop over | kept |
|---|---|---|---|---|
| $A$ | () | $R$: {1, 2}, $T$: {1, 2} | {1, 2} (2) | 1, 2 |
| $B$ | (1) | $R[1]$: {1, 2}, $S$: {1, 2, 3} | {1, 2} (2) | 1, 2 |
| $B$ | (2) | $R[2]$: {1, 3}, $S$: {1, 2, 3} | {1, 3} (2) | 1, 3 |
| $C$ | (1, 1) | $S[1]$: {2, 3}, $T[1]$: {2, 3} | {2, 3} (2) | 2, 3 |
| $C$ | (1, 2) | $S[2]$: {3}, $T[1]$: {2, 3} | {3} (1) | 3 |
| $C$ | (2, 1) | $S[1]$: {2, 3}, $T[2]$: {1, 3} | {2, 3} (2) | 3 |
| $C$ | (2, 3) | $S[3]$: {1}, $T[2]$: {1, 3} | {1} (1) | 1 |

The output is $(1,1,2), (1,1,3), (1,2,3), (2,1,3), (2,3,1)$. The work per level is 2, 4 and 6. The AGM bound is $\sqrt{4 \cdot 4 \cdot 4} = 8$, and each level stays within it.

**The skewed triangle.** Let each of $R, S, T$ be $\{(0, i), (i, 0) : 1 \le i \le m\}$, so $N = 2m$ and the output is empty. Every pairwise join has $m^2 + m$ tuples. For $m = 200$ ($N = 400$), that is 40,200 intermediate tuples, while generic join loops over 201, 400 and 400 candidates at the three levels, 1,001 in total, against the bound $N^{3/2} = 8000$ per level.

## Correctness

By induction on the level, the tuples pushed with level $i$ are exactly the tuples over $v_1, \ldots, v_i$ whose projection on each edge is in the projection of that relation. A tuple $(t, a)$ has this property if and only if $t$ has it and $a$ lies in $R_e[t]$ for each edge $e \ni v_i$, which is the test of line L6 over the loop of line L5. At level $k$ the property says $t[e] \in R_e$ for each $e$, so the output is the join, and each tuple appears once. The full proof is in the proof file.

## Complexity

Let $W_i = \sum_t \min_{e \ni v_i} |R_e[t]|$ be the number of iterations of line L5 at level $i$, summed over the prefixes $t$ that reach level $i$.

- **Work per level.** For each fractional edge cover $x$, $W_i \le \prod_e |R_e|^{x_e}$. The proof uses a uniform random element of the iterated pairs and the entropy argument of the AGM bound (Shearer's lemma with Gibbs' inequality); Ngo, Ré and Rudra prove the same bound by induction with Hölder's inequality.
- **Time.** Building the tries takes $O(k n)$ expected time with hashing. Each iteration costs $O(r)$ lookups, and each prefix costs $O(r)$ to pick the smallest set. The total is $O(k n + k r \cdot \text{AGM}(Q, D))$ expected with hash tries, and $O((k n + k r \cdot \text{AGM}) \log n)$ worst case with sorted arrays and binary search.
- **Optimality.** Since some instances have output $\Omega(\text{AGM})$ up to a factor $2^{-k}$ (see the AGM bound), no algorithm can be faster in the worst case over all instances with the same relation sizes. This is what *worst-case optimal* means. It says nothing about a given instance: on an instance with small output and small intermediate results, a pairwise plan can be as fast.
- **Space.** $O(k n)$ for the tries, plus the stack, which holds at most $k$ levels of pending candidates at a time in a depth-first order.

For the triangle query with $N$ tuples per relation, the bound is $W_i \le N^{3/2}$, so the time is $O(N^{3/2})$ expected. This matches the classic triangle listing bound $O(m^{3/2})$ for a graph with $m$ edges.

## Properties

- **Any attribute order works for the bound.** The bound holds for each order; the order changes only the constants and the actual work on a given instance.
- **No large intermediate result.** Generic join never materializes the join of two relations; its intermediate state is a set of prefixes, each a projection of a join of projections.
- **Pipelined.** The depth-first version outputs the first tuple before the whole search ends.
- **Not output sensitive.** On an acyclic query whose output is small, it can still take time near the AGM bound, while the [Yannakakis algorithm](/yannakakis-algorithm/) takes time linear in input plus output.

## Variants and improvements

- **NPRR.** The first worst-case optimal algorithm (Ngo, Porat, Ré and Rudra 2012) splits values into heavy and light by the cover weights. Generic join is a simpler algorithm with the same bound.
- **[Leapfrog triejoin](/leapfrog-triejoin/).** The same scheme with sorted tries and a leapfrog intersection by seeks. It is the variant used in LogicBlox and in several graph engines.
- **Hybrid plans.** Real systems use pairwise hash joins for the acyclic parts of a query and generic join for the cyclic cores, or decide per query.
- **Factorized and free-connex output.** When the output itself is large, a factorized representation can be much smaller than the list of tuples.
- **Parallel.** In the [HyperCube (shares) join](/hypercube-shares-join/), each worker runs generic join on its share of the data.

## When to use it

Use generic join for cyclic queries such as triangles, cliques and cycles in graph data, and for queries over skewed data where a pairwise plan can blow up. For acyclic queries with small outputs, pairwise joins with semijoin reduction are as good and simpler. For a two-relation join it is a plain [hash join](/hash-join/) or sort-merge join.

## Pitfalls

- **Intersect by the smallest set.** Looping over a fixed relation's set instead of the smallest one breaks the bound: on the skewed triangle, looping over $S[t]$ at $C$ when $T[t]$ is small brings back $\Theta(N^2)$ work.
- **Tries in the wrong order.** Each trie must list its attributes in the global order. A trie built in another order cannot give $R_e[t]$ by one descent.
- **Counting only the output.** The AGM bound is on the work per level, not only on the output; prefixes that die at a later level are paid for at their own level.
- **Duplicates.** The analysis is for set semantics. Bag relations need counts on the trie leaves.

## Implementations

## History

Atserias, Grohe and Marx (2008) proved the size bound and showed that plans of pairwise joins can be far from it. Ngo, Porat, Ré and Rudra (PODS 2012) gave the first algorithm that runs within the bound for every query. Veldhuizen (ICDT 2014) showed that the leapfrog triejoin of the LogicBlox system is also worst-case optimal. Ngo, Ré and Rudra (2013) described generic join as the common core of these algorithms in their survey "Skew strikes back".

## References
