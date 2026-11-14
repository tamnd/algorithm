---
tag: W2ATK6
kind: technique
slug: design-for-assembly
name: Design for assembly
aliases:
- Boothroyd-Dewhurst method
- DFA method
area: cad/mechanism-and-assembly-design
level: intro
summary: Boothroyd and Dewhurst's analysis that asks whether each part must be separate and scores its handling and insertion time, to cut part count and cost.
see_also: [assembly-sequence-planning, manufacturability-analysis, disassembly-sequence-planning, liaison-graph, tolerance-stack-up, computer-aided-process-planning, fixture-planning]
sources:
  - book: doi:10.1201/9781420089288
    title: Geoffrey Boothroyd, Peter Dewhurst and Winston Knight, Product Design for Manufacture and Assembly, 3rd edition, CRC Press, 2010
    locator: the chapters on manual assembly, with the three questions for the minimum number of parts, the tables of handling and insertion times, and the design efficiency
  - paper: doi:10.1016/0010-4485(94)90082-5
    title: Geoffrey Boothroyd, Product design for manufacture and assembly, Computer-Aided Design 26(7), 505 to 520 (1994)
    locator: the method and a case study of a redesign with fewer parts
---

Design for assembly is a review of a product design that tries to make the product cheaper to put together. It has two steps. First, it asks three questions about each part to find the parts that must be separate, and so gives the theoretical minimum number of parts. Every other part is a candidate to remove or to combine with a neighbour. Second, it gives each part a time to handle it and a time to insert it, read from tables of measured times, and adds them. The two results give the design efficiency, the ideal time of the minimum parts divided by the estimated total time. Boothroyd and Dewhurst made the method from time studies of manual assembly, and the efficiency is an empirical index, not a proved quantity. The method changes the design. The [assembly sequence planning](/assembly-sequence-planning/) problem takes the design as fixed and finds an order to build it.

## In plain words

Each part of a product costs time on the line. A worker must pick it up, turn it the right way and put it in place. Screws cost the most, because each one must also be turned.

The method looks at each part and asks: does this part really need to be a separate part? If it does not move against the others, is not of a different material, and is not needed apart for building or repair, then it could be part of a neighbour. A plastic base can have its bracket and its clips molded on.

Then the method gives each part a time from tables, adds the times, and compares the total with an ideal. A low score shows where to work: remove parts, and make the rest easy to pick up and to put in.

## When it applies

- **Manual assembly of a product with many small parts.** The tables of times come from studies of workers who assemble parts by hand at a bench. The questions and the idea of fewer parts apply more widely, but the times do not.
- **Early in design.** The method needs only a list of parts and a rough idea of their shape and of how they go together. The largest savings come before the tools for the parts are made.
- **A comparison of designs.** The scores are most useful to compare two designs of the same product, scored by the same tables.

**Motion model and hand model.** The method does not compute motions. It scores each insertion by its kind, read from the shape: whether the part goes straight in from above, must be held down, needs a turn of a screw, or meets an obstruction. The hand model is linear: the parts are added one at a time to one growing assembly, in an order that the analyst chooses, and each part is picked up with one hand or with two. The answers to the three questions depend on that order, because each question is about the parts already assembled.

## The template

1. **List the parts** in an assembly order. Count each fastener as a part.
2. **Ask the three questions** for each part, in that order. When the part is in operation, does it move relative to all the parts already assembled? Must it be of a different material from those parts, or be isolated from them? Must it be separate from them because otherwise a necessary assembly or disassembly of other parts would be impossible? The first part, the base, counts as necessary.
3. **Count the minimum.** $N_{\min}$ is the number of parts with at least one yes. The parts with three answers of no are candidates to remove or to combine.
4. **Estimate the times.** For each part, read a handling time $t_h$ from its size, its symmetry and how easy it is to grasp, and an insertion time $t_i$ from its access, its alignment and its fastening. The method gives tables of these times. The total time is $t_{\text{total}} = \sum (t_h + t_i)$ over all parts.
5. **Compute the efficiency.**
$$E = \frac{3\, N_{\min}}{t_{\text{total}}},$$
with times in seconds. The 3 s is the ideal time that Boothroyd and Dewhurst take for one part with no difficulty of handling or insertion.
6. **Redesign and repeat.** Remove or combine the candidates, change the parts with long times, and score the new design.

**What is measured and what is not.** The three questions are rules of design, not results of an analysis. The times in the tables are averages from time studies, and the 3 s ideal is a number taken from those studies. So $E$ is an empirical index. It is a good guide to compare designs, but it does not predict a cost exactly, and no theorem bounds it. A score such as $E = 0.6$ has no meaning outside the tables that made it.

## Classic examples

**A small housing, with made-up times.** The times in this example are invented for the exercise. They are not values from the tables of Boothroyd and Dewhurst. A sensor has a plastic base, a circuit board, a metal bracket that holds the board, a spacer, four screws for the board, a cover and two screws for the cover. The order is base, spacer, bracket, board, four screws, cover, two screws.

| part | number | move? | material? | separate? | needed | time per part (s) |
|---|---|---|---|---|---|---|
| base | 1 | first part | | | 1 | 3 |
| spacer | 1 | no | no | no | 0 | 5 |
| bracket | 1 | no | no | no | 0 | 7 |
| board | 1 | no | yes | no | 1 | 6 |
| board screw | 4 | no | no | no | 0 | 8 |
| cover | 1 | no | no | yes, for service | 1 | 5 |
| cover screw | 2 | no | no | no | 0 | 8 |

- **Before.** $N_{\min} = 3$ of 11 parts, and $t_{\text{total}} = 3 + 5 + 7 + 6 + 32 + 5 + 16 = 74$ s, so $E = 9/74 \approx 0.12$.
- **After.** Mold the spacer and the bracket into the base, let the board snap into the base, and let the cover snap on. Three parts are left, with made-up times of 3, 6 and 4 s, so $t_{\text{total}} = 13$ s and $E = 9/13 \approx 0.69$.
- **What the example shows.** The fasteners took 48 of the 74 s. Most of the gain comes from parts that the questions mark as candidates, and not from faster insertion of the parts that stay.

The cover is needed for service, so the answer to the third question is yes. A snap fit that cannot be opened again would make the cover a candidate, and would also make the board hard to repair, which the [disassembly](/disassembly-sequence-planning/) of the product must allow.

## Variations

- **Automatic and robot assembly.** The same questions apply, but the times are replaced by the cost of feeders, of orienting the parts and of the robot cycle.
- **Design for manufacture and assembly.** The assembly score is set against the cost of making each part, because a combined part can cost more to mold or to machine than the parts it replaces. [Manufacturability analysis](/manufacturability-analysis/) checks those parts.
- **Other scoring systems.** Other companies and schools give penalty points for each difficult operation instead of times. They share the idea of fewer and simpler parts, and their scores cannot be compared with $E$.
- **Disassembly and service.** The same review can be run on the steps of a repair or of recycling, with the questions asked about the parts that must come out.

## Pitfalls

- **The order changes the answers.** The questions are about the parts already assembled, so a different order can change $N_{\min}$. Keep the order fixed when two designs are compared.
- **Fewer parts can cost more.** A combined part can need a costly mold or a tight tolerance. The [tolerance stack-up](/tolerance-stack-up/) of the new part must still close.
- **Service is not free.** Removing every screw can make a product that cannot be opened for repair. The third question must include service, as in the example.
- **The efficiency is not a probability or a cost.** It is a ratio with an empirical constant. Do not compare scores from different tables or from different methods.
- **The tables are for manual work.** For a robot cell, the times of the tables do not apply.

## Exercises

1. A lamp has a base, a stem screwed to the base with one screw, a socket in the stem, a shade and a ring that holds the shade. Ask the three questions in that order and find $N_{\min}$. Which parts are candidates?
2. In the example above, the designer keeps the two cover screws for service and removes all other candidates. With the made-up times, the screws take 8 s each and the other parts take 3, 6 and 5 s. Compute $t_{\text{total}}$ and $E$.
3. Show that $E$ can change when the list of parts does not change, by an example where a different assembly order changes the answer to one of the three questions.
4. A design has $N_{\min} = 10$ and $t_{\text{total}} = 150$ s. A redesign removes 5 candidate parts of 6 s each and makes no other change. Compute $E$ before and after. Which change in the redesign could make the product more expensive in spite of the higher $E$?

*Answers.* 2: $t_{\text{total}} = 3 + 6 + 5 + 16 = 30$ s and $E = 9/30 = 0.3$. 4: $E = 30/150 = 0.2$ before and $30/120 = 0.25$ after. A combined part can need a more costly mold or a tighter tolerance.

## References
