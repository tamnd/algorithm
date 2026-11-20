---
tag: GWGCR1
kind: algorithm
slug: boston-mechanism
name: Boston mechanism
aliases:
- immediate acceptance mechanism
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Each round, every unassigned student applies to her next school and schools accept by priority for good. Pareto efficient for the reported lists, but not strategyproof and not stable.
solves: [school-choice-problem]
model: word-ram
complexity:
  vars: {n: the number of students, m: the number of schools}
  time: {worst: O(n m log n)}
  space: {extra: O(n m)}
properties: {deterministic: true, recursive: false}
history:
  year: 2003
  people: [Atila Abdulkadiroglu, Tayfun Sonmez]
  note: Boston Public Schools and other districts used this rule for years. Abdulkadiroglu and Sonmez analyzed it in 2003, and Boston replaced it with student-proposing deferred acceptance in 2005.
prereqs: [school-choice-problem, gale-shapley]
see_also: [school-choice-problem, gale-shapley, top-trading-cycles, serial-dictatorship, hospitals-residents-problem, dominant-strategy-incentive-compatibility, pareto-optimality, nash-equilibrium]
sources:
  - paper: doi:10.1257/000282803322157061
    title: Atila Abdulkadiroglu and Tayfun Sonmez, School choice, a mechanism design approach, American Economic Review 93(3), 729 to 747 (2003)
    locator: the description of the Boston student assignment mechanism and its shortcomings
  - paper: doi:10.1016/j.jpubeco.2005.02.002
    title: Haluk Ergin and Tayfun Sonmez, Games of school choice under the Boston mechanism, Journal of Public Economics 90(1-2), 215 to 237 (2006)
    locator: the results on the Nash equilibria of the Boston game under complete information
  - paper: doi:10.1257/000282805774669637
    title: Atila Abdulkadiroglu, Parag A. Pathak, Alvin E. Roth and Tayfun Sonmez, The Boston public school match, American Economic Review 95(2), 368 to 371 (2005)
    locator: the whole paper (the old rule, the evidence of strategic play, and the change to deferred acceptance)
  - paper: doi:10.1257/aer.98.4.1636
    title: Parag A. Pathak and Tayfun Sonmez, Leveling the playing field, sincere and sophisticated players in the Boston mechanism, American Economic Review 98(4), 1636 to 1652 (2008)
    locator: the whole paper (equilibria with sincere and sophisticated students)
  - paper: doi:10.1016/j.jet.2004.10.006
    title: Yan Chen and Tayfun Sonmez, School choice, an experimental study, Journal of Economic Theory 127(1), 202 to 231 (2006)
    locator: the whole paper (laboratory comparison of the Boston mechanism, deferred acceptance and top trading cycles)
  - paper: doi:10.1257/aer.101.1.399
    title: Atila Abdulkadiroglu, Yeon-Koo Che and Yosuke Yasuda, Resolving conflicting preferences in school choice, the Boston mechanism reconsidered, American Economic Review 101(1), 399 to 410 (2011)
    locator: the whole paper (ex ante welfare with cardinal preferences and equal priorities)
---

The Boston mechanism assigns students to schools in rounds: in round $k$ every student who has no seat yet applies to the $k$-th school on her list, and each school takes applicants by priority up to the seats it has left, and keeps them for good. It is one algorithm for the [school choice problem](/school-choice-problem/), which defines the input and the goals. It differs from student-proposing [deferred acceptance](/gale-shapley/) in one point: deferred acceptance holds applicants only tentatively, so a later applicant with higher priority can take the seat, while the Boston mechanism accepts immediately. That one change makes the outcome Pareto efficient for the reported lists, but it destroys strategyproofness and stability.

## In plain words

Every student writes a ranked list of schools. In the first round, each school looks only at the students who put it first and fills its seats with the best of them by its priority order. Those students are done. In the second round, the students who are left apply to their second choice, and schools that still have seats fill them the same way. This goes on until every list is used up. The trouble is that a seat at a popular school is lost if you do not rank it first. So a student who expects to lose at her favorite school does better to rank a safer school first, and honest families can lose out to families that play this game.

## The problem

There are $n$ students and $m$ schools. School $s$ has $q_s \ge 0$ seats and a strict priority order $\succ_s$ over all students. Each student $i$ reports a strict list $P_i$ of the schools she finds acceptable, best first; the list may be shorter than $m$. An assignment gives each student at most one school on her list and gives school $s$ at most $q_s$ students. The full problem, with the properties a district may want (stability, efficiency and strategyproofness), is on [school choice problem](/school-choice-problem/).

## The algorithm

```pseudo id=main
BOSTON(lists P, priorities, capacities q)
L1  left[s] ← q_s for each school s;  U ← the set of all students
L2  for k ← 1 to m do
L3      for each school s do A_s ← the students i ∈ U with s at place k of P_i
L4      for each school s with A_s nonempty do
L5          T ← the min(left[s], |A_s|) students of A_s with the highest priority at s
L6          assign every student of T to s for good;  U ← U \ T;  left[s] ← left[s] - |T|
L7  return the assignment (the students still in U get no school)
```

Line L3 collects the applications of round $k$. A student whose list is shorter than $k$ does not apply. Lines L5 and L6 are the immediate acceptance: an accepted student never loses her seat, and a rejected student never comes back to that school. A school whose seats are gone after a round rejects every later applicant, whatever her priority.

## Example

Three students $i_1, i_2, i_3$ and three schools $s_1, s_2, s_3$ with one seat each. The lists and priorities are:

| student | list | | school | priority |
|---|---|---|---|---|
| $i_1$ | $s_2, s_1, s_3$ | | $s_1$ | $i_1, i_3, i_2$ |
| $i_2$ | $s_3, s_2, s_1$ | | $s_2$ | $i_3, i_2, i_1$ |
| $i_3$ | $s_3, s_2, s_1$ | | $s_3$ | $i_1, i_2, i_3$ |

| round | applications | accepted | seats left after the round |
|---|---|---|---|
| 1 | $i_1 \to s_2$; $i_2, i_3 \to s_3$ | $i_1$ at $s_2$; $i_2$ at $s_3$ (higher priority than $i_3$) | $s_1$: 1, $s_2$: 0, $s_3$: 0 |
| 2 | $i_3 \to s_2$ | nobody, $s_2$ is full | $s_1$: 1 |
| 3 | $i_3 \to s_1$ | $i_3$ at $s_1$ | none |

The outcome is $i_1 \to s_2$, $i_2 \to s_3$, $i_3 \to s_1$. Student $i_3$ gets her last choice.

The outcome is not stable. Student $i_3$ prefers $s_2$ to $s_1$, and $s_2$ gives $i_3$ higher priority than $i_1$, who holds the seat. This is justified envy. Student-proposing deferred acceptance on the same lists gives $i_1 \to s_1$, $i_2 \to s_3$, $i_3 \to s_2$, which is stable.

The mechanism is not strategyproof. Suppose $i_3$ reports $s_2, s_3, s_1$ instead. In round 1, $i_1$ and $i_3$ both apply to $s_2$, and $s_2$ takes $i_3$, who has higher priority. Student $i_2$ gets $s_3$. In round 2, $i_1$ applies to $s_1$ and gets it. Now $i_3$ has $s_2$, her second true choice, instead of $s_1$, her third. The lie gains her one place. The tests in `impl/python` check this example, the trace above and the manipulation.

## Correctness

The full proofs are in `proofs/correctness.md`. The main claims are these.

- **Feasibility.** Each student gets at most one school, which is on her list, and no school takes more than $q_s$ students. Line L5 never takes more than the seats left.
- **Pareto efficiency for the reported lists.** No other assignment makes some student better off, by her reported list, and no student worse off. The proof is an induction on the rounds: a student accepted in round $k$ was rejected in rounds $1, \ldots, k-1$ by schools that were full of students accepted in earlier rounds, and these students cannot be moved without hurting them.
- **Most first choices.** The number of students who get their reported first choice is the maximum over all assignments. Round 1 gives school $s$ exactly $\min(q_s, f_s)$ students, where $f_s$ is the number of students who list $s$ first, and no assignment can give more.
- **Deferred acceptance in disguise.** Change the priority of school $s$ so that students who list $s$ at place $1$ come first, then those who list it at place $2$, and so on, with ties broken by $\succ_s$. Student-proposing deferred acceptance with these adjusted priorities gives exactly the Boston outcome. The tests use this as the reference method on random instances.

The efficiency is only for the reported lists. When students misreport, the outcome can be inefficient for their true preferences, and in the example above the truthful outcome leaves justified envy.

## Complexity

Line L1 and the precomputation of a rank table, so that the priority of a student at a school is found in constant time, take $O(nm)$ time and space. There are $m$ rounds. In each round, line L3 scans the unassigned students, and line L5 sorts the applicants of each school by priority, so a round costs $O(n \log n)$ and the whole run $O(nm \log n)$. Each student applies at most once per round, so there are at most $nm$ applications in total. With a linear-time selection of the top $\text{left}[s]$ applicants instead of a sort, the time is $O(nm)$, which is the size of the input when all priorities are given.

## Properties

- **Not strategyproof.** Ranking a school first is the only safe way to get it, so a student can gain by ranking a less popular school first, as in the example.
- **Not stable.** The outcome can leave justified envy (the example). Deferred acceptance is stable and strategyproof for students; see [Gale-Shapley](/gale-shapley/).
- **Equilibria are stable matchings.** Ergin and Sonmez (2006) proved that, when all students know all lists and priorities (complete information) and play the Boston game, the outcomes of its Nash equilibria are exactly the stable matchings for the true preferences. So in equilibrium the Boston mechanism does at best what deferred acceptance does under truth, and the student-optimal stable matching is among the equilibrium outcomes. The tests check this claim by brute force over all $6^3 = 216$ report profiles of 3 students and 3 schools.
- **Sincere and sophisticated students.** Pathak and Sonmez (2008) studied a mix of students who report truthfully and students who play best responses. They show that the best equilibrium outcome for the sophisticated students is the student-optimal stable matching of a changed economy, in which the sincere students lose their priority to sophisticated students at every school except their first choice.
- **Pareto efficient for the reports.** See Correctness. It is not efficient for the true preferences in general.

## Variants and improvements

- **Deferred acceptance.** Replace the immediate acceptance in line L6 by tentative holding. This is the mechanism Boston adopted in 2005.
- **Top trading cycles for schools.** Efficient and strategyproof for students, but not stable; see [top trading cycles](/top-trading-cycles/) and the comparison on [school choice problem](/school-choice-problem/).
- **Truncated lists.** Many districts limit the length of the list. With a short list, even deferred acceptance stops being strategyproof, because a student must choose which schools to list.
- **Tie-breaking.** Real priorities have large classes of equal priority (walk zone and siblings). A lottery breaks the ties, either one lottery for all schools or one per school; the Boston mechanism then works on the strict priorities.
- **Ex ante welfare.** With cardinal preferences and equal priorities, Abdulkadiroglu, Che and Yasuda (2011) show that the Boston mechanism can give every student a higher expected utility in equilibrium than deferred acceptance, because a student can show how strongly she wants a school by ranking it first.

## When to use it

Use it to model a district that uses immediate acceptance, or to measure how much honest families lose. For a new design, deferred acceptance is the usual choice when stability matters, and top trading cycles when efficiency for students matters more; both make truth telling a dominant strategy for students. The Boston mechanism is a reasonable choice only when a designer wants students to signal intensity of preference and accepts that strategic skill then matters.

## Pitfalls

- Efficiency for the reported lists is not efficiency for the true preferences. Reports under the Boston mechanism are often strategic, so welfare figures computed from reports mean little.
- A student who is rejected in round $k$ does not reapply to that school later, even if seats appear. Seats never appear, because acceptance is final.
- In the version used in practice, a student may list fewer schools than there are; a student whose list is used up stays unassigned and goes to an administrative assignment. The pseudocode returns no school for her.
- The rule depends on the round in which a student applies, not only on her priority, so a high-priority student can lose a seat to a low-priority student. Do not describe the outcome as "assignment by priority".
- Laboratory evidence is a measurement, not a theorem: Chen and Sonmez (2006) found a high rate of preference manipulation under the Boston mechanism in their experiments.

## Implementations

## History

Boston and several other US school districts used versions of this rule, which Abdulkadiroglu and Sonmez (2003) analyzed under the name Boston student assignment mechanism. They showed that it is not strategyproof and not stable, and proposed deferred acceptance and top trading cycles instead. Abdulkadiroglu, Pathak, Roth and Sonmez (2005) documented that some Boston families played the rule strategically, and in 2005 Boston Public Schools replaced it by student-proposing deferred acceptance. Ergin and Sonmez (2006) characterized its Nash equilibria under complete information. The name "immediate acceptance" contrasts it with deferred acceptance.

## References
