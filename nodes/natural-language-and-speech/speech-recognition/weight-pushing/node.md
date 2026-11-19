---
tag: GPP9K3
kind: algorithm
slug: weight-pushing
name: Weight pushing
aliases:
- WFST weight pushing
area: natural-language-and-speech/speech-recognition
level: advanced
summary: Move the weights of a weighted automaton toward the initial state using shortest distances to the final states, which aids pruning.
model: word-ram
complexity:
  vars: {n: the number of states, m: the number of arcs}
  time: {worst: "O(n m)"}
  space: {extra: "O(n + m)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1997
  people: [Mehryar Mohri]
  note: Mohri used weight pushing in 1997 as the first step of the minimization of weighted automata, and Mohri, Pereira and Riley applied it to the networks of speech recognizers to make pruning work better.
prereqs: [weighted-automaton, bellman-ford]
see_also: [dag-shortest-paths, dijkstra, weighted-determinization, weighted-transducer-composition, hclg-decoding-graph, dfa-minimization, forward-backward-algorithm, time-synchronous-beam-search]
sources:
  - url: https://aclanthology.org/J97-2003/
    title: Mehryar Mohri, Finite-state transducers in language and speech processing, Computational Linguistics 23(2), 1997, pages 269 to 311
    locator: the section on the minimization of weighted automata, which first pushes the weights toward the initial state
  - paper: doi:10.25596/jalc-2002-321
    title: Mehryar Mohri, Semiring frameworks and algorithms for shortest-distance problems, Journal of Automata, Languages and Combinatorics 7(3), 2002, pages 321 to 350
    locator: the generic single-source shortest-distance algorithm
  - book: isbn:9783642014918
    title: Mehryar Mohri, Weighted automata algorithms, in Manfred Droste, Werner Kuich and Heiko Vogler (editors), Handbook of Weighted Automata, Springer, 2009
    locator: "Section 6.3 (weight pushing, Proposition 7 and its running times) and Theorem 8 (minimization by pushing and unweighted minimization)"
  - paper: doi:10.1006/csla.2001.0184
    title: Mehryar Mohri, Fernando Pereira and Michael Riley, Weighted finite-state transducers in speech recognition, Computer Speech and Language 16(1), 2002, pages 69 to 88
    locator: the section on weight pushing and its effect on pruning in the recognition network
---

Weight pushing moves the weights of a weighted automaton or transducer as far as possible toward the start state, and keeps the weight of every string the same. It first computes, for each state $q$, the shortest distance $d(q)$ from $q$ to the final states. Then it adds $d(n) - d(p)$ to each arc from $p$ to $n$, adds $d$ of the start state to the initial weight, and subtracts $d(q)$ from each final weight. In the tropical semiring, the cheapest way out of each state then costs exactly 0. In the log semiring, the result is stochastic: the weights that leave a state are probabilities that add up to 1. A speech decoder prunes better on a pushed graph, because the cost of a partial path then shows the cost of its best ending.

## In plain words

Each path through a weighted graph has a total cost. Where the cost sits along the path does not change the total, but it changes what a search sees early. If a path starts cheap and ends expensive, a search that drops costly partial paths keeps the wrong ones.

So for each state, find the cheapest way from it to the end. Charge that amount as early as you can. Each arc then costs only how much worse it is than the best choice at its state. The totals stay the same, and the best choice at each state costs 0.

## The problem

A weighted transducer over a semiring $(K, \oplus, \otimes, \bar 0, \bar 1)$ has states $Q$, a start state $i$ with an initial weight $\lambda$, final weights $\rho(q)$, and arcs $(p, a, b, w, n)$ from $p$ to $n$ with input label $a$, output label $b$ and weight $w$ ([weighted automaton](/weighted-automaton/)). The labels play no part here. The distance to the final states is

$$D(p) = \bigoplus_{\pi \text{ from } p \text{ to a final } q} w(\pi) \otimes \rho(q).$$

The task: build an equivalent machine in which, at every state, $\rho(p) \oplus \bigoplus_e w(e) = \bar 1$ over the arcs $e$ that leave $p$.

The weights here are costs $c = -\log p$, as in Mohri, Pereira and Riley 2002. A probability $p$ becomes the cost $-\log p$, and a probability of 0 becomes $+\infty$. The tropical semiring $(\mathbb{R} \cup \{+\infty\}, \min, +, +\infty, 0)$ keeps the best path, and the log semiring with $a \oplus b = -\log(e^{-a} + e^{-b})$ adds probabilities. In both, $\otimes$ is $+$, and dividing by a finite weight $w$ is subtracting $w$.

## The algorithm

The first part is Mohri's generic single-source shortest-distance algorithm, run backward from the final states. Each state $q$ keeps the distance $d(q)$ found so far and the residual $r(q)$, the part of $d(q)$ that it has not yet passed to its predecessors. The second part is the reweighting.

```pseudo id=main
WEIGHT-PUSH(T)
L1  for each final q: d(q) ← r(q) ← ρ(q); enqueue q          ▷ all other d, r are 0̄
L2  while the queue S is not empty do
L3      q ← DEQUEUE(S)
L4      R ← r(q);  r(q) ← 0̄
L5      for each arc (p, a, b, w, q) into q do
L6          if d(p) ⊕ (w ⊗ R) differs from d(p) then d(p) ← d(p) ⊕ (w ⊗ R);  r(p) ← r(p) ⊕ (w ⊗ R)
L7              if p ∉ S then ENQUEUE(S, p)
L8  if d(i) = 0̄ then fail: no successful path
L9  drop the states q with d(q) = 0̄ and their arcs
L10 λ ← λ ⊗ d(i)
L11 for each arc e from p to n: w(e) ← d(p)⁻¹ ⊗ w(e) ⊗ d(n)     ▷ on costs: w + d(n) - d(p)
L12 for each final q: ρ(q) ← d(q)⁻¹ ⊗ ρ(q)                      ▷ on costs: ρ(q) - d(q)
```

In the tropical semiring "differs" at line L6 means "is smaller". In the log semiring it means "changes by more than $\delta$". With a FIFO queue in the tropical semiring, lines L1 to L7 are the queue form of [Bellman-Ford](/bellman-ford/) on the reversed graph. In the log semiring they are a fixed-point iteration for the linear system $x = P x + f$ of the probabilities, which stops at tolerance $\delta$.

## Example

The machine has the arcs $0 \xrightarrow{a/0} 1$, $0 \xrightarrow{b/1} 2$, $1 \xrightarrow{c/3} 3$, $2 \xrightarrow{c/1} 3$ and $2 \xrightarrow{d/4} 3$, with state 3 final with weight 0 and $\lambda = 0$. Its strings are $ac$ with cost 3, $bc$ with cost 2 and $bd$ with cost 5.

In the tropical semiring the distances are $d = (2, 3, 1, 0)$. The pushed machine:

| arc | old weight | $w + d(n) - d(p)$ |
|---|---|---|
| $0 \xrightarrow{a} 1$ | 0 | $0 + 3 - 2 = 1$ |
| $0 \xrightarrow{b} 2$ | 1 | $1 + 1 - 2 = 0$ |
| $1 \xrightarrow{c} 3$ | 3 | $3 + 0 - 3 = 0$ |
| $2 \xrightarrow{c} 3$ | 1 | $1 + 0 - 1 = 0$ |
| $2 \xrightarrow{d} 3$ | 4 | $4 + 0 - 1 = 3$ |

The initial weight becomes $\lambda = 2$. The string $ac$ costs $2 + 1 + 0 = 3$, $bc$ costs $2 + 0 + 0 = 2$ and $bd$ costs $2 + 0 + 3 = 5$, as before. At each of the states 0, 1 and 2, the cheapest arc out costs 0.

Now consider a beam search that reads one symbol and keeps the cheaper partial path. Before pushing, $a$ costs 0 and $b$ costs 1, so it keeps $a$, whose best ending gives 3. After pushing, $a$ costs 1 and $b$ costs 0, so it keeps $b$, which leads to the best string $bc$ with cost 2.

In the log semiring, $d(2) = -\log(e^{-1} + e^{-4}) \approx 0.9514$, $d(1) = 3$ and $d(0) = -\log(e^{-3} + e^{-2} + e^{-5}) \approx 1.651$. The pushed arcs from state 0 have the probabilities $0.2595$ for $a$ and $0.7405$ for $b$, and those from state 2 have $0.9526$ for $c$ and $0.0474$ for $d$. Each set adds up to 1, and $e^{-1.651} \approx 0.1919$ is the total probability of the machine.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It has two parts.

- **Equivalence for any potential.** Along a successful path $i = q_0, \ldots, q_k$, the added terms $d(q_j) - d(q_{j-1})$ telescope, and $+d(i)$ in $\lambda$ and $-d(q_k)$ in $\rho$ cancel the rest. So every path keeps its weight for any finite $d$, even an approximate one.
- **The normal form.** The distances satisfy $D(p) = \rho(p) \oplus \bigoplus_e w(e) \otimes D(n)$. Subtracting $D(p)$ on both sides gives $\rho'(p) \oplus \bigoplus_e w'(e) = 0 = \bar 1$. In the tropical semiring this means the minimum is 0. In the log semiring it means the probabilities add up to 1.

Lines L1 to L7 compute $D$ exactly in the tropical semiring when no cycle has a negative cost. The proof shows that each $d(p)$ is always the weight of some path, so $d \ge D$, and that at the end $d(p) \le w + d(q)$ for every arc, so $d \le D$.

## Complexity

Let $n$ be the number of states and $m$ the number of arcs, in the word-RAM model.

- **Tropical semiring, FIFO queue.** $O(n m)$ time, as for Bellman-Ford, with no cycle of negative cost.
- **Tropical semiring, non-negative weights.** With a priority queue instead of the FIFO queue, it is [Dijkstra's algorithm](/dijkstra/), with $O(m + n \log n)$ time (Mohri 2009, Section 6.3).
- **Acyclic machines.** In reverse topological order each state is handled once, so the time is $O(n + m)$ in any semiring ([DAG shortest paths](/dag-shortest-paths/)).
- **Log semiring, with cycles.** The number of rounds depends on $\delta$ and on how fast the probabilities of long paths fall. There is no bound in $n$ and $m$ alone.

Lines L8 to L12 take $O(n + m)$ time. The extra space is $O(n + m)$ for the distances, the residuals, the queue and the reversed arcs.

## Properties

- **Exact.** Every string, or string pair, keeps its weight, whatever values $d$ has.
- **The machine shape does not change.** Pushing changes only weights and drops states that reach no final state. It never adds a state or an arc.
- **Stochastic in the log semiring.** At each state, the outgoing probabilities and the final probability add up to 1, so the pushed machine reads as a Markov chain over its arcs.
- **Non-negative in the tropical semiring.** All pushed weights are at least 0, and the best arc out of each state has weight 0.
- **A canonical form.** Two equivalent deterministic machines that differ only in where their weights sit become equal after pushing and unweighted minimization (Mohri 2009, Theorem 8).

## Variants and improvements

- **Pushing toward the final states.** Run the same steps on the reversed machine, with distances from the start state.
- **Pushing labels.** The same idea moves output labels toward the start state in a transducer.
- **Approximate distances.** Any potential keeps the weights, so a decoder can push with distances from a smaller model or with a cut-off $\delta$, and lose only the normal form.
- **The log semiring for the tropical search.** Speech toolkits often push a graph in the log semiring and then search it in the tropical semiring. The result is stochastic, which keeps language model probabilities comparable across states.

## When to use it

Use it on a recognition graph after [composition](/weighted-transducer-composition/) and [determinization](/weighted-determinization/) (see [HCLG decoding graph](/hclg-decoding-graph/)), so that a beam search sees the language model cost of a word as early as possible. Use it as the first step of the minimization of a weighted automaton. Use it when you want a stochastic machine from one that has arbitrary non-negative weights. Do not expect it to help a search that does not prune, because an exact search finds the same best path either way.

## Pitfalls

- **No successful path.** If no final state can be reached from the start, $d(i) = \bar 0$ and there is nothing to push. The code raises an error.
- **Dead states.** A state that reaches no final state has $d = +\infty$, and $w + d(n) - d(p)$ would give $\infty - \infty$. Drop those states first.
- **Negative cycles.** In the tropical semiring a cycle of negative cost makes $D$ equal $-\infty$, and the FIFO loop never stops.
- **Divergent sums.** In the log semiring a cycle whose probabilities add up to 1 or more makes $D$ infinite or undefined. The weights must form a convergent system.
- **Tolerance.** In the log semiring the loop stops at $\delta$, so the result is stochastic only up to about $\delta$ per state.
- **Pushing changes intermediate scores.** A decoder that reports partial scores, or a lattice that keeps arc scores, shows different numbers after pushing, even though the totals agree.

## Implementations

The Python code pushes weighted transducers with costs in the tropical and the log semiring, with the generic shortest-distance algorithm on a FIFO queue. The tests check the tropical distances against Bellman-Ford and the log distances against Gaussian elimination on random machines with cycles, check that every string of length at most 4 keeps its weight, check the normal form at every state (minimum 0, or probabilities that add up to 1), check the example, check that two equivalent machines with differently placed weights become equal, and check the error when no final state can be reached.

## History

Mohri 1997 introduced weight pushing as the first step of the minimization of weighted automata over the tropical semiring: push the weights, then minimize with each (label, weight) pair as one symbol. Mohri 2002 gave the generic shortest-distance algorithm over semirings that pushing uses. Mohri, Pereira and Riley 2002 described its use in speech recognition, where pushing the language model weights forward in the recognition network makes beam pruning more accurate, and Mohri 2009 gives the general algorithm and its running times.

## References
