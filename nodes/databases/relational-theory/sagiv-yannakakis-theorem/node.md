---
tag: 45C56P
kind: theorem
slug: sagiv-yannakakis-theorem
name: Sagiv-Yannakakis theorem
aliases:
- containment of unions of conjunctive queries
area: databases/relational-theory
level: advanced
summary: A union of conjunctive queries is contained in another union exactly when each of its members is contained in some member of the other.
prereqs: [conjunctive-query, chandra-merlin-theorem]
see_also: [query-containment-problem, conjunctive-query-minimization, datalog, relational-algebra, answering-queries-using-views, polynomial-hierarchy, np-complete, certain-answers]
sources:
  - paper: doi:10.1145/322217.322221
    title: Yehoshua Sagiv and Mihalis Yannakakis, Equivalences among relational expressions with the union and difference operators, Journal of the ACM 27(4), 633 to 655 (1980)
    locator: the containment test for unions of tableaux, and the Pi-2-p-completeness of equivalence for select, project, join and union expressions
  - paper: doi:10.1145/800105.803397
    title: Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, Proceedings of the 9th Annual ACM Symposium on Theory of Computing (STOC), 77 to 90 (1977)
    locator: the homomorphism criterion and the canonical database for one conjunctive query
  - paper: doi:10.1145/153850.153856
    title: Surajit Chaudhuri and Moshe Y. Vardi, Optimization of real conjunctive queries, Proceedings of the 12th ACM Symposium on Principles of Database Systems (PODS), 59 to 70 (1993)
    locator: containment and equivalence of conjunctive queries under bag semantics
  - paper: doi:10.1016/0743-1066(93)90040-N
    title: Oded Shmueli, Equivalence of DATALOG queries is undecidable, Journal of Logic Programming 15(3), 231 to 241 (1993)
    locator: containment and equivalence of Datalog programs are undecidable
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 6 (static analysis and optimization), the section on unions of conjunctive queries
---

The Sagiv-Yannakakis theorem extends the [Chandra-Merlin theorem](/chandra-merlin-theorem/) from one [conjunctive query](/conjunctive-query/) to a finite union of them. A union $Q_1 \cup \cdots \cup Q_k$ is contained in a union $P_1 \cup \cdots \cup P_l$ if and only if each $Q_i$ is contained in some single $P_j$. So no member of the first union needs two members of the second union to cover it, and [query containment](/query-containment-problem/) for unions of conjunctive queries reduces to $k \cdot l$ tests for single queries. Sagiv and Yannakakis proved it in 1980, in the language of tableaux.

## Statement

We use set semantics: a relation is a set of tuples, and a query returns a set of tuples. A *conjunctive query* (CQ) is a rule $Q(\bar x) \mathbin{:\!-} R_1(\bar u_1), \ldots, R_m(\bar u_m)$ in which each variable of the head $\bar x$ occurs in the body. A *union of conjunctive queries* (UCQ) is a finite union $Q = Q_1 \cup \cdots \cup Q_k$ of CQs whose heads have the same arity, with $Q(D) = Q_1(D) \cup \cdots \cup Q_k(D)$. $Q \subseteq P$ means $Q(D) \subseteq P(D)$ for every database $D$.

**Theorem (Sagiv and Yannakakis 1980).** Let $Q = Q_1 \cup \cdots \cup Q_k$ and $P = P_1 \cup \cdots \cup P_l$ be UCQs over the same schema with heads of the same arity. Then $Q \subseteq P$ if and only if for each $i \in \{1, \ldots, k\}$ there is $j \in \{1, \ldots, l\}$ with $Q_i \subseteq P_j$, that is, with a homomorphism from $P_j$ to $Q_i$.

## In plain words

A union of queries returns every answer that any one of its parts returns. Say you want to know whether one union never gives an answer that a second union misses.

You might expect that a part of the first union could be covered by several parts of the second union together, each catching some of its answers. The theorem says that this never happens for these simple queries. Each part of the first union must be covered by one single part of the second union.

The reason is that each simple query has one most typical database, the query itself read as data. On that database the query finds its own pattern, and one part of the second union must find that answer. That part then finds all the answers.

## Proof

*If.* Let each $Q_i$ be contained in some $P_{j(i)}$. For a database $D$,
$$Q(D) = \bigcup_i Q_i(D) \subseteq \bigcup_i P_{j(i)}(D) \subseteq P(D).$$

*Only if.* Let $Q \subseteq P$, and fix $i$. Let $\bar x_i$ be the head of $Q_i$, and let $D_i$ be the canonical database of $Q_i$: one fact for each atom of the body, with each variable read as a new constant of its own. The identity valuation maps the body of $Q_i$ into $D_i$, so $\bar x_i \in Q_i(D_i) \subseteq Q(D_i) \subseteq P(D_i)$. So $\bar x_i \in P_j(D_i)$ for some $j$. By the Chandra-Merlin theorem, form (3) implies form (1), so $Q_i \subseteq P_j$, and there is a homomorphism from $P_j$ to $Q_i$. $\blacksquare$

The only property of a single CQ that the proof uses is that one database, $D_i$, decides containment of $Q_i$ in every query that is preserved by homomorphisms of databases. Each UCQ is such a query.

## Consequences

- **Containment and equivalence are NP-complete.** For the upper bound, guess for each $i$ an index $j$ and a homomorphism from $P_j$ to $Q_i$, and check the guess in polynomial time. The lower bound holds already for $k = l = 1$, by the reduction from [3-coloring](/three-coloring/) on the Chandra-Merlin page. Equivalence is containment in both directions.
- **An example.** Let $Q_1(x) \mathbin{:\!-} E(x, y), E(y, x)$ and $Q = Q_1$. Let $P_1(x) \mathbin{:\!-} E(x, x)$ and $P_2(x) \mathbin{:\!-} E(x, y), E(y, z)$. The map $y \mapsto y$, $z \mapsto x$ sends $P_2$ into $Q_1$, so $Q \subseteq P_1 \cup P_2$. $P_1$ alone does not cover $Q_1$, because the canonical database $\{E(x, y), E(y, x)\}$ has no loop.
- **Minimization of UCQs.** Delete each member $Q_i$ that is contained in another member that stays, and minimize each remaining member as in [conjunctive query minimization](/conjunctive-query-minimization/). Call the result *irredundant*. If two irredundant UCQs are equivalent, the theorem gives maps $i \mapsto j(i)$ and $j \mapsto i(j)$ with $Q_i \subseteq P_{j(i)} \subseteq Q_{i(j(i))}$. Irredundancy gives $i(j(i)) = i$, so the members match one to one, and each pair is equivalent. So the irredundant form is unique up to renaming, and it has the fewest members and the fewest atoms.
- **Relational expressions with union.** A select, project, join and union expression is a UCQ, but writing it as a UCQ can multiply out unions inside joins and give exponentially many members. Sagiv and Yannakakis showed that equivalence of such expressions is $\Pi_2^p$-complete, a level of the [polynomial hierarchy](/polynomial-hierarchy/) above NP.
- **Non-recursive Datalog.** A non-recursive [Datalog](/datalog/) program unfolds into a UCQ, so containment between such programs is decidable by the theorem, although the unfolding can be large.
- **Rewriting with views.** The rewritings of a query by views in [answering queries using views](/answering-queries-using-views/) are often UCQs, and the test for a correct rewriting is this theorem.

## Tightness

- **Bag semantics.** Count each answer with its multiplicity and use the bag union. Let $Q = Q_1 \uplus Q_2$ with $Q_1(x) \mathbin{:\!-} R(x)$ and $Q_2(x) \mathbin{:\!-} R(x)$, and let $P(x) \mathbin{:\!-} R(x)$. Each member of $Q$ is contained in $P$, but on a relation $R$ with one tuple, $Q$ returns it twice and $P$ once. So the "if" direction fails. Already for single CQs under bag semantics, Chaudhuri and Vardi (1993) showed that equivalence means isomorphism, and containment is harder, with cases that are still open.
- **Comparisons.** With $\le$ in the bodies, let $Q() \mathbin{:\!-} R(x, y)$, $P_1() \mathbin{:\!-} R(x, y), x \le y$ and $P_2() \mathbin{:\!-} R(x, y), y \le x$. Each pair of values is ordered one way or the other, so $Q \subseteq P_1 \cup P_2$, but $Q$ is contained in neither $P_1$ nor $P_2$.
- **Negation.** In the same way, $Q() \mathbin{:\!-} R(x)$ is contained in the union of $R(x), S(x)$ and $R(x), \neg S(x)$, but in neither member. The canonical database argument needs queries that are preserved by homomorphisms.
- **Infinite unions.** A recursive Datalog program is an infinite union of CQs. Containment of a CQ in such a program is still decidable, by evaluating the program on the canonical database. Containment of one Datalog program in another is undecidable (Shmueli 1993).

## History

Yehoshua Sagiv and Mihalis Yannakakis proved the theorem in their 1980 paper on relational expressions with union and difference, written in terms of tableaux, which are another notation for CQs. The same paper showed $\Pi_2^p$-completeness of equivalence for expressions with union and studied expressions with difference. The result extends the homomorphism theorem of Chandra and Merlin (1977), and the textbook of Abiteboul, Hull and Vianu presents both together.

## References
