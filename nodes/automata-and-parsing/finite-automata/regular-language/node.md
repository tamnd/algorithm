---
tag: 804C5Z
kind: definition
slug: regular-language
name: Regular language
aliases:
- rational language
- regular set
area: automata-and-parsing/finite-automata
level: intro
summary: Language recognized by a finite automaton, equivalently described by a regular expression.
prereqs: [alphabet, deterministic-finite-automaton]
see_also:
- nondeterministic-finite-automaton
- regular-expression
- kleene-theorem
- myhill-nerode-theorem
- pumping-lemma-for-regular-languages
- closure-properties-of-regular-languages
- context-free-language
- star-free-language
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.1, Finite Automata (the definition of a regular language); Section 1.3, Regular Expressions (the equivalence with finite automata); Section 1.4, Nonregular Languages
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.2 (the language of a DFA), Chapter 3, Regular Expressions and Languages, and Chapter 4, Properties of Regular Languages
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 3, Finite Automata and Regular Sets; Lectures 11 and 12 (limitations of finite automata and the pumping lemma)
  - paper: "Stephen C. Kleene, Representation of events in nerve nets and finite automata, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 3 to 41 (regular events and their equivalence with finite automata)
---

A regular language is a set of strings over a finite [alphabet](/alphabet/) that some [deterministic finite automaton](/deterministic-finite-automaton/) accepts. The same class has many other descriptions: the languages of [NFAs](/nondeterministic-finite-automaton/), of [regular expressions](/regular-expression/), of right-linear grammars, and the languages with finitely many [Myhill-Nerode classes](/myhill-nerode-relation/). Regular languages are the languages that a program can decide in one left-to-right pass with a fixed amount of memory, so they are the base of lexical analysis, of pattern search and of many checks in verification.

## Definition

Let $\Sigma$ be a finite, non-empty alphabet. A *string* over $\Sigma$ is a finite sequence $a_1 a_2 \cdots a_n$ of symbols of $\Sigma$, with $n \ge 0$; the string with $n = 0$ is the empty string $\varepsilon$. The set of all strings is $\Sigma^*$. A *language* over $\Sigma$ is a subset $L \subseteq \Sigma^*$.

**Definition.** A language $L \subseteq \Sigma^*$ is *regular* if there is a DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $L(M) = L$. The DFA is complete and has no $\varepsilon$-moves, as on the [DFA](/deterministic-finite-automaton/) page.

The definition fixes the alphabet. A language over $\Sigma$ is also a language over each larger alphabet $\Sigma' \supseteq \Sigma$, and it is regular over $\Sigma$ if and only if it is regular over $\Sigma'$: add a dead state for the new symbols in one direction, and delete the transitions on the new symbols in the other.

**Equivalent definitions.** For a language $L \subseteq \Sigma^*$ the following are equivalent.

1. Some DFA accepts $L$.
2. Some [NFA](/nondeterministic-finite-automaton/) accepts $L$. An NFA with $n$ states has an equivalent DFA with at most $2^n$ states ([Rabin-Scott theorem](/rabin-scott-theorem/)), and each DFA is an NFA.
3. Some [epsilon-NFA](/epsilon-nfa/) accepts $L$.
4. Some [regular expression](/regular-expression/) denotes $L$. In other words, $L$ is in the smallest class of languages that holds $\emptyset$, $\{\varepsilon\}$ and $\{a\}$ for each $a \in \Sigma$, and that is closed under union, concatenation and the [Kleene star](/kleene-star/). This is [Kleene's theorem](/kleene-theorem/), and the reason for the name *rational language*.
5. The [Myhill-Nerode relation](/myhill-nerode-relation/) of $L$ has finitely many classes ([Myhill-Nerode theorem](/myhill-nerode-theorem/)).
6. The [syntactic monoid](/syntactic-monoid/) of $L$ is finite.
7. Some right-linear grammar generates $L$: each rule has the form $A \to aB$, $A \to a$ or $A \to \varepsilon$, with nonterminals $A, B$ and $a \in \Sigma$. The nonterminals act as the states of an NFA.

The class is closed under union, intersection, complement, concatenation, star, reversal, homomorphism and inverse homomorphism. The proofs are on the [closure properties](/closure-properties-of-regular-languages/) page.

## Examples and non-examples

### Regular languages

- **Finite languages.** Each finite language is regular. A DFA for it is the trie of its strings plus one dead state. For $L = \{ab, ba\}$ over $\{a, b\}$ the smallest DFA has 5 states: the start, one state after $a$, one after $b$, one accepting state, and the dead state.
- **Substring search.** The strings over $\{a, b\}$ that contain $aba$ form a regular language. Its smallest DFA has 4 states, one for each length 0 to 3 of the longest suffix of the input that is a prefix of $aba$. This is the [string-matching automaton](/string-matching-automaton/) of the pattern.
- **Order constraints.** The language $a^* b^*$ of strings in which no $a$ follows a $b$ has a smallest DFA with 3 states: "only $a$s so far", "some $b$ seen", and a dead state for a $b$ followed by an $a$.
- **$\emptyset$ and $\Sigma^*$.** Both are regular, with one-state DFAs. So are the strings with an even number of 1s and the binary numerals of the multiples of 3, the two examples of the [DFA](/deterministic-finite-automaton/) page.

### Regular languages over one letter

For $\Sigma = \{a\}$ there is an exact test. Call a set $S$ of natural numbers *ultimately periodic* if there are $t \ge 0$ and $p \ge 1$ with $k \in S \iff k + p \in S$ for each $k \ge t$.

**Claim.** A language $L \subseteq \{a\}^*$ is regular if and only if its set of lengths $S = \{ k : a^k \in L \}$ is ultimately periodic.

*Proof.* Let a DFA with $n$ states accept $L$, and let $q_k = \delta^*(q_0, a^k)$. Among $q_0, \ldots, q_n$ two states are equal, say $q_i = q_j$ with $i < j$, by the [pigeonhole principle](/pigeonhole-principle/). Each state determines the next one, so $q_{k + (j - i)} = q_k$ for each $k \ge i$, and $S$ is ultimately periodic with $t = i$ and $p = j - i$. Conversely, if $S$ is ultimately periodic with $t$ and $p$, take the states $0, 1, \ldots, t + p - 1$, the start state 0, the moves $k \to k + 1$ for $k < t + p - 1$ and $t + p - 1 \to t$, and the accepting states $k$ with $k \in S$. After $a^k$ this DFA is in state $k$ for $k < t + p$, and in a state $k'$ with $t \le k' < t + p$ and $k' \equiv k \pmod p$ after that, so it accepts $a^k$ exactly when $k \in S$. $\square$

For example, the lengths $\{1\} \cup \{4, 6, 8, \ldots\}$ are ultimately periodic with $t = 3$ and $p = 2$, and the smallest DFA of the language has $5 = t + p$ states: a path through 0, 1 and 2, then a cycle of length 2.

### Non-examples

Each proof below finds infinitely many strings that are pairwise *distinguishable*: for two of them, $x$ and $y$, some $z$ has exactly one of $xz$ and $yz$ in $L$. A DFA reaches different states on two distinguishable strings, so it would need infinitely many states. The [pumping lemma](/pumping-lemma-for-regular-languages/) gives another method.

- **Palindromes.** The strings over $\{a, b\}$ that read the same in both directions are not regular. For $i \ne j$ the suffix $b a^i$ separates $a^i b$ from $a^j b$: $a^i b b a^i$ is a palindrome and $a^j b b a^i$ is not.
- **Balanced parentheses.** The [Dyck language](/dyck-language/) of balanced strings of ( and ) is not regular. The suffix $)^i$ separates $(^i$ from $(^j$ for $i \ne j$.
- **Squares in unary.** The language $\{a^{k^2} : k \ge 0\}$ is not regular, because its set of lengths is not ultimately periodic. For each $t$ and $p$ take $m$ with $m^2 \ge t$ and $2m + 1 > p$. Then $m^2$ is a square and $m^2 + p$ lies strictly between $m^2$ and $(m + 1)^2$, so it is not.
- **A subset of a regular language.** The language $\{a^n b^n : n \ge 0\}$ is not regular, though it is a subset of the regular $a^* b^*$. So regularity is not kept by taking subsets. The [context-free languages](/context-free-language/) contain it.

## Related definitions

- [Deterministic finite automaton](/deterministic-finite-automaton/) and [nondeterministic finite automaton](/nondeterministic-finite-automaton/): the machines that accept the regular languages.
- [Regular expression](/regular-expression/) and [Kleene's theorem](/kleene-theorem/): the algebraic description of the class.
- [Myhill-Nerode relation](/myhill-nerode-relation/) and [Myhill-Nerode theorem](/myhill-nerode-theorem/): the characterization by right congruences, which also gives the size of the smallest DFA.
- [Pumping lemma for regular languages](/pumping-lemma-for-regular-languages/): a necessary condition, used to prove that a language is not regular.
- [Closure properties of regular languages](/closure-properties-of-regular-languages/): the operations that keep a language regular.
- [Star-free language](/star-free-language/): the subclass that needs no star when complement is allowed.
- [Context-free language](/context-free-language/): the next class of the Chomsky hierarchy. Each regular language is context-free.
- [State complexity](/state-complexity/): the number of states that a regular language and the results of operations on it need.

## References
