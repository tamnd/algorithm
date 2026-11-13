---
tag: CJPE4E
kind: concept
slug: ramification-problem
name: Ramification problem
area: games-and-search/planning
level: intro
summary: Deriving the indirect consequences of an action's direct effects.
prereqs: [state-space]
see_also: [frame-problem, qualification-problem, conditional-effects, strips, pddl, datalog, fixed-point, invariant]
sources:
  - paper: "Jeffrey J. Finger, Exploiting Constraints in Design Synthesis, PhD thesis, Stanford University, 1987"
    title: Finger 1987
    locator: the discussion of ramifications of actions (general locator)
  - paper: doi:10.1016/0004-3702(88)90011-2
    title: "Matthew L. Ginsberg and David E. Smith, Reasoning about action I: A possible worlds approach, Artificial Intelligence 35(2) (1988)"
    locator: pp. 165 to 195 (indirect effects from domain constraints by the nearest possible worlds)
  - paper: "Stefan Edelkamp and Jörg Hoffmann, PDDL2.2: The language for the classical part of the 4th International Planning Competition, Technical Report 195, Institut für Informatik, Universität Freiburg, 2004"
    title: Edelkamp and Hoffmann 2004
    locator: the section on derived predicates (general locator)
  - book: isbn:9780262193849
    title: Murray Shanahan, Solving the Frame Problem, A Mathematical Investigation of the Common Sense Law of Inertia, MIT Press, 1997
    locator: the chapters on domain constraints and ramifications (general locator)
---

The ramification problem is the problem of finding all the indirect effects of an action: the facts that change because the direct effects, together with the laws of the domain, force them to change. If a robot carries a briefcase out of a room, the papers in the briefcase leave the room too, although the action only moves the briefcase. Finger (1987) named the problem. It is one of three problems with describing actions, beside the [frame problem](/frame-problem/) (what does not change) and the [qualification problem](/qualification-problem/) (when the action is possible).

## In plain words

Some changes happen as a side effect of other changes. Put a block on another block, and the lower block is no longer free to take a new block. Turn on both switches of a two-switch lamp, and the lamp lights up. A list of what an action does directly misses these side effects, unless someone works them out and writes them into every action. The ramification problem is how to get the side effects from a few general rules about the world, and to get them right, so that the rules do not also produce changes that should not happen.

## The idea

### Domain constraints

A domain constraint, or state constraint, is a law that holds in every state, such as

- $\mathit{on}(x, y) \to \lnot \mathit{clear}(y)$: a block with another block on it is not clear;
- $\mathit{in}(o) \land \mathit{at\text{-}b}(l) \to \mathit{at}(o, l)$: an object in the briefcase is where the briefcase is;
- $\mathit{light} \leftrightarrow \mathit{up}_1 \land \mathit{up}_2$: the lamp is on exactly when both switches are up.

If an action states only its direct effects, the state after it must still satisfy the constraints, and the facts that change to restore them are the ramifications. The question is which facts change. The frame problem says "as little as possible", and the constraints say "enough to be consistent"; the two pull against each other.

### Minimal change is not enough

Ginsberg and Smith (1988) took the result of an action to be the possible worlds nearest to the old state that satisfy the direct effects and the constraints. The lamp shows the limit of that idea. Start with switch 1 down, switch 2 up and the lamp off, and flip switch 1 up. Two states each differ from the old state in one fact beside the direct effect: in one the lamp turns on, in the other switch 2 flips down and the lamp stays off. Both are nearest, but only the first is right, because switches cause the lamp to change, not the other way round. Later theories of action add causal rules for this reason: a constraint is read as "a change of the switches causes a change of the lamp", with a direction.

### Ramifications in planning languages

[STRIPS](/strips/) has no domain constraints, so every ramification must be written by hand into the actions that cause it. The STRIPS action $\mathit{stack}(x, y)$ deletes $\mathit{clear}(y)$ for this reason: the fact is an indirect effect of putting $x$ on $y$. There are three ways to state ramifications more compactly:

- [Conditional effects](/conditional-effects/). The briefcase action $\mathit{move}(l, m)$ has, for each object $o$, the effect "when $\mathit{in}(o)$, add $\mathit{at}(o, m)$ and delete $\mathit{at}(o, l)$". The constraint is compiled into each action, one effect for each object.
- Derived predicates (PDDL2.2, Edelkamp and Hoffmann 2004). A derived predicate is defined by rules over the basic facts, for example $\mathit{above}(x, y)$ as the transitive closure of $\mathit{on}$. Actions never change it; its value in each state is the least [fixed point](/fixed-point/) of the rules, as in [Datalog](/datalog/). This handles ramifications that are definitions, but not ones that need a direction of causation between basic facts.
- Invariants. Many constraints are already [invariants](/invariant/) of a correct STRIPS domain, such as "exactly one of $\mathit{handempty}$ and $\mathit{holding}(x)$ for the blocks $x$". The [SAS+](/sas-plus/) translation finds them and turns them into multi-valued variables, so the ramifications become a single change of one variable value.

## Examples

- The blocks world. Moving $A$ onto $B$ directly changes $\mathit{on}(A, B)$. The ramifications are $\lnot \mathit{clear}(B)$, $\mathit{clear}$ of the block $A$ was on, and, for a derived $\mathit{above}$, the facts $\mathit{above}(A, z)$ for $B$ and for every block $z$ below $B$. A STRIPS move lists the first two and cannot express the third except through extra facts kept up to date by every action.
- The briefcase. Moving the briefcase moves each object inside it; the number of these ramifications depends on the state.
- The two-switch lamp above, where the direction of the constraint matters.
- A database with integrity constraints. Deleting a customer row can cascade to delete the customer's orders. The cascade is a ramification, stated once in the schema instead of in each delete.

## Where it is used

- Planning: derived predicates in PDDL2.2 and later, conditional effects, and domain axioms in planners that support them.
- Logics of action: causal rules in the situation calculus and in the event calculus, which compute the indirect effects of an event.
- Databases and spreadsheets: triggers, cascades and derived values propagate the consequences of an update.
- Simulation and games: rule engines that apply physics or game laws after each move compute ramifications.

## References
