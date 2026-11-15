---
tag: 822MPG
kind: model
slug: event-calculus
name: Event calculus
aliases:
- Kowalski-Sergot event calculus
area: information-retrieval-and-ai-reasoning/knowledge-representation-and-description-logics
level: advanced
summary: A logic of events on a time line in which events initiate and terminate fluents, fluents persist between such events, and circumscription makes the lists of events and effects complete.
prereqs: [situation-calculus, circumscription, frame-problem]
see_also: [successor-state-axioms, yale-shooting-problem, clark-completion, negation-as-failure, logic-programming, abductive-reasoning, temporal-logic, sat]
sources:
  - paper: doi:10.1007/BF03037383
    title: Robert Kowalski and Marek Sergot, A logic-based calculus of events, New Generation Computing 4(1), 1986, pages 67 to 95
    locator: the original calculus as a logic program with negation as failure, with events that start and end periods of time (general locator)
  - paper: doi:10.1007/3-540-48317-9_17
    title: Murray Shanahan, The event calculus explained, in Michael J. Wooldridge and Manuela Veloso (eds.), Artificial Intelligence Today, Lecture Notes in Artificial Intelligence 1600, Springer, 1999, pages 409 to 430
    locator: the simple event calculus in classical logic with circumscription, its reduction to predicate completion, and the extensions for continuous change (general locator)
  - book: isbn:9780262193849
    title: Murray Shanahan, Solving the Frame Problem, A Mathematical Investigation of the Common Sense Law of Inertia, MIT Press, 1997
    locator: the chapters on the event calculus and on circumscription (general locator)
  - paper: doi:10.1007/3-540-45632-5_17
    title: Rob Miller and Murray Shanahan, Some alternative formulations of the event calculus, in Antonis C. Kakas and Fariba Sadri (eds.), Computational Logic, Logic Programming and Beyond, Lecture Notes in Artificial Intelligence 2408, Springer, 2002, pages 452 to 490
    locator: variants of the axioms, including different treatments of time points, concurrent events and release from inertia (general locator)
  - book: isbn:9780128014165
    title: Erik T. Mueller, Commonsense Reasoning, An Event Calculus Based Approach, second edition, Morgan Kaufmann, 2015
    locator: the discrete event calculus over integer time and its reasoner that encodes bounded problems as SAT (general locator)
  - book: isbn:9780444522115
    title: Frank van Harmelen, Vladimir Lifschitz and Bruce Porter (eds.), Handbook of Knowledge Representation, Elsevier, 2008
    locator: Chapter 17, Event Calculus, by Erik T. Mueller (general locator)
---

The event calculus is a logic for reasoning about events that happen at points on a time line and about the fluents that they make true or false. A fluent made true by an event stays true until an event makes it false; this *commonsense law of inertia* is written once, as a few domain-independent axioms. Kowalski and Sergot (1986) introduced the calculus as a logic program, and Shanahan (1997, 1999) recast it in classical logic with [circumscription](/circumscription/). The [situation calculus](/situation-calculus/) reasons about branching hypothetical histories and states inertia fluent by fluent in its [successor state axioms](/successor-state-axioms/); the event calculus reasons about one actual narrative of events on a linear time line, which makes concurrent events, events at given times and continuous change easier to state.

## The machine

**Syntax.** The language is many-sorted, with sorts for events (often actions), fluents and time points. Time points are ordered by $<$; they are the integers in the discrete event calculus and the non-negative reals in other versions. The basic predicates are

| predicate | meaning |
|---|---|
| $Happens(e, t)$ | event $e$ occurs at time $t$ |
| $Initiates(e, f, t)$ | if $e$ occurs at $t$, fluent $f$ is true after $t$ |
| $Terminates(e, f, t)$ | if $e$ occurs at $t$, fluent $f$ is false after $t$ |
| $HoldsAt(f, t)$ | fluent $f$ is true at time $t$ |
| $InitiallyP(f)$, $InitiallyN(f)$ | $f$ is true, or false, at time 0 |
| $Clipped(t_1, f, t_2)$ | some event terminates $f$ strictly between $t_1$ and $t_2$ |
| $Declipped(t_1, f, t_2)$ | some event initiates $f$ strictly between $t_1$ and $t_2$ |

**Domain-independent axioms.** A basic form of the axioms, in the style of Shanahan (1999), is

- $HoldsAt(f, t) \leftarrow InitiallyP(f) \wedge \neg Clipped(0, f, t)$;
- $HoldsAt(f, t_2) \leftarrow Happens(e, t_1) \wedge Initiates(e, f, t_1) \wedge t_1 < t_2 \wedge \neg Clipped(t_1, f, t_2)$;
- $Clipped(t_1, f, t_2) \leftrightarrow \exists e\, \exists t\, \big(Happens(e, t) \wedge t_1 < t < t_2 \wedge Terminates(e, f, t)\big)$;

and the same three with $\neg HoldsAt$, $InitiallyN$, $Terminates$ and $Declipped$ in place of $HoldsAt$, $InitiallyP$, $Initiates$ and $Clipped$. Miller and Shanahan (2002) compare variants that differ in such details as whether an event at $t_1$ itself can clip a fluent, and whether a fluent holds at the time point of the event that initiates it.

**Domain description.** A problem consists of

- $\Sigma$, the effect axioms, as definitions of $Initiates$ and $Terminates$, possibly with conditions on $HoldsAt$ at the time of the event;
- $\Delta$, the narrative, as facts or formulas about $Happens$;
- $\Gamma$, observations, such as $InitiallyP$ facts or $HoldsAt$ facts;
- $\Omega$, unique names axioms for events and fluents.

**Semantics.** The theory is

$$\mathrm{CIRC}[\Sigma; Initiates, Terminates] \wedge \mathrm{CIRC}[\Delta; Happens] \wedge \Gamma \wedge \Omega \wedge EC,$$

where $EC$ is the set of domain-independent axioms. Circumscribing $Initiates$ and $Terminates$ in $\Sigma$ makes the effects listed in $\Sigma$ the only effects, and circumscribing $Happens$ in $\Delta$ makes the events listed in $\Delta$ the only events. Persistence then follows from the axioms: with no event that terminates $f$, nothing clips it. The original calculus of Kowalski and Sergot (1986) gets the same effect from [negation as failure](/negation-as-failure/) in a [logic program](/logic-programming/).

**Example.** A light with the effects $Initiates(on, Light, t)$ and $Terminates(off, Light, t)$, and the narrative $Happens(on, 1)$, $Happens(off, 5)$, $Happens(on, 8)$. The circumscription makes these the only events and effects. Then $HoldsAt(Light, 3)$ holds, because $on$ occurs at 1 and no $off$ occurs between 1 and 3. $\neg HoldsAt(Light, 6)$ holds by the negative axioms, because $off$ occurs at 5. $HoldsAt(Light, 10)$ holds again. Two events at the same time point are allowed: adding $Happens(off, 8)$ makes both $Initiates$ and $Terminates$ apply after 8, and the axioms then give both $HoldsAt(Light, 10)$ and $\neg HoldsAt(Light, 10)$, so the theory is inconsistent. A domain that allows such events must say which effect wins, for example with a condition in $\Sigma$.

## What it counts

Every question is an entailment question from the circumscribed theory. The usual tasks are

- **temporal projection (deduction):** given $\Sigma$, $\Delta$ and the initial state, does $HoldsAt(f, t)$ follow?
- **planning (abduction):** given $\Sigma$, the initial state and a goal $HoldsAt(g, t)$, find a narrative $\Delta$ that, added to the theory, entails the goal; this is [abduction](/abductive-reasoning/), and the events of $\Delta$ are the plan;
- **explanation (abduction):** given observations at later times, find events in the past that account for them;
- **learning effects (induction):** given narratives and observations, find $\Sigma$.

## Relation to other models

- **[Situation calculus](/situation-calculus/).** A situation is a history of actions and every history is a possible future, so the situations form a tree; the event calculus has one time line and a narrative of what actually happens on it. The situation calculus states inertia in one successor state axiom for each fluent; the event calculus states it once in $EC$ and gets completeness of the effects from circumscription. Concurrent events and events at known times fit the event calculus directly.
- **[Yale shooting problem](/yale-shooting-problem/).** Minimizing change, as in early uses of circumscription, gives an unwanted model in which the gun becomes unloaded during a wait. The event calculus minimizes events and effects, not change, so the gun can only become unloaded through an event in $\Delta$ that terminates $Loaded$, and there is none.
- **Logic programs.** The original calculus is a logic program with negation as failure. When $\Sigma$ and $\Delta$ are definitions without recursion through the minimized predicates, the circumscriptions equal the [Clark completion](/clark-completion/) of those predicates (Shanahan 1999), which links the two readings.
- **[Temporal logic](/temporal-logic/)** describes properties of paths of states with modal operators; the event calculus names time points explicitly and quantifies over them.

## Known results in the model

- **Circumscription becomes completion.** If the effect axioms and the narrative do not define $Initiates$, $Terminates$ or $Happens$ in terms of themselves, each circumscription is equivalent to the predicate completion of the minimized predicates, a first-order formula (Shanahan 1999). Under this condition the whole theory is first-order, and projection is first-order entailment.
- **Undecidable in general.** The theory may contain arbitrary first-order formulas over unbounded time, so entailment is undecidable in general.
- **Bounded discrete problems are propositional.** With integer time up to a bound $T$ and finitely many ground events and fluents, the theory after completion is a propositional formula with $O(T)$ copies of each fluent and event, and each query is a [SAT](/sat/) or unsatisfiability question. Mueller's reasoner for the discrete event calculus works this way (Mueller 2015).
- **Continuous change.** The full event calculus adds a predicate $Releases$, which frees a fluent from inertia, and $Trajectory(f_1, t_1, f_2, d)$, which says how a fluent $f_2$ changes during the time $d$ after $f_1$ became true at $t_1$, for quantities such as the level of water in a filling tank (Shanahan 1999; Miller and Shanahan 2002).

## References
