---
tag: NS3NNE
kind: concept
slug: search-problem
name: Search problem
aliases:
- constructive problem
- function problem
area: complexity/reductions-catalogue
level: intro
summary: A problem given by a relation R that asks, for an instance x, for some w with (x, w) in R, or for the answer that none exists. Its decision version only asks whether one exists.
prereqs: [decision-problem, certificate]
see_also: [fnp, fp, tfnp, search-to-decision-reduction, levin-reduction, optimization-to-decision-reduction, integer-factorization, one-way-function]
sources:
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press, 2008
    locator: Chapter 2, search problems and the classes PF and PC, and Section 2.2.3, self-reducibility of search problems
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 2.5, Decision versus search
  - paper: doi:10.1137/S0097539792228289
    title: "Mihir Bellare and Shafi Goldwasser, The complexity of decision versus search, SIAM Journal on Computing 23(1) (1994), 97-119"
    locator: search problems of NP languages whose search does not reduce to decision unless deterministic and nondeterministic double-exponential time are equal
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 5.1, Turing Reducibility and NP-Hard Problems (search problems and their NP-hardness)
---

A search problem asks for a solution, not only for a yes or no answer. It is given by a relation $R$ between instances and solutions: on input $x$, the task is to output some $w$ with $(x, w) \in R$, or to report that no such $w$ exists. Every search problem has a [decision problem](/decision-problem/) beside it, "does $x$ have a solution?", and the main question about the pair is how much harder the search is than the decision.

## In plain words

A decision problem asks "is there a way?". A search problem asks "show me a way". For a puzzle, the first wants yes or no, and the second wants a filled-in grid. Often the two are equally hard: with a helper that only answers yes or no, you can build a solution one piece at a time by asking whether each partial choice can still be completed. But some search problems always have an answer, so the yes or no question is trivial, and finding the answer may still be hard. Splitting a large number into its prime factors is the standard example: every number has a factorization, and no fast way to find one is known.

## The idea

A *relation* $R \subseteq \{0,1\}^* \times \{0,1\}^*$ defines the search problem: given $x$, find a $w$ in $R(x) = \{w : (x, w) \in R\}$, or say "none" if $R(x)$ is empty. Any valid solution is accepted, so the answer need not be unique. This is what separates a search problem from a *function problem* in the strict sense, where each input has one correct output, although the two names are often used for the same thing. Its decision version is the language $L_R = \{x : R(x) \neq \emptyset\}$.

The most studied search problems are those of NP relations: solutions are short, $|w| \le q(|x|)$ for a polynomial $q$, and each candidate can be checked in polynomial time. These are the [certificates](/certificate/) of the language $L_R \in$ NP. The classes of search problems are:

- **[FNP](/fnp/)** (Goldreich calls it PC): search problems of NP relations.
- **[FP](/fp/)** (Goldreich calls it PF): search problems that some polynomial-time algorithm solves, finding a solution when one exists.
- **[TFNP](/tfnp/)**: search problems of NP relations that are *total*, so that every instance has a solution. Its subclasses [PLS](/pls/) and [PPAD](/ppad/) collect problems whose solutions exist for a specific combinatorial reason.

FP = FNP holds if and only if P = NP. If P = NP, a [search-to-decision reduction](/search-to-decision-reduction/) through SAT solves every FNP problem; conversely, an FNP solver decides SAT.

Three questions relate a search problem to other problems.

- **Search versus decision.** For SAT and for every NP-complete language, search reduces to decision with polynomially many oracle questions ([self-reducibility](/self-reducibility/)). Bellare and Goldwasser (1994) showed that this fails for some NP languages under a plausible assumption about double-exponential time.
- **Search versus optimization.** An optimization problem asks for the best solution, and its decision version asks whether a solution of value at least $k$ exists; binary search on $k$ links them ([optimization to decision](/optimization-to-decision-reduction/)).
- **Reductions between search problems.** A [Levin reduction](/levin-reduction/) maps instances and also maps solutions back. A [Cook reduction](/turing-reduction/) with a search oracle may ask many questions.

## Examples

- **SAT search.** Given a CNF formula, find a satisfying assignment. For $\psi = (x_1 \lor x_2) \land (\neg x_1 \lor x_3) \land (\neg x_2 \lor \neg x_3) \land (x_3 \lor x_4) \land (\neg x_4 \lor \neg x_1)$, which has $2$ satisfying assignments, a decision oracle finds the solution $x_1 x_2 x_3 x_4 = 1010$ with $5$ questions, as traced on [search-to-decision reduction](/search-to-decision-reduction/).
- **Factoring.** Given $N > 1$, find its prime factors. This search problem is total. The decision version "does $N$ have a divisor $d$ with $2 \le d \le k$?" is in NP and in coNP, and binary search on $k$ turns a decision oracle into a factoring algorithm. For $N = 1001$ this search finds $7$, $11$ and $13$ with $21$ oracle questions; for $N = 1024$ it finds ten factors of $2$ with $63$ questions. No polynomial-time algorithm for [integer factorization](/integer-factorization/) is known.
- **Hamiltonian cycle.** Given a graph, find a cycle through every vertex once. Deleting edges one at a time, and keeping a deletion when the oracle still says yes, finds a cycle with one question per edge.
- **Nash equilibria.** Every finite game has a mixed [Nash equilibrium](/nash-equilibrium/), so the decision version is trivial, but finding one is complete for PPAD, a class not known to be in FP.
- **Local optima.** A [local search problem](/local-search-problem/) asks for a solution that no neighbor improves. One always exists, and many such problems are complete for PLS.
- **Inverting a function.** Given $y$, find some $x$ with $F(x) = y$. A [one-way function](/one-way-function/) is one for which this search is hard on average, even though checking a proposed $x$ is easy.

## Where it is used

- **Defining NP-hardness for non-languages.** Garey and Johnson (1979, Section 5.1) define a search problem to be NP-hard when SAT [Cook-reduces](/turing-reduction/) to it. This covers optimization and construction problems that are not sets of strings.
- **Algorithms from decision procedures.** A decision algorithm together with a self-reduction gives a search algorithm with only polynomial overhead. So a lower bound or an upper bound for the decision version of an [NP-hard](/np-hard/) problem usually says the same about its search version.
- **Cryptography.** Security is defined by search problems that must be hard for most inputs: inverting a one-way function, or finding a secret key.
- **Total search.** The classes inside TFNP describe problems where search is the only question, such as finding Nash equilibria and local optima.

## References
