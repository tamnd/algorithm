---
tag: PJ252Y
kind: problem
slug: yale-shooting-problem
name: Yale shooting problem
aliases:
- Hanks-McDermott problem
area: information-retrieval-and-ai-reasoning/rule-based-and-nonmonotonic-reasoning
level: core
summary: After loading a gun, waiting and shooting, naive minimization of change gives an unintended model where the gun unloads and the victim lives.
prereqs: [frame-problem, circumscription, situation-calculus]
see_also: [default-logic, successor-state-axioms, event-calculus, answer-set-programming, ramification-problem, qualification-problem, nonmonotonic-reasoning]
sources:
  - paper: doi:10.1016/0004-3702(87)90043-9
    title: Steve Hanks and Drew McDermott, Nonmonotonic logic and temporal projection, Artificial Intelligence 33(3), 379 to 412 (1987)
    locator: the shooting scenario in the situation calculus, the two minimal models under circumscription of abnormality, and the same failure in default logic and in McDermott's nonmonotonic logic
  - paper: doi:10.1016/0004-3702(80)90011-9
    title: John McCarthy, Circumscription, a form of non-monotonic reasoning, Artificial Intelligence 13(1-2), 27 to 39 (1980)
    locator: the minimization of abnormality that the scenario tests
  - paper: doi:10.1016/0304-3975(93)90073-3
    title: Thomas Eiter and Georg Gottlob, Propositional circumscription and extended closed-world reasoning are Pi2P-complete, Theoretical Computer Science 114(2), 231 to 245 (1993)
    locator: the main theorem, which bounds inference from a propositional encoding of the scenario under plain circumscription
---

The Yale shooting problem is a three-step story that showed, in 1986, that the obvious nonmonotonic answer to the [frame problem](/frame-problem/) does not work. A person is alive. A gun is loaded, the shooter waits, and then fires. Everyone expects the person to be dead. Hanks and McDermott (1987) wrote the story in the [situation calculus](/situation-calculus/) with the common-sense rule "fluents normally persist", minimized abnormality with [circumscription](/circumscription/), and found two minimal models. In the intended one the shot kills. In the anomalous one the gun becomes unloaded during the wait, for no reason, and the person survives. Both models have exactly one abnormal change, so plain minimization cannot choose. The same happens with [default logic](/default-logic/), which gives two extensions.

## In plain words

To avoid writing "this action does not change that fact" for every pair, we say "facts stay the same unless something makes them change" and ask the logic to assume as few changes as possible. The trouble is that "as few as possible" counts changes, not causes. Shooting a loaded gun must change something: either the victim dies, or the gun was already unloaded so that the shot does nothing. An unexplained unloading during the wait costs one change, and so does the death. The logic sees two equally good stories, while a person sees only one, because the gun had no reason to unload.

## Definition

The input is a description of actions and their effects, a starting state and a sequence of actions. The question is what holds at the end. In the propositional form used here, the fluents are $\mathit{alive}_t$ and $\mathit{loaded}_t$ at the time points $t = 0, 1, 2, 3$. The actions are $\mathit{load}$ from 0 to 1, $\mathit{wait}$ from 1 to 2 and $\mathit{shoot}$ from 2 to 3. For each fluent $f$ and step $t$ there is an abnormality atom $\mathit{ab}_{f,t}$, meaning "$f$ may change between $t$ and $t + 1$". The theory $A$ is:

1. $\mathit{alive}_0$ (the start),
2. $\mathit{loaded}_1$ (the effect of loading),
3. $\mathit{loaded}_2 \supset \neg\mathit{alive}_3 \wedge \mathit{ab}_{\mathit{alive},2}$ (the effect of shooting a loaded gun, which is an abnormal change for $\mathit{alive}$),
4. $f_t \wedge \neg\mathit{ab}_{f,t} \supset f_{t+1}$ for each fluent $f$ and $t = 0, 1, 2$ (inertia: a fluent that holds keeps holding unless it is abnormal).

The intended answer is $\neg\mathit{alive}_3$. The problem is to find a nonmonotonic semantics for theories of this form that gives the intended answer here and in similar stories, without extra axioms written by hand for each story.

**The failure.** Circumscribe the abnormality atoms with all other atoms varying. Two sets of abnormality atoms are minimal:

- $\{\mathit{ab}_{\mathit{alive},2}\}$: the gun stays loaded, the shot kills, and $\neg\mathit{alive}_3$ holds. This is the intended model.
- $\{\mathit{ab}_{\mathit{loaded},1}\}$: the gun stops being loaded during the wait, so axiom 3 says nothing, inertia keeps the person alive, and $\mathit{alive}_3$ holds. This is the anomalous model.

Neither set is a subset of the other, so the circumscription entails neither $\mathit{alive}_3$ nor $\neg\mathit{alive}_3$. With the inertia defaults $: \neg\mathit{ab}_{f,t} / \neg\mathit{ab}_{f,t}$ in default logic, the same two choices give two extensions.

## Variants

- **Prediction** (forward reasoning) is the original problem: given the start and the actions, what holds at the end?
- **Explanation** (backward reasoning) gives a later observation and asks what happened before. Kautz's *stolen car problem* (1986) is the standard example: a car is parked, two time steps pass, and the car is gone. A good solution must say that the car was stolen at some point, without choosing the latest point only because changes are pushed late.
- **Effects with conditions and side effects** lead to the [qualification problem](/qualification-problem/) and the [ramification problem](/ramification-problem/), which test the same solutions in harder settings.
- **Concurrency, nondeterminism and continuous time** extend the story to the [event calculus](/event-calculus/) and to action languages.

## Examples

- **The original story.** As above, plain minimization gives two models, and only one is intended.
- **Without the wait.** Remove the wait, so the actions are $\mathit{load}$ and then $\mathit{shoot}$ at once. There is no gap in which the gun could unload, and the only minimal model is the intended one. The anomaly needs a step in which nothing should happen.
- **Chronological minimization.** Prefer the model whose abnormalities happen later. The anomalous model has its abnormality at step 1, the intended model at step 2, so the intended model wins and $\neg\mathit{alive}_3$ follows. For the stolen car, the same preference wrongly concludes that the car was stolen in the last step.

## Known algorithms

These are the main solutions, each a different semantics with its own procedure.

- **Chronological minimization.** Shoham (1988, chronological ignorance) and Kautz (1986) minimize abnormality earlier time points first. This solves prediction with deterministic actions, and prediction then is a forward simulation that takes time linear in the number of steps. It fails on explanation, as the stolen car shows.
- **Causal minimization.** Lifschitz (1987) separates what an action causes from what persists: the effects are given by a predicate of causes, which is minimized, and every fluent that is not caused to change keeps its value. Baker (1991) kept the situation calculus but let the function from situations to their successors vary during circumscription. Both solve prediction and the stolen car.
- **[Successor state axioms](/successor-state-axioms/).** Reiter's monotonic solution writes, for each fluent, one axiom that lists all the ways it can become true or false. With these axioms the story has a single model up to the irrelevant atoms, and no minimization is needed.
- **[Event calculus](/event-calculus/).** Fluents are initiated and terminated by events, and the circumscription minimizes the events and their effects separately, which removes the anomaly.
- **[Answer set programming](/answer-set-programming/).** Inertia is the rule "a fluent holds at $t + 1$ if it holds at $t$ and is not known to stop holding". The effects are rules, not abnormality facts, so the unexplained unloading has no support, and the program has a single [stable model](/stable-model-semantics/), the intended one.

## Bounds

For a fixed story, the encoding above has a constant number of atoms, so every semantics is computed in constant time. The interest is in general theories of action. Plain circumscription of a propositional theory is $\Pi_2^p$-complete (Eiter and Gottlob 1993), so the naive approach is also expensive. Skeptical default reasoning has the same $\Pi_2^p$ bound, see [the complexity of default logic](/default-logic-complexity/). The fixes above are cheaper for deterministic actions: with successor state axioms or chronological minimization, prediction is a simulation that takes one step per action, with the cost of evaluating the effect conditions at each step.

## Reductions

- **Temporal projection to circumscription** is the encoding in the definition: one abnormality atom per fluent and step, and the inertia axioms of item 4.
- **Temporal projection to default logic** replaces the circumscription by the normal defaults $: \neg\mathit{ab}_{f,t} / \neg\mathit{ab}_{f,t}$. The extensions are then the maximal consistent choices of non-abnormality, which here are the same two stories.
- **Temporal projection to logic programs** writes inertia as a rule with negation as failure. The encoding is linear in the number of fluents times the number of steps.

## Applications

The problem is a test case, not an application. It shaped how nonmonotonic logics are used to reason about action: in robot control languages based on the situation calculus, in planning, and in answer set programs for planning and diagnosis of dynamic systems. A modern theory of action is expected to give the intended answer on the Yale shooting scenario and on the stolen car.

## References
