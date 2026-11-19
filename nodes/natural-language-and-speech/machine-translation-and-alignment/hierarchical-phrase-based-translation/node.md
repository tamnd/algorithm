---
tag: FRYX8C
kind: model
slug: hierarchical-phrase-based-translation
name: Hierarchical phrase-based translation
aliases:
- Hiero
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: Chiang's model of synchronous CFG rules with phrases and gaps learned from aligned text, decoded by CKY-style chart parsing.
history:
  year: 2005
  people: [David Chiang]
  note: Chiang (2005) extended phrase pairs with gaps, so that rules learned from a word-aligned corpus without any parser could reorder sub-phrases, and decoded with a chart parser. Chiang (2007) gave the full model with cube pruning, and the method was built into the Joshua, cdec and Moses decoders.
prereqs: [synchronous-context-free-grammar, phrase-pair-extraction, log-linear-translation-model]
see_also: [cube-pruning, phrase-based-translation-model, inversion-transduction-grammar, ghkm-rule-extraction, probabilistic-cky, chart-parsing, hypergraph, minimum-error-rate-training]
sources:
  - paper: "David Chiang, A hierarchical phrase-based model for statistical machine translation, ACL 2005, pages 263 to 270"
    title: Chiang 2005
    locator: hierarchical phrase pairs, their extraction from initial phrase pairs, the features, the chart decoder and the comparison with a phrase-based system
  - paper: "David Chiang, Hierarchical phrase-based translation, Computational Linguistics 33(2), 2007, pages 201 to 228, ACL Anthology J07-2003"
    title: Chiang 2007
    locator: the grammar with the glue rules, the rule extraction and its limits, the log-linear features, and decoding with a language model by cube pruning
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 11 (tree-based models: hierarchical phrase-based models)"
---

Hierarchical phrase-based translation, often called Hiero, is a [synchronous context-free grammar](/synchronous-context-free-grammar/) with a single nonterminal $X$ whose rules are phrase pairs with gaps, for example $X \to \langle X_1 \text{ de } X_2, \text{ the } X_2 \text{ that } X_1 \rangle$. The rules are learned from a word-aligned [parallel corpus](/parallel-corpus/) by cutting smaller phrase pairs out of larger ones, so no parser is needed, and a [log-linear model](/log-linear-translation-model/) scores the derivations. Decoding is chart parsing of the source sentence, in the style of [CKY](/probabilistic-cky/), with the language model added by [cube pruning](/cube-pruning/). The gaps let a rule move whole sub-phrases, which the [phrase-based model](/phrase-based-translation-model/) can only do with a separate reordering model.

## The machine

**Direction and notation.** Translation runs from the source $f = f_1 \ldots f_m$ to the target $e$. Spans are fencepost: $(s, t)$ covers $f_{s+1} \ldots f_t$. Logs are natural.

**The grammar.** The rules have the form $X \to \langle \gamma, \alpha, \sim \rangle$, where $\gamma$ is a string of source words and nonterminals, $\alpha$ a string of target words and nonterminals, and $\sim$ links the nonterminals one to one. Two *glue rules*

$$S \to \langle S_1 \, X_2, \; S_1 \, X_2 \rangle, \qquad S \to \langle X_1, \; X_1 \rangle$$

join translated blocks from left to right without reordering, as a fallback for long sentences.

**Rule extraction.** Start from the *initial phrase pairs*, the phrase pairs consistent with the word alignment as in [phrase pair extraction](/phrase-pair-extraction/). Each initial pair $\langle \bar f, \bar e \rangle$ is a rule $X \to \langle \bar f, \bar e \rangle$. If $X \to \langle \gamma, \alpha \rangle$ is a rule and an initial pair $\langle \bar f', \bar e' \rangle$ lies inside it, with $\gamma = \gamma_1 \bar f' \gamma_2$ and $\alpha = \alpha_1 \bar e' \alpha_2$, then

$$X \to \langle \gamma_1 \, X_k \, \gamma_2, \; \alpha_1 \, X_k \, \alpha_2 \rangle$$

is also a rule, with a new index $k$. Without limits this gives far too many rules, so Chiang (2005, 2007) used these heuristic limits: initial phrases of at most 10 source words, at most 2 nonterminals per rule, at most 5 symbols (words and nonterminals) on the source side, no two nonterminals next to each other on the source side, and at least one aligned word pair in each rule. The rule counts are split among the rules extracted from one initial pair and turned into relative frequencies.

**Features.** As in the phrase-based model: the rule translation probabilities $P(\gamma \mid \alpha)$ and $P(\alpha \mid \gamma)$, the lexical weights in both directions, a rule penalty, a word penalty, a penalty for each glue rule, and an [n-gram language model](/n-gram-language-model/). The weights are tuned by [minimum error rate training](/minimum-error-rate-training/).

**Example.** A Chinese sentence in the style of Chiang (2005), in pinyin: Aozhou shi yu Beihan you bangjiao de shaoshu guojia zhiyi, "Australia is one of the few countries that have diplomatic relations with North Korea". The initial pair ⟨yu Beihan you bangjiao, have diplomatic relations with North Korea⟩ contains the initial pairs ⟨Beihan, North Korea⟩ and ⟨bangjiao, diplomatic relations⟩. Cutting both out gives

$$X \to \langle \text{yu } X_1 \text{ you } X_2, \; \text{have } X_2 \text{ with } X_1 \rangle,$$

a rule that learns how a Chinese "with" phrase before the verb becomes an English one after it. With the rules $X \to \langle X_1 \text{ de } X_2, \text{ the } X_2 \text{ that } X_1 \rangle$ and $X \to \langle X_1 \text{ zhiyi}, \text{ one of } X_1 \rangle$ and phrase rules for the words, the derivation is

| step | source span | target |
|---|---|---|
| yu $X_1$ you $X_2$ | yu Beihan you bangjiao | have diplomatic relations with North Korea |
| $X_1$ de $X_2$ | yu ... bangjiao de shaoshu guojia | the few countries that have diplomatic relations with North Korea |
| $X_1$ zhiyi | yu ... guojia zhiyi | one of the few countries that ... |
| glue rules | the whole sentence | Australia is one of the few countries that ... |

Each rule reorders a whole sub-phrase, and the three rules nest. A phrase-based system would need to learn this as one long phrase or as long jumps.

## What it counts

The model scores a derivation, a tree of rule applications, by the weighted sum of its features. Costs are counted on the [word RAM](/word-ram/), with one rule or language model lookup as one step.

- **Without a language model**, decoding is chart parsing of the source with the source sides of the rules, filling one cell per span $(s, t)$. Nonterminals are never adjacent on the source side, so for a fixed span a rule can match in at most $O(m)$ ways, and parsing takes $O(m^3)$ times the number of rules, a theorem by the same count as for [CKY](/probabilistic-cky/). The result is a packed forest, a [hypergraph](/hypergraph/).
- **With an n-gram language model**, the items of a cell must also be told apart by their first and last $n - 1$ target words. The exact search becomes polynomial of a much higher degree, and decoders instead keep a beam of items per cell and build it by [cube pruning](/cube-pruning/), which is a heuristic.
- **Span limit.** The hierarchical rules apply only to spans of at most 10 words, the same as the initial phrase limit; longer spans are built by the glue rules, so the number of rule applications grows only linearly with $m$ for long sentences.

## Relation to other models

- **Phrase-based model.** Every phrase pair is a Hiero rule without gaps, so the phrase-based model's phrases are a subset of the grammar. The [phrase-based model](/phrase-based-translation-model/) reorders by jumps scored by a distortion cost; Hiero reorders by rules with gaps and is decoded by chart parsing instead of [left-to-right stack search](/phrase-based-stack-decoding/).
- **Inversion transduction grammar.** Both are rank 2 SCFGs, but an [ITG](/inversion-transduction-grammar/) has binary rules over words and only straight or inverted order, while a Hiero rule holds phrases and gaps learned from data.
- **Syntax-based models.** Hiero has one nonterminal label and no linguistic syntax: it is formally syntax-based but not linguistically. String-to-tree models with [GHKM rules](/ghkm-rule-extraction/) use target parse labels, which restricts which rules fit together.
- **Log-linear framework.** The features, the tuning by MERT and the treatment of the language model are the same as in the [log-linear model](/log-linear-translation-model/) of phrase-based systems.

## Known results in the model

- **A rank 2 SCFG (theorem).** With at most two nonterminals per rule, the grammar is a synchronous CFG of rank 2, so the source projection is a context-free language and the forest of all derivations of a source sentence has polynomial size.
- **Better than phrase-based on Chinese to English (measurement).** Chiang (2005, 2007) reported higher BLEU scores than the phrase-based Pharaoh system on Chinese to English translation with the same training data.
- **The limits are heuristic.** The limits of 10 words, 2 nonterminals and 5 source symbols keep the grammar and the search small. They were chosen by experiment and are not part of the model; other systems change them.
- **Large grammars (measurement).** The extracted grammar is much larger than a phrase table from the same data, and systems usually filter it to the rules whose source side matches the test sentences.
- **Spurious ambiguity.** Many derivations give the same target string, for example by cutting a phrase in different places. The decoder uses the max over derivations, and $k$-best lists need extra work to hold distinct strings.

## References
