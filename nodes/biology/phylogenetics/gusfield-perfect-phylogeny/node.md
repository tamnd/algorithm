---
tag: TF5DB1
kind: algorithm
slug: gusfield-perfect-phylogeny
name: Gusfield's perfect phylogeny algorithm
aliases:
- Gusfield's algorithm
area: biology/phylogenetics
level: advanced
summary: Decide in O(nm) time whether a binary n by m character matrix has a perfect phylogeny, and build one, by radix sorting the columns as binary numbers and checking that they nest.
solves: [perfect-phylogeny]
model: word-ram
complexity:
  vars: {n: the number of taxa (rows), m: the number of binary characters (columns)}
  time: {worst: Θ(n·m), best: Θ(n·m)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1991
  people: [Dan Gusfield]
  note: Gusfield gave the linear-time algorithm in Networks in 1991. The pairwise test it replaces goes back to Buneman 1971 and to Estabrook, Johnson and McMorris 1976.
prereqs: [perfect-phylogeny, four-gamete-condition, radix-sort]
see_also: [character-compatibility, phylogenetic-tree, splits-of-a-tree, camin-sokal-parsimony, dollo-parsimony, ancestral-recombination-graph-inference, counting-sort]
sources:
  - paper: doi:10.1002/net.3230210104
    title: Dan Gusfield, Efficient algorithms for inferring evolutionary trees, Networks 21(1), 1991
    locator: pp. 19 to 28, the O(nm) algorithm for binary characters by sorting the columns as binary numbers
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 17, the section on the perfect phylogeny problem for binary characters
  - book: isbn:9780198509424
    title: Charles Semple and Mike Steel, Phylogenetics, Oxford University Press, 2003
    locator: Chapter 4, compatibility of binary characters
  - paper: doi:10.1016/0025-5564(76)90035-3
    title: George F. Estabrook, C. S. Johnson Jr. and F. R. McMorris, A mathematical foundation for the analysis of cladistic character compatibility, Mathematical Biosciences 29(1-2), 1976
    locator: pp. 181 to 187, pairwise compatibility of binary characters implies joint compatibility
  - book: isbn:9780878931774
    title: Joseph Felsenstein, Inferring Phylogenies, Sinauer Associates, 2004
    locator: Chapter 8, compatibility
---

Gusfield's algorithm decides whether a binary character matrix has a [perfect phylogeny](/perfect-phylogeny/), and builds one if it does. The input is an $n \times m$ matrix of 0s and 1s: rows are taxa and columns are characters. The rooted version takes the ancestor to be the all-zero row. The algorithm sorts the columns as binary numbers with a [radix sort](/radix-sort/), then makes one pass over each row to check that the columns nest. It runs in $\Theta(nm)$ time, which is the size of the input. The pairwise [four-gamete test](/four-gamete-condition/) answers the same yes or no question in $O(nm^2)$ time and builds no tree.

## In plain words

Each column says which taxa have a trait. In a perfect phylogeny, each trait appears one time, on one branch of the tree, and every taxon below that branch keeps it. So the group of taxa with a trait is the set of leaves below one branch. Two such groups must be either separate or one inside the other. They can never overlap only in part.

The algorithm puts the biggest groups first, so that a group always comes before the groups inside it. Then each taxon reads its traits in that order. Each trait should hang under the trait that the taxon read just before it. If two taxa with the same trait disagree about where it hangs, there is no perfect phylogeny. If they all agree, these "hangs under" links are the tree.

## The problem

The input is a matrix $M$ with $n$ rows and $m$ columns, with $M[i][c] \in \{0, 1\}$. Let $O_c$ be the set of rows with a 1 in column $c$. A rooted perfect phylogeny with the all-zero ancestor is a rooted tree in which each nonzero column labels exactly one edge, each row is a leaf, and the labels on the path from the root to row $i$ are exactly the columns where row $i$ holds a 1. Internal nodes may have one child. The question is whether such a tree exists, and if so, to output one. This is the binary, rooted case of the [perfect phylogeny problem](/perfect-phylogeny/). The unrooted case reduces to it, as the section on variants shows.

## The algorithm

Rows are numbered from 1 here, and row 1 is the most significant digit when a column is read as a binary number.

```pseudo id=main
GUSFIELD-PERFECT-PHYLOGENY(M)             ▷ M is n × m with entries 0 and 1, ancestor all zero
L1  order ← the columns in decreasing binary value, row 1 most significant   ▷ radix sort
L2  in this order, drop the all-zero columns and merge each run of equal columns into one class
L3  let C_1, …, C_k be the classes in this order; parent[1 .. k] ← nil
L4  for i ← 1 to n do
L5      last ← 0
L6      for j ← 1 to k do
L7          if M[i][C_j] = 1 then
L8              if parent[j] = nil then parent[j] ← last
L9              else if parent[j] ≠ last then return NO PHYLOGENY
L10             last ← j
L11     leaf[i] ← last
L12 return the tree on nodes 0 .. k with edges parent[j] → j labeled C_j, and row i as a leaf below node leaf[i]
```

Line L1 is a least significant digit radix sort with base 2. It makes $n$ stable passes, from row $n$ up to row 1. Each pass puts the columns with a 1 in that row before the columns with a 0. After the sort, a column that is a strict superset of another one comes first, because it is a larger binary number. Equal columns end up next to each other, so line L2 can merge them by comparing each column with the one before it.

In the loop of line L6, $last$ is the class that row $i$ met most recently. When row $i$ meets class $j$, the edge of $j$ must hang below the edge of $last$. Line L8 records this for the first row of class $j$. Line L9 checks it for every other row of class $j$. Node 0 is the root, and $parent[j] < j$ always holds, so the edges form a tree.

## Example

Take five taxa A to E and five characters $c_0$ to $c_4$.

| row | $c_0$ | $c_1$ | $c_2$ | $c_3$ | $c_4$ |
|---|---|---|---|---|---|
| A | 1 | 1 | 0 | 0 | 0 |
| B | 0 | 0 | 1 | 0 | 0 |
| C | 1 | 1 | 0 | 0 | 1 |
| D | 0 | 0 | 1 | 1 | 0 |
| E | 0 | 1 | 0 | 0 | 0 |

Read down each column with row A as the most significant digit. Then $c_0 = 10100_2 = 20$, $c_1 = 10101_2 = 21$, $c_2 = 01010_2 = 10$, $c_3 = 00010_2 = 2$ and $c_4 = 00100_2 = 4$. Line L1 gives the order $c_1, c_0, c_2, c_4, c_3$. No column is zero and no two are equal, so the classes are $C_1 = c_1$, $C_2 = c_0$, $C_3 = c_2$, $C_4 = c_4$ and $C_5 = c_3$.

| row | classes met, in order | parent entries set or checked | leaf |
|---|---|---|---|
| A | 1, 2 | parent[1] ← 0, parent[2] ← 1 | 2 |
| B | 3 | parent[3] ← 0 | 3 |
| C | 1, 2, 4 | 1 is 0 (ok), 2 is 1 (ok), parent[4] ← 2 | 4 |
| D | 3, 5 | 3 is 0 (ok), parent[5] ← 3 | 5 |
| E | 1 | 1 is 0 (ok) | 1 |

The result is the tree `((E,(A,(C)c4)c0)c1,(B,(D)c3)c2)`. Here a pair of parentheses is a node, and the label after it is the character on the edge above that node. The edge $c_1$ leads to the group $\{A, C, E\}$. Below it, $c_0$ leads to $\{A, C\}$, and $c_4$ leads to $C$ alone. The other side of the root has $c_2$ to $\{B, D\}$, then $c_3$ to $D$. Every root to leaf path spells its row. For example, the path to C crosses $c_1$, $c_0$ and $c_4$.

Now add a column $c_5 = (1, 0, 0, 0, 1)$, which is $10001_2 = 17$. It sorts between $c_0$ and $c_2$, so it is class 3. Row A meets classes 1, 2, 3 and sets $parent[3] \leftarrow 2$. Row E then meets class 1 and class 3, so it has $last = 1$ at class 3. Since $parent[3] = 2 \ne 1$, line L9 returns NO PHYLOGENY. The reason is that $O_{c_5} = \{A, E\}$ and $O_{c_0} = \{A, C\}$ share A, but neither contains the other. The tests in the implementation check both runs.

## Correctness

The proof is in four steps. First, in a rooted perfect phylogeny, $O_c$ is the set of leaves below the edge of $c$, and two such sets are disjoint or nested. Second, after the sort, a strict superset always comes before its subsets. Third, if the sets are laminar, every column before $j$ that contains a row of $O_j$ is a strict superset of $O_j$, so all rows of $O_j$ give the same $last$ at line L9, and the run reaches line L12. Fourth, if the run reaches line L12, a strong induction on $j$ shows that the sets are laminar, and the chain $leaf[i], parent[leaf[i]], \ldots, 0$ visits exactly the classes that contain row $i$. So the output is a perfect phylogeny. The full proof is in the proof file of this page. It also shows that the rooted problem has a solution if and only if no two columns show all three pairs 01, 10 and 11.

## Complexity

- **Time.** The radix sort of line L1 makes $n$ passes, and each pass moves $m$ columns, so it takes $\Theta(nm)$ time. Line L2 compares each column with the one before it in $O(n)$ time, so $O(nm)$ in total. Lines L4 to L11 read each entry of the $k \le m$ class columns one time, which is $O(nm)$. The total is $\Theta(nm)$ on every input, including the inputs that have no phylogeny, because the sort always runs to the end.
- **Space.** Besides the matrix, the algorithm stores the column order, the classes, the array $parent$ and the array $leaf$. This is $O(n + m)$ words. The output tree has $k + 1 \le m + 1$ internal nodes and $n$ leaves.
- **Model.** The cost is counted on the [word RAM](/word-ram/), with the matrix stored as an array of entries. The algorithm reads each entry a constant number of times, so it is linear in the input size.

The pairwise four-gamete test takes $O(nm^2)$ time, because it looks at every pair of columns. Gusfield's algorithm avoids the pairs: after the sort, each class needs only to agree with one parent.

## Properties

- **It builds the tree.** A yes answer comes with a perfect phylogeny. Its internal nodes are the distinct column sets, and the parent of each set is the smallest set that strictly contains it.
- **It finds a witness on failure.** Suppose line L9 fails at class $j$ for row $i$, and let $q$ be the larger of $parent[j]$ and $last$. Then $q \ge 1$, and the sets of $C_j$ and $C_q$ overlap but neither contains the other. So these two columns show the three pairs 01, 10 and 11. The reason: the row that set $parent[j]$ and the row $i$ disagree on whether they contain $C_q$, and a class before $j$ cannot be a strict subset of $C_j$.
- **Deterministic and not recursive.** It uses two arrays and two nested loops.

## Variants and improvements

- **The unrooted problem.** If no ancestor is given, complement every column where row 1 holds a 1. Then row 1 is all zero, and the rooted problem on the new matrix is equivalent to the unrooted problem on the old one, because a column and its complement change on the same edge. Root the tree at row 1 and forget the root. The cost stays $\Theta(nm)$. On the new matrix, three gametes in a pair of columns means four gametes in the old one, because row 1 adds the pair 00. This is how the [four-gamete condition](/four-gamete-condition/) follows from the rooted test.
- **Sorting by the number of ones.** A strict superset also has more ones. So a [counting sort](/counting-sort/) of the columns by their number of ones, in decreasing order, also makes the proof work, and it also costs $O(nm)$ to count the ones. Equal columns need not be adjacent in this order. They then give a chain of unary nodes, which can be merged later.
- **Multistate characters.** For characters with more than two states the problem is [NP-complete](/np-complete/) (Bodlaender, Fellows and Warnow 1992, and Steel 1992). It is polynomial when the number of states $r$ is fixed: Agarwala and Fernández-Baca gave an $O(2^{3r}(nm^3 + m^4))$ algorithm in 1994, and Kannan and Warnow an $O(2^{2r} n m^2)$ algorithm in 1997. The [perfect phylogeny](/perfect-phylogeny/) page has the details.
- **Haplotypes.** In the perfect phylogeny haplotyping problem, the input is genotypes and the two haplotypes of each row are unknown. Gusfield reduced it to a graph realization problem in 2002, and later work by Ding, Filkov and Gusfield gave a linear-time algorithm.

## When to use it

Use it when the data are binary and you expect no homoplasy: each mutation happened one time and was never lost. This is the infinite sites model of population genetics for a region without recombination, and it is a common model for single nucleotide variants in tumor phylogenies. A yes answer gives the tree in linear time. Real data usually have errors, recombination or back mutation, and then the answer is no. In that case use the four-gamete test to find the conflicting pairs, a [character compatibility](/character-compatibility/) method to keep a largest consistent subset, a parsimony method such as [maximum parsimony](/maximum-parsimony/), or a model with recombination such as the [ancestral recombination graph](/ancestral-recombination-graph-inference/).

## Pitfalls

- **The wrong root.** The rooted version assumes that the ancestor is all zero. The matrix with rows $(0,1)$, $(1,0)$ and $(1,1)$ has no rooted perfect phylogeny, but it has an unrooted one: complement column 2 and the rooted test succeeds. Decide which problem you need before you call the rooted version.
- **Sorting in increasing order.** Then subsets come before supersets, and line L9 rejects matrices that have a phylogeny.
- **Comparing only adjacent classes.** A check that each class is nested in the class just before it in sorted order is wrong. In the example above, $c_2$ follows $c_0$ but is disjoint from it. The check must use the previous class of each row.
- **Equal columns as separate classes without care.** With radix sort, equal columns are adjacent, and keeping them separate gives a unary node for each copy. That is still a valid tree, but code that expects $k$ distinct sets must merge them.
- **Zero columns.** An all-zero column labels no edge. If it is kept as a class, it has no rows, and line L8 never sets its parent.
- **Missing entries.** The algorithm needs a complete matrix. Reading an unknown entry as 0 or as 1 can turn a yes into a no, or build a tree that the true data do not support. Missing data need a different algorithm.

## Implementations

## History

The pairwise test for binary characters is older than the algorithm. Buneman showed in 1971 that pairwise compatible splits fit on one tree, and Estabrook, Johnson and McMorris proved in 1976 that pairwise compatibility of binary characters implies that all of them fit on one tree. Checking all pairs costs $O(nm^2)$. Gusfield gave the $O(nm)$ algorithm in his 1991 paper "Efficient algorithms for inferring evolutionary trees", together with other results on tree reconstruction. His 1997 book presents it as the main algorithm for binary perfect phylogeny. Later work used it as a base for haplotype inference and for phylogenies with recombination, such as the galled trees of Gusfield, Eddhu and Langley.

## References
