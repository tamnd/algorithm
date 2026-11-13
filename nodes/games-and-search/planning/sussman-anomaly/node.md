---
tag: 0Z947C
kind: concept
slug: sussman-anomaly
name: Sussman anomaly
aliases:
- Sussman's anomaly
area: games-and-search/planning
level: intro
summary: Goal interactions in blocks world that defeat naive linear, goal-by-goal planners.
prereqs: [blocks-world]
see_also: [pop-partial-order-planning, goal-regression, means-ends-analysis, least-commitment-principle, causal-link, plan-space-planning, strips, classical-planning]
sources:
  - paper: "Gerald Jay Sussman, A Computer Model of Skill Acquisition, American Elsevier, 1975"
    title: Sussman 1975
    locator: the discussion of HACKER and of goals that interfere with each other (general locator)
  - paper: doi:10.1016/0004-3702(92)90028-V
    title: "Naresh Gupta and Dana S. Nau, On the complexity of blocks-world planning, Artificial Intelligence 56(2-3) (1992)"
    locator: footnote 2 (the anomaly is credited to Allen Brown, citing Waldinger 1977, p. 127, and was made known by Sussman 1975)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: the discussion of interacting goals in the chapters on state-space and plan-space planning (general locator)
  - book: isbn:9780134610993
    title: Stuart Russell and Peter Norvig, Artificial Intelligence, A Modern Approach, fourth edition, Pearson, 2020
    locator: Chapter 11 (the Sussman anomaly as an example of interacting subgoals; general locator)
---

The Sussman anomaly is a three-block [blocks world](/blocks-world/) task that no planner can solve well by achieving its two goals one after the other. Block $C$ is on $A$, $B$ is on the table, and the goal is $A$ on $B$ and $B$ on $C$. Whichever goal is achieved first, the work for the second one undoes it, so a goal-by-goal plan has 5 moves where 3 suffice, and a planner that protects each achieved goal finds no plan at all. Sussman (1975) made the example known through his program HACKER; it led to planners that interleave work on several goals, such as [partial-order planning](/pop-partial-order-planning/).

## In plain words

Three blocks: $C$ sits on $A$, and $B$ stands alone. You want a tower with $A$ on top, $B$ in the middle and $C$ at the bottom. The natural idea is to split the job: first put $A$ on $B$, then put $B$ on $C$. But once $A$ is on $B$, you cannot move $B$ without taking $A$ off again. Try the other order: put $B$ on $C$ first. Now $C$, with $B$ on it, still sits on $A$, so $A$ is buried. Either way the second step wrecks the first. The short solution does a bit of one goal, then the other, then the rest of the first.

## The idea

### The task

The initial state is $\{\mathit{on}(C, A), \mathit{ontable}(A), \mathit{ontable}(B), \mathit{clear}(C), \mathit{clear}(B)\}$ and the goal is $\{\mathit{on}(A, B), \mathit{on}(B, C)\}$, two facts that must hold at the same time. In the move encoding of the blocks world the task has 13 reachable states, and the unique shortest plan has 3 moves:

1. move $C$ from $A$ to the table;
2. move $B$ from the table onto $C$;
3. move $A$ from the table onto $B$.

With the four operators of the competitions the unique shortest plan has 6 actions: $\mathit{unstack}(C, A)$, $\mathit{putdown}(C)$, $\mathit{pickup}(B)$, $\mathit{stack}(B, C)$, $\mathit{pickup}(A)$, $\mathit{stack}(A, B)$. No plan has 2 moves or 5 actions.

### Goal by goal

A linear (noninterleaved) planner achieves the goals one at a time: it finds a plan for the first goal, and then a plan for all goals from the state where the first plan ends. Take shortest plans at each stage.

- $\mathit{on}(A, B)$ first: move $C$ to the table and $A$ onto $B$ (2 moves). Now $B$ is under $A$, and $\mathit{on}(B, C)$ needs 3 more moves: $A$ to the table, $B$ onto $C$, $A$ onto $B$. Total 5.
- $\mathit{on}(B, C)$ first: move $B$ onto $C$ (1 move). Now the tower is $A$, $C$, $B$ from the bottom, $A$ is buried under two blocks, and the full goal needs 4 more moves. Total 5.

Both orders give 5 moves, against an optimum of 3. In the four-operator encoding both orders give 10 actions (4 plus 6, and 2 plus 8), against an optimum of 6. No goal-by-goal plan is shorter, in either order and in either encoding.

### Goal protection makes it worse

Some early planners protected a goal once they had achieved it: no later action may delete it. With $\mathit{on}(A, B)$ protected, $B$ can never move again, so $\mathit{on}(B, C)$ is out of reach. With $\mathit{on}(B, C)$ protected, $C$ and $B$ must stay on $A$, so $A$ can never become clear. In both orders the search ends with no plan, although the task is easy. So a linear planner with protection is incomplete.

### Why the optimal plan is not serial

In the optimal plan, $\mathit{on}(B, C)$ first holds after move 2, and $\mathit{on}(A, B)$ after move 3. But move 1, which clears $A$, serves the goal $\mathit{on}(A, B)$, and the shortest plan for $\mathit{on}(B, C)$ alone has only 1 move. So the optimal plan starts work on one goal, switches to the other, and then finishes the first. No plan that solves one goal completely before it starts the other can be optimal. The goals are not independent: they interact through the shared block $B$ and through the order in which blocks must become clear.

### Who found it

The example is usually named after Sussman, whose HACKER program met it. Gupta and Nau (1992) credit it to Allen Brown, citing Waldinger (1977, p. 127), and state that Sussman made it widely known.

## Examples

- Larger instances. Any goal that asks for a tower in a different order than the blocks are in now has the same structure: a block that must end up high is buried under a block that must end up low. Gupta and Nau call such mutual blocking a deadlock, and deadlocks are what make optimal blocks world planning NP-hard.
- The four-operator encoding. The interaction is the same, but every count doubles: optimum 6, goal-by-goal 10.
- Interacting goals outside blocks. Swapping the values of two registers with only assignment actions is a similar case: making $x$ hold the old value of $y$ destroys the value that $y$ needs to receive, so one goal must be prepared before the other is achieved, with a temporary register.

## Where it is used

- As a test case. Nearly every textbook planning method is shown on it, because it is the smallest task on which goal-by-goal planning fails.
- Motivation for plan-space planning. Partial-order planners such as [POP](/pop-partial-order-planning/) record why each action is in the plan with [causal links](/causal-link/), detect when one action threatens another goal, and order the actions to avoid the threat. On the anomaly this orders "move $C$ to the table" before "move $B$ onto $C$" before "move $A$ onto $B$" without committing to an order early; see the [least commitment principle](/least-commitment-principle/) and [plan-space planning](/plan-space-planning/).
- Motivation for regression and interleaving. [Goal regression](/goal-regression/), as in Waldinger's work, passes a goal back through the actions of a partial plan, so that a new action can be inserted at an earlier point. [Means-ends analysis](/means-ends-analysis/) in its original form, which works on one difference at a time, has the same trouble as any goal-by-goal method.
- Modern planners. A forward state-space search with a domain-independent heuristic solves the anomaly at once, since it searches over whole states and never splits the goal. The anomaly remains the standard example of goal interaction, which heuristics such as those of the [delete relaxation](/delete-relaxation/) partly ignore.

## References
