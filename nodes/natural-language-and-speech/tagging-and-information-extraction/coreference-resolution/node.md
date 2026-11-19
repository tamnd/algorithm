---
tag: 2AK9Q7
kind: problem
slug: coreference-resolution
name: Coreference resolution
aliases:
- coreference
- anaphora resolution
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Group the mentions in a text into clusters that refer to the same entity, such as a name, a description and a pronoun."
prereqs: [named-entity-recognition]
see_also: [mention-pair-model, span-ranking-coreference, hobbs-algorithm, centering-theory, b-cubed-metric, entity-linking, correlation-clustering, bell-numbers]
sources:
  - paper: doi:10.1162/089120101753342653
    title: "Wee Meng Soon, Hwee Tou Ng and Daniel Chung Yong Lim, A machine learning approach to coreference resolution of noun phrases, Computational Linguistics 27(4), 2001, pages 521 to 544"
    locator: the learned mention-pair model and its MUC-6 and MUC-7 results
  - paper: "Marc Vilain, John Burger, John Aberdeen, Dennis Connolly and Lynette Hirschman, A model-theoretic coreference scoring scheme, Proceedings of the Sixth Message Understanding Conference (MUC-6), 1995"
    title: Vilain et al. 1995
    locator: the MUC link-based recall and precision
  - paper: "Sameer Pradhan, Lance Ramshaw, Mitchell Marcus, Martha Palmer, Ralph Weischedel and Nianwen Xue, CoNLL-2011 shared task: modeling unrestricted coreference in OntoNotes, Proceedings of CoNLL 2011: Shared Task, pages 1 to 27"
    title: Pradhan et al. 2011
    locator: the OntoNotes coreference annotation, with no singleton mentions, and the official score
  - paper: "Sameer Pradhan, Alessandro Moschitti, Nianwen Xue, Olga Uryupina and Yuchen Zhang, CoNLL-2012 shared task: modeling multilingual unrestricted coreference in OntoNotes, Proceedings of the Joint Conference on EMNLP and CoNLL: Shared Task, 2012, pages 1 to 40"
    title: Pradhan et al. 2012
    locator: the English, Chinese and Arabic data and the official score, the mean of the MUC, B-cubed and CEAF-e F1 values
  - paper: doi:10.3115/v1/P14-2006
    title: "Sameer Pradhan, Xiaoqiang Luo, Marta Recasens, Eduard Hovy, Vincent Ng and Michael Strube, Scoring coreference partitions of predicted mentions: a reference implementation, ACL 2014, pages 30 to 35"
    locator: the reference scorer for MUC, B-cubed and CEAF with predicted mentions
  - paper: doi:10.1023/B:MACH.0000033116.57574.95
    title: "Nikhil Bansal, Avrim Blum and Shuchi Chawla, Correlation clustering, Machine Learning 56, 2004, pages 89 to 113"
    locator: the NP-hardness of correlation clustering on complete graphs with positive and negative edges
  - paper: doi:10.18653/v1/D17-1018
    title: "Kenton Lee, Luheng He, Mike Lewis and Luke Zettlemoyer, End-to-end neural coreference resolution, Proceedings of EMNLP 2017, pages 188 to 197"
    locator: the span-ranking model and its CoNLL-2012 English test results
---

Coreference resolution finds which expressions in a text refer to the same thing. In "Marie Curie moved to Paris. There she met Pierre Curie and married him", it groups "Marie Curie" with "she", "Paris" with "There", and "Pierre Curie" with "him". Each group is an entity, and the expressions are its mentions. The task joins the names found by [named entity recognition](/named-entity-recognition/) with descriptions ("the young student") and pronouns, so that later steps such as [relation extraction](/relation-extraction/) and [entity linking](/entity-linking/) see every place where an entity occurs. It is hard because the clues are spread over the text and sometimes need world knowledge, and because a decision about one pair of mentions limits the decisions about the others: the output must be a consistent grouping.

## In plain words

Underline every name, description and pronoun in a text. Then put underlined phrases into groups, so that the phrases in one group all talk about the same person, place or thing. A pronoun such as "she" usually goes with a person mentioned shortly before, of the same gender and number. A name repeated later ("Curie") goes with the earlier full name. A description ("the scientist") needs knowledge about the entity. The groups must be consistent: if A goes with B and B goes with C, then A goes with C. Phrases that talk about something mentioned only once stay alone.

## Definition

**Input.** A document of tokens $x_1, \ldots, x_n$. In the classic form, also the set $M$ of mentions, each a span $(i, j)$ in fencepost indices, so that $(i, j)$ covers the tokens $i + 1, \ldots, j$. In the end-to-end form the system finds the mentions itself.

**Output.** A partition of the mentions into clusters, one cluster per entity. A cluster with one mention is a singleton.

**Antecedent form.** Order the mentions by position. An equivalent output gives each mention $m$ either one earlier mention, its antecedent, or none. The links form a forest, and its trees are the clusters. Many forests give the same partition, so methods that predict antecedents must not be scored on the exact links.

**Coreference and anaphora.** An anaphor is an expression whose meaning depends on an earlier expression. Coreference and anaphora overlap but differ. Two full names can corefer with no anaphor ("Barack Obama ... Obama"). And an anaphor need not corefer with its antecedent: in "Every student brought his book", "his" depends on "every student" but does not refer to one fixed person, and in "I lost my pen and bought a new one", "one" does not refer to the lost pen. Coreference data sets mark only the identity relation.

**Score.** The data sets of the CoNLL-2011 and CoNLL-2012 shared tasks, from OntoNotes, are the usual benchmark. The official CoNLL score is the mean of the F1 values of three metrics (Pradhan et al. 2011, 2012):

- MUC (Vilain et al. 1995) counts the links needed to join each gold cluster, and ignores singletons.
- [B-cubed](/b-cubed-metric/) averages precision and recall over mentions.
- CEAF-e aligns gold and predicted clusters one to one with the best total similarity, an [assignment problem](/assignment-problem/) solved by the [Hungarian algorithm](/hungarian-algorithm/).

With predicted mentions, the gold and predicted partitions cover different sets, and the reference scorer of Pradhan et al. (2014) fixes how each metric handles this. OntoNotes does not mark singletons, so a system must also learn which mentions to leave out.

## Variants

- Pronoun resolution: find the antecedent of each third person pronoun only, as the [Hobbs algorithm](/hobbs-algorithm/) does.
- Entity coreference with given mentions, as in the MUC-6 and MUC-7 tasks, or end-to-end with mentions found by the system, as in CoNLL-2012.
- Event coreference: group the mentions of the same event, such as "the attack" and "it happened".
- Cross-document coreference: group mentions of the same entity across many documents; with a knowledge base this meets [entity linking](/entity-linking/).
- Bridging: link a mention to an earlier one that it is related to but not equal to, as "the door" to "a house".
- Commonsense pronoun tests: pairs of sentences that differ in one word and need world knowledge, in the style of Winograd's example "The city councilmen refused the demonstrators a permit because they feared violence", where "they" changes from the councilmen to the demonstrators if "feared" becomes "advocated".

## Examples

Tokens: "Marie Curie moved to Paris in 1891 . There the young Polish student met Pierre Curie . She married him in 1895 ." The mentions and gold clusters are:

| cluster | mentions (fencepost spans) |
|---|---|
| Marie Curie | "Marie Curie" $(0, 2)$, "the young Polish student" $(9, 13)$, "She" $(17, 18)$ |
| Paris | "Paris" $(4, 5)$, "There" $(8, 9)$ |
| Pierre Curie | "Pierre Curie" $(14, 16)$, "him" $(19, 20)$ |
| 1891 | "1891" $(6, 7)$, a singleton |
| 1895 | "1895" $(21, 22)$, a singleton |

A system that links "Pierre Curie" to "Marie Curie", because of the shared surname, merges the third cluster into the first. That is one wrong decision of a left-to-right linker, but it adds six wrong pairs of mentions, two times three.

Gender and number do not always decide: in "John told Bill that he had won", "he" can be either man, and readers use the context.

## Known algorithms

- Syntactic pronoun methods: the [Hobbs algorithm](/hobbs-algorithm/) walks parse trees in a fixed order (Hobbs 1978). A heuristic, and a strong baseline for pronouns.
- Discourse methods: the algorithm of Brennan, Friedman and Pollard (1987) picks the antecedents that give the most preferred transition of [centering theory](/centering-theory/). Salience methods, such as Lappin and Leass (1994), keep a score per entity that grows with each mention in a strong position and decays with distance.
- The [mention-pair model](/mention-pair-model/): a classifier decides for each pair whether it corefers, and a linker builds clusters. Soon, Ng and Lim (2001) report MUC F1 of 62.6 on MUC-6 and 60.4 on MUC-7 (measurements).
- Mention ranking and entity models: rank all candidate antecedents of a mention together, or compare a mention with the partial cluster built so far.
- Rule-based sieves: a sequence of deterministic passes from the most precise rule (exact string match) to the least precise (pronouns), each pass merging clusters.
- End-to-end span ranking: the [span-ranking model](/span-ranking-coreference/) of Lee et al. (2017) scores every span up to a width as a mention and ranks its antecedents, with no parser. It reached a CoNLL F1 of 67.2 with one model and 68.8 with an ensemble on the CoNLL-2012 English test set (measurements). Later models keep this design with pretrained encoders such as [BERT](/bert/).

## Bounds

- A set of $k$ mentions has $B_k$ partitions, the [Bell number](/bell-numbers/), and $k!$ antecedent forests, since mention $t$ has $t$ choices (none or one of the $t - 1$ earlier mentions). Both counts are theorems; both grow faster than $c^k$ for every constant $c$, so no method enumerates them.
- Scoring all pairs of $k$ mentions takes $O(k^2)$ classifier calls, and left-to-right linking with these scores takes $O(k^2)$ time (a theorem, by counting).
- Finding the partition that agrees best with signed pair scores is [correlation clustering](/correlation-clustering/), which is NP-hard (Bansal, Blum and Chawla 2004, a theorem). So exact global clustering from pair scores is intractable in the worst case, and systems use greedy linking, ranking or approximation.
- In the end-to-end form, a document of $n$ tokens has $O(n w)$ spans of width at most $w$, and $O(n^2 w^2)$ pairs of spans. Span-ranking models therefore prune the spans to $O(n)$ and keep at most a fixed number of antecedents per span.

## Reductions

- Coreference with pair scores reduces to [correlation clustering](/correlation-clustering/), or to [agglomerative clustering](/agglomerative-clustering/) with a stopping threshold.
- The antecedent form turns the clustering into one ranking decision per mention; the transitive closure of the links, computed with a [disjoint set](/disjoint-set/) structure, gives the clusters.
- Mention detection reduces to span classification, like nested [named entity recognition](/named-entity-recognition/), but with pronouns and descriptions as well as names.
- Cross-document coreference with a knowledge base reduces to [entity linking](/entity-linking/) plus clustering of the mentions linked to no entry.

## Applications

- Information extraction: relation and event extraction must know that "he" in one sentence is the person named in another.
- Question answering and reading comprehension: answers often sit in a sentence that uses only a pronoun for the entity asked about.
- Summarization: a summary that keeps a sentence with "she" must make sure the reader can tell who she is.
- Machine translation: the gender of a pronoun in the target language can depend on its antecedent.

## References
