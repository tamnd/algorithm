---
tag: 2Q2G89
kind: algorithm
slug: product-construction
name: Product construction
aliases:
- cross-product construction
- synchronous product
- direct product of automata
area: automata-and-parsing/finite-automata
level: core
summary: Runs two automata in parallel on pair states to recognize intersections, unions and other Boolean combinations.
solves: [regular-language-intersection]
model: word-ram
complexity:
  vars: {n: the number of states of the first DFA, k: the number of states of the second DFA, σ: the alphabet size}
  time: {worst: O(n k σ)}
  space: {extra: O(n k σ)}
properties: {deterministic: true, recursive: false}
history:
  year: 1959
  people: [Michael O. Rabin, Dana Scott]
  note: Rabin and Scott defined the direct product of two automata, with pairs of states, to build an automaton for the intersection in one step.
prereqs: [deterministic-finite-automaton]
see_also: [regular-language-intersection, closure-properties-of-regular-languages, dfa-emptiness, dfa-equivalence, nfa-equivalence, ltl-model-checking, state-complexity, hopcroft-karp-equivalence]
sources:
  - paper: doi:10.1147/rd.32.0114
    title: Michael O. Rabin and Dana Scott, Finite automata and their decision problems, IBM Journal of Research and Development 3(2) (1959)
    locator: Definition 7 (the direct product of two automata), pp. 114 to 125
  - book: isbn:9781133187790
    title: Michael Sipser, Introduction to the Theory of Computation, third edition
    locator: Section 1.1, Finite Automata (Theorem 1.25, the class of regular languages is closed under union, proved with pairs of states)
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.2.1, Closure of Regular Languages Under Boolean Operations (the product automaton for intersection)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 4, More on Regular Sets (the product construction)
---

The product construction builds one [deterministic finite automaton](/deterministic-finite-automaton/) that runs two DFAs side by side. Its states are pairs $(p, q)$ of a state of each DFA, and a pair is accepting when a chosen Boolean function of "the first DFA accepts" and "the second DFA accepts" is true. With "and" it gives the intersection of the two languages, with "or" the union, and with other functions the difference and the symmetric difference. For DFAs with $n_1$ and $n_2$ states it builds at most $n_1 n_2$ states in $O(n_1 n_2 \sigma)$ time, and some pairs of languages need all of them.

## In plain words

Suppose you want to check two rules about a string at once, and you have a machine for each rule. Feed every letter to both machines at the same time, and write down the pair of states that they are in. The pair after the last letter tells you whether each machine accepts. Then you decide: both accept, at least one accepts, the first accepts and the second does not, and so on.

The pairs behave like the states of one machine, because the next pair depends only on the current pair and the letter. The construction makes this machine, and it builds only the pairs that some input can reach.

## The problem

The input is two complete DFAs over the same alphabet, $M_1 = (Q_1, \Sigma, \delta_1, s_1, F_1)$ and $M_2 = (Q_2, \Sigma, \delta_2, s_2, F_2)$, with $\delta_i : Q_i \times \Sigma \to Q_i$ and no $\varepsilon$-moves, and a Boolean function $\mathrm{op} : \{0, 1\}^2 \to \{0, 1\}$. The output is a complete DFA $P$ with

$$L(P) = \{ w \in \Sigma^* : \mathrm{op}(w \in L(M_1),\ w \in L(M_2)) \}.$$

For op = and this is the [intersection](/regular-language-intersection/) $L(M_1) \cap L(M_2)$.

## The algorithm

```pseudo id=main
PRODUCT(M1, M2, op)                    ▷ complete DFAs over one alphabet Σ
L1  s ← (s1, s2)
L2  Q ← {s};  W ← a queue that holds s
L3  while W is not empty do
L4      (p, q) ← remove the first pair of W
L5      for each a ∈ Σ do
L6          t ← (δ1(p, a), δ2(q, a))
L7          if t ∉ Q then add t to Q and to the end of W
L8          δ((p, q), a) ← t
L9  F ← { (p, q) ∈ Q : op(p ∈ F1, q ∈ F2) }
L10 return P = (Q, Σ, δ, s, F)
```

Line L1 pairs the two start states. Lines L3 to L8 explore the pairs that some string reaches, in breadth-first order, and line L6 moves both DFAs on the same symbol. Line L9 is the only line that depends on op, so one search serves all sixteen Boolean functions. The full product $Q_1 \times Q_2$ accepts the same language; the search only leaves out the pairs that no string reaches.

## Example

Let $M_1$ accept the strings over $\{a, b\}$ with an even number of $a$s: states 0 (even) and 1 (odd), start 0, $F_1 = \{0\}$, where $a$ swaps the states and $b$ keeps them. Let $M_2$ accept the strings that contain $bb$: state 0 (no progress), 1 (the last symbol is a $b$), 2 (seen $bb$), start 0, $F_2 = \{2\}$, with $0 \xrightarrow{a} 0$, $0 \xrightarrow{b} 1$, $1 \xrightarrow{a} 0$, $1 \xrightarrow{b} 2$, and 2 a sink. The table lists the pairs in the order in which line L4 removes them.

| pair | on $a$ | on $b$ | and | or | $M_1$ but not $M_2$ | xor |
|---|---|---|---|---|---|---|
| $(0, 0)$ start | $(1, 0)$ | $(0, 1)$ | no | yes | yes | yes |
| $(1, 0)$ | $(0, 0)$ | $(1, 1)$ | no | no | no | no |
| $(0, 1)$ | $(1, 0)$ | $(0, 2)$ | no | yes | yes | yes |
| $(1, 1)$ | $(0, 0)$ | $(1, 2)$ | no | no | no | no |
| $(0, 2)$ | $(1, 2)$ | $(0, 2)$ | yes | yes | no | no |
| $(1, 2)$ | $(0, 2)$ | $(1, 2)$ | no | yes | no | yes |

All $2 \cdot 3 = 6$ pairs are reachable. For "and" and "xor" the six states are pairwise distinguishable, so the product is the minimal DFA. For "or" and for the difference, the minimal DFA has 5 states: for "or", $(0, 2)$ and $(1, 2)$ both accept everything that follows, so they merge; for the difference, both are dead and merge. On $abab$ the run is $(0,0), (1,0), (1,1), (0,0), (0,1)$: the string has two $a$s and no $bb$, so it is accepted by "or" and by the difference, and rejected by "and".

## Correctness

The main invariant is that after a string $w$ the product is in the pair of states that the two DFAs reach on $w$: $\delta^*(s, w) = (\delta_1^*(s_1, w), \delta_2^*(s_2, w))$. It holds for $w = \varepsilon$ by line L1, and line L6 keeps it, since both components move on the same symbol. Then line L9 makes $w$ accepted exactly when $\mathrm{op}(w \in L(M_1), w \in L(M_2))$ holds. The loop stops because each of the at most $n_1 n_2$ pairs enters the queue once. The full proof, with the reachability of the pairs and the role of completeness, is in the proof file below.

## Complexity

- **Time.** Each reachable pair is removed from $W$ once, and each removal costs $\sigma$ lookups and $\sigma$ tests of line L7. With an array indexed by $(p, q)$, or a hash table, each test is $O(1)$, so the time is $O(N \sigma)$ for $N \le n_1 n_2$ reachable pairs, and $O(n_1 n_2 \sigma)$ in the worst case.
- **Space.** The pairs and the table: $O(N \sigma)$, at most $O(n_1 n_2 \sigma)$.
- **Lower bound.** The output can need $n_1 n_2$ states. Let $M_1$ count the $a$s modulo $m$ and $M_2$ count the $b$s modulo $n$, each accepting at 0. The intersection is the set of strings with $|w|_a \equiv 0 \pmod m$ and $|w|_b \equiv 0 \pmod n$. The $mn$ strings $a^i b^j$ with $0 \le i < m$ and $0 \le j < n$ are pairwise distinguishable: the suffix $a^{m-i} b^{n-j}$ leads $a^i b^j$ into the language and each other $a^{i'} b^{j'}$ out of it. So the minimal DFA has $mn$ states, for all $m, n \ge 1$, by the [Myhill-Nerode theorem](/myhill-nerode-theorem/).

## Properties

- **Exact for all Boolean operations,** when both inputs are complete DFAs over the same alphabet.
- **Complete and deterministic output,** with only reachable states. It need not be minimal, as the example shows for "or".
- **One search for all operations.** Lines L1 to L8 do not depend on op.
- **Associative in practice.** A product of $k$ DFAs is built by repeated products or directly with $k$-tuples; it has at most $n_1 n_2 \cdots n_k$ states.

## Variants and improvements

- **Products of NFAs.** For [NFAs](/nondeterministic-finite-automaton/), the pairs with $\delta((p, q), a) = \delta_1(p, a) \times \delta_2(q, a)$ give an NFA for the intersection, with $n_1 n_2$ states. For union, complement and difference this is wrong; union of NFAs uses a new start state instead, and complement needs [determinization](/nfa-determinization/).
- **On-the-fly emptiness.** To decide whether $L(M_1) \cap L(M_2) = \emptyset$, run the search and stop at the first pair in $F_1 \times F_2$. This is [DFA emptiness](/dfa-emptiness/) on the product, without building the rest.
- **Equivalence.** $L(M_1) = L(M_2)$ if and only if no reachable pair has exactly one accepting component, which is the product with op = xor. [Hopcroft and Karp's algorithm](/hopcroft-karp-equivalence/) merges pairs with a union-find structure and needs almost linear time instead of $n_1 n_2$.
- **Many automata.** The product of $k$ DFAs can have $n^k$ states, and deciding whether the intersection of $k$ given DFAs is empty is PSPACE-complete when $k$ is part of the input (see [regular-language intersection](/regular-language-intersection/)).
- **Infinite words.** For [Büchi automata](/buchi-automaton/), the plain product with $F_1 \times F_2$ is wrong for intersection, because the two automata can visit their accepting states at different times. The standard fix adds a component that records which automaton the run waits for. [LTL model checking](/ltl-model-checking/) builds such a product of a system and a property automaton.
- **Different alphabets.** For systems that synchronize only on shared symbols, the product moves one component alone on a symbol that the other does not have. This is the product of transition systems used in [explicit-state model checking](/explicit-state-model-checking/).

## When to use it

Use the product when you need a DFA for a Boolean combination of two regular languages, or when you need to search the joint behavior of two automata: emptiness of an intersection, inclusion $L(M_1) \subseteq L(M_2)$ (the product with $x \wedge \neg y$ is empty), or equivalence. When the inputs are NFAs, use it only for intersection, or determinize first. When only equivalence of two DFAs is asked, Hopcroft and Karp's method is faster.

## Pitfalls

- **Partial DFAs.** If a DFA has missing transitions, line L6 cannot build a pair, and every string that falls into the gap is rejected. This keeps "and" correct but breaks "or", "xor" and the difference. Add a dead state first.
- **Different alphabets.** The two DFAs must read the same $\Sigma$. If one has an extra symbol, give the other a move to a dead state on it.
- **Accepting pairs for union.** For "or", a pair is accepting when either component is accepting, which is $(F_1 \times Q_2) \cup (Q_1 \times F_2)$, not $F_1 \times F_2$.
- **Complement by swapping on an NFA.** The difference $L_1 \setminus L_2$ is the product of $M_1$ with the complement of $M_2$, and the complement of an NFA is not the NFA with $F$ and $Q \setminus F$ swapped.
- **Building all pairs.** Making all of $Q_1 \times Q_2$ before the search costs $n_1 n_2 \sigma$ even when few pairs are reachable. Start from $(s_1, s_2)$ as in line L2.
- **Size of repeated products.** The product of $k$ automata grows as the product of their sizes. Minimize after each step when the results are combined further.

## Implementations

## History

Rabin and Scott (1959) defined the direct product of two automata, with pairs of states and $F_1 \times F_2$ as the accepting states, to build an automaton for the intersection of two sets in one step. Textbooks use the same pairs, with different accepting states, for union and the other Boolean operations.

## References
