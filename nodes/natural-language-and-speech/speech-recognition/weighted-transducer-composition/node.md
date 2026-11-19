---
tag: BWQJKE
kind: algorithm
slug: weighted-transducer-composition
name: Weighted transducer composition
aliases:
- WFST composition
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Build the transducer of the relation of T1 followed by T2, pairing states and matching labels, with weights combined in the semiring and an epsilon filter.
model: word-ram
complexity:
  vars: {p: the number of states of T1, q: the number of states of T2, m: the number of arcs of T1, n: the number of arcs of T2}
  time: {worst: "O(p q + m n)"}
  space: {extra: "O(p q + m n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1996
  people: [Mehryar Mohri, Fernando Pereira, Michael Riley]
  note: Mohri, Pereira and Riley gave weighted composition with the epsilon filter in their 1996 work on weighted automata for text and speech, and used it to build speech recognizers as cascades of transducers.
prereqs: [weighted-automaton, finite-state-transducer]
see_also: [product-construction, epsilon-nfa, weighted-determinization, weight-pushing, hclg-decoding-graph, provenance-semirings, depth-first-search, pronunciation-lexicon]
sources:
  - paper: doi:10.1006/csla.2001.0184
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted finite-state transducers in speech recognition, Computer Speech and Language 16(1), 2002, pages 69 to 88
    locator: the section on composition and its use to combine the models of a recognizer
  - book: isbn:9783642014918
    title: Mehryar Mohri, Weighted automata algorithms, in Manfred Droste, Werner Kuich and Heiko Vogler (editors), Handbook of Weighted Automata, Springer, 2009
    locator: "Section 5.1 (composition: the epsilon-free algorithm, its O(|T1| |T2|) cost, the redundant epsilon paths and the filter transducer)"
  - url: https://arxiv.org/abs/cs/0503077
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted automata in text and speech processing, ECAI 96 Workshop on Extended Finite State Models of Language, Budapest, 1996
    locator: the composition of weighted transducers and the epsilon filter
  - url: https://research.google/pubs/a-generalized-composition-algorithm-for-weighted-finite-state-transducers/
    title: Cyril Allauzen, Michael Riley and Johan Schalkwyk, A generalized composition algorithm for weighted finite-state transducers, Proceedings of Interspeech 2009, pages 1203 to 1206
    locator: the composition filter as a parameter of the algorithm, and the filters that remove useless epsilon paths
---

Weighted transducer composition takes a weighted transducer $T_1$ that maps strings $x$ to strings $y$ and a weighted transducer $T_2$ that maps $y$ to $z$, and builds one transducer $T_1 \circ T_2$ that maps $x$ to $z$ directly. Its states are pairs of states of the two machines, an arc exists where an output label of $T_1$ meets the same input label of $T_2$, and the weights combine with the $\otimes$ of the semiring. Speech recognizers use it to join the HMM, the context dependency, the [pronunciation lexicon](/pronunciation-lexicon/) and the language model into one search graph (see [HCLG decoding graph](/hclg-decoding-graph/)). Empty labels need care: without an epsilon filter, the same pair of paths can appear more than once in the result, and in a non-idempotent semiring the weights come out wrong.

## In plain words

The first machine rewrites a string into another string, and gives the rewrite a cost. The second machine rewrites that result again, with its own cost. Composition builds one machine that does both rewrites in one step. A state of the new machine remembers where each of the two machines is. The new machine moves when the first machine writes a symbol and the second machine reads that same symbol. The cost of the move is the sum of the two costs.

Some moves write or read nothing. Then one machine moves and the other waits, or both move. There are several orders for such moves, and they all lead to the same place. A small extra counter allows only one order, so that each way through the two machines is counted once.

## The problem

A weighted transducer over a semiring $(K, \oplus, \otimes, \bar 0, \bar 1)$ has a finite set of states, a start state $i$, final weights $\rho(q)$, and arcs $(q, a, b, w, n)$ from $q$ to $n$ with input label $a$, output label $b$ and weight $w$ ([weighted automaton](/weighted-automaton/), [finite-state transducer](/finite-state-transducer/)). A label can be $\varepsilon$, the empty string. The weight of a successful path is the $\otimes$-product of its arc weights and the final weight, and $T(x, y)$ is the $\oplus$-sum of the weights of all successful paths that read $x$ and write $y$. The composition is

$$(T_1 \circ T_2)(x, z) = \bigoplus_{y} T_1(x, y) \otimes T_2(y, z).$$

The task is to build a transducer $T$ with $T(x, z) = (T_1 \circ T_2)(x, z)$ for all $x$ and $z$. The semiring must be commutative.

The weights here are costs $c = -\log p$, as in Mohri, Pereira and Riley 2002. A probability $p$ becomes the cost $-\log p$, and a probability of 0 becomes $+\infty$. Two semirings are used on costs: the tropical semiring $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$, which keeps the best path, and the log semiring with $a \oplus b = -\log(e^{-a} + e^{-b})$, which adds probabilities. The page writes $s_1, s_2$ for the numbers of states and $e_1, e_2$ for the numbers of arcs of $T_1$ and $T_2$.

## The algorithm

The states of $T$ are triples $(q_1, q_2, f)$. The filter state $f$ records the last kind of move: 0 after a matched move or a move where both machines take an $\varepsilon$ arc, 1 after a move of $T_1$ alone, 2 after a move of $T_2$ alone. The algorithm builds only the triples that are reachable from the start, with a stack.

```pseudo id=main
COMPOSE(T1, T2)                     ▷ output labels of T1 meet input labels of T2
L1  i ← (i1, i2, 0);  Q ← {i};  S ← [i]
L2  while S is not empty do
L3      (q1, q2, f) ← POP(S)
L4      if q1 ∈ F1 and q2 ∈ F2 then ρ(q1, q2, f) ← ρ1(q1) ⊗ ρ2(q2)
L5      for each arc (q1, a, b, w1, n1) with b ≠ ε and each arc (q2, b, c, w2, n2) do ADD(a, c, w1 ⊗ w2, (n1, n2, 0))
L6      if f = 0 then for each arc (q1, a, ε, w1, n1) and each arc (q2, ε, c, w2, n2) do ADD(a, c, w1 ⊗ w2, (n1, n2, 0))
L7      if f ≠ 2 then for each arc (q1, a, ε, w1, n1) do ADD(a, ε, w1, (n1, q2, 1))      ▷ T1 moves, T2 waits
L8      if f ≠ 1 then for each arc (q2, ε, c, w2, n2) do ADD(ε, c, w2, (q1, n2, 2))      ▷ T2 moves, T1 waits
L9  return the transducer with states Q, start i, the arcs and ρ
ADD(a, c, w, n)                     ▷ an arc out of the current triple (q1, q2, f)
L10 if n ∉ Q then add n to Q and push n on S
L11 add the arc ((q1, q2, f), a, c, w, n)
```

Line L5 is the plain product construction ([product construction](/product-construction/) for automata). Lines L6 to L8 handle the $\varepsilon$ labels. In the notation of Mohri 2009, Section 5.1, they are the composition $\tilde T_1 \circ F \circ \tilde T_2$ with a three-state filter transducer $F$: from filter state 1 only $T_1$ may move alone, and from filter state 2 only $T_2$.

## Example

Take $T_1$ with the arcs $0 \xrightarrow{a:x/1} 1$ and $0 \xrightarrow{a:y/2} 1$, and $T_2$ with the arcs $0 \xrightarrow{x:u/0.5} 1$ and $0 \xrightarrow{y:u/0.25} 1$. State 1 is final with weight 0 in both. There are no $\varepsilon$ labels, so only line L5 runs. From $(0, 0, 0)$ it makes two arcs to $(1, 1, 0)$: $a{:}u$ with cost $1 + 0.5 = 1.5$ through $x$, and $a{:}u$ with cost $2 + 0.25 = 2.25$ through $y$. The result has 2 states and 2 arcs, within the bounds $s_1 s_2 = 4$ and $e_1 e_2 = 4$.

The weight of the pair $(a, u)$ depends on the semiring. In the tropical semiring it is $\min(1.5, 2.25) = 1.5$, the cost of the best path. In the log semiring it is $-\log(e^{-1.5} + e^{-2.25}) = -\log(0.223130 + 0.105399) = 1.113129$, the cost of the total probability $0.328529$.

Now the filter. Let $T_1$ be the single arc $0 \xrightarrow{a:\varepsilon/0} 1$ and $T_2$ the single arc $0 \xrightarrow{\varepsilon:c/0} 1$. The only result is $T_1 \circ T_2(a, c) = 0 + 0 = 0$, from one pair of paths. The trace from $(0, 0, 0)$:

| line | move | new triple |
|---|---|---|
| L6 | both take their $\varepsilon$ arc | $(1, 1, 0)$, final |
| L7 | $T_1$ alone | $(1, 0, 1)$ |
| L8 | $T_2$ alone | $(0, 1, 2)$ |

From $(1, 0, 1)$, $T_2$ may not move alone, because $f = 1$; from $(0, 1, 2)$, $T_1$ may not move alone, because $f = 2$. So the result has 4 states, 3 arcs and one successful path, of cost 0. Two of its states are dead ends, which a trim step removes. Without the filter, both dead ends lead on to $(1, 1)$, and there are three successful paths. In the tropical semiring the result is still $\min(0, 0, 0) = 0$. In the log semiring it is $-\log 3 = -1.098612$, which is wrong.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). The search of lines L2 to L8 visits each reachable triple once and adds every move out of it once. The filter allows, between two matched moves, only the move sequences of the form $J^* A^*$ or $J^* B^*$, where $J$ is a joint $\varepsilon$ move, $A$ a move of $T_1$ alone and $B$ a move of $T_2$ alone, and exactly one of these words fits each pair of $\varepsilon$ runs. This gives a bijection between the successful paths of $T$ and the pairs of successful paths of $T_1$ and $T_2$ that agree on the middle string, with $w(\pi) = w(\pi_1) \otimes w(\pi_2)$ by commutativity. Distributivity then gives $T(x, z) = \bigoplus_y T_1(x, y) \otimes T_2(y, z)$.

## Complexity

In the word-RAM model, with the states of $T$ kept in an array indexed by the triple, or in a hash table in expected time, and the arcs of $T_2$ grouped by input label, a popped triple $(q_1, q_2, f)$ costs $O(1 + d_1(q_1) d_2(q_2))$, where $d_1$ and $d_2$ are the out-degrees. Each triple is popped once and there are at most $3 s_1 s_2$ triples, so the time is $O(s_1 s_2 + e_1 e_2)$. The output has $O(s_1 s_2)$ states and $O(e_1 e_2)$ arcs, which is also the space.

Without $\varepsilon$ labels on the shared side, the proof shows that $T$ has at most $s_1 s_2$ states and at most $e_1 e_2$ arcs. The bound is reached: if both machines have one state and $k$ self loops that all carry the same middle label, the result has $k^2$ arcs. With labels from a large alphabet, most pairs of arcs do not match, and the result is much smaller than the bound. This is why recognizers compose large machines in practice. Mohri 2009 gives the same $O(|T_1| |T_2|)$ bound, where $|T|$ counts states and arcs.

## Properties

- **Exact in any commutative semiring.** With the filter, every pair of paths is counted once, so the result is right in the log semiring as well as in the tropical one.
- **Lazy.** A triple is expanded only when the search reaches it, so the same loop can run on demand during decoding, and the parts of $T$ that are never reached are never built.
- **Not trim.** The result can have states that reach no final state, such as the dead ends of the example. A trim pass removes them in linear time.
- **Associative.** $(T_1 \circ T_2) \circ T_3$ and $T_1 \circ (T_2 \circ T_3)$ give the same relation, so a cascade can be composed in any grouping. The sizes of the intermediate machines can differ a lot.
- **Acceptors.** For two weighted automata (input label equal to output label), composition is the weighted intersection.

## Variants and improvements

- **Without the filter.** In an idempotent semiring such as the tropical one, the redundant paths do not change the weights, and some implementations skip the filter there. The result has more arcs and more paths.
- **Generalized filters.** Allauzen, Riley and Schalkwyk 2009 make the filter a parameter of the algorithm. Their filters also remove $\varepsilon$ paths that lead nowhere, and push labels and weights forward along $\varepsilon$ paths. OpenFst uses this design.
- **Dynamic composition.** Decoders can compose the lexicon with the language model on the fly, which avoids building the full static graph.
- **Three-way and multi-tape composition.** Composing three machines at once can avoid a large intermediate result.

## When to use it

Use composition whenever a system is a chain of rewrites, each with its own model: phones to context dependent units, phones to words, words to a weighted language model. Compose the chain once, offline, and then optimize the result with [weighted determinization](/weighted-determinization/), [weight pushing](/weight-pushing/) and minimization. When the composed machine is too large to store, compose lazily at search time.

## Pitfalls

- **Counting $\varepsilon$ paths twice.** Without a filter, a pair of $\varepsilon$ moves can be taken in several orders. The log semiring then adds the same probability several times, as in the example.
- **The order of the machines.** The output side of $T_1$ must meet the input side of $T_2$. Swapping the machines gives a different relation, and usually an empty one.
- **Sorting the arcs.** Without an index by label, line L5 tests every pair of arcs, which is slow for states with many arcs. Sort or hash the arcs of one machine by label.
- **Blow-up.** The bound $e_1 e_2$ can be reached. An unpruned trigram model composed with a large lexicon can be too large for memory, so recognizers prune the language model or compose lazily.
- **A non-commutative semiring.** The string semiring and some product semirings are not commutative, and then the weight of a path of $T$ is not the product of the weights of the two paths. The proof needs commutativity.

## Implementations

The Python code builds the reachable triples with a stack and keeps the arcs of $T_2$ in a dictionary by input label. It works in the tropical and in the log semiring on costs, with the filter on or off. The tests compare the weight of every string pair of the composed machine with a brute force sum over all pairs of paths of the two machines, on random machines with $\varepsilon$ labels, and check that the unfiltered version is right in the tropical semiring but wrong in the log semiring.

## History

Composition of unweighted transducers is a classical construction of automata theory. Mohri, Pereira and Riley 1996 gave the weighted version for language and speech, with the epsilon filter that makes it correct in any commutative semiring, and their 2002 paper in Computer Speech and Language describes recognizers built as a cascade of compositions. Mohri 2009 gives the algorithm and the filter in the general setting of weighted automata. Allauzen, Riley and Schalkwyk 2009 turned the filter into a parameter, which allows faster dynamic composition in recognizers.

## References
