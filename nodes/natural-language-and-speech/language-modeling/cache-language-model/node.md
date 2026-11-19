---
tag: K67FPM
kind: model
slug: cache-language-model
name: Cache language model
aliases:
- Kuhn-De Mori cache model
area: natural-language-and-speech/language-modeling
level: advanced
summary: "Interpolate a static language model with a unigram or bigram model of the recent words in the document, since words just used tend to recur."
history:
  year: 1990
  people: [Roland Kuhn, Renato De Mori]
  note: Kuhn and De Mori added a cache of recent words to each part-of-speech class of a speech recognition language model. Jelinek and colleagues added a cache to a word trigram model in 1991.
prereqs: [n-gram-language-model]
see_also: [n-gram-language-model, deleted-interpolation, adaptive-modeling, prediction-by-partial-matching, maximum-entropy-language-model, recurrent-neural-network-language-model, perplexity, sliding-window]
sources:
  - paper: doi:10.1109/34.56193
    title: Roland Kuhn and Renato De Mori, A cache-based natural language model for speech recognition, IEEE Transactions on Pattern Analysis and Machine Intelligence 12(6), 1990, pages 570 to 583
    locator: the cache component for each part-of-speech class, mixed with the static word probabilities of a model over part-of-speech trigrams, tested on the LOB corpus
  - paper: "Roland Kuhn and Renato De Mori, Correction to A cache-based natural language model for speech recognition, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(6), 1992, pages 691 to 692"
    title: Kuhn and De Mori 1992
    locator: the correction to the 1990 paper
  - paper: "Frederick Jelinek, Bernard Merialdo, Salim Roukos and Martin Strauss, A dynamic language model for speech recognition, Proceedings of the DARPA Speech and Natural Language Workshop, 1991"
    title: Jelinek, Merialdo, Roukos and Strauss 1991
    locator: a word trigram model interpolated with caches of the recent text
  - paper: "Edouard Grave, Armand Joulin and Nicolas Usunier, Improving neural language models with a continuous cache, ICLR 2017, arXiv:1612.04426"
    title: Grave, Joulin and Usunier 2017
    locator: the neural cache, which stores recent hidden states with the words that followed them
  - paper: "Joshua T. Goodman, A bit of progress in language modeling, extended version, arXiv:cs/0108005, 2001"
    title: Goodman 2001
    locator: the section on caching, one of the improvements of n-gram models that the report compares on the same data
---

A cache language model adds a short-term memory to a static language model. Text is not a sequence of independent draws: a word that appeared a moment ago, such as a name or the topic of a news story, is much more likely than usual to appear again. A static [n-gram model](/n-gram-language-model/) cannot see this, because its counts come from the whole training corpus and its history is only the last $n - 1$ words. The cache model keeps the last $K$ words of the current document, builds a unigram (or bigram) distribution from them, and mixes it with the static model at a fixed weight. Kuhn and De Mori introduced the idea for speech recognition in 1990, with one cache for each part-of-speech class.

## The machine

**Parts.** A static model $P_s(w \mid h)$, trained once, with $h$ the last $n - 1$ words; a cache size $K$; a weight $\lambda \in [0, 1]$.

**State.** The cache holds the last $K$ words $w_{t-K}, \ldots, w_{t-1}$ of the current document and their counts $c_t(w)$, with $\sum_w c_t(w) = \min(t - 1, K)$.

**The prediction.** For the next word $w_t$, with $h$ the last $n - 1$ words,

$$P(w \mid h, \text{cache}) = \lambda\, P_c(w) + (1 - \lambda)\, P_s(w \mid h), \qquad P_c(w) = \frac{c_t(w)}{\sum_v c_t(v)}.$$

Both parts are distributions over the vocabulary, so the mixture is one too. At the start of a document the cache is empty and $\lambda$ is taken as 0.

**The update.** After $w_t$ is known, add one to $c(w_t)$, and if the cache holds more than $K$ words, subtract one for the oldest. This is a [sliding window](/sliding-window/) of counts. In evaluation $w_t$ is the true next word of the test text; in a speech recognizer it is the recognized word.

**Variants of the cache part.**

- *A bigram cache* uses $c_t(v w)/c_t(v)$ for the previous word $v$, often together with the unigram cache.
- *A class cache*, as in Kuhn and De Mori, keeps one cache for each part-of-speech class $g$ and mixes $P_c(w \mid g)$ with the static $P(w \mid g)$ inside a model over class trigrams.
- *A decaying cache* gives each past occurrence a weight that falls with its distance, in place of the hard window.
- *A neural cache* (Grave, Joulin and Usunier) stores the hidden state of a [recurrent model](/recurrent-neural-network-language-model/) at each recent position together with the word that followed, and weights each stored word by the similarity of its state to the current one.

**An example.** Let the static trigram give a rare name $P_s(\text{Mars} \mid h) = 0.0001$, and let the name occur 4 times among the last $K = 200$ words, so $P_c(\text{Mars}) = 0.02$. With $\lambda = 0.1$,

$$P(\text{Mars} \mid h, \text{cache}) = 0.1 \cdot 0.02 + 0.9 \cdot 0.0001 = 0.00209,$$

about 21 times the static value. A word that is not in the cache gets $0.9$ times its static probability. So the cache helps a word exactly when $P_c(w) > P_s(w \mid h)$, and costs every other word the factor $1 - \lambda$.

## What it counts

The model is measured by its [perplexity](/perplexity/) on test text, read in order, with the cache filled from the test words already seen, and in a speech recognizer by the word error rate. The cost of a prediction is the cost of the static model plus $O(1)$ expected time for the cache: one [hash table](/hash-table/) lookup for $c_t(w)$, and $O(1)$ for the update when the count of the window is kept. A full distribution over the vocabulary $V$ costs $O(|V|)$ more, or $O(K)$ more if only the cached words are changed and the rest is scaled by $1 - \lambda$. The memory is $O(K)$. The weight $\lambda$, and $K$, are set on held-out documents, for example by the EM procedure of [deleted interpolation](/deleted-interpolation/).

## Relation to other models

- **Static n-gram model.** With $\lambda = 0$ it is the static model.
- **Linear interpolation.** The cache model is a mixture of two models with a fixed weight, the same form as [deleted interpolation](/deleted-interpolation/) and [Jelinek-Mercer smoothing](/jelinek-mercer-smoothing/), but one of the two parts changes as the document is read.
- **Adaptive models in compression.** An [adaptive model](/adaptive-modeling/) updates its counts after each symbol. [Prediction by partial matching](/prediction-by-partial-matching/) and [context mixing](/context-mixing/) do this for every context, which makes them caches of every order with no static part.
- **Trigger models.** A [maximum entropy language model](/maximum-entropy-language-model/) with trigger features, as in Rosenfeld (1996), generalizes the self-trigger of the cache: a word in the history can raise the probability of other related words, not only of itself.
- **Topic models.** A model such as [latent Dirichlet allocation](/latent-dirichlet-allocation/) explains the same burstiness of words with a document-level topic mixture.
- **Recurrent models.** A [recurrent neural network language model](/recurrent-neural-network-language-model/) can in principle remember recent words in its state, but in practice an explicit cache still helps it, which is the point of the neural cache.
- **Caches in computing.** The name comes from the memory [cache](/cache/), which also keeps recently used items because they are likely to be used again. Here nothing is evicted by a policy; the window simply moves.

## Known results in the model

- **A proper distribution.** For any $\lambda \in [0, 1]$ the mixture of two distributions is a distribution, so perplexity is well defined.
- **A gain on recurring words.** The model gains exactly on the words whose cache probability exceeds their static probability, as in the example. For a good static model, most of these are content words of the current topic: names, numbers and the words of the subject.
- **Perplexity against error rate.** Caches give large perplexity reductions, but the reduction of the word error rate is often much smaller. One reason is that a recognizer fills the cache with its own output, so an error makes the same error more likely later in the document.
- **Part-of-speech caches.** Kuhn and De Mori tested a cache for each part-of-speech class on text of the LOB corpus and reported a lower perplexity than the same model without the cache. A correction to the paper appeared in 1992.
- **Word models.** Jelinek and colleagues (1991) put caches of the recent text into a word trigram model for speech recognition, so that the cache works on words directly and needs no tagger.
- **Neural models.** Grave, Joulin and Usunier (2017) showed that a cache of recent hidden states lowers the perplexity of LSTM language models, with no extra training, and that it can use a very large window.

## References
