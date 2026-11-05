---
tag: R0H62M
kind: algorithm
slug: hopcroft-karp-equivalence
name: Hopcroft-Karp equivalence algorithm
aliases:
- Hopcroft-Karp algorithm for DFA equivalence
area: automata-and-parsing/finite-automata
level: advanced
summary: Decides DFA equivalence in near-linear time using union-find to merge state pairs.
solves: [dfa-equivalence]
model: word-ram
complexity:
  vars: {n: the total number of states of the two DFAs, σ: the alphabet size}
  time: {worst: O(σ n α(n))}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
history:
  year: 1971
  people: [John E. Hopcroft, Richard M. Karp]
  note: Hopcroft and Karp gave the union-find test for the equivalence of finite automata in a Cornell technical report.
prereqs: [dfa-equivalence, disjoint-set, deterministic-finite-automaton]
see_also: [dfa-minimization, moore-minimization, hopcroft-minimization, inverse-ackermann-function, bisimulation, nfa-equivalence, product-construction, minimal-dfa-uniqueness]
sources:
  - paper: "John E. Hopcroft and Richard M. Karp, A linear algorithm for testing equivalence of finite automata, Technical Report 71-114, Department of Computer Science, Cornell University, 1971"
    locator: the whole report
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Chapter 4, Data Structures for Set Manipulation Problems (the union-find structure and its application to the equivalence of finite automata)
  - paper: doi:10.1145/2429069.2429124
    title: Filippo Bonchi and Damien Pous, Checking NFA equivalence with bisimulations up to congruence, 40th ACM Symposium on Principles of Programming Languages (POPL 2013)
    locator: pp. 457 to 468 (the algorithm of Hopcroft and Karp as a bisimulation up to equivalence)
  - paper: doi:10.1145/321879.321884
    title: Robert E. Tarjan, Efficiency of a good but not linear set union algorithm, Journal of the ACM 22(2) (1975)
    locator: pp. 215 to 225 (the inverse Ackermann bound for union-find)
---

The Hopcroft-Karp algorithm decides whether two [DFAs](/deterministic-finite-automaton/) accept the same language in $O(\sigma n \alpha(n))$ time, where $n$ is the total number of states and $\alpha$ is the [inverse Ackermann function](/inverse-ackermann-function/). It assumes that the two start states are equivalent and follows the consequences: if two states are equivalent, so are their successors on each symbol. It keeps the states that must be equivalent in a [disjoint-set](/disjoint-set/) structure. A pair of states that are already in one set needs no more work, so the algorithm merges at most $n - 1$ times and stops quickly. If a merge ever puts an accepting and a rejecting state together, the string that led to them is a counterexample.

## In plain words

Suppose the two machines are the same. Then their start states must behave alike, and so must the two states they reach on each letter, and so on. The algorithm writes down these "must be alike" claims as groups of states.

It starts with one group, the two start states. Each time it takes a claimed pair, it looks at where each letter sends the two states, and puts the two targets in one group. If the targets are already in one group, the claim is already known and nothing needs to be done. This is what keeps the work small: there are only as many merges as there are states. If some group ever holds a state that says yes and a state that says no, the claim was false, and the letters that led there show a word on which the machines disagree.

## The problem

The input is two complete DFAs $M_i = (Q_i, \Sigma, \delta_i, q_i, F_i)$ for $i = 1, 2$, over the same alphabet, with no $\varepsilon$-moves. Let $n = |Q_1| + |Q_2|$ and $\sigma = |\Sigma|$, and treat $Q_1$ and $Q_2$ as disjoint. The output is "equivalent" if $L(M_1) = L(M_2)$, and otherwise "not equivalent" with a string in exactly one of the two languages. This is [DFA equivalence](/dfa-equivalence/).

## The algorithm

Each pair that the algorithm pushes is a state $p \in Q_1$ and a state $r \in Q_2$, together with the string that led to them, stored as a pointer to the parent pair and the last symbol.

```pseudo id=main
HOPCROFT-KARP(M1, M2)
L1  make a disjoint-set structure on Q1 ∪ Q2, one set per state
L2  UNION(q1, q2); push (q1, q2) with the string ε on the stack S
L3  while S is not empty
L4      pop (p, r) with its string w
L5      if (p ∈ F1) ≠ (r ∈ F2): return "not equivalent", w
L6      for a in Σ
L7          p' ← δ1(p, a); r' ← δ2(r, a)
L8          if FIND(p') ≠ FIND(r')
L9              UNION(p', r'); push (p', r') with the string w a
L10 return "equivalent"
```

Lines L1 and L2 start with the claim that $q_1$ and $q_2$ are equivalent. Line L4 takes the next claimed pair, and line L5 checks it on the empty string. Lines L6 to L9 add the successor pairs, but only when they are not already in one set: then line L9 merges the two sets and pushes the pair. If the stack runs empty without a bad pair, line L10 reports equivalence. The string of a pair is recovered by following parent pointers, so pushing costs $O(1)$.

## Example

Over $\{a, b\}$, let $M_1$ count the $a$s modulo 2 with $F_1 = \{0\}$, and let $M_2$ count them modulo 3 with $F_2 = \{0\}$. Both ignore $b$. Write the states of $M_2$ as $0', 1', 2'$.

| step | pop | accepts? | on $a$ | on $b$ | sets after the step |
|---|---|---|---|---|---|
| start | | | | | $\{0, 0'\}$ |
| 1 | $(0, 0')$, $\varepsilon$ | yes, yes | $(1, 1')$: merge, push $a$ | $(0, 0')$: same set | $\{0, 0'\}, \{1, 1'\}$ |
| 2 | $(1, 1')$, $a$ | no, no | $(0, 2')$: merge, push $aa$ | $(1, 1')$: same set | $\{0, 0', 2'\}, \{1, 1'\}$ |
| 3 | $(0, 2')$, $aa$ | yes, no | | | |

Step 3 finds a bad pair, so the answer is "not equivalent" with the counterexample $aa$, which $M_1$ accepts and $M_2$ rejects.

Now let $M_3$ count the $a$s modulo 4 with $F_3 = \{0, 2\}$, and compare $M_1$ with $M_3$. The pushed pairs are $(0, 0')$, $(1, 1')$ on $a$, $(0, 2')$ on $aa$ and $(1, 3')$ on $aaa$. When $(1, 3')$ is popped, its successor on $a$ is $(0, 0')$, already in one set. No pair is bad, so the answer is "equivalent", with the final sets $\{0, 0', 2'\}$ and $\{1, 1', 3'\}$. The algorithm made 4 merges for 6 states. The test file checks both results.

## Correctness

Every pushed pair $(p, r)$ with string $w$ has $p = \delta_1^*(q_1, w)$ and $r = \delta_2^*(q_2, w)$, by induction on the order of pushes. So if line L5 fires, $w$ is in exactly one of the two languages.

If line L10 is reached, every pushed pair was popped and passed line L5. Let $\equiv$ be the final partition. The pushed pairs connect each set of $\equiv$, since each merge pushed one pair across the two merged sets. Two states that are joined by a pushed pair agree on acceptance, so all states of one set do. And for each pushed pair $(p, r)$ and each $a$, line L8 made $\delta_1(p, a) \equiv \delta_2(r, a)$. Following a chain of pushed pairs, this gives $x \equiv y \Rightarrow \delta(x, a) \equiv \delta(y, a)$ for all states, where $\delta$ is $\delta_1$ or $\delta_2$ as needed. By induction on $|w|$, $q_1 \equiv q_2$ gives $\delta_1^*(q_1, w) \equiv \delta_2^*(q_2, w)$, so the two states agree on acceptance, and $w \in L(M_1) \Leftrightarrow w \in L(M_2)$. The full proof is in the correctness file.

## Complexity

- **Merges.** Each UNION reduces the number of sets by one, and there are $n$ sets at the start, so there are at most $n - 1$ merges, including the one of line L2. Each push follows a merge, so at most $n - 1$ pairs are pushed and popped.
- **Finds.** Each pop runs line L8 for $\sigma$ symbols, with two FIND operations each. So there are at most $2 \sigma (n - 1)$ finds and $n - 1$ unions.
- **Total.** With union by size and path compression or path halving, $m$ operations on $n$ elements take $O(m \, \alpha(m, n))$ time (Tarjan, 1975), so the time is $O(\sigma n \alpha(n))$. The extra space is $O(n)$ for the disjoint sets and the stack.
- **Counterexample length.** A pushed pair's string is one symbol longer than its parent's, and there are at most $n - 1$ pushed pairs, so the counterexample has length at most $n - 2$. This matches the bound $n_1 + n_2 - 2$ of the [DFA equivalence](/dfa-equivalence/) page, which is tight.

## Properties

- **Almost linear.** It reads each transition of a reached pair at most once, and it does not build the product automaton, which can have $|Q_1| \cdot |Q_2|$ states.
- **Counterexamples.** It returns a counterexample of length at most $n - 2$, but not always a shortest one, because the stack order and the merges can hide a shorter path.
- **Equivalence as a by-product.** When the answer is "equivalent", the final partition relates each reachable state of $M_1$ to the states of $M_2$ that are equivalent to it, restricted to the pairs that the search reached. It is a *bisimulation up to equivalence* in the terms of Bonchi and Pous (2013).
- **Not recursive.** The search uses an explicit stack, and the union-find structure needs no recursion with path halving.

## Variants and improvements

- **Queue instead of stack.** Any order of processing the pairs is correct. A queue makes the counterexamples shorter in practice, but still not always shortest.
- **The naive product search.** Without union-find, a [breadth-first search](/breadth-first-search/) of the [product](/product-construction/) visits up to $|Q_1| \cdot |Q_2|$ pairs and takes $O(\sigma n_1 n_2)$ time, but returns a shortest counterexample.
- **NFAs.** Running the algorithm on the subset automata of two NFAs, built on the fly, decides [NFA equivalence](/nfa-equivalence/). Bonchi and Pous (2013) replaced the equivalence closure by a congruence closure with respect to union of sets, which can skip exponentially many subsets.
- **Unification.** The algorithm is a form of unification of rational trees: it merges two terms and propagates the merge to their arguments, the same technique as in the near-linear unification algorithms for infinite terms.

## When to use it

Use it to check two DFAs for equality when only a yes-or-no answer and some counterexample are needed: in tests of regular-expression compilers, in learning loops such as [L*](/lstar-algorithm/) where equivalence queries are answered against a known automaton, and in tools that grade automata. Use the product search when the shortest counterexample matters.

## Pitfalls

- **Partial DFAs.** A missing transition must go to a dead state. If one DFA lacks the transition and the other has it, the pair is not a pair of states at all. Complete both DFAs first.
- **Checking acceptance too late.** Line L5 must check every pushed pair, including the first one. An implementation that only checks pairs when they are merged misses the case where $q_1$ accepts and $q_2$ does not.
- **Merging in the same set.** Two states of $M_1$ can end in one set, and that is correct: it says that both are equivalent to a state of $M_2$. Do not reject a merge only because the states come from the same machine.
- **Different alphabets.** The two DFAs must use the same alphabet. A symbol that one of them lacks must be added to it, with transitions to a dead state.

## Implementations

## History

Hopcroft and Karp described the algorithm in a 1971 technical report, as an application of the set-union structure; the book of Aho, Hopcroft and Ullman (1974) presented it with the union-find analysis. Tarjan's analysis (1975) gave the inverse Ackermann bound. Bonchi and Pous (2013) recast it as a coinductive proof method, a bisimulation up to equivalence, and extended it to NFAs with up-to-congruence techniques.

## References
