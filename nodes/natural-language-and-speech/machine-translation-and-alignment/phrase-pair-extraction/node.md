---
tag: ZVR7MS
kind: algorithm
slug: phrase-pair-extraction
name: Phrase pair extraction
aliases:
- consistent phrase extraction
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Extract every pair of source and target spans consistent with a word alignment, that is with no link leaving the pair.
solves: [machine-translation]
model: word-ram
complexity:
  vars: {m: the source sentence length, l: the target sentence length, a: the number of links, p: the maximum phrase length}
  time: {worst: "O(m p (a + l^2))"}
  space: {extra: "O(a + l)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1999
  people: [Franz Josef Och, Christoph Tillmann, Hermann Ney, Philipp Koehn, Daniel Marcu]
  note: Och, Tillmann and Ney (1999) took phrase pairs (alignment templates) from word-aligned text. Koehn, Och and Marcu (2003) stated the consistency rule for phrase-based translation, and the Moses toolkit made it the standard first step of training.
prereqs: [word-alignment]
see_also: [grow-diag-final-symmetrization, phrase-based-translation-model, lexicalized-reordering-model, hierarchical-phrase-based-translation, ghkm-rule-extraction, parallel-corpus, ibm-model-1, fast-align]
sources:
  - paper: "Franz Josef Och, Christoph Tillmann and Hermann Ney, Improved alignment models for statistical machine translation, Joint SIGDAT Conference on Empirical Methods in Natural Language Processing and Very Large Corpora (EMNLP/VLC) 1999, pages 20 to 28"
    title: Och, Tillmann and Ney 1999
    locator: the alignment template approach, with phrase pairs taken from a symmetrized word alignment
  - paper: "Philipp Koehn, Franz Josef Och and Daniel Marcu, Statistical phrase-based translation, HLT-NAACL 2003, ACL Anthology N03-1017"
    title: Koehn, Och and Marcu 2003
    locator: the definition of phrase pairs consistent with a word alignment, and the comparison of phrase extraction methods
  - paper: "Philipp Koehn, Amittai Axelrod, Alexandra Birch Mayne, Chris Callison-Burch, Miles Osborne and David Talbot, Edinburgh system description for the 2005 IWSLT speech translation evaluation, IWSLT 2005, ACL Anthology 2005.iwslt-1.8"
    title: Koehn et al. 2005
    locator: "Section 2.4 (phrase extraction: a phrase pair must contain at least one alignment point and be consistent with the alignment)"
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 5 (phrase-based models: learning a phrase translation table)"
---

Phrase pair extraction is the step of statistical [machine translation](/machine-translation/) that reads a word-aligned sentence pair and lists every pair of a source phrase and a target phrase that the [word alignment](/word-alignment/) allows. A pair is allowed, or *consistent*, when it holds at least one link and no link joins a word inside the pair to a word outside it. The pairs of a whole [parallel corpus](/parallel-corpus/) are counted to build the phrase table of a [phrase-based translation model](/phrase-based-translation-model/). The rule is exact with respect to its definition, but the definition itself is a heuristic: it trusts the alignment, and an alignment error removes or adds many pairs.

## In plain words

Take a sentence and its translation, with lines drawn between words that mean the same thing. Now cut out a piece of the sentence and a piece of the translation. The two pieces form a good pair if no line leaves the box that they make together: every word in one piece is joined only to words in the other piece, and at least one line is inside. Short pieces give word translations, longer pieces give whole expressions with their word order.

A word with no line at all does not break any box, so it can be added at the edge of a piece. This gives several pairs that differ only by such loose words. The method tries every source piece up to a length limit, finds the smallest target piece that it needs, and then grows that piece over loose words on both sides.

## The problem

The input is a source sentence $f = f_1 \ldots f_m$, a target sentence $e = e_1 \ldots e_l$, a set $A$ of links $(j, i)$ between source position $j$ and target position $i$, and a length limit $p$. Spans are fencepost: the span $(s, t)$ covers the words $s + 1, \ldots, t$, so it has $t - s$ words. A phrase pair is $((s, t), (u, v))$, a source span and a target span. It is *consistent with $A$* if

1. some link $(j, i) \in A$ has $s < j \le t$ and $u < i \le v$, and
2. no link $(j, i) \in A$ has exactly one of $s < j \le t$ and $u < i \le v$.

The output is the set of all consistent pairs with $t - s \le p$ and $v - u \le p$. Moses uses $p = 7$. The direction of translation does not matter here, because the definition is symmetric in the two sides.

## The algorithm

For a source span, the target words it is linked to fix the smallest target span it can pair with. If some link reaches into that target span from outside the source span, no pair with this source span is consistent. Otherwise every pair is the smallest target span grown by any number of unaligned target words on the left and on the right.

```pseudo id=main
EXTRACT(m, l, A, p)                 ▷ spans are fencepost: (s, t) covers s+1 .. t
L1  P ← ∅
L2  for s ← 0 to m − 1 do
L3      for t ← s + 1 to min(m, s + p) do
L4          T ← { i : (j, i) ∈ A and s < j ≤ t }
L5          if T = ∅ then continue
L6          u ← min T − 1; v ← max T
L7          if some (j, i) ∈ A has u < i ≤ v and not s < j ≤ t then continue
L8          u2 ← u
L9          repeat
L10             v2 ← v
L11             repeat
L12                 if v2 − u2 ≤ p then P ← P ∪ {((s, t), (u2, v2))}
L13                 v2 ← v2 + 1
L14             until v2 > l or e_{v2} is aligned
L15             u2 ← u2 − 1
L16         until u2 < 0 or e_{u2+1} is aligned
L17 return P
```

Lines L4 to L6 find the smallest target span. Line L7 tests the second condition from the target side. Lines L8 to L16 grow the target span: the outer loop moves the left end over unaligned words, the inner loop moves the right end. Each new word is checked when it enters the span, at line L14 or line L16.

## Example

Take the German sentence $f$ = er geht ja nicht nach hause and the English $e$ = he does not go home, with $m = 6$, $l = 5$ and the links

$A = \{(1,1), (2,4), (4,2), (4,3), (5,5), (6,5)\}$:

er to he, geht to go, nicht to both does and not, and nach and hause both to home. The word ja is not aligned. With $p = 7$ the algorithm finds 10 pairs.

| source phrase | target phrase |
|---|---|
| er | he |
| er geht ja nicht | he does not go |
| er geht ja nicht nach hause | he does not go home |
| geht | go |
| geht ja | go |
| geht ja nicht | does not go |
| geht ja nicht nach hause | does not go home |
| ja nicht | does not |
| nicht | does not |
| nach hause | home |

Some spans give nothing. The source span "ja" has no links (line L5). The span "er geht" has targets $\{1, 4\}$, so $(u, v) = (0, 4)$, and the links of nicht reach into it from outside (line L7). The span "nach" alone has the target home, which is also linked to hause, so line L7 rejects it. Here no target word is unaligned, so lines L8 to L16 add exactly one pair for each source span that passes.

Unaligned target words give more pairs. For $f$ = das haus ist klein and $e$ = the house is very small, with $A = \{(1,1), (2,2), (3,3), (4,5)\}$, the target word very is not aligned. The source span "klein" gives both "small" and "very small", and "ist" gives "is" and "is very". In total there are 14 pairs.

## Correctness

The proofs file shows that the set returned is exactly the set of consistent pairs within the length limit. The key fact is that a pair is consistent if and only if its target span contains the smallest span of line L6, no link reaches into that smallest span from outside the source span, and every target word between the smallest span and the ends of the pair is unaligned. Line L7 tests the middle condition, and the two loops enumerate the rest. The test file compares the result with a brute force search over all pairs of spans on 400 random alignments.

## Complexity

Count in the [word RAM](/word-ram/) model. There are at most $m p$ source spans. For each, lines L4 and L7 read the $a$ links once, in $O(a)$ time. The loops of lines L8 to L16 run once for each pair of a left end and a right end inside the runs of unaligned words around the smallest span, so at most $O(l^2)$ times, and in practice a few times. The total time is $O(m p (a + l^2))$. Faster versions keep the minimum and the maximum of the targets as $t$ grows, so that line L4 costs $O(1)$ amortized for each span. The extra space is $O(a + l)$, not counting the output.

The output itself can be large. A sentence pair with a diagonal alignment of $n$ words has $n(n + 1)/2$ pairs without a length limit; for $n = 4$ that is 10.

## Properties

- **Exact for its definition.** It returns every consistent pair and nothing else (a theorem, proved in the proofs file).
- **Symmetric.** Swapping the roles of $f$ and $e$ gives the same pairs with the sides swapped.
- **Needs at least one link.** A pair of two unaligned words is not extracted, by condition 1. An empty alignment gives no pairs.
- **Many pairs for one span.** Unaligned words at the edges multiply the pairs: a source span with $x$ unaligned target words to its left and $y$ to its right can give up to $(x + 1)(y + 1)$ pairs.
- **Not a model.** The pairs have no probabilities. The [phrase-based model](/phrase-based-translation-model/) counts them over the corpus to estimate the phrase translation probabilities.

## Variants and improvements

- **Length limit.** Moses uses at most 7 words on each side. Longer limits give more pairs that are seldom used again.
- **Orientation counts.** The [lexicalized reordering model](/lexicalized-reordering-model/) records, for each extracted pair, whether the previous and the next pair are monotone, swapped or discontinuous. The extraction is the same; only extra counts are kept.
- **Hierarchical rules.** [Hierarchical phrase-based translation](/hierarchical-phrase-based-translation/) starts from these pairs (with a limit of 10 words) and cuts smaller consistent pairs out of them to make rules with gaps.
- **Syntax-based rules.** [GHKM rule extraction](/ghkm-rule-extraction/) uses the same idea of consistency, but only at nodes of a target parse tree, and it needs the closure of the span to be free of outside links.
- **Weighted pairs.** Instead of trusting one alignment, some systems count pairs from several alignments or weight them by alignment posteriors.

## When to use it

Use it to build the phrase table of a phrase-based system from a [symmetrized](/grow-diag-final-symmetrization/) word alignment. The heuristic works best with alignments that have high recall, such as grow-diag-final, because a missing link can make a pair consistent that should not be, while an extra wrong link removes many good pairs. Koehn, Och and Marcu (2003) found in their measurements that this simple method was better than phrase pairs from syntactic constituents only, and that phrases longer than three words gave little extra gain.

## Pitfalls

- **Off-by-one spans.** Use fencepost spans throughout. Mixing "covers $s$ to $t$" with "covers $s + 1$ to $t$" moves every pair by one word.
- **Testing condition 2 on one side only.** It is not enough that the source words link only into the target span. Line L7 must also check that no target word inside the span links to a source word outside. "Er geht" fails only that test.
- **Growing over aligned words.** The loops must stop at the first aligned word on each side. Growing over it breaks condition 2.
- **Forgetting the empty test.** Without line L5, unaligned source words would pair with every unaligned target word.
- **Memory.** On a large corpus, write the pairs to disk and count them there. A table in memory of all pairs of a corpus is usually too big.

## Implementations

## History

Och, Tillmann and Ney (1999) introduced the alignment template approach, which took phrase pairs from symmetrized word alignments. Koehn, Och and Marcu (2003) wrote down the consistency rule in the form used since, and compared it with phrases from syntactic constituents and from a joint phrase model. The Pharaoh decoder and then the Moses toolkit made extraction from a grow-diag-final alignment, with up to 7 words on each side, the standard way to build a phrase table. The same rule is the base of the rule extraction for hierarchical and syntax-based models.

## References
