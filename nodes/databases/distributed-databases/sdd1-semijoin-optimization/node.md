---
tag: ER70WT
kind: algorithm
slug: sdd1-semijoin-optimization
name: SDD-1 semijoin optimization
aliases:
- semijoin program
- Bernstein-Goodman semijoin reduction
area: databases/distributed-databases
level: advanced
summary: "Algorithm OPT of SDD-1: add the most profitable semijoin while its estimated benefit is larger than its cost, then send the reduced relations to the site that holds the most data."
solves: [distributed-query-processing]
model: word-ram
complexity:
  vars: {q: the number of candidate semijoins (ordered pairs of relations at different sites with a common attribute), e: "the number of (relation, attribute) pairs in the profile"}
  time: {worst: "O(q^3 e)"}
  space: {extra: "O(q e)"}
properties: {deterministic: true, exact: false, online: false, in_place: false, recursive: false}
history:
  year: 1981
  people: [Philip A. Bernstein, Nathan Goodman, Eugene Wong, Christopher L. Reeve, James B. Rothnie Jr.]
  note: "SDD-1 was a distributed database system built at Computer Corporation of America. Bernstein, Goodman, Wong, Reeve and Rothnie (1981) described its query processor, which reduces the relations by semijoins and then moves them to one site."
prereqs: [semijoin, distributed-query-processing]
see_also: [bloom-join, yannakakis-algorithm, acyclic-hypergraph, cardinality-estimation, selectivity, cost-model, hill-climbing, parallel-hash-join]
sources:
  - paper: doi:10.1145/319628.319650
    title: Philip A. Bernstein, Nathan Goodman, Eugene Wong, Christopher L. Reeve and James B. Rothnie Jr., Query processing in a system for distributed databases (SDD-1), ACM Transactions on Database Systems 6(4), 1981, pages 602 to 625
    locator: Section 3 (the database profile, the selectivity of a set of values, the estimated effect of a semijoin with the piecewise Yao function, and the cost and benefit of a semijoin), Section 4.1 (Algorithm OPT), Section 4.2 (the two enhancements) and Section 4.3 (the worked example with S, Y and P)
  - paper: doi:10.1145/322234.322238
    title: Philip A. Bernstein and Dah-Ming W. Chiu, Using semi-joins to solve relational queries, Journal of the ACM 28(1), 1981, pages 25 to 40
    locator: the full reducer of a tree query
  - paper: doi:10.1137/0210059
    title: Philip A. Bernstein and Nathan Goodman, Power of natural semijoins, SIAM Journal on Computing 10(4), 1981, pages 751 to 771
    locator: the result that cyclic queries have no full reducer
  - book: isbn:9783030262525
    title: M. Tamer Özsu and Patrick Valduriez, Principles of Distributed Database Systems, fourth edition, Springer, 2020
    locator: Chapter 4, Distributed Query Processing, the part on semijoin based algorithms
---

SDD-1 was one of the first distributed database systems, and its query optimizer, Algorithm OPT, decides how to answer a join query over relations stored at different sites. OPT first sends [semijoins](/semijoin/) between the sites to drop rows that cannot take part in the answer, and then moves what is left to one site, which computes the join. It picks the semijoins one at a time by a [hill-climbing](/hill-climbing/) rule: the next semijoin is the one whose estimated benefit exceeds its estimated cost by the most. The answer is always exact, but the plan is only as good as the estimates, and the greedy rule is a heuristic.

## In plain words

Three offices each keep one list: suppliers, shipments and parts. A question needs all three lists together, and sending a long list over the network is slow. So the offices first send short notes to each other. A note is a list of the numbers that one office holds, such as the supplier numbers in Massachusetts. The office that gets the note crosses out each row whose number is not on the note, because such a row cannot be in the answer. A note costs time to send, and it helps only if it crosses out many rows. The optimizer guesses both amounts from statistics, sends the best note first, and goes on while some note still saves more than it costs. At the end, all the short lists go to the office that has the most data, and that office computes the answer.

## The problem

The query is a natural join $Q = R_1 \bowtie \dots \bowtie R_r$ with local selections, as in the [distributed query processing problem](/distributed-query-processing/). Each relation is stored at one site, and attributes with the same name are joined. The bags and the NULLs follow the [relational model](/relational-model/): a NULL matches nothing. The plan must leave the answer at some site. Its cost is the amount of data sent between sites, counted in the units of the attribute widths; local work and the number of messages are free in this model.

A semijoin $R_i \ltimes_A R_j$ sends the distinct non-null values of $R_j[A]$ to the site of $R_i$ and keeps the rows of $R_i$ whose $A$ value is among them. Its cost is $|R_j[A]| \cdot w(A)$, or 0 when the two relations are at the same site.

**The profile.** OPT works before it sees the data, from a database profile. For each attribute domain $X$ the profile holds its size $c(X)$ and width $w(X)$. For each relation it holds the number of rows $c(R)$ and, for the join attributes, the number of distinct values $c(R.A)$. The estimates assume that the values of a column are a random subset of the domain, that the rows are spread evenly over the values, and that different columns are independent.

**Estimates.** A set of values such as $R[A]$ has a *selectivity* $\rho = c(R.A)/c(X)$. A semijoin $R_i \ltimes_A R_j$ gives $R_i[A]$ the new estimate $\rho \cdot c(X)$, where $\rho$ is the product of the selectivities of the independent reductions that $R_i[A]$ and $R_j[A]$ have had; the paper keeps this history as a graph of labeled edges, so that one reduction is not counted twice. The new $c(R_i)$ is $c(R_i) \cdot c(R_i.A)_{new}/c(R_i.A)_{old}$. For every other attribute $B$ of $R_i$, the new $c(R_i.B)$ is Yao's function of the new $c(R_i)$ and the old $c(R_i.B)$, the expected number of distinct values left when that many rows are kept. The paper uses a piecewise approximation: $n$ if $n < b/2$, then $(n + b)/3$ if $n < 2b$, else $b$, for $n$ rows kept and $b$ distinct values before. The *benefit* of the semijoin is the drop in $c(R_i)$ times the width of $R_i$.

## The algorithm

```pseudo id=main
OPT(profile, selections)
L1  for each local selection σ on a relation R do update the estimates of R by σ
L2      append σ to the program P
L3  for each nonlocal semijoin sj = R_i ⋉_A R_j not yet in P do profit(sj) ← benefit(sj) - cost(sj)
L4      if no sj has profit(sj) > 0 then go to L6; else pick sj with the largest profit
L5      append sj to P, update the estimates of R_i by its effect, and go to L3
L6  S_a ← the site with the largest estimated data, the sum of c(R) · width(R) over its relations
L7  for each semijoin of P that reduces a relation at S_a: drop it if P without it costs less
L8  return P, then move every relation to S_a and join there
```

Lines L1 and L2 are the local work of the paper: selections at one site cost nothing and make every later estimate smaller. Lines L3 to L5 are the main loop. Line L6 chooses the assembly site so that the least data has to move, since the relations at that site stay where they are. Line L7 is the second enhancement of the paper: once the site is fixed, a semijoin that only shrinks a relation that will not move is useless, unless it helps a later semijoin. The test in line L7 replays the whole program with the estimates, so an indirect gain is kept.

The paper writes the loop of line L3 as "while some nonlocal semijoin has benefit > cost". The implementation uses each semijoin at most once. Without this rule, in a cyclic query the semijoins can keep lowering one another's estimates through Yao's function, with smaller and smaller gains, and the loop need not end. In the example below, no semijoin is chosen twice anyway.

## Example

This is the example of Section 4.3 of the paper. Suppliers $S(s\#, sname, location)$, shipments $Y(s\#, p\#)$ and parts $P(p\#, pname, type)$ are at three different sites, and every attribute has width 1. The query asks for the suppliers in Massachusetts, the micro parts and their shipments: the local selections are $location = MA$ and $type = micro$. The domains of $s\#$ and $p\#$ have 10,000 values, the domain of $location$ has 50 values and the domain of $type$ has 5. The paper prints 100,000 for the first two domains, but its numbers follow only from 10,000.

| relation | rows | distinct values of the join attributes | after the local selection |
|---|---|---|---|
| S | 10,000 | s#: 10,000 | 200 rows, s#: 200 |
| Y | 100,000 | s#: 1,000, p#: 1,000 | no change |
| P | 10,000 | p#: 10,000 | 2,000 rows, p#: 2,000 |

The four nonlocal semijoins start with these estimates:

| semijoin | cost | benefit |
|---|---|---|
| $S \ltimes_{s\#} Y$ | 1,000 | $180 \times 3 = 540$ |
| $P \ltimes_{p\#} Y$ | 1,000 | $1{,}800 \times 3 = 5{,}400$ |
| $Y \ltimes_{s\#} S$ | 200 | $98{,}000 \times 2 = 196{,}000$ |
| $Y \ltimes_{p\#} P$ | 2,000 | $80{,}000 \times 2 = 160{,}000$ |

OPT picks four semijoins in this order.

1. $Y \ltimes_{s\#} S$, cost 200. The selectivity of $Y.s\#$ becomes $0.1 \times 0.02$, so $Y.s\#$ has 20 values and $Y$ has $20 \times 100{,}000/1{,}000 = 2{,}000$ rows. Yao's function of 2,000 rows and 1,000 values gives 1,000, so $Y.p\#$ keeps 1,000 values.
2. $P \ltimes_{p\#} Y$, cost 1,000, benefit 5,400. $P$ drops to 200 rows.
3. $Y \ltimes_{p\#} P$, cost 200, benefit 3,200. $Y$ drops to 400 rows.
4. $S \ltimes_{s\#} Y$, cost 20, benefit 540. $S$ drops to 20 rows.

Now no semijoin is profitable. The semijoins cost $200 + 1{,}000 + 200 + 20 = 1{,}420$. The estimated data is 60 at the site of $S$, 800 at the site of $Y$ and 600 at the site of $P$, so line L6 picks the site of $Y$, and the move costs $60 + 600 = 660$, for a total of 2,080. Line L7 then drops the third semijoin: it shrinks $Y$, which does not move, and no later semijoin needs it. The final program costs 1,880, as in the paper. The tests of the implementation check every number in this section.

## Correctness

Every semijoin program gives the exact answer, with the right count for every row. A row that takes part in the answer agrees on the semijoin attributes with a row of the other relation that also takes part, so a semijoin never drops it; the dropped rows have no partner and add nothing to the join. This holds for any data, whatever the estimates say. The cost of a plan, on the other hand, depends on the estimates, and nothing guarantees that OPT finds the cheapest plan. The proofs are on [the proof page](proofs/correctness.md).

## Complexity

- **Steps (theorem).** The main loop picks at most $q$ semijoins, where $q$ is the number of candidates, and each pass of line L3 evaluates at most $q$ of them. Line L7 replays the program at most $2q$ times.
- **Time.** One estimate takes time linear in the size of its reduction history, which has $O(q e)$ edges. So this implementation does $O(q^3 e)$ arithmetic operations in the worst case, counted on the word RAM with an exact rational as one word. The paper states no bound, and a careful implementation can cache the selectivities.
- **Plan cost (measurement only).** The data sent by the plan is an estimate. How close it is to the real cost depends on how far the data is from the uniform and independent model.

## Properties

- **Exact answer, heuristic plan.** The answer is exact for any program (a theorem); the choice of the program is a heuristic.
- **Greedy.** OPT seeks the largest immediate gain, does not look ahead and does not go back, and the paper says that its plans are "in general, suboptimal". The example shows this even for the estimated cost: the plan of the main loop costs 2,080, and a plan with one semijoin less costs 1,880.
- **Transmission only.** The cost counts data sent. In the networks of the time this was the dominant cost; on a fast local network, the local work and the number of messages can matter more.
- **Reduce, then join.** The plan has two phases: semijoins between sites, then all joins at one site.

## Variants and improvements

- **Moving expensive semijoins later.** The first enhancement of the paper permutes the semijoins of the program, in decreasing order of cost, so that an expensive semijoin runs after the cheaper ones that shrink the data it sends.
- **Full reducers.** For a tree query, the program of Bernstein and Chiu (1981) does a semijoin up each edge of a join tree and then down each edge, $2(r - 1)$ semijoins in all, and leaves in every relation exactly the rows that take part in the answer. Bernstein and Goodman (1981) showed that cyclic queries have no full reducer in general. The [Yannakakis algorithm](/yannakakis-algorithm/) uses the same passes for [acyclic join evaluation](/acyclic-join-evaluation/) on one site.
- **Bloom joins.** A [Bloom join](/bloom-join/) sends a [Bloom filter](/bloom-filter/) of the join values instead of the values. It costs a fixed number of bits and lets a few rows through by error.
- **Joins between sites.** The paper suggests plans that alternate semijoins with joins at several sites, since a join can make new semijoins profitable. Later optimizers, such as the methods in the textbook of Özsu and Valduriez, search over [join orders](/join-ordering/) and sites with a [cost model](/cost-model/) instead.

## When to use it

Use semijoin reduction when the network is slow compared with local work, the join is selective, and the join columns are narrow compared with the rows. It helps most when a relation is large and only a few of its rows join, as with the shipments in the example. When most rows join, a semijoin costs data and drops almost nothing; then move the relations directly, or use a [parallel hash join](/parallel-hash-join/) on a fast cluster.

## Pitfalls

- **Trusting the estimates.** The benefit comes from a uniform and independent model. Correlated columns or skewed values can make a semijoin that looks profitable drop nothing.
- **Counting one reduction twice.** Two sets of values that come from the same earlier reduction are not independent. Multiplying their selectivities as if they were gives too small an estimate. The reduction history of the paper exists to avoid this.
- **Single attributes on a tree query.** A full reducer must use all the common attributes of the two relations at once. Two semijoins on one attribute each can keep a row that a semijoin on both attributes drops.
- **Cyclic queries.** No semijoin program can remove the dangling rows of some cyclic queries: in the triangle $R(A, B)$, $S(B, C)$, $T(C, A)$ with $R = S = \{(0, 0), (1, 1)\}$ and $T = \{(0, 1), (1, 0)\}$, no semijoin drops a row, but the join is empty.
- **NULLs.** A NULL join value must not be sent as a value, since it matches nothing. Rows with a NULL join value are dropped by any semijoin on that attribute.

## Implementations

## History

SDD-1, a System for Distributed Databases, was developed at Computer Corporation of America, and an overview of the system appeared in ACM Transactions on Database Systems in 1980. Bernstein, Goodman, Wong, Reeve and Rothnie described its query processor in 1981. They made the semijoin the main tool of distributed query processing, and they gave the profile model of estimates that later work used. In the same year Bernstein and Chiu studied which queries semijoins can solve and gave the full reducer of a tree query, and Bernstein and Goodman showed the limits of semijoins on cyclic queries. Yannakakis (1981) used the same passes to evaluate acyclic joins in time linear in the input and the output.

## References
