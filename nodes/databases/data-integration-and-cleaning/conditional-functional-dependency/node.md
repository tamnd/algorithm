---
tag: CYNKMP
kind: definition
slug: conditional-functional-dependency
name: Conditional functional dependency
aliases:
- CFD
area: databases/data-integration-and-cleaning
level: advanced
summary: "A functional dependency that holds only on the tuples that match a pattern of constants and wildcards. It can also fix the value that a matching tuple must have."
prereqs: [functional-dependency, armstrongs-axioms]
see_also: [denial-constraint, functional-dependency, database-repair, holoclean, functional-dependency-discovery, equality-generating-dependency, consistent-query-answering, candidate-key]
sources:
  - paper: doi:10.1109/icde.2007.367920
    title: "Philip Bohannon, Wenfei Fan, Floris Geerts, Xibei Jia and Anastasios Kementsietsidis, Conditional functional dependencies for data cleaning, ICDE 2007"
    locator: "pages 746-755: the definition and Example 3.1, Theorems 3.1 to 3.4 on consistency, inference and implication, and Section 4.1 on detection in SQL"
  - paper: doi:10.1145/1366102.1366103
    title: "Wenfei Fan, Floris Geerts, Xibei Jia and Anastasios Kementsietsidis, Conditional functional dependencies for capturing data inconsistencies, ACM TODS 33(2), 2008"
    locator: "the journal version, with the customer example, the static analysis and the SQL detection queries"
  - paper: doi:10.14778/2536258.2536262
    title: "Xu Chu, Ihab F. Ilyas and Paolo Papotti, Discovering denial constraints, PVLDB 6(13), 2013"
    locator: "pages 1498-1509, CFDs as a special case of denial constraints"
---

A conditional functional dependency (CFD) is a [functional dependency](/functional-dependency/) that applies only to the tuples that match a pattern, and that can also state the exact value a matching tuple must have. "Area code 908 means city MH" is a CFD: it holds for the tuples with that area code and says nothing about the others. A plain functional dependency cannot say this. A [denial constraint](/denial-constraint/) can, since each CFD is a set of denial constraints, but denial constraints also allow order comparisons, which CFDs do not have. CFDs keep the equality-only form of functional dependencies, and that keeps their reasoning closer to [Armstrong's axioms](/armstrongs-axioms/).

## Definition

Let $R$ be a relation schema with attributes $\text{attr}(R)$. A **conditional functional dependency** is a pair $\varphi = (X \to Y, T_p)$, where $X \to Y$ is a functional dependency on $R$ and $T_p$ is a *pattern tableau*: a finite set of pattern tuples $t_p$ over $X \cup Y$, each entry of which is a constant of the domain of its attribute or the wildcard "_". A value $a$ *matches* an entry $e$, written $a \asymp e$, if $e$ is "_" or $a = e$. This extends to tuples position by position.

Set semantics holds. An instance $I$ of $R$ *satisfies* $\varphi$ if for every pattern $t_p \in T_p$ and all tuples $t_1, t_2 \in I$, which may be the same tuple,

$$t_1[X] = t_2[X] \asymp t_p[X] \;\implies\; t_1[Y] = t_2[Y] \asymp t_p[Y].$$

Two readings follow from the formula. With $t_1 = t_2$, every tuple that matches $t_p[X]$ must match $t_p[Y]$, so a constant in $t_p[Y]$ fixes a value for one tuple alone. With $t_1 \ne t_2$, two tuples that match $t_p[X]$ and agree on $X$ must agree on $Y$. A plain functional dependency $X \to Y$ is the CFD with one pattern of wildcards only.

## Examples and non-examples

The table Cust has the attributes CC (country code), AC (area code), PN (phone number), NM, STR, CT (city) and ZIP. It is a small table in the style of the customer example of Fan, Geerts, Jia and Kementsietsidis:

| row | CC | AC | PN | NM | STR | CT | ZIP |
|---|---|---|---|---|---|---|---|
| 0 | 01 | 908 | 1111111 | Mike | Tree Ave. | MH | 07974 |
| 1 | 01 | 908 | 1111111 | Rick | Tree Ave. | NYC | 07974 |
| 2 | 01 | 212 | 2222222 | Joe | Elm Str. | NYC | 01202 |
| 3 | 01 | 212 | 2222222 | Jim | Elm Str. | NYC | 02404 |
| 4 | 44 | 131 | 3333333 | Ben | High St. | EDI | EH4 1DT |

- **A CFD with three patterns.** $\varphi = ([\text{CC}, \text{AC}, \text{PN}] \to [\text{STR}, \text{CT}, \text{ZIP}], T_p)$ with the patterns (_, _, _ ‖ _, _, _), (01, 908, _ ‖ _, MH, _) and (01, 212, _ ‖ _, NYC, _). Rows 2 and 3 break the first pattern, the plain functional dependency, since they agree on the phone number but not on the zip code. Row 1 breaks the second pattern alone, since its area code is 908 and its city is not MH. Rows 0 and 1 also break the first pattern on CT. Row 4 matches no constant pattern and has no partner, so it is fine. The violating rows are 0, 1, 2 and 3.
- **The value of one tuple.** $([\text{CC}, \text{AC}] \to [\text{CT}], \{(01, 908 \;‖\; \text{MH}), (01, 212 \;‖\; \text{NYC})\})$ is violated by row 1 alone, in an instance with no other row. The plain dependency $[\text{CC}, \text{AC}] \to [\text{CT}]$ holds on that instance, since one tuple never breaks a functional dependency.
- **An unsatisfiable tableau.** $([A] \to [B], \{(\_ \;‖\; b), (\_ \;‖\; c)\})$ asks every tuple to have $B = b$ and $B = c$. Only the empty instance satisfies it. Functional dependencies never conflict like this, since a one-tuple instance satisfies every set of them.
- **Non-example: an order condition.** "In one state, a higher salary has a rate at least as high" compares values with $<$. It is a denial constraint but not a CFD.
- **Non-example: a disjunction of values.** "The city is MH or NYC" for area code 908 is not a CFD, since a pattern holds one constant or a wildcard. Two patterns with MH and NYC would ask for both.

The violations of one CFD can be found by one scan and one grouping per pattern. This is what the SQL queries $Q^C$ and $Q^V$ of Bohannon et al. do, the second with a GROUP BY on $X$:

```pseudo id=main
CFD-VIOLATIONS(I, (X -> Y, Tp))
L1  V <- empty
L2  for each pattern tp in Tp do
L3      M <- the rows t of I with t[X] matching tp[X]
L4      add to V each row t of M with t[Y] not matching tp[Y]
L5      group the rows of M by t[X]
L6      add to V the rows of each group that holds two different values of t[Y]
L7  return V
```

Line L4 finds the violations by one tuple and line L6 those by two tuples. The result is the set of rows that take part in some violating pair, the same set as checking all pairs, which the code tests against. With hashing, the cost is $O(|T_p| \cdot n \cdot (|X| + |Y|))$ for $n$ rows.

## Related definitions

- **[Functional dependency](/functional-dependency/).** The CFD with one pattern of wildcards.
- **[Denial constraint](/denial-constraint/).** Each CFD is a set of denial constraints. A pattern with a constant in $Y$ gives a constraint on one tuple, such as $\neg (t.\text{CC} = 01 \wedge t.\text{AC} = 908 \wedge t.\text{CT} \ne \text{MH})$. Agreement on $Y$ gives constraints on two tuples.
- **Consistency.** A set of CFDs is consistent if some nonempty instance satisfies it. Bohannon et al. prove that this is NP-complete (Theorem 3.1). The hardness needs attributes with finite domains: without them, consistency is decidable in $O(|\Sigma|^2)$ time (Theorem 3.2).
- **Implication.** Bohannon et al. give a sound and complete inference system for CFDs (Theorem 3.3) and prove that implication is coNP-complete (Theorem 3.4). For plain functional dependencies, implication takes linear time.
- **Repairs.** A CFD violation can be repaired by changing values or by deleting tuples, as on the [database repair](/database-repair/) page. Systems such as [HoloClean](/holoclean/) use CFDs as denial constraints.
- **Discovery.** CFDs can be mined from data, extending the [discovery of functional dependencies](/functional-dependency-discovery/).

## References
