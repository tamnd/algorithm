---
tag: KMTGEA
kind: theorem
slug: rabin-scott-theorem
name: Rabin-Scott theorem
aliases:
- NFA-DFA equivalence theorem
- powerset construction theorem
area: automata-and-parsing/finite-automata
level: core
summary: Every NFA with n states has an equivalent DFA with at most 2^n states, so nondeterminism does not add recognition power.
prereqs: [nondeterministic-finite-automaton, deterministic-finite-automaton]
see_also: [subset-construction, nfa-determinization, determinization-blowup-lower-bound, regular-language, epsilon-nfa, state-complexity, nfa-universality, myhill-nerode-theorem]
sources:
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (nondeterministic automata and their equivalence with deterministic automata)
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.2, Nondeterminism (Theorem 1.39, every NFA has an equivalent DFA, and its proof)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.3.5, Equivalence of Deterministic and Nondeterministic Finite Automata, and Section 2.3.6, A Bad Case for the Subset Construction
  - paper: doi:10.1109/T-C.1971.223108
    title: Frank R. Moore, On the bounds for state-set size in the proofs of equivalence between deterministic, nondeterministic, and two-way finite automata, IEEE Transactions on Computers C-20(10) (1971)
    locator: pp. 1211 to 1214 (n-state NFAs whose equivalent DFAs need 2^n states)
  - paper: "Oleg B. Lupanov, A comparison of two types of finite sources, Problemy Kibernetiki 9 (1963)"
    locator: pp. 321 to 326
  - paper: "Marek Chrobak, Finite automata and unary languages, Theoretical Computer Science 47 (1986)"
    locator: pp. 149 to 158 (the conversion of unary NFAs to DFAs)
  - url: "https://en.wikipedia.org/wiki/Powerset_construction"
    locator: lead (first published by Rabin and Scott in 1959) and section Complexity (the bound is reached, Lupanov 1963 and Moore 1971)
---

The Rabin-Scott theorem says that for each [nondeterministic finite automaton](/nondeterministic-finite-automaton/) with $n$ states there is a [deterministic finite automaton](/deterministic-finite-automaton/) with at most $2^n$ states that accepts the same language. So NFAs accept exactly the [regular languages](/regular-language/), and nondeterminism changes only the size of the automaton. The proof is the [subset construction](/subset-construction/), and the bound $2^n$ is reached for each $n$, even over a two-letter alphabet.

## Statement

An NFA is $N = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to \mathcal{P}(Q)$, one start state and no $\varepsilon$-moves, as on the [NFA](/nondeterministic-finite-automaton/) page. It need not be complete: $\delta(q, a) = \emptyset$ is allowed. An [epsilon-NFA](/epsilon-nfa/) has $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$. A DFA $M = (Q', \Sigma, \delta', q_0', F')$ is complete, with $\delta' : Q' \times \Sigma \to Q'$, and has no $\varepsilon$-moves.

**Theorem (Rabin and Scott, 1959).** Let $N$ be an NFA or an epsilon-NFA with $n$ states. Then there is a DFA $M$ with at most $2^n$ states and $L(M) = L(N)$. The DFA is the *subset automaton*

$$M = (\mathcal{P}(Q), \Sigma, \delta', q_0', F'), \quad \delta'(S, a) = E\Big( \bigcup_{q \in S} \delta(q, a) \Big), \quad q_0' = E(\{q_0\}), \quad F' = \{ S : S \cap F \ne \emptyset \},$$

where $E(S)$ is the [epsilon-closure](/epsilon-closure/) of $S$, the set of states reachable from $S$ by $\varepsilon$-moves alone. For an NFA without $\varepsilon$-moves, $E(S) = S$.

**Corollary.** A language is regular if and only if some NFA accepts it, if and only if some epsilon-NFA accepts it.

## In plain words

An NFA can be in several states at once, because a letter can lead to more than one state. A DFA can copy this by using one state for each *set* of NFA states. After each letter, the DFA moves to the set of all NFA states that some choice of moves can reach. It accepts when this set contains an accepting state of the NFA.

There are only finitely many sets of states, so the copy is a finite automaton. The price is size: with $n$ NFA states there can be up to $2^n$ sets, and for some NFAs all of them are needed.

## Proof

For a string $w$, let $R(w)$ be the set of states in which some run of $N$ on $w$ ends. For an epsilon-NFA, a run on $w = a_1 \cdots a_\ell$ is a path of moves from $q_0$ whose labels are $a_1, \ldots, a_\ell$ in this order, with any number of $\varepsilon$ labels before, between and after them. By the definition of acceptance, $w \in L(N)$ if and only if $R(w) \cap F \ne \emptyset$.

**Lemma.** For each $w \in \Sigma^*$, $\delta'^*(q_0', w) = R(w)$.

*Proof.* By induction on $|w|$.

For $w = \varepsilon$, a run on $\varepsilon$ uses only $\varepsilon$-moves from $q_0$, so $R(\varepsilon) = E(\{q_0\}) = q_0'$.

Let $w = v a$ with $a \in \Sigma$, and assume $\delta'^*(q_0', v) = R(v)$. Then $\delta'^*(q_0', va) = \delta'(R(v), a) = E(\bigcup_{q \in R(v)} \delta(q, a))$. We show that this set equals $R(va)$.

($\subseteq$) Let $r$ be in the set. Then there are $q \in R(v)$, $p \in \delta(q, a)$, and a path of $\varepsilon$-moves from $p$ to $r$. A run on $v$ that ends in $q$, then the $a$-move to $p$, then the $\varepsilon$-path to $r$, is a run on $va$ that ends in $r$. So $r \in R(va)$.

($\supseteq$) Let $r \in R(va)$, and take a run on $va$ that ends in $r$. Its last move with a label in $\Sigma$ has the label $a$; say it goes from $q$ to $p$, so $p \in \delta(q, a)$. The part of the run before this move is a run on $v$, so $q \in R(v)$. The part after it uses only $\varepsilon$-moves, so $r \in E(\{p\})$. Thus $r \in E(\bigcup_{q \in R(v)} \delta(q, a))$. $\square$

*Proof of the theorem.* $M$ is a complete DFA: for each $S \subseteq Q$ and $a \in \Sigma$, $\delta'(S, a)$ is one subset of $Q$. It has $|\mathcal{P}(Q)| = 2^n$ states. By the lemma and the definition of $F'$, $w \in L(M) \iff R(w) \in F' \iff R(w) \cap F \ne \emptyset \iff w \in L(N)$.

For the corollary, each DFA is an NFA whose sets $\delta(q, a)$ have one element, and each NFA is an epsilon-NFA with no $\varepsilon$-moves. The theorem gives the third inclusion. $\blacksquare$

The [subset construction](/subset-construction/) builds only the subsets that are reachable from $q_0'$. These are the sets $R(w)$, so the reachable part has at most $2^n$ states, and often far fewer. Its proof of correctness, with the closure computation, is on that page.

## Consequences

- **The NFA languages are the regular languages.** This makes the NFA the convenient tool for the [closure properties](/closure-properties-of-regular-languages/): union, concatenation, star and reversal have small NFA constructions, and the theorem turns them back into DFAs. Kleene's theorem uses the same route from a [regular expression](/regular-expression/) to a DFA.
- **Complement and difference need determinization.** To complement an NFA, determinize it and swap the accepting and non-accepting states of the complete DFA. Swapping the accepting states of an NFA does not complement its language in general. The cost is the $2^n$ blowup, and it cannot be avoided: some languages with $n$-state NFAs have complements whose smallest NFAs have $2^n$ states (see [state complexity](/state-complexity/)).
- **Decision procedures.** Universality and equivalence of NFAs become questions about DFAs with up to $2^n$ states, so they are decidable in $O(2^n)$ time times a polynomial. They are PSPACE-complete ([NFA universality](/nfa-universality/), [NFA equivalence](/nfa-equivalence/)), so an exponential cost in the worst case is expected.
- **A bound on the size of the minimal DFA.** The minimal DFA of $L(N)$ has at most $2^n$ states. By the [Myhill-Nerode theorem](/myhill-nerode-theorem/), $L(N)$ has at most $2^n$ classes: two strings $u, v$ with $R(u) = R(v)$ are equivalent.

## Tightness

The bound $2^n$ cannot be lowered. Lupanov (1963) and Moore (1971) gave $n$-state NFAs whose equivalent DFAs all have $2^n$ states. Here is a binary example with a complete proof.

**Witness.** For $n \ge 1$, let $A_n$ have the states $Q = \{0, 1, \ldots, n - 1\}$, the alphabet $\{a, b\}$, start state 0 and $F = \{0\}$, with

$$\delta(i, a) = \{ (i + 1) \bmod n \} \text{ for } i \ne 0, \quad \delta(0, a) = \{0, 1 \bmod n\}, \quad \delta(0, b) = \emptyset, \quad \delta(i, b) = \{i\} \text{ for } i \ne 0.$$

On a set $S$ of states, $b$ removes 0: $\delta'(S, b) = S \setminus \{0\}$. The letter $a$ adds 1 to each element modulo $n$, and keeps 0 if 0 is in $S$: $\delta'(S, a) = (S + 1) \cup (S \cap \{0\})$. If $0 \notin S$ or $n - 1 \in S$, then $0 \in S + 1$ or $S \cap \{0\} = \emptyset$, so in both cases $\delta'(S, a) = S + 1$, a pure rotation.

**Claim.** In the subset automaton of $A_n$, all $2^n$ subsets of $Q$ are reachable from $\{0\}$, and they are pairwise distinguishable. So the smallest DFA for $L(A_n)$ has exactly $2^n$ states.

*Proof of reachability.* By induction on $k$, $\delta'^*(\{0\}, a^k) = \{0, 1, \ldots, k\}$ for $0 \le k \le n - 1$, because 0 stays and each element moves up by one. So the full set $Q$ is reachable by $a^{n-1}$. Let $T \subseteq Q$ be a target. Start from $Q$ and do $n - 1$ steps, for $j = 0, 1, \ldots, n - 2$: if $n - 1 - j \notin T$, read $b$; then read $a$. After the $n - 1$ steps, read $b$ once more if $0 \notin T$. Track an element $x$ of the full set: after $j$ rotations it sits at $x + j$, so at step $j$ the element at position 0 is $x = -j \bmod n$, and it ends at position $-j + (n - 1) \equiv n - 1 - j$. The $b$ at step $j$ removes exactly the element that would end at position $n - 1 - j$. Each $a$ is a pure rotation: before the $a$ of step $j$, the element at position $n - 1$ is $x = -j - 1 \bmod n$, which is examined only at step $j + 1$, so it has not been removed. The last $b$ removes the element that ends at 0. So the final set is $T$.

*Proof of distinguishability.* Let $S \ne T$, and take $i$ in exactly one of them; by symmetry $i \in S \setminus T$. If $i = 0$, the empty string separates them, since $F' = \{ U : 0 \in U \}$. If $i \ge 1$, take $z = b (ab)^{n - i - 1} a$. The first $b$ removes 0. After that, before each $a$ the set does not contain 0, so each $a$ is a pure rotation, and each $b$ removes the element that has just reached 0. An element $j \ge 1$ reaches 0 after exactly $n - j$ letters $a$. The string $z$ has $n - i$ letters $a$, and a $b$ follows each of them except the last. So the elements $j > i$ reach 0 early and are removed, the elements $j < i$ do not reach 0, and $i$ reaches 0 at the last $a$. Hence $\delta'^*(U, z)$ contains 0 if and only if $i \in U$, and $z$ is accepted from $S$ and rejected from $T$. $\square$

For example, in $A_3$ the string $aa$ reaches $\{0, 1, 2\}$, and then $a\,ba$ reaches $\{0, 2\}$: $\{0, 1, 2\} \xrightarrow{a} \{0, 1, 2\} \xrightarrow{b} \{1, 2\} \xrightarrow{a} \{0, 2\}$.

**A natural example.** The language of strings over $\{a, b\}$ whose $n$-th symbol from the end is $a$ has an NFA with $n + 1$ states, and its smallest DFA has $2^n$ states, because all $2^n$ strings of length $n$ are pairwise distinguishable. The proof is on the [NFA](/nondeterministic-finite-automaton/) page, and more lower bounds are on the [determinization blowup](/determinization-blowup-lower-bound/) page.

**Unary alphabets.** Over one letter the bound is much smaller: Chrobak showed that an $n$-state unary NFA has an equivalent DFA with $e^{\Theta(\sqrt{n \ln n})}$ states, and that this is tight. See [state complexity](/state-complexity/).

## History

Rabin and Scott defined nondeterministic finite automata and proved this theorem in their 1959 paper "Finite automata and their decision problems". Lupanov (1963) and Moore (1971) showed that the exponential bound is reached.

## References
