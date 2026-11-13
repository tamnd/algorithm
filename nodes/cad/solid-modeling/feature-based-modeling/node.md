---
tag: 3XGR2J
kind: concept
slug: feature-based-modeling
name: Feature-based modeling
aliases:
- feature modeling
- parametric feature modeling
area: cad/solid-modeling
level: core
summary: Design by a history of parameterized features such as holes, pockets, bosses and fillets, each with a meaning for function and manufacture.
prereqs: [boundary-representation, constructive-solid-geometry]
see_also: [feature-recognition, persistent-naming-problem, attributed-adjacency-graph, variational-geometry, geometric-constraint, solid-boolean-operations, blending-surface, pocket-machining]
sources:
  - book: isbn:9780471002147
    title: Jami J. Shah and Martti Mäntylä, Parametric and Feature-Based CAD/CAM, Concepts, Techniques, and Applications, Wiley, 1995
    locator: the parts on feature-based design, feature representation and feature recognition (chapter numbers not checked)
  - paper: doi:10.1016/0010-4485(91)90027-T
    title: Jami J. Shah, Assessment of features technology, Computer-Aided Design 23(5), 331 to 343, 1991
    locator: the whole paper (the definition of form features, and the three ways to build a feature model, interactive definition, automatic recognition and design by features)
  - paper: "Xiangping Chen and Christoph M. Hoffmann, Towards feature attachment, Computer-Aided Design 27(9), 695 to 702, 1995"
    locator: the description of how a feature is attached to faces and edges of the model built before it
---

Feature-based modeling builds a part as an ordered list of *features*, form elements such as a block, a hole, a slot, a pocket, a boss, a rib, a fillet or a chamfer, each given by a few parameters and placed by references to the geometry made before it. The modeler replays the list to evaluate a [boundary representation](/boundary-representation/): each feature adds or removes material with a [Boolean operation](/solid-boolean-operations/), or changes the shape locally, as a fillet does. A change of a parameter is a change of one number in the list, followed by a replay. The features also carry meaning that the bare faces lack: a hole knows that it is a hole, which a process planner, a tolerancing tool or a later edit can use.

## In plain words

Instead of drawing every face of a part, the designer describes how the part is made: start from a block of these sizes, drill a hole of this diameter here, cut a slot of this width there, round these edges. The computer keeps this recipe and computes the shape from it.

To change the part, the designer changes a number in the recipe, for example the width of the block, and the computer cooks the part again. If the hole was placed at a distance from an edge, it moves with that edge.

The recipe also tells what each part of the shape is for. A drill press needs to know where the holes are, and the recipe says so directly.

## The idea

A *form feature* is a region of the shape of a part with an engineering meaning, together with a generic shape and its parameters. A through hole has a diameter, an axis and the face where it starts; a rectangular pocket has a length, a width, a depth and a corner radius; a fillet has a radius and the edges it rounds. Shah's assessment of features technology sorts the ways to get a feature model into three: the designer marks features on an existing model by hand, a program finds them in a model without features, which is [feature recognition](/feature-recognition/), or the designer builds the part from features from the start, which is design by features.

In design by features, the model has three layers.

- **The history.** An ordered list, or a tree, of feature instances. Each instance stores its type, its parameters and its references. Many features start from a 2D sketch whose lines and arcs are held by [geometric constraints](/geometric-constraint/) and dimensions, solved as in [variational geometry](/variational-geometry/), and then extruded, revolved or swept.
- **The evaluation.** Replaying the history gives the B-rep. A feature that adds material, such as a boss, is a regularized union with the current solid, a feature that removes material, such as a hole, is a regularized difference, so the history is a [CSG](/constructive-solid-geometry/) expression with extra operations. Local operations such as fillets, chamfers, drafts and shells are applied to the B-rep directly; a fillet is a [blending surface](/blending-surface/).
- **The references.** A feature is attached to the model built before it: the hole starts on *this* face, the fillet rounds *these* edges. The references point to faces and edges of an intermediate B-rep, which is computed again at each replay, so they must be stored in a form that survives the replay. This is the [persistent naming problem](/persistent-naming-problem/).

Editing a parameter of feature $k$ replays the history from $k$ on. The new model can differ in topology, because a face can split, vanish or merge, and then a later feature can lose its references or change its meaning. Feature modelers therefore check *validity* after an edit: a through hole must still go through, a pocket must still be open where its tool enters, and a fillet radius must fit its edges. Two features *interact* when one changes the shape of the other, for example when a slot cuts through a boss; the stored meaning of each must then be revised.

Design features and manufacturing features are different views of one part. A designer may add a rib, while the machinist sees two pockets on either side of it. A single feature model rarely fits all views, so a system converts between them, by mapping features or by recognizing the features of one view in the geometry made by the other.

## Examples

- **A plate with a hole.** Feature 1 is a block, a sketch rectangle of $100 \times 60$ extruded by $10$. Feature 2 is a through hole of diameter $8$ on the top face, with its center $25$ from the left face and $30$ from the front face. Changing the length of the block to $80$ replays feature 2 with the same references, so the hole stays $25$ from the left face, now $55$ from the right face. If the hole had been dimensioned $75$ from the right face instead, the same edit would put it $5$ from the left face. The two models are equal before the edit and differ after it. The meaning of a dimension depends on what it is attached to.
- **Order matters.** A fillet of radius $2$ on all edges of the top face, then a pocket cut into the top face, leaves the rim of the pocket sharp, because the rim did not exist when the fillet was made. In the other order the edges of the top face include the rim, and the fillet rounds it too. The two histories give different solids from the same features.
- **A lost reference.** A chamfer is attached to the edge where the hole meets the top face. The designer then moves the hole off the plate. The edge no longer exists, and the replay must report that the chamfer has no edge, rather than chamfer some other edge.
- **Two views.** A bracket designed as a plate with a boss and a hole is, for milling, a stock block with the material around the boss removed as a pocket and the hole drilled. The design features do not list the pocket; recognizing it from the faces is a job for an [attributed adjacency graph](/attributed-adjacency-graph/).

## Where it is used

- **Mechanical CAD.** Most current mechanical CAD systems are history-based feature modelers with sketches and constraints. Some offer direct editing of faces without a history as well.
- **Process planning.** Machining features map to operations: a hole to drilling, a pocket to [pocket machining](/pocket-machining/), a slot to a slotting cut. Computer-aided process planning reads them from the feature model, or recognizes them when the model has none.
- **Tolerancing and inspection.** Tolerances are stated on features, such as the position of a hole, and a [tolerance stack-up](/tolerance-stack-up/) is a chain of feature dimensions.
- **Data exchange.** A neutral B-rep file carries faces but no history, so a model received this way has no features until they are recognized again.

## References
