---
tag: K5VMHF
kind: algorithm
slug: chang-lawler-algorithm
name: Chang-Lawler algorithm
aliases:
- Chang-Lawler sublinear matching
area: strings/approximate-matching
level: research
summary: Sublinear expected-time k-differences matching for patterns that are long relative to k.
solves: [k-differences-problem, approximate-string-matching]
model: word-ram
complexity:
  vars: {m: the pattern length, n: the text length, k: the error bound, σ: the alphabet size}
  time: {worst: O(m n), average: "O((n / m) (k + 1) log_σ m)"}
  space: {extra: O(m)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1990
  people: [William I. Chang, Eugene L. Lawler]
  note: Chang and Lawler presented the linear and sublinear expected time algorithms at FOCS 1990, with the journal version in Algorithmica in 1994, and introduced matching statistics for them.
prereqs: [k-differences-problem, sellers-algorithm, matching-statistics]
see_also: [suffix-automaton, suffix-tree, q-gram-filtering, pigeonhole-filtering, landau-vishkin-algorithm, ukkonen-cutoff-algorithm, wu-manber-approximate-matching, myers-bit-parallel-algorithm]
sources:
  - paper: "William I. Chang and Eugene L. Lawler, Sublinear approximate string matching and biological applications, Algorithmica 12(4-5), 1994, 327-344"
    locator: the LET and SET algorithms, matching statistics computed with the suffix tree of the pattern, and the expected time analysis for random text
  - paper: "William I. Chang and Eugene L. Lawler, Approximate string matching in sublinear expected time, Proceedings of the 31st IEEE Symposium on Foundations of Computer Science (FOCS), 1990"
    locator: the conference version of the two algorithms
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: the section on filtering algorithms (Chang and Lawler's LET and SET filters, their maximal match jumps and their average-case ranges)
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 7 (matching statistics with a suffix tree) and Chapter 12 (exclusion methods with fast expected time, including the method of Chang and Lawler)
---

The Chang-Lawler algorithm solves the [k-differences problem](/k-differences-problem/) by a filter that reads only part of the text. It cuts the text into blocks of length about $(m - k)/2$, where every match must contain a whole block. From the start of each block it makes $k + 1$ jumps over maximal pieces of the pattern, given by [matching statistics](/matching-statistics/). If the jumps stay inside the block, no match contains the block, and only the few remaining blocks get the [Sellers](/sellers-algorithm/) dynamic program. On random text with $k$ small compared with $m / \log m$, the expected time is $O((n/m)\, k \log_\sigma m)$, which is sublinear in $n$.

## In plain words

Any match of the pattern is long: at least the pattern length minus the allowed number of errors. So it covers a whole block, if the text is cut into blocks of half that length.

Now take a block and read it from its start. Find the longest piece that occurs somewhere in the pattern, then step over one more letter and do it again. Each such piece with its extra letter does not occur in the pattern, so a match that covers it must spend an error inside it. If one more piece than the number of allowed errors fits inside the block, a match cannot cover the block.

In random text the pieces are short, so this test reads a small part of each block and rules out most blocks. The slow exact method runs only near the blocks that remain.

## The problem

The input is a pattern $P = P[0 \ldots m-1]$, a text $T = T[0 \ldots n-1]$ over an alphabet of size $\sigma$, and an integer $k \ge 0$. Indices are 0-based. The edit model is Levenshtein: insertions, deletions and substitutions of single symbols, each of cost 1, with no transpositions, and $\mathrm{ed}$ is the distance. The output is the sorted list of **end positions** $j \in \{0, \ldots, n\}$ such that $\mathrm{ed}(P, T[h \ldots j)) \le k$ for some $h \le j$.

**Matching statistics.** For $0 \le p < n$, $ms(p)$ is the length of the longest prefix of $T[p \ldots n)$ that is a substring of $P$. If $p + ms(p) < n$, the **piece** $T[p \ldots p + ms(p)]$, of length $ms(p) + 1$, is not a substring of $P$, by the maximality of $ms(p)$. With a [suffix automaton](/suffix-automaton/) or a [suffix tree](/suffix-tree/) of $P$, $ms(p)$ is computed in $O(ms(p) + 1)$ time by reading the text from $p$.

**Blocks.** Let $b = \lfloor (m - k)/2 \rfloor$ and, when $b \ge 1$, let block $t$ be $T[tb \ldots tb + b)$ for $0 \le t < \lfloor n / b \rfloor$. Every substring $A$ with $\mathrm{ed}(P, A) \le k$ has $m - k \le |A| \le m + k$, so it is at least $2b$ long and contains a whole block.

## The algorithm

```pseudo id=main
CHANG-LAWLER-SET(P, T, k)
L1  if m − k < 2 then return SELLERS(P, T, k)
L2  b ← ⌊(m − k)/2⌋, build the suffix automaton of P
L3  for t ← 0 to ⌊n/b⌋ − 1 do
L4      p ← tb; repeat k + 1 times while p < (t + 1)b: p ← p + ms(p) + 1
L5      block t is live if the loop stopped early or p > (t + 1)b
L6      if block t is live then W ← [max(0, (t + 1)b − m − k), min(n, tb + m + k))
L7      merge W into the previous window if they overlap, else start a new window
L8  for each window [lo, hi): add lo to each end position of SELLERS(P, T[lo … hi), k)
L9  return the sorted end positions
```

Line L4 makes the jumps $p_0 = tb$ and $p_{r+1} = p_r + ms(p_r) + 1$. Line L5 calls the block **dead** when $p_{k+1} \le (t + 1)b$: then the $k + 1$ pieces between $p_0$ and $p_{k+1}$ lie inside the block. If some $p_r$ with $r \le k$ reaches the end of the block, then $p_{k+1}$ is beyond it, and the block is live. The window of line L6 holds every substring of length at most $m + k$ that contains block $t$.

## Example

Let $P = \texttt{GATTACAGAT}$ ($m = 10$), $k = 1$, and

$$ T = \texttt{CCTCCGGTGCTGAAGTCCGGGATTTCAGATGCGCTGTGCT} \quad (n = 40). $$

Then $b = \lfloor 9 / 2 \rfloor = 4$, and there are 10 blocks. Each row lists the $k + 1 = 2$ pieces from the start of the block.

| block $t$ | text | pieces from $4t$ | $p_2$ | result |
|---|---|---|---|---|
| 0 | CCTC | CC, TC | 4 | dead |
| 1 | CGGT | CG, GT | 8 | dead |
| 2 | GCTG | GC, TG | 12 | dead |
| 3 | AAGT | AA, GT | 16 | dead |
| 4 | CCGG | CC, GG | 20 | dead |
| 5 | GATT | GATTT, which leaves the block | | live |
| 6 | TCAG | TC, AGATG | 31 | live |
| 7 | ATGC | ATG, CG | 33 | live |
| 8 | GCTG | GC, TG | 36 | dead |
| 9 | TGCT | TG, CT | 40 | dead |

For block 0, $ms(0) = 1$: C occurs in $P$ but CC does not, so the first piece is CC and $p_1 = 2$; the second piece is TC and $p_2 = 4$, which is the end of the block. The windows of blocks 5, 6 and 7 are $[13, 31)$, $[17, 35)$ and $[21, 39)$, which merge into $[13, 39)$. Sellers' program on these 26 columns finds the single end position $30$: the substring $T[20 \ldots 30) = \texttt{GATTTCAGAT}$ is one substitution away from $P$. The dynamic program skips 14 of the 40 columns.

## Correctness

The output is a subset of the true answer, because each window is a substring of $T$ and Sellers' program reports only real matches. For the converse, take a match $A = T[h \ldots j)$ with $\mathrm{ed}(P, A) \le k$. It contains a whole block $t$. Fix an optimal alignment of $P$ with $A$. A piece that lies inside $A$ and contains no error of the alignment would be matched symbol by symbol to a substring of $P$, which is impossible, so each such piece holds an error. The pieces are disjoint and there are at most $k$ errors, so $A$ contains at most $k$ whole pieces. If block $t$ were dead, $A$ would contain the $k + 1$ pieces of the block. So block $t$ is live, $A$ lies in its window, and Sellers' program reports $j$. The [full proof](proofs/correctness.md) gives the details, including what "an error inside a piece" means for a deletion.

## Complexity

- **Worst case.** Each jump of line L4 costs $O(ms(p) + 1)$ time, so a block costs $O(b + m)$, and all jumps cost $O(n m / b)$. The merged windows are disjoint, so Sellers' program costs $O(m n)$ in total. With the suffix automaton, which has $O(m)$ states and transitions, the worst case is $O(mn)$ time, no worse than Sellers' algorithm alone, and the extra space is $O(m)$.
- **Expected jumps.** Let $T$ be uniformly random over $\sigma \ge 2$ symbols, with $P$ fixed. By the union bound over the at most $m$ positions of $P$, a fixed text position starts a substring of $P$ of length $L$ with probability at most $m \sigma^{-L}$. So $E[ms(p)] \le \sum_{L \ge 1} \min(1, m \sigma^{-L}) \le \lceil \log_\sigma m \rceil + 1/(\sigma - 1)$. Each jump reads the text only up to the symbol before the next start, so the jumps of a block see fresh random symbols, and a block costs $O((k + 1)(\log_\sigma m + 1))$ expected time. When $k \le m/3$ and $m \ge 6$, $b \ge m/6$, so over the $\lfloor n/b \rfloor$ blocks this is $O((n/m)(k + 1)(\log_\sigma m + 1))$.
- **Expected dynamic program.** A block is live only if its $k + 1$ pieces have total length above $b$. Chang and Lawler show that for $k$ below a bound of order $m / \log_\sigma m$ this is rare enough that Sellers' program adds no more than the jumps in expectation, which gives the sublinear bound $O((n/m)\, k \log_\sigma m)$.

## Properties

- **A filter with an exact check.** It never misses a match, and the dynamic program removes the false alarms.
- **Sublinear on average.** For small $k$ it does not read most of the text, like the Boyer-Moore method for exact matching.
- **Pattern index only.** It needs a suffix automaton or a suffix tree of the pattern, not of the text.
- **Works for any $k$.** Once $k + 1$ pieces of typical length $\log_\sigma m$ no longer fit in a block, that is, for $k$ of order $m / \log_\sigma m$, most blocks become live, and the time grows to that of Sellers' program.

## Variants and improvements

- **LET (linear expected time).** Cut the whole text into consecutive pieces $p_{r+1} = p_r + ms(p_r) + 1$ from $p_0 = 0$. A match contains at most $k$ whole pieces, so it lies within $k + 2$ consecutive pieces. When $k + 2$ consecutive pieces are shorter than $m - k$ in total, no match starts in the first of them. The dynamic program runs only on the other stretches. Every text symbol is read once, and the expected time is $O(n)$ for $k$ of order $m / \log_\sigma m$.
- **Other partitions.** The [pigeonhole filter](/pigeonhole-filtering/) splits the pattern into $k + 1$ pieces and searches for them exactly, and the [q-gram filter](/q-gram-filtering/) counts shared q-grams. Both also give sublinear average time with a fast exact matcher.
- **Faster checks.** The verification can use [Ukkonen's cutoff](/ukkonen-cutoff-algorithm/), [Landau-Vishkin](/landau-vishkin-algorithm/) or [Myers' bit-parallel algorithm](/myers-bit-parallel-algorithm/) in place of the full dynamic program.

## When to use it

Use it for long patterns with a low error rate in large texts that look random, for example a DNA or protein sequence searched with a few percent of errors. It needs only an index of the pattern. For high error rates or texts with long repeats of the pattern, use a method with a good worst case, such as [Myers' algorithm](/myers-bit-parallel-algorithm/), or an index of the text.

## Pitfalls

- **Short patterns.** When $m - k < 2$, the block length is 0 and the filter does not apply; run the dynamic program directly.
- **The last jump.** A piece that reaches the end of the text is a substring of $P$, not a non-substring. The test is safe only because such a jump puts $p$ beyond the block.
- **Window bounds.** The window must reach $m + k$ symbols on each side of the block, not $m$, since a match can be $m + k$ long.
- **Average, not worst case.** On periodic or repetitive text, such as runs of one symbol that occur in $P$, almost every block is live and the time is $\Theta(mn)$.

## Implementations

## History

Chang and Lawler presented the LET and SET algorithms at FOCS 1990 and in the journal Algorithmica in 1994. They introduced matching statistics, computed with the suffix tree of the pattern, for this purpose. Their analysis showed that approximate matching can run in sublinear expected time when $k$ is small compared with $m / \log m$. Later filters, surveyed by Navarro, use the same plan of a fast test followed by a dynamic program near the surviving text.

## References
