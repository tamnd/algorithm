---
tag: JN05T5
kind: model
slug: semantic-network
name: Semantic network
aliases:
- semantic net
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: intro
summary: Represents knowledge as a graph whose nodes are concepts and individuals and whose labeled edges, such as is-a and has-part, are relations; properties are inherited along is-a.
prereqs: [graph, graph-reachability]
see_also: [frame-knowledge-representation, description-logic, ontology-knowledge-representation, concept-subsumption, structural-subsumption, nonmonotonic-reasoning, default-logic, transitive-closure]
sources:
  - paper: "M. Ross Quillian, Semantic memory, in Marvin Minsky (ed.), Semantic Information Processing, MIT Press, 1968, pages 227 to 270"
    locator: the memory model of word concepts as nodes joined by associative links, and the search that spreads from two nodes until the paths meet
  - paper: doi:10.1016/S0022-5371(69)80069-1
    title: Allan M. Collins and M. Ross Quillian, Retrieval time from semantic memory, Journal of Verbal Learning and Verbal Behavior 8(2), 1969, pages 240 to 247
    locator: the hierarchy with properties stored at the most general level, and the measured verification times that grow with the number of levels
  - paper: "William A. Woods, What's in a link: foundations for semantic networks, in Daniel G. Bobrow and Allan Collins (eds.), Representation and Understanding, Academic Press, 1975, pages 35 to 82"
    locator: the lack of a semantics for links in early networks, and the distinction between structural links and assertions (general locator)
  - paper: doi:10.1109/MC.1983.1654194
    title: Ronald J. Brachman, What IS-A is and isn't, an analysis of taxonomic links in semantic networks, Computer 16(10), 1983, pages 30 to 36
    locator: the many different relations that systems wrote as one is-a link (general locator)
  - paper: doi:10.1207/s15516709cog0902_1
    title: Ronald J. Brachman and James G. Schmolze, An overview of the KL-ONE knowledge representation system, Cognitive Science 9(2), 1985, pages 171 to 216
    locator: structured concepts with roles and a classifier that places a concept in the hierarchy (general locator)
  - paper: "Bart Selman and Hector J. Levesque, The complexity of path-based defeasible inheritance, Artificial Intelligence 62(2), 1993, pages 303 to 339"
    locator: NP-hardness results for path-based inheritance with exceptions (general locator)
---

A semantic network represents knowledge as a directed [graph](/graph/): nodes stand for concepts (classes) and individuals, and each edge has a label that names a relation, such as *is-a*, *instance-of* or *has-part*. Its main inference is inheritance: a node gets the properties of every node it reaches by is-a edges. This page treats the network as a model of reasoning, with a syntax, a meaning for the links and the cost of its queries. The [frame](/frame-knowledge-representation/) page groups the edges of one node into a record of slots, and the [description logic](/description-logic/) page gives the formal language that grew out of the attempt to fix the meaning of the links.

## The machine

**Syntax.** A network is a finite set of nodes, split into concept nodes and individual nodes, and a finite set of labeled edges $(a, r, b)$. Three kinds of labels are usual:

- $(A, \textit{is-a}, B)$ between concepts: every $A$ is a $B$;
- $(i, \textit{instance-of}, A)$ from an individual to a concept: $i$ is an $A$;
- $(A, r, B)$ for any other role $r$, such as *has-part* or *color*: an $A$ has an $r$ that is a $B$.

**Semantics.** Early networks gave the links no fixed meaning, which Woods (1975) showed to be their main weakness. One reading, the one that [description logics](/description-logic/) adopted, translates each edge into first-order logic, with a unary predicate for each concept and a binary predicate for each role:

| edge | first-order reading |
|---|---|
| $(A, \textit{is-a}, B)$ | $\forall x\, (A(x) \rightarrow B(x))$ |
| $(i, \textit{instance-of}, A)$ | $A(i)$ |
| $(A, r, B)$ | $\forall x\, (A(x) \rightarrow \exists y\, (r(x, y) \wedge B(y)))$ |

Under this reading the network is a set of axioms, and a question is answered by entailment from them. A second reading treats role edges as defaults: "a bird can fly" holds for a bird unless a more specific node says otherwise. This reading is not first-order, and it belongs to [nonmonotonic reasoning](/nonmonotonic-reasoning/).

**Example.** Take the nodes *animal*, *bird*, *canary*, *penguin* and the individual *tweety*, with the edges (bird, is-a, animal), (canary, is-a, bird), (penguin, is-a, bird), (tweety, instance-of, penguin), (animal, has, skin), (bird, has-part, wings), (bird, can, fly), (canary, can, sing) and the exception (penguin, cannot, fly). Stored this way, each property is written once, at the most general node to which it applies, as in Collins and Quillian (1969).

## What it counts

The model answers three kinds of questions:

- **Subsumption:** is every $A$ a $B$? Under the strict reading this is the question whether $B$ is reachable from $A$ by is-a edges.
- **Instance checking:** is $i$ an $A$? Follow the instance-of edge from $i$ and ask whether $A$ is reachable from one of its concepts.
- **Inherited properties:** which role edges hold for $A$? Take the role edges of every node reachable from $A$ by is-a edges.

In the example, *tweety* is an animal and has skin and wings. With defaults, the edge (penguin, cannot, fly) is more specific than (bird, can, fly), because penguin is below bird, so the network concludes that *tweety* cannot fly. Without defaults, the two edges give a contradiction, and the strict reading has to drop (bird, can, fly) in favour of a weaker axiom.

## Relation to other models

- **[Frames](/frame-knowledge-representation/)** store the same information grouped by node: the role edges that leave a node become the slots of its frame, and the is-a edge becomes its parent.
- **[Description logics](/description-logic/)** are the formal successor. The KL-ONE system (Brachman and Schmolze 1985) gave each concept a structured definition from roles and other concepts, and a classifier that computes the is-a edges from these definitions instead of taking them as given. The third row of the table above is the description logic axiom $A \sqsubseteq \exists r.B$.
- **[Ontologies](/ontology-knowledge-representation/)** in the modern sense are often drawn as semantic networks but written in a description logic, so the drawing has a fixed meaning.
- **Logic programs.** The strict reading fits in [Horn clauses](/horn-clause/): $B(x) \leftarrow A(x)$ for each is-a edge, so inheritance is [forward chaining](/forward-chaining/). The existential in the third row does not fit in Horn clauses without new constants.

## Known results in the model

- **Strict inheritance is graph reachability.** Under the first-order reading, with only is-a and instance-of edges, $A$ is subsumed by $B$ if and only if there is a directed path from $A$ to $B$. One query is a [breadth-first search](/breadth-first-search/) in $O(V + E)$ time for $V$ nodes and $E$ edges, and all queries together follow from the [transitive closure](/transitive-closure/) of the is-a edges. Role edges of the form $A \sqsubseteq \exists r.B$ do not add new is-a consequences between named concepts, so the same bound holds for the inherited properties.
- **Defeasible inheritance can be hard.** With exceptions, there are several competing definitions of which paths count, and conflicts such as two parents with opposite defaults leave the answer open. Selman and Levesque (1993) showed that some of these path-based definitions give NP-hard questions.
- **The is-a link is overloaded.** Brachman (1983) listed the different relations that systems wrote as one is-a link, such as the subset relation between two classes and the membership of an individual in a class, and argued that mixing them gives wrong inheritance.
- **Retrieval time in people.** Collins and Quillian (1969) measured that people take longer to verify a property stored more levels up in such a hierarchy, for example "a canary has skin" against "a canary can sing". This is a measurement on people, not a property of the model.

## References
