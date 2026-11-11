---
tag: C1843X
kind: concept
slug: adaptive-dictionary-compression
name: Adaptive dictionary compression
aliases:
- adaptive dictionary
area: compression-and-coding/dictionary-compression
level: intro
summary: Dictionary compression in which the dictionary is built from the text already coded, so the decoder rebuilds it and no dictionary is sent.
prereqs: [dictionary-based-compression]
see_also: [static-dictionary-compression, lz77, lz78, lzw, back-reference, lempel-ziv-parsing, ziv-lempel-entropy-theorem, match-finding]
sources:
  - book: isbn:9780139119910
    title: Timothy C. Bell, John G. Cleary and Ian H. Witten, Text Compression, Prentice Hall, 1990
    locator: the chapter on dictionary techniques (adaptive dictionary encoders, the LZ77 and LZ78 families)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, fifth edition, Springer, 2010
    locator: Chapter 6, Dictionary Methods (Section 6.3 LZ77, Section 6.4 LZSS, Section 6.13 LZW)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding-window dictionary)
  - paper: doi:10.1109/TIT.1978.1055934
    title: Jacob Ziv and Abraham Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 1978
    locator: pages 530 to 536 (the incremental parsing dictionary)
  - paper: doi:10.1109/MC.1984.1659158
    title: Terry A. Welch, A Technique for High-Performance Data Compression, IEEE Computer 17(6), 1984
    locator: pages 8 to 19 (the string table that starts with all single symbols)
---

Adaptive dictionary compression is [dictionary-based compression](/dictionary-based-compression/) in which the dictionary at each step is a function of the text already coded. The decoder sees the same text in the same order, so it builds the same dictionary, and the message carries no dictionary. All Lempel-Ziv methods work this way: in the [LZ77](/lz77/) family the dictionary is the recent text itself, and in the [LZ78](/lz78/) family it is a list of phrases that grows by one entry per step.

## In plain words

The writer and the reader start with the same empty list, or with a list of single letters. The writer codes the first part of the text with that list. Then both of them add to the list from the text that they now both know. The writer never sends the list, because the reader can make it from the same text.

So the list fits the text without any work from the user. A file of program code gets a list of program words, and a file of numbers gets a list of number patterns.

The cost is that the list starts small. The first part of each text compresses badly. Also, the two sides must stay in step: if one bit of the message is wrong, the reader builds a different list, and the rest of the text is wrong too.

## The idea

Write $T = w_1 w_2 \cdots w_k$ for the parse and $p_j = |w_1 \cdots w_{j-1}|$ for the length of text coded before phrase $j$. An adaptive method fixes a rule $D_j = F(T[1..p_j])$ that gives the dictionary from the coded prefix. The encoder picks $w_j \in D_j$ (usually the longest match) and writes its code. The decoder knows $T[1..p_j]$, computes the same $D_j$, and reads $w_j$ from the code. Correct decoding needs only that $F$ is a fixed, deterministic rule that both sides apply.

**Two rules for $F$.**

| | LZ77 family | LZ78 family |
|---|---|---|
| Dictionary $D_j$ | all substrings that start in the last $W$ positions of the coded text | the phrases $w_1, \ldots, w_{j-1}$ (plus the single symbols in [LZW](/lzw/)) |
| Size | up to $W$ start points, many lengths each | one entry per phrase |
| A reference | a [back-reference](/back-reference/) $(d, \ell)$ | an index into the phrase list |
| Encoder work | find the longest match in the window ([match finding](/match-finding/)) | walk down a [trie](/trie/) of the phrases |
| Decoder work | copy $\ell$ symbols | look up the phrase by index |
| Examples | [LZ77](/lz77/), [LZSS](/lzss/), [DEFLATE](/deflate/), [LZ4](/lz4/), [Zstandard](/zstandard/), [LZMA](/lzma/) | [LZ78](/lz78/), [LZW](/lzw/), Unix `compress`, GIF |

In the LZ77 family the dictionary holds every substring of the window at no cost, but a reference must name both a position and a length. In the LZ78 family a reference is a single index, but the dictionary grows by only one phrase per step, so it learns a long repeat slowly: a run of $n$ equal symbols takes about $\sqrt{2n}$ LZ78 phrases and $O(1)$ LZ77 references.

**Bounded memory.** A real coder cannot keep an unbounded dictionary. The LZ77 family uses a sliding window of the last $W$ symbols, so old text drops out by itself. The LZ78 family must choose what to do when the phrase table is full: stop adding phrases (freeze), clear the table and start again (reset, as in GIF and `compress`), or remove old entries. Each choice is a part of the format, since the decoder must do the same.

**Universality.** For any stationary ergodic source, the number of bits per symbol of the LZ77 and LZ78 coders tends to the entropy rate as the input grows, with no model of the source given in advance. The [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/) states the result. The convergence is slow, which is one reason why practical coders add an entropy coder on the tokens.

**Combined with a static start.** An adaptive coder can begin with a [static dictionary](/static-dictionary-compression/) in place of an empty one. The zlib preset dictionary, the Brotli built-in dictionary and Zstandard dictionaries all do this, which helps short messages.

## Examples

**LZ77 on abracadabra.** Before position 8 the coded text is $abracad$, and the dictionary is the set of substrings that start in it. The rest of the input is $abra$. Each LZ77 triple ends with one literal symbol, so here the copy is at most 3 symbols long. The longest match is $abr$ at distance 7, and the triple is $(7, 3, a)$.

**LZ78 on abracadabra.** The phrase list grows as $a$, $b$, $r$, $ac$, $ad$, $ab$, $ra$. At each step the encoder finds the longest phrase in the list that matches, writes its index and the next symbol, and adds the two together as a new phrase.

**LZW on abababab.** The table starts with the 256 byte values. The encoder writes the codes 97, 98, 256, 258, 98 and adds $ab = 256$, $ba = 257$, $aba = 258$, $abab = 259$. Code 258 is used one step after it is made, before the decoder has it in its table; [LZW](/lzw/) shows how the decoder handles this case.

## Where it is used

- **General-purpose compression.** Nearly every file and stream compressor in use is an adaptive dictionary coder of the LZ77 family with an entropy coder on the tokens: gzip and zip ([DEFLATE](/deflate/)), [Zstandard](/zstandard/), [Brotli](/brotli/), xz and 7-Zip ([LZMA](/lzma/)), [LZ4](/lz4/) and [Snappy](/snappy/).
- **The LZ78 family.** [LZW](/lzw/) in Unix `compress`, the GIF image format, TIFF and the LZWDecode filter of PDF, and the ITU-T V.42bis modem standard.
- **Measures of repetition.** The phrase count of an adaptive parse is a measure of the repetition in a string; see [Lempel-Ziv parsing](/lempel-ziv-parsing/) and [Lempel-Ziv complexity](/lempel-ziv-complexity/).

## References
