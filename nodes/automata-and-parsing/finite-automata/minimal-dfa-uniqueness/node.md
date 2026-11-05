---
tag: 8C2ZR2
kind: theorem
slug: minimal-dfa-uniqueness
name: Uniqueness of the minimal DFA
aliases:
- minimal DFA is unique up to isomorphism
area: automata-and-parsing/finite-automata
level: core
summary: Every regular language has a unique minimal DFA up to renaming of states.
prereqs: [myhill-nerode-relation, deterministic-finite-automaton]
see_also: [myhill-nerode-theorem, dfa-minimization, hopcroft-minimization, moore-minimization, brzozowski-minimization, dfa-equivalence, nfa-minimization, regular-language]
sources:
  - paper: doi:10.1090/S0002-9939-1958-0135681-9
    title: Anil Nerode, Linear automaton transformations, Proceedings of the American Mathematical Society 9(4) (1958)
    locator: pp. 541 to 544
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 15, Myhill-Nerode Relations (the isomorphism between DFAs without unreachable states and Myhill-Nerode relations), and Lecture 16, The Myhill-Nerode Theorem
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.4.4, Why the Minimized DFA Can't Be Beaten
  - paper: "Edward F. Moore, Gedanken-experiments on sequential machines, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 129 to 153 (equivalent states and the reduced machine)
  - paper: doi:10.1137/0222067
    title: Tao Jiang and B. Ravikumar, Minimal NFA problems are hard, SIAM Journal on Computing 22(6) (1993)
    locator: pp. 1117 to 1141
---

Every [regular language](/regular-language/) has a smallest complete [DFA](/deterministic-finite-automaton/), and this DFA is unique: any two complete DFAs for the language with the smallest number of states differ only in the names of their states. Every other DFA for the language without unreachable states maps onto the minimal one by a map that respects the start state, the transitions and the accepting states. So "the" minimal DFA is a canonical form of a regular language, and two DFAs accept the same language exactly when their minimizations are the same up to renaming. The theorem does not hold for NFAs.

## Statement

A DFA here is complete and has no $\varepsilon$-moves: $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$. A state is *reachable* if it is $\delta^*(q_0, x)$ for some $x$. Two DFAs $M = (Q, \Sigma, \delta, q_0, F)$ and $M' = (Q', \Sigma, \delta', q_0', F')$ are *isomorphic* if there is a bijection $\varphi : Q \to Q'$ with $\varphi(q_0) = q_0'$, $\varphi(\delta(q, a)) = \delta'(\varphi(q), a)$ for all $q$ and $a$, and $q \in F \Leftrightarrow \varphi(q) \in F'$. States $p, q$ of one DFA are *equivalent* if $\delta^*(p, z) \in F \Leftrightarrow \delta^*(q, z) \in F$ for every $z \in \Sigma^*$.

**Theorem.** Let $L \subseteq \Sigma^*$ be regular, and let $\equiv_L$ be its [Myhill-Nerode relation](/myhill-nerode-relation/), with index $k$. Then:

1. Every complete DFA for $L$ has at least $k$ states, and the DFA $M_L$ on the classes of $\equiv_L$ has exactly $k$.
2. Every complete DFA for $L$ with $k$ states is isomorphic to $M_L$. So any two minimal DFAs for $L$ are isomorphic.
3. A complete DFA for $L$ is minimal if and only if all its states are reachable and no two of its states are equivalent.
4. For every complete DFA $M$ for $L$ whose states are all reachable, the map $\varphi(\delta^*(q_0, x)) = [x]$ is a well-defined surjective homomorphism from $M$ onto $M_L$.

## In plain words

A machine that reads a word letter by letter must remember enough about what it has read to answer correctly for every possible ending. Two beginnings that some ending can tell apart must lead to different states. Two beginnings that no ending can tell apart may share a state.

The smallest machine gives exactly one state to each group of beginnings that no ending can tell apart. Any other machine for the same words is this smallest machine with some states split into copies, plus perhaps some states that can never be reached. So when two machines are both as small as possible, they are the same machine with different state names. This gives a simple test of whether two machines accept the same words: shrink both, then compare.

## Proof

Let $M_L$ have the states $\{[x] : x \in \Sigma^*\}$, the start state $[\varepsilon]$, the transitions $\delta_L([x], a) = [xa]$ and the accepting states $\{[x] : x \in L\}$. The [Myhill-Nerode relation](/myhill-nerode-relation/) page shows that $M_L$ is a well-defined complete DFA, that $\delta_L^*([\varepsilon], x) = [x]$, and that $L(M_L) = L$.

**Part 4.** Let $M = (Q, \Sigma, \delta, q_0, F)$ be a complete DFA for $L$ in which every state is reachable. For $q \in Q$ pick $x$ with $\delta^*(q_0, x) = q$ and set $\varphi(q) = [x]$.

- *Well defined.* If also $\delta^*(q_0, y) = q$, then for each $z$, $\delta^*(q_0, xz) = \delta^*(q, z) = \delta^*(q_0, yz)$ by the lemma $\delta^*(q, uv) = \delta^*(\delta^*(q, u), v)$, so $xz \in L \Leftrightarrow yz \in L$. Hence $x \equiv_L y$ and $[x] = [y]$.
- *Surjective.* The class $[x]$ is $\varphi(\delta^*(q_0, x))$.
- *Start state.* $\varphi(q_0) = [\varepsilon]$, since $\delta^*(q_0, \varepsilon) = q_0$.
- *Transitions.* If $\delta^*(q_0, x) = q$, then $\delta^*(q_0, xa) = \delta(q, a)$, so $\varphi(\delta(q, a)) = [xa] = \delta_L([x], a) = \delta_L(\varphi(q), a)$.
- *Accepting states.* $q \in F \Leftrightarrow x \in L \Leftrightarrow [x]$ is accepting in $M_L$.

**Part 1.** Let $M$ be any complete DFA for $L$. Removing its unreachable states gives a complete DFA for $L$ with at most as many states, because no transition leads from a reachable state to an unreachable one. By Part 4 there is a surjection from its states onto the $k$ classes, so it has at least $k$ states, and $M$ has at least $k$ states too.

**Part 2.** Let $M$ be a complete DFA for $L$ with exactly $k$ states. All its states are reachable: otherwise the reachable part would be a complete DFA for $L$ with fewer than $k$ states, which contradicts Part 1. By Part 4, $\varphi$ is a surjection from a set of $k$ states onto a set of $k$ classes, so it is a bijection. A bijective homomorphism is an isomorphism, because the three conditions in the definition of an isomorphism are exactly the three properties of $\varphi$ that Part 4 proves. If $M$ and $M'$ are both minimal, both are isomorphic to $M_L$, and so to each other.

**Part 3.** Let $M$ be a complete DFA for $L$ whose states are all reachable, and let $\varphi$ be the map of Part 4. For reachable states $p = \delta^*(q_0, x)$ and $q = \delta^*(q_0, y)$, the lemma $\delta^*(q_0, xz) = \delta^*(p, z)$ gives $\delta^*(p, z) \in F \Leftrightarrow xz \in L$, and the same for $q$ and $y$. So $p$ and $q$ are equivalent if and only if $x \equiv_L y$, that is, if and only if $\varphi(p) = \varphi(q)$. If $M$ is minimal, all its states are reachable, as in Part 2, and $\varphi$ is a bijection, so no two different states are equivalent. Conversely, if all states are reachable and no two are equivalent, then $\varphi$ is injective, so $|Q| = k$, and $M$ is minimal by Part 1. $\blacksquare$

**Example.** Over $\{a, b\}$, let $L$ be the set of strings that end in $ab$. A DFA $M$ that remembers the last two symbols has the 7 states $\varepsilon, a, b, aa, ab, ba, bb$, with $\delta(s, c)$ equal to the last two symbols of $sc$, and $F = \{ab\}$. All 7 states are reachable. The relation $\equiv_L$ has the 3 classes $[\varepsilon]$, $[a]$ and $[ab]$, and $M_L$ has $\delta_L([\varepsilon], a) = [a]$, $\delta_L([\varepsilon], b) = [\varepsilon]$, $\delta_L([a], a) = [a]$, $\delta_L([a], b) = [ab]$, $\delta_L([ab], a) = [a]$ and $\delta_L([ab], b) = [\varepsilon]$. The homomorphism of Part 4 is

| state of $M$ | $\varepsilon$ | $b$ | $bb$ | $a$ | $aa$ | $ba$ | $ab$ |
|---|---|---|---|---|---|---|---|
| $\varphi$ | $[\varepsilon]$ | $[\varepsilon]$ | $[\varepsilon]$ | $[a]$ | $[a]$ | $[a]$ | $[ab]$ |

A script checked that $\varphi$ commutes with all 14 transitions, that $M$ accepts exactly the strings that end in $ab$ up to length 10, and that $M$ minimizes to 3 states.

## Consequences

- **Canonical form.** The minimal DFA, with its states numbered in the order of a [breadth-first search](/breadth-first-search/) that tries the symbols in a fixed order, is a canonical form: two DFAs accept the same language if and only if their canonical forms are equal. This decides [DFA equivalence](/dfa-equivalence/) and gives a hash key for regular languages.
- **Correctness of minimization.** Any algorithm that removes unreachable states and then merges exactly the equivalent states outputs the minimal DFA, by Part 3. This covers the [table-filling algorithm](/table-filling-minimization/), [Moore's algorithm](/moore-minimization/), [Hopcroft's algorithm](/hopcroft-minimization/) and [Brzozowski's algorithm](/brzozowski-minimization/). See [DFA minimization](/dfa-minimization/).
- **Lower bounds on DFA size.** To show that $L$ needs $k$ states, it is enough to give $k$ strings that are pairwise distinguishable for $L$. This is the method of [state complexity](/state-complexity/) and of the [determinization blow-up lower bound](/determinization-blowup-lower-bound/).
- **Learning.** A learner that identifies the classes of $\equiv_L$ outputs the same DFA whatever the teacher's DFA looks like, which is what the [L* algorithm](/lstar-algorithm/) does.

## Tightness

- **Completeness matters for the count.** Among partial DFAs, the minimal one is the minimal complete DFA with its dead state removed, if it has one: the class of strings that no suffix brings into $L$. So the minimal partial DFA has $k - 1$ or $k$ states, and it is unique as well.
- **Reachability is needed in Part 4.** An unreachable state $q$ can accept a language $\{ z : \delta^*(q, z) \in F \}$ that is not of the form $\{ z : xz \in L \}$ for any $x$, and then no homomorphism maps $q$ into $M_L$.
- **NFAs.** Minimal NFAs need not be unique. For $L = a a^*$ over $\{a\}$, the NFA with $0 \xrightarrow{a} 1$, $1 \xrightarrow{a} 1$ and $F = \{1\}$, and the NFA with $0 \xrightarrow{a} 0$, $0 \xrightarrow{a} 1$ and $F = \{1\}$ both have 2 states, and a 1-state NFA cannot accept $L$, because it accepts $\varepsilon$ when its state is accepting and accepts nothing otherwise. The two NFAs are not isomorphic, since only the second has a loop at its start state. A search over all 2-state NFAs over $\{a, b\}$ found 6 different minimal NFAs for this language. Finding a minimal NFA is PSPACE-complete, even when the input is a DFA (Jiang and Ravikumar, 1993). See [NFA minimization](/nfa-minimization/).

## History

Moore (1956) studied equivalent states of sequential machines and the reduced machine in which no two states are equivalent, and Huffman (1954) did similar work for switching circuits. Myhill (1957) and Nerode (1958) characterized the regular languages by congruences of finite index, and the minimal automaton is the automaton of the coarsest such right congruence. The textbook form of the theorem, with the homomorphism onto the quotient automaton, follows Nerode.

## References
