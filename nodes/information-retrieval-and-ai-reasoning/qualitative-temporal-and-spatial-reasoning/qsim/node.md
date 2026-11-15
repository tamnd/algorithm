---
tag: 9H896N
kind: algorithm
slug: qsim
name: QSIM
aliases:
- Kuipers qualitative simulation
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Kuipers's 1986 qualitative simulation. From a qualitative differential equation it builds a tree of possible behaviors by Table 1 transitions and constraint filtering. Sound, not complete.
model: word-ram
complexity:
  vars: {n: the number of variables, c: the number of constraints, b: the number of states in the behavior tree, L: the largest number of landmarks of a variable, m: the bound on the length of a behavior}
  time: {worst: "O(b (c^3 + c n 4^n))"}
  space: {extra: "O(b (n L + c m))"}
properties: {deterministic: true, exact: false, in_place: false, online: false, recursive: false}
history:
  year: 1986
  people: [Benjamin Kuipers]
  note: Kuipers (Artificial Intelligence 29, 1986) defined qualitative differential equations and the QSIM algorithm, proved that it never misses a real behavior (Theorem 5.2) and showed that it can predict behaviors that no real system has (Theorem 5.3).
prereqs: [ode-initial-value-problem, constraint-satisfaction-problem, arc-consistency]
see_also: [qualitative-process-theory, euler-method, constraint-propagation, forward-checking]
sources:
  - paper: doi:10.1016/0004-3702(86)90073-1
    title: Benjamin Kuipers, Qualitative simulation, Artificial Intelligence 29(3), 1986
    locator: pages 289 to 338 (Section 2 reasonable functions and qualitative states, Section 3 the constraints, Section 4.2 the algorithm, Table 1 the transitions, Section 4.3 the ball thrown upward, Section 4.8 the global filters, Theorem 5.2 soundness, Theorem 5.3 spurious behaviors of the spring, Appendices A and B the proofs)
  - paper: "Benjamin Kuipers, Qualitative Reasoning: Modeling and Simulation with Incomplete Knowledge, MIT Press, 1994"
    locator: the book account of qualitative differential equations, QSIM and its later filters
  - paper: doi:10.1016/0004-3702(84)90038-9
    title: Kenneth D. Forbus, Qualitative process theory, Artificial Intelligence 24, 1984
    locator: pages 85 to 168 (quantity spaces and influences, the modelling language that QSIM models are often compiled from)
  - paper: "Johan de Kleer and John Seely Brown, A qualitative physics based on confluences, Artificial Intelligence 24, 1984"
    locator: pages 7 to 83 (confluences, an earlier qualitative physics with sign equations)
---

QSIM predicts how a physical system can change over time when its laws are known only qualitatively, for example "the force grows with the stretch of the spring" with no number for the stiffness. It reasons about continuous systems that a differential equation describes, not about temporal or spatial relations between events or regions as the other calculi in this area do. From a qualitative differential equation and an initial state, it builds a tree whose branches are the possible behaviors. Kuipers (1986) proved that QSIM is sound but not complete: every real behavior is in the tree, but the tree can also contain behaviors that no real system has.

## In plain words

Throw a ball up. You do not know its speed or the strength of gravity, but you know that the height grows while the speed is positive and that the speed falls all the time. From that alone you can say what happens: the ball goes up, stops at some highest point, falls back to where it started and goes on down.

QSIM does this step by step. Each quantity is described only by where it is among a few named values, such as zero or the starting speed, and by whether it goes up, stays, or goes down. For each quantity it lists the few ways that this description can change next. It keeps only the combinations that agree with the laws, and each surviving combination starts a new branch. When a quantity stops between two named values, that point gets a new name, such as "highest point".

## The problem

A *qualitative differential equation* has a list of variables, a *quantity space* for each variable (a finite ordered list of landmark names from $-\infty$ to $+\infty$ that contains 0), and constraints between variables: DERIV$(f, g)$ for $g = f'$, $M^+(f, g)$ and $M^-(f, g)$ for $f = H(g)$ with $H$ strictly increasing or strictly decreasing, ADD$(f, g, h)$ for $f + g = h$, MINUS$(f, g)$ for $f = -g$, and CONSTANT$(f)$. A monotonic or ADD constraint can carry *corresponding values*, tuples of landmarks that the functions take at the same time, such as $H(0) = 0$. Many [ordinary differential equations](/ode-initial-value-problem/) with unknown functions and constants give the same qualitative equation.

The *qualitative state* of a variable is a pair: its value, which is a landmark or an open interval between two adjacent landmarks, and its direction, inc, std or dec. The input is a qualitative differential equation, the qualitative state of every variable at the time point $t_0$, and a bound on the length of a behavior. The output is the tree of behaviors: sequences of states that alternate between time points and the open intervals between them, each with a status (cycle, quiescent, end or cut).

## The algorithm

```pseudo id=main
QSIM(variables, quantity spaces, constraints, initial state, max)
L1  S0 ← the initial state at the time point t0, with the corresponding values that it shows
L2  ACTIVE ← {S0}
L3  while ACTIVE is not empty do take a state S from ACTIVE; if its depth is max then record the behavior of S as cut and continue
L4      for each variable, list its transitions from Table 1: P rules if S is a time point, I rules if S is an interval; drop the moves to minus or plus infinity
L5      for each constraint, keep the tuples of transitions of its arguments that the constraint accepts
L6      Waltz filtering: remove a tuple if a constraint that shares a variable with it has no tuple with the same transition for that variable; repeat until nothing changes
L7      find every global interpretation by depth-first search: one transition per variable, so that each constraint gets one of its kept tuples
L8      build one successor for each interpretation; an I8 or I9 move adds a new landmark, and arguments that are all at landmarks add corresponding values
L9      No Change: if S is an interval, drop a successor in which every variable takes I1, I4 or I7
L10     Cycle: if a time-point successor equals an earlier time-point state on its path, record its behavior as a cycle
L11     Quiescence: else if every direction of a time-point successor is std, record its behavior as quiescent
L12     else push the successor onto ACTIVE
L13     if no successor of S is left after line L9, record the behavior of S as end
```

Line L4 uses Table 1 of Kuipers (1986). From a time point, a variable at a landmark with direction std can stay (P1) or move into the interval above (P2) or below (P3); with direction inc or dec it moves into the next interval (P4, P6); inside an interval it stays there (P5, P7). From an interval, a variable that increases in $(l_j, l_{j+1})$ can reach $l_{j+1}$ and stop (I2) or go on (I3), stay inside the interval (I4), or stop inside it at a new landmark (I8); I5, I6, I7 and I9 are the decreasing cases, and I1 keeps a variable constant at a landmark. So each variable has at most four candidates.

Line L5 tests each tuple against the meaning of the constraint. For DERIV$(f, g)$ the direction of $f$ must be the sign of $g$. For $M^+$ the two directions must be equal, and for each pair of corresponding values $(p, q)$ the sign of $f - p$ must equal the sign of $g - q$. For ADD the signs must be possible for a sum of reals. Line L6 is [arc consistency](/arc-consistency/) between constraints that share a variable, the method that Waltz used for line drawings. Line L7 then solves the remaining [constraint satisfaction problem](/constraint-satisfaction-problem/) exactly. Lines L9 to L11 are the global filters of Kuipers (1986, Section 4.8), and line L4 also removes moves to $\pm\infty$, so the implementation predicts only finite behaviors.

## Example

The ball of Kuipers (1986, Section 4.3) has the variables $Y$ (height), $V$ (velocity) and $A$ (acceleration), the constraints DERIV$(Y, V)$, DERIV$(V, A)$ and CONSTANT$(A)$, and the quantity spaces $Y$: $-\infty, 0, \infty$; $V$: $-\infty, 0, v_0, \infty$; $A$: $-\infty, g, 0, \infty$, with $g < 0$. The initial state is $Y = 0$ inc, $V = v_0$ dec and $A = g$ std.

| State | $Y$ | $V$ | $A$ | Transitions |
| --- | --- | --- | --- | --- |
| $t_0$ | $0$, inc | $v_0$, dec | $g$, std | initial |
| $(t_0, t_1)$ | $(0, \infty)$, inc | $(0, v_0)$, dec | $g$, std | P4, P6, P1 |
| $t_1$ | $Y_{max}$, std | $0$, dec | $g$, std | I8, I6, I1 |
| $(t_1, t_2)$ | $(0, Y_{max})$, dec | $(-\infty, 0)$, dec | $g$, std | P3, P6, P1 |
| $t_2$ | $0$, dec | $(-\infty, 0)$, dec | $g$, std | I6, I7, I1 |
| $(t_2, t_3)$ | $(-\infty, 0)$, dec | $(-\infty, 0)$, dec | $g$, std | P6, P7, P1 |

At the state on $(t_0, t_1)$, line L4 gives $Y$ the candidates I4 and I8 (I2 and I3 would go to $\infty$), $V$ the candidates I5, I6, I7 and I9, and $A$ only I1. Line L5 keeps for DERIV$(Y, V)$ the pairs (I4, I7), (I4, I9), (I8, I5) and (I8, I6): $Y$ goes on rising only while $V$ is positive. For DERIV$(V, A)$ it keeps (I6, I1) and (I7, I1), since $V$ must decrease. Line L6 removes (I4, I9) and (I8, I5), and line L7 gives two interpretations. The interpretation (I4, I7, I1) changes nothing and is removed by line L9. The other one, (I8, I6, I1), is the top of the flight: $V$ reaches 0 and $Y$ stops at the new landmark $Y_{max}$. In the last state every candidate of $Y$ and $V$ except I7 and I9 goes to $-\infty$, the only interpretation is (I7, I7, I1), and line L9 removes it, so the behavior ends with the ball falling below its start.

**A spurious behavior.** Take the spring without friction: DERIV$(X, V)$, DERIV$(V, A)$ and $M^-(A, X)$ with the corresponding values $(0, 0)$, starting at $X = 0$ inc, $V = v_0$ std, $A = 0$ dec. With a bound of 10 states QSIM returns three behaviors. One is a cycle: the spring stretches to $X_3$, comes back to $X = 0$ with speed $V_4 < 0$, compresses to $X_4 < 0$ and returns to $X = 0$, $V = v_0$. In the two others, after one swing the spring comes back to $X = 0$ with a new speed landmark $V_5 \ne v_0$, or reaches $V = v_0$ while $X$ is not 0. Every real spring keeps the energy $\int_0^X H(y)\,dy + V^2/2$, so it must pass $X = 0$ with speed $v_0$ again, and these two behaviors are impossible. This is Theorem 5.3 of Kuipers (1986): the constraints do not express the energy law, so QSIM cannot rule them out.

## Correctness

QSIM is sound: if a real system with reasonable functions (continuous, continuously differentiable, with finitely many critical points in a bounded interval) satisfies the qualitative equation and starts in the initial state, its qualitative behavior is a branch of the tree, up to the names of new landmarks (Kuipers 1986, Theorem 5.2). The proof goes step by step. Table 1 lists every change that one reasonable function can make between adjacent distinguished time points (Appendix A). Each constraint test of line L5 is a consequence of the real relation, so it accepts the true tuple (Appendix B). Waltz filtering removes only tuples that cannot be part of any global interpretation, the search of line L7 finds every global interpretation, and the filters of lines L9 to L11 remove only states that add nothing new.

QSIM is not complete: a branch need not be the behavior of any real system, as the spring shows. The constraints are tested locally, one time step at a time, and facts that link distant states, such as conservation of energy, are lost. The full proof for this implementation is in [proofs/correctness.md](proofs/correctness.md). The tests also check soundness against numeric solutions: they integrate a ball and a damped spring with the [Euler method](/euler-method/) for random constants and check that each sampled trajectory, read qualitatively, is a prefix of a branch.

## Complexity

Each variable has at most four candidates, so line L5 tests at most $4^3$ tuples per constraint, $O(c)$ tests in total. Each pass of line L6 compares every pair of constraints, $O(c^2)$ pairs with at most $4^3$ tuples each, and every pass except the last removes a tuple, so there are $O(c)$ passes and $O(c^3)$ work. Line L7 can visit up to $4^n$ choices and check $O(c)$ constraints at each of $n$ levels, which is $O(c n 4^n)$. One state therefore costs $O(c^3 + c n 4^n)$, and the whole run costs $O(b (c^3 + c n 4^n))$ for $b$ states. Each state stores the quantity spaces, at most $L$ landmarks for each of the $n$ variables, and the corresponding values, at most $m$ tuples per constraint for a bound $m$ on the length of a behavior, which gives the space bound.

The real cost is the size $b$ of the tree, which can grow exponentially with the length bound. For the damped spring of the tests, the number of behaviors is 1, 7, 29, 123 and 535 for the bounds 4, 6, 8, 10 and 12. Most of this growth comes from branching on variables whose direction is not fixed by the equation, so that every order of their changes becomes a separate branch.

## Properties

- **Sound.** No real behavior is missing from the tree (Kuipers 1986, Theorem 5.2).
- **Not complete.** The tree can contain spurious behaviors (Kuipers 1986, Theorem 5.3).
- **Deterministic.** The tree depends only on the input; the order of the branches depends on the order of the variables.
- **Makes new landmarks.** Lines L4 and L8 add a landmark each time a variable stops inside an interval, such as the top of the ball's flight, so the quantity spaces grow along a branch.
- **Needs no numbers.** It uses only signs and order. A model with unknown constants describes every system with any values of those constants.

## Variants and improvements

- **Global filters.** Kuipers's pure algorithm has the No Change and Cycle filters and the treatment of infinite values. Later work added filters that use energy, higher-order derivatives and the shape of phase space to remove many spurious behaviors.
- **Numeric ranges.** Q2 and its successors attach real intervals to the landmarks and remove behaviors whose ranges become empty, so that the tree mixes qualitative and partial numeric knowledge.
- **Model building.** [Qualitative process theory](/qualitative-process-theory/) writes the model in terms of processes and influences; its models can be compiled into qualitative differential equations for QSIM.
- **Confluences.** De Kleer and Brown's qualitative physics uses sign equations between derivatives, called confluences, in place of the constraint types of QSIM.

## When to use it

Use QSIM when the structure of a system is known but its parameters are not, and you want every behavior that the structure allows: diagnosis, monitoring, design checks, teaching physics. When a few numbers are known, use one of the variants with numeric ranges. When all parameters are known, a numeric method for the [initial value problem](/ode-initial-value-problem/) gives one exact behavior and is much cheaper. Because the result can contain spurious behaviors, a branch that QSIM predicts is a possibility to check, not a proof that the system can do it; a property that holds on every branch does hold for every real system.

## Pitfalls

- **No No Change filter.** If line L9 is left out, an interval state has a successor that repeats it with I1, I4 or I7 for every variable, and the tree fills with copies of the same interval. In the ball example, (I4, I7, I1) would follow every interval. Line L9 must drop that successor when $S$ is an interval.
- **Taking the product after Waltz filtering.** If line L7 is replaced by every combination of the candidates that survive line L6, the result can contain combinations that break a constraint, because arc consistency is a local test. Line L7 must check each constraint against the full choice.
- **Mixing up the P and I rules.** If line L4 applies the I rules at a time point, a variable at 0 with direction inc can stay at 0, which no differentiable function does. Line L4 must use the P rules after a time point and the I rules after an interval, so that states alternate.
- **Testing a new landmark as an old one.** A landmark found by I8 or I9 lies strictly inside the interval. If line L5 compares it as equal to the end of the interval, DERIV$(Y, V)$ can reject the top of the ball's flight. Line L5 must treat it as the open interval until line L8 puts it into the quantity space.
- **Reading a branch as a guarantee.** If the behaviors that line L12 and lines L10 and L11 record are reported as real, spurious branches such as the two of the spring are reported too. A recorded branch is only a possible behavior; check it with more knowledge, such as energy, before you report it as real.

## Implementations

## History

Kuipers (1986) defined qualitative differential equations and the QSIM algorithm, gave the ball and the spring as examples, and proved Theorems 5.2 and 5.3 on soundness and spurious behaviors. Earlier qualitative physics, such as the confluences of de Kleer and Brown (1984) and the qualitative process theory of Forbus (1984), had the same aim with different representations. Kuipers's book (1994) collects QSIM and its later filters and numeric extensions.

## References
