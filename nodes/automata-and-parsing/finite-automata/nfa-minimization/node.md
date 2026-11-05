---
tag: B5XD4W
kind: problem
slug: nfa-minimization
name: NFA minimization
aliases:
- minimum-state NFA problem
- minimal NFA problem
area: automata-and-parsing/finite-automata
level: advanced
summary: Find an equivalent NFA with the fewest states; PSPACE-hard, even when the input is a DFA.
prereqs: [nondeterministic-finite-automaton, dfa-minimization, nfa-equivalence]
see_also: [fooling-set-method, myhill-nerode-theorem, nfa-universality, state-complexity, bisimulation, regex-minimization, determinization-blowup-lower-bound, unambiguous-nfa]
sources:
  - paper: "Tao Jiang and B. Ravikumar, Minimal NFA problems are hard, SIAM Journal on Computing 22(6) (1993)"
    locator: pp. 1117 to 1141 (NFA minimization is PSPACE-complete, also when the input is a DFA; minimization of unambiguous automata is NP-complete)
  - paper: "Gregor Gramlich and Georg Schnitger, Minimizing NFA's and regular expressions, 22nd Symposium on Theoretical Aspects of Computer Science (STACS 2005), Lecture Notes in Computer Science 3404"
    locator: pp. 399 to 411 (no efficient approximation within a factor o(n) for a given NFA unless P = PSPACE; a factor of at least n over a power of log n for a given DFA, under cryptographic assumptions)
  - paper: "Tsunehiko Kameda and Peter Weiner, On the state minimization of nondeterministic finite automata, IEEE Transactions on Computers C-19(7) (1970)"
    locator: pp. 617 to 627 (an exact method with coverings of a matrix built from the DFAs of the language and of its reversal)
  - paper: "Ian Glaister and Jeffrey Shallit, A lower bound technique for the size of nondeterministic finite automata, Information Processing Letters 59(2) (1996)"
    locator: pp. 75 to 77 (the fooling set lower bound)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.4, Equivalence and Minimization of Automata (the minimal DFA and its uniqueness, for comparison)
---

NFA minimization is the problem of finding, for a regular language given by a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) or a [DFA](/deterministic-finite-automaton/), an NFA with the fewest states that accepts it. Unlike [DFA minimization](/dfa-minimization/), it has no polynomial time algorithm unless P = [PSPACE](/pspace/): its decision version is PSPACE-complete, even when the input is a DFA (Jiang and Ravikumar, 1993), and the minimum cannot be approximated well (Gramlich and Schnitger, 2005). A minimal NFA can be exponentially smaller than the minimal DFA, and it is not unique.

## In plain words

For a deterministic machine there is one smallest machine for each set of strings, and a fast method finds it. For a nondeterministic machine both of these facts fail. There can be many different smallest machines, and finding one is very hard: even the question "is there a machine with at most this many states?" is as hard as every problem that a computer solves with a reasonable amount of memory.

In practice, programs make a machine smaller by merging states that behave alike, which is fast but does not always reach the minimum. To prove that a machine is the smallest, people use lower bound arguments, such as a set of strings that must all lead to different states.

## Definition

**Input.** A regular language $L \subseteq \Sigma^*$, given by an NFA $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to \mathcal{P}(Q)$, one start state and no $\varepsilon$-moves, or by a complete DFA, or by a [regular expression](/regular-expression/).

**Output.** An NFA $N'$ of the same kind with $L(N') = L$ and the least number of states. This number is the *nondeterministic state complexity* $\mathrm{nsc}(L)$.

**Decision version.** Given $N$ and an integer $k$, is there an NFA with at most $k$ states that accepts $L(N)$?

The measure is the number of states. Other measures, such as the number of transitions, give different problems.

## Variants

- **Input given as a DFA.** The input is larger, since a DFA can be exponentially larger than an NFA for the same language, but the problem stays PSPACE-complete (Jiang and Ravikumar, 1993).
- **Unambiguous output.** Find a minimal [unambiguous NFA](/unambiguous-nfa/). Given a DFA, this is NP-complete (Jiang and Ravikumar, 1993).
- **Regular expressions.** Find a shortest regular expression for $L$. This is [regex minimization](/regex-minimization/), and it is PSPACE-complete in the same way.
- **Reduction without a guarantee.** Find a smaller equivalent NFA, not necessarily a minimal one, in polynomial time. This is what tools do.
- **Lower bounds.** Prove that $\mathrm{nsc}(L) \ge k$ for a given $L$ and $k$, by hand or by a method such as fooling sets.

## Examples

**Minimal NFAs are not unique.** Over $\{a\}$, the language $a^+ = \{a^\ell : \ell \ge 1\}$ needs 2 states, since the only languages of one-state NFAs are $\emptyset$, $\{\varepsilon\}$ and $a^*$. With states 0 (start) and 1, and $F = \{1\}$, exactly six NFAs accept $a^+$: $\delta(0, a)$ is $\{1\}$ or $\{0, 1\}$, and $\delta(1, a)$ is any subset when $\delta(0, a) = \{0, 1\}$, or $\{1\}$ or $\{0, 1\}$ when $\delta(0, a) = \{1\}$. They have different transition graphs, so no state renaming maps one to another. The minimal DFA, in contrast, is unique up to renaming by the [Myhill-Nerode theorem](/myhill-nerode-theorem/).

**Exponential gap to the DFA.** Let $L_n$ be the strings over $\{a, b\}$ whose $n$-th symbol from the end is $a$. An NFA with $n + 1$ states accepts $L_n$: it loops in state 0, guesses the $a$, and counts $n - 1$ more symbols. The minimal DFA has $2^n$ states. The NFA is minimal, by a fooling set of size $n + 1$: let $x_i$ be the first $i$ symbols of $a b^{n - 1}$ and $y_i$ the rest, for $0 \le i \le n$. Each $x_i y_i = a b^{n - 1}$ is in $L_n$. For $i < j$ the string $x_i y_j$ has length $n - (j - i) < n$, so it is not in $L_n$. By the lemma below, every NFA for $L_n$ has at least $n + 1$ states. For $n = 2$ the fooling set is $(\varepsilon, ab), (a, b), (ab, \varepsilon)$, and no NFA with 2 states accepts $L_2$.

## Known algorithms

- **Exact search.** For $k = 1, 2, \ldots$, try all NFAs with $k$ states and test each for [equivalence](/nfa-equivalence/) with the input. Correct, but the number of candidates is $2^{\Theta(k^2 \sigma)}$, and each test is itself PSPACE-complete.
- **Kameda and Weiner (1970).** Build the minimal DFA of $L$ and the minimal DFA of the reversal of $L$, and a matrix with a row for each state of the first, a column for each state of the second, and an entry that records whether the two states share a string. A minimal NFA corresponds to a cover of this matrix by a least number of "grids" that satisfies an extra condition. The method is exact and exponential.
- **Reduction by bisimulation and simulation.** Merge the states of $N$ that are equivalent under the largest [bisimulation](/bisimulation/), or under mutual simulation, on $N$ or on its reversal. The result accepts $L(N)$, is never larger, and is computed in polynomial time, but it is not minimal in general.
- **Determinize, minimize, then reduce.** Build the minimal DFA by [subset construction](/subset-construction/) and [DFA minimization](/dfa-minimization/), then reduce it as an NFA. The first step can cost $2^n$.
- **SAT encodings.** Encode "there is an NFA with $k$ states that agrees with $L$" as a satisfiability problem over the transition variables, and test the candidates found. This works for small $k$.

## Bounds

**Complexity.** The decision version is PSPACE-complete when the input is an NFA, a regular expression or a DFA (Jiang and Ravikumar, 1993). The hardness for NFA input follows from [NFA universality](/nfa-universality/): $L(N) = \Sigma^*$ if and only if the minimal NFA of $L(N)$ is the one-state NFA with $F = \{q_0\}$ and a loop on each symbol, so a polynomial algorithm for minimization would decide universality. Membership in PSPACE: guess an NFA with $k$ states and test equivalence in polynomial space.

**Approximation.** No polynomial time algorithm approximates $\mathrm{nsc}(L)$ within a factor $o(n)$ for a given NFA with $n$ states, unless P = PSPACE. For a given DFA with $n$ states, a factor of at least $n / \mathrm{poly}(\log n)$ is needed under cryptographic assumptions (Gramlich and Schnitger, 2005).

**Relation to DFA size.** Let $d$ be the number of states of the minimal complete DFA of $L$. Then $\lceil \log_2 d \rceil \le \mathrm{nsc}(L) \le d$. The lower bound holds because the [subset construction](/subset-construction/) turns an NFA with $k$ states into a DFA with at most $2^k$ states, and the example $L_n$ shows that it is tight up to one state.

**Fooling set lemma.** Let $(x_1, y_1), \ldots, (x_k, y_k)$ be pairs of strings with $x_i y_i \in L$ for all $i$, and, for all $i \ne j$, $x_i y_j \notin L$ or $x_j y_i \notin L$. Then every NFA for $L$ has at least $k$ states (Glaister and Shallit, 1996). *Proof.* Fix an NFA for $L$, and for each $i$ an accepting run on $x_i y_i$; let $p_i$ be its state after $x_i$. If $p_i = p_j$ for some $i \ne j$, then the run on $x_i$ to $p_i$ followed by the run from $p_j$ on $y_j$ is an accepting run on $x_i y_j$, and likewise $x_j y_i$ has an accepting run. Both strings are then in $L$, which contradicts the condition. So the $p_i$ are pairwise distinct. The bound can be far from $\mathrm{nsc}(L)$, and more general methods, such as covers of the matrix of [nondeterministic communication complexity](/nondeterministic-communication-complexity/), give better bounds; see the [fooling set method](/fooling-set-method/).

## Reductions

- **From universality.** As in the bounds above, a minimizer decides [NFA universality](/nfa-universality/), so NFA minimization is PSPACE-hard for NFA input.
- **From the universality of a list of DFAs.** Jiang and Ravikumar reduce from the PSPACE-complete problem "is $L(A_1) \cup \cdots \cup L(A_t) = \Sigma^*$ for DFAs $A_1, \ldots, A_t$" to get hardness for DFA input.
- **To equivalence.** A candidate NFA is checked by [NFA equivalence](/nfa-equivalence/) with the input.
- **Relation to regular expressions.** A regular expression with $k$ occurrences of symbols has an NFA with $k + 1$ states (the [Glushkov automaton](/glushkov-automaton/)), so $\mathrm{nsc}(L)$ is at most one more than the least number of symbol occurrences in an expression for $L$.

## Applications

- **Smaller automata for matching.** Regular expression engines and network intrusion systems that simulate NFAs run faster on smaller NFAs, so they reduce them with simulation-based merging.
- **Model checking.** Reducing property automata, such as [Büchi automata](/buchi-automaton/), shrinks the product with the system.
- **Descriptional complexity.** The number $\mathrm{nsc}(L)$ is the measure in the nondeterministic part of [state complexity](/state-complexity/), where fooling sets give the lower bounds.

## References
