---
tag: 94G9A7
kind: concept
slug: self-reducibility
name: Self-reducibility
aliases:
- random self-reducibility
area: complexity/reductions-catalogue
level: advanced
summary: A problem is self-reducible when an instance can be solved in polynomial time from answers for smaller instances of the same problem. SAT is the standard example.
prereqs: [search-to-decision-reduction]
see_also: [search-problem, turing-reduction, levin-reduction, mahaneys-theorem, karp-lipton-theorem, pspace, sat, graph-isomorphism-problem]
sources:
  - paper: "\"Optimal algorithms for self-reducible problems\""
    title: "Claus-Peter Schnorr, Optimal algorithms for self-reducible problems, in S. Michaelson and R. Milner (eds.), Automata, Languages and Programming (ICALP 1976), Edinburgh University Press, 1976, 322-337"
    locator: the definition of self-reducible problems and optimal algorithms for them
  - book: isbn:9780521884730
    title: Oded Goldreich, Computational Complexity, A Conceptual Perspective, Cambridge University Press, 2008
    locator: Section 2.2.3, Self-Reducibility of Search Problems (the definition, and the result that the search problems of NP-complete sets are self-reducible)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 2.5, Decision versus search (the remark that SAT is downward self-reducible)
  - paper: doi:10.1137/S0097539792228289
    title: "Mihir Bellare and Shafi Goldwasser, The complexity of decision versus search, SIAM Journal on Computing 23(1) (1994), 97-119"
    locator: languages in NP whose search problem does not reduce to decision under a double-exponential time assumption
---

A problem is self-reducible when any instance can be solved in polynomial time from the answers to smaller instances of the same problem. SAT is the main example: a formula is satisfiable exactly when it stays satisfiable after setting $x_1 = 0$ or after setting $x_1 = 1$, and both are formulas with fewer variables. Self-reducibility is the structure behind [search-to-decision reductions](/search-to-decision-reduction/): it lets a yes-or-no algorithm build a solution. Schnorr (1976) introduced the notion. The alias "random self-reducibility" names a different property, where a worst-case instance is solved from random instances, and this encyclopedia has no page on it yet.

## In plain words

Some problems contain smaller copies of themselves. If you can answer the question for every smaller copy, you can answer it for the whole thing with little extra work. For a list of yes or no switches that must satisfy some rules, set the first switch both ways. Each choice leaves a smaller problem of the same kind, and the original has a solution exactly when one of the two smaller problems has one. This structure has two uses. It lets a helper that only answers yes or no find an actual solution, one switch at a time. And it limits how strange such problems can be: their behavior on large inputs is tied to their behavior on small ones.

## The idea

Two forms of the property are in common use.

**Downward self-reducibility (for languages).** A language $L$ is *downward self-reducible* if some polynomial-time [oracle machine](/oracle-turing-machine/) $M$ decides $L$ with oracle $L$, and on every input $x$, $M$ asks only questions shorter than $x$ (or smaller under another polynomial measure, such as the number of variables). For SAT,

$$\varphi \in \mathrm{SAT} \iff \varphi|_{x_1 = 0} \in \mathrm{SAT} \ \text{ or } \ \varphi|_{x_1 = 1} \in \mathrm{SAT},$$

and a formula with no variables is decided directly. Unfolding the recursion gives a decision procedure that uses polynomial space, since the depth is at most the size of the input and each level stores a polynomial amount. So every downward self-reducible language is in [PSPACE](/pspace/).

**Self-reducibility of search problems.** The search problem of a relation $R$ is *self-reducible* when it [Cook-reduces](/turing-reduction/) to $L_R = \{x : \text{some } w \text{ has } (x, w) \in R\}$, the decision problem of $R$ itself (Goldreich, Section 2.2.3). The usual reason is that each prefix question, "does $x$ have a solution that starts with $u$?", can be written in polynomial time as an instance of $L_R$. Then the [search-to-decision template](/search-to-decision-reduction/) extends $u$ one piece at a time.

**NP-complete sets.** If $L_R$ is NP-complete, the search problem of $R$ reduces to deciding $L_R$, even when the prefix questions are not instances of $L_R$ in an obvious way. The proof composes three steps. A [Levin reduction](/levin-reduction/) from $R$ to SAT maps $x$ to a formula $\varphi_x$. The search for a satisfying assignment of $\varphi_x$ uses SAT's own self-reducibility, and each SAT question is mapped back to $L_R$ by a Karp reduction, since $L_R$ is NP-complete. The backward map of the Levin reduction turns the assignment into a solution for $x$ (Goldreich, Section 2.2.3).

**Not every problem.** For general NP languages the property can fail. Bellare and Goldwasser (1994) showed that if deterministic and nondeterministic double-exponential time differ, some language in NP has a search problem that is not reducible to its decision problem in polynomial time. And for total problems the decision version is trivial: every integer $N > 1$ has a factorization, so "does $N$ have a factorization?" says nothing, and factoring is not self-reducible in this sense.

## Examples

- **SAT** is downward self-reducible and search self-reducible. For $\psi = (x_1 \lor x_2) \land (\neg x_1 \lor x_3) \land (\neg x_2 \lor \neg x_3) \land (x_3 \lor x_4) \land (\neg x_4 \lor \neg x_1)$, the search with a decision oracle finds $x_1 x_2 x_3 x_4 = 1010$ in $5$ questions.
- **Clique.** Deleting a vertex gives a smaller instance of CLIQUE. On the $7$-vertex example graph on [search-to-decision reduction](/search-to-decision-reduction/), deletions find the maximum clique $\{0, 1, 2, 3\}$ with $8$ questions.
- **Graph isomorphism.** Finding an isomorphism between two graphs reduces to deciding whether two graphs are isomorphic: attach the same distinct marker, such as a large clique or a long path, to a vertex in each graph and ask whether the marked graphs are still isomorphic. This is a self-reduction for a problem in NP that is not known to be NP-complete ([graph isomorphism](/graph-isomorphism-problem/)).
- **Non-example: factoring.** The decision problem "is $N$ composite?" is in P and does not help to find a factor. A different decision problem, "does $N$ have a divisor at most $k$?", does reduce factoring to decision, but it is not the trivial decision version of the total search problem.

## Where it is used

- **Search from decision.** Any polynomial-time decision algorithm for a self-reducible problem gives a polynomial-time search algorithm. With SAT this shows that if P = NP, all NP search problems are easy.
- **Optimal algorithms.** Schnorr (1976) introduced self-reducibility in a study of optimal algorithms for such problems.
- **Sparse sets and circuits.** The proofs of [Mahaney's theorem](/mahaneys-theorem/) and the [Karp-Lipton theorem](/karp-lipton-theorem/) both use the self-reducibility of SAT. In Karp-Lipton, a small circuit that decides SAT is turned into a small circuit that finds satisfying assignments, so that its answers can be checked.
- **Upper bounds.** Downward self-reducibility places a language in PSPACE, as shown above.

## References
