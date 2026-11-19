---
tag: 3HD1N4
kind: model
slug: lexicalized-reordering-model
name: Lexicalized reordering model
aliases:
- MSD reordering model
area: natural-language-and-speech/machine-translation-and-alignment
level: advanced
summary: The probability that a phrase pair is placed monotone, swapped or discontinuous relative to the previous phrase, learned per phrase pair.
history:
  year: 2004
  people: [Christoph Tillmann]
  note: Tillmann (2004) modeled the orientation of each phrase with respect to its neighbour, conditioned on the phrase itself. Koehn et al. (2005) gave the monotone, swap and discontinuous form that the Moses decoder uses, and Galley and Manning (2008) later computed the orientation with respect to blocks of phrases instead of single phrases.
prereqs: [phrase-based-translation-model]
see_also: [phrase-based-stack-decoding, phrase-pair-extraction, log-linear-translation-model, word-alignment, inversion-transduction-grammar, hierarchical-phrase-based-translation, minimum-error-rate-training, maximum-likelihood-estimation]
sources:
  - paper: "Christoph Tillmann, A unigram orientation model for statistical machine translation, HLT-NAACL 2004, Short Papers, pages 101 to 104"
    title: Tillmann 2004
    locator: the orientation of a phrase with respect to the previous phrase and its probability given the phrase
  - paper: "Philipp Koehn, Amittai Axelrod, Alexandra Birch Mayne, Chris Callison-Burch, Miles Osborne and David Talbot, Edinburgh system description for the 2005 IWSLT speech translation evaluation, IWSLT 2005, ACL Anthology 2005.iwslt-1.8"
    title: Koehn et al. 2005
    locator: "Section 2.6 (lexicalised reordering: the monotone, swap and discontinuous orientations, read from the alignment points at the top left and top right of a phrase pair)"
  - book: isbn:9780521874151
    title: Philipp Koehn, Statistical Machine Translation, Cambridge University Press, 2010
    locator: "Chapter 5 (phrase-based models: lexicalized reordering)"
---

The lexicalized reordering model gives each phrase pair of a [phrase-based model](/phrase-based-translation-model/) its own probabilities for three orientations: *monotone* (the phrase follows the previous phrase directly in the source), *swap* (it comes directly before the previous phrase in the source) and *discontinuous* (anything else). The probabilities are counted from the word-aligned training data when the phrase pairs are [extracted](/phrase-pair-extraction/). The plain distortion cost only penalizes the distance of a jump, the same for all words; the lexicalized model can learn that, for example, a French adjective is often swapped with the noun before it. It is a feature of the [log-linear model](/log-linear-translation-model/), next to the distortion cost.

## The machine

**Direction and notation.** Translation runs from the source $f = f_1 \ldots f_m$ to the target $e = e_1 \ldots e_l$, and the phrases are placed in target order, left to right. Spans are fencepost: the source span $(s, t)$ covers $f_{s+1} \ldots f_t$, and the target span $(u, v)$ covers $e_{u+1} \ldots e_v$. Logs are natural.

**Orientation in decoding.** A derivation places phrase pairs with source spans $(s_1, t_1), \ldots, (s_n, t_n)$ in target order, with a virtual phrase $(s_0, t_0) = (0, 0)$ at the start. The orientation of phrase $k$ with respect to phrase $k - 1$ is

- monotone if $s_k = t_{k-1}$: it starts right where the previous phrase ended;
- swap if $t_k = s_{k-1}$: it ends right where the previous phrase started;
- discontinuous otherwise.

**Orientation in training.** For an extracted phrase pair with source span $(s, t)$ and target span $(u, v)$, the word before the target phrase is $e_u$, and its alignment decides the orientation. The pair is monotone if $e_u$ is aligned to $f_s$, the word before the source phrase (the alignment point at the top left of the pair in the alignment matrix), swap if $e_u$ is aligned to $f_{t+1}$, the word after the source phrase (the top right), and discontinuous otherwise. At the start of the sentence, $(s, u) = (0, 0)$ counts as an alignment point.

**Estimation.** With $c(o, \bar f, \bar e)$ the number of extractions of the pair $(\bar f, \bar e)$ with orientation $o \in \{\mathrm{m}, \mathrm{s}, \mathrm{d}\}$, the relative frequency estimate is

$$p(o \mid \bar f, \bar e) = \frac{c(o, \bar f, \bar e)}{\sum_{o'} c(o', \bar f, \bar e)}.$$

Most phrase pairs are seen only a few times, so this estimate is usually smoothed toward the orientation distribution of all pairs.

**The feature.** For a derivation with phrase pairs $(\bar f_k, \bar e_k)$ and orientations $o_k$, the feature is $\sum_k \ln p(o_k \mid \bar f_k, \bar e_k)$. Moses splits it into one feature per orientation, each with its own weight, and also uses a second model for the orientation of the next phrase with respect to the current one. With both directions and three orientations, that gives six weights.

**Example.** Translate f = maison bleue into English. Suppose the training data gives these orientation probabilities:

| phrase pair | monotone | swap | discontinuous |
|---|---|---|---|
| maison, house | 0.4 | 0.5 | 0.1 |
| bleue, blue | 0.3 | 0.1 | 0.6 |

For the order "blue house", the first phrase bleue has the source span (1, 2) and does not start at 0, so it is discontinuous. Then maison with span (0, 1) ends where bleue started, so it is a swap. The score is $\ln 0.6 + \ln 0.5 = -0.511 - 0.693 = -1.204$. For "house blue", both phrases are monotone, with the score $\ln 0.4 + \ln 0.3 = -0.916 - 1.204 = -2.120$. The lexicalized model prefers "blue house" by $0.916$. The distance-based distortion cost $-\sum_k |s_k - t_{k-1}|$ gives $-(1 + 2) = -3$ to "blue house" and $0$ to "house blue", so on its own it prefers the wrong order, and only the language model could correct it.

## What it counts

The model counts orientations: three numbers per phrase pair, or six with both directions.

- **Training** adds two lookups in the alignment matrix for each extracted phrase pair, so it costs no more than [phrase pair extraction](/phrase-pair-extraction/) itself. The reordering table has one row per phrase pair, the same size as the phrase table.
- **Decoding** adds one table lookup per phrase. The orientation of a new phrase needs the start and the end of the previous phrase, so a [stack decoder](/phrase-based-stack-decoding/) must keep the start of the last phrase in its state, next to the end. Hypotheses that differ in it can no longer be recombined, which makes the search space a little larger.

## Relation to other models

- **Distance-based distortion.** The plain distortion cost $-\sum_k |s_k - t_{k-1}|$ depends only on the jump width. The lexicalized model depends only on the orientation class and the phrase pair. They measure different things, and systems use both.
- **Phrase-based model.** The lexicalized reordering model is one feature family of the [phrase-based model](/phrase-based-translation-model/); it does not change the derivations, only their scores.
- **Hierarchical reordering.** Galley and Manning (2008) decide the orientation with respect to the largest block of earlier phrases that is adjacent in the source, not the single previous phrase. This makes the classes depend less on how the source was segmented and captures swaps of longer blocks.
- **Inversion transduction grammar.** An [ITG](/inversion-transduction-grammar/) also has two orientations, straight and inverted, but it applies them to nested constituents at all levels, not only to adjacent phrases.
- **Hierarchical phrase-based model.** [Hiero](/hierarchical-phrase-based-translation/) writes the reordering into its rules with gaps, so it needs no separate orientation model for the reordering inside a rule.

## Known results in the model

- **The orientations partition the cases (theorem).** In decoding, monotone and swap cannot hold together for nonempty phrases: $s_k = t_{k-1}$ and $t_k = s_{k-1}$ would give $t_k = s_{k-1} < t_{k-1} = s_k < t_k$. So every placement has exactly one orientation.
- **Training can be ambiguous.** In training, $e_u$ can be aligned to both $f_s$ and $f_{t+1}$, so both tests can succeed. Implementations test monotone first. With a word-based test, a pair is also called discontinuous when $e_u$ is unaligned, even if the phrase follows its neighbour directly; this is a property of the definition, and the block-based test of Galley and Manning (2008) reduces it.
- **Gains over distance only (measurement).** Tillmann (2004) and Koehn et al. (2005) reported better translation scores with orientation probabilities than with the distance-based cost alone.
- **Local reordering only.** The model scores each step relative to its neighbour, and it cannot express long-distance patterns such as moving a verb to the end of a clause; long jumps all fall into the discontinuous class.

## References
