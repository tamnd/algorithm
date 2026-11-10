---
tag: FE4TJK
kind: algorithm
slug: boyer-moore-majority
name: Boyer-Moore majority vote algorithm
aliases:
- Boyer-Moore voting algorithm
- majority vote algorithm
- MJRTY
area: online-and-streaming/streaming-sketches
level: intro
summary: Keeps one candidate and a counter, finding a majority element in one pass with constant space.
solves: [majority-element-problem]
model: streaming-model
complexity:
  vars: {m: the stream length}
  time: {worst: Θ(m), average: Θ(m), best: Θ(m)}
  space: {extra: Θ(1)}
properties: {online: false, deterministic: true, comparison: true, recursive: false}
prereqs: [majority-element-problem, loop-invariant, streaming-model]
see_also: [misra-gries-summary, frequent-items-problem, space-saving, index-problem-lower-bound, majority-problem]
sources:
  - paper: "Robert S. Boyer and J Strother Moore, MJRTY: a fast majority vote algorithm, in Robert S. Boyer (ed.), Automated Reasoning: Essays in Honor of Woody Bledsoe, Kluwer Academic Publishers, 1991, pages 105 to 117"
    locator: the algorithm, its correctness argument, the bound of at most two comparisons for each vote, and the mechanically checked Fortran version
  - paper: "Robert S. Boyer and J Strother Moore, MJRTY: a fast majority vote algorithm, Technical Report ICSCA-CMP-32, Institute for Computing Science, University of Texas at Austin, 1981"
    locator: the first written version of the algorithm
  - paper: doi:10.1016/0167-6423(82)90012-0
    title: Jayadev Misra and David Gries, Finding repeated elements, Science of Computer Programming 2(2), 1982
    locator: pages 143 to 152, the generalization from the majority (more than m/2) to items that occur more than m/k times
---

The Boyer-Moore majority vote algorithm finds the item that occurs more than half of the time in a sequence, if there is one. It solves the [majority element problem](/majority-element-problem/) with two passes over the data, $\Theta(m)$ time for $m$ items, and only two words of memory: a candidate and a counter. The first pass is a [streaming](/streaming-model/) pass that needs only an equality test on items. The second pass checks the candidate, and it is necessary, because one pass with constant memory cannot tell whether a majority exists.

## In plain words

Think of an election where each vote names one person. You read the votes one at a time. You keep one name and one number in your head. When the number is zero, the next vote gives the new name and the number becomes one. A vote for the name in your head adds one. A vote for someone else takes one away.

Each time you take one away, you cancel two votes for two different people. A person who has more than half of all votes cannot lose all of their votes to such cancels, because each cancel also uses a vote of someone else. So that person is the name in your head at the end.

If nobody has more than half, the name at the end can be anyone. So you read the votes a second time and count that one name.

## The problem

The input is a sequence $\sigma = a_1, a_2, \ldots, a_m$ of items from a universe of size $n$. The items need only an equality test, not an order. Let $f_x$ be the number of indices $t$ with $a_t = x$. An item $x$ is a *majority* if $f_x > m/2$. There is at most one majority. The output is the majority, or "none". This is the [majority element problem](/majority-element-problem/), the case $k = 2$ of the [frequent items problem](/frequent-items-problem/).

## The algorithm

```pseudo id=main
MAJORITY-CANDIDATE(σ)                    ▷ one pass over a_1, ..., a_m
L1  candidate ← none, count ← 0
L2  for each item x of σ, in order do
L3      if count = 0 then
L4          candidate ← x, count ← 1
L5      else if x = candidate then
L6          count ← count + 1
L7      else
L8          count ← count − 1
L9  return (candidate, count)

MAJORITY(σ)                              ▷ second pass
L10 occ ← the number of t with a_t = candidate
L11 if 2 · occ > m then return candidate else return none
```

The counter is the number of copies of the candidate that are not yet cancelled. Line L8 cancels one copy of the candidate against the arriving item, which is a different item. Line L4 starts a new candidate when all earlier copies are cancelled. MAJORITY runs MAJORITY-CANDIDATE, then counts the candidate in a second pass over the same data.

## Example

Run the first pass on $\sigma = a, b, a, c, a, a, b, a$, so $m = 8$.

| $t$ | $a_t$ | line | candidate | count |
|---|---|---|---|---|
| 1 | a | L4 | a | 1 |
| 2 | b | L8 | a | 0 |
| 3 | a | L4 | a | 1 |
| 4 | c | L8 | a | 0 |
| 5 | a | L4 | a | 1 |
| 6 | a | L6 | a | 2 |
| 7 | b | L8 | a | 1 |
| 8 | a | L6 | a | 2 |

The candidate is $a$. The second pass counts $f_a = 5$, and $2 \cdot 5 > 8$, so $a$ is the majority.

The second pass matters. On $a, b, c, a, b, c$ the first pass ends with candidate $b$ and count $0$. On $a, a, b, b, c$ it ends with candidate $c$ and count $1$. In both cases the second pass finds that the candidate is not a majority, and the output is "none".

## Correctness

The key [loop invariant](/loop-invariant/) is a pairing. After $t$ items, the prefix $a_1, \ldots, a_t$ splits into $count$ copies of $candidate$ and $(t - count)/2$ pairs, where the two items of each pair are different. A majority $x$ of $\sigma$ has at most one copy in each pair, so at most $(m - count)/2 < m/2$ copies in the pairs. So some copy of $x$ is not in a pair, and the only items that are not in pairs are copies of the candidate. Hence the candidate is $x$. Line L11 then accepts it, and it rejects each candidate that is not a majority. The full proof is below.

## Complexity

- **Time.** Each item takes $O(1)$ steps in each pass, so the time is $\Theta(m)$ in every case.
- **Comparisons.** The first pass makes one equality test for each item that arrives when $count > 0$, so at most $m - 1$ tests. The second pass makes $m$ tests. The total is at most $2m - 1$.
- **Space.** One item and one counter of $\lceil \log_2(m+1) \rceil$ bits, so $\Theta(1)$ words in the [word RAM](/word-ram/) sense, and $O(\log n + \log m)$ bits.

One pass is not enough for the decision. Any one-pass algorithm that decides whether a majority exists, even with randomness and error $1/3$, needs $\Omega(n)$ bits on streams of length $2n$ over a universe of size $n$. The reduction from INDEX is on the [INDEX lower bound](/index-problem-lower-bound/) page.

## Properties

- **Not online as a whole.** The first pass is a one-pass streaming algorithm. The decision needs the second pass, so the data must be stored or replayed.
- **Deterministic.** There are no random choices.
- **Equality only.** The items need no order and no hash function. This is why the method works on any type with an equality test.
- **Not a frequency estimate.** The final count is not $f_x$. In the example the count is 2 and $f_a = 5$. The pairing below shows only that $count \ge 2 f_{candidate} - m$.

## Variants and improvements

- **More than $m/k$ times.** The [Misra-Gries summary](/misra-gries-summary/) keeps $k - 1$ candidates with counters. With $k = 2$ it is this algorithm. A second pass that counts the $k - 1$ candidates finds all items with $f_x > m/k$.
- **Counters that overestimate.** [Space-Saving](/space-saving/) with $k$ counters is the same summary seen from the other side: its counts are upper bounds.
- **Parallel and distributed runs.** Two (candidate, count) pairs merge: if the candidates are equal, add the counts; else keep the candidate with the larger count, and its count minus the smaller count. The pairing invariant holds for the concatenation, so the merged candidate is still correct. This is the $k = 2$ case of the merge of [mergeable summaries](/mergeable-summaries/).

## When to use it

Use it when you know or suspect that one value fills more than half of the data, and memory is tight: a vote count, a dominant key in a shard, the leader in a log of messages. If a second pass is not possible, use a [Misra-Gries summary](/misra-gries-summary/) and accept an approximate answer. If the items have a total order and the data is in memory, selection of the median also finds the majority, since a majority is always the median.

## Pitfalls

- **No second pass.** Returning the candidate of line L9 as the answer is wrong when there is no majority. On $a, a, b, b, c$ it returns $c$. Keep lines L10 and L11.
- **Testing $count > 0$ for the decision.** A positive final count does not show a majority, as $a, a, b, b, c$ shows. Only the count of line L10 decides.
- **Half is not a majority.** An item with exactly $m/2$ copies is not a majority. Line L11 uses $2 \cdot occ > m$, not $\ge$.
- **Using the count as the frequency.** The final count is not $f_{candidate}$. To report how often the majority occurs, use $occ$ of line L10.
- **Merging by adding counts.** When two partial runs with different candidates are merged, adding the counts is wrong. Subtract the smaller count from the larger one, and keep the candidate of the larger one.

## Implementations

## History

Robert S. Boyer and J Strother Moore wrote the algorithm up as a technical report of the University of Texas at Austin in 1981, and published it in 1991 under the name MJRTY, in a book of essays for Woody Bledsoe. The paper gives a Fortran version and a proof of it checked with their mechanical theorem prover. Misra and Gries generalized the method to $k - 1$ counters in 1982, and their summary became a base of the [frequent items](/frequent-items-problem/) algorithms for data streams.

## References
