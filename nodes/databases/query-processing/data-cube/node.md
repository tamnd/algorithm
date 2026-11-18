---
tag: 8ETAEP
kind: definition
slug: data-cube
name: Data cube
aliases:
- CUBE operator
- OLAP cube
area: databases/query-processing
level: core
summary: The aggregates of a fact table over all subsets of a set of grouping attributes, as defined by the CUBE operator of Gray et al.
prereqs: [group-by-aggregation, relational-algebra]
see_also: [bottom-up-cube, hash-aggregation, sort-based-aggregation, materialized-view, view-selection, hru-greedy-view-selection, sql-null-semantics]
sources:
  - paper: doi:10.1023/A:1009726021843
    title: Jim Gray, Surajit Chaudhuri, Adam Bosworth, Andrew Layman, Don Reichart, Murali Venkatrao, Frank Pellow and Hamid Pirahesh, Data cube, a relational aggregation operator generalizing group-by, cross-tab, and sub-totals, Data Mining and Knowledge Discovery 1(1), 29 to 53 (1997)
    locator: the CUBE and ROLLUP operators, the ALL value, and the distributive, algebraic and holistic classes of aggregate functions
  - paper: doi:10.1109/ICDE.1996.492099
    title: Jim Gray, Adam Bosworth, Andrew Layman and Hamid Pirahesh, Data cube, a relational aggregation operator generalizing group-by, cross-tab, and sub-totals, Proceedings of the 12th International Conference on Data Engineering (ICDE), 1996, 152 to 159
    locator: the first version of the CUBE operator
  - paper: doi:10.1145/233269.233333
    title: Venky Harinarayan, Anand Rajaraman and Jeffrey D. Ullman, Implementing data cubes efficiently, Proceedings of ACM SIGMOD 1996, 205 to 216
    locator: the lattice of group-bys of a cube
---

The data cube of a relation $R$ over grouping attributes $A_1, \ldots, A_D$ is the union of the [group-by aggregations](/group-by-aggregation/) of $R$ over all $2^D$ subsets of these attributes. Gray et al. (1996, 1997) defined it as the relational operator CUBE, with a special value ALL in the attributes that a row does not group by. So one table holds the detail rows, all subtotals and the grand total. ROLLUP is the part of the cube that keeps only the prefixes $\{A_1, \ldots, A_k\}$.

## Definition

Let $R$ be a relation, let $A_1, \ldots, A_D$ be attributes of $R$, called the dimensions, and let $f_1, \ldots, f_q$ be aggregates on other attributes, called the measures. For a subset $S \subseteq \{A_1, \ldots, A_D\}$, the group-by on $S$ is $\gamma_{S;\, f_1, \ldots, f_q}(R)$, one row per value combination of $S$ that occurs in $R$. Pad each of its rows to the schema $(A_1, \ldots, A_D, f_1, \ldots, f_q)$ by putting ALL in every $A_i \notin S$. The **data cube** is

$$\text{CUBE}(R) = \bigcup_{S \subseteq \{A_1, \ldots, A_D\}} \text{pad}\big(\gamma_{S;\, f_1, \ldots, f_q}(R)\big).$$

Each row is a **cell**. A cell $c$ fixes the dimensions where $c_i \ne \text{ALL}$, and its group is the set of rows of $R$ that agree with $c$ on them. ALL is not a value of any domain, so a cell with ALL is never confused with a detail row. For $S = \emptyset$, the group-by has one row, the grand total, even when $R$ is empty, as in SQL.

**Size.** If $A_i$ has $C_i$ distinct values in $R$, the cube has at most $\prod_{i=1}^{D} (C_i + 1)$ cells, since each dimension of a cell is one of its $C_i$ values or ALL. Each row of $R$ lies in exactly one cell of each group-by, so the cube also has at most $1 + (2^D - 1)\, n$ cells for $n$ rows. A cube is **dense** when most of the $\prod_i C_i$ finest cells occur, and **sparse** when few do.

**The lattice.** Order the group-bys by inclusion of their sets $S$. This gives the lattice of all subsets of $\{A_1, \ldots, A_D\}$, with the group-by on all dimensions at one end and the grand total at the other. If $S \subseteq T$, the group-by on $S$ can be computed from the group-by on $T$ for the first two classes of aggregates below, which is the basis of [view selection](/view-selection/) for cubes.

**Classes of aggregates.** Gray et al. sort the aggregates by what is needed to combine partial results. Let the multiset $X$ be split into parts $X_1, \ldots, X_m$.

- An aggregate $F$ is **distributive** if there is a $G$ with $F(X) = G(F(X_1), \ldots, F(X_m))$. COUNT, SUM, MIN and MAX are distributive; COUNT is combined with SUM.
- $F$ is **algebraic** if there are a $G$ with values in tuples of a fixed size $M$ and an $H$ with $F(X) = H(G(X_1), \ldots, G(X_m))$. AVG is algebraic with $G = (\text{SUM}, \text{COUNT})$, and so is the standard deviation, with the sum of squares added.
- $F$ is **holistic** if no fixed $M$ is enough for its partial results. MEDIAN, MODE and RANK are holistic.

**ROLLUP and grouping sets.** $\text{ROLLUP}(A_1, \ldots, A_D)$ is the union of the group-bys on the $D + 1$ prefixes $\{A_1, \ldots, A_k\}$, $0 \le k \le D$. A grouping set is any chosen family of subsets; CUBE takes all of them. SQL writes these as `GROUP BY CUBE (...)`, `GROUP BY ROLLUP (...)` and `GROUP BY GROUPING SETS (...)`, shows ALL as a null, and gives the function `GROUPING` to tell such a null from a null of the data.

## Examples and non-examples

**A full cube.** Take the sales (tea, 2023, 4), (tea, 2024, 9), (coffee, 2023, 5), (coffee, 2024, 6), (coffee, 2024, 1), with dimensions product and year and the measure SUM(amount).

| product | year | SUM | group-by |
|---|---|---|---|
| coffee | 2023 | 5 | {product, year} |
| coffee | 2024 | 7 | {product, year} |
| tea | 2023 | 4 | {product, year} |
| tea | 2024 | 9 | {product, year} |
| coffee | ALL | 12 | {product} |
| tea | ALL | 13 | {product} |
| ALL | 2023 | 9 | {year} |
| ALL | 2024 | 16 | {year} |
| ALL | ALL | 25 | {} |

Every pair occurs, so the cube has $(2 + 1)(2 + 1) = 9$ cells. $\text{ROLLUP}(\text{product}, \text{year})$ is the same table without the two rows of the group-by on {year}, 7 rows. Drawn as a two-way table with products as rows and years as columns, the cube is a cross-tab with its row totals, column totals and grand total.

**A sparse cube.** If the sale (tea, 2024, 9) is removed, the cell (tea, 2024) does not occur, and the cube has 8 cells, fewer than the bound 9. There is no row with SUM 0 for a missing pair, because a group-by only has groups that occur.

**Non-example: one GROUP BY.** `GROUP BY product, year` gives only the first four rows. It is one group-by of the cube, not the cube.

**Non-example: the subtotals of a holistic aggregate.** The MEDIAN of (coffee, ALL) cannot be found from the medians of (coffee, 2023) and (coffee, 2024): the medians 5 and 3.5 come from the parts {5} and {6, 1}, while the median of {5, 6, 1} is 5. Such a cell must be computed from its rows, not from finer cells.

**Non-example: null as ALL.** If a sale has a null year, the group-by on {product, year} has a cell (coffee, null). This is a detail cell of the data, not the subtotal (coffee, ALL). Writing ALL as a null without `GROUPING` makes the two look the same.

## Related definitions

- **Group-by aggregation.** One element of the cube; the cube is the union over all subsets of the dimensions. It is computed by [hash aggregation](/hash-aggregation/) or [sort-based aggregation](/sort-based-aggregation/).
- **Iceberg cube.** The cells of the cube whose group has at least a given number of rows, which is CUBE with a `HAVING COUNT(*)` condition. [BUC](/bottom-up-cube/) computes it and skips small groups early.
- **Cuboid.** Another name for the group-by on one subset $S$, seen as one node of the lattice.
- **Materialized view.** A stored query result. A system can store some group-bys of the cube as [materialized views](/materialized-view/) and answer the others from them; [greedy view selection](/hru-greedy-view-selection/) picks which ones.
- **Null semantics.** The rules of [SQL nulls](/sql-null-semantics/) decide how nulls in a dimension group, and why ALL needs to be told apart from them.

## References
