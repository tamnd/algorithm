---
tag: 7G9Q4Y
kind: problem
slug: approximate-dictionary-lookup
name: Approximate dictionary lookup
aliases:
- spell checking
- fuzzy dictionary search
area: strings/approximate-matching
level: core
summary: Find all dictionary words within a given edit distance of a query string.
prereqs: [edit-distance, trie]
see_also: [levenshtein-automaton, bk-tree, trie, q-gram-filtering, pigeonhole-filtering, string-similarity-join, damerau-levenshtein-distance, metric-space-indexing]
sources:
  - paper: doi:10.1145/146370.146380
    title: Karen Kukich, Techniques for automatically correcting words in text, ACM Computing Surveys 24(4), 1992
    locator: pages 377 to 439 (isolated-word error correction, minimum edit distance and dictionary lookup techniques)
  - paper: doi:10.1145/362003.362025
    title: W. A. Burkhard and R. M. Keller, Some approaches to best-match file searching, Communications of the ACM 16(4), 1973
    locator: pages 230 to 236 (the tree on a discrete metric, now called the BK-tree)
  - paper: "Klaus U. Schulz and Stoyan Mihov, Fast string correction with Levenshtein automata, International Journal on Document Analysis and Recognition 5(1), 2002"
    locator: the deterministic Levenshtein automaton of a word and its parallel traversal with the automaton of a dictionary
  - paper: "Leonid Boytsov, Indexing methods for approximate dictionary searching: comparative analysis, ACM Journal of Experimental Algorithmics 16, 2011"
    locator: the survey and experimental comparison of tries, neighborhood generation, q-gram and metric space methods
---

Approximate dictionary lookup is the problem of finding all words of a fixed set that lie within a given [edit distance](/edit-distance/) $k$ of a query word. It is the core step of a spelling corrector: a word that is not in the dictionary is replaced by the dictionary words close to it. The dictionary is known in advance, so the methods build an index once, such as a [trie](/trie/), a [BK-tree](/bk-tree/), a hash table of variants or a [q-gram](/q-gram-filtering/) index, and answer many queries. For a fixed $k$, good indexes answer a query far faster than a comparison with every word.

## In plain words

A spelling checker finds a word that is not in its word list. To suggest corrections, it needs the words of the list that are only one or two typing errors away from the wrong word.

Comparing the wrong word with every word of the list works, but the list can have millions of words. So the checker prepares the list once, in a structure that groups words with shared beginnings or shared pieces. For each query, it then walks only through the parts of the structure that can still lead to a close word, and stops early in the parts that are already too far.

The same problem appears when a search engine suggests "did you mean", and when a program matches names or codes with errors against a list.

## Definition

Let $\Sigma$ be an alphabet and $d$ the Levenshtein distance (unit-cost insertions, deletions and substitutions, no transpositions). A dictionary is a finite set $D \subseteq \Sigma^*$ of $N$ words with total length $L = \sum_{w \in D} |w|$. Indices of strings are 0-based.

The problem: preprocess $D$. Then, for each query $(x, k)$ with $x \in \Sigma^*$ and an integer $k \ge 0$, report the set

$$\{\, w \in D : d(x, w) \le k \,\},$$

as whole words (each word at most once, possibly with its distance). The match is global: the whole query is compared with the whole word, not with a substring of it. Let $m = |x|$ and let $\mathrm{occ}$ be the size of the answer.

## Variants

- **Nearest words.** Report the words with the least distance to $x$, or the $t$ nearest words, with no fixed $k$.
- **Other distances.** The [Damerau-Levenshtein distance](/damerau-levenshtein-distance/), which counts a swap of two neighbours as one error, a [weighted edit distance](/weighted-edit-distance/) with costs for keyboard neighbours, or the [Hamming distance](/hamming-distance/) for words of equal length, such as DNA barcodes.
- **Phonetic keys.** Report the words with the same [Soundex](/soundex/) or [Metaphone](/metaphone/) code. This is exact matching on codes, not a distance.
- **Dynamic dictionaries.** Words are inserted and deleted between queries.
- **Batch queries.** Answer a set of queries at once. With the dictionary itself as the query set, this is a [string similarity join](/string-similarity-join/).
- **Bounded error.** Many systems fix $k$ at 1 or 2, because most typing errors are a single edit.

## Examples

Let $D = \{\texttt{act}, \texttt{bat}, \texttt{cart}, \texttt{cast}, \texttt{cat}, \texttt{chart}, \texttt{coat}, \texttt{cut}, \texttt{dog}, \texttt{scat}, \texttt{tac}\}$ and $x = \texttt{cat}$.

| word | Levenshtein | Damerau-Levenshtein |
|---|---|---|
| cat | 0 | 0 |
| bat, cart, cast, coat, cut, scat | 1 | 1 |
| act | 2 | 1 |
| chart, tac | 2 | 2 |
| dog | 3 | 3 |

With $k = 1$, the answer is $\{\texttt{cat}, \texttt{bat}, \texttt{cart}, \texttt{cast}, \texttt{coat}, \texttt{cut}, \texttt{scat}\}$. Under the Damerau-Levenshtein distance it also contains $\texttt{act}$, because $\texttt{cat} \to \texttt{act}$ is one transposition. With $k = 0$ the answer is $\{\texttt{cat}\}$, an exact lookup.

## Known algorithms

| method | index | query time | notes |
|---|---|---|---|
| compare with each word | none | $O(\sum_{w} \min(m, \lvert w \rvert)\, k)$ with a band of width $2k + 1$ | skip words with $\lvert \lvert w \rvert - m \rvert > k$ |
| trie walk | [trie](/trie/), $O(L)$ nodes | $O(m)$ per visited node | prune when a column of the table exceeds $k$ |
| [Levenshtein automaton](/levenshtein-automaton/) | trie or minimal automaton of $D$ | the size of the visited part of $D$ | the automaton of $x$ is built in $O(m)$ time for fixed $k$ |
| neighborhood generation | [hash table](/hash-table/) of $D$ | $O((m \sigma)^k)$ lookups of $O(m + k)$ time each | generate all strings within $k$ of $x$ |
| deletion neighborhoods | hash table of all deletion variants | $O(m^k)$ lookups, then verification | index size grows like $L \cdot \ell^k$ for words of length $\ell$ |
| [BK-tree](/bk-tree/) | tree on the metric $d$ | depends on the data | needs a metric, prunes by the [triangle inequality](/triangle-inequality/) |
| [q-gram filter](/q-gram-filtering/) | inverted lists of q-grams | the length of the lists read, then verification | threshold $\max(m, \lvert w \rvert) - q + 1 - kq$ |

**Trie walk.** Do a depth-first walk of a trie of $D$. At a node with label $u$, keep the column $C[i] = d(x[0 \ldots i), u)$ for $i = 0, \ldots, m$ of the [Wagner-Fischer](/wagner-fischer-algorithm/) table; a child with letter $c$ gets its column in $O(m)$ time from the parent's column. Report $u$ when it is a word and $C[m] \le k$. Prune the subtree when $\min_i C[i] > k$, because the minimum of a column never decreases when the walk goes deeper. Words with common prefixes share the work.

**Levenshtein automaton.** Schulz and Mihov build a deterministic automaton that accepts exactly the words within distance $k$ of $x$, and walk it in parallel with the automaton of the dictionary. A state of the dictionary is visited only while the Levenshtein automaton is not in its dead state.

**Deletion neighborhoods.** If $d(x, w) \le k$, then deleting at most $k$ characters from each of $x$ and $w$ gives the same string: delete from $x$ the characters in substitution and deletion columns of an optimal alignment, and from $w$ those in substitution and insertion columns. So the index stores all strings obtained from each word by at most $k$ deletions, and a query looks up all strings obtained from $x$ the same way. The converse fails, so each hit needs a check: $\texttt{ab}$ and $\texttt{ba}$ both give $\texttt{a}$ after one deletion, but their distance is 2.

## Bounds

- **Output and input.** Each query reads $x$ and writes the answer, so it needs $\Omega(m + \mathrm{occ})$ time.
- **Size of the neighborhood.** A string within distance $k$ of $x$ comes from at most $k$ operations, and each operation is one of at most $(m + k + 1)(2\sigma + 1)$ choices: a position, and a deletion, one of $\sigma$ substitutions or one of $\sigma$ insertions. So at most $\sum_{i=0}^{k} ((m + k + 1)(2\sigma + 1))^i$ strings lie within distance $k$ of $x$, which is $O((m \sigma)^k)$ for a fixed $k$. Neighborhood generation is practical only for small $k$ and small alphabets.
- **Long words.** For $N = 1$, a query decides whether $d(x, w) \le k$ for one word $w$. So with words of unbounded length, a query is as hard as deciding the edit distance, which under the Strong Exponential Time Hypothesis has no algorithm in time $O(n^{2 - \varepsilon})$; see [edit distance hardness](/edit-distance-hardness/).

## Reductions

- **From edit distance.** The decision version of the [edit distance](/edit-distance/) problem is the case $N = 1$, as above.
- **To metric search.** The Levenshtein distance is a metric, so the problem is a range query in the [metric space](/metric-space/) $(\Sigma^*, d)$, and every [metric space index](/metric-space-indexing/), such as the [BK-tree](/bk-tree/), applies. A distance that breaks the triangle inequality, such as the optimal string alignment distance, cannot use these indexes.
- **To approximate string matching.** Concatenate the words with a separator $\$ \notin \Sigma$. A word is within distance $k$ of $x$ only if its region of the text holds an approximate occurrence of $x$, so [approximate string matching](/approximate-string-matching/) on the concatenation gives a set of candidates, which are then checked for the whole word.
- **To similarity joins.** Answering every word of a second set as a query is a [string similarity join](/string-similarity-join/).

## Applications

- **Spelling correction.** Kukich surveys the methods for isolated words: the misspelled word is the query, and the dictionary words within one or two edits are the suggestions, often ranked by frequency.
- **Search engines.** A query term with no or few results is replaced by a close term from the vocabulary.
- **Optical character recognition.** A recognized word is corrected to a close word of a lexicon, which is the setting of Schulz and Mihov.
- **Record matching.** Names and addresses with typing errors are matched against a reference list.
- **DNA barcodes.** Reads tagged with short barcodes are assigned to the barcode within a small Hamming or edit distance.

## References
