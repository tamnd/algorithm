---
tag: 38S9XN
kind: algorithm
slug: hypercube-shares-join
name: Hypercube (Shares) join
aliases:
- Shares algorithm
- Afrati-Ullman join
- HyperCube algorithm
area: parallel/mapreduce-and-bsp
level: research
summary: Assign each join variable a share of reducers forming a hypercube, minimizing communication for a multiway join.
solves: [multiway-join]
model: mapreduce-model
complexity:
  vars: {r: the number of tuples in each relation of the triangle query, k: the number of reducers}
  time: {expected: "O(r k^(1/3) + r^(3/2))"}
  space: {extra: "Θ(r k^(1/3))"}
  depth: {expected: "O(r^(3/2) / k)"}
  communication: {worst: "Θ(r k^(1/3))"}
properties: {deterministic: true, in_place: false, online: false}
history:
  year: 2010
  people: [Foto N. Afrati, Jeffrey D. Ullman]
  note: Afrati and Ullman gave the Shares method at EDBT 2010 and in a longer paper in IEEE TKDE in 2011. Beame, Koutris and Suciu later called it HyperCube and proved that it is optimal on inputs without skew.
prereqs: [mapreduce-model, reduce-side-join, multiway-join, lagrange-multiplier, hash-partitioning]
see_also: [reduce-side-join, map-side-join, data-skew, agm-bound, generic-join, triangle-listing-by-degree, mrc-model, mapreduce-communication-lower-bounds]
sources:
  - paper: doi:10.1145/1739041.1739056
    title: Foto N. Afrati and Jeffrey D. Ullman, Optimizing joins in a map-reduce environment, EDBT 2010
    locator: the one-round multiway join with shares, the cost as a sum over relations, the solution by Lagrange multipliers, dominated attributes, and the chain and star joins
  - paper: doi:10.1109/TKDE.2011.47
    title: Foto N. Afrati and Jeffrey D. Ullman, Optimizing multiway joins in a map-reduce environment, IEEE Transactions on Knowledge and Data Engineering 23(9), 2011
    locator: the journal version, with the full treatment of the shares and of the special cases
  - paper: doi:10.1145/2594538.2594558
    title: Paul Beame, Paraschos Koutris and Dan Suciu, Skew in parallel query processing, PODS 2014
    locator: Section 3.1 (the HyperCube algorithm and its load on inputs without skew, Lemma 3.1 and Corollary 3.2) and Theorem 1.1 (HyperCube is optimal on inputs without skew)
  - book: isbn:9781108476348
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, third edition, Cambridge University Press, 2020
    locator: Section 2.5.3, Multiway Joins (the chain of three relations, with shares b and c and the cost s + 2 sqrt(krt))
---

The Shares join, also called the HyperCube algorithm, computes a join of several relations in one MapReduce round. It arranges the $k$ reducers as a grid with one dimension for each attribute of the query. The side of the grid in the direction of attribute $A$ is the *share* $x_A$, and the shares multiply to $k$. Each tuple fixes its position along the attributes it has, by a hash of each value, and is copied to every cell along the attributes it does not have. Then every output tuple finds all its parts at exactly one reducer. Afrati and Ullman (2010) chose the shares to make the communication as small as possible, with [Lagrange multipliers](/lagrange-multiplier/). For the triangle query $R(A, B) \bowtie S(B, C) \bowtie T(C, A)$ with three relations of size $r$, each share is $k^{1/3}$ and the communication is $3 r k^{1/3}$.

## In plain words

Suppose you want to find all groups of three people who all know each other, from a list of pairs of friends, and you have many computers. Arrange the computers in a cube, with one side for each of the three people in a group. A fixed rule gives each person a row number on each side. A pair of friends fixes two of the three positions in the cube, so it goes to the whole line of computers along the third side. Every group of three then meets in exactly one computer. A cube of 1,000 computers has sides of 10, so each pair goes to 10 computers. A cube that is long in one direction would copy some pairs many more times, so the even cube is the cheapest.

## The problem

The input is a natural join query $Q = R_1 \bowtie \cdots \bowtie R_n$ over attributes $A_1, \ldots, A_m$, the relations themselves, and a number $k$ of reducers. The output is the bag $Q$. This is the [multiway join](/multiway-join/) problem in the [MapReduce model](/mapreduce-model/), with one round. The costs are the communication, that is the number of tuples sent to reducers, and the largest reducer input. A cascade of two-way joins needs several rounds and can have intermediate results far larger than the input and the output. The Shares join does one round and never builds an intermediate result.

## The algorithm

Choose positive integer shares $x_1, \ldots, x_m$ with $x_1 x_2 \cdots x_m = k$ and a hash function $h_j$ from values of $A_j$ to $\{0, \ldots, x_j - 1\}$ for each attribute. The reducers are the cells $(c_1, \ldots, c_m)$ with $0 \le c_j < x_j$.

```pseudo id=main
SHARES-JOIN(Q, x)                          ▷ Q has attributes A_1, ..., A_m; x_1 x_2 ⋯ x_m = k
L1  for each relation R_i of Q, in parallel do              ▷ map
L2      for each tuple t of R_i do
L3          for each cell c with c_j = h_j(t.A_j) for every A_j of R_i, and any c_j for every other A_j do
L4              emit (c, (R_i, t))
L5  for each cell c, at its own reducer, in parallel do     ▷ reduce
L6      join the tuples that c received, on one machine, and output the result
```

In the program, the cell $(c_1, \ldots, c_m)$ is reducer number $c_1 x_2 \cdots x_m + c_2 x_3 \cdots x_m + \cdots + c_m$, and each $h_j$ is a CRC-32 of the attribute name and the value, modulo $x_j$. Line L6 can use any one-machine join. A [worst-case optimal join](/generic-join/) is a good choice for cyclic queries.

**Choosing the shares.** A tuple of $R_i$ is copied to $\prod_{A_j \notin R_i} x_j$ cells. So the communication is

$$f(x) = \sum_{i=1}^{n} |R_i| \prod_{A_j \notin R_i} x_j, \qquad \text{to be minimized subject to } \prod_{j} x_j = k.$$

Treat the shares as real numbers. If every relation that contains $A_j$ also contains $A_l$, then $A_j$ is *dominated*, and its share can be set to 1 at no cost. At a minimum, for each attribute with share above 1, the terms of the relations that do not contain it add up to the same value $\lambda k$. Solve these equations, then round the shares to integers whose product is at most $k$.

**The triangle.** For $R(A, B) \bowtie S(B, C) \bowtie T(C, A)$ with sizes $r$, $s$ and $t$, each attribute is missing from exactly one relation, so the cost is $r x_C + s x_A + t x_B$. The condition says that the three terms are equal, so $s x_A = t x_B = r x_C = (rstk)^{1/3}$, and the cost is $3(rstk)^{1/3}$. For $r = s = t$, every share is $k^{1/3}$ and the cost is $3 r k^{1/3}$.

**The chain.** For $R(A, B) \bowtie S(B, C) \bowtie T(C, D)$, $A$ and $D$ are dominated, so $x_A = x_D = 1$. Then $x_B = \sqrt{kr/t}$, $x_C = \sqrt{kt/r}$, and the cost is $s + 2\sqrt{krt}$. The middle relation is not copied at all.

## Example

**A small triangle.** Let $R = S = T = \{(1, 2), (2, 3), (3, 1)\}$, the edges of a directed cycle, with $k = 8$ and shares $x_A = x_B = x_C = 2$. For this example take $h(v) = v \bmod 2$ for all three attributes, so $h(1) = 1$, $h(2) = 0$ and $h(3) = 1$. The tuple $(1, 2)$ of $R$ fixes $c_A = 1$ and $c_B = 0$, and goes to cells $(1, 0, 0)$ and $(1, 0, 1)$. Each of the 9 tuples goes to 2 cells, so 18 tuples are sent, which is $3 \cdot 3 \cdot 2$.

| output $(a, b, c)$ | its cell | the parts that meet there |
|---|---|---|
| (1, 2, 3) | (1, 0, 1) | $R(1, 2)$, $S(2, 3)$, $T(3, 1)$ |
| (2, 3, 1) | (0, 1, 1) | $R(2, 3)$, $S(3, 1)$, $T(1, 2)$ |
| (3, 1, 2) | (1, 1, 0) | $R(3, 1)$, $S(1, 2)$, $T(2, 3)$ |

Cell $(1, 1, 1)$ also gets one tuple of each relation, $R(3, 1)$, $S(3, 1)$ and $T(3, 1)$, but they do not join, so it outputs nothing.

**A large triangle.** With $r = s = t = 10^6$ and $k = 1000$, the shares are 10, each tuple goes to 10 reducers, and the communication is $3 \cdot 10^6 \cdot 10 = 3 \cdot 10^7$ tuples. The average reducer input is $3r / k^{2/3} = 30{,}000$. Hashing only on $A$, with shares $(1000, 1, 1)$, would copy all of $S$ to every reducer, for $2 \cdot 10^6 + 10^9$ tuples.

**A random graph.** Take 3,000 distinct directed edges on 300 vertices, chosen at random with a fixed seed, as $R$, $S$ and $T$, and $k = 27$ with shares 3. The Shares join sends exactly $3 \cdot 3{,}000 \cdot 3 = 27{,}000$ tuples, an average of 1,000 for each reducer, and the reducer inputs go from 805 to 1,277. The output has 982 tuples. A cascade of two reduce-side joins first shuffles 6,000 tuples and makes the 29,912 paths of length two, then shuffles these with $T$, which is 32,912 more. That is 38,912 tuples in two rounds.

## Correctness

Let $u$ be an output tuple and $\text{cell}(u) = (h_1(u.A_1), \ldots, h_m(u.A_m))$. For each relation $R_i$, the tuple $u|_{R_i}$ fixes the coordinates of the attributes of $R_i$ to exactly the values in $\text{cell}(u)$, so line L3 sends it there, once. So the reducer of $\text{cell}(u)$ has every part of $u$ and outputs $u$ with the right multiplicity. No other cell can output $u$: every attribute occurs in some relation, and a tuple of that relation at cell $c$ forces the coordinate of $c$ for that attribute to the hash of its value. The formula for $f$ counts the cells listed by line L3. The optimal shares of the triangle follow from the inequality of the arithmetic and geometric means, $r x_C + s x_A + t x_B \ge 3(rst \, x_A x_B x_C)^{1/3}$, with equality when the three terms are equal. The full proof is below.

## Complexity

For the triangle with $r = s = t$ and shares $k^{1/3}$:

- **Rounds.** One.
- **Communication.** Exactly $3 r k^{1/3}$ tuples. The replication rate, the number of copies of each input tuple, is $k^{1/3}$.
- **Reducer input.** $3 r / k^{2/3}$ on average. Beame, Koutris and Suciu prove (Section 3.1) that on inputs with no heavy values, the largest reducer input is $O(r / k^{2/3})$ with high probability, up to a logarithmic factor. They also show that no one-round algorithm has a smaller load on such inputs, up to that factor.
- **Local work.** A reducer with input $L$ lists its triangles in $O(L^{3/2})$ time with a worst-case optimal join, because a triangle query with relations of size $L$ has at most $L^{3/2}$ answers by the [AGM bound](/agm-bound/). With $L = O(r/k^{2/3})$, the time of the reduce phase is $O(r^{3/2}/k)$, and the total over the $k$ reducers is $O(r^{3/2})$, the same as on one machine.

For a general query, the communication is $f(x)$ above, and the average reducer input is $f(x)/k$. Beame, Koutris and Suciu show that, with the best shares, the load on inputs with no heavy values is about $r / k^{1/\tau^*}$, where $\tau^*$ is the fractional edge packing number of the [hypergraph](/hypergraph/) of the query. For the triangle, $\tau^* = 3/2$.

## Properties

- **One round.** Any natural join, cyclic or not, is computed in one round, with no intermediate results.
- **Communication grows with $k$.** Unlike a two-way join, the total communication grows as $k^{1/3}$ for the triangle. More reducers mean less input for each, but more copies in total. This trade-off is the subject of the [communication lower bounds](/mapreduce-communication-lower-bounds/) for MapReduce.
- **Two-way joins as a special case.** For $R(A, B) \bowtie S(B, C)$, $A$ and $C$ are dominated, so the optimum puts all $k$ on $B$, which is the [reduce-side join](/reduce-side-join/). With shares on $A$ and $C$ only, it is a grid in which each tuple of $R$ is copied along $C$ and each tuple of $S$ along $A$.
- **Sensitive to skew.** A value that occurs $d$ times in a relation puts at least about $d / x$ tuples on one cell, where $x$ is the share of another attribute of that relation.
- **Deterministic.** For fixed hash functions, the cells and the loads depend only on the input.

## Variants and improvements

- **Integer shares.** The real optimum must be rounded. Afrati and Ullman discuss the rounding. When $k$ is not a cube, the best integer shares for the triangle can be found by trying all ways to write a number at most $k$ as a product of three integers.
- **Skew-aware HyperCube.** Beame, Koutris and Suciu (2014) find the heavy values first, then run a separate HyperCube with its own shares for each group of heavy values, on its own set of reducers. Their algorithm for two-way joins is described on the [data skew](/data-skew/) page.
- **Several rounds.** The one-round load bound $r / k^{1/\tau^*}$ can be beaten with more rounds. For acyclic queries, a plan in the style of the [Yannakakis algorithm](/yannakakis-algorithm/) uses several rounds of two-way joins and semijoins.
- **Triangle listing by degree.** Suri and Vassilvitskii (2011) gave a MapReduce triangle counting method that colors the vertices into a small number of groups and sends each edge to the triples of groups it can belong to. It is the same grid idea. See [triangle counting](/triangle-counting/) and [triangle listing by degree](/triangle-listing-by-degree/).

## When to use it

Use the Shares join for a multiway join whose two-way intermediate results would be much larger than the input or the output, which is the case for cyclic queries such as triangles and cycles, and for joins on several attributes. Use it when a single round matters more than the lowest communication. For a two-way join, it reduces to the [reduce-side join](/reduce-side-join/). For a join of a large relation with small ones, a [map-side join](/map-side-join/) is cheaper. When some values are very frequent, use a skew-aware version.

## Pitfalls

- **Forgetting dominated attributes.** An attribute that occurs only in one relation, or only in relations that contain another attribute, should get share 1. A share above 1 on it only adds copies.
- **Rounding badly.** Rounding each real share up can give a product far above $k$. Round so that the product stays at most $k$, or search the integer shares directly.
- **A hash that differs between map tasks.** Every map task must give the same coordinate to the same value of an attribute. Otherwise the parts of an output tuple go to different cells, and the tuple is lost with no error. The built-in string hash of some languages, Python among them, changes from process to process.
- **Counting each triangle several times.** With $R = S = T$ as a directed edge list, each directed 3-cycle appears three times in the output, once for each rotation. Fix an order on the vertices if each triangle should appear once.
- **Trusting the average load.** The communication formula gives the average. A heavy value can make one reducer much slower than the average.

## Implementations

## History

Afrati and Ullman introduced the Shares method at EDBT 2010 and gave the full version in IEEE Transactions on Knowledge and Data Engineering in 2011. They set the cost of a one-round join as a sum over the relations, found the shares with Lagrange multipliers, and treated chain joins, star joins and dominated attributes. Beame, Koutris and Suciu (2013) studied the method in the massively parallel communication model under the name HyperCube. In 2014, Beame, Koutris and Suciu proved that HyperCube is optimal for one round on inputs without skew, and gave skew-aware versions. The method also appears in Section 2.5.3 of the textbook by Leskovec, Rajaraman and Ullman.

## References
