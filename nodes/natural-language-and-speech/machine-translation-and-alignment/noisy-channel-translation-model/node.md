---
tag: BXSW8F
kind: model
slug: noisy-channel-translation-model
name: Noisy channel model of translation
aliases:
- source-channel translation model
area: natural-language-and-speech/machine-translation-and-alignment
level: intro
summary: Find the target sentence e that maximizes P(e) P(f | e), a language model times a translation model, for the source sentence f.
history:
  year: 1990
  people: [Peter F. Brown, John Cocke, Stephen A. Della Pietra, Vincent J. Della Pietra, Fredrick Jelinek, John D. Lafferty, Robert L. Mercer, Paul S. Roossin]
  note: The IBM group took the source-channel method of speech recognition and applied it to French and English translation in 1990. The 1993 paper gave the five IBM translation models for the channel.
prereqs: [bayes-theorem, language-model]
see_also: [ibm-model-1, n-gram-language-model, noisy-channel-spelling-correction, source-channel-speech-recognition, log-linear-translation-model, phrase-based-stack-decoding, encoder-decoder-model, machine-translation]
sources:
  - paper: "Peter F. Brown, John Cocke, Stephen A. Della Pietra, Vincent J. Della Pietra, Fredrick Jelinek, John D. Lafferty, Robert L. Mercer and Paul S. Roossin, A statistical approach to machine translation, Computational Linguistics 16(2), 1990, pages 79 to 85, ACL Anthology J90-2002"
    title: Brown et al. 1990
    locator: the decision rule with a language model and a translation model, and the first experiments from French to English
  - paper: "Peter F. Brown, Stephen A. Della Pietra, Vincent J. Della Pietra and Robert L. Mercer, The mathematics of statistical machine translation: parameter estimation, Computational Linguistics 19(2), 1993, pages 263 to 311"
    title: Brown, Della Pietra, Della Pietra and Mercer 1993
    locator: the fundamental equation of statistical machine translation and the division into a language model, a translation model and a search
  - paper: "Kevin Knight, Decoding complexity in word-replacement translation models, Computational Linguistics 25(4), 1999, pages 607 to 615, ACL Anthology J99-4005"
    title: Knight 1999
    locator: the NP-completeness of decoding with IBM Model 1 and a bigram language model
  - paper: doi:10.3115/1073083.1073133
    title: Franz Josef Och and Hermann Ney, Discriminative training and maximum entropy models for statistical machine translation, ACL 2002, pages 295 to 302
    locator: the log-linear model that contains the source-channel model as a special case
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 4 (word-based models and the noisy-channel model)"
---

The noisy channel model of translation treats a sentence $f$ in the source language as if it were a target sentence $e$ that went through a noisy channel and came out in another language. To translate $f$ is to guess the $e$ that most probably went in. By [Bayes' theorem](/bayes-theorem/),

$$\hat e = \arg\max_e p(e \mid f) = \arg\max_e p(e) \, p(f \mid e),$$

because $p(f)$ does not depend on $e$. The rule splits translation into three parts: a [language model](/language-model/) $p(e)$, which says how likely $e$ is as a sentence of the target language; a translation model $p(f \mid e)$, which says how well $e$ explains $f$; and a decoder, which searches for $\hat e$. Brown et al. (1990) proposed it for French to English, after the same rule had worked in [speech recognition](/source-channel-speech-recognition/), and the [IBM models](/ibm-model-1/) are channel models for it. Statistical translation was built on this rule until the [log-linear model](/log-linear-translation-model/) took its place.

## The machine

**Variables.** The input is a source sentence $f = f_1 \ldots f_m$. The output is a target sentence $e = e_1 \ldots e_l$, chosen from all strings over the target vocabulary. Translation runs from $f$ to $e$, but the channel model runs the other way, from $e$ to $f$. This is why the IBM papers, which translate French into English, write the translation model as $p(f \mid e)$.

**The three parts.**

- **Source model** $p(e)$: a language model of the target language, in practice an [n-gram language model](/n-gram-language-model/). It is trained on text in the target language only, which is plentiful.
- **Channel model** $p(f \mid e)$: a translation model, such as [IBM Model 1](/ibm-model-1/), [Model 2](/ibm-model-2/), [Model 3](/ibm-model-3/), the [HMM alignment model](/hmm-alignment-model/) or the [phrase-based model](/phrase-based-translation-model/). It is trained on a [parallel corpus](/parallel-corpus/). Most of these models sum over hidden [word alignments](/word-alignment/): $p(f \mid e) = \sum_a p(f, a \mid e)$.
- **Decoder**: a search for $\arg\max_e p(e) \, p(f \mid e)$ over a space of candidates that grows exponentially with the length of $f$, for example by [stack decoding](/phrase-based-stack-decoding/) with pruning. In practice the decoder often maximizes over the alignment too, with $\max_a p(e) \, p(f, a \mid e)$ in place of the sum.

**Why the split helps.** The direct model $p(e \mid f)$ would have to give high probability only to target sentences that are both fluent and faithful. In the split, the two jobs go to two models. The channel model may give weight to target sentences that are not good sentences, as long as they contain the right words, because the language model gives such sentences a low score. And each model can be estimated from the data that suits it.

**Example.** Take $f$ = "la maison" and three candidates, with numbers made up for the illustration:

| candidate $e$ | $p(e)$ | $p(f \mid e)$ | $p(e) \, p(f \mid e)$ |
|---|---|---|---|
| the house | 0.004 | 0.20 | 0.0008 |
| house the | 0.00001 | 0.25 | 0.0000025 |
| the home | 0.002 | 0.05 | 0.0001 |

A word-for-word channel model scores "house the" a little higher than "the house", because it does not care about order. The language model gives that word order a very low probability, and the product picks "the house".

## What it counts

The model assigns a score $p(e) \, p(f \mid e)$ to each pair, and its output is the candidate with the highest score. One step is one arithmetic operation on real numbers or one table lookup, as on the [real RAM](/real-ram/). Two kinds of cost matter:

- **Scoring** one pair $(e, f)$: for an n-gram language model, $\Theta(l)$ lookups; for the channel, $\Theta(l m)$ under Models 1 and 2 and $\Theta(m l^2)$ under the HMM model, by the algorithms of those pages.
- **Decoding**, the search over $e$: the number of candidates of length $l$ is the vocabulary size to the power $l$, so the search must be heuristic or restricted.

Errors are counted in two kinds. A *search error* is an output whose score is lower than that of another candidate the decoder missed. A *model error* is an output with the best score that is still a bad translation. Better search fixes only the first kind.

## Relation to other models

- **Noisy channel spelling correction.** [Spelling correction](/noisy-channel-spelling-correction/) uses the same rule, with a model of words as the source and a model of typing errors as the channel.
- **Source-channel speech recognition.** In [speech recognition](/source-channel-speech-recognition/) the source is the word sequence and the channel produces the sound, with $\hat W = \arg\max_W p(W) \, p(A \mid W)$. The IBM translation work came from this group and this method.
- **Log-linear model.** The [log-linear translation model](/log-linear-translation-model/) of Och and Ney (2002) scores $e$ by $\sum_k \lambda_k h_k(e, f)$ with any feature functions $h_k$. With the two features $\ln p(e)$ and $\ln p(f \mid e)$ and weights 1, it is the noisy channel rule. With other weights and more features, such as $\ln p(e \mid f)$ and a length penalty, it usually translates better, and the weights are tuned by [minimum error rate training](/minimum-error-rate-training/).
- **Neural models.** An [encoder-decoder model](/encoder-decoder-model/) models $p(e \mid f)$ directly, without the split. The channel direction still appears, for example to rerank candidates or to make training data by [back-translation](/back-translation/).

## Known results in the model

- **Bayes decision rule (theorem).** If $p(e)$ and $p(f \mid e)$ are the true distributions, the rule minimizes the probability that the output is not the reference sentence, because it picks the mode of the true posterior $p(e \mid f)$. With estimated models this guarantee does not hold, and nothing in the rule rewards outputs that are close to the reference without being equal to it.
- **Decoding is NP-complete (theorem).** For IBM Model 1 as the channel and a bigram language model, the decision version of decoding is NP-complete (Knight 1999). So no polynomial algorithm finds $\hat e$ exactly unless P = NP, and decoders use beam search and other heuristics. For the higher IBM models even finding the best alignment of a fixed pair is NP-hard (Udupa and Maji 2006; see [word alignment](/word-alignment/)).
- **Separate training.** Because $p(e)$ needs only target-language text, the language model can be trained on far more data than the parallel corpus has. A better language model improves the fluency of the output without any new parallel data.

## References
