---
tag: NH530P
kind: technique
slug: front-coding
name: Front coding
aliases:
- incremental encoding of sorted strings
area: information-retrieval-and-ai-reasoning/indexing-and-query-processing
level: core
summary: Stores each term of a sorted dictionary as the length of the prefix it shares with the previous term plus its remaining suffix.
prereqs: [lexicographic-order, variable-byte-encoding]
see_also: [inverted-index, lcp-array, trie, radix-tree, string-b-tree, b-plus-tree, dictionary-based-compression, binary-search]
sources:
  - book: isbn:9780521865715
    title: Christopher D. Manning, Prabhakar Raghavan and Hinrich Schuetze, Introduction to Information Retrieval, Cambridge University Press, 2008
    locator: Chapter 5, Section 5.2.2 (the dictionary as a string, blocked storage with k = 4, front coding with Figure 5.7 and the automata example, the sizes 7.6 MB, 7.1 MB and 5.9 MB for Reuters-RCV1 in Table 5.2, and the cost of a lookup in a blocked dictionary)
  - book: isbn:9781558605701
    title: Ian H. Witten, Alistair Moffat and Timothy C. Bell, Managing Gigabytes, Compressing and Indexing Documents and Images, second edition, Morgan Kaufmann, 1999
    locator: Chapter 4, Section 4.1 (the storage of the lexicon, with front coding of the sorted terms and the use of blocks with a full term at the start of each)
---

Front coding is the technique of storing a sorted list of strings by writing, for each string, the length of the prefix it shares with the string before it, followed by the rest of the string. Sorted terms share long prefixes ("automata", "automate", "automatic"), so the shared part is written once and the dictionary of an [inverted index](/inverted-index/) gets much smaller. To keep lookups fast, the list is cut into blocks of $k$ strings, and the first string of each block is written in full, so a search can start at any block. The lengths are small numbers and are written with a [variable byte code](/variable-byte-encoding/).

## In plain words

In a dictionary, neighbors look alike: "automata" is followed by "automate", "automatic" and "automation". Writing all four words in full repeats "automat" four times. Front coding writes the first word in full, and for each next word it writes only how many letters it shares with the word before and the letters that are new. So "automate" becomes "7, then e".

To read a word back, the reader must know the word before it, and that one needs the one before it, and so on. To avoid reading the whole list for one word, the list is cut into small groups, and the first word of each group is written in full. A search jumps to the right group, then reads at most a few words in it.

## When it applies

- **The strings are sorted.** The order of [lexicographic order](/lexicographic-order/) puts strings with long common prefixes next to each other. On an unsorted list front coding still works, but it saves little.
- **The list is read more than it is changed.** An insertion in the middle changes the prefix length of the next string and, with blocks, can move the block heads. Static dictionaries, index files and sorted runs suit it; a dictionary that changes often needs a tree.
- **Lookups can afford a short scan.** A lookup decodes up to $k - 1$ strings of a block after a [binary search](/binary-search/) over the block heads.
- **The strings share prefixes.** Long words of a large vocabulary, URLs, file paths and sorted keys gain much; short words of a small vocabulary gain little or nothing, as the toy example below shows.

## The template

The encoder below writes the number of strings first, then each string as described. The holes to fill are in capitals.

```pseudo id=main
FRONT-ENCODE(t_0, ..., t_{n-1}, k)        ▷ t sorted, k ≥ 1
L1  out ← WRITE-NUMBER(n)
L2  for i ← 0 to n - 1 do
L3      if i mod k = 0 then p ← 0                         ▷ a block head is written in full
L4      else p ← LCP(t_{i-1}, t_i)
L5          append WRITE-NUMBER(p) to out
L6      append WRITE-NUMBER(|t_i| - p) and the bytes t_i[p..] to out
L7  return out
```

**The holes.** LCP is the length of the longest common prefix of two strings, in bytes. WRITE-NUMBER is the code of the lengths: the code here is a variable byte code with 7 bits per byte and the high bit on the last byte, so every length below 128 costs one byte. The block size $k$ trades space for lookup time: $k = 1$ is no front coding, and $k = n$ is one block. The decoder reads in the same order and rebuilds $t_i$ as the first $p$ bytes of $t_{i-1}$ followed by the bytes it reads; at a block head it needs nothing from before.

**The invariant.** After the decoder has read string $i$, it holds $t_i$ exactly. At a block head this is because the string is written in full. Elsewhere it holds $t_{i-1}$ by induction, and $t_{i-1}$ and $t_i$ agree on their first $p$ bytes by the definition of LCP, so the first $p$ bytes of $t_{i-1}$ followed by the rest give $t_i$. This holds for any list, sorted or not, and for empty strings.

**The cost.** Encoding and decoding take time linear in the total length of the strings. The output has the stored rest bytes plus one or two length numbers per string. A lookup of a string $x$ makes a binary search over the $\lceil n/k \rceil$ block heads, which needs an array of the byte offsets of the blocks, then decodes at most $k - 1$ strings of one block.

**A worked example.** The four strings "automata", "automate", "automatic" and "automation" form one block with $k = 4$.

| string | p | rest | bytes |
|---|---|---|---|
| automata | (head) | automata | 1 + 8 = 9 |
| automate | 7 | e | 1 + 1 + 1 = 3 |
| automatic | 7 | ic | 1 + 1 + 2 = 4 |
| automation | 8 | on | 1 + 1 + 2 = 4 |

The block takes 20 bytes, against 39 bytes for the four strings each with a one-byte length. On the 50 terms of the toy collection the plain list with one-byte lengths takes 284 bytes, and front coding takes 292 bytes for $k = 4$ and 279 for $k = 16$. The words are short and share only 53 letters with their neighbors in all, often one or two, and the extra prefix byte of each string costs about as much as it saves.

## Classic examples

- **The dictionary of an [inverted index](/inverted-index/).** Manning, Raghavan and Schuetze store the RCV1 dictionary as one long string with pointers, in 7.6 MB. Blocks of $k = 4$, which need a term pointer only for every fourth term, bring it to 7.1 MB, and front coding inside the blocks to 5.9 MB.
- **Leaves of a [B+ tree](/b-plus-tree/) or a [string B-tree](/string-b-tree/).** Keys in a leaf are sorted and share prefixes, so storing them front coded fits more keys in a disk page and makes the tree shallower.
- **The [LCP array](/lcp-array/).** The sorted suffixes of a text, written with the length of the prefix that each shares with the one before, are a front coding of the suffixes; the LCP array is exactly the list of those prefix lengths.
- **A [trie](/trie/) flattened in order.** Walking a trie in order and writing, at each word, how far to go back up and which letters to add gives the same numbers as front coding. A [radix tree](/radix-tree/) stores each shared prefix once, as front coding does within a block.

## Variations

- **Shared prefix of the block.** Manning, Raghavan and Schuetze write the prefix common to the whole block once, after the first term, and then each other term as its length and the letters after that prefix. This is simpler to decode but saves less when the terms of a block share different prefixes.
- **Count from the end.** Store how many bytes to remove from the end of the previous string, $|t_{i-1}| - p$, in place of $p$. The two numbers carry the same information, and the count from the end is small when long strings differ only near their ends.
- **Front coding with a code of the lengths.** Use a bit-level code such as a gamma code for the prefix lengths, or pack both lengths in one byte when both are below 16.
- **Compressed strings.** Code the rest bytes with a [dictionary-based compressor](/dictionary-based-compression/) or a Huffman code of the characters, on top of front coding.

## Pitfalls

- **No block heads.** With $k = n$, every lookup decodes from the first string, in time linear in the list. Choose $k$ so that a block fits in a few cache lines or one disk read.
- **Prefix lengths in characters against bytes.** For UTF-8 strings, a prefix length counted in characters cuts the bytes wrongly when the two strings differ inside a character. Compute LCP and slice on the same unit; the code here works on bytes throughout.
- **Trailing or missing data.** The decoder must check that it reads exactly the encoded bytes. The code here raises an error when bytes are left over, so a padded or joined buffer does not decode silently to a wrong list.
- **Expecting a gain on short words.** On a small vocabulary of short words, front coding can make the dictionary larger, as on the toy collection. Measure before choosing $k$.
- **Updates in place.** Inserting one string in the middle changes the prefix length of the string after it. Rebuild the block, not only the entry.

## References
