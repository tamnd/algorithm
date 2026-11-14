---
tag: 6GR8VE
kind: technique
slug: rule-based-constraint-solving
name: Rule-based constraint solving
aliases:
- knowledge-based constraint solving
area: cad/geometric-constraint-solving
level: core
summary: Solves sketches by rewrite rules that derive new known elements from known ones, as in Bruderlin and Sunde, a logic form of constructive solving.
prereqs: [constructive-constraint-solving, forward-chaining]
see_also: [fudos-hoffmann-reduction, production-system, rete-algorithm, datalog, newman-lemma, ruler-and-compass-constructibility, circle-circle-intersection, root-identification-problem]
sources:
  - paper: "G. Sunde, Specification of shape by dimensions and other geometric constraints, in M. J. Wozny, H. W. McLaughlin and J. L. Encarnação (editors), Geometric Modeling for CAD Applications, North-Holland, 199 to 213, 1988"
    locator: the sets of points with fixed distances and the sets of segments with fixed angles, and the rules that merge them (general locator)
  - paper: doi:10.1016/0010-4485(92)90040-H
    title: Anne Verroust, François Schonek and Dieter Roller, Rule-oriented method for parameterized computer-aided design, Computer-Aided Design 24(10), 531 to 540, 1992
    locator: a rule-based solver for dimensioned drawings in parametric CAD (general locator)
  - paper: doi:10.1016/0304-3975(93)90324-M
    title: Beat Brüderlin, Using geometric rewrite rules for solving geometric problems symbolically, Theoretical Computer Science 116(2), 291 to 303, 1993
    locator: the rewrite rules on geometric predicates, the derivation of ruler and compass constructions, and the proof of completeness and termination by local confluence and a well-founded ordering of terms (general locator)
  - paper: "Robert Joan-Arinyo and Antoni Soto-Riera, A correct rule-based geometric constraint solver, Computers and Graphics 21(5), 599 to 609, 1997"
    locator: a rule-based solver for points and lines with distance and angle constraints, and the proof that it is correct (general locator)
---

Rule-based constraint solving, also called knowledge-based solving, writes the geometry of a sketch as a set of rules. A rule says: if these elements are already known relative to each other, and these constraints hold between them, then this new element, or this larger group, is known too, and here is how to construct it. An inference engine applies the rules by [forward chaining](/forward-chaining/) until no rule adds anything. The list of rules that fired is a construction plan, and the solver then runs the plan with the real dimension values, mostly by ruler and compass steps such as a [circle-circle intersection](/circle-circle-intersection/). It is the logic form of [constructive constraint solving](/constructive-constraint-solving/): the analysis is symbolic reasoning about which elements are fixed, and the construction is the numeric evaluation. Sunde (1988) solved sketches by rules that merge sets of points with fixed distances and sets of segments with fixed angles, and Brüderlin (1993) wrote the rules as a rewrite system on geometric predicates and proved it complete and terminating.

## In plain words

A draftsman who gets a dimensioned sketch does not solve equations. He reasons: these two points are 4 apart, so I can draw them. This third point is 5 from the first and 3 from the second, so I can find it with two arcs. Now these three are fixed, so this fourth point can be found the same way. Each step is a small piece of knowledge, used again and again.

A rule-based solver writes that knowledge down as rules and lets a program apply them. It keeps a list of what is known. It looks for a rule whose conditions are met, adds what the rule concludes, and writes down the step. When no rule helps any more, either the whole sketch is known, and the steps form a recipe to draw it, or some part is left over, which the rules cannot handle.

## When it applies

- The sketch is in the plane, or in space with a small set of shapes, and its elements are points, lines, circles and the like, with constraints such as distances, angles, incidence, tangency and parallelism.
- Most of the sketch can be built step by step: each new element, or each new rigid group, is fixed by a few constraints to elements that are already fixed. This is the case for most engineering drawings, where a dimension is placed so that a draftsman can construct the part.
- The constructions are of low degree. The usual rules use only lines and circles, so the solutions are [constructible by ruler and compass](/ruler-and-compass-constructibility/), and each step has finitely many solutions, often two.
- The rules see only which constraints there are, not their values. So, as with all graph methods, a value that makes the geometry special, such as three points on a line, is not seen by the analysis and must be caught by the construction.

## The template

The state is a set of *facts*. A fact is a given constraint, or a derived statement such as "the points of the set $S$ are fixed relative to each other", in the style of Sunde's sets of points with fixed distances. A rule has premises, which are facts with variables, and one conclusion, together with a construction that computes the new element from the old ones.

```pseudo id=template
RULE-SOLVE(entities, constraints, rules)
L1  facts ← the constraints, and one fact "fixed(x)" for each entity that the user fixes
L2  plan ← an empty list
L3  repeat
L4      find a rule r and facts f1, …, fk that match its premises, with a conclusion g that is new   ▷ ⟨MATCH⟩
L5      if there is none then leave the repeat
L6      add g to facts;  append (r, f1, …, fk, g) to plan                                            ▷ ⟨FIRE⟩
L7  if some entity is not fixed relative to the others then return ⟨FALLBACK⟩(facts)
L8  for each step (r, f1, …, fk, g) of plan, in order do
L9      compute the candidate placements of g from the placements of f1, …, fk by the construction of r   ▷ ⟨CONSTRUCT⟩
L10     keep one of them   ▷ ⟨SELECT⟩
L11 return the placements
```

The holes are these.

- **RULES.** The knowledge base. A typical set for points and distances in the plane has two rules. *Pair*: two points with a distance form a rigid set. *Triangle*: three rigid sets that pairwise share one point, at three distinct points, merge into one rigid set; the construction places the three shared points as a triangle, by a circle-circle intersection, and moves the three sets onto it. Sunde's rules also merge sets of segments with fixed angles, and Joan-Arinyo and Soto-Riera add rules for sets of points and lines with point-line distances.
- **MATCH.** The search for a rule that can fire. A naive search tries every rule on every tuple of facts; a [production system](/production-system/) uses the [Rete algorithm](/rete-algorithm/) to update the matches as facts are added.
- **FIRE.** The control. When several rules can fire, the engine picks one by priority or by order. If the rules are *monotone*, see below, the choice does not change the result.
- **CONSTRUCT.** The numeric step of each rule: a circle-circle intersection, a line-circle intersection, a rotation by a given angle. It must check its input: two circles that do not meet give no real solution.
- **SELECT.** Each construction can have several solutions. Choosing the one that matches the draft is the [root identification problem](/root-identification-problem/).
- **FALLBACK.** What to do when the rules stop early: report the parts that are still free, ask the user for more dimensions, or solve the remaining clusters together with a numeric method.

**Why the order does not matter for monotone rules.** Call the rules *monotone* when they only add facts and a rule that can fire stays able to fire when more facts are added, as with [Horn clauses](/horn-clause/) and [Datalog](/datalog/). Let $\mathcal{F}$ be the finite set of all facts that can be written about the sketch.

*Claim.* For monotone rules, the loop of lines L3 to L6 stops after at most $|\mathcal{F}|$ firings, and its final set of facts is the same for every order of firing: it is the smallest set that contains the initial facts and is closed under the rules.

*Proof.* Each firing adds a new fact of $\mathcal{F}$, so there are at most $|\mathcal{F}|$ firings. A set is *closed* if every rule whose premises it contains has its conclusion in it as well. The intersection of closed sets that contain the initial facts is closed, since a rule whose premises lie in the intersection has them in every set, so its conclusion is in every set. Let $C$ be the smallest such set. Each derived fact lies in $C$, by induction on the firings: its premises lie in $C$ and $C$ is closed. When the loop stops, no rule can add a new fact, so the final set is closed and contains the initial facts, and therefore contains $C$. So it equals $C$. $\square$

A solver that *replaces* old facts, for example merges two rigid sets into one and forgets the two, is a rewrite system and not a monotone one. Then the result can depend on the order. The standard way out is to show that the rewrite system terminates and is locally confluent, which by [Newman's lemma](/newman-lemma/) makes it confluent, so every order gives the same final state. Brüderlin's rules are made complete and terminating in this way, by making them locally confluent and giving a well-founded order on the terms.

**Example.** Take four points $A, B, C, D$ with the distances $AB = 4$, $AC = 5$, $BC = 3$, $CD = 2$ and $BD = \sqrt{13}$, and the rules Pair and Triangle above.

| step | rule | premises | conclusion | construction |
|---|---|---|---|---|
| 1 to 5 | Pair | each distance | $\{A, B\}, \{A, C\}, \{B, C\}, \{C, D\}, \{B, D\}$ rigid | none yet |
| 6 | Triangle | $\{A, B\}, \{A, C\}, \{B, C\}$ | $\{A, B, C\}$ rigid | $A = (0, 0)$, $B = (4, 0)$, $C$ on the circles of radius 5 about $A$ and 3 about $B$ |
| 7 | Triangle | $\{A, B, C\}, \{B, D\}, \{C, D\}$ | $\{A, B, C, D\}$ rigid | $D$ on the circles of radius $\sqrt{13}$ about $B$ and 2 about $C$ |

At step 6 the circles meet at $C = (4, 3)$ and $C = (4, -3)$; take $(4, 3)$. At step 7 they meet at $(6, 3)$ and $(2, 3)$, the mirror images in the line $BC$. So the sketch has $2 \cdot 2 = 4$ solutions, two up to reflection of the whole. The engine could also have merged $\{B, C\}, \{C, D\}, \{B, D\}$ first into $\{B, C, D\}$, and then merged that with $\{A, B\}$ and $\{A, C\}$. The plan differs, but the final fact, that all four points are rigid, is the same, as the claim says.

## Classic examples

- **Sunde (1988).** Sets of points with fixed distances and sets of segments with fixed angles. Rules merge two sets when they share a point and are tied by a constraint, and the sketch is solved when one set holds everything. Only points and lines are handled.
- **Verroust, Schonek and Roller (1992).** A rule-oriented solver for dimensioned drawings in parametric CAD, which builds on the same kind of sets and merge rules as Sunde.
- **Brüderlin (1993).** A rewrite system on geometric predicates, such as distances and angles, that derives a symbolic ruler and compass construction for a configuration and reasons about congruence. He showed completeness and termination by local confluence and a well-founded ordering of the terms.
- **Joan-Arinyo and Soto-Riera (1997).** A rule-based solver for points and lines with distance and angle constraints, with a proof that the solver is correct, and with rules for point-line distances.
- **The graph form.** The [Fudos-Hoffmann reduction](/fudos-hoffmann-reduction/) uses the Triangle rule on the constraint graph, as a graph algorithm in $O(n^2)$ time instead of a general inference engine. The rules are the same; the matching is specialized.

## Variations

- **Expert system shells.** The rules are written for a general [production system](/production-system/) or in Prolog, and the engine is generic. This is easy to extend with new rules but slow on large sketches, since matching is the main cost.
- **Graph-constructive solvers.** The rules become patterns on the [constraint graph](/geometric-constraint-graph/), found by graph algorithms, as in Fudos and Hoffmann and in [Owen's decomposition](/owen-triconnected-decomposition/). These are faster and easier to prove complete for their class.
- **Local propagation.** The simplest rules fix one unknown of one constraint at a time, as in [local propagation](/local-propagation-solving/). They fail on the cycles that the Triangle rule handles.
- **Hybrid solvers.** When the rules stop with several rigid sets, a numeric method, such as [Newton's method](/newton-method-for-systems/), solves the rest. A [DR-plan](/dr-plan/) makes this systematic: the rules give the small nodes and a general solver the large ones.

## Pitfalls

- **Too many facts.** Facts about every rigid subset can number $2^n$. Keep only the maximal rigid sets and merge them in place, but then the rules are a rewrite system, and their confluence must be shown, as above.
- **Stopping is not a verdict.** When the rules stop with several rigid sets, the sketch may still be well-constrained: the prism and $K_{3,3}$ are rigid in the plane, but no Triangle rule applies to them. The rules are complete only for the class they were made for. Use a count, such as [Laman's theorem](/laman-theorem/) for points and distances, before saying that a sketch is under-constrained.
- **The analysis does not see the values.** A rule can fire, and its construction still fail: two circles that do not meet, or meet in one point, or a triangle with three collinear points. Check each construction, and report the step that fails.
- **Redundant and conflicting constraints.** A rule that derives a fact already known, such as a distance between two points of one rigid set, signals a redundant constraint. Its value must be checked against the construction; a different value is a conflict, not a new fact.
- **Choice of solutions.** Each step has several solutions, and a local choice can make a later step impossible. Keep the orientation of the draft at each step, and allow going back.

## Exercises

1. Write rules for points and lines in the plane, with point-point distances, line-line angles and point-on-line incidence, and give the construction of each rule.
2. Add a rule Overlap: two rigid sets that share two points merge into one. Show that Pair, Triangle and Overlap, applied in place with merging, give the same final rigid sets for every order. Show also that without Overlap the order can matter.
3. Find a sketch of six points with $2 \cdot 6 - 3$ distances that is rigid but on which Pair and Triangle stop with more than one rigid set.
4. Give a set of two rewrite rules whose result depends on the order in which they fire, and add a rule that makes it confluent.
5. In the example, give the four solutions and show that they form two pairs of mirror images.

## References
