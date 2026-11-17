---
tag: E5TT1K
kind: algorithm
slug: elementary-flux-mode-enumeration
name: Elementary flux mode enumeration
aliases:
- double description method for elementary modes
area: biology/systems-biology
level: advanced
summary: "List all elementary flux modes of a network by the double description method, as the extreme rays of the flux cone after each reversible reaction is split."
model: real-ram
complexity:
  vars: {m: the number of reactions after splitting, d: the dimension of the kernel of the split matrix, R: the largest number of rays kept after a step}
  time: {worst: O(m^2 d^2 R^2), per_step: O(m d^2 R^2)}
  space: {extra: O(m R)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1994
  people: [Stefan Schuster, Claus Hilgetag]
  note: Schuster and Hilgetag defined elementary flux modes and gave an algorithm that builds them by combining pairs of vectors, one constraint at a time, which is a form of the double description method.
prereqs: [elementary-flux-mode]
see_also: [fourier-motzkin-elimination, vertex-enumeration, extreme-point, nullspace-computation, output-sensitive-enumeration, counting-problem, flux-balance-analysis, matroid]
sources:
  - paper: doi:10.1142/S0218339094000131
    title: Stefan Schuster and Claus Hilgetag, On elementary flux modes in biochemical reaction systems at steady state, Journal of Biological Systems 2(2), 1994, 165-182
    locator: the definition of elementary flux modes and the first algorithm that combines pairs of vectors to cancel one coordinate at a time
  - paper: doi:10.1038/73786
    title: Stefan Schuster, David A. Fell and Thomas Dandekar, A general definition of metabolic pathways useful for systematic organization and analysis of complex metabolic networks, Nature Biotechnology 18(3), 2000, 326-332
    locator: the use of elementary modes as metabolic pathways, with the computation of modes for example networks
  - paper: doi:10.1021/jp034523f
    title: Clemens Wagner, Nullspace approach to determine the elementary modes of chemical reaction systems, Journal of Physical Chemistry B 108(7), 2004, 2425-2431
    locator: the start of the iteration from a kernel basis of the stoichiometric matrix
  - paper: doi:10.1186/1471-2105-5-175
    title: Julien Gagneur and Steffen Klamt, Computation of elementary modes, a unifying framework and the new binary approach, BMC Bioinformatics 5, 2004, 175
    locator: the description of the known algorithms as the double description method, the splitting of reversible reactions, the adjacency tests, and the binary approach
  - paper: doi:10.1007/3-540-61576-8_77
    title: Komei Fukuda and Alain Prodon, Double description method revisited, Combinatorics and Computer Science, Lecture Notes in Computer Science 1120, 1996, 91-111
    locator: the double description step, the adjacency test by tight constraints, and the effect of the order in which constraints are added
  - paper: doi:10.1016/j.biosystems.2008.06.015
    title: Vicente Acuña, Flavio Chierichetti, Vincent Lacroix, Alberto Marchetti-Spaccamela, Marie-France Sagot and Leen Stougie, Modes and cuts in metabolic networks, complexity and algorithms, BioSystems 95(1), 2009, 51-60
    locator: Section 3.2 (counting elementary modes is #P-complete), and the discussion of enumeration with polynomial delay for networks with only reversible reactions
---

Elementary flux mode enumeration lists every [elementary flux mode](/elementary-flux-mode/) of a metabolic network: every minimal set of reactions that can carry a steady flux in the allowed directions. The standard method is the double description method, applied to the flux cone. First each reversible reaction is split into a forward and a backward irreversible copy, so that the modes become the extreme rays of a pointed cone. The method starts from a kernel basis of the stoichiometric matrix and adds the sign constraints one by one. At each step it keeps the rays that satisfy the new constraint and joins each adjacent pair of rays with opposite signs into a new ray. The output can be exponential in the size of the network, and counting the modes is #P-complete, so no method is fast on all networks. On networks of moderate size the method is practical, and it is the core of the standard tools.

## In plain words

A metabolic network can usually run in many ways. Some of these ways are as small as possible: if you remove any one reaction from them, they stop working. These smallest routes are called elementary flux modes. Every way the network can run is a mix of them, so a list of all of them describes the whole network.

The method builds the list step by step. It starts with a few simple routes that balance every metabolite but may run some reactions the wrong way. Then it fixes one reaction at a time. Routes that run that reaction the right way are kept. Pairs of routes that run it in opposite directions are added together so that the reaction cancels, but only for pairs that are close neighbours. At the end, every route left is a correct smallest route, and none is missing.

## The problem

**Input.** An $n \times m_0$ stoichiometric matrix $S$ with rational entries and the set of reversible reactions.

**Output.** All elementary flux modes of the flux cone $C = \{v : S v = 0, \; v_j \ge 0 \text{ for irreversible } j\}$, that is, the non-zero vectors of $C$ whose support is minimal. Each mode is given once, as the vector of coprime integers in its ray. A mode made only of reversible reactions and its negative are two different modes.

## The algorithm

```pseudo id=main
EFM-ENUMERATION(S, rev)
L1  S' ← S with a column -S_j added for each reversible j; record which column came from which reaction
L2  compute the reduced row echelon form of S', with pivot columns Π and free columns F,
    and the kernel basis that is the identity on F; let K be the matrix of this basis and d = |F|
L3  rays ← the d basis vectors; done ← F
L4  for each pivot column p in Π:
L5      split rays into pos (x_p > 0), zero (x_p = 0) and neg (x_p < 0)
L6      new ← empty list
L7      for each x in pos and each y in neg:
L8          if the rows K_i with i in done, x_i = 0 and y_i = 0 have rank d - 2:
                append x_p y - y_p x to new
L9      rays ← pos + zero + new; add p to done
L10 drop the rays whose support is the two copies of one reaction, and map each other ray back to the original reactions
L11 return the modes, each scaled to coprime integers, sorted
```

Every stored vector lies in the kernel of $S'$, and its coordinate $x_i$ is the value of the constraint $x_i \ge 0$, so the zero set of a ray is its set of tight constraints. In the kernel basis of line L2 the free coordinates are the identity, so the starting cone, the part of the kernel with $x_F \ge 0$, is a simplicial cone whose extreme rays are the basis vectors. The rank test of line L8 is the adjacency test of the double description method. The code first skips pairs with fewer than $d - 2$ common zeros, which cannot pass the test. The new ray $x_p y - y_p x$ is a positive combination of $x$ and $y$ (since $x_p > 0 > y_p$), and its coordinate $p$ is zero. The code works with exact fractions.

## Example

Take network E of the [definition page](/elementary-flux-mode/), with metabolites $A$, $B$, $C$ and reactions R1 ($\to A$), R2 ($A \to B$), R3 ($A \leftrightarrow C$, reversible), R4 ($B \to C$), R5 ($C \to$) and R6 ($B \to$). Line L1 adds the column R3b, the backward copy of R3, so $S'$ has seven columns in the order R1, ..., R6, R3b. The pivot columns are R1, R2, R3 and the free columns are R4, R5, R6, R3b, so $d = 4$. The kernel basis, written as $(x_1, \ldots, x_6, x_{3b})$, is:

| ray | R1 | R2 | R3 | R4 | R5 | R6 | R3b |
|---|---|---|---|---|---|---|---|
| $b_1$ | 0 | 1 | -1 | 1 | 0 | 0 | 0 |
| $b_2$ | 1 | 0 | 1 | 0 | 1 | 0 | 0 |
| $b_3$ | 1 | 1 | 0 | 0 | 0 | 1 | 0 |
| $b_4$ | 0 | 0 | 1 | 0 | 0 | 0 | 1 |

The constraints for R1 and R2 change nothing, because no ray is negative there. For R3, $b_1$ is negative, $b_2$ and $b_4$ are positive, and $b_3$ is zero. The pair $(b_2, b_1)$ has the common zeros R6 and R3b among the processed constraints, and these two rows of $K$ have rank $2 = d - 2$, so the pair is adjacent. It gives $b_1 + b_2 = (1, 1, 0, 1, 1, 0, 0)$, the route R1, R2, R4, R5. The pair $(b_4, b_1)$ has the common zeros R1, R5, R6, also of rank 2, and gives $b_1 + b_4 = (0, 1, 0, 1, 0, 0, 1)$, the cycle R2, R4, R3b. The list now has five rays. Line L10 drops $b_4$, which runs R3 forward and backward, and maps R3b back to R3 with a minus sign. The result is the four modes of the definition page: $(1, 1, 0, 0, 0, 1)$, $(1, 0, 1, 0, 1, 0)$, $(1, 1, 0, 1, 1, 0)$ and the cycle $(0, 1, -1, 1, 0, 0)$.

On network N of the [FBA page](/flux-balance-analysis/) the code finds the three modes for growth by RESP1, by RESP2 and by fermentation. On a chain of $k$ diamonds, with $2k + 2$ reactions, it finds $2^k$ modes. The tests check these cases, a cycle of three reversible reactions (two modes, one in each direction), and 60 random networks against a brute force search over all supports.

## Correctness

The proof has three parts. Splitting is a bijection between the modes of the original network and the modes of the split network that are not two-cycles. In the split network every reaction is irreversible, so the cone is pointed and its extreme rays are exactly its modes, by the rank test for modes. The double description step is correct: when a constraint $h t \ge 0$ is added to a pointed cone, the extreme rays of the new cone are the old extreme rays with $h t \ge 0$, together with one new ray for each adjacent pair with opposite signs, and no ray appears twice. Adjacency means that the common tight constraints have rank $d - 2$, so the two rays span a two-dimensional face. By induction over the pivots, the final list holds each extreme ray of the split cone once. Both are theorems, and the full proof is below.

## Complexity

- **Output size.** The number of modes can be exponential in the size of the network: the chain of $k$ diamonds has $2k + 2$ reactions and $2^k$ modes. So no algorithm lists the modes in time polynomial in the input alone. This is a theorem.
- **Counting.** Counting the modes is #P-complete (Acuña and co-authors 2009, Section 3.2), by a reduction from counting perfect matchings of a bipartite graph. So even the number of modes is hard to compute. This is a theorem.
- **Polynomial delay.** If every reaction is reversible, the supports of the modes are the circuits of a linear [matroid](/matroid/), and they can be listed with polynomial delay. Acuña and co-authors (2009) note that the question is open for networks with irreversible reactions. This is a theorem for the reversible case.
- **Cost of this method.** Each of the at most $m$ steps tests at most $R^2$ pairs, and each rank test is a Gaussian elimination on at most $m$ rows with $d$ columns, which costs $O(m d^2)$ operations. So the time is $O(m^2 d^2 R^2)$ arithmetic operations, where $R$ is the largest list of rays after a step, and the space is $O(m R)$. This is a theorem.
- **Intermediate lists.** $R$ is at least the number of modes and can be much larger, because the cones of the middle steps can have more extreme rays than the final cone. How large it gets depends on the order of the pivots, and Fukuda and Prodon (1996) discuss orders for the double description method in general. This is a heuristic: no order is known to be good on all inputs.
- **Exact arithmetic.** With fractions, the entries can grow during the run. Scaling each new ray to coprime integers keeps them small in practice, which is a heuristic.

## Properties

- **Exact and complete.** With exact arithmetic the method returns every mode once and nothing else.
- **Not output sensitive.** The work depends on the intermediate lists, not only on the output.
- **Deterministic.** The set of modes does not depend on the order of the pivots, though the work does.
- **Generates the cone.** The modes generate the flux cone by non-negative combinations with matching signs. The tests check that a random steady-state vector is a non-negative combination of the modes.
- **Splitting doubles some work.** Each reversible reaction adds one column and one two-cycle to the split cone, and the two-cycle is removed at the end.

## Variants and improvements

- **The original tableau method.** Schuster and Hilgetag (1994) started from a tableau of the transposed stoichiometric matrix with an identity block and cancelled one metabolite at a time. It is also a double description method, with a different start.
- **The nullspace approach.** Wagner (2004) started from a kernel basis, as this page does, so that only the sign constraints of reactions remain. The number of steps is then the rank of the matrix, which is at most the number of metabolites.
- **Combinatorial adjacency.** Instead of the rank test, two rays are adjacent if no third ray is zero on all their common zeros. This test needs only the zero sets, and it can be stored as bit vectors. Gagneur and Klamt (2004) compare the two tests and describe the binary approach, which stores the zero sets as bit vectors to save memory.
- **Reversible reactions without splitting.** Many tools treat reversible reactions directly: they process the irreversible constraints and handle the lineality space of the cone separately. This avoids the extra columns.
- **Partial lists.** When the full list is too large, a [mixed-integer program](/mixed-integer-programming/) can find modes one at a time, for example the shortest modes or the modes that use a given reaction. Finding one mode is polynomial, but finding a shortest one is NP-hard (Acuña and co-authors 2009).
- **Related enumerations.** [Vertex enumeration](/vertex-enumeration/) of polytopes and [Fourier-Motzkin elimination](/fourier-motzkin-elimination/) use the same pairing step.

## When to use it

Use it to list all routes of a small or medium network, such as central carbon metabolism, to find the routes with the best yield, the reactions that every route needs, or the minimal cut sets. For a genome-scale model the list is usually far too large, and [flux balance analysis](/flux-balance-analysis/) or flux variability analysis answer most questions with linear programs. If you need only some modes, compute them one at a time instead.

## Pitfalls

- **Forgetting the two-cycles.** After splitting, each reversible reaction gives a two-cycle that is an extreme ray of the split cone but not a mode. It must be removed.
- **Exchange reactions.** Whether exchange reactions are in $S$ changes the answer. Without them, only internal cycles are modes.
- **Floating point.** The rank test with a tolerance can give wrong adjacency on large networks. Exact or integer arithmetic avoids this at a cost.
- **Memory.** The intermediate lists, not the output, usually decide whether the run finishes.
- **Reading modes as fluxes.** A mode is a direction, not a flux that the cell uses. Real flux vectors are combinations of many modes.

## Implementations

## History

Schuster and Hilgetag (1994) defined elementary flux modes and gave the first algorithm, which combines pairs of rows of a tableau to cancel one coordinate at a time. Schuster, Fell and Dandekar (2000) made modes a general definition of a metabolic pathway and computed them for example networks. In 2004 Wagner started the iteration from a kernel basis, and Gagneur and Klamt showed that the known algorithms are forms of the double description method, which comes from the study of polyhedral cones in the 1950s. Acuña and co-authors (2009) proved that counting the modes is #P-complete.

## References
