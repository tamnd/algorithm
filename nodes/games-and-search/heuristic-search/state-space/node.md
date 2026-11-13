---
tag: Y2VQM1
kind: definition
slug: state-space
name: State space
aliases:
- state graph
area: games-and-search/heuristic-search
level: intro
summary: The states of a problem with the actions between them, a transition function, action costs, a start state and a set of goals. It is a graph, usually given by a successor function.
prereqs: [graph, implicit-graph]
see_also: [state-space-search, search-tree, state-space-tree, search-strategy, state-space-planning, sliding-tile-puzzle, tower-of-hanoi, configuration-space]
sources:
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition
    locator: Chapter 3, Section 3.1 (the parts of a search problem and the state space as a graph) and Section 3.2 (example problems, the 8-puzzle among them)
  - book: isbn:9780201055948
    title: Judea Pearl, Heuristics, Intelligent Search Strategies for Computer Problem Solving
    locator: Chapter 1 (state-space representations and the graphs they define)
  - book: isbn:9780123725127
    title: Stefan Edelkamp and Stefan Schroedl, Heuristic Search, Theory and Applications
    locator: Chapter 1 (state space problems, their graphs, and implicit graphs given by a successor function)
---

A *state space* is the model of a problem that [state-space search](/state-space-search/) works on. It has a set of states, a set of actions with a rule that says which actions apply in which state and where each one leads, a cost for each action, one start state and a set of goal states. Seen as a [graph](/graph/), the states are the vertices and the actions are the weighted arcs, and a solution is a path from the start to a goal. The graph is almost never stored. It is an [implicit graph](/implicit-graph/), given by a function that lists the successors of a state, because the number of states is usually exponential in the size of the description of the problem. The 8-puzzle has 181,440 states that can reach its goal, the 15-puzzle about $10^{13}$, and a search can only look at a small part of such a space.

## Definition

A **state space** is a tuple $(S, A, \mathrm{app}, T, c, s_0, G)$ where

- $S$ is a set of *states*;
- $A$ is a set of *actions*, and $\mathrm{app}(s) \subseteq A$ is the set of actions that apply in the state $s$;
- $T$ is the *transition function*: for $a \in \mathrm{app}(s)$, $T(s, a) \in S$ is the state that $a$ leads to;
- $c(s, a) \ge 0$ is the *cost* of the action $a$ in $s$;
- $s_0 \in S$ is the *start state*, and $G \subseteq S$ is the set of *goal states*, often given by a goal test.

The **state graph** has the vertex set $S$ and an arc $s \to T(s, a)$ with the label $a$ and the weight $c(s, a)$ for each $a \in \mathrm{app}(s)$. A *path* is a sequence of actions $a_1, \ldots, a_k$ with $a_i \in \mathrm{app}(s_{i-1})$ and $s_i = T(s_{i-1}, a_i)$, and its cost is $\sum_i c(s_{i-1}, a_i)$. A *solution* is a path from $s_0$ to a state in $G$, and an *optimal solution* is one of least cost, $C^*$.

Most algorithms need only the *successor function*

$$ \mathrm{succ}(s) = \{ (a, T(s, a), c(s, a)) : a \in \mathrm{app}(s) \} $$

and the goal test. These two functions and $s_0$ give the space *implicitly*: the search builds the part of the graph that it visits, and the states that it never reaches cost nothing. The *reachable* state space is the set of states on some path from $s_0$. Some problems also give a *predecessor function*, which backward and [bidirectional search](/bidirectional-search/) need.

The numbers that describe a state space for search are the number of reachable states, the number of successors of a state, which is the [branching factor](/branching-factor/), the cost or the depth $d$ of a cheapest solution, and the largest distance between two states. A space is *reversible* if each action has an inverse of the same cost, so that the state graph is undirected.

## Examples and non-examples

- **The 8-puzzle.** A state places 8 tiles and the blank on a 3 by 3 board. There are $9! = 362{,}880$ placements, and they fall into two classes of $181{,}440$ by the parity of a permutation, see [sliding tile puzzle](/sliding-tile-puzzle/). An action slides a tile into the blank at cost 1, so the space is reversible, and each state has 2, 3 or 4 successors. A [breadth-first search](/breadth-first-search/) from the goal with the blank in a corner reaches the $181{,}440$ states of its class over $241{,}920$ edges, and the farthest of them are 31 moves away.
- **The 2 by 3 puzzle.** With 5 tiles the same search reaches $6!/2 = 360$ states over 420 edges, the farthest 21 moves from the goal.
- **The 15-puzzle.** Its class has $16!/2 = 10{,}461{,}394{,}944{,}000$ states. A search cannot store this space, so it must use a heuristic and visit few states.
- **The Tower of Hanoi.** With $n$ discs on 3 pegs, a state says which peg each disc is on, and each of the $3^n$ assignments is a legal state, because the order of the discs on a peg is forced. The state graph has $3(3^n - 1)/2$ edges, and moving the whole tower from one peg to another takes $2^n - 1$ moves, see [Tower of Hanoi](/tower-of-hanoi/). Breadth-first search confirms both counts for $n = 1$ to $7$.
- **Route finding.** On a road map the states are places and the actions are roads, with their lengths as costs. Here the graph is given explicitly, and the shortest path algorithms of graph theory, such as [Dijkstra's algorithm](/dijkstra/), apply to it directly.
- **Planning tasks.** In [classical planning](/classical-planning/), a state is a set of facts, and the actions are given by schemas with preconditions and effects. With $k$ facts there are up to $2^k$ states, which is why the plan existence problem for STRIPS is [PSPACE-complete](/strips-plan-existence-pspace-complete/) and not polynomial in the size of the task.
- **Not a state space: a search tree.** In a [search tree](/search-tree/) each node is a path from the start, so one state can appear at many nodes. The tree is the unrolling of the state graph from $s_0$, and it is infinite as soon as the graph has a cycle.
- **Not a state space: a state-space tree of backtracking.** The [state-space tree](/state-space-tree/) of a backtracking algorithm has partial solutions as its nodes and complete candidates as its leaves. It has no action costs, and each partial solution has one parent, so it is a tree by construction.
- **Not a state space in this sense: a game.** A [game tree](/game-tree/) has states and moves, but two players choose the moves, and a solution is a strategy, not a path.
- **Not a state space in this sense: a Markov decision process.** In a [Markov decision process](/markov-decision-process/) an action leads to a probability distribution over states, not to one state.

## Related definitions

- **[State-space search](/state-space-search/).** The problem of finding a solution, or an optimal solution, in a state space. A [search strategy](/search-strategy/), such as [best-first search](/best-first-search/), [uniform-cost search](/uniform-cost-search/) or breadth-first search, fixes the order in which states are visited.
- **[Implicit graph](/implicit-graph/).** The general graph-theory idea of a graph whose arcs are computed by a rule. A state space is an implicit graph with a start, goals and costs.
- **[State-space planning](/state-space-planning/).** Search in the state space that a planning task defines, forward from the initial state or backward from the goal. It is an application of state-space search to one way of describing state spaces.
- **[Configuration space](/configuration-space/).** In motion planning the states are positions of a robot and form a continuous space, so it is discretized or sampled before a search.
- **Abstraction.** A map from the states of one space to the states of a smaller space that keeps the actions. Optimal costs in the abstract space are lower bounds in the original one, which is how [pattern databases](/pattern-database/) are built.
- **[Heuristic function](/heuristic-function/).** A function on the states that estimates the cost from a state to the nearest goal.

## References
