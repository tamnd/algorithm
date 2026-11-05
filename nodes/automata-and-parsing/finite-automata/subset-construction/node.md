---
tag: 19CF15
kind: algorithm
slug: subset-construction
name: Subset construction
aliases:
- powerset construction
- NFA determinization
area: automata-and-parsing/finite-automata
level: intro
summary: Builds a DFA whose states are sets of NFA states, yielding an equivalent deterministic automaton.
solves: [nfa-determinization]
model: word-ram
complexity:
  vars: {n: the number of NFA states, m: the number of NFA transitions, σ: the alphabet size}
  time: {worst: O(2^n σ(n + m))}
  space: {extra: O(2^n (n + σ))}
properties: {deterministic: true, recursive: false}
history:
  year: 1959
  people: [Michael O. Rabin, Dana Scott]
  note: Rabin and Scott used the construction to prove that nondeterministic automata accept only regular sets.
prereqs: [nondeterministic-finite-automaton, epsilon-closure, deterministic-finite-automaton]
see_also: [rabin-scott-theorem, nfa-simulation, lazy-dfa-construction, determinization-blowup-lower-bound, brzozowski-minimization, hopcroft-minimization, thompson-construction, nfa-universality]
sources:
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.2, Nondeterminism (Theorem 1.39 and its proof, which handles the epsilon-arrows with the closure E(R))
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 2.3.5, Equivalence of Deterministic and Nondeterministic Finite Automata (the lazy evaluation of subsets), Section 2.3.6, A Bad Case for the Subset Construction, and Section 2.5.5, Eliminating epsilon-Transitions
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 6, The Subset Construction
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: pp. 114 to 125 (the definition of nondeterministic automata and the construction of an equivalent deterministic automaton)
---

The subset construction turns a [nondeterministic finite automaton](/nondeterministic-finite-automaton/) into a [deterministic one](/deterministic-finite-automaton/) that accepts the same language. Each state of the DFA is a set of NFA states: the set of states in which the NFA can be after the input read so far. The method builds only the sets that the input can reach, starting from the [epsilon-closure](/epsilon-closure/) of the start state. It proves the [Rabin-Scott theorem](/rabin-scott-theorem/), and its output can have $2^n$ states for an NFA with $n$ states, which is sometimes necessary.

## In plain words

An NFA can be in several states at the same time, because a letter can lead to several places. Suppose you write down, after each letter, the full set of states in which the NFA can be. The next set depends only on the current set and the next letter, not on the letters before. So the sets behave like the states of an ordinary automaton with one move per letter.

The construction makes this automaton. It starts from the set of the start state, plus every state that free moves reach from it. For each set it knows and each letter, it computes the next set. A set that it has not seen before becomes a new state. It stops when no new sets appear. A set is accepting when it holds an accepting state of the NFA.

## The problem

The input is an NFA $N = (Q, \Sigma, \delta, q_0, F)$ that may have $\varepsilon$-moves: $\delta : Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$, as on the [epsilon-NFA](/epsilon-nfa/) page. An NFA without $\varepsilon$-moves is the case $\delta(q, \varepsilon) = \emptyset$ for each $q$. The output is a complete DFA $D = (Q', \Sigma, \delta', S_0, F')$, without $\varepsilon$-moves, with $L(D) = L(N)$. This is the problem of [NFA determinization](/nfa-determinization/).

For a set $S \subseteq Q$, the closure $E(S)$ is the set of states that a path of zero or more $\varepsilon$-moves reaches from a state of $S$. A run of $N$ on a string may take any number of $\varepsilon$-moves before, between and after the symbols.

## The algorithm

```pseudo id=main
SUBSET-CONSTRUCTION(N)                 ▷ N = (Q, Σ, δ, q0, F), ε-moves allowed
L1  S0 ← CLOSE({q0})
L2  Q' ← {S0};  W ← a queue that holds S0
L3  while W is not empty do
L4      S ← remove the first set of W
L5      for each a ∈ Σ do
L6          T ← CLOSE(⋃ over q ∈ S of δ(q, a))
L7          if T ∉ Q' then add T to Q' and to the end of W
L8          δ'(S, a) ← T
L9  F' ← { S ∈ Q' : S ∩ F ≠ ∅ }
L10 return D = (Q', Σ, δ', S0, F')

CLOSE(S)                               ▷ the ε-closure E(S)
L11 C ← S;  K ← a stack that holds the elements of S
L12 while K is not empty do
L13     q ← pop K
L14     for each r ∈ δ(q, ε) with r ∉ C do add r to C and push r on K
L15 return C
```

Line L1 makes the start state of $D$: the states that $N$ can be in before it reads a symbol. Lines L3 to L8 explore the sets that $D$ can reach, in breadth-first order. Line L6 takes one step on $a$ from each state of $S$, then the $\varepsilon$-moves after it. Line L7 makes $T$ a new state of $D$ the first time it appears. The set $T$ can be empty; then it becomes a dead state, whose moves all lead back to $\emptyset$, and $D$ stays complete. Line L9 makes a set accepting when some run that it stands for can accept. CLOSE uses an explicit stack, so a long chain of $\varepsilon$-moves needs no recursion.

## Example

Let $N$ accept $a^* b^* \cup (ab)^*$, with $Q = \{0, 1, 2, 3, 4\}$, $q_0 = 0$ and $F = \{2, 3\}$. The moves are $0 \xrightarrow{\varepsilon} 1$, $0 \xrightarrow{\varepsilon} 3$, $1 \xrightarrow{a} 1$, $1 \xrightarrow{\varepsilon} 2$, $2 \xrightarrow{b} 2$ for the part $a^* b^*$, and $3 \xrightarrow{a} 4$, $4 \xrightarrow{b} 3$ for the part $(ab)^*$.

Line L1 gives $S_0 = E(\{0\}) = \{0, 1, 2, 3\}$. The table lists the sets in the order in which line L4 removes them.

| removed set $S$ | $\delta'(S, a)$ | $\delta'(S, b)$ | in $F'$ | new sets |
|---|---|---|---|---|
| $\{0,1,2,3\}$ | $\{1,2,4\}$ | $\{2\}$ | yes | $\{1,2,4\}$, $\{2\}$ |
| $\{1,2,4\}$ | $\{1,2\}$ | $\{2,3\}$ | yes | $\{1,2\}$, $\{2,3\}$ |
| $\{2\}$ | $\emptyset$ | $\{2\}$ | yes | $\emptyset$ |
| $\{1,2\}$ | $\{1,2\}$ | $\{2\}$ | yes | none |
| $\{2,3\}$ | $\{4\}$ | $\{2\}$ | yes | $\{4\}$ |
| $\emptyset$ | $\emptyset$ | $\emptyset$ | no | none |
| $\{4\}$ | $\emptyset$ | $\{3\}$ | no | $\{3\}$ |
| $\{3\}$ | $\{4\}$ | $\emptyset$ | yes | none |

The first row: from $\{0, 1, 2, 3\}$ on $a$, state 1 goes to 1 and state 3 goes to 4, and the closure of $\{1, 4\}$ adds 2. On $b$, only state 2 moves, to 2. The DFA has 8 of the $2^5 = 32$ possible sets, and none of its states can be merged: it is the smallest DFA for the language. On $abab$ the run of $D$ is $\{0,1,2,3\}, \{1,2,4\}, \{2,3\}, \{4\}, \{3\}$, which ends in $F'$; on $aba$ it ends in $\{4\}$, which is not accepting.

## Correctness

For a string $w$, let $R(w)$ be the set of states in which some run of $N$ on $w$, with $\varepsilon$-moves allowed, can end. The key invariant is that the state of $D$ after $w$ is exactly $R(w)$: $\delta'^*(S_0, w) = R(w)$. It holds for $w = \varepsilon$ because $R(\varepsilon) = E(\{q_0\}) = S_0$, and it is kept by line L6 because $R(wa) = E\big(\bigcup_{q \in R(w)} \delta(q, a)\big)$. Then $w \in L(D) \iff R(w) \cap F \ne \emptyset \iff w \in L(N)$. The loop stops because each set enters $W$ only once and there are at most $2^{|Q|}$ sets. The full proof, with the correctness of CLOSE, is in the proof file below.

## Complexity

Let $n = |Q|$, $m$ the number of transitions of $N$ (with the $\varepsilon$-moves), $\sigma = |\Sigma|$, and $N'$ the number of sets that the algorithm produces, so $N' \le 2^n$.

- **Time.** Each set is removed from $W$ once. For each of its $\sigma$ symbols, the union of line L6 reads at most all $m$ transitions and makes a set of at most $n$ states, CLOSE pushes each state at most once and reads each $\varepsilon$-move at most once, and the test of line L7 hashes a set of at most $n$ states. So one pair $(S, a)$ costs $O(n + m)$, and the total is $O(N' \sigma (n + m))$, which is $O(2^n \sigma (n + m))$. With a hash table the test of line L7 is $O(n)$ expected time; a trie over the bit vectors of the sets makes it $O(n)$ in the worst case.
- **Space.** $D$ has $N'$ sets of at most $n$ states and a table of $N' \sigma$ entries: $O(N' (n + \sigma))$, which is $O(2^n (n + \sigma))$.
- **Lower bound.** The language "the $n$-th symbol from the end is $a$" has an NFA with $n + 1$ states, and the construction produces $2^n$ sets for it. Its smallest DFA has $2^n$ states, so every determinization method needs $\Omega(2^n)$ time on it. See the [determinization blow-up lower bound](/determinization-blowup-lower-bound/).

The bound is output sensitive: when only a few sets are reachable, as in the example, the work is small.

## Properties

- **Exact language.** $L(D) = L(N)$, with no restriction on $N$.
- **Complete output.** The empty set is a state when it is reachable, so each state of $D$ has a move on each symbol.
- **Reachable states only.** Each state of $D$ is reachable from $S_0$. The output need not be minimal: two different sets can have the same future, and a [minimization](/dfa-minimization/) step can merge them.
- **Deterministic and iterative.** The order of $W$ fixes the numbering of the states; any order gives the same set of states and the same language.

## Variants and improvements

- **Lazy construction.** Build a set only when an input reaches it, and keep the sets in a cache. This is the [lazy DFA construction](/lazy-dfa-construction/) of regular expression engines.
- **Minimal output.** Run [Hopcroft's algorithm](/hopcroft-minimization/) on the result. [Brzozowski's algorithm](/brzozowski-minimization/) instead reverses and determinizes twice, and the second determinization gives the minimal DFA directly.
- **Bit vectors.** For $n$ up to the word size, a set is one machine word, and the union of line L6 is a few word operations per state.
- **Searches without the full DFA.** [NFA universality](/nfa-universality/) and [NFA equivalence](/nfa-equivalence/) explore the same sets and stop at the first counterexample. Antichains skip a set that contains a set already seen.
- **Infinite words.** For a [Büchi automaton](/buchi-automaton/) the plain subset construction is wrong, because acceptance depends on infinitely many visits to accepting states, and a set of states does not record which run made them. Determinization there needs a more complex construction.

## When to use it

Use the subset construction when the same automaton runs on many inputs, as in a lexical analyzer: the DFA reads each symbol with one table lookup. When the automaton runs on one input only, or when the DFA may be large, [NFA simulation](/nfa-simulation/) computes the same sets on the fly in $O(\ell (n + m))$ time and $O(n)$ space for an input of length $\ell$. A lazy DFA sits between the two.

## Pitfalls

- **No closure of the start state.** Line L1 must apply CLOSE to $\{q_0\}$. If it uses $\{q_0\}$, the DFA misses the states that $\varepsilon$-moves reach before the first symbol, and in the example it rejects $b$.
- **No closure after a step.** Line L6 must close the union. Without the closure, the move of $\{0,1,2,3\}$ on $a$ gives $\{1, 4\}$, which misses state 2, so the DFA rejects $a$.
- **Dropping the empty set.** If line L7 skips $T = \emptyset$, the DFA is partial. Its complement, made by swapping $F'$ and $Q' \setminus F'$, is then wrong, as the [DFA](/deterministic-finite-automaton/) page explains.
- **Accepting by inclusion.** Line L9 tests $S \cap F \ne \emptyset$. The test $S \subseteq F$ accepts only when all runs accept, which is a different language.
- **All subsets at once.** Making all $2^n$ subsets, reachable or not, costs $\Theta(2^n)$ even when few are reachable. Explore from $S_0$ as in line L3.
- **Mutable keys.** A set that serves as a key of a dictionary must not change after it is stored. Use an immutable set or a bit vector.

## Implementations

## History

Rabin and Scott (1959) defined nondeterministic finite automata and used this construction to prove that they accept the same sets as deterministic ones. The handling of $\varepsilon$-moves by a closure appears in the textbooks of Hopcroft, Motwani and Ullman and of Sipser. The lazy form, which builds only the subsets that the input needs, is the usual method in regular expression engines.

## References
