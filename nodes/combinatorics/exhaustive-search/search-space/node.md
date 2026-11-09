---
tag: 2AFFB3
kind: concept
slug: search-space
name: Search space
aliases:
- solution space
- state space
- candidate space
area: combinatorics/exhaustive-search
level: intro
summary: The set of all candidate solutions that an exhaustive method must consider.
prereqs: [asymptotic-notation]
see_also: [brute-force-search, generate-and-test, combinatorial-explosion, state-space-tree, search-tree-pruning, symmetry-breaking, n-queens-problem, state-space]
sources:
  - book: isbn:9780201038064
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4B, Combinatorial Algorithms, Part 2
    locator: Section 7.2.2, Backtrack programming (the domains of the variables, the n queens example and the estimate of the size of a search tree)
  - book: isbn:9780849339882
    title: Donald L. Kreher and Douglas R. Stinson, Combinatorial Algorithms, Generation, Enumeration, and Search, CRC Press, 1999
    locator: Chapter 4, Backtracking algorithms (the state space tree and the pruning of the space)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Solving problems by searching (states, the state space and the search tree)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, 1979
    locator: Chapter 1 (polynomial time algorithms, intractable problems and the growth of exponential time functions)
---

The search space of a problem is the set of candidates that a method examines to find a solution: all the objects that could be answers before any test is applied. An [exhaustive method](/brute-force-search/) is correct only if its search space holds every solution, or at least one optimal solution, and its cost is roughly the size of that space times the cost to test one candidate. The same problem has many possible search spaces, and the choice of the space is often the most important design decision of an exhaustive search.

## In plain words

Before you can search for an answer, you must say where you look. The search space is the list of all the things that you are ready to try. For a lock with three dials, it is every setting of the three dials. For a seating plan, it is every order of the guests.

A good search space has two properties. First, it must contain the answer, or the search can fail. Second, it must be as small as possible, because the search takes time for each thing in it. The same puzzle can be described in a loose way, with many useless candidates, or in a tight way, where the rules of the puzzle already remove most bad candidates. A tight description can be millions of times smaller.

## The idea

**Definition.** Fix a problem instance $I$. A *search space* for $I$ is a finite set $S$ together with a way to list its members and a test or a cost for each member:

- for a search problem, a predicate $P : S \to \{\text{true}, \text{false}\}$, and the task is to find (or list) the members $x \in S$ with $P(x)$;
- for an optimization problem, a cost $c : S \to \mathbb{R} \cup \{+\infty\}$, and the task is to find $x \in S$ with the least $c(x)$.

The space is *complete* for the task when it loses nothing: for listing, $S$ contains every solution of $I$; for finding one solution, $S$ contains a solution whenever $I$ has one; for optimization, $S$ contains an optimal solution. Completeness is the condition of correctness of [brute-force search](/brute-force-search/) and of [generate and test](/generate-and-test/) over $S$.

**Size and cost.** If one member of $S$ costs time $t$ to produce and test, the plain exhaustive method takes $\Theta(|S| \cdot t)$ time in the worst case. So a smaller complete space is a faster method. Three common ways to shrink a space:

1. **Encode the constraints in the representation.** Choose a representation in which many constraints hold by construction, so that candidates that break them do not exist in $S$.
2. **Remove symmetric copies.** If a group of symmetries maps solutions to solutions, keep one candidate from each orbit, or one canonical form. This is [symmetry breaking](/symmetry-breaking/).
3. **Remove dominated candidates.** In an optimization problem, drop a candidate when another candidate is at least as good in every case. The space stays complete for the optimum but not for the list of all solutions.

**Spaces of partial solutions.** A candidate is often a sequence of decisions $x_1 \ldots x_n$ with $x_k \in D_k$. Then the prefixes of the candidates form a tree, the [state space tree](/state-space-tree/), with $\sum_{k=0}^{n} \prod_{j \le k} |D_j|$ nodes. A [backtracking](/generic-backtracking-algorithm/) search walks this tree and cuts a subtree when a prefix cannot be extended to a solution. The space that it really examines is the set of prefixes that pass the tests, and this set can be far smaller than the set of complete candidates. In artificial intelligence the word [state space](/state-space/) means a related object: a graph of states with moves between them, searched for a path from a start state to a goal state.

**Implicit spaces.** In nearly all useful cases, $S$ is never stored. It is defined by a rule and listed one member at a time, with [combinatorial generation](/combinatorial-generation/) methods such as the [power set enumeration](/power-set-enumeration/) of all subsets or [the generation of all permutations](/generating-all-permutations/). The size of $S$ is still the right measure of the work, because each member is produced once.

## Examples

**The eight queens.** Place 8 queens on a chessboard so that no two attack each other. Three complete spaces for this problem:

| candidates | size of the space |
|---|---|
| any 8 of the 64 squares | $\binom{64}{8} = 4{,}426{,}165{,}368$ |
| one queen in each row, any column | $8^8 = 16{,}777{,}216$ |
| one queen in each row and each column (a permutation) | $8! = 40{,}320$ |

All three contain all 92 solutions, because a solution has exactly one queen in each row and in each column. The third space is more than $10^5$ times smaller than the first. The [n-queens problem](/n-queens-problem/) page gives the backtracking search, which examines only 2,057 prefixes that pass its tests for $n = 8$.

**Subsets.** For [subset sum](/subset-sum-problem/) on $n$ numbers, the natural space is the set of all $2^n$ subsets. For $n = 40$ it has $2^{40} = 1{,}099{,}511{,}627{,}776$ members. The [Horowitz and Sahni](/horowitz-sahni-algorithm/) method splits the numbers into two halves and searches two spaces of $2^{20} = 1{,}048{,}576$ subsets each, then joins them. The space is the same, but the method does not list it member by member.

**Tours.** For the [traveling salesman problem](/traveling-salesman-problem/) on $n \ge 3$ cities, a tour is a cyclic order of the cities. Fix the start city and identify a tour with its reverse: there are $(n-1)!/2$ distinct tours. For $n = 10$ this is $181{,}440$. A space of all $n!$ orders is also complete, but it holds each tour $2n$ times.

**Assignments.** For [graph coloring](/graph-coloring/) with $k$ colors on $n$ vertices, the space of all color assignments has $k^n$ members. Since a permutation of the colors maps a proper coloring to a proper coloring, it is enough to keep the assignments in which the colors appear for the first time in the order $1, 2, \ldots$; this is a complete space for the question "is there a $k$-coloring?". For [SAT](/sat/) on $n$ variables, the space is the set of $2^n$ truth assignments.

**A non-example.** For the eight queens, the space "one queen in each row, all in columns 1 to 4" is small, but it is not complete: it contains none of the 92 solutions, since a solution uses all 8 columns. A search over it is fast and wrong.

## Where it is used

- **Design of exhaustive algorithms.** [Brute-force search](/brute-force-search/), [generate and test](/generate-and-test/), [backtracking](/generic-backtracking-algorithm/) and [branch and bound](/depth-first-branch-and-bound/) all start from a search space. Their correctness depends on its completeness, and their cost on its size.
- **Complexity theory.** A problem in [NP](/np/) has, for each instance, a search space of certificates of polynomial length, so of size $2^{\mathrm{poly}(n)}$. The [combinatorial explosion](/combinatorial-explosion/) of this space is why exhaustive search is not a polynomial-time method.
- **Estimation.** Knuth's random-path estimate in Section 7.2.2 of *The Art of Computer Programming* predicts the size of a backtrack tree before a long run.
- **Exact exponential algorithms.** The field of [exact exponential algorithms](/exact-exponential-algorithms/) studies how far below the size of the natural space a correct method can go.

## References
