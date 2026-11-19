---
tag: 97NM6X
kind: problem
slug: constituency-parsing
name: Constituency parsing
aliases:
- phrase-structure parsing
area: natural-language-and-speech/natural-language-parsing
level: core
summary: "Find the phrase-structure tree of a natural language sentence, with labeled constituents such as NP and VP over spans of words."
model: word-ram
complexity:
  vars: {n: the number of words, g: the number of rules of a PCFG in Chomsky normal form, k: the number of nonterminals}
  time: {worst: O(g n^3)}
  space: {worst: O(k n^2)}
prereqs: [parse-tree, context-free-grammar, treebank]
see_also: [probabilistic-cky, inside-outside-algorithm, most-probable-parse, chart-parsing, dependency-parsing, parseval-measures, span-based-constituency-parsing, valiant-lee-theorem]
sources:
  - book: isbn:9780262133609
    title: "Christopher D. Manning and Hinrich Schütze, Foundations of Statistical Natural Language Processing"
    locator: "Chapter 11, Probabilistic Context Free Grammars, and Chapter 12, Probabilistic Parsing"
  - paper: "Mitchell P. Marcus, Beatrice Santorini and Mary Ann Marcinkiewicz, Building a Large Annotated Corpus of English, The Penn Treebank, Computational Linguistics 19(2), 1993"
    title: "Marcus, Santorini and Marcinkiewicz, Building a Large Annotated Corpus of English, The Penn Treebank"
    locator: "pp. 313-330; the bracketing scheme of the trees that parsers predict"
  - paper: doi:10.1162/089120103322753356
    title: "Michael Collins, Head-Driven Statistical Models for Natural Language Parsing, Computational Linguistics 29(4), 2003"
    locator: "pp. 589-637; the head-driven lexicalized models and their evaluation on the Wall Street Journal treebank"
  - paper: "Eugene Charniak, Tree-bank Grammars, Proceedings of AAAI-96"
    title: "Eugene Charniak, Tree-bank Grammars"
    locator: "the bracket precision and recall of a grammar read off the Wall Street Journal trees"
  - paper: doi:10.3115/1034678.1034748
    title: "Jason Eisner and Giorgio Satta, Efficient Parsing for Bilexical Context-Free Grammars and Head Automaton Grammars, ACL 1999"
    locator: "pp. 457-464; the O(n^4) algorithm for bilexical grammars and the O(n^3) special case"
  - paper: doi:10.1145/505241.505242
    title: "Lillian Lee, Fast context-free grammar parsing requires fast Boolean matrix multiplication, Journal of the ACM 49(1), 2002"
    locator: "the reduction from Boolean matrix multiplication to parsing"
  - paper: doi:10.18653/v1/P18-1249
    title: "Nikita Kitaev and Dan Klein, Constituency Parsing with a Self-Attentive Encoder, ACL 2018"
    locator: "pp. 2676-2686; the span parser with a self-attentive encoder and its Penn Treebank results"
---

Constituency parsing is the problem of finding the phrase-structure tree of a sentence. The tree groups the words into nested constituents, such as noun phrases (NP) and verb phrases (VP), and gives each constituent a label. Most sentences have many trees that a grammar allows, so a statistical parser defines a score for each tree and returns the best one. For a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) in Chomsky normal form, the best tree is found in time $O(g n^3)$ by [probabilistic CKY](/probabilistic-cky/), where $n$ is the number of words and $g$ the number of rules. Parsers are trained and tested on a [treebank](/treebank/), most often the Wall Street Journal part of the Penn Treebank, and scored with the [PARSEVAL measures](/parseval-measures/). The sister problem, [dependency parsing](/dependency-parsing/), links words to words instead of grouping them into phrases.

## In plain words

A sentence is more than a row of words. Some words belong together as a unit: in "the old man saw a dog", the words "the old man" form one unit that names who did the seeing, and "saw a dog" forms another unit that says what happened. Units can sit inside larger units, so the structure of a sentence is a tree.

A constituency parser takes a sentence and draws this tree, with a name on each unit, such as noun phrase or verb phrase. The hard part is choice: a long sentence can be grouped in a very large number of ways, and most of them are wrong. The parser uses scores learned from many sentences with known trees to pick the grouping that is most likely right.

## Definition

Let $w = w_1 \cdots w_n$ be a sentence and let $\mathcal{L}$ be a finite set of phrase labels. A fencepost span $(i, j)$ with $0 \le i < j \le n$ covers the words $w_{i+1}, \ldots, w_j$. A **constituency tree** of $w$ is an ordered tree whose leaves are $w_1, \ldots, w_n$ in this order, whose preterminals are the part-of-speech tags of the words, and whose other nodes carry labels in $\mathcal{L}$. Each such node covers a span, and the labeled spans $(\ell, i, j)$ of a tree form a laminar family: two spans are either disjoint or one contains the other. The root covers $(0, n)$ and may have any number of children. In the Penn Treebank, the root S of a declarative sentence often has three children, NP, VP and the final period, while the unlabeled outer bracket that wraps each tree usually has a single child.

**Input.** The sentence $w$, sometimes with its tags, and a model that gives each tree $t$ of $w$ a score $s(w, t)$.

**Output.** A tree $\hat t = \arg\max_{t \in \mathcal{T}(w)} s(w, t)$, where $\mathcal{T}(w)$ is the set of trees that the model allows.

For a PCFG $G = (N, \Sigma, R, S)$ with rule probabilities $q$, the score is $\log P(t) = \sum_{r \in t} \log q(r)$, and the problem is the [most probable parse](/most-probable-parse/). For a neural span parser, the score is a sum of learned span scores. In both cases the output is judged against a gold tree with the labeled bracket $F_1$ of the PARSEVAL measures.

**The standard benchmark.** The usual English benchmark trains on sections 02 to 21 of the Wall Street Journal part of the Penn Treebank, develops on section 22, and tests on section 23. Almost all published results on English use this split, so their numbers can be compared.

## Variants

- **Recognition.** Decide only whether $w$ has a tree under a [context-free grammar](/context-free-grammar/). This is the [CFG parsing problem](/cfg-parsing-problem/) of formal language theory.
- **All parses.** Return every tree, packed into a [shared packed parse forest](/shared-packed-parse-forest/) of polynomial size, or the $k$ best trees.
- **Minimum risk.** Return the tree with the largest expected number of correct constituents, computed from the marginals of the [inside-outside algorithm](/inside-outside-algorithm/), instead of the most probable tree.
- **Unlabeled.** Return only the bracketing, with no labels. Unsupervised grammar induction is often scored this way.
- **Full annotation.** Also predict the function tags (as in NP-SBJ) and the empty elements of the Penn Treebank. Most parsers remove both before training and do not predict them.
- **Discontinuous constituents.** Allow a constituent to cover words that are not adjacent, as in some German treebanks. The trees are then no longer laminar families of spans, and the dynamic programs below do not apply directly.
- **Incremental.** Build the tree word by word from left to right, as in [incremental parsing](/incremental-parsing/) and [shift-reduce parsing](/shift-reduce-parsing/).

## Examples

**A prepositional phrase attachment.** The PCFG of Manning and Schütze, shown on the [PCFG page](/probabilistic-context-free-grammar/), gives the sentence *astronomers saw stars with ears* two trees. In $t_1$ the phrase *with ears* belongs to the noun phrase *stars with ears*, by the rule $NP \to NP\ PP$; in $t_2$ it attaches to the verb phrase, by the rule $VP \to VP\ PP$. The probabilities are

$$P(t_1) = 0.0009072, \qquad P(t_2) = 0.0006804,$$

so the best tree is $t_1$, with conditional probability $P(t_1 \mid w) = 0.0009072 / 0.0015876 = 4/7$. [Probabilistic CKY](/probabilistic-cky/) finds $t_1$ with a table of $\binom{6}{2} = 15$ spans. In labeled spans, the two trees differ in one span each way: $t_1$ has NP(2, 5) and $t_2$ has VP(1, 3).

**The number of trees.** If every tree is binary and labels are ignored, a sentence of $n$ words has $C_{n-1}$ trees, where $C_m = \frac{1}{m+1} \binom{2m}{m}$ is a [Catalan number](/catalan-numbers/). This is a theorem: a binary tree over $n$ leaves splits at one of $n - 1$ points into two binary trees, which is the Catalan recurrence.

| $n$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| binary trees | 1 | 1 | 2 | 5 | 14 | 42 | 132 |

The count grows like $4^n / n^{3/2}$, so a parser cannot list the trees. The dynamic programs below share the work over the $O(n^2)$ spans instead.

## Known algorithms

| method | score | time | exact |
|---|---|---|---|
| [Probabilistic CKY](/probabilistic-cky/) | PCFG in CNF | $O(g n^3)$ | yes |
| [Earley parser](/earley-parser/) | any PCFG | $O(n^3)$ for a fixed grammar | yes |
| [A* parsing](/a-star-parsing/) | PCFG | $O(g n^3)$ worst case | yes, with an admissible heuristic |
| [Lexicalized PCFG](/lexicalized-pcfg/), naive CKY | head words on nodes | $O(n^5)$ for a fixed grammar | yes |
| Lexicalized PCFG, Eisner and Satta | bilexical grammar | $O(n^4)$ | yes |
| [Latent-variable PCFG](/latent-variable-pcfg/) | sum over subcategories | NP-hard for the best tree | no, approximate decoding |
| [Span-based parser](/span-based-constituency-parsing/) | sum of span scores | $\Theta(n^3 + n^2 L)$ for $L$ labels | yes |
| [Shift-reduce parsing](/shift-reduce-parsing/) | score of each action | $O(n)$ actions, greedy or with a beam | no |

The time bounds are theorems about the algorithms. Which method gives the most accurate trees is a measurement. Two notes on the lexicalized rows. A lexicalized CKY parser keeps a head word index in each chart item, which raises the cost from $O(n^3)$ to $O(n^5)$. Eisner and Satta (1999) reduced bilexical parsing to $O(n^4)$, and to $O(n^3)$ in a special case. For dependency trees, which are the bilexical structures with no phrase labels, the [Eisner algorithm](/eisner-algorithm/) of 1996 runs in $O(n^3)$.

Some measurements show the progress. A plain treebank grammar reaches a bracket precision of 82.0 and a recall of 80.0 in Charniak (1996), on test sentences of 2 to 40 words with gold tags. On section 23, Kitaev and Klein (2018) report an $F_1$ of 93.55 for a span parser with a self-attentive encoder, and 95.13 with pre-trained word representations.

## Bounds

- **Upper bound.** $O(g n^3)$ time and $O(k n^2)$ space for a PCFG in Chomsky normal form, by probabilistic CKY. This is a theorem.
- **Subcubic recognition.** [Valiant's algorithm](/valiant-algorithm/) decides context-free recognition in the time of [Boolean matrix multiplication](/boolean-matrix-multiplication/), which is $O(n^{\omega})$ with $\omega < 2.38$. This is a theorem. The constants are large, and no practical natural language parser uses it.
- **Conditional lower bound.** By the [Valiant-Lee theorem](/valiant-lee-theorem/), a parser that finds all constituents in time $O(g n^{3 - \epsilon})$ would give Boolean matrix multiplication of $m \times m$ matrices in time $O(m^{3 - \epsilon/3})$. So a combinatorial parser much faster than cubic would be a major result. This is a theorem about the reduction.
- **Hardness with hidden structure.** If the score of a tree is a sum over hidden derivations, as in a stochastic tree substitution grammar or a [latent-variable PCFG](/latent-variable-pcfg/), finding the most probable tree is NP-hard. Sima'an proved this for stochastic tree substitution grammars, and the latent-variable case follows by the reduction that Matsuzaki, Miyao and Tsujii sketch. See [most probable parse](/most-probable-parse/).
- **Output.** A tree without unary chains or empty nodes has at most $n - 1$ phrasal nodes above the preterminals, so the output has size $O(n)$.

## Reductions

- **From recognition.** A sentence has a parse under a grammar exactly when it is in the language of the grammar, so constituency parsing with a grammar is at least as hard as [context-free language recognition](/context-free-language-recognition/).
- **From Boolean matrix multiplication.** Lee (2002) builds, for two Boolean matrices, a grammar and a string whose constituents encode the product. This is the reduction behind the conditional lower bound.
- **To dependency parsing.** [Head rules](/head-rules/) pick a head child at each node, and the heads turn a constituency tree into a [dependency tree](/dependency-tree/). The reverse direction is not unique, because a dependency tree does not fix the phrase labels or the order in which dependents attach.
- **To span scoring.** A span parser reduces the problem to scoring each labeled span and running a CKY-style dynamic program over the spans, with no grammar.
- **To sequence labeling.** Trees can also be written as sequences of actions or labels, one per word or per step, which turns parsing into the prediction of a sequence. Shift-reduce parsers work this way.

## Applications

- Information extraction, where the path through the tree between two names is a feature for the relation between them.
- Syntax-based machine translation, which reorders or translates whole constituents.
- [Semantic parsing](/semantic-parsing/) and semantic role labeling, whose arguments are often constituents.
- Shallow parsing: the chunks used to train and test text chunkers are often derived from treebank trees.
- Linguistic study of a corpus, where queries over trees find constructions such as relative clauses.
- Grammar induction and the study of language acquisition, as in the [dependency model with valence](/dependency-model-with-valence/) for dependency structure.

## References
