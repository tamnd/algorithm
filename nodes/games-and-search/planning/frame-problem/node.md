---
tag: 39FTT0
kind: concept
slug: frame-problem
name: Frame problem
aliases:
- frame axioms
area: games-and-search/planning
level: intro
summary: Specifying which facts an action leaves unchanged, without listing every non-effect.
prereqs: [state-space]
see_also: [strips, qualification-problem, ramification-problem, closed-world-assumption, conditional-effects, satplan, separation-logic, hoare-logic]
sources:
  - paper: "John McCarthy and Patrick J. Hayes, Some philosophical problems from the standpoint of artificial intelligence, in B. Meltzer and D. Michie (editors), Machine Intelligence 4, Edinburgh University Press, 1969"
    title: McCarthy and Hayes 1969
    locator: pp. 463 to 502 (the situation calculus and the frame problem); reprinted in Readings in Artificial Intelligence, 1981, pp. 431 to 450
  - paper: doi:10.1016/B978-0-12-450010-5.50026-8
    title: "Raymond Reiter, The frame problem in the situation calculus: A simple solution (sometimes) and a completeness result for goal regression, in V. Lifschitz (editor), Artificial Intelligence and Mathematical Theory of Computation, Academic Press, 1991"
    locator: pp. 359 to 380 (successor state axioms)
  - book: isbn:9780262193849
    title: Murray Shanahan, Solving the Frame Problem, A Mathematical Investigation of the Common Sense Law of Inertia, MIT Press, 1997
    locator: the chapters on the situation calculus, on nonmonotonic solutions and on the event calculus (general locator)
  - paper: doi:10.1016/0004-3702(71)90010-5
    title: "Richard E. Fikes and Nils J. Nilsson, STRIPS: A new approach to the application of theorem proving to problem solving, Artificial Intelligence 2(3-4) (1971)"
    locator: pp. 189 to 208 (add and delete lists in place of frame axioms)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: the discussion of the frame problem in the chapter on logical agents and in Chapter 11 (general locator)
---

The frame problem is the problem of saying what an action does not change, without writing one axiom for each pair of an action and a fact it leaves alone. McCarthy and Hayes (1969) found it when they described actions in first-order logic, in the situation calculus: effect axioms say what changes, but nothing in the logic says that the rest stays the same, so a reasoner cannot conclude that moving a block leaves its color as it was. The [STRIPS](/strips/) model avoids the problem by a rule outside the logic, that an action changes only the facts in its add and delete lists. Reiter's successor state axioms solve it inside the logic for a large class of domains.

## In plain words

When you move a cup, you know that the table stays where it is, the lights stay on and the cup keeps its color. A computer that reasons from rules does not know this unless it is told. If the rules only say what each action changes, the computer cannot prove that anything else is still true afterwards. Telling it, one rule for each action and each thing the action does not touch, takes a huge number of rules. The frame problem is how to say "everything else stays the same" in a short and correct way.

## The idea

### Effect axioms are not enough

In the situation calculus a fact that can change, a fluent, has an extra argument for the situation, and $\mathit{do}(a, s)$ is the situation after action $a$ in situation $s$. An effect axiom for the blocks world:

$$\mathit{clear}(b, s) \land \mathit{clear}(y, s) \land \mathit{on}(b, x, s) \to \mathit{on}(b, y, \mathit{do}(\mathit{move}(b, x, y), s)).$$

Add a fluent $\mathit{color}(b, c, s)$ and an action $\mathit{paint}(b, c)$. Nothing in the effect axioms implies $\mathit{color}(A, \mathit{red}, \mathit{do}(\mathit{move}(A, B, C), s))$ from $\mathit{color}(A, \mathit{red}, s)$: there are models in which the move repaints the block. To exclude them one adds frame axioms, such as

$$\mathit{color}(b, c, s) \to \mathit{color}(b, c, \mathit{do}(\mathit{move}(b', x, y), s)).$$

### The count

With $|A|$ actions and $|F|$ fluents, frame axioms are needed for most of the $|A| \cdot |F|$ pairs, in both directions (a true fact stays true, a false fact stays false). Take the move [blocks world](/blocks-world/) with 3 blocks: 18 ground actions and 12 facts ($6$ $\mathit{on}$, $3$ $\mathit{ontable}$, $3$ $\mathit{clear}$). The 6 moves from block to block change 4 facts each, and the 12 moves to or from the table change 3 each, so $6 \cdot 8 + 12 \cdot 9 = 156$ pairs of an action and a fact are unchanged, and each needs a frame axiom in each direction, 312 in all. The STRIPS lists of the same domain have $6 \cdot 4 + 12 \cdot 3 = 60$ entries in total. The gap grows with the domain: frame axioms grow as $|A| \cdot |F|$, effect lists as the total size of the changes.

### Three ways out

- A rule outside the logic. STRIPS computes the next state as $(s \setminus \mathit{del}(a)) \cup \mathit{add}(a)$: facts outside the lists keep their values. This is the STRIPS assumption, and the [closed world assumption](/closed-world-assumption/) on states makes it complete. It is a sound solution as long as every effect of an action is in its lists.
- Successor state axioms (Reiter 1991). Assume that the effect axioms list all the ways a fluent can change (the causal completeness assumption). Then each fluent $F$ gets one axiom

  $$F(\vec x, \mathit{do}(a, s)) \leftrightarrow \gamma^+_F(\vec x, a, s) \lor \big(F(\vec x, s) \land \lnot \gamma^-_F(\vec x, a, s)\big),$$

  where $\gamma^+_F$ says when $a$ makes $F$ true and $\gamma^-_F$ when it makes $F$ false. With unique names axioms for actions, this gives one axiom for each fluent, not one for each pair. It is the same formula as the STRIPS successor, read fact by fact, and as the regression rule for [conditional effects](/conditional-effects/).
- Nonmonotonic persistence. Say "fluents normally persist" as a default, and minimize change by circumscription or a default logic. These logics found problems of their own: in the Yale shooting problem of Hanks and McDermott, the minimal-change models include one in which a loaded gun becomes unloaded while the agent waits, so the target survives. Later theories, such as the event calculus, avoid this anomaly by minimizing which events occur and what they cause, not the change itself.

### What it is not

The frame problem is about the non-effects of an action. Two related problems are about the other parts of an action description: the [qualification problem](/qualification-problem/) about its preconditions, which can never all be listed, and the [ramification problem](/ramification-problem/) about its indirect effects, which follow from the direct effects and the laws of the domain.

## Examples

- Blocks and colors. Moving $A$ onto $C$ changes $\mathit{on}(A, B)$, $\mathit{on}(A, C)$, $\mathit{clear}(B)$ and $\mathit{clear}(C)$. With $k$ colors and the fluent $\mathit{color}(b, c)$, each of the 18 moves needs $3k$ more frame axioms, one for each block and color, while its STRIPS lists do not change.
- A SAT encoding of planning. [SATPLAN](/satplan/) has variables $f_t$ for each fact $f$ and step $t$, and $a_t$ for each action. Explanatory frame axioms state, for each fact, $f_t \land \lnot f_{t+1} \to \bigvee \{a_t : f \in \mathit{del}(a)\}$ and $\lnot f_t \land f_{t+1} \to \bigvee \{a_t : f \in \mathit{add}(a)\}$: a fact changes only if some action that changes it occurs. This is the successor state idea in propositional form, with $2 |F|$ clauses for each step instead of $|A| \cdot |F|$.
- A database transaction. An update that changes one row leaves all other rows as they were. The database does not state this; it is built into the update operation, as the STRIPS assumption is built into the successor.

## Where it is used

- Planning languages: [STRIPS](/strips/) and [PDDL](/pddl/) adopt the STRIPS assumption, so a domain lists only the changes.
- Logics of action: the situation calculus with successor state axioms underlies the agent language Golog and the theory of [goal regression](/goal-regression/), which Reiter proved complete for such theories.
- Program verification: a Hoare triple $\{P\}\ C\ \{Q\}$ says nothing about the variables that $C$ does not mention, and verification languages add "modifies" clauses. The frame rule of [separation logic](/separation-logic/) states that a command that works on one part of the heap leaves the disjoint rest unchanged; its name refers to the frame problem. See also [Hoare logic](/hoare-logic/).
- Model checking and SAT based verification: transition relations include frame conditions for the state variables a step does not assign.

## References
