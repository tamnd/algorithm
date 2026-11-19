---
tag: GMM8NT
kind: problem
slug: natural-language-inference
name: Natural language inference
aliases:
- recognizing textual entailment
- NLI
area: natural-language-and-speech/natural-language-parsing
level: core
summary: Decide whether a premise sentence entails, contradicts or is neutral toward a hypothesis sentence.
prereqs: [language-model, sentence-embedding]
see_also: [sentence-bert, bert, cross-encoder-reranking, semantic-parsing, semantic-role-labeling, co-np, undecidability, automatic-summarization]
sources:
  - paper: doi:10.1007/11736790_9
    title: "Ido Dagan, Oren Glickman and Bernardo Magnini, The PASCAL Recognising Textual Entailment Challenge, in Machine Learning Challenges (MLCW 2005), Lecture Notes in Computer Science 3944, 177-190, 2006"
    locator: "the definition of textual entailment by what a typical human reader would infer, the two-way task and the first RTE data set"
  - paper: doi:10.18653/v1/D15-1075
    title: "Samuel R. Bowman, Gabor Angeli, Christopher Potts and Christopher D. Manning, A large annotated corpus for learning natural language inference, Proceedings of EMNLP 2015, 632-642"
    locator: "the SNLI corpus of 570K sentence pairs with three labels, its collection from image captions, and its baselines"
  - paper: doi:10.18653/v1/N18-2017
    title: "Suchin Gururangan, Swabha Swayamdipta, Omer Levy, Roy Schwartz, Samuel R. Bowman and Noah A. Smith, Annotation Artifacts in Natural Language Inference Data, Proceedings of NAACL 2018, Volume 2, 107-112"
    locator: "the classifier that sees only the hypothesis, and the words that reveal the label"
  - paper: "Adam Poliak, Jason Naradowsky, Aparajita Haldar, Rachel Rudinger and Benjamin Van Durme, Hypothesis only baselines in natural language inference, Proceedings of *SEM 2018, 180-191"
    title: "Adam Poliak et al., Hypothesis only baselines in natural language inference"
    locator: "hypothesis-only baselines across many NLI data sets"
---

Natural language inference (NLI) takes two sentences, a premise and a hypothesis, and decides whether the premise entails the hypothesis, contradicts it, or neither. Entailment here is what a typical reader would conclude, using common knowledge, not strict logical consequence, so the problem is defined by human judgements and solved by models learned from labeled pairs. NLI tests whether a system understands meaning beyond word overlap, and it is used as a building block for question answering, the checking of summaries and the training of [sentence embeddings](/sentence-embedding/).

## In plain words

Read "A man is playing a guitar on stage" and then "A man is performing music". Most people would say that the second sentence must be true if the first one is. That is entailment.

Now read "The man is asleep". It cannot be true together with the first sentence. That is contradiction. Finally, read "The man is famous". The first sentence does not tell us either way. That is neutral.

An NLI system gets many such pairs with their answers and learns to give the answer for new pairs. It must handle synonyms, negation, numbers, word order and world knowledge, and it must not rely on shallow clues.

## Definition

**Input.** A premise $p$ and a hypothesis $h$, each a sentence or a short text.

**Output.** A label in $\{\text{entailment}, \text{contradiction}, \text{neutral}\}$.

**Question.** Following Dagan, Glickman and Magnini (2006), $p$ entails $h$ if a typical human reading $p$ would infer that $h$ is most likely true. $p$ contradicts $h$ if such a reader would infer that $h$ is most likely false. Otherwise the pair is neutral. The gold label of a pair is the label that most annotators chose.

**Solution method.** There is no exact algorithm, because the labels come from people. A system is a classifier $f(p, h)$ trained on labeled pairs, and it is measured by its accuracy on held-out pairs (measurement). The agreement between annotators bounds the accuracy that can be measured.

## Variants

- **Two-way recognizing textual entailment.** The PASCAL challenges asked only whether $p$ entails $h$, with contradiction and neutral merged.
- **Three-way NLI.** The SNLI corpus (Bowman and others 2015) has 570K pairs with three labels, collected by asking crowd workers to write, for an image caption, one hypothesis that is true, one that might be true and one that is false. MultiNLI extended the method to several genres of text.
- **Graded inference.** The label is a probability or a score of how likely $h$ is given $p$.
- **Long premises.** The premise is a paragraph or a document, as when checking a summary against its source.
- **Formal entailment.** Premise and hypothesis are translated into logic, and the question becomes logical consequence; see the bounds below.

## Examples

| premise | hypothesis | label |
|---|---|---|
| A man is playing a guitar on stage. | A man is performing music. | entailment |
| A man is playing a guitar on stage. | The man is asleep. | contradiction |
| A man is playing a guitar on stage. | The man is famous. | neutral |
| No dogs are in the park. | A poodle is in the park. | contradiction |
| Every student passed the exam. | Kim, a student, passed. | entailment |
| Kim passed the exam. | Every student passed. | neutral |

The last three rows need reasoning about quantifiers and word meanings ("a poodle is a dog"), which is where systems that rely on word overlap fail.

## Known algorithms

- **Overlap and alignment features.** Early systems aligned the words of $h$ to words of $p$ and classified the pair from the quality of the alignment, with features for negation, numbers and antonyms (heuristic).
- **Logic-based inference.** Translate $p$ and $h$ into logical forms by [semantic parsing](/semantic-parsing/), add background axioms, and run a theorem prover. Natural logic systems instead edit $p$ into $h$ step by step and track how each edit, such as replacing a word by a more general one, affects entailment. These methods are precise on what they cover and brittle on the rest (heuristic).
- **Sentence encoders.** Encode $p$ and $h$ separately into vectors $u$ and $v$, and classify a vector built from them, such as $(u, v, |u - v|)$, with a small network. This gives reusable [sentence embeddings](/sentence-embedding/); [Sentence-BERT](/sentence-bert/) is trained this way on SNLI and MultiNLI.
- **Cross-attention models.** Align each word of $h$ with the words of $p$ by attention, compare the aligned pairs, and combine the comparisons. These models see both sentences at once.
- **Pretrained transformers.** Feed $p$ and $h$ together into a pretrained encoder such as [BERT](/bert/), with a classifier on the first position, as a [cross-encoder](/cross-encoder-reranking/) does for ranking. Fine-tuned encoders and large language models give the best measured accuracy on the standard benchmarks (measurement, varies by benchmark).

## Bounds

- **Formal entailment is hard (theorem).** If $p$ and $h$ are formulas of propositional logic, deciding whether $p$ entails $h$ is [coNP](/co-np/)-complete, since $p$ entails $h$ exactly when $p \wedge \neg h$ is unsatisfiable. In first-order logic, entailment is [undecidable](/undecidability/) (Church and Turing). A logic-based NLI system inherits these limits for the fragment it covers.
- **Annotation artifacts (measurement).** A classifier that sees only the hypothesis, never the premise, labels about 67% of the SNLI test pairs and 53% of the MultiNLI pairs correctly, against about 33% for chance (Gururangan and others 2018). Negation words in a hypothesis predict contradiction, and generic words predict entailment, because of how crowd workers wrote them. Poliak and others (2018) found such hypothesis-only baselines well above the majority class on many NLI data sets. High accuracy on one benchmark is therefore weak evidence of inference.
- **Agreement (measurement).** On pairs with several annotators, not all annotators agree with the gold label, which caps the accuracy a fair benchmark can show.

## Reductions

- **From question answering.** Turn a question and a candidate answer into a hypothesis ("Paris is the capital of France"), and check whether a passage entails it.
- **From text classification without training labels.** Turn each label into a hypothesis ("This text is about sports"), and pick the label whose hypothesis the text entails most strongly (heuristic).
- **From checking summaries.** A summary sentence that is not entailed by the source document may be a hallucination. This is used to score the faithfulness of [automatic summarization](/automatic-summarization/) (heuristic).
- **Paraphrase.** Two sentences are paraphrases if each entails the other (heuristic definition).

## Applications

- Evaluation of language understanding, as part of benchmark suites.
- Training data for general-purpose [sentence embeddings](/sentence-embedding/).
- Fact verification against a source, and the faithfulness of summaries and generated text.
- Question answering and information extraction, by the reductions above.

## References
