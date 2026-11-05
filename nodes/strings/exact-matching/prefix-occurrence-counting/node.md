---
tag: JXWNXG
kind: problem
slug: prefix-occurrence-counting
name: Counting the occurrences of each prefix
aliases:
- Counting the number of occurrences of each prefix
area: strings/exact-matching
level: core
summary: Problem of computing how many times each prefix of a string occurs in it, using the prefix function in linear time.
prereqs: [prefix-function, border, string-matching]
see_also: [z-algorithm, knuth-morris-pratt, string-period, suffix-automaton, suffix-array]
sources:
  - url: https://cp-algorithms.com/string/prefix-function.html
    title: CP-Algorithms, Prefix function. Knuth-Morris-Pratt algorithm
    locator: the application "Counting the number of occurrences of each prefix" (counting by the values of the prefix function, then pushing the counts down the border chains)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 32.4, The Knuth-Morris-Pratt algorithm (the prefix-function iteration lemma, which lists the borders of a prefix by iterating π)
  - url: https://cp-algorithms.com/string/z-function.html
    title: CP-Algorithms, Z-function and its calculation
    locator: the definition of the Z-function, whose values count the prefix occurrences at each position
---

Counting the occurrences of each prefix asks, for a string $S$ of length $N$ and every length $k$ from 1 to $N$, how many times the prefix $S[0 \ldots k-1]$ occurs in $S$, or in a second string $T$. Occurrences may overlap. The problem is solved in $\Theta(N)$ time, or $\Theta(N + |T|)$ for a second string, by counting the values of the [prefix function](/prefix-function/) and pushing the counts down the chains of [borders](/border/). It is a standard application of the prefix function, and shows that one pass of [KMP](/knuth-morris-pratt/) preprocessing holds much more information than the single answer "found or not".

## In plain words

Take a word such as abacaba and ask: how often does "a" appear in it? How often "ab", "aba", and so on, up to the whole word? Each such start of the word can appear many times, and appearances may overlap.

At each place in the word, look at the longest start of the word that ends there. Every shorter start of the word that also ends there is a border of that longest one, and the borders form a chain. So count, for each place, only the longest start, then pass each count down the chain to the shorter starts. Doing the passing from the longest lengths to the shortest needs one sweep, and every count is final at the end.

## Definition

**Input.** A string $S[0 \ldots N-1]$ over a general alphabet, where only equality tests are used, and in the second form also a string $T[0 \ldots n-1]$. Indices are 0-based.

**Output.** The array $\mathrm{cnt}[1 \ldots N]$ with

$$\mathrm{cnt}[k] = \big|\{\, j : 0 \le j \le N - k,\ S[j \ldots j+k-1] = S[0 \ldots k-1] \,\}\big|,$$

the number of occurrences of the prefix of length $k$ in $S$, counted with overlaps. In the second form, $j$ ranges over $0 \le j \le n - k$ and the condition is $T[j \ldots j+k-1] = S[0 \ldots k-1]$. The empty prefix ($k = 0$) is excluded; it would occur $N + 1$ times. A prefix longer than $T$ occurs 0 times in $T$.

## Variants

- **Occurrences in the string itself.** The main form above. Each $\mathrm{cnt}[k] \ge 1$, because the prefix occurs at position 0.
- **Occurrences in another string.** Count the prefixes of $S$ in $T$. Run the same method on $S \# T$, with a separator $\#$ outside the alphabet, and use only the positions in $T$.
- **Prefixes that are also suffixes.** Report, for each border of $S$, its number of occurrences. The borders are the chain $\pi[N-1], \pi[\pi[N-1]-1], \ldots$ and the counts come from the same array.
- **Distinct starting positions.** Count, for each $k$, the positions $j$ where $S[j \ldots]$ starts with the prefix of length $k$, which is the same number; with the [Z array](/z-algorithm/), $\mathrm{cnt}[k] = |\{\, j : Z[j] \ge k \,\}|$ with $Z[0] = N$.
- **Occurrences of every substring.** Counting all distinct substrings, not only prefixes, needs a [suffix automaton](/suffix-automaton/) or a [suffix array](/suffix-array/).

## Examples

**$S$ = abacaba.** The prefix function is $\pi$ = 0 0 1 0 1 2 3.

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| prefix | a | ab | aba | abac | abaca | abacab | abacaba |
| $\mathrm{cnt}[k]$ | 4 | 2 | 2 | 1 | 1 | 1 | 1 |

The prefix a occurs at positions 0, 2, 4 and 6; aba occurs at 0 and 4.

**The computation.** First count how often each value appears in $\pi$: the value 0 three times, 1 twice, 2 once and 3 once, so $c$ = 3 2 1 1 0 0 0 0 for $k = 0, \ldots, 7$. Then, for $i = N - 1$ down to 1, add $c[i]$ to $c[\pi[i-1]]$: $c[3]$ = 1 goes to $c[\pi[2]] = c[1]$, $c[2]$ = 1 goes to $c[\pi[1]] = c[0]$, and $c[1]$ = 3 goes to $c[0]$, giving $c$ = 7 3 1 1 0 0 0 0. Finally add 1 to each $c[k]$ for the occurrence at position 0: 4 2 2 1 1 1 1.

**Periodic strings.** For $S = a^4$, $\mathrm{cnt}$ = 4 3 2 1. For $S$ = abab, $\mathrm{cnt}$ = 2 2 1 1.

**In another string.** The prefixes a, ab, aba of $S$ = aba occur 4, 3 and 3 times in $T$ = abababa.

**A non-example.** The value $\pi[i]$ alone is not the count: in abacaba, $\pi$ has the value 1 twice, but the prefix a occurs 4 times. The occurrence at position 6 ends abacaba, where the longest border is aba, so it is hidden behind that longer border and must be passed down the chain; the occurrence at position 0 is the prefix itself.

## Known algorithms

| algorithm | time | space | idea |
|---|---|---|---|
| naive, test every position for every $k$ | $O(N^3)$, or $O(N^2)$ by extending matches | $O(1)$ | the definition |
| prefix function and border chains | $\Theta(N)$ | $\Theta(N)$ | count $\pi$ values, push down the chains |
| Z array and suffix sums | $\Theta(N)$ | $\Theta(N)$ | $\mathrm{cnt}[k] = |\{ j : Z[j] \ge k \}|$, by counting sort |
| either method on $S \# T$ | $\Theta(N + n)$ | $\Theta(N + n)$ | occurrences in $T$ |

The prefix-function method:

1. Compute $\pi$ in $O(N)$ time.
2. Set $c[\pi[i]] \leftarrow c[\pi[i]] + 1$ for every $i$.
3. For $i = N - 1$ down to 1, set $c[\pi[i-1]] \leftarrow c[\pi[i-1]] + c[i]$.
4. Set $\mathrm{cnt}[k] = c[k] + 1$ for $1 \le k \le N$.

It is correct because the prefixes of $S$ that end at position $i$ and are shorter than $i + 1$ are exactly $\pi[i]$ and the lengths below it in its border chain, by the prefix-function iteration lemma. Step 3 processes lengths in decreasing order, and $\pi[i-1] < i$, so each count is complete when it is passed down. For occurrences in $T$, count in step 2 only the positions of $T$ in $S \# T$, where the value $N$ can occur, run step 3 from $i = N$, and skip step 4.

## Bounds

The output has $N$ numbers and every character must be read, so $\Omega(N)$ time is needed, and the two linear methods are optimal: $\Theta(N)$. They use only equality tests, so they work over a general alphabet. The counts can be as large as $N$ (for $a^N$), so each fits in a machine word in the [word RAM](/word-ram/) model.

## Reductions

- **From string matching.** The number of occurrences of $P$ in $T$ is the last entry of the counts of the prefixes of $P$ in $T$. So this problem is at least as hard as counting the occurrences in [string matching](/string-matching/).
- **To prefix function and Z array.** Both arrays determine the counts in $O(N)$ time, as above, so the problem reduces to computing either one.
- **Border counts.** The number of borders of $S$ is the length of the chain from $\pi[N-1]$, and the occurrences of each border come from the same array, so "how often does each border occur" reduces to this problem.

## Applications

- Counting the occurrences of each border of a string, a frequent contest task.
- Statistics on how strongly a string repeats its beginning, related to its [periods](/string-period/).
- Checking how many times each prefix of a query occurs in a document, for autocompletion-style ranking over a single text, with the second form.
- Teaching: it shows the [prefix function](/prefix-function/) as a compact encoding of all prefix occurrences, not only of the full pattern.

## References
