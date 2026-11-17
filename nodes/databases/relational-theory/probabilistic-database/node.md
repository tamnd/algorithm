---
tag: 1X7PAG
kind: model
slug: probabilistic-database
name: Probabilistic database
aliases:
- tuple-independent probabilistic database
area: databases/relational-theory
level: advanced
summary: "A database whose tuples are present with given probabilities; a query returns each answer with the probability that it holds."
prereqs: [relational-algebra, model-counting]
see_also: [dalvi-suciu-dichotomy, provenance-semirings, why-and-where-provenance, d-dnnf, karp-luby-algorithm, ordered-binary-decision-diagram, certain-answers, data-and-combined-complexity]
sources:
  - book: isbn:9781608456802
    title: Dan Suciu, Dan Olteanu, Christopher Re and Christoph Koch, Probabilistic Databases, Synthesis Lectures on Data Management, Morgan and Claypool (2011)
    locator: Chapter 2 (possible worlds, tuple-independent and block-independent-disjoint databases), Chapter 3 (the query evaluation problem and lineage), Chapter 4 (extensional evaluation and the lifted rules), Chapter 5 (intensional evaluation and compilation)
  - paper: "Nilesh Dalvi and Dan Suciu, Efficient query evaluation on probabilistic databases, Proceedings of the 30th International Conference on Very Large Data Bases (VLDB), 864 to 875 (2004)"
    locator: the possible worlds semantics for independent tuples, safe plans, and the #P-hardness of a conjunctive query
  - paper: doi:10.1007/s00778-006-0004-3
    title: Nilesh Dalvi and Dan Suciu, Efficient query evaluation on probabilistic databases, The VLDB Journal 16(4), 523 to 544 (2007)
    locator: journal version, with the dichotomy for conjunctive queries without self-joins
  - paper: doi:10.1016/0196-6774(89)90038-2
    title: Richard M. Karp, Michael Luby and Neal Madras, Monte-Carlo approximation algorithms for enumeration problems, Journal of Algorithms 10(3), 429 to 448 (1989)
    locator: the union of sets estimator, which approximates the probability of a DNF formula
---

A probabilistic database is a database in which each tuple is present only with some probability, so that the database stands for a probability distribution over ordinary instances, its *possible worlds*. A query returns each answer together with its *marginal probability*, the total probability of the worlds in which the answer holds. The common models are tuple-independent databases, where the tuples are independent events, and block-independent-disjoint databases, where the tuples of a block exclude each other. Computing the probability of a query answer is a weighted counting problem, #P-hard in general, and for some queries it can be done in polynomial time by rules that use independence.

## The machine

The setting is the relational model under set semantics, with a fixed schema; the notation is that of [relational algebra](/relational-algebra/).

**Possible worlds.** A *probabilistic database* is a pair $(\mathcal{W}, P)$ of a finite set $\mathcal{W}$ of instances, the possible worlds, and a probability distribution $P$ on $\mathcal{W}$, so $P(W) \geq 0$ and $\sum_{W \in \mathcal{W}} P(W) = 1$. Listing the worlds is not practical, so the models below describe $P$ by a table.

**Tuple-independent databases (TID).** Each relation is a set of tuples, and each tuple $t$ carries a probability $p(t)$ with $0 < p(t) \leq 1$. Let $T$ be the set of all these tuples. The possible worlds are all subsets $W \subseteq T$, with

$$P(W) = \prod_{t \in W} p(t) \cdot \prod_{t \in T \setminus W} \big(1 - p(t)\big).$$

So each tuple is present with probability $p(t)$, independently of the others. A database with $n$ tuples has $2^{n}$ worlds, all described by $n$ numbers. A tuple with $p(t) = 1$ is certain, and a relation all of whose tuples are certain is *deterministic*.

**Block-independent-disjoint databases (BID).** The tuples of a relation are split into blocks, usually the tuples with the same key. In a world, at most one tuple of each block is present: tuple $t$ of block $b$ with probability $p(t)$, and no tuple of $b$ with probability $1 - \sum_{t \in b} p(t)$, so the probabilities in a block sum to at most 1. Different blocks are independent. A TID is the BID in which every block has one tuple. BIDs express attributes with an uncertain value, such as a city that is Paris with probability $0.6$ or Rome with probability $0.3$.

**Queries.** A query $Q$ of the relational calculus or algebra is evaluated in each world. For a Boolean query,

$$P(Q) = \sum \{\, P(W) \mid W \in \mathcal{W},\ W \models Q \,\}.$$

For a query with free variables, each candidate answer $a$ gets the probability $P(Q[a])$ of the Boolean query $Q[a]$ obtained by substituting $a$. The output is the set of pairs $(a, P(Q[a]))$ with $P(Q[a]) > 0$. The query itself is an ordinary query; only the evaluation changes.

**Lineage.** For a union of conjunctive queries $Q$ on a TID, introduce a Boolean variable $X_t$ for each tuple $t$, meaning "$t$ is present". The *lineage* $\Phi_Q$ is the DNF formula with one conjunction $X_{t_1} \land \cdots \land X_{t_k}$ for each set $\{t_1, \ldots, t_k\}$ of tuples that together make $Q$ true, that is, the disjunction over the witnesses of $Q$ (see [why-provenance](/why-and-where-provenance/)). A world satisfies $Q$ exactly when its tuples satisfy $\Phi_Q$, so $P(Q) = P(\Phi_Q)$ when each $X_t$ is true independently with probability $p(t)$. The lineage is the provenance of $Q$ in the semiring of positive Boolean formulas (see [provenance semirings](/provenance-semirings/)), and for a fixed $Q$ it has polynomial size in the database.

## What it counts

The model assigns to each answer a probability, the weight of the set of worlds in which it holds. For a TID and a union of conjunctive queries this is the probability of a monotone DNF formula under independent variables, which is a *weighted model count*: the sum, over the satisfying assignments of $\Phi_Q$, of the product of $p(t)$ for true variables and $1 - p(t)$ for false ones (see [model counting](/model-counting/)). With all $p(t) = 1/2$, $P(Q) \cdot 2^{n}$ is the number of satisfying assignments.

**Example.** A TID with $R(x)$ and $S(x, y)$:

| tuple | $p$ |
|---|---|
| $r_1 = R(a)$ | 0.5 |
| $r_2 = R(b)$ | 0.4 |
| $s_1 = S(a, c)$ | 0.6 |
| $s_2 = S(a, d)$ | 0.5 |
| $s_3 = S(b, c)$ | 0.2 |

The Boolean query $Q = \exists x\, \exists y\, (R(x) \land S(x, y))$ has the lineage $\Phi_Q = r_1 s_1 \lor r_1 s_2 \lor r_2 s_3$. The two values of $x$ use disjoint tuples, so they are independent:

- for $x = a$: $P(R(a) \land \exists y\, S(a, y)) = 0.5 \cdot \big(1 - (1 - 0.6)(1 - 0.5)\big) = 0.5 \cdot 0.8 = 0.4$;
- for $x = b$: $0.4 \cdot 0.2 = 0.08$;
- so $P(Q) = 1 - (1 - 0.4)(1 - 0.08) = 1 - 0.6 \cdot 0.92 = 0.448$.

Summing $P(W)$ over the $2^{5} = 32$ worlds that satisfy $\Phi_Q$ gives the same 0.448.

**A wrong plan.** Compute the join first, $R(a) S(a, c)$ with probability $0.5 \cdot 0.6 = 0.3$, $R(a) S(a, d)$ with $0.25$ and $R(b) S(b, c)$ with $0.08$, and then treat the three join tuples as independent in the projection: $1 - 0.7 \cdot 0.75 \cdot 0.92 = 0.517$. This is wrong, because the first two join tuples share $r_1$ and are not independent. The plan that projects $y$ away inside $S$ before the join, as above, gives the right answer. Plans whose every step respects independence are the *safe plans* of Dalvi and Suciu (2004).

## Relation to other models

- **Incomplete databases.** An incomplete database is a set of possible worlds without probabilities; its [certain answers](/certain-answers/) are the answers true in every world. A probabilistic database adds a distribution, and an answer has probability 1 exactly when it is true in every world with positive probability.
- **Provenance semirings.** Query evaluation by lineage is evaluation in the semiring of positive Boolean formulas, followed by a probability computation that is not a semiring homomorphism: $P(\varphi \land \psi) = P(\varphi) P(\psi)$ only when $\varphi$ and $\psi$ share no variable. See [provenance semirings](/provenance-semirings/).
- **Knowledge compilation.** Intensional evaluation compiles $\Phi_Q$ into a form with linear-time probability computation, such as a [d-DNNF](/d-dnnf/) or an [ordered binary decision diagram](/ordered-binary-decision-diagram/), by [Shannon expansion](/shannon-expansion/) and decomposition into independent parts. The cost is the size of the compiled form.
- **Graphical models.** A TID is the simplest probabilistic model, with all variables independent. Correlations are added by richer representations, for example by conditions on tuples or by factors over tuples as in a [factor graph](/factor-graph/); query evaluation then becomes inference in that model.

## Known results in the model

All results are in data complexity: the query is fixed and the input is the database with its probabilities (see [data and combined complexity](/data-and-combined-complexity/)).

- **Hardness in general.** Computing $P(Q)$ is in $\mathrm{FP}^{\#\mathrm{P}}$ for every fixed query of the relational calculus, by summing over the worlds with a #P oracle. It is #P-hard for some fixed conjunctive queries, already for $H_0 = \exists x\, \exists y\, (R(x) \land S(x, y) \land T(y))$ on a TID (Dalvi and Suciu 2004).
- **Dichotomy.** For unions of conjunctive queries on TIDs, each query is either computable in polynomial time by the lifted inference rules (independent join, independent union, independent project, inclusion-exclusion) or #P-hard. For conjunctive queries without self-joins, the polynomial ones are exactly the hierarchical ones. This is the [Dalvi-Suciu dichotomy](/dalvi-suciu-dichotomy/).
- **Extensional evaluation.** The lifted rules compute $P(Q)$ from the probabilities of smaller queries, without building the lineage. For a fixed query that the rules accept, the time is polynomial in the database (Suciu, Olteanu, Re and Koch 2011, Chapter 4).
- **Intensional evaluation.** Every query can be evaluated by computing $\Phi_Q$ and then its probability, by compilation or by exact model counting. The time is exponential in the worst case.
- **Approximation.** For a union of conjunctive queries, $\Phi_Q$ is a DNF of polynomial size, and the probability of a DNF under independent variables has a fully polynomial randomized approximation scheme, by the estimator of Karp, Luby and Madras (1989) (see [Karp-Luby algorithm](/karp-luby-algorithm/) and [FPRAS](/fpras/)). So $P(Q)$ can be approximated within a factor $1 \pm \varepsilon$ with high probability in time polynomial in the database and $1/\varepsilon$, also for the #P-hard queries.
- **BID databases.** The rules extend to BIDs, with one more rule that adds the probabilities of the disjoint tuples of a block (Suciu, Olteanu, Re and Koch 2011, Chapter 4). A TID is a BID, so every query that is #P-hard on TIDs stays #P-hard on BIDs.

## References
