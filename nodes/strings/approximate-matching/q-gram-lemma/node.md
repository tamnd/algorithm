---
tag: 57WF4P
kind: theorem
slug: q-gram-lemma
name: q-gram lemma
aliases:
- q-gram counting lemma
area: strings/approximate-matching
level: core
summary: Strings within k edits share at least (n - q + 1) - kq common q-grams.
prereqs: [edit-distance, wagner-fischer-algorithm]
see_also: [q-gram-filtering, pigeonhole-filtering, approximate-string-matching, string-similarity-join, approximate-dictionary-lookup, kmer-index, alignment-free-comparison]
sources:
  - paper: "Petteri Jokinen and Esko Ukkonen, Two algorithms for approximate string matching in static texts, Mathematical Foundations of Computer Science 1991, Lecture Notes in Computer Science 520, Springer"
    locator: the lemma that an approximate occurrence keeps at least m + 1 - (k + 1) q of the q-grams of the pattern, used for a q-gram index of the text
  - paper: "Esko Ukkonen, Approximate string-matching with q-grams and maximal matches, Theoretical Computer Science 92(1), 1992, 191-211"
    locator: the q-gram distance and its use as a lower bound of the edit distance
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 8 (filtering algorithms, the counting filters based on q-grams)
  - book: isbn:9780521813075
    title: Gonzalo Navarro and Mathieu Raffinot, Flexible Pattern Matching in Strings, Cambridge University Press, 2002
    locator: Chapter 6 (filtering for approximate matching)
---

The q-gram lemma states that if two strings have [edit distance](/edit-distance/) at most $k$, and the first has length $m$, then at least $m - q + 1 - kq$ of the substrings of length $q$ of the first string also occur in the second, at nearby positions. Each edit can destroy at most $q$ of these substrings, and the lemma counts what is left. It is the basis of [q-gram filtering](/q-gram-filtering/), which discards text regions or candidate pairs that share too few q-grams before any edit distance is computed. Jokinen and Ukkonen stated it in 1991.

## Statement

Let $q \ge 1$ and $k \ge 0$ be integers, and let $x = x[0 \ldots m-1]$ and $y = y[0 \ldots n-1]$ be strings. Indices are 0-based, and $d$ is the Levenshtein distance (insertions, deletions and substitutions of single characters, unit costs, no transpositions). The **q-grams** of $x$ are the substrings $x[i \ldots i+q)$ for $0 \le i \le m - q$, so $x$ has $m - q + 1$ of them, counted by position, when $m \ge q$. The **q-gram profile** $G_x(v)$ is the number of positions $i$ with $x[i \ldots i+q) = v$, for $v \in \Sigma^q$.

**Theorem (q-gram lemma).** If $d(x, y) \le k$, then there is a set $I \subseteq \{0, \ldots, m-q\}$ with

$$|I| \ge m - q + 1 - kq$$

and a strictly increasing map $\varphi : I \to \{0, \ldots, n-q\}$ such that for each $i \in I$, $y[\varphi(i) \ldots \varphi(i) + q) = x[i \ldots i+q)$ and $|\varphi(i) - i| \le k$. In particular,

$$\sum_{v \in \Sigma^q} \min\bigl(G_x(v), G_y(v)\bigr) \ge m - q + 1 - kq.$$

When $m - q + 1 - kq \le 0$, that is, when $q \ge (m + 1)/(k + 1)$, the statement says nothing.

## In plain words

Cut a word into all its short pieces of a fixed length, overlapping, one starting at each letter. A small change to the word, such as one wrong letter, breaks only the pieces that cover that letter. The number of pieces that cover a letter is at most the piece length.

So if a second word is a few changes away from the first, most pieces of the first word survive and appear in the second word, at about the same place. If two words share few pieces, they must be far apart. A search can then skip all places in a text that share too few pieces with the pattern, and run the slow exact comparison only on the rest.

## Proof

By the [Wagner-Fischer algorithm](/wagner-fischer-algorithm/) page, $d(x, y)$ is the least cost of an alignment of $x$ and $y$, where an alignment is a sequence of columns $(a, b)$, $(a, -)$ or $(-, b)$ that spells $x$ in the top row and $y$ in the bottom row when the gaps are removed, and a column costs 0 if it is $(a, a)$ and 1 otherwise. Fix an alignment of cost at most $k$. Call its columns of cost 1 the edit columns. There are at most $k$ of them.

Each character $x[p]$ lies in exactly one column $c(p)$, and $c(0) < c(1) < \cdots < c(m-1)$. Call the q-gram at $i$ **kept** if every column from $c(i)$ to $c(i + q - 1)$ is a match column $(a, a)$. Let $I$ be the set of kept q-grams.

*At most $kq$ q-grams are not kept.* A q-gram at $i$ is not kept only if some edit column lies in the range from $c(i)$ to $c(i+q-1)$. Take one edit column $e$.

- If $e$ holds a character $x[p]$ (a substitution or a deletion), then $e$ lies in the range of the q-gram at $i$ only if $i \le p \le i + q - 1$. At most $q$ values of $i$ satisfy this.
- If $e = (-, b)$ is an insertion between $c(p-1)$ and $c(p)$, then $e$ lies in the range only if $i \le p - 1$ and $p \le i + q - 1$. At most $q - 1$ values of $i$ satisfy this. An insertion before $c(0)$ or after $c(m-1)$ lies in no range.

So each edit column rules out at most $q$ q-grams, and $|I| \ge (m - q + 1) - kq$.

*The map.* For $i \in I$, the columns from $c(i)$ to $c(i + q - 1)$ are match columns, and each holds a character of $x$. A column between $c(p)$ and $c(p+1)$ would hold no character of $x$, so it would be an insertion, which is an edit column. So these $q$ columns are consecutive. Their bottom row is a run of $q$ consecutive characters of $y$, say $y[i' \ldots i'+q)$, and each column is $(a, a)$, so $y[i' \ldots i'+q) = x[i \ldots i+q)$. Set $\varphi(i) = i'$. If $i_1 < i_2$ are in $I$, then $c(i_1) < c(i_2)$, and the bottom character of $c(i_1)$ comes before that of $c(i_2)$ in $y$, so $\varphi(i_1) < \varphi(i_2)$.

*The offset.* Let $a$ be the number of insertion columns and $b$ the number of deletion columns before $c(i)$. The columns before $c(i)$ hold $i$ characters of $x$ and $i'$ characters of $y$, so $i' - i = a - b$. Both $a$ and $b$ are at most $k$ and at least 0, so $|i' - i| \le \max(a, b) \le k$.

*The profile bound.* For a fixed $v \in \Sigma^q$, let $I_v = \{ i \in I : x[i \ldots i+q) = v \}$. These are $|I_v|$ distinct positions of $v$ in $x$, so $|I_v| \le G_x(v)$. Their images under $\varphi$ are $|I_v|$ distinct positions of $v$ in $y$, because $\varphi$ is injective, so $|I_v| \le G_y(v)$. Summing $|I_v| \le \min(G_x(v), G_y(v))$ over $v$ gives $|I| \le \sum_v \min(G_x(v), G_y(v))$. $\blacksquare$

## Consequences

- **Both strings.** The distance is symmetric, so the bound also holds with $n$ in place of $m$. The shared q-grams number at least $\max(m, n) - q + 1 - kq$.
- **The q-gram distance.** Let $D_q(x, y) = \sum_v |G_x(v) - G_y(v)|$. Then $D_q(x, y) \le 2q \cdot d(x, y)$. Proof: a substitution at $p$ removes the at most $q$ q-grams that cover $p$ and adds at most $q$ new ones. An insertion removes at most $q - 1$ q-grams, those that span the new gap, and adds at most $q$, those that cover the new character. A deletion is the inverse of an insertion. So each operation changes the profile by at most $2q$ in the sum of absolute values, and the triangle inequality for this sum along an optimal script of $d(x, y)$ operations gives the bound. Ukkonen used $D_q / (2q)$ as a fast lower bound for the edit distance.
- **Filters for approximate matching.** If a substring of a text has distance at most $k$ to a pattern of length $m$, it shares at least $m - q + 1 - kq$ q-grams with the pattern. A [q-gram filter](/q-gram-filtering/) counts the shared q-grams of each text window and checks only the windows that reach the threshold. The threshold is positive only when $q < (m + 1)/(k + 1)$.
- **Hamming distance.** If $x$ and $y$ have equal length and differ in at most $k$ positions, the same proof with no gaps gives $\varphi(i) = i$: at least $m - q + 1 - kq$ q-grams occur at the same position.
- **Transpositions.** A transposition of $x[p]$ and $x[p+1]$ breaks the q-grams that cover $p$ or $p + 1$, which are at most $q + 1$. So for the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/) the bound becomes $m - q + 1 - k(q + 1)$.
- **Exact pieces.** The case of disjoint pieces instead of all q-grams gives the [pigeonhole filter](/pigeonhole-filtering/): split the pattern into $k + 1$ parts, and one part survives intact.

## Tightness

The bound is exact for all $m$, $q$ and $k$ with $m - q + 1 - kq \ge 0$. Let $x$ consist of $m$ distinct characters, and let $y$ replace $x[p_r]$ by a new character for $p_r = (q - 1) + (r - 1) q$, $r = 1, \ldots, k$. The condition $m - q + 1 - kq \ge 0$ gives $p_k \le m - q$. Each $p_r$ is covered by exactly $q$ q-grams of $x$, and these sets are disjoint because the positions are $q$ apart. A q-gram of $y$ that contains a new character occurs nowhere in $x$, and the other q-grams of $x$ are unchanged and distinct. So exactly $m - q + 1 - kq$ q-grams are shared, with $d(x, y) \le k$.

For example, $x = \texttt{abcdefgh}$ and $y = \texttt{axcdexgh}$ with $q = 2$ and $k = 2$ give the bound $8 - 2 + 1 - 4 = 3$. The shared 2-grams are $\texttt{cd}$, $\texttt{de}$ and $\texttt{gh}$, exactly 3.

## History

Jokinen and Ukkonen stated the lemma in 1991 and used it for approximate matching in a text with a q-gram index. Ukkonen introduced the q-gram distance in 1992 and showed that it gives a lower bound for the edit distance. Navarro's survey describes the later counting filters built on the lemma.

## References
