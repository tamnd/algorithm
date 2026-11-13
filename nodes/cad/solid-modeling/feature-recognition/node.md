---
tag: M4TTJP
kind: problem
slug: feature-recognition
name: Feature recognition
aliases:
- automatic feature recognition
area: cad/solid-modeling
level: core
summary: Find machining or design features such as holes, slots and pockets in a B-rep that has only faces and edges, as needed by process planning.
prereqs: [boundary-representation, feature-based-modeling]
see_also: [attributed-adjacency-graph, subgraph-isomorphism, set-cover, pocket-machining, toolpath-planning, accessibility-cone, mesh-segmentation, regularized-set-operations]
sources:
  - paper: doi:10.1109/70.897789
    title: JungHyun Han, Mike Pratt and William C. Regli, Manufacturing feature recognition from solid models, a status report, IEEE Transactions on Robotics and Automation 16(6), 782 to 796, 2000
    locator: the whole survey (graph-based, volumetric decomposition and hint-based recognition, feature interactions, multiple interpretations, and the open issues)
  - paper: doi:10.1016/0010-4485(88)90050-4
    title: S. Joshi and T. C. Chang, Graph-based heuristics for recognition of machined features from a 3D solid model, Computer-Aided Design 20(2), 58 to 66, 1988
    locator: the whole paper (the attributed adjacency graph and the matching of feature graphs)
  - paper: doi:10.1016/0010-4485(91)90027-T
    title: Jami J. Shah, Assessment of features technology, Computer-Aided Design 23(5), 331 to 343, 1991
    locator: the part on automatic feature recognition as one of the three ways to build a feature model
  - book: isbn:9780471002147
    title: Jami J. Shah and Martti Mäntylä, Parametric and Feature-Based CAD/CAM, Concepts, Techniques, and Applications, Wiley, 1995
    locator: the part on feature recognition (chapter number not checked)
---

Feature recognition takes a solid that is given only by its faces, edges and vertices, and finds in it the *features* that a designer or a machinist would name: holes, slots, steps, pockets, bosses. A recognized feature is a set of faces of the part, or a volume of material that one machining operation removes, with its type and its parameters. The problem connects the geometry of a [B-rep](/boundary-representation/) with the meaning that process planning needs, and it is needed whenever a part was not built with [feature-based modeling](/feature-based-modeling/), or was built with design features that differ from the machining ones. The answer is often not unique, and there is no single agreed formal statement.

## In plain words

A machine shop receives the shape of a part as a list of faces. To plan the work, it must know where the holes are, where the slots are and how deep the pockets go. A person sees this at a glance. A program sees only faces and the edges between them.

Feature recognition is the job of finding these familiar shapes in the faces. It is hard because features overlap. A hole drilled through the bottom of a slot breaks the faces of both, so neither looks like the textbook pattern any more.

It is also unclear what the right answer is. Two crossing slots can be seen as two long slots, or as one long slot and two short ones. Both plans can make the part.

## Definition

There are two common formal versions. Both start from the same input.

**Input.** A part $P$, a solid given as a [boundary representation](/boundary-representation/) with planar and simple curved faces, and for the volumetric version a stock $W \supseteq P$, often the bounding box. A library $\mathcal{L}$ of feature classes. Each class has a type, such as through slot, blind hole or rectangular pocket, a list of parameters, and a definition, which is either a pattern of faces and edges or a family of volumes $V(\theta)$ that one tool motion can remove.

**Output.**

- *Surface-based version.* A set of feature instances. Each instance is a class $c \in \mathcal{L}$, parameters $\theta$, and a set of faces of $P$ that has the pattern of $c$, with the convexity of the shared edges as the pattern states. An edge is convex when the solid angle of material along it is less than $\pi$, measured with outward face normals by the right-hand rule.
- *Volumetric version.* An *interpretation*: a finite set of instances $V_1 = V(\theta_1), \dots, V_m = V(\theta_m)$ such that no $V_i$ cuts into the part, $\operatorname{int} V_i \cap P = \emptyset$, and together they remove the whole delta volume $D = \operatorname{cl}(W \setminus P)$, so $D \subseteq V_1 \cup \dots \cup V_m$. Each $V_i$ must also be accessible to its tool from some direction. Some formulations ask for one interpretation, some for all of them, and some for one that is best for a cost, such as the number of setups.

**Constraints.** Features may interact: their volumes may overlap, and one feature may remove faces of another, so a face pattern can be broken or a new one can appear by chance. Volumes may extend outside $W$ into air. Degenerate cases are part of the input: two coplanar faces of different features, a hole tangent to a wall, an edge where the faces meet at exactly $\pi$, which is neither convex nor concave and must be merged or labeled. The convexity of an edge is a sign, and for curved faces near tangency it is the sign of a small number, so the [orientation test](/orientation-test/) and [catastrophic cancellation](/catastrophic-cancellation/) matter here as in any solid modeler. The fix is to compute the sign exactly, which is possible for planar faces with rational vertices.

**Size.** The number $n$ of faces of $P$, the size of the library, and the number $k$ of faces in the largest feature pattern.

**Model.** Exact B-rep geometry with exact signs, as in [exact geometric computation](/exact-geometric-computation/), for the recognition step. The library is part of the problem, not of the input data of the part: the same part has different features for milling and for casting.

## Variants

- **Design features versus machining features.** Design recognition looks for the features a designer would have used. Machining recognition looks for removal volumes and is tied to a process.
- **2.5D versus 3D.** Most work treats 2.5D features, whose volumes are a planar profile swept along a line, as milled from one direction. Freeform faces and 5-axis access are much less settled.
- **With interactions.** Recognition that must find features whose faces are split, merged or partly missing because other features cut them.
- **Single versus multiple interpretations.** Return one cover of $D$, all minimal covers, or the cover that is best for a cost.
- **From meshes and scans.** The input is a triangle mesh or a point cloud. The first step is a [mesh segmentation](/mesh-segmentation/) into faces, which adds noise to every later decision.
- **Incremental.** Update the features after a small edit, without recognizing the whole part again.

## Examples

- **A through slot.** A block $[0, 6] \times [0, 4] \times [0, 2]$ with the slot $[2, 4] \times [0, 4] \times [1, 2]$ removed. The slot has a bottom face and two walls; the two edges where the walls meet the bottom are concave, and the four edges where the walls meet the top face are convex. Surface-based recognition finds a face pattern "floor with two concave neighbors that face each other". The volumetric version has $D$ equal to the box of the slot, and one instance covers it.
- **Two crossing slots.** Cut the slot of the first example and a second slot $[0, 6] \times [1, 3] \times [1, 2]$. The delta volume is a cross. It is covered by two long slots that overlap in the square $[2, 4] \times [1, 3] \times [1, 2]$, or by one long slot and two short ones, which do not overlap. Both are valid interpretations. In the surface view the walls of each slot are split into two faces by the other, so a template with two whole walls does not match.
- **A step or a slot.** Cut $[4, 6] \times [0, 4] \times [1, 2]$ from the block instead. With the block as stock this is a step, with one wall and one floor, and its volume is open at the top and at the side $x = 6$. Its wall meets its floor in one concave edge, and a slot template with two walls does not match it, so the library needs both classes. A step and a slot differ only in the number of walls.
- **A hole in a slot floor.** A through hole drilled down from the floor of the slot. The cylindrical face starts at the floor, not at the top face of the block, so its depth is $1$, and a recognizer that measures holes from the top face reports the wrong depth.

## Known algorithms

- **Graph-based recognition.** Build the face adjacency graph, label each edge convex or concave, and find feature patterns as labeled subgraphs. The [attributed adjacency graph](/attributed-adjacency-graph/) of Joshi and Chang (1988) is the standard example. It is exact for isolated features whose patterns are in the library, and weak on interactions, which break the patterns.
- **Rule-based and syntactic recognition.** Early systems wrote each feature as a rule over faces and edges and searched for matches with logic programming or grammars. They are the surface-based version with a more general pattern language.
- **Volumetric decomposition.** Split the delta volume into pieces and combine them into feature volumes. The convex hull method writes the part as an alternating sum of convex volumes, and the cell method splits $D$ along the extended faces of $P$ and joins cells into removal volumes. Choosing the fewest candidate volumes that cover all cells is a [set cover](/set-cover/) problem.
- **Hint-based recognition.** Look for traces of features, such as two opposite parallel walls for a slot or a cylindrical face for a hole, then grow each trace into the largest volume that does not cut the part, and verify it. Vandenbrande and Requicha (1993) made this approach well known; it handles interactions better because a trace survives when the full pattern does not.
- **Learning methods.** Neural networks trained on labeled parts, on graphs or on voxel or mesh inputs. They are measured on test sets, and nothing is proved about them.

Han, Pratt and Regli survey these families and conclude that each handles some interactions and fails on others.

## Bounds

**What is proved.**

- *Matching.* For a fixed library, each pattern has at most $k$ faces, and a brute-force search over ordered $k$-tuples of faces finds every match of the surface-based version in $O(n^k k^2)$ time. If the patterns are part of the input and may be arbitrary graphs, the matching step is [subgraph isomorphism](/subgraph-isomorphism/), which is NP-complete. Feature graphs are small and the labels prune the search, which is why the step is fast in practice.
- *Exact labels.* For a polyhedral part with rational vertices, the convexity of each edge is the sign of a determinant of integers, so the face graph and its labels can be computed with no error.
- *Volumetric covering.* Over a finite set of candidate volumes, deciding whether there is a cover of $D$ with at most $m$ volumes is a set cover question. Set cover is NP-complete in general. This page does not claim a hardness result for the special set systems that arise from parts.

**What is only measured.** The quality of a recognizer, which interactions it handles and how often it reports the features that a process planner wants, is judged on test parts, mostly chosen by the authors of each method. There is no agreed set of parts with agreed answers, so the published success rates of different methods cannot be compared directly.

## Reductions

- **To labeled subgraph isomorphism.** The surface-based version with a fixed library reduces to induced labeled subgraph isomorphism between each template and the face graph of the part, with face and edge labels. This is the step that the [attributed adjacency graph](/attributed-adjacency-graph/) method solves.
- **To set cover.** The volumetric version reduces, once a finite candidate set is fixed, to covering the cells of $D$ by candidate volumes that do not cut $P$.
- **From [regularized set operations](/regularized-set-operations/).** The delta volume is $W -^* P$, and checking a candidate volume is a Boolean test, $\operatorname{int} V \cap P = \emptyset$.
- **To accessibility.** Deciding whether a volume is machinable from a direction is a question about [accessibility cones](/accessibility-cone/).

## Applications

- **Process planning.** Each recognized feature maps to operations, tools and a setup: holes to drilling, slots and steps to end milling, pockets to [pocket machining](/pocket-machining/), and the plan orders them.
- **Toolpath generation.** A recognized pocket gives its floor, walls and depth to [toolpath planning](/toolpath-planning/).
- **Manufacturability checks.** Thin walls, deep narrow holes and sharp inside corners are found on the features and reported to the designer.
- **Data exchange.** A model read from a neutral B-rep file has no history. Recognition gives back a feature structure that can be edited or reused.
- **Cost estimation.** Quotes for machined parts are computed from the list and sizes of features.

## References
