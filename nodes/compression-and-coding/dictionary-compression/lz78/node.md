---
tag: ZJ9XSK
kind: algorithm
slug: lz78
name: LZ78
aliases:
- Ziv-Lempel 1978
area: compression-and-coding/dictionary-compression
level: intro
summary: Adaptive dictionary coder that writes each phrase as the index of an earlier phrase plus one symbol, and adds the phrase to a trie.
solves: [lz78-parsing, lossless-compression]
model: word-ram
complexity:
  vars: {n: the length of the input, σ: the alphabet size, c: the number of phrases}
  time: {worst: O(n log σ), expected: O(n)}
  space: {aux: Θ(c)}
properties: {deterministic: true, recursive: false, online: true, comparison: false}
history:
  year: 1978
  people: [Jacob Ziv, Abraham Lempel]
  note: Ziv and Lempel defined incremental parsing and its coder in IEEE Transactions on Information Theory in 1978.
prereqs: [lz78-parsing, adaptive-dictionary-compression]
see_also: [lzw, lz77, trie, lz-index, ziv-lempel-entropy-theorem, lempel-ziv-parsing, pattern-matching-in-compressed-text, hash-table]
sources:
  - paper: doi:10.1109/TIT.1978.1055934
    title: Jacob Ziv and Abraham Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 1978
    locator: pages 530 to 536 (incremental parsing, the codeword of a phrase index and a symbol, and the comparison with finite-state encoders)
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Chapter 13, Universal Source Coding, Sections 13.4 and 13.5 (the tree-structured Lempel-Ziv algorithm and its optimality)
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, Morgan Kaufmann, 2017
    locator: Chapter 5, Dictionary Techniques (the LZ78 approach, with a worked example)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, fifth edition, Springer, 2010
    locator: Chapter 6, Dictionary Methods (LZ78 and its trie)
---

LZ78 is the second compressor of Ziv and Lempel (1978). It keeps an explicit dictionary of phrases, stored in a [trie](/trie/), and writes the text as pairs $(j, c)$: the index $j$ of the longest phrase in the dictionary that matches the text here, and the next symbol $c$. The new phrase, phrase $j$ followed by $c$, gets the next index. The phrases are those of [LZ78 parsing](/lz78-parsing/), and the method solves [lossless compression](/lossless-compression/) with an [adaptive dictionary](/adaptive-dictionary-compression/) that both sides build in the same way. [LZW](/lzw/) is its best known variant.

## In plain words

The coder and the reader each keep a numbered list of phrases. At the start the list holds only the empty phrase, number 0.

The coder reads the text and finds the longest phrase in the list that matches the text here. It writes the number of that phrase and the next letter. The phrase plus the letter is new, so both sides add it to the list under the next free number.

The reader gets a number and a letter. It looks up the phrase with that number, writes it and the letter, and adds the two together to its own list. So both lists stay the same, and the list is never sent.

Each new phrase is one letter longer than an old one, so the list learns long repeats slowly.

## The problem

The input is a string $T = T[1..n]$ over an alphabet $\Sigma$ of $\sigma$ symbols. The encoder writes a sequence of pairs $(j, c)$ with $j$ an index and $c \in \Sigma \cup \{\bot\}$, and the decoder must rebuild $T$ from them. In a bit stream, pair number $k$ needs $\lceil \log_2 k \rceil$ bits for $j$ (it is one of the $k$ phrases $0, \ldots, k-1$) and $\lceil \log_2 \sigma \rceil$ bits for $c$; both sides know $k$, so the width needs no signal.

## The algorithm

The trie has one node per phrase. Node 0 is the root, the empty phrase, and node $k$ is phrase $k$. The encoder walks down from the root along the text; when the next symbol has no child, it writes the pair and adds that child.

```pseudo id=main
LZ78-ENCODE(T)                             ▷ T[1 .. n]
L1  make a trie with only the root, node 0; next ← 1
L2  out ← the empty list; v ← 0
L3  for i ← 1 to n do
L4      if v has a child for T[i] then
L5          v ← that child
L6      else
L7          append (v, T[i]) to out
L8          add a child of v for T[i] with number next; next ← next + 1
L9          v ← 0
L10 if v ≠ 0 then append (v, ⊥) to out
L11 return out

LZ78-DECODE(pairs)
L12 P[0] ← the empty string; next ← 1
L13 for each pair (j, c) in order do
L14     w ← P[j] followed by c, or P[j] alone if c = ⊥
L15     output w; P[next] ← w; next ← next + 1
L16 return
```

Line L10 handles an input that ends inside a known phrase: the last pair has no symbol. The decoder needs only the array $P$ of phrases; storing each phrase as (parent index, last symbol) instead of as a string keeps its memory at $O(c)$ words, with each phrase written out by following the parents.

## Example

**abracadabra.** The pairs and the trie:

| $k$ | phrase | pair | new child |
|---|---|---|---|
| 1 | a | $(0, a)$ | node 1 under the root |
| 2 | b | $(0, b)$ | node 2 under the root |
| 3 | r | $(0, r)$ | node 3 under the root |
| 4 | ac | $(1, c)$ | node 4 under node 1 |
| 5 | ad | $(1, d)$ | node 5 under node 1 |
| 6 | ab | $(1, b)$ | node 6 under node 1 |
| 7 | ra | $(3, a)$ | node 7 under node 3 |

At $k = 6$ the walk goes from the root to node 1 on $a$, finds no child for $b$, writes $(1, b)$ and adds node 6. The decoder reads $(1, b)$, finds $P[1] = a$, writes $ab$ and sets $P[6] = ab$.

**aaaaaaaa.** The pairs are $(0, a)$, $(1, a)$, $(2, a)$, $(2, \bot)$: the phrases $a, aa, aaa$, and then the input ends inside phrase 2.

**abababab.** The pairs are $(0, a)$, $(0, b)$, $(1, b)$, $(3, a)$, $(2, \bot)$.

## Correctness

The encoder keeps two invariants at the top of line L3: the trie holds exactly the phrases written so far, each as the node with its number, and $v$ is the node of $T[p..i-1]$, where $p$ is the start of the current phrase. So when line L4 fails, $T[p..i-1]$ is the longest phrase in the dictionary that is a prefix of the rest of the text, and the pair $(v, T[i])$ is the LZ78 phrase. The decoder keeps the invariant that $P[k]$ is phrase $k$ and the output so far is phrases $1, \ldots, k$ in order. Since $j < k$ in each pair, $P[j]$ is known when it is needed. The full proof is below.

## Complexity

**Time.** The loop of line L3 runs $n$ times, and each round does one child lookup and at most one insertion. With a [hash table](/hash-table/) keyed by (node, symbol), this is $O(n)$ expected time. With an array of $\sigma$ children per node it is $O(n)$ worst-case time and $O(c\sigma)$ space; with a balanced search tree per node it is $O(n \log \sigma)$ time. The decoder takes $O(n)$ time to write the output.

**Space.** The trie has $c + 1$ nodes, where $c$ is the number of pairs, so the space is $\Theta(c)$ words. The bounds on [LZ78 parsing](/lz78-parsing/) give $\sqrt{2n} - O(1) \le c \le O(n / \log_\sigma n)$.

**Output size.** With the widths above the output has $\sum_{k=1}^{c} (\lceil \log_2 k \rceil + \lceil \log_2 \sigma \rceil) \le c (\log_2 c + \log_2 \sigma + 2)$ bits. For a stationary ergodic source, this divided by $n$ tends to the entropy rate; see the [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/).

## Properties

- **Lossless and deterministic.**
- **Online.** The encoder decides each pair after reading its last symbol, and the decoder writes each phrase as soon as it reads the pair.
- **No window.** Any earlier phrase can be used, however far back, but only whole phrases: a repeat that does not start at a phrase boundary is found only in part.
- **Memory grows.** The trie grows by one node per phrase with no limit; practical variants bound it.
- **Distinct phrases.** All phrases but possibly the last are distinct, which is the key to the bound on $c$ and to the entropy result.

## Variants and improvements

- **LZW.** Start the dictionary with all single symbols and write only indexes; the symbol of each pair moves into the next phrase. See [LZW](/lzw/).
- **Bounded dictionary.** When the table is full, freeze it, clear it and start again, or remove old phrases. Unix `compress` clears the table when the ratio drops, and GIF lets the encoder send a clear code.
- **Faster learning.** Some variants add more than one phrase per step, such as the concatenation of the last two phrases, so that repeats are learned faster.
- **Entropy-coded indexes.** The index can be coded with a model of how likely each phrase is, instead of $\lceil \log_2 k \rceil$ bits.
- **Indexes.** The [LZ-index](/lz-index/) keeps the LZ78 trie, and a second trie of the reversed phrases, to search the text in compressed form; see also [pattern matching in compressed text](/pattern-matching-in-compressed-text/).

## When to use it

Use LZ78 when you want an adaptive dictionary coder that is simple to analyze, with a single index per phrase and no search over a window, or when you need the trie of phrases itself, as in compressed indexes and in prediction. For general-purpose compression, LZ77-family formats with entropy coding give better results at a similar speed. No standard library has an LZ78 codec and there are no official test vectors; the reference implementation is tested by round trips and by parses worked out by hand.

## Pitfalls

- **The last phrase.** If the input ends inside a known phrase, the encoder must write it (line L10); a coder that writes pairs only in line L7 drops the end of the input.
- **Index width.** The encoder and the decoder must use the same width for pair $k$. An error of one in the count of phrases breaks the rest of the stream.
- **Unknown indexes.** A decoder must reject $j \ge k$ in pair $k$; such an index names a phrase that does not exist yet.
- **Memory.** On a long input the trie can use much memory; bound it, and say in the format what happens when it is full.
- **Repeats far apart and long.** LZ78 learns a repeat of length $\ell$ in about $\sqrt{2\ell}$ steps at best, so it compresses long exact repeats much worse than LZ77.

## Implementations

## History

Ziv and Lempel published LZ78 in 1978, a year after [LZ77](/lz77/). The paper defines incremental parsing and proves that, for every individual infinite sequence, the compression ratio of the method is asymptotically as good as that of any finite-state encoder. Terry Welch's variant [LZW](/lzw/) (1984) removed the explicit symbol from each pair; it became the method of Unix `compress` and of the GIF image format.

## References
