---
tag: DM6GS3
kind: model
slug: pddl
name: Planning Domain Definition Language
aliases:
- PDDL
area: games-and-search/planning
level: intro
summary: Standard input language for planning domains and problems, used in the planning competitions.
prereqs: [strips, action-schema]
see_also: [grounding, classical-planning, conditional-effects, closed-world-assumption, international-planning-competition, temporal-planning, sas-plus, blocks-world]
sources:
  - paper: "Drew McDermott, Malik Ghallab, Adele Howe, Craig Knoblock, Ashwin Ram, Manuela Veloso, Daniel Weld and David Wilkins, PDDL, The Planning Domain Definition Language, Version 1.2, Technical Report CVC TR-98-003/DCS TR-1165, Yale Center for Computational Vision and Control, 1998"
    title: McDermott et al. 1998
    locator: the sections on requirements, domains, actions and problems (general locator)
  - paper: doi:10.1613/jair.1129
    title: "Maria Fox and Derek Long, PDDL2.1: An extension to PDDL for expressing temporal planning domains, Journal of Artificial Intelligence Research 20 (2003)"
    locator: the sections on numeric expressions, plan metrics and durative actions (general locator)
  - paper: "Stefan Edelkamp and Jörg Hoffmann, PDDL2.2: The language for the classical part of the 4th International Planning Competition, Technical Report 195, Institut für Informatik, Universität Freiburg, 2004"
    title: Edelkamp and Hoffmann 2004
    locator: the sections on derived predicates and timed initial literals (general locator)
  - paper: doi:10.1016/j.artint.2008.10.012
    title: "Alfonso E. Gerevini, Patrik Haslum, Derek Long, Alessandro Saetti and Yannis Dimopoulos, Deterministic planning in the fifth international planning competition: PDDL3 and experimental evaluation of the planners, Artificial Intelligence 173(5-6) (2009)"
    locator: pp. 619 to 668 (state trajectory constraints and preferences)
  - paper: "Håkan L. S. Younes and Michael L. Littman, PPDDL1.0: An extension to PDDL for expressing planning domains with probabilistic effects, Technical Report CMU-CS-04-167, Carnegie Mellon University, 2004"
    title: Younes and Littman 2004
    locator: the sections on probabilistic effects (general locator)
  - book: isbn:9783031004568
    title: Patrik Haslum, Nir Lipovetzky, Daniele Magazzeni and Christian Muise, An Introduction to the Planning Domain Definition Language, Springer (Synthesis Lectures on Artificial Intelligence and Machine Learning), 2019
    locator: the chapters on the STRIPS and ADL fragments and on the later extensions (general locator)
  - paper: doi:10.1016/0004-3702(94)00080-k
    title: "Kutluhan Erol, Dana S. Nau and V. S. Subrahmanian, Complexity, decidability and undecidability results for domain-independent planning, Artificial Intelligence 76(1-2) (1995)"
    locator: pp. 75 to 88
---

PDDL is the standard text language for [classical planning](/classical-planning/) tasks and their extensions. A task comes in two files: a domain, with the predicates and the [action schemas](/action-schema/), and a problem, with the objects, the initial state and the goal. McDermott and others defined it in 1998 for the first International Planning Competition, and each later [competition](/international-planning-competition/) extended it. Its `:strips` fragment is lifted [STRIPS](/strips/), and [grounding](/grounding/) turns it into a ground STRIPS task.

## The machine

### Syntax

PDDL uses Lisp-style lists. Names are not case sensitive, variables start with `?`, and `;` starts a comment. Here is the four-operator [blocks world](/blocks-world/) in the style of the 2000 competition, and the [Sussman anomaly](/sussman-anomaly/) as a problem:

```lisp
(define (domain blocksworld)
  (:requirements :strips)
  (:predicates (clear ?x) (ontable ?x) (handempty) (holding ?x) (on ?x ?y))
  (:action pick-up
    :parameters (?x)
    :precondition (and (clear ?x) (ontable ?x) (handempty))
    :effect (and (holding ?x) (not (clear ?x)) (not (ontable ?x)) (not (handempty))))
  (:action put-down
    :parameters (?x)
    :precondition (holding ?x)
    :effect (and (clear ?x) (handempty) (ontable ?x) (not (holding ?x))))
  (:action stack
    :parameters (?x ?y)
    :precondition (and (holding ?x) (clear ?y))
    :effect (and (not (holding ?x)) (not (clear ?y)) (clear ?x) (handempty) (on ?x ?y)))
  (:action unstack
    :parameters (?x ?y)
    :precondition (and (on ?x ?y) (clear ?x) (handempty))
    :effect (and (holding ?x) (clear ?y) (not (clear ?x)) (not (handempty)) (not (on ?x ?y)))))

(define (problem sussman)
  (:domain blocksworld)
  (:objects a b c)
  (:init (clear c) (on c a) (ontable a) (clear b) (ontable b) (handempty))
  (:goal (and (on a b) (on b c))))
```

A domain has the sections `:requirements`, `:types`, `:constants`, `:predicates` and one `:action` for each schema. An action has `:parameters`, a `:precondition` formula and an `:effect`; in the STRIPS fragment the precondition is a conjunction of atoms and the effect is a conjunction of atoms (the add list) and negated atoms (the delete list). A problem has `:objects`, `:init`, a list of ground atoms, and `:goal`, a formula.

### Requirements

The `:requirements` section names the features that the domain uses, so a planner can reject a domain it does not support. The main flags of PDDL 1.2 are:

- `:strips`: conjunctive preconditions and add and delete effects.
- `:typing`: typed parameters and objects, with a type hierarchy such as `truck package - locatable`.
- `:equality`: the built-in predicate `=`, mostly used as `(not (= ?x ?y))`.
- `:negative-preconditions` and `:disjunctive-preconditions`: `not` and `or` in preconditions.
- `:existential-preconditions` and `:universal-preconditions`: `exists` and `forall` in preconditions.
- `:conditional-effects`: `when` and `forall` in effects; see [conditional effects](/conditional-effects/).
- `:adl`: all of the above, the ADL language of Pednault.

A domain with no `:requirements` section is taken to require `:strips`.

### Semantics

The problem is read under the [closed world assumption](/closed-world-assumption/): the ground atoms in `:init` are true, and every other ground atom is false. The objects are the objects of the problem plus the constants of the domain. Each action schema stands for all its ground instances over the objects, with types respected; the result of a ground action in state $s$ is $(s \setminus \mathit{del}) \cup \mathit{add}$, as in STRIPS. A plan is a sequence of ground actions, written as `(unstack c a)`, that is applicable from the initial state and ends in a state where the goal formula is true.

Grounding the example gives 24 actions: 3 `pick-up`, 3 `put-down`, 9 `stack` and 9 `unstack`. The domain does not use `:equality`, so `(stack a a)` is among them. The task has 22 reachable states, and a shortest plan is `(unstack c a) (put-down c) (pick-up b) (stack b c) (pick-up a) (stack a b)`. Adding `:equality` and `(not (= ?x ?y))` to the two binary actions removes the 6 self-stacking actions and leaves 18.

### Types

With `:typing`, `(:types truck package - locatable location)` declares `truck` and `package` as subtypes of `locatable`, and `location` as a subtype of the root type `object`. A parameter `?x - locatable` then ranges over all trucks and packages. In a tiny logistics task with one truck, two packages and two locations, the schemas `drive`, `load` and `unload` give $1 \cdot 2 \cdot 2 + 2 \cdot (2 \cdot 1 \cdot 2) = 12$ ground actions, and a delivery that swaps the packages needs 6.

### Versions

- PDDL 1.2 (McDermott et al. 1998): the STRIPS and ADL fragments above, for the 1998 competition.
- PDDL2.1 (Fox and Long 2003): numeric fluents, plan metrics and durative actions, for [temporal planning](/temporal-planning/).
- PDDL2.2 (Edelkamp and Hoffmann 2004): derived predicates, which are defined by rules over the state, and timed initial literals, which become true at fixed times.
- PDDL3 (Gerevini et al. 2009): state trajectory constraints and soft goals (preferences) with a cost for each violated one.
- PPDDL (Younes and Littman 2004): probabilistic effects, which make a task a [Markov decision process](/markov-decision-process/).

## What it counts

A PDDL task describes a ground STRIPS (or richer) task, and what is counted is the same as for that task: the plan length, or the total cost when actions have costs, or a metric expression under PDDL2.1. The plan is a sequence of ground action names with their arguments, and plans are sequential in the classical fragments. Durative actions in PDDL2.1 give plans with start times instead.

The size of the input is the size of the two files. The ground task can be much larger: a schema with $k$ parameters over $o$ objects has up to $o^k$ instances, and a predicate of arity $k$ gives up to $o^k$ ground atoms, so a short domain file can stand for an exponentially large ground task. Planners report the time of grounding and of search separately for this reason.

## Relation to other models

- [STRIPS](/strips/): the `:strips` fragment, after grounding, is exactly a STRIPS task.
- ADL: the `:adl` fragment is Pednault's ADL. Its features compile into STRIPS, except that the compilation of conditional effects either grows the number of actions exponentially or grows the plan length; see [conditional effects](/conditional-effects/).
- [SAS+](/sas-plus/): planners such as Fast Downward translate PDDL into finite-domain variables before the search.
- [Markov decision process](/markov-decision-process/): PPDDL describes factored MDPs.
- [Datalog](/datalog/): the delete-free part of a PDDL domain is a Datalog program, which is how grounders compute the reachable atoms.
- HTN languages: hierarchical planners use a different input, with tasks and methods; see [HTN planning](/htn-planning/).

## Known results in the model

- Lifted plan existence. For the STRIPS fragment with a finite set of objects and no function symbols, plan existence is EXPSPACE-complete when the domain is part of the input, and PSPACE-complete when the domain is fixed and only the problem varies (Erol, Nau and Subrahmanian 1995). With function symbols, so that terms can be nested and the set of objects is infinite, plan existence is undecidable in general.
- Ground plan existence. After grounding, plan existence is PSPACE-complete in the size of the ground task; see [strips-plan-existence-pspace-complete](/strips-plan-existence-pspace-complete/).
- Size of the grounding. The grounding of the competition blocks world has $2n + 2n^2$ actions for $n$ blocks, and $2n^2$ with `:equality`; the brute force grounding of a schema of arity $k$ has $o^k$ instances. Grounders that join preconditions with the reachable atoms avoid most of the useless ones; see [grounding](/grounding/).

## References
