---
tag: EDXW2V
kind: concept
slug: qualification-problem
name: Qualification problem
area: games-and-search/planning
level: intro
summary: An action's preconditions can never be listed exhaustively.
prereqs: [state-space]
see_also: [frame-problem, ramification-problem, strips, closed-world-assumption, execution-monitoring, replanning, markov-decision-process, contingent-planning]
sources:
  - paper: "John McCarthy, Epistemological problems of artificial intelligence, Proceedings of the Fifth International Joint Conference on Artificial Intelligence (IJCAI), 1977"
    title: McCarthy 1977
    locator: pp. 1038 to 1044 (the qualification problem, with the boat of the missionaries and cannibals puzzle)
  - paper: doi:10.1016/0004-3702(80)90011-9
    title: "John McCarthy, Circumscription: A form of non-monotonic reasoning, Artificial Intelligence 13(1-2) (1980)"
    locator: the discussion of the missionaries and cannibals puzzle and of conjecturing that no unstated obstacle exists (general locator)
  - paper: doi:10.1016/0004-3702(88)90020-3
    title: "Matthew L. Ginsberg and David E. Smith, Reasoning about action II: The qualification problem, Artificial Intelligence 35(3) (1988)"
    locator: pp. 311 to 342 (qualifications derived from domain constraints)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: the discussion of the qualification problem in the chapter on logical agents (general locator)
---

The qualification problem is that the conditions under which an action succeeds can never be listed in full. McCarthy (1977) named it: a rowing boat crosses a river if it has oars, if it does not leak, if no one has stolen the oars, and so on without end. A planner must act on a finite list of preconditions, so it assumes that the unlisted ones hold. The [STRIPS](/strips/) model makes that assumption silently; logics of action make it explicit with defaults, and planners that act in the real world back it up with [execution monitoring](/execution-monitoring/) and [replanning](/replanning/).

## In plain words

To start a car you need the key, fuel and a working battery. You also need the engine to be in the car, no potato in the exhaust pipe, no one sitting on the hood with a brick, and a thousand more things no one would think to write down. Any finite list of conditions leaves some out. People handle this by assuming that nothing unusual is wrong unless there is a reason to think so, and by noticing when the car does not start. A computer that plans must do the same, because a full list does not exist.

## The idea

### Why a list is never complete

In a logic of actions, the precondition of an action is a formula $\mathit{Poss}(a, s)$, and the planner may apply $a$ only when it can prove $\mathit{Poss}(a, s)$. If the formula includes every condition that could block the action, the planner can almost never prove it, because most of the conditions (the boat does not leak, the oars are not stolen) are not known. If the formula leaves conditions out, the logic proves false conclusions about the world whenever one of them fails.

### Assume nothing is abnormal

McCarthy's answer was to write the precondition with an abnormality predicate, $\lnot \mathit{ab}(a, s) \land \mathit{oars}(s) \to \mathit{Poss}(\mathit{row}(a), s)$, and to minimize $\mathit{ab}$ by circumscription: the reasoner concludes that the boat can cross unless something it knows makes the case abnormal. The conclusion is nonmonotonic. Learning that the boat leaks makes it abnormal, and the conclusion is withdrawn.

### Qualifications from domain constraints

Ginsberg and Smith (1988) derived many qualifications from the laws of the domain. If a law says that two objects cannot be in the same place, then an action whose effect would put a block where another block is cannot take place, and the planner does not need a separate precondition for it. The same law can also be read the other way, as a reason for other facts to change, which is the [ramification problem](/ramification-problem/). Deciding which reading applies is part of the difficulty.

### In classical planning

[Classical planning](/classical-planning/) assumes the qualification problem away: the listed precondition is the whole truth, and an applicable action always has its stated effect. This is a [closed world assumption](/closed-world-assumption/) about preconditions. When a plan runs in a real world, the gap shows up as an action that fails or has another result. Systems close the gap in three ways:

- monitor the execution, and [replan](/replanning/) from the observed state when an action fails;
- plan for some failures in advance, with [contingent planning](/contingent-planning/);
- give each action a probability of failure, and plan in a [Markov decision process](/markov-decision-process/), which folds all the unlisted qualifications into one number.

## Examples

- The boat. The missionaries and cannibals puzzle states a capacity for the boat and nothing else. A solver that gets the puzzle as a task uses only that condition; McCarthy's point was that a person who reads the puzzle also assumes the boat has oars, does not leak, and that there is no bridge, and that a formal reasoner needs a way to make these assumptions.
- The blocks world. The STRIPS action $\mathit{pickup}(x)$ needs $\mathit{clear}(x)$, $\mathit{ontable}(x)$ and $\mathit{handempty}$. A robot arm also needs the block to be light enough, not glued to the table and within reach. The planning model lists none of these, and a failed grasp is handled when the plan runs.
- The car. The precondition "the key is in the ignition" is listed; "there is no potato in the tailpipe" is the classic example of a qualification that no one lists but that blocks the action.

## Where it is used

- Logics of action and commonsense reasoning, where default rules and circumscription state that unlisted qualifications hold.
- Planning and acting systems: the decision of how much to list in a precondition and how much to leave to execution monitoring is a design choice in every robot planner.
- Software: an API call has documented preconditions, and it can still fail for reasons outside the list (the disk is full, the network is down). Exceptions and error codes play the role of execution monitoring.

## References
