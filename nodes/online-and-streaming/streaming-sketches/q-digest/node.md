---
tag: A0RJGY
kind: data-structure
slug: q-digest
name: q-digest
aliases:
- quantile digest
- Q-Digest
area: online-and-streaming/streaming-sketches
level: core
summary: Deterministic mergeable quantile summary for integers in [0, U) that stores counts on dyadic intervals, with rank error at most εn in O((1/ε) log U) nodes.
model: word-ram
complexity:
  vars: {n: the stream length, U: the universe size, ε: the rank accuracy, k: "the compression parameter, ⌈log2 U/ε⌉", L: "log2 U"}
  time: {worst: O(k log k)}
  space: {extra: O(k)}
properties: {online: true, deterministic: true, mergeable: true}
history:
  year: 2004
  people: [Nisheeth Shrivastava, Chiranjeeb Buragohain, Divyakant Agrawal, Subhash Suri]
  note: The q-digest was designed for medians and other quantiles in sensor networks, where nodes merge the digests of their children. Scala (2024) showed that the size lemma of the paper is wrong as stated and proved a bound of 4k + 1 nodes.
prereqs: [dyadic-intervals, quantile-summary-problem, trie]
see_also: [greenwald-khanna-summary, kll-sketch, t-digest, count-min-sketch, mergeable-summaries, segment-tree, linear-sketch]
sources:
  - paper: doi:10.1145/1031495.1031524
    title: Nisheeth Shrivastava, Chiranjeeb Buragohain, Divyakant Agrawal and Subhash Suri, Medians and beyond, new aggregation techniques for sensor networks, SenSys 2004
    locator: pp. 239 to 249, Section 3 (the q-digest, its two properties, COMPRESS, merging, and the error bound log U times n/k)
  - url: https://arxiv.org/abs/2401.10118
    title: Mauro Scala, Techniques for authenticating quantile digests, 2024
    locator: the section on the size of a q-digest (a counterexample to the bound |Q| < 3k and the proof of |Q| ≤ 4k + 1)
  - paper: doi:10.1145/2213556.2213562
    title: Pankaj K. Agarwal, Graham Cormode, Zengfeng Huang, Jeff M. Phillips, Zhewei Wei and Ke Yi, Mergeable summaries, PODS 2012
    locator: the section on quantiles (the q-digest is mergeable)
  - book: isbn:9781108477444
    title: Graham Cormode and Ke Yi, Small Summaries for Big Data, Cambridge University Press, 2020
    locator: Chapter 4, Section 4.1, Q-Digest
---

The q-digest is a deterministic summary of a stream of integers from $[0, U)$ that answers rank and quantile queries with an error of at most $\varepsilon n$. It keeps counts on a small set of [dyadic intervals](/dyadic-intervals/), the nodes of the complete binary tree over the universe, and it pushes counts up the tree whenever a node, its sibling and its parent together hold few items. With compression parameter $k = \lceil \log_2 U / \varepsilon \rceil$ it keeps at most $4k$ nodes, so $O((1/\varepsilon)\log U)$ words. Two q-digests with the same parameters merge into a q-digest of the union with the same guarantee. On this page $n$ is the stream length, $U = 2^L$ is the size of the universe, and the stream $\sigma$ is insertion only.

## In plain words

Picture the numbers 0 to $U - 1$ at the leaves of a binary tree. Each inner node stands for a block of neighboring numbers. The q-digest keeps a count at some of the nodes. A new number adds 1 at its leaf. When a node, its sibling and their parent hold only a few items together, the digest moves the two counts up into the parent. Then the digest knows only that those items lie somewhere in the parent's block. Big blocks never hold many items, so for any number the uncertain items are few. Popular numbers keep their own leaves and exact counts, and rare ones are lumped together.

## The abstract type

The q-digest solves the [quantile summary problem](/quantile-summary-problem/) for integer items, with the operations:

- **Insert(x)** for $0 \le x < U$.
- **Rank(x)** returns $\hat R(x)$ with $R(x) - \varepsilon n \le \hat R(x) \le R(x)$, where $R(x)$ is the number of items at most $x$.
- **Query(r)** returns a value $x$ with $R(x) \ge r$ and $R(x - 1) < r + \varepsilon n$. If $x$ occurs in the stream, some copy of $x$ is at a position in $[r, r + \varepsilon n]$.
- **Merge(Q₁, Q₂)** returns a q-digest of the two streams together.

It is not comparison-based: it uses the binary digits of the items. So it is not bound by the comparison lower bound $\Omega((1/\varepsilon)\log(\varepsilon n))$ of the [GK summary](/greenwald-khanna-summary/) page.

## Representation

A node $v = (j, i)$ at level $j$ is the dyadic interval $[i 2^j, (i + 1)2^j - 1]$. Level 0 has the leaves, and level $L$ has the root $[0, U - 1]$. The digest $Q$ is a map from nodes to positive counts $c(v)$, with $c(v) = 0$ for the nodes not in $Q$. Each item is counted at exactly one node, and that node contains the item, so $\sum_v c(v) = n$. With the compression parameter $k$, the digest keeps:

- **Property 1.** $c(v) \le \lfloor n/k \rfloor$ for each node $v$ that is not a leaf.
- **Property 2.** After a compress, $c(v) + c(\mathrm{sibling}(v)) + c(\mathrm{parent}(v)) > \lfloor n/k \rfloor$ for each node $v \in Q$ other than the root.

Property 1 bounds the error, and Property 2 bounds the size. The pair (level, index) of a node is one word, so each node takes two words.

## Operations

```pseudo id=main
QD-INSERT(Q, x)
L1  n ← n + 1; c(leaf x) ← c(leaf x) + 1
L2  if |Q| > 4k then QD-COMPRESS(Q)

QD-COMPRESS(Q)
L3  repeat
L4      for j ← 0 to L − 1, for each node v of level j in Q, from left to right do
L5          if c(v) + c(sibling(v)) + c(parent(v)) ≤ ⌊n/k⌋ then
L6              c(parent(v)) ← c(v) + c(sibling(v)) + c(parent(v)); remove v and sibling(v)
L7  until a full pass makes no change

QD-QUERY(Q, r)
L8  sort the nodes by right end; among equal right ends, smaller levels first
L9  s ← 0; for each node v in this order: s ← s + c(v); if s ≥ r then return the right end of v

QD-MERGE(Q₁, Q₂)
L10 for each node v: c(v) ← c₁(v) + c₂(v); n ← n₁ + n₂
L11 QD-COMPRESS(Q)
```

Rank($x$) is the sum of $c(v)$ over the nodes whose right end is at most $x$. Line L9 returns the smallest $x$ with $\mathrm{Rank}(x) \ge r$. Each merge of line L6 moves counts up one level, so the sum of $c(v)$ times the height of $v$ above the leaves goes up at each merge and is at most $nL$. So the loop of lines L3 to L7 ends.

The original paper runs one bottom-up pass. Lines L3 to L7 repeat the pass until no merge applies, which makes Property 2 hold for every node; a single pass can leave a node whose parent was later merged away.

## Example

Take $L = 3$, so $U = 8$, and $k = 5$. The stream is 1, 6, 3, 3, 0, 7, 3, 5, 3, 2, 6, 4, 3, 1, 7, 3, so $n = 16$ and $\lfloor n/k \rfloor = 3$. For the example we run one compress at the end. Before it, the leaves hold the counts 0:1, 1:2, 2:1, 3:6, 4:1, 5:1, 6:2, 7:2.

| step | node and family | sum | action |
|---|---|---|---|
| level 0 | leaf 0, sibling 1, parent [0,1] | 1 + 2 + 0 = 3 | merge into [0,1] with count 3 |
| level 0 | leaf 2, sibling 3 | 1 + 6 = 7 | keep |
| level 0 | leaf 4, sibling 5 | 1 + 1 = 2 | merge into [4,5] with count 2 |
| level 0 | leaf 6, sibling 7 | 2 + 2 = 4 | keep |
| level 1 | [0,1], sibling [2,3] absent | 3 + 0 + 0 = 3 | merge into [0,3] with count 3 |
| level 1 | [4,5], sibling [6,7] absent | 2 + 0 + 0 = 2 | merge into [4,7] with count 2 |
| level 2 | [0,3], sibling [4,7] | 3 + 2 = 5 | keep |

A second pass changes nothing, so the digest is {2: 1, 3: 6, 6: 2, 7: 2, [0,3]: 3, [4,7]: 2}, six nodes. Leaf 3, the popular value, keeps its exact count.

The estimated ranks for $x = 0, \ldots, 7$ are 0, 0, 1, 10, 10, 10, 12, 16, and the true ranks are 1, 3, 4, 10, 11, 12, 14, 16. The largest error is 3, at $x = 1$, within the bound $L\lfloor n/k \rfloor = 9$. For Query(8), line L8 orders the nodes as 2, 3, [0,3], 6, 7, [4,7], and the running sums are 1, 7, 10. The sum first reaches 8 at [0,3], so the answer is 3. The copies of 3 are at the positions 5 to 10, which contain 8.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). The key facts are these. Property 1 holds always: inserts change only leaves, line L6 sets a count to at most $\lfloor n/k \rfloor$, $n$ never goes down, and in a merge $\lfloor n_1/k \rfloor + \lfloor n_2/k \rfloor \le \lfloor (n_1 + n_2)/k \rfloor$. For a value $x$, the items at most $x$ that Rank($x$) misses are counted at nodes that contain $x$ and end after $x$. These are proper ancestors of the leaf $x$, at most one at each level from 1 to $L$, and by Property 1 each holds at most $\lfloor n/k \rfloor$ items. So $0 \le R(x) - \hat R(x) \le L\lfloor n/k \rfloor \le \varepsilon n$ when $k \ge L/\varepsilon$. The quantile bound follows from the rank bound at $x$ and at $x - 1$.

**Size.** After a compress, Property 2 holds for every node of $Q$ other than the root. Sum it over these nodes. Each count $c(u)$ appears at most four times in the sum: once for $u$ itself, once as the sibling of its sibling, and at most twice as the parent of its two children. Each term of the sum is an integer above $\lfloor n/k \rfloor$, so at least $\lfloor n/k \rfloor + 1 > n/k$. So $(|Q| - 1)\,n/k < 4n$, and $|Q| \le 4k$. The paper states $|Q| < 3k$ (its Lemma 1). Scala (2024) gave a counterexample with $U = 64$, $n = 22$ and $k = 4$, where the digest has 13 nodes, and proved $|Q| \le 4k + 1$ for the algorithm of the paper.

## Complexity

**Space.** At most $4k$ nodes after each compress and $4k + 1$ between compresses, two words each, plus $n$. With $k = \lceil \log_2 U/\varepsilon \rceil$ this is $O((1/\varepsilon)\log U)$ words. The structure needs no knowledge of $n$.

**Time.** An insert is $O(1)$ with a hash map, plus a compress when $|Q| > 4k$. One pass of the compress sorts the nodes of each level, $O(k\log k)$ in all. The potential argument above bounds the number of passes only by $nL + 1$; we know no better bound for the repeated pass, but in 300 seeded runs with $L$ up to 10 the loop never needed more than 5 passes, the last one without a merge. The single bottom-up pass of the paper takes $O(k\log k)$ time. A query sorts the nodes, $O(k\log k)$, or $O(k)$ if the order is kept. A merge costs $O(k)$ plus a compress.

**Guarantees in the cost model.** The error $\varepsilon n$ is deterministic, so $\delta = 0$, and there are no random seeds. The model is insertion only; deletions would break Property 1, since a count above can no longer be bounded by $\lfloor n/k \rfloor$ after $n$ goes down.

## Variants

- **Fixed $U$ versus growing $U$.** If the universe is not known, start with a small tree and double it when a larger item arrives; the old root becomes a child of the new root.
- **Turnstile streams.** Use one [Count-Min sketch](/count-min-sketch/) per level of the dyadic tree instead, as on the [dyadic intervals](/dyadic-intervals/) page.
- **Comparison-based summaries.** The [GK summary](/greenwald-khanna-summary/) uses $O((1/\varepsilon)\log(\varepsilon n))$ items for any ordered type. The [KLL sketch](/kll-sketch/) uses fewer items but is randomized.
- **Other queries.** In the paper, the same digest answers inverse quantiles, range counts and consensus queries over a sensor network.

## When to use it

Use the q-digest when the items are integers from a known range, such as latencies in microseconds or IP addresses, when summaries must be merged (from sensors, shards or time buckets), and when you want a deterministic guarantee. For floating-point data, map the values to integers first, or use a comparison-based summary. When $\log U$ is much larger than $\log(\varepsilon n)$, the GK summary or the KLL sketch is smaller.

## Pitfalls

- **The size bound.** The bound $3k$ from the paper is false. Allocate for $4k + 1$ nodes.
- **The order in a query.** Among nodes that end at the same value, process the smaller ones first. All of them end at $x$, so the order does not change the answer, but a wrong key (for example by left end) does.
- **The guarantee is one-sided.** Rank($x$) never overestimates. The value from Query($r$) is at a position at or above $r$, not centered on it.
- **Deletions.** The q-digest does not support them.
- **Choosing $k$.** The error is $L\lfloor n/k \rfloor$, so $k$ must grow with $\log U$. With $U = 2^{32}$ and $\varepsilon = 0.01$, $k = 3200$ and up to 12800 nodes.

## Implementations

## History

Shrivastava, Buragohain, Agrawal and Suri introduced the q-digest at SenSys 2004 for sensor networks, where each sensor merges the digests of its children and sends one small message. Agarwal et al. (2012) listed it as a deterministic mergeable summary in their study of [mergeable summaries](/mergeable-summaries/). Scala (2024) corrected the size lemma.

## References
