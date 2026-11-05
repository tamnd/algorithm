---
tag: BM9CKW
kind: problem
slug: regex-equivalence
name: Regex equivalence
aliases:
- regular expression equivalence
area: automata-and-parsing/regular-expressions
level: advanced
summary: Decide whether two regular expressions denote the same language.
prereqs: [regular-expression, nfa-equivalence, pspace]
see_also: [regex-equivalence-pspace-completeness, regex-inclusion, regex-universality, kleene-algebra, brzozowski-derivatives, hopcroft-karp-equivalence, dfa-equivalence, regex-minimization]
sources:
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (equivalence is complete for polynomial space, and for exponential space with squaring)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (inequivalence is NP-complete without star and over a one-letter alphabet; non-elementary with complement)
  - paper: "Janusz A. Brzozowski, Derivatives of regular expressions, Journal of the ACM 11(4) (1964)"
    locator: pp. 481 to 494 (finitely many dissimilar derivatives, and their use to test equivalence)
  - paper: "John E. Hopcroft and Richard M. Karp, A linear algorithm for testing equivalence of finite automata, Technical Report 71-114, Department of Computer Science, Cornell University, 1971"
    locator: the whole report (the union-find algorithm for equivalence)
  - paper: doi:10.1145/2429069.2429124
    title: Filippo Bonchi and Damien Pous, Checking NFA equivalence with bisimulations up to congruence, 40th ACM Symposium on Principles of Programming Languages (POPL 2013)
    locator: pp. 457 to 468 (the algorithms HK and HKC on the subsets of NFA states, and the comparison with antichains)
  - paper: doi:10.1145/321312.321326
    title: Arto Salomaa, Two complete axiom systems for the algebra of regular events, Journal of the ACM 13(1) (1966)
    locator: pp. 158 to 169 (complete axioms for equivalence, with the rule that solves X = XA | B as X = BA*)
  - paper: "Dexter Kozen, A completeness theorem for Kleene algebras and the algebra of regular events, Information and Computation 110(2) (1994)"
    locator: pp. 366 to 390 (the axioms of Kleene algebra are complete for the equivalence of regular expressions)
  - paper: "Richard E. Stearns and Harry B. Hunt III, On the equivalence and containment problems for unambiguous regular expressions, regular grammars and finite automata, SIAM Journal on Computing 14(3) (1985)"
    locator: pp. 598 to 611 (polynomial time for unambiguous expressions and automata)
---

Regex equivalence is the problem of deciding, for two [regular expressions](/regular-expression/) $r$ and $s$, whether $L(r) = L(s)$, written $r \equiv s$. It is decidable, because both languages are regular and every regular language has a unique minimal DFA, but it is hard: for alphabets with at least two symbols it is PSPACE-complete ([Meyer and Stockmeyer, 1972](/regex-equivalence-pspace-completeness/)). All known algorithms take time exponential in the size of the expressions in the worst case. They compare the two languages through automata, through [Brzozowski derivatives](/brzozowski-derivatives/), or through the equational laws of [Kleene algebra](/kleene-algebra/).

## In plain words

Two patterns can look different and still describe the same strings: "any mix of a and b" and "any number of blocks, each a run of a followed by a run of b" are two such patterns. The question is how to tell, for any two patterns, whether they always agree.

Trying strings one by one never ends, so the checkers run two machines side by side, one for each pattern, and follow every way they can move together. If at some point one machine accepts and the other does not, the letters read so far form a string on which the patterns disagree. If no such point can be reached, they are equivalent. The number of situations to follow can grow exponentially with the size of the patterns, and complexity theory says this cannot be avoided in general.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Let $m$ be the sum of the sizes of $r$ and $s$, counted as nodes of their syntax trees.

**Input.** A finite alphabet $\Sigma$ and regular expressions $r$ and $s$ over $\Sigma$.

**Output.** Yes if $L(r) = L(s)$, no otherwise; in the "no" case, optionally a *witness*, a string in the symmetric difference $L(r) \mathbin{\triangle} L(s)$, preferably a shortest one.

Two expressions are equivalent exactly when they are equal as elements of the algebra of regular languages, so the problem is also the word problem for that algebra.

## Variants

- **Inclusion.** Is $L(r) \subseteq L(s)$? Equivalence is two inclusions, and inclusion has the same complexity ([regex inclusion](/regex-inclusion/)).
- **Universality.** Is $r \equiv \Sigma^*$? A special case that is already PSPACE-complete ([regex universality](/regex-universality/)).
- **Automata.** For NFAs the problem has the same complexity ([NFA equivalence](/nfa-equivalence/)). For DFAs it takes almost linear time by the union-find algorithm of [Hopcroft and Karp](/hopcroft-karp-equivalence/) ([DFA equivalence](/dfa-equivalence/)).
- **One letter.** Over $\Sigma = \{a\}$, inequivalence is NP-complete and equivalence coNP-complete (Stockmeyer and Meyer, 1973).
- **No star.** Expressions without star denote finite sets of strings, and inequivalence is NP-complete (Stockmeyer and Meyer, 1973): a witness is a string no longer than the expressions, and membership is easy to check.
- **More operators.** With a squaring operator equivalence is EXPSPACE-complete, and with complement it is non-elementary ([extended regular expressions](/extended-regular-expressions/)).
- **Restricted classes.** For unambiguous expressions it is polynomial (Stearns and Hunt, 1985), and for deterministic expressions, whose [Glushkov automaton](/glushkov-automaton/) is a DFA, it reduces to DFA equivalence.
- **Practical syntax.** Character classes, $r^+$, $r?$ and bounded repetition expand into the core syntax, the last one with an increase in size that is exponential in the number of digits of the bounds, close to the case of squaring. Backreferences go beyond regular languages, and the automaton methods do not apply to them; lookaround stays within regular languages but must first be compiled away ([lookaround](/regex-lookaround/)).

## Examples

The table was checked by a script that searched pairs of subsets of the two [Glushkov automata](/glushkov-automaton/) in breadth-first order, and against the lists of all strings of length at most 9.

| $r$ | $s$ | equivalent? | shortest witness |
|---|---|---|---|
| $(a \mid b)^*$ | $(a^* b^*)^*$ | yes | none |
| $(a \mid b)^*$ | $(a^* b)^* a^*$ | yes | none |
| $(ab)^* a$ | $a (ba)^*$ | yes | none |
| $a^*$ | $(aa)^* (\varepsilon \mid a)$ | yes | none |
| $(aa \mid aaa)^*$ | $\varepsilon \mid aa\, a^*$ | yes | none |
| $(a \mid ab)^*$ | $(a \mid ba)^*$ | no | $ab$ |
| $a^* b^* \mid b^* a^*$ | $(a \mid b)^*$ | no | $aba$ |
| $(a \mid b)^* abb$ | $(a \mid b)^* bb$ | no | $bb$ |

The first two rows are the denesting law $(x \mid y)^* \equiv (x^* y^*)^* \equiv (x^* y)^* x^*$, the third is the sliding law $(xy)^* x \equiv x (yx)^*$, and the fifth says that every length except 1 is a sum of 2s and 3s.

**A check by derivatives.** Let $r = (ab)^* a$ and $s = a (ba)^*$. The [Brzozowski derivative](/brzozowski-derivatives/) $\partial_c$ removes a first symbol $c$. Start from the pair $(r, s)$ and take derivatives of both sides by each symbol:

| pair | both nullable? | by $a$ | by $b$ |
|---|---|---|---|
| $((ab)^* a,\; a(ba)^*)$ | no, no | $(b(ab)^* a \mid \varepsilon,\; (ba)^*)$ | $(\emptyset, \emptyset)$ |
| $(b(ab)^* a \mid \varepsilon,\; (ba)^*)$ | yes, yes | $(\emptyset, \emptyset)$ | $((ab)^* a,\; a(ba)^*)$, seen |
| $(\emptyset, \emptyset)$ | no, no | seen | seen |

Every pair agrees on whether it accepts the empty string, and the set of pairs is closed under derivatives. That set is a bisimulation, so $r \equiv s$.

## Known algorithms

| method | time in the worst case | notes |
|---|---|---|
| Minimal DFAs | $2^{O(m)}$ | build, minimize, compare up to renaming |
| Search over pairs of subsets | $2^{O(m)}$ | on the fly, gives a shortest witness |
| Hopcroft-Karp on subsets, up to congruence | $2^{O(m)}$ | often explores far fewer pairs |
| Derivatives of expressions | $2^{O(m)}$ pairs | no automaton needed |
| Nondeterministic search with Savitch | space $O(m^2)$ | the PSPACE upper bound |

- **Minimal DFAs.** Convert $r$ and $s$ to DFAs by the [subset construction](/subset-construction/), minimize them ([DFA minimization](/dfa-minimization/)), and check that the minimal DFAs are the same up to renaming of states. Simple, but it builds both DFAs in full, which can have $2^{\Omega(m)}$ states ([state blowup](/regex-dfa-state-blowup/)).
- **Search over pairs of subsets.** Build NFAs $N_r$ and $N_s$ with $O(m)$ states. Search, in breadth-first order, the pairs $(S, T)$ of subsets that one string leads to in the two NFAs, starting from the pair of start sets and following each symbol. The expressions differ if and only if some reachable pair has exactly one side containing an accepting state, and breadth-first order gives a shortest witness. Only the reachable part of the product of the two DFAs is built, and the search stops at the first disagreement.
- **Hopcroft-Karp and up to congruence.** Hopcroft and Karp (1971) test DFA equivalence by merging the two states of each pair into one class with [union-find](/disjoint-set/) and skipping pairs that are already in the same class. Applied to the subsets of NFA states, it is a bisimulation up to equivalence. Bonchi and Pous (2013) also skip pairs that follow from the pairs found so far by unions of sets, a bisimulation up to congruence, and they show families on which this explores exponentially fewer pairs than the plain search or the antichain methods.
- **Derivatives.** Brzozowski (1964) showed that each expression has finitely many derivatives up to associativity, commutativity and idempotence of union. Exploring the pairs $(\partial_w r, \partial_w s)$ and checking that the two sides agree on $\varepsilon$, as in the example above, decides equivalence. [Antimirov's partial derivatives](/antimirov-derivatives/) give sets of at most $m + 1$ expressions in place of single expressions and keep the pairs small.
- **Axioms.** Salomaa (1966) and Kozen (1994) gave finite sets of equations and rules from which every true equivalence can be derived, the axioms of [Kleene algebra](/kleene-algebra/) in Kozen's version. A derivation is a certificate that a proof assistant can check, but finding one is no easier than the problem, and the decision procedures in proof assistants run one of the algorithms above.
- **Polynomial space.** Guess a witness one symbol at a time and keep only the current pair $(S, T)$ and a counter. This puts inequivalence in NPSPACE, which equals PSPACE by [Savitch's theorem](/savitch-theorem/).

## Bounds

- **Complexity class.** PSPACE-complete for $\lvert\Sigma\rvert \ge 2$, already for expressions of star height 1 ([PSPACE-completeness of regex equivalence](/regex-equivalence-pspace-completeness/)). coNP-complete for one letter, and coNP-complete without star.
- **Time.** $2^{O(m)}$ by the search over pairs of subsets: there are at most $2^{O(m)}$ pairs, and each step costs time polynomial in $m$. No polynomial algorithm exists unless P = PSPACE.
- **Witnesses.** A shortest witness has length less than the number of pairs of subsets, $2^{O(m)}$. It can be superpolynomially long in $m$; the expressions with primes on the [universality](/regex-universality/) page give an example, compared with $a^*$.
- **Restricted cases.** Polynomial for DFAs, for unambiguous expressions, and for deterministic expressions.

## Reductions

- **From universality.** $L(r) = \Sigma^*$ if and only if $r \equiv (a_1 \mid \cdots \mid a_k)^*$ for $\Sigma = \{a_1, \ldots, a_k\}$. So equivalence is PSPACE-hard.
- **To inclusion.** $r \equiv s$ if and only if $L(r) \subseteq L(s)$ and $L(s) \subseteq L(r)$.
- **To NFA equivalence and back.** Expressions convert to NFAs in linear time ([regex to NFA conversion](/regex-to-nfa-conversion/)), and both problems are PSPACE-complete, so each reduces to the other in polynomial time.
- **Not to emptiness.** $r \equiv s$ is emptiness of $(L(r) \setminus L(s)) \cup (L(s) \setminus L(r))$, but writing that set as an expression needs complement, which can cost an exponential, so the linear test for [emptiness](/regex-emptiness/) does not help.

## Applications

- **Checking rewrites of patterns.** Tools that simplify or optimize patterns, and people who refactor them, can check that the new pattern accepts the same strings, and get a string that shows the difference when it does not.
- **Teaching tools.** Systems that grade exercises on regular expressions and automata compare the answer with a reference expression and show a witness when they differ.
- **Program equivalence.** [Kleene algebra with tests](/kleene-algebra-with-tests/) extends regular expressions with Boolean tests and models simple imperative programs; equivalence of such programs reduces to equivalence of expressions, and the algorithms above, in particular bisimulation up to congruence, decide it.
- **Minimizing expressions.** Searching for a smaller equivalent expression needs an equivalence test for each candidate ([regex minimization](/regex-minimization/)).

## References
