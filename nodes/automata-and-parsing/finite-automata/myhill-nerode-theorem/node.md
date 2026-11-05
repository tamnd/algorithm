---
tag: SZ7FHW
kind: theorem
slug: myhill-nerode-theorem
name: Myhill-Nerode theorem
aliases:
- Myhill-Nerode theorem
- Nerode theorem
area: automata-and-parsing/finite-automata
level: core
summary: A language is regular iff its Myhill-Nerode relation has finitely many classes; the class count is the minimal DFA size.
prereqs: [myhill-nerode-relation, deterministic-finite-automaton]
see_also: [minimal-dfa-uniqueness, dfa-minimization, table-filling-minimization, hopcroft-minimization, pumping-lemma-for-regular-languages, syntactic-monoid, lstar-algorithm, regular-language]
sources:
  - paper: doi:10.1090/S0002-9939-1958-0135681-9
    title: Anil Nerode, Linear automaton transformations, Proceedings of the American Mathematical Society 9(4) (1958)
    locator: pp. 541 to 544
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 15, Myhill-Nerode Relations, and Lecture 16, The Myhill-Nerode Theorem
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, first edition, Addison-Wesley, 1979
    locator: Section 3.4, The Myhill-Nerode Theorem and Minimization of Finite Automata
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.4, Equivalence and Minimization of Automata
  - url: "https://en.wikipedia.org/wiki/Myhill%E2%80%93Nerode_theorem"
    locator: lead (Myhill and Nerode proved it at the University of Chicago in 1957) and section Statement
---

The Myhill-Nerode theorem says that a language $L$ is regular if and only if its [Myhill-Nerode relation](/myhill-nerode-relation/) $\equiv_L$ has finitely many classes. It says more: the number of classes is exactly the number of states of the smallest complete [DFA](/deterministic-finite-automaton/) for $L$, and this smallest DFA is unique up to the names of its states. It gives an exact test for regularity, exact lower bounds on the size of DFAs, and the target that every [DFA minimization](/dfa-minimization/) algorithm computes.

## Statement

Let $\Sigma$ be a finite alphabet and $L \subseteq \Sigma^*$. For $x, y \in \Sigma^*$, $x \equiv_L y$ means that $xz \in L \Leftrightarrow yz \in L$ for each $z \in \Sigma^*$. The *index* of an equivalence relation is its number of classes. A relation $\equiv$ on $\Sigma^*$ is a *right congruence* if $x \equiv y$ implies $xa \equiv ya$ for each $a \in \Sigma$, and it *refines* $L$ if $x \equiv y$ and $x \in L$ imply $y \in L$. DFAs are complete, with $\delta : Q \times \Sigma \to Q$, and have no $\varepsilon$-moves.

**Theorem (Myhill and Nerode).** For $L \subseteq \Sigma^*$ the following are equivalent.

1. $L$ is regular, that is, some DFA accepts $L$.
2. Some right congruence of finite index refines $L$; in other words, $L$ is a union of classes of such a relation.
3. $\equiv_L$ has finite index.

Moreover, if $L$ is regular with $k$ classes of $\equiv_L$, then:

4. Each DFA that accepts $L$ has at least $k$ states, and the DFA $M_L$ below has exactly $k$ states.
5. Each DFA with exactly $k$ states that accepts $L$ is isomorphic to $M_L$.

Here $M_L$ has the states $\{[x] : x \in \Sigma^*\}$, the classes of $\equiv_L$, the start state $[\varepsilon]$, the transitions $\delta_L([x], a) = [xa]$, and the accepting states $\{[x] : x \in L\}$. Two DFAs are *isomorphic* if a bijection between their state sets maps the start state to the start state, accepting states to accepting states and non-accepting states to non-accepting states, and commutes with the transitions.

## In plain words

Two strings are equivalent for a language if no ending can tell them apart: whatever you append, both results are in the language or both are out. A machine that reads from left to right and has finished one of these strings needs to remember only which group it belongs to, never the string itself.

So a language can be recognized with finite memory exactly when there are finitely many groups. The groups also give the best machine: one state for each group, and a move from the group of a string to the group of that string with one more letter. No correct machine has fewer states, and every machine with the same number of states is this one with new names.

## Proof

Two facts from the [Myhill-Nerode relation](/myhill-nerode-relation/) page are used, each with a one-line proof.

(a) $\equiv_L$ is a right congruence that refines $L$. If $x \equiv_L y$ and $z \in \Sigma^*$, then $(xa)z = x(az)$ and $(ya)z = y(az)$ agree on membership, so $xa \equiv_L ya$. With $z = \varepsilon$, $x \in L \Leftrightarrow y \in L$.

(b) Each right congruence $\equiv$ that refines $L$ refines $\equiv_L$. If $x \equiv y$, then $xz \equiv yz$ for each $z$, by induction on $|z|$, and since $\equiv$ refines $L$, $xz \in L \Leftrightarrow yz \in L$. So $x \equiv_L y$. As a result, each class of $\equiv_L$ is a union of classes of $\equiv$, and the index of $\equiv_L$ is at most the index of $\equiv$.

For a DFA $M = (Q, \Sigma, \delta, q_0, F)$, let $x \equiv_M y$ mean $\delta^*(q_0, x) = \delta^*(q_0, y)$. Its classes correspond to the reachable states, so its index is the number of reachable states, at most $|Q|$.

**(1) implies (2).** Let $M$ accept $L$. The relation $\equiv_M$ is a right congruence: if $\delta^*(q_0, x) = \delta^*(q_0, y)$, then $\delta^*(q_0, xa) = \delta(\delta^*(q_0, x), a) = \delta(\delta^*(q_0, y), a) = \delta^*(q_0, ya)$. It refines $L$, because $x \in L$ if and only if $\delta^*(q_0, x) \in F$. Its index is finite.

**(2) implies (3).** By (b), the index of $\equiv_L$ is at most the finite index of the given relation.

**(3) implies (1).** Let $\equiv_L$ have finite index. Then $M_L$ has finitely many states. Its transitions are well defined: if $[x] = [y]$, then $[xa] = [ya]$ by (a). Its accepting set is well defined: if $[x] = [y]$, then $x \in L \Leftrightarrow y \in L$ by (a). By induction on $|w|$, $\delta_L^*([\varepsilon], w) = [w]$: the case $w = \varepsilon$ is the start state, and $\delta_L^*([\varepsilon], va) = \delta_L([v], a) = [va]$. So $M_L$ accepts $w$ if and only if $[w]$ is accepting, if and only if $w \in L$. Thus $M_L$ is a DFA for $L$, and $L$ is regular.

**Proof of 4.** $M_L$ has $k$ states by definition. Let $M$ be any DFA for $L$. By the proof of (1) implies (2), $\equiv_M$ is a right congruence that refines $L$, so by (b) its index is at least $k$. Its index is the number of reachable states of $M$, so $M$ has at least $k$ states.

**Proof of 5.** Let $M = (Q, \Sigma, \delta, q_0, F)$ accept $L$ with $|Q| = k$. By the proof of 4, $M$ has at least $k$ reachable states, so all $k$ states are reachable, and $\equiv_M$ has index $k$. Since $\equiv_M$ refines $\equiv_L$ and both have $k$ classes, each class of $\equiv_L$ is exactly one class of $\equiv_M$, so the two relations are equal. Define $\varphi : Q \to \{[x]\}$ by $\varphi(\delta^*(q_0, x)) = [x]$. Each state is $\delta^*(q_0, x)$ for some $x$, and the value does not depend on the choice of $x$: if $\delta^*(q_0, x) = \delta^*(q_0, y)$, then $x \equiv_M y$, so $[x] = [y]$. The map is injective, because $[x] = [y]$ gives $x \equiv_M y$, and surjective, because each class $[x]$ is the image of $\delta^*(q_0, x)$. It maps $q_0 = \delta^*(q_0, \varepsilon)$ to $[\varepsilon]$. It commutes with the transitions: $\varphi(\delta(\delta^*(q_0, x), a)) = \varphi(\delta^*(q_0, xa)) = [xa] = \delta_L([x], a)$. And $\delta^*(q_0, x) \in F \Leftrightarrow x \in L \Leftrightarrow [x]$ is accepting in $M_L$. So $\varphi$ is an isomorphism. $\blacksquare$

## Consequences

**Proofs of non-regularity.** To show that $L$ is not regular, find infinitely many strings that are pairwise distinguishable. For $\{w \in \{a, b\}^* : w \text{ has as many } a\text{s as } b\text{s}\}$, the strings $a^i$, $i \ge 0$, are pairwise distinguishable: the suffix $b^i$ puts $a^i b^i$ in the language and $a^j b^i$ out for $j \ne i$. Unlike the [pumping lemma](/pumping-lemma-for-regular-languages/), this method is exact: each non-regular language has such an infinite set, by (3).

**Exact lower bounds for DFAs.** If $L$ has $k$ pairwise distinguishable strings, each DFA for $L$ has at least $k$ states, by 4. The table below gives the number of classes for some languages. For each language, the representatives in the table are pairwise distinguishable, and each string is equivalent to one of them.

| language over the given alphabet | classes of $\equiv_L$ | representatives |
|---|---|---|
| binary numerals divisible by 3, with $\varepsilon$ read as 0 | 3 | $\varepsilon$, $1$, $10$ (the value modulo 3) |
| strings over $\{a, b\}$ whose third symbol from the end is $a$ | 8 | $\varepsilon$, $a$, $aa$, $ab$, $aaa$, $aab$, $aba$, $abb$ |
| $(ab)^*$ | 3 | $\varepsilon$, $a$, $b$ (the last one is the dead class) |
| strings over $\{a, b\}$ with as many $a$s as $b$s | infinite | $a^i$ for $i \ge 0$ |

For the multiples of 3, a string $x$ of value $r$ followed by $z$ has the value $r \cdot 2^{|z|} + \mathrm{val}(z)$. So the class of $x$ depends only on $r \bmod 3$, and for $r \not\equiv s \pmod 3$ a suffix $z$ of length 2 with $\mathrm{val}(z) \equiv -r \pmod 3$ separates them, since $2^2 \equiv 1 \pmod 3$. For the third symbol from the end, the class of $x$ is fixed by the last three symbols of $x$, padded on the left; two different windows differ at some position $t \in \{1, 2, 3\}$ from the end, and a suffix of length $3 - t$ moves that position to the third from the end. The same argument with $n$ in place of 3 gives $2^n$ classes, the lower bound on the [NFA](/nondeterministic-finite-automaton/) and [Rabin-Scott](/rabin-scott-theorem/) pages.

**Minimization.** By 5 the minimal DFA is unique up to isomorphism ([uniqueness of the minimal DFA](/minimal-dfa-uniqueness/)). For a DFA $M$ without unreachable states, two states $\delta^*(q_0, x)$ and $\delta^*(q_0, y)$ must be merged exactly when $x \equiv_L y$, that is, when no suffix leads one of them to $F$ and the other out of $F$. The [table-filling algorithm](/table-filling-minimization/), [Moore's algorithm](/moore-minimization/) and [Hopcroft's algorithm](/hopcroft-minimization/) compute this relation on the states, and the quotient is $M_L$.

**Equivalence by canonical forms.** Two DFAs accept the same language if and only if their minimal DFAs are isomorphic. Since a DFA has one start state and is complete, an isomorphism is found by one joint search from the two start states, so [DFA equivalence](/dfa-equivalence/) can be decided this way.

**Learning.** The [L* algorithm](/lstar-algorithm/) learns $M_L$ from membership and equivalence queries. It finds representatives of the classes of $\equiv_L$ and distinguishing suffixes, and the number of classes bounds the number of its rounds.

**Algebraic version.** The two-sided relation $x \sim_L y \iff (uxz \in L \Leftrightarrow uyz \in L$ for all $u, z)$ refines $\equiv_L$. $L$ is regular if and only if $\sim_L$ has finite index, and the quotient is the [syntactic monoid](/syntactic-monoid/). This version leads to [Schutzenberger's theorem](/schutzenberger-theorem/) on star-free languages.

## Tightness

The size statement 4 is exact for complete DFAs, so there is nothing to improve there. The limits are in what it covers.

**Partial DFAs.** If some class of $\equiv_L$ consists of the strings $x$ with $xz \notin L$ for all $z$, that class is a dead state. A DFA that may leave transitions undefined can drop it, so the smallest such DFA has $k - 1$ states. For $(ab)^*$ this gives 2 states.

**NFAs.** No analogue holds for NFAs. The classes of $\equiv_L$ give only the lower bound $\lceil \log_2 k \rceil$ on the number of states of an NFA for $L$, by the [Rabin-Scott theorem](/rabin-scott-theorem/), and this bound can be far from the truth. Minimal NFAs need not be unique up to isomorphism, and finding one is PSPACE-hard ([NFA minimization](/nfa-minimization/)).

**Two-sided congruence.** The syntactic congruence can have many more classes than $\equiv_L$. For the strings that end in $ab$, $\equiv_L$ has 3 classes and $\sim_L$ has 5. For a minimal DFA with $n$ states, $\sim_L$ has at most $n^n$ classes, one for each map from the states to the states.

## History

The theorem is named after John Myhill and Anil Nerode, who proved it at the University of Chicago in 1957. Nerode published the result in 1958. Hopcroft and Ullman (1979, Section 3.4) present it together with the minimization of finite automata.

## References
