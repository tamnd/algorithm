---
tag: C7G29A
kind: problem
slug: morphological-analysis
name: Morphological analysis
aliases:
- morphological parsing
area: natural-language-and-speech/tokenization-and-text-normalization
level: core
summary: Map a word form to its lemma and features, such as cats to cat plus noun plus plural, and the reverse map for generation.
prereqs: [text-tokenization, finite-state-transducer]
see_also: [two-level-morphology, lemmatization, stemming, morfessor, part-of-speech-tagging, regular-language, product-construction, subword-tokenization]
sources:
  - paper: "Kimmo Koskenniemi, Two-level morphology: a general computational model for word-form recognition and production, Publications No. 11, Department of General Linguistics, University of Helsinki, 1983"
    title: Koskenniemi 1983
    locator: the two-level model, with a lexicon and parallel rules for recognition and production, applied to Finnish
  - url: https://aclanthology.org/J94-3001/
    title: Ronald M. Kaplan and Martin Kay, Regular models of phonological rule systems, Computational Linguistics 20(3), 1994, pages 331 to 378
    locator: rewrite rules and two-level rules as regular relations, compiled into finite-state transducers and combined by composition
  - book: isbn:9781575864341
    title: Kenneth R. Beesley and Lauri Karttunen, Finite State Morphology, CSLI Publications, 2003
    locator: the lexicon, the rules and the composed lexical transducer used for both analysis and generation
---

Morphological analysis is the problem of taking a word form and finding its parts: the lemma and the grammatical features that the form expresses. For example, "cats" is analyzed as cat+N+PL, the noun "cat" in the plural. The reverse problem, from cat+N+PL to "cats", is generation. A form can have more than one analysis, so the answer is a set. For languages whose word formation is regular, both directions are solved by a [finite-state transducer](/finite-state-transducer/) built from a lexicon and rules, as in [two-level morphology](/two-level-morphology/).

## In plain words

Many words are built from smaller parts: a stem such as "walk" and endings such as "-ed" or "-s". The ending tells you the tense, the number or the case. Spelling changes can hide the parts: "cities" is "city" plus a plural ending, with the y changed to ie.

A morphological analyzer reads a word and lists what it can be: which dictionary word it comes from and which endings it has. Some words have several answers. "flies" is the plural of the noun "fly" and also a form of the verb "fly". The same machine can run backwards and build the right word from a dictionary word and a list of features.

## Definition

Let $\Sigma$ be the alphabet of surface forms (the letters) and let $\Gamma$ be the alphabet of analyses (the letters of lemmas plus feature symbols such as +N, +V, +PL and +3SG). A morphology of a language is a relation $R \subseteq \Gamma^* \times \Sigma^*$: the pair $(a, w)$ is in $R$ when $w$ is a correct form for the analysis $a$.

**Input:** a word form $w \in \Sigma^*$ of $n$ characters, and a description of $R$, usually a lexicon of stems and affixes with their order (the morphotactics) and rules for the spelling changes at the boundaries.

**Output (analysis):** the set $\{a : (a, w) \in R\}$, which is empty for a form that is not a word.

**Output (generation):** for a given analysis $a$, the set $\{w : (a, w) \in R\}$.

A morphology is regular when $R$ is a regular relation, that is, the relation of some finite-state transducer. Kaplan and Kay (1994) showed that the usual rewrite rules of phonology and spelling, when a rule cannot apply to its own output, define regular relations, and that a cascade of such rules is again regular. So for regular morphology one transducer $T$ represents $R$, and analysis and generation are the two directions of the same machine.

## Variants

- **Analysis out of context.** The definition above: all analyses of one form. Choosing the right analysis in a sentence is a different problem, solved with [part-of-speech tagging](/part-of-speech-tagging/) or a disambiguator; [lemmatization](/lemmatization/) is this choice restricted to the lemma.
- **Segmentation only.** Split the form into morphs, such as walk + ed, without labels. [Morfessor](/morfessor/) learns such splits without supervision, and [stemming](/stemming/) cuts suffixes by rules, often to a string that is not a word.
- **Unknown words.** A guesser proposes analyses for a stem that is not in the lexicon from its ending alone.
- **Non-concatenative morphology.** In root-and-pattern languages such as Arabic, the parts of a word interleave. Finite-state methods need extensions here, which Beesley and Karttunen (2003) describe.

## Examples

A small English lexicon, with the analysis on the left and the form on the right:

| analysis | form | what happens |
|---|---|---|
| cat+N+PL | cats | the plural ending s is added |
| fox+N+PL | foxes | an e is inserted after x, s, z, ch and sh |
| city+N+PL | cities | y becomes ie after a consonant |
| goose+N+PL | geese | an irregular form, listed in the lexicon |
| fly+N+PL | flies | y becomes ie |
| fly+V+3SG | flies | the same form for the verb |

Analysis of "flies" returns both fly+N+PL and fly+V+3SG. Generation from fox+N+PL returns "foxes" and not "foxs", because the e-insertion rule must apply. Analysis of "foxs" returns the empty set.

## Known algorithms

- **Lookup in a lexical transducer.** Compile the lexicon and the rules into one transducer $T$ and run $w$ through it. Beesley and Karttunen (2003) describe this approach: the lexicon is a finite-state network of stems and affixes, the rules are transducers, and the composition of all of them is the lexical transducer. Run on the surface side it analyzes, and run on the lexical side it generates.
- **Two-level rules.** Koskenniemi (1983) used a lexicon and a set of rule transducers that run in parallel, each one checking one constraint on the pairs of lexical and surface characters. See [two-level morphology](/two-level-morphology/). Kaplan and Kay (1994) showed how to compile both kinds of rules into single transducers.
- **Learned analyzers.** Analyzers can also be learned from annotated forms. This page does not cover them.

## Bounds

Let $T$ have $q$ states and $t$ transitions, and let the word have $n$ characters. Positions in $w$ are fenceposts $0, \ldots, n$, and position $i$ means that $i$ characters have been read.

- **Lookup cost (theorem).** The analyses of $w$ are the output strings of the accepting paths in the product of $T$ with the linear automaton of $w$ (see [product construction](/product-construction/)). The product has at most $(n + 1) q$ states, one per pair of a position and a state of $T$, and at most $(n + 1) t$ transitions, since each transition of $T$ either reads the next character or reads nothing. A search builds its useful part in $O(n t)$ time. Reading the word needs $\Omega(n)$ time, so for a fixed $T$ the cost is linear in $n$ plus the size of the output.
- **Output size (theorem).** The set of analyses can be large. If $T$ has a cycle that reads nothing and writes something, the set is infinite; practical analyzers avoid such cycles. Without them the set is finite, but for compounds it can grow exponentially in $n$, because each split of a long compound may give its own analysis.
- **Determinism.** A morphology is often not a function from forms to analyses ("flies" has two analyses), so $T$ cannot in general be made deterministic on its input side. Each form may still be looked up in time linear in the size of the product.

## Reductions

- **To transducer lookup.** For regular morphology, analysis is the image of $\{w\}$ under the regular relation $R$, and generation is the image of $\{a\}$ under its inverse. Both are computed by the product above.
- **From lemmatization.** [Lemmatization](/lemmatization/) reduces to analysis followed by a choice: analyze the form and keep the lemma of the analysis that the context selects.
- **To rule compilation.** Building $T$ from rules reduces to operations on regular relations: union, concatenation, [Kleene star](/kleene-star/) and composition (Kaplan and Kay 1994).

## Applications

- [Lemmatization](/lemmatization/) and the indexing of search engines, where all forms of a word should match.
- Spelling checkers and spelling correction for languages with rich inflection, where a list of all forms would be too large. Koskenniemi (1983) built the model for Finnish.
- [Part-of-speech tagging](/part-of-speech-tagging/) and parsing, which use the features of each analysis.
- Machine translation and text generation, which need generation to produce the correct form of a word.
- A linguistically informed alternative to [subword tokenization](/subword-tokenization/), which splits words by frequency and not by morphology.

## References

- Kimmo Koskenniemi. Two-level morphology: a general computational model for word-form recognition and production. Publications No. 11, Department of General Linguistics, University of Helsinki, 1983.
- Ronald M. Kaplan and Martin Kay. Regular models of phonological rule systems. Computational Linguistics 20(3), 1994, pages 331 to 378. https://aclanthology.org/J94-3001/.
- Kenneth R. Beesley and Lauri Karttunen. Finite State Morphology. CSLI Publications, 2003. ISBN 9781575864341.
