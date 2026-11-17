---
tag: JN7WRZ
kind: model
slug: provenance-semirings
name: Provenance semirings
aliases:
- K-relations
- how-provenance
area: databases/relational-theory
level: advanced
summary: "Annotate tuples with elements of a commutative semiring and carry them through positive queries; provenance polynomials are the most general."
prereqs: [relational-algebra, datalog]
see_also: [why-and-where-provenance, probabilistic-database, datalog-program-analysis, kleene-fixed-point-theorem, semi-naive-evaluation, incremental-view-maintenance, floyd-warshall, knowledge-compilation]
sources:
  - paper: doi:10.1145/1265530.1265535
    title: Todd J. Green, Grigoris Karvounarakis and Val Tannen, Provenance semirings, Proceedings of the 26th ACM Symposium on Principles of Database Systems (PODS), 31 to 40 (2007)
    locator: K-relations and the positive algebra on them, commutation with homomorphisms, the provenance polynomials N[X] as the most general annotations, and Datalog over omega-continuous semirings with formal power series
  - paper: doi:10.1145/1634.1886
    title: Tomasz Imielinski and Witold Lipski, Incomplete information in relational databases, Journal of the ACM 31(4), 761 to 791 (1984)
    locator: conditional tables, whose tuples carry Boolean conditions through the algebra, an early case of annotated relations
  - paper: doi:10.1561/1900000006
    title: James Cheney, Laura Chiticariu and Wang-Chiew Tan, Provenance in databases, why, how, and where, Foundations and Trends in Databases 1(4), 379 to 474 (2009)
    locator: how-provenance and its relation to lineage and why-provenance
---

Provenance semirings are a model of query evaluation in which each tuple carries an annotation from a commutative semiring, and the operators of the positive relational algebra combine the annotations by the semiring operations: alternative use of data adds them, and joint use multiplies them. Green, Karvounarakis and Tannen introduced the model in 2007. With the Boolean semiring it is set semantics, with the natural numbers it is bag semantics, and with the semiring $\mathbb{N}[X]$ of polynomials it records *how* each output was derived. That last case, the provenance polynomials, is the most general one: every other annotation is obtained from it by evaluating the polynomials.

## The machine

**Semirings.** A *commutative semiring* is a set $K$ with two operations $+$ and $\cdot$ and two elements $0$ and $1$ such that $+$ and $\cdot$ are associative and commutative, $0$ is the identity of $+$, $1$ is the identity of $\cdot$, $\cdot$ distributes over $+$, and $0 \cdot a = 0$ for all $a$. There is no subtraction or division in general. The examples used here:

| Semiring | Set | $+$ | $\cdot$ | $0$ | $1$ | Use |
|---|---|---|---|---|---|---|
| $\mathbb{B}$ | $\{\mathit{false}, \mathit{true}\}$ | or | and | false | true | set semantics |
| $\mathbb{N}$ | $\{0, 1, 2, \ldots\}$ | sum | product | $0$ | $1$ | bag semantics |
| tropical | $\mathbb{N} \cup \{\infty\}$ | min | sum | $\infty$ | $0$ | cost of the cheapest derivation |
| Viterbi | $[0, 1]$ | max | product | $0$ | $1$ | confidence of the best derivation |
| $\mathrm{Why}(X)$ | sets of subsets of $X$ | union | pairwise union | $\emptyset$ | $\{\emptyset\}$ | why-provenance |
| $\mathbb{N}[X]$ | polynomials over $X$ with coefficients in $\mathbb{N}$ | sum | product | $0$ | $1$ | provenance polynomials |

In $\mathrm{Why}(X)$, the pairwise union of $A$ and $B$ is $\{a \cup b \mid a \in A, b \in B\}$.

**K-relations.** Fix a commutative semiring $K$. A *K-relation* over a set of attributes $U$ is a function $R$ from the tuples over $U$ to $K$ whose *support* $\{t \mid R(t) \neq 0\}$ is finite. The value $R(t)$ is the annotation of $t$; a tuple with annotation $0$ is absent. A K-instance gives a K-relation to each relation name. For provenance, each input tuple gets its own variable as its annotation, from a set $X$ of tuple identifiers.

**The positive algebra on K-relations** (Green, Karvounarakis and Tannen 2007). For K-relations $R, R_1$ over $U$, $R_2$ over $U_2$, and a selection predicate $P$ that returns $0$ or $1$:

- *empty relation*: $\emptyset(t) = 0$ for every $t$;
- *union*: $(R \cup R')(t) = R(t) + R'(t)$;
- *projection*: $(\pi_{V} R)(t) = \sum \{\, R(t') \mid t'[V] = t,\ R(t') \neq 0 \,\}$;
- *selection*: $(\sigma_{P} R)(t) = R(t) \cdot P(t)$;
- *natural join*: $(R_1 \bowtie R_2)(t) = R_1(t[U]) \cdot R_2(t[U_2])$, for $t$ over $U \cup U_2$;
- *renaming*: moves the annotation with the tuple.

The sums are finite, because supports are finite. So $+$ means "derived in another way" and $\cdot$ means "derived by using both". Union and projection, which merge tuples, add; join, which needs both inputs, multiplies.

**Datalog.** A recursive rule can derive a tuple in infinitely many ways, so its annotation is an infinite sum. Green, Karvounarakis and Tannen use *omega-continuous* semirings: $K$ is ordered by $a \leq b$ if $b = a + c$ for some $c$, every increasing chain $a_0 \leq a_1 \leq \cdots$ has a least upper bound, and $+$ and $\cdot$ preserve these bounds. Then the immediate consequence operator of a [Datalog](/datalog/) program on K-instances is omega-continuous, and the program's meaning is its least fixed point, the limit of the rounds of naive evaluation starting from the empty instance, as in the [Kleene fixed-point theorem](/kleene-fixed-point-theorem/). $\mathbb{B}$, $\mathbb{N}^{\infty} = \mathbb{N} \cup \{\infty\}$ and the tropical semiring are omega-continuous; $\mathbb{N}$ is not, since $1 + 1 + \cdots$ has no bound in $\mathbb{N}$.

## What it counts

The model assigns to each output tuple an element of $K$, computed from the annotations of the input tuples. What the element means depends on $K$: presence ($\mathbb{B}$), multiplicity ($\mathbb{N}$), the cost or confidence of the best derivation (tropical, Viterbi), the sets of tuples that witness it ($\mathrm{Why}(X)$), or the full derivation record ($\mathbb{N}[X]$). In $\mathbb{N}[X]$, each monomial is one derivation: its variables are the input tuples it uses, and an exponent counts how many times it uses a tuple. The coefficient counts the derivations that use the same tuples the same number of times.

**Example.** Let $E(\mathit{src}, \mathit{dst})$ have the three edges $(a, b)$, $(b, a)$, $(a, a)$, annotated $u$, $v$, $w$. The query

$$Q = \pi_{\mathit{src}}\big(E \bowtie \rho_{\mathit{dst} \to \mathit{src},\ \mathit{src} \to \mathit{dst}}(E)\big)$$

returns each node $x$ with edges $(x, y)$ and $(y, x)$, that is, each node on a cycle of length 1 or 2. Node $a$ has two derivations, $y = b$ with edges $u$ and $v$, and $y = a$ with the edge $w$ used twice. Node $b$ has one, with $v$ and $u$. So in $\mathbb{N}[X]$

$$Q(a) = uv + w^{2}, \qquad Q(b) = uv.$$

Each other semiring gives its value by substitution:

- $\mathbb{B}$ with $u = v = w = \mathit{true}$: both nodes are in the answer, as in set semantics.
- $\mathbb{N}$ with $u = 2$, $v = 1$, $w = 3$, that is, two copies of $(a, b)$ and three of $(a, a)$ in a bag: $Q(a) = 2 \cdot 1 + 3^{2} = 11$ and $Q(b) = 2$. Evaluating the same query on the bag directly gives 11 copies of $a$ and 2 of $b$.
- Tropical with edge costs $u = 1$, $v = 2$, $w = 5$: $Q(a) = \min(1 + 2, 5 + 5) = 3$ and $Q(b) = 3$.
- $\mathrm{Why}(X)$ with $u = \{\{u\}\}$ and so on: $Q(a) = \{\{u, v\}, \{w\}\}$. Deleting $w$ keeps $a$ in the answer, through $\{u, v\}$; deleting $u$ also keeps it, through $\{w\}$.

**A recursive example.** With two edges $(a, b)$ and $(b, a)$, annotated $x$ and $y$, the transitive closure program $T(s, d) \leftarrow E(s, d)$, $T(s, d) \leftarrow T(s, m), E(m, d)$ derives $T(a, b)$ by the paths $a b$, $a b a b$, $a b a b a b$, and so on. Its annotation is the formal power series $x + x^{2} y + x^{3} y^{2} + \cdots$ in $\mathbb{N}^{\infty}[[X]]$. In $\mathbb{N}^{\infty}$ with $x = y = 1$ this is $\infty$, the number of derivations; in $\mathbb{B}$ it is true; in the tropical semiring with costs $x$ and $y$ it is $x$, the cost of the shortest path.

## Relation to other models

- **Set and bag semantics.** A $\mathbb{B}$-relation is an ordinary relation, and the positive algebra on $\mathbb{B}$-relations is the [relational algebra](/relational-algebra/) under set semantics. An $\mathbb{N}$-relation is a bag, and the positive algebra on $\mathbb{N}$-relations is bag semantics, as in SQL without DISTINCT. The model puts the two under one definition.
- **Why-provenance and lineage.** [Why-provenance](/why-and-where-provenance/) is the $\mathrm{Why}(X)$ semiring; lineage and the minimal witness basis are two further semirings. Each is a homomorphic image of $\mathbb{N}[X]$, so how-provenance contains strictly more information than each of them: $uv + w^{2}$ and $uv + w$ have the same why-provenance, $\{\{u, v\}, \{w\}\}$, but are different polynomials.
- **Conditional tables and probabilistic databases.** The conditional tables of Imielinski and Lipski (1984) annotate tuples with Boolean conditions; for positive queries this is a K-relation over the semiring of positive Boolean expressions. A [probabilistic database](/probabilistic-database/) evaluates a query by computing such an expression for each answer, its *lineage formula*, and then its probability. Turning the formula into a form where the probability is easy is [knowledge compilation](/knowledge-compilation/).
- **Program analysis and path problems.** A Datalog program over an omega-continuous semiring is a system of fixpoint equations over that semiring, as in [Datalog-based program analysis](/datalog-program-analysis/) and the algebraic path problems: all-pairs shortest paths, as in [Floyd-Warshall](/floyd-warshall/), is the transitive closure program over the tropical semiring. The equations over the semiring of regular languages are those of [Kleene algebra](/kleene-algebra/).
- **Incremental maintenance.** Counting the derivations of each tuple, the $\mathbb{N}$ annotation, is the counting algorithm of [incremental view maintenance](/incremental-view-maintenance/): a deletion subtracts the derivations it removes, and the tuple disappears when its count reaches 0.

## Known results in the model

All results are from Green, Karvounarakis and Tannen (2007) and are for the positive relational algebra (union of conjunctive queries) unless they say Datalog.

- **Commutation with homomorphisms.** If $h : K \to K'$ is a semiring homomorphism (it preserves $+$, $\cdot$, $0$ and $1$) and $Q$ is a positive algebra query, then $Q(h(I)) = h(Q(I))$, where $h(I)$ applies $h$ to every annotation. *Proof.* Each operator computes its output annotations by $+$ and $\cdot$ from its inputs, and $h$ commutes with both; induction on $Q$.
- **$\mathbb{N}[X]$ is the most general.** $\mathbb{N}[X]$ is the free commutative semiring generated by $X$: every map $\nu : X \to K$ into a commutative semiring extends to exactly one homomorphism $\mathrm{Eval}_{\nu} : \mathbb{N}[X] \to K$, which substitutes $\nu(x)$ for each $x$. With the previous result, for every K-instance $I$ whose tuples are annotated $\nu(x)$ for tuple variables $x$, the K-annotation of each answer is $\mathrm{Eval}_{\nu}$ of its provenance polynomial. So one evaluation in $\mathbb{N}[X]$ serves every semiring.
- **Equivalence.** Two positive queries return the same $\mathbb{N}[X]$-relation on every $\mathbb{N}[X]$-instance if and only if they return the same K-relation on every K-instance, for every commutative semiring $K$. This follows from the previous result, so equivalence under $\mathbb{N}[X]$ is the strongest notion of equivalence in the model, stronger than bag equivalence, which is stronger than set equivalence.
- **Which identities hold.** The usual identities of the positive algebra, associativity and commutativity of union and join, distributivity of join over union, and the pushing of selections and projections, hold on K-relations because $K$ is a commutative semiring; Green, Karvounarakis and Tannen showed that the semiring laws are what these identities need. Identities such as $R \cup R = R$ need $+$ to be idempotent, so they hold in $\mathbb{B}$ but not in $\mathbb{N}$ or $\mathbb{N}[X]$.
- **Datalog.** Over omega-continuous semirings the least fixed point exists and is reached as the limit of the rounds of naive evaluation. The most general annotation domain for Datalog is the semiring $\mathbb{N}^{\infty}[[X]]$ of formal power series with coefficients in $\mathbb{N}^{\infty}$: the coefficient of a monomial is the number of derivation trees of the tuple that use exactly those tuples, and it can be $\infty$. Green, Karvounarakis and Tannen gave algorithms that decide, for each output tuple, whether its series is a polynomial, and compute it when it is.
- **Limits.** Difference and negation are not covered: a commutative semiring has no subtraction, and $R - S$ does not fit the "derived in another way, derived by using both" reading. Aggregation is not covered either. Both need extensions of the model with more structure on $K$.

## References
