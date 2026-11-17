---
tag: 66MQQF
kind: concept
slug: sql-null-semantics
name: Three-valued logic of SQL nulls
aliases:
- SQL null semantics
- unknown truth value in SQL
area: databases/relational-theory
level: core
summary: "SQL gives a comparison with NULL the value UNKNOWN, combines truth values by Kleene's three-valued logic and keeps a row only when its condition is TRUE, so answers need not be certain."
prereqs: [relational-algebra, relational-calculus]
see_also: [certain-answers, codds-theorem, group-by-aggregation, hash-aggregation, semijoin, universal-solution, chase-algorithm, relational-model]
sources:
  - book: isbn:9780131873254
    title: Hector Garcia-Molina, Jeffrey D. Ullman and Jennifer Widom, Database Systems, The Complete Book, second edition, Pearson (2008)
    locator: Section 6.1 (null values, comparisons with NULL and the truth value UNKNOWN) and Section 6.4 (grouping, aggregation and nulls)
  - paper: doi:10.1145/2877206
    title: Leonid Libkin, SQL's three-valued logic and certain answers, ACM Transactions on Database Systems 41(1), article 1, 1 to 28 (2016)
    locator: SQL answers compared with certain answers, with false positives and false negatives, and a modified three-valued semantics that gives correctness guarantees
  - paper: doi:10.1145/1634.1886
    title: Tomasz Imielinski and Witold Lipski, Incomplete information in relational databases, Journal of the ACM 31(4), 761 to 791 (1984)
    locator: Codd tables, naive tables and conditional tables, and the computation of certain answers
  - paper: doi:10.1145/320107.320109
    title: E. F. Codd, Extending the database relational model to capture more meaning, ACM Transactions on Database Systems 4(4), 397 to 434 (1979)
    locator: the null value with a three-valued logic for the relational model
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 19 (incomplete information, Codd tables and certain answers)
---

SQL marks a missing value with NULL and evaluates conditions in a three-valued logic: a comparison that involves NULL is neither TRUE nor FALSE but UNKNOWN, and AND, OR and NOT follow the strong three-valued logic of Kleene. A query keeps a row only when its WHERE condition is TRUE, but other parts of the language, such as GROUP BY, DISTINCT and CHECK constraints, treat NULL in other ways. The result is easy to run but does not match the logical meaning of "unknown value": a SQL answer can contain a row that is not certain, and it can miss a row that is certain, in the sense of [certain answers](/certain-answers/). This page is about the rules of SQL; the theory of incomplete databases uses labeled nulls and certain answers instead.

## In plain words

A database cell can be empty because the value is not known. SQL writes this as NULL. When you ask "is this unknown salary above 1000?", SQL does not answer yes or no. It answers "unknown". A filter keeps a row only on yes, so unknown rows drop out.

That sounds safe, but it is not the same as reasoning about all the values that the empty cell could hold. Some questions are yes for every possible value, and SQL still says unknown. Some answers that SQL returns would be wrong for some possible values. And a few SQL features, such as grouping and removing duplicates, treat two empty cells as equal, while a plain comparison of two empty cells gives unknown. Programmers who forget these rules write queries that silently lose rows.

## The idea

**Three truth values.** SQL has TRUE, FALSE and UNKNOWN. Order them as FALSE < UNKNOWN < TRUE. In Kleene's strong three-valued logic, AND is the minimum, OR is the maximum, and NOT swaps TRUE and FALSE and keeps UNKNOWN:

| $p$ | $q$ | $p$ AND $q$ | $p$ OR $q$ | NOT $p$ |
|---|---|---|---|---|
| TRUE | UNKNOWN | UNKNOWN | TRUE | FALSE |
| FALSE | UNKNOWN | FALSE | UNKNOWN | TRUE |
| UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN | UNKNOWN |

The other rows follow by symmetry or are those of two-valued logic. For one connective, the Kleene value is the value on which both ways of filling in each UNKNOWN agree, and UNKNOWN if they disagree: FALSE AND UNKNOWN is FALSE because FALSE AND $x$ is FALSE for both values of $x$. That is the reason for the rules, and also their limit: two UNKNOWNs that come from the same null are not independent, and the logic does not see it, so $p$ OR NOT $p$ is UNKNOWN when $p$ is UNKNOWN.

**The rules of SQL** (the SQL standard, as described by Garcia-Molina, Ullman and Widom):

- A comparison $x \,\theta\, y$ with $\theta \in \{=, \neq, <, \le, >, \ge\}$ is UNKNOWN if $x$ or $y$ is NULL. In particular NULL = NULL is UNKNOWN. The tests $x$ IS NULL and $x$ IS NOT NULL are always TRUE or FALSE.
- WHERE, ON and HAVING keep a row only if the condition is TRUE. Both FALSE and UNKNOWN drop it.
- A CHECK constraint rejects a row only if its condition is FALSE. So CHECK (salary > 0) accepts a row whose salary is NULL.
- GROUP BY, DISTINCT, UNION, INTERSECT and EXCEPT treat two NULLs as the same value: all rows with NULL in the grouping column form one group, and duplicates with NULL in the same places are removed. The predicate IS NOT DISTINCT FROM gives this comparison explicitly.
- Aggregates skip NULL inputs, except COUNT(*), which counts rows. SUM, AVG, MIN and MAX of an empty input, or of only NULLs, give NULL; COUNT of such an input gives 0.
- $x$ IN (subquery) is $x = v_1$ OR $x = v_2$ OR ... over the values $v_i$ of the subquery, and $x$ NOT IN (subquery) is its negation. If the subquery returns a NULL and no $v_i$ equals $x$, the disjunction is UNKNOWN, so NOT IN is never TRUE.
- Outer joins pad the missing side with NULLs. These NULLs behave in later operators like every other NULL.

In code one writes NULL as `None` and the three truth values as `True`, `False` and `None`, with a filter that keeps a row only when the condition is `True`, not when it is `None`.

**Certain answers.** Read each NULL as an unknown value of the domain, a different unknown for each occurrence (a *Codd null*). A *completion* (possible world) of a database $D$ replaces each NULL by a constant. A tuple $t$ without nulls is a *certain answer* of $Q$ on $D$ if $t \in Q(D')$ for every completion $D'$ (Imielinski and Lipski 1984). SQL does not compute this. Libkin (2016) showed that SQL answers can have *false positives*, rows that are not certain, and *false negatives*, certain rows that SQL misses, and that in general the two semantics can be unrelated. He also showed that a modified three-valued evaluation of relational calculus queries does give certainty guarantees. For unions of conjunctive queries over tables with nulls, naive evaluation (treat each null as a fresh constant, evaluate, drop the rows with nulls) gives the certain answers (Imielinski and Lipski 1984); SQL does not do this either, because it compares nulls with UNKNOWN instead of as constants.

## Examples

All examples use set semantics for the answers unless they show counts.

- **Comparison with NULL.** Emp(name, salary) has the rows (ann, 1200), (bob, NULL). SELECT name FROM Emp WHERE salary > 1000 returns ann only. WHERE salary <= 1000 returns nobody. So the two queries together do not return all rows, although every salary is either above 1000 or not. WHERE salary = NULL returns nobody, even bob; the correct test is salary IS NULL.
- **A false negative.** R(A) has the single row (NULL). SELECT 'yes' FROM R WHERE A = 1 OR A <> 1 returns nothing: both comparisons are UNKNOWN, and UNKNOWN OR UNKNOWN is UNKNOWN. In every completion of R, one of the two comparisons is true, so 'yes' is a certain answer that SQL misses.
- **A false positive.** R(A) = {(1)} and S(A) = {(NULL)}. SELECT A FROM R EXCEPT SELECT A FROM S returns (1), because EXCEPT treats NULL as a value distinct from 1. In the completion where the NULL is 1, the difference is empty. So (1) is not a certain answer.
- **NOT IN against NOT EXISTS.** Customer(id) = {1, 2, 3} and Orders(cust) = {1, NULL}. The query SELECT id FROM Customer WHERE id NOT IN (SELECT cust FROM Orders) returns nothing: for id = 2, the test is NOT (2 = 1 OR 2 = NULL), which is NOT (FALSE OR UNKNOWN), which is UNKNOWN. The query SELECT id FROM Customer c WHERE NOT EXISTS (SELECT * FROM Orders o WHERE o.cust = c.id) returns {2, 3}, because the inner WHERE is not TRUE for the NULL row, so no row is found. The two queries are equivalent on databases without nulls, and they differ here. The certain answer is empty: the completion that puts 2 in place of the NULL removes 2 from the answer, and the completion that puts 3 there removes 3, so neither is in every answer. Here NOT IN happens to give the certain answer and NOT EXISTS gives two false positives.
- **Aggregates.** T(x) has the rows 1, NULL and 3. COUNT(*) is 3, COUNT(x) is 2, SUM(x) is 4, and AVG(x) is 2, the average of 1 and 3, not 4/3. On an empty T, COUNT(*) and COUNT(x) are 0 and SUM(x) is NULL.
- **Grouping.** U(dept, pay) has the rows (a, 10), (NULL, 20), (NULL, 30). SELECT dept, SUM(pay) FROM U GROUP BY dept returns two groups, (a, 10) and (NULL, 50): the two NULLs are put in one group, although NULL = NULL is UNKNOWN.
- **CHECK.** A table with CHECK (pay > 0) accepts the row (c, NULL), because the condition is UNKNOWN, not FALSE.
- **Outer join and a later filter.** Customer LEFT OUTER JOIN Orders ON Orders.cust = Customer.id, with the data above, pads customers 2 and 3 with a NULL order. A later WHERE Orders.cust = Customer.id drops those rows again, and the outer join behaves like an inner join. To find the customers without orders, write WHERE Orders.cust IS NULL.

## Where it is used

- **Every SQL query.** WHERE, ON, HAVING and CHECK follow the rules above, so the rules decide the answer of each query over columns that allow NULL.
- **Query rewriting.** An optimizer must keep the NULL behavior when it rewrites a query. NOT IN cannot be turned into an anti-join (see [semijoin](/semijoin/) for semijoin and antijoin) unless the inner column is known to be NOT NULL or the rewrite adds a test for NULL, because the anti-join keeps the rows that NOT IN drops. Rewrites of predicates such as NOT (a > b) into a <= b are valid in three-valued logic, while p OR NOT p into TRUE is not.
- **Aggregation operators.** Physical [grouping and aggregation](/group-by-aggregation/), for example [hash aggregation](/hash-aggregation/), must put all NULL keys in one group and skip NULL inputs of SUM, AVG, MIN and MAX.
- **Incomplete databases in theory.** Data exchange and data integration use labeled nulls and certain answers instead of SQL NULLs; see [universal solution](/universal-solution/) and the [chase](/chase-algorithm/). Codd (1979) proposed a null with a three-valued logic for the relational model, and the rules of SQL descend from that proposal. Imielinski and Lipski (1984) defined the representation systems (Codd tables, naive tables, conditional tables) in which certain answers are computed exactly.
- **Equivalence of query languages.** [Codd's theorem](/codds-theorem/) assumes two-valued logic without nulls. With NULL, the equivalence of SQL and the relational calculus must be stated for the three-valued semantics.

## References
