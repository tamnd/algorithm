---
tag: X8DF57
kind: algorithm
slug: k-degree-anonymization
name: k-degree anonymization
aliases:
- Liu-Terzi algorithm
area: security-and-privacy/data-anonymization
level: advanced
summary: Makes each degree of a graph shared by at least k vertices; a dynamic program finds the cheapest such degree sequence, then edges are added to realize it.
model: word-ram
complexity:
  vars: {n: the number of vertices, k: the anonymity parameter, r: the largest number of edges a vertex must gain}
  time: {worst: O(n log n + n k + n r)}
  space: {extra: O(n)}
properties: {deterministic: true, randomized: false}
history:
  year: 2008
  people: [Kun Liu, Evimaria Terzi]
  note: Liu and Terzi defined k-degree anonymous graphs at SIGMOD 2008 and split the problem into a dynamic program on the degree sequence and a graph construction step.
prereqs: [k-anonymity, degree, handshake-lemma]
see_also: [active-attack-on-social-graphs, social-network-deanonymization, k-anonymity, degree-distribution, simple-graph, principle-of-optimality, differential-privacy-definition, linkage-attack]
sources:
  - paper: doi:10.1145/1376616.1376629
    title: "Kun Liu and Evimaria Terzi, Towards identity anonymization on graphs, ACM SIGMOD 2008, pages 93-106"
    locator: Section 2 (Definitions 1 and 2, Proposition 1, Problem 1 and Equation 1), Section 4 (Observation 1, the DP Recursions 2 to 4, Theorem 1 and the Greedy algorithm), Section 5.1 (Lemma 1 and Algorithm 1, ConstructGraph), Section 5.2 (Definition 4, Lemma 2 and Supergraph), Section 5.3 (Algorithm 2, Probing), Section 6 (Greedy_Swap and Priority for the relaxed problem), Section 7 (the experiments) and Section 8 (additions and deletions together)
  - paper: doi:10.14778/1453856.1453873
    title: "Michael Hay, Gerome Miklau, David Jensen, Don Towsley and Philip Weis, Resisting structural re-identification in anonymized social networks, PVLDB 1(1), 2008, pages 102-114"
    locator: the degree-based and other structural knowledge of an attacker, and the defense that groups vertices into supernodes
  - paper: doi:10.1145/1242572.1242598
    title: "Lars Backstrom, Cynthia Dwork and Jon Kleinberg, Wherefore art thou R3579X? Anonymized social networks, hidden patterns, and structural steganography, WWW 2007, pages 181-190"
    locator: the attacks on graphs released with random identifiers, which motivate structural anonymity
  - paper: doi:10.1109/icdm.2009.11
    title: "Michael Hay, Chao Li, Gerome Miklau and David Jensen, Accurate estimation of the degree distribution of private networks, IEEE ICDM 2009, pages 169-178"
    locator: the release of a degree distribution under differential privacy with edge neighbors
---

k-degree anonymization changes a graph so that every vertex shares its degree with at least $k - 1$ other vertices. The goal is to stop one kind of re-identification: in a social network released with the names removed, an attacker who knows that a person has, say, 97 friends can find the person if only one vertex has degree 97. Liu and Terzi (SIGMOD 2008) asked for a k-degree anonymous supergraph of the input with the fewest added edges. Their method has two steps. A dynamic program finds, in $O(n k)$ time for $n$ vertices, the k-anonymous degree sequence closest to the input in the $L_1$ distance; this step is exact. A graph construction step then tries to add edges that give each vertex its new degree; this step is a heuristic, which may answer "unknown". When it succeeds, the result has the fewest possible added edges. The value of $k$ is a policy choice, and the protection covers only an attacker whose knowledge is the degree.

## In plain words

In a friendship graph, one person may have far more friends than anyone else. If you know that number, you can find the person even without names.

The fix is to add some friendships so that each friend count is shared by at least $k$ people. Adding edges can only raise counts, so the plan first decides the new counts. It sorts the people by count, cuts the sorted list into runs of at least $k$ people, and raises everyone in a run to the largest count of the run. A dynamic program picks the cuts that need the least total raising.

Then the plan adds the edges. It takes the person who needs the most new friends and links them to the people who also need the most, skipping people who are friends already. If it gets stuck, it reports that it could not finish.

## The problem

The input is a simple graph $G = (V, E)$ with $n$ vertices and an integer $k \ge 1$. A vector of integers is **k-anonymous** if every value in it appears at least $k$ times (Definition 1 of the paper). A graph is **k-degree anonymous** if its degree sequence is k-anonymous (Definition 2). Problem 1 of the paper asks for a k-degree anonymous simple graph $\hat G = (V, \hat E)$ with $E \subseteq \hat E$ and $|\hat E| - |E|$ as small as possible.

By the [handshake lemma](/handshake-lemma/), $|\hat E| - |E| = \tfrac12 L_1(\hat d - d)$, where $d$ and $\hat d$ are the degree sequences (Equation 1). So the problem splits into two:

- **Degree anonymization.** Given $d$ sorted with $d(1) \ge \cdots \ge d(n)$, find a k-anonymous $\hat d \ge d$ with the least $L_1(\hat d - d)$.
- **Graph construction.** Given $G$ and $\hat d$, find a supergraph of $G$ with degree sequence $\hat d$.

A complete graph is always k-degree anonymous, so a solution exists when $n \ge k$.

## The algorithm

Write $I(i, j) = \sum_{\ell = i}^{j} (d(i) - d(\ell))$ for the cost of raising the positions $i$ to $j$ of the sorted sequence to $d(i)$, and $DA(i)$ for the least cost of a k-anonymous raise of the first $i$ positions.

```pseudo id=main
K-DEGREE-ANONYMIZE(G, k)            ▷ n ≥ k
L1  d ← the degrees of G, sorted so that d(1) ≥ ... ≥ d(n)
L2  for i ← 1 to n do
L3      if i < 2k then DA(i) ← I(1, i), cut(i) ← 0
L4      else DA(i) ← min of DA(t) + I(t + 1, i) over max(k, i − 2k + 1) ≤ t ≤ i − k, cut(i) ← the best t
L5  follow cut from n back to 0; raise each group (t, i] to d(t + 1), giving d̂
L6  a(v) ← d̂(v) − d(v) for every vertex v
L7  if the sum of a is odd then return UNKNOWN
L8  while some a(v) > 0 do
L9      v ← a vertex with the largest a(v)
L10     W ← the a(v) vertices w ≠ v, not adjacent to v, with a(w) > 0 and a(w) as large as possible
L11     if |W| < a(v) then return UNKNOWN
L12     for each w in W, add the edge (v, w) and set a(w) ← a(w) − 1
L13     a(v) ← 0
L14 return G with the added edges
```

Lines L1 to L5 are the DP algorithm of the paper with its faster recursion (Equation 4). In an optimal $\hat d$, the vertices that end with the same degree form a run of the sorted sequence (Observation 1), and the run is raised to its first value. Line L3 covers prefixes shorter than $2k$, which cannot hold two runs of at least $k$. Line L4 tries every last run $(t, i]$ of length between $k$ and $2k - 1$; a longer run never helps, because it can be cut into two runs of at least $k$ without raising the cost. Lines L6 to L13 are Supergraph (Section 5.2). The paper picks an arbitrary vertex at line L9; the code takes the largest $a(v)$ and breaks ties by the position in the sorted order.

## Example

The graph has seven synthetic vertices $a, \ldots, g$ and the edges $ab$, $ac$, $ad$, $ae$, $bc$, $bf$, $de$. Its sorted degree sequence is $d = (4, 3, 2, 2, 2, 1, 0)$ for $a, b, c, d, e, f, g$. Take $k = 2$.

| $i$ | rule | candidates $DA(t) + I(t+1, i)$ | $DA(i)$ | cut$(i)$ |
|---|---|---|---|---|
| 1 | $i < 4$ | $I(1,1) = 0$ | 0 | 0 |
| 2 | $i < 4$ | $I(1,2) = 1$ | 1 | 0 |
| 3 | $i < 4$ | $I(1,3) = 1 + 2$ | 3 | 0 |
| 4 | $t = 2$ | $1 + 0$ | 1 | 2 |
| 5 | $t \in \{2, 3\}$ | $1 + 0$, $3 + 0$ | 1 | 2 |
| 6 | $t \in \{3, 4\}$ | $3 + 1$, $1 + 1$ | 2 | 4 |
| 7 | $t \in \{4, 5\}$ | $1 + 3$, $1 + 1$ | 2 | 5 |

Line L5 follows the cuts $7 \to 5 \to 2 \to 0$, so the runs are $\{a, b\}$, $\{c, d, e\}$ and $\{f, g\}$, and $\hat d = (4, 4, 2, 2, 2, 1, 1)$. The cost is $DA(7) = 2$, so at least one edge must be added. Line L6 gives $a(b) = 1$, $a(g) = 1$ and 0 elsewhere; the sum is even. Line L9 takes $b$, line L10 finds $g$, which is not adjacent to $b$, and line L12 adds the edge $bg$. The new degrees are $4, 4, 2, 2, 2, 1, 1$: every degree appears at least twice, and one added edge is the least possible.

## Correctness

The DP part is exact (Theorem 1 of the paper). By Observation 1, an optimal $\hat d$ cuts the sorted sequence into runs of at least $k$ positions, and the cost of a run $(t, i]$ is $I(t + 1, i)$. The optimal cost of the first $i$ positions is the best last run plus the optimal cost of what comes before it, which is the [principle of optimality](/principle-of-optimality/). Line L4 may skip runs of $2k$ or more: such a run $(t, i]$ splits into $(t, t + k]$ and $(t + k, i]$, both of at least $k$ positions, and raising the second part to $d(t + k + 1) \le d(t + 1)$ costs no more. So $DA(n) = \min L_1(\hat d - d)$ over all k-anonymous $\hat d \ge d$.

The construction part keeps the invariant that the current graph is a simple supergraph of $G$ and that each vertex $v$ still needs $a(v)$ edges to reach $\hat d(v)$. Line L10 only picks vertices not adjacent to $v$ and that still need edges, so no edge is repeated and no vertex goes past its target. If the loop ends, all $a(v)$ are 0, so the graph has degree sequence $\hat d$, which is k-anonymous, with exactly $DA(n)/2$ added edges. Any k-degree anonymous supergraph needs at least $DA(n)/2$ added edges, because its degree sequence is a k-anonymous vector at least $d$. So a graph returned at line L14 is optimal. UNKNOWN does not mean that no such supergraph exists; Supergraph is not an oracle, unlike ConstructGraph for graphs built from nothing (Algorithm 1, based on the Erdős-Gallai condition). The full proof is in proofs/correctness.md.

## Complexity

- Line L1 sorts in $O(n \log n)$ time, or $O(n)$ with a counting sort, since degrees are below $n$.
- With prefix sums $P(j) = d(1) + \cdots + d(j)$, each $I(t + 1, i) = (i - t)\, d(t + 1) - (P(i) - P(t))$ takes $O(1)$ time. Line L4 tries at most $k$ values of $t$, so lines L2 to L4 take $O(n k)$ time (Section 4). The paper notes that the factor $k$ can be removed with more bookkeeping, for $O(n)$ time.
- Line L5 takes $O(n)$ time.
- The paper gives $O(n\, a_{max})$ time for Supergraph with bucket arrays of vertices by residual degree, where $a_{max}$ is the largest $a(v)$. The code is simpler: each pass of line L9 scans all vertices and sorts the candidates, which costs $O(n^2 \log n)$ in the worst case.
- The extra space is $O(n)$ besides the graph.

## Properties

- **Additions only.** Every edge of $G$ stays. Running the same method on the complement graph gives the version with deletions only (Section 2).
- **Monotone in $k$.** A k-degree anonymous graph is also $k'$-degree anonymous for every $k' \le k$ (Proposition 1).
- **Exact first step, heuristic second step.** The degree sequence is optimal; the graph may not exist as a supergraph of $G$, and Supergraph may miss one that does.
- **Deterministic as coded.** The paper's Supergraph picks an arbitrary vertex at line L9; the code fixes the choice.

## Variants and improvements

- **Greedy degree anonymization.** The paper also gives a greedy $O(n k)$ method that starts each run with $k$ vertices and decides for each next vertex whether to join the run or start a new one by comparing two costs. It is not exact; in their experiments its cost was at most 1.5 times the DP cost (a measurement, Section 7.2).
- **Probing.** When Supergraph answers UNKNOWN, the Probing scheme of Section 5.3 (Algorithm 2) adds a little random noise to the input degrees, recomputes $\hat d$ and tries again, at the price of a few more edges. Their noise slightly raises the degrees of low-degree vertices, which gives the high-degree vertices more partners. The loop ends at the latest when all degrees reach $n - 1$.
- **The relaxed problem.** Section 6 drops the rule $E \subseteq \hat E$ and asks only for a large overlap. Greedy_Swap (Algorithm 3) builds a graph with degree sequence $\hat d$ from nothing and then makes edge swaps that keep the degrees and increase the overlap with $E$. The Priority algorithm instead prefers edges of $G$ while it builds.
- **Additions and deletions together.** Section 8 shows that the same framework, with small changes, handles graphs that may both gain and lose edges.
- **Stronger structural models.** Hay et al. (PVLDB 2008) group vertices into supernodes and publish only counts of edges within and between groups, which protects against attackers who know more than the degree, such as the shape of a neighbourhood.
- **Differential privacy instead.** Hay, Li, Miklau and Jensen (ICDM 2009) publish the [degree distribution](/degree-distribution/) itself under [differential privacy](/differential-privacy-definition/) with edge neighbors, where two graphs are neighbors if they differ in one edge. Node neighbors, which differ in one vertex and all its edges, give a far stronger guarantee for a person and need much more noise.

## When to use it

Use k-degree anonymization when a graph must be released as a graph, the threat is an attacker who knows degrees, and the added edges are an acceptable distortion. Liu and Terzi measured how close the anonymized graphs stay to the input, with the clustering coefficient, the average path length and other structural measures, on synthetic and real graphs of up to about 8000 vertices (Section 7). Do not use it as a general protection. An attacker who knows a neighbourhood, or who planted accounts before the release as in the [active attack on social graphs](/active-attack-on-social-graphs/), is not stopped by equal degrees, and [de-anonymization by structure](/social-network-deanonymization/) uses much more than degrees. For statistics of a graph, a differentially private release is the safer choice.

## Pitfalls

- **Allowing $t < k$ at line L4.** If the range of $t$ starts below $k$, the first run can be shorter than $k$, and the result is not k-anonymous. Both ends of the range matter: $t \ge k$ for the first runs and $t \le i - k$ for the last.
- **Raising a run to the wrong value at line L5.** Raising a run to its smallest or its mean degree needs edge deletions for the vertices above that value, which Problem 1 does not allow. With additions only, a run must go to its largest degree $d(t + 1)$.
- **Picking adjacent vertices at line L10.** If line L10 does not skip the vertices already adjacent to $v$, it adds an edge that already exists, and the result is not a simple graph. The degrees on paper are then wrong.
- **Skipping the parity test at line L7.** If the sum of $a$ is odd, no set of new edges can add exactly $a(v)$ to each vertex, because each edge adds 2 to the sum. Without the test, the loop ends with one vertex short.
- **Reading UNKNOWN at lines L7 and L11 as "impossible".** Take one edge on three vertices and $k = 2$. The DP gives $\hat d = (1, 1, 1)$ with cost 1, whose sum is odd, so line L7 answers UNKNOWN. Yet adding the two missing edges gives a triangle, which is 2-degree anonymous. Probing, or a different choice at line L9, can find a graph that the first try misses.
- **Treating degree anonymity as anonymity.** The guarantee covers only an attacker whose knowledge is one number per person. Backstrom, Dwork and Kleinberg and later work show that structure beyond degrees re-identifies people in released graphs.

## Implementations

## History

Backstrom, Dwork and Kleinberg showed in 2007 that replacing names by random identifiers does not protect a social graph. Liu and Terzi answered with k-degree anonymity at SIGMOD 2008, adapting [k-anonymity](/k-anonymity/) to graphs with the degree as the quasi-identifier. In the same year Hay et al. studied stronger structural knowledge and proposed supernodes. From 2009, work on graphs moved towards differential privacy, starting with degree distributions under edge neighbors.

## References
