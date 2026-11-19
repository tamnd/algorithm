---
tag: JXF310
kind: definition
slug: parallel-corpus
name: Parallel corpus
aliases:
- bitext
- bilingual corpus
area: natural-language-and-speech/machine-translation-and-alignment
level: intro
summary: A collection of texts paired with their translations, aligned at the document or sentence level, the training data of translation models.
prereqs: []
see_also: [sentence-alignment, word-alignment, gale-church-alignment, machine-translation, back-translation, ibm-model-1, sentence-boundary-detection, bleu]
sources:
  - paper: "Philipp Koehn, Europarl: a parallel corpus for statistical machine translation, MT Summit X, 2005, pages 79 to 86"
    title: Koehn 2005
    locator: the collection of the European Parliament proceedings, their alignment at the document and sentence level, and the translation systems trained on it
  - paper: doi:10.3115/981344.981366
    title: Peter F. Brown, Jennifer C. Lai and Robert L. Mercer, Aligning sentences in parallel corpora, 29th Annual Meeting of the ACL, 1991, pages 169 to 176
    locator: the Canadian Hansards as a parallel corpus of English and French, and their alignment at the sentence level
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 2 (Words, Sentences, Corpora)"
---

A parallel corpus, or bitext, is a collection of texts in one language together with their translations in another language, in which each text is paired with its translation. The pairs are usually aligned further, so that each sentence or short group of sentences is paired with its translation. The sentence pairs are the training data of statistical and neural [machine translation](/machine-translation/): a translation model learns from them which words and phrases translate each other, first by [word alignment](/word-alignment/). Early large examples were the Canadian Hansards, the English and French proceedings of the Canadian parliament, and Europarl, the proceedings of the European Parliament (Koehn 2005).

## Definition

A **document-level parallel corpus** is a finite set of pairs $(d, d')$, where $d$ is a text in language $L$ and $d'$ is a text in language $L'$ with the same content: one translates the other, or both translate a third text.

A **sentence-aligned parallel corpus** is a finite sequence of pairs $(f_k, e_k)$, $k = 1, \ldots, N$, where $f_k$ is a sentence or a short block of consecutive sentences of a text in $L$, $e_k$ is the corresponding block of its translation in $L'$, and the blocks are found by [sentence alignment](/sentence-alignment/). The pair is a sentence pair even if a block has two sentences, or none. Many corpora drop the pairs in which one side is empty.

A **multi-parallel corpus** has the same content in more than two languages, so that each text comes as a tuple of translations.

The definition requires the content to be the same, not the form. Translations can split and merge sentences, change their order inside a sentence, add explanations and leave things out. A corpus can also record the direction of translation, which original text was translated into which language, because translated text differs in style from original text.

## Examples and non-examples

- **The Canadian Hansards.** The debates of the Canadian parliament are published in English and in French. Brown, Lai and Mercer (1991) aligned them at the sentence level, and the IBM translation models were trained on them.
- **Europarl.** The proceedings of the European Parliament in the official languages of the European Union, collected and aligned at the document and sentence level by Koehn (2005). Because every text exists in many languages, it is a multi-parallel corpus.
- **The Rosetta Stone.** The same decree written in Egyptian hieroglyphs, Demotic script and Greek. It is a small multi-parallel text, and it helped scholars to read hieroglyphs.
- **A tiny sentence-aligned corpus.** The three pairs ("das Haus", "the house"), ("das Buch", "the book") and ("ein Buch", "a book") are the example corpus on which [IBM Model 1](/ibm-model-1/) learns that "Haus" translates "house".
- **Synthetic pairs.** [Back-translation](/back-translation/) translates monolingual text by machine to get more pairs. The result is used as a parallel corpus, but one side is not a human translation, and it is usually marked as synthetic.
- **Non-example: a comparable corpus.** News articles in two languages about the same events are related but do not translate each other. Some of their sentences are translations, and a search for such sentence pairs can build a parallel corpus from them, but the articles themselves are not parallel.
- **Non-example: two unrelated texts in two languages.** Without the relation of translation there is nothing to align.

## Related definitions

- [Sentence alignment](/sentence-alignment/) turns a document-level corpus into a sentence-aligned one, for example by [Gale-Church alignment](/gale-church-alignment/), which uses sentence lengths only. It needs the sentences, which [sentence boundary detection](/sentence-boundary-detection/) finds.
- [Word alignment](/word-alignment/) adds links between the words of each sentence pair.
- Test sets for evaluation are small parallel corpora held out from training. Metrics such as [BLEU](/bleu/) compare a system output with the human translation of the test set.

## References
