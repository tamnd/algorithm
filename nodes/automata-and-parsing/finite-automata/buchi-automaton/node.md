---
tag: VJESXK
kind: model
slug: buchi-automaton
name: Büchi automaton
aliases:
- Buchi automaton
- Büchi automaton on infinite words
- omega-automaton
area: automata-and-parsing/finite-automata
level: advanced
summary: Automaton on infinite words that accepts if an accepting state recurs infinitely often.
prereqs: [nondeterministic-finite-automaton, deterministic-finite-automaton, strongly-connected-components]
see_also:
- linear-temporal-logic
- ltl-to-buchi-translation
- ltl-model-checking
- automata-theoretic-approach
- nested-depth-first-search
- alternating-finite-automaton
- parity-game
- language-containment
sources:
  - book: doi:10.1007/978-1-4613-8928-6_23
    title: J. Richard Büchi, On a decision method in restricted second order arithmetic, Proceedings of the 1960 International Congress on Logic, Methodology and Philosophy of Science (1962), reprinted in The Collected Works of J. Richard Büchi (1990)
    locator: pp. 425 to 435 of the reprint (automata on infinite sequences and their complementation)
  - paper: doi:10.1016/s0019-9958(66)80013-x
    title: Robert McNaughton, Testing and generating infinite sequences by a finite automaton, Information and Control 9(5) (1966)
    locator: pp. 521 to 530 (deterministic automata with Muller acceptance)
  - paper: doi:10.1016/0304-3975(87)90008-9
    title: A. Prasad Sistla, Moshe Y. Vardi and Pierre Wolper, The complementation problem for Büchi automata with applications to temporal logic, Theoretical Computer Science 49(2-3) (1987)
    locator: pp. 217 to 237
  - paper: doi:10.1109/sfcs.1988.21948
    title: Shmuel Safra, On the complexity of omega-automata, 29th Annual Symposium on Foundations of Computer Science (1988)
    locator: pp. 319 to 327
  - paper: doi:10.1006/inco.1994.1092
    title: Moshe Y. Vardi and Pierre Wolper, Reasoning about infinite computations, Information and Computation 115(1) (1994)
    locator: pp. 1 to 37 (from temporal logic formulas to Büchi automata)
  - paper: doi:10.1007/bf00121128
    title: Costas Courcoubetis, Moshe Y. Vardi, Pierre Wolper and Mihalis Yannakakis, Memory-efficient algorithms for the verification of temporal properties, Formal Methods in System Design 1(2-3) (1992)
    locator: pp. 275 to 288 (the nested depth-first search for emptiness)
  - book: doi:10.1016/b978-0-444-88074-1.50009-3
    title: Wolfgang Thomas, Automata on infinite objects, Handbook of Theoretical Computer Science, Volume B, Formal Models and Semantics (1990)
    locator: pp. 133 to 191
---

A Büchi automaton reads an infinite word. It has the same parts as an [NFA](/nondeterministic-finite-automaton/), but a run never ends, so it cannot accept by ending in an accepting state. It accepts instead when its run passes through an accepting state infinitely often. The languages of Büchi automata are the *ω-regular languages*. They are closed under union, intersection and complement, and their emptiness can be decided in linear time by a search for a cycle. These facts make Büchi automata the standard model of the behaviour of nonterminating systems: in [LTL model checking](/ltl-model-checking/), a temporal formula becomes a Büchi automaton, and a system is correct if its product with the automaton for the negated formula is empty.

## The machine

An ω-word over $\Sigma$ is an infinite sequence $w = a_1 a_2 a_3 \cdots$ with $a_i \in \Sigma$, and $\Sigma^\omega$ is the set of all ω-words. For a nonempty finite word $v$, $v^\omega = v v v \cdots$, and $u v^\omega$ is an *ultimately periodic* word.

A (nondeterministic) Büchi automaton is a tuple $B = (Q, \Sigma, \delta, q_0, F)$ with a finite set of states $Q$, a start state $q_0$, a set of accepting states $F \subseteq Q$ and

$$\delta : Q \times \Sigma \to 2^Q.$$

There are no $\varepsilon$-moves. The automaton need not be complete: $\delta(q, a) = \emptyset$ is allowed, and a run that meets it dies. A *run* of $B$ on $w$ is an infinite sequence of states $r_0 r_1 r_2 \cdots$ with $r_0 = q_0$ and $r_{i} \in \delta(r_{i-1}, a_i)$ for all $i \ge 1$. Let $\mathrm{Inf}(r)$ be the set of states that occur infinitely often in $r$; it is nonempty because $Q$ is finite. The run is *accepting* if

$$\mathrm{Inf}(r) \cap F \neq \emptyset,$$

and $L_\omega(B)$ is the set of ω-words that have an accepting run. A *deterministic* Büchi automaton (DBA) has $|\delta(q, a)| = 1$ for all $q$ and $a$, so it is complete and has exactly one run on each word.

**Examples.** Over $\Sigma = \{a, b\}$:

- The DBA $A$ with the states $0, 1$, start 0, $\delta(q, a) = 1$, $\delta(q, b) = 0$ and $F = \{1\}$ remembers the last symbol. It accepts the words with infinitely many $a$s, since state 1 recurs exactly when $a$ recurs.
- The automaton $N$ with the states $0, 1$, start 0, $\delta(0, a) = \{0\}$, $\delta(0, b) = \{0, 1\}$, $\delta(1, b) = \{1\}$, $\delta(1, a) = \emptyset$ and $F = \{1\}$ accepts the words with finitely many $a$s. It waits in state 0, guesses the point after the last $a$, and then must read only $b$s in state 1.

A script checked both automata on all ultimately periodic words $u v^\omega$ with $|u| \le 4$ and $1 \le |v| \le 4$.

## What it counts

A run is infinite, so there is no running time to measure on one input. The measures are:

- **Size.** The number of states $n = |Q|$ and the number of transitions $m$. Constructions such as complementation and determinization are measured by the number of states of the result.
- **Cost of decision procedures.** Algorithms take the automaton, not a word, as input, and their time is measured in $n$ and $m$ on a [word RAM](/word-ram/). Emptiness takes $O(n + m)$ time; universality and inclusion are much harder.
- **Membership of ultimately periodic words.** An infinite word is not a finite input, but $u v^\omega$ is given by two finite words. Its membership is emptiness of a product of $B$ with a cycle of $|v|$ positions after a path of $|u|$ positions, which takes $O((|u| + |v|)(n + m))$ time.

Two Büchi automata with the same ultimately periodic words accept the same language, because the difference of the two languages is ω-regular and every nonempty ω-regular language contains an ultimately periodic word (see the emptiness lemma below).

## Relation to other models

- **NFAs.** A Büchi automaton has the syntax of an NFA. Only the acceptance condition differs: "the run ends in $F$" becomes "the run visits $F$ infinitely often".
- **Deterministic Büchi automata are weaker.** Unlike for finite words, determinism loses power: no DBA accepts the language of $N$ above (proof below). The [subset construction](/subset-construction/) fails because a subset run can visit accepting subsets infinitely often while no single run does.
- **Other acceptance conditions.** A *Muller* automaton accepts when $\mathrm{Inf}(r)$ is one of a given family of sets of states; *Rabin*, *Streett* and *parity* automata use pairs of sets or priorities. McNaughton (1966) proved that every ω-regular language has a deterministic Muller automaton, and Safra (1988) gave a construction from a Büchi automaton with $n$ states to a deterministic Rabin automaton with $2^{O(n \log n)}$ states. All these nondeterministic models accept the ω-regular languages. Parity automata connect to [parity games](/parity-game/).
- **Generalized Büchi automata.** These have $k$ accepting sets $F_1, \ldots, F_k$ and require each to be visited infinitely often. A copy counter modulo $k$, as in the intersection construction below, turns one into a Büchi automaton with $kn$ states. Translations from temporal logic produce them naturally.
- **Logic.** Büchi (1962) introduced the model to prove that the monadic second-order theory of the natural numbers with successor (S1S) is decidable: the sets of ω-words defined by S1S formulas are exactly the ω-regular languages. Each formula $\varphi$ of [linear temporal logic](/linear-temporal-logic/) has a Büchi automaton with $2^{O(|\varphi|)}$ states that accepts its models (Vardi and Wolper, 1994); see [LTL to Büchi translation](/ltl-to-buchi-translation/).
- **Alternation.** Alternating Büchi automata add universal branching as in [alternating finite automata](/alternating-finite-automaton/). An LTL formula has an alternating Büchi automaton of linear size, and removing the alternation costs one exponential.

## Known results in the model

### Emptiness and ultimately periodic words

**Lemma.** $L_\omega(B) \neq \emptyset$ if and only if some accepting state $f$ is reachable from $q_0$ and lies on a cycle, that is, there are words $u$ and $v \neq \varepsilon$ with a path from $q_0$ to $f$ labelled $u$ and a path from $f$ to $f$ labelled $v$. In that case $u v^\omega \in L_\omega(B)$, and $u$ and $v$ can be chosen with $|u| \le n - 1$ and $|v| \le n$.

*Proof.* If the paths exist, the run that follows the $u$ path and then the $v$ cycle forever is a run on $u v^\omega$ that visits $f$ infinitely often, so it is accepting. Conversely, let $r$ be an accepting run on $w = a_1 a_2 \cdots$. Some state of $F$ is in $\mathrm{Inf}(r)$, say $f$, so there are positions $i < j$ with $r_i = r_j = f$. Then $u = a_1 \cdots a_i$ labels a path from $q_0$ to $f$, and $v = a_{i+1} \cdots a_j$, which is nonempty, labels a path from $f$ to $f$. For the lengths, replace the first path by a shortest path from $q_0$ to $f$, which repeats no state and so has at most $n - 1$ edges, and the second by a shortest cycle through $f$, which has at most $n$ edges. $\square$

So emptiness is a graph problem on the transition graph. Compute the states reachable from $q_0$ and the [strongly connected components](/strongly-connected-components/), for instance with [Tarjan's algorithm](/tarjan-scc/). The language is nonempty if and only if some reachable accepting state lies in a component that contains at least one edge. This takes $O(n + m)$ time. The [nested depth-first search](/nested-depth-first-search/) of Courcoubetis, Vardi, Wolper and Yannakakis (1992) does the same with two depth-first searches and only a few bits of memory per state, and works on the fly, while the product with a system is still being built. A script compared the cycle test with a search over all words $u v^\omega$ with $|u| \le n - 1$ and $|v| \le n$ on 1500 random automata with at most 4 states.

**Corollary (structure of ω-regular languages).** $L_\omega(B) = \bigcup_{f \in F} U_f \, V_f^\omega$, where $U_f$ is the regular language of words that lead from $q_0$ to $f$, $V_f$ is the regular language of nonempty words that lead from $f$ to $f$, and $V^\omega$ is the set of infinite concatenations of words of $V$. *Proof.* A word in $U_f V_f^\omega$ has a run that visits $f$ at the end of each factor, so it is accepted. Conversely, if an accepting run visits $f \in F$ at the positions $i_0 < i_1 < i_2 < \cdots$, cutting $w$ at these positions writes it as $u v_1 v_2 \cdots$ with $u \in U_f$ and each $v_k \in V_f$. $\square$ Büchi (1962) showed the converse: every finite union of sets $U V^\omega$ with $U, V$ regular and $\varepsilon \notin V$ is the language of a Büchi automaton.

### Closure under union and intersection

**Union.** Take the disjoint union of $B_1$ and $B_2$ with a new start state that copies the outgoing transitions of both start states. The new state has no incoming transitions, so a run uses it once and then stays in one of the two automata, and it is accepting exactly when it is accepting there.

**Intersection.** The plain product with $F_1 \times F_2$ is wrong: the two runs can visit their accepting states infinitely often but never at the same time. The fix keeps a flag. The states are $Q_1 \times Q_2 \times \{1, 2\}$, with start $(q_1, q_2, 1)$ and transitions $(p_1, p_2, k) \xrightarrow{a} (p_1', p_2', k')$ for $p_1' \in \delta_1(p_1, a)$ and $p_2' \in \delta_2(p_2, a)$, where

$$k' = 2 \text{ if } k = 1 \text{ and } p_1 \in F_1, \qquad k' = 1 \text{ if } k = 2 \text{ and } p_2 \in F_2, \qquad k' = k \text{ otherwise}.$$

The accepting states are $Q_1 \times F_2 \times \{2\}$.

*Proof.* A run of the product is a pair of runs $r^1, r^2$ of $B_1, B_2$ together with a flag sequence. Suppose that the product run is accepting. Each visit to $Q_1 \times F_2 \times \{2\}$ sets the flag to 1, and the flag only returns to 2 at a visit of $r^1$ to $F_1$. So between two accepting visits there is a visit of $r^1$ to $F_1$, and both $r^1$ and $r^2$ visit their accepting sets infinitely often. Conversely, suppose that $r^1$ and $r^2$ are accepting. When the flag is 1, the next visit of $r^1$ to $F_1$ sets it to 2; when the flag is 2, the next visit of $r^2$ to $F_2$ is an accepting state of the product and sets the flag to 1. So the flag changes infinitely often, and the product visits its accepting states infinitely often. $\square$

The product has $2 n_1 n_2$ states. A script checked it against the definition on 400 random pairs of automata with at most 3 states each, on all words $u v^\omega$ with $|u| \le 2$ and $1 \le |v| \le 3$. The same counter with $k$ values turns a generalized Büchi automaton into a Büchi automaton.

### Deterministic Büchi automata are weaker

**Claim.** No DBA accepts $L = \{ w \in \{a, b\}^\omega : w \text{ has finitely many } a\text{s} \}$.

*Proof.* Suppose that the DBA $D$ accepts $L$, and write $\hat\delta(x)$ for its state after a finite word $x$. Since $b^\omega \in L$, the run on $b^\omega$ visits $F$, so there is $n_1 \ge 1$ with $\hat\delta(b^{n_1}) \in F$. Since $b^{n_1} a b^\omega \in L$, there is $n_2 \ge 1$ with $\hat\delta(b^{n_1} a b^{n_2}) \in F$. Going on, we get $n_1, n_2, \ldots$ such that $\hat\delta(b^{n_1} a b^{n_2} a \cdots a b^{n_k}) \in F$ for every $k$. Because $D$ is deterministic, its single run on $w = b^{n_1} a b^{n_2} a b^{n_3} \cdots$ passes through these states, so it visits $F$ infinitely often and $D$ accepts $w$. But $w$ has infinitely many $a$s, so $w \notin L$. $\square$

The complement of $L$, "infinitely many $a$s", has the DBA $A$. So the class of DBA languages is not closed under complement. It is closed under union and intersection, by the constructions above, which keep determinism.

### Complementation

The ω-regular languages are closed under complement (Büchi, 1962), but the construction is hard, because a Büchi automaton cannot be determinized into a Büchi automaton and the subset construction does not apply. Büchi's proof used Ramsey's theorem. Sistla, Vardi and Wolper (1987) made it give $2^{O(n^2)}$ states, and Safra (1988) gave $2^{O(n \log n)}$ states by determinizing into a Rabin automaton. A lower bound of $n!$ states, due to Michel (1988), shows that $2^{O(n \log n)}$ is the right order; later work has narrowed the base of the exponent.

### Decision problems

- **Emptiness:** $O(n + m)$ time, by the lemma above.
- **Membership of $u v^\omega$:** polynomial time, by emptiness of a product.
- **Universality, inclusion and equivalence:** PSPACE-complete (Sistla, Vardi and Wolper, 1987). Inclusion $L_\omega(B_1) \subseteq L_\omega(B_2)$ is the emptiness of $L_\omega(B_1) \cap \overline{L_\omega(B_2)}$, and the complement is built on the fly in polynomial space. For [language containment](/language-containment/) in model checking, the specification side is usually given as a formula and complemented by negation, which avoids this cost.

### Pitfalls

- **Swapping accepting states does not complement.** For the DBA $A$ above, $F = \{0\}$ gives "infinitely many $b$s", not "finitely many $a$s"; the word $(ab)^\omega$ is in both. A script found 120 words $u v^\omega$ with $|u|, |v| \le 3$ on which the two differ. Even for a DBA, the complement needs a different acceptance condition (co-Büchi: visit $F$ only finitely often).
- **Plain product for intersection.** Using $F_1 \times F_2$ as the accepting set misses words whose two runs visit their accepting sets at different times. Use the flag construction.
- **Finite-word thinking.** A state in $F$ that is reached but not on a cycle does not make the language nonempty. Emptiness checks must look for a reachable accepting cycle, not a reachable accepting state.
- **Dead ends.** Runs that reach a state with no transition on the next symbol die. Removing the states that cannot reach an accepting cycle does not change the language, and simplifies later constructions.

## References
