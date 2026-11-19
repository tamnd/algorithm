---
tag: 53WN6E
kind: model
slug: phrase-based-translation-model
name: Phrase-based translation model
aliases:
- phrase-based SMT
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Translate by segmenting the source into phrases, translating each by a phrase table and reordering them, scored by a log-linear model.
history:
  year: 2003
  people: [Philipp Koehn, Franz Josef Och, Daniel Marcu]
  note: Och, Tillmann and Ney (1999) translated with alignment templates, and Koehn, Och and Marcu (2003) gave the simple phrase-based model with a phrase table from word alignments, lexical weights and a distortion cost. With the Pharaoh and Moses decoders it was the main approach to machine translation until neural models took over around 2015.
prereqs: [log-linear-translation-model, phrase-pair-extraction, n-gram-language-model]
see_also: [phrase-based-stack-decoding, lexicalized-reordering-model, minimum-error-rate-training, noisy-channel-translation-model, ibm-model-1, hierarchical-phrase-based-translation, grow-diag-final-symmetrization, encoder-decoder-model]
sources:
  - paper: "Philipp Koehn, Franz Josef Och and Daniel Marcu, Statistical phrase-based translation, HLT-NAACL 2003, ACL Anthology N03-1017"
    title: Koehn, Och and Marcu 2003
    locator: the phrase-based model, the phrase translation table by relative frequency, the lexical weighting and the distortion model
  - paper: "Franz Josef Och and Hermann Ney, The alignment template approach to statistical machine translation, Computational Linguistics 30(4), 2004, pages 417 to 449"
    title: Och and Ney 2004
    locator: phrase-level translation with alignment templates inside a log-linear model
  - paper: "Philipp Koehn, Amittai Axelrod, Alexandra Birch Mayne, Chris Callison-Burch, Miles Osborne and David Talbot, Edinburgh system description for the 2005 IWSLT speech translation evaluation, IWSLT 2005, ACL Anthology 2005.iwslt-1.8"
    title: Koehn et al. 2005
    locator: "Section 2.2 (the list of features), Equation 3 (phrase translation by relative frequency) and Equation 4 (lexical weighting)"
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 5 (phrase-based models)"
---

The phrase-based translation model translates a sentence by cutting the source into phrases (any sequences of consecutive words, not necessarily linguistic phrases), translating each phrase with a phrase table learned from a word-aligned [parallel corpus](/parallel-corpus/), and putting the translated phrases in some order. A [log-linear model](/log-linear-translation-model/) scores each such derivation with phrase translation probabilities in both directions, lexical weights, a phrase and a word penalty, a distortion cost for reordering, and an [n-gram language model](/n-gram-language-model/). It is the model of the Pharaoh and Moses systems. Phrases capture local context and local reordering that word-based models such as [IBM Model 1](/ibm-model-1/) cannot express.

## The machine

**Direction and notation.** Translation runs from the source $f = f_1 \ldots f_m$ to the target $e$. Spans are fencepost: $(s, t)$ covers $f_{s+1} \ldots f_t$. Logs are natural.

**Derivations.** A derivation $d$ is a sequence of steps $(s_k, t_k, \bar e_k)$, $k = 1, \ldots, n$, whose source spans cover every source word exactly once, and each $\bar e_k$ is a translation of the source phrase $\bar f_k = f_{s_k+1} \ldots f_{t_k}$ that is listed in the phrase table. The target sentence is $e = \bar e_1 \bar e_2 \cdots \bar e_n$, in the order of the steps. So the segmentation of the source, the choice of a translation for each phrase, and the order of the phrases are all hidden, and different derivations can give the same $e$.

**The phrase table.** It is built in three steps. Word-align the corpus in both directions and [symmetrize](/grow-diag-final-symmetrization/). [Extract](/phrase-pair-extraction/) all phrase pairs consistent with the alignment, up to 7 words on each side. Estimate, for each pair, four scores:

- the phrase translation probabilities $\phi(\bar f \mid \bar e) = \mathrm{count}(\bar f, \bar e) / \sum_{\bar f'} \mathrm{count}(\bar f', \bar e)$ and $\phi(\bar e \mid \bar f)$, by relative frequency of the extracted pairs;
- the lexical weights $p_w(\bar f \mid \bar e, a)$ and $p_w(\bar e \mid \bar f, a)$, which check how well the words inside the pair translate each other. With the word translation table $w$ from the word-aligned corpus,

$$p_w(\bar f \mid \bar e, a) = \prod_{x=1}^{|\bar f|} \frac{1}{|\{y : (x, y) \in a\}|} \sum_{(x, y) \in a} w(\bar f_x \mid \bar e_y),$$

where an unaligned source word is aligned to a null word.

**The score.** A derivation is scored by $\sum_q \lambda_q h_q(d)$ with the features

| feature $h_q$ | value for a derivation |
|---|---|
| phrase translation, both directions | $\sum_k \ln \phi(\bar f_k \mid \bar e_k)$ and $\sum_k \ln \phi(\bar e_k \mid \bar f_k)$ |
| lexical weights, both directions | $\sum_k \ln p_w(\bar f_k \mid \bar e_k)$ and $\sum_k \ln p_w(\bar e_k \mid \bar f_k)$ |
| phrase penalty | $n$, the number of phrases |
| word penalty | $|e|$, the number of target words |
| distortion | $-\sum_k |s_k - t_{k-1}|$, with $t_0 = 0$ |
| language model | $\ln p_{\mathrm{LM}}(\texttt{<s>} \; e \; \texttt{</s>})$ |

The weights $\lambda_q$ are tuned on held-out data, usually by [minimum error rate training](/minimum-error-rate-training/). The [lexicalized reordering model](/lexicalized-reordering-model/) adds orientation probabilities for each phrase pair as more features, next to the plain distortion cost.

**Example.** Suppose "das haus" was extracted 10 times in the corpus, 8 times with "the house" and 2 times with "the home". Then $\phi(\text{the house} \mid \text{das haus}) = 8/10 = 0.8$, with $\ln 0.8 = -0.223$. For the pair geht ja nicht to does not go, with the links geht to go and nicht to both does and not, and ja unaligned, the lexical weight with $w(\text{geht} \mid \text{go}) = 0.5$, $w(\text{ja} \mid \text{null}) = 0.1$, $w(\text{nicht} \mid \text{does}) = 0.2$ and $w(\text{nicht} \mid \text{not}) = 0.8$ is

$$p_w = 0.5 \times 0.1 \times \tfrac{1}{2}(0.2 + 0.8) = 0.025, \qquad \ln 0.025 = -3.689.$$

The low value comes from the unaligned ja, and it warns the model that this pair is less reliable than its relative frequency suggests.

## What it counts

The model assigns a score to each derivation, and the system outputs the target of the best derivation, $\hat e = e(\arg\max_d \sum_q \lambda_q h_q(d))$. It does not sum over the derivations that give the same $e$; this max approximation makes search simpler. Costs are counted in table lookups and arithmetic operations, as on the [word RAM](/word-ram/):

- **Scoring one derivation** costs $O(n + |e|)$ lookups: the phrase features once per phrase, the language model once per target word.
- **Training** costs one pass of phrase extraction over the corpus and a count of the extracted pairs, so it is linear in the number of extracted pairs, which can be large.
- **Decoding**, the search over derivations, is the expensive part and is done by [multi-stack beam search](/phrase-based-stack-decoding/).

Errors are of two kinds: model errors (the best derivation is a bad translation) and search errors (the decoder misses the best derivation because of pruning).

## Relation to other models

- **Log-linear translation model.** The [log-linear model](/log-linear-translation-model/) is the general framework: any features, combined with weights. The phrase-based model is one instance, with phrase-level features and a derivation made of phrase steps.
- **Noisy channel model.** With only two features, $\ln \phi(\bar f \mid \bar e)$ and the language model, both with weight 1, the score is a [noisy channel](/noisy-channel-translation-model/) score in which the channel model is the product of phrase translation probabilities.
- **Word-based models.** The [IBM models](/ibm-model-1/) translate word by word. The phrase-based model uses them only to align words before extraction, and it uses their word translation table in the lexical weights.
- **Hierarchical phrase-based model.** [Hiero](/hierarchical-phrase-based-translation/) extends phrases with gaps, so that a rule can reorder whole sub-phrases; it is decoded by chart parsing instead of left-to-right search.
- **Stack decoding.** The [stack decoder](/phrase-based-stack-decoding/) is the search algorithm for this model; the model defines what is scored, the decoder how the best derivation is found.
- **Neural models.** An [encoder-decoder model](/encoder-decoder-model/) replaces the phrase table, the reordering model and the language model by one network and has no explicit segmentation.

## Known results in the model

- **Decoding is NP-hard (theorem).** With free reordering, finding the best derivation is [NP-hard](/np-hard/). It contains the decoding of IBM Model 1 with a bigram language model, whose decision version is [NP-complete](/np-complete/) (Knight 1999). With a distortion limit, decoding is polynomial in the sentence length for a fixed limit.
- **Phrases beat words (measurement).** Koehn, Och and Marcu (2003) measured clearly higher BLEU for phrase-based translation than for word-based translation, and found that phrases from symmetrized word alignments did better than phrases restricted to syntactic constituents.
- **Lexical weights help (measurement).** In the same experiments, adding the lexical weights to the phrase probabilities improved the BLEU score.
- **Long phrases give little (measurement).** In those experiments, raising the maximum phrase length beyond about three words gave only small gains, while the phrase table grew much larger.
- **Overestimated long phrases.** Relative frequency gives a probability of 1 to many rare long phrase pairs seen once. This is a known weakness of the estimate; the lexical weights and smoothing reduce it.

## References
