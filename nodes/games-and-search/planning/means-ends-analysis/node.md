---
tag: GDKDXZ
kind: algorithm
slug: means-ends-analysis
name: Means-ends analysis
aliases:
- General Problem Solver
area: games-and-search/planning
level: intro
summary: Picks a difference between the state and the goal, applies an operator that removes it after it solves the operator's preconditions as a subproblem, and repeats. GPS uses it. It is incomplete.
solves: [classical-planning]
model: word-ram
complexity:
  vars: {n: the number of facts, m: the number of actions, k: the depth bound on nested subproblems}
  time: {worst: O(n (2 n m)^k), best: O(n)}
  space: {extra: "O(k (n + 2^k))"}
properties: {deterministic: true}
prereqs: [strips, goal-regression]
see_also: [backward-state-space-search, goal-regression, sussman-anomaly, pop-partial-order-planning, forward-state-space-search, hierarchical-task-network, state-space-planning, depth-first-search]
sources:
  - book: isbn:9780134454030
    title: Allen Newell and Herbert A. Simon, Human Problem Solving, Prentice-Hall, 1972
    locator: the chapters on GPS, means-ends analysis and the table of connections (general locator)
  - book: isbn:9781558601918
    title: Peter Norvig, Paradigms of Artificial Intelligence Programming, Case Studies in Common Lisp, Morgan Kaufmann, 1992
    locator: Chapter 4 (GPS, the General Problem Solver; the clobbered sibling goal problem and the leaping before you look problem)
  - paper: doi:10.1016/0004-3702(71)90010-5
    title: "Richard E. Fikes and Nils J. Nilsson, STRIPS: a new approach to the application of theorem proving to problem solving, Artificial Intelligence 2(3-4) (1971)"
    locator: pp. 189 to 208 (the GPS-style search of STRIPS for operators relevant to the differences)
  - book: isbn:9781558608566
    title: Malik Ghallab, Dana Nau and Paolo Traverso, Automated Planning, Theory and Practice, Morgan Kaufmann, 2004
    locator: Chapter 4, Section 4.4 (the STRIPS algorithm, a means-ends planner, and its incompleteness)
---

Means-ends analysis is the method of the General Problem Solver (GPS) of Newell, Shaw and Simon. It compares the current state with the goal and finds the *differences*, the goal conditions that do not hold. It picks one difference and an operator that removes it, taken from a *difference table* that lists, for each kind of difference, the operators that can remove it. If the operator cannot be applied yet, the method sets up a subproblem: make the preconditions of the operator true, with the same method. Then it applies the operator and goes on with the differences that are left. In a [STRIPS](/strips/) task a difference is a goal fact that is false, and the table lists the actions that add it. The method is goal directed, like [backward search](/backward-state-space-search/), but it builds the plan from the front and it can only produce plans of a special shape. It is sound, and with a depth bound it always stops, but it is incomplete: some solvable tasks have no plan that it can find.

## In plain words

You want to go to a meeting in another city. The difference between where you are and where you want to be is a long distance. The table says: for a long distance, take a train. But to take a train you must be at the station, which is a new difference. For a short distance, walk. So you walk to the station, take the train, and then work on what is left, for example the walk from the station to the office.

The method always asks: what is the difference, and what removes it? It solves the preconditions of the step first, takes the step, then looks at the goal again. People often plan this way. But it never takes a step that removes no difference. If the only plan needs such a step early, for example "save a copy first", the method does not find it.

## The problem

The input is a ground STRIPS task $(F, A, I, G)$, as on [forward search](/forward-state-space-search/): facts $F$, actions $A$ with preconditions, add lists and delete lists, an initial state $I$ and a goal $G$. Write $s[o] = (s \setminus \mathit{del}(o)) \cup \mathit{add}(o)$. The input also has a depth bound $k$ on the nesting of subproblems and an order in which to try the differences. The output is a plan for the task, or *failure*. Failure does not mean that no plan exists. Write $n = |F|$ and $m = |A|$.

## The algorithm

```pseudo id=main
MEANS-ENDS(A, I, G, k)
L1  T ← the difference table: T[p] = the operators o with p ∈ add(o)
L2  r ← SOLVE(I, G, k)
L3  if r = failure then return failure
L4  return the plan of r

SOLVE(s, g, d)                          ▷ returns a final state and a plan, or failure
L5  if g ⊆ s then return (s, the empty plan)
L6  if d = 0 then return failure
L7  for each difference p in g \ s, in the chosen order do
L8      for each operator o in T[p] do
L9          r1 ← SOLVE(s, pre(o), d − 1)                ▷ subproblem: make o applicable
L10         if r1 = failure then continue
L11         (s1, π1) ← r1
L12         s2 ← (s1 \ del(o)) ∪ add(o)                  ▷ apply o
L13         r2 ← SOLVE(s2, g, d − 1)                    ▷ the differences that are left
L14         if r2 = failure then continue
L15         (s3, π2) ← r2
L16         return (s3, π1 · o · π2)
L17 return failure
```

SOLVE works on a pair: a state and a set of facts to make true. It returns the plan it found together with the state that the plan reaches, because the caller must go on from that state. Lines L7 and L8 backtrack over the choice of the difference and of the operator, but the result of a subproblem is fixed: SOLVE takes the first plan that a subproblem returns and never asks it for another one. Line L13 tests the whole goal $g$ again, and not only the differences that were left, so a goal fact that the operator or the subplan destroyed becomes a difference again. The depth bound $d$ falls by one on each nested call; without it the method can loop, for example by trying to make a precondition true with an operator whose own precondition is the goal it works on.

The implementation keeps a table of results keyed by $(s, g, d)$. The bound $d$ falls on each call, so a key is never on the call stack twice, and the table changes only the running time, not the result.

GPS had two more parts. Its differences were general features chosen by the user, such as "the distance is large" or "the object is in the wrong place", and it ordered them by difficulty, so it removed the hardest difference first. It also checked that a subproblem was easier than the problem that set it up. The STRIPS version above has one difference per false goal fact and leaves the order as an input.

## Example

In the delivery task of [forward search](/forward-state-space-search/), $I = \{t_A, p_A\}$ and $G = \{p_B\}$, with the differences tried in alphabetical order. The run with $k = 4$ goes as follows.

1. SOLVE($I$, $\{p_B\}$, 4). The difference is $p_B$, and $T[p_B]$ = (unload(B)). Its precondition $\{t_B, p_T\}$ does not hold, so a subproblem starts.
2. SOLVE($I$, $\{t_B, p_T\}$, 3). The first difference is $p_T$, and $T[p_T]$ = (load(A), load(B)). The precondition $\{t_A, p_A\}$ of load(A) holds, so the subplan is empty; after load(A) the state is $\{t_A, p_T\}$.
3. SOLVE($\{t_A, p_T\}$, $\{t_B, p_T\}$, 2). The difference is $t_B$, and drive(A,B) applies. The state is $\{t_B, p_T\}$, which contains the subgoal. Step 2 returns load(A), drive(A,B).
4. Back in step 1, unload(B) applies, the state is $\{t_B, p_B\}$, and the goal holds.

The plan is load(A), drive(A,B), unload(B), the shortest plan. On the logistics task with one truck, three places and 2 packages, the method with $k = 4$ finds a plan of 6 actions, which is also the shortest.

### Goals that interact

The [Sussman anomaly](/sussman-anomaly/) starts from C on A with A and B on the table and has the goal $\{\mathrm{on}(A,B), \mathrm{on}(B,C)\}$. With the alphabetical order the method works on on(A,B) first. For $k \le 4$ it fails. For $k = 5$ it returns 10 actions:

unstack(C,A), putdown(C), pickup(A), stack(A,B), unstack(A,B), putdown(A), pickup(B), stack(B,C), pickup(A), stack(A,B).

It reaches on(A,B) after 4 actions. Then on(B,C) is the only difference, and its subproblem clear(B) undoes on(A,B). After stack(B,C) the test of line L13 sees on(A,B) again and builds it a second time. The shortest plan has 6 actions. A larger bound does not help: the bounds 6, 8 and 10 give plans of 12, 14 and 16 actions, because a deeper subproblem accepts a first plan with detours such as pickup(A), putdown(A). On the Tower of Hanoi with 3 disks, $k = 4$ gives 11 moves where 7 are enough.

### A task it cannot solve

Three registers R1, R2 and R3 hold the values a, b and c. The goal is that R1 holds b and R2 holds a. The action assign(r, q) copies the value of q into r and overwrites the old value of r; the ground task has 36 actions. The shortest plan has 3 actions: copy R1 into R3, copy R2 into R1, copy R3 into R2. The implementation fails for every bound $k$ from 1 to 10.

The reason is the shape of the plans. For each difference the method applies one operator, and before it the method only makes the preconditions of that operator true. The first step of the swap, saving a in R3, removes no difference of the goal, and it is not a precondition of the operator that removes the first difference. Whatever the method does first, it overwrites R1 or R2 before the other value is saved, and the lost value can never come back. The [proof page](proofs/correctness.md) gives a version with 6 actions and proves that the method fails on it for every bound and every order of the differences.

## Correctness

The proofs are in [proofs/correctness.md](proofs/correctness.md). By induction on $d$, if SOLVE($s$, $g$, $d$) returns $(s', \pi)$, then $\pi$ is applicable from $s$, ends in $s'$, and $g \subseteq s'$: the subplan $\pi_1$ makes $\mathit{pre}(o)$ true, so $o$ applies, and $\pi_2$ ends in a state that contains $g$. So a returned plan is a plan (soundness). Every nested call has a smaller $d$ and the loops are finite, so the method stops. It is not complete: on the six-action swap every plan that SOLVE can build applies an operator that destroys the only copy of a value before the other copy exists, for every depth bound and every order of the differences.

## Complexity

**Time.** One call of SOLVE, apart from its nested calls, tests $g \subseteq s$ and loops over the pairs of a difference $p$ and an operator in $T[p]$. There are at most $\sum_o |\mathit{add}(o)| \le n m$ such pairs, and each makes two nested calls. So there are at most $(2 n m)^j$ calls at nesting level $j$, and the total time without the table is $O(n (2 n m)^k)$; the plans have at most $2^k - 1$ actions, since a plan at bound $d$ is two plans at bound $d - 1$ and one operator. The best case is $G \subseteq I$, one test in $O(n)$ time. With the table of results the number of distinct calls is at most the number of states times $m + 1$ subgoals ($G$ and the preconditions) times $k + 1$ bounds, which makes the time polynomial in the number of reachable states.

**Space.** The recursion is at most $k$ calls deep, and each call holds a state of $O(n)$ bits and a partial plan of at most $2^k$ actions, so the space is $O(k (n + 2^k))$ without the table.

## Properties

- **Sound.** Every returned plan is valid.
- **Terminating.** The depth bound makes it stop on every task.
- **Incomplete.** It can fail on a solvable task, for every depth bound, as the swap shows. A failure says nothing about solvability.
- **Not optimal.** It can return a plan much longer than the shortest, as on the Sussman task.
- **Linear.** The plan for a set of goals is built one goal at a time, so it cannot interleave the steps for different goals in arbitrary ways.
- **Goal directed.** It only tries operators that remove a difference, so it ignores most actions of a large task.

## Variants and improvements

- **GPS.** Differences are features chosen by the user, ordered by difficulty, and the table of connections lists the operators for each feature. GPS was applied to logic proofs, puzzles such as the missionaries and cannibals, and integration (Ernst and Newell 1969).
- **STRIPS.** The planner of Fikes and Nilsson (1971) used a goal stack in this style: it chose an operator relevant to a difference, pushed its preconditions as subgoals, and checked the whole goal again at the end. It is the STRIPS algorithm of Ghallab, Nau and Traverso, Section 4.4.
- **Goal protection.** Refuse to apply an operator that deletes a goal already reached. This removes the long Sussman plans, but then the Sussman task has no solution of the linear shape: with on(A,B) first, clearing B undoes it, and with on(B,C) first, B sits on C, which still sits on A, so clearing A undoes on(B,C).
- **Interleaving and regression.** Planners such as Warplan and Waldinger's planner insert an action at an earlier point of the plan and regress the goals through it ([goal regression](/goal-regression/)). This solves the register swap. [Partial-order planning](/pop-partial-order-planning/) goes further and keeps the order open until a conflict forces it.
- **Complete search.** [Backward state-space search](/backward-state-space-search/) considers every relevant action at every point of the plan, and it is complete.
- **Hierarchical planning.** [HTN planning](/hierarchical-task-network/) keeps the idea of reducing a problem to subproblems, with methods given by the user.

## When to use it

Use it as a model of how people plan, or for a quick planner in a domain where the goals are almost independent, so that each difference can be removed without damage to the others. Do not use it when completeness or short plans matter: use [forward search](/forward-state-space-search/) with a heuristic, or [backward search](/backward-state-space-search/). The method is also a good teaching example of how a natural heuristic idea can lose completeness.

## Pitfalls

- **Testing only the remaining differences.** After the operator, test the whole goal again (line L13). If the method only works on the differences that were left, it can return a plan that destroyed an earlier goal, as on the Sussman task.
- **No depth bound.** A subproblem can contain itself, for example when the precondition of the chosen operator needs the fact that the operator is supposed to add. Without a bound, or a check that the subproblem is new, the method does not stop.
- **Reading failure as unsolvability.** The method fails on the register swap, which has a plan of 3 actions.
- **Expecting a larger bound to give a better plan.** On the Sussman task the bounds 5, 6, 8 and 10 give 10, 12, 14 and 16 actions.
- **Losing the state of a subproblem.** The subplan changes the state, and the operator must be applied to the state at the end of the subplan, not to the state before it.

## Implementations

## History

Newell, Shaw and Simon described GPS at the International Conference on Information Processing in Paris in 1959. Its central method was means-ends analysis, with differences between objects, a table of connections from differences to operators, and subgoals to reduce a difference and to apply an operator. Ernst and Newell (1969) gave a full account of GPS and its use on many kinds of tasks in their book "GPS: A Case Study in Generality and Problem Solving", and Newell and Simon (1972) used the method in their theory of human problem solving. Fikes and Nilsson (1971) took the method into STRIPS, with differences computed by a theorem prover. The interaction of goals in the blocks world, found by Sussman (1975), and the register swap showed that the linear form of the method is incomplete, and led to planners that interleave goals and to [partial-order planning](/pop-partial-order-planning/).

## References
