---
tag: PXW84P
kind: model
slug: lexicalized-pcfg
name: Lexicalized PCFG
aliases:
- head-driven statistical parsing model
- Collins parsing model
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: "A PCFG whose nonterminals carry their head word and tag, with rule probabilities factored into head and dependent generation steps."
history:
  year: 1997
  people: [Michael Collins, Eugene Charniak]
  note: "Collins and Charniak each published a generative parser that conditions the expansion of a node on its head word. The head-driven factorization of Collins became the standard form."
prereqs: [probabilistic-context-free-grammar, head-rules, treebank]
see_also: [parent-annotation, latent-variable-pcfg, probabilistic-cky, eisner-algorithm, dependency-model-with-valence, deleted-interpolation, constituency-parsing, dependency-parsing]
sources:
  - paper: doi:10.3115/976909.979620
    title: "Michael Collins, Three Generative, Lexicalised Models for Statistical Parsing, ACL 1997"
    locator: "pp. 16-23; the head-outward generation of a rule, the distance measure, and Models 1, 2 and 3"
  - paper: doi:10.1162/089120103322753356
    title: "Michael Collins, Head-Driven Statistical Models for Natural Language Parsing, Computational Linguistics 29(4), 2003"
    locator: "pp. 589-637; the full description of the models, the smoothing, the parsing algorithm and the head rules"
  - paper: "Eugene Charniak, Statistical parsing with a context-free grammar and word statistics, Proceedings of AAAI-97"
    title: "Eugene Charniak, Statistical parsing with a context-free grammar and word statistics"
    locator: "the PCFG with head words and the probability of a head word given the head of the parent"
  - paper: doi:10.3115/1034678.1034748
    title: "Jason Eisner and Giorgio Satta, Efficient Parsing for Bilexical Context-Free Grammars and Head Automaton Grammars, ACL 1999"
    locator: "pp. 457-464; the O(n^4) parser for bilexical grammars and the O(n^3) special case"
  - paper: doi:10.3115/1075096.1075150
    title: "Dan Klein and Christopher D. Manning, Accurate Unlexicalized Parsing, ACL 2003"
    locator: "pp. 423-430; the comparison of lexicalized and unlexicalized parsing and the cost of lexicalized chart parsing"
---

A lexicalized PCFG is a [probabilistic context-free grammar](/probabilistic-context-free-grammar/) in which every nonterminal carries the head word of its phrase and the part-of-speech tag of that word. The noun phrase *the stock market* becomes NP(market, NN), and the sentence *payrolls fell* becomes S(fell, VBD). With heads on the nodes, the probability of an expansion can depend on words, so the model can learn that *saw* takes a noun phrase object and that *fell* does not. A plain PCFG cannot see the words above the preterminals. There are far too many lexicalized rules to estimate each one from a [treebank](/treebank/), so the head-driven models of Michael Collins (1997, 2003) generate a rule in small steps: first the head child, then the dependents to its left and to its right, one at a time, each conditioned on the parent and the head. The heads in the training trees come from [head rules](/head-rules/). The price of the words is in the chart: a naive CKY parser for a lexicalized grammar takes time $O(n^5)$, against $O(n^3)$ for a plain PCFG.

## The machine

**Lexicalized nonterminals.** Let $N$ be the phrase labels, $T$ the tags and $V$ the words. A lexicalized nonterminal is $X(h)$ with $X \in N \cup T$ and $h = (w, \tau)$ a head word $w \in V$ with tag $\tau \in T$. A rule has the form

$$X(h) \to L_m(l_m) \cdots L_1(l_1)\ H(h)\ R_1(r_1) \cdots R_k(r_k),$$

where $H$ is the head child, which shares the head $h$ of the parent, and the $L_i(l_i)$ and $R_i(r_i)$ are the left and right dependents with their own heads. The root may have any number of children. In the Penn Treebank the root is usually S, with a subject NP to the left of the head VP and often a final period to its right.

**Head-driven generation.** Collins Model 1 gives the rule the probability

$$P_H(H \mid X, h) \cdot \prod_{i=1}^{m+1} P_L\big(L_i(l_i) \mid X, H, h, \Delta_L(i)\big) \cdot \prod_{i=1}^{k+1} P_R\big(R_i(r_i) \mid X, H, h, \Delta_R(i)\big),$$

with $L_{m+1} = R_{k+1} = \mathrm{STOP}$. The head child is generated first. Then the left dependents are generated outward from the head until STOP, and the right dependents in the same way. Each step is a Markov decision that sees the parent label $X$, the head child label $H$, the head $h$ and a distance $\Delta$. The distance records facts about the words between the head and the new dependent, such as whether the dependent is adjacent to the head and whether a verb lies between them. The dependent is in turn generated in two parts, first its label and tag, then its head word given the label, the tag and the context.

**The tree.** The probability of a tree is the product of the probabilities of its rules, as in any PCFG. The heads of the preterminals are the words, so the tree fixes all the heads, and the model gives a joint probability $P(t, w)$ of the tree and the sentence. A parser returns $\arg\max_t P(t, w)$ over the trees of $w$.

**Models 2 and 3.** Model 2 marks each dependent as a complement or an adjunct, and generates a set of required complements on each side of the head (a subcategorization frame) before the dependents. A STOP is not allowed while a required complement is missing. Model 3 adds a treatment of the traces of wh-movement.

**Estimation.** Each distribution is estimated by relative frequency from the head-annotated treebank. The full contexts are too sparse, so each estimate is interpolated with estimates that drop part of the context, first the head word, as in [deleted interpolation](/deleted-interpolation/). The interpolation is a heuristic; its weights are set by a fixed formula, not by maximum likelihood.

## What it counts

The model counts the joint probability of a tree and its words, and so ranks the trees of a sentence by $P(t \mid w) \propto P(t, w)$.

**A rule probability.** Take the rule S(fell, VBD) → NP(payrolls, NNS) VP(fell, VBD) of the sentence *payrolls fell*, and the made-up parameters

| step | probability |
|---|---|
| $P_H(\mathrm{VP} \mid \mathrm{S}, \textit{fell}, \mathrm{VBD})$ | $7/10$ |
| $P_L(\mathrm{NP}(\textit{payrolls}, \mathrm{NNS}) \mid \mathrm{S}, \mathrm{VP}, \textit{fell}, \mathrm{VBD}, \text{adjacent})$ | $1/50$ |
| $P_L(\mathrm{STOP} \mid \mathrm{S}, \mathrm{VP}, \textit{fell}, \mathrm{VBD}, \text{not adjacent})$ | $9/10$ |
| $P_R(\mathrm{STOP} \mid \mathrm{S}, \mathrm{VP}, \textit{fell}, \mathrm{VBD}, \text{adjacent})$ | $19/20$ |

The rule has probability $\frac{7}{10} \cdot \frac{1}{50} \cdot \frac{9}{10} \cdot \frac{19}{20} = \frac{1197}{100000} = 0.01197$. Each factor has its own small context, and the factor $1/50$ is the only one that sees both words, *fell* and *payrolls*. Such a factor, with two words, is a bilexical probability. It is the sparsest kind, and it is the first one that the interpolation backs off.

**What the words decide.** In *astronomers saw stars with ears*, the attachment of the prepositional phrase is decided by the factor that generates PP(with, IN) as a dependent, either of VP(saw, VBD) or of NP(stars, NNS). The head of a PP under the usual head rules is the preposition, so this factor sees *saw* or *stars* and *with*, but not *ears*. The noun *ears* is generated later, inside the PP, and the same factor would pick the same attachment for *with telescopes*. This follows from the factorization, and it shows that the model sees one word of each dependent, not all of them.

**The number of parameters.** A bilexical distribution has a context for each parent label, head child label and head word, and an outcome for each dependent label with its word, so its table has on the order of $|N|^3 |V|^2$ entries. With $|V|$ in the tens of thousands, almost all of them are unseen in a treebank of a million words. This is why the backoff to unlexicalized estimates is a central part of the model.

## Relation to other models

- **Plain PCFG.** A [probabilistic context-free grammar](/probabilistic-context-free-grammar/) chooses the whole right side of a rule at once, from a finite rule set, given only the label of the parent. A lexicalized PCFG differs in two ways. Its nonterminals are pairs of a label and a head, so the rule set is much larger. And in the Collins form, the right side is generated by a Markov process that can produce any number of dependents, so the set of possible rules is not finite. With the heads restricted to the words of one sentence, the grammar used for that sentence is again a finite PCFG, and [probabilistic CKY](/probabilistic-cky/) parses it.
- **Parent annotation.** [Parent annotation](/parent-annotation/) adds context from above to each label, while lexicalization adds the head word. Klein and Manning (2003) showed that an unlexicalized grammar with parent annotation, sibling context and some hand-made splits comes close to the early lexicalized parsers, and parses in $O(n^3)$.
- **Latent-variable PCFG.** A [latent-variable PCFG](/latent-variable-pcfg/) splits each label into subcategories learned by EM. The subcategories play the role of the head words, but there are few of them, so the parser stays cubic.
- **Dependency models.** Remove the phrase labels from a lexicalized tree and keep only the head of each dependent: the result is a [dependency tree](/dependency-tree/). The head-outward generation with STOP decisions is the same process as in a head automaton grammar and in the [dependency model with valence](/dependency-model-with-valence/), which applies it to tags without words.
- **Head rules.** The model needs the head child of each node in the training trees. [Head rules](/head-rules/) give it, and their choices change the model.

## Known results in the model

- **Termination of each rule (theorem).** If STOP has a positive probability in every context of $P_L$ and $P_R$, each side of a rule ends after finitely many dependents with probability 1, because the contexts form a finite set and so the STOP probability has a positive lower bound $c$, and the chance of more than $k$ dependents is at most $(1 - c)^k$.
- **Naive parsing time (theorem).** A chart item is $(X, i, j, h)$ with a head position $h$ inside the span $(i, j)$. Combining two items chooses $i < k < j$ and a head in each part, so CKY on a binarized lexicalized grammar takes time $O(n^5)$ for a fixed set of labels.
- **Faster parsing (theorem).** Eisner and Satta (1999) gave an $O(n^4)$ algorithm for bilexical context-free grammars and head automaton grammars, which previously took $O(n^5)$, and an $O(n^3)$ algorithm for a special case, with a better grammar constant than Eisner's earlier result. For dependency trees without labels, the [Eisner algorithm](/eisner-algorithm/) of 1996 runs in $O(n^3)$ by keeping each head at the end of its span.
- **Exact parsing (theorem).** The model is a PCFG for each fixed sentence, so the Viterbi parse is exact with any of these charts. In practice, parsers prune the chart with a beam, which is a heuristic and can lose the best tree.
- **Accuracy (measurement).** Lexicalized parsers were the most accurate generative parsers on the Penn Treebank in the late 1990s. Klein and Manning (2003) measured that much of the gain over a plain treebank grammar can also be had without words, by better labels.

## References
