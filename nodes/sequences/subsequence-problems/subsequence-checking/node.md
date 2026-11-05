---
tag: REEV9S
kind: problem
slug: subsequence-checking
name: Subsequence checking
aliases:
- is subsequence
- subsequence test
area: sequences/subsequence-problems
level: intro
summary: Decide whether one string is a subsequence of another, which a two-pointer scan solves in linear time.
prereqs: [subsequence, two-pointers]
see_also: [subsequence-automaton, minimum-window-subsequence, count-subsequence-occurrences, longest-common-subsequence, string-matching, binary-search]
sources:
  - paper: "Ricardo A. Baeza-Yates, Searching subsequences, Theoretical Computer Science 78(2), 1991, 363-376"
    locator: the greedy scan for one pattern, and the preprocessing of the text for many patterns (the subsequence automaton)
  - book: "M. Lothaire, Combinatorics on Words, Cambridge Mathematical Library, Cambridge University Press, 1997"
    locator: Chapter 6, Subwords (the subword order and the leftmost occurrence of a subword)
  - paper: "Maxime Crochemore, Borivoj Melichar and Zdenek Troniček, Directed acyclic subsequence graph: overview, Journal of Discrete Algorithms 1(3-4), 2003, 255-280"
    locator: the subsequence test against a preprocessed text, with tables and with position lists
---

Subsequence checking is the problem of deciding whether a pattern $P$ of length $m$ is a [subsequence](/subsequence/) of a text $T$ of length $n$: whether the letters of $P$ appear in $T$ in order, with any gaps. One left-to-right scan with [two pointers](/two-pointers/), which matches each letter of $P$ at its first possible place, solves it in $O(n)$ time and $O(1)$ extra space. When one text is tested against many patterns, a preprocessed text answers each query in time that depends on $m$ only: see the [subsequence automaton](/subsequence-automaton/).

## In plain words

You want to know if you can find the letters of a short word in a long text, in the same order, while you skip any letters of the text that you like. Put one finger on the first letter of the word and read the text from left to right. Each time the text letter is the letter under your finger, move the finger to the next letter of the word. If the finger gets past the end of the word, the answer is yes. If the text ends first, the answer is no.

Taking each letter at the first place you can is never a mistake. An early match leaves more of the text for the rest of the word.

## Definition

**Input.** A pattern $P = p_1 \cdots p_m$ and a text $T = t_1 \cdots t_n$ over an alphabet $\Sigma$.

**Output.** Yes if there are indices $1 \le i_1 < \cdots < i_m \le n$ with $t_{i_k} = p_k$ for all $k$, and no otherwise. A search version also outputs one such list of indices.

**The greedy scan.**

```pseudo id=scan
IS-SUBSEQUENCE(P[1 .. m], T[1 .. n])
L1  k ← 1
L2  for i ← 1 to n do
L3      if k ≤ m and T[i] = P[k] then k ← k + 1     ▷ match P[k] at position i
L4  return k = m + 1
```

**Why the greedy scan is right.** Let $g_1 < g_2 < \cdots$ be the positions where line L3 matches. We claim: if $(i_1, \ldots, i_m)$ is any embedding of $P$ in $T$, then the scan matches all of $P$ and $g_k \le i_k$ for each $k$. The proof is by induction on $k$. For $k = 1$, $g_1$ is the first position of $T$ that holds $p_1$, and $t_{i_1} = p_1$, so $g_1$ exists and $g_1 \le i_1$. For $k \ge 2$, the scan looks for $p_k$ at the positions after $g_{k-1}$. By the induction hypothesis $g_{k-1} \le i_{k-1} < i_k$, and $t_{i_k} = p_k$, so the scan finds $p_k$ at some position $g_k \le i_k$. Conversely, if the scan matches all of $P$, the positions $g_1 < \cdots < g_m$ are an embedding. So the scan says yes if and only if $P \preceq T$. The list $(g_1, \ldots, g_m)$ is the *leftmost embedding*: it is pointwise at most each other embedding.

## Variants

- **Many patterns, one text.** Preprocess $T$ once. A next-occurrence table $\mathrm{nxt}[i][c]$, the least position $\ge i$ that holds the letter $c$, takes $O(n \sigma)$ space for an alphabet of size $\sigma$ and answers a query in $O(m)$ time. Sorted lists of positions for each letter take $O(n)$ space and answer in $O(m \log n)$ time with [binary search](/binary-search/). This is the [subsequence automaton](/subsequence-automaton/).
- **Many texts, one pattern.** Run the scan on each text, or count the texts that contain the pattern.
- **Longest matched prefix.** The final value $k - 1$ of the scan is the length of the longest prefix of $P$ that is a subsequence of $T$, by the same proof.
- **Gap constraints.** Each gap $i_{k+1} - i_k$ must be at most a bound. The greedy scan is then not correct, and a table or an automaton is used.
- **Shortest window.** Find the shortest substring of $T$ that contains $P$ as a subsequence: [minimum window subsequence](/minimum-window-subsequence/).
- **Counting.** Count the embeddings of $P$ in $T$: [counting pattern occurrences as a subsequence](/count-subsequence-occurrences/).

## Examples

| $P$ | $T$ | matched positions $g_k$ | answer |
| --- | --- | --- | --- |
| ACE | ABCDE | 1, 3, 5 | yes |
| AEC | ABCDE | 1, 5 | no: no C after position 5 |
| ADB | ABCBDAB | 1, 5, 7 | yes |
| ABBA | ABCBDAB | 1, 2, 4, 6 | yes |
| BBBB | ABCBDAB | 2, 4, 7 | no: the text has only three B's |

For ADB, the leftmost embedding $(1, 5, 7)$ is also the only one: the A must come before the single D at position 5, so it is at position 1, and only position 7 holds a B after the D.

**A non-example of greedy.** For substring search (the letters must be next to each other), "match at the first possible place and never go back" is wrong: for the pattern AAB and the text AAAB, a scan that starts the pattern again after a mismatch, and never moves back in the text, matches A, A, then fails on the third A, and misses the occurrence at positions 2 to 4. That problem needs [string matching](/string-matching/) algorithms. The subsequence problem allows gaps, and that is why the greedy rule is safe.

## Known algorithms

| method | preprocessing | query time | space |
| --- | --- | --- | --- |
| greedy two-pointer scan | none | $O(n)$, at most $n$ letter tests | $O(1)$ |
| next-occurrence table | $O(n \sigma)$ | $O(m)$ | $O(n \sigma)$ |
| position lists and binary search | $O(n)$ | $O(m \log n)$ | $O(n)$ |
| [LCS table](/lcs-dynamic-programming/) | none | $O(nm)$ | $O(m)$ |

The scan stops early when $k = m + 1$, so it reads only the prefix of $T$ up to $g_m$. The LCS method is a reduction ($P \preceq T$ if and only if $\mathrm{lcs}(P, T) = m$), and it is slower; do not use it for this problem.

## Bounds

- **Upper bound.** $O(n)$ time and $O(1)$ extra space by the scan. With $m > n$ the answer is no at once.
- **Lower bound.** In the worst case an algorithm must read all $n$ letters of $T$. Take $P = c$, one letter, and a text $T$ that does not contain $c$. If an algorithm does not read position $i$ of $T$, it gives the same answer on the text with $c$ at position $i$, where the right answer is yes. So it needs $n$ reads, and the scan is optimal.
- **With preprocessing.** A query must at least read $P$, so $O(m)$ per query, as the next-occurrence table gives, is optimal.

## Reductions

- **To LCS.** $P \preceq T$ if and only if $\mathrm{lcs}(P, T) = |P|$. See [longest common subsequence](/longest-common-subsequence/).
- **To regular expressions.** $P \preceq T$ if and only if $T$ matches the regular expression $\Sigma^* p_1 \Sigma^* p_2 \cdots \Sigma^* p_m \Sigma^*$. The scan is the run of the automaton of this expression, which is deterministic.
- **To edit distance.** $P \preceq T$ if and only if $T$ can be turned into $P$ by $n - m$ deletions and no other edit.

## Applications

- **Fuzzy finders.** The file and command pickers of editors keep the names that contain the typed letters as a subsequence, then rank them.
- **Filters.** In mining of event logs, a pattern of events, in order but with other events between, is a subsequence query.
- **A step in other algorithms.** Subsequence tests appear inside the search for the [shortest common supersequence](/shortest-common-supersequence/) and in tests of LCS candidates.

## References
