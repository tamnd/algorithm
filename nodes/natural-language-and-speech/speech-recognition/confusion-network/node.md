---
tag: Q6R3VD
kind: data-structure
slug: confusion-network
name: Confusion network
aliases:
- sausage
area: natural-language-and-speech/speech-recognition
level: advanced
summary: A lattice reduced to a linear sequence of slots of competing words with posteriors, whose best path approximately minimizes expected word errors.
model: word-ram
complexity:
  vars: {N: the number of lattice nodes, E: the number of lattice arcs}
  time: {worst: "O(N^2 + E^3)"}
  space: {extra: "O(N^2 + E^2)"}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [word-lattice, forward-backward-algorithm, edit-distance, word-error-rate]
see_also: [minimum-bayes-risk-decoding, lattice-rescoring, multiple-sequence-alignment, progressive-alignment, agglomerative-clustering, transitive-closure, keyword-spotting, time-synchronous-beam-search]
sources:
  - paper: doi:10.1006/csla.2000.0152
    title: Lidia Mangu, Eric Brill and Andreas Stolcke, Finding consensus in speech recognition, word error minimization and other applications of confusion networks, Computer Speech and Language 14(4), 2000, pages 373 to 400
    locator: the lattice alignment algorithm (initial classes, intra-word and inter-word clustering, pruning), confusion networks with the empty word, and the consensus hypothesis
  - url: https://arxiv.org/abs/cs/0010012
    title: The same paper as submitted, arXiv cs/0010012, 2000
    locator: Section 3 (the algorithm, with the similarity measures in equations 5 and 6 and the score scaling in Section 3.7), Appendix B (pseudo-code and the O(T^3) cost) and Appendix C (proof that merging keeps a consistent partial order)
---

A confusion network, also called a sausage, is a [word lattice](/word-lattice/) squeezed into a straight line. It is a sequence of slots. Each slot holds the words that compete for one position, with their posterior probabilities, and an empty word $\varepsilon$ for the paths that put no word there. Any choice of one entry per slot is a hypothesis. Mangu, Brill and Stolcke 2000 build it by aligning all the lattice paths with each other: the lattice arcs are clustered into slots by time overlap and word similarity, in a way that keeps the order of the lattice. Taking the most likely entry in each slot gives the *consensus hypothesis*. It minimizes the expected number of errors counted slot by slot, and that count is an upper bound on the word error, so the consensus approximately minimizes the expected word error, often better than the most likely path does.

## In plain words

A lattice holds many possible sentences, and they share parts. The best whole sentence is not always the one with the fewest expected word mistakes. Word error counts words, so it is better to ask, position by position, which word is most likely.

To do that, you must first decide which words of different sentences stand at the same position. A confusion network lines all the sentences up. Words that cover the same stretch of time and sound alike go into the same slot, and every slot gets a "no word" choice for the sentences that skip it. Then you pick the strongest word in each slot.

## The abstract type

A confusion network is built once from a lattice and then queried.

- `build(lattice, λ, ip, κ, θ)` computes arc posteriors with the language model weight $\lambda$, the insertion penalty $ip$ and the acoustic scale $\kappa$, drops the arcs with a posterior of at most $\theta$, and aligns the rest into slots.
- `slots[i]` maps each word $w$ of slot $i$ to its posterior $p_i(w)$, and `eps[i]` is $p_i(\varepsilon)$.
- `consensus()` returns the word of largest posterior in each slot, without $\varepsilon$.
- `expected_errors(c)` returns $\sum_i (1 - p_i(c_i))$ for one choice $c_i$ per slot.
- `slot_of[e]` is the slot of lattice arc $e$.

## Representation

The network is a list of $L$ slots, each a map from words to posteriors, plus one number for $\varepsilon$. As a graph it has $L + 1$ nodes in a line and one arc per entry between neighbors. The code also keeps the slot of every lattice arc.

**Invariant.**

- **(C1) Probabilities.** In every slot, the word posteriors and $p_i(\varepsilon)$ are at least 0 and add up to 1.
- **(C2) Order.** If a lattice arc $e$ can come before an arc $f$ on a path, the slot of $e$ is before the slot of $f$.
- **(C3) Exclusion.** No lattice path uses two arcs of the same slot.

## Operations

```pseudo id=main
BUILD-CONFUSION-NETWORK(Λ, λ, ip, κ, θ)
L1  γ ← ARC-POSTERIORS(Λ, λ, ip, κ); keep the arcs with γ(e) > θ
L2  e ≺ f ⟺ a path of kept arcs leads from the end of e to the start of f
L3  classes ← the kept arcs grouped by (word, start time, end time); < ← the transitive closure of ≺ on classes
L4  while two unordered classes with the same word have SIM₁ > 0 do
L5      MERGE the pair with the largest SIM₁
L6  while two classes are unordered do
L7      MERGE the pair with the largest SIM₂
L8  sort the classes by <; slot i gets p_i(w) ← the sum of γ(e) over e in C_i with the word w
L9  p_i(ε) ← 1 - the sum of p_i(w) over the words w

CONSENSUS(network)
L10 for each slot i: choose the word or ε with the largest p_i, and output the words
```

The similarities are those of Mangu, Brill and Stolcke 2000. For the intra-word step, $\mathrm{SIM}_1(A, B)$ is the largest $\mathrm{overlap}(e, f)\, \gamma(e)\, \gamma(f)$ over $e \in A$ and $f \in B$, where the overlap is the common time of the two arcs divided by the sum of their lengths. For the inter-word step, $\mathrm{SIM}_2(A, B)$ is the average of $\mathrm{sim}(w_1, w_2)\, p_A(w_1)\, p_B(w_2)$ over the words $w_1$ of $A$ and $w_2$ of $B$, where $\mathrm{sim}$ is 1 minus the edit distance of the pronunciations divided by the sum of their lengths. The code has no pronunciations and uses the letters of the words instead. You can pass another similarity.

MERGE joins two unordered classes $a$ and $b$. The new class comes after every class that came before $a$ or $b$ and before every class that came after $a$ or $b$, and every class before $a$ now also comes before every class after $b$, and the other way round. This keeps the order transitive and consistent with the lattice, and it never orders a class before itself, because $a$ and $b$ were unordered. Each merge removes a class, and the loop of line L6 runs until every pair is ordered, so the result is a total order.

The acoustic scale $\kappa$ of line L1 matters as much as on the lattice. Mangu, Brill and Stolcke 2000 found that the best scale was 1 for the language model log probabilities and $1 / \lambda$ for the acoustic ones. With a peaked posterior, the consensus moves to the most likely path.

## Example

Take the lattice of the [word lattice](/word-lattice/) page with $\lambda = 10$ and $\kappa = 1 / 10$. The arcs a and x span the frames 0 to 30, and the arcs b (twice), c span 30 to 60. Their posteriors are a 0.6262, x 0.3738, b 0.2819 (after a), c 0.3443 and b 0.3738 (after x).

1. Line L3 gives four classes: $\{a\}$, $\{x\}$, $\{b, b\}$ (same word and same times) and $\{c\}$. The lattice orders $\{a\}$ before $\{b, b\}$ and $\{c\}$, and $\{x\}$ before $\{b, b\}$.
2. No two classes have the same word, so the intra-word step does nothing.
3. Three pairs are unordered: $\{a\}, \{x\}$; $\{b, b\}, \{c\}$; and $\{x\}, \{c\}$, since no path goes from x to c. Every pair of distinct one-letter words has the similarity $1 - 1/2 = 0.5$, so $\mathrm{SIM}_2$ is $0.5 \cdot 0.6262 \cdot 0.3738 = 0.1170$, $0.5 \cdot 0.6557 \cdot 0.3443 = 0.1129$ and $0.5 \cdot 0.3738 \cdot 0.3443 = 0.0644$. The first pair is merged. The new class $\{a, x\}$ comes before both $\{b, b\}$ and $\{c\}$, so only $\{b, b\}, \{c\}$ is left, and it is merged next.

The network has two slots with no $\varepsilon$:

| slot | entries |
|---|---|
| 1 | a 0.6262, x 0.3738 |
| 2 | b 0.6557, c 0.3443 |

The consensus is "a b", with $(1 - 0.6262) + (1 - 0.6557) = 0.7181$ expected errors. The most likely path "x b" has 0.9705, and "a c" has 1.0295. Here "a b" is the path with the lowest score in the lattice, yet it has the fewest expected errors. The network has $2 \cdot 2 = 4$ paths, one more than the lattice: "x c" was not a lattice path.

With $\kappa = 1$ instead, the slots become a 0.3326, x 0.6674 and b 0.7070, c 0.2930, and the consensus is "x b", the most likely path. This is the effect of a peaked posterior.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). Line L3 starts with a consistent order, since start times strictly increase along the lattice order. MERGE keeps the order irreflexive, transitive and consistent with the lattice whenever the two classes are unordered, so two arcs in one class are never on one path. Hence each lattice path picks at most one entry per slot, which gives three facts. Every lattice path is a network path, with $\varepsilon$ in the slots it skips. The posterior $p_i(w)$ is the probability that a path has the word $w$ in slot $i$, and $p_i(\varepsilon)$ is the probability that it has nothing there. The expected number of slots in which a choice $c$ differs from a random path is $\sum_i (1 - p_i(c_i))$. The consensus minimizes each term. Finally, the slots align any two hypotheses, so the slot errors are at least the word edit distance, and the consensus minimizes an upper bound on the expected word error, not the word error itself.

The tests check these facts on random lattices against enumeration of all paths, and check that the consensus is the best of all network paths by the slot error.

## Complexity

Let $N$ be the number of lattice nodes and $E$ the number of arcs. The posteriors take $O(N + E)$ time. The reachability of line L2 takes $O(N (N + E))$ time and $O(N^2)$ bits. The initial order compares arcs of all pairs of classes, $O(E^2)$ in total. Each round of a clustering loop looks at all pairs of classes, at a cost of $O(E^2)$ for the similarities and order tests, and a merge updates $O(E)$ successor sets of size $O(E)$. There are at most $E - 1$ merges, so the clustering takes $O(E^3)$ time, which matches the $O(T^3)$ of Mangu, Brill and Stolcke for $T$ links. In total this is $O(N^2 + E^3)$ time and $O(N^2 + E^2)$ space, with a word similarity in $O(1)$. That is why the lattice is pruned first: Mangu, Brill and Stolcke report that about 95 percent of the links can be removed without hurting the consensus.

The consensus, the expected errors and the path count take time linear in the size of the network.

## Variants

- **Pruning threshold.** With $\theta > 0$, unlikely paths no longer force likely words into different slots. This helped accuracy in the original experiments. The slot mass can then exceed 1 a little, since two arcs of one slot can share a pruned path.
- **Without times.** If the lattice has no times, the overlap can use path lengths as approximate times, or the intra-word step can use the posteriors alone, as tested by Mangu, Brill and Stolcke.
- **Other similarities.** Phone edit distance with features such as voicing, or plain letter distance as in the code.
- **Minimum Bayes risk decoding.** The consensus is a cheap form of [minimum Bayes risk decoding](/minimum-bayes-risk-decoding/) with an alignment fixed in advance. Exact search for the minimum expected word error over a lattice is much harder.
- **System combination.** Networks from several recognizers can be aligned with each other and voted on, slot by slot.

## When to use it

Use a confusion network when the goal is a low word error rate and you have lattices with good posteriors. It also gives a word confidence (the slot posterior), compact storage of the alternatives, and a simple index for [keyword spotting](/keyword-spotting/). Do not use it when a later step needs the exact sentence set of the lattice: the network adds paths that the lattice did not have, and it loses the language model scores between words.

## Pitfalls

- **Unscaled posteriors.** With $\kappa = 1$, almost all the mass goes to the best path, and the consensus is just the most likely path.
- **Low-probability arcs.** One unlikely path that puts a word before a similar word can force them into different slots. Prune first.
- **Not exact.** The consensus minimizes the expected slot error, not the expected word error. The clustering is a heuristic, and the best multiple alignment has no known efficient algorithm.
- **New sentences.** The consensus may not be a path of the lattice at all, and it may not be grammatical.
- **Silence and filler words.** They should be mapped to $\varepsilon$ before the consensus, or they compete with real words.
- **Cubic time.** Without pruning, the clustering is slow on large lattices.

## Implementations

The Python code computes arc posteriors by forward-backward on a lattice whose arcs move forward in time, the reachability of nodes as bit masks, the initial classes and their order, the two clustering loops with the similarities of the paper (letters in place of phones), and the slots with $\varepsilon$. The tests compare slot posteriors and $\varepsilon$ with enumeration of all lattice paths, check that every lattice path maps to increasing slots, check that the consensus has the smallest expected slot error of all network paths and that the slot error is at least the word edit distance, check pruning, and check the example.

## History

Stolcke, Konig and Weintraub 1997 minimized word error over N-best lists, which is limited by the size of the list. Mangu, Brill and Stolcke 2000 moved word error minimization to lattices by aligning all the lattice paths into one confusion network, and they showed that it lowered the word error in their experiments, which included Switchboard. The same paper used the networks for lattice compression, word spotting and confidence annotation.

## References
