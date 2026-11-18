---
tag: ZZTPQ8
kind: algorithm
slug: maximum-matching-segmentation
name: Maximum matching segmentation
aliases:
- MaxMatch
- greedy longest-match segmentation
area: natural-language-and-speech/tokenization-and-text-normalization
level: intro
summary: Segment a string into words by repeatedly taking the longest dictionary word that starts at the current position, from left to right.
solves: [word-segmentation]
model: word-ram
complexity:
  vars: {n: the length of the string in characters, m: the length of the longest dictionary word, L: the total length of the dictionary words}
  time: {worst: O(n m), trie_build: O(L)}
  space: {trie: O(L), output: O(n)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 1992
  people: [Keh-Jiann Chen, Shing-Huan Liu, Pak-kwong Wong, Chorkin Chan]
  note: Maximum matching was a common dictionary method for Chinese text by the early 1990s. Chen and Liu (1992) used a variant that compares chunks of three words. Wong and Chan (1996) used forward maximum matching with word binding forces. This page does not trace the first use.
prereqs: [trie, word-segmentation]
see_also: [unigram-language-model-tokenization, wordpiece, fast-wordpiece-tokenization, maximal-munch, greedy-algorithm, dag-shortest-paths, text-segmentation, double-array-trie]
sources:
  - url: https://aclanthology.org/C92-1019/
    title: Keh-Jiann Chen and Shing-Huan Liu, Word identification for Mandarin Chinese sentences, COLING 1992 Volume 1, Nantes
    locator: Section 3.1, Matching algorithm and disambiguation rules (the three-word chunks and heuristic rules 1 and 2)
  - paper: doi:10.3115/992628.992665
    title: Pak-kwong Wong and Chorkin Chan, Chinese word segmentation based on maximum matching and word binding force, COLING 1996 Volume 1, Copenhagen
    locator: pages 200 to 203, Section 2 (the forward maximum matching method) and the description of the lexicon tables
  - url: https://aclanthology.org/J96-3004/
    title: Richard Sproat, Chilin Shih, William Gale and Nancy Chang, A stochastic finite-state word-segmentation algorithm for Chinese, Computational Linguistics 22(3), 1996
    locator: pages 377 to 404 (the weighted finite-state model that scores whole segmentations)
---

Maximum matching segmentation, or MaxMatch, cuts a string with no spaces into words with a dictionary: at the current position it takes the longest dictionary word that starts there, and it continues after that word. It is one greedy algorithm for the [word segmentation](/word-segmentation/) problem, which asks for the right cut, so it can return a wrong cut where a model-based method returns the right one. The longest match is found with a [trie](/trie/) of the dictionary: the trie is the data structure, and MaxMatch is the rule that walks it. The backward variant works from the right end, and the bidirectional variant runs both directions and keeps one result.

## In plain words

You have a line of text with no spaces and a list of known words. Start at the first letter. Look for the longest known word that starts there, cut it off, and start again after it. If no known word starts at a letter, cut off that single letter. Repeat until the line is used up.

The method never looks back. When the longest word at a place is the wrong choice, the error stays and can push the next words out of place. A word list stored as a tree of letters makes each search fast: you follow the letters of the text down the tree and remember the last place where a word ended.

## The problem

The input is a string $s = s[0 \ldots n)$ and a finite dictionary $D$ of nonempty strings. The output is a list of strings $w_1, \ldots, w_r$ whose concatenation is $s$. A span $s[i \ldots j)$ is written with fencepost indices: it covers the characters $i + 1$ to $j$ in 1-based counting. MaxMatch does not optimize a score. Its output is defined by the rule itself: $w_t$ is the longest word of $D$ that is a prefix of the rest of the string, or one character if there is no such word.

## The algorithm

The trie $T$ holds the words of $D$. Each node is a prefix of a word, and a node is marked when it is a full word.

```pseudo id=main
MAX-MATCH(s, T)                            ▷ |s| = n, T is a trie of D
L1  i ← 0, W ← empty list
L2  while i < n do
L3      v ← root of T, j ← i + 1, k ← i    ▷ j is the end of the longest match so far
L4      while k < n and v has a child for s[k] do
L5          v ← that child, k ← k + 1
L6          if v is marked as a word then j ← k
L7      append s[i..j) to W
L8      i ← j
L9  return W
```

Line L3 sets the default end $j = i + 1$, so that a position where no word starts gives a word of one character. Lines L4 to L6 follow the characters of $s$ down the trie and record the last position where a word ends. The walk stops when the trie has no edge for the next character, because then no longer word can match. Lines L7 and L8 cut off the longest match and move on.

The backward variant is MAX-MATCH on the reversed string with a trie of the reversed words, and it reverses the result. The bidirectional variant runs both and keeps the result with fewer words, then the one with fewer characters outside the dictionary, then the one with fewer one-character words, and the backward result on a full tie. This rule is a heuristic: it optimizes no model.

## Example

Take the dictionary $D = \{$the, table, down, there, theta, bled, own, tab, led, a, here$\}$ and the string $s =$ thetabledownthere, with $n = 17$. The intended reading is "the table down there". In the table, "ends" lists every $k$ at which line L6 found a word.

| step | $i$ | characters read in L4 and L5 | why the walk stops | ends | $j$ | word |
|---|---|---|---|---|---|---|
| 1 | 0 | t h e t a | no edge for b after "theta" | 3, 5 | 5 | theta |
| 2 | 5 | b l e d | no edge for o after "bled" | 9 | 9 | bled |
| 3 | 9 | o w n | no edge for t after "own" | 12 | 12 | own |
| 4 | 12 | t h e r e | $k = n$ | 15, 17 | 17 | there |

Forward MaxMatch returns theta, bled, own, there. The first greedy choice "theta" takes the "ta" of "table", and the next two words are wrong as a result. Backward MaxMatch takes there, then the longest word that ends at position 12 (down, not own), then table, then the, so it returns the right reading. Both results have 4 words, no unknown characters and no one-character words, so the bidirectional rule falls to its last tie break and keeps the backward result.

Now give the words counts: the 30, a 6, there 5, down 4, table 3, own 2, here 2, and 1 for each of theta, bled, tab and led, 56 in all, with $P(w) = c(w)/56$. The string has exactly three segmentations into dictionary words. Their natural log probabilities are $-8.605865$ for the table down there, $-13.798822$ for theta bled own there, and $-14.422976$ for the tab led own there. The unigram dynamic program on the [word segmentation](/word-segmentation/) page picks the first. MaxMatch has no access to the counts, so it cannot make this choice.

A second case shows a dead end. With $D = \{$ab, abc, cd$\}$ and $s =$ abcd, forward MaxMatch takes abc and then has to cut off d as an unknown character, although ab, cd uses only dictionary words.

## Correctness

MaxMatch is correct with respect to its own rule, not with respect to the intended words. The proof shows two facts. First, the inner loop keeps the invariant that $v$ is the trie node of $s[i \ldots k)$ and $j$ is the end of the longest dictionary word seen so far, so it ends with the longest match at $i$, or $i + 1$ if there is none. Second, the outer loop keeps the invariant that $W$ is the list of the first $t$ words and that their concatenation is $s[0 \ldots i)$. Since $j > i$ in each pass, the loop stops after at most $n$ passes with $i = n$. The full proof is in proofs/correctness.md.

## Complexity

- **Time.** Let $m$ be the length of the longest word in $D$. The inner loop reads at most $m$ characters, because a path in the trie has at most $m$ edges. Each read is a child lookup, which costs $O(1)$ with a hash table per node or an array over a fixed alphabet. So a pass of the outer loop costs $O(m)$, and the at most $n$ passes cost $O(n m)$. The bound is reached: for $D = \{a, a^{m-1}b\}$, the string $a^n$ makes each walk read up to $m - 1$ characters and then cut off a single a.
- **Build.** The trie of a dictionary of total length $L$ has at most $L + 1$ nodes and is built in $O(L)$ time.
- **Space.** $O(L)$ for the trie and $O(n)$ for the output. The backward variant needs a second trie of the reversed words, and the bidirectional variant runs the algorithm twice.

## Properties

- **Total.** It always returns a segmentation, because of the one-character default. A model-based method can fail where no cut into dictionary words exists.
- **Greedy.** Each word is fixed when it is chosen. The output is not the cut with the fewest words: with $D = \{$a, ab, bcd, c, d$\}$, the string abcd gives ab, c, d, but a, bcd has two words.
- **Direction matters.** With $D = \{$a, ab, bc, c, d$\}$, forward MaxMatch cuts abcd as ab, c, d and backward MaxMatch cuts it as a, bc, d.
- **Deterministic.** The output depends only on $s$ and on the set $D$, not on the order of the dictionary.
- **Look-ahead.** The algorithm reads at most $m$ characters past the current position, so it can work on a stream with a buffer of $m$ characters.

## Variants and improvements

- **Backward maximum matching.** Run from the right end, as in the example. Neither direction is better on all inputs: the Properties section has a string where the two differ, and the example has one where only backward is right.
- **Bidirectional maximum matching.** Run both directions and choose by a rule such as the one above. The rules differ between systems.
- **Chunk matching.** Chen and Liu (1992) look at all chunks of three words that start at the current position. Their heuristic rule 1 picks the chunk with the largest total length, and rule 2 breaks ties by the smallest variance of the word lengths. The paper adds more rules for the remaining ties.
- **Linear-time longest match.** WordPiece tokenizers use the same greedy longest-match-first rule on subwords. [Fast WordPiece tokenization](/fast-wordpiece-tokenization/) adds failure links in the style of [Aho-Corasick](/aho-corasick/), so the whole text takes $O(n)$ time instead of $O(n m)$.
- **Compact tries.** A [double-array trie](/double-array-trie/) stores a large dictionary in two integer arrays with $O(1)$ child lookups.
- **Statistical segmentation.** With word frequencies, the best cut under a unigram model is a shortest path in a [DAG](/dag-shortest-paths/) of positions. This is the usual replacement for MaxMatch.

## When to use it

Use MaxMatch as a fast baseline when you have a good dictionary and no word frequencies, or to split identifiers and compound strings when errors are cheap. It is also the rule of the WordPiece tokenizer at inference time. When you have counts, use the unigram dynamic program, which costs the same $O(n m)$ and finds the most probable cut. For Chinese and Japanese text with many unknown words, use a trained sequence labeler, because no dictionary method can find a word that is not in its dictionary.

## Pitfalls

- **No default for an unknown character.** If line L3 does not set $j \leftarrow i + 1$, a position where no word starts leaves $j$ undefined or equal to $i$, and the loop never ends. The default must be set before the walk.
- **The last trie node is not the last word.** The walk can pass the end of the longest word and go on along a path that ends nowhere. Line L6 must record $j$ only at marked nodes. Taking $j \leftarrow k$ after the loop is wrong: with $D = \{$the, theta$\}$ and the string thetb, the walk reaches "thet", which is not a word.
- **Greedy is not optimal.** Do not claim that MaxMatch gives the fewest words or the most probable cut. The Properties section gives a counterexample to each.
- **Characters and bytes.** Index the string by code points, and normalize it first (see [Unicode text segmentation](/unicode-text-segmentation/)). A walk over UTF-8 bytes can cut a character in two.
- **Errors spread.** One wrong long word can shift the next cuts, as in the example, so word error counts can be larger than the number of wrong greedy choices.

## Implementations

## History

Dictionary matching was the usual method for Chinese segmentation before statistical models. Chen and Liu (1992) reported that maximal matching was the most effective of their heuristic rules, and they used it on chunks of three words. Wong and Chan (1996) used forward maximum matching with a lexicon of about 80,000 words and word binding forces, and they describe the method as greedy and suboptimal. Sproat, Shih, Gale and Chang (1996) replaced the greedy choice with a weighted finite-state model that scores whole segmentations. The same greedy longest-match rule appears in lexers as the [maximal munch](/maximal-munch/) rule and in WordPiece subword tokenizers.

## References
