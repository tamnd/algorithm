---
tag: M6D811
kind: definition
slug: prefix-code
name: Prefix code
aliases:
- prefix-free code
- instantaneous code
area: compression-and-coding/entropy-coding
level: intro
summary: A code in which no codeword is a prefix of another. Each codeword is decoded as soon as its last bit arrives, by a walk in a code tree or by a table lookup.
prereqs: [binary-tree]
see_also: [kraft-inequality, uniquely-decodable-code, variable-length-code, huffman-coding, canonical-huffman-code, trie, deflate, elias-gamma-coding]
sources:
  - book: isbn:9780471241959
    title: Thomas M. Cover and Joy A. Thomas, Elements of Information Theory, second edition, Wiley, 2006
    locator: Section 5.1 (the definition of a prefix or instantaneous code, and Table 5.1 of the classes of codes) and Section 5.2 (the code tree and the Kraft inequality)
  - book: isbn:9780521642989
    title: David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003
    locator: Chapter 5, Symbol codes (prefix codes, their binary trees, and complete codes)
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: P. Deutsch, DEFLATE Compressed Data Format Specification version 1.3, RFC 1951, 1996
    locator: Section 3.2.2 (prefix codes as binary trees, and the codes rebuilt from their bit lengths)
---

A prefix code is a code in which no codeword is a prefix of another codeword. Because of this, a decoder that reads the encoded bits from left to right knows that a codeword has ended at the moment its last bit arrives, with no look-ahead and no separators. That is why prefix codes are also called *instantaneous* codes. The codewords are the leaves of a code tree, and decoding is a walk from the root to a leaf, or one lookup in a table. Prefix codes lose nothing against the larger class of [uniquely decodable codes](/uniquely-decodable-code/), so almost every practical variable-length code is a prefix code.

## Definition

Notation. $\Sigma$ is the source alphabet, of size $\sigma$. The code alphabet is $\{0, 1\}$; everything below also holds with $D$ code letters and $D$-ary trees. A code is a map $C : \Sigma \to \{0, 1\}^+$ that sends each symbol to a nonempty codeword, and a message $x_1 \cdots x_n$ is encoded as $C(x_1) \cdots C(x_n)$. $\ell(x) = |C(x)|$ is the length of the codeword of $x$. No probability model is needed for the definition.

**Definition.** $C$ is a *prefix code* (or *prefix-free code*) if, for all $x \ne y$ in $\Sigma$, $C(x)$ is not a prefix of $C(y)$. In particular the codewords are distinct.

**Instantaneous decoding.** A code is *instantaneous* if every codeword in an encoded stream can be recognized as soon as its last bit is read, without reading any bit after it. A code is instantaneous if and only if it is a prefix code.

*Proof.* If $C$ is prefix-free and the decoder has read the bits $b_1 \cdots b_t$ since the end of the last codeword, then at most one codeword equals $b_1 \cdots b_t$, and if one does, no other codeword starts with it. So the decoder can output that symbol at once, and it is correct, since the true codeword at this point starts with $b_1 \cdots b_t$ and is a codeword. Conversely, if $C(x)$ is a proper prefix of $C(y)$, a decoder that has read exactly $C(x)$ cannot tell whether the symbol is $x$ or the start of $y$ without reading further. $\square$

**The code tree.** Put the codewords in a binary [trie](/trie/): from the root, the bit 0 goes to the left child and the bit 1 to the right child. The codeword $C(x)$ is the node at the end of its path. The code is prefix-free exactly when no codeword is an ancestor of another, that is, when every codeword is a leaf of the trie made of the codewords and their prefixes. The length $\ell(x)$ is the depth of the leaf.

**Completeness.** A binary prefix code is *complete* if every internal node of its code tree has two children. Then every infinite bit string starts with exactly one codeword, the decoder never meets a bit pattern that has no meaning, and the [Kraft sum](/kraft-inequality/) $\sum_x 2^{-\ell(x)}$ equals 1. If the code is not complete, the sum is less than 1, some bit patterns are errors, and some codewords can be made shorter.

### Decoding

**Tree walk.** Start at the root. For each input bit, go to the left or right child. At a leaf, output its symbol and go back to the root. Decoding $n$ symbols takes one step per bit, $\sum_i \ell(x_i)$ steps in total. If the code is not complete, a step to a child that does not exist is a decoding error.

**Table lookup.** Let $L = \max_x \ell(x)$. Build a table $T$ of $2^L$ entries. For each symbol $x$, the $2^{L - \ell(x)}$ entries whose index starts with the bits of $C(x)$ hold the pair $(x, \ell(x))$. To decode, peek at the next $L$ bits (pad with zeros at the end of the stream), read $(x, \ell) = T[\text{bits}]$, output $x$ and consume only $\ell$ bits. This decodes one symbol per lookup. The entries of a complete code fill the table exactly, by the Kraft sum. When $L$ is large, decoders use a first table indexed by a few bits and smaller second-level tables for the long codewords; the DEFLATE decoder in zlib works this way.

**No loss against uniquely decodable codes.** Every prefix code is uniquely decodable. Conversely, by McMillan's theorem the lengths of any uniquely decodable code satisfy the Kraft inequality, and by Kraft's construction there is then a prefix code with the same lengths (see [Kraft inequality](/kraft-inequality/)). So, for any cost that depends only on the lengths, such as the mean length under a probability law, the best prefix code is as good as the best uniquely decodable code. [Huffman coding](/huffman-coding/) finds the best one.

## Examples and non-examples

**A complete code.** $C(a) = 0$, $C(b) = 10$, $C(c) = 110$, $C(d) = 111$. Its Kraft sum is $1/2 + 1/4 + 1/8 + 1/8 = 1$, so it is complete. The message $abacd$ is encoded as $0 \, 10 \, 0 \, 110 \, 111 = 0100110111$. The decoder reads 0 and outputs $a$; reads 1, then 0, and outputs $b$; and so on, each symbol at the moment its codeword ends. For $L = 3$ the decoding table has 8 entries: the indices 000 to 011 hold $(a, 1)$, 100 and 101 hold $(b, 2)$, 110 holds $(c, 3)$ and 111 holds $(d, 3)$. The code on this page implements both decoders and checks that they agree.

**An incomplete code.** $\{a \mapsto 0, b \mapsto 10, c \mapsto 110\}$ has Kraft sum $7/8$. The stream $111$ starts no codeword, so a decoder must report an error. The codeword $110$ can be shortened to $11$.

**Other prefix codes.** A fixed-length code, such as ASCII with 8 bits per character, is a prefix code, since no two different words of the same length are prefixes of each other. The [unary code](/unary-coding/) and the [Elias gamma code](/elias-gamma-coding/) are prefix codes for all positive integers, and UTF-8 is a prefix code for Unicode code points.

**Non-examples.**

- $\{0, 01, 11\}$ is not a prefix code, since $0$ is a prefix of $01$. It is uniquely decodable, but a decoder that has read $0$ followed by $1 1 1 \cdots$ cannot output the first symbol until the run of ones ends, because the parse depends on whether the run has odd or even length.
- $\{0, 01, 10\}$ is not a prefix code and not uniquely decodable: $010 = 0 \cdot 10 = 01 \cdot 0$.
- Morse code, as dots and dashes only, is not a prefix code: the codeword of E (a dot) is a prefix of the codeword of A (dot, dash). It is decodable only because of the pauses between letters, which act as a third code letter.
- A set of codewords plus an end marker, such as words separated by spaces, is a prefix code over the larger alphabet, but the marker costs space that a prefix code does not need.

## Related definitions

- A [uniquely decodable code](/uniquely-decodable-code/) is the larger class of codes whose concatenations parse in only one way; prefix codes are the uniquely decodable codes that need no look-ahead.
- A *suffix code* is a code in which no codeword is a suffix of another; it is uniquely decodable, since it decodes from right to left, but in general not instantaneous from left to right.
- The [Kraft inequality](/kraft-inequality/) characterizes the lengths of prefix codes.
- A [variable-length code](/variable-length-code/) is any code with codewords of different lengths; most are prefix codes.
- The [canonical Huffman code](/canonical-huffman-code/) is a prefix code that is fixed by its list of lengths, which makes table decoding simple.
- In Kolmogorov complexity, prefix-free sets of programs give the prefix complexity $K(x)$, for which the Kraft inequality holds for the program lengths.

## References
