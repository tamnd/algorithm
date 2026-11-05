---
tag: HJJDQK
kind: algorithm
slug: hopcroft-minimization
name: Hopcroft's DFA minimization algorithm
aliases:
- Hopcroft partition refinement
area: automata-and-parsing/finite-automata
level: core
summary: Minimizes a DFA in O(n log n) time by refining a partition of states, processing the smaller half first.
solves: [dfa-minimization]
model: word-ram
complexity:
  vars: {n: the number of states, σ: the alphabet size}
  time: {worst: O(σ n log n)}
  space: {extra: O(σ n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1971
  people: [John E. Hopcroft]
  note: Hopcroft published the algorithm in the volume Theory of Machines and Computations in 1971.
prereqs: [dfa-minimization, partition-refinement, moore-minimization]
see_also: [moore-minimization, brzozowski-minimization, table-filling-minimization, minimal-dfa-uniqueness, myhill-nerode-relation, bisimulation, hopcroft-karp-equivalence]
sources:
  - paper: "John E. Hopcroft, An n log n algorithm for minimizing states in a finite automaton, in Z. Kohavi and A. Paz (eds.), Theory of Machines and Computations, Academic Press, 1971"
    locator: pp. 189 to 196
  - paper: "David Gries, Describing an algorithm by Hopcroft, Acta Informatica 2(2) (1973)"
    locator: pp. 97 to 109 (a structured presentation and proof of the algorithm)
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Section 4.13, Partitioning (the smaller-half partitioning algorithm and its application to finite automata)
  - paper: doi:10.1137/0216062
    title: Robert Paige and Robert E. Tarjan, Three partition refinement algorithms, SIAM Journal on Computing 16(6) (1987)
    locator: pp. 973 to 989
  - paper: "Jean Berstel and Olivier Carton, On the complexity of Hopcroft's state minimization algorithm, Implementation and Application of Automata (CIAA 2004), Lecture Notes in Computer Science 3317, Springer, 2005"
    locator: pp. 35 to 44 (unary automata on which the algorithm takes Θ(n log n) time)
---

Hopcroft's algorithm [minimizes a DFA](/dfa-minimization/) in $O(\sigma n \log n)$ time, for $n$ states and $\sigma$ symbols, which is the best worst-case bound known. Like [Moore's algorithm](/moore-minimization/) it refines a partition of the states, starting from the accepting and the rejecting states, until states in one block are equivalent. Instead of rounds, it keeps a work list of *splitters*: a pair of a block $S$ and a symbol $a$ splits each block into the states that move into $S$ on $a$ and the others. When a block splits, only the smaller half needs to become a new splitter, and this "smaller half" rule gives the logarithmic factor. It is the classic case of [partition refinement](/partition-refinement/).

## In plain words

Start with two groups of states: those that say yes and those that say no. A group can serve as a test: for a letter, ask each state "does this letter take you into that group?" If the members of some other group give different answers, that group must split, because some ending tells its members apart.

The algorithm keeps a list of tests to run. A test may split groups, and new groups bring new tests. The trick is in which tests to add. When a group splits in two, a test with one half tells the same as a test with the other half, since the whole group was already tested or still waits. So only the smaller half is added. A state can be in a smaller half only a few times, since each time its group at least halves, and this keeps the total work small.

## The problem

The input is a complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$, no $\varepsilon$-moves, $n = |Q|$ and $\sigma = |\Sigma|$. The output is the minimal complete DFA for $L(M)$ and the map from each reachable state to its state in the output. This is [DFA minimization](/dfa-minimization/).

## The algorithm

$P$ is the partition, and $W$ is the work list of pairs (block, symbol). A pair in $W$ refers to the current contents of its block. For a set $S$, $\delta_a^{-1}(S)$ is the set of states $q$ with $\delta(q, a) \in S$.

```pseudo id=main
HOPCROFT-MINIMIZE(Q, Σ, δ, q0, F)
L1  R ← the states reachable from q0                      ▷ graph search
L2  for each a ∈ Σ and r ∈ R: pre_a(r) ← { q ∈ R : δ(q, a) = r }
L3  P ← the non-empty sets among F ∩ R and R \ F
L4  W ← ∅; if |P| = 2 then add (the smaller block of P, a) to W for each a ∈ Σ
L5  while W ≠ ∅ do
L6      remove a pair (S, a) from W
L7      X ← the union of pre_a(r) over r ∈ S                ▷ X = δ_a^{-1}(S)
L8      for each block B of P with B ∩ X ≠ ∅ and B ⊄ X do
L9          replace B in P by B1 = B ∩ X and B2 = B \ X
L10         for each c ∈ Σ do
L11             if (B, c) ∈ W then replace (B, c) in W by (B1, c) and (B2, c)
L12             else add (the smaller of B1 and B2, c) to W
L13 return the quotient DFA whose states are the blocks of P
```

Lines L1 and L2 drop the unreachable states and build the reverse edges for each symbol. Line L3 sets up the first partition, and line L4 puts the smaller of its two blocks in the work list with each symbol; the larger block is not needed, since testing with a set and with its complement splits the same blocks. Each pass removes a splitter $(S, a)$, collects the states that move into $S$ on $a$, and splits each block that has states on both sides. Line L11 keeps a pending test valid when its block splits: the test with $B$ becomes the tests with both halves. Line L12 is the smaller-half rule. At the end, line L13 makes each block a state, with $[q] \xrightarrow{a} [\delta(q, a)]$, the start state $[q_0]$, and the blocks inside $F$ as accepting states.

**Data structures.** The blocks are kept as sets with an array that gives the block of each state. In a split, line L7 has already listed the states of $B \cap X$, so the algorithm moves them to a new block in $O(|B \cap X|)$ time and leaves $B \setminus X$ under the old name. A set of the pairs in $W$ answers the test of line L11 in $O(1)$ time. The order in which line L6 removes pairs does not matter for correctness or for the bound; the implementation uses a queue.

## Example

Let $\Sigma = \{a, b\}$, $q_0 = 0$ and $F = \{3, 4, 6\}$, with $\delta(\cdot, a) = (1, 3, 4, 5, 5, 5, 6)$ and $\delta(\cdot, b) = (2, 4, 3, 5, 5, 5, 3)$ for the states $0, \ldots, 6$. It accepts the strings of length 2. Line L1 drops the unreachable state 6, line L3 gives $P = \{\{3, 4\}, \{0, 1, 2, 5\}\}$, and line L4 gives $W = [(\{3, 4\}, a), (\{3, 4\}, b)]$.

| pass | removed pair | $X$ | split | $W$ after the pass |
|---|---|---|---|---|
| 1 | $(\{3, 4\}, a)$ | $\{1, 2\}$ | $\{0, 1, 2, 5\}$ into $\{1, 2\}$ and $\{0, 5\}$ | $(\{3,4\}, b)$, $(\{1,2\}, a)$, $(\{1,2\}, b)$ |
| 2 | $(\{3, 4\}, b)$ | $\{1, 2\}$ | none | $(\{1,2\}, a)$, $(\{1,2\}, b)$ |
| 3 | $(\{1, 2\}, a)$ | $\{0\}$ | $\{0, 5\}$ into $\{0\}$ and $\{5\}$ | $(\{1,2\}, b)$, $(\{0\}, a)$, $(\{0\}, b)$ |
| 4 | $(\{1, 2\}, b)$ | $\{0\}$ | none | $(\{0\}, a)$, $(\{0\}, b)$ |
| 5 | $(\{0\}, a)$ | $\emptyset$ | none | $(\{0\}, b)$ |
| 6 | $(\{0\}, b)$ | $\emptyset$ | none | empty |

In passes 1 and 3 the two halves have equal size, and the implementation adds the half $B \cap X$. The final blocks $\{0\}$, $\{1, 2\}$, $\{3, 4\}$, $\{5\}$, numbered in breadth-first order, give the minimal DFA with $0 \to 1 \to 2 \to 3$ on both symbols, a loop at 3, start 0 and $F' = \{2\}$. The test file checks this result.

## Correctness

Three invariants give correctness; the full proof is below.

- **No wrong split.** Every block is a union of classes of the state equivalence $\sim$. A splitter $(S, a)$ has $S$ a union of classes, and equivalent states move into equivalent states, so they fall on the same side of $X$.
- **Termination.** Each split adds a block, so there are at most $n - 1$ splits, and each adds at most $\sigma$ pairs to $W$.
- **Stability at the end.** For each symbol $c$, every block can be written with unions, intersections and differences from $R$, the blocks paired with $c$ in $W$, and the sets for which the partition is already stable on $c$. Removing $(S, a)$ and splitting by $X$ makes the partition stable for $S$ on $a$. A split under line L11 puts both halves into $W$, and a split under line L12 puts one half into $W$ and leaves the other as a difference. Stability for a set survives refinement and is closed under the three operations. So when $W$ is empty, the partition is stable for every block on every symbol.

A stable partition that separates $F$ from the other states has only equivalent states in each block. With the first invariant, the blocks are exactly the classes of $\sim$, and the quotient is the minimal DFA by the [uniqueness theorem](/minimal-dfa-uniqueness/).

## Complexity

The cost of a pass is $O(1 + |X|)$ plus $O(\sigma)$ per split. The splits and the passes contribute $O(\sigma n)$ in total, so the main term is $\sum |X|$ over all passes, where $|X| = \sum_{r \in S} |\mathrm{pre}_a(r)|$.

Fix a state $r$ and a symbol $a$. After a pair $(S, a)$ with $r \in S$ is removed, the next pair with $a$ that contains $r$ can enter $W$ only by line L12, as the smaller half of a block inside $S$, so it has at most $|S|/2$ states. Hence $r$ is in at most $\lfloor \log_2 n \rfloor + 1$ removed pairs with $a$, and each time it contributes $|\mathrm{pre}_a(r)|$ to the sum. Since $\sum_r |\mathrm{pre}_a(r)| \le n$ for each $a$,

$$\sum_{\text{passes}} |X| \le (\lfloor \log_2 n \rfloor + 1)\, \sigma n.$$

- **Time.** $O(\sigma n \log n)$ in the worst case, including $O(\sigma n)$ for lines L1, L2 and L13.
- **Space.** $O(\sigma n)$ for the reverse edges, plus $O(n)$ for the blocks and $O(\sigma n)$ for the work list.
- **Tightness.** The bound is reached. Berstel and Carton (2004) gave unary DFAs, built from de Bruijn words, on which the algorithm takes $\Theta(n \log n)$ time for some orders of the work list, and Castiglione, Restivo and Sciortino (2008) gave families, built from Fibonacci words, on which every order takes $\Theta(n \log n)$ time.

## Properties

- **Deterministic and not recursive.** The output does not depend on the order of the work list, because it is the unique minimal DFA; only the running time does.
- **Not incremental.** Unlike Moore's algorithm, the partition in the middle of the run has no simple meaning such as "agree on all words of length $i$".
- **Canonical output.** Numbering the blocks in breadth-first order from the start block, with the symbols in a fixed order, gives a canonical form of the language: two DFAs accept the same language if and only if the outputs are equal.

## Variants and improvements

- **Partial DFAs.** Valmari and Lehtinen (2008) adapted the algorithm to partial transition functions, in $O(m \log n)$ time for $m$ transitions, without completing the DFA.
- **Splitters without symbols.** Some versions store blocks in $W$ and process all symbols for a removed block at once, with the same bound.
- **Coarsest stable partition of a relation.** Paige and Tarjan (1987) generalized the smaller-half idea to a relation instead of $\sigma$ functions. It computes the coarsest [bisimulation](/bisimulation/) of a labelled transition system in $O(m \log n)$ time.
- **Moore and Mealy machines.** Start with one block per output value instead of $F$ and $R \setminus F$, and put all blocks but the largest in $W$.
- **Other minimizers.** [Moore's algorithm](/moore-minimization/) is simpler and has $O(\sigma n^2)$ worst-case time. [Brzozowski's algorithm](/brzozowski-minimization/) works on NFAs too but can take exponential time. The [table-filling algorithm](/table-filling-minimization/) needs $\Theta(n^2)$ space.

## When to use it

Use Hopcroft's algorithm when the DFA is large or when inputs with long chains of distinguishable states can occur, since its worst case is $O(\sigma n \log n)$. Lexer generators and automata libraries use it for this reason. For small DFAs or for a quick implementation, Moore's algorithm is simpler and often as fast.

## Pitfalls

- **Adding only the smaller half when the block was pending.** If $(B, c)$ is in $W$ and $B$ splits, both halves must go into $W$ (line L11). Adding only the smaller half loses the test with the larger half, and the result can be too coarse.
- **Computing $B \setminus X$ by scanning $B$.** This costs $O(|B|)$ per split and breaks the $O(n \log n)$ bound on chains. Move the states of $B \cap X$ out instead.
- **Forgetting unreachable states.** Without line L1, an unreachable state can stay in a block of its own, and the output is not minimal.
- **Partial transition functions.** Treat a missing transition as a move to an explicit dead state, or use the partial version, or states with different missing transitions may be merged.
- **Duplicate pairs in $W$.** Keep a set of the pairs in $W$. A pair added twice is processed twice, which wastes time but is not wrong.

## Implementations

## History

Hopcroft (1971) gave the algorithm and the $O(n \log n)$ bound, building on the round-based refinement of Moore (1956). Aho, Hopcroft and Ullman (1974) presented it as a general partitioning algorithm, and Gries (1973) gave a structured description with a proof. Paige and Tarjan (1987) extended the method to the relational coarsest partition problem. Later papers by Knuutila (2001), Berstel and Carton (2004), and Castiglione, Restivo and Sciortino (2008) studied the role of the order of the work list and showed that the $\log n$ factor is tight.

## References
