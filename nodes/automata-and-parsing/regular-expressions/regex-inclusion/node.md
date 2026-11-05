---
tag: 5GV812
kind: problem
slug: regex-inclusion
name: Regex inclusion
aliases:
- containment of regular expressions
area: automata-and-parsing/regular-expressions
level: advanced
summary: Decide whether the language of one regex is contained in that of another.
prereqs: [regular-expression, nfa-universality, pspace]
see_also: [regex-equivalence, regex-equivalence-pspace-completeness, regex-universality, regex-emptiness, product-construction, subset-construction, nfa-equivalence, co-np]
sources:
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (the encoding of space-bounded computations; universality, and so inclusion, is PSPACE-hard)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (the cases without star and over a one-letter alphabet)
  - paper: "Martin De Wulf, Laurent Doyen, Thomas A. Henzinger and Jean-Francois Raskin, Antichains: a new algorithm for checking universality of finite automata, Computer Aided Verification (CAV 2006), Lecture Notes in Computer Science 4144"
    locator: pp. 17 to 30 (antichains for universality and for language inclusion)
  - paper: "Parosh A. Abdulla, Yu-Fang Chen, Lukáš Holík, Richard Mayr and Tomáš Vojnar, When simulation meets antichains, TACAS 2010, Lecture Notes in Computer Science 6015"
    locator: pp. 158 to 174 (pruning the antichain search for inclusion with simulation relations)
  - paper: doi:10.1145/2429069.2429124
    title: Filippo Bonchi and Damien Pous, Checking NFA equivalence with bisimulations up to congruence, 40th ACM Symposium on Principles of Programming Languages (POPL 2013)
    locator: pp. 457 to 468 (the algorithm HKC and its use for language inclusion)
  - paper: "Richard E. Stearns and Harry B. Hunt III, On the equivalence and containment problems for unambiguous regular expressions, regular grammars and finite automata, SIAM Journal on Computing 14(3) (1985)"
    locator: pp. 598 to 611 (polynomial containment for unambiguous expressions and automata)
  - paper: "Haruo Hosoya, Jérôme Vouillon and Benjamin C. Pierce, Regular expression types for XML, ACM Transactions on Programming Languages and Systems 27(1) (2005)"
    locator: pp. 46 to 90 (subtyping as inclusion of regular expression types, decided with tree automata)
---

Regex inclusion is the problem of deciding, for two [regular expressions](/regular-expression/) $r$ and $s$, whether $L(r) \subseteq L(s)$: every string that $r$ describes is also described by $s$. It is PSPACE-complete in general, like [equivalence](/regex-equivalence/), which is two inclusions. Unlike equivalence it is asymmetric: the search for a counterexample needs to determinize only $s$, so the cost is exponential in the size of $s$ and polynomial in the size of $r$, and when $s$ is deterministic the problem is polynomial.

## In plain words

One pattern is included in another when every string that fits the first also fits the second. To show that it is not, it is enough to find one string that fits the first pattern and not the second.

A checker runs a machine for each pattern on the same letters. For the first pattern it can follow one path at a time and guess where to go. For the second it must keep the set of all places the machine could be in, because a string fails the second pattern only if every path through it fails. A counterexample is found when the first machine accepts and the set for the second contains no accepting place. The sets make the search expensive, and only the second pattern produces them.

## Definition

The expressions use the syntax of the [regular expression](/regular-expression/) page: symbols of $\Sigma$, $\varepsilon$, $\emptyset$, union $\mid$, concatenation and star $^*$. Let $m_r$ and $m_s$ be the sizes of $r$ and $s$ and $m = m_r + m_s$.

**Input.** A finite alphabet $\Sigma$ and regular expressions $r$ and $s$ over $\Sigma$.

**Output.** Yes if $L(r) \subseteq L(s)$, no otherwise; in the "no" case, optionally a *counterexample* $w \in L(r) \setminus L(s)$.

## Variants

- **Equivalence.** $r \equiv s$ if and only if both inclusions hold ([regex equivalence](/regex-equivalence/)).
- **Universality.** $L(s) = \Sigma^*$ is the inclusion $\Sigma^* \subseteq L(s)$, with a fixed left side ([regex universality](/regex-universality/)).
- **Emptiness.** $L(r) = \emptyset$ is the inclusion $L(r) \subseteq L(\emptyset)$, with a fixed right side, and takes linear time ([regex emptiness](/regex-emptiness/)).
- **Deterministic right side.** If $s$ is given as a DFA, or is a deterministic expression whose [Glushkov automaton](/glushkov-automaton/) is a DFA, the problem is polynomial: complement the DFA by swapping accepting and rejecting states, and test emptiness of its product with an NFA for $r$ ([product construction](/product-construction/)).
- **Unambiguous expressions.** Inclusion is polynomial for unambiguous expressions and automata (Stearns and Hunt, 1985).
- **No star on the left.** If $r$ has no star, every string of $L(r)$ is no longer than $r$, and a counterexample is checked in polynomial time by [regex matching](/regex-matching/). So the problem is in [coNP](/co-np/), and the example below shows that it is coNP-complete.
- **One letter.** Over $\Sigma = \{a\}$ it is coNP-complete (Stockmeyer and Meyer, 1973).
- **Practical syntax.** Character classes, $r^+$, $r?$ and bounded repetition expand into the core syntax. Backreferences go beyond regular languages and the automaton methods do not apply to them.

## Examples

The table was checked by a script that searched the pairs of subsets of the two [Glushkov automata](/glushkov-automaton/), and against the lists of all strings of length at most 9.

| $r$ | $s$ | $L(r) \subseteq L(s)$? | shortest counterexample |
|---|---|---|---|
| $(ab)^*$ | $(a \mid b)^* b \mid \varepsilon$ | yes | none |
| $a (ba)^* b$ | $(ab)^*$ | yes | none |
| $(a \mid b)^* abb$ | $(a \mid b)^* bb$ | yes | none |
| $(a \mid b)^* bb$ | $(a \mid b)^* abb$ | no | $bb$ |
| $(a \mid b)^* a$ | $(a \mid b)^* b$ | no | $a$ |

The third and fourth rows show the asymmetry: the strings that end in $abb$ all end in $bb$, but not the other way round.

**Inclusion encodes unsatisfiability.** Take a formula in conjunctive normal form over $x_1, \ldots, x_n$, and read a string of $\{0, 1\}^n$ as an assignment. For each clause write an expression of the assignments that make it false: position $i$ is $0$ if $x_i$ is in the clause, $1$ if $\neg x_i$ is, and $(0 \mid 1)$ otherwise. Let $s$ be the union of these expressions and $r = (0 \mid 1)^n$. Then $L(r) \subseteq L(s)$ if and only if every assignment falsifies some clause, that is, if and only if the formula is unsatisfiable. For
$$(x_1 \vee x_2)(\neg x_1 \vee x_3)(\neg x_2 \vee \neg x_3)(\neg x_1 \vee \neg x_3)$$
the expression is $s = 00(0 \mid 1) \mid 1(0 \mid 1)0 \mid (0 \mid 1)11 \mid 1(0 \mid 1)1$, and the search finds the counterexample $010$, which is the only satisfying assignment. Adding the clause $(x_1 \vee \neg x_2)$ adds the term $01(0 \mid 1)$, and then the inclusion holds. A script checked the reduction on 300 random formulas with up to 5 variables. Neither expression has a star, so inclusion of star-free expressions is coNP-hard, and coNP-complete by the variant above.

## Known algorithms

- **Search with one side determinized.** Build NFAs $N_r$ and $N_s$, the second without $\varepsilon$-moves or with $\varepsilon$-closures. Search the pairs $(q, T)$, where $q$ is a state of $N_r$ and $T$ is the set of states that $N_s$ can reach on the same string: from $(q, T)$ and a move $q \xrightarrow{a} q'$ go to $(q', T')$, where $T'$ is the set of states reached from $T$ by $a$. Inclusion fails if and only if some reachable pair has $q$ accepting and $T$ without accepting states, and [breadth-first search](/breadth-first-search/) gives a shortest counterexample. There are at most $O(m_r) \cdot 2^{O(m_s)}$ pairs, so the time is polynomial in $m_r$ and exponential only in $m_s$.
- **Antichains.** If $(q, T)$ leads to a counterexample, so does $(q, T')$ for every $T' \subseteq T$, since a smaller set of states accepts less. So the search needs to keep, for each $q$, only the minimal sets $T$ it has found (De Wulf, Doyen, Henzinger and Raskin, 2006). Abdulla, Chen, Holík, Mayr and Vojnar (2010) prune more with simulation relations between states. The worst case stays exponential, but the savings in practice are large.
- **Bisimulation up to congruence.** The algorithm of Bonchi and Pous (2013) for equivalence also decides inclusion, since $L(r) \subseteq L(s)$ if and only if $L(r) \cup L(s) = L(s)$, that is, $r \mid s \equiv s$.
- **Through equivalence.** For the same reason, any algorithm for [equivalence](/regex-equivalence/) decides inclusion with one call. This loses the asymmetry, since it determinizes both sides.
- **Polynomial space.** Guess a counterexample one symbol at a time, keeping $q$, $T$ and a counter, and apply [Savitch's theorem](/savitch-theorem/).

## Bounds

- **General case.** PSPACE-complete for $\lvert\Sigma\rvert \ge 2$: universality is the special case $\Sigma^* \subseteq L(s)$ and is PSPACE-hard ([PSPACE-completeness of regex equivalence](/regex-equivalence-pspace-completeness/)), and the search above runs in polynomial space.
- **Time.** $O(m_r) \cdot 2^{O(m_s)}$ times a polynomial in $m$. So the problem is fixed-parameter tractable in the size of $s$, and polynomial whenever $m_s = O(\log m_r)$.
- **Fixed sides.** With $s$ fixed the problem takes linear time in $m_r$, since $s$ has a fixed DFA. With $r$ fixed it can stay PSPACE-hard, as $r = (0 \mid 1)^*$ shows.
- **Without star or over one letter.** coNP-complete.
- **Counterexamples.** A shortest counterexample can be superpolynomially long in $m$, as for universality.

## Reductions

- **From universality and from unsatisfiability.** As above.
- **To equivalence.** $L(r) \subseteq L(s)$ if and only if $r \mid s \equiv s$, a linear-size reduction.
- **From equivalence.** Two calls, one for each direction.
- **To emptiness with a deterministic right side.** $L(r) \subseteq L(D)$ for a DFA $D$ is emptiness of $L(r) \cap \overline{L(D)}$.

## Applications

- **Types for strings and documents.** In languages with regular expression types for XML, one type is a subtype of another when its language is included in the other's, so type checking runs inclusion tests (Hosoya, Vouillon and Pierce, 2005). The tests are on tree automata, which generalize the string case.
- **Schema evolution.** A new version of a schema accepts every old document when each content model of the old version is included in the new one.
- **Validators and sanitizers.** Checking that every string a validator accepts is safe is the inclusion of the validator's pattern in a pattern of safe strings, and a counterexample is an input that slips through.
- **Model checking.** In automata-based verification, a system satisfies a specification when the language of its behaviors is included in that of the specification; antichain algorithms were designed for this setting.

## References
