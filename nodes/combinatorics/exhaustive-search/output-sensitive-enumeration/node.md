---
tag: NZT4MF
kind: concept
slug: output-sensitive-enumeration
name: Output-sensitive enumeration
aliases:
- output-sensitive algorithm
- output-sensitive generation
- polynomial-delay enumeration
area: combinatorics/exhaustive-search
level: advanced
summary: Enumeration whose running time is measured in terms of the number of outputs as well as the input size.
prereqs: [enumeration-problem, polynomial-time, amortized-cost]
see_also: [enumeration-problem, reverse-search, tsukiyama-algorithm, fredman-khachiyan-algorithm, maximal-independent-set-enumeration, constant-amortized-time-generation, output-sensitive-generation, kirkpatrick-seidel]
sources:
  - paper: doi:10.1016/0020-0190(88)90065-8
    title: David S. Johnson, Mihalis Yannakakis and Christos H. Papadimitriou, On generating all maximal independent sets, Information Processing Letters 27(3), 1988, 119 to 123
    locator: the definitions of polynomial total time, incremental polynomial time and polynomial delay, and maximal independent sets with polynomial delay in lexicographic order
  - paper: "Yann Strozecki, Enumeration complexity, Bulletin of the EATCS 129, 2019"
    locator: the classes of enumeration problems (output polynomial, incremental polynomial, polynomial delay) and their relations
  - paper: doi:10.1137/0206036
    title: Shuji Tsukiyama, Mikio Ide, Hiromu Ariyoshi and Isao Shirakawa, A new algorithm for generating all the maximal independent sets, SIAM Journal on Computing 6(3), 1977, 505 to 517
    locator: the bound O(nmμ) on the total time for μ maximal independent sets, with O(n + m) space
  - paper: doi:10.1006/jagm.1996.0062
    title: Michael L. Fredman and Leonid Khachiyan, On the complexity of dualization of monotone disjunctive normal forms, Journal of Algorithms 21(3), 1996, 618 to 628
    locator: the incremental quasi-polynomial bound for the duality of monotone forms, and so for the enumeration of minimal transversals
  - paper: "David G. Kirkpatrick and Raimund Seidel, The ultimate planar convex hull algorithm?, SIAM Journal on Computing 15(1), 1986, 287 to 299"
    locator: the convex hull of n points with h hull vertices in O(n log h) time, and the matching lower bound
---

An algorithm is *output-sensitive* when its running time is bounded in terms of the size of its output as well as the size of its input. For an [enumeration problem](/enumeration-problem/), which asks for all solutions of an instance, this is the natural measure: the number of solutions can be exponential in the input, so a bound in the input alone says little, and the useful question is how much work the algorithm does for each solution. The standard measures are polynomial total time, incremental polynomial time and polynomial delay, defined by Johnson, Yannakakis and Papadimitriou in 1988.

## In plain words

Some questions have a few answers and some have millions. If a program must print every answer, then a question with millions of answers must take a long time, and that is not the fault of the program. A fair way to judge such a program is to ask how much time it needs for each answer that it prints.

A good program prints the answers at a steady pace: it never waits a very long time between two answers. A weaker program may be slow between answers but still finishes in time that is reasonable for the number of answers. A bad program may spend most of its time exploring choices that lead to no answer at all.

## The idea

Fix an enumeration problem: an instance $x$ of size $n$ has a set $R(x)$ of solutions, of size $N = |R(x)|$. An algorithm prints the solutions without repeats. The classes, from weakest to strongest:

- **Polynomial total time (output polynomial).** The whole run takes time polynomial in $n$ and $N$.
- **Incremental polynomial time.** For each $i \le N$, the $i$-th solution is printed after time polynomial in $n$ and $i$, and the end of the run comes after time polynomial in $n$ and $N$. Equivalently, given $x$ and some of its solutions, the algorithm finds one more or reports that there are no more in time polynomial in $n$ and the number of solutions given.
- **Polynomial delay.** The time before the first solution, between any two consecutive solutions, and after the last one is bounded by a polynomial in $n$ alone.

Polynomial delay implies incremental polynomial time, which implies polynomial total time. Finer measures are also used:

- **Amortized time per solution.** The total time divided by $N$. In [combinatorial generation](/combinatorial-generation/), an algorithm with $O(1)$ amortized time per object is called [constant amortized time](/constant-amortized-time-generation/).
- **Worst-case delay of $O(1)$.** Each step from one object to the next takes constant time. This is [loopless generation](/loopless-generation/), and it is usually stated for objects that are changed in place, such as the swaps of [Heap's algorithm](/heaps-algorithm/).
- **Space.** The best methods use space polynomial in $n$, independent of $N$. A method that stores all solutions found so far, to avoid repeats, can need space proportional to $N$.

**Why backtracking alone is not enough.** A [backtracking](/generic-backtracking-algorithm/) search prints a solution at some leaves of its search tree and wastes time in subtrees with no solution. Its delay is bounded only when every node of the tree lies above some solution. The *flashlight* or *extension* method ensures this: before going into a branch, it decides whether the current partial solution extends to a full one, and it enters the branch only if the answer is yes. If that extension question is solvable in polynomial time and the tree has polynomial depth, the result has polynomial delay. Conversely, if the decision problem "is $R(x)$ empty?" is NP-hard, then no algorithm runs in polynomial total time unless $\mathrm{P} = \mathrm{NP}$, because a run cut off after the polynomial bound for $N = 0$ decides emptiness.

**Other designs.** Besides the flashlight method, the main tools are:

- *Parent-child trees.* Give each solution except a root a unique parent that is also a solution, computable in polynomial time. The solutions form a tree, and a depth-first walk of it needs no memory of what was seen. This is [reverse search](/reverse-search/), and [Tsukiyama's algorithm](/tsukiyama-algorithm/) for maximal independent sets has this form.
- *Supergraph of solutions.* Define a graph on the solutions in which each solution has polynomially many neighbors, all computable in polynomial time, and the graph is connected. A search of this graph gives incremental polynomial time, and with a lexicographic order and a priority queue, Johnson, Yannakakis and Papadimitriou obtain polynomial delay for maximal independent sets, at the cost of space.
- *Duality.* For [minimal transversals](/minimal-transversal-enumeration/) of a hypergraph, the step "find one more" is the problem of testing whether two monotone Boolean functions are dual. The [Fredman-Khachiyan algorithm](/fredman-khachiyan-algorithm/) solves it in quasi-polynomial time, which gives incremental quasi-polynomial time.

## Examples

**Paths in a directed acyclic graph.** List all paths from $s$ to $t$ in a DAG with $n$ vertices and $m$ edges. A plain depth-first search can explore long branches that never reach $t$. First delete every vertex from which $t$ cannot be reached, in $O(n + m)$ time. Then every branch of the depth-first search ends at $t$, every path has at most $n$ vertices, and the delay between two outputs is $O(n + m)$. With $N$ paths, the total time is $O((n + m) N)$ after the first step.

**Simple cycles and simple paths.** In a general directed graph the pruning test above is not enough, because a vertex can reach $t$ only through vertices that are already on the path. [Johnson's algorithm](/johnson-elementary-cycles-algorithm/) for elementary cycles uses blocking sets and runs in $O((n + m)(c + 1))$ time for $c$ cycles, and the [Read-Tarjan method](/read-tarjan-path-enumeration/) lists simple paths with $O(n + m)$ time per path.

**Maximal independent sets.** The sets of a graph with $n$ vertices and $m$ edges can number $3^{n/3}$. [Tsukiyama's algorithm](/tsukiyama-algorithm/) lists all $\mu$ of them in $O(n (n + m) \mu)$ total time and $O(n + m)$ space, with polynomial delay. In lexicographic order, Johnson, Yannakakis and Papadimitriou also give polynomial delay, but they show that no algorithm lists them in reverse lexicographic order with polynomial delay unless $\mathrm{P} = \mathrm{NP}$. So the order of the output can change the complexity. See [maximal independent set enumeration](/maximal-independent-set-enumeration/).

**Minimal transversals.** Whether the minimal transversals of a hypergraph can be listed in polynomial total time is a well-known open problem. The best known bound is incremental quasi-polynomial, from Fredman and Khachiyan.

**Convex hulls.** The phrase *output-sensitive* is also used in geometry. The [Kirkpatrick-Seidel algorithm](/kirkpatrick-seidel/) finds the [convex hull](/convex-hull/) of $n$ points in the plane in $O(n \log h)$ time, where $h$ is the number of hull vertices, and this is optimal in terms of $n$ and $h$. [Chan's algorithm](/chan-algorithm/) reaches the same bound more simply.

**Exact cover.** Deciding whether an [exact cover](/exact-cover/) exists is NP-complete, so listing all exact covers in polynomial total time would give $\mathrm{P} = \mathrm{NP}$. A search such as [Algorithm X](/algorithm-x/) has no polynomial bound on its delay.

## Where it is used

- **Graph algorithms.** Listing [spanning trees](/spanning-tree-enumeration/), [simple paths](/enumerating-simple-paths/), [cycles](/enumerating-elementary-cycles/), [maximal cliques](/maximal-clique-enumeration/) and maximal independent sets.
- **Data mining.** Listing frequent and closed item sets, where the number of outputs can be large and the input is a database.
- **Databases.** Query answering with bounded delay, where the answers of a join are printed one at a time.
- **Logic and AI.** Listing models of formulas, prime implicants, minimal hitting sets for diagnosis, and the dualization of monotone Boolean functions.
- **Polyhedral computation.** [Vertex enumeration](/vertex-enumeration/) of polytopes, where [reverse search](/reverse-search/) gives bounds per vertex.
- **Combinatorial generation.** Lists of permutations, subsets, partitions and trees, where the stronger goals are constant amortized time and loopless generation.

## References
