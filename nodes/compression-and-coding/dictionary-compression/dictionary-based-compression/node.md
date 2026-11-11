---
tag: ED51P9
kind: concept
slug: dictionary-based-compression
name: Dictionary-based compression
aliases:
- dictionary coding
- dictionary compression
- substitutional compression
area: compression-and-coding/dictionary-compression
level: intro
summary: Lossless compression that cuts the input into phrases and writes each phrase as a short reference to an entry of a dictionary that the decoder also has.
prereqs: [lossless-compression]
see_also: [static-dictionary-compression, adaptive-dictionary-compression, back-reference, lempel-ziv-parsing, optimal-parsing, grammar-based-compression, ziv-lempel-entropy-theorem, deflate]
sources:
  - book: isbn:9780139119910
    title: Timothy C. Bell, John G. Cleary and Ian H. Witten, Text Compression, Prentice Hall, 1990
    locator: the chapter on dictionary techniques (static, semi-adaptive and adaptive dictionaries, parsing strategies, and the LZ77 and LZ78 families)
  - book: isbn:9780128094747
    title: Khalid Sayood, Introduction to Data Compression, fifth edition, Morgan Kaufmann, 2017
    locator: Chapter 5, Dictionary Techniques (static dictionaries, LZ77, LZ78, LZW and their applications)
  - book: isbn:9781848829022
    title: David Salomon and Giovanni Motta, Handbook of Data Compression, fifth edition, Springer, 2010
    locator: Chapter 6, Dictionary Methods (Section 6.1 String Compression, Section 6.2 Simple Dictionary Compression, Section 6.3 LZ77)
  - paper: doi:10.1145/179812.179892
    title: Timothy C. Bell and Ian H. Witten, The relationship between greedy parsing and symbolwise text compression, Journal of the ACM 41(4), 1994
    locator: pages 708 to 724 (parsing methods against symbolwise methods)
  - paper: doi:10.1109/TIT.1977.1055714
    title: Jacob Ziv and Abraham Lempel, A universal algorithm for sequential data compression, IEEE Transactions on Information Theory 23(3), 1977
    locator: pages 337 to 343 (the sliding-window method, LZ77)
  - paper: doi:10.1109/TIT.1978.1055934
    title: Jacob Ziv and Abraham Lempel, Compression of individual sequences via variable-rate coding, IEEE Transactions on Information Theory 24(5), 1978
    locator: pages 530 to 536 (the incremental parsing method, LZ78)
---

Dictionary-based compression is a form of [lossless compression](/lossless-compression/) that cuts the input into phrases and writes each phrase as a reference to an entry of a *dictionary*, a set of strings that the encoder and the decoder both know. The output is shorter when a reference costs fewer bits than the phrase it stands for. The methods differ in where the dictionary comes from: it is fixed in advance ([static](/static-dictionary-compression/)), built for one message and sent first (semi-static), or built from the text already coded ([adaptive](/adaptive-dictionary-compression/)). The adaptive methods of Ziv and Lempel, [LZ77](/lz77/) and [LZ78](/lz78/), are the base of DEFLATE, LZ4, Zstandard, Brotli, LZMA and LZW.

## In plain words

Think of a text with many repeated words. You can give each common word a short number and write the numbers in place of the words. The reader has the same list of words, so the reader can turn the numbers back into words. That list is the dictionary.

There are two questions. The first is where the list comes from. It can be a list that both sides agreed on before, or a list that the writer makes from the text and sends first, or a list that both sides build as they go, from the text already written. The third way needs no extra data, and it adapts to any text.

The second question is how to cut the text into pieces that are in the list. Taking the longest piece each time is fast, but it is not always the best cut.

## The idea

Fix an alphabet $\Sigma$ of size $\sigma$ and a text $T = T[1..n] \in \Sigma^n$. A *dictionary* is a set $D \subseteq \Sigma^{+}$ of strings, each with a codeword $\mathrm{code}(w)$ that the decoder can read. To make every text codable, $D$ usually holds all single symbols. A *parse* of $T$ over $D$ is a factorization

$$T = w_1 w_2 \cdots w_k, \qquad w_j \in D \text{ for each } j,$$

and the output is $\mathrm{code}(w_1)\,\mathrm{code}(w_2) \cdots \mathrm{code}(w_k)$. Its length is $\sum_{j} |\mathrm{code}(w_j)|$ bits. The decoder replaces each codeword by its string. So the scheme is lossless when the sequence of codewords can be read back without ambiguity, for example when the codewords form a [prefix code](/prefix-code/).

**Two choices make a method.**

1. *The dictionary.* A **static** dictionary is the same for all inputs. A **semi-static** (semi-adaptive) dictionary is chosen for the input and sent before the codes. An **adaptive** dictionary is a function of the prefix $T[1..i-1]$ that is already coded, so the decoder can rebuild it with no side information.
2. *The parse.* For a given dictionary, [greedy parsing](/greedy-parsing/) takes the longest entry that matches at the current position. [Optimal parsing](/optimal-parsing/) minimizes the total number of output bits.

**Optimal parsing for a fixed dictionary is a shortest path.** Make a graph with nodes $1, 2, \ldots, n+1$. For each position $i$ and each $w \in D$ with $T[i..i+|w|-1] = w$, add an edge $i \to i + |w|$ with weight $|\mathrm{code}(w)|$. A parse is exactly a path from node 1 to node $n+1$, and its cost is the path weight. All edges go forward, so the graph is acyclic, and the [shortest path in a DAG](/dag-shortest-paths/) gives an optimal parse in time linear in the number of edges. With codewords of equal length, the optimal parse is the one with the fewest phrases.

**Greedy parsing is not optimal for every dictionary.** With $D = \{a, b, ab, bbbb\}$ and $T = abbbb$, greedy parsing takes $ab$, and then three single $b$ phrases, four phrases in all, while $a \cdot bbbb$ uses two. For the adaptive LZ77 dictionary (all substrings of the text before the current position), greedy parsing does give the fewest phrases; the [Lempel-Ziv factorization](/lempel-ziv-factorization/) page proves it. With variable-length codewords, even for LZ77, a parse with more phrases can cost fewer bits; that is the subject of [optimal LZ parsing](/optimal-lz-parsing/).

**The two adaptive families.**

- **LZ77 type.** The dictionary is the set of all substrings that start in a window of the recent text. A phrase is written as a [back-reference](/back-reference/) $(d, \ell)$: copy $\ell$ symbols from $d$ positions back. [LZ77](/lz77/) adds one literal symbol to each phrase, and [LZSS](/lzss/) writes either a literal or a pair. Finding the longest match is the [match finding](/match-finding/) problem.
- **LZ78 type.** The dictionary is an explicit list of phrases, stored in a [trie](/trie/). Each step writes the index of the longest phrase that matches and adds one new phrase. [LZ78](/lz78/) writes (index, next symbol), and [LZW](/lzw/) writes only indexes.

[Lempel-Ziv parsing](/lempel-ziv-parsing/) compares the parses of the two families on the same strings.

**A second stage.** A dictionary coder turns the text into a sequence of tokens (literals, lengths, distances, indexes). These tokens have a skewed distribution, so most modern formats code them with an entropy coder: [Huffman coding](/huffman-coding/) in DEFLATE, [range coding](/range-coding/) in LZMA, [asymmetric numeral systems](/asymmetric-numeral-systems/) and Huffman coding in Zstandard.

**Dictionary methods and statistical methods.** A statistical (symbolwise) method codes one symbol at a time from a probability model. Bell and Witten (1994) compare the two classes and conclude that work on better compression should go to symbolwise models, while parsing methods are chosen for speed and small memory. In the limit, the adaptive dictionary methods still reach the entropy rate of a stationary ergodic source; the [Ziv-Lempel entropy theorem](/ziv-lempel-entropy-theorem/) states this.

## Examples

**A static dictionary, greedy against optimal.** Let $D = \{a, b, ab, bbbb\}$ with 2-bit codes $a = 00$, $b = 01$, $ab = 10$, $bbbb = 11$. For $T = abbbb$ the greedy parse $ab \cdot b \cdot b \cdot b$ gives 8 bits, and the optimal parse $a \cdot bbbb$ gives 4 bits. The plain text needs 5 symbols of 1 bit each (the alphabet has two symbols), so here only the optimal parse saves bits.

**LZ77 on abracadabra.** The text $T = abracadabra$ has the repeat $abra$ at positions 1 and 8. The greedy LZ77 parse with an unbounded window writes the triples $(0,0,a)$, $(0,0,b)$, $(0,0,r)$, $(3,1,c)$, $(2,1,d)$, $(7,3,a)$. The last triple copies $abr$ from 7 positions back and adds $a$. See [LZ77](/lz77/) for the trace.

**LZ78 on the same text.** The LZ78 parse is $a \mid b \mid r \mid ac \mid ad \mid ab \mid ra$: seven phrases, each an earlier phrase plus one symbol. See [LZ78](/lz78/).

**A run.** For $T = a^8$ (eight copies of $a$), LZ77 writes $(0,0,a)$ and $(1,6,a)$: the second copy reads from 1 position back and overlaps the text it writes. LZ78 writes $a \mid aa \mid aaa \mid aa$. A run of $n$ equal symbols costs LZ77 a constant number of triples when the length field is large enough, while LZ78 needs about $\sqrt{2n}$ phrases. [Run-length encoding](/run-length-encoding/) is the special case of a back-reference with distance 1.

**A preset dictionary.** The zlib format (RFC 1950) lets the encoder start the LZ77 window with a preset dictionary that the decoder must also have; the stream names it by its Adler-32 checksum. This is a static dictionary in front of an adaptive one. See [static dictionary compression](/static-dictionary-compression/).

## Where it is used

- **General-purpose formats.** [DEFLATE](/deflate/) (zip, gzip, PNG, HTTP content coding), [LZ4](/lz4/), [Snappy](/snappy/), [LZO](/lzo/), [Zstandard](/zstandard/), [Brotli](/brotli/), [LZMA](/lzma/) and [LZX](/lzx/) are LZ77 coders with different match finders, parsers and entropy coders.
- **LZW.** The Unix `compress` program, the GIF image format, TIFF and the LZWDecode filter of PDF use [LZW](/lzw/).
- **Dictionaries made for a message.** [Grammar-based compression](/grammar-based-compression/), [Re-Pair](/re-pair/) and [byte pair encoding](/byte-pair-encoding/) build a set of phrases for the input and send it, which is the semi-static case.
- **String algorithms.** The number of phrases of the [Lempel-Ziv factorization](/lempel-ziv-factorization/) is a measure of repetition. It bounds the size of the smallest grammar and the smallest [string attractor](/string-attractor/), and it is the base of the [LZ-index](/lz-index/), of other [compressed indexes](/compressed-indexing/), and of [pattern matching in compressed text](/pattern-matching-in-compressed-text/).

Do not confuse this with [string compression by period](/string-compression-by-period/), which finds the shortest string whose repetition gives the input. That is one fixed kind of repetition, not a dictionary of phrases.

## References
