---
tag: 1HTN05
kind: concept
slug: preference-articulation
name: Preference articulation
aliases:
- a priori preferences
- a posteriori preferences
- interactive preferences
- no-preference methods
area: optimization/multi-objective
level: intro
summary: 'The classification of multi-objective methods by when the decision maker states preferences: never, before the search, after it, or during it.'
prereqs: [pareto-front, utility-function]
see_also: [scalarization, reference-point-method, achievement-scalarizing-function, goal-programming, lexicographic-optimization, weighted-tchebycheff-method, nsga-ii]
sources:
  - book: doi:10.1007/978-3-642-45511-7
    title: Ching-Lai Hwang and Abu Syed Md. Masud, Multiple Objective Decision Making, Methods and Applications, Lecture Notes in Economics and Mathematical Systems 164, Springer, 1979
    locator: the classification of methods by the stage at which preference information is given
  - book: isbn:9780792382782
    title: Kaisa Miettinen, Nonlinear Multiobjective Optimization, Kluwer, 1999
    locator: Part II, Chapters 2 to 5 (no-preference, a posteriori, a priori and interactive methods)
  - book: doi:10.1007/978-3-540-88908-3
    title: Jürgen Branke, Kalyanmoy Deb, Kaisa Miettinen and Roman Słowiński (editors), Multiobjective Optimization, Interactive and Evolutionary Approaches, Lecture Notes in Computer Science 5252, Springer, 2008
    locator: Chapters 1 and 2 (noninteractive and interactive approaches)
---

Preference articulation is the classification of [multi-objective optimization](/multi-objective-optimization/) methods by when the decision maker gives information about what they want. In *no-preference* methods they give none. In *a priori* methods they give it before the search, in *a posteriori* methods after the [Pareto front](/pareto-front/) is computed, and in *interactive* methods during the search, in several rounds. The choice of class decides how much computation is needed and how much the decision maker must know in advance.

## In plain words

Suppose you plan a trip and care about the price and the travel time. There are four ways to work with a travel agent.

You can say nothing, and the agent picks some sensible balance. You can say at the start how much one hour is worth to you, and the agent finds the best trip for that rule. You can ask the agent for the full list of fair trade-offs and choose yourself. Or you can look at one offer, say "a little cheaper, please", look at the next offer, and stop when you are happy.

The first two ways are fast but need you to know your mind early. The third shows you everything, but the list can be very long. The fourth lets you learn what is possible as you go.

## The idea

**Convention.** All objectives are minimized unless a page says otherwise. The number of objectives is $p \ge 2$, $y = f(x)$ is the image of $x \in X$, and $Y_N$ is the front.

A method takes the problem $(X, f)$ and some preference information $\pi$, and returns one solution or a set of solutions. The classes differ in what $\pi$ is and when it arrives.

| class | the decision maker gives | the method returns | the number of single-objective solves | the main risk |
|---|---|---|---|---|
| no preference | nothing | one "neutral" Pareto optimal point | usually 1 to $p + 1$ | the point may suit nobody |
| a priori | a [utility function](/utility-function/), weights, goals or a priority order, before the search | one Pareto optimal point | 1, or $p$ for a lexicographic order | the stated preference may not be what the decision maker wants once they see the results |
| a posteriori | a choice from the front, after the search | all of $Y_N$ or a representative subset | at least one per returned point | the front can be huge or hard to show for $p \ge 4$ |
| interactive | a new reference point, new weights or a classification of the objectives, in each round | one point per round | one per round | each round needs the decision maker's time |

**No-preference methods.** The method fixes a neutral rule. The *global criterion* method minimizes the distance $\| f(x) - y^I \|$ to the [ideal point](/ideal-point/), often after normalization by the [nadir point](/nadir-point/). On the set of points $y \geqq y^I$, the Euclidean distance to $y^I$ grows strictly when one entry of $y$ grows, so the minimizer is Pareto optimal.

**A priori methods.** The decision maker gives the parameters of one [scalarization](/scalarization/): the weights of the [weighted sum method](/weighted-sum-method/), the goals of [goal programming](/goal-programming/), or the order of [lexicographic optimization](/lexicographic-optimization/). The method solves one problem. The cost is low, but weights are hard to choose. They depend on the units of the objectives, and a small change of weights can move the optimum far along the front, or not at all.

**A posteriori methods.** The method computes the front, or a set of points that represents it, and the decision maker chooses. Exact methods sweep the parameter of a scalarization: the [epsilon-constraint method](/epsilon-constraint-method/), the [weighted Tchebycheff method](/weighted-tchebycheff-method/) or [normal boundary intersection](/normal-boundary-intersection/). [Benson's algorithm](/benson-algorithm/) gives the front of a linear problem. Evolutionary methods such as [NSGA-II](/nsga-ii/) and [MOEA/D](/moea-d/) return an approximation in one run. The decision maker sees the whole range of trade-offs, but for combinatorial problems the front can have exponentially many points (see [multi-objective shortest path](/multi-objective-shortest-path/)).

**Interactive methods.** The method and the decision maker alternate. In each round the method computes one Pareto optimal point from the current preference information, and the decision maker reacts. The [reference point method](/reference-point-method/) of Wierzbicki asks for aspiration levels and projects them onto the front with an [achievement scalarizing function](/achievement-scalarizing-function/). The interactive weighted Tchebycheff procedure of Steuer and Choo (1983) shows a few points and narrows the weight space around the one the decision maker likes. The decision maker learns what is possible and can change their mind, which a priori methods do not allow.

**Requirements on the method.** In every class, the returned point should be Pareto optimal, and each Pareto optimal point should be reachable by some preference information. Otherwise the method hides choices from the decision maker. The weighted sum fails the second condition on nonconvex fronts. The weighted Tchebycheff method, the epsilon-constraint method and the achievement scalarizing function meet it, at the price that some of their optima are only weakly Pareto optimal unless the augmented forms are used.

## Examples

Take the seven images $a = (2, 9)$, $b = (3, 6)$, $c = (4, 7)$, $d = (5, 4)$, $e = (7, 3)$, $f = (8, 5)$ and $g = (9, 1)$, with front $\{a, b, d, e, g\}$, ideal point $(2, 1)$ and nadir point $(9, 9)$.

- **No preference.** Normalize each objective to $[0, 1]$ with the ideal and nadir points, and minimize the Euclidean distance to the ideal point. The normalized points are $a = (0, 1)$, $b = (1/7, 5/8)$, $d = (3/7, 3/8)$, $e = (5/7, 1/4)$ and $g = (1, 0)$. The squared distances are $1$, about $0.411$, about $0.324$, about $0.573$ and $1$. The method returns $d$.
- **A priori.** The decision maker says that one unit of the second objective is worth two units of the first, so the method minimizes $y_1 + 2 y_2$. The values on the front are $20, 15, 13, 13, 11$, and the method returns $g$.
- **A posteriori.** The method returns all five points of the front, and the decision maker chooses, perhaps $e$, which no weighted sum can produce.
- **Interactive.** The decision maker first asks for the reference point $(4, 4)$. The achievement function $\max(y_1 - 4, y_2 - 4)$ is $5$ at $a$, $2$ at $b$, $1$ at $d$, $3$ at $e$ and $5$ at $g$, so the method returns $d = (5, 4)$. The decision maker wants a smaller second objective and asks for $(6, 2)$. The values are now $7$ at $a$, $4$ at $b$, $2$ at $d$, $1$ at $e$ and $3$ at $g$, so the method returns $e = (7, 3)$. The decision maker accepts it.

## Where it is used

- Each page of the [scalarization](/scalarization/) methods states which classes it serves: weights and goals are a priori, parameter sweeps are a posteriori, and reference points are interactive.
- The [utility function](/utility-function/) page gives the model behind a priori methods and the monotonicity that makes their answers Pareto optimal.
- Evolutionary methods are a posteriori by default. Reference-point versions, such as the reference directions of [NSGA-III](/nsga-iii/), move them toward the interactive class.

## References
