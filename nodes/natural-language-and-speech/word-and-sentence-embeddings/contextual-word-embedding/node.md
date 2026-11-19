---
tag: H013XA
kind: concept
slug: contextual-word-embedding
name: Contextual word embedding
aliases:
- contextualized word representation
area: natural-language-and-speech/word-and-sentence-embeddings
level: core
summary: A vector for each occurrence of a word computed from the whole sentence by a deep network, so one word gets different vectors in different senses.
history:
  year: 2018
  people: [Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee, Luke Zettlemoyer]
  note: ELMo made vectors from the layers of a pretrained bidirectional language model the standard input of task models. BERT followed in 2019 with a transformer that is fine-tuned on each task.
prereqs: [word-embedding, language-model]
see_also: [elmo, bert, generative-pretrained-transformer, masked-language-modeling, word-sense-disambiguation, sentence-embedding, bertscore, skip-gram-model]
sources:
  - paper: doi:10.18653/v1/N18-1202
    title: Matthew E. Peters, Mark Neumann, Mohit Iyyer, Matt Gardner, Christopher Clark, Kenton Lee and Luke Zettlemoyer, Deep contextualized word representations, NAACL-HLT 2018, pages 2227 to 2237
    locator: the definition of the task vector as a weighted sum of the biLM layers, the results on six tasks, and the word sense and part of speech experiments on single layers
  - paper: doi:10.18653/v1/N19-1423
    title: Jacob Devlin, Ming-Wei Chang, Kenton Lee and Kristina Toutanova, BERT, Pre-training of deep bidirectional transformers for language understanding, NAACL-HLT 2019, pages 4171 to 4186
    locator: the masked language model pretraining and the feature-based use of the layers
  - paper: doi:10.18653/v1/D19-1006
    title: Kawin Ethayarajh, How contextual are contextualized word representations? Comparing the geometry of BERT, ELMo and GPT-2 embeddings, EMNLP-IJCNLP 2019, pages 55 to 65
    locator: the measures of self-similarity, intra-sentence similarity and maximum explainable variance, and the anisotropy of every layer
  - paper: "Bryan McCann, James Bradbury, Caiming Xiong and Richard Socher, Learned in translation: contextualized word vectors, Advances in Neural Information Processing Systems 30 (NIPS 2017)"
    title: McCann et al. 2017
    locator: the CoVe vectors taken from the encoder of a translation model
---

A contextual word embedding gives a vector to each occurrence of a word, not to the word type. The vector is computed by a deep network from the whole sentence, so "bank" in "the river bank" and "bank" in "the bank loan" get different vectors. A static [word embedding](/word-embedding/), such as [skip-gram](/skip-gram-model/) or [GloVe](/glove/), gives both the same vector. The networks that compute contextual vectors are [language models](/language-model/) pretrained on large corpora, such as [ELMo](/elmo/), [BERT](/bert/) and [GPT](/generative-pretrained-transformer/).

## In plain words

A table of word vectors has one row per word. That row must serve every meaning of the word, so "bank" is a blend of the money sense and the river sense, and the network that uses it must sort out the meaning from the other words. A contextual embedding does this work first. A large network reads the whole sentence and returns one vector for each position. The vector for "bank" now depends on whether "river" or "loan" is near it. Since the network was trained to predict words from their neighbors on billions of words, its vectors hold much of what a task needs: the part of speech, the sense of the word, and how it relates to the rest of the sentence.

## The idea

A static embedding is a function of the word type: $e(w)$ is one row of a matrix $E$ with $|V|$ rows. A contextual embedding is a function of the whole sequence and a position: for tokens $t_1, \ldots, t_N$ the network returns $h_k = f(t_1, \ldots, t_N, k)$ for each $k$. Two occurrences of one word type at positions $k$ and $k'$ get different vectors when their contexts differ.

The function $f$ is the hidden state of a network trained as a language model. In [ELMo](/elmo/), $f$ is a learned weighted sum of the layers of a two-layer bidirectional LSTM language model over character-based token vectors. In [BERT](/bert/), $f$ is a layer of a transformer encoder trained by [masked language modeling](/masked-language-modeling/). In [GPT](/generative-pretrained-transformer/), $f$ sees only the tokens to the left, because the model is trained by [causal language modeling](/causal-language-modeling/). Most of these models work on subword pieces, such as [WordPiece](/wordpiece/), so the vector of a word made of several pieces is taken from its first piece or from the mean of its pieces.

There are two ways to use the vectors. In the feature-based way, the network is frozen and its vectors are the input of a task model, as ELMo was used. In the fine-tuning way, a small output layer is added and the whole network is trained further on the task, as BERT was used. In both, a static embedding is a special case: a network that ignores the context gives the same vector at every position.

Ethayarajh 2019 measured how much the vectors depend on the context with three numbers: the self-similarity of a word (the mean cosine between its vectors in different contexts), the intra-sentence similarity (the mean cosine between the vectors in one sentence and their mean), and the maximum explainable variance (the share of the variance of the vectors of a word that its first principal component explains).

## Examples

**A toy contextualizer.** This is not a trained model; it shows only the definition. Let the static vectors be the $(0, 0)$, river $(0, 2)$, loan $(2, 0)$ and bank $(1, 1)$, and let $h_k = e(t_k) + \frac{1}{2}(e(t_{k-1}) + e(t_{k+1}))$, with the zero vector outside the sentence. In "the river bank", bank gets $(1, 1) + \frac{1}{2}(0, 2) = (1, 2)$. In "the bank loan", bank gets $(1, 1) + \frac{1}{2}((0, 0) + (2, 0)) = (2, 1)$. The cosine of the two bank vectors is $4/5 = 0.8$, where a static embedding gives 1. The cosine of the first bank vector with river is $4 / (2\sqrt{5}) = 0.894$, against $2 / (2\sqrt{2}) = 0.707$ for the static vector of bank, and the second bank vector has the same cosine 0.894 with loan.

**Layers hold different information (measurement).** Peters et al. 2018 trained a classifier on the vectors of single layers of the ELMo language model. For word sense disambiguation, the top layer gave an F1 of 69.0 and the first layer 67.4. For part of speech tagging, the first layer gave an accuracy of 97.3 and the top layer 96.8. The lower layer holds more syntax and the upper layer more meaning.

**Geometry (measurement).** Ethayarajh 2019 found that the vectors of ELMo, BERT and GPT-2 are anisotropic in every layer: two random words have a high mean cosine. The self-similarity of a word is lower in the upper layers, so those layers are more specific to the context. On average, a static vector explains less than 5% of the variance of the contextual vectors of a word, so the vectors are not just a few sense vectors.

## Where it is used

- **Task models.** Adding ELMo vectors to the input of existing models for question answering, [natural language inference](/natural-language-inference/), [semantic role labeling](/semantic-role-labeling/), [coreference](/coreference-resolution/), [named entity recognition](/named-entity-recognition/) and [sentiment](/sentiment-analysis/) reduced the relative error by 6% to 20% (Peters et al. 2018, a measurement). Fine-tuning BERT then improved most of these tasks again.
- **Word senses.** The nearest labeled occurrence by cosine is a simple [word sense disambiguation](/word-sense-disambiguation/) method on contextual vectors.
- **Evaluation metrics.** [BERTScore](/bertscore/) matches the contextual vectors of the tokens of a candidate text and a reference by cosine.
- **Sentence vectors.** Pooling the token vectors gives a [sentence embedding](/sentence-embedding/). Plain pooling of BERT vectors measured worse than averaged GloVe vectors on similarity tasks; [Sentence-BERT](/sentence-bert/) and [SimCSE](/simcse/) train the network so that pooled vectors work.

## References
