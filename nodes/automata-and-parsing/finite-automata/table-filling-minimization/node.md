---
tag: ZY1X60
kind: algorithm
slug: table-filling-minimization
name: Table-filling DFA minimization
aliases:
- Myhill-Nerode table filling
- table-filling algorithm
- pair marking algorithm
area: automata-and-parsing/finite-automata
level: core
summary: Marks pairs of distinguishable states in a table, propagating distinctions backwards until no more are found, then merges the unmarked pairs.
solves: [dfa-minimization]
model: word-ram
complexity:
  vars: {n: the number of states, σ: the alphabet size}
  time: {worst: O(σ n^2)}
  space: {extra: O(σ n^2)}
properties: {deterministic: true, recursive: false}
history:
  year: 1979
  people: [John E. Hopcroft, Jeffrey D. Ullman]
  note: Their textbook gave the marking of pairs of inequivalent states with a list of waiting pairs for each pair, which makes the method run in time quadratic in the number of states.
prereqs: [deterministic-finite-automaton, myhill-nerode-theorem]
see_also: [dfa-minimization, moore-minimization, hopcroft-minimization, brzozowski-minimization, minimal-dfa-uniqueness, myhill-nerode-relation, dfa-equivalence, partition-refinement]
sources:
  - book: isbn:9780321455369
    title: John E. Hopcroft, Rajeev Motwani and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, third edition
    locator: Section 4.4.1, Testing Equivalence of States (the table-filling algorithm and its correctness), Section 4.4.2, Testing Equivalence of Regular Languages, and Section 4.4.3, Minimization of DFA's
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, first edition, Addison-Wesley, 1979
    locator: Section 3.4, The Myhill-Nerode Theorem and Minimization of Finite Automata (the marking algorithm with lists of pairs)
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lectures 13 and 14 (minimization by collapsing equivalent states, and the algorithm that marks pairs)
  - paper: "Edward F. Moore, Gedanken-experiments on sequential machines, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 129 to 153 (equivalent states of a sequential machine and the experiments that separate them)
---

The table-filling algorithm minimizes a complete [deterministic finite automaton](/deterministic-finite-automaton/) by deciding, for every pair of states, whether some input string leads one of them to acceptance and the other not. It first marks the pairs with exactly one accepting state, then marks a pair whenever some symbol leads it to a marked pair, and merges all pairs that stay unmarked. By the [Myhill-Nerode theorem](/myhill-nerode-theorem/) the result, built on the reachable states, is the unique minimal DFA. With a list of waiting pairs for each pair, it runs in $O(\sigma n^2)$ time; it is slower than [Hopcroft's algorithm](/hopcroft-minimization/), but it is short, easy to prove, and it gives a distinguishing string for each pair.

## In plain words

Two states of a machine are "the same" if no continuation of the input can ever show a difference: from both, the same strings lead to acceptance. The algorithm finds all pairs that are different, and merges the rest.

Draw a table with one cell for each pair of states. First put a mark in each cell where one state accepts and the other does not; the empty string tells them apart. Then repeat: if a letter takes a pair to a marked pair, mark that pair too, because that letter followed by the old difference tells them apart. When no new marks appear, every unmarked pair is truly equivalent. Merge these, and the machine is as small as possible.

## The problem

The input is a complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$ and no $\varepsilon$-moves. The output is a complete DFA $M'$ with $L(M') = L(M)$ and the least number of states. This is [DFA minimization](/dfa-minimization/).

States $p$ and $q$ are *distinguishable* if some $z \in \Sigma^*$ has exactly one of $\delta^*(p, z)$ and $\delta^*(q, z)$ in $F$, and *equivalent* otherwise. On the reachable states, equivalence is the [Myhill-Nerode relation](/myhill-nerode-relation/) moved from strings to states.

## The algorithm

```pseudo id=main
TABLE-FILLING(M)                       ▷ M = (Q, Σ, δ, q0, F) complete
L1  R ← the states reachable from q0      ▷ a breadth-first search
L2  for each pair {p, q} of distinct states of R do D[p, q] ← false;  S[p, q] ← an empty list
L3  K ← an empty stack
L4  for each pair {p, q} with p ∈ F and q ∉ F do D[p, q] ← true;  push {p, q} on K
L5  for each pair {p, q} and each a ∈ Σ with δ(p, a) ≠ δ(q, a) do append {p, q} to S[δ(p, a), δ(q, a)]
L6  while K is not empty do
L7      {r, s} ← pop K
L8      for each {p, q} in S[r, s] with D[p, q] = false do
L9          D[p, q] ← true;  push {p, q} on K
L10 for each p ∈ R do C[p] ← the first state q of R, in a fixed order, with q = p or D[p, q] = false
L11 Q' ← { C[p] : p ∈ R };  δ'(C[p], a) ← C[δ(p, a)];  F' ← { C[p] : p ∈ F ∩ R }
L12 return M' = (Q', Σ, δ', C[q0], F')
```

Line L1 drops the unreachable states, which no input can visit and which would otherwise stay in the output. Line L4 marks the pairs that the empty string separates. Line L5 records, for each pair $\{r, s\}$, the pairs that some symbol leads to $\{r, s\}$; these are the pairs that wait for $\{r, s\}$. Lines L6 to L9 spread the marks backwards along the symbols: when $\{r, s\}$ is known to be distinguishable, every pair waiting for it is too. Line L10 picks one representative per class of unmarked pairs, and lines L11 and L12 build the quotient.

The classic textbook form replaces lines L5 to L9 by rounds: in each round, mark every unmarked pair that some symbol leads to a marked pair, and stop after a round with no new mark. It marks the same pairs, but it can need $n - 1$ rounds of $O(\sigma n^2)$ work each.

## Example

The DFA below accepts the strings over $\{a, b\}$ that end in $ab$, with each state of the minimal DFA copied once, and with one unreachable state 6. The start state is 0 and $F = \{2, 5\}$.

| state | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| on $a$ | 1 | 4 | 4 | 1 | 1 | 1 | 6 |
| on $b$ | 3 | 2 | 3 | 0 | 5 | 0 | 2 |

Line L1 drops state 6. Line L4 marks the 8 pairs that contain exactly one of 2 and 5. Lines L6 to L9 then mark 4 more pairs, each through the symbol $b$: $\{0, 1\}$ goes to $\{3, 2\}$, $\{1, 3\}$ to $\{2, 0\}$, $\{0, 4\}$ to $\{3, 5\}$, and $\{3, 4\}$ to $\{0, 5\}$. The table shows a shortest distinguishing string in each marked cell, and $\equiv$ in the 3 cells that stay unmarked.

| | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| **1** | $b$ | | | | |
| **2** | $\varepsilon$ | $\varepsilon$ | | | |
| **3** | $\equiv$ | $b$ | $\varepsilon$ | | |
| **4** | $b$ | $\equiv$ | $\varepsilon$ | $b$ | |
| **5** | $\varepsilon$ | $\varepsilon$ | $\equiv$ | $\varepsilon$ | $\varepsilon$ |

The classes are $\{0, 3\}$, $\{1, 4\}$ and $\{2, 5\}$. The quotient has 3 states: $[0] \xrightarrow{a} [1]$, $[0] \xrightarrow{b} [0]$, $[1] \xrightarrow{a} [1]$, $[1] \xrightarrow{b} [2]$, $[2] \xrightarrow{a} [1]$, $[2] \xrightarrow{b} [0]$, with $[2]$ accepting. This is the minimal DFA for "ends in $ab$": no state, then "last symbol $a$", then "last two symbols $ab$".

## Correctness

The main claim is that, when the loop stops, a pair is marked if and only if its states are distinguishable. *Soundness*: a pair marked at line L4 is separated by $\varepsilon$, and a pair marked at line L9 has a symbol $a$ that leads it to a marked pair $\{r, s\}$, so $a$ followed by the string that separates $r$ and $s$ separates it. *Completeness*: by induction on the length of a shortest separating string $az$, the pair $\{\delta(p, a), \delta(q, a)\}$ is marked, so it is pushed and later popped, and then line L8 reads its list, which contains $\{p, q\}$.

Equivalence of states is an equivalence relation that the transitions and $F$ respect, so the quotient of lines L10 to L12 is well defined and accepts $L(M)$. Its states are reachable and pairwise distinguishable, so they correspond to different Myhill-Nerode classes, and no complete DFA for $L(M)$ has fewer states. The full proof is in the proof file below.

## Complexity

Let $n = |R|$ and $\sigma = |\Sigma|$.

- **Time.** There are $\binom{n}{2}$ pairs. Lines L2 to L5 do $O(\sigma)$ work per pair, and the lists hold at most $\sigma \binom{n}{2}$ entries. Each pair is pushed at most once, so each list is read at most once in lines L6 to L9. So the time is $O(\sigma n^2)$ in the worst case, on the [word RAM](/word-ram/) with the table stored as an array indexed by pairs. The search of line L1 adds $O(|Q| \sigma)$.
- **Space.** The table and the lists: $O(\sigma n^2)$. Without the lists (the round-based form), the space is $O(n^2)$ but the time is $O(\sigma n^3)$ in the worst case, since there can be $n - 1$ rounds.
- **The bound is tight for this method.** The table has $\binom{n}{2}$ cells, and each is written, so the algorithm takes $\Omega(n^2)$ time on every input with $n$ reachable states.
- **Comparison.** [Moore's algorithm](/moore-minimization/) refines a partition in $O(\sigma n^2)$ worst-case time and $O(n + \sigma n)$ space, and [Hopcroft's algorithm](/hopcroft-minimization/) takes $O(\sigma n \log n)$.

## Properties

- **Exact.** The output is the minimal complete DFA, unique up to the names of the states by the [uniqueness of the minimal DFA](/minimal-dfa-uniqueness/).
- **Witnesses.** If each mark also records the symbol and the pair that caused it, following these records gives a distinguishing string for each marked pair, of the least length when the marks are processed in breadth-first order instead of with a stack.
- **Quadratic memory.** The table has a cell for each pair, so the method does not scale to DFAs with millions of states, where partition refinement is used.
- **Deterministic and iterative.** No recursion: the stack $K$ replaces the recursive marking of the textbook version.

## Variants and improvements

- **Round-based marking.** Repeat passes over all unmarked pairs until nothing changes. Simpler, $O(n^2)$ space, $O(\sigma n^3)$ time.
- **Equivalence of two DFAs.** Put the two DFAs side by side as one DFA with two start states, run the marking, and check whether the two start states are marked. They are unmarked if and only if the languages are equal ([DFA equivalence](/dfa-equivalence/)). [Hopcroft and Karp's algorithm](/hopcroft-karp-equivalence/) does this test in almost linear time.
- **Partition refinement.** [Moore's algorithm](/moore-minimization/) computes the same relation as a partition, one round per length of the distinguishing strings, and [Hopcroft's algorithm](/hopcroft-minimization/) processes the smaller half of each split. See [partition refinement](/partition-refinement/).
- **Brzozowski's method.** [Brzozowski's algorithm](/brzozowski-minimization/) reverses and determinizes twice and needs no table, but it can take exponential time.
- **Bisimulation.** On transition systems and NFAs, the same marking computes bisimilarity, a finer relation than language equivalence, which gives a smaller NFA that is not always minimal.

## When to use it

Use the table-filling algorithm for small DFAs, for teaching, and when you need a distinguishing string for each pair of states, for example to explain why two states cannot be merged or to produce test inputs. For large DFAs, use Hopcroft's algorithm, or Moore's algorithm when simplicity and linear memory matter more than the $\log n$ factor.

## Pitfalls

- **Keeping unreachable states.** The marking only merges equivalent states. An unreachable state that is not equivalent to any reachable one, such as a second accepting sink that no input reaches, stays in the output, which is then not minimal. Remove the unreachable states first, as in line L1.
- **Partial DFAs.** With missing transitions, line L5 has no successor pair, and a pair with a missing move on one side can be left unmarked by mistake. Complete the DFA with a dead state first.
- **Ordered pairs.** The table is over unordered pairs: $\{p, q\}$ and $\{q, p\}$ are one cell. Store the pair with the smaller index first, or the marks of one half are never seen.
- **Pairs with equal successors.** If $\delta(p, a) = \delta(q, a)$, the symbol $a$ cannot separate $p$ and $q$, and there is no pair to wait for. Line L5 skips it.
- **Stopping after one round.** In the round-based form, one pass is not enough: a pair can become distinguishable only after another pair is marked later in the same pass. Repeat until a pass makes no change.
- **Recursion.** Marking the waiting pairs by a recursive call can go $\binom{n}{2}$ levels deep. Use an explicit stack.

## Implementations

## History

Moore (1956) studied the experiments that separate states of a sequential machine, the idea behind the table. Hopcroft and Ullman (1979) gave the form with a list of waiting pairs for each pair, and with the bound quadratic in the number of states. Hopcroft, Motwani and Ullman call it the table-filling algorithm.

## References
