---
tag: HYAQNT
kind: problem
slug: lz78-parsing
name: LZ78 parsing
aliases:
- LZ78 factorization
area: compression-and-coding/dictionary-compression
level: intro
summary: Cut a string into phrases, each the longest earlier phrase that is a prefix of the rest plus one symbol, so that all phrases are distinct.
model: word-ram
complexity:
  vars: {n: the length of the string, σ: the alphabet size, c: the number of phrases}
  time: {worst: O(n log σ), expected: O(n)}
  space: {aux: Θ(c)}
prereqs: [lempel-ziv-parsing, trie]
see_also: [lz78, lzw, lempel-ziv-factorization, lz-index, ziv-lempel-entropy-theorem, lempel-ziv-complexity, adaptive-dictionary-compression, pattern-matching-in-compressed-text]
sources:
  - paper: doi:10.1109/TIT.1978.1055934
    title: Jacob Ziv and Abraham Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 1978
    locator: pages 530 to 536 (the incremental parsing into distinct phrases and the bound on their number)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 13, Universal Source Coding, Section 13.5 (the bound on the number of phrases of a distinct parsing, and the optimality of the tree-structured Lempel-Ziv algorithm)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, Cambridge University Press, 2016
    locator: the chapter on compressed text indexes (the LZ78 parsing and the trie of its phrases)
---

LZ78 parsing, also called incremental parsing, cuts a string from left to right into phrases. Each phrase is the longest *earlier phrase* that is a prefix of the rest of the string, followed by one more symbol, so every phrase is new and every prefix of a phrase is also a phrase. Ziv and Lempel defined it in 1978 as the parse of the [LZ78](/lz78/) compressor. It takes $O(n)$ trie steps, and a string of length $n$ over $\sigma \ge 2$ symbols has at most $O(n / \log_\sigma n)$ phrases.

## In plain words

Keep a list of phrases, which is empty at the start. Read the text. At each place, find the longest phrase in the list that matches the text here, and take one more letter after it. That new piece is the next phrase: it goes into the list, and you go on after it.

Each phrase is one letter longer than some earlier phrase, so every phrase is new. Long repeats are learned slowly: the phrases for a repeat grow by one letter at a time.

The list fits in a tree in which each phrase hangs below the phrase it extends. A walk down the tree finds the longest match, and the new phrase is a new leaf.

## Definition

**Input.** A string $T = T[1..n]$ over an alphabet $\Sigma$ with $\sigma$ symbols.

**Output.** Phrases $w_1, \ldots, w_c$ with $T = w_1 w_2 \cdots w_c$. Let $w_0 = \varepsilon$ be the empty phrase, and let $p_k = 1 + |w_1 \cdots w_{k-1}|$ be the start of $w_k$. Then $w_k = w_j \, T[p_k + |w_j|]$, where $w_j$ ($0 \le j < k$) is the longest phrase among $w_0, \ldots, w_{k-1}$ that is a prefix of $T[p_k..n]$. If the string ends inside a known phrase, the last phrase $w_c$ is that phrase with no extra symbol. Each phrase is reported as the pair $(j, a)$ of the index of $w_j$ and the added symbol $a$, with $a = \bot$ for a last phrase with no extra symbol.

**Two facts that follow.** The phrases $w_1, \ldots, w_{c-1}$ are distinct, and so is $w_c$ unless it has no extra symbol. The set $\{w_0, w_1, \ldots\}$ is closed under taking prefixes, since each $w_k$ is $w_j$ plus one symbol; so the phrases are the nodes of a [trie](/trie/) with $w_0$ at the root.

## Variants

- **LZW parsing.** The list starts with all $\sigma$ single symbols, a phrase is the longest entry that matches (with no extra symbol), and the entry added is the phrase followed by the next symbol. See [LZW](/lzw/).
- **Bounded dictionary.** A compressor stops adding phrases when the list is full, or clears the list and starts again; the parse then depends on the bound.
- **Other growth rules.** Some variants add more than one new phrase per step, for example the concatenation of the last two phrases, so that repeats are learned faster.
- **The LZ factorization.** If a phrase may copy *any* earlier substring, the parse becomes the [Lempel-Ziv factorization](/lempel-ziv-factorization/), with fewer phrases. [Lempel-Ziv parsing](/lempel-ziv-parsing/) compares the two.

## Examples

**abracadabra.** The phrases are

| $k$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $w_k$ | a | b | r | ac | ad | ab | ra |
| $(j, a)$ | (0, a) | (0, b) | (0, r) | (1, c) | (1, d) | (1, b) | (3, a) |

At $k = 6$ the rest of the text is $abra$; the phrase $ab$ is not yet in the list, so the longest match is $w_1 = a$ and the new phrase is $ab$.

**aaaaaaaa.** The phrases are $a \mid aa \mid aaa \mid aa$, as $(0, a)$, $(1, a)$, $(2, a)$, $(2, \bot)$: the text ends inside the known phrase $aa$.

**abababab.** The phrases are $a \mid b \mid ab \mid aba \mid b$, as $(0, a)$, $(0, b)$, $(1, b)$, $(3, a)$, $(2, \bot)$.

**A run.** For $T = a^n$ with $n = k(k+1)/2$, the phrases are $a, a^2, \ldots, a^k$, so $c = k \approx \sqrt{2n}$. The [Lempel-Ziv factorization](/lempel-ziv-factorization/) of the same run has 2 factors.

## Known algorithms

**Trie walk.** Keep the phrases in a trie. At each phrase start, walk down from the root while the child for the next symbol exists, then add a new child for the symbol that has no child. Each symbol of $T$ causes one step down or one new node, so there are exactly $n$ child operations and $c$ nodes. The [LZ78](/lz78/) page gives the pseudocode.

**Cost of a child operation.**

- An array of $\sigma$ children per node gives $O(1)$ per step, so $O(n)$ time, but $O(c \sigma)$ space.
- A hash table keyed by (node, symbol) gives $O(n)$ expected time and $O(c)$ space. The reference implementation does this.
- A balanced search tree or a sorted list per node gives $O(n \log \sigma)$ worst-case time and $O(c)$ space.

**Compact versions.** For indexes, the trie can be stored in succinct form; the [LZ-index](/lz-index/) stores the LZ78 trie and the trie of the reversed phrases in space close to that of the compressed text.

## Bounds

Let $c$ be the number of phrases and $c' \ge c - 1$ the number of distinct ones, with $\sigma \ge 2$.

**Upper bound, $c = O(n / \log_\sigma n)$ in the worst case.** *Proof.* For an integer $k \ge 1$, at most $\sigma + \sigma^2 + \cdots + \sigma^{k-1} \le \sigma^k$ distinct phrases are shorter than $k$, so at least $c' - \sigma^k$ phrases have length at least $k$, and $n \ge k (c' - \sigma^k)$. Take $k = \lfloor \log_\sigma (c'/2) \rfloor$, which is at least 1 when $c' \ge 2\sigma$. Then $\sigma^k \le c'/2$ and $k \ge \log_\sigma(c' / (2\sigma))$, so

$$c' \log_\sigma \frac{c'}{2\sigma} \le 2n.$$

If $c' \ge 2\sigma\sqrt{n}$, the logarithm is at least $\tfrac12 \log_\sigma n$, which gives $c' \le 4n / \log_\sigma n$. Otherwise $c' < 2\sigma\sqrt{n}$. So $c' \le \max(4n / \log_\sigma n,\ 2\sigma\sqrt{n})$. When $\sigma < \sqrt{n} / \log_2 n$, the second term is less than $2n / \log_2 n \le 2n / \log_\sigma n$. When $\sigma \ge \sqrt{n} / \log_2 n$, $\log_\sigma n \le 3$ for large $n$, and $c \le n$ is already $O(n / \log_\sigma n)$. $\square$

**Lower bound, $c = \Omega(\sqrt{n})$.** *Proof.* The distinct phrases form a prefix-closed set. If one of them has length $\ell$, its $\ell$ nonempty prefixes are distinct phrases of lengths $1, \ldots, \ell$; so the $i$-th shortest distinct phrase has length at most $i$, and the distinct phrases have total length at most $c'(c'+1)/2$. A repeated last phrase adds at most $c'$. So $n \le c'(c'+1)/2 + c'$. $\square$ The run $a^{k(k+1)/2}$ above meets the bound with $c = k$.

**Entropy.** For a stationary ergodic source, the code length of the LZ78 coder, about $c \log_2 c + c \log_2 \sigma$ bits, divided by $n$ tends to the entropy rate with probability 1. This is the [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/); the bound on $c$ above is one of its steps (Cover and Thomas, Section 13.5).

**Against the LZ factorization.** $z \le 2c$, where $z$ is the number of [Lempel-Ziv factors](/lempel-ziv-factor/); the [Lempel-Ziv factorization](/lempel-ziv-factorization/) page proves it. The run example shows that $c$ can be about $\sqrt{2n}$ while $z = 2$, so no bound of the form $c = O(z)$ holds.

## Reductions

- **To trie insertion.** The parse is $n$ child lookups and $c$ insertions in a trie; the time is that of the child dictionary.
- **To the LZ78 code.** The pairs $(j, a)$ are the output of the [LZ78](/lz78/) compressor; writing $j$ in $\lceil \log_2 k \rceil$ bits at step $k$ gives the code length used in the entropy bound.
- **To LZW.** The [LZW](/lzw/) parse is the same rule with the list started at all single symbols and with the added symbol moved to the start of the next phrase.

## Applications

- **Compression.** [LZ78](/lz78/) and [LZW](/lzw/) (Unix `compress`, GIF, TIFF, PDF) are this parse with a code for each phrase.
- **Compressed indexes.** The [LZ-index](/lz-index/) and related [compressed indexes](/compressed-indexing/) store the LZ78 trie, and [pattern matching in compressed text](/pattern-matching-in-compressed-text/) uses the fact that each phrase is an earlier phrase plus one symbol.
- **Entropy estimation and complexity.** The phrase count $c$ gives an estimate of the entropy rate of a sequence, and it is one form of [Lempel-Ziv complexity](/lempel-ziv-complexity/).
- **Prediction.** The phrase trie, with counts in its nodes, is a model for predicting the next symbol, used in universal prediction and in prefetching.

## References
