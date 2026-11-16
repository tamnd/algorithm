---
tag: ZT8VGE
kind: theorem
slug: apsp-negative-triangle-equivalence
name: APSP and negative triangle equivalence
aliases:
- Vassilevska Williams-Williams reduction
area: complexity/fine-grained-complexity
level: advanced
summary: "Vassilevska Williams and Williams (2010): APSP, the min-plus product and negative triangle detection are subcubic equivalent. A truly subcubic algorithm for one gives one for all."
prereqs: [apsp-conjecture, negative-triangle, fine-grained-reduction]
see_also: [fine-grained-equivalence-class, min-plus-matrix-multiplication, apsp-repeated-squaring, all-pairs-shortest-paths, conditional-lower-bound, combinatorial-bmm-conjecture, zero-k-clique-hypothesis, floyd-warshall]
sources:
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010, 645-654)"
    locator: the introduction (the list of subcubic equivalent problems), the definition of subcubic reductions, and the reductions from the min-plus product to all-pairs negative triangle and from all-pairs negative triangle to negative triangle detection; this page relies on the journal version
  - paper: "Liam Roditty and Virginia Vassilevska Williams, Minimum weight cycles and triangles: equivalences and algorithms, Proceedings of the 52nd IEEE Symposium on Foundations of Computer Science (FOCS 2011), 180-189"
    locator: the subcubic equivalence of minimum weight cycle with APSP
  - paper: "Amir Abboud, Fabrizio Grandoni and Virginia Vassilevska Williams, Subcubic equivalences between graph centrality problems, APSP and diameter, Proceedings of the 26th ACM-SIAM Symposium on Discrete Algorithms (SODA 2015), 1681-1697"
    locator: the subcubic equivalence of radius, median and betweenness centrality with APSP
  - paper: doi:10.1006/jcss.1997.1388
    title: "Noga Alon, Zvi Galil and Oded Margalit, On the exponent of the all pairs shortest path problem, Journal of Computer and System Sciences 54(2), 1997, 255-262"
    locator: the computation of the distance product of matrices with small integer entries by fast matrix multiplication
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: Theorem 2 (the min-plus product and APSP in deterministic time O(n^2.9995)), Theorem 21(b) (the reduction from exact triangle with the same n^2 T(n^(1/3)) shape) and the list of problems in the APSP class in Section 1.2; not yet refereed
---

The theorem says that three cubic problems stand or fall together: [all-pairs shortest paths](/all-pairs-shortest-paths/) (APSP), the [min-plus product](/min-plus-matrix-multiplication/) of two matrices, and the detection of a [negative triangle](/negative-triangle/). If one of them has an algorithm with time $O(n^{3-\varepsilon})$ for some $\varepsilon > 0$, then all three have one. Vassilevska Williams and Williams proved it at FOCS 2010, in the paper that started the study of subcubic equivalences. The hard direction turns a yes or no answer for a whole graph into all $n^2$ entries of a matrix product, and it loses only a factor 3 in the saving of the exponent.

So the [APSP conjecture](/apsp-conjecture/) can be stated as a conjecture about one triangle. This page gives the full proof of the equivalence. The list of other problems in the class is on [fine-grained equivalence class](/fine-grained-equivalence-class/).

## Statement

The model is the [word RAM](/word-ram/) with words of $O(\log n)$ bits. Weights are integers in $\{-M, \ldots, M\}$ with $M \le n^{c}$ for a constant $c$, so that each weight and each sum of $O(n)$ weights fits in $O(1)$ words. A missing edge or entry has the value $\infty$.

- **APSP:** given a directed graph on $n$ vertices with no negative cycle, compute the distance between every ordered pair of vertices.
- **Min-plus product:** given $n \times n$ matrices $A$ and $B$, compute $C[i,k] = \min_j (A[i,j] + B[j,k])$.
- **Negative triangle:** given a graph on $n$ vertices, decide whether three distinct vertices $i, j, k$ have $w(i,j) + w(j,k) + w(k,i) < 0$.

Let $T(n)$ be the time of an algorithm for negative triangle on tripartite graphs with $n$ vertices in each part, and let $T$ be non-decreasing with $T(2n) = O(T(n))$, as for every polynomial bound.

**Theorem (Vassilevska Williams and Williams 2010).** All reductions below are deterministic.

1. The min-plus product of $n \times n$ matrices with entries in $\{-M, \ldots, M\}$ can be computed in time $O(n^2\, T(n^{1/3}) \log n \log M)$.
2. APSP on $n$ vertices with weights in $\{-M, \ldots, M\}$ can be solved in time $O(n^2\, T(n^{1/3}) \log^2 n \log(nM))$.
3. If APSP on $n$ vertices has an algorithm with time $S(n)$, then the min-plus product and negative triangle have algorithms with time $O(S(3n) + n^2)$.

**Corollary.** For weights bounded by a polynomial in $n$, the following are equivalent: APSP has a truly subcubic algorithm; the min-plus product has one; negative triangle has one. In numbers, an $O(n^{3-\varepsilon})$ algorithm for negative triangle gives $O(n^{3-\varepsilon/3} \log^3 n)$ for APSP, and an $O(n^{3-\varepsilon})$ algorithm for APSP gives $O(n^{3-\varepsilon})$ for negative triangle.

The theorem and the corollary are **unconditional**. Read with the APSP conjecture, they say that negative triangle has no $O(n^{3-\varepsilon})$ algorithm, **conditional on the APSP conjecture**. In the language of [fine-grained reductions](/fine-grained-reduction/), each direction is an $(n^3, n^3)$-reduction.

## In plain words

You have a road map with signed costs and want the cheapest trip between every pair of towns. The question looks huge: one answer for each pair. Now take a tiny question: is there a round trip through three towns with a total cost below zero? It has a single yes or no answer.

The theorem says that the tiny question is just as hard as the huge one. If you can answer it fast, you can also find all the cheapest trips fast.

The trick has two parts. First, a yes or no helper can point to one bad round trip, by cutting the map into halves and asking again. Second, you cut the map into many small pieces, ask about each small piece, and remove each road that you have already explained. Each answer is cheap, and there are not too many answers.

## Proof

### Tripartite instances

All reductions work with a tripartite graph: three disjoint parts $I$, $J$ and $K$, with edges only between different parts. It is given by three matrices: $A[i,j]$ is the weight of the edge $\{i, j\}$ with $i \in I$, $j \in J$; $B[j,k]$ the weight of $\{j, k\}$ with $k \in K$; and $D[i,k]$ the weight of $\{k, i\}$. The weight of the triangle $(i, j, k)$ is $A[i,j] + B[j,k] + D[i,k]$, and it is $\infty$ if an edge is missing. For index sets $I' \subseteq I$, $J' \subseteq J$, $K' \subseteq K$, write $G[I', J', K']$ for the subgraph on them. A detector answers yes or no for one subgraph.

A general graph becomes tripartite with no change in the answer. For a directed graph with weights $W$ and no self-loops, take three copies of the vertex set and set $A = B = W$ and $D[i,k] = W[k,i]$. A triangle $(i, j, k)$ of the copy has weight $W[i,j] + W[j,k] + W[k,i]$, so it is a directed cycle $i \to j \to k \to i$ in the graph. Its three vertices are distinct, because $W$ has no self-loops. An undirected graph is a directed graph with both directions of each edge. The copy has $n$ vertices in each part, so a detector for tripartite graphs with time $T(n)$ decides the general problem in time $T(n) + O(n^2)$.

### APSP and the min-plus product

*APSP to the min-plus product.* Let $D_1$ be the weight matrix with zeros on the diagonal. The min-plus power $D_1^{\ell}$ holds the least weight of a path with at most $\ell$ edges. With no negative cycle, a shortest path has at most $n - 1$ edges, so $D_1^{\ell}$ for any $\ell \ge n - 1$ is the distance matrix. Repeated squaring reaches it with $\lceil \log_2 (n-1) \rceil$ products, each with entries of absolute value at most $(n-1) M$ ([APSP by repeated squaring](/apsp-repeated-squaring/)).

*The min-plus product to APSP.* Build a directed graph with layers $I$, $J$ and $K$ of $n$ vertices each, an edge $i \to j$ of weight $A[i,j]$ and an edge $j \to k$ of weight $B[j,k]$. It has no cycle at all, so negative weights are allowed. Every path from $i$ to $k$ has the form $i \to j \to k$, so the distance from $i$ to $k$ is $C[i,k]$. This is one call on $3n$ vertices.

### Negative triangle to the min-plus product

Compute $C = A \star B$, the min-plus product, and answer yes if $C[i,k] + D[i,k] < 0$ for some $i$ and $k$. This is correct because $C[i,k] + D[i,k] = \min_j (A[i,j] + B[j,k] + D[i,k])$ is the least weight of a triangle through $i$ and $k$. It is one product and $O(n^2)$ more work. With the reduction above, an APSP algorithm with time $S(n)$ decides negative triangle on a tripartite graph with $n$ vertices per part in time $O(S(3n) + n^2)$. A general graph on $n$ vertices goes through the tripartite copy, which has $n$ vertices per part, so the same bound holds. This proves part 3.

### The pseudocode of the hard direction

The hard direction has three routines. FIND turns a detector into a search. ALL-PAIRS-NT reports every pair $(i, k)$ whose edge lies on a negative triangle. MIN-PLUS-VIA-NT runs a binary search for all $n^2$ entries of the product at the same time.

```pseudo id=main
MIN-PLUS-VIA-NT(A, B, DETECT)       ▷ entries in {-M, ..., M} or ∞
L1  for each (i, k): lo[i,k] ← -2M;  hi[i,k] ← 2M + 1        ▷ 2M + 1 stands for ∞
L2  while lo[i,k] < hi[i,k] for some (i, k) do
L3      for each (i, k): mid[i,k] ← ⌊(lo[i,k] + hi[i,k]) / 2⌋;  D[i,k] ← -(mid[i,k] + 1)
L4      Y ← ALL-PAIRS-NT(A, B, D, DETECT)
L5      for each (i, k) with lo[i,k] < hi[i,k]: if (i, k) ∈ Y then hi[i,k] ← mid[i,k] else lo[i,k] ← mid[i,k] + 1
L6  return lo                           ▷ the value 2M + 1 means ∞

ALL-PAIRS-NT(A, B, D, DETECT)        ▷ n is the largest part size
L7  s ← ⌈n^(1/3)⌉;  cut I, J and K into groups of at most s vertices
L8  Y ← ∅;  work on a copy of D
L9  for each triple of groups (I_a, J_b, K_c) do
L10     while DETECT(G[I_a, J_b, K_c]) do
L11         (i, j, k) ← FIND(G[I_a, J_b, K_c], DETECT)
L12         Y ← Y ∪ {(i, k)};  D[i,k] ← ∞            ▷ delete the edge {k, i}
L13 return Y

FIND(H, DETECT)                       ▷ H has a negative triangle
L14 while some part of H has two or more vertices do
L15     cut each such part into two halves; this gives at most 8 subgraphs
L16     H ← the first of these subgraphs on which DETECT answers yes
L17 return the vertices of H, one in each part
```

### Lemma 1: a detector finds a triangle

**Lemma 1.** If $H$ has a negative triangle and its largest part has $s$ vertices, then FIND returns a negative triangle of $H$ after at most $8 \lceil \log_2 s \rceil$ calls to DETECT.

*Proof.* The invariant is that $H$ has a negative triangle. It holds at the start. In a round, let $(i, j, k)$ be a negative triangle of $H$. Line L15 puts $i$ in one half of its part, and the same for $j$ and $k$, so one of the at most 8 subgraphs contains all three vertices and with them the triangle. So DETECT answers yes on at least one subgraph, and line L16 keeps one on which it answers yes. A part of size $m$ becomes a part of size at most $\lceil m/2 \rceil$, so after $\lceil \log_2 s \rceil$ rounds every part has one vertex. Then $H$ is one triangle, and by the invariant it is negative. Each round makes at most 8 calls. $\square$

### Lemma 2: all pairs from a detector

**Lemma 2.** ALL-PAIRS-NT returns exactly the pairs $(i, k)$ such that some $j$ has $A[i,j] + B[j,k] + D[i,k] < 0$ for the input $D$. It calls DETECT at most $g^3 + n^2 (1 + 8 \lceil \log_2 s \rceil)$ times, where $g = \lceil n/s \rceil$, and each call is on a subgraph with at most $s$ vertices per part.

*Proof.* Only line L12 changes $D$, and it only deletes $I$-$K$ edges; the matrices $A$ and $B$ never change.

- *Every reported pair is correct.* Line L12 adds $(i, k)$ only after FIND returned the negative triangle $(i, j, k)$ of the current graph. The current graph is a subgraph of the input with the same weights, so $(i, j, k)$ is a negative triangle of the input.
- *Every correct pair is reported.* Let $(i, j, k)$ be a negative triangle of the input, and let $I_a$, $J_b$ and $K_c$ be the groups of $i$, $j$ and $k$. The loop at line L10 for this triple ends only when DETECT answers no, that is, when $G[I_a, J_b, K_c]$ has no negative triangle. The edges $\{i, j\}$ and $\{j, k\}$ are never deleted, so at that time the edge $\{k, i\}$ must be gone. Only line L12 deletes it, and line L12 adds $(i, k)$ to $Y$ at the same time.
- *The count.* Each call at line L10 either answers no, which ends the loop for one triple, or answers yes, which leads to one deletion. There are $g^3$ triples. Each deletion removes an edge that FIND found in the current graph, so it removes a different edge each time, and there are at most $n^2$ of them. Each deletion also costs one call to FIND, which makes at most $8 \lceil \log_2 s \rceil$ calls by Lemma 1. $\square$

With $s = \lceil n^{1/3} \rceil$, $g^3 = O(n^2)$, so ALL-PAIRS-NT makes $O(n^2 \log n)$ calls, each on a graph with at most $s$ vertices per part. Each call costs at most $T(s) = O(T(n^{1/3}))$, and the work outside the calls is $O(n^2 \log n)$. So ALL-PAIRS-NT runs in time $O(n^2\, T(n^{1/3}) \log n)$.

### Lemma 3: the product by binary search

**Lemma 3.** MIN-PLUS-VIA-NT returns the min-plus product $C = A \star B$ after $\lceil \log_2 (4M + 2) \rceil$ calls to ALL-PAIRS-NT, on instances with weights in $\{-(2M+1), \ldots, 2M + 1\}$.

*Proof.* Let $C^{*}[i,k] = \min(C[i,k], 2M + 1)$. A finite entry of $C$ is a sum of two entries in $\{-M, \ldots, M\}$, so $C^{*}[i,k] = C[i,k]$ when $C[i,k]$ is finite, and $C^{*}[i,k] = 2M + 1$ when it is $\infty$. The invariant is $lo[i,k] \le C^{*}[i,k] \le hi[i,k]$. It holds after line L1.

Take a round and a pair with $lo[i,k] < hi[i,k]$. Then $mid[i,k] < hi[i,k] \le 2M + 1$. The triangle $(i, j, k)$ has weight $A[i,j] + B[j,k] - mid[i,k] - 1$, which is negative if and only if $A[i,j] + B[j,k] \le mid[i,k]$. So by Lemma 2, $(i, k) \in Y$ if and only if $C[i,k] \le mid[i,k]$, which is the same as $C^{*}[i,k] \le mid[i,k]$ because $mid[i,k] \le 2M$. Line L5 sets $hi$ to $mid$ in the first case and $lo$ to $mid + 1$ in the second, so the invariant holds. The interval $hi - lo + 1$ starts at $4M + 2$ and at least halves, rounded up, in each round; pairs with $lo = hi$ do not change. So after $\lceil \log_2 (4M + 2) \rceil$ rounds every interval has one value, and it is $C^{*}[i,k]$. Line L6 reads $2M + 1$ as $\infty$. $\square$

### Putting the parts together

By Lemmas 2 and 3, the min-plus product costs $O(\log M)$ calls to ALL-PAIRS-NT, which gives part 1: $O(n^2\, T(n^{1/3}) \log n \log M)$, plus $O(n^2 \log M)$ for the bookkeeping. For part 2, APSP needs $\lceil \log_2 (n-1) \rceil$ products with entries bounded by $nM$, so it costs $O(n^2\, T(n^{1/3}) \log^2 n \log(nM))$.

For the corollary, let $T(n) = O(n^{3-\varepsilon})$. Then $n^2\, T(n^{1/3}) = O(n^{2 + (3 - \varepsilon)/3}) = O(n^{3 - \varepsilon/3})$. With $M \le n^{c}$, $\log(nM) = O(\log n)$, so APSP takes $O(n^{3 - \varepsilon/3} \log^3 n)$, which is $O(n^{3 - \varepsilon/4})$. The other direction is part 3. $\blacksquare$

### A worked example

**A negative triangle through the product.** Take the directed graph on the vertices $0, 1, 2, 3$ with the edges $0 \to 1$ of weight 2, $0 \to 2$ of weight 4, $1 \to 2$ of weight $-3$, $1 \to 3$ of weight 1, $2 \to 0$ of weight $-1$, $2 \to 3$ of weight 2 and $3 \to 0$ of weight $-2$. Its directed triangles are $0 \to 1 \to 2 \to 0$ with weight $-2$, $0 \to 1 \to 3 \to 0$ with weight 1, and $0 \to 2 \to 3 \to 0$ with weight 4. In the tripartite copy, the product entry is $C[0,2] = W[0,1] + W[1,2] = -1$, and $C[0,2] + W[2,0] = -2 < 0$, so the answer is yes. ALL-PAIRS-NT on the copy reports the pairs $(0, 2)$, $(1, 0)$ and $(2, 1)$: the three rotations of the one negative cycle, each named by its first and last vertex.

**The product by binary search.** Take

$$A = \begin{pmatrix} 3 & -2 & 0 \\ 1 & 4 & -5 \\ -1 & 2 & 2 \end{pmatrix}, \qquad B = \begin{pmatrix} 0 & 5 & -3 \\ 2 & -4 & 1 \\ 4 & 0 & 3 \end{pmatrix}.$$

Here $M = 5$, so every interval starts as $[-10, 11]$ and the search takes $\lceil \log_2 22 \rceil = 5$ rounds. For the entry $(1, 1)$, the rounds test $mid = 0$ (yes), $-5$ (yes), $-8$ (no) and $-6$ (no), and stop at $C[1,1] = -5$, which is $A[1,2] + B[2,1] = -5 + 0$. The run returns

$$C = \begin{pmatrix} 0 & -6 & -1 \\ -1 & -5 & -2 \\ -1 & -2 & -4 \end{pmatrix},$$

the min-plus product, after 143 calls to a brute-force detector. Most entries need 4 rounds; the entries $(0, 1)$ and $(2, 2)$ need all 5.

**The count of calls.** On a tripartite graph with 27 vertices per part and random weights in $\{-10, \ldots, 10\}$ (seed 20261116), $s = 3$ and there are $9^3 = 729$ triples. Every one of the 729 pairs lies on a negative triangle, and ALL-PAIRS-NT made 6,983 calls to the detector, below the bound $729 + 729 \cdot 17 = 13{,}122$ of Lemma 2.

### Implementation and tests

The Python file implements FIND, ALL-PAIRS-NT, MIN-PLUS-VIA-NT, the two reductions between APSP and the min-plus product, the reduction from negative triangle to the min-plus product, and the tripartite copy of a directed graph. The detector is a parameter. The tests use a brute-force detector that counts its calls, with seeds from 20261116. They check FIND on 300 random tripartite graphs with up to 7 vertices per part, ALL-PAIRS-NT against brute force on 250 graphs with up to 9 vertices per part and missing edges, the call bound of Lemma 2 for 8, 27 and 30 vertices per part, the product against brute force on 80 pairs of matrices with $\infty$ entries, APSP through the detector against Floyd-Warshall on 40 graphs with negative edges and no negative cycle, and the examples above.

## Consequences

- **One triangle carries the APSP conjecture.** Conditional on the APSP conjecture, negative triangle has no $O(n^{3-\varepsilon})$ algorithm. Negative triangle is the usual start of a new reduction, because it is a decision problem with a small witness.
- **More members of the class.** The same paper adds the verification of a min-plus product, deciding whether a matrix is a metric, replacement paths and the second shortest simple path. Roditty and Vassilevska Williams (FOCS 2011) added minimum weight cycle. Abboud, Grandoni and Vassilevska Williams (SODA 2015) added radius, median and betweenness centrality. See [fine-grained equivalence class](/fine-grained-equivalence-class/).
- **The Boolean form.** The same method shows that, for combinatorial algorithms, Boolean matrix multiplication and triangle detection are subcubic equivalent. See the [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/).
- **A template for new reductions.** The steps "detect, then find by halving, then list with deletions on small groups" work for other triangle problems. Alman and Vassilevska Williams (arXiv:2610.06783) use a reduction of the same shape, with time $n^2\, T(n^{1/3})$, from exact triangle to the min-plus product and APSP (their Theorem 21(b)).

### Status in 2026

In October 2026, Alman and Vassilevska Williams posted a preprint with deterministic algorithms for the min-plus product and for APSP with weights bounded by a polynomial in $n$, in time $O(n^{2.9995})$. The paper is not yet refereed. If it is correct, the APSP conjecture is false, and by the reduction to the min-plus product, negative triangle has a deterministic $O(n^{2.9995})$ algorithm too.

The theorem on this page does not change. It is a pair of reductions, and both still hold. It now says that every member of the class is truly subcubic, instead of saying that a fast algorithm for one would be surprising. The exponents also follow the factor 3 of the proof: an exact triangle algorithm with saving $0.0017$ in the exponent gives a saving of about $0.0017/3 \approx 0.00057$ for APSP.

## Tightness

- **The loss of a factor 3.** The reduction from the product to negative triangle turns a saving $\varepsilon$ into $\varepsilon/3$. The other direction keeps $\varepsilon$. So the class is equivalent for "truly subcubic", but the proof does not say that all members have the same exponent.
- **The range of weights matters.** The binary search costs $O(\log M)$ rounds, so the reduction is subcubic only for $\log M = n^{o(1)}$; the usual form takes $M \le n^{c}$. For small weights the problems are easier: the min-plus product with entries in $\{-M, \ldots, M\}$ has an $\tilde{O}(M n^{\omega})$ algorithm by fast matrix multiplication of polynomials in one variable (Alon, Galil and Margalit 1997), so the hard instances have large weights.
- **The group size is the best choice.** With groups of size $s$, the count is $O((n^2 + (n/s)^3) \log s)$ calls of cost $T(s)$. Groups smaller than $n^{1/3}$ make $(n/s)^3$ larger than $n^2$; larger groups make each call more expensive. For $T(s) = s^{3-\varepsilon}$, $s = n^{1/3}$ balances the two terms.
- **Dense graphs only.** The theorem is about $n$-vertex graphs with $\Theta(n^2)$ possible edges. It says nothing about sparse graphs with $m$ edges, where minimum weight cycle and related problems have their own hypotheses.

## History

The equivalence of APSP and the min-plus product, by repeated squaring and a layered graph, is older than the theorem. Vassilevska Williams and Williams presented the reduction to negative triangle at FOCS 2010 under the title "Subcubic equivalences between path, matrix, and triangle problems", and the journal version appeared in the Journal of the ACM in 2018. They defined subcubic reductions, the form of fine-grained reduction for cubic problems, and proved that a long list of path, matrix and triangle problems are equivalent under them. The paper also gave the combinatorial equivalence of Boolean matrix multiplication and triangle detection. Roditty and Vassilevska Williams (2011) and Abboud, Grandoni and Vassilevska Williams (2015) extended the class. The same scheme, with exact triangle in place of negative triangle, is the last step of the 2026 preprint of Alman and Vassilevska Williams.

## References
