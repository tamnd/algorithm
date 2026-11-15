---
tag: TXE1ST
kind: model
slug: frame-knowledge-representation
name: Frame (knowledge representation)
aliases:
- Minsky frames
- frame-based representation
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: intro
summary: A record for a stereotyped object or situation with named slots, default fillers and attached procedures, placed in an is-a hierarchy from which slots are inherited.
prereqs: [semantic-network]
see_also: [description-logic, ontology-knowledge-representation, production-system, default-logic, nonmonotonic-reasoning, structural-subsumption, frame-problem, tbox-and-abox]
sources:
  - paper: "Marvin Minsky, A framework for representing knowledge, MIT Artificial Intelligence Laboratory, AI Memo 306, 1974, hdl:1721.1/6089; reprinted in Patrick H. Winston (ed.), The Psychology of Computer Vision, McGraw-Hill, 1975, pages 211 to 277"
    locator: frames as data structures for stereotyped situations, with terminals filled by default assignments that later evidence can replace (general locator)
  - paper: doi:10.1515/9783110858778-005
    title: Patrick J. Hayes, The logic of frames, in Dieter Metzing (ed.), Frame Conceptions and Text Understanding, Walter de Gruyter, 1979, pages 46 to 61
    locator: the reading of frames and slots as first-order predicates and relations, with defaults as the part that is not first-order (general locator)
  - paper: doi:10.1145/4284.4285
    title: Richard Fikes and Tom Kehler, The role of frame-based representation in reasoning, Communications of the ACM 28(9), 1985, pages 904 to 920
    locator: frames, slots and facets, inheritance of slot values, attached procedures, and the combination of frames with rules in KEE (general locator)
  - paper: doi:10.1207/s15516709cog0902_1
    title: Ronald J. Brachman and James G. Schmolze, An overview of the KL-ONE knowledge representation system, Cognitive Science 9(2), 1985, pages 171 to 216
    locator: structured concepts with roles and restrictions, a frame-like language with a classifier (general locator)
---

A frame is a record that describes a stereotyped object or situation, such as a bird, a room or a birthday party. It has a name, a parent in an is-a hierarchy, and named *slots*. Each slot holds a value, or a default that holds unless something more specific is known, or a procedure that computes the value on demand. Minsky (1974) proposed frames as a way to bring a whole package of expectations to a new situation at once. A [semantic network](/semantic-network/) stores the same kind of knowledge as separate edges; a frame groups the edges of one node into one record and adds defaults and procedures. A frame in this sense has nothing to do with the [frame problem](/frame-problem/), which is about the effects of actions.

## The machine

**Syntax.** A frame system is a set of frames. Each frame has

- a name, and a flag that says whether it is a *class* frame or an *instance* frame;
- one or more parents: an instance frame has instance-of parents, and a class frame has is-a parents;
- a set of slots. Each slot has *facets*: a value, a default, a type restriction on the filler (often another class frame), a number restriction, and attached procedures, such as *if-needed* (run when the value is asked for and missing) and *if-added* (run when a value is stored).

Fikes and Kehler (1985) describe this structure, with slots and facets, as it appears in the KEE system.

**Semantics.** Hayes (1979) argued that most of a frame system is a notation for first-order logic. A class frame $C$ is a unary predicate; a slot $s$ is a binary relation; an is-a parent $D$ gives $\forall x\, (C(x) \rightarrow D(x))$; a type restriction $T$ on $s$ gives $\forall x\, \forall y\, (C(x) \wedge s(x, y) \rightarrow T(y))$; a slot value $v$ on an instance $i$ gives $s(i, v)$. Two parts do not fit this reading: defaults, which can be withdrawn and so are [nonmonotonic](/nonmonotonic-reasoning/), and attached procedures, which are programs.

**Lookup.** The basic query asks for the value of slot $s$ of frame $f$:

1. if $f$ has a stored value for $s$, return it;
2. else if $f$ or an ancestor has an if-needed procedure for $s$, run the nearest one and return its result;
3. else return the default of $s$ in the nearest ancestor that has one.

"Nearest" means the first in the order in which the ancestors are searched. With one parent per frame the ancestors form a chain and the order is clear.

**Example.**

| frame | parent | slots |
|---|---|---|
| Animal | | covering: default skin |
| Bird | is-a Animal | legs: 2; locomotion: default fly; covering: default feathers |
| Penguin | is-a Bird | locomotion: default walk and swim |
| Tweety | instance-of Penguin | birth-year: 2020; age: if-needed (current year minus birth-year) |

The value of locomotion for Tweety is "walk and swim", from Penguin, because Penguin is nearer than Bird. Legs is 2, inherited from Bird. Covering is "feathers": the default of Bird overrides the default of Animal. Age is computed when it is asked for.

## What it counts

The model answers slot queries, the value of slot $s$ of frame $f$, and the subsumption question whether one class frame is below another. Under the reading of Hayes, a slot query without defaults and procedures asks which values $v$ make $s(f, v)$ follow from the axioms, and subsumption asks whether $\forall x\, (C(x) \rightarrow D(x))$ follows. With defaults, the answer is the value that the most specific frame gives, and later knowledge can change it, so the consequence relation is nonmonotonic.

## Relation to other models

- **[Semantic networks](/semantic-network/)** hold the same facts as edges. A frame is the set of edges that leave one node.
- **[Description logics](/description-logic/)** came out of frame languages. KL-ONE (Brachman and Schmolze 1985) gave each class frame a definition from roles and restrictions and computed the is-a hierarchy from the definitions with a classifier. Description logics keep the first-order part and drop defaults and procedures. The type restriction above is the axiom $C \sqsubseteq \forall s.T$, and the class frames and the instance frames correspond to the [TBox and ABox](/tbox-and-abox/).
- **Rules.** KEE and other systems combined frames with [production rules](/production-system/): rules match on slot values, and their actions store slot values.
- **Classes in programming languages** also have fields, defaults and methods, and inherit them from a parent. A frame differs in that a slot can carry constraints and defaults that the system reasons with, not only a stored value.
- **[Default logic](/default-logic/)** gives a formal reading of slot defaults: a default $d$ for slot $s$ of $C$ is the default rule "if $C(x)$ and it is consistent that $s(x, d)$, then $s(x, d)$".

## Known results in the model

- **The first-order part is first-order logic.** By the translation of Hayes (1979), frames without defaults and procedures say nothing that first-order logic cannot say; they are a way to organize it. The questions of the first-order part therefore have the cost of the logic that the slots express, and the [description logic](/description-logic/) pages give these costs for the usual fragments.
- **Lookup with one parent is a walk up a chain.** A slot query visits at most $h + 1$ frames for a hierarchy of height $h$, with constant work for each frame if the slots are kept in a hash table.
- **Multiple inheritance needs a rule for conflicts.** If Nixon is both a Quaker, with the default pacifist, and a Republican, with the default not pacifist, the lookup above depends on the search order. Nonmonotonic logics treat this case as two competing conclusions, and frame systems choose an order of the parents or report the conflict.
- **Procedures remove all bounds.** An if-needed procedure is an arbitrary program, so a slot query in general has no time bound and need not terminate.

## References
