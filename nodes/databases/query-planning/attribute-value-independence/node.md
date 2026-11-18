---
tag: TE37FY
kind: concept
slug: attribute-value-independence
name: Attribute value independence assumption
aliases:
- AVI assumption
- independence assumption of selectivity estimation
area: databases/query-planning
level: core
summary: "The assumption that predicates on different columns are independent, so the selectivity of a conjunction is the product of their selectivities. With correlated columns it underestimates."
prereqs: [selectivity, histogram]
see_also: [cardinality-estimation, estimation-error-propagation, conditional-independence, bayesian-network, learned-cardinality-estimation, pessimistic-cardinality-estimation, selinger-join-enumeration, guaranteed-error-estimator]
sources:
  - paper: doi:10.1145/582095.582099
    title: P. Griffiths Selinger, M. M. Astrahan, D. D. Chamberlin, R. A. Lorie and T. G. Price, Access path selection in a relational database management system, Proceedings of ACM SIGMOD 1979, 23 to 34
    locator: "Section 4, Table 1, p. 26 (selectivity factors: the product for AND, which the paper says assumes independent column values, and the default factors 1/10, 1/3 and 1/4)"
  - paper: "Stavros Christodoulakis, Implications of certain assumptions in database performance evaluation, ACM Transactions on Database Systems 9(2) (1984), 163 to 186"
    title: Implications of certain assumptions in database performance evaluation
    locator: the effect of the uniformity and independence assumptions on the estimates of cost models
  - paper: "Viswanath Poosala and Yannis E. Ioannidis, Selectivity estimation without the attribute value independence assumption, Proceedings of VLDB 1997, 486 to 495"
    title: Selectivity estimation without the attribute value independence assumption
    locator: multidimensional histograms and the singular value decomposition as ways to estimate the selectivity of predicates on several columns
  - paper: doi:10.14778/2850583.2850594
    title: Viktor Leis, Andrey Gubichev, Atanas Mirchev, Peter Boncz, Alfons Kemper and Thomas Neumann, How good are query optimizers, really?, Proceedings of the VLDB Endowment 9(3) (2015), 204 to 215
    locator: Section 3 (measured cardinality estimates of several systems on the Join Order Benchmark, by number of joins)
---

The attribute value independence assumption (AVI) says that the values of different columns of a table are independent. A query optimizer uses it to estimate the [selectivity](/selectivity/) of a conjunction of predicates on several columns: it estimates each predicate on its own, from a one-column [histogram](/histogram/) or a default, and multiplies the results. System R introduced this rule in 1979, and most systems still use it as the default. It needs only statistics on single columns, but it is wrong when columns are correlated, and then it usually underestimates. This page states the assumption, shows how far off it can be, and lists the fixes. The general problem is on the [cardinality estimation](/cardinality-estimation/) page, and the growth of errors through joins is on the [estimation error propagation](/estimation-error-propagation/) page.

## In plain words

A car table has a column for the maker and a column for the model. A query asks for cars made by Honda with the model Accord. The database knows that one car in ten is a Honda and one car in twenty is an Accord. If it treats the two columns as unrelated, it guesses that one car in two hundred matches both.

But every Accord is a Honda, so the true answer is one car in twenty, ten times more than the guess. The database plans for a small result and gets a large one. The plan it picks can be slow.

The guess is cheap, because it needs facts about each column alone. It is right only when knowing one column tells you nothing about the other.

## The idea

Let a table $R$ have $N$ rows, and let a row be picked uniformly at random. The selectivity of a predicate $p$ is $s(p) = |\sigma_p(R)| / N$, the probability that the random row satisfies $p$. For predicates $p_1, \ldots, p_k$ on different columns, the assumption is that the events "the row satisfies $p_i$" are mutually independent. Then

$$s(p_1 \wedge \cdots \wedge p_k) = \prod_{i=1}^k s(p_i), \qquad s(p_1 \vee p_2) = s(p_1) + s(p_2) - s(p_1) s(p_2), \qquad s(\neg p) = 1 - s(p).$$

Table 1 of Selinger et al. gives exactly these three rules and notes that the rule for AND assumes that the column values are independent. Two other assumptions often come with it, and they are separate. The uniformity assumption says that the values inside a column, or inside one bucket of a histogram, are equally frequent. The containment assumption for joins says that the join column with fewer distinct values has its values contained in the other column. Together, they give the classic estimate $|R \bowtie_{R.a = S.b} S| \approx |R|\,|S| / \max(V(R, a), V(S, b))$, where $V$ is the number of distinct values. The three are assumptions about the data, not facts. The estimate is exact only when the data happens to satisfy them.

**How far off it can be.** For two predicates with selectivities $s_1$ and $s_2$, the true selectivity $s_{12}$ of the conjunction can be any value with

$$\max(0,\ s_1 + s_2 - 1) \le s_{12} \le \min(s_1, s_2).$$

The upper bound holds because the rows that satisfy both satisfy each. The lower bound holds because at most $N - |\sigma_{p_1}(R)|$ rows fail $p_1$, so at least $s_1 + s_2 - 1$ of the rows satisfy both. Both ends can be reached: nested sets of rows reach the upper end, and sets that overlap as little as possible reach the lower end. The product $s_1 s_2$ always lies in this range, because $s_1 s_2 \le \min(s_1, s_2)$ and $s_1 s_2 - (s_1 + s_2 - 1) = (1 - s_1)(1 - s_2) \ge 0$. So the AVI estimate is never impossible, but it can be off by a large factor in both directions:

- **Underestimate.** The ratio of the truth to the estimate is at most $\min(s_1, s_2)/(s_1 s_2) = 1/\max(s_1, s_2)$. With $k$ predicates, the same argument gives a ratio of at most $\min_i s_i / \prod_i s_i$, the product of all the selectivities but the smallest one, inverted. This bound is reached when the sets of rows are nested, for example when one predicate implies the others.
- **Overestimate.** When the sets of rows are disjoint, the truth is 0 and the estimate is $N s_1 s_2$ rows. No finite ratio bounds this case.

Predicates with small selectivities, which are the common case in a WHERE clause, allow the largest underestimates. And in a query with several tables, the estimate of each intermediate result is used to estimate the next one, so the factors multiply.

## Examples

**Implied columns.** A table of 1000 cars has 100 Hondas ($s_1 = 0.1$) and 50 Accords ($s_2 = 0.05$), and every Accord is a Honda. AVI estimates $1000 \cdot 0.1 \cdot 0.05 = 5$ rows for make = 'Honda' AND model = 'Accord'. The true result has 50 rows, 10 times more. This is the largest possible underestimate for these two selectivities, $1/\max(0.1, 0.05) = 10$, because the Accords are a subset of the Hondas.

**Disjoint columns.** In the same table, 200 cars are Toyotas. For make = 'Toyota' AND model = 'Accord', AVI estimates $1000 \cdot 0.2 \cdot 0.05 = 10$ rows. The true result is empty.

**A chain of implications.** A table of $10^6$ customers has 1 percent in the city of Munich, 10 percent in Germany and 30 percent who pay in euros. Every customer in Munich lives in Germany, and every customer in Germany pays in euros. For the conjunction of the three predicates, AVI estimates $10^6 \cdot 0.01 \cdot 0.1 \cdot 0.3 = 300$ rows. The true result is the 10,000 customers in Munich, about 33 times more. The bound above is $0.01/(0.01 \cdot 0.1 \cdot 0.3) = 1/0.03 \approx 33.3$, so this is again the worst case. Each extra implied predicate with selectivity $s$ divides the estimate by $1/s$ more.

**Independent columns.** If the color of a car does not depend on its maker, and 20 percent of the cars are red, then AVI estimates 20 red Hondas among the 100 Hondas, and the true number is close to 20. On real data, columns such as color and maker are rarely exactly independent, so even here the estimate has some error.

## Where it is used

- **Cost-based optimizers.** System R used the product rule and default selectivities (1/10 for an equality without an index, 1/3 for a range, 1/4 for BETWEEN) in 1979, and most optimizers based on [Selinger's method](/selinger-join-enumeration/) still use the product rule when they have no statistics on several columns.
- **Measured effect.** Leis et al. (2015) measured the estimates of several systems on the Join Order Benchmark, built on the IMDB data set, which has many correlated columns. The estimates were mostly too small, and the errors grew with the number of joins, by several orders of magnitude for the larger queries. This is a measurement, not a theorem. The [estimation error propagation](/estimation-error-propagation/) page gives the theorem of Ioannidis and Christodoulakis (1991) for a model of this growth.
- **Statistics on column groups.** Many systems let the administrator create statistics on a group of columns, for example the CREATE STATISTICS command of PostgreSQL with functional dependencies and multi-column distinct counts. The optimizer then uses the joint statistics in place of the product.
- **Multidimensional histograms.** Poosala and Ioannidis (1997) estimated the joint distribution of several columns with multidimensional histograms and with the singular value decomposition, without the assumption.
- **Models of the joint distribution.** Estimators based on a [Bayesian network](/bayesian-network/) keep only some dependencies and assume [conditional independence](/conditional-independence/) for the rest, which is weaker than AVI. [Learned cardinality estimation](/learned-cardinality-estimation/) fits a model of the joint distribution or of the queries.
- **Bounds instead of estimates.** [Pessimistic cardinality estimation](/pessimistic-cardinality-estimation/) gives an upper bound on the result size that holds for all data with the given statistics, so it cannot underestimate.

## References
