---
tag: VSNYKN
kind: definition
slug: myhill-nerode-relation
name: Myhill-Nerode relation
aliases:
- Nerode right congruence
area: automata-and-parsing/finite-automata
level: core
summary: Right-congruence on strings where two strings are equivalent if no suffix separates them in the language.
prereqs: [deterministic-finite-automaton, equivalence-relation]
see_also: [myhill-nerode-theorem, minimal-dfa-uniqueness, dfa-minimization, syntactic-monoid, congruence, table-filling-minimization, lstar-algorithm, regular-language]
sources:
  - paper: doi:10.1090/S0002-9939-1958-0135681-9
    title: Anil Nerode, Linear automaton transformations, Proceedings of the American Mathematical Society 9(4) (1958)
    locator: pp. 541 to 544 (the right congruence of a set of strings and the characterization of finite automaton transformations)
  - paper: "John Myhill, Finite automata and the representation of events, WADD Technical Report 57-624, Wright Air Development Center (1957)"
    locator: the whole report (the congruence of a set of strings and its finite index)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 15, Myhill-Nerode Relations, and Lecture 16, The Myhill-Nerode Theorem
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.4, Equivalence and Minimization of Automata
---

The Myhill-Nerode relation of a language $L$ puts two strings in one class when no continuation tells them apart: for every suffix $z$, either both strings followed by $z$ are in $L$ or neither is. It is the relation that a DFA must respect, since a DFA cannot treat two strings differently in the future once it is in the same state after them. Its number of classes is the number of states of the smallest complete DFA for $L$, and it is finite exactly when $L$ is regular, by the [Myhill-Nerode theorem](/myhill-nerode-theorem/).

## Definition

Let $\Sigma$ be a finite alphabet and $L \subseteq \Sigma^*$.

**The relation $\equiv_L$.** For $x, y \in \Sigma^*$,

$$x \equiv_L y \iff \text{for all } z \in \Sigma^*: \ (xz \in L \Leftrightarrow yz \in L).$$

A string $z$ with $xz \in L$ and $yz \notin L$, or the other way round, is a *distinguishing extension* of $x$ and $y$, and $x$ and $y$ are then *distinguishable*. The *index* of $\equiv_L$ is its number of classes, which may be infinite. We write $[x]$ for the class of $x$.

**Basic facts.** For every $L$:

1. $\equiv_L$ is an [equivalence relation](/equivalence-relation/), since "$xz \in L \Leftrightarrow yz \in L$" is reflexive, symmetric and transitive for each fixed $z$.
2. $\equiv_L$ is a *right congruence*: $x \equiv_L y$ implies $xa \equiv_L ya$ for each $a \in \Sigma$, and so $xu \equiv_L yu$ for each $u \in \Sigma^*$. For a suffix $z$, apply the definition to the suffix $az$.
3. $\equiv_L$ *refines* $L$: $x \equiv_L y$ and $x \in L$ imply $y \in L$. Take $z = \varepsilon$. So $L$ is a union of classes.

**Myhill-Nerode relations.** Following Kozen, a *Myhill-Nerode relation for $L$* is any equivalence relation $\equiv$ on $\Sigma^*$ that is a right congruence, refines $L$, and has finite index.

**$\equiv_L$ is the coarsest one.** Every right congruence $\equiv$ that refines $L$ refines $\equiv_L$: if $x \equiv y$, then $xz \equiv yz$ for each $z$, and since $\equiv$ refines $L$, $xz \in L \Leftrightarrow yz \in L$; so $x \equiv_L y$. Hence each class of $\equiv_L$ is a union of classes of $\equiv$, and the index of $\equiv_L$ is at most the index of $\equiv$.

**The relation of a DFA.** For a complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves, let $x \equiv_M y$ when $\delta^*(q_0, x) = \delta^*(q_0, y)$. It is a right congruence, by the lemma $\delta^*(q_0, xa) = \delta(\delta^*(q_0, x), a)$; it refines $L(M)$, since acceptance depends only on the last state; and its index is the number of reachable states, at most $|Q|$. So $\equiv_M$ is a Myhill-Nerode relation for $L(M)$, and by the previous paragraph $\equiv_M$ refines $\equiv_{L(M)}$. In words: if two strings lead to the same state, no suffix distinguishes them.

**The DFA of a relation.** Conversely, let $\equiv$ be a Myhill-Nerode relation for $L$ with the classes $[x]$. Define $M_\equiv$ with the states $\{[x] : x \in \Sigma^*\}$, the start state $[\varepsilon]$, $\delta([x], a) = [xa]$ and $F = \{[x] : x \in L\}$. The transition is well defined because $\equiv$ is a right congruence, and $F$ is well defined because $\equiv$ refines $L$. By induction on $|w|$, $\delta^*([x], w) = [xw]$, so $M_\equiv$ accepts $w$ exactly when $[w] \in F$, that is, when $w \in L$. So $M_\equiv$ is a complete DFA for $L$ with as many states as $\equiv$ has classes.

The two maps are inverse to each other up to renaming of states, for DFAs without unreachable states. Applied to $\equiv_L$, they give the smallest complete DFA for $L$ and show that its number of states is the index of $\equiv_L$. This is the [Myhill-Nerode theorem](/myhill-nerode-theorem/), and the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/) follows from the same correspondence.

## Examples and non-examples

The class counts below were checked by a script that compares all strings of length at most 6 on all suffixes of length at most 6.

- **Even number of 1s.** For the binary strings with an even number of 1s, $x \equiv_L y$ if and only if $x$ and $y$ have the same number of 1s modulo 2. Two classes, and the minimal DFA has 2 states.
- **Strings that end in $ab$.** Over $\{a, b\}$, the classes are $[\varepsilon]$ (the strings that end in neither $a$ nor $ab$, together with $\varepsilon$), $[a]$ (the strings that end in $a$) and $[ab]$ (the strings that end in $ab$). The suffix $b$ distinguishes $\varepsilon$ from $a$, and $\varepsilon$ distinguishes $ab$ from both. Three classes.
- **A finite language.** For $L = \{a\}$ over $\{a, b\}$, the classes are $[\varepsilon] = \{\varepsilon\}$, $[a] = \{a\}$, and one class of all other strings, which no suffix can bring into $L$. Three classes; the last one is the dead state of the minimal complete DFA.
- **A language of infinite index.** For $L = \{a^n b^n : n \ge 0\}$, the strings $a^i$ and $a^j$ with $i \neq j$ are distinguished by the suffix $b^i$. So $\equiv_L$ has infinitely many classes, and $L$ is not regular.
- **Non-example: same length.** The relation "$|x| = |y|$" is a right congruence, but it does not refine the language of the even number of 1s, because $0$ is in the language and $1$ is not. So it is not a Myhill-Nerode relation for that language.
- **Non-example: same length modulo 2, for $\Sigma^*$.** For $L = \Sigma^*$, the relation "$|x| \equiv |y| \pmod 2$" is a Myhill-Nerode relation with 2 classes. It is not $\equiv_L$, which has 1 class. A Myhill-Nerode relation can be finer than $\equiv_L$, and it then corresponds to a DFA that is not minimal.

## Related definitions

- **Syntactic congruence.** The two-sided relation $x \sim_L y$ if and only if $uxz \in L \Leftrightarrow uyz \in L$ for all $u, z$ is a congruence of the monoid $\Sigma^*$ and refines $\equiv_L$. Its quotient is the [syntactic monoid](/syntactic-monoid/) of $L$, the transition monoid of the minimal DFA. For the strings that end in $ab$, $\equiv_L$ has 3 classes and $\sim_L$ has 5.
- **Equivalent states.** In a DFA, states $p$ and $q$ are equivalent when $\delta^*(p, z) \in F \Leftrightarrow \delta^*(q, z) \in F$ for all $z$. For reachable states $p = \delta^*(q_0, x)$ and $q = \delta^*(q_0, y)$ this holds exactly when $x \equiv_L y$. [DFA minimization](/dfa-minimization/) merges equivalent states, for example by the [table-filling algorithm](/table-filling-minimization/), [Moore's algorithm](/moore-minimization/) or [Hopcroft's algorithm](/hopcroft-minimization/).
- **Bounded versions.** The relation $\equiv_L^{(k)}$ uses only suffixes $z$ of length at most $k$. It is coarser than $\equiv_L$, and for a DFA with $n$ states, $\equiv_L^{(n-2)}$ already equals $\equiv_L$ on the reachable states when $n \ge 2$. Moore's algorithm computes these relations round by round.
- **Learning.** The rows of the observation table of the [L* algorithm](/lstar-algorithm/) are finite samples of the distinguishing extensions, and the algorithm learns the classes of $\equiv_L$.
- **Other structures.** The same idea defines the minimal [Moore machine](/moore-machine/) and [Mealy machine](/mealy-machine/), with outputs in place of acceptance, and the minimal sequential transducer.

## References
