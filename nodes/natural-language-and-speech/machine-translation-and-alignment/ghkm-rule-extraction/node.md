---
tag: 6NN595
kind: algorithm
slug: ghkm-rule-extraction
name: GHKM rule extraction
aliases:
- string-to-tree rule extraction
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: Extract minimal rules that pair a fragment of the target parse tree with a source string, cutting the word-aligned tree at its frontier nodes.
solves: [machine-translation]
model: word-ram
complexity:
  vars: {n: the number of nodes of the target tree, m: the source sentence length}
  time: {worst: "O(n m)"}
  space: {extra: "O(n m)"}
properties: {deterministic: true, exact: true, online: false, recursive: true}
history:
  year: 2004
  people: [Michel Galley, Mark Hopkins, Kevin Knight, Daniel Marcu]
  note: Galley, Hopkins, Knight and Marcu (2004) defined the frontier set of a word-aligned tree and the minimal rules it gives. Galley et al. (2006) added composed rules, the handling of unaligned words, and probability estimates for the rules.
prereqs: [word-alignment, parse-tree, synchronous-context-free-grammar]
see_also: [phrase-pair-extraction, hierarchical-phrase-based-translation, cube-pruning, constituency-parsing, treebank, syntax-directed-translation, inversion-transduction-grammar, tree-adjoining-grammar]
sources:
  - paper: "Michel Galley, Mark Hopkins, Kevin Knight and Daniel Marcu, What's in a translation rule?, HLT-NAACL 2004, pages 273 to 280, ACL Anthology N04-1035"
    title: Galley, Hopkins, Knight and Marcu 2004
    locator: the span and complement span of a node, the frontier set, and the extraction of minimal rules from the frontier graph
  - paper: "Michel Galley, Jonathan Graehl, Kevin Knight, Daniel Marcu, Steve DeNeefe, Wei Wang and Ignacio Thayer, Scalable inference and training of context-rich syntactic translation models, COLING-ACL 2006, pages 961 to 968, ACL Anthology P06-1121"
    title: Galley et al. 2006
    locator: composed rules, the attachments of unaligned words, and the estimation of rule probabilities
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 11 (tree-based models: learning syntactic translation rules)"
---

GHKM rule extraction reads a sentence pair with a parse tree of the target sentence and a [word alignment](/word-alignment/), and cuts the tree into translation rules. Each rule pairs a fragment of the target tree with a string of source words and variables, and the cuts are made only at *frontier nodes*, the nodes whose aligned source words form a block that no outside link reaches into. The rules found this way are the *minimal rules*; together they derive exactly the given tree and source sentence. They are the training step of string-to-tree syntax-based translation, where the decoder parses the source and builds a target tree.

## In plain words

Take a sentence, its translation, a parse tree of the translation, and lines between words that mean the same thing. Look at one node of the tree and the source words that are joined to the words under it. If those source words form one block, and no source word inside the block is joined to a word outside the node, the node is a good place to cut. It is a frontier node.

Now cut the tree at all frontier nodes. Each piece reaches from one frontier node down to the next ones, and becomes a rule: on one side the piece of tree, with the lower frontier nodes as holes, and on the other side the block of source words, with the blocks of the holes as holes too. Put all the pieces back together and you get the whole tree and the whole sentence again.

## The problem

Translation in the final system runs from a source sentence $f = f_1 \ldots f_m$ to a target sentence $e = e_1 \ldots e_l$ with its parse tree. The extraction input is $f$, a parse tree $T$ of $e$ whose leaves are the target positions $1, \ldots, l$, and a set $A$ of links $(j, i)$ from source position $j$ to target position $i$. For an internal node $n$ of $T$ with leaf set $Y(n)$:

- $\mathrm{span}(n) = \{j : (j, i) \in A, i \in Y(n)\}$, the source positions aligned to the words under $n$;
- $\mathrm{comp}(n) = \{j : (j, i) \in A, i \notin Y(n)\}$, the complement span, the source positions aligned to the words outside $n$;
- $n$ is a *frontier node* if $\mathrm{span}(n) \ne \emptyset$ and the closure $[\min \mathrm{span}(n), \max \mathrm{span}(n)]$ holds no position of $\mathrm{comp}(n)$.

The output is the set of *minimal rules*, one for each frontier node $n$. Its left side is the tree fragment from $n$ down to the next frontier nodes, which become variables $x_0, x_1, \ldots$, or down to words. Its right side is the source positions of the closure of $\mathrm{span}(n)$ in order, with the closure of each variable node replaced by its variable. This page gives the root the whole range $1, \ldots, m$, and lets an unaligned source word be taken by the lowest frontier node whose range holds it.

The rules pair a target tree fragment with a source string. Galley et al. (2004) read them in the direction of the noisy channel, from the English tree to the foreign string, which is why they are often called tree-to-string rules. A string-to-tree decoder uses them the other way: it parses the source string and builds the target tree.

## The algorithm

```pseudo id=main
GHKM(T, f, A)
L1  for each node n, children first: span(n) ← union of the spans of its children and the positions aligned to its leaf children
L2  comp(root) ← ∅; for each node n, parents first, and each child k of n: comp(k) ← comp(n) ∪ the spans of the other children of n
L3  F ← { n : span(n) ≠ ∅ and no position of comp(n) lies in [min span(n), max span(n)] }
L4  for each n in F, in tree order do
L5      lhs ← the fragment below n: a child in F becomes a new variable x_q, a leaf stays a word, any other child is expanded
L6      R ← [1, m] if n is the root, else [min span(n), max span(n)]
L7      rhs ← the positions of R from left to right, where the closure of the span of variable x_q is written once as x_q and every other position j as f_j
L8      output the rule lhs → rhs
L9  return the rules
```

Line L2 works because the leaves outside a child $k$ of $n$ are the leaves outside $n$ plus the leaves under the siblings of $k$. Line L7 is well defined because the closures of the variables of one rule are disjoint and lie inside $R$, which the proofs file shows.

## Example

Take the French source $f$ = il ne va pas and the English tree S(NP(PRP he) VP(AUX does, RB not, VB go)), with the links il to he, ne to not, va to go and pas to not. The word does is not aligned. The spans and complement spans are

| node | span | closure | complement span | frontier? |
|---|---|---|---|---|
| S | 1, 2, 3, 4 | 1 to 4 | none | yes |
| NP, PRP | 1 | 1 | 2, 3, 4 | yes |
| VP | 2, 3, 4 | 2 to 4 | 1 | yes |
| AUX | none | | 1, 2, 3, 4 | no (empty span) |
| RB | 2, 4 | 2 to 4 | 1, 3 | no (3 is inside) |
| VB | 3 | 3 | 1, 2, 4 | yes |

RB is not a frontier node, because not is linked to both ne and pas, and va lies between them but belongs to go. The five minimal rules are

| node | left side (target tree fragment) | right side (source) |
|---|---|---|
| S | S($x_0$:NP $x_1$:VP) | $x_0$ $x_1$ |
| NP | NP($x_0$:PRP) | $x_0$ |
| PRP | PRP(he) | il |
| VP | VP(AUX(does) RB(not) $x_0$:VB) | ne $x_0$ pas |
| VB | VB(go) | va |

The VP rule is the interesting one: it learns that "ne ... pas" around a verb becomes "does not" before it, with an English word, does, that has no source counterpart. A phrase-based model could not state this with a gap. Substituting the rules into each other gives back the tree and "il ne va pas".

**Unaligned source words.** With the tree S(NP(DT the, NN house) VP(VBZ is, JJ small)), the source das haus ist ja klein, and the links das to the, haus to house, ist to is and klein to small, the word ja is not aligned. It lies in the closure 3 to 5 of the VP, so the VP rule is VP($x_0$:VBZ $x_1$:JJ) → $x_0$ ja $x_1$.

## Correctness

The proofs file shows three facts. Lines L1 to L3 compute the spans, the complement spans and the frontier set as defined. In each rule, the closures of the variable nodes are disjoint and lie in the range of the rule, so the right side has each variable once. And applying the rules from the root down gives back the target tree and the whole source sentence. The extraction is exact for its definition; whether the rules translate well depends on the parse and the alignment. The test file compares the frontier set with a direct form of the definition on 500 random trees and alignments, and checks that the rules derive the input.

## Complexity

Count in the [word RAM](/word-ram/) model, with the spans as bit sets or sorted lists of at most $m$ positions. Line L1 does $O(n)$ unions of sets of size at most $m$, and line L2 the same if each node keeps the union of its children's spans and subtracts, or combines prefix and suffix unions of its children. Line L3 costs $O(m)$ for each node. Each node is inside one fragment, and each range has at most $m$ positions, so lines L4 to L8 cost $O(n + |F| m)$. The total is $O(n m)$ time and space for one sentence pair.

## Properties

- **Unique minimal rules.** Given the tree, the alignment and the convention for unaligned words, the set of minimal rules is fixed by the definition: there is one rule for each frontier node.
- **Derives the input.** The rules form one derivation of the sentence pair.
- **Rules can be large.** When the alignment crosses a lot, few nodes are frontier nodes, and a rule may cover a large part of the tree.
- **Many-to-many words.** A rule can hold target words with no source word (does above) and source words with no target word (ja above).
- **Reordering in the rule.** The order of the variables on the right side can differ from the left side, so the rules reorder whole constituents.

## Variants and improvements

- **Composed rules.** Galley et al. (2006) join adjacent minimal rules into larger rules, up to a size limit, which gives more context and better translations in their measurements.
- **All attachments of unaligned words.** Instead of one fixed attachment, Galley et al. (2006) consider every frontier node that an unaligned source word can attach to, and weight the derivations by expectation maximization.
- **Tree-to-string and tree-to-tree.** With a parse of the source instead of the target, the same frontier test gives rules for tree-to-string decoding, and with parses of both, for tree-to-tree models.
- **Binarization and relabeling.** Restructuring the tree (for example binarizing flat nodes) creates more frontier nodes and smaller rules.
- **Hierarchical rules without syntax.** [Hiero](/hierarchical-phrase-based-translation/) extracts rules with gaps from any consistent [phrase pair](/phrase-pair-extraction/), with one nonterminal label, instead of only at tree nodes.

## When to use it

Use GHKM to train a string-to-tree system, where target syntax should guide reordering and output grammar, for language pairs with very different word order such as Chinese to English or German to English. It needs a good target parser and a reasonably precise alignment, because one wrong link can remove frontier nodes. Without a parser, use [Hiero](/hierarchical-phrase-based-translation/) or a [phrase-based model](/phrase-based-translation-model/).

## Pitfalls

- **Testing the span instead of its closure.** A node can have aligned positions with a gap that holds a word aligned elsewhere, as for RB above. Test the closure against the complement span.
- **Losing unaligned source words.** If unaligned words outside every closure are not attached somewhere, the rules no longer derive the whole sentence. Give the root the whole range, or attach them to a neighbouring node.
- **Counting leaves as frontier nodes.** Only internal nodes can be frontier nodes; the words are the terminals of the rules.
- **Variable order.** Number the variables in the order of the tree, and write them on the source side in source order. Mixing the two scrambles the reordering.
- **Rule size.** Composed rules grow fast. Limit their size, or the rule table becomes too large to store.

## Implementations

## History

Yamada and Knight (2001) had proposed a syntax-based channel model with fixed node operations. Galley, Hopkins, Knight and Marcu (2004) asked which tree-to-string rules a word-aligned parse tree can explain, defined the frontier set, and showed how to extract the minimal rules. The name GHKM comes from the initials of these four authors. Galley et al. (2006) made the method practical with composed rules, the handling of unaligned words, and rule probabilities, and it became the rule extractor of string-to-tree systems such as the ISI system and the syntax mode of Moses.

## References
