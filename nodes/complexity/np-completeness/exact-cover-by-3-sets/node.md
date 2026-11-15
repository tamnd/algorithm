---
tag: RM8D4P
kind: problem
slug: exact-cover-by-3-sets
name: Exact cover by 3-sets
aliases:
- 3-exact cover
- X3C
area: complexity/np-completeness
level: advanced
summary: Given a set of 3q elements and a collection of 3-element subsets, decide whether q of the subsets partition the set. NP-complete in the strong sense.
prereqs: [three-dimensional-matching, exact-cover]
see_also: [exact-cover, three-dimensional-matching, subset-sum-problem, set-cover, set-packing, algorithm-x, crossword-filling-problem, steiner-tree-problem]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1 (X3C as a generalization of 3DM, and its use in later proofs) and the appendix, problem SP2 (EXACT COVER BY 3-SETS)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, the problems EXACT COVER and 3-DIMENSIONAL MATCHING, and the reduction from EXACT COVER to KNAPSACK
  - paper: Teofilo F. Gonzalez, Clustering to minimize the maximum intercluster distance, Theoretical Computer Science 38, 1985
    title: Gonzalez, X3C stays NP-complete when each element occurs in exactly three sets
    locator: the NP-completeness lemma for the restricted X3C
  - paper: Andreas Björklund, Thore Husfeldt and Mikko Koivisto, Set partitioning via inclusion-exclusion, SIAM Journal on Computing 39(2), 2009
    title: Björklund, Husfeldt and Koivisto, exact covers counted in O*(2^n) time
    locator: the main theorem
---

Exact cover by 3-sets, or X3C, asks whether a given collection of 3-element subsets of a set with $3q$ elements contains $q$ subsets that partition the set. It is the [exact cover](/exact-cover/) problem with all subsets of size three, and it generalizes [three-dimensional matching](/three-dimensional-matching/), which adds the condition that the elements come in three groups and each subset takes one element from each group. X3C is [NP-complete](/np-complete/), and it stays NP-complete when each element is in exactly three subsets. Garey and Johnson list it as SP2 and use it as a source problem in many proofs, because it has no extra structure to respect. With subsets of size two, the question is whether a graph has a perfect matching, which is in P.

## In plain words

You have nine friends and a list of possible teams of three. Can you choose three teams so that every friend is in exactly one team?

Each choice of a team removes three friends, and the remaining friends must still be covered by the remaining teams. A wrong early choice can leave one friend who fits in no team. For small cases you can try the choices one by one. For large cases no fast method is known. The problem is a standard hard problem, and many puzzles and planning tasks can be written as it.

## Definition

**Instance.** A finite set $X$ with $\lvert X \rvert = 3q$, and a collection $C$ of 3-element subsets of $X$.

**Question.** Does $C$ contain a subcollection $C'$ such that each element of $X$ is in exactly one member of $C'$? Such a $C'$ has exactly $q$ members.

**Encoding.** The instance lists the elements and the $\lvert C \rvert \le \binom{3q}{3}$ subsets. There are no large numbers. The subcollection $C'$ is a certificate that a verifier checks in linear time, so the problem is in NP.

**Complexity.** X3C is NP-complete under Karp reductions. [Three-dimensional matching](/three-dimensional-matching/) is its special case, so the reduction from 3DM is a restriction (Garey and Johnson, Section 3.1). 3DM is NP-complete by Karp (1972) and by Garey and Johnson (Section 3.1.2). X3C has no numbers, so it is NP-complete in the [strong sense](/strong-np-hardness/).

## Variants

- **Exactly three occurrences.** X3C stays NP-complete when each element is in exactly three subsets (Gonzalez 1985).
- **At most two occurrences.** When each element is in at most two subsets, X3C is in P. Give each subset $S$ a variable $x_S \in \{0, 1\}$. An element in no subset gives a no-answer. An element in one subset $S$ forces $x_S = 1$. An element in two subsets $S$ and $T$ needs $x_S \neq x_T$. These are the constraints of a 2-colouring of the graph whose vertices are the subsets, with some vertices forced to colour 1, and a search over each connected component checks them in linear time.
- **General sizes.** With subsets of any size, the problem is [exact cover](/exact-cover/). With subsets of size two, it is [perfect matching](/perfect-matching/) in a general graph, which is in P.
- **Covering and packing.** Allow overlaps and ask for $q$ subsets that cover $X$: since $q$ sets of size 3 cover $3q$ elements only when they are disjoint, this is the same question, so [set cover](/set-cover/) with sets of size 3 is NP-complete. Ask for the largest number of disjoint subsets: this is 3-set packing; see [set packing](/set-packing/).
- **Counting.** Count the exact covers. The inclusion-exclusion method below counts them.

## Examples

**A yes-instance with two solutions.** Let $X = \{1, \ldots, 9\}$, written as a $3 \times 3$ grid with rows $\{1, 2, 3\}$, $\{4, 5, 6\}$, $\{7, 8, 9\}$, and let $C$ contain the three rows and the three columns $\{1, 4, 7\}$, $\{2, 5, 8\}$, $\{3, 6, 9\}$. There are exactly two exact covers: the rows and the columns.

**A no-instance.** Let $X = \{1, \ldots, 9\}$ and

$$C = \{\{1, 2, 3\}, \{1, 4, 5\}, \{2, 4, 6\}, \{3, 5, 6\}, \{6, 7, 8\}, \{7, 8, 9\}\}.$$

The element 9 is only in $\{7, 8, 9\}$, so this subset must be chosen, and then $\{6, 7, 8\}$ cannot be. The elements 1 to 6 must be covered by two disjoint subsets from the first four. But each two of the first four subsets share an element. So there is no exact cover.

**Reduction to subset sum.** Let $X = \{1, \ldots, 6\}$ and $C = \{\{1, 2, 3\}, \{4, 5, 6\}, \{1, 2, 4\}\}$, with $m = 3$ subsets. In base $m + 1 = 4$, with one digit for each element and element 1 in the last digit, the subsets become $000111_4 = 21$, $111000_4 = 1344$ and $001011_4 = 69$. The target is $111111_4 = 1365$. The answer is yes: $21 + 1344 = 1365$, which corresponds to the exact cover $\{1, 2, 3\}, \{4, 5, 6\}$.

## Known algorithms

- **Backtracking.** [Algorithm X](/algorithm-x/) with [dancing links](/dancing-links/) picks an uncovered element with the fewest candidate subsets and branches on them. It is the usual practical method, with exponential worst-case time; see [exact cover](/exact-cover/).
- **Inclusion-exclusion (Björklund, Husfeldt and Koivisto 2009).** Exact covers of an $n$-element set are counted in $O^*(2^n)$ time, which is $O^*(8^q)$ for X3C, on a [word RAM](/word-ram/).
- **Dynamic programming over subsets.** Keep the set of covered elements, and always cover the smallest uncovered element next. This takes $O^*(2^{3q})$ time and space.
- **Parameterized packing.** Finding $k$ disjoint subsets is [fixed-parameter tractable](/fixed-parameter-tractable/) in $k$; see [parameterized set packing](/parameterized-set-packing/).
- **Bounded occurrences.** With at most two occurrences of each element, linear time by the 2-colouring argument above.

## Bounds

- **NP-completeness.** NP-complete under Karp reductions, even with exactly three occurrences of each element. There is no polynomial-time algorithm unless P = NP.
- **Strong NP-completeness.** X3C has no numbers, so it is NP-complete in the strong sense, and it can be the source of pseudo-polynomial transformations.
- **Boundary.** At most two occurrences of each element give a problem in P, and exactly three occurrences give an NP-complete problem, unless P = NP.

## Reductions

- **From three-dimensional matching (restriction).** Replace each triple $(w, x, y)$ by the set $\{w, x, y\}$ over the universe $W \cup X \cup Y$. On the two 3DM examples of [three-dimensional matching](/three-dimensional-matching/), with 7 and 8 triples, this gives X3C instances on 9 elements whose answers are yes and no, as for 3DM.
- **To subset sum (Karp reduction).** Number the elements $0, \ldots, 3q - 1$, and map the subset $S$ to $\sum_{i \in S} (m+1)^i$, where $m = \lvert C \rvert$. The target is $\sum_{i < 3q} (m+1)^i$. In each digit at most $m$ ones are added, so no carries occur, and a subset of numbers hits the target if and only if the subsets cover each element exactly once. The numbers have $3q$ digits in base $m + 1$, so the reduction takes polynomial time. See the [subset sum problem](/subset-sum-problem/).
- **To set cover (Karp reduction).** Ask for a cover by $q$ subsets, as in Variants.
- **To exact cover.** X3C is a special case of [exact cover](/exact-cover/). Karp (1972) reduced exact cover to the [Steiner tree problem](/steiner-tree-problem/) in graphs and to knapsack, so these reductions also start from X3C.
- **To puzzles.** Fill-in puzzles such as [crossword filling](/crossword-filling-problem/) are shown NP-complete by reductions from X3C.

## Applications

- **NP-hardness proofs.** X3C is a common source problem for proofs on graphs, covering, clustering and scheduling, because its instances are uniform and its certificates are simple.
- **Design and grouping.** Splitting $3q$ people into teams of three from a list of allowed teams, or $3q$ tasks into groups of three that can run together, is X3C.
- **Combinatorial designs.** A Steiner triple system is a collection of triples such that each pair of points is in exactly one triple. Finding a parallel class of such a system, that is, a set of disjoint triples that covers every point, is an exact cover by 3-sets question.

## References
