---
tag: PZXMS8
kind: algorithm
slug: fast-wordpiece-tokenization
name: Fast WordPiece tokenization
aliases:
- LinMaxMatch
area: natural-language-and-speech/tokenization-and-text-normalization
level: research
summary: Linear-time greedy longest-match WordPiece encoding with a trie extended by failure links and failure pops, in the style of Aho-Corasick.
solves: [text-tokenization]
model: word-ram
complexity:
  vars: {n: the length of the word in characters, m: the length of the longest token, M: the total length of all tokens}
  time: {precompute: O(M m), encode_word: O(n)}
  space: {trie_with_pops: O(M m), encode_word: O(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 2021
  people: [Xinying Song, Alex Salcianu, Yang Song, Dave Dopson, Denny Zhou]
  note: Song et al. gave LinMaxMatch for single words and an end-to-end version that also does the pre-tokenization, both in one left-to-right pass.
prereqs: [wordpiece, trie, aho-corasick]
see_also: [maximum-matching-segmentation, maximal-munch, knuth-morris-pratt, double-array-trie, finite-state-transducer, bert, byte-level-bpe, unigram-language-model-tokenization]
sources:
  - paper: doi:10.18653/v1/2021.emnlp-main.160
    title: Xinying Song, Alex Salcianu, Yang Song, Dave Dopson and Denny Zhou, Fast WordPiece tokenization, EMNLP 2021, pages 2089 to 2103
    locator: Section 3 (Definition 1, Algorithms 1 and 2, the example of Figure 1 and Table 2, the complexity in Section 3.5), Section 4 (end-to-end WordPiece), Section 5 (setup and Table 3, page 2097)
  - paper: doi:10.1145/360825.360855
    title: Alfred V. Aho and Margaret J. Corasick, Efficient string matching, an aid to bibliographic search, Communications of the ACM 18(6) (1975), 333-340
    locator: Algorithms 2 and 3 (the goto and failure functions)
  - url: https://github.com/google-research/bert/blob/master/tokenization.py
    title: Google Research, BERT reference code, tokenization.py
    locator: class WordpieceTokenizer (the original greedy longest-match-first encoder)
---

Fast WordPiece tokenization computes the same pieces as the greedy longest-match-first encoder of [WordPiece](/wordpiece/), but in time linear in the length of the word. It puts the vocabulary in a [trie](/trie/) and adds to each node a failure link and a list of failure pops, much as [Aho-Corasick](/aho-corasick/) adds failure links to a trie of patterns. The single-word algorithm is called LinMaxMatch. Song et al. (2021) also give an end-to-end version that splits the text into words in the same pass.

## In plain words

The usual WordPiece encoder tries the longest piece at a position, then a shorter one, then a shorter one, and only then moves on. On a bad word it reads the same letters many times.

The fast encoder reads each letter once. It walks down a tree of all pieces, one letter at a time. When the next letter has no branch, it does not go back. Each place in the tree already knows two things, worked out once for the whole vocabulary: which pieces the slow encoder would output from the letters read so far, and at which place in the tree to go on. So the encoder outputs those pieces, jumps there, and tries the same letter again. A letter can be tried again only a few times in total, so the work grows like the length of the word.

## The problem

The input is a vocabulary $V$ of tokens, where a token that does not start a word carries the prefix $\sharp$ = "##", and a word $w$ of $n$ characters. The output is the list that greedy longest match first (MAXMATCH) gives: the longest token that is a prefix of $w$, then the longest token "##"$y$ such that $y$ follows it in $w$, and so on, or [UNK] if some position has no token. The BERT code does this with up to $n$ dictionary lookups per position. With a trie and tokens of at most $m$ characters it costs $O(n m)$, and on the vocabulary {a, ##a, $a^m b$} and the word $a^n$ that bound is reached: each position walks $m$ edges toward $a^m b$ and then backs up.

## The algorithm

The trie holds every token and the string "##". Its root is $r$, the node of "##" is $r_\sharp$, $\chi_v$ is the string of node $v$, and $\delta(u, c)$ is the child of $u$ along character $c$. For a node $v$, the failure pops $F(v)$ are the tokens that MAXMATCH would emit from $\chi_v$, longest first, until the rest, written as "##" followed by the unread characters, is again a node of the trie; that node is the failure link $f(v)$. If MAXMATCH gets stuck first, $f(v)$ is none. The links are filled in breadth-first order (Algorithm 2 of the paper):

```pseudo id=precompute
PRECOMPUTE(V)
P1  build the trie of V ∪ {##}; r ← root, r♯ ← node of ##
P2  f(v) ← none and F(v) ← [] for every node v
P3  queue ← [r, r♯]
P4  while queue is not empty do
P5      u ← dequeue(queue)
P6      for each edge from u to v with label c do
P7          if v = r♯ then skip to the next edge
P8          if χv ∈ V then f(v) ← r♯, F(v) ← [χv]
P9          else
P10             z ← f(u), Z ← []
P11             while z ≠ none and δ(z, c) = none do
P12                 Z ← Z + F(z), z ← f(z)
P13             if z ≠ none then f(v) ← δ(z, c), F(v) ← F(u) + Z
P14         enqueue v
P15 return the trie with f and F
```

Encoding one word walks the trie and follows a failure link whenever the next character has no edge (Algorithm 1 of the paper):

```pseudo id=main
LINMAXMATCH(w)                       ▷ uses the trie from PRECOMPUTE
L1  s ← w followed by the end mark ␣, which is in no token
L2  u ← r, tokens ← empty list, i ← 0
L3  while i < |s| do
L4      while δ(u, s[i]) = none do
L5          if f(u) = none then leave both loops
L6          append the list F(u) to tokens
L7          u ← f(u)
L8      u ← δ(u, s[i]), i ← i + 1
L9  if i < |w| or u ∉ {r, r♯} then return [UNK]
L10 if u = r♯ and tokens is empty then return MAXMATCH("##")
L11 return tokens
```

The end mark of line L1 has no edge anywhere, so at the end of the word the loop pops every pending token. A successful run stops at $r_\sharp$, where all characters are covered, or at $r$ for the empty word. Line L10 handles the word "##", whose path from the root also ends at $r_\sharp$. Positions are 0-based, and $w[i..j)$ is the span $(i, j)$ in fencepost indices.

## Example

This is the example of Song et al. Let $V$ = {a, abcdx, ##b, ##c, ##cdy, ##dz}. PRECOMPUTE gives:

| node $\chi_v$ | $F(v)$ | $f(v)$ |
|---|---|---|
| a | [a] | ## |
| ab | [a] | ##b |
| abc | [a, ##b] | ##c |
| abcd | [a, ##b] | ##cd |
| abcdx | [abcdx] | ## |
| ##b | [##b] | ## |
| ##c | [##c] | ## |
| ##cd | [##c] | ##d |
| ##cdy | [##cdy] | ## |
| ##d | [] | none |
| ##dz | [##dz] | ## |

The root, "#" and "##" have empty pops and no link. For the node abcd, MAXMATCH would emit a and then ##b, and the rest "##cd" is a node, so the encoder can go on from there without reading c and d again.

On the word abcdz the encoder walks a, ab, abc, abcd. The letter z has no edge from abcd, so it emits a, ##b and moves to ##cd. There is still no edge for z, so it emits ##c and moves to ##d, where z leads to ##dz. The end mark has no edge, so it emits ##dz and moves to ##, whose link is none. The result is a, ##b, ##c, ##dz after 5 steps along edges and 3 failure steps. The word abcz stops at abc with i = 3 < 4, and abcd stops at ##d, which has no link, so both give [UNK], as MAXMATCH does.

## Correctness

PRECOMPUTE fills $f$ and $F$ as defined, by induction in breadth-first order: when a node $v = \delta(u, c)$ is not a token, MAXMATCH on $\chi_v$ emits the pops of $u$ and then follows the chain of links from $f(u)$ until some node has an edge for $c$, which is what lines P10 to P13 do. LINMAXMATCH keeps the invariant that its tokens are a prefix of the MAXMATCH output and that the current node spells the unmatched rest. When the next character has no edge, no token can reach past it, so the next MAXMATCH tokens are exactly the failure pops. The equality is a theorem for every word that does not start with "##", and for every word when the one-character token "#" is not in $V$. For $V$ = {#, ###c} and the word "##c", MAXMATCH gives #, ###c and LINMAXMATCH gives [UNK]; BERT splits off "#" as punctuation, so such words do not reach its encoder. The proofs are in proofs/correctness.md.

## Complexity

- **Encoding.** In the word-RAM model, line L8 runs at most $n$ times. Define the level of a node as the length of its string without a leading "##". Each step along an edge raises the level by one (except the single step from "#" to "##"), and each failure step lowers it, so line L7 also runs at most $n$ times. At most $n$ tokens are appended. The total is $O(n)$, with no factor of $m$. This is a theorem.
- **Precomputation.** The breadth-first search visits $O(M)$ nodes. Song et al. bound the link computation by $O(M)$ in the style of Aho-Corasick, and copying the pop lists, each of at most $m$ tokens, costs $O(M m)$ time and space in a direct implementation.

## Properties

- **Exact.** The output is that of the BERT encoder, under the condition above, so a model trained with the slow encoder can switch to this one.
- **Each character once.** The input is read once from left to right, and failure steps never move the read position back.
- **Measurements.** Song et al. ran C++ code on a Linux desktop with a six-core Intel Xeon at 3.60 GHz and 64 GB of memory, with the BERT-Base Multilingual Cased vocabulary and 1,000 sentences from multilingual Wikipedia. The mean time per word was 82 ns, against 274 ns for Hugging Face Tokenizers (Rust) and 246 ns for TensorFlow Text, about 3 times faster. For end-to-end tokenization of text the means were 1,629 ns, 13,397 ns and 8,247 ns, so 8.2 and 5.1 times faster. These are measurements, not bounds.

## Variants and improvements

- **End-to-end WordPiece.** Section 4 of the paper adds the pre-tokenization of BERT to the same automaton: whitespace and punctuation get their own nodes, so one pass splits the text into words and words into pieces.
- **A transducer view.** The trie with failure links and pops is a [finite-state transducer](/finite-state-transducer/) whose failure steps emit tokens; Song et al. describe this view in Section 3.6.
- **Compact tries.** The paper stores the trie as a [double-array trie](/double-array-trie/) for speed.

## When to use it

Use it to serve a model that was trained with [WordPiece](/wordpiece/), such as [BERT](/bert/), when tokenization time matters, as in high-volume inference. It changes nothing in the model or in the vocabulary. If the vocabulary has no long tokens, the plain encoder with a trie costs $O(n m)$ with a small $m$, and the gain is smaller.

## Pitfalls

- **The end mark.** The mark must not occur in any token or word. Without it, pending tokens at the end of the word are never popped.
- **The node of "##".** It must never be enqueued as the child of "#" (line P7), and its own link must stay none. Otherwise a word that starts with "##" walks into suffix nodes with the wrong pops.
- **Pop lists are long.** Storing $F(v)$ as a full list at each node costs $O(M m)$ space. If memory is tight, store each list once and let nodes with the same list share it.
- **[UNK] is decided at the end.** A word can emit several pops and still end as [UNK], so tokens must not be streamed out before the word ends.

## Implementations

## History

Greedy longest match first came with WordPiece in BERT, where each position costs a series of dictionary lookups. Song et al. (2021) observed that the failure links of Aho and Corasick (1975) carry over if each link also carries the tokens to emit, and called the result LinMaxMatch. Their end-to-end version folds the pre-tokenization into the same pass.

## References
