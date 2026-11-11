---
tag: D6TXZ9
kind: algorithm
slug: tunstall-coding
name: Tunstall coding
aliases:
- Tunstall code
area: compression-and-coding/entropy-coding
level: advanced
summary: "Variable-to-fixed code: split the most probable dictionary word while the words fit in 2^B, then parse the input into words and send each as a B-bit index."
solves: [lossless-compression]
model: word-ram
complexity:
  vars: {M: the number of dictionary words (at most 2^B), n: the length of the message}
  time: {worst: O(M log M + n), average: O(M log M + n)}
  space: {extra: Θ(M)}
properties: {deterministic: true, recursive: false, comparison: true}
history:
  year: 1967
  people: [Brian P. Tunstall]
  note: Tunstall gave the construction in his 1967 Ph.D. thesis at the Georgia Institute of Technology. Jelinek and Schneider studied variable-length-to-block codes in 1972.
prereqs: [prefix-code, shannon-entropy, huffman-coding]
see_also: [arithmetic-coding, lzw, lz78, source-coding-theorem, variable-length-code, kraft-inequality, golomb-coding, run-length-encoding]
sources:
  - paper: "Brian P. Tunstall, Synthesis of noiseless compression codes, Ph.D. thesis, Georgia Institute of Technology, 1967"
    title: Synthesis of noiseless compression codes
    locator: the whole thesis (the dictionary built by splitting the most probable word)
  - paper: doi:10.1109/tit.1972.1054899
    title: Frederick Jelinek and Kenneth S. Schneider, On variable-length-to-block coding, IEEE Transactions on Information Theory 18(6), 1972
    locator: pages 765 to 774
---

Tunstall coding is a variable-to-fixed code for a memoryless source. Where a [Huffman code](/huffman-coding/) maps each source symbol to a codeword of variable length, a Tunstall code maps source words of variable length to codewords of one fixed length $B$. The dictionary of source words is built as a tree. Start with the single symbols and, while one more split still fits in $2^B$ words, replace the most probable word by its one-symbol extensions. The words are the leaves of a full tree, so the dictionary is *complete* and *proper*: every long enough string starts with exactly one word, and the input is cut into words in only one way. Among all such dictionaries of the same size, the Tunstall dictionary has the longest mean word, and the bits per source symbol tend to the [entropy](/shannon-entropy/) $H$ as $B$ grows. Tunstall gave the method in his 1967 thesis.

## In plain words

You want to send text with codewords that all have the same number of bits, say 3 bits, so 8 codewords. Each codeword will stand for a piece of the text, and common pieces should be long, so that each codeword carries a lot of text.

Start with one piece for each letter. Then take the most likely piece and replace it by itself followed by each letter. Do that again and again while the pieces still fit in your 8 codewords.

The pieces now have a useful property. If you read the text from the start, exactly one piece matches, so cutting the text into pieces is easy and has only one answer. Number the pieces, and send the number of each piece in 3 bits. The receiver looks the numbers up in the same list.

## The algorithm

The input is the probabilities $p(s) > 0$ of the $\sigma$ source symbols, with sum 1, and the codeword length $B$, with $2^B \ge \sigma$. The probability of a word is the product of the probabilities of its symbols. A word $x$ followed by a symbol $s$ is written $xs$.

```pseudo id=main
TUNSTALL(p[1 .. σ], B)
L1  D ← the σ one-symbol words, in a max-priority queue keyed by probability
L2  while |D| + σ − 1 ≤ 2^B do
L3      x ← the most probable word in D; remove x from D
L4      for each symbol s do insert xs into D, with P(xs) = P(x) p(s)
L5  number the words of D in a fixed order; word i gets the B-bit codeword i
```

```pseudo id=parse
ENCODE(text, D)
P1  u ← the empty word
P2  for each symbol s of text do
P3      u ← us
P4      if u is a word of D then output its codeword; u ← the empty word
P5  if u is not empty then extend u with the symbol 0 until it is a word of D, and output its codeword
P6  send the length of text as well; the decoder outputs the words of its codewords and cuts at that length
```

Line L2 allows a split only if the dictionary still fits in $2^B$ words after it. A split adds $\sigma - 1$ words, so the final size $M$ satisfies $2^B - \sigma + 1 < M \le 2^B$. For a binary source $M = 2^B$ exactly; for larger alphabets up to $\sigma - 2$ codewords stay unused.

The words are the leaves of a tree whose inner nodes are the words that were split, together with the empty word at the root. Each inner node has all $\sigma$ children. For the parse, keep the tree as a trie and walk down it, one symbol at a time: an inner node always has a child for the next symbol, and a leaf is a word. At the end of the text the walk may stop at an inner node, so line P5 pads it with a fixed symbol, and line P6 lets the decoder drop the padding. A reserved codeword or an outer layer that knows the length works as well.

**Mean word length.** Each word $x$ is the first word of the parse with probability $P(x)$. The expected number of source symbols per codeword is $E[L] = \sum_x P(x) |x|$, and it is also the sum of the probabilities of the inner nodes, the root included. Each split adds the probability of the split word to $E[L]$, and the algorithm always adds the largest one it can. The rate is $B / E[L]$ bits per source symbol.

## Example

A binary source with $P(a) = 0.7$ and $P(b) = 0.3$, so $H \approx 0.8813$ bits per symbol, and $B = 3$, so 8 codewords.

| step | split | its probability | words after the step |
|---|---|---|---|
| start | | | a 0.7, b 0.3 |
| 1 | a | 0.7 | aa 0.49, ab 0.21, b 0.3 |
| 2 | aa | 0.49 | aaa 0.343, aab 0.147, ab, b |
| 3 | aaa | 0.343 | aaaa 0.2401, aaab 0.1029, aab, ab, b |
| 4 | b | 0.3 | aaaa, aaab, aab, ab, ba 0.21, bb 0.09 |
| 5 | aaaa | 0.2401 | aaaaa 0.16807, aaaab 0.07203, aaab, aab, ab, ba, bb |
| 6 | ab | 0.21 | aaaaa, aaaab, aaab, aab, aba 0.147, abb 0.063, ba, bb |

At step 6 the words ab and ba tie at 0.21; the implementation takes the first in alphabetical order, and either choice gives the same mean length. After step 6 the dictionary has 8 words and a further split would make 9, so the loop stops. In alphabetical order the codewords are:

| word | aaaaa | aaaab | aaab | aab | aba | abb | ba | bb |
|---|---|---|---|---|---|---|---|---|
| codeword | 000 | 001 | 010 | 011 | 100 | 101 | 110 | 111 |

The inner nodes are the root, a, aa, aaa, aaaa, b and ab, so $E[L] = 1 + 0.7 + 0.49 + 0.343 + 0.2401 + 0.3 + 0.21 = 3.2831$ symbols per codeword. The rate is $3 / 3.2831 \approx 0.9138$ bits per symbol. A Huffman code on single symbols needs 1 bit per symbol here, and a Huffman code on pairs of symbols, with lengths 1, 2, 3, 3 for aa, ab, ba, bb, needs $1.81 / 2 = 0.905$.

The text aaaaa aab ba abb aaab, 17 symbols, is cut into 5 words and sent as 000 011 110 101 010, 15 bits. The text bbaa ends at the inner node aa after the word bb; it is padded to aaaaa and sent as 111 000 with the length 4.

Larger dictionaries come closer to $H$, but not at every step:

| $B$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 10 |
|---|---|---|---|---|---|---|---|---|
| bits per symbol | 0.9132 | 0.9138 | 0.9038 | 0.8990 | 0.8951 | 0.8929 | 0.8919 | 0.8898 |

## Correctness

Each split turns a leaf into an inner node with all its children, so the words stay the leaves of a full tree. Walking down that tree along any long enough string reaches exactly one leaf, which gives the unique parse, and the decoder only concatenates words. The mean word length is the sum of the inner node probabilities. The algorithm splits a node of the largest probability among all nodes not yet split, because every other node lies below a current leaf, and probabilities do not grow down a path. So no complete proper dictionary of the same size has a longer mean word. Since the words are independent, the entropy of a word is $H \cdot E[L]$, which is at most $B$, so the rate $B / E[L]$ is at least $H$. Every inner node is at least as probable as every leaf, and this gives an upper bound on the rate that tends to $H$. The full proofs are in proofs/correctness.md.

## Complexity

- **Building the dictionary.** About $M / (\sigma - 1)$ splits, each with one removal and $\sigma$ insertions in a binary heap: $O(M \log M)$ time and $\Theta(M)$ space for the tree.
- **Encoding.** One step down the trie per source symbol and one codeword per word: $O(n)$ time for a text of $n$ symbols, with the trie children in arrays of size $\sigma$.
- **Decoding.** One table lookup per codeword, which yields a whole word: $O(n)$ time. A table of $2^B$ words, each up to the depth of the tree, is all the decoder needs.
- **Rate.** At least $H$ and at most $H B / (\log_2 M - \log_2 (1 / p_{\min}))$, where $p_{\min}$ is the smallest symbol probability. The distance to $H$ thus falls like $1 / B$.

## Properties

- **Variable-to-fixed.** Source words of different lengths, codewords of one length $B$. Huffman and [arithmetic coding](/arithmetic-coding/) go the other way, or have no fixed boundaries at all.
- **Complete and proper dictionary.** The words form the leaves of a full $\sigma$-ary tree, so every text has one parse.
- **Optimal among such dictionaries.** For a memoryless source, no complete proper dictionary with $M$ words has a larger mean word length.
- **Close to the entropy.** The rate tends to $H$ as $B$ grows, as the [source coding theorem](/source-coding-theorem/) allows; it is never below $H$.
- **Not monotone.** A larger $B$ can give a slightly worse rate, as from $B = 2$ to $B = 3$ in the example.
- **Errors stay local.** A bit error changes one codeword and so one word of output, and the codeword boundaries stay in place.
- **Inner nodes outweigh leaves.** At every step every inner node is at least as probable as every leaf; the rate bound comes from this.

## Variants and improvements

- **Huffman's dual.** A Huffman code fixes the source words, the symbols, and chooses codeword lengths; a Tunstall code fixes the codeword length and chooses source words. Huffman's algorithm builds its tree from the bottom by merging, Tunstall's from the top by splitting.
- **Variable-to-variable codes.** Code the Tunstall words with a Huffman code instead of fixed indices. This mixes both kinds of code and can lower the rate further.
- **Spare codewords.** When $M < 2^B$, the unused codewords can mark the end of the text or carry an escape, which removes the need to send the length.
- **Adaptive dictionaries.** [LZ78](/lz78/) and [LZW](/lzw/) are variable-to-fixed in each phase too, but they grow their dictionary from the text itself and need no model of the source.
- **Sources with memory.** For a Markov source, the probability of a word depends on the state, and the construction must take the state into account.

## When to use it

Use a Tunstall code when a fixed codeword length helps more than the last fraction of a bit per symbol. Decoding is one table lookup per codeword, with no bit-by-bit work, and it outputs several symbols at a time. Fixed codewords also keep bit errors from spreading and make it easy to jump to the $k$-th codeword. It suits skewed sources with few symbols, such as a binary source, where coding symbol by symbol cannot go below 1 bit per symbol. If the rate matters most, [arithmetic coding](/arithmetic-coding/) gets closer to $H$; if the source model is unknown, an adaptive dictionary method such as LZW fits better.

## Pitfalls

- **The tail.** The text can end inside a word, at an inner node of the tree. Pad it and send the length, or reserve a codeword for the end.
- **Not a Huffman code.** Do not merge the two least probable words; the Tunstall tree grows from the root by splitting the most probable one.
- **The size test.** Split only while the dictionary after the split fits in $2^B$ words; for $\sigma > 2$ the dictionary usually has fewer than $2^B$ words, and $2^B$ must be at least $\sigma$.
- **Ties.** Different tie rules give different dictionaries with the same mean length. The encoder and the decoder must build the same one, so fix the rule and the order of the words, or send the dictionary.
- **Floating point.** Products of many probabilities lose precision, which can change the order of near ties. Use the same arithmetic on both sides, or logarithms with a fixed tie rule.
- **Large $B$.** The dictionary has up to $2^B$ words, so memory grows fast while the gain in rate falls like $1 / B$.

## Implementations

## History

Brian P. Tunstall gave the construction in his Ph.D. thesis at the Georgia Institute of Technology in 1967. Jelinek and Schneider (1972) studied variable-length-to-block coding in the IEEE Transactions on Information Theory. The Tunstall code is the standard example of a variable-to-fixed code and the counterpart of the Huffman code, which is fixed-to-variable.

## References
