---
tag: 9Q3JB9
kind: technique
slug: back-translation
name: Back-translation
aliases:
- backtranslation
area: natural-language-and-speech/machine-translation-and-alignment
level: core
summary: Translate monolingual target text into the source language with a reverse model, and add the synthetic pairs to the training data.
history:
  year: 2016
  people: [Rico Sennrich, Barry Haddow, Alexandra Birch]
  note: Sennrich, Haddow and Birch used back-translations of target-side monolingual text as extra parallel data for neural translation at ACL 2016. Edunov et al. (2018) scaled it to hundreds of millions of sentences and compared the ways to generate the synthetic sources.
prereqs: [encoder-decoder-model, beam-search]
see_also: [multilingual-neural-translation, sequence-level-knowledge-distillation, data-augmentation, temperature-sampling, noisy-channel-translation-model, bleu, machine-translation, transformer]
sources:
  - paper: doi:10.18653/v1/P16-1009
    title: Rico Sennrich, Barry Haddow and Alexandra Birch, Improving Neural Machine Translation Models with Monolingual Data, ACL 2016, pages 86 to 96
    locator: "abstract (back-translated monolingual data as extra parallel data; +2.8 to 3.7 BLEU on WMT 15 English and German, +2.1 to 3.4 BLEU on IWSLT 14 Turkish to English)"
  - paper: doi:10.18653/v1/D18-1045
    title: Sergey Edunov, Myle Ott, Michael Auli and David Grangier, Understanding Back-Translation at Scale, EMNLP 2018, pages 489 to 500
    locator: "abstract (sampling or noised beam outputs work best except in resource-poor settings; 35 BLEU on the WMT'14 English to German test set)"
---

Back-translation turns monolingual text in the target language into extra training data for a translation model. A second model, trained in the reverse direction, translates each target sentence into the source language. Each pair of a synthetic source and a real target sentence is added to the parallel corpus, and the forward model trains on the mix. The target side of every added pair is real text, so the forward model learns to produce fluent output even though its inputs are noisy. Sennrich, Haddow and Birch (2016) introduced it for neural translation, and Edunov et al. (2018) showed how the choice of the reverse decoder changes the result.

## In plain words

Parallel text, where each sentence has a human translation, is rare and expensive. Text in one language alone is cheap and plentiful.

To translate from German into English, first train a small English to German model. Use it to translate a large amount of English text into German. The German side is machine output and has errors, but the English side is real.

Now train the German to English model on the real pairs plus these new pairs. The model sees many more examples of good English output. It learns to write fluent English, and it learns to cope with inputs that are not perfect.

## When it applies

- You have a parallel corpus for the pair, large enough to train a usable reverse model.
- You have much more monolingual text in the target language than parallel text, ideally from the domain you care about.
- The forward model is a neural sequence model that trains on pairs, such as an [encoder-decoder model](/encoder-decoder-model/) or a [transformer](/transformer/). The technique changes the data, not the architecture.
- You can afford to translate the monolingual text once with the reverse model, which is a large but one-time cost.

## The template

Given parallel data $D = \{(x, y)\}$ from source to target and monolingual target text $M = \{y'\}$:

1. Train a reverse model $Q(x \mid y)$ on $D$ with the roles of the two languages swapped.
2. For each $y' \in M$, generate a synthetic source $\hat x = \mathrm{gen}_Q(y')$. The generator is one of: [beam search](/beam-search/) or greedy search for the most probable $\hat x$; sampling from $Q(\cdot \mid y')$, possibly with a [temperature](/temperature-sampling/) or top-k restriction; or beam search followed by added noise.
3. Form $D' = D \cup \{(\hat x, y') : y' \in M\}$. Optionally mark the synthetic pairs, or upsample $D$ to set the ratio of real to synthetic pairs.
4. Train the forward model $P(y \mid x)$ on $D'$ by the usual maximum likelihood objective. Optionally fine-tune on $D$ alone at the end.

The method is a heuristic: nothing guarantees that the synthetic pairs help. Its value is measured, and the measurements depend on the amount of real data, the generator and the ratio. One way to see why it can help: the model $P(y \mid x)$ is trained on more examples of real target text, which is what a target language model would learn, while the noisy inputs act as a regularizer on the encoder.

## Classic examples

- **WMT and IWSLT.** Sennrich, Haddow and Birch (2016) report gains of 2.8 to 3.7 BLEU on the WMT 15 English and German tasks in both directions, and 2.1 to 3.4 BLEU on the low-resource IWSLT 14 Turkish to English task (measurements, from the abstract). The same paper compares the back-translations with a dummy empty source, which helps less.
- **At scale.** Edunov et al. (2018) back-translated hundreds of millions of English sentences into German and reached 35 BLEU on the WMT'14 English to German test set (a measurement). They found that sampling or noised beam outputs give a stronger training signal than beam or greedy outputs in all but resource-poor settings. Beam search outputs are too regular: they lack the variety of real sources and are easy for the forward model to fit.
- **A worked toy case.** Suppose $D$ has 1000 pairs and $M$ has 9000 sentences. After step 3 the forward model sees 10,000 target sentences, 90% of them with synthetic sources. If the reverse model is weak, upsampling $D$ (for example, repeating it so that the real pairs are a third of the data) keeps the clean signal from being drowned.

## Variations

- **Generator.** Beam, greedy, unrestricted sampling, top-k sampling, or beam with noise such as word deletion, replacement by a filler token and local swaps. The best choice depends on the amount of real data (Edunov et al. 2018).
- **Tagged back-translation.** Add a special tag to every synthetic source, so the model knows which inputs are synthetic. This recovers much of the gain of noise with plain beam outputs (Caswell, Chelba and Grangier 2019, a measurement).
- **Iterative back-translation.** Use the improved forward model to back-translate source-side monolingual text for the reverse model, and repeat. The two models improve each other.
- **Forward translation.** Translating source-side monolingual text with the forward model gives pairs with real sources and synthetic targets. This is closer to [sequence-level knowledge distillation](/sequence-level-knowledge-distillation/) and helps less for fluency, because the targets are machine output.
- **Multilingual models.** In a [multilingual model](/multilingual-neural-translation/), one model can back-translate into many languages, and back-translation can create data for pairs with no parallel text.

## Pitfalls

- **Test set contamination.** Monolingual text crawled from the web can contain the test references. Remove the test sets from $M$ before back-translation.
- **Translationese on the source side.** The forward model trains on machine-translated inputs. Gains measured on test sets whose source side was itself translated from the target language can overstate the gain on original text.
- **Too much synthetic data.** With a weak reverse model and a large $M$, the noise in the sources can hurt. Control the ratio by upsampling the real data, and check on held-out data.
- **Beam outputs in high-resource settings.** Edunov et al. measured that beam back-translations help less than sampled ones there. Do not assume that a better reverse BLEU means better synthetic data.
- **Domain mismatch.** Back-translated text from another domain moves the model toward that domain. Choose $M$ from the target domain.

## Exercises

1. Why must the target side, not the source side, be the real text? *Answer:* the decoder learns to produce what it sees as targets; synthetic targets would teach it the errors of the generator, while synthetic sources only add noise to the input.
2. A reverse model gives the same beam output for two different target sentences $y'_1$ and $y'_2$. What does the forward model learn from these two pairs? *Answer:* that one source has two good translations, which spreads probability between them; with sampling the sources would differ.
3. With 4 million real pairs and 20 million back-translated pairs, how many times must the real data be repeated so that real pairs make up half of each epoch? *Answer:* 5 times.

## References
