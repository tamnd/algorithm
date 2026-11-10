---
tag: QF7GHN
kind: technique
slug: list-contraction
name: List contraction
aliases:
- independent-set removal
area: parallel/parallel-primitives
level: advanced
summary: Splice an independent set of nodes out of a list, folding their values into their neighbours, recurse on the shorter list, then put them back. Random coins remove a quarter per round.
prereqs: [linked-list, independent-set, linearity-of-expectation, work-span-model]
see_also: [list-ranking, parallel-list-ranking, pointer-jumping, tree-contraction, random-mate-contraction, graph-contraction, chernoff-bound, cole-vishkin]
sources:
  - paper: doi:10.1109/SFCS.1985.43
    title: Gary L. Miller and John H. Reif, Parallel tree contraction and its application, 26th Annual Symposium on Foundations of Computer Science (FOCS), 1985
    locator: pp. 478 to 489 (random mate, the coin-flip choice of nodes to splice out in the COMPRESS step)
  - book: isbn:9780201548563
    title: Joseph JaJa, An Introduction to Parallel Algorithms, Addison-Wesley, 1992
    locator: Chapter 2, Section 2.7 (breaking symmetry, deterministic coin tossing) and Chapter 3, Section 3.1 (list ranking by removing independent sets)
  - paper: doi:10.1007/BF01759076
    title: Richard J. Anderson and Gary L. Miller, Deterministic parallel list ranking, Algorithmica 6(6), 1991
    locator: pp. 859 to 868 (contraction with deterministically chosen independent sets in O(log n) time on the EREW PRAM)
  - book: isbn:9781107154889
    title: Michael Mitzenmacher and Eli Upfal, Probability and Computing, second edition
    locator: Chapter 4, Section 4.2 (the Chernoff bounds used for the high-probability statement)
---

List contraction is a parallel technique for [linked lists](/linked-list/): choose an [independent set](/independent-set/) of nodes (no two of them adjacent), splice each chosen node out of the list by linking its predecessor to its successor, fold the value of the chosen node into its predecessor, and recurse on the shorter list. When the recursion returns, each removed node computes its own result from its successor's result. With the random mate rule (each node flips a coin, and a node is removed when it flips heads and its successor flips tails) a round removes a quarter of the nodes in expectation, so $O(\log n)$ rounds with high probability and $O(n)$ expected work contract the whole list. It is the work-efficient core of [list ranking](/list-ranking/) and the COMPRESS step of [tree contraction](/tree-contraction/).

Notation on this page: $m$ is the number of live nodes in a round, $n$ the number at the start, $W$ the work and $S$ the span in the [work-span model](/work-span-model/). Probabilities are over the coins of the algorithm only; the input is arbitrary.

## In plain words

People stand in a line, and each person holds a card with a word. The goal is that each person learns the sentence from their own card to the end of the line.

Each person tosses a coin. A person leaves the line when they toss heads and the person behind them tosses tails. Two neighbours can never both leave, so nobody is confused about who is next. Before leaving, each person gives their word to the person in front of them, who writes it at the end of their own card, and remembers who stood behind them.

About one person in four leaves in each round, so the line gets short fast. When the short line has its answers, the people come back in the reverse order. Each one takes the answer of the person who was behind them and puts their own word in front.

## When it applies

- The input is a set of disjoint linked lists (or chains inside a bigger structure, such as the unary paths of a tree), and the result at each node is a sum along the list with an [associative operator](/associative-operator/).
- The removal of one node is a local change: it touches only the node and its two neighbours.
- You want $O(n)$ work. [Pointer jumping](/pointer-jumping/) is simpler, but it does $\Theta(n \log n)$ work, because it never makes the list shorter.

## The template

Each live node $i$ has $next[i]$, $prev[i]$ and a value $val[i]$, which is the $\oplus$-sum of the original values from $i$ up to, but not including, $next[i]$. At the start $val[i] = x_i$. The holes are the choice rule CHOOSE, the fold $\oplus$, and the base case.

```pseudo id=main
LIST-CONTRACT(L)                             ▷ L: the live nodes of a set of lists
L1  if L = ∅ then return                     ▷ BASE: or rank a small list directly
L2  for all i ∈ L in parallel: coin[i] ← a fair random bit
L3  R ← { i ∈ L : coin[i] = H and (next[i] = nil or coin[next[i]] = T) }      ▷ CHOOSE
L4  for all i ∈ R in parallel do             ▷ SPLICE
        p ← prev[i], q ← next[i]
        if p ≠ nil then val[p] ← val[p] ⊕ val[i], next[p] ← q
        if q ≠ nil then prev[q] ← p
L5  L′ ← L \ R                               ▷ a pack, by prefix sums
L6  LIST-CONTRACT(L′)
L7  for all i ∈ R in parallel do             ▷ EXPAND
        y[i] ← val[i] if next[i] = nil else val[i] ⊕ y[next[i]]
```

A removed node keeps its own $next[i]$ and $val[i]$ from the moment it left, because later rounds only change live nodes. Line L7 runs after the recursion, so $y[next[i]]$ is known: the successor of a removed node was live in that round, and it either stayed to the end or was removed in a later round and got its result before.

### Why it is correct

**Lemma 1 (independence).** If $i \in R$ then $next[i] \notin R$. *Proof.* If $next[i] = q \ne \mathit{nil}$, then $coin[q] = T$ by line L3, but each node in $R$ has $coin = H$. $\square$

So the splices of line L4 do not interfere: node $i$ writes only to $p = prev[i]$ and $q = next[i]$, which are live by Lemma 1; $p$ has only one successor, so only $i$ writes $val[p]$ and $next[p]$, and $q$ has only one predecessor, so only $i$ writes $prev[q]$. The splice keeps the meaning of $val$: after it, $val[p]$ covers the original nodes from $p$ up to $q$, because $val[p]$ covered $p$ up to $i$ and $val[i]$ covered $i$ up to $q$, and $\oplus$ is associative.

**Lemma 2 (expansion).** For each node $i$, $y[i] = val[i] \oplus y[next[i]]$ with the values at the time $i$ left, and this is the suffix sum of $i$. *Proof.* By induction on the rounds, from the last to the first. When $i$ leaves, $val[i]$ covers $i$ up to $q = next[i]$, and $y[q]$ is the suffix sum from $q$. So $val[i] \oplus y[q]$ covers $i$ to the tail. If $q = \mathit{nil}$, $val[i]$ already covers $i$ to the tail. $\square$

### Cost of one round

**Lemma 3 (expected size of R).** Let one round see $m$ live nodes in $t$ lists. Then $\mathbb{E}[|R|] = (m + t)/4 \ge m/4$.

*Proof.* A node with a successor is in $R$ when its coin is $H$ and its successor's coin is $T$: probability $1/4$. A tail is in $R$ when its coin is $H$: probability $1/2$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[|R|] = (m - t)/4 + t/2 = (m + t)/4$. $\square$

**Lemma 4 (high probability).** $\Pr[|R| < m/16] \le e^{-m/64}$.

*Proof.* In each list, take the nodes at even distance from the head: positions $0, 2, 4, \ldots$. There are at least $m/2$ of them. The event "$i \in R$" depends only on the coins of $i$ and $next[i]$, and these pairs are disjoint for nodes at even positions, so the events are independent. Let $X$ count them; $X \le |R|$ and $\mu = \mathbb{E}[X] \ge m/8$. The [Chernoff bound](/chernoff-bound/) $\Pr[X \le \mu/2] \le e^{-\mu/8}$ gives $\Pr[X < m/16] \le \Pr[X \le \mu/2] \le e^{-m/64}$. $\square$

### Cost of the whole contraction

Let $m_r$ be the number of live nodes at the start of round $r$, with $m_0 = n$. Lemma 3 gives $\mathbb{E}[m_{r+1} \mid m_r] \le \frac{3}{4} m_r$, so $\mathbb{E}[m_r] \le (3/4)^r n$.

- **Rounds.** Let $R^\ast$ be the number of rounds. Then $\Pr[R^\ast > r] = \Pr[m_r \ge 1] \le \mathbb{E}[m_r] \le (3/4)^r n$ by [Markov's inequality](/markov-inequality/). With $r_0 = \lceil \log_{4/3} n \rceil$, $\mathbb{E}[R^\ast] = \sum_{r \ge 0} \Pr[R^\ast > r] \le r_0 + \sum_{r \ge r_0} (3/4)^{r} n \le r_0 + 4 \le \log_{4/3} n + 5$. With $r = (1 + c) \log_{4/3} n$, $\Pr[R^\ast > r] \le n^{-c}$, so $R^\ast = O(\log n)$ with high probability. Here $\log_{4/3} n \approx 2.41 \log_2 n$.
- **Work.** A round costs $O(m_r)$ work, including the pack of line L5 by [prefix sums](/all-prefix-sums/), and the expansion costs $O(|R|)$. So $\mathbb{E}[W] = O(\sum_r \mathbb{E}[m_r]) = O(\sum_r (3/4)^r n) = O(n)$.
- **Span.** A round costs $O(1)$ span for lines L2 to L4 and L7, and $O(\log m_r)$ for the pack. So $S = O(\log^2 n)$ with high probability. Without the pack the span is $O(\log n)$ with high probability, but each round then costs $O(n)$ work over all the original slots.

## Classic examples

**One round.** Take the list $3 \to 0 \to 6 \to 2 \to 5 \to 1 \to 7 \to 4$ with the values $x = $ d, a, g, c, f, b, h, e in list order and $\oplus$ the concatenation of strings, which is associative but not commutative. Let the coins in list order be H, T, H, H, T, H, T, H. Line L3 removes 3 (next is T), 2 (next is T), 1 (next is T) and the tail 4, so $R = \{3, 2, 1, 4\}$; node 6 stays because its successor 2 flipped H. Node 3 is a head, so nothing is folded. Node 6 gets $val[6] = $ gc and $next[6] = 5$; node 5 gets fb and $next[5] = 7$; node 7 gets he and $next[7] = \mathit{nil}$. The new list is $0 \to 6 \to 5 \to 7$ with values a, gc, fb, he. When it returns with $y[0] = $ agcfbhe, $y[5] = $ fbhe and $y[7] = $ he, the expansion gives $y[3] = $ d $\oplus$ agcfbhe $=$ dagcfbhe, $y[2] = $ cfbhe, $y[1] = $ bhe and $y[4] = $ e.

- **[Parallel list ranking](/parallel-list-ranking/).** The template with $\oplus = +$ and $x_i = 1$ (0 at the tail). It is the randomized work-efficient list ranking algorithm.
- **The COMPRESS step of [tree contraction](/tree-contraction/).** The nodes of a tree with one child form chains, and COMPRESS is one round of list contraction on those chains. In [tree expression evaluation](/tree-expression-evaluation/) the fold is the composition of linear functions.
- **[Graph contraction](/graph-contraction/).** [Random mate contraction](/random-mate-contraction/) of a graph uses the same coin rule on the edges of a graph to merge a constant fraction of the vertices in each round.

## Variations

- **Deterministic choice.** [Deterministic coin tossing](/cole-vishkin/) colours a list with three colours in $O(\log^* n)$ rounds, and the nodes whose colour is larger than both neighbours' colours form an independent set with a constant fraction of the nodes. Cole and Vishkin and then Anderson and Miller use such sets for deterministic list ranking in $O(\log n)$ time with $O(n)$ work on the EREW PRAM.
- **Contract, then jump.** Contract until about $n / \log n$ nodes remain, then run [pointer jumping](/pointer-jumping/) on the small list: $O(n)$ work for the jumping, and fewer rounds than contracting to the end.
- **Remove a node only when the predecessor flips tails.** The mirror rule, $coin[i] = H$ and $coin[prev[i]] = T$, works the same way and folds the values into the successor instead.
- **Sparse ruling sets.** Instead of removing nodes one by one, choose about $n / k$ ruler nodes and let each ruler walk its sublist until the next ruler. This trades rounds for work per round and is common on GPUs.

## Pitfalls

- **A rule that is not independent.** The rule "remove each node with heads" can remove two neighbours $i$ and $next[i]$, and then the splice of $i$ links its predecessor to a node that is also leaving. Line L3 must look at the successor's coin.
- **Folding into the wrong side.** With a non-commutative operator, the fold into the predecessor is $val[p] \oplus val[i]$, not $val[i] \oplus val[p]$, and the expansion is $val[i] \oplus y[next[i]]$.
- **Forgetting the pack.** Without line L5, every round scans all $n$ slots, the work becomes $\Theta(n \log n)$ in expectation, and the method loses its point.
- **Changing a removed node.** The expansion needs $next[i]$ and $val[i]$ as they were when $i$ left. A program that keeps splicing pointers of removed nodes in later rounds breaks Lemma 2.

## Exercises

1. Show that on one list of $m$ nodes, $|R| \le \lceil m/2 \rceil$ in each round, and give coins that reach this.
2. For one list of $m$ nodes, show that $\mathbb{E}[m_{r+1} \mid m_r] = (3 m_r - 1)/4$ when $m_r \ge 1$.
3. Change the template to compute, for each node, the head of its list.

## References
