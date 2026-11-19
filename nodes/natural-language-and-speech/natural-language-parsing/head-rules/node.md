---
tag: EXAQEX
kind: algorithm
slug: head-rules
name: Head rules
aliases:
- head percolation table
- Magerman-Collins head rules
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "A table that picks the head child of each phrase type, used to lexicalize trees and to convert constituency trees to dependencies."
model: word-ram
complexity:
  vars: {n: the number of words, s: the number of nodes of the tree, l: the length of the longest priority list of the table}
  time: {worst: O(s l), best: Θ(s)}
  space: {extra: Θ(s)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1995
  people: [David M. Magerman, Michael Collins]
  note: Magerman used a head table to pass head words up the trees of his decision-tree parser in 1995; Collins revised it for his lexicalized parsers and printed it in his 1999 thesis.
prereqs: [parse-tree, treebank]
see_also: [lexicalized-pcfg, dependency-tree, projective-dependency-tree, dependency-parsing, constituency-parsing, attachment-score, dependency-model-with-valence, eisner-algorithm]
sources:
  - paper: "Michael Collins, Head-Driven Statistical Models for Natural Language Parsing, PhD thesis, University of Pennsylvania (1999)"
    title: "Michael Collins, Head-Driven Statistical Models for Natural Language Parsing, PhD thesis"
    locator: "Appendix A, the head table and the special rule for NP"
  - paper: doi:10.3115/981658.981695
    title: "David M. Magerman, Statistical Decision-Tree Models for Parsing, ACL 1995"
    locator: pp. 276 to 283
  - paper: doi:10.1162/089120103322753356
    title: "Michael Collins, Head-Driven Statistical Models for Natural Language Parsing, Computational Linguistics 29(4), 2003"
    locator: "pp. 589 to 637, the head-driven models that use the head table"
  - paper: doi:10.3115/1218955.1219016
    title: "Dan Klein and Christopher D. Manning, Corpus-Based Induction of Syntactic Structure, Models of Dependency and Constituency, ACL 2004"
    locator: "the evaluation section, gold dependencies read off the Penn Treebank with the Collins head rules, and the change of the NP head to the determiner"
  - url: https://github.com/stanfordnlp/CoreNLP/blob/main/src/edu/stanford/nlp/trees/CollinsHeadFinder.java
    title: "Stanford CoreNLP, CollinsHeadFinder, an implementation of the head finder of the Collins thesis"
    locator: the table nonTerminalInfo and the coordination fix in postOperationFix
---

Head rules pick, for each phrase in a [parse tree](/parse-tree/), the one child that is its head: the verb phrase in a sentence, the noun in a noun phrase, the preposition in a prepositional phrase. The rules are a table indexed by the parent label. Each entry gives a scan direction and a priority list of child labels. Once every phrase has a head child, each phrase gets a head word passed up from below. This is what a [lexicalized PCFG](/lexicalized-pcfg/) needs, and it also turns a constituency tree into a [dependency tree](/dependency-tree/): the head word of each non-head child depends on the head word of the phrase. Magerman used such a table in 1995 and Collins published the version that most later work copies in his 1999 thesis. The conversion is linear in the size of the tree. The table itself is a heuristic: it encodes linguistic choices, and other tables give other heads.

## In plain words

A phrase such as "the big dog" is about one word, "dog", its head. If we know the head of every phrase, we know which word each other word attaches to: "the" and "big" attach to "dog", and "dog" attaches to whatever word heads the phrase above it.

The head rules find the head with a short recipe for each kind of phrase. For a prepositional phrase, look from the right for a preposition. For a verb phrase, look from the left for a verb, then a modal, then another verb phrase, and so on down a list. If nothing in the list is found, take the first child on the side where the search starts. Noun phrases have their own recipe, which looks for the last noun.

Applied from the bottom of the tree to the top, this gives every word one head word: a dependency tree.

## The problem

The input is a constituency tree $t$ over the words $w_1, \ldots, w_n$, such as a tree of the Penn [treebank](/treebank/): internal nodes carry phrase labels (S, NP, VP, PP, ...), preterminals carry part-of-speech tags, and the leaves are the words. The output has two parts.

1. For each internal node $v$ with children $u_1, \ldots, u_m$, an index $c(v) \in \{1, \ldots, m\}$, the head child. The head word $\mathrm{head}(v)$ is the word of $v$ itself if $v$ is a preterminal, and $\mathrm{head}(u_{c(v)})$ otherwise.
2. The dependency tree $h$: for every word $d$, its head $h(d) \in \{0, \ldots, n\}$, with 0 the artificial root. At each node $v$ and each child $u_k$ with $k \ne c(v)$, the word $\mathrm{head}(u_k)$ gets the head $\mathrm{head}(v)$. The head word of the whole tree gets the head 0, so the root has exactly one child.

There is no single correct answer to part 1. A head table is a convention, and the problem is to apply a given table exactly. The rest of this page uses the table of Collins (1999), with the labels of the Penn Treebank. Function tags and indices are removed before lookup, so NP-SBJ-1 is looked up as NP.

## The algorithm

A table entry is a pair (dir, list). "Left" means the children are scanned from the left, "right" from the right. The outer loop goes through the list in priority order and the inner loop through the children, so a label early in the list beats a label that is closer to the start. Part of the Collins table:

| parent | dir | priority list |
|---|---|---|
| S | left | TO IN VP S SBAR ADJP UCP NP |
| VP | left | TO VBD VBN MD VBZ VB VBG VBP VP ADJP NN NNS NP |
| PP | right | IN TO VBG VBN RP FW |
| SBAR | left | WHNP WHPP WHADVP WHADJP IN DT S SQ SINV SBAR FRAG |
| ADJP | left | NNS QP NN \$ ADVP JJ VBN VBG ADJP JJR NP JJS DT FW RBR RBS SBAR RB |
| ADVP | right | RB RBR RBS FW ADVP TO CD JJR JJ IN NP JJS NN |
| PRN | left | (empty) |
| FRAG | right | (empty) |

The implementation holds the full table, with 24 entries and the NP rule. NP has its own rule, NP-HEAD, which goes by position within a set of labels: the first child from the right that is a noun tag, not the noun with the highest priority.

```pseudo id=main
HEAD-CHILD(X, Y1 … Ym)                 ▷ X: parent label; Y1 … Ym: child labels
L1  if m = 1 then return 1
L2  if X = NP then return NP-HEAD(Y1 … Ym)
L3  (dir, list) ← table[X], or (left, empty list) if X has no entry
L4  order ← 1, 2, …, m if dir = left, else m, m-1, …, 1
L5  for each label Z in list, in priority order do
L6      for each k in order do
L7          if Yk = Z then return k
L8  return the first index of order

DEPENDENCIES(t)                          ▷ t: a tree over the words w1 … wn
L9  for each node v of t, children before parents do
L10     if v is a preterminal over word i then head(v) ← i
L11     else c ← HEAD-CHILD(label of v, labels of its children u1 … um);  head(v) ← head(uc)
L12          for each k ≠ c do h(head(uk)) ← head(v)
L13 h(head(root)) ← 0
L14 return h

NP-HEAD(Y1 … Ym)
L15 if Ym = POS then return m
L16 for each step (dir, set) in the list below, in order do
L17     for each k in the order of dir do
L18         if Yk ∈ set then return k
L19 return m
```

The steps of line L16 are: from the right, any of NN NNP NNPS NNS NX POS JJR; from the left, NP; from the right, any of \$ ADJP PRN; from the right, CD; from the right, any of JJ JJS RB QP. Line L15 makes the possessive marker the head of a possessive NP such as "John 's", so that the whole phrase can attach to the noun it modifies. Line L8 is the fallback when no child label is in the list; for the entries with an empty list, such as PRN and FRAG, it is the only rule. Lines L9 to L12 visit the tree children first, so the head words of the children are known when line L11 needs them. The implementation keeps them on a stack instead of using recursion, because treebank trees can be deep.

## Example

Take the tree

$$[_S\ [_{NP\text{-}SBJ}\ \text{The company}]\ [_{VP}\ [_{MD}\ \text{will}]\ [_{VP}\ [_{VB}\ \text{sell}]\ [_{NP}\ \text{its assets}]\ [_{PP}\ [_{TO}\ \text{to}]\ [_{NP}\ \text{investors}]]]]\ [_.\ .]]$$

with the words numbered 1 to 9: The, company, will, sell, its, assets, to, investors, ".". The preterminals are DT NN, MD, VB, PRP\$ NNS, TO, NNS and the period. The walk finishes the phrases in this order.

| step | node | child labels | rule that fires | head child | head word | arcs written |
|---|---|---|---|---|---|---|
| 1 | NP-SBJ | DT NN | NP-HEAD, first step | NN | company | The → company |
| 2 | NP | PRP\$ NNS | NP-HEAD, first step | NNS | assets | its → assets |
| 3 | NP | NNS | line L1 | NNS | investors | none |
| 4 | PP | TO NP | PP, right: no IN, then TO | TO | to | investors → to |
| 5 | VP | VB NP PP | VP, left: VB is the first label of the list present | VB | sell | assets → sell, to → sell |
| 6 | VP | MD VP | VP, left: MD comes before VP in the list | MD | will | sell → will |
| 7 | S | NP-SBJ VP . | S, left: no TO or IN, then VP | VP | will | company → will, . → will |

Line L13 gives "will" the head 0. The result, with $h(d)$ for $d = 1, \ldots, 9$, is $h = (2, 3, 0, 3, 6, 4, 4, 7, 3)$. Step 6 shows a choice of the table: Collins makes the modal the head of the verb group, so the main verb "sell" depends on "will". Universal Dependencies makes the opposite choice. The tests check this tree and the sentence of Figure 1 of Klein and Manning (2004), "Factory payrolls fell in September", whose result $h = (2, 3, 0, 3, 4)$ matches the dependencies in that figure.

## Correctness

Whatever the table says, the output is a dependency tree in the sense of the area: every word has exactly one head, the root 0 has exactly one child, there is no cycle, and the tree is projective. Each constituent is a connected piece of it: exactly one word of its span, the head word, has its head outside the span.

The key invariant is about a finished node $v$: every word of its span except $\mathrm{head}(v)$ has its final head inside the span and reaches $\mathrm{head}(v)$ by following heads. A new node keeps the invariant because line L12 attaches the head words of the other children to the head word of the head child, and no later step touches a word of the span except $\mathrm{head}(v)$. Projectivity follows because an arc written at $v$ joins two words of the span of $v$, every word between them is in that span, and every word of the span is below $\mathrm{head}(v)$. The full proof is in [the correctness proof](proofs/correctness.md).

This is a theorem about the shape of the output. That the heads are linguistically right is a different claim, and it is only a heuristic.

## Complexity

**Time.** For a node with $m$ children, HEAD-CHILD runs the loop of lines L5 to L7 at most $\ell \cdot m$ times, where $\ell$ is the length of the longest priority list. The sum of $m$ over all nodes is $s - 1$ for a tree of $s$ nodes, so the time is $O(s \ell)$ on the [word RAM](/word-ram/). With a fixed table, $\ell \le 18$ is a constant and the time is $\Theta(s)$. If the first label of each list matches at once, every node costs $O(1)$ after its children, which gives the best case $\Theta(s)$.

**Space.** The explicit stack of the walk and the stack of head words hold $O(s)$ entries, and the output has $n + 1$ entries.

## Properties

- **Deterministic and total.** Every node gets exactly one head child, because line L8 always has an answer.
- **The output is projective.** No conversion by head rules can produce crossing arcs. Non-projective structure in a treebank lives in its traces and empty elements, which head rules ignore.
- **One root child.** The root gets exactly one dependent, the head word of the top node.
- **Local.** The head of a node depends only on its own label and the labels of its children, not on the words.
- **The list order beats the child order.** The outer loop runs over the list, so a VP with the children NN VBD picks VBD, the second child, because VBD comes before NN in the list.

## Variants and improvements

- **Coordination.** Collins also moves the head in a coordinated phrase: when the child just before the chosen head is CC, the head moves to the conjunct before it. The CoreNLP implementation does this in a separate step. The code on this page leaves it out.
- **Other tables.** Some later converters choose content words as heads, so the main verb heads a verb group and the noun heads a prepositional phrase. Universal Dependencies follows this choice. The algorithm stays the same; only the table changes, and the code takes the table as an argument.
- **Lexicalization.** In a [lexicalized PCFG](/lexicalized-pcfg/), each nonterminal carries its head word and tag. The head rules decide which child passes its head up, and the model generates the other children as dependents of that head.

## When to use it

Use a head table when a treebank has only phrase-structure trees and you need head words: to train a lexicalized parser, to make gold dependencies for [dependency parsing](/dependency-parsing/) or an [attachment score](/attachment-score/), or to evaluate an unsupervised model such as the [dependency model with valence](/dependency-model-with-valence/). Use the same table for training and evaluation, and name it. If the treebank already has dependency annotation, use that instead.

## Pitfalls

- **Priority order and position order mixed up.** Lines L5 and L6 loop over the list first and the children second. Swapping them makes line L7 return the first child in the scan whose label is anywhere in the list. For a VP with the children NN VBD, the swapped loops return NN, while the right answer is VBD, which comes earlier in the list.
- **Function tags not stripped.** The Penn Treebank writes NP-SBJ, PP-LOC or NP-1. Looking these up without removing the suffix makes line L3 miss the entry and fall back to the leftmost child.
- **Empty elements and traces.** Remove -NONE- preterminals and their empty parents before line L9, or they become words of the dependency tree.
- **Different tables give different scores.** Klein and Manning (2004) report that making determiners the heads of noun phrases changes the directed accuracy of their model on WSJ10 from 43.2% to 55.7%. This is a measurement. An attachment score is only comparable with the same head table.
- **Deep trees.** A recursive walk can hit Python's recursion limit on long right-branching phrases. Line L9 needs an explicit stack.

## Implementations

## History

Head words entered statistical parsing in the early 1990s, when parsers began to condition rule choices on lexical items. Magerman (1995) passed head words up the trees of his decision-tree parser with a table of this kind. Collins revised the table for his parsers of the late 1990s and printed it in appendix A of his 1999 thesis, together with the special NP rule. That table, as implemented in tools such as the CollinsHeadFinder of Stanford CoreNLP, became the standard way to read dependencies off the Penn Treebank, and it was used to make the gold dependencies of many papers, for example the WSJ10 evaluation of Klein and Manning (2004).

## References
