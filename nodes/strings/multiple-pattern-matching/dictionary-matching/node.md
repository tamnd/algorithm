---
tag: 6YANVC
kind: problem
slug: dictionary-matching
name: Dictionary matching
aliases:
- static dictionary matching
- keyword matching
area: strings/multiple-pattern-matching
level: advanced
summary: Multiple string matching against a fixed dictionary, preprocessed once, with fast queries on many texts.
model: word-ram
complexity:
  vars: {n: the length of a query text, m: the total length of the dictionary, z: the number of occurrences in the text}
  time: {build: O(m), query: O(n + z)}
  space: {extra: O(m)}
prereqs: [multiple-string-matching, trie]
see_also: [aho-corasick, dictionary-suffix-link, dynamic-dictionary-matching, two-dimensional-dictionary-matching, commentz-walter, wu-manber, perfect-hashing, approximate-dictionary-lookup]
sources:
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6) (1975), 333-340
    locator: the construction of the pattern matching machine from the keywords and its use on any text string
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 3.4, Exact matching with a set of patterns, and Section 7.2, APL2, Suffix trees and the exact set matching problem
  - url: https://arxiv.org/abs/1001.2860
    title: Djamal Belazzougui, Succinct dictionary matching with no slowdown, Combinatorial Pattern Matching (CPM 2010), Lecture Notes in Computer Science 6129, 88-100 (arXiv 1001.2860)
    locator: the abstract and the main theorem (the Aho-Corasick automaton in about one character code per state plus O(d log(m/d)) bits, with O(n + z) query time)
  - url: https://arxiv.org/abs/1504.06242
    title: Raphael Clifford, Allyx Fontaine, Ely Porat, Benjamin Sach and Tatiana Starikovskaya, Dictionary matching in a stream, Algorithms (ESA 2015), Lecture Notes in Computer Science 9294, 361-372 (arXiv 1504.06242)
    locator: the abstract and the main theorem (O(log log(d + ℓmax)) time per character and O(d log ℓmax) words of space, randomised)
---

Dictionary matching is [multiple string matching](/multiple-string-matching/) in which the set of patterns, the dictionary, is fixed in advance and preprocessed once, and then many texts arrive as queries. The goal is a structure of size $O(m)$ for a dictionary of total length $m$, built in $O(m)$ time, that reports all $z$ occurrences in a text of length $n$ in $O(n + z)$ time, independent of $m$ and of the number of patterns. The [Aho-Corasick automaton](/aho-corasick/) meets this goal and is the standard solution. Research on the problem studies the space of the structure, updates to the dictionary, streams and two dimensions.

## In plain words

A virus scanner has a list of a hundred thousand byte strings that mark known viruses. The list changes rarely, but the scanner reads millions of files. It should do the hard work on the list once, and then read each file quickly.

Dictionary matching is this task: prepare a fixed list of words once, so that for each new text you can quickly find every place where a word of the list occurs. The time to search a text should depend on the length of the text and on the number of hits, but not on how long the list is. The size of the prepared structure also matters, because the list may be large and must stay in memory.

## Definition

**Alphabet.** An integer [alphabet](/alphabet/) $\Sigma = \{0, \ldots, \sigma - 1\}$, with each character in one machine word. Indices are 0-based.

**Dictionary.** A list $\mathcal{D} = (P_0, \ldots, P_{d-1})$ of strings over $\Sigma$, of total length $m = \sum_j |P_j|$. Write $\ell_{\max}$ for the longest pattern length.

**Preprocessing.** Build a structure $S(\mathcal{D})$. Its costs are the build time and its size, in words or in bits.

**Query.** Given a text $T = T[0 \ldots n-1]$, report the set

$$\mathrm{Occ}(\mathcal{D}, T) = \{\, (s, j) : 0 \le j < d,\ 0 \le s \le n - |P_j|,\ T[s \ldots s + |P_j| - 1] = P_j \,\},$$

with $z = |\mathrm{Occ}(\mathcal{D}, T)|$. The query may read $S(\mathcal{D})$ and $T$ but not $\mathcal{D}$ itself, unless $S$ contains it.

**Conventions.** These are the conventions of multiple string matching. Occurrences may overlap and may lie inside each other. A pattern listed twice is reported once for each index. An empty pattern occurs at every $s$ from $0$ to $n$. The order of the output is free; a left-to-right scan reports by end position.

**The difference from multiple string matching.** There, one text and one set are given together, and the cost is $O(n + m + z)$ for both. Here the build cost is paid once, and each query should cost $O(n + z)$, with no term in $m$. So a solution that rebuilds anything of size $m$ for each text does not count, and the size of $S(\mathcal{D})$ becomes a measure of its own.

## Variants

- **Decision and first hit.** Does any pattern occur in $T$, and where does the first occurrence end? A scanner can stop at the first hit, so the time is $O(e)$ for the end position $e$ of that hit.
- **Longest match at each position.** For each end position $e$, report only the longest pattern that ends at $e$, or that starts at $e$. Tokenizers and dictionary-based parsers in the style of [LZ78](/lz78/) use these, and the output has size at most $n + 1$, whatever $z$ is.
- **Counting.** Report for each pattern its number of occurrences, in $O(n + m)$ time with the failure tree, or for each position the number of patterns that end there, in $O(n)$ time after storing at each node the number of patterns among its suffixes.
- **Compressed dictionary.** The structure must take space close to the information content of $\mathcal{D}$, in bits, while keeping the query time $O(n + z)$.
- **Dynamic dictionary.** Patterns are inserted and deleted between queries: [dynamic dictionary matching](/dynamic-dictionary-matching/).
- **Streaming.** The text arrives one character at a time, each occurrence must be reported when its last character arrives, and the space must be much smaller than $m$.
- **Two dimensions.** The patterns are matrices and the text is a matrix: [two-dimensional dictionary matching](/two-dimensional-dictionary-matching/).
- **Errors.** An occurrence may have a few mismatches or edits, or the query is a single word to be looked up with errors: [approximate dictionary lookup](/approximate-dictionary-lookup/).

## Examples

The dictionary of Aho and Corasick is $P_0$ = he, $P_1$ = she, $P_2$ = his, $P_3$ = hers. It is preprocessed once into a trie of 10 nodes, and then serves each of these queries.

| text | occurrences $(s, j)$ | $z$ | longest pattern ending at $e = 1, \ldots, n$ |
|---|---|---|---|
| ushers | (1, 1), (2, 0), (2, 3) | 3 | 0, 0, 0, 3, 0, 4 |
| hishers | (0, 2), (2, 1), (3, 0), (3, 3) | 4 | 0, 0, 3, 0, 3, 0, 4 |
| shehis | (0, 1), (1, 0), (3, 2) | 3 | 0, 0, 3, 0, 0, 3 |
| hhhh | none | 0 | 0, 0, 0, 0 |

In hishers, the occurrence of she at 2 overlaps his at 0, and he at 3 is a prefix of hers at 3. The last column is the longest-match variant: at the end position 4 of hishers, both she and he end, and only she, of length 3, is reported. The query cost on hhhh is 4 steps of the automaton with no output; it does not depend on the size of the dictionary.

## Known algorithms

- **[Aho-Corasick](/aho-corasick/).** Build the trie with [failure links](/failure-link/) and [dictionary suffix links](/dictionary-suffix-link/) in $O(m)$ steps; answer a query in $O(n + z)$ steps. With a static [perfect hash table](/perfect-hashing/) for the children of each node, the build takes $O(m)$ expected time, every child lookup takes $O(1)$ time in the worst case, and so the query takes $O(n + z)$ time in the worst case. The size is $O(m)$ words.
- **The full automaton.** Store the transition $\delta(v, a)$ for every node $v$ and character $a$, as a [deterministic finite automaton](/deterministic-finite-automaton/): $O(m\sigma)$ space, and exactly one table lookup per text character, which gives a constant time per character instead of the amortized constant of the failure links.
- **Skipping algorithms.** [Commentz-Walter](/commentz-walter/), [Set Horspool](/set-horspool/) and [Wu-Manber](/wu-manber/) preprocess the reversed patterns or blocks of characters and skip parts of the text. On random text with long patterns they read far fewer than $n$ characters on average, but their worst cases are larger than $O(n + z)$ in their basic forms.
- **Hashing, for one pattern length.** If all patterns have the same length $\ell$, store their fingerprints in a [hash table](/hash-table/) and look up the rolling fingerprint of each text window: [Karp-Rabin with many patterns](/karp-rabin-multiple-patterns/), with $O(n)$ expected query time plus verification.
- **Succinct Aho-Corasick.** Belazzougui (2010) stores the Aho-Corasick automaton of a dictionary with $M$ trie nodes in $M(\log_2 \sigma + O(1)) + O(d \log(m/d))$ bits and still answers queries in $O(n + z)$ time; with a small alphabet, the first term can be reduced to the empirical entropy of the trie labels.
- **Streaming.** Clifford, Fontaine, Porat, Sach and Starikovskaya (2015) give a randomized algorithm with $O(\log \log(d + \ell_{\max}))$ time per character and $O(d \log \ell_{\max})$ words of space, which is much less than $m$ when the patterns are long.

## Bounds

- **Query lower bound.** A query must write $z$ pairs and, in the worst case, read the whole text: with a single pattern, any algorithm reads at least $n - \ell + 1$ characters of the text in the worst case, by the [string matching lower bound](/string-matching-lower-bound/). So $\Omega(n + z)$ for $n \ge 2\ell_{\max}$, and Aho-Corasick with perfect hashing is optimal.
- **Build lower bound.** Each character of each pattern can change the answer to some query, so the build must read all $m$ characters: $\Omega(m)$.
- **Space.** A structure that answers all queries determines the set of distinct patterns, because the query on $T = P_j$ reveals whether $P_j$ is in the set. So its size in bits is at least the logarithm of the number of possible dictionaries, which for a trie with $M$ nodes is about $M \log_2 \sigma$ bits when $\sigma$ is large. The succinct Aho-Corasick structure reaches this order.
- **Average case.** On random text, any algorithm must read $\Omega(n \log_\sigma(d\ell)/\ell)$ characters on average for $d$ random patterns of length $\ell$ (Navarro and Fredriksson); see [multiple string matching](/multiple-string-matching/).

## Reductions

- **To multiple string matching.** Each query is an instance of multiple string matching with the same set. A per-query algorithm in $O(n + m + z)$ gives a dictionary solution with no build and $O(n + m + z)$ queries; the preprocessed form removes the $m$.
- **From multiple string matching.** Build $S(\mathcal{D})$ and run one query: $O(m + n + z)$. So the two problems have the same total cost for one text.
- **The other preprocessing.** If the text is fixed and the patterns vary, the roles swap: build a [suffix tree](/suffix-tree/) of the text and search each pattern in it, in $O(|P_j| + z_j)$ time for $z_j$ occurrences (Gusfield, Section 7.2). Dictionary matching is the case where the patterns are the fixed part.
- **Two dimensions.** Matching the rows of a set of matrix patterns is a dictionary query on each row of the text matrix; the [Bird-Baker](/bird-baker/) method and the Amir-Farach algorithm build on it.

## Applications

- **Malware and intrusion detection.** Antivirus engines and network intrusion detection systems match files and packet payloads against fixed sets of signatures; the sets change by occasional updates, and the scans are continuous.
- **Text search tools.** `grep -F -f wordlist` searches many files with one fixed list of strings.
- **Filtering.** Spam and content filters check messages against fixed lists of words or URLs.
- **Biology.** Search many sequencing reads for a fixed set of adapters, barcodes or primers.
- **Compression and parsing.** Dictionary-based parsers find the longest dictionary word at each position.

## References
