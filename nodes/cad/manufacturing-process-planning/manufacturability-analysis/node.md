---
tag: YAK20R
kind: concept
slug: manufacturability-analysis
name: Manufacturability analysis
aliases:
- design for manufacturing
- DFM
area: cad/manufacturing-process-planning
level: core
summary: Checks a design against the limits of a process, such as wall thickness, draft, tool access, hole depth and bend radius, and reports features that are hard to make.
see_also: [computer-aided-process-planning, feature-recognition, accessibility-cone, design-for-assembly, draft-angle-analysis, undercut-detection, casting-hot-spot-detection, medial-axis]
sources:
  - paper: doi:10.1007/BF01596601
    title: Satyandra K. Gupta, William C. Regli, Diganta Das and Dana S. Nau, Automated manufacturability analysis, a survey, Research in Engineering Design 9(3), 1997, 168 to 190
    locator: the split into direct (rule-based) and indirect (plan-based) approaches, and the kinds of rating, from a yes or no answer to an estimate of time and cost
  - paper: doi:10.1016/0010-4485(95)96797-p
    title: Satyandra K. Gupta and Dana S. Nau, Systematic approach to analysing the manufacturability of machined parts, Computer-Aided Design 27(5), 1995, 323 to 342
    locator: a plan-based analysis that makes the alternative operation plans of a machined part and rates the part by its best plan
  - book: doi:10.1201/9781420089288
    title: Geoffrey Boothroyd, Peter Dewhurst and Winston Knight, Product Design for Manufacture and Assembly, 3rd edition, CRC Press, 2010
    locator: the chapters on design for machining, injection molding, sheet metal working and casting, with the design rules and cost models of each process
---

Manufacturability analysis checks a design against the limits of a manufacturing process and reports the features that are hard, costly or impossible to make. Typical checks are the thickness of a wall, the draft of a molded face, the access of a tool to a feature, the depth of a hole against its diameter, the radius of an inside corner against the tool, and the radius of a bend against the sheet thickness. The output is a list of problems, each tied to a feature, and often a rating of the whole part. Design for manufacturing (DFM) is the name of the wider practice: the designer takes the process into account while the part is still easy to change. The analysis is the tool of that practice, the step that a computer can do on the model.

## In plain words

A designer can draw a part that no shop can make, or that only a slow and costly process can make. A hole may be too deep and too thin for a drill. A pocket may have a sharp inside corner that no round cutter can reach. A molded part may have a face with no slope, so it sticks in the mold. These problems are cheap to fix on the drawing and costly to fix after the tools are made.

Manufacturability analysis looks at the model of the part and finds such problems early. One kind of analysis checks the part against a list of rules for a process. Another kind tries to plan how the part would be made and reports the cost or the time of the best plan. Both point the designer to the feature that causes the trouble.

## The idea

**Direct and plan-based analysis.** Gupta, Regli, Das and Nau (1997) split the methods into two kinds.

- *Direct* (rule-based) analysis checks each feature against rules of the process, with no plan. A rule has a test and a limit, for example "the depth of a drilled hole is at most $k$ times its diameter". It is fast and easy to explain, but the rules do not see how features interact, and a part can pass all rules and still need a costly plan.
- *Indirect* (plan-based) analysis makes one or more process plans for the part, as a [process planning](/computer-aided-process-planning/) system does, and rates the part by its best plan. Gupta and Nau (1995) make all alternative operation plans of a machined part and keep the best. This sees the interactions, such as a feature that adds a whole setup, but it is slower and needs a planner model.

**What is checked.** The checks depend on the process. Each check needs a geometric query on the model:

| process | typical check | geometric query |
|---|---|---|
| machining | tool access to each face of a feature | the [accessibility cone](/accessibility-cone/) of the feature |
| machining | inside corner radius against the tool radius | corner radii of the [features](/feature-recognition/) |
| machining | hole depth against diameter | hole features and their sizes |
| injection molding | draft on faces parallel to the pull | [draft angle analysis](/draft-angle-analysis/) |
| injection molding, casting | regions that lock the part in the mold | [undercut detection](/undercut-detection/) |
| molding, casting | thin and thick walls | local thickness, for example from the [medial axis](/medial-axis/) |
| casting | thick regions that solidify last | [hot spot detection](/casting-hot-spot-detection/) |
| sheet metal | bend radius, hole near a bend, a bend sequence with no collision | [bend sequence planning](/bend-sequence-planning/) |

**The rating.** Gupta, Regli, Das and Nau (1997) also sort the outputs. A *binary* rating says whether the part can be made at all. A *qualitative* rating gives a grade, such as poor, fair or good. A *quantitative* rating gives a number: an abstract score, or an estimate of the time or the cost. Time and cost are the most useful to a designer, since they compare two designs directly, but they need a process model.

**Feedback.** A good analysis does more than reject. It names the feature and the rule, and it can suggest a change, such as a larger corner radius or a draft of a few degrees. Design for assembly is the companion analysis for the assembly of the parts, and it has [its own page](/design-for-assembly/). Boothroyd, Dewhurst and Knight (2010) treat the two together.

**Limits.** Each rule holds for a process, a machine and a shop, so the limits in a rule set are local choices, not constants of nature. The analysis can only find problems that its rules or its planner model cover.

## Examples

**Rule checks on a machined bracket.** A shop sets two rules for its tools: a drilled hole must have depth at most 10 times its diameter, and an end mill must have a reach of at most 4 times its diameter. These limits are assumptions of this example, not standard values. The part has two features:

- A hole of diameter 3 mm and depth 40 mm. The ratio is $40/3 = 13.3 > 10$, so the rule flags it. Fixes: make the hole wider, make it shallower, or plan a special deep-hole process.
- A pocket of depth 30 mm with inside corners of radius 2 mm. A cutter that reaches 30 mm has diameter at least $30/4 = 7.5$ mm, so radius at least 3.75 mm. A round cutter of radius $r$ leaves an inside corner of radius at least $r$, and $3.75 > 2$, so the rule flags the corners. Fixes: a corner radius of at least 3.75 mm, a shallower pocket, or a second process such as electrical discharge machining for the corners.

**A plan-based check of the same bracket.** Suppose the pocket opens to the top and the hole is on a side face. The rules above pass both features after the fixes. A plan-based analysis also groups the features into setups and finds that the hole needs a second setup, with a new fixture and a new datum. If the hole can move to the top face with no change to its function, the plan needs one setup. No single feature rule sees this, because the cost comes from the two features together.

**Draft on a molded box.** An open box is molded with the pull along $+z$. The analysis computes the angle of each face normal to the pull. The four side walls are at 90 degrees, so their draft is zero, and the part would drag on the mold when it is ejected. The report flags the four walls, and the designer tilts them by a small draft angle. The [draft angle analysis](/draft-angle-analysis/) page gives the test.

## Where it is used

- **CAD systems.** Commercial CAD tools have checks for molding draft and thickness, for sheet metal bends and for machining access, run on the model as the designer works.
- **Cost estimates.** Quantitative ratings give a cost per part at the design stage, and they let a designer compare two versions of a part.
- **Process selection.** The same checks, run for several processes, show which process suits a part: for example machining for a few parts and molding for many.
- **Process planning.** Plan-based analysis shares its model with [computer-aided process planning](/computer-aided-process-planning/), and a failed plan is itself a report of a manufacturability problem.

There are no standard benchmarks for manufacturability analysis. Each system is shown on its own test parts and its own rule set, so the results cannot be compared from paper to paper.

## References
