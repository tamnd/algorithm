---
tag: V5RPFP
kind: definition
slug: enumeration-problem
name: Enumeration problem
aliases:
- listing problem
- generation problem
area: combinatorics/exhaustive-search
level: core
summary: The task of listing every object satisfying a property, rather than counting or finding one.
prereqs: [search-problem, polynomial-time]
see_also: [output-sensitive-enumeration, counting-problem, search-problem, decision-problem, combinatorial-generation, maximal-independent-set-enumeration, minimal-transversal-enumeration, reverse-search]
sources:
  - paper: doi:10.1016/0020-0190(88)90065-8
    title: David S. Johnson, Mihalis Yannakakis and Christos H. Papadimitriou, On generating all maximal independent sets, Information Processing Letters 27(3), 1988, 119 to 123
    locator: the definitions of polynomial total time, incremental polynomial time and polynomial delay
  - paper: "Yann Strozecki, Enumeration complexity, Bulletin of the EATCS 129 (2019)"
    locator: the definition of enumeration problems, the class EnumP and the classes of tractable enumeration
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.2.1, Generating basic combinatorial patterns (the visit of each object of a family)
  - book: "Frank Ruskey, Combinatorial Generation, unpublished book draft, University of Victoria, 2003"
    locator: Chapter 1 (listing, ranking and the cost measures of generation algorithms)
---

An enumeration problem asks, for each input, for the list of all its solutions, each exactly once. It is the third task on a set of solutions, beside the [search problem](/search-problem/) (find one solution) and the [counting problem](/counting-problem/) (find how many there are). Since the list can be exponentially longer than the input, the cost of an enumeration algorithm is measured against the size of the input and the number of solutions together, as in [output-sensitive enumeration](/output-sensitive-enumeration/).

## Definition

Let $\Sigma$ be a finite alphabet and let $R \subseteq \Sigma^* \times \Sigma^*$ be a binary relation. For an input $x$, write $R(x) = \{ y : (x, y) \in R \}$ for its set of *solutions*. Assume that $R(x)$ is finite for each $x$.

**Definition.** The *enumeration problem* of $R$, written $\textsc{Enum}\cdot R$, is this task: given $x$, output the elements of $R(x)$, each exactly once and in any order, and then halt.

An algorithm *solves* $\textsc{Enum}\cdot R$ when, for each input $x$, the sequence $y_1, \ldots, y_N$ that it outputs before it halts satisfies $\{y_1, \ldots, y_N\} = R(x)$ and $y_i \ne y_j$ for $i \ne j$. So $N = |R(x)|$. An *ordered* enumeration problem also fixes the order of the output, for example lexicographic order.

The usual complexity theory adds two conditions, which define the class **EnumP**: $R$ is *polynomially balanced*, so $|y| \le p(|x|)$ for a polynomial $p$ and each $y \in R(x)$, and the test "$(x, y) \in R$?" runs in polynomial time. These are the conditions of [NP](/np/) witnesses, so each problem of NP has a natural enumeration problem: list all witnesses.

**Cost measures.** For an algorithm $A$ and an input $x$ with $N = |R(x)|$, let $t_i(x)$ be the time at which $A$ outputs $y_i$, and let $t_{N+1}(x)$ be the time at which $A$ halts; set $t_0 = 0$.

- The *total time* is $t_{N+1}(x)$.
- The *delay* is $\max_{0 \le i \le N} (t_{i+1}(x) - t_i(x))$: the longest wait before the first output, between two outputs, or after the last.
- The *space* is the largest memory in use, not counting the output.

[Output-sensitive enumeration](/output-sensitive-enumeration/) defines the classes of tractable enumeration from these measures: polynomial total time, incremental polynomial time and polynomial delay (Johnson, Yannakakis and Papadimitriou, 1988).

**Proposition.** If $\textsc{Enum}\cdot R$ has an algorithm with total time at most $p(|x|, |R(x)|)$ for a polynomial $p$, then the decision problem "is $R(x) \ne \emptyset$?" is in polynomial time.

*Proof.* Given $x$, run the algorithm for $p(|x|, 0) + 1$ steps. If $R(x) = \emptyset$, the algorithm halts within $p(|x|, 0)$ steps with no output. So if within these steps the algorithm outputs a solution or does not halt, then $R(x) \ne \emptyset$; if it halts with no output, $R(x) = \emptyset$. The time is $p(|x|, 0) + 1$ steps plus the cost of the simulation, which is polynomial in $|x|$. $\square$

So an enumeration problem whose decision version is NP-complete, such as listing all satisfying assignments of a CNF formula, has no algorithm of polynomial total time unless $\mathrm{P} = \mathrm{NP}$.

## Examples and non-examples

**Examples.**

- **All subsets of $[n]$.** Input $n$, solutions the $2^n$ subsets. Here $R(x)$ is exponential in $|x|$ but a [Gray code](/gray-code/) lists it with $O(1)$ delay. Most problems of [combinatorial generation](/combinatorial-generation/) have this form: the input is a size, and the solutions are all objects of a family.
- **All maximal independent sets of a graph.** See [maximal independent set enumeration](/maximal-independent-set-enumeration/). The number of solutions ranges from 1 to $3^{n/3}$, and the [Tsukiyama algorithm](/tsukiyama-algorithm/) lists them with polynomial delay.
- **All minimal transversals of a hypergraph.** See [minimal transversal enumeration](/minimal-transversal-enumeration/). It is open whether this problem has an algorithm of polynomial total time; the [Fredman-Khachiyan algorithm](/fredman-khachiyan-algorithm/) gives quasi-polynomial total time.
- **All simple paths between two vertices.** See [enumerating simple paths](/enumerating-simple-paths/). Backtracking with a reachability test gives polynomial delay.
- **All solutions of an exact cover instance.** See [exact cover](/exact-cover/). Since the decision version is NP-complete, the proposition shows that no algorithm has polynomial total time unless $\mathrm{P} = \mathrm{NP}$.
- **All maximal independent sets in reverse lexicographic order.** An ordered enumeration problem. Johnson, Yannakakis and Papadimitriou showed that it has no polynomial-delay algorithm unless $\mathrm{P} = \mathrm{NP}$, although the same sets in lexicographic order have one.

**Non-examples.**

- **Count the perfect matchings of a graph.** The output is one number, $|R(x)|$. This is a [counting problem](/counting-problem/), and it can be much faster than listing, or much harder than deciding, depending on the problem.
- **Find one Hamiltonian cycle.** The output is one element of $R(x)$. This is a [search problem](/search-problem/).
- **List all prime numbers.** The set of solutions is infinite, so no algorithm halts after the last one. This is a computably enumerable set, a notion of computability theory, not an enumeration problem in the sense above.
- **List all subsets of $[n]$ with their sums, with repeats allowed.** An algorithm that outputs some solution twice does not solve an enumeration problem, even if it outputs all of them.

## Related definitions

- **[Search problem](/search-problem/)** and **[decision problem](/decision-problem/).** Find one element of $R(x)$, or decide whether $R(x)$ is empty. The proposition above links them to enumeration.
- **[Counting problem](/counting-problem/).** Compute $|R(x)|$. For relations of EnumP this defines the class #P.
- **[Output-sensitive enumeration](/output-sensitive-enumeration/).** The cost measures and classes of enumeration: total time, incremental time, delay, and the classes OutputP, IncP and DelayP.
- **[Combinatorial generation](/combinatorial-generation/).** The listing of all objects of a combinatorial family, such as permutations or partitions, often with [constant amortized time](/constant-amortized-time-generation/) or [loopless](/loopless-generation/) bounds.
- **Ranking and unranking.** For a listing in a fixed order, the rank of an object is its position. See [combinatorial ranking and unranking](/combinatorial-ranking-and-unranking/).
- **[Reverse search](/reverse-search/).** A general method that gives polynomial delay and small space for many enumeration problems.

## References
