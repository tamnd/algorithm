---
tag: C2Z2BC
kind: problem
slug: zero-one-equations
name: Zero-one equations
area: complexity/reductions-catalogue
level: core
summary: Given a 0-1 matrix A, decide whether some 0-1 vector x satisfies Ax = 1, so that every row has exactly one chosen 1. NP-complete; it is exact cover in matrix form.
prereqs: [np-complete, three-dimensional-matching, exact-cover]
see_also: [exact-cover-by-3-sets, subset-sum-problem, binary-integer-programming, knapsack-decision, hamiltonian-cycle-problem, traveling-salesman-decision, karp-21-np-complete, strong-np-hardness]
sources:
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms, McGraw-Hill, 2006
    locator: Section 8.1 (the problem ZOE), Figure 8.7 (the tree of reductions) and Section 8.3 (the reductions 3D MATCHING to ZOE, ZOE to SUBSET SUM, ZOE to ILP and ZOE to RUDRATA CYCLE)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, Plenum Press, 1972, pages 85 to 103
    locator: Section 4, problems 2 (0-1 INTEGER PROGRAMMING) and 14 (EXACT COVER), and the reductions from EXACT COVER to 3-DIMENSIONAL MATCHING and to KNAPSACK
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 3.1.2 (3-DIMENSIONAL MATCHING) and Appendix A3.1, problems SP1 (3DM) and SP2 (exact cover by 3-sets)
---

The zero-one equations problem, ZOE, gives a matrix $A$ whose entries are 0 and 1, and asks whether some vector $x$ of zeros and ones satisfies $Ax = \mathbf{1}$, the vector of all ones. Each column is a set of rows, and each equation says that exactly one chosen column covers its row, so ZOE is [exact cover](/exact-cover/) written as a matrix. Dasgupta, Papadimitriou and Vazirani use it as a hub in their chain of reductions: it comes from [3-dimensional matching](/three-dimensional-matching/), and it leads to [subset sum](/subset-sum-problem/), [integer linear programming](/binary-integer-programming/) and Rudrata (Hamiltonian) cycle. It is [NP-complete](/np-complete/), and since all its numbers are 0 and 1, it is NP-complete in the [strong sense](/strong-np-hardness/).

## In plain words

A school has several clubs, and each club has a list of members. The question is whether we can pick some of the clubs so that every student is in exactly one picked club: nobody left out, and nobody in two.

Write a table with one row per student and one column per club, with a 1 where the student is a member. Picking clubs is choosing columns, and the rule says that the chosen columns add up to exactly 1 in every row.

Checking a choice is easy. Finding one is hard in general, because matching problems that are known to be hard can be written as such tables.

## Definition

**Instance.** An $m \times n$ matrix $A$ with entries in $\{0, 1\}$.

**Question.** Is there a vector $x \in \{0, 1\}^n$ with $Ax = \mathbf{1}$, that is, $\sum_{j} a_{ij} x_j = 1$ for every row $i$?

**Encoding.** The matrix is given as its $mn$ bits, or as the list of its 1 entries. The certificate is $x$, and the verifier computes the $m$ row sums, in $O(mn)$ time on a [word RAM](/word-ram/) and in polynomial time on the [multitape Turing machine](/multitape-turing-machine/). So the problem is in NP.

**Complexity.** NP-complete under Karp (polynomial-time many-one) reductions, from 3-dimensional matching (Dasgupta, Papadimitriou and Vazirani, Section 8.3). It is the same problem as EXACT COVER, which Karp (1972) proved NP-complete from chromatic number. All numbers in an instance are 0 or 1, so it is NP-complete in the strong sense.

## Variants

- **Exact cover.** Rows are elements and columns are sets; $x$ selects sets that partition the elements. The two problems have the same instances up to this reading. See [exact cover](/exact-cover/), and [exact cover by 3-sets](/exact-cover-by-3-sets/) for the case where every column has exactly three 1s.
- **Integer linear programming.** ZOE is the special case of [0-1 integer programming](/binary-integer-programming/) with a 0-1 matrix and right side $\mathbf{1}$, and Karp's problem 2 asks whether $Cx = d$ has a 0-1 solution for any integer $C$ and $d$.
- **Inequalities.** $Ax \le \mathbf{1}$ alone is [set packing](/set-packing/), and $Ax \ge \mathbf{1}$ alone is [set cover](/set-cover/); with a bound on $\sum_j x_j$ both are NP-complete.
- **Over GF(2).** If the equations are taken modulo 2, the problem is solvable by [Gaussian elimination](/gaussian-elimination/) in polynomial time; this is [XOR-SAT](/xor-sat/). The hardness comes from the integer sum, which forbids two chosen 1s in a row.
- **Two ones per column.** If every column has at most two 1s, a column is an edge of a graph on the rows, and ZOE asks for a perfect matching (with loops for single 1s), which is in P.

## Examples

**From a 3DM instance.** Let $X = \{a_1, a_2\}$, $Y = \{b_1, b_2\}$, $Z = \{c_1, c_2\}$ and take the five triples
$$t_1 = (a_1, b_1, c_1),\ t_2 = (a_1, b_2, c_2),\ t_3 = (a_2, b_2, c_2),\ t_4 = (a_2, b_1, c_2),\ t_5 = (a_2, b_2, c_1).$$
The reduction below gives one column per triple and one row per element:

| row | $t_1$ | $t_2$ | $t_3$ | $t_4$ | $t_5$ |
|---|---|---|---|---|---|
| $a_1$ | 1 | 1 | 0 | 0 | 0 |
| $a_2$ | 0 | 0 | 1 | 1 | 1 |
| $b_1$ | 1 | 0 | 0 | 1 | 0 |
| $b_2$ | 0 | 1 | 1 | 0 | 1 |
| $c_1$ | 1 | 0 | 0 | 0 | 1 |
| $c_2$ | 0 | 1 | 1 | 1 | 0 |

A script checked all 32 vectors. The only solution is $x = (1, 0, 1, 0, 0)$, which picks $t_1$ and $t_3$, and $\{t_1, t_3\}$ is the only perfect matching. Forward, the matching $\{t_1, t_3\}$ gives $x$ with $x_1 = x_3 = 1$, and each row has one 1 among the columns $t_1, t_3$. Backward, the solution $x$ selects two triples that use every element once.

**On to subset sum.** Read each column as a number in base $n + 1 = 6$, with row $a_1$ as the lowest digit. The columns become $1333, 7993, 7998, 7818, 1518$ and the target, all digits 1, is $9331$. The script found that the only subset with sum $9331$ is $\{1333, 7998\}$, the columns $t_1$ and $t_3$.

**Why base $n + 1$.** In base 2 the columns are $21, 41, 42, 38, 26$ with target $63$, and here base 2 happens to give the right answer. But on 400 random matrices, base 2 gave a wrong answer 14 times, because digits can carry. Base $n + 1$ gave the right answer every time (183 yes-instances and 217 no-instances).

## Known algorithms

- **Brute force.** Test all $2^n$ vectors, each in $O(mn)$ time.
- **Exact cover search.** Backtracking that always branches on a row with the fewest 1s, as in Knuth's Algorithm X with dancing links, is the practical method; see [exact cover](/exact-cover/).
- **Through other problems.** Any solver for [0-1 integer programming](/binary-integer-programming/) or SAT can solve ZOE through the reductions below.

## Bounds

- **NP-completeness.** No polynomial-time algorithm exists unless P = NP.
- **Strong hardness.** Since the entries are 0 and 1, there is no pseudo-polynomial algorithm either, unless P = NP. The hardness of subset sum obtained from ZOE is only weak, because the base $n + 1$ numbers have $m$ digits.

## Reductions

All reductions here are Karp reductions.

**From 3-dimensional matching.** An instance is a set $T \subseteq X \times Y \times Z$ with $\lvert X \rvert = \lvert Y \rvert = \lvert Z \rvert = q$.

- *Map.* One variable $x_t$ per triple $t$ and one equation per element $e \in X \cup Y \cup Z$: the sum of $x_t$ over the triples $t$ that contain $e$ equals 1. The matrix is $3q \times \lvert T \rvert$.
- *Cost.* $O(q \lvert T \rvert)$ time.
- *If there is a perfect matching, then the equations have a solution.* Set $x_t = 1$ for the $q$ triples of the matching and $x_t = 0$ otherwise. Each element is in exactly one matching triple.
- *If the equations have a solution, then there is a perfect matching.* Take any solution and let $M = \{t : x_t = 1\}$. Each element is in exactly one triple of $M$. So the triples of $M$ are disjoint and cover all $3q$ elements, which means $\lvert M \rvert = q$ and $M$ is a perfect matching.

On 300 random 3DM instances with $q \le 3$, the script confirmed the equivalence (176 yes-instances and 124 no-instances).

**To subset sum.** Let $A$ be $m \times n$.

- *Map.* For each column $j$, let $a_j = \sum_{i=1}^{m} A_{ij} (n+1)^{i-1}$, and let the target be $t = \sum_{i=1}^{m} (n+1)^{i-1}$.
- *Cost.* Each number has $m$ digits in base $n + 1$, that is $O(m \log n)$ bits, so the map is polynomial.
- *If $Ax = \mathbf{1}$, then the numbers $a_j$ with $x_j = 1$ sum to $t$.* Digit $i$ of the sum is $\sum_j A_{ij} x_j = 1$, and no digit carries.
- *If some set $S$ of numbers sums to $t$, then $x = \mathbf{1}_S$ solves $Ax = \mathbf{1}$.* In base $n + 1$, digit $i$ of $\sum_{j \in S} a_j$ before carrying is $\sum_{j \in S} A_{ij} \le n$, which is a single digit. So the sum has these digits exactly, with no carry, and comparing with $t$ digit by digit gives $\sum_{j \in S} A_{ij} = 1$ for every row $i$.

**To 0-1 integer linear programming.** Write each equation as the two inequalities $\sum_j A_{ij} x_j \le 1$ and $-\sum_j A_{ij} x_j \le -1$, and add $x_j \le 1$ and $-x_j \le 0$. An integer vector satisfies these inequalities if and only if it is a 0-1 solution of $Ax = \mathbf{1}$, so both directions are immediate. See [0-1 integer programming](/binary-integer-programming/).

**To Rudrata cycle and TSP.** Dasgupta, Papadimitriou and Vazirani also reduce ZOE to Rudrata cycle, the Hamiltonian cycle problem. They first build a graph in which some pairs of edges are tied so that a cycle must use exactly one edge of each pair, and then replace each pair by a gadget with 12 vertices. From Rudrata cycle, the reduction with distances 1 and 2 gives [TSP](/traveling-salesman-decision/). The more common route to Hamiltonian cycle uses [vertex cover](/hamiltonian-cycle-np-completeness/).

**Karp's route.** Karp reduced CHROMATIC NUMBER to EXACT COVER, and EXACT COVER to 3-DIMENSIONAL MATCHING, HITTING SET, STEINER TREE and KNAPSACK. See [Karp's reduction tree](/karp-21-np-complete/).

## Applications

- **A hub for reductions.** ZOE turns a matching or covering structure into arithmetic, which makes it a convenient middle step to number problems such as subset sum, [knapsack](/knapsack-decision/) and integer programming.
- **Exact cover puzzles.** Tiling puzzles, Sudoku and the placement of polyominoes are often solved by writing them as exact cover, that is, as ZOE.
- **Integer programming.** The NP-hardness of 0-1 integer programming, even with 0-1 coefficients and right side 1, comes from ZOE.

## References
