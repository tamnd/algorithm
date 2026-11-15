---
tag: ZMYFJA
kind: technique
slug: answer-set-programming
name: Answer set programming
aliases:
- ASP
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: Solves a search problem by writing a logic program whose stable models are exactly its solutions and calling a solver to find them.
prereqs: [stable-model-semantics, np-complete]
see_also: [choice-rule, answer-set-grounding, smodels-algorithm, conflict-driven-answer-set-solving, stable-model-np-completeness, disjunctive-logic-program, graph-coloring, sat]
sources:
  - paper: doi:10.1023/a:1018930122475
    title: Ilkka Niemelä, Logic programs with stable model semantics as a constraint programming paradigm, Annals of Mathematics and Artificial Intelligence 25(3-4), 241 to 273 (1999)
    locator: the proposal to use stable models as a constraint programming method for NP search problems
  - paper: doi:10.1007/978-3-642-60085-2_17
    title: "Victor W. Marek and Mirosław Truszczyński, Stable models and an alternative logic programming paradigm, in Krzysztof R. Apt, Victor W. Marek, Mirosław Truszczyński and David S. Warren (eds.), The Logic Programming Paradigm: a 25-Year Perspective, Springer, 375 to 398 (1999)"
    locator: the proposal of stable logic programming, where solutions are models and not answers to queries
  - paper: doi:10.1016/s0004-3702(02)00186-8
    title: Vladimir Lifschitz, Answer set programming and plan generation, Artificial Intelligence 138(1-2), 39 to 54 (2002)
    locator: the description of answer set programming as generate and test, and its use for planning
  - book: isbn:9781608459711
    title: Martin Gebser, Roland Kaminski, Benjamin Kaufmann and Torsten Schaub, Answer Set Solving in Practice, Morgan and Claypool (2012)
    locator: the modeling chapters, the grounding chapter (Chapter 4) and the solving chapters
  - paper: doi:10.1016/s0004-3702(02)00187-x
    title: Patrik Simons, Ilkka Niemelä and Timo Soininen, Extending and implementing the stable model semantics, Artificial Intelligence 138(1-2), 181 to 234 (2002)
    locator: the smodels system, choice rules, cardinality and weight constraints, and optimization statements
  - paper: doi:10.1016/j.artint.2012.04.001
    title: Martin Gebser, Benjamin Kaufmann and Torsten Schaub, Conflict-driven answer set solving, from theory to practice, Artificial Intelligence 187-188, 52 to 89 (2012)
    locator: the conflict-driven solver clasp
  - paper: doi:10.1145/1149114.1149117
    title: Nicola Leone, Gerald Pfeifer, Wolfgang Faber, Thomas Eiter, Georg Gottlob, Simona Perri and Francesco Scarcello, The DLV system for knowledge representation and reasoning, ACM Transactions on Computational Logic 7(3) (2006)
    locator: the DLV system for disjunctive programs and weak constraints
---

Answer set programming (ASP) is a declarative way to solve hard search problems. You write a logic program in which each [stable model](/stable-model-semantics/) is one solution, and a solver computes the stable models. Niemelä (1999) and Marek and Truszczyński (1999) proposed it, and the name refers to the answer sets of Gelfond and Lifschitz. The method fits the problems in NP, because deciding whether a finite propositional normal program has a stable model is [NP-complete](/stable-model-np-completeness/).

## In plain words

You do not write steps that find the answer. You describe what an answer looks like. First you say which choices are open, for example "each node gets one colour". Then you say which choices are wrong, for example "two neighbours must not get the same colour". A solver then finds the sets of choices that break no rule. Each such set is one answer. If you want more answers, the solver lists them, and if you want the best one, you add a cost and the solver finds the cheapest. The description is short and close to the problem statement, so it is easy to change. The work is in the solver, which uses the same search methods as modern SAT solvers.

## When it applies

ASP fits a problem when these conditions hold.

- The solutions are finite sets of facts over a finite domain, and a proposed solution can be checked by rules. This is the class NP for normal programs, and $\Sigma_2^p$ with [disjunctive programs](/disjunctive-logic-program/).
- The constraints are logical and combinatorial, such as colourings, assignments, schedules, paths and plans of bounded length.
- Recursive definitions are needed, such as reachability. Stable models give these their least fixed point meaning, which a plain [SAT](/sat/) encoding must add by hand.
- Default reasoning or closed world assumptions are part of the problem: an atom that no rule derives is false.

ASP does not fit well when the domain is large and numeric, such as real-valued optimization, or when the program has a huge ground instance, because the [grounder](/answer-set-grounding/) builds all relevant rule instances before the search.

## The template

A typical program has four parts over a set of facts that describe the instance (Lifschitz 2002; Gebser, Kaminski, Kaufmann and Schaub 2012).

1. **Instance.** Facts such as $v(1)$, $e(1, 2)$.
2. **Generate.** [Choice rules](/choice-rule/) state the open choices, for example $1\ \{c(X, r), c(X, g), c(X, b)\}\ 1 \leftarrow v(X)$.
3. **Define.** Normal rules derive auxiliary atoms, for example reachability $r(Y) \leftarrow r(X), \mathit{in}(X, Y)$.
4. **Test.** Constraints $\leftarrow B$ reject the candidates in which $B$ holds, for example $\leftarrow e(X, Y), c(X, C), c(Y, C)$.

An optional fifth part states a cost to minimize, as in the optimization statements of smodels (Simons, Niemelä and Soininen 2002) or the weak constraints of DLV (Leone et al. 2006).

The solver runs in two phases. The grounder replaces variables by constants and produces a propositional program. The solver searches for stable models of it, with [smodels-style propagation](/smodels-algorithm/) or [conflict-driven nogood learning](/conflict-driven-answer-set-solving/). The input language of clingo writes the colouring program as follows.

```
v(1..4).
e(1,2). e(2,3). e(3,4). e(4,1). e(1,3).
1 { c(X,r); c(X,g); c(X,b) } 1 :- v(X).
:- e(X,Y), c(X,C), c(Y,C).
```

## Classic examples

- **Graph colouring.** For the graph with vertices $1, 2, 3, 4$ and edges $12, 23, 34, 41, 13$, the program above has $6$ answer sets, one for each proper 3-colouring. Vertices $1$ and $3$ take two different colours, and $2$ and $4$ both take the third colour. Without the edge $13$ the graph is a 4-cycle and the program has $18$ answer sets. See [graph colouring](/graph-coloring/).
- **Hamiltonian cycle.** Choose a set of arcs with $\{\mathit{in}(X, Y)\} \leftarrow e(X, Y)$ over both directions of each edge, forbid two arcs out of or into one vertex, define $r(Y) \leftarrow \mathit{in}(1, Y)$ and $r(Y) \leftarrow r(X), \mathit{in}(X, Y)$, and add $\leftarrow \mathit{not}\ r(X)$ for each vertex. For the graph above the answer sets are the two directions of the cycle $1, 2, 3, 4$. The recursive definition of $r$ is essential: the [completion](/clark-completion/) of the program also accepts the arcs $12, 21, 34, 43$, where $r(3)$ and $r(4)$ support each other, but no stable model contains them. See [Hamiltonian cycle](/hamiltonian-cycle/).
- **Planning.** With a fixed horizon $T$, choose actions at each step, define the state at the next step with effect rules and frame rules such as $h(F, T+1) \leftarrow h(F, T), \mathit{not}\ \mathit{ab}(F, T)$, and constrain the goal at the last step. Lifschitz (2002) describes encodings of this kind.
- **SAT.** For each variable $x$, the pair $x \leftarrow \mathit{not}\ \bar{x}$, $\bar{x} \leftarrow \mathit{not}\ x$ generates the two values, and each clause becomes a constraint. The stable models are the satisfying assignments, which is the reduction in the [NP-completeness proof](/stable-model-np-completeness/).

## Variations

- **Optimization.** Minimize statements and weak constraints rank the answer sets by cost. Solvers search for a model and then for a better one, until none exists.
- **Disjunctive ASP.** Rules with disjunctive heads express problems at the second level of the polynomial hierarchy, such as 2-QBF; existence is [$\Sigma_2^p$-complete](/disjunctive-asp-sigma2-completeness/).
- **Aggregates and weights.** Cardinality and weight constraints, and aggregates such as count and sum, express numeric conditions without auxiliary atoms (Simons, Niemelä and Soininen 2002).
- **Brave and cautious reasoning.** Instead of listing models, ask whether an atom is in some answer set or in all of them. For normal programs these tasks are NP-complete and coNP-complete.
- **Abductive reasoning.** [Abductive logic programs](/abductive-logic-programming/) declare some atoms as hypotheses, and with a choice rule over them an ASP solver computes explanations.

## Pitfalls

- **The grounding is too large.** A rule with $k$ variables over $c$ constants can have $c^k$ instances. Reduce the number of variables per rule, and give each variable a domain atom in the positive body. The [grounding page](/answer-set-grounding/) gives a family where the ground program grows exponentially.
- **Unsafe variables.** Every variable of a rule must occur in a positive body atom. A rule such as $p(X) \leftarrow \mathit{not}\ q(X)$ is rejected by grounders, because $X$ has no domain.
- **A choice with no test.** A choice rule without constraints permits every subset. The program $\{a, b, c\} \leftarrow$ has $8$ answer sets, not $1$.
- **Constraints do not derive atoms.** A constraint $\leftarrow \mathit{not}\ a$ removes the models without $a$; it does not make $a$ true. If no rule can derive $a$, the program has no answer set.
- **Positive loops are not support.** Atoms that only support each other through a positive cycle are false in every stable model, as in the Hamiltonian cycle example. Encodings that rely on such loops for truth, and translations to SAT that use only the completion, give wrong results.
- **Symmetric answer sets.** Swapping colour names gives another answer set of the colouring program, so the $6$ answer sets above are $1$ colouring up to the names. Counting or enumerating without symmetry breaking can take much longer than finding one model.
- **Closed world.** An atom that no rule derives is false, so a missing fact in the instance changes the answer without any warning.

## Exercises

1. Write a program whose answer sets are the independent sets of size at least $2$ of a graph given by facts $v(X)$ and $e(X, Y)$. *Hint*: a choice rule over $\mathit{in}(X)$, a constraint on edges, and a cardinality constraint in a constraint body.
2. Show that the program $\{a\} \leftarrow$, $b \leftarrow a$, $\leftarrow \mathit{not}\ b$ has exactly one answer set and find it.
3. In the Hamiltonian cycle program, remove the rules for $r$ and the constraints $\leftarrow \mathit{not}\ r(X)$. Describe the answer sets that are added, in terms of cycles in the graph.
4. Encode the N-queens problem for $N = 4$ with one choice rule and constraints, and count its answer sets by hand. *Answer*: $2$.
5. Give a program with variables whose ground instance over $c$ constants has at least $c^3$ rules, and rewrite it with the same answer sets and $O(c^2)$ rules.

## References
