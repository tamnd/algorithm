---
tag: 8H71X7
kind: algorithm
slug: byte-pair-encoding
name: Byte-pair encoding
aliases:
- BPE
- byte pair encoding
- BPE tokenizer
area: compression-and-coding/dictionary-compression
level: intro
summary: Iteratively merges the most frequent adjacent pair into a new symbol; originally a compressor, now used for tokenization.
model: word-ram
complexity:
  vars: {n: the input length, k: the number of merges in one block (at most 255)}
  time: {worst: O(k n)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false, online: false, comparison: false}
history:
  year: 1994
  people: [Philip Gage]
  note: Published as a compressor in The C Users Journal in 1994; Sennrich, Haddow and Birch used it to learn subword units for machine translation in 2016.
prereqs: [hash-table]
see_also: [re-pair, grammar-based-compression, sequitur, straight-line-program-grammar, dictionary-based-compression, lzw, huffman-coding, smallest-grammar-problem]
sources:
  - paper: "Philip Gage, A new algorithm for data compression, The C Users Journal 12(2), February 1994, pages 23 to 38"
    locator: the compressor (blocks of bytes, the pair table, replacing the most frequent pair by a byte that does not occur in the block, the threshold) and the expansion
  - paper: doi:10.18653/v1/P16-1162
    title: Rico Sennrich, Barry Haddow and Alexandra Birch, Neural machine translation of rare words with subword units, Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (ACL 2016), pages 1715 to 1725
    locator: Section 3.2 and Algorithm 1 (learning merges on a table of word counts, with an end-of-word symbol, and applying them to new words)
  - paper: doi:10.1109/5.892708
    title: N. Jesper Larsson and Alistair Moffat, Off-line dictionary-based compression, Proceedings of the IEEE 88(11), 2000
    locator: Re-Pair, the same pair replacement without a byte budget, for comparison
---

Byte-pair encoding (BPE) replaces the most frequent pair of adjacent symbols by a new symbol, and repeats. Philip Gage published it in 1994 as a simple compressor: it works on a block of bytes, takes each new symbol from the byte values that do not occur in the block, and stores a small table of pairs so that the block can be expanded again. In 2016 Sennrich, Haddow and Birch used the same merge loop for a different goal: to learn a vocabulary of subword units for machine translation. The two uses share the loop but differ in input, output and stopping rule, and this page keeps them apart. BPE is a close relative of [Re-Pair](/re-pair/), and its output is a small [grammar](/grammar-based-compression/).

## In plain words

Look at a text and find the two neighbouring letters that appear together most often, for example "a" followed by "a". Pick a byte value that never appears in the text, and use it as a short name for that pair. Replace the pair by its name everywhere, and write "name = pair" in a small table. The text is now shorter.

Repeat. A pair can now hold a name, so names can stand for longer and longer pieces. Stop when there are no more free byte values, or when the best pair is too rare to be worth a table entry. To get the text back, replace each name by its pair until no names are left.

The tokenizer runs the same loop on a list of words and keeps the list of merges. To split a new word, it applies them in the same order.

## The problem

**As a compressor (Gage).** The input is a block $B$ of $n$ bytes and a threshold $t \ge 2$. The output is a table of entries $(c, a, b)$ and a shorter block, such that replacing each code $c$ by $ab$, again and again, gives back $B$. Each code must be a byte value that does not occur in the original block; otherwise the decoder could not tell a code from a plain byte. The input file is cut into blocks, and each block is compressed alone.

**As a tokenizer (Sennrich et al.).** The input is a table of words with their counts and a number $m$ of merges. The output is an ordered list of at most $m$ merges, each a pair of strings. A new word is split into units by starting from its characters and applying the merges in order. The units are strings, not bytes, so there is no budget of free byte values; the number of merges is the size of the vocabulary that the user wants.

## The algorithm

```pseudo id=main
BPE-COMPRESS-BLOCK(B, t)                    ▷ B a block of bytes, t ≥ 2 the threshold
L1  U ← the byte values that do not occur in B, smallest first
L2  T ← empty table of pairs
L3  while U is not empty do
L4      count the non-overlapping occurrences of each pair of adjacent bytes in B
L5      ab ← the pair with the largest count (the smallest pair on a tie)
L6      if the count of ab is less than t then stop
L7      c ← the first value in U; remove it from U
L8      replace each occurrence of ab in B by c, from left to right
L9      append (c, a, b) to T
L10 return T and B
```

Line L1 finds the free codes. Line L4 counts pairs with a [hash table](/hash-table/); in a run such as zzz the two copies of zz overlap, so the run counts once, because line L8 can replace only one of them. Line L6 is the threshold: an entry of the table costs 3 bytes, and replacing $c$ occurrences saves $c$ bytes, so a pair that occurs only 2 or 3 times does not pay for itself. The implementation uses $t = 4$ by default. Line L8 scans the block once from left to right.

To expand, read the packed block and push each byte on a stack. When the top of the stack has an entry $(c, a, b)$ in the table, replace it by $b$ and then $a$; otherwise write it out. The stack avoids recursion, since codes can be nested up to 255 levels deep.

**The tokenizer.** Start each training word as its characters followed by an end-of-word symbol, written `</w>`, so that a unit at the end of a word differs from the same letters inside a word. Then repeat $m$ times: count each pair of adjacent units over all words, weighted by the count of the word; take the most frequent pair; merge it in every word; and record it. To split a new word, start from its characters and `</w>`, and apply the recorded merges in the order they were learned. This follows Algorithm 1 of Sennrich et al.; the pair counts there include overlapping copies, and this implementation does the same.

## Example

**The compressor.** Take the block aaabdaaabac ($n = 11$) with threshold $t = 2$. The letters use bytes 97 to 100, so the free codes start at 0, 1, 2. Write the codes as $c_0$, $c_1$, $c_2$.

| step | counts of the best pairs | chosen pair | new entry | block | length |
|---|---|---|---|---|---|
| start | | | | a a a b d a a a b a c | 11 |
| 1 | aa 2, ab 2 | aa | $c_0$ = aa | $c_0$ a b d $c_0$ a b a c | 9 |
| 2 | $c_0$a 2, ab 2 | $c_0$a | $c_1$ = $c_0$a | $c_1$ b d $c_1$ b a c | 7 |
| 3 | $c_1$b 2 | $c_1$b | $c_2$ = $c_1$b | $c_2$ d $c_2$ a c | 5 |

In step 1, aa and ab both occur twice (each aaa holds one copy of aa that does not overlap), and aa wins as the smaller pair. In step 2 the pair $(c_0, a)$ is $(0, 97)$, which is smaller than $(97, 98)$, so it wins the tie. After step 3 no pair occurs twice and the loop stops. The table has 3 entries and the block has 5 bytes. Expanding $c_2$ gives $c_1$b, then $c_0$ab, then aaab.

**The tokenizer.** Take the training words low (5 times), lower (2), newest (6) and widest (3), the example of Algorithm 1 in Sennrich et al., and learn 10 merges with ties going to the smaller pair.

| merge | pair | count |
|---|---|---|
| 1 | e + s | 9 |
| 2 | es + t | 9 |
| 3 | est + `</w>` | 9 |
| 4 | l + o | 7 |
| 5 | lo + w | 7 |
| 6 | e + w | 6 |
| 7 | ew + est`</w>` | 6 |
| 8 | n + ewest`</w>` | 6 |
| 9 | low + `</w>` | 5 |
| 10 | d + est`</w>` | 3 |

The new word lowest, which was not in the training data, splits as low + est`</w>`. The word newer splits as n + ew + e + r + `</w>`, because no merge joins e and r.

## Correctness

For the compressor, the proof keeps an invariant at line L3: the free codes, the codes in the table and the bytes of the original block are three disjoint sets, and expanding the current block with the table gives the original block. A merge takes a code that does not occur yet, so writing it in the block and adding its entry keeps the expansion the same. Each entry refers only to earlier entries, so the expansion stops. Each pass uses up one free code, so the loop stops after at most 255 passes. For the tokenizer, applying the merges in the learned order to a training word gives the same units as the training did. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

- **Compressor.** Each pass of the loop counts pairs and replaces them in one scan of the block, which takes $O(n)$ expected time with a hash table, or $O(n + 2^{16})$ worst case with a table of $256 \times 256$ counters indexed by the pair. A block has at most $k \le 255$ merges, so the time is $O(k n)$, which is $O(n)$ for a fixed byte alphabet but with a large constant. The extra space is $O(n)$ for the block and $O(1)$ for the table of at most 255 entries.
- **Expansion.** Each step of the stack writes one byte or replaces one code by two bytes. Each code in the output tree is expanded once, so the time is linear in the output.
- **Tokenizer.** The simple version here recounts all pairs for each merge, in $O(N)$ time for $N$ symbols in the word table, so learning $m$ merges takes $O(m N)$ time. Segmenting a word of length $\ell$ applies the merges in order, in $O(m \ell)$ time.

## Properties

- **Off-line within a block.** Each block is read whole before the first merge, so compression is not on-line.
- **Bounded budget.** The number of codes in a block is at most the number of byte values that do not occur in it. A block that uses all 256 values cannot be compressed at all.
- **Self-delimiting codes.** Because each code is a byte that does not occur in the block, the decoder needs only the table to tell codes from plain bytes.
- **Deterministic.** With a fixed tie rule and threshold, the output depends only on the input.

## Variants and improvements

**Differences from Re-Pair.** [Re-Pair](/re-pair/) uses the same rule, replace the most frequent pair, but:

- Re-Pair has no budget. Its new symbols are fresh integers, so it can make as many rules as it needs, nested as deep as needed. BPE has at most 255 codes per block, which also limits the nesting depth.
- BPE needs codes that do not occur in the block; Re-Pair needs no free values.
- BPE stops when the best count is below the threshold; Re-Pair stops only when no pair occurs twice.
- The tie rule depends on the numbering. In the example above, BPE gives the second code to $c_0$a because code 0 is small. Re-Pair numbers new symbols from 256, so on the same block it takes ab second and gets the rules aa, ab, then a rule for the two together.
- BPE recounts the whole block after each merge; Re-Pair updates its counts locally and runs in linear expected time on the whole input.

**Other variants.**

- **Larger blocks or wider codes.** With 16-bit symbols the budget grows and the method becomes close to Re-Pair.
- **Tokenizers.** Later tokenizers start from bytes instead of characters, so that each input can be split, or use other rules for choosing merges. These are outside the scope of this page.

## When to use it

Use the compressor when you need a very small, simple decoder that expands with one stack and no other memory, or as a first example of pair replacement. For general files, LZ77-based compressors such as [Deflate](/deflate/) are the usual choice. Use the tokenizer when you need a fixed-size vocabulary of subword units for a language model or a translation model; it handles rare and new words by splitting them into known pieces.

## Pitfalls

- **Using a code that occurs in the block.** If line L1 takes a value that is already in the block, the decoder expands a plain byte as a pair and the output is wrong.
- **Counting overlapping copies in the compressor.** If line L4 counts zzz as two copies of zz, the loop can choose a pair that line L8 replaces only once, and the table entry costs more than it saves.
- **No threshold.** If line L6 is left out, the loop spends codes on pairs that occur twice, and each such entry makes the output larger.
- **Mixing up the two uses.** The tokenizer learns merges on a table of word counts and keeps them in order; the compressor replaces bytes in one block and keeps a table of codes. A tokenizer that applies the merges in another order than they were learned gives different units than the training did.
- **Forgetting the end-of-word symbol.** Without `</w>`, the tokenizer cannot tell est at the end of a word from est inside a word.

## Implementations

## History

Philip Gage described byte-pair encoding as a compressor in "A new algorithm for data compression" in The C Users Journal in February 1994. Larsson and Moffat's Re-Pair (1999) made the same pair replacement on the whole input with fresh symbols and linear expected time. In 2016 Rico Sennrich, Barry Haddow and Alexandra Birch adapted BPE to learn subword units for neural machine translation, so that a model with a fixed vocabulary can handle rare words. Since then, BPE and its variants have been a standard way to build the vocabulary of language models.

## References
