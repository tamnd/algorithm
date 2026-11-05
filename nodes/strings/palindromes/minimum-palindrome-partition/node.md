---
tag: 7RF17S
kind: problem
slug: minimum-palindrome-partition
name: Minimum palindrome partition
aliases:
- minimum palindromic factorization
- palindromic length
- minimum cuts for palindrome partitioning
area: strings/palindromes
level: core
summary: Find the fewest palindromic pieces into which a string can be split.
model: comparison-model
complexity:
  vars: {n: the length of the string}
  time: {worst: Θ(n)}
  space: {aux: O(n)}
prereqs: [palindrome, palindrome-partitioning]
see_also: [palindrome-partition-dp, palindrome-partition-backtracking, series-links, palindromic-tree, manacher, palindrome-edit-distance, text-segmentation, dag-dynamic-programming]
sources:
  - paper: doi:10.1016/j.jda.2014.08.001
    title: Gabriele Fici, Travis Gagie, Juha Kärkkäinen and Dominik Kempa, A subquadratic algorithm for minimum palindromic factorization, Journal of Discrete Algorithms 28 (2014), 41-48
    locator: the problem statement and the O(n log n) algorithm that groups the palindromic suffixes of each prefix into O(log n) arithmetic progressions
  - paper: doi:10.1007/978-3-319-07566-2_16
    title: Tomohiro I, Shiho Sugimoto, Shunsuke Inenaga, Hideo Bannai and Masayuki Takeda, Computing palindromic factorizations and palindromic covers on-line, CPM 2014, Lecture Notes in Computer Science 8486, 150-161
    locator: the on-line O(n log n) computation of a minimum palindromic factorization, and the smallest palindromic cover
  - paper: doi:10.1016/j.ejc.2017.07.021
    title: Mikhail Rubinchik and Arseny M. Shur, EERTREE, an efficient data structure for processing palindromes in strings, European Journal of Combinatorics 68 (2018), 249-265
    locator: the section on palindromic factorization (series links in the eertree and the O(n log n) computation of the palindromic length of each prefix)
  - paper: doi:10.4230/LIPIcs.CPM.2017.23
    title: Kirill Borozdin, Dmitry Kosolobov, Mikhail Rubinchik and Arseny M. Shur, Palindromic length in linear time, CPM 2017, LIPIcs 78, 23:1-23:12
    locator: the main theorem (the palindromic length of a string, and of each prefix on-line, in O(n) time)
  - paper: doi:10.1145/322047.322056
    title: Zvi Galil and Joel Seiferas, A linear-time on-line recognition algorithm for Palstar, Journal of the ACM 25(1) (1978), 102-111
    locator: the whole paper (on-line recognition of concatenations of even palindromes)
---

The minimum palindrome partition problem asks for the least number of [palindromes](/palindrome/) whose concatenation is a given string $s$. This number is the *palindromic length* $\mathrm{PL}(s)$, and $\mathrm{PL}(s) - 1$ is the minimum number of cuts. A [dynamic program](/palindrome-partition-dp/) over prefixes solves it in $\Theta(n^2)$ time, [series links](/series-links/) in the [palindromic tree](/palindromic-tree/) bring this down to $O(n \log n)$, and Borozdin, Kosolobov, Rubinchik and Shur (2017) reach $O(n)$. It is the optimization form of [palindrome partitioning](/palindrome-partitioning/).

## In plain words

You want to cut a word into as few pieces as you can, so that each piece reads the same from both ends. Single letters always work, so the answer is never more than the length of the word. A word that is itself a palindrome needs one piece and no cut. Taking the longest palindrome at the start each time does not always give the best result, so a method must compare choices. The usual method goes from left to right and keeps the best answer for each start of the word. The last piece of a best split ends at the current letter, so the best answer is one more than the best answer just before some palindrome that ends there.

## Definition

**Input.** A string $s = s[0..n-1]$ over an [alphabet](/alphabet/) $\Sigma$, $n \ge 0$, with 0-based indices; $s[j..i]$ includes both ends. Algorithms test symbols for equality only, except where a method says that it uses an ordered or integer alphabet.

**Output.** The palindromic length
$$ \mathrm{PL}(s) = \min\{k : s = p_1 p_2 \cdots p_k,\ \text{each } p_t \text{ a nonempty palindrome}\}, $$
and, if asked, one partition with $\mathrm{PL}(s)$ pieces. The pieces may be odd or even palindromes, and $\mathrm{PL}(\varepsilon) = 0$. The *minimum cut* form asks for $\mathrm{PL}(s) - 1$ when $n \ge 1$.

**Prefix recurrence.** With $\mathrm{PL}_i = \mathrm{PL}(s[0..i-1])$,
$$ \mathrm{PL}_0 = 0, \qquad \mathrm{PL}_{i+1} = \min\{\mathrm{PL}_j + 1 : 0 \le j \le i,\ s[j..i] \text{ is a palindrome}\}. $$
The last piece of a best partition of $s[0..i]$ is a palindromic suffix $s[j..i]$, and the pieces before it form a best partition of $s[0..j-1]$.

## Variants

- **Each prefix, online.** Report $\mathrm{PL}$ of each prefix after each new symbol. The quadratic dynamic program, the series-link method and the linear method of Borozdin et al. are all online.
- **Exactly $k$ pieces.** Decide whether $s$ is a concatenation of $k$ palindromes, for a fixed $k$. Rubinchik and Shur (2020) decide this online in linear time; see [palindrome partitioning](/palindrome-partitioning/).
- **Even palindromes only.** The concatenations of even palindromes of length at least 2 form the language Palstar, which Galil and Seiferas (1978) recognize online in linear time. With the same prefix recurrence restricted to even pieces, the minimum is $\infty$ when no partition exists.
- **Palindromic cover.** Cover $s$ by the fewest maximal palindromes, which may overlap. I, Sugimoto, Inenaga, Bannai and Takeda (2014) compute it in $O(n)$ time.
- **Distance to a palindrome.** Editing $s$ into one palindrome, instead of cutting it into many, is [palindrome edit distance](/palindrome-edit-distance/).
- **Weighted pieces.** A cost per piece, such as a cost that depends on its length, keeps the prefix recurrence with $\mathrm{cost}(s[j..i])$ in place of 1, but not the series-link speedup in general.

## Examples

| $s$ | $\mathrm{PL}(s)$ | a best partition | pieces by the greedy longest prefix |
| --- | --- | --- | --- |
| $\varepsilon$ | 0 | none | 0 |
| `abc` | 3 | a, b, c | 3 |
| `aab` | 2 | aa, b | 2 |
| `aaba` | 2 | a, aba | 3 (aa, b, a) |
| `abaab` | 2 | a, baab | 3 (aba, a, b) |
| `banana` | 2 | b, anana | 2 |
| `abbaab` | 3 | a, b, baab | 3 |
| `abacaba` | 1 | abacaba | 1 |
| $a^n$, $n \ge 1$ | 1 | $a^n$ | 1 |
| `abcabc` | 6 | single symbols | 6 |

The last column shows that taking the longest palindromic prefix at each step is not optimal: on `aaba` it takes `aa` and is left with `ba`, which needs two pieces.

## Known algorithms

**Brute force, $O(2^n n)$.** Try every set of cuts and test each piece. Useful only as a check.

**Dynamic programming, $\Theta(n^2)$.** Compute the prefix recurrence for $i = 0, \ldots, n - 1$, with a table of palindromic substrings filled column by column in the same loop. [Palindrome partition dynamic programming](/palindrome-partition-dp/) gives the algorithm, its proof and the rebuild of a partition. Expanding around the $2n - 1$ centers from left to right gives the same values in $O(n)$ space and $O(n + N_{\mathrm{occ}}(s))$ time, where $N_{\mathrm{occ}}(s) \le n(n+1)/2$ counts the palindromic occurrences.

**Series links, $O(n \log n)$.** The palindromic suffixes of a prefix, sorted by length, form $O(\log n)$ groups in which the lengths are in arithmetic progression with the same difference. In the [palindromic tree](/palindromic-tree/) each node $v$ has the length $\mathrm{len}[v]$, the suffix link $\mathrm{link}[v]$, the difference $\mathrm{diff}[v] = \mathrm{len}[v] - \mathrm{len}[\mathrm{link}[v]]$, and the series link $\mathrm{slink}[v]$, the first node on the suffix-link path from $v$ whose difference is not $\mathrm{diff}[v]$. A value $\mathrm{ser}[v]$ stores the minimum of $\mathrm{PL}_j$ over the starts $j$ of the group of $v$.

```pseudo id=series
SERIES-LINK-PL(s)                      ▷ s[0 .. n − 1]
L1  best[0] ← 0, T ← empty palindromic tree with diff and slink
L2  for i ← 1 to n do
L3      add s[i − 1] to T, v ← the node of the longest palindromic suffix of s[0 .. i − 1]
L4      best[i] ← ∞
L5      while len[v] > 0 do
L6          ser[v] ← best[i − len[slink[v]] − diff[v]]
L7          if diff[v] = diff[link[v]] then ser[v] ← min(ser[v], ser[link[v]])
L8          best[i] ← min(best[i], ser[v] + 1)
L9          v ← slink[v]
L10 return best[n]
```

Line L6 reads the start of the shortest palindrome of the group of $v$. Line L7 reuses the rest of the group: when $\mathrm{diff}[v] = \mathrm{diff}[\mathrm{link}[v]]$, the node $\mathrm{link}[v]$ was last on a series path at position $i - \mathrm{diff}[v]$, and the starts of its group there are the other starts of the group of $v$ now (Fici et al.; Rubinchik and Shur). Each position follows $O(\log n)$ series links, so the time is $O(n \log n)$ for a constant-size alphabet. With the sum in place of the minimum, the same loop counts the partitions.

**Linear time.** Borozdin, Kosolobov, Rubinchik and Shur (2017) compute $\mathrm{PL}$ of all prefixes online in $O(n)$ time. Their method builds on the same series of palindromic suffixes as the $O(n \log n)$ algorithms.

**History.** The prefix recurrence is folklore. Galil and Seiferas (1978) gave the linear online recognition of Palstar, the concatenations of even palindromes. The first subquadratic algorithms for the minimum came in 2014, from Fici, Gagie, Kärkkäinen and Kempa and, at the same time, from I, Sugimoto, Inenaga, Bannai and Takeda, with the $O(\log n)$ grouping of palindromic suffixes. Rubinchik and Shur expressed the method with series links in the eertree, and Borozdin, Kosolobov, Rubinchik and Shur reached linear time in 2017.

## Bounds

- **Range.** $1 \le \mathrm{PL}(s) \le n$ for $n \ge 1$. $\mathrm{PL}(s) = 1$ if and only if $s$ is a palindrome.
- **When $\mathrm{PL}(s) = n$.** $\mathrm{PL}(s) = n$ if and only if $s$ has no palindromic substring of length 2 or 3. If $s$ has such a substring, a partition with that piece and single symbols has $n - 1$ or $n - 2$ pieces. If it has none, it has no palindrome of length at least 2 at all, because each such palindrome has one of length 2 or 3 at its center, so every piece is a single symbol. Over two letters every string of length 3 has the form $xyx$ or contains $xx$, so $\mathrm{PL}(s) < n$ for binary strings with $n \ge 3$.
- **One more symbol.** $|\mathrm{PL}(s\,a) - \mathrm{PL}(s)| \le 1$ for each symbol $a$. Adding $a$ as a new piece gives $\mathrm{PL}(s\,a) \le \mathrm{PL}(s) + 1$. Conversely, if the last piece of a best partition of $s\,a$ is $a\,q\,a$, then $q$ is a palindrome and $a\,q$ splits into the two pieces $a$ and $q$, or into one if $q$ is empty; if the last piece is $a$, remove it. So $\mathrm{PL}(s) \le \mathrm{PL}(s\,a) + 1$.
- **Subadditivity.** $\mathrm{PL}(u\,v) \le \mathrm{PL}(u) + \mathrm{PL}(v)$, and $\mathrm{PL}(s^R) = \mathrm{PL}(s)$.
- **Time.** $O(n)$ is reached. In the comparison model with $|\Sigma| \ge 2$, at least $\lfloor n/2 \rfloor$ tests are needed on $a^n$, because deciding $\mathrm{PL}(s) = 1$ is [palindrome recognition](/palindrome-recognition/). So the problem is $\Theta(n)$.

## Reductions

- **From palindrome recognition.** $s$ is a palindrome if and only if $\mathrm{PL}(s) = 1$.
- **To a shortest path.** $\mathrm{PL}(s)$ is the length of a shortest path from 0 to $n$ in the DAG on the positions $0, \ldots, n$ with an edge $j \to i + 1$ for each palindrome $s[j..i]$. The graph has $N_{\mathrm{occ}}(s)$ edges, and [DAG dynamic programming](/dag-dynamic-programming/) in position order gives the quadratic algorithm.
- **To text segmentation.** It is [text segmentation](/text-segmentation/) with the fewest words, where the dictionary is the set of all palindromes.
- **To palindromic suffixes.** Each algorithm above only needs, at each prefix, the set of its palindromic suffixes, which the palindromic tree gives.

## Applications

- **Combinatorics on words.** The palindromic length of the prefixes and factors of infinite words, such as the [Fibonacci word](/fibonacci-word/), is a studied measure, and the online algorithms compute it for long prefixes.
- **Structure of DNA.** Splitting a sequence into palindromic parts, possibly with gaps and errors, models hairpin structures; see [palindrome partitioning](/palindrome-partitioning/) and [gapped palindrome](/gapped-palindrome/).
- **Programming tasks.** The minimum number of cuts for a palindrome partition is a standard exercise in dynamic programming over prefixes.

## References
