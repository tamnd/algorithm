---
tag: EFQK8W
kind: technique
slug: multilingual-neural-translation
name: Multilingual neural machine translation
aliases:
- target language token
- zero-shot translation
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: One model translates among many languages by a token that names the target language, and can translate pairs never seen together.
history:
  year: 2017
  people: [Melvin Johnson, Mike Schuster, Quoc V. Le, Maxim Krikun, Yonghui Wu, Zhifeng Chen, Nikhil Thorat, Fernanda Viégas, Martin Wattenberg, Greg Corrado, Macduff Hughes, Jeffrey Dean]
  note: Johnson et al. at Google trained one translation model for many language pairs by adding an artificial token to the input, with no change to the architecture, and showed translation between pairs that had no training data (TACL 2017).
prereqs: [encoder-decoder-model, byte-pair-encoding]
see_also: [back-translation, sequence-level-knowledge-distillation, transformer, temperature-sampling, cross-lingual-embedding-mapping, bleu, machine-translation, additive-attention]
sources:
  - paper: doi:10.1162/tacl_a_00065
    title: Melvin Johnson, Mike Schuster, Quoc V. Le, Maxim Krikun, Yonghui Wu, Zhifeng Chen, Nikhil Thorat, Fernanda Viégas, Martin Wattenberg, Greg Corrado, Macduff Hughes and Jeffrey Dean, Google's Multilingual Neural Machine Translation System - Enabling Zero-Shot Translation, Transactions of the Association for Computational Linguistics 5, 2017, pages 339 to 351
    locator: "the artificial token at the start of the input that names the target language, the shared wordpiece vocabulary, the WMT'14 and WMT'15 results, models with up to twelve language pairs, and translation between pairs never seen in training"
---

Multilingual neural machine translation trains one model to translate among many languages. In the method of Johnson et al. (2017), each training source sentence gets an artificial token at its start that names the language of the wanted output, for example `<2es>` for Spanish. The training data of all pairs is mixed, all languages share one subword vocabulary, and the architecture of the [encoder-decoder model](/encoder-decoder-model/) does not change. At test time the token chooses the output language. The same model can then be asked for a pair it never saw in training, for example Portuguese to Spanish after training only on pairs with English. That this works at all is a measured result, not a property of the method.

## In plain words

Usually one translation model handles one direction, such as German to English. A company that serves 100 languages would need thousands of models.

The multilingual approach puts all the training pairs into one big pile and trains a single model. To tell the model which language to write, it adds a special word to the start of each input, such as "<2es>" for "to Spanish". The model learns to read any of its languages and to write the one the special word asks for.

Because the languages share one model, a language with little data borrows strength from the others. And if the model has learned Portuguese to English and English to Spanish, it can sometimes go straight from Portuguese to Spanish, a direction it was never shown.

## When it applies

- You need translation among several languages, and one model is easier to train, store and serve than one model per direction.
- Some pairs have little parallel data, while related languages or English pairs have much more.
- You can build one subword vocabulary over all the languages, for example with [byte-pair encoding](/byte-pair-encoding/) or wordpieces, so that every language uses the same input and output tables.
- The model is a standard sequence-to-sequence network. The method changes only the data.

## The template

Given parallel corpora $D_{s \to t}$ for a set of directions $(s, t)$, and one token $\tau_t$ for each target language $t$:

1. Learn one subword vocabulary on text from all the languages, with the tokens $\tau_t$ added as reserved symbols.
2. For every pair $(x, y) \in D_{s \to t}$, form the training pair $(\tau_t\, x, \; y)$: put $\tau_t$ in front of the source.
3. Mix all directions into one training set. Choose how often to draw each direction, for example in proportion to its size, or with a flatter distribution so small pairs are seen more often.
4. Train one [encoder-decoder model](/encoder-decoder-model/) by maximum likelihood on the mixed set.
5. To translate $x$ into language $t$, decode from $\tau_t\, x$.

The model learns $P(y \mid \tau_t, x)$. Nothing in the objective asks the encoder to map sentences of different languages with the same meaning to similar vectors, but the shared parameters push it that way. Johnson et al. report analyses that suggest a shared, language-independent representation (a measurement on their models, not a theorem).

**Directions with no data.** For a pair $(s, t)$ with no data, step 5 still runs: the model has seen $s$ as a source (with other targets) and $t$ as a target (from other sources). This is called zero-shot translation. Its quality is a measurement and is usually below a model trained on the pair or a pivot through English.

## Classic examples

- **One model for many pairs.** Johnson et al. (2017) report that a single multilingual model on the WMT'14 benchmarks was comparable for English to French and better than the published results for English to German, and that it beat the published results for French to English and German to English on WMT'14 and WMT'15. Production models with up to twelve language pairs improved many of the individual pairs (measurements, from the abstract).
- **A worked toy case.** With corpora for Portuguese to English, English to Portuguese, Spanish to English and English to Spanish, the training set has four directions and three target tokens, `<2en>`, `<2pt>` and `<2es>`. The pair "<2es> Obrigado." to "Gracias." never occurs. Asking the trained model for it uses the encoder's reading of Portuguese and the decoder's writing of Spanish, learned from other pairs.
- **Implicit bridging.** Johnson et al. found that their models could translate between pairs with no explicit training data, which they call implicit bridging, and that adding a little data for the new pair improves it fast (measurements).

## Variations

- **Many to one and one to many.** If all targets are English, no token is needed; the model is many to one. If all sources are English, the token is necessary.
- **Separate parts per language.** Earlier and later systems use language-specific encoders, decoders or adapter layers with shared parts, which adds capacity but also parameters.
- **Sampling the directions.** Draw each direction with a probability proportional to its size raised to a power below 1, a [temperature](/temperature-sampling/) on the data distribution, so low-resource pairs are not drowned. The power is a heuristic tuned on held-out data.
- **Target token in the decoder.** Put the language token as the first decoder input instead of in the source. This works the same way for the decoder and leaves the encoder input clean.
- **Back-translation for missing pairs.** Use the multilingual model to [back-translate](/back-translation/) into a pair with no data, then train on the synthetic pairs. This usually improves on direct zero-shot output.
- **Mixed tokens.** Johnson et al. also mixed the embeddings of two target tokens and observed outputs that switch between the two languages (a measurement).

## Pitfalls

- **Wrong output language.** In zero-shot directions the model often writes the right meaning in the wrong language, usually English, because it never saw the requested pair. Check the output language before scoring.
- **Capacity dilution.** A model of fixed size shared among many languages can get worse on the high-resource pairs. Larger models or language-specific layers reduce the loss.
- **Vocabulary imbalance.** A subword vocabulary learned on data dominated by a few languages splits the other languages into many short pieces, which makes their sequences long and their quality worse. Balance the text used to learn the vocabulary.
- **Data imbalance.** Sampling directions in proportion to their size starves small pairs; sampling uniformly overfits them. Tune the balance.
- **Comparing with bilingual models.** Report whether the bilingual baselines had the same size, data and training time; otherwise the comparison mixes several effects.

## Exercises

1. A model handles 10 languages, all directions. How many directions does one token per target language cover, and how many bilingual models would be needed? *Answer:* 10 tokens cover $10 \cdot 9 = 90$ directions, which would need 90 bilingual models.
2. Why does a many-to-one model need no target token? *Answer:* the output language is always the same, so there is nothing to choose.
3. The model was trained on Portuguese to English and English to Spanish only. Name two ways to get Portuguese to Spanish, and say which needs two decoding passes. *Answer:* zero-shot decoding with the Spanish token (one pass), and pivoting through English (two passes).

## References
