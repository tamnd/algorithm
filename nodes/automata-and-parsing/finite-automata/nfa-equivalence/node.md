---
tag: TJXAJ6
kind: problem
slug: nfa-equivalence
name: NFA equivalence
aliases:
- equivalence problem for NFAs
- NFA language equivalence
area: automata-and-parsing/finite-automata
level: advanced
summary: Decide whether two NFAs recognize the same language; PSPACE-complete.
model: word-ram
complexity:
  vars: {n: the total number of states of the two NFAs, m: the total number of transitions, σ: the alphabet size}
  time: {worst: O(2^n σ(n + m))}
prereqs: [nondeterministic-finite-automaton, subset-construction, nfa-universality]
see_also: [dfa-equivalence, hopcroft-karp-equivalence, product-construction, bisimulation, regex-equivalence-pspace-completeness, regex-inclusion, unambiguous-nfa, equivalence-checking]
sources:
  - paper: "Albert R. Meyer and Larry J. Stockmeyer, The equivalence problem for regular expressions with squaring requires exponential space, 13th Annual Symposium on Switching and Automata Theory (1972)"
    locator: pp. 125 to 129 (the equivalence of regular expressions, and so of NFAs, is PSPACE-hard)
  - paper: "Larry J. Stockmeyer and Albert R. Meyer, Word problems requiring exponential time, Fifth Annual ACM Symposium on Theory of Computing (STOC 1973)"
    locator: pp. 1 to 9 (inequivalence of regular expressions over a one-letter alphabet is NP-complete)
  - paper: "Filippo Bonchi and Damien Pous, Checking NFA equivalence with bisimulations up to congruence, 40th ACM Symposium on Principles of Programming Languages (POPL 2013)"
    locator: pp. 457 to 468 (the algorithms HK and HKC, and the comparison with antichains)
  - paper: "Martin De Wulf, Laurent Doyen, Thomas A. Henzinger and Jean-Francois Raskin, Antichains: a new algorithm for checking universality of finite automata, Computer Aided Verification (CAV 2006), Lecture Notes in Computer Science 4144"
    locator: pp. 17 to 30 (antichains for universality and for language inclusion)
  - paper: "Richard E. Stearns and Harry B. Hunt III, On the equivalence and containment problems for unambiguous regular expressions, regular grammars and finite automata, SIAM Journal on Computing 14(3) (1985)"
    locator: pp. 598 to 611 (polynomial time equivalence and inclusion for unambiguous automata)
  - paper: "John E. Hopcroft and Richard M. Karp, A linear algorithm for testing equivalence of finite automata, Technical Report 71-114, Cornell University (1971)"
    locator: the algorithm that merges pairs of states with union-find
---

NFA equivalence is the problem of deciding, for two [nondeterministic finite automata](/nondeterministic-finite-automaton/) $N_1$ and $N_2$ over one alphabet, whether $L(N_1) = L(N_2)$. It is [PSPACE](/pspace/)-complete (Meyer and Stockmeyer, 1972), since [NFA universality](/nfa-universality/) is the special case where one NFA accepts every string. The standard algorithms determinize both NFAs on the fly and search the pairs of subsets for a string that exactly one of them accepts; Hopcroft and Karp's merging and its improvement up to congruence (Bonchi and Pous, 2013) often avoid most of the pairs.

## In plain words

Two machines are equivalent when they say yes to exactly the same strings, even if they look very different inside. To show that they are not equivalent, one string that one machine accepts and the other rejects is enough.

Both machines are nondeterministic, so after some input each one is in a set of possible states. Run both on the same letters and keep the pair of sets. If you reach a pair where exactly one of the sets contains an accepting state, the letters so far give a string on which the machines differ. If you run out of new pairs, they are equivalent. The number of pairs can be huge, and no known method avoids that in all cases.

## Definition

**Input.** Two NFAs $N_i = (Q_i, \Sigma, \delta_i, q_i, F_i)$, $i = 1, 2$, over one alphabet $\Sigma$, with $\delta_i : Q_i \times \Sigma \to \mathcal{P}(Q_i)$, one start state each, and no $\varepsilon$-moves. They need not be complete. Let $n = |Q_1| + |Q_2|$, $m$ the total number of transitions, and $\sigma = |\Sigma|$.

**Question.** Is $L(N_1) = L(N_2)$?

A *distinguishing string* is a $w$ in the symmetric difference $L(N_1) \triangle L(N_2)$. For a pair of sets $(X, Y)$ with $X \subseteq Q_1$ and $Y \subseteq Q_2$, call the pair *bad* if exactly one of $X \cap F_1$ and $Y \cap F_2$ is non-empty. Then $w$ is distinguishing if and only if the pair $(\delta_1^*(\{q_1\}, w), \delta_2^*(\{q_2\}, w))$ is bad.

## Variants

- **Inclusion.** Is $L(N_1) \subseteq L(N_2)$? Equivalence is two inclusions, and inclusion is the special case of equivalence $L(N_1) \cup L(N_2) = L(N_2)$, where the union of two NFAs is one NFA with a new start state. Both are PSPACE-complete.
- **DFAs.** For DFAs the problem is in polynomial time: [DFA equivalence](/dfa-equivalence/) by the [product construction](/product-construction/) in $O(n^2 \sigma)$ or by [Hopcroft and Karp's algorithm](/hopcroft-karp-equivalence/) in almost linear time.
- **One NFA and one DFA.** If $N_2$ is a DFA, inclusion $L(N_1) \subseteq L(N_2)$ is in polynomial time (search the product of $N_1$ with the complement of $N_2$), but equivalence stays PSPACE-hard, since universality is the case where $N_2$ is the one-state DFA for $\Sigma^*$.
- **Unambiguous NFAs.** For [unambiguous NFAs](/unambiguous-nfa/), equivalence and inclusion are in polynomial time (Stearns and Hunt, 1985).
- **One-letter alphabet.** For $\Sigma = \{a\}$, the problem is coNP-complete (Stockmeyer and Meyer, 1973).
- **Regular expressions.** [Regex equivalence](/regex-equivalence-pspace-completeness/) is PSPACE-complete as well, and becomes EXPSPACE-complete when a squaring operator is allowed (Meyer and Stockmeyer, 1972).

## Examples

**An NFA and a DFA for one language.** Let $N_1$ accept the strings over $\{a, b\}$ whose second symbol from the end is $a$: states 0, 1, 2, start 0, $F_1 = \{2\}$, $\delta_1(0, a) = \{0, 1\}$, $\delta_1(0, b) = \{0\}$, $\delta_1(1, a) = \delta_1(1, b) = \{2\}$, and no moves from 2. Let $D$ be the 4-state DFA that remembers the last two symbols: states 0 to 3, start 0, $F = \{2, 3\}$, with $0 \xrightarrow{a} 1$, $0 \xrightarrow{b} 0$, $1 \xrightarrow{a} 2$, $1 \xrightarrow{b} 3$, $2 \xrightarrow{a} 2$, $2 \xrightarrow{b} 3$, $3 \xrightarrow{a} 1$, $3 \xrightarrow{b} 0$. The search meets four pairs and none is bad, so the languages are equal:

| string | set of $N_1$ | state of $D$ | bad |
|---|---|---|---|
| $\varepsilon$ | $\{0\}$ | 0 | no |
| $a$ | $\{0, 1\}$ | 1 | no |
| $aa$ | $\{0, 1, 2\}$ | 2 | no |
| $ab$ | $\{0, 2\}$ | 3 | no |

**A small change.** Let $N_2$ be $N_1$ with the loops $2 \xrightarrow{a} 2$ and $2 \xrightarrow{b} 2$ added, so $L(N_2) = \Sigma^* a \Sigma \Sigma^*$: the strings with an $a$ that is not the last symbol. The search from $(\{0\}, \{0\})$ meets $(\{0, 1\}, \{0, 1\})$ on $a$, $(\{0, 1, 2\}, \{0, 1, 2\})$ on $aa$, $(\{0, 2\}, \{0, 2\})$ on $ab$, and then the bad pair $(\{0, 1\}, \{0, 1, 2\})$ on $aba$. So $aba$ is a shortest distinguishing string: $N_2$ accepts it, and $N_1$ does not, because its second symbol from the end is $b$.

**A long distinguishing string.** The NFA with cycles of prime lengths 2, 3, 5 and 7 on the [NFA universality](/nfa-universality/) page has 18 states, and it differs from the one-state NFA for $\{a\}^*$ only on strings $a^\ell$ with $\ell \equiv 209 \pmod{210}$. So the shortest distinguishing string has length 209.

## Known algorithms

- **Determinize and compare.** Apply the [subset construction](/subset-construction/) to both NFAs, then decide [DFA equivalence](/dfa-equivalence/). Worst case $O(2^{n} \sigma (n + m))$ for the construction, plus the comparison.
- **Search of pairs of subsets.** Search the pairs $(X, Y)$ reachable from $(\{q_1\}, \{q_2\})$ with $(X, Y) \xrightarrow{a} (\mathrm{post}_a(X), \mathrm{post}_a(Y))$, in breadth-first order, and stop at the first bad pair. This is the [product construction](/product-construction/) of the two determinized NFAs, built only as far as needed. Up to $2^{|Q_1|} \cdot 2^{|Q_2|} = 2^n$ pairs, each processed in $O(\sigma(n + m))$ time.
- **Hopcroft and Karp's merging (HK).** Keep a union-find structure on the subsets. For each pair $(X, Y)$ taken from a queue, skip it if $X$ and $Y$ are already in one class; else check that it is not bad, merge the classes, and queue the successor pairs. The final relation is a bisimulation between the two determinized automata, so the languages are equal. On DFAs this is the almost linear [Hopcroft-Karp equivalence](/hopcroft-karp-equivalence/) test.
- **Bisimulation up to congruence (HKC).** Skip a pair $(X, Y)$ also when it lies in the congruence closure of the pairs already processed: the least equivalence relation that contains them and is closed under $(X_1, Y_1), (X_2, Y_2) \mapsto (X_1 \cup X_2, Y_1 \cup Y_2)$. This is sound for determinized NFAs because the language of $X_1 \cup X_2$ is the union of the languages of $X_1$ and $X_2$. Bonchi and Pous (2013) give families of NFAs on which HKC processes exponentially fewer pairs than HK and than antichains.
- **Antichains for inclusion.** For $L(N_1) \subseteq L(N_2)$, search pairs $(p, Y)$ with $p \in Q_1$ and $Y \subseteq Q_2$, and drop $(p, Y)$ when a pair $(p, Y')$ with $Y' \subseteq Y$ is already present (De Wulf, Doyen, Henzinger and Raskin, 2006). A counterexample is a pair with $p \in F_1$ and $Y \cap F_2 = \emptyset$.
- **Polynomial space.** Guess a distinguishing string symbol by symbol and keep only the current pair of sets: $O(n)$ space nondeterministically, so $O(n^2)$ deterministic space by [Savitch's theorem](/savitch-theorem/).

## Bounds

**Complexity class.** NFA equivalence is in PSPACE by the polynomial space algorithm, and PSPACE-hard because universality reduces to it (Meyer and Stockmeyer, 1972; the reduction is on the [NFA universality](/nfa-universality/) page). So it is PSPACE-complete, and, unless P = PSPACE, no algorithm runs in time polynomial in $n$.

**Length of a shortest distinguishing string.** If one exists, there is one of length less than $2^n$: along a shortest distinguishing string, the pairs of sets after its prefixes are pairwise distinct, since a repeated pair would give a shorter one, and there are at most $2^{|Q_1|} \cdot 2^{|Q_2|} = 2^n$ pairs. The prime-cycle example shows that the length can be $e^{\Theta(\sqrt{n \log n})}$ even over one letter. For two complete DFAs, a shortest distinguishing string has length at most $n - 2$, by [Moore's](/moore-minimization/) refinement on the disjoint union.

**Time.** The pair search runs in $O(2^n \sigma (n + m))$ time on the [word RAM](/word-ram/) in the worst case, with hashing of the pairs.

**Special cases.** Polynomial for DFAs and for unambiguous NFAs. coNP-complete for one letter. Inclusion of an NFA in a DFA is in polynomial time.

## Reductions

- **From universality.** $L(N) = \Sigma^*$ if and only if $N$ is equivalent to the one-state NFA with a loop on each symbol. This gives PSPACE-hardness.
- **To universality.** $L(N_1) \subseteq L(N_2)$ if and only if $\overline{L(N_1)} \cup L(N_2) = \Sigma^*$. This needs the complement of $N_1$, so a determinization, and is not a polynomial reduction; but both problems are in PSPACE, so a polynomial reduction exists through the general hardness proof.
- **From regular expressions.** [Regex equivalence](/regex-equivalence-pspace-completeness/) and [regex inclusion](/regex-inclusion/) reduce to this problem by the [Thompson construction](/thompson-construction/).
- **To emptiness.** $L(N_1) = L(N_2)$ if and only if the symmetric difference is empty, which is [DFA emptiness](/dfa-emptiness/) of the product of the two determinized automata with the bad pairs as accepting states.

## Applications

- **Verification.** Checking that an implementation, given as an automaton, has the same traces as a specification, or a subset of them ([trace equivalence](/trace-equivalence/)).
- **Regular expressions.** Checking that a rewritten regular expression, for example a faster one, matches exactly the same strings as the original; the distinguishing string is a test case.
- **Kleene algebra.** Deciding equations of [Kleene algebra](/kleene-algebra/) and of [Kleene algebra with tests](/kleene-algebra-with-tests/) reduces to the equivalence of automata.
- **Grading and learning.** Comparing a student's automaton with a reference automaton, and answering equivalence queries in [DFA learning](/dfa-learning/).

## References
