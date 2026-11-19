---
tag: FJT4Y5
kind: definition
slug: treebank
name: Treebank
aliases:
- syntactically annotated corpus
area: natural-language-and-speech/natural-language-parsing
level: intro
summary: "A corpus of sentences annotated with their syntactic trees, used to read off grammars and to train and test parsers."
prereqs: [parse-tree, context-free-grammar]
see_also: [probabilistic-context-free-grammar, constituency-parsing, parseval-measures, head-rules, parent-annotation, dependency-tree, maximum-likelihood-estimation, part-of-speech-tagging]
sources:
  - paper: "Mitchell P. Marcus, Beatrice Santorini and Mary Ann Marcinkiewicz, Building a Large Annotated Corpus of English, The Penn Treebank, Computational Linguistics 19(2), 1993"
    title: "Marcus, Santorini and Marcinkiewicz, Building a Large Annotated Corpus of English, The Penn Treebank"
    locator: "pp. 313-330; the part-of-speech tagset, the bracketing scheme and the annotation process"
  - paper: "Eugene Charniak, Tree-bank Grammars, Proceedings of AAAI-96"
    title: "Eugene Charniak, Tree-bank Grammars"
    locator: "the grammar read off the Wall Street Journal trees, its 15953 rules, and its bracket precision and recall"
  - paper: doi:10.3115/1075096.1075150
    title: "Dan Klein and Christopher D. Manning, Accurate Unlexicalized Parsing, ACL 2003"
    locator: "pp. 423-430; Figure 2, the F1 of the plain treebank grammar"
---

A treebank is a collection of sentences, each paired with a syntactic tree that a trained annotator has checked. The trees follow a written scheme, which fixes the labels, the shape of each construction and the treatment of punctuation and of missing words. A treebank serves three purposes in parsing: grammars are read off its trees, statistical parsers are trained on it, and parsers are tested against its held-out trees with the [PARSEVAL measures](/parseval-measures/). The best known is the Penn Treebank of Marcus, Santorini and Marcinkiewicz (1993), whose Wall Street Journal part is the usual benchmark for English [constituency parsing](/constituency-parsing/). A treebank can also hold [dependency trees](/dependency-tree/) instead of phrase structure trees.

## Definition

An annotation scheme fixes a set of word categories (the part-of-speech tags), a set of phrase labels, and rules for drawing a tree over a sentence. A **treebank** under such a scheme is a finite sequence of pairs

$$D = \big( (w^{(1)}, t^{(1)}), \ldots, (w^{(K)}, t^{(K)}) \big),$$

where each $w^{(k)}$ is a tokenized sentence and each $t^{(k)}$ is a [parse tree](/parse-tree/) whose yield is $w^{(k)}$ and whose labels come from the scheme. In a constituency treebank, the leaves are the words, the parents of the leaves are the tags (the preterminals), and the other nodes carry phrase labels such as S, NP and VP. In a dependency treebank, $t^{(k)}$ is a set of arcs from heads to dependents.

**The treebank grammar.** For every internal node of every tree, with label $A$ and children labeled $\alpha = X_1 \cdots X_k$, the treebank contains one occurrence of the rule $A \to \alpha$. The treebank grammar has these rules, with the relative frequency estimate

$$q(A \to \alpha) = \frac{\mathrm{count}(A \to \alpha)}{\sum_{\beta} \mathrm{count}(A \to \beta)},$$

which is the [maximum likelihood estimate](/maximum-likelihood-estimation/) of a [PCFG](/probabilistic-context-free-grammar/) from fully observed trees. This is a theorem: the log likelihood of the trees separates into one multinomial per left side $A$, and the relative frequencies maximize each one.

**The Penn Treebank.** The trees of the Wall Street Journal part are divided into sections 00 to 24. The standard split for parsing is sections 02 to 21 for training, section 22 for development and section 23 for test. Each tree is wrapped in an outer bracket without a label, which has one child, usually S. Parsers usually remove the function tags (as in NP-SBJ) and the empty elements (tag -NONE-) before training. In the Universal Dependencies treebanks, the root of every dependency tree has exactly one child.

## Examples and non-examples

- **A four-tree treebank.** The trees

  (S (NP (PRP she)) (VP (VBD saw) (NP (DT the) (NN cat)))), (S (NP (PRP he)) (VP (VBD fed) (NP (DT the) (NN dog)))), (S (NP (DT the) (NN dog)) (VP (VBD saw) (NP (PRP her)))), (S (NP (PRP they)) (VP (VBD left)))

  form a small treebank. Its grammar has the rules $S \to NP\ VP$ with probability 1, $NP \to PRP$ with $4/7$, $NP \to DT\ NN$ with $3/7$, $VP \to VBD\ NP$ with $3/4$ and $VP \to VBD$ with $1/4$, and lexical rules such as $VBD \to saw$ with $2/4 = 1/2$. The tree of *they left* has probability $1 \cdot 4/7 \cdot 1/4 \cdot 1/4 \cdot 1/4 = 1/112$. These exact values are checked by the tests of [parent annotation](/parent-annotation/), which uses the same treebank.
- **The Penn Treebank grammar.** Charniak (1996) read a grammar off about a million words of Wall Street Journal trees. It had 15953 rules, of which 6785 occur more than once. Parsing the part-of-speech tags of test sentences of 2 to 40 words, it reached a bracket precision of 82.0 and a recall of 80.0. Charniak argued that such grammars do better than was commonly believed. This is a measurement.
- **A measured baseline.** Klein and Manning (2003) report an F1 of 72.62 for the plain treebank grammar, with 9657 rules, on their development set. Their preprocessing differs from Charniak's, so the two results are not directly comparable. Tree transforms such as [parent annotation](/parent-annotation/) and models with head words such as [lexicalized PCFGs](/lexicalized-pcfg/) improve on it.
- **Non-example: a tagged corpus.** A corpus in which each word has a part-of-speech tag but no tree is not a treebank. It trains [part-of-speech taggers](/part-of-speech-tagging/), but no grammar can be read off it.
- **Non-example: a grammar.** A hand-written grammar describes the trees that are allowed, but it is not a treebank: it says nothing about which tree is right for a given sentence, or how often a rule is used.
- **Non-example: parser output.** A corpus parsed automatically, without checking by annotators, has the form of a treebank, but its trees contain the errors of the parser. Training on it and testing on it measure the parser against itself.

## Related definitions

- [Parse tree](/parse-tree/) and [context-free grammar](/context-free-grammar/): the objects that a constituency treebank holds and the grammar read off it.
- [Probabilistic context-free grammar](/probabilistic-context-free-grammar/): the model that the treebank grammar estimates.
- [Head rules](/head-rules/): the tables that pick a head child in each tree, used to lexicalize a treebank or to convert it to dependencies.
- [Dependency tree](/dependency-tree/): the structure of a dependency treebank.
- [PARSEVAL measures](/parseval-measures/): the scores that compare parser output with the held-out trees.

## References
