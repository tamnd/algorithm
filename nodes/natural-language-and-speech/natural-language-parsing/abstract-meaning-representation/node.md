---
tag: 9CXJWG
kind: definition
slug: abstract-meaning-representation
name: Abstract meaning representation
aliases:
- AMR graph
area: natural-language-and-speech/natural-language-parsing
level: advanced
summary: A rooted, directed, labeled graph of concepts and relations that captures who did what to whom in a sentence, abstracting from syntax.
history:
  year: 2013
  people: [Laura Banarescu, Claire Bonial, Shu Cai, Madalina Georgescu, Kira Griffitt, Ulf Hermjakob, Kevin Knight, Philipp Koehn, Martha Palmer, Nathan Schneider]
  note: "Banarescu and others defined AMR for a large sembank of English sentences, using PropBank framesets for predicates and the PENMAN notation for graphs, and measured agreement between annotators with Smatch."
prereqs: [semantic-role-labeling, semantic-network]
see_also: [smatch, semantic-parsing, dependency-tree, frame-knowledge-representation, coreference-resolution, directed-acyclic-graph, natural-language-inference, description-logic]
sources:
  - paper: "Laura Banarescu, Claire Bonial, Shu Cai, Madalina Georgescu, Kira Griffitt, Ulf Hermjakob, Kevin Knight, Philipp Koehn, Martha Palmer and Nathan Schneider, Abstract Meaning Representation for Sembanking, Proceedings of the 7th Linguistic Annotation Workshop and Interoperability with Discourse, 2013, 178-186"
    title: "Laura Banarescu et al., Abstract Meaning Representation for Sembanking"
    locator: "the format of AMR (concepts, PropBank framesets, relations, inverse relations and reentrancy), the PENMAN notation, the limitations of AMR, and the agreement measured with Smatch"
  - paper: "Martha Palmer, Daniel Gildea and Paul Kingsbury, The Proposition Bank: an annotated corpus of semantic roles, Computational Linguistics 31(1), 71-106, 2005"
    title: "Martha Palmer, Daniel Gildea and Paul Kingsbury, The Proposition Bank"
    locator: "the framesets and numbered arguments that AMR uses for predicates"
  - paper: "Shu Cai and Kevin Knight, Smatch: an Evaluation Metric for Semantic Feature Structures, Proceedings of ACL 2013 (Volume 2: Short Papers), 748-752"
    title: "Shu Cai and Kevin Knight, Smatch: an Evaluation Metric for Semantic Feature Structures"
    locator: "Section 2, AMR graphs as sets of triples"
---

An abstract meaning representation (AMR) is a rooted, directed graph with labeled nodes and edges that states the meaning of a sentence: its nodes are concepts such as events and entities, and its edges are the relations between them, such as who did what to whom. It abstracts from syntax, so sentences with different words and structure but the same meaning, such as an active sentence and its passive, get the same graph. A node can have more than one parent, which is how AMR shows that one entity plays roles in several events. AMR is the target of [semantic parsing](/semantic-parsing/) into graphs, and two AMRs are compared with [Smatch](/smatch/).

## Definition

Fix a set $C$ of concepts, a set $L$ of relation labels and a set $K$ of constants (strings, numbers and the symbol $-$). An AMR is a tuple $(V, r, \mathrm{concept}, E)$ where

- $V$ is a finite set of variables, one for each node,
- $r \in V$ is the root, which is the main focus of the sentence,
- $\mathrm{concept} : V \to C$ gives each node its concept,
- $E \subseteq V \times L \times (V \cup K)$ is a set of labeled edges, from a variable to a variable or to a constant,

and every node is reachable from the root by edges. The concepts are of three kinds: framesets of PropBank for events and states, such as `want-01` or `go-01`, with the sense number after the hyphen; English lemmas for entities, such as `boy`; and special concepts such as `and`, `name`, `date-entity` and `have-org-role-91`. The labels include the numbered arguments `:ARG0` to `:ARG5` of the frameset, whose meaning the frameset defines in the style of [semantic role labeling](/semantic-role-labeling/), and general relations such as `:mod`, `:location`, `:time`, `:polarity`, `:quant`, `:name` and `:op1`, `:op2`, and so on for the parts of a name or the members of a list.

**Notation.** AMRs are written in PENMAN notation. A node is `(v / c ...)`, with the variable $v$ and the concept $c$, followed by its outgoing edges as `:label value`. A value is a new node in parentheses, a variable already introduced, which makes a reentrancy, or a constant. A label with the suffix `-of` is an inverse edge: `(b / boy :ARG0-of (w / want-01))` is the same edge as `(w / want-01 :ARG0 (b / boy))`. Inverse edges let the notation keep a chosen node as the root while still writing the graph as one nested expression.

**Triples.** An AMR is the same as a set of triples: `instance(v, c)` for each node, `label(v, w)` for each edge between variables and `label(v, k)` for each edge to a constant. This is the form that [Smatch](/smatch/) compares. The variable names carry no meaning, so two AMRs are the same if a renaming of variables maps one set of triples onto the other.

## Examples and non-examples

**Control and reentrancy.** "The boy wants to go":

```
(w / want-01
   :ARG0 (b / boy)
   :ARG1 (g / go-01
            :ARG0 b))
```

The boy is the wanter, `:ARG0` of `want-01`, and the goer, `:ARG0` of `go-01`. The second mention is the variable `b` again, so the node `b` has two parents. The graph is not a tree. Its triples are `instance(w, want-01)`, `instance(b, boy)`, `instance(g, go-01)`, `ARG0(w, b)`, `ARG1(w, g)` and `ARG0(g, b)`.

**Abstraction from syntax.** "The boy saw the girl" and "The girl was seen by the boy" both have the AMR `(s / see-01 :ARG0 (b / boy) :ARG1 (g / girl))`. Voice, word order and function words do not appear.

**Negation and names.** "Kim does not want to go" adds `:polarity -` to `want-01` and replaces the boy by `(p / person :name (n / name :op1 "Kim"))`. The constant `-` and the string `"Kim"` are leaves that are not variables.

**Focus with an inverse role.** "The boy who wants to go" has the boy as its focus, so the root is the boy: `(b / boy :ARG0-of (w / want-01 :ARG1 (g / go-01 :ARG0 b)))`. The edge set is the same as in the first example; only the root differs.

**Non-example: a dependency tree.** A [dependency tree](/dependency-tree/) has one node for each word, syntactic labels such as subject and object, and exactly one parent for each word. In "The boy wants to go" it attaches "boy" only to "wants". AMR drops "the" and "to", uses frames instead of words, and gives the boy a second parent.

**Non-example: a logical form with scope.** AMR does not fix the scope of quantifiers. "Every boy wants a girl" gets one AMR, while a logical form must choose whether there is one girl or one for each boy.

**Non-example: tense, number and articles.** In the AMR guidelines described by Banarescu and others, the graph does not record tense, singular or plural, or definite and indefinite articles. "The boy wanted to go" and "Boys want to go" get the same AMR as the first example.

**Non-example: an alignment.** An AMR does not say which word produced which node. Parsers that need such a link must infer it, and evaluation with Smatch does not use it.

## Related definitions

- **Semantic network.** AMR is a [semantic network](/semantic-network/) for a single sentence, with a root and a fixed inventory of concepts and relations. Its concepts and roles resemble the slots of a [frame](/frame-knowledge-representation/).
- **Semantic roles.** The numbered arguments of an AMR predicate are the PropBank roles that [semantic role labeling](/semantic-role-labeling/) finds. Semantic role labeling marks spans of the sentence and stops there; AMR adds entity types, coreference within the sentence, negation, modality and named entities, and drops the link to the words.
- **Coreference.** A reentrancy is coreference inside one sentence. Links across sentences, as in [coreference resolution](/coreference-resolution/), need a multi-sentence extension.
- **Smatch.** The similarity of two AMRs is the F1 of matching triples under the best renaming of variables, defined on the [Smatch](/smatch/) page.
- **AMR parsing and generation.** AMR parsing maps a sentence to its AMR, a case of [semantic parsing](/semantic-parsing/). AMR-to-text generation goes the other way. Because AMR drops tense and articles, generation has to choose them.

## References
