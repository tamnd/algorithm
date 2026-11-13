---
tag: S4GYZ6
kind: problem
slug: persistent-naming-problem
name: Persistent naming problem
aliases:
- topological naming problem
area: cad/solid-modeling
level: research
summary: Name the faces and edges of a parametric model so that a feature that refers to them still finds the right ones after the history is edited and replayed.
prereqs: [feature-based-modeling, boundary-representation]
see_also: [feature-recognition, maximum-common-subgraph, graph-isomorphism-problem, geometric-constraint, variational-geometry, euler-operators, blending-surface, solid-boolean-operations]
sources:
  - paper: "Jiri Kripac, A mechanism for persistently naming topological entities in history-based parametric solid models, Computer-Aided Design 29(2), 113 to 122, 1997"
    locator: the whole paper (the topological ID system, which names faces by the feature that made them and names edges and vertices by their faces, and the matching of names after a replay)
  - paper: "Vasilis Capoyleas, Xiangping Chen and Christoph M. Hoffmann, Generic naming in generative, constraint-based design, Computer-Aided Design 28(1), 17 to 26, 1996"
    locator: the whole paper (names built from the operation that creates an entity and the entities it is made from, with extra terms to tell apart entities that split)
  - paper: "Xiangping Chen and Christoph M. Hoffmann, Towards feature attachment, Computer-Aided Design 27(9), 695 to 702, 1995"
    locator: the whole paper (how a feature refers to entities of the model built before it, and what happens to these references when the model is regenerated)
  - paper: "David Marcheix and Guy Pierra, A survey of the persistent naming problem, Proceedings of the Seventh ACM Symposium on Solid Modeling and Applications, 13 to 22, 2002"
    locator: the whole survey (the statement of the problem, the classes of naming methods and their known failures)
---

The persistent naming problem asks how a feature in a history-based model should refer to a face, an edge or a vertex of the model built before it, so that the reference still means the same entity after an earlier feature is edited and the history is replayed. The [boundary representation](/boundary-representation/) is computed again at each replay, and its entities are new objects, so a reference cannot be a pointer or an index. It must be a *name* that is computed from how the entity was made, and a rule that finds the entity with that name in the new model. The problem has no single formal statement, because "the same entity" in two different models is a matter of design intent, which the model does not hold. Kripac, Capoyleas, Chen and Hoffmann, and the survey of Marcheix and Pierra give the usual formulations.

## In plain words

A designer makes a block, then rounds one of its edges. The program must remember which edge. It cannot remember "edge number 7", because after the designer changes the block, the program builds all the edges again and numbers them in a new order.

So the program needs a way to describe the edge that still works after the change, like "the edge between the top face and the front face of the block". Then it can find that edge again in the new block.

This is hard when the change alters the shape a lot. The edge may be cut in two by a new slot, or it may disappear. Then it is not clear which edge the designer meant, and different programs give different answers.

## Definition

The following is the most precise version in common use. No standard formal statement exists, and the authors cited here differ in the details.

**Input.**

- A history $h = (f_1, \dots, f_m)$ of features, as in [feature-based modeling](/feature-based-modeling/). Replaying it gives models $M_0 = \emptyset, M_1, \dots, M_m$, where $M_i$ is the B-rep after feature $f_i$.
- For each feature $f_j$, a list of references to entities of $M_{j - 1}$: the faces a hole starts on, the edges a fillet rounds, the face a sketch lies on.
- An edit, which changes the parameters of some features, or inserts, deletes or reorders features, and gives a new history $h'$ with models $M'_i$.

**Output.**

- A naming scheme: a function $\mathrm{name}_i$ that maps each entity $e$ of $M_i$ to a name computed only from $h$ and the replay, not from memory addresses or the order in which a kernel happens to build the entities.
- A resolution rule: a function that maps a name and a model $M'_i$ to one entity, to a set of entities, or to the report that no entity has the name. Each reference of $f'_j$ is resolved in $M'_{j - 1}$.

**Constraints.**

- *Persistence.* When the edit does not change the topology of $M_i$, every name resolves to the entity in $M'_i$ that has the same role.
- *Splits and merges.* When an entity of $M_i$ becomes several entities of $M'_i$, or several become one, the resolution must say so, rather than choose one at random.
- *Failure.* When no entity of $M'_i$ corresponds, the resolution must report failure, rather than pick another entity.
- *Determinism.* Two replays of the same history must give the same names.

What "the same role" and "corresponds" mean is the hard part. The common reading is generative: an entity of $M'_i$ corresponds to an entity of $M_i$ when the same feature operation made both, from entities that correspond in turn, for example the side face that an extrusion sweeps from the same line of its sketch. This defines a relation between the entities of $M_i$ and $M'_i$, one to one when the topology does not change and one to many or many to one when it does. It does not decide every case, because a generative history can make the same entity in several ways, and a split entity has parts that the history does not tell apart.

**Size.** The length $m$ of the history, the number of entities of each model, and the number of references.

**Model.** Exact B-rep topology, with the faces of each model labeled by the feature that made them. The geometry is used only to break ties.

## Variants

- **Faces only, or all entities.** Naming faces is easier, because most faces come from one generating entity of one feature. Edges and vertices are usually named by the faces that meet at them, which fails when two faces meet along several edges.
- **Single model or exchange.** Within one CAD system, the names may use internal data of the kernel. For the exchange of parametric models between systems, the names must be defined by the operations alone.
- **History-free editing.** In direct modeling, faces are moved without a history, and the problem becomes keeping the identity of faces across a local edit, a related but easier problem.
- **References from constraints.** A sketch dimension or an assembly mate that refers to a face of a part is a [geometric constraint](/geometric-constraint/) on a named entity, and loses its meaning in the same way.

## Examples

- **Index names fail.** A block has six faces, numbered in the order the kernel made them, and a chamfer is attached to the edge between face 2 and face 5. The designer then inserts a hole before the chamfer. The replay makes the faces in a different order, face 2 is now another face, and the chamfer moves to the wrong edge without any error. This is the failure that persistent names prevent.
- **A generative name.** A sketch rectangle with lines $\ell_1, \dots, \ell_4$ is extruded. The side face made from $\ell_3$ gets the name "the face swept from $\ell_3$ by extrusion 1", and the top face "the end cap of extrusion 1". A fillet on the edge between these two faces keeps its meaning when the rectangle is resized, because the sketch lines keep their identity.
- **A split.** Then the designer inserts, before the fillet, a through slot that cuts across the top face and across the face of $\ell_3$. The edge between them is now two edges, one on each side of the slot. The generative relation maps the old edge to both. Whether the fillet should round both, one, or neither is a question of intent: a designer who wanted to break a sharp edge wants both, and one who wanted to blend into a mating part on the left may want only one. No name computed from the history alone can know which.
- **A disappearance.** A fillet is attached to the edge where a boss meets the top face. The designer then suppresses the boss. The edge no longer exists, and the correct answer is a failure report, not a fillet on some other edge.
- **Symmetric pieces.** A through slot across the middle of a block splits the top face into two halves that are mirror images, and a later chamfer is attached to an edge of the left half. Both halves come from the same face by the same cut, so their generative names are equal. A scheme must add something to tell them apart, such as the side of the slot each lies on, or the faces around each piece.

## Known algorithms

The approaches are only listed here; no algorithm solves the problem as stated, because the constraints refer to intent.

- **Topological ID.** Kripac's mechanism names each face by the feature that made it and by its generating entity, names edges and vertices by the faces around them, and after a replay matches the new entities to the old ones by their names, using the surrounding faces to tell apart the pieces of a split.
- **Generic naming.** Capoyleas, Chen and Hoffmann build a name from the operation that creates an entity and the names of the entities it is made from, and add terms from the neighboring entities when the name alone is ambiguous. Chen and Hoffmann had earlier described how a feature is attached to such names.
- **Geometric matching.** Match the entities of the new model to the old ones by position, normal and shape, alone or as a tie breaker. It handles symmetric ties but fails when the edit moves the geometry a lot.
- **Graph matching.** Match the face adjacency graphs of the two models, which is a form of [maximum common subgraph](/maximum-common-subgraph/), with the feature labels as node labels.

Marcheix and Pierra survey these classes and list cases where each one fails.

## Bounds

**What is proved.** Little. For an edit that keeps the topology of every model of the history, a generative scheme is one to one, by induction on the history, provided that each operation makes its entities in a way that depends only on the topology of its inputs. Beyond that, no scheme is proved to meet the constraints, and the split example shows that the constraints themselves do not fix the answer, so there is nothing to prove without a formal notion of intent. Matching face graphs exactly, without the generative labels, includes [graph isomorphism](/graph-isomorphism-problem/) as a special case, and maximum common subgraph is NP-hard; the generative labels make the matching easy in practice.

**What is only measured.** The quality of a scheme is judged on test histories and edits chosen by its authors, and on the bug reports of users of CAD systems. There is no agreed benchmark of edits with agreed answers.

## Reductions

- **From [feature-based modeling](/feature-based-modeling/).** Every history-based modeler must solve some version of the problem at each replay.
- **To graph matching.** Resolving names after a topological change is a labeled matching of the entities of two B-reps, with the feature labels and the adjacencies as constraints.
- **Related to [Euler operators](/euler-operators/).** If each modeling step is written as a sequence of Euler operators, each new entity has a known creating operator, which is a basis for generative names.
- **Related to [feature recognition](/feature-recognition/).** When a model arrives without a history, there are no names at all, and recognition must rebuild the features before references can be made.

## Applications

- **Parametric CAD.** Fillets, chamfers, drafts, sketch planes and hole positions refer to faces and edges, and every edit of an earlier feature tests the naming scheme.
- **Assemblies.** Mates between parts refer to faces of each part, and an edit of a part must keep them.
- **Downstream data.** Toolpaths, inspection plans and finite element loads are attached to faces, and must follow the faces through edits.
- **Exchange of histories.** Sending a parametric model with its history to another system needs names that both systems compute the same way.

## References
