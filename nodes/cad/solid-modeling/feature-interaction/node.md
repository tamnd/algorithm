---
tag: GE8178
kind: concept
slug: feature-interaction
name: Feature interaction
aliases:
- interacting features
area: cad/solid-modeling
level: advanced
summary: When features overlap, or one consumes faces another refers to, their shapes and meanings change, which breaks feature recognition and parametric replay.
prereqs: [feature-based-modeling, feature-recognition, regularized-set-operations]
see_also: [hint-based-feature-recognition, volume-decomposition-feature-recognition, alternating-sum-of-volumes, attributed-adjacency-graph, persistent-naming-problem, generic-naming-scheme, operation-sequencing, direct-modeling]
sources:
  - book: isbn:9780471002147
    title: Jami J. Shah and Martti Mäntylä, Parametric and Feature-Based CAD/CAM, Concepts, Techniques, and Applications, Wiley, 1995
    locator: the treatment of interacting features in the parts on feature validation and on feature recognition (chapter numbers not checked)
  - paper: "Rafael Bidarra and Willem F. Bronsvoort, Semantic feature modelling, Computer-Aided Design 32(3), 201 to 225, 2000"
    locator: feature classes with boundary and interaction constraints, the interaction types, and validity maintenance after each modeling operation
  - paper: "Willem F. Bronsvoort, Rafael Bidarra and Paulos J. Nyirenda, Developments in feature modelling, Computer-Aided Design and Applications 3(5), 655 to 664, 2006"
    locator: Section 3 (a through hole turned into a blind hole by a stiffener) and Section 4 (boundary constraints, closure faces, feature interactions as changes of meaning, and the splitting interaction)
  - paper: "Shuming Gao and Jami J. Shah, Automatic recognition of interacting machining features based on minimal condition subgraph, Computer-Aided Design 30(9), 727 to 739, 1998"
    locator: why interactions break the face patterns of graph-based recognition, and the minimal condition subgraph that survives them
  - paper: doi:10.1109/34.250845
    title: Jan H. Vandenbrande and Aristides A. G. Requicha, Spatial reasoning for the automatic recognition of machinable features in solid models, IEEE Transactions on Pattern Analysis and Machine Intelligence 15(12), 1269 to 1285, 1993
    locator: traces of features that survive interactions, and their completion into volumes
  - paper: doi:10.1109/70.897789
    title: JungHyun Han, Mike Pratt and William C. Regli, Manufacturing feature recognition from solid models, a status report, IEEE Transactions on Robotics and Automation 16(6), 782 to 796, 2000
    locator: the sections on feature interactions and multiple interpretations
---

Two features *interact* when one of them changes the shape of the other, so that the faces the part ends up with are not the faces either feature would have alone. A slot cut across another slot splits its walls. A hole drilled from the floor of a pocket is shorter than a hole drilled from the top. A rib placed over the exit of a through hole makes it blind. Interactions matter in two directions. In [feature-based modeling](/feature-based-modeling/), an edit can create an interaction that silently changes what a feature means, so the system has to check the meaning after each change. In [feature recognition](/feature-recognition/), the input part shows only the faces left after all the interactions, so a recognizer that looks for the textbook face pattern of each feature misses the interacting ones. In the volumetric view the concept can be made precise. Each feature is a volume with some faces that are meant to appear on the part, and an interaction is an overlap of volumes or a nominal face that does not appear in full. Two simple facts follow. The part depends only on the union of the removed volumes, so interacting features can be read in more than one way. And the faces of the part are not the union of the faces of the features.

## In plain words

Think of a block of wood. You cut a groove across it. Then you cut a second, deeper groove the other way. The first groove is now in two pieces, with a gap where the second one crossed it.

If someone hands you only the finished block, you might say "two short grooves and one long one". Or you might say "two long grooves that cross". Both describe the same block. A computer that looks for "a groove with two whole side walls" finds neither, because every side wall has been cut.

The same thing happens when you edit a design. Move a bracket over the exit of a hole, and the hole no longer goes through. The block is still a valid solid, but the hole has quietly become something else.

## The idea

**Features as volumes.** Take the removal view, which suits machining. A stock $W$ and features $f_1, \dots, f_m$ are given. Each feature $f_i$ has a volume $V_i$, a closed solid, and its boundary is split into *nominal faces* and *closure faces*. The nominal faces are the faces that the feature is meant to leave on the part: the floor and the two walls of a slot, the cylinder of a hole. The closure faces only close off the volume, like the open top of a slot. The part is the [regularized difference](/regularized-set-operations/)
$$P = W -^* (V_1 \cup \dots \cup V_m).$$
Features that add material, such as bosses and ribs, are handled in the same way with unions, but then the order of the operations matters.

**Isolated and interacting.** Feature $f_i$ is *isolated* when its volume meets no other feature volume except along boundaries, every nominal face of $V_i$ lies on the boundary of $P$ in full, and no closure face does. Otherwise $f_i$ *interacts*. The common cases are these.

- **Volume overlap.** $\operatorname{int} V_i \cap \operatorname{int} V_j \ne \emptyset$. The crossing slots and the hole in a slot floor are of this kind.
- **Nominal face lost or split.** Part of a nominal face of $V_i$ lies inside another volume, so the face on $P$ is smaller, in several pieces, or gone. Bidarra and Bronsvoort call it a *splitting* interaction when a slot is cut into two separate, smaller slots.
- **Closure face covered.** A closure face of $V_i$ ends up on the boundary of $P$, because material was added there. The through hole that a stiffener makes blind is the standard example. Bidarra and Bronsvoort's interaction types include closure and absorption as well as splitting. Their classes can forbid any type for their instances, and the system checks those constraints after each operation.
- **Absorbed.** $V_i \subseteq V_j$, so $f_i$ leaves no trace on $P$ at all.

**Fact 1: the part sees only the union.** For removal features, $P$ depends on the set $V_1 \cup \dots \cup V_m$ and nothing else, by the formula above. So any two families of volumes with the same union give the same part. When volumes overlap there is usually more than one such family, and a recognizer must either pick one or return all of them. This is the source of the *multiple interpretations* in volumetric recognition. With removal features alone the order does not matter either, since union is commutative. When a feature adds material, $(W -^* V_1) \cup^* B$ and $(W \cup^* B) -^* V_1$ differ wherever the added material $B$ meets $V_1$. That is the case of the blinded hole.

**Fact 2: faces are not additive.** Every face of $P$ lies on the boundary of $W$ or of some $V_i$, because the boundary of a Boolean result lies in the union of the boundaries of its operands. But the faces of $P$ are pieces of those faces, cut by the other volumes. A nominal face of an isolated feature appears whole. A nominal face of an interacting feature appears in pieces, smaller, or not at all. So a recognizer that matches whole-face patterns, as the [attributed adjacency graph](/attributed-adjacency-graph/) method does, is exact for isolated features and can fail on interacting ones. Recognizers that cope with interactions look for what survives: a minimal subgraph of the pattern (Gao and Shah), a trace such as one wall or a piece of a floor, completed into a volume ([hint-based recognition](/hint-based-feature-recognition/)), or a decomposition of the removed volume itself ([cell decomposition](/volume-decomposition-feature-recognition/) and [alternating sums of volumes](/alternating-sum-of-volumes/)).

## Examples

All examples use the block $W = [0, 6] \times [0, 4] \times [0, 2]$.

- **Splitting.** Slot $A = [2, 4] \times [0, 4] \times [1, 2]$ runs along $y$ with its floor at $z = 1$. Slot $B = [0, 6] \times [1, 3] \times [0.5, 2]$ runs along $x$ and is deeper, with its floor at $z = 0.5$. On the part, the floor of $A$ is two rectangles, $[2, 4] \times [0, 1]$ and $[2, 4] \times [3, 4]$, and each wall of $A$ is two pieces. The walls of $B$ are also cut where $A$ crosses them, but $B$'s floor is whole. $A$ has become two short slots, one at each end, and $B$ is a long slot with notches in its walls.
- **Two readings of one part.** If the slots have equal depth, so $B = [0, 6] \times [1, 3] \times [1, 2]$, the removed volume is a cross of total volume $2 \cdot 4 \cdot 1 + 6 \cdot 2 \cdot 1 - 2 \cdot 2 \cdot 1 = 16$. It is the union of the two long slots, and also the union of the long slot $B$ with the two short slots $[2, 4] \times [0, 1] \times [1, 2]$ and $[2, 4] \times [3, 4] \times [1, 2]$. By Fact 1 both families give the same part. A process planner may prefer either one.
- **A hole in a floor.** A hole of radius $0.4$ about the axis $x = 3$, $y = 0.5$ is drilled from the top through the whole block. Its volume overlaps slot $A$ for $z \in [1, 2]$. On the part its cylindrical face runs only from $z = 0$ to $z = 1$, so a recognizer that reads the hole from its face finds a hole of depth 1 starting at the slot floor. That is also how a machinist would drill it.
- **Absorption.** A blind hole of radius $0.4$ about the same axis, of depth $0.8$ from the top, lies wholly inside slot $A$. It leaves no face on the part. If the slot is later made shallower, with its floor at $z = 1.5$, the hole reappears with depth $0.3$. A feature that was invisible becomes real after an edit of another feature.
- **Closure in a history.** A through hole is drilled in a plate, and then a rib is added under the plate across the exit of the hole. The hole is now blind. The model is a valid solid, but the hole's meaning has changed. A semantic feature modeler flags this, because the bottom closure face of the hole is now on the boundary of the part, which the hole's class forbids.

## Where it is used

- **Feature recognition.** Interactions are the main reason recognition is hard. The surveys of Han, Pratt and Regli, and of Shah and Mäntylä, sort methods by how they treat them. Graph matching handles isolated features. Minimal condition subgraphs, hints and volume decompositions handle more interactions, and none handles all of them.
- **Validity maintenance in design.** Semantic feature modeling lets a feature class state which faces must stay on the boundary and which interactions are not allowed. After each operation the modeler checks the constraints and reports violations, as Bidarra and Bronsvoort describe.
- **Process planning.** An interaction between machining features sets an order. The hole that starts at the slot floor is drilled after the slot is milled, because its depth and its entry face are those of the floor. These precedences are inputs to [operation sequencing](/operation-sequencing/).
- **Parametric replay and naming.** An edit that changes interactions changes the topology, so faces split, merge or vanish. References from later features then break or move, which is the [persistent naming problem](/persistent-naming-problem/). [Generic naming](/generic-naming-scheme/) extends names by their neighbours to cope with splits.
- **Direct editing.** A [direct modeling](/direct-modeling/) edit that moves a face across another feature creates an interaction on the spot, and the modeler has to choose the topology that results.

## References
