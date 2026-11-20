---
tag: 3PBBBD
kind: problem
slug: school-choice-problem
name: School choice problem
aliases:
- student assignment problem
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: Assign students to schools with seats, given student preferences and school priorities. The goals are no justified envy, Pareto efficiency for students and strategyproofness.
model: word-ram
complexity:
  vars: {n: the number of students, m: the number of schools}
  time: {worst: O(n m)}
prereqs: [stable-matching, hospitals-residents-problem]
see_also: [boston-mechanism, gale-shapley, top-trading-cycles, hospitals-residents-problem, stable-matching-with-ties, house-allocation-problem, dominant-strategy-incentive-compatibility, pareto-optimality]
sources:
  - paper: doi:10.1257/000282803322157061
    title: Atila Abdulkadiroglu and Tayfun Sonmez, School choice, a mechanism design approach, American Economic Review 93(3), 729 to 747 (2003)
    locator: the whole paper (the model, the properties, and the student-optimal stable and top trading cycles mechanisms)
  - paper: doi:10.1257/000282805774670167
    title: Atila Abdulkadiroglu, Parag A. Pathak and Alvin E. Roth, The New York City high school match, American Economic Review 95(2), 364 to 367 (2005)
    locator: the whole paper
  - paper: doi:10.1257/000282805774669637
    title: Atila Abdulkadiroglu, Parag A. Pathak, Alvin E. Roth and Tayfun Sonmez, The Boston public school match, American Economic Review 95(2), 368 to 371 (2005)
    locator: the whole paper
  - paper: doi:10.1257/aer.98.3.669
    title: Aytek Erdil and Haluk Ergin, What's the matter with tie-breaking? Improving efficiency in school choice, American Economic Review 98(3), 669 to 689 (2008)
    locator: the whole paper (tie-breaking and stable improvement cycles)
  - paper: doi:10.1257/aer.99.5.1954
    title: Atila Abdulkadiroglu, Parag A. Pathak and Alvin E. Roth, Strategy-proofness versus efficiency in matching with indifferences, redesigning the NYC high school match, American Economic Review 99(5), 1954 to 1978 (2009)
    locator: the whole paper
  - paper: doi:10.1162/qjec.2010.125.3.1297
    title: Onur Kesten, School choice with consent, Quarterly Journal of Economics 125(3), 1297 to 1348 (2010)
    locator: the efficiency-adjusted deferred acceptance mechanism
  - book: isbn:9789814425247
    title: David F. Manlove, Algorithmics of Matching Under Preferences, World Scientific (2013)
    locator: Chapter 3 (the hospitals-residents problem and its variants)
---

The school choice problem asks how to assign students to public schools with limited seats, when each student ranks the schools and each school ranks the students by a priority set by law or policy (walk zone, siblings, a lottery number). It is the [hospitals-residents problem](/hospitals-residents-problem/) with one change of meaning: schools are not agents with preferences, only students are, so the welfare and the incentives that count are those of the students, and stability becomes a fairness rule called "no justified envy". This page states the problem and compares its mechanisms; the [Boston mechanism](/boston-mechanism/) is one of them, with its own page.

## In plain words

Every family ranks the schools it wants. Every school has a fixed number of seats and an order of priority among the students. A good assignment should be fair: if a student wants a school more than the one she got, then that school should be full of students with higher priority than her. It should not waste seats. It should be efficient: no other assignment should make some students happier and nobody less happy. And it should be safe to tell the truth. No method has all these properties at once, so a district must choose. Deferred acceptance is fair and safe, top trading cycles is efficient and safe, and the old Boston method is efficient for what families report but not safe.

## Definition

An instance has a set $I$ of $n$ students, a set $S$ of $m$ schools, a capacity $q_s \ge 1$ for each school, a strict priority order $\succ_s$ over $I$ for each school, and a strict preference order $P_i$ for each student over $S \cup \{\varnothing\}$, where $\varnothing$ is the outside option (a private school or an administrative assignment). School $s$ is acceptable to $i$ when $i$ ranks $s$ above $\varnothing$.

An *assignment* $\mu$ gives each student one element of $S \cup \{\varnothing\}$ and gives each school $s$ at most $q_s$ students. The properties are:

- *Individually rational*: every student gets an acceptable school or $\varnothing$.
- *Non-wasteful*: if $i$ prefers $s$ to $\mu(i)$, then $s$ has no empty seat.
- *No justified envy (fair)*: if $i$ prefers $s$ to $\mu(i)$, then every student at $s$ has higher priority at $s$ than $i$.
- *Stable*: all three of the above. A stable assignment is exactly a stable matching of the hospitals-residents instance in which school $s$ ranks students by $\succ_s$.
- *Pareto efficient (for students)*: no other assignment makes every student at least as well off and some student better off. The schools' priorities do not count here.

A *mechanism* maps every reported profile $(P_i)$ to an assignment. It is *strategyproof* (for students) when truthful reporting is a dominant strategy for every student: no student gets a school she prefers by reporting a false order, whatever the others report. The priorities are not reports; they are fixed by the district.

The output is an assignment; the measure is the set of properties above that the mechanism guarantees.

## Variants

- **Weak priorities.** Real priorities have large classes of equal students. A tie-breaking rule (one lottery for all schools, or one lottery per school) makes them strict. The choice changes the outcome and its efficiency; see [stable matching with ties](/stable-matching-with-ties/) for the general model.
- **Controlled choice.** Districts with diversity goals add type quotas or reserves to each school. Stability then needs a changed definition.
- **Short lists.** Many districts let a family list at most $k$ schools. With a short list, even deferred acceptance is not strategyproof, because the family must guess which schools to leave out.
- **Coarse outside options.** Some districts give every unassigned student a seat at a school near home, which changes the participation constraint.
- **Objects without priorities.** If schools have no priorities, the problem becomes the [house allocation problem](/house-allocation-problem/), solved for example by [serial dictatorship](/serial-dictatorship/).

## Examples

Three students and three schools with one seat each. The first instance has these lists and priorities:

| student | list | | school | priority |
|---|---|---|---|---|
| $i_1$ | $s_2, s_1, s_3$ | | $s_1$ | $i_1, i_3, i_2$ |
| $i_2$ | $s_3, s_2, s_1$ | | $s_2$ | $i_3, i_2, i_1$ |
| $i_3$ | $s_3, s_2, s_1$ | | $s_3$ | $i_1, i_2, i_3$ |

The three main mechanisms give three different assignments:

| mechanism | $i_1$ | $i_2$ | $i_3$ | properties of this outcome |
|---|---|---|---|---|
| student-proposing deferred acceptance | $s_1$ (2nd) | $s_3$ (1st) | $s_2$ (2nd) | stable |
| top trading cycles | $s_2$ (1st) | $s_1$ (3rd) | $s_3$ (1st) | Pareto efficient; $i_2$ has justified envy at $s_3$ |
| Boston mechanism | $s_2$ (1st) | $s_3$ (1st) | $s_1$ (3rd) | Pareto efficient for the reports; $i_3$ has justified envy at $s_2$ |

In top trading cycles, each student points to her top school and each school points to its top-priority student. The first cycle is $i_1 \to s_2 \to i_3 \to s_3 \to i_1$, so $i_1$ gets $s_2$ and $i_3$ gets $s_3$; then $i_2$ is left with $s_1$. But $i_2$ prefers $s_3$, and $s_3$ ranks $i_2$ above $i_3$, so the outcome is not fair.

The second instance shows that fairness and efficiency conflict. The lists are $i_1$: $s_2, s_1, s_3$; $i_2$: $s_1, s_2, s_3$; $i_3$: $s_1, s_2, s_3$; the priorities are $s_1$: $i_1, i_3, i_2$; $s_2$: $i_2, i_1, i_3$; $s_3$: $i_1, i_2, i_3$. A check of all six assignments shows that the only stable one is $i_1 \to s_1$, $i_2 \to s_2$, $i_3 \to s_3$. But $i_1$ and $i_2$ both prefer to swap, and the swap is fair to everyone except $i_3$, whose priority at $s_1$ is above $i_2$. So every stable assignment here is Pareto dominated, and no mechanism can be both stable and Pareto efficient. Both instances were checked by a script that enumerates all assignments.

## Known algorithms

- **Student-proposing deferred acceptance** ([Gale-Shapley](/gale-shapley/) on the hospitals-residents instance). It gives the student-optimal stable assignment: every student weakly prefers it to every other stable assignment. It is strategyproof for students (Dubins and Freedman 1981, Roth 1982; see [strategyproofness of deferred acceptance](/deferred-acceptance-strategyproofness/)). It is not Pareto efficient, as the second example shows. Time $O(nm)$ with complete lists. Boston adopted it in 2005, and New York City has used a version of it for its high school match since the 2003-04 school year.
- **Top trading cycles** ([top trading cycles](/top-trading-cycles/), with schools pointing by priority and capacities counted down). Pareto efficient and strategyproof for students, but not stable (first example). Abdulkadiroglu and Sonmez (2003) proposed it next to deferred acceptance.
- **Boston mechanism** ([Boston mechanism](/boston-mechanism/)). Pareto efficient for the reported lists, but neither stable nor strategyproof.
- **Efficiency-adjusted deferred acceptance** (Kesten 2010). Students may consent to waive a priority that does not help them. The mechanism Pareto improves on deferred acceptance and is Pareto efficient when all students consent, but it is not strategyproof.
- **Stable improvement cycles** (Erdil and Ergin 2008). With weak priorities, deferred acceptance after a random tie-break can be Pareto dominated by another stable assignment. Their algorithm repeats cycles of exchanges that keep stability until it reaches a student-optimal stable assignment for the weak priorities. It is not strategyproof.

## Bounds

- No mechanism is both stable and Pareto efficient for students (second example). Among stable assignments, the student-optimal one is the best for every student at once.
- Deferred acceptance is strategyproof for students. It does not matter here that it is not strategyproof for schools, because schools do not report.
- Top trading cycles and serial-dictatorship-like rules are efficient and strategyproof, but give up fairness.
- With weak priorities, the tie-breaking matters. Abdulkadiroglu, Pathak and Roth (2009) studied the trade-off between strategyproofness and efficiency under indifferences with data from the New York City match; the efficiency gains of stable improvement cycles come at the cost of strategyproofness.
- Every listed mechanism runs in polynomial time: $O(nm)$ for deferred acceptance and for the Boston mechanism with selection, and polynomial time for top trading cycles. The hard questions are about properties, not about time.

## Reductions

- With strict priorities, a school choice instance is a [hospitals-residents](/hospitals-residents-problem/) instance in which school $s$ ranks students by $\succ_s$ and lists only the students who find it acceptable. Stable assignments are the same in both. So the structure of stable matchings carries over: the stable assignments form a [lattice](/lattice-of-stable-matchings/), and by the [rural hospitals theorem](/rural-hospitals-theorem/) every stable assignment fills each school to the same number of seats and assigns the same students.
- With weak priorities, stability is weak stability of [stable matching with ties](/stable-matching-with-ties/). There, finding a weakly stable matching of maximum size is NP-hard, so the size of the assignment depends on the tie-breaking.
- Without priorities, it is the [house allocation problem](/house-allocation-problem/).

## Applications

The model came from US school districts. Abdulkadiroglu and Sonmez (2003) wrote it down to criticize the mechanisms in use. Economists then helped New York City redesign its high school match (first used in the 2003-04 school year) and Boston redesign its assignment (adopted in 2005), both with student-proposing deferred acceptance; the 2005 papers in the American Economic Review describe both redesigns. Other cities, and assignment systems for colleges and for kindergartens in several countries, use variants of deferred acceptance, top trading cycles or Boston-like rules.

## References
