---
tag: BE8VD3
kind: technique
slug: adversary-argument
name: Adversary argument
aliases:
- Adversary method
- Ambainis adversary
- adversary lower bound
- adversary method
area: foundations/lower-bounds
level: core
summary: An adversary answers queries so as to keep the algorithm uncertain, forcing many queries before the answer is determined.
prereqs: [lower-bound, decision-tree-model, comparison-model]
see_also: [decision-tree-method, information-theoretic-bound, max-finding-lower-bound, max-min-lower-bound, second-largest-lower-bound, merging-lower-bound, quantum-adversary-method, yao-minimax-principle]
sources:
  - book: isbn:9780201896855
    title: Donald E. Knuth, The Art of Computer Programming, Volume 3, second edition
    locator: Section 5.3.2 (adversary arguments for merging) and Section 5.3.3 (minimum-comparison selection, the adversary with weights for the second largest)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 9.1, Minimum and maximum, and its exercises (the lower bound of ceil(3n/2) - 2 by an adversary)
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach
    locator: Chapter 12, Decision trees (lower bounds by adversaries, certificate complexity)
  - paper: doi:10.1145/361405.361423
    title: Ira Pohl, A sorting problem and its complexity, Communications of the ACM 15(6) (1972)
    locator: pp. 462 to 464 (the bound for the maximum and the minimum)
  - paper: "Andris Ambainis, Quantum lower bounds by quantum arguments, Journal of Computer and System Sciences 64(4) (2002)"
    locator: pp. 750 to 767 (the quantum adversary method)
---

An adversary argument proves a lower bound by a game. The algorithm asks queries about a hidden input, and an adversary answers them. The adversary does not fix the input in advance. It chooses each answer so that the algorithm learns as little as possible, and it only promises that at the end some input agrees with all its answers. If the adversary can keep two inputs with different correct outputs alive for $t$ queries, every algorithm of the model needs more than $t$ queries in the worst case. It gives the exact bounds $n - 1$ for the [maximum](/max-finding-lower-bound/), $\lceil 3n/2 \rceil - 2$ for the [maximum and minimum](/max-min-lower-bound/) and $n + \lceil \lg n \rceil - 2$ for the [second largest](/second-largest-lower-bound/).

## In plain words

Think of a game of twenty questions with a player who cheats. The player has not picked a secret. Each time you ask a question, the player picks the reply that leaves you with the most cases still open, and only takes care never to contradict an earlier reply. If you stop and guess while two cases are still open, the player picks the other one, and you are wrong.

A lower bound by an adversary works in the same way. Any method asks questions about the input, and the adversary replies so as to make each question count for as little as possible. You keep a score of how much is still unknown, and you show that one question lowers it only by a little. Since the method cannot stop while the answer is still open, it must ask many questions.

## When it applies

- The algorithms learn about the input only through queries, as in the [comparison model](/comparison-model/) or a [decision tree](/decision-tree-model/), and the cost is the number of queries.
- The problem has few outputs, so leaf counting is weak, but much must be checked before the answer is known: the maximum, the maximum and minimum, connectivity, merging.
- The algorithms are deterministic. An adversary that adapts to the queries cannot fool a randomized algorithm in the same way. For randomized algorithms, use the [Yao minimax principle](/yao-minimax-principle/).

## The template

The adversary keeps the set $S$ of inputs that agree with all answers so far, or a compact summary of it, and a measure of progress $\Phi$.

```pseudo id=main
ADVERSARY-GAME(A, n)                    ▷ A is any algorithm of the model
L1  S ← all inputs of size n             ▷ the inputs that agree with every answer so far
L2  while A has not stopped do
L3      q ← the next query of A
L4      choose an answer a with S_a = {x ∈ S : q(x) = a} not empty and Φ(S_a) ≥ Φ(S) − δ
L5      S ← S_a; give the answer a to A
L6  ▷ A is correct only if every x in S has the same output
```

To use it, fill in four holes.

1. **The state.** Choose what the adversary records: a status for each item (never compared, has only won, has only lost, both), a weight, an interval of candidate positions, or the set of edges known to be present and absent.
2. **The potential.** Define $\Phi$ with a known start value $\Phi_0$, and show that while two inputs in $S$ have different correct outputs, $\Phi > \Phi_{\mathrm{end}}$.
3. **The answer rule.** For each kind of query, give an answer that lowers $\Phi$ by at most $\delta$, and show that it agrees with an input: at each step, $S_a$ is not empty. Often the proof keeps an explicit input and changes it in ways that keep all earlier answers true.
4. **The count.** The algorithm cannot stop before $\Phi \le \Phi_{\mathrm{end}}$, so it makes at least $\lceil (\Phi_0 - \Phi_{\mathrm{end}})/\delta \rceil$ queries. When different queries lower $\Phi$ by different amounts, count each kind separately.

A tree view of the same argument: the adversary picks one path of the [decision tree](/decision-tree-model/) of the algorithm, and the bound is the length of that path.

## Classic examples

**1. OR of $n$ bits, and search in an unsorted array.** The adversary answers 0 to each query. While a bit is unread, the inputs "all zero" and "all zero except a 1 at the unread bit" agree with all answers and have different outputs. So $n$ queries are needed. For search, the adversary answers "not here" to each probe, and [linear search](/linear-search/) is optimal.

**2. Maximum.** The state is the set of items that have never lost. The adversary answers each comparison of two distinct items consistently with a fixed order of distinct values, but before each answer it may raise an item that has never lost above all others, which keeps all earlier answers true. Each comparison removes at most one item from the set. The algorithm cannot stop while two items have never lost, so it needs $n - 1$ comparisons. See the [maximum finding lower bound](/max-finding-lower-bound/).

**3. Maximum and minimum.** The state is a label for each item: N (never compared), W (has won and never lost), L (has lost and never won), M (both). The potential counts 2 for N, 1 for W or L, and 0 for M. It starts at $2n$ and must reach 2. Only a comparison of two N items lowers it by 2, and there are at most $\lfloor n/2 \rfloor$ of them. So $2n - 2 - \lfloor n/2 \rfloor = \lceil 3n/2 \rceil - 2$ comparisons are needed (Pohl, 1972). See the [max-min lower bound](/max-min-lower-bound/).

**4. Second largest.** Each item that has never lost carries a weight, at first 1. When two such items meet, the heavier one wins and takes the weight of the other. The final maximum ends with weight $n$, and each of its comparisons at most doubles its weight, so it met at least $\lceil \lg n \rceil$ items. Each of those but one must also lose to another item. With $n - 1$ first losses this gives $n + \lceil \lg n \rceil - 2$. See the [second largest lower bound](/second-largest-lower-bound/).

**5. Merging.** The adversary fixes the order $a_1 < b_1 < a_2 < \dots < a_n < b_n$ and answers truthfully. Every one of the $2n - 1$ adjacent pairs must be compared, since otherwise swapping its two values changes the output and no answer. See the [merging lower bound](/merging-lower-bound/).

**6. Connectivity of a graph on $v$ vertices.** The algorithm asks "is $\{u, w\}$ an edge?". Let $Y$ be the pairs answered yes and $U$ the pairs not yet asked. The adversary answers no, unless the graph $Y \cup U$ without $\{u, w\}$ would be disconnected; then it answers yes. So $Y \cup U$ stays connected. Each yes answer is to a bridge of $Y \cup U$, so it closes no cycle with $Y$, and $Y$ stays a forest.

*Claim.* While $U$ is not empty, $Y$ is disconnected. Suppose $Y$ is connected and $\{a, b\} \in U$. Then $Y$ is a spanning tree with a path $P$ from $a$ to $b$. Let $f$ be the edge of $P$ that was answered last. When $f$ was answered, each other edge of $P$ was in $Y$ or in $U$, and so was $\{a, b\}$. So $f$ lay on the cycle $P + \{a, b\}$ in $Y \cup U$, and it was not a bridge. But then the adversary answered no to $f$, a contradiction.

So while a pair is unasked, the graph $Y$ (disconnected) and the graph $Y \cup U$ (connected) both agree with all answers, and the algorithm cannot stop. Every algorithm asks all $\binom{v}{2}$ pairs on some input: connectivity is evasive. For $v = 10$ that is 45 queries.

**7. Search in a sorted array.** The adversary keeps the interval of gaps where the key can still fall and answers to keep the larger part. Each answer keeps at least half of the open gaps, which gives $\lceil \lg(n+1) \rceil$. See the [sorted search lower bound](/sorted-search-lower-bound/).

The bounds of the comparison examples for $n = 8$ and $n = 100$:

| problem | bound | $n = 8$ | $n = 100$ | leaf counting alone |
|---|---|---|---|---|
| maximum | $n - 1$ | 7 | 99 | $\lceil \lg n \rceil$: 3 and 7 |
| maximum and minimum | $\lceil 3n/2 \rceil - 2$ | 10 | 148 | $\lceil \lg(n(n-1)) \rceil$: 6 and 14 |
| second largest | $n + \lceil \lg n \rceil - 2$ | 9 | 105 | $\lceil \lg(n(n-1)) \rceil$: 6 and 14 |
| merging two lists of $n/2$ | $n - 1$ | 7 | 99 | $\lceil \lg \binom{n}{n/2} \rceil$: 7 and 97 |

## Variations

- **Information adversary.** Answer so that the largest part of the remaining outputs survives. This gives the [information-theoretic bound](/information-theoretic-bound/) and is the weakest form.
- **Potential or weight adversary.** As in examples 3 and 4: a numeric potential and a bound on its change per query.
- **Fixed input with local changes.** As in examples 2 and 5: the adversary fixes one input and shows that a path that skips a query admits a changed input with a different output. This is the path form of the [decision tree method](/decision-tree-method/).
- **Evasiveness.** Adversaries for graph properties that force all $\binom{v}{2}$ queries. The Aanderaa, Karp and Rosenberg conjecture says that every nontrivial monotone graph property is evasive. See the [decision tree model](/decision-tree-model/).
- **Quantum adversary.** Ambainis (2002) gave an adversary method for quantum query algorithms. It weighs pairs of inputs with different outputs and bounds how fast one query can separate them, and it gives the bound $\Omega(\sqrt{n})$ for unordered search. See the [quantum adversary method](/quantum-adversary-method/).
- **Adversaries in online algorithms.** The words [adaptive adversary](/adaptive-adversary/) and [oblivious adversary](/oblivious-adversary/) in competitive analysis name a related idea: the adversary chooses the request sequence. The bound is on the competitive ratio, not on the number of queries.

### Pitfalls

- **Inconsistent answers.** The adversary must never answer in a way that no input satisfies. Each rule needs a proof that an input agrees with all answers. In the maximum and minimum game, an item labelled W may be raised and an item labelled L may be lowered, because no earlier answer forbids it. Raising an item labelled L could break an answer.
- **Assuming a strategy for the algorithm.** The bound must hold for every algorithm. The adversary may react to the queries, but the proof may not assume which queries come, or in which order.
- **A missing end condition.** The proof must show that the algorithm cannot stop early: two inputs with different correct outputs must remain while $\Phi > \Phi_{\mathrm{end}}$.
- **Counting the best query only.** The decrease $\delta$ must bound every possible query, including ones that look useless. In the maximum and minimum game, a comparison of two N items is the one that lowers the potential by 2, and the count must allow for it.
- **Randomized algorithms.** An adaptive adversary argument proves nothing about a randomized algorithm, whose next query the adversary cannot predict. Use a distribution on inputs and Yao's principle.

## Exercises

1. Give an adversary that forces each comparison algorithm for the minimum of $n$ distinct items to make $n - 1$ comparisons.
2. Show that deciding whether a graph on $v$ vertices given by its adjacency matrix has at least one edge needs $\binom{v}{2}$ queries.
3. Prove that merging a sorted list of 2 items with a sorted list of $n$ items needs at least $\lceil \lg \binom{n+2}{2} \rceil$ comparisons, and give an adversary that matches it for $n = 3$.
4. Show that deciding whether a graph on $v$ vertices has a vertex of degree $v - 1$ needs $\Omega(v^2)$ queries.
5. In the maximum and minimum game, explain why the adversary may not answer a comparison of two W items by its fixed order without raising one of them first.
6. Show that the adversary for the maximum also proves that every algorithm makes at least $n - 1$ comparisons on every input, not only on one.

## References
