---
tag: THAFBS
kind: problem
slug: dependency-implication-problem
name: Dependency implication problem
aliases:
- implication of dependencies
- FD implication problem
- membership problem for functional dependencies
area: systems/database-algorithms
level: advanced
summary: "Decide whether a set of dependencies implies another. For FDs this takes linear time, but finding a key of size at most k and testing a prime attribute are NP-complete."
prereqs: [attribute-closure-algorithm, armstrongs-axioms, np-complete]
see_also: [attribute-closure-problem, minimal-cover-problem, third-normal-form, chase-algorithm, query-containment-problem, vertex-cover, horn-sat, hitting-set]
sources:
  - paper: doi:10.1145/320064.320066
    title: Catriel Beeri and Philip A. Bernstein, Computational problems related to the design of normal form relational schemas, ACM Transactions on Database Systems 4(1), 30 to 59 (1979)
    locator: the membership problem for functional dependencies, its linear-time algorithm, and the equivalence of FD sets
  - paper: doi:10.1016/0022-0000(78)90009-0
    title: Cláudio L. Lucchesi and Sylvia L. Osborn, Candidate keys for relations, Journal of Computer and System Sciences 17(2), 270 to 279 (1978)
    locator: the algorithm that lists all candidate keys, and the NP-completeness of the key of bounded size and of the prime attribute problems
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Section 8.2 (the implication problem for functional dependencies); Section 8.4 (the chase); Chapter 9 (inclusion dependencies, undecidability of fd's with ind's)
  - book: isbn:9780881751888
    title: Jeffrey D. Ullman, Principles of Database and Knowledge-Base Systems, Volume I, Computer Science Press (1988)
    locator: Section 7.3 (reasoning about functional dependencies, keys and equivalence of sets of dependencies)
  - paper: "Catriel Beeri, On the membership problem for functional and multivalued dependencies in relational databases, ACM Transactions on Database Systems 5(3), 241 to 259 (1980)"
    locator: a polynomial algorithm for implication of functional and multivalued dependencies
  - paper: "Marco A. Casanova, Ronald Fagin and Christos H. Papadimitriou, Inclusion dependencies and their interaction with functional dependencies, Journal of Computer and System Sciences 28(1), 29 to 59 (1984)"
    locator: implication of inclusion dependencies is PSPACE-complete
  - paper: "Ashok K. Chandra and Moshe Y. Vardi, The implication problem for functional and inclusion dependencies is undecidable, SIAM Journal on Computing 14(3), 671 to 677 (1985)"
    locator: the undecidability result
---

The dependency implication problem asks whether a set $F$ of dependencies implies a dependency $\sigma$: does each relation that satisfies $F$ also satisfy $\sigma$? For [functional dependencies](/functional-dependency/), the answer comes from one [attribute closure](/attribute-closure-algorithm/), so it takes linear time. Questions about keys are harder: deciding whether a schema has a key of at most $k$ attributes, and whether an attribute is in some key, are [NP-complete](/np-complete/) (Lucchesi and Osborn 1978). For richer classes of dependencies, implication ranges from polynomial to undecidable.

## In plain words

A designer writes down rules such as "the course fixes the teacher". The question is whether some other rule follows from them, so that it need not be stored or checked. For these rules the question is easy: start from the columns on the left of the new rule, find all columns they fix, and see whether the right side is among them. A harder question is about keys, the smallest sets of columns that fix all the others. A schema can have very many keys. Finding whether a small key exists is as hard as the hardest search problems in NP.

## Definition

**Implication.** Let $U$ be a finite attribute set, $F$ a set of dependencies over $U$ and $\sigma$ one more dependency. $F \models \sigma$ if each relation over $U$ that satisfies $F$ satisfies $\sigma$. $F \models_{\mathrm{fin}} \sigma$ is the same with finite relations only.

**FD implication.** For FDs, the input is $U$, $F$ and $X \to Y$, of size $n = |U|$ and $m = \|F\|$, the number of attribute occurrences in $F$. By [Armstrong's axioms](/armstrongs-axioms/),

$$F \models X \to Y \iff Y \subseteq X^+_F,$$

and finite and unrestricted implication coincide, because the counterexample in the completeness proof has two tuples.

**Keys.** $K \subseteq U$ is a *superkey* if $K^+ = U$, and a *key* (candidate key) if it is a superkey and no proper subset is. An attribute is *prime* if it is in some key.

## Variants

| question | input | complexity |
| --- | --- | --- |
| membership: $F \models X \to Y$? | $F$, $X \to Y$ | $O(n + m)$ |
| equivalence: $F^+ = G^+$? | $F$, $G$ | $O(\vert F\vert \cdot (n + \|G\|) + \vert G\vert \cdot (n + \|F\|))$ |
| is $K$ a superkey? | $F$, $K$ | $O(n + m)$ |
| is $K$ a key? | $F$, $K$ | $\vert K\vert + 1$ closures |
| find one key | $F$ | $n$ closures |
| is there a key of size at most $k$? | $F$, $k$ | NP-complete |
| is $A$ prime? | $F$, $A$ | NP-complete |
| list all keys | $F$ | polynomial in $n$, $\vert F\vert$ and the number of keys |

- **Equivalence.** $F$ and $G$ are *equivalent* if $F^+ = G^+$. Test $G \models V \to W$ for each FD of $F$, and $F \models V \to W$ for each FD of $G$, each with one closure.
- **One key.** Start with $K = U$. For each attribute $A$, if $(K - A)^+ = U$, remove $A$. The result is a key, because the superkey property is monotone: if $K - A$ fails at the time $A$ is tested, then each subset of $K - A$ fails too.
- **Other dependency classes.** Implication of FDs with multivalued dependencies is polynomial (Beeri 1980). Implication of inclusion dependencies is PSPACE-complete (Casanova, Fagin and Papadimitriou 1984). For FDs with inclusion dependencies, both $\models$ and $\models_{\mathrm{fin}}$ are undecidable, and they differ (Chandra and Vardi 1985; Mitchell 1983). The [chase](/chase-algorithm/) decides implication for full dependencies, the class that contains FDs, multivalued and join dependencies.

## Examples

**Membership.** With Ullman's course schema, $U = CTHRSG$ and $F = \{C \to T, HR \to C, HT \to R, CS \to G, HS \to R\}$, $F \models HR \to T$ because $HR^+ = CTHR$, and $F \not\models CS \to H$ because $CS^+ = CTSG$. The only key is $HS$, since $HS^+ = U$ and neither $H$ nor $S$ is a superkey on its own, and no key can omit $H$ or $S$, since no FD has $H$ or $S$ on its right side. So the prime attributes are $H$ and $S$.

**Equivalence.** $\{A \to B, B \to C, A \to C\}$ is equivalent to $\{A \to B, B \to C\}$: the FD $A \to C$ is implied, because $A^+ = ABC$ under the second set. $\{A \to BC\}$ is not equivalent to $\{A \to B, B \to C\}$: the second set implies $B \to C$, but under the first set $B^+ = B$.

**Two keys.** $U = CSZ$ (city, street, zip) with $F = \{CS \to Z, Z \to C\}$ has the keys $SZ$ and $CS$. All three attributes are prime.

**Many keys.** $U = \{A_1, \ldots, A_n, B_1, \ldots, B_n\}$ with $F = \{A_i \to B_i, B_i \to A_i : 1 \le i \le n\}$ has $2^n$ keys: each key picks $A_i$ or $B_i$ for each $i$. The input has size $\Theta(n)$, so no algorithm lists all keys in polynomial time in the input alone. For $n = 5$ the implementation finds all 32 keys.

## Known algorithms

**Membership and equivalence.** Compute closures with the [attribute closure algorithm](/attribute-closure-algorithm/) of Beeri and Bernstein (1979), in time $O(n + m)$ each.

**All keys: Lucchesi and Osborn (1978).** The algorithm grows a list of keys. A *minimize* step turns a superkey $S$ into a key by dropping attributes, as in "one key" above.

1. Let $\mathcal{K} = [\text{minimize}(U)]$.
2. For each key $K$ of $\mathcal{K}$, in list order, and for each FD $X \to Y$ in $F$: let $S = X \cup (K - Y)$. If no key of $\mathcal{K}$ is a subset of $S$, append $\text{minimize}(S)$ to $\mathcal{K}$.
3. Return $\mathcal{K}$.

$S$ is a superkey: $S^+ \supseteq X \cup (K - Y)$, so it holds $Y$ by $X \to Y$, so it holds $K$, so it is $U$. So each appended set is a key, and it is new, because it is a subset of $S$ while no earlier key is.

*Completeness.* Suppose some key $J$ is not in the final list $\mathcal{K}$. Then no key of $\mathcal{K}$ is a subset of $J$, since keys are minimal. Among the sets $S$ with $J \subseteq S \subseteq U$ that hold no key of $\mathcal{K}$, take a maximal one. $S \ne U$, since $U$ holds the first key. $S$ is a superkey, since it holds $J$, so $S^+ = U \ne S$, and some FD $X \to Y$ in $F$ has $X \subseteq S$ and $Y \not\subseteq S$. Take $A \in Y - S$. By maximality, $S \cup \{A\}$ holds some $K \in \mathcal{K}$, so $K - Y \subseteq K - \{A\} \subseteq S$, and $X \cup (K - Y) \subseteq S$. When the algorithm processed $K$ with $X \to Y$, it made sure that a key of $\mathcal{K}$ is a subset of $X \cup (K - Y)$, so also of $S$. This contradicts the choice of $S$. $\square$

*Cost.* With $k$ keys, the algorithm handles $k \cdot |F|$ pairs. Each pair costs $O(kn)$ for the subset tests, and at most one minimize step of $n$ closures, $O(n(n + m))$. The total is $O(|F| \cdot k \cdot (kn + n(n + m)))$, polynomial in the input size and $k$. The implementation compares the list with a brute-force search over all $2^n$ subsets on 300 random schemas.

*Trace on $CSZ$.* Minimize $U$, trying $C$, $S$, $Z$ in turn: $SZ^+ = U$, so drop $C$; $Z^+ = CZ$, so keep $S$; $S^+ = S$, so keep $Z$. The first key is $SZ$. For $K = SZ$ and $CS \to Z$, $S = CS \cup (SZ - Z) = CS$, which holds no found key; minimize gives the new key $CS$. For $K = SZ$ and $Z \to C$, $S = SZ$, which holds $SZ$. For $K = CS$, both FDs give $S = CS$ or $S = SZ$, which hold found keys. The output is $[SZ, CS]$.

**Prime attributes.** An attribute is prime if and only if it is in some key, so listing all keys decides it, in time polynomial in the number of keys. A brute-force search tries the subsets of $U$ in order of size.

## Bounds

- Membership for FDs takes $\Theta(n + m)$ time, which is optimal, since each attribute occurrence of $F$ can matter.
- **Key of size at most $k$ is NP-complete** (Lucchesi and Osborn 1978). It is in NP: guess $K$ with $|K| \le k$ and check $K^+ = U$ in linear time.
- **Prime attribute is NP-complete** (Lucchesi and Osborn 1978). It is in NP: guess a set $K$ that holds $A$, and check that it is a superkey and that no $K - B$ is a superkey, with $|K| + 1$ closures.
- The number of keys can be $2^{n/2}$, as in the example above, so listing all keys takes exponential time in the worst case. The Lucchesi and Osborn algorithm is polynomial in the input plus the output.
- For FDs with inclusion dependencies, implication is undecidable (Chandra and Vardi 1985).

## Reductions

**From [vertex cover](/vertex-cover/) to a key of size at most $k$.** This reduction shows NP-hardness in a short way. It is a reduction written for this page; Lucchesi and Osborn give their own proof. Let $G = (V, E)$ be a graph. Use one attribute for each vertex and one attribute $a_e$ for each edge, so $U = V \cup \{a_e : e \in E\}$. Let $F$ have $u \to a_e$ and $v \to a_e$ for each edge $e = \{u, v\}$, and one FD $\{a_e : e \in E\} \to V$.

*Claim: $G$ has a vertex cover of size $k$ if and only if $(U, F)$ has a superkey of size $k$.* If $C$ is a vertex cover, then $C^+$ holds each $a_e$, through an endpoint in $C$, and then all of $V$. So $C$ is a superkey. Conversely, let $K$ be a superkey. Replace each $a_e \in K$ by one endpoint of $e$. The new set $K'$ is a superkey, because the endpoint gives $a_e$, and $|K'| \le |K|$, and $K' \subseteq V$. If an edge $e = \{u, v\}$ had $u, v \notin K'$, then $a_e$ could enter $K'^+$ only through $u$ or $v$, and they enter only through the last FD, which needs $a_e$ first. So $K'^+ \ne U$, a contradiction. So $K'$ is a vertex cover of size at most $|K|$. A superkey of size $k$ holds a key of size at most $k$, so "a key of size at most $k$" has the same answer. The reduction takes linear time, and the implementation checks on 60 random graphs that the smallest key size equals the smallest vertex cover size.

**To Horn logic.** FD implication is propositional Horn implication: each FD $A_1 \cdots A_k \to B$ is the [Horn clause](/horn-clause/) $A_1 \wedge \cdots \wedge A_k \Rightarrow B$, and $F \models X \to B$ if and only if the clauses with the facts $X$ imply $B$. Each Horn implication reduces back to FD implication in linear time. See [Horn-SAT](/horn-sat/).

**Keys as hitting sets.** The keys of $(U, F)$ are the minimal transversals of a [hypergraph](/hypergraph/): a set is a superkey if and only if it meets the complement of each closed set other than $U$. So listing the keys is a minimal [hitting set](/hitting-set/) problem, given the maximal closed sets.

## Applications

- **Normal form tests.** [Third normal form](/third-normal-form/) asks whether each right-side attribute of a violation is prime, so testing 3NF is NP-complete too (Jou and Fischer 1982). [Boyce-Codd normal form](/boyce-codd-normal-form/) needs only superkey tests on the given FDs, so it takes polynomial time for a schema with its own FDs.
- **Covers.** A [minimal cover](/minimal-cover-problem/) is built from membership tests: an FD is redundant if the rest of the set implies it.
- **Schema design tools.** Design tools list keys and prime attributes, and they warn when the number of keys is large.
- **Query optimization.** An optimizer uses FD implication to remove redundant grouping and ordering columns, and key information to remove needless DISTINCT and joins.
- **Query containment.** For conjunctive queries under FDs, containment is decided by the chase, and the chase uses the same idea as FD implication. See the [query containment problem](/query-containment-problem/).

## References
