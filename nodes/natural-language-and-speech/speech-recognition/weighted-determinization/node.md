---
tag: 40YQAC
kind: algorithm
slug: weighted-determinization
name: Weighted determinization
aliases:
- WFST determinization
- Mohri determinization
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Turn a weighted automaton with the twins property into an equivalent one with at most one transition per label from each state, by subsets with residual weights.
model: word-ram
complexity:
  vars: {N: the number of states of the result, M: the number of arcs of the result, s: the number of states of the input, e: the number of arcs of the input}
  time: {worst: "O(N e + M s log s)"}
  space: {extra: "O(N s + M)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1997
  people: [Mehryar Mohri]
  note: Mohri gave the determinization of weighted automata and transducers over the tropical semiring in 1997, with the twins property as the condition for it to stop, and used it to shrink the networks of speech recognizers.
prereqs: [weighted-automaton, nfa-determinization]
see_also: [determinization-blowup-lower-bound, weighted-transducer-composition, weight-pushing, hclg-decoding-graph, dfa-minimization, finite-state-transducer, epsilon-closure]
sources:
  - url: https://aclanthology.org/J97-2003/
    title: Mehryar Mohri, Finite-state transducers in language and speech processing, Computational Linguistics 23(2), 1997, pages 269 to 311
    locator: the sections on the determinization of weighted automata and transducers over the tropical semiring and the twins property
  - book: isbn:9783642014918
    title: Mehryar Mohri, Weighted automata algorithms, in Manfred Droste, Werner Kuich and Heiko Vogler (editors), Handbook of Weighted Automata, Springer, 2009
    locator: "Section 6.2 (determinization: the algorithm for weakly divisible semirings, siblings and twins, Theorems 5 and 6, and the example that cannot be determinized)"
  - paper: doi:10.1006/csla.2001.0184
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted finite-state transducers in speech recognition, Computer Speech and Language 16(1), 2002, pages 69 to 88
    locator: the section on determinization and its effect on the size and speed of the recognition network
---

Weighted determinization turns a weighted automaton into an equivalent one in which each state has at most one outgoing arc per label. It is the [subset construction](/nfa-determinization/) with a weight attached to each state of a subset. That weight, the residual, is the part of the path weight that the new machine has not yet emitted. The result gives every string the same weight as the input, and a decoder that walks it never has two arcs to follow for one label. Unlike the unweighted subset construction, it does not always stop: Mohri 1997 shows that it stops when the input has the twins property over the tropical semiring, and some weighted automata have no deterministic equivalent at all.

## In plain words

A machine reads a string and can follow several paths at once, each with its own cost. You want a machine that follows only one path. Run all the old paths together. A new state is the set of old states you could be in, and for each of them the extra cost it has collected beyond the cheapest one.

On each symbol, the new arc carries the smallest cost among the old paths. Each old state keeps only its extra cost. If the extra costs keep growing forever, you get new sets without end, and the method never stops. A simple condition on the cycles of the machine rules this out.

## The problem

A weighted acceptor over a semiring $(K, \oplus, \otimes, \bar 0, \bar 1)$ has a set of states $Q$, a start state $i$ with an initial weight $\lambda$, final weights $\rho(q)$ and arcs $(q, a, w, n)$ ([weighted automaton](/weighted-automaton/)). It gives each string $u$ the weight $A(u)$, the $\oplus$-sum over the paths that read $u$ of $\lambda$, the arc weights and the final weight, multiplied with $\otimes$. The acceptor is deterministic if no state has two arcs with the same label. The task: given an $\varepsilon$-free $A$, build a deterministic $D$ with $D(u) = A(u)$ for every string $u$.

The weights here are costs $c = -\log p$, as in Mohri, Pereira and Riley 2002. A probability $p$ becomes the cost $-\log p$, and a probability of 0 becomes $+\infty$. The tropical semiring $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$ keeps the best path, and the log semiring with $a \oplus b = -\log(e^{-a} + e^{-b})$ adds probabilities. In both, $\otimes$ is $+$, and dividing by a finite weight $w$ is subtracting $w$. A transducer is handled by reading each pair (input, output) as one label, or with residual output strings as in Mohri 1997.

## The algorithm

A state of $D$ is a weighted subset $\{(q_1, r_1), \ldots, (q_k, r_k)\}$. The pair $(q, r)$ means: the input can be in state $q$, and its best (or total) weight up to here is the weight already emitted by $D$ times $r$.

```pseudo id=main
WEIGHTED-DETERMINIZE(A)
L1  λ' ← λ;  i' ← {(i, 1̄)};  Q' ← {i'};  S ← [i']
L2  while S is not empty do
L3      p' ← DEQUEUE(S)
L4      if p' holds a final state then ρ'(p') ← ⊕ of r ⊗ ρ(q) over the pairs (q, r) ∈ p' with q final
L5      for each label a on an arc that leaves a state of p' do
L6          w' ← ⊕ of r ⊗ w over (q, r) ∈ p' and arcs (q, a, w, n)
L7          v(n) ← ⊕ of r ⊗ w over (q, r) ∈ p' and arcs (q, a, w, n), for each target n
L8          n' ← {(n, w'^{-1} ⊗ v(n))}          ▷ on costs, the residual is v(n) - w'
L9          add the arc (p', a, w', n')
L10         if n' ∉ Q' then add n' to Q' and enqueue n' on S
```

Line L6 is the weight that $D$ emits on the arc: the minimum in the tropical semiring, the total in the log semiring. Line L8 keeps, for each target, only what remains. In the tropical semiring, at least one residual of every new subset is 0.

## Example

The acceptor $A$ has the arcs $0 \xrightarrow{a/1} 1$, $0 \xrightarrow{a/2} 2$, $1 \xrightarrow{b/3} 3$, $2 \xrightarrow{b/1} 3$ and $1 \xrightarrow{c/5} 3$, the final state 3 with weight 0, and the tropical semiring. State 0 has two arcs labelled $a$, so $A$ is not deterministic.

| subset | label | $w'$ (L6) | target subset (L8) |
|---|---|---|---|
| $\{(0, 0)\}$ | $a$ | $\min(0 + 1, 0 + 2) = 1$ | $\{(1, 0), (2, 1)\}$ |
| $\{(1, 0), (2, 1)\}$ | $b$ | $\min(0 + 3, 1 + 1) = 2$ | $\{(3, 0)\}$ |
| $\{(1, 0), (2, 1)\}$ | $c$ | $0 + 5 = 5$ | $\{(3, 0)\}$ |

The result has 3 states and 3 arcs, and it is deterministic. The string $ab$ costs $1 + 2 = 3$, which is $\min(1 + 3, 2 + 1)$ in $A$. The string $ac$ costs $1 + 5 = 6$, as in $A$. The residual 1 of state 2 in the middle subset records that the path through state 2 is 1 worse than the best path so far; on $b$ it catches up, since $1 + 1 < 0 + 3$.

Now an input that has no deterministic equivalent. Take the arcs $0 \xrightarrow{a/0} 1$, $0 \xrightarrow{a/0} 2$, the loops $1 \xrightarrow{a/3} 1$ and $2 \xrightarrow{a/4} 2$, then $1 \xrightarrow{b/0} 3$ and $2 \xrightarrow{c/0} 3$, with state 3 final. After $a^k$ the subset is $\{(1, 0), (2, k - 1)\}$. The residual grows by one on each $a$, so every $k$ gives a new state and the loop never stops. A deterministic machine would have to know, after $a^k$, whether to charge 3 or 4 per $a$, and it cannot know that until it sees $b$ or $c$. Mohri 2009, Figure 11(c), shows an acceptor of the same kind, with cycle weights 3 and 4.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Let $\delta(u, q)$ be the weight of the paths from $i$ to $q$ that read $u$. The invariant, by induction on $|u|$, is that the subset reached by $u$ holds exactly the states $q$ with $\delta(u, q) \ne \bar 0$, and that $\lambda \otimes \delta(u, q) = W(u) \otimes r_q$, where $W(u)$ is the weight $D$ has emitted on $u$. Line L4 then gives $D(u) = A(u)$.

Termination is a separate question. Two states $q$ and $q'$ are siblings if one string $x$ reaches both from $i$ and one string $y$ labels a cycle at $q$ and a cycle at $q'$. They are twins if, for all such $x$ and $y$, $\delta(xy, q) - \delta(x, q) = \delta(xy, q') - \delta(x, q')$: the cycles cost the same at both. The input has the twins property if all its siblings are twins. Over the tropical semiring:

- **Theorem (Mohri 1997; Mohri 2009, Theorem 5).** If $A$ has the twins property, $A$ is determinizable, and the algorithm stops.
- **Theorem (Mohri 2009, Theorem 6).** If $A$ is trim and unambiguous, $A$ is determinizable if and only if it has the twins property.
- **Acyclic inputs.** Every acyclic acceptor over a semiring with no zero sums, such as the tropical and the log semiring, is determinizable, because it reads only finitely many strings.

In the second example, states 1 and 2 are siblings ($x = a$, $y = a$) with cycle costs 3 and 4, so they are not twins.

## Complexity

The size of the result can be exponential. The unweighted automaton for $(a \mid b)^* a (a \mid b)^{n-1}$ has $n + 1$ states, and every deterministic equivalent has at least $2^n$ states ([determinization blow-up lower bound](/determinization-blowup-lower-bound/)); weights do not help. So the cost is stated in the size of the output.

In the word-RAM model, with $N$ states and $M$ arcs in the result and $s$ states and $e$ arcs in the input, a state of $D$ holds at most $s$ pairs, and lines L5 to L7 look at most $e$ arcs of the input for it. Building and hashing the target subsets costs $O(s \log s)$ per arc of $D$, for the sort that gives each subset a canonical order. The total is $O(N e + M s \log s)$ time, with hashing in expected time. The space is $O(N s + M)$ for the subsets and the arcs.

The twins property can be tested in $O(s^2 + e^2)$ time over the tropical semiring (Allauzen and Mohri 2003, as cited in Mohri 2009, Section 6.2).

## Properties

- **Exact when it stops.** $D(u) = A(u)$ for every string, in the tropical and in the log semiring.
- **Not always possible.** Some weighted automata have no deterministic equivalent, unlike unweighted ones.
- **Output-sensitive.** The cost depends on the size of the result, which can be exponential in the size of the input.
- **Weights move forward.** $D$ emits on each arc the best (or total) weight so far, so weights tend to come earlier than in $A$. [Weight pushing](/weight-pushing/) moves them as far forward as possible.
- **A canonical form with minimization.** Determinization, then weight pushing, then unweighted minimization with (label, weight) pairs as labels, gives the minimal deterministic machine (Mohri 2009, Theorem 8; see [DFA minimization](/dfa-minimization/)).

## Variants and improvements

- **Transducers.** Mohri 1997 also determinizes sequential transducers: a subset then holds residual output strings as well as residual weights. A transducer with ambiguous outputs, such as a lexicon with homophones, needs extra symbols first (see [HCLG decoding graph](/hclg-decoding-graph/)).
- **The log semiring.** The same loop works in any weakly divisible semiring with a suitable division (Mohri 2009). The code accepts the log semiring on costs, and the tests use it on acyclic inputs.
- **On-the-fly determinization.** Build a state of $D$ only when a search reaches it, as for lazy composition.
- **Disambiguation.** Some machines that cannot be determinized can still be made unambiguous, so that each string has at most one path.

## When to use it

Use it on the search graph of a speech recognizer, after composition, so that each state has at most one arc per label. This removes redundant paths, makes the graph smaller in practice, and makes the search faster, because the decoder no longer evaluates the same HMM state on several parallel arcs. Use it also to compute the best weight of each string of a lattice, by determinizing the lattice in the tropical semiring. Do not use it on an input that may lack the twins property without a size limit.

## Pitfalls

- **No termination.** An input without the twins property makes the loop run until memory runs out. Use a state limit, as the code does, or make the input determinizable first.
- **Homophones in a lexicon.** Two words with the same pronunciation make the lexicon transducer not determinizable as a transducer. Add disambiguation symbols.
- **Floating-point residuals.** Two subsets that should be equal can have residuals that differ in the last bits. Compare residuals after rounding to a small quantum $\delta$, as OpenFst does with its delta parameter. Too large a $\delta$ merges subsets that should differ and changes the weights a little.
- **Epsilons.** The algorithm needs an $\varepsilon$-free input. Remove the $\varepsilon$ arcs first, or treat $\varepsilon$ as an ordinary label.
- **Blow-up.** Even when it stops, the result can be exponential. In speech graphs it is usually smaller than the input, but that is a measurement on those graphs, not a guarantee.

## Implementations

The Python code determinizes $\varepsilon$-free weighted acceptors in the tropical and the log semiring on costs, with a queue of weighted subsets and a state limit. The tests compare the weight of every string of length at most 4 before and after, on random acyclic acceptors and on random cyclic acceptors with the twins property, check that the result is deterministic, check that the example without the twins property hits the state limit with the residuals $0, 1, 2, \ldots$, and check the $2^n$ states for $(a \mid b)^* a (a \mid b)^{n-1}$.

## History

The subset construction for unweighted automata is from Rabin and Scott 1959. Mohri 1997 extended it to weighted automata and to transducers over the tropical semiring, introduced the twins property, and proved that it makes the algorithm stop. Mohri, Pereira and Riley used it, with composition and weight pushing, to build the compact networks of large vocabulary speech recognizers, and Mohri 2009 gives the algorithm for weakly divisible semirings.

## References
