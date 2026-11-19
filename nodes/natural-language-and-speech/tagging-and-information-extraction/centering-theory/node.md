---
tag: DMS6SX
kind: model
slug: centering-theory
name: Centering theory
aliases:
- centering model of local coherence
area: natural-language-and-speech/tagging-and-information-extraction
level: advanced
summary: "A model of local discourse coherence that ranks the entities of each utterance and classifies transitions as continue, retain, smooth shift or rough shift."
history:
  year: 1995
  people: [Barbara J. Grosz, Aravind K. Joshi, Scott Weinstein, Susan E. Brennan, Marilyn W. Friedman, Carl J. Pollard]
  note: "Grosz, Joshi and Weinstein first presented centering in 1983 and gave the full account in 1995; Brennan, Friedman and Pollard (1987) turned it into a pronoun resolution algorithm with four transitions."
prereqs: [coreference-resolution]
see_also: [hobbs-algorithm, mention-pair-model, span-ranking-coreference, rhetorical-structure-theory, incremental-algorithm-referring-expressions, dependency-parsing, named-entity-recognition, entity-linking]
sources:
  - paper: "Barbara J. Grosz, Aravind K. Joshi and Scott Weinstein, Centering: a framework for modeling the local coherence of discourse, Computational Linguistics 21(2), 1995, pages 203 to 225"
    title: Grosz, Joshi and Weinstein 1995
    locator: the definitions of the forward-looking and backward-looking centers, the constraints, Rule 1 on pronouns and Rule 2 on the ordering of transitions
  - paper: "Susan E. Brennan, Marilyn W. Friedman and Carl J. Pollard, A centering approach to pronouns, Proceedings of ACL 1987, pages 155 to 162"
    title: Brennan, Friedman and Pollard 1987
    locator: "the ranking of the forward-looking centers by grammatical role, the four transitions continuing, retaining, shifting-1 and shifting (Figure 3), their preference order, and the algorithm that generates, filters and ranks the anchors"
  - paper: "Marilyn A. Walker, Masayo Iida and Sharon Cote, Japanese discourse and the process of centering, Computational Linguistics 20(2), 1994, pages 193 to 233"
    title: Walker, Iida and Cote 1994
    locator: the names smooth shift and rough shift for the two shift transitions, and the ranking of centers for Japanese
  - paper: "Joel R. Tetreault, A corpus-based evaluation of centering and pronoun resolution, Computational Linguistics 27(4), 2001, pages 507 to 520"
    title: Tetreault 2001
    locator: the left-right centering algorithm and the corpus comparison with the algorithm of Brennan, Friedman and Pollard and with the Hobbs algorithm
  - book: isbn:9780131873216
    title: "Daniel Jurafsky and James H. Martin, Speech and Language Processing, 2nd edition, Prentice Hall, 2009"
    locator: "Chapter 21, Computational Discourse (the section on the centering algorithm for pronoun resolution, with worked examples)"
---

Centering theory is a model of local coherence: why some sequences of sentences about the same entities read smoothly and others do not. In each utterance it ranks the entities that the utterance mentions, and it names one of them, the backward-looking center, as the entity that the utterance is mainly about and that links it to the previous utterance. A text is easier to read when it keeps the same center and keeps that center in the most prominent position. The model was given its standard form by Grosz, Joshi and Weinstein (1995). Brennan, Friedman and Pollard (1987) turned it into an algorithm for pronouns: choose the referents that make the most preferred transition. The model is a set of definitions and preferences, a heuristic theory of reading, not a theorem about texts.

## The machine

**Utterances and centers.** A discourse is a sequence of utterances $U_1, \ldots, U_m$, usually clauses or sentences. Each utterance $U_t$ has:

- the forward-looking centers $\mathrm{Cf}(U_t)$, the list of entities that $U_t$ mentions, ranked by prominence;
- the preferred center $\mathrm{Cp}(U_t)$, the highest-ranked element of $\mathrm{Cf}(U_t)$;
- the backward-looking center $\mathrm{Cb}(U_t)$, the highest-ranked element of $\mathrm{Cf}(U_{t-1})$ that $U_t$ also mentions.

The Cb of the first utterance is undefined, and so is the Cb of an utterance that mentions no entity of the previous one.

**Ranking.** The ranking of $\mathrm{Cf}$ depends on the language. Brennan, Friedman and Pollard (1987) rank by grammatical role, as subject > object > second object > other subcategorized arguments > adjuncts. Walker, Iida and Cote (1994) give a different ranking for Japanese, with topic marking at the top.

**Constraints and rules** (Grosz, Joshi and Weinstein 1995). Each utterance has at most one Cb, which is the highest-ranked element of $\mathrm{Cf}(U_{t-1})$ realized in $U_t$. Rule 1: if any element of $\mathrm{Cf}(U_{t-1})$ is realized by a pronoun in $U_t$, then $\mathrm{Cb}(U_t)$ is realized by a pronoun too. Rule 2: sequences of continuations are preferred over sequences of retaining, which are preferred over sequences of shifting.

**Transitions.** From $U_{t-1}$ to $U_t$, compare two yes or no questions: is $\mathrm{Cb}(U_t) = \mathrm{Cb}(U_{t-1})$ (or is $\mathrm{Cb}(U_{t-1})$ undefined), and is $\mathrm{Cb}(U_t) = \mathrm{Cp}(U_t)$?

| | Cb same as before | Cb changed |
|---|---|---|
| Cb is the Cp | continue | smooth shift |
| Cb is not the Cp | retain | rough shift |

Brennan, Friedman and Pollard (1987) called the four cells continuing, retaining, shifting-1 and shifting, and ordered them continuing > retaining > shifting-1 > shifting. The names smooth shift and rough shift come from Walker, Iida and Cote (1994). Grosz, Joshi and Weinstein (1995) use only three transitions, continue, retain and shift.

**The pronoun algorithm** (Brennan, Friedman and Pollard 1987). For each utterance:

1. Generate every anchor: a choice of a referent for each pronoun, with the resulting $\mathrm{Cf}$ list and a possible Cb.
2. Filter out the anchors that break agreement, binding constraints, or Rule 1.
3. Rank the rest by the transition they give, and pick an anchor with the most preferred one.

## What it counts

The model counts transitions. A text with many continue transitions is predicted to be more coherent, and easier to process, than the same content with more shifts. Two kinds of events are marked as costs: a change of the Cb, and a Cb that is not the most prominent entity of its utterance. Rule 1 also counts a violation each time an entity other than the Cb is a pronoun while the Cb is not.

Example from Jurafsky and Martin: "John saw a beautiful 1961 Ford Falcon at the used car dealership. He showed it to Bob. He bought it."

- $U_1$: $\mathrm{Cf} = [\text{John}, \text{Ford}, \text{dealership}]$, Cb undefined.
- $U_2$: "He" is John, "it" is the Ford. $\mathrm{Cf} = [\text{John}, \text{Ford}, \text{Bob}]$, $\mathrm{Cb} = \mathrm{Cp} = \text{John}$: continue.
- $U_3$ with "He" = John: $\mathrm{Cf} = [\text{John}, \text{Ford}]$, $\mathrm{Cb} = \mathrm{Cp} = \text{John}$, the same Cb: continue.
- $U_3$ with "He" = Bob: $\mathrm{Cf} = [\text{Bob}, \text{Ford}]$. The highest element of $\mathrm{Cf}(U_2)$ realized in $U_3$ is the Ford, so $\mathrm{Cb} = \text{Ford}$, while $\mathrm{Cp} = \text{Bob}$ and the Cb changed: rough shift.

Continue is preferred, so the algorithm resolves "He" to John, as a reader does.

The model can also prefer the wrong reading. In "Bob opened up a new dealership last week. John took a look at the Fords in his lot. He ended up buying one", $U_2$ has $\mathrm{Cb} = \text{Bob}$ (through "his") and $\mathrm{Cp} = \text{John}$. Resolving "He" to Bob in $U_3$ keeps Bob as Cb and Cp, a continue; resolving it to John changes the Cb to John, a smooth shift. The algorithm picks Bob, but a reader picks John. Jurafsky and Martin use this pair of texts to compare centering with the [Hobbs algorithm](/hobbs-algorithm/), which picks John.

## Relation to other models

- The [Hobbs algorithm](/hobbs-algorithm/) also prefers subjects and nearby sentences, but by a fixed walk of the parse trees, one pronoun at a time. Centering chooses the referents of all pronouns of an utterance together, by the transition they make.
- Salience methods, such as Lappin and Leass (1994), replace the single Cb by a numeric score per entity that adds weights for grammatical role and recency and decays with distance.
- Learned coreference models, such as the [mention-pair model](/mention-pair-model/) and the [span-ranking model](/span-ranking-coreference/), use features related to centering, such as the grammatical role and the distance of the candidate, but learn their weights from data.
- Global coherence models, such as [rhetorical structure theory](/rhetorical-structure-theory/), describe relations between larger parts of a text, such as cause and contrast. Centering describes only how adjacent utterances share entities; Grosz, Joshi and Weinstein place it inside a larger theory of discourse structure, where it works within one discourse segment.
- The entity grid of Barzilay and Lapata (Computational Linguistics, 2008) records, for each entity and each sentence, the grammatical role of the entity, and scores coherence by the frequencies of role transitions. It keeps the centering idea that role and continuity matter, but learns the preferences.
- Generation: centering also predicts when to use a pronoun, which matters for choosing referring expressions, the problem of the [incremental algorithm for referring expressions](/incremental-algorithm-referring-expressions/).

## Known results in the model

- The pronoun algorithm generates all anchors. If an utterance has $p$ pronouns with at most $c$ candidates each, there are up to $c^p$ anchors, so the time per utterance is exponential in $p$ (a theorem, by counting). Utterances have few pronouns, so this is small in practice.
- The four transitions are a complete classification: every pair of adjacent utterances with a defined Cb falls into exactly one cell of the table (a theorem, from the two yes or no questions).
- Rule 1 and Rule 2 are claims about the preferences of readers and writers, not theorems. Studies of corpora found that the parameters, such as what counts as an utterance and how to rank $\mathrm{Cf}$, change which transitions a text has (a measurement).
- Pronoun resolution: Tetreault (2001) compared centering algorithms and the Hobbs algorithm on news and fiction text and found that his left-right centering method, which searches the current utterance and then the previous ones in Cf order, did better than the algorithm of Brennan, Friedman and Pollard on his data (a measurement).
- Languages: Walker, Iida and Cote (1994) applied centering to Japanese, where zero pronouns play the role of English pronouns and the topic marker affects the ranking.

## References
