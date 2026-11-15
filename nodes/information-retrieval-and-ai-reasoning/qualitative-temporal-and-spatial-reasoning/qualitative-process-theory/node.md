---
tag: 92522T
kind: model
slug: qualitative-process-theory
name: Qualitative process theory
aliases:
- QPT
- Forbus process theory
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Models physical change by processes that influence quantities, with quantity spaces and signs of derivatives in place of numbers.
prereqs: [ode-initial-value-problem]
see_also: [qsim, euler-method, constraint-propagation]
sources:
  - paper: doi:10.1016/0004-3702(84)90038-9
    title: Kenneth D. Forbus, Qualitative process theory, Artificial Intelligence 24, 1984
    locator: pages 85 to 168 (quantities, quantity spaces, individual views, processes, direct and indirect influences, the sole mechanism assumption, influence resolution and limit analysis)
  - paper: "Kenneth D. Forbus, Qualitative process theory, twelve years after, Artificial Intelligence 59, 1993"
    locator: pages 115 to 123 (the author's review of the theory, its implementations and its later use)
  - paper: "Daniel S. Weld and Johan de Kleer, editors, Readings in Qualitative Reasoning about Physical Systems, Morgan Kaufmann, 1990"
    locator: pages 178 to 219 (a reprint of Forbus 1984)
  - paper: "Brian Falkenhainer and Kenneth D. Forbus, Compositional modeling, finding the right model for the job, Artificial Intelligence 51, 1991"
    locator: the assembly of a process model from a library of model fragments, an extension of qualitative process theory
---

Qualitative process theory (QPT), from Forbus (1984), is a language for qualitative models of physical systems in which every change is caused by a process, such as a flow of heat, a flow of liquid or boiling. It reasons about continuous systems, quantities such as a temperature or an amount of water that change continuously in time, not about temporal or spatial relations between events or regions as the other calculi in this area do. A quantity has no number: it has a sign, a derivative sign, and a place in a partial order of values called its quantity space. From a description of the objects present, a QPT reasoner finds which processes are active, what they change, and how the situation can change next.

## The machine

**Quantities.** Each quantity $Q$ has an amount $A[Q]$ and a derivative $D[Q]$. Each of them has a sign in $\{-, 0, +\}$ and a magnitude. The *quantity space* of $Q$ is a partial order that relates $A[Q]$ to other values that matter, for example the temperature of some water to its boiling point and to the temperature of the stove. The value of a quantity is known only through these order relations.

**Individual views.** An individual view describes an object in some state, for example "the water in a cup, as a contained liquid". It has four parts: the individuals it is about, preconditions (facts outside the theory, such as "the valve is open"), quantity conditions (inequalities in quantity spaces, such as "the amount of water is greater than zero"), and relations that hold while the view is active.

**Processes.** A process has the same four parts and, in addition, *direct influences*: $I+(Q, n)$ or $I-(Q, n)$, which say that while the process is active it adds $n$ to or takes $n$ from the derivative of $Q$. Quantities are also linked by *qualitative proportionalities*: $Q_1 \propto_{Q+} Q_2$ says that $Q_1$ is a function of $Q_2$, among others, that increases with $Q_2$, and $\propto_{Q-}$ says that it decreases. These are *indirect influences*.

**Sole mechanism assumption.** Every change in a physical system is caused, directly or indirectly, by processes. So if no active process influences a quantity, its derivative is 0.

**Influence resolution.** The sign of $D[Q]$ is the sign of the sum of the direct influences on $Q$, and for an indirectly influenced quantity it follows from the signs of the quantities that it depends on. If the influences all have one sign, the result is that sign. If some are positive and some negative, the result is ambiguous unless the order of their magnitudes is known, and the reasoner must consider each possible sign.

**Limit analysis.** A changing quantity moves toward the next value in its quantity space. When it reaches that value, an inequality changes, so a quantity condition can become true or false, and a process or view can start or stop. Limit analysis lists these possible changes, and each of them gives a possible next state.

**Example: heat flow.** Two objects $s$ and $d$ are joined by a heat path. The process heat-flow has the quantity condition $T(s) > T(d)$, a flow rate $F$ with $F \propto_{Q+} T(s)$ and $F \propto_{Q-} T(d)$, and the influences $I-(\mathrm{heat}(s), F)$ and $I+(\mathrm{heat}(d), F)$; the temperature of each object rises with its heat, $T \propto_{Q+} \mathrm{heat}$. While $T(s) > T(d)$, the flow rate is positive, so $D[\mathrm{heat}(s)]$ is $-$ and $D[\mathrm{heat}(d)]$ is $+$, and so $T(s)$ falls and $T(d)$ rises. Limit analysis finds one change: the two temperatures can become equal, the quantity condition then fails, and the flow stops. The qualitative model does not say whether this happens in finite time.

**Example: an ambiguous influence.** A tank has an inflow process with $I+(\mathrm{amount}, f_{in})$ and a drain with $I-(\mathrm{amount}, f_{out})$. With no order known between $f_{in}$ and $f_{out}$, the sign of $D[\mathrm{amount}]$ can be $+$, $0$ or $-$, and the reasoner keeps three branches.

## What it counts

The object of a QPT computation is an *envisionment*: a graph whose nodes are qualitative states and whose edges are the transitions found by limit analysis. A qualitative state fixes which views and processes are active, the order relations in each quantity space, and the sign of each derivative. The *attainable* envisionment contains the states reachable from a given initial state, and the *total* envisionment contains every consistent state.

Cost is counted in the number of states. The quantity spaces are finite, so the number of states is finite, but it can grow exponentially with the number of quantities: with $q$ quantities, each with $k$ possible positions in its quantity space and 3 derivative signs, there can be up to $(3k)^q$ states. Each ambiguous influence multiplies the branches. Forbus implemented the theory in GIZMO and later in QPE, the Qualitative Process Engine.

## Relation to other models

- **QSIM.** [QSIM](/qsim/) takes a fixed qualitative differential equation, a set of constraints on the variables, and simulates it. QPT adds a layer above it: it decides from the objects and their state which processes act, and so which equations hold, and that set can change during a behavior. Crawford, Farquhar and Kuipers built a compiler, QPC, that turns process models into qualitative differential equations for QSIM.
- **Confluences.** The qualitative physics of de Kleer and Brown (1984) is device-centered: a system is a network of components joined by conduits, each described by sign equations. QPT is process-centered: the same physical object can take part in different processes at different times.
- **Differential equations.** A QPT model stands for a family of [ordinary differential equation](/ode-initial-value-problem/) models that share the signs of their influences. A numeric method such as the [Euler method](/euler-method/) needs one member of the family, with numbers for every parameter.
- **Compositional modeling.** Falkenhainer and Forbus (1991) assemble a model from a library of fragments, with explicit modeling assumptions, so that the reasoner chooses the right level of detail for a question.

## Known results in the model

| question | result | source |
| --- | --- | --- |
| which processes are active | decided by the preconditions and the quantity conditions of each process instance | Forbus 1984 |
| sign of a derivative | the sign of the sum of the direct influences; ambiguous with opposing influences of unknown order | Forbus 1984 |
| next states | given by limit analysis on the quantity spaces | Forbus 1984 |
| size of the envisionment | finite, and up to exponential in the number of quantities | Forbus 1984 |
| model building from fragments | compositional modeling | Falkenhainer and Forbus 1991 |

**Spurious behaviors.** The envisionment uses only signs and orders, so, as with QSIM, it can contain paths that no numeric model in the family shows. Ambiguous influence resolution is one source of branching: the tank of the example keeps three branches, and which of them a real tank takes depends on numbers that the model does not have.

**Later work.** Forbus (1993) reviews twelve years of the theory, its implementations, and later work such as compositional modeling.

## References
