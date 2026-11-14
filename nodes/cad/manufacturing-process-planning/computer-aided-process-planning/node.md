---
tag: C1Q2KK
kind: concept
slug: computer-aided-process-planning
name: Computer-aided process planning
aliases:
- CAPP
- variant process planning
- generative process planning
area: cad/manufacturing-process-planning
level: intro
summary: Turns a part design into a sequence of operations, machines, tools and setups, by adapting the plan of a similar part (variant) or by reasoning (generative).
see_also: [feature-recognition, setup-planning, operation-sequencing, fixture-planning, cutting-parameter-optimization, manufacturability-analysis, accessibility-cone, toolpath-planning]
sources:
  - paper: doi:10.1080/00207548908942569
    title: Leo Alting and Hongchao Zhang, Computer aided process planning, the state-of-the-art survey, International Journal of Production Research 27(4), 1989, 553 to 585
    locator: the variant and the generative approach, group technology coding for variant systems, decision tables, decision trees and expert systems for generative systems, and a survey of the systems of the time
  - book: doi:10.1007/978-94-011-1250-5
    title: Gideon Halevi and Roland D. Weill, Principles of Process Planning, a Logical Approach, Chapman and Hall, 1995
    locator: the chapter Computer-aided process planning (CAPP), and the earlier chapters on the steps of a manual plan
  - book: isbn:9780133128741
    title: Serope Kalpakjian and Steven R. Schmid, Manufacturing Engineering and Technology, 7th edition, Pearson, 2014
    locator: Section 38.6 (computer-aided process planning, variant and generative systems) and Section 38.8 (group technology, part families and classification and coding)
---

Computer-aided process planning (CAPP) is the use of a computer to make a process plan: the list of operations that turns raw stock into a finished part, with the machine, the tool, the setup, the fixture and the cutting conditions of each operation. It sits between design and manufacturing. Its input is the part model or drawing, and its output is the route sheet and the operation sheets that the shop follows. There are two kinds. Variant process planning finds a similar part that the shop already makes and edits its plan. Generative process planning builds a new plan from the features of the part and from rules about processes. Most real systems mix the two.

## In plain words

Before a part is made, someone must decide how to make it. Which machine cuts it first? How is it held? Which tool makes each hole, and in which order? How fast does each tool cut? The answer is a process plan, a list of steps for the shop. An experienced planner writes it from memory and from the plans of parts that look like this one.

A planning system does the same work with a computer. One kind keeps a library of standard plans, one for each family of similar parts. For a new part, it finds the family and gives the planner the standard plan to edit. The other kind reads the shapes on the part, such as holes, slots and pockets, and uses rules to choose a process for each shape and to put the steps in order.

## The idea

**What a plan holds.** A process plan answers a chain of questions, and each one has its own page here:

1. Read the design: the stock, the material, the [features](/feature-recognition/) to make and their tolerances.
2. Choose a process for each feature, for example drill and ream for a precise hole.
3. Choose machines and tools.
4. Group the operations into setups, each a fixed orientation of the part ([setup planning](/setup-planning/)).
5. Choose how to hold the part in each setup ([fixture planning](/fixture-planning/)).
6. Order the operations ([operation sequencing](/operation-sequencing/)).
7. Choose the speed, feed and depth of each cut ([cutting parameter optimization](/cutting-parameter-optimization/)).
8. Estimate the time and the cost.

**Variant process planning.** This kind rests on group technology. Group technology is the practice of sorting parts into families of similar shape or similar processing, so that one family can share one plan, one group of machines or one fixture. A part gets a classification code, a string of digits where each digit stands for one property: the main shape, the outer and inner form, the holes, the size, the material. The Opitz system is a well-known code of this type. A variant system stores one standard plan per family. To plan a new part, the planner codes it, the system finds the family with that code, and the planner edits the standard plan for the details of the new part. The system is only as good as its library of families and plans, and it cannot plan a part that fits no family.

**Generative process planning.** This kind makes a plan from the part and from general knowledge, with no stored plan of a similar part. The input is a model of the part in terms of features, often found by [feature recognition](/feature-recognition/) on the solid model. Rules map each feature and its tolerance to a chain of processes. Geometric reasoning, such as the [accessibility cone](/accessibility-cone/) of each feature, groups the features into setups. Precedence rules and an objective, such as few tool changes, order the operations. The early systems wrote the rules as decision tables and decision trees, and later ones as expert systems (Alting and Zhang 1989). A fully generative system needs no planner for routine parts, but it needs a complete model of the processes, which is hard to build. Many systems are called semi-generative: they generate parts of the plan and leave the rest to a planner or to a stored plan.

**Why the two kinds differ.** A variant system reuses the experience of the shop and is cheap to build, but it copies the old habits, good and bad, and it needs a planner. A generative system can plan new parts and gives the same plan for the same part each time, but its rules cover only the processes and features that it knows.

## Examples

**Variant planning of a shaft.** A shop codes its turned parts. A family holds shafts with two diameters, one shoulder and one keyway. Its standard plan is: face and center both ends; rough turn; finish turn the two diameters; mill the keyway; deburr. A new shaft with the same code gets this plan. The planner then sets the lengths, the diameters and the cutting conditions for the new part. If the new shaft also has a cross hole, it fits no family exactly, and the planner adds a drilling operation by hand.

**Generative planning of a block.** A block has a flat top face that is a datum, a through hole of diameter 10 mm with a tight tolerance from the top, a pocket open to the top, and a slot on one side. Rules choose:

| feature | rule | operations |
|---|---|---|
| top face (datum) | a datum is made first | face mill |
| hole, tight tolerance | a precise hole is drilled, then reamed | center drill, drill 9.8 mm, ream 10 mm |
| pocket | rough, then finish | rough end mill, finish end mill |
| side slot | a slot is milled with a slot cutter | slot mill |

The top face, the hole and the pocket are reachable from $+z$, and the slot only from one side, so setup planning makes two setups. In the first setup the order puts the face before the hole, because the hole tolerance is measured from the face, and it groups the operations by tool to save tool changes. A real system also checks the stock, the machine and the fixture, but each choice above is a rule of the same kind.

## Where it is used

- **Machining.** Most CAPP work is for machined parts: prismatic parts on machining centers and rotational parts on lathes.
- **Sheet metal, casting and assembly.** The same steps appear with other processes: [bend sequence planning](/bend-sequence-planning/) for press brakes, [cutting sequence planning](/cutting-sequence-planning/) for laser and plasma cutting, and assembly planning for products.
- **Cost estimation and design feedback.** A plan gives the time and cost of a part at the design stage, and the same rules support [manufacturability analysis](/manufacturability-analysis/).
- **CAM.** The plan fixes the setups and tools that the CAM system turns into [toolpaths](/toolpath-planning/).

There are no standard benchmarks for process planning. Systems are shown on example parts of their own, so their results cannot be compared from paper to paper.

## References
