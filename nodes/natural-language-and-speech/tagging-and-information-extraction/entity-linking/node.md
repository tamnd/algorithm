---
tag: Y009F8
kind: problem
slug: entity-linking
name: Entity linking
aliases:
- named entity disambiguation
- wikification
area: natural-language-and-speech/tagging-and-information-extraction
level: core
summary: "Map each entity mention in a text to its entry in a knowledge base, or to none, using the mention, its context and coherence."
prereqs: [named-entity-recognition, word-sense-disambiguation]
see_also: [coreference-resolution, relation-extraction, personalized-pagerank, tf-idf, cosine-similarity, maximum-cut, inverted-index, bert]
sources:
  - paper: "Razvan Bunescu and Marius Paşca, Using encyclopedic knowledge for named entity disambiguation, Proceedings of EACL 2006"
    title: Bunescu and Paşca 2006
    locator: the use of Wikipedia articles, redirects and disambiguation pages as the knowledge base, and the ranking of candidates by context similarity
  - paper: "Rada Mihalcea and Andras Csomai, Wikify! Linking documents to encyclopedic knowledge, Proceedings of CIKM 2007"
    title: Mihalcea and Csomai 2007
    locator: the task of linking the important phrases of a document to Wikipedia articles
  - paper: "David Milne and Ian H. Witten, Learning to link with Wikipedia, Proceedings of CIKM 2008"
    title: Milne and Witten 2008
    locator: the commonness prior from anchor texts, the link-based relatedness and the learned disambiguation
  - paper: "Lev Ratinov, Dan Roth, Doug Downey and Mike Anderson, Local and global algorithms for disambiguation to Wikipedia, Proceedings of ACL 2011, pages 1375 to 1384"
    title: Ratinov et al. 2011
    locator: the split into local and global scores, and the use of a first local pass to approximate the global problem
---

Entity linking decides which real-world entity each name in a text refers to, by mapping the name to an entry of a knowledge base such as Wikipedia, or to NIL when the knowledge base has no entry for it. It is the step after [named entity recognition](/named-entity-recognition/): recognition says that "Jordan" is a person, linking says which person. The problem is like [word sense disambiguation](/word-sense-disambiguation/), with the entries of the knowledge base as the senses, but the set of senses is huge and open, and names have many surface forms ("NYC", "New York City", "the Big Apple"). Systems use three kinds of evidence: how often a name refers to each entity, how well the entity fits the words around the mention, and whether the entities chosen for a document fit together.

## In plain words

You read "Jordan played for Chicago in 1991". Which Jordan, and which Chicago? A list of names collected from links in Wikipedia says which articles a name usually points to: "Jordan" most often means the country or the basketball player, "Chicago" most often the city. The words around the name help: "played" fits a sportsman. And the choices must make sense together: Michael Jordan and the Chicago Bulls belong together, so here "Chicago" means the team, not the city. If no article fits, the answer is "not in the knowledge base".

## Definition

**Input.** A document $D$; a set of mentions $m_1, \ldots, m_k$ in $D$, each a span of tokens (or, in the end-to-end form, no mentions, which the system must find); and a knowledge base: a set $E$ of entities, each with names, a description and links to other entities.

**Output.** For each mention $m_i$, an entity $e_i \in E \cup \{\mathrm{NIL}\}$. NIL means that the entity is not in the knowledge base.

**Common decomposition.** (1) Candidate generation: a dictionary of surface forms, built from article titles, redirects, disambiguation pages and the anchor texts of links, gives a short candidate list $C(m) \subseteq E$ for each mention, often with a prior $p(e \mid m)$, the share of links with text $m$ that point to $e$. (2) Local ranking: a score $\phi(m, e)$ from the prior and from the similarity of the mention's context to the entity's description. (3) Global coherence: a score $\psi(e, e')$ for each pair of chosen entities, from their links or types. A global system picks

$$\arg\max_{e_1 \in C(m_1), \ldots, e_k \in C(m_k)} \; \sum_i \phi(m_i, e_i) + \sum_{i < j} \psi(e_i, e_j).$$

**Score.** Accuracy over mentions when the mentions are given; precision, recall and F1 over (span, entity) pairs in the end-to-end form. In-KB accuracy counts only mentions whose gold entity is in $E$.

## Variants

- Named entity disambiguation: only the named entities of the text, with given spans.
- Wikification: link every important phrase, including common nouns such as "jazz", to a Wikipedia article. Mihalcea and Csomai introduced the word for this task.
- End-to-end linking: find the mentions and link them together.
- NIL clustering: group the NIL mentions that refer to the same new entity, as in the knowledge base population tasks of the Text Analysis Conference.
- Linking to other knowledge bases: Wikidata, domain ontologies of genes, drugs or products; zero-shot linking to entities seen only through their descriptions.
- Cross-lingual linking: a mention in one language, a knowledge base in another.

## Examples

"Jordan played for Chicago in 1991." Candidates: Jordan → {Jordan (country), Michael Jordan, Jordan River, ...}, Chicago → {Chicago (city), Chicago Bulls, Chicago (musical), ...}. The prior alone picks the country and the city. The context word "played" moves Jordan to Michael Jordan. Coherence then moves Chicago to the Chicago Bulls, since the two articles link to each other. Ratinov et al. (2011) call the first two steps local and the last global.

"Paris Hilton visited Paris." The two mentions with the same text link to different entities; a system that links each string once per document fails here.

A NIL case: in a local news story, "John Smith, a teacher at the high school" is a person who has no Wikipedia article; the right output is NIL, even though the knowledge base has many entries named John Smith.

## Known algorithms

- Prior only: link each mention to its most frequent target. A strong baseline on news text, because most names usually mean their most common entity (a measurement, true of the common data sets).
- Context similarity: rank candidates by the [cosine similarity](/cosine-similarity/) of [tf-idf](/tf-idf/) vectors of the mention's context and the entity's article, with a classifier or ranker trained on Wikipedia's own links (Bunescu and Paşca 2006).
- Learned local and global features: Milne and Witten (2008) combine the prior with a relatedness of the candidate to the unambiguous mentions of the document, measured by shared incoming links. Ratinov et al. (2011) first rank locally, then use the top local choices of the other mentions as the context for the global features.
- Graph methods: build a graph of mentions and candidates and rank the candidates by a random walk, such as [personalized PageRank](/personalized-pagerank/), or find a dense subgraph with one entity per mention.
- Neural bi-encoders and cross-encoders: encode the mention in context and the entity description with a [transformer](/transformer/) such as [BERT](/bert/); retrieve candidates by nearest neighbor search over entity vectors, then rerank the top few with a model that reads both together.

## Bounds

- Candidate lookup: with a hash table or an [inverted index](/inverted-index/) of surface forms, each lookup costs time proportional to the length of the mention and of the list it returns.
- Local linking: $O(k c d)$ time for $k$ mentions with at most $c$ candidates each and $d$ features per pair; each mention is decided alone.
- Global linking is NP-hard in general (a theorem). Reduction from [maximum cut](/maximum-cut/): for a graph, make one mention per vertex with two candidates, 0 and 1, set $\phi = 0$, and for each edge $\{u, v\}$ let $\psi = 1$ when the two mentions take different candidates and 0 otherwise. The best assignment is a maximum cut. So exact global linking takes time exponential in $k$ in the worst case ($c^k$ by enumeration), and systems use approximations: a local first pass, greedy or iterative updates, or loopy belief propagation.
- If the coherence terms form a chain, such as only between adjacent mentions, dynamic programming finds the best assignment in $O(k c^2)$ time (a theorem, as for the [Viterbi algorithm](/viterbi-algorithm/)).

## Reductions

- Entity linking generalizes [word sense disambiguation](/word-sense-disambiguation/): the knowledge base is the sense inventory, and the prior is the most frequent sense.
- With given mentions and NIL treated as one more candidate, local linking is a ranking problem over a candidate list per mention.
- [Coreference resolution](/coreference-resolution/) and linking help each other: mentions in one coreference chain link to the same entity, and NIL clustering is cross-document coreference of the NIL mentions.
- Entity linking is a step of [relation extraction](/relation-extraction/) for knowledge base population and of [distant supervision](/distant-supervision/), which needs to know which entity pair a sentence mentions.

## Applications

- Knowledge base population: add facts read from text to the right entries.
- Semantic search: retrieve documents about an entity, not about a string.
- Question answering over knowledge bases: map the names in a question to entities.
- Distant supervision for relation extraction: match the entity pairs of a knowledge base to sentences.

## References
