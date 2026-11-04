---
tag: SBQ67V
kind: problem
slug: optimal-tape-storage
name: Storing files on tape
aliases:
- optimal storage on tapes
- optimal tape storage
area: techniques/greedy
level: intro
summary: Chooses the order of files on a tape to minimize average access cost, solved by a greedy rule that places shorter files first.
prereqs: [greedy-algorithm, exchange-argument]
see_also: [shortest-job-first, smith-rule, minimizing-weighted-completion-time, optimal-merge-pattern, greedy-choice-property, scheduling-notation]
sources:
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 4, The Greedy Method (optimal storage on tapes)
  - paper: doi:10.1002/nav.3800030106
    title: Wayne E. Smith, Various optimizers for single-stage production, Naval Research Logistics Quarterly 3(1-2), 1956
    locator: pages 59 to 66
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Problem 16-2, Scheduling to minimize average completion time
---

Optimal tape storage is the problem of ordering $n$ files on a tape so that the mean time to read a file is as small as possible, when reading a file means reading the tape from the start up to the end of that file. If every file is read equally often, storing the files in order of nondecreasing length is optimal. If file $i$ is read with frequency $f_i$, the order by nondecreasing ratio $L_i / f_i$ of length to frequency is optimal. The problem is [minimizing weighted completion time](/minimizing-weighted-completion-time/) on one machine with new names, and both rules cost one sort.

## In plain words

A tape can only be read from the start. To read a file, the drive starts at the beginning and runs past every file stored before it. So a file near the end is slow to read, and every file in front of it adds to the wait.

If all files are read equally often, put the short files first. A short file in front delays the others only a little. A long file in front would delay every file behind it a lot.

If some files are read much more often than others, length is not enough. A long file that is read all the time can deserve a place near the front. The right measure is the length of a file divided by how often it is read: smaller values go first.

## Definition

**Input.** Files $1, \ldots, n$ with lengths $L_i > 0$, and optionally access frequencies $f_i \ge 0$. Without frequencies, take $f_i = 1$.

**Cost.** An order $\pi$ stores file $\pi_1$ first, then $\pi_2$, and so on. Reading file $\pi_k$ costs
$$ t(\pi_k) = \sum_{l=1}^{k} L_{\pi_l}, $$
the length of the tape read up to its end. The goal is an order that minimizes the total weighted cost $\sum_i f_i\, t(i)$. With $F = \sum_i f_i > 0$, this is the same as minimizing the mean retrieval time $\frac{1}{F} \sum_i f_i\, t(i)$.

**Theorem.** An order is optimal if and only if $L_{\pi_1} / f_{\pi_1} \le L_{\pi_2} / f_{\pi_2} \le \cdots$, read as $L_a f_b \le L_b f_a$ for each pair of adjacent files $a$ before $b$. With equal frequencies, this is the order of nondecreasing length.

*Proof.* Let $a$ and $b$ be adjacent, $a$ first, and let $s$ be the tape length before them. Swapping them changes no other cost. Before the swap they cost $f_a (s + L_a) + f_b (s + L_a + L_b)$, and after it $f_b (s + L_b) + f_a (s + L_a + L_b)$. The difference, after minus before, is $f_a L_b - f_b L_a$. If an order has an adjacent pair with $L_a f_b > L_b f_a$, the swap lowers the cost, so the order is not optimal. Conversely, any two orders that satisfy the condition differ only in the order of files with equal ratios, which can be changed by adjacent swaps of cost difference 0, so they have the same cost. An optimal order exists and satisfies the condition, so every order that satisfies it is optimal. $\square$

This is the proof of [Smith's rule](/smith-rule/), with lengths as processing times and frequencies as weights.

## Variants

- **Equal frequencies.** Sort by length. This is [shortest job first](/shortest-job-first/) for the problem $1 \| \sum C_j$.
- **Frequencies.** Sort by $L_i / f_i$, smallest first. A file with $f_i = 0$ goes last.
- **Several tapes.** With $m$ tapes, each file goes on one tape and is read from the start of that tape. With equal frequencies, sort the files by length and deal them out in turn to tapes $1, 2, \ldots, m, 1, 2, \ldots$, so that the $k$-th shortest file goes on tape $((k - 1) \bmod m) + 1$. This is optimal: it is shortest job first on $m$ parallel machines, $P \| \sum C_j$. With frequencies and several tapes, the problem includes $P2 \| \sum w_j C_j$, which is NP-hard.
- **Seek and rewind costs.** Real drives can wind forward from the current position without a rewind. If the read requests come in a known sequence, the problem changes and the simple rules no longer apply.

## Examples

**Three files of equal frequency.** Lengths $A = 5$, $B = 10$, $C = 3$. The six orders have the total retrieval times below.

| order | retrieval times | total |
| --- | --- | --- |
| $A, B, C$ | 5, 15, 18 | 38 |
| $A, C, B$ | 5, 8, 18 | 31 |
| $B, A, C$ | 10, 15, 18 | 43 |
| $B, C, A$ | 10, 13, 18 | 41 |
| $C, A, B$ | 3, 8, 18 | 29 |
| $C, B, A$ | 3, 13, 18 | 34 |

The order by length, $C, A, B$, is best, with mean retrieval time $29 / 3$. The longest-first order $B, A, C$ is worst.

**Four files with frequencies.** $(L_i, f_i)$: $A = (8, 6)$, $B = (2, 1)$, $C = (5, 5)$, $D = (4, 2)$. The ratios $L_i / f_i$ are $4/3$, $2$, $1$ and $2$. The order $C, A, B, D$ costs $5 \cdot 5 + 6 \cdot 13 + 1 \cdot 15 + 2 \cdot 19 = 156$, and $C, A, D, B$, with the tie between $B$ and $D$ broken the other way, also costs 156. These two orders are the only optimal ones among the 24. Shortest first ($B, D, C, A$) costs 183, most frequent first ($A, C, D, B$) costs 166, and the worst order costs 193.

**Two tapes.** Lengths $2, 3, 4, 6, 7, 9, 12$ with equal frequencies. Dealing the sorted files in turn gives tape 1 with $2, 4, 7, 12$ (retrieval times $2, 6, 13, 25$) and tape 2 with $3, 6, 9$ (retrieval times $3, 9, 18$). The total is 76, the least over all ways to split and order the files. One tape in sorted order would cost 127.

## Known algorithms

- **Sort by length.** For equal frequencies. $O(n \log n)$ time.
- **Sort by ratio.** For frequencies, compare $L_a f_b$ with $L_b f_a$ to avoid division. $O(n \log n)$ time. This is [Smith's rule](/smith-rule/).
- **Sort and deal.** For $m$ tapes and equal frequencies, sort and assign round robin. $O(n \log n)$ time.

## Bounds

- **Upper bound.** $O(n \log n)$ time in the comparison model, by one sort.
- **Lower bound.** $\Omega(n \log n)$ comparisons to output an optimal order, because with distinct lengths the unique optimal order is the sorted order.
- **Value.** With equal frequencies and $L_1 \le \cdots \le L_n$, the optimal total is $\sum_{k=1}^{n} (n - k + 1) L_k$.

## Reductions

- **Same as weighted completion time.** Files are jobs, lengths are processing times, frequencies are weights, and the retrieval time of a file is the completion time of its job. So the problem is $1 \| \sum w_j C_j$, studied on the page [minimizing weighted completion time](/minimizing-weighted-completion-time/).
- **Contrast with merge patterns.** The [optimal merge pattern](/optimal-merge-pattern/) problem also charges each item for the operations it takes part in, but the cost structure is a tree, not a line, and its greedy rule is Huffman's.

## Applications

- **Sequential storage.** Tapes, and any medium read from the front, such as a linked list scanned from its head.
- **Self-organizing lists.** Ordering list items by access frequency, the case of equal lengths, is the static optimum that move-to-front and transpose heuristics try to approach.
- **Teaching.** A small and clear example of a greedy rule proved by an adjacent exchange.

## References
