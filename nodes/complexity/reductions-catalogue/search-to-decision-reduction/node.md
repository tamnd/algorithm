---
tag: 7B7TBW
kind: technique
slug: search-to-decision-reduction
name: Search-to-decision reduction
aliases:
- decision-to-search reduction
- self-reduction for search
- self-reduction from decision
- self-reduction from search to decision
area: complexity/reductions-catalogue
level: core
summary: Finds a solution with a yes-or-no oracle by fixing the solution one piece at a time and asking whether the partial choice can still be completed.
prereqs: [search-problem, turing-reduction]
see_also: [self-reducibility, optimization-to-decision-reduction, levin-reduction, sat, valiant-vazirani-theorem, integer-factorization, tfnp, fnp]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 2.5, Decision versus search (the variable-by-variable search for SAT and the consequence for NP search problems if P = NP)
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press, 2008
    locator: Section 2.2.3, Self-Reducibility of Search Problems
  - paper: doi:10.1137/S0097539792228289
    title: "Mihir Bellare and Shafi Goldwasser, The complexity of decision versus search, SIAM Journal on Computing 23(1) (1994), 97-119"
    locator: the main result, an NP language whose search problem does not reduce to its decision problem if deterministic and nondeterministic double-exponential time differ
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Section 5.1, Turing Reducibility and NP-Hard Problems
---

A search-to-decision reduction solves a [search problem](/search-problem/) with an oracle that only answers yes or no. It builds a solution one piece at a time: for each piece it tries a value and asks the oracle whether the partial solution can still be completed, and it keeps a value that gets a yes. For SAT this finds a satisfying assignment of an $n$-variable formula with $n + 1$ questions, so a polynomial-time decision algorithm for SAT would give a polynomial-time search algorithm. The reduction is a [Cook reduction](/turing-reduction/), since it asks many adaptive questions.

## In plain words

Suppose a friend can tell you whether a puzzle has a solution, but will not show it. You can still find one. Fill in the first square with a guess and ask your friend whether the puzzle still has a solution. If yes, keep the guess; if no, try another value. Move on to the next square and repeat. Every answer keeps you on a path that still leads to a solution, so when the last square is filled you have one. The number of questions is about the number of squares times the number of values per square. The method needs one thing: a partly filled puzzle must again be a puzzle your friend can answer.

## When it applies

The technique needs three things.

1. **Solutions in pieces.** A solution $w$ of an instance $x$ is a sequence of $\ell(x)$ pieces, each from a set of choices of polynomial size, with $\ell(x)$ polynomial in $|x|$.
2. **Restriction stays in the language.** For a partial solution $u$ (some pieces fixed), the question "does $x$ have a solution that extends $u$?" can be written in polynomial time as an instance $\mathrm{RESTRICT}(x, u)$ of the decision problem that the oracle answers. For SAT, fixing $x_i = b$ and simplifying gives a smaller formula. When the restricted instance is an instance of the same problem, the problem is called [self-reducible](/self-reducibility/).
3. **Polynomially many questions.** The total number of oracle questions is polynomial in $|x|$.

It does not apply as stated when a partial solution cannot be expressed in the oracle's own language, and it fails in a deeper way for total problems, whose decision versions are trivial (see Pitfalls).

## The template

```pseudo id=template
SEARCH(x)                         ▷ DECIDE is the oracle for the decision problem
L1  if not DECIDE(x) then return NONE
L2  u ← empty partial solution
L3  for i ← 1 to ℓ(x)               ▷ hole: the number of pieces
L4      for each choice c of piece i, except the last
L5          if DECIDE(RESTRICT(x, u + (i ↦ c))) then
L6              u ← u + (i ↦ c); go to the next i
L7      u ← u + (i ↦ last choice)    ▷ no question needed
L8  return u
```

The holes are the decomposition into pieces ($\ell$ and the choices), the encoding RESTRICT, and the oracle DECIDE.

**Invariant.** After line L1 and after each round of the outer loop, $x$ has a solution that extends $u$.

**Correctness.** Line L1 makes the invariant true at the start. In round $i$, the invariant gives a solution $w$ extending $u$; its piece $i$ is one of the choices, so some choice $c$ makes $\mathrm{RESTRICT}(x, u + (i \mapsto c))$ a yes-instance. If the loop at L4 finds a yes, the invariant holds for the new $u$. If every tried choice gets a no, the remaining choice must be the piece of $w$, so line L7 keeps the invariant without asking. After the last round $u$ fixes every piece and extends to a solution, so $u$ is a solution. If $x$ has no solution, line L1 returns NONE correctly.

**Cost.** With at most $k$ choices per piece, the number of questions is at most $1 + \ell(x)(k - 1)$, and the time is polynomial if RESTRICT is. For binary pieces this is $\ell(x) + 1$.

## Classic examples

### SAT, variable by variable

Pieces are the values of $x_1, \ldots, x_n$; RESTRICT substitutes the fixed values. Take

$$\psi = (x_1 \lor x_2) \land (\neg x_1 \lor x_3) \land (\neg x_2 \lor \neg x_3) \land (x_3 \lor x_4) \land (\neg x_4 \lor \neg x_1),$$

which has $2$ satisfying assignments. The run asks, in order:

| question | instance | answer | fixed |
| --- | --- | --- | --- |
| Q1 | $\psi$ | yes | |
| Q2 | $\psi$ with $x_1 = 1$ | yes | $x_1 = 1$ |
| Q3 | $\ldots$ and $x_2 = 1$ | no | $x_2 = 0$ |
| Q4 | $\ldots$ and $x_3 = 1$ | yes | $x_3 = 1$ |
| Q5 | $\ldots$ and $x_4 = 1$ | no | $x_4 = 0$ |

The result $x_1 x_2 x_3 x_4 = 1010$ satisfies $\psi$, after $5 = n + 1$ questions.

### Clique, by deleting vertices

For CLIQUE ("does $G$ have a clique of size $k$?"), deleting a vertex gives another instance of CLIQUE. First find the clique number $\omega$ by binary search on $k$ ([optimization to decision](/optimization-to-decision-reduction/)); then for each vertex $v$ in turn, delete $v$ if the graph without $v$ still has a clique of size $\omega$. The vertices that remain form a maximum clique. On the graph with vertices $0, \ldots, 6$, all edges inside $\{0,1,2,3\}$, the triangle $\{4,5,6\}$ and the edges $3$-$4$ and $2$-$5$ ($11$ edges), binary search asks $k = 4, 6, 5$ and gets $\omega = 4$ in $3$ questions. The deletion phase asks $1$ question for the start and $7$ deletions: deleting $0$, $1$, $2$ or $3$ gets a no, deleting $4$, $5$ or $6$ gets a yes, so $\{0, 1, 2, 3\}$ remains, after $8 = n + 1$ questions.

### Hamiltonian cycle, by deleting edges

For [Hamiltonian cycle](/hamiltonian-cycle-problem/), fixing "this edge is in the cycle" is not an instance of the same problem, but deleting an edge is. Go through the edges once; delete an edge if the graph without it still has a Hamiltonian cycle. At the end every remaining edge is needed, so the remaining graph is a single Hamiltonian cycle. This uses $m + 1$ questions for $m$ edges.

### Factoring, by binary search

The decision problem "does $N$ have a divisor $d$ with $2 \le d \le k$?" is in NP and in coNP. Binary search on $k$ over $[2, N - 1]$ finds the least divisor of $N$, which is prime; divide and repeat. Each factor costs $O(\log N)$ questions, and $N$ has at most $\log_2 N$ prime factors, so the total is $O(\log^2 N)$, polynomial in the number of bits. With one first question "is $N$ composite?" per round, the search finds $1001 = 7 \cdot 11 \cdot 13$ with $21$ questions and $1024 = 2^{10}$ with $63$ questions. Here the pieces are bits of a number, not bits of a solution string, but the invariant is the same.

## Variations

- **Through a complete problem.** If the decision problem $L$ is NP-complete, any NP search problem reduces to it: a [Levin reduction](/levin-reduction/) maps the instance to a SAT formula, the template finds a satisfying assignment using the SAT oracle (each SAT question is mapped to $L$ by a Karp reduction), and the backward map of the Levin reduction gives a solution. So for NP-complete languages, search reduces to decision (Goldreich, Section 2.2.3). It also shows that if P = NP, every NP search problem is in FP (Arora and Barak, Section 2.5).
- **Optimization.** For an optimization problem, first find the optimal value by binary search on a bound, then search for a solution with that value. This is how a decision oracle for the [traveling salesman](/traveling-salesman-decision/) problem gives an optimal tour.
- **Non-adaptive search.** The template asks adaptive questions. If the solution is unique, the questions "is there a solution with piece $i = 1$?" can be asked all at once, in parallel. The [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) makes the solution unique with a random restriction, which gives a randomized non-adaptive search for SAT.
- **Not always possible.** Bellare and Goldwasser (1994) proved that if deterministic and nondeterministic double-exponential time differ, some language in NP has a search problem that does not reduce to its decision problem in polynomial time. So the technique depends on structure, not only on membership in NP.

## Pitfalls

- **The wrong direction.** Decision reduces to search trivially: find a solution and answer yes if one is found. The interesting direction is search to decision. The alias "decision-to-search reduction" names the trivial direction and should not be used for this technique.
- **Restrictions outside the language.** Fixing a piece may give an instance that the oracle cannot answer. For Hamiltonian cycle, "the cycle must use edge $e$" is not a plain graph question; edge deletion solves this. When no such encoding exists, the problem may still be searched through a Levin reduction to SAT.
- **Total problems.** If every instance has a solution, the decision version is trivial and the template learns nothing from it. "Is $N$ composite?" does not help to factor $N$; the bounded-divisor question does. Problems in [TFNP](/tfnp/), such as finding a Nash equilibrium, have no useful decision version of this kind.
- **Counting the size in binary.** For number problems, a search over all values $1, \ldots, N$ uses $N$ questions, exponential in the input size $\log N$. Use binary search over the value.
- **Forgetting the first question.** Without line L1, the template returns a full "solution" even when none exists. Check the result, or ask first.

## Exercises

1. Give a search-to-decision reduction for [vertex cover](/vertex-cover/) that deletes vertices, and count its questions.
2. Show that if the oracle for SAT answers only for formulas in [3-CNF](/3-sat/), the template still works. Hint: substituting a value only shortens clauses.
3. A graph with $n$ vertices has a [3-coloring](/three-coloring/). Find one with $O(n^2)$ questions to a 3-colorability oracle. Hint: to force two vertices to have the same color, merge them; to force different colors, add an edge.
4. Explain why the factoring reduction needs the decision problem "is there a divisor at most $k$?" and does not work with "is $N$ composite?" alone.

## References
