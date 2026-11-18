---
tag: S34RXX
kind: model
slug: two-level-morphology
name: Two-level morphology
aliases:
- Koskenniemi two-level model
area: natural-language-and-speech/tokenization-and-text-normalization
level: core
summary: Koskenniemi's model in which parallel finite-state transducers relate lexical and surface forms, so a lexicon and rules give analysis and generation.
history:
  year: 1983
  people: [Kimmo Koskenniemi]
  note: Koskenniemi described the model in his 1983 thesis and in a COLING 1984 paper, with Finnish as the main test. Kaplan and Kay (1994) gave the theory of compiling such rules into finite-state transducers.
prereqs: [finite-state-transducer, morphological-analysis]
see_also: [product-construction, deterministic-finite-automaton, regular-language, trie, lemmatization, stemming, morfessor, dfa-minimization]
sources:
  - paper: "Kimmo Koskenniemi, Two-level morphology: a general computational model for word-form recognition and production, Publications No. 11, Department of General Linguistics, University of Helsinki, 1983"
    title: Koskenniemi 1983
    locator: the full description of the model and of Finnish morphology in it
  - paper: doi:10.3115/980491.980529
    title: Kimmo Koskenniemi, A general computational model for word-form recognition and production, COLING 1984, Stanford, pages 178 to 181
    locator: Section 2 (the cascade of Kay and Kaplan and the size of the merged automaton), Section 4 (the example lasiIA and laseja, rules 1' and 2'), Section 5 (rules as automata, the automaton 1'' and its table, the parallel rules), the two-level lexicon system (minilexicons), Section 6 (current status, about 0.05 CPU seconds per word)
  - url: https://aclanthology.org/J94-3001/
    title: Ronald M. Kaplan and Martin Kay, Regular models of phonological rule systems, Computational Linguistics 20(3), 1994, pages 331 to 378
    locator: rewrite rules and two-level rules as regular relations, same-length relations and their closure under intersection, and the compilation of rules into transducers
  - book: isbn:9781575864341
    title: Kenneth R. Beesley and Lauri Karttunen, Finite State Morphology, CSLI Publications, 2003
    locator: the two-level rule compiler and the lexical transducer that joins the lexicon and the rules
---

Two-level morphology is a model of word structure in which a word has exactly two representations: a lexical string, made of the morphemes as the lexicon lists them, and a surface string, the word as it is written or spoken. A set of rules states which lexical characters may correspond to which surface characters, and in which contexts. Each rule is a finite automaton over pairs of characters, and all rules run in parallel on the same pair string. Kimmo Koskenniemi introduced the model in 1983. Because the description only states a relation, the same lexicon and rules give both [morphological analysis](/morphological-analysis/) and generation.

## The machine

**Pairs.** Let $\Lambda$ be the lexical alphabet and $\Sigma$ the surface alphabet. A pair $a{:}b$ says that the lexical character $a$ is realized as the surface character $b$. A lexical string $l$ and a surface string $s$ of the same length correspond through the pair string $(l_1{:}s_1)(l_2{:}s_2) \cdots (l_n{:}s_n)$. In later two-level systems a pair may have a null on one side, so that a character can be inserted or deleted.

**Rules.** Each rule is a finite automaton that reads pairs. It accepts a pair string when the string satisfies the rule. Koskenniemi (1984) writes rules in the form

$$a{:}b \Leftrightarrow \text{left context} \;\_\_\; \text{right context},$$

which means: the lexical $a$ may be realized as $b$ only in this context, and in this context it must be realized as $b$. Both halves are needed. The first excludes $a{:}b$ elsewhere, and the second excludes the default pair $a{:}a$ in the context.

**Lexicon.** The lexicon is a finite-state network of morphemes. In Koskenniemi's system it is made of minilexicons: each entry gives a part of a stem or an ending and names the minilexicon that may follow, so stems with the same alternation share one set of endings.

**Correspondence.** A surface string $s$ is a correct form of the lexical string $l$ when $l$ is accepted by the lexicon and the pair string of $l$ and $s$ is accepted by every rule automaton at the same time. Rules have no order. They compare the two levels directly, and no intermediate string exists, even in principle.

**The example of the source.** The Finnish noun lasi "glass" has the partitive plural laseja. In the two-level description, its lexical string is lasiIA: the stem lasi, the plural morpheme I and the partitive ending A. The pair string is

| lexical | l | a | s | i | I | A |
|---|---|---|---|---|---|---|
| surface | l | a | s | e | j | a |

Three alternations happen: the stem-final i becomes e before the plural I, the plural I becomes j between vowels, and A becomes a by vowel harmony. Rule 1' of the source states the first one: $i{:}e \Leftrightarrow \_\_\; I{:}{=}$, where $=$ stands for any character. Its automaton 1'' has three states, with 1 and 2 accepting:

| state | i:e | i:= | I:= | =:= |
|---|---|---|---|---|
| 1 | 3 | 2 | 1 | 1 |
| 2 | 3 | 2 | 0 | 1 |
| 3 | 0 | 0 | 1 | 0 |

A 0 means that the automaton rejects. A column with a more specific pair applies before a column with $=$: the column i:= covers a lexical i with any surface character except e. A script that runs the table gives these results:

- lasiIA with laseja: the states 1, 1, 1, 1, 3, 1, 1; it ends in 1, so the rule accepts.
- lasiIA with lasija: the states 1, 1, 1, 1, 2 and then 0 at the pair I:j, because a lexical i before I must become e. The rule rejects.
- lasi with lase: the run ends in state 3, which does not accept, because i:e is allowed only before I. The rule rejects.

## What it counts

The model counts the size of a description: the number of rules $k$, the number of states of each rule automaton, and the size of the lexicon. For one word, it counts the steps of the automata: for a pair string of length $n$, each rule makes $n$ transitions, so checking a given pair string costs $O(k n)$ table lookups. In analysis the lexical side is unknown. The program then walks the lexicon and the $k$ rule automata together, one surface character at a time, and its cost depends on how many lexical choices stay open at each step.

## Relation to other models

- **Cascades of rewrite rules.** Generative phonology derives the surface form from the lexical form by a sequence of ordered rewrite rules. Kay and Kaplan observed that each such rule can be represented by a finite-state transducer, so the cascade is a cascade of transducers, and it can in principle be merged into one. Koskenniemi (1984, Section 2) noted that for a language such as Finnish the merged automaton seemed likely to grow prohibitively large, and proposed parallel rules instead of a cascade.
- **Finite-state transducers.** A two-level rule is a [finite-state transducer](/finite-state-transducer/) that reads the lexical and the surface character at the same time. The set of rules in parallel accepts the intersection of their pair languages, which the [product construction](/product-construction/) builds as one automaton.
- **Lexical transducers.** Beesley and Karttunen (2003) describe compiling the rules, intersecting them and composing the result with the lexicon into one transducer, the lexical transducer, which maps analyses to surface forms.
- **Unsupervised segmentation.** [Morfessor](/morfessor/) and [subword tokenization](/subword-tokenization/) split words without a lexicon or rules. They give segments, not features, and they do not model spelling changes.

## Known results in the model

- **Bidirectional (theorem).** The description defines a relation between lexical and surface strings, so the same lexicon and rules generate surface forms from lexical ones and analyze surface forms into lexical ones (Koskenniemi 1984).
- **Parallel rules are one automaton (theorem).** If the rules have $q_1, \ldots, q_k$ states, the strings that all of them accept are the strings accepted by their product, a finite automaton over pairs with at most $q_1 q_2 \cdots q_k$ states. So a two-level description defines a [regular language](/regular-language/) of pair strings.
- **Closure under intersection (theorem).** Regular relations in general are not closed under intersection. Same-length regular relations, which pair strings of equal length as two-level rules do when the null is treated as an ordinary symbol, are closed under intersection (Kaplan and Kay 1994). So the rules in parallel still define a regular relation.
- **Compilation (theorem).** Two-level rules and ordered rewrite rules both compile to finite-state transducers (Kaplan and Kay 1994).
- **Speed in 1984 (measurement).** Koskenniemi's PASCAL program took about 0.05 CPU seconds per word on the computers of the time, with no work on speed (Koskenniemi 1984, Section 6).
- **Coverage (measurement).** By 1984 there were two-level descriptions in progress or done for Finnish, English, Japanese, Rumanian, French, Swedish, Old Church Slavonic, Greek, Lappish and Arabic (Koskenniemi 1984, abstract).

## References

- Kimmo Koskenniemi. Two-level morphology: a general computational model for word-form recognition and production. Publications No. 11, Department of General Linguistics, University of Helsinki, 1983.
- Kimmo Koskenniemi. A general computational model for word-form recognition and production. COLING 1984, Stanford, pages 178 to 181. doi:10.3115/980491.980529.
- Ronald M. Kaplan and Martin Kay. Regular models of phonological rule systems. Computational Linguistics 20(3), 1994, pages 331 to 378. https://aclanthology.org/J94-3001/.
- Kenneth R. Beesley and Lauri Karttunen. Finite State Morphology. CSLI Publications, 2003. ISBN 9781575864341.
