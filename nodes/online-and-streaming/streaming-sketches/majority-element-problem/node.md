---
tag: 9X4CH1
kind: problem
slug: majority-element-problem
name: Majority element problem
aliases:
- majority vote problem
- majority element
area: online-and-streaming/streaming-sketches
level: intro
summary: Find an item occurring more than half the time in a stream, if one exists, using one pass and constant memory.
prereqs: [streaming-model]
see_also: [boyer-moore-majority, frequent-items-problem, misra-gries-summary, index-problem-lower-bound, median-of-medians, frequency-vector]
sources:
  - paper: "Robert S. Boyer and J Strother Moore, MJRTY: a fast majority vote algorithm, in Robert S. Boyer (ed.), Automated Reasoning: Essays in Honor of Woody Bledsoe, Kluwer Academic Publishers, 1991, pages 105 to 117"
    locator: the majority vote problem and the two-pass algorithm
  - paper: doi:10.1016/0167-6423(82)90012-0
    title: Jayadev Misra and David Gries, Finding repeated elements, Science of Computer Programming 2(2), 1982
    locator: pages 143 to 152, the majority problem and its generalization to more than m/k occurrences
  - url: https://web.stanford.edu/class/cs168/l/l2.pdf
    title: Tim Roughgarden and Gregory Valiant, CS168 The Modern Algorithmic Toolbox, Lecture 2, Approximate heavy hitters and the count-min sketch, Stanford University
    locator: Section 1 (the majority problem in one pass) and Section 2 (the heavy hitters problem)
---

The majority element problem asks for the item that fills more than half of a sequence, or for the answer that there is none. With random access it is easy. In the [streaming model](/streaming-model/) it is the simplest problem where memory matters: two passes with a constant number of words solve it exactly, by the [Boyer-Moore majority vote](/boyer-moore-majority/), while one pass needs memory linear in the universe size to decide whether a majority exists.

## In plain words

You get a long list of votes, one name in each vote. You must say which name has more than half of all votes, or say that no name has. You may keep only a few numbers in memory, not a table of all names.

A name with more than half of the votes is special: if you cancel each of its votes against a vote for a different name, some of its votes are always left over. The well-known method uses this fact to find the only possible winner in one pass. A second pass counts that one name to check it. Without a second pass you cannot be sure, because a list with no winner can look the same as a list with one.

## Definition

The input is a stream $\sigma = a_1, \ldots, a_m$ of items from the universe $[n] = \{1, \ldots, n\}$. Let $f$ be the [frequency vector](/frequency-vector/): $f_x = |\{t : a_t = x\}|$. An item $x$ is a **majority** of $\sigma$ if
$$ f_x > \frac{m}{2}. $$
The output is the majority $x$ if one exists, and "none" otherwise. There is at most one majority, because two of them would have more than $m$ occurrences in total.

On this page $m$ is the stream length and $n$ is the universe size. Space is counted in bits unless the text says words; a word holds one item or one counter, so it has $O(\log n + \log m)$ bits.

## Variants

- **Decision.** Say only whether a majority exists.
- **Search with a promise.** A majority is known to exist; output it. One pass of the Boyer-Moore vote is then enough, because its candidate is the majority.
- **More than $m/k$ times.** Output all items with $f_x > m/k$. There are fewer than $k$ of them. This is the exact version of the [frequent items problem](/frequent-items-problem/).
- **Approximate majority.** Output each item with $f_x > m/2$, and maybe also items with $f_x > (1/2 - \varepsilon) m$. A [Misra-Gries summary](/misra-gries-summary/) solves it in one pass with $O(1/\varepsilon)$ words.
- **Plurality.** Output the most frequent item, the mode. This is much harder: it is the exact [frequency moment](/frequency-moment-problem/) $F_\infty$ question, and one pass needs $\Omega(n)$ bits even to approximate $\max_x f_x$ within a factor less than 2.
- **The Boolean majority function.** The [majority problem](/majority-problem/) of communication complexity is a different question: whether more than half of $n$ bits are 1.

## Examples

| stream $\sigma$ | $m$ | frequencies | answer |
|---|---|---|---|
| a, b, a, c, a, a, b, a | 8 | a: 5, b: 2, c: 1 | a |
| a, b, c, a, b, c | 6 | a: 2, b: 2, c: 2 | none |
| a, a, b, b | 4 | a: 2, b: 2 | none, since $2 \not> 2$ |
| a, a, b, b, c | 5 | a: 2, b: 2, c: 1 | none |
| 7 | 1 | 7: 1 | 7 |

The fourth row is the classic trap. One pass of the vote ends with candidate $c$ and a positive count, but $c$ is not a majority. Only the second pass shows that.

## Known algorithms

- **[Boyer-Moore majority vote](/boyer-moore-majority/).** One pass keeps a candidate and a counter: a new candidate when the counter is 0, plus one for a copy of the candidate, minus one for another item. A second pass counts the candidate. Time $\Theta(m)$, two words of memory, at most $2m - 1$ equality tests. This is the two-pass exact method.
- **[Misra-Gries summary](/misra-gries-summary/) with $k - 1$ counters.** The case $k = 2$ is the vote above. Larger $k$ finds all items with more than $m/k$ copies, again with a second pass.
- **Counting with a hash table.** One pass with a [frequency counter](/frequency-counter/) gives each $f_x$. It is exact and online, but it needs one entry for each distinct item, up to $\min(n, m)$ words.
- **Sorting or selection.** If the items have a total order, a majority is always the median, because it fills more than half of the positions of the sorted order. Find the median in $\Theta(m)$ time with [median of medians](/median-of-medians/), then count it. This needs random access, not a stream.
- **Random sampling.** If a majority exists, a random position holds it with probability more than $1/2$. Pick $t$ random positions and count each of their items. This finds the majority with probability more than $1 - 2^{-t}$, in $O(tm)$ time.

## Bounds

**Upper bounds.** Two passes and $O(\log n + \log m)$ bits suffice, by the Boyer-Moore vote. With the promise that a majority exists, one pass and the same space suffice. The time is $\Theta(m)$, which is optimal, since an algorithm that does not read some item can be fooled by a change of that item.

**One pass is not enough for the decision.** Each one-pass algorithm that decides whether a majority exists, with error probability at most $1/3$ on each input, uses $\Omega(n)$ bits of memory on streams of length at most $2n$. The proof is a reduction from the INDEX problem: Alice streams the positions of the ones of her bit string $x$, and Bob appends $|x|$ copies of his index $j$. The item $j$ is then a majority if and only if $x_j = 1$. The full argument, with the one-way [communication](/communication-complexity/) lower bound for INDEX, is on the [INDEX lower bound](/index-problem-lower-bound/) page. A deterministic one-pass algorithm needs $\Omega(n)$ bits by the same reduction.

## Reductions

- **To frequent items.** The majority problem is the frequent items problem with threshold $m/2$.
- **To the median.** With a total order on the items, the majority, if any, is the median of the sequence.
- **From INDEX.** As above, INDEX on $n$ bits reduces to the one-pass majority decision on a universe of size $n$, with one extra message of $\lceil \log_2(n+1) \rceil$ bits for the number $|x|$.

## Applications

- **Fault-tolerant voting.** Several replicas compute the same value, and the system accepts the value that a majority returns.
- **Dominant keys.** Find a key that fills more than half of a shard or of a log, for example a hot key in a cache, with a fixed amount of memory.
- **A building block.** The vote is the $k = 2$ case of the counter-based [heavy hitters](/frequent-items-problem/) summaries, which are used in network monitoring and in database query planning.

## References
