---
tag: KKPM23
kind: problem
slug: text-segmentation
name: Text segmentation
aliases:
- word break
- interpunctio verborum
area: techniques/dynamic-programming
level: intro
summary: Decides whether a string without spaces can be split into valid words, solved by recursion with memoization or dynamic programming.
prereqs: [recursion, memoization, tabulation]
see_also: [memoization, dp-on-dag, trie, aho-corasick, hash-table, optimal-text-wrapping, deterministic-finite-automaton, viterbi-algorithm]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms, first edition, 2019
    locator: Chapter 2, section Text Segmentation (Interpunctio Verborum); Chapter 3, section Interpunctio Verborum Redux
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6), 333-340, 1975
    locator: the automaton that reports all occurrences of a finite set of keywords in one pass over the text
---

The text segmentation problem takes a string $A[1..n]$ with no spaces and a dictionary of words, and asks whether $A$ can be split into a sequence of words from the dictionary. The dictionary is given as an oracle $\text{IsWord}$ that answers whether a string is a word. A plain recursive search tries every first word and can take exponential time, but the recursion only ever asks about suffixes of $A$, so [memoization](/memoization/) or a table over the $n + 1$ suffixes solves it with $O(n^2)$ calls to the oracle. Erickson uses it as the first example in both his backtracking and his dynamic programming chapters. The same table counts the splittings or finds the best one under a score, and the problem is a reachability question in a [DAG](/dp-on-dag/) on the positions of the string.

## In plain words

Someone wrote a sentence and left out all the spaces. You have a list of real words. Can you put the spaces back so that every piece is a real word?

Try a first word, then try to split the rest. If the rest cannot be split, try a longer first word. This search can repeat the same work many times, because many different first pieces lead to the same rest of the string.

But the rest is always a tail of the string, and there are only $n + 1$ tails. So answer the question once for each tail, from the shortest tail to the full string, and store the answers. Each answer looks at the possible first words of its tail and reuses stored answers.

## Definition

**Input.** A string $A[1..n]$ over an alphabet, and a predicate $\text{IsWord}(w)$ that tells whether a string $w$ is in the dictionary.

**Output.** Whether there are indices $1 = i_1 < i_2 < \cdots < i_k < i_{k+1} = n + 1$ such that each piece $A[i_t .. i_{t+1} - 1]$ is a word. The empty string has the empty splitting.

The usual cost model counts calls to $\text{IsWord}$. If the dictionary is in a [hash table](/hash-table/) or a [trie](/trie/), a call on a piece of length $\ell$ costs $O(\ell)$ time.

## Variants

- **Construct a splitting.** Return the words, not only yes or no.
- **Count the splittings.** Replace "or" by "+" in the recurrence. The count can be exponential in $n$.
- **Fewest words, or best score.** Give each word a score, for example the log of its probability in a language model, and find the splitting of best total score. With word probabilities this is the most likely splitting, and the recurrence is the same as in the [Viterbi algorithm](/viterbi-algorithm/).
- **Bounded word length.** If no word is longer than $L$, each suffix needs only $L$ oracle calls.
- **Line breaking.** If the words are given and the choice is where to end each line, with a cost per line, the problem becomes [optimal text wrapping](/optimal-text-wrapping/), which has the same suffix structure.

## Examples

Take Erickson's string `bothearthandsaturnspin` ($n = 22$) and the dictionary

> a, and, art, at, bot, both, ear, earth, hand, hands, he, heart, hearth, pin, sat, saturn, spin, the, turn, turns, urn, urns.

Let $\text{Splittable}(i)$ be true if the suffix that starts at position $i$ can be split, and $N(i)$ the number of its splittings (positions from 0 here):

| $i$ | suffix | Splittable | $N(i)$ |
|---|---|---|---|
| 22 | (empty) | true | 1 |
| 18 | `spin` | true | 1 |
| 14 | `turnspin` | true | 2 |
| 12 | `saturnspin` | true | 3 |
| 9 | `andsaturnspin` | true | 3 |
| 8 | `handsaturnspin` | true | 7 |
| 4 | `earthandsaturnspin` | true | 3 |
| 3 | `hearthandsaturnspin` | true | 17 |
| 1 | `othearthandsaturnspin` | false | 0 |
| 0 | `bothearthandsaturnspin` | true | 20 |

So the string has 20 splittings, for example `both earth and saturn spin`, `bot heart hands at urns pin` and `bot hearth and sat urn spin`. The splitting with the fewest words is `both earth and saturn spin`, with 5 words.

**Exponential growth.** For the string $a^n$ and the dictionary $\{a, aa\}$, the number of splittings is the Fibonacci number $F_{n+1}$: 1, 2, 3, 5, 8, ... for $n = 1, 2, 3, 4, 5$, and 1,346,269 for $n = 30$. A search that lists all splittings, or a recursion without memoization that tries both first words at each step, does exponential work on this input, while the table has only $n + 1$ entries.

## Known algorithms

**Backtracking.** $\text{Splittable}(i)$ tries each $j \ge i$ with $\text{IsWord}(A[i..j])$ and recurses on $j + 1$. Without memoization the number of calls satisfies $T(n) \le \sum_{m < n} T(m) + O(n)$, which allows $2^{n-1}$ calls, and the input $a^n b$ with the dictionary $\{a, aa\}$ forces exponential time, since no call succeeds and every branch is explored.

**Dynamic programming, $O(n^2)$ oracle calls.** With $\text{Splittable}(n + 1) = \text{true}$,

$$\text{Splittable}(i) = \bigvee_{j = i}^{n} \bigl( \text{IsWord}(A[i..j]) \wedge \text{Splittable}(j + 1) \bigr).$$

*Why it is correct.* A splitting of the suffix at $i$ has a first word $A[i..j]$ for some $j$, and the rest is a splitting of the suffix at $j + 1$. Conversely, any word $A[i..j]$ followed by a splitting of the suffix at $j + 1$ is a splitting of the suffix at $i$. So the suffix at $i$ is splittable exactly when some $j$ makes both parts true.

Fill the table for $i = n + 1$ down to $1$. Each entry makes at most $n - i + 1$ oracle calls, so there are $O(n^2)$ calls in total, and $O(n)$ space. To return the words, store for each $i$ a $j$ that made the entry true and follow these from $i = 1$. If each oracle call costs $O(\ell)$ for a piece of length $\ell$, the time is $O(n^3)$, or $O(nL^2)$ with word length at most $L$.

**A trie walk, $O(nL)$.** From each start $i$, walk down a [trie](/trie/) of the dictionary along $A[i], A[i+1], \ldots$ and stop when the trie has no child. Each step tells whether $A[i..j]$ is a word in $O(1)$ time, so the work for $i$ is $O(L)$ and the total is $O(nL) \subseteq O(n^2)$.

**Aho-Corasick, $O(n + m)$.** Build the [Aho-Corasick](/aho-corasick/) automaton of the dictionary and scan $A$ once. It reports every pair $(i, j)$ with $A[i..j]$ a word, in time linear in $n$ plus the number $m$ of such occurrences. These pairs are the edges of the DAG below, and a pass over the edges in order of $j$ finishes the dynamic program. Here $m$ can be as large as $nL$.

## Bounds

- $O(n^2)$ oracle calls in the general oracle model, by the dynamic program.
- $O(nL)$ time with a trie, where $L$ is the length of the longest word, after building the trie in time linear in the size of the dictionary.
- The number of splittings can be $F_{n+1}$, which grows like $1.618^n$, so listing all of them takes exponential time in the worst case, while deciding, counting and optimizing are polynomial.

## Reductions

- **To reachability in a DAG.** Make a vertex for each position $1, \ldots, n + 1$ and an edge $i \to j + 1$ whenever $A[i..j]$ is a word. A splitting is a path from $1$ to $n + 1$. The DAG is acyclic because edges go forward. Counting paths counts splittings, and a shortest path gives the fewest words. See [DP on a DAG](/dp-on-dag/).
- **To a regular language.** For a finite dictionary $D$, the splittable strings are the language $D^*$, which is regular. So a [deterministic finite automaton](/deterministic-finite-automaton/) for $D^*$ decides the problem in $O(n)$ time after it is built, although the automaton can be large.
- **To line breaking.** [Optimal text wrapping](/optimal-text-wrapping/) and [printing neatly](/printing-neatly/) have the same structure: a sequence is cut into consecutive pieces, and each piece has a cost that depends only on its ends.

## Applications

- **Word segmentation** for languages written without spaces between words, such as Chinese, Japanese and Thai, where a scored version with word frequencies is a standard baseline.
- **Splitting compound words**, as in German, and splitting hashtags, domain names and identifiers such as `getfilename` into words.
- **Recovering text** from sources that lost the spaces, as in old Latin and Greek texts written in scriptio continua, with no spaces between words. "Interpunctio verborum" is Latin for the marking of words.

## References
