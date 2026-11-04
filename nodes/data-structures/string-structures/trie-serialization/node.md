---
tag: AHFA41
kind: technique
slug: trie-serialization
name: Trie serialization
aliases:
- Trie serialization for compression
area: data-structures/string-structures
level: core
summary: Technique for writing a Huffman code trie to a bit stream and reading it back, using preorder with leaf flags.
prereqs: [huffman-coding, binary-tree, preorder-traversal, prefix-code]
see_also: [huffman-coding, canonical-huffman-code, prefix-code, deflate, balanced-parentheses-representation, louds-trie, catalan-numbers, trie]
sources:
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 5.5 (Data compression), Huffman compression, the methods writeTrie and readTrie
  - url: https://www.rfc-editor.org/rfc/rfc1951
    title: L. Peter Deutsch, DEFLATE Compressed Data Format Specification version 1.3, RFC 1951 (1996)
    locator: Section 3.2.2 (Use of Huffman coding in the deflate format) and Section 3.2.7 (Compression with dynamic Huffman codes)
  - paper: Guy Jacobson, Space-efficient static trees and graphs, Proceedings of the 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), doi:10.1109/SFCS.1989.63533
    locator: pages 549 to 554, the representation of trees in about 2 bits per node
---

Trie serialization writes a binary code [trie](/trie/), such as the one built by [Huffman coding](/huffman-coding/), to a bit stream so that a decoder can rebuild the same trie. The standard method walks the trie in [preorder](/preorder-traversal/): it writes a 0 for each inner node and a 1 followed by the symbol for each leaf. The reader rebuilds the trie with the same walk, reading a bit to decide whether the next node is a leaf. A trie with $L$ leaves takes $2L - 1$ flag bits plus the $L$ symbols, and the flag bits are within a lower order term of the minimum needed to tell the shapes apart.

## In plain words

A compressor that uses its own code for each file must send the code along with the compressed bits, or the receiver cannot decode them. The code is a tree: each letter sits at a leaf, and the path to the leaf spells its code word.

To send a tree, walk it in a fixed order, the node first and then its left and right parts. For a branching point write a 0. For a leaf write a 1 and then the letter. The receiver reads the same way: a 0 means "a branching point, now read its left part, then its right part", and a 1 means "a leaf, the next letter is its symbol". Since every branching point in a code tree has two children, these flags are enough to fix the shape.

## When it applies

The method applies to any tree in which each inner node has a fixed number of children, so that the shape is determined by which nodes are leaves. Code tries of [prefix codes](/prefix-code/) built by Huffman's algorithm are full binary trees: every inner node has two children. The data of the tree must sit at the leaves, or each inner node's data must be written after its flag.

It is the right choice when the trie is small compared with the message, the writer and the reader share no state, and simple code matters more than the last few bits. When the code is a [canonical Huffman code](/canonical-huffman-code/), sending only the code length of each symbol is shorter and is what [DEFLATE](/deflate/) does.

## The template

The input is a full binary tree whose leaves hold symbols of $b$ bits. The pseudocode is recursive for clarity; both walks can use an explicit stack, as described under Pitfalls.

```pseudo id=main
WRITE-TRIE(x, out)
L1  if x is a leaf then
L2      write the bit 1 to out
L3      write the b bits of x.symbol to out
L4  else
L5      write the bit 0 to out
L6      WRITE-TRIE(x.left, out)
L7      WRITE-TRIE(x.right, out)

READ-TRIE(in)
L8  if read one bit from in = 1 then
L9      return a new leaf with symbol (read b bits from in)
L10 left ← READ-TRIE(in)
L11 right ← READ-TRIE(in)
L12 return a new inner node with children left and right
```

**Why the reader rebuilds the same trie.** By induction on the size of the subtree: the writer emits the encoding of a subtree as one contiguous run, the flag of its root followed by the run of the left subtree and then the run of the right subtree. The reader at the start of such a run reads the same flag. For a leaf it reads the same $b$ bits. For an inner node, by the induction hypothesis the first recursive call reads exactly the run of the left subtree and returns a copy of it, so the second call starts at the run of the right subtree. In particular the reader knows where the trie ends without a length field, because preorder codes of full binary trees form a prefix code: no encoding of a tree is a proper prefix of another.

**Size.** A full binary tree with $L$ leaves has $L - 1$ inner nodes, so the stream has $2L - 1$ flag bits and $bL$ symbol bits, $(b + 2)L - 1$ bits in all. For bytes ($b = 8$), this is $10L - 1$ bits.

**Near optimality of the flags.** The number of full binary trees with $L$ leaves is the Catalan number $C_{L-1} = \frac{1}{L} \binom{2L-2}{L-1}$, which is $\Theta(4^L / L^{3/2})$. Any encoding that can tell all shapes apart needs at least $\lg C_{L-1} = 2L - O(\log L)$ bits for some shape, so the $2L - 1$ flag bits are optimal up to $O(\log L)$ bits. See [Catalan numbers](/catalan-numbers/).

## Classic examples

**A four-leaf Huffman trie.** Take the code A = 0, B = 10, C = 110, D = 111. Its trie has the root, whose left child is the leaf A and whose right child is an inner node; that node has the leaf B on the left and an inner node with the leaves C and D. The preorder walk gives:

| node visited | bits written |
|---|---|
| root (inner) | 0 |
| A (leaf) | 1, then the 8 bits of A |
| inner node of "1" | 0 |
| B (leaf) | 1, then the 8 bits of B |
| inner node of "11" | 0 |
| C (leaf) | 1, then the 8 bits of C |
| D (leaf) | 1, then the 8 bits of D |

The flags read 0 1 0 1 0 1 1, which is $2 \cdot 4 - 1 = 7$ bits, and the stream has $10 \cdot 4 - 1 = 39$ bits. The reader reads 0 (inner), then 1 and A (the left leaf), then 0 (the right inner node), and so on, and stops after D because the right child of the last inner node is complete.

**Huffman compression in Sedgewick and Wayne.** Their Huffman compressor writes the trie with this method, then the number of symbols of the message as a fixed width integer, then the code bits. The decompressor reads the trie, then the count, and then decodes that many symbols by walking the trie from the root for each one.

**Code lengths in DEFLATE.** A DEFLATE block with dynamic Huffman codes does not send the trie. It sends the code length of each symbol of the alphabet, and both sides build the canonical code of those lengths (RFC 1951, Section 3.2.2). The lengths are themselves Huffman coded with a small code, and runs of equal lengths are written with repeat codes (Section 3.2.7).

## Variations

- **Level order instead of preorder.** Writing the flags in breadth-first order gives a level-order bitmap of the tree, the binary case of the [LOUDS](/louds-trie/) representation. It supports navigation on the stored bits with rank and select, without rebuilding the tree.
- **Balanced parentheses.** Writing "(" when entering a node and ")" when leaving it gives the [balanced parentheses](/balanced-parentheses-representation/) form, which takes $2$ bits per node and works for trees of any degree.
- **Inner node data.** If inner nodes also carry data, as in a general trie with values at inner nodes, write the data after the flag of each node, or write a separate bit for "has a value".
- **Canonical codes.** If the code is canonical, the shape is determined by the multiset of code lengths, and the symbols by the sorted order within each length. Send the lengths only, as in DEFLATE.
- **Symbols as indexes.** If the leaves are known to be a subset of a fixed alphabet of size $R$, a leaf can be written with $\lceil \lg R \rceil$ bits, which is $b$ for bytes.

## Pitfalls

- **Recursion depth.** A Huffman trie on $L$ symbols can have depth $L - 1$, for example with Fibonacci frequencies. A recursive reader on a long alphabet can overflow the call stack. Use an explicit stack: when reading a 0, push a new inner node that waits for two children; when a subtree is complete, attach it to the inner node on top of the stack.
- **The one-symbol message.** A message that uses only one symbol gives a trie with one leaf and an empty code word, so the code bits are empty and the decoder cannot count symbols from them. Write the message length, as Sedgewick and Wayne do, or add a dummy second symbol so that the root is an inner node.
- **Bit order.** The writer and the reader must agree on the order of bits within a byte and on the bit order of the symbol fields. DEFLATE packs bits starting from the least significant bit of each byte, and Huffman codes are packed starting with their most significant bit (RFC 1951, Section 3.1.1).
- **Trailing bits.** The stream usually ends in the middle of a byte. The reader must not treat the padding bits as more data, which is another reason to send the symbol count.
- **Untrusted input.** A corrupt stream can describe a trie that never closes. The reader should stop at the end of the input and reject it, and bound the number of leaves by the alphabet size.

## Exercises

1. Write the stream of flags for the Huffman trie of the frequencies A: 5, B: 2, R: 2, C: 1, D: 1, !: 1, with ties broken as you choose, and check that it has 11 flag bits.
2. Prove that the set of preorder flag strings of full binary trees is a prefix code, using the fact that a flag string is complete exactly when it has one more 1 than 0 and no proper prefix has this property.
3. Write READ-TRIE with an explicit stack and no recursion.
4. Show that for a canonical Huffman code over 256 byte values, sending 256 code lengths of 4 bits each (1024 bits) can be longer than the preorder stream when only a few symbols occur, and find the number of used symbols at which the two methods cost the same.
5. Extend the method to a trie of a [prefix code](/prefix-code/) whose inner nodes may have one child, by writing two flags for each inner node.

## References
