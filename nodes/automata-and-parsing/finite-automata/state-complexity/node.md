---
tag: PW04PE
kind: concept
slug: state-complexity
name: State complexity
aliases:
- state complexity of operations
- descriptional complexity of regular languages
area: automata-and-parsing/finite-automata
level: advanced
summary: Measure of the number of states needed to recognize the result of a regular-language operation.
prereqs: [deterministic-finite-automaton, myhill-nerode-theorem, regular-language]
see_also: [product-construction, subset-construction, rabin-scott-theorem, nfa-minimization, fooling-set-method, regular-language-intersection, two-way-finite-automaton, determinization-blowup-lower-bound]
sources:
  - paper: doi:10.1016/0304-3975(92)00011-F
    title: Sheng Yu, Qingyu Zhuang and Kai Salomaa, The state complexities of some basic operations on regular languages, Theoretical Computer Science 125(2) (1994)
    locator: pp. 315 to 328 (the tight bounds for union, intersection, concatenation, star, reversal and quotients, and the unary case)
  - paper: "Markus Holzer and Martin Kutrib, Nondeterministic descriptional complexity of regular languages, International Journal of Foundations of Computer Science 14(6) (2003)"
    locator: pp. 1087 to 1102 (the tight bounds on the number of NFA states for the operations)
  - paper: "Marek Chrobak, Finite automata and unary languages, Theoretical Computer Science 47 (1986)"
    locator: pp. 149 to 158 (unary NFAs and their DFAs)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.3.6, A Bad Case for the Subset Construction, and Section 4.4, Equivalence and Minimization of Automata
---

The state complexity of a [regular language](/regular-language/) $L$ is the number of states of its minimal complete [DFA](/deterministic-finite-automaton/), and the state complexity of an operation on regular languages is the largest state complexity of its result, as a function of the state complexities of its arguments. For example, intersection has state complexity $mn$, concatenation $m 2^n - 2^{n - 1}$, and reversal $2^n$ (Yu, Zhuang and Salomaa, 1994). The same questions for NFAs give the *nondeterministic* state complexity, with very different values (Holzer and Kutrib, 2003).

## In plain words

A machine that recognizes a set of strings needs a certain least number of states, and this number measures how complex the set is. When you combine two sets, for example by taking the strings in both, or by gluing a string of one onto a string of the other, the result can need more states than the parts.

State complexity asks: in the worst case, how many states does the result need? The answer is an exact formula in the sizes of the parts. To prove it, you show a construction that never needs more, and you find example sets that need every one of those states. The answers tell you which operations are cheap, like taking the opposite set, and which can explode, like reversing the strings.

## The idea

**Definition.** For a regular language $L$, $\mathrm{sc}(L)$ is the number of states of the minimal complete DFA of $L$, which by the [Myhill-Nerode theorem](/myhill-nerode-theorem/) is the number of classes of the Myhill-Nerode relation of $L$. The value $\mathrm{nsc}(L)$ is the least number of states of an NFA for $L$ (with one start state and no $\varepsilon$-moves), see [NFA minimization](/nfa-minimization/). For a binary operation $\circ$, its state complexity is

$$f_\circ(m, n) = \max \{ \mathrm{sc}(L_1 \circ L_2) : \mathrm{sc}(L_1) \le m,\ \mathrm{sc}(L_2) \le n \},$$

with the maximum over all alphabets unless an alphabet is fixed; a unary operation has a function of one argument. A bound is *tight* when witness languages reach it.

**Two halves of each result.** An upper bound comes from a construction: the [product construction](/product-construction/) for Boolean operations, or a [subset construction](/subset-construction/) for reversal, concatenation and star. A lower bound needs witnesses $L_1, L_2$, and a proof that all states of the construction are reachable and pairwise distinguishable, which by the Myhill-Nerode theorem gives the exact value.

**Example of an upper bound proof: concatenation.** Let $D_1 = (Q_1, \Sigma, \delta_1, s_1, F_1)$ and $D_2 = (Q_2, \Sigma, \delta_2, s_2, F_2)$ be complete DFAs with $m$ and $n$ states, with $F_1 \ne \emptyset$ (else $L_1 L_2 = \emptyset$ and one state suffices). The subset construction on the NFA for $L_1 L_2$ gives states $(q, S)$ with $q \in Q_1$ and $S \subseteq Q_2$, where $S$ is the set of states of $D_2$ that are active. Whenever $q \in F_1$, the state $s_2$ is in $S$, since a new copy of $D_2$ starts. So the reachable states number at most $m 2^n - |F_1| \cdot 2^{n - 1} \le m 2^n - 2^{n - 1}$.

**Deterministic state complexity.** For $m, n \ge 2$ unless noted, from Yu, Zhuang and Salomaa (1994), except complement, which is direct:

| operation | $f(m, n)$ or $f(n)$ | upper bound by |
|---|---|---|
| complement $\overline{L}$ | $n$ | swapping $F$ and $Q \setminus F$ |
| union $L_1 \cup L_2$ | $mn$ | product |
| intersection $L_1 \cap L_2$ | $mn$ | product |
| concatenation $L_1 L_2$ | $m 2^n - 2^{n - 1}$ | pairs $(q, S)$ as above |
| star $L^*$ | $2^{n - 1} + 2^{n - 2}$ | subsets of $Q$ with a fresh start |
| reversal $L^R$ | $2^n$ | subset construction on the reversed NFA |

**Nondeterministic state complexity.** From Holzer and Kutrib (2003), for NFAs with $m$ and $n$ states: union $m + n + 1$, intersection $mn$, concatenation $m + n$, star $n + 1$, reversal $n + 1$, and complement $2^n$, all tight. Complement is the expensive operation here, the reverse of the deterministic case, because it needs [determinization](/nfa-determinization/).

**Unary languages.** Over one letter the values are smaller. A unary minimal DFA is a tail followed by a cycle, so the cycle lengths control the results: for example, intersecting $\{a^k : m \mid k\}$ with $\{a^k : n \mid k\}$ gives $\{a^k : \mathrm{lcm}(m, n) \mid k\}$, with $\mathrm{lcm}(m, n)$ states, which is $mn$ for coprime $m$ and $n$. Converting a unary NFA with $n$ states to a DFA costs $e^{\Theta(\sqrt{n \ln n})}$ states (Chrobak, 1986), not $2^n$.

**Composed operations.** The state complexity of a combination, such as $(L_1 \cup L_2)^*$, is in general smaller than the composition of the individual bounds, because the witnesses for one operation are not the worst case input for the next. Each combination needs its own analysis.

## Examples

**Intersection reaches $mn$.** Over $\{a, b\}$, let $L_1$ count the $a$s modulo $m$ and $L_2$ count the $b$s modulo $n$, each accepting at 0. The $mn$ strings $a^i b^j$ ($0 \le i < m$, $0 \le j < n$) are pairwise distinguishable for $L_1 \cap L_2$, so it needs $mn$ states. The same strings show that $L_1 \cup L_2$ needs $mn$ states. Details are on the [regular language intersection](/regular-language-intersection/) page.

**Reversal reaches $2^n$.** The language "the $n$-th symbol from the end is $a$" has a minimal DFA with $2^n$ states, while its reversal, "the $n$-th symbol from the start is $a$", has $n + 2$ states (a chain of $n$ states, an accepting sink and a dead state). Read in the other direction, this gives a language with $n + 2$ states whose reversal needs $2^n$, close to the bound $2^n$ for $n + 2$ states but not equal to it. Witnesses with exactly $n$ states whose reversal needs $2^n$ states also exist, as the search below shows for $n = 3$.

**Small cases by exhaustive search.** Over $\{a, b\}$, among all complete DFAs with 3 states, the largest minimal DFA for the star has $6 = 2^2 + 2^1$ states, and the largest for the reversal has $8 = 2^3$. Among pairs of 2-state DFAs, the largest minimal DFA for the concatenation has $6 = 2 \cdot 2^2 - 2^1$ states. These match the formulas of the table.

**A cheap operation.** Complement never costs more: $\mathrm{sc}(\overline{L}) = \mathrm{sc}(L)$, since swapping accepting and non-accepting states of a complete DFA gives a complete DFA for the complement, and the swap is its own inverse.

## Where it is used

- **Size of automata in tools.** Libraries for regular expressions, model checkers and lexer generators combine automata by these operations, and the bounds predict when a result can grow out of memory: products grow as $mn$, and reversal or concatenation can grow exponentially.
- **Lower bounds for algorithms.** An algorithm that must output a DFA for $L_1 L_2$ or $L^R$ takes exponential time in the worst case, since the output alone is that large.
- **Comparing models.** State complexity measures the succinctness of NFAs, [two-way automata](/two-way-finite-automaton/), [unambiguous NFAs](/unambiguous-nfa/) and regular expressions against DFAs, as in the [Rabin-Scott theorem](/rabin-scott-theorem/) and the [determinization blowup](/determinization-blowup-lower-bound/).
- **Lower bound techniques.** Myhill-Nerode classes give exact DFA bounds, and [fooling sets](/fooling-set-method/) give NFA bounds.

## References
