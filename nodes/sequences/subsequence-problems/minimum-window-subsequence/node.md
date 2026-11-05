---
tag: B532N7
kind: problem
slug: minimum-window-subsequence
name: Minimum window subsequence
aliases:
- shortest substring containing a subsequence
area: sequences/subsequence-problems
level: intro
summary: Find the shortest contiguous window of a string that contains a given pattern as a subsequence.
prereqs: [subsequence-checking, sliding-window, tabulation]
see_also: [subsequence-automaton, minimum-window-substring, two-pointers, count-subsequence-occurrences, longest-common-subsequence]
sources:
  - paper: "Gautam Das, Rudolf Fleischer, Leszek Gasieniec, Dimitrios Gunopulos and Juha Karkkainen, Episode matching, Combinatorial Pattern Matching (CPM 1997), Lecture Notes in Computer Science 1264, 1997, 12-27"
    locator: the problem of the minimal windows of a text that contain a pattern as a subsequence, and the O(nm) algorithms
  - paper: "Heikki Mannila, Hannu Toivonen and A. Inkeri Verkamo, Discovery of frequent episodes in event sequences, Data Mining and Knowledge Discovery 1(3), 1997, 259-289"
    locator: serial episodes and their occurrence in windows of an event sequence
  - paper: "Ricardo A. Baeza-Yates, Searching subsequences, Theoretical Computer Science 78(2), 1991, 363-376"
    locator: the preprocessing of the text for subsequence queries (next-occurrence tables)
---

The minimum window subsequence problem takes a text $S$ of length $n$ and a pattern $T$ of length $m$ and asks for a shortest substring $S[l \ldots r]$ that contains $T$ as a [subsequence](/subsequence/). A table that records, for each text position and each prefix of $T$, the latest start of a window that ends there solves it in $O(nm)$ time and $O(m)$ space. In data mining the same question is the matching of a *serial episode*: a list of events that must happen in order inside a short time window.

## In plain words

You have a long text and a short word. You want the shortest piece of the text, without gaps, in which you can find the letters of the word in order, maybe with other letters between them. For the text "abcdebdde" and the word "bde", the answer is "bcde": it starts with b, it has d and then e later, and no shorter piece has b, d and e in this order.

For each place where a piece could end, the best piece starts as late as it can. So for each end, find the latest start, and keep the shortest piece. A table over the text and the beginnings of the word gives each latest start from the one before it.

## Definition

**Input.** A text $S = s_1 \cdots s_n$ and a pattern $T = t_1 \cdots t_m$ with $m \ge 1$, over an alphabet $\Sigma$.

**Output.** A window $[l, r]$, $1 \le l \le r \le n$, with $T \preceq s_l \cdots s_r$ and $r - l + 1$ minimum, or "none" if $T$ is not a subsequence of $S$. The usual tie rule takes the window with the smallest $l$.

**Latest starts.** For $1 \le i \le n$ and $0 \le j \le m$, let $f(i, j)$ be the largest $l \le i + 1$ with $t_1 \cdots t_j \preceq s_l \cdots s_i$, or $-\infty$ if there is none. Then $f(i, 0) = i + 1$ (the empty window after $i$), $f(0, j) = -\infty$ for $j \ge 1$, and for $i, j \ge 1$

$$f(i, j) = \begin{cases} f(i-1, j-1) & \text{if } s_i = t_j, \\ f(i-1, j) & \text{if } s_i \ne t_j. \end{cases}$$

The shortest window that ends at $r$ is $[f(r, m), r]$, and the answer is the shortest of these over all $r$.

*Proof.* Fix $i, j \ge 1$ and $l \le i$. An embedding of $t_1 \cdots t_j$ in $s_l \cdots s_i$ either does not use position $i$, and then it embeds $t_1 \cdots t_j$ in $s_l \cdots s_{i-1}$, or it uses $i$ for $t_j$, which needs $s_i = t_j$, and then it embeds $t_1 \cdots t_{j-1}$ in $s_l \cdots s_{i-1}$. If $s_i \ne t_j$, only the first kind exists, so $f(i, j) = f(i-1, j)$. If $s_i = t_j$, the set of good starts is the union of the good starts of the two kinds. Each start that is good for $t_1 \cdots t_j$ in $s_l \cdots s_{i-1}$ is also good for the shorter $t_1 \cdots t_{j-1}$, so the second set contains the first, and $f(i, j) = f(i-1, j-1)$. (For $j = 1$ this gives $f(i, 1) = f(i-1, 0) = i$, the window $[i, i]$.) Last, a window $[l, r]$ is good if and only if $l \le f(r, m)$, so among the good windows that end at $r$, the shortest starts at $f(r, m)$. $\square$

```pseudo id=window
MIN-WINDOW-SUBSEQUENCE(S[1 .. n], T[1 .. m])
L1  F[1 .. m] ← −∞; best ← none
L2  for i ← 1 to n do
L3      for j ← m downto 1 do                     ▷ downward, so F[j − 1] is still from row i − 1
L4          if S[i] = T[j] then F[j] ← (i if j = 1 else F[j − 1])
L5      if F[m] ≠ −∞ and (best = none or i − F[m] < best.r − best.l) then best ← [F[m], i]
L6  return best
```

## Variants

- **All minimal windows.** A window is minimal if no window strictly inside it is good. Each end position $r$ has at most one minimal window, $[f(r, m), r]$, so there are at most $n$. The window $[f(r, m), r]$ is minimal exactly when $f(r, m) > f(r-1, m)$ (with $f(0, m) = -\infty$): if the two are equal, $[f(r, m), r-1]$ is a good window inside it; if not, each good window that ends before $r$ starts before $f(r, m)$. So the same scan lists all minimal windows.
- **Windows of bounded width.** Episode matching often fixes a width $w$ and asks for the number of windows of width $w$ that contain the pattern, or for the frequency of an episode.
- **Substring with a multiset.** If the order of the pattern letters does not matter (each letter of $T$ must appear, with multiplicity, in any order), the problem is [minimum window substring](/minimum-window-substring/), solved in $O(n + m)$ time with a [sliding window](/sliding-window/).
- **Many patterns, one text.** A [subsequence automaton](/subsequence-automaton/) of $S$ and of its reverse lets each pattern be handled by jumps through next-occurrence tables.

## Examples

**The standard example.** $S = \text{abcdebdde}$, $T = \text{bde}$. The values $F[1], F[2], F[3]$ (latest starts for b, bd, bde) after each position $i$:

| $i$ | $s_i$ | $F[1]$ | $F[2]$ | $F[3]$ | window ending at $i$ |
| --- | --- | --- | --- | --- | --- |
| 1 | a | none | none | none | |
| 2 | b | 2 | none | none | |
| 3 | c | 2 | none | none | |
| 4 | d | 2 | 2 | none | |
| 5 | e | 2 | 2 | 2 | [2, 5] = bcde |
| 6 | b | 6 | 2 | 2 | [2, 6] |
| 7 | d | 6 | 6 | 2 | [2, 7] |
| 8 | d | 6 | 6 | 2 | [2, 8] |
| 9 | e | 6 | 6 | 6 | [6, 9] = bdde |

Two windows have length 4, bcde and bdde, and the tie rule gives bcde.

**More inputs.**

| $S$ | $T$ | answer |
| --- | --- | --- |
| ABCBDAB | BA | BDA, positions 4 to 6 |
| ABCBDAB | ADB | the whole text: the only embedding is $(1, 5, 7)$ |
| abc | d | none |

## Known algorithms

- **Latest-start DP.** MIN-WINDOW-SUBSEQUENCE takes $\Theta(nm)$ time and $O(m)$ space. It is correct by the recurrence and an induction on $i$. Since line L4 changes $F[j]$ only when $s_i = t_j$, a list of the pattern positions of each letter reduces the work to $O(n + r)$, where $r$ is the number of pairs $(i, j)$ with $s_i = t_j$.
- **Forward and backward scans.** From a position $p$, scan forward with the greedy [subsequence check](/subsequence-checking/) until $T$ is matched, at some end $r$. Then scan backward from $r$ and match $T$ from its last letter to its first; the place where the backward scan ends is the latest start $l = f(r, m)$, by the mirror form of the leftmost-embedding lemma. Record $[l, r]$, and start again at $p = l + 1$. Each round costs $O(r - l + m)$ and finds one minimal window; in the worst case the total is $O(nm)$, but it is fast when windows are short.
- **Next-occurrence jumps.** With a table $\mathrm{nxt}[i][c]$ of the next position $\ge i$ holding $c$, one candidate start costs $O(m)$ jumps. Trying each start $l$ with $s_l = t_1$ gives $O(nm)$ in the worst case, after $O(n \sigma)$ preprocessing.

## Bounds

- **Upper bound.** $O(nm)$ time and $O(m)$ space by the DP.
- **Lower bound.** $\Omega(n)$ reads of $S$ for the same reason as in [subsequence checking](/subsequence-checking/): with $m = 1$ and a letter that does not occur, an unread position could hold it.
- **Number of answers.** At most $n$ minimal windows, one for each end.

## Reductions

- **From subsequence checking.** The answer is "none" if and only if $T$ is not a subsequence of $S$.
- **Relation to LCS.** A window $[l, r]$ is good if and only if $\mathrm{lcs}(T, s_l \cdots s_r) = m$. This gives a slow method, but it explains why the table has the same shape as the [LCS table](/lcs-dynamic-programming/).

## Applications

- **Event logs and alarms.** In telecommunication alarm logs, a serial episode is a list of alarm types that occur in this order within a short time; the minimal windows show where it happens (Mannila, Toivonen and Verkamo).
- **Text search with gaps.** Find the shortest passage of a document in which given words occur in a given order.

## References
