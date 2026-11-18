---
tag: PG4SYW
kind: theorem
slug: view-rewriting-np-completeness
name: NP-completeness of rewriting queries using views
aliases:
- Levy-Mendelzon-Sagiv-Srivastava theorem
area: databases/data-integration-and-cleaning
level: advanced
summary: "Deciding whether a conjunctive query has an equivalent rewriting using conjunctive views is NP-complete, and a rewriting needs no more view atoms than the query has subgoals."
prereqs: [conjunctive-query, chandra-merlin-theorem, query-containment-problem, np-complete]
see_also: [answering-queries-using-views, minicon-algorithm, bucket-algorithm, inverse-rules-algorithm, conjunctive-query-minimization, materialized-view, view-selection, three-coloring]
sources:
  - paper: doi:10.1145/212433.220198
    title: "Alon Y. Levy, Alberto O. Mendelzon, Yehoshua Sagiv and Divesh Srivastava, Answering queries using views, PODS 1995"
    locator: "pages 95-104, the bound on the size of a rewriting and the NP-completeness of finding complete and partial rewritings"
  - paper: doi:10.1007/s007780100054
    title: "Alon Y. Halevy, Answering queries using views: a survey, The VLDB Journal 10(4), 2001"
    locator: "pages 270-294, the section on the complexity of finding rewritings"
  - paper: doi:10.1145/800105.803397
    title: "Ashok K. Chandra and Philip M. Merlin, Optimal implementation of conjunctive queries in relational data bases, STOC 1977"
    locator: "pages 77-90, containment of conjunctive queries by homomorphisms and its NP-completeness"
---

Levy, Mendelzon, Sagiv and Srivastava proved in 1995 that deciding whether a [conjunctive query](/conjunctive-query/) can be computed exactly from a set of conjunctive views is NP-complete. The key step is a size bound: if an equivalent rewriting exists, one exists with at most as many view atoms as the query has subgoals. The theorem is about equivalent rewritings, the ones used to optimize queries with [materialized views](/materialized-view/). The algorithms for data integration, such as [MiniCon](/minicon-algorithm/), look for maximally contained rewritings instead, which always exist, so for them the question is how large they are, not whether they exist.

## Statement

A query is $Q(\bar x) \text{ :- } R_1(\bar u_1), \ldots, R_n(\bar u_n)$ in AHV notation, and each view is a conjunctive query $V(\bar Y) \text{ :- } S_1(\bar w_1), \ldots, S_r(\bar w_r)$. There are no comparison predicates, and set semantics holds. A *rewriting* of $Q$ using the views is a conjunctive query $P$ whose body atoms are view atoms. Its *expansion* $P^{exp}$ replaces each view atom by the body of the view, with the head variables replaced by the arguments of the atom and the existential variables replaced by new variables. $P$ is an *equivalent rewriting* if $P^{exp} \equiv Q$, that is, $P^{exp} \subseteq Q$ and $Q \subseteq P^{exp}$.

**Theorem (Levy, Mendelzon, Sagiv and Srivastava).** Let $Q$ have $n$ subgoals.

1. **Bounded size.** If $Q$ has an equivalent rewriting using the views, then it has one with at most $n$ view atoms.
2. **Complexity.** The problem "given $Q$ and the views, does $Q$ have an equivalent rewriting using them?" is NP-complete in combined complexity. It stays NP-hard with a single view.

The paper also studies partial rewritings, which may mix view atoms with atoms of the base relations. This page proves the statement for rewritings that use views only.

## In plain words

You want to answer a question using only some stored answers to other questions. The theorem says two things. First, if it can be done at all, you never need more stored tables than the question has parts, so the search space is finite and small to describe. Second, the search is as hard as the hardest problems whose answers are easy to check: a proposed plan can be checked quickly, but finding one can take time that grows exponentially in the size of the question. This is no worse than checking whether two questions always give the same answers, which is already this hard.

## Proof

The proof uses the [Chandra-Merlin theorem](/chandra-merlin-theorem/): $A \subseteq B$ for conjunctive queries if and only if there is a containment mapping from $B$ to $A$, a map on variables that sends the head of $B$ to the head of $A$ and each body atom of $B$ to a body atom of $A$.

**Lemma 1 (bounded size).** Let $P$ be an equivalent rewriting of $Q$. Then $P$ has a sub-rewriting $P'$ with at most $n$ view atoms that is also equivalent to $Q$.

*Proof.* Since $P^{exp} \subseteq Q$, there is a containment mapping $\tau$ from $Q$ to $P^{exp}$. Each of the $n$ subgoals of $Q$ goes to an atom of the expansion of one view atom of $P$. Let $P'$ keep the head of $P$ and only these at most $n$ view atoms. The head of $P$ is $\tau(\bar x)$, whose variables occur in the image atoms, so $P'$ is safe. Then $\tau$ is also a containment mapping from $Q$ to $P'^{exp}$, so $P'^{exp} \subseteq Q$. The body of $P'$ is a subset of the body of $P$, so the identity on $P'^{exp}$ is a containment mapping into $P^{exp}$, and $P^{exp} \subseteq P'^{exp}$. Together, $Q \subseteq P^{exp} \subseteq P'^{exp} \subseteq Q$. $\square$

The rewriting $P'$ has at most $n$ atoms, each with at most $a$ arguments for the largest view arity $a$, so after renaming its variables it has size polynomial in the input.

**Lemma 2 (membership in NP).** The problem is in NP.

*Proof.* A certificate is a rewriting $P'$ with at most $n$ view atoms, a containment mapping from $Q$ to $P'^{exp}$, and a containment mapping from $P'^{exp}$ to $Q$. The expansion has at most $n m$ atoms, where $m$ bounds the size of a view body, so all three objects have polynomial size, and checking that two maps are containment mappings takes polynomial time. By Lemma 1, a certificate exists whenever an equivalent rewriting exists. $\square$

**Lemma 3 (NP-hardness with one view).** Containment of Boolean conjunctive queries reduces to the problem in polynomial time.

*Proof.* Let $A$ and $B$ be Boolean conjunctive queries. Rename the variables of $B$ apart from those of $A$, giving $B'$. Let $Q() \text{ :- } \text{body}(A)$ and let the only view be $V() \text{ :- } \text{body}(A), \text{body}(B')$. A rewriting is $Q'() \text{ :- } V(), \ldots, V()$ with one or more atoms, and the expansions of all of them are equivalent to $A \wedge B'$, since copies of a Boolean conjunction add nothing. Always $A \wedge B' \subseteq A$. A containment mapping from $A \wedge B'$ to $A$ exists if and only if one exists from $B'$ to $A$, since the two parts share no variables and the identity handles the part $A$. So $Q$ has an equivalent rewriting if and only if $A \subseteq B$. Containment of Boolean conjunctive queries is NP-hard: a graph $G$ is [3-colorable](/three-coloring/) if and only if the query "there is a triangle of colors" with the edges of $K_3$ in both directions is contained in the query that has one atom per edge of $G$. $\square$

**Proof of the theorem.** Part 1 is Lemma 1. Part 2 is Lemmas 2 and 3, and Lemma 3 uses one view. $\blacksquare$

## Consequences

- **A finite search.** Lemma 1 gives the brute-force algorithm: try all sets of at most $n$ view atoms over the variables of $Q$, and test each for equivalence. The [bucket algorithm](/bucket-algorithm/) and MiniCon organize this search.
- **Hardness is inherited from containment.** The problem is no harder than [query containment](/query-containment-problem/), and Lemma 3 shows it is no easier. Classes of queries where containment is in polynomial time, such as acyclic queries, are natural places to look for easier cases.
- **Minimal rewritings.** The rewriting of Lemma 1 can be further [minimized](/conjunctive-query-minimization/) by dropping atoms while equivalence holds, as for any conjunctive query.
- **View selection.** Choosing which views to store so that a workload has equivalent rewritings, the [view selection](/view-selection/) problem, builds on this test.

## Tightness

- **The size bound $n$ is tight.** Let $Q(x_1, \ldots, x_n) \text{ :- } p_1(x_1), \ldots, p_n(x_n)$ with views $V_i(x) \text{ :- } p_i(x)$. Each $p_i$ occurs in only one view, so each equivalent rewriting needs at least one $V_i$ atom for each $i$, that is, $n$ atoms.
- **No smaller bound in terms of the views.** The bound does not depend on the number or the size of the views, and it cannot be improved to the number of views: in the previous example a single view $V(x) \text{ :- } p(x)$ for $Q(x_1, \ldots, x_n) \text{ :- } p(x_1), \ldots, p(x_n)$ still needs $n$ atoms.
- **Comparisons and other languages.** With comparison predicates, unions or recursion in the query or the views, the bound and the complexity change, and the proof above does not apply as stated.

## History

Chandra and Merlin proved in 1977 that containment and equivalence of conjunctive queries are decidable by homomorphisms and NP-complete. Levy, Mendelzon, Sagiv and Srivastava studied the use of views for query answering at PODS 1995. They proved the bound on the size of rewritings and the NP-completeness of finding rewritings, for rewritings that use only views and for partial ones. Halevy's 2001 survey made the result the starting point of the theory of answering queries using views.

## References
