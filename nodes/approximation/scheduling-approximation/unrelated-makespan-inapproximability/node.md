---
tag: 4SQE09
kind: theorem
slug: unrelated-makespan-inapproximability
name: Inapproximability of unrelated-machine makespan
aliases:
- 3/2 hardness for R||Cmax
- Lenstra-Shmoys-Tardos hardness
- 3/2 hardness for restricted assignment
area: approximation/scheduling-approximation
level: research
summary: R||Cmax has no (3/2 - epsilon)-approximation unless P = NP.
prereqs: [unrelated-machine-scheduling, three-dimensional-matching, np-complete, approximation-ratio, gap-problem]
see_also: [lenstra-shmoys-tardos, restricted-assignment-scheduling, scheduling-makespan-inapproximability, unrelated-machine-scheduling-makespan, gap-preserving-reduction, polynomial-time-reduction]
sources:
  - paper: doi:10.1007/BF01585745
    title: "J. K. Lenstra, D. B. Shmoys and É. Tardos, Approximation algorithms for scheduling unrelated parallel machines, Mathematical Programming 46, 1990"
    locator: the reduction from three-dimensional matching that shows that makespan 2 is NP-hard to decide
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: "R. M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972"
    locator: the NP-completeness of three-dimensional matching
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness
    locator: Section 3.1 and problem SP1 (3-dimensional matching)
  - paper: "P. Schuurman and G. J. Woeginger, Polynomial time approximation algorithms for machine scheduling: ten open problems, Journal of Scheduling 2(5), 1999"
    locator: the open question of closing the gap between 3/2 and 2 for unrelated machines
---

The 3/2 hardness theorem for unrelated machines says that no polynomial algorithm for $R \mid\mid C_{\max}$ has ratio below $3/2$ unless P = NP. Lenstra, Shmoys and Tardos (1990) proved it by a reduction from [three-dimensional matching](/three-dimensional-matching/): the instances have optimal makespan 2 when a perfect matching exists and at least 3 otherwise. The instances use only the times 1, 2 and $\infty$, and the time of a job does not depend on the machine where it may run, so the bound holds already for [restricted assignment](/restricted-assignment-scheduling/). The same paper gives the [2-approximation](/lenstra-shmoys-tardos/), and the gap between $3/2$ and 2 is still open.

## Statement

An instance of $R \mid\mid C_{\max}$ has $n$ jobs, $m$ machines and times $p_{ij} \in \{0, 1, 2, \ldots\} \cup \{\infty\}$, where $\infty$ means that job $j$ cannot run on machine $i$. $\mathrm{OPT}$ is the least makespan over all assignments of jobs to machines. A $\rho$-approximation returns an assignment of makespan at most $\rho \cdot \mathrm{OPT}$ on every instance, with $\rho \ge 1$.

**Theorem (Lenstra, Shmoys and Tardos 1990).**

1. It is NP-complete to decide whether $\mathrm{OPT} \le 2$, even when every finite $p_{ij}$ is 1 or 2 and each job has the same time on all machines where it can run.
2. Hence, for every $\rho < 3/2$, there is no polynomial $\rho$-approximation for $R \mid\mid C_{\max}$ unless P = NP. The same holds for the restricted assignment problem $P \mid M_j \mid C_{\max}$.

The bound is a hardness threshold for the problem, with the number of machines part of the input. It is absolute: no additive constant appears. It is not known to be tight, since the best ratio known is $2 - 1/m$.

## In plain words

Some tasks must go to workers, and each task can be done only by certain workers. The question "can everyone be done within two hours?" turns out to be as hard as a classic hard puzzle: picking a set of triples out of a list so that each item is used exactly once.

The trick is to build tasks from the puzzle so that a good choice of triples gives a plan of two hours, and a bad puzzle forces some worker to work three hours. Then a method that always gets within less than one and a half times the best plan would always tell two hours from three, and so it would solve the puzzle. So such a method is not expected to exist.

## Proof

**The source problem.** An instance of three-dimensional matching is three disjoint sets $A$, $B$, $C$, each with $q$ elements, and a list $F$ of $t$ triples $(a, b, c) \in A \times B \times C$. A *perfect matching* is a set of $q$ triples of $F$ that together contain every element of $A \cup B \cup C$ exactly once. Deciding whether one exists is NP-complete (Karp 1972). We may assume that each element of $A$ lies in at least one triple, since otherwise the answer is no and we output a fixed instance with $\mathrm{OPT} = 3$. Let $t_a \ge 1$ be the number of triples that contain $a \in A$.

**The construction.** Make one machine for each triple of $F$ and these jobs:

- an *element job* for each $b \in B$ and each $c \in C$, with time 1 on each machine whose triple contains that element and $\infty$ on the others;
- for each $a \in A$, $t_a - 1$ *dummy jobs* of type $a$, with time 2 on each machine whose triple contains $a$ and $\infty$ on the others.

There are $t$ machines and $2q + \sum_a (t_a - 1) = 2q + t - q = q + t$ jobs. The construction takes polynomial time, and each job has one finite time, so the instance is also an instance of restricted assignment.

**A perfect matching gives makespan 2.** Let $M$ be a perfect matching. For each $a \in A$ exactly one triple of $M$ contains $a$, so exactly $t_a - 1$ triples outside $M$ contain $a$; put one dummy job of type $a$ on each of them. Each triple outside $M$ contains exactly one element of $A$, so it gets exactly one dummy job and load 2. Put the element jobs of $b$ and $c$ on the machine of the triple $(a, b, c) \in M$; since $M$ covers each element of $B$ and $C$ once, each element job gets one machine, and each machine of $M$ gets two jobs of time 1. All loads are at most 2, so $\mathrm{OPT} \le 2$.

**Makespan 2 gives a perfect matching.** Take a schedule of makespan at most 2. A dummy job has time 2, so a machine with a dummy job has no other job. The $t_a - 1$ dummy jobs of type $a$ are on distinct machines whose triples contain $a$, so for each $a$ exactly one triple that contains $a$ has no dummy job. Call these $q$ triples *free*, one for each $a \in A$. The machines with dummy jobs are full, so all $2q$ element jobs run on the $q$ free machines, at most two on each because each has time 1. So each free machine has exactly two element jobs. The machine of a triple $(a, b, c)$ can run only the element jobs of $b$ and of $c$, so it runs exactly these two. Then each $b \in B$ and each $c \in C$ lies in exactly one free triple, because its element job runs once, and each $a \in A$ lies in exactly one free triple by the choice of the free triples. So the free triples form a perfect matching.

So the instance has $\mathrm{OPT} \le 2$ if and only if a perfect matching exists. The decision problem is in NP, since a schedule is a certificate, which proves part 1.

**From the gap to the ratio.** All times are integers, so if no perfect matching exists, $\mathrm{OPT} \ge 3$. Suppose a polynomial algorithm has ratio $\rho < 3/2$. On an instance with $\mathrm{OPT} \le 2$ it returns makespan at most $2\rho < 3$, and so at most 2. On an instance with $\mathrm{OPT} \ge 3$ it returns at least 3. Comparing its answer with 2 decides three-dimensional matching in polynomial time, so P = NP. This proves part 2. $\blacksquare$

**An example.** Take $A = \{a_1, a_2\}$, $B = \{b_1, b_2\}$, $C = \{c_1, c_2\}$ and the triples $T_1 = (a_1, b_1, c_1)$, $T_2 = (a_1, b_2, c_1)$ and $T_3 = (a_2, b_2, c_2)$. There is one dummy job, of type $a_1$, with time 2 on $T_1$ and $T_2$. The perfect matching $\{T_1, T_3\}$ gives the schedule: dummy on $T_2$, the jobs $b_1, c_1$ on $T_1$, and $b_2, c_2$ on $T_3$, with makespan 2. Now take instead $T_2 = (a_1, b_2, c_2)$ and $T_3 = (a_2, b_2, c_1)$, which has no perfect matching. The dummy job must go on $T_1$ or $T_2$. On $T_1$ it shares the machine with $b_1$, which can run only there; on $T_2$ it shares the machine with $c_2$, which can run only there. So the makespan is 3.

## Consequences

- **The 2-approximation is close.** The [Lenstra-Shmoys-Tardos rounding](/lenstra-shmoys-tardos/) gives 2, and later work gives $2 - 1/m$. No polynomial algorithm can beat $3/2$ unless P = NP, so $R \mid\mid C_{\max}$ is APX-hard and has no PTAS.
- **Restricted assignment and two sizes.** The hardness holds for [restricted assignment](/restricted-assignment-scheduling/) with only two job sizes, 1 and 2. Ebenlendr, Krčál and Sgall (2008) showed that the $3/2$ bound holds even for graph balancing, where each job can run on at most two machines.
- **A contrast with simpler machines.** Identical machines and uniform machines have a PTAS, so for them no constant above 1 is a threshold; see [the Hochbaum-Shmoys PTAS](/hochbaum-shmoys-ptas/) and [uniform machine scheduling](/uniform-machine-scheduling/). For a fixed number of unrelated machines there is an FPTAS, so the hardness needs $m$ in the input.
- **Value and schedule.** The proof shows hardness of telling makespan 2 from 3. For restricted assignment, Svensson (2012) showed that the optimum can be *estimated* within a factor $33/17 < 2$ by the configuration LP. His proof uses a local search that is not known to run in polynomial time, so it bounds the optimum value but does not give a schedule of this quality in polynomial time.

## Tightness

The reduction separates makespan 2 from makespan 3, and this is the smallest gap of this kind: deciding whether $\mathrm{OPT} \le 1$ with times in $\{1, \infty\}$ is a [bipartite matching](/bipartite-matching/) question, which is polynomial. With times in $\{0, 1, \ldots\}$, a gap from $k$ to $k + 1$ gives only $1 + 1/k$, so the gap from 2 to 3 is the best that such a direct argument can give. No better hardness than $3/2$ is known for $R \mid\mid C_{\max}$, and no algorithm better than $2 - 1/m$ is known. Closing this gap is one of the ten open problems in the survey of Schuurman and Woeginger (1999).

## History

Lenstra, Shmoys and Tardos presented the result at FOCS 1987, in the same paper as the 2-approximation, and published it in Mathematical Programming in 1990. The source problem, three-dimensional matching, is one of Karp's 21 NP-complete problems of 1972. The same reduction idea, dummy jobs that fill all but one machine of each group, appears in many later hardness proofs for assignment problems.

## References
