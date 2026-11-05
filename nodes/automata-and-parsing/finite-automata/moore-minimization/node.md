---
tag: 7CHN37
kind: algorithm
slug: moore-minimization
name: Moore's DFA minimization algorithm
aliases:
- Moore partition refinement
area: automata-and-parsing/finite-automata
level: core
summary: Minimizes a DFA by repeatedly splitting state classes by successor class until stable, in O(n^2) time for a fixed alphabet.
solves: [dfa-minimization]
model: word-ram
complexity:
  vars: {n: the number of states, σ: the alphabet size}
  time: {worst: O(σ n^2), best: O(σ n)}
  space: {extra: O(σ n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1956
  people: [Edward F. Moore]
  note: Moore described the refinement of states by experiments of growing length in Gedanken-experiments on sequential machines.
prereqs: [dfa-minimization, myhill-nerode-relation, partition-refinement]
see_also: [hopcroft-minimization, brzozowski-minimization, table-filling-minimization, minimal-dfa-uniqueness, dfa-equivalence, moore-machine]
sources:
  - paper: "Edward F. Moore, Gedanken-experiments on sequential machines, in C. E. Shannon and J. McCarthy (eds.), Automata Studies, Annals of Mathematics Studies 34, Princeton University Press, 1956"
    locator: pp. 129 to 153 (equivalent states, distinguishing experiments of bounded length, and the reduced machine)
  - book: isbn:9780201029888
    title: John E. Hopcroft and Jeffrey D. Ullman, Introduction to Automata Theory, Languages, and Computation, first edition, 1979
    locator: Section 3.4, The Myhill-Nerode Theorem and Minimization of Finite Automata
  - book: isbn:9780387949079
    title: Dexter C. Kozen, Automata and Computability, Springer, 1997
    locator: Lecture 14, A Minimization Algorithm (merging equivalent states, and the marking of distinguishable pairs)
  - paper: "Frédérique Bassino, Julien David and Cyril Nicaud, On the average complexity of Moore's state minimization algorithm, 26th International Symposium on Theoretical Aspects of Computer Science (STACS 2009), LIPIcs 3"
    locator: pp. 123 to 134 (the average number of rounds and the O(n log n) average time)
---

Moore's algorithm [minimizes a DFA](/dfa-minimization/) by refining a partition of its states in rounds. It starts with the accepting and the rejecting states. In each round it gives each state a signature, made of its own class and the classes of its successors, and splits the classes by signature. When a round splits nothing, two states are in one class exactly when they are equivalent, and the classes are the states of the minimal DFA. Each round takes $O(\sigma n)$ time and there are at most $n - 1$ rounds, so the time is $O(\sigma n^2)$ in the worst case, but few rounds are needed on typical inputs.

## In plain words

Think of each state as a person who answers "yes" or "no" at the end of a word. At first we know only who says yes now, so the states fall into two groups. Then each state looks at where each letter sends it and writes down the group of each target, next to its own group. States with the same notes stay together, and states with different notes split.

This repeats. After one round, two states in one group agree on every word of length at most one. After two rounds, on every word of length at most two, and so on. When a round splits no group, no longer word can split one either, and each group becomes one state of the smallest machine.

## The problem

The input is a complete DFA $M = (Q, \Sigma, \delta, q_0, F)$ with $\delta : Q \times \Sigma \to Q$, no $\varepsilon$-moves, $n = |Q|$ and $\sigma = |\Sigma|$. The output is the minimal complete DFA for $L(M)$, and the map from each reachable state to its state in the output. This is [DFA minimization](/dfa-minimization/).

## The algorithm

The classes are numbers. A signature is a tuple of $\sigma + 1$ class numbers, and a dictionary gives each distinct signature a new number, in the order of first appearance.

```pseudo id=main
MOORE-MINIMIZE(Q, Σ, δ, q0, F)
L1  R ← the states reachable from q0                   ▷ graph search
L2  for q in R: cls[q] ← 1 if q ∈ F else 0
L3  k ← the number of distinct values cls[q]
L4  repeat
L5      for q in R: sig[q] ← (cls[q], cls[δ(q, a1)], ..., cls[δ(q, aσ)])
L6      number the distinct signatures 0, 1, 2, ...; new[q] ← the number of sig[q]
L7      k' ← the number of distinct signatures
L8      stable ← (k' = k)
L9      cls ← new, k ← k'
L10 until stable
L11 return the DFA with states 0, ..., k − 1, start cls[q0],
        δ'(cls[q], a) = cls[δ(q, a)], F' = { cls[q] : q ∈ F ∩ R }
```

Line L1 drops the unreachable states, which could otherwise survive as extra classes. Lines L2 and L3 set up round 0, with one class or two. In each round, line L5 builds the signatures from the classes of the previous round, and line L6 renumbers the classes. A signature starts with the old class, so the new partition refines the old one, and line L8 detects a round with no split by comparing the number of classes. Line L11 reads the minimal DFA off the final classes: the transition of a class is well defined because the partition is stable.

## Example

Let $\Sigma = \{a, b\}$, $q_0 = 0$ and $F = \{3, 4, 6\}$, with $\delta(\cdot, a) = (1, 3, 4, 5, 5, 5, 6)$ and $\delta(\cdot, b) = (2, 4, 3, 5, 5, 5, 3)$ for the states $0, \ldots, 6$. It accepts the strings of length 2. Line L1 finds $R = \{0, 1, 2, 3, 4, 5\}$ and drops state 6. Signatures are written as (own class, class on $a$, class on $b$).

| state | 0 | 1 | 2 | 3 | 4 | 5 | $k$ |
|---|---|---|---|---|---|---|---|
| round 0 class | 0 | 0 | 0 | 1 | 1 | 0 | 2 |
| round 1 signature | (0,0,0) | (0,1,1) | (0,1,1) | (1,0,0) | (1,0,0) | (0,0,0) | |
| round 1 class | 0 | 1 | 1 | 2 | 2 | 0 | 3 |
| round 2 signature | (0,1,1) | (1,2,2) | (1,2,2) | (2,0,0) | (2,0,0) | (0,0,0) | |
| round 2 class | 0 | 1 | 1 | 2 | 2 | 3 | 4 |
| round 3 signature | (0,1,1) | (1,2,2) | (1,2,2) | (2,3,3) | (2,3,3) | (3,3,3) | |
| round 3 class | 0 | 1 | 1 | 2 | 2 | 3 | 4 |

Round 1 separates the states that reach $F$ in one step. Round 2 separates 0 from 5, because 0 moves to class 1 and 5 to class 0. Round 3 has 4 distinct signatures, the same number as before, so it stops. The output has the states 0 to 3 with $\delta'(0, \cdot) = 1$, $\delta'(1, \cdot) = 2$, $\delta'(2, \cdot) = 3$, $\delta'(3, \cdot) = 3$ on both symbols, start 0 and $F' = \{2\}$. The test file checks this trace.

## Correctness

Call states $p, q$ *$i$-equivalent*, $p \sim_i q$, if $\delta^*(p, z) \in F \Leftrightarrow \delta^*(q, z) \in F$ for every $z$ with $|z| \le i$. Then $p \sim_{i+1} q$ if and only if $p \sim_i q$ and $\delta(p, a) \sim_i \delta(q, a)$ for each $a$, since a word of length at most $i + 1$ is empty or is $a z$ with $|z| \le i$. By induction on the round number $i$, the classes after round $i$ are exactly the classes of $\sim_i$ on $R$: round 0 is $\sim_0$, and line L5 compares the old class and the old classes of the successors, which is the right side of the recursion. If round $i + 1$ makes no new class, then $\sim_{i+1} = \sim_i$, the recursion gives $\sim_{i+2} = \sim_{i+1}$, and so on, so $\sim_i$ is the equivalence $\sim$ of [DFA minimization](/dfa-minimization/). The output is the quotient $M / {\sim}$ on the reachable states, which is the minimal DFA by the [uniqueness theorem](/minimal-dfa-uniqueness/). The full proof is below.

## Complexity

- **Rounds.** Each round that does not stop adds at least one class. Round 0 has at least one class and there are never more than $|R| \le n$ classes, so at most $n - 1$ rounds split, and the algorithm makes at most $n$ rounds in all. With round 0 having two classes, the bound is $n - 1$ rounds, $n - 2$ of which split, so all classes agree on words of length $n - 2$, as in the [Myhill-Nerode relation](/myhill-nerode-relation/) page.
- **One round.** Building the $n$ signatures reads $\sigma n$ classes. Numbering them with a hash table takes $O(\sigma n)$ expected time. A radix sort of the signatures, with $\sigma + 1$ digits in the range $0, \ldots, n - 1$, numbers them in $O(\sigma n)$ worst-case time.
- **Total.** $O(\sigma n^2)$ time in the worst case and $O(\sigma n)$ extra space. The bound is reached: on the chain $0 \to 1 \to \cdots \to n - 1$ with a loop at $n - 1$ and $F = \{n - 1\}$, each round splits off one state, so the algorithm makes $n - 1$ rounds, each of cost $\Theta(\sigma n)$. A script counted these rounds for $n = 2, \ldots, 8$.
- **Best case.** When round 1 already splits nothing, the time is $O(\sigma n)$.
- **Average.** Over uniformly random DFAs with a fixed alphabet, the expected number of rounds is $O(\log n)$, so the average time is $O(n \log n)$ (Bassino, David and Nicaud, 2009).

## Properties

- **Deterministic and not recursive.** Each round is a pass over the states.
- **Round $i$ is meaningful.** The partition after round $i$ is the $i$-equivalence. So the algorithm also answers "which states agree on all words of length at most $i$" for each $i$.
- **Easy to parallelize.** The signatures of one round are independent of each other, so a round is a parallel map and a parallel sort.
- **Canonical numbering is free.** With the "first appearance" numbering of line L6 in the order of a breadth-first search from $q_0$, the output is a canonical form of the language.

## Variants and improvements

- **[Hopcroft's algorithm](/hopcroft-minimization/).** It refines with one splitter at a time and processes only the smaller half of each split, for $O(\sigma n \log n)$ time in the worst case.
- **Table filling.** It marks distinguishable pairs of states. It also takes $O(\sigma n^2)$ time with backward propagation, but it needs $\Theta(n^2)$ space.
- **Moore and Mealy machines.** Start with one class per output value instead of $F$ and $Q \setminus F$. This is the setting of Moore's paper. See [Moore machine](/moore-machine/).
- **Bisimulation.** The same naive refinement computes the coarsest [bisimulation](/bisimulation/) of a labelled transition system, with sets of successor classes in place of tuples.

## When to use it

Use Moore's algorithm when simplicity matters, when DFAs are small or random, or when the rounds should run in parallel. It is often as fast as Hopcroft's algorithm in practice because few rounds are needed. Use Hopcroft's algorithm when worst-case inputs, such as long chains, are possible.

## Pitfalls

- **Forgetting the unreachable states.** Without line L1, an unreachable state can form a class of its own, and the output is not minimal. In the example, state 6 would make a fifth class.
- **Dropping the old class from the signature.** If the signature has only the successors' classes, then an accepting and a rejecting state with the same successors get the same class. In the example, states 3 and 5 both go to 5 on each symbol.
- **Stopping on "no state changed its number".** The numbers change from round to round even when the partition does not, so compare the number of classes, as line L8 does, or compare the partitions themselves.
- **Partial DFAs.** A missing transition must count as a class of its own, the dead class. Complete the DFA first, or treat the missing value as a fixed extra class.

## Implementations

## History

Moore (1956) defined equivalent states of a sequential machine by experiments, showed that experiments of bounded length suffice to tell inequivalent states apart, and computed the reduced machine by refining the states for experiments of growing length. Huffman (1954) did similar work for switching circuits. The algorithm appears in the textbooks of Hopcroft and Ullman as the basic minimization method, and Hopcroft (1971) improved it to $O(n \log n)$. Bassino, David and Nicaud (2009) explained its good practical speed by an average-case analysis.

## References
