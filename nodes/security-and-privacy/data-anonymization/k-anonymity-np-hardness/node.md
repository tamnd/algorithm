---
tag: H3YNYG
kind: theorem
slug: k-anonymity-np-hardness
name: NP-hardness of optimal k-anonymity
aliases:
- Meyerson-Williams theorem
area: security-and-privacy/data-anonymization
level: core
summary: "Fewest suppressed cells for k-anonymity is NP-hard for each fixed k at least 3 (Meyerson-Williams), also with a ternary alphabet (Aggarwal et al.). 2-anonymity is in P."
prereqs: [k-anonymity, three-dimensional-matching, polynomial-time-reduction, np-complete]
see_also: [k-anonymity-approximation, generalization-and-suppression, mondrian-anonymization, samarati-algorithm, exact-cover-by-3-sets, perfect-matching, hypergraph, apx]
sources:
  - paper: doi:10.1145/1055558.1055591
    title: "Adam Meyerson and Ryan Williams, On the complexity of optimal k-anonymity, Proceedings of the 23rd ACM Symposium on Principles of Database Systems (PODS 2004)"
    locator: "pp. 223 to 228, Theorem 3.1 (entry suppression), Theorem 3.2 (attribute suppression) and Section 4 (the approximation algorithms)"
  - paper: doi:10.1007/978-3-540-30570-5_17
    title: "Gagan Aggarwal, Tomas Feder, Krishnaram Kenthapadi, Rajeev Motwani, Rina Panigrahy, Dilys Thomas and An Zhu, Anonymizing tables, Proceedings of ICDT 2005, LNCS 3363"
    locator: "pp. 246 to 258, Theorem 1, NP-hardness for k = 3 over a ternary alphabet by a reduction from edge partition into triangles"
  - url: "https://arxiv.org/abs/1004.3811"
    title: Jeremiah Blocki and Ryan Williams, Resolving the complexity of some data privacy problems, ICALP 2010
    locator: "the abstract and the main results, 2-anonymity is in P, binary 3-anonymity is NP-hard, and 3-anonymity with 27 attributes is MAX SNP-hard"
  - url: "https://arxiv.org/abs/0707.0421"
    title: Paola Bonizzoni, Gianluca Della Vedova and Riccardo Dondi, The k-anonymity problem is hard
    locator: "the abstract and the main results, APX-hardness for a binary alphabet with k = 3 and for rows of length at most 8 with k = 4"
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, a guide to the theory of NP-completeness, W. H. Freeman, 1979
    locator: "Section 3.1.2 and Appendix A3.1, problem [SP1], 3-dimensional matching"
---

To make a table [k-anonymous](/k-anonymity/) by suppression, replace some cells by a star until each row is equal to at least $k - 1$ other rows. Each suppressed cell loses information, so the natural goal is the fewest stars. Meyerson and Williams (2004) proved that this goal is [NP-hard](/np-hard/) for each fixed $k \ge 3$, by a reduction from perfect matching in hypergraphs. They also proved it for the suppression of whole columns. Aggarwal et al. (2005) showed that the hardness for $k = 3$ holds even when each cell has one of three values. For $k = 2$ the problem is in P. So no exact polynomial algorithm is expected, and the practical algorithms are heuristics or [approximations](/k-anonymity-approximation/).

## Statement

A *table* is a list of $n$ rows $v_1, \ldots, v_n \in \Sigma^m$ over an alphabet $\Sigma$. A *suppression* replaces some entries by the symbol $*$, which is not in $\Sigma$. The result is *k-anonymous* if each row is equal to at least $k - 1$ other rows. Its *cost* is the number of stars. The decision problem ENTRY-SUPPRESSION$_k$ is: given a table and an integer $c$, is there a k-anonymous suppression of cost at most $c$? The problem ATTRIBUTE-SUPPRESSION$_k$ is the same, but each column is either kept in all rows or suppressed in all rows, and the cost is the number of suppressed columns.

**Theorem 1 (Meyerson and Williams 2004, Theorem 3.1).** For each fixed $k \ge 3$, ENTRY-SUPPRESSION$_k$ is NP-complete when the alphabet may grow with the input. The proof below uses $n + 1$ values for $n$ rows.

**Theorem 2 (Meyerson and Williams 2004, Theorem 3.2).** For each fixed $k \ge 3$, ATTRIBUTE-SUPPRESSION$_k$ is NP-hard, already for a binary alphabet.

**Theorem 3 (Aggarwal et al. 2005, Theorem 1).** ENTRY-SUPPRESSION$_3$ is NP-hard for the alphabet $\{0, 1, 2\}$, with an unbounded number of columns.

## In plain words

Give each person a row, and each candidate group a column. A person who is in the group gets a 0 in that column, and everyone else gets a value that is theirs alone. A group of rows can look the same only in a column where all of them have a 0, that is, in the column of a candidate group that holds all of them. Two rows that share two such columns would have to be in two candidate groups at once, and no $k$ rows can be. So in the cheapest release each row keeps one cell, and the groups of the release are candidate groups that do not overlap and cover everybody. Finding such a cover is a classic hard problem. So finding the cheapest release is at least as hard.

## Proof

**Membership in NP.** A certificate is the suppressed table. A verifier counts the stars and sorts the rows to check that each class of equal rows has at least $k$ rows, in polynomial time.

**The source problem.** A $k$-uniform [hypergraph](/hypergraph/) $H = (U, E)$ has a set $U$ of vertices and a set $E$ of distinct edges, each a set of exactly $k$ vertices. A *perfect matching* is a set of pairwise disjoint edges whose union is $U$. PERFECT-MATCHING$_k$ asks whether $H$ has one. For $k = 3$ it is NP-complete: it contains [3-dimensional matching](/three-dimensional-matching/), the problem [SP1] of Garey and Johnson, where $U = X \cup Y \cup Z$ with $|X| = |Y| = |Z| = q$ and each edge has one vertex in each part. For $k > 3$, map a 3-dimensional matching instance to the $k$-uniform hypergraph with vertex set $X \cup Y \cup Z \cup X^{(1)} \cup \cdots \cup X^{(k-3)}$, where each $X^{(i)}$ is a new copy of $X$, and with the edge $\{x, y, z, x^{(1)}, \ldots, x^{(k-3)}\}$ for each triple $(x, y, z)$. Distinct triples give distinct edges. A perfect matching has $q$ edges, and the triples of $q$ disjoint edges are disjoint and cover $X$, $Y$ and $Z$; conversely, a 3-dimensional matching gives $q$ disjoint edges that cover all copies, because the copies of $x$ follow $x$. So PERFECT-MATCHING$_k$ is NP-complete for each fixed $k \ge 3$.

**The reduction (proof of Theorem 1).** Let $U = \{u_1, \ldots, u_n\}$ and $E = \{e_1, \ldots, e_m\}$, with $m \ge 1$. Build the table with $n$ rows and $m$ columns:
$$v_i[j] = \begin{cases} 0 & \text{if } u_i \in e_j, \\ i & \text{otherwise,} \end{cases}$$
over the alphabet $\{0, 1, \ldots, n\}$, and set $c = n(m - 1)$. The table has $n m$ entries and takes polynomial time to build. We show that $H$ has a perfect matching if and only if the table has a k-anonymous suppression of cost at most $c$.

*If.* Let $M$ be a perfect matching. Each row $i$ lies in exactly one edge $e_j \in M$. In row $i$, keep column $j$ and suppress the other $m - 1$ entries. For each $e_j \in M$, its $k$ rows all have $0$ in column $j$, so they are equal after the suppression: $0$ in column $j$ and $*$ elsewhere. Each class has $k$ rows, and the cost is $n(m - 1) = c$.

*Only if.* Take a k-anonymous suppression of cost at most $c$, and split the rows into classes of equal suppressed rows. Each class has at least $k \ge 3$ rows.

Claim A: if row $i$ keeps column $j$, then $v_i[j] = 0$, and each row $i'$ of its class has $u_{i'} \in e_j$. Proof: each row $i'$ of the class keeps column $j$ with the same value as row $i$. Take $i' \ne i$ in the class, which exists since the class has at least 2 rows. The entries of row $i'$ are $0$ or $i'$, so the value $i$ cannot be in it. So the common value is $0$, and $u_{i'} \in e_j$ for each row $i'$ of the class, including $i$.

Claim B: each row keeps at most one column. Proof: suppose row $i$ keeps the columns $j \ne j'$, and let $C$ be its class. By Claim A, the vertices of the rows of $C$ are in $e_j \cap e_{j'}$. So $|e_j \cap e_{j'}| \ge |C| \ge k = |e_j| = |e_{j'}|$, and $e_j = e_{j'}$. This contradicts that the edges are distinct.

By Claim B each row has at least $m - 1$ stars, so the cost is at least $n(m - 1) = c$. As the cost is at most $c$, each row keeps exactly one column. Let $C$ be a class, and let $j$ be the column its rows keep; all rows of $C$ keep the same column, since they are equal. By Claim A the vertices of $C$ are in $e_j$, so $k \le |C| \le |e_j| = k$, and the vertices of $C$ are exactly $e_j$. The classes are disjoint and cover all rows, so their edges are disjoint and cover $U$, and they form a perfect matching.

So PERFECT-MATCHING$_k \le_p$ ENTRY-SUPPRESSION$_k$ by a [polynomial-time reduction](/polynomial-time-reduction/), and with the membership in NP, ENTRY-SUPPRESSION$_k$ is [NP-complete](/np-complete/) for each fixed $k \ge 3$. $\blacksquare$

**Worked example.** Let $k = 3$, $U = \{1, \ldots, 6\}$, and $e_1 = \{1, 2, 3\}$, $e_2 = \{4, 5, 6\}$, $e_3 = \{3, 4, 5\}$, so $m = 3$ and $c = 12$.

| row | $e_1$ | $e_2$ | $e_3$ |
|---|---|---|---|
| 1 | 0 | 1 | 1 |
| 2 | 0 | 2 | 2 |
| 3 | 0 | 3 | 0 |
| 4 | 4 | 0 | 0 |
| 5 | 5 | 0 | 0 |
| 6 | 6 | 0 | 6 |

The matching $\{e_1, e_2\}$ gives the classes $\{1, 2, 3\}$, released as $(0, *, *)$, and $\{4, 5, 6\}$, released as $(*, 0, *)$, with cost 12. If $e_2$ is replaced by $\{2, 5, 6\}$, no two edges are disjoint and no perfect matching exists. A search over all splits into classes of at least 3 rows then gives a least cost of 15, which is more than 12, as the proof says.

**Sketch of Theorem 2 (cited, Meyerson and Williams 2004, Theorem 3.2).** Suppressing a whole column is the same as full-domain generalization with a hierarchy of two levels, the value and $*$. Meyerson and Williams prove NP-hardness of the least number of suppressed columns for $k \ge 3$ by a separate reduction, which works with two values per cell. We do not repeat that construction here; see the paper.

**Sketch of Theorem 3 (cited, Aggarwal et al. 2005, Theorem 1).** The source problem is edge partition into triangles: can the edges of a graph be split into triangles? It is NP-complete, and Aggarwal et al. cite Kann (1994) for it. Take a graph with $3m$ edges, so that a partition has $m$ triangles. A row stands for an edge and a column for a vertex, with a 1 at the two ends of the edge. A triangle of rows then needs 3 stars per row, so 9 per triangle. But a star of three edges at one vertex has the same cost, so a binary table cannot tell the two apart. The fix uses $t = 1 + \lceil \log_2(3m) \rceil$ blocks of columns: in each block, the two ends of an edge get the values 1 and 2, in an order set by one bit of the number of the edge. Aggarwal et al. show that the table has a 3-anonymous suppression of cost at most $9mt$ if and only if the graph has a partition into triangles, and they extend the result to $k = \binom{r}{2}$ with partitions into cliques of $r$ vertices.

## Consequences

- **No exact polynomial algorithm, unless P = NP.** Each algorithm that always finds the fewest stars, for some fixed $k \ge 3$, takes more than polynomial time on some inputs, unless P = NP. This is why the practical algorithms are heuristics, such as [Datafly](/datafly/) and [Mondrian](/mondrian-anonymization/), or exact searches over a restricted space, such as [Samarati's algorithm](/samarati-algorithm/) over the lattice of full-domain generalizations, whose size is exponential in the number of attributes.
- **Full-domain generalization is also hard.** By Theorem 2, the least number of suppressed columns is NP-hard to find, even with hierarchies of two levels. So the exponential size of the lattice in [generalization and suppression](/generalization-and-suppression/) is not only a weakness of the known searches.
- **Approximation.** Meyerson and Williams (2004) give an $O(k \log k)$ approximation, $3k(1 + \ln 2k)$, in time exponential in $k$, and an $O(k \log m)$ approximation in polynomial time, where $m$ is the number of columns. Aggarwal et al. (2005) give a polynomial $O(k)$ approximation, the [O(k) approximation for k-anonymity](/k-anonymity-approximation/). Park and Shim (2007) improve the ratio to $O(\log k)$; see their paper for the running time.
- **No approximation scheme.** For a binary alphabet with $k = 3$, and for rows of length at most 8 with $k = 4$, the problem is [APX](/apx/)-hard (Bonizzoni, Della Vedova and Dondi). So there is no polynomial-time approximation scheme for these cases unless P = NP.

## Tightness

- **$k \ge 3$ is needed.** For $k = 1$ each table is 1-anonymous with no stars. For $k = 2$, Blocki and Williams (2010) show that the problem is in P. So the condition $k \ge 3$ of Theorem 1 cannot be dropped.
- **The large alphabet is not needed.** Theorem 1 uses $n + 1$ values. Theorem 3 needs only three, and Blocki and Williams give another proof that 3-anonymity stays NP-hard with binary values. So the condition on the alphabet in Theorem 1 is a feature of that proof, not of the problem.
- **Many columns are needed, or many values.** Blocki and Williams show that with $n$ rows, $c = O(1)$ values and at most $\log_{2c+2} \log n$ columns, the problem is in P, and in $O(n)$ time when $c$ and the number of columns are constants. With 27 columns, 3-anonymity is already MAX SNP-hard.
- **Exponential in $n$, not worse.** For each $k > 1$, the problem can be solved in $O(4^n \mathrm{poly}(n))$ time (Blocki and Williams 2010).

## History

Samarati and Sweeney introduced k-anonymity with generalization and suppression in 1998, and the early algorithms searched for the least generalization without a bound on their running time. Meyerson and Williams asked how hard the optimal version is and proved, at PODS 2004, NP-hardness for entry and attribute suppression with $k \ge 3$, together with the first approximation algorithms. Aggarwal, Feder, Kenthapadi, Motwani, Panigrahy, Thomas and Zhu brought the alphabet down to three values and gave the $O(k)$ approximation at ICDT 2005. Bonizzoni, Della Vedova and Dondi proved APX-hardness for binary tables in 2007, and Blocki and Williams settled the case $k = 2$ at ICALP 2010.

## References
