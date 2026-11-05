---
tag: VX6BMT
kind: concept
slug: edit-operations
name: Edit operations
aliases:
- insertion, deletion and substitution
area: strings/approximate-matching
level: intro
summary: The elementary insert, delete and replace steps whose costs define edit distance.
prereqs: [alphabet]
see_also: [edit-distance, hamming-distance, damerau-levenshtein-distance, weighted-edit-distance, longest-common-subsequence, shortest-edit-script, global-alignment, approximate-string-matching]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11 (edit transcripts, string alignment and the edit distance)
  - paper: doi:10.1145/321796.321811
    title: Robert A. Wagner and Michael J. Fischer, The string-to-string correction problem, Journal of the ACM 21(1), 1974
    locator: pages 168 to 173 (edit operations, their costs, and traces)
  - paper: doi:10.1145/375360.375365
    title: Gonzalo Navarro, A guided tour to approximate string matching, ACM Computing Surveys 33(1), 2001
    locator: Section 3.1 (the edit operations and the distances that they define)
---

Edit operations are the elementary steps that change one string into another: insert one character, delete one character, or replace one character by another. A set of allowed operations and a cost for each operation define an [edit distance](/edit-distance/): the least total cost of a sequence of operations that turns one string into the other. The choice of operations gives the common string distances, from [Hamming distance](/hamming-distance/) to the [Damerau-Levenshtein distance](/damerau-levenshtein-distance/).

## In plain words

Think of a word processor with only three keys. One key types a letter at the cursor. One key deletes the letter at the cursor. One key overwrites the letter at the cursor with another letter. Any text can become any other text with these keys. The question is how few key presses you need.

The fewest key presses measure how different two texts are. Two texts that need one press are close, for example a word with one typing error and the correct word. Two texts that need many presses are far apart.

Other measures change the set of keys. With only the overwrite key, the two texts must have the same length. A fourth key that swaps two neighbouring letters fixes the most common typing error with one press.

## The idea

Fix an [alphabet](/alphabet/) $\Sigma$ and strings over it. Indices are 0-based. The operations on a string $s$ are:

- **Insertion** of a character $c$ at position $i$, for $0 \le i \le |s|$: $s[0 \ldots i-1]\, c\, s[i \ldots |s|-1]$. We write it $\varepsilon \to c$.
- **Deletion** of the character at position $i$, for $0 \le i < |s|$: $s[0 \ldots i-1]\, s[i+1 \ldots |s|-1]$. We write it $c \to \varepsilon$, where $c = s[i]$.
- **Substitution** of $s[i]$ by a character $c \ne s[i]$. We write it $s[i] \to c$. Some texts call it replacement.
- **Transposition** of the adjacent characters $s[i]$ and $s[i+1]$, for $0 \le i < |s| - 1$. We write it $ab \to ba$.

A cost function $\gamma$ gives a non-negative cost to each operation, for example $\gamma(a \to b)$ for a substitution. An edit script from $x$ to $y$ is a sequence of operations that turns $x$ into $y$. Its cost is the sum of the costs of its operations. The distance $d(x, y)$ is the least cost of a script from $x$ to $y$.

Each set of operations gives a standard distance:

| operations | distance | condition |
|---|---|---|
| substitution | [Hamming distance](/hamming-distance/) | $\lvert x \rvert = \lvert y \rvert$ |
| insertion, deletion | indel distance, $\lvert x \rvert + \lvert y \rvert - 2\,\mathrm{LCS}(x, y)$ | none |
| insertion, deletion, substitution | Levenshtein distance | none |
| the three above and transposition | [Damerau-Levenshtein distance](/damerau-levenshtein-distance/) | none |

The distances in the table use cost 1 for each operation. With other costs, the distance is a [weighted edit distance](/weighted-edit-distance/). In the second row, $\mathrm{LCS}(x, y)$ is the length of a [longest common subsequence](/longest-common-subsequence/). The kept characters of a script with only insertions and deletions form a common subsequence, and each other character costs one operation.

**Scripts and alignments.** An alignment writes $x$ and $y$ in two rows, with gap symbols $-$, so that the rows have the same length and no column holds two gaps. A column $\binom{a}{b}$ with $a = b$ is a match, a column with $a \ne b$ is a substitution, a column $\binom{-}{b}$ is an insertion and a column $\binom{a}{-}$ is a deletion. Wagner and Fischer call this structure a trace. A trace changes each character at most once. A script can change the same position many times, so a script can cost less than each trace. When the costs satisfy the [triangle inequality](/triangle-inequality/), for example $\gamma(a \to c) \le \gamma(a \to b) + \gamma(b \to c)$, the least cost of a script equals the least cost of an alignment. Then the distance is a shortest path in a grid graph, and a [dynamic program](/wagner-fischer-algorithm/) computes it.

**Symmetry.** Insertion of $c$ and deletion of $c$ undo each other, and $a \to b$ undoes $b \to a$. So when $\gamma(\varepsilon \to c) = \gamma(c \to \varepsilon)$ and $\gamma(a \to b) = \gamma(b \to a)$, a script from $x$ to $y$ read backwards with each operation undone is a script from $y$ to $x$ of the same cost, and $d(x, y) = d(y, x)$.

## Examples

**Two substitutions and an insertion.** The script $k \to s$, $e \to i$, $\varepsilon \to g$ turns $\texttt{kitten}$ into $\texttt{sitting}$ with three operations: $\texttt{kitten} \to \texttt{sitten} \to \texttt{sittin} \to \texttt{sitting}$. No script with two operations exists, so the Levenshtein distance is 3. The alignment is:

```
k i t t e n -
s i t t i n g
```

**The same pair under other operations.** With only insertions and deletions, $\mathrm{LCS}(\texttt{kitten}, \texttt{sitting}) = 4$ (the subsequence $\texttt{ittn}$), so the indel distance is $6 + 7 - 2 \cdot 4 = 5$. The Hamming distance is not defined, because the lengths differ. For $\texttt{karolin}$ and $\texttt{kathrin}$, the Hamming distance and the Levenshtein distance are both 3.

**A transposition.** The strings $\texttt{ab}$ and $\texttt{ba}$ have Levenshtein distance 2, for example by two substitutions. With transpositions, the distance is 1.

**A script that changes a position twice.** The script $\texttt{ca} \to \texttt{ac} \to \texttt{abc}$ uses a transposition, then an insertion between the two swapped characters. It costs 2. A variant that edits each part of the string at most once, the optimal string alignment distance, gives 3 for this pair, so this variant is not the Damerau-Levenshtein distance.

**Non-example.** A block move, for example $\texttt{abcxyz} \to \texttt{xyzabc}$, is not an edit operation. With the operations above, it costs several unit steps. The [block edit distance](/block-edit-distance/) adds such moves as single operations.

## Where it is used

- **Spelling correction.** Damerau observed that most typing errors are one insertion, one deletion, one substitution or one transposition of adjacent letters. [Approximate dictionary lookup](/approximate-dictionary-lookup/) finds the words at a small distance from a misspelt word.
- **Approximate search in text.** The [approximate string matching](/approximate-string-matching/) problem finds the places in a text where a pattern occurs with at most $k$ operations.
- **File comparison.** The diff tools compute a [shortest edit script](/shortest-edit-script/) with only insertions and deletions of lines, for example by the [Myers diff](/myers-diff/) algorithm.
- **Biology.** A [global alignment](/global-alignment/) of two DNA or protein sequences uses substitution costs from a score matrix, and gaps model insertions and deletions in evolution.

## References
