---
tag: M9QEWS
kind: algorithm
slug: span-based-constituency-parsing
name: Span-based neural constituency parsing
aliases:
- chart-based neural parser
area: natural-language-and-speech/natural-language-parsing
level: research
summary: "A neural network scores each labeled span of the sentence, and a CKY-style dynamic program over spans finds the binary tree with the largest total score."
solves: [constituency-parsing]
model: word-ram
complexity:
  vars: {n: the number of words, L: the number of labels including the empty label}
  time: {worst: Θ(n^3 + n^2 L), best: Θ(n^3 + n^2 L)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 2017
  people: [Mitchell Stern, Jacob Andreas, Dan Klein]
  note: "Stern, Andreas and Klein scored spans from differences of BiLSTM states and decoded exactly with a chart over spans, with no grammar."
prereqs: [probabilistic-cky, constituency-parsing]
see_also: [structured-prediction, hinge-loss, transformer, parseval-measures, a-star-parsing, biaffine-dependency-parser, semi-markov-crf, catalan-numbers]
sources:
  - paper: doi:10.18653/v1/P17-1076
    title: "Mitchell Stern, Jacob Andreas and Dan Klein, A Minimal Span-Based Neural Constituency Parser, ACL 2017"
    locator: "pp. 818-827; the span representation, the label and span scores, the chart parser, the top-down parser, the margin training with loss-augmented decoding, and the test results"
  - paper: doi:10.18653/v1/P18-1249
    title: "Nikita Kitaev and Dan Klein, Constituency Parsing with a Self-Attentive Encoder, ACL 2018"
    locator: pp. 2676-2686; the self-attentive encoder over the same span decoder and the results on the Penn Treebank
---

A span-based constituency parser splits [constituency parsing](/constituency-parsing/) into two parts. A neural network reads the sentence and gives a score to every pair of a span and a label. A chart decoder then finds the binary tree whose spans have the largest total score. The decoder is a CKY-style dynamic program like [probabilistic CKY](/probabilistic-cky/), but it has no grammar: any label can go on any span, and the tree score is a plain sum over spans. Stern, Andreas and Klein introduced this minimal form in 2017. The decoder is exact for this score and runs in cubic time. With a better encoder, the self-attentive encoder of Kitaev and Klein, the same kind of decoder reached 95.13 F1 on the Penn Treebank. This page is about the decoder and its training loss. The code takes the network outputs as given.

## In plain words

A parse tree of a sentence is a set of nested pieces, each piece a run of words with a name such as noun phrase or verb phrase. The parser first lets a neural network look at the whole sentence and give a number to every possible piece and every possible name. A high number means the network thinks that piece with that name belongs in the tree.

The parser then looks for the set of nested pieces with the largest sum of numbers. It does this from short pieces to long ones. For each piece it remembers the best way to cut it in two, so a long piece reuses the answers for its parts.

Some pieces get a special empty name. They exist only to keep the tree binary, and the parser removes them at the end. What remains is the final tree.

## The problem

The input is a sentence of $n \ge 1$ words and a label set $\{0, 1, \ldots, L - 1\}$, where label 0 is the empty label $\varnothing$. For every fencepost span $(i, j)$ with $0 \le i < j \le n$, which covers the words $i + 1$ to $j$, the network gives a label score $s_{\text{label}}(i, j, \ell)$ for every label and a span score $s_{\text{span}}(i, j)$. All scores are arbitrary reals.

A binary tree over the sentence is a set of $2n - 1$ spans: the root span $(0, n)$, the $n$ spans of one word, and for every span of more than one word a split $k$ with $i < k < j$ such that $(i, k)$ and $(k, j)$ are also in the set. Each span gets one label. The score of a labeled tree $T$ is

$$s(T) = \sum_{(i, j, \ell) \in T} \big[ s_{\text{label}}(i, j, \ell) + s_{\text{span}}(i, j) \big].$$

The task is to find a labeled binary tree of largest score. There are 1, 1, 2, 5, 14, 42, 132 binary trees over 1 to 7 words, the [Catalan numbers](/catalan-numbers/), so trying them all is exponential.

The binary tree is a coding of an ordinary treebank tree. Stern et al. binarize the gold tree and give the new spans the label $\varnothing$, and they turn a chain of unary nodes into one atomic label, such as S+VP. Words are not part of the label set: part-of-speech tags are not predicted. After decoding, the spans labeled $\varnothing$ are deleted, so the result can be n-ary, and the root can have more than one child.

In Stern et al. the span score enters through the two children at each split, so the root span has no span score. The code adds $s_{\text{span}}$ for every span of the tree, root included. Every tree contains the root span, so the two scores differ by the constant $s_{\text{span}}(0, n)$, and they have the same best tree.

## The algorithm

```pseudo id=main
CHART-PARSE(n, s_label, s_span)
L1  for len ← 1 to n do
L2      for i ← 0 to n - len do
L3          j ← i + len
L4          lab ← a label ℓ of largest s_label(i, j, ℓ);  v ← s_label(i, j, lab) + s_span(i, j)
L5          if len = 1 then best(i, j) ← v
L6          else split(i, j) ← the first k with i < k < j of largest best(i, k) + best(k, j)
L7               best(i, j) ← v + best(i, split(i, j)) + best(split(i, j), j)
L8          label(i, j) ← lab
L9  walk from (0, n): output (i, j, label(i, j)), and if j - i > 1 walk (i, split(i, j)) and (split(i, j), j)
L10 return best(0, n) and the 2n - 1 labeled spans of the walk
```

The label of a span does not depend on what is inside the span, and the split does not depend on the label. So line L4 picks the label once per span, in $O(L)$ time, and line L6 picks the split once per span, in $O(n)$ time. This is the main difference from probabilistic CKY, where the best split depends on the labels of the two children through the grammar rules.

The walk of line L9 uses an explicit stack, so a long sentence does not hit a recursion limit.

**Training.** Stern et al. train the network with a margin loss. For the binarized gold tree $T^*$, the Hamming loss $\Delta(T, T^*)$ counts the spans of $T$ whose label differs from the gold label, where a span that is not in $T^*$ has the gold label $\varnothing$. The hinge loss is

$$\max\Big(0,\ \max_T \big[s(T) + \Delta(T, T^*)\big] - s(T^*)\Big).$$

The inner maximum is computed by CHART-PARSE itself, after 1 is added to every label score $s_{\text{label}}(i, j, \ell)$ with $\ell$ different from the gold label of $(i, j)$. The loss is a [hinge loss](/hinge-loss/) for [structured prediction](/structured-prediction/), and its gradient flows into the network through the scores of the two trees.

## Example

Take the sentence *She enjoys playing tennis*, with $n = 4$ and the labels $\varnothing$, S, NP, VP. The scores below are made up for the example; in a real parser they come from the network.

| span | words | $\varnothing$ | S | NP | VP | $s_{\text{span}}$ |
|---|---|---|---|---|---|---|
| $(0, 1)$ | She | 0 | -2 | 2 | -1 | 0 |
| $(1, 2)$ | enjoys | 1 | -2 | -1 | 0 | 0 |
| $(2, 3)$ | playing | 1 | -1 | -1 | 0 | 0 |
| $(3, 4)$ | tennis | 0 | -2 | 2 | -1 | 0 |
| $(0, 2)$ | She enjoys | 0 | -1 | -1 | -1 | 0.8 |
| $(1, 3)$ | enjoys playing | 0.5 | -2 | -2 | 0 | 0.5 |
| $(2, 4)$ | playing tennis | 0 | -1 | 0 | 1.5 | 0 |
| $(0, 3)$ | She enjoys playing | 0 | -1 | -2 | -2 | 0 |
| $(1, 4)$ | enjoys playing tennis | 0 | -1 | -2 | 2 | 1 |
| $(0, 4)$ | the whole sentence | -1 | 3 | -1 | 0 | 0 |

The chart, in the order of lines L1 to L8. The column $v$ is the value of line L4, and the split column lists $\mathrm{best}(i, k) + \mathrm{best}(k, j)$ for each $k$.

| span | label | $v$ | splits | split | best |
|---|---|---|---|---|---|
| $(0, 1)$ | NP | 2 | | | 2 |
| $(1, 2)$ | $\varnothing$ | 1 | | | 1 |
| $(2, 3)$ | $\varnothing$ | 1 | | | 1 |
| $(3, 4)$ | NP | 2 | | | 2 |
| $(0, 2)$ | $\varnothing$ | 0.8 | $k = 1$: 3 | 1 | 3.8 |
| $(1, 3)$ | $\varnothing$ | 1 | $k = 2$: 2 | 2 | 3 |
| $(2, 4)$ | VP | 1.5 | $k = 3$: 3 | 3 | 4.5 |
| $(0, 3)$ | $\varnothing$ | 0 | $k = 1$: 5, $k = 2$: 4.8 | 1 | 5 |
| $(1, 4)$ | VP | 3 | $k = 2$: 5.5, $k = 3$: 5 | 2 | 8.5 |
| $(0, 4)$ | S | 3 | $k = 1$: 10.5, $k = 2$: 8.3, $k = 3$: 7 | 1 | 13.5 |

The walk of line L9 gives the seven spans $(0,4)$ S, $(0,1)$ NP, $(1,4)$ VP, $(1,2)$ $\varnothing$, $(2,4)$ VP, $(2,3)$ $\varnothing$, $(3,4)$ NP, with score 13.5. After the $\varnothing$ spans are deleted, the tree is (S (NP She) (VP enjoys (VP playing (NP tennis)))). The root has two children.

The greedy top-down decoder of Stern et al. picks the best label of a span and then the split $k$ with the largest $s_{\text{span}}(i, k) + s_{\text{span}}(k, j)$, from the root down. At the root the split values are 1, 0.8 and 0 for $k = 1, 2, 3$, so it takes $k = 1$, as the chart does. At $(1, 4)$ the values are 0 for $k = 2$ and 0.5 for $k = 3$, so it takes $k = 3$ and keeps the span *enjoys playing*, with the label $\varnothing$. Its tree is (S (NP She) (VP enjoys playing (NP tennis))) with score 13.0, and it misses the inner VP. The tests check both results and check the chart against all 5 binary trees and all labelings.

## Correctness

The claim is: CHART-PARSE stops and returns a labeled binary tree of largest score $s(T)$, together with that score. This is a theorem.

The proof has two steps. First, for a fixed set of spans the score is a sum with one term per span, and the term of a span depends only on its own label, so the best labeling takes the best label of each span. The problem becomes the choice of the spans, with the weight $m(i, j) = \max_\ell s_{\text{label}}(i, j, \ell) + s_{\text{span}}(i, j)$ on each span. Second, a binary tree over $(i, j)$ with more than one word is the span $(i, j)$, a split $k$, and two independent binary trees over $(i, k)$ and $(k, j)$. So the best weight satisfies

$$\mathrm{best}(i, j) = m(i, j) + \max_{i < k < j} \big[\mathrm{best}(i, k) + \mathrm{best}(k, j)\big],$$

which is what lines L4 to L7 compute, from short spans to long ones. Since the scores can be any reals, the same theorem applied to the augmented label scores shows that loss-augmented decoding maximizes $s(T) + \Delta(T, T^*)$ exactly. The full proof is in [the correctness proof](proofs/correctness.md).

The exactness is with respect to the factored score only. Whether the best-scoring tree is the right tree depends on the network, and that is a measurement, not a theorem.

## Complexity

**Time.** There are $n(n + 1)/2$ spans. Line L4 costs $O(L)$ per span, and line L6 costs $O(j - i)$ per span. The total is $\sum_{\text{len}=1}^{n} (n - \text{len} + 1)(\text{len} - 1) = (n^3 - n)/6$ split checks plus $O(n^2 L)$ for the labels, so the decoder takes $\Theta(n^3 + n^2 L)$ time on the [word RAM](/word-ram/), on every input. The cost of the network that produces the $O(n^2 L)$ scores is not included; for a BiLSTM or a [transformer](/transformer/) encoder it is often larger than the cost of the decoder.

**Space.** The tables best, split and label take $\Theta(n^2)$ space. The input scores themselves take $\Theta(n^2 L)$.

**Greedy decoding.** The top-down decoder computes $O(n)$ splits, each in $O(n)$ time, so it takes $O(n^2 + n L)$ time, but it is not exact.

## Properties

- **Exact for the model.** The decoder returns a tree of maximum score for any real scores. Ties are broken toward the first label and the smallest split.
- **No grammar.** Every label can appear on every span, and every pair of labels can be parent and child. The decoder cannot produce a tree that is ungrammatical, because there is no grammar to break.
- **Label and split separate.** The best label of a span and the best split below it are found independently. Probabilistic CKY with a grammar of $m$ nonterminals takes $O(n^3 g)$ for $g$ binary rules, while this decoder takes $O(n^3 + n^2 L)$.
- **Fixed size.** Every binary tree over $n$ words has $2n - 1$ spans, so trees of different shapes are compared over the same number of terms.
- **n-ary output.** Deleting the $\varnothing$ spans turns the binary tree into an n-ary tree. The root span can also get the label $\varnothing$; the code then puts a placeholder label on the root, and a parser can forbid $\varnothing$ at $(0, n)$ instead.
- **Measurement.** Stern et al. report test F1 of 91.69 for the chart parser and 91.58 for the greedy top-down parser on the Penn Treebank. Kitaev and Klein report 93.55 with a self-attentive encoder and the same kind of chart decoder, and 95.13 with pre-trained word representations.

## Variants and improvements

- **The span representation.** Stern et al. represent the span $(i, j)$ by $[f_j - f_i;\ b_i - b_j]$, the differences of forward and backward BiLSTM states at its two fenceposts, and compute the label scores by a feedforward network with one output per label. Kitaev and Klein keep the decoder and replace the BiLSTM by a self-attentive encoder built from [multi-head attention](/multi-head-attention/).
- **Top-down greedy decoding.** The decoder of the example picks splits by span scores alone, from the root down. It is faster and lost little accuracy in the measurements of Stern et al., but it is not exact.
- **Sum instead of max.** Replacing max by a log-sum-exp in lines L4, L6 and L7 gives the log of the sum of $\exp s(T)$ over all labeled trees, the partition function of a tree-structured [conditional random field](/conditional-random-field/). This allows training by likelihood instead of the margin.
- **Pruning and faster decoders.** Since the label scores are known in advance, spans whose best label score is very low can be removed before the chart is filled. This is a heuristic and can lose the best tree.
- **The same idea for other structures.** Scoring spans and decoding exactly is also the basis of the [semi-Markov CRF](/semi-markov-crf/) for segmentation, where the spans do not nest, and of the [biaffine dependency parser](/biaffine-dependency-parser/), which scores word pairs instead of spans.

## When to use it

Use this decoder when a neural network can score spans and an exact, simple decoder is wanted. It needs no grammar, no rule extraction and no binarization of a grammar, only a binarized training tree. For sentences of ordinary length the cubic loop is usually cheap next to the encoder, but this is an observation about typical inputs, not a bound. For very long inputs or tight time budgets, the greedy top-down decoder or a transition-based parser is faster. When a grammar with hard constraints is needed, use [probabilistic CKY](/probabilistic-cky/) or [A* parsing](/a-star-parsing/) instead. Evaluate the result with the [PARSEVAL measures](/parseval-measures/) after the $\varnothing$ spans are deleted and the unary chains are expanded.

## Pitfalls

- **The split range.** Writing line L6 as "for k ← i to j" lets a span split into itself and an empty span. The right line is "the first k with i < k < j".
- **The bonus in the loss.** Writing the augmented score as $s_{\text{label}}(i, j, \ell) + [\ell = \ell^*(i, j)]$ rewards agreement with the gold tree, so the decoder looks for trees close to it and the loss is never 0. The right score is $s_{\text{label}}(i, j, \ell) + [\ell \ne \ell^*(i, j)]$, which rewards mistakes, so that the decoder finds the tree that violates the margin most.
- **Forgetting the empty gold label.** A span that is not in the binarized gold tree has the gold label $\varnothing$. Skipping such spans when adding the bonus makes the loss ignore extra brackets.
- **Length-one spans.** For a span of one word the loop of line L6 is empty. Without the base case of line L5, best$(i, i + 1)$ is undefined. Line L5 sets it to $v$.
- **Scoring with $\varnothing$ spans.** PARSEVAL counts the brackets of the n-ary tree. Counting the $\varnothing$ spans of the binary tree, or not expanding a unary chain label such as S+VP into its two nodes, gives wrong precision and recall.
- **Greedy is not exact.** The example shows a tree of score 13.0 from the greedy decoder against 13.5 from the chart. Use the chart for loss-augmented decoding, since a greedy maximum can make the hinge loss too small.

## Implementations

## History

Before 2016, statistical constituency parsers scored grammar rules, as in [lexicalized PCFGs](/lexicalized-pcfg/) and [latent-variable PCFGs](/latent-variable-pcfg/). The first neural constituency parsers used transition systems or sequence models, and some of them already used BiLSTM features of spans. Stern, Andreas and Klein (2017) showed that the span scores are enough: with no grammar and no transition system, a chart over spans, trained with a margin loss and loss-augmented decoding, gave 91.69 F1 on the Penn Treebank. Kitaev and Klein (2018) kept the decoder, replaced the encoder by self-attention and reached 93.55 F1, and 95.13 with pre-trained representations. Later parsers kept the span chart and changed the encoder or the training loss.

## References
