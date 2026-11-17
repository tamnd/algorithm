---
tag: GAQSFQ
kind: theorem
slug: prime-attribute-np-completeness
name: NP-completeness of the prime attribute problem
aliases:
- prime attribute problem
area: databases/relational-theory
level: advanced
summary: "Deciding whether an attribute belongs to some candidate key of a schema with functional dependencies is NP-complete (Lucchesi and Osborn 1978). Finding one key is easy."
prereqs: [candidate-key, np-complete, dependency-implication-problem]
see_also: [third-normal-form, attribute-closure-algorithm, sat, 3-sat, vertex-cover, strongly-connected-components, polynomial-time-reduction, cook-levin-theorem]
sources:
  - paper: doi:10.1016/0022-0000(78)90009-0
    title: Cláudio L. Lucchesi and Sylvia L. Osborn, Candidate keys for relations, Journal of Computer and System Sciences 17(2), 270 to 279 (1978)
    locator: the NP-completeness of the prime attribute problem and of a key of bounded size, and the algorithm that lists all keys
  - paper: "Jieh Hsiang Jou and Patrick C. Fischer, The complexity of recognizing 3NF relation schemes, Information Processing Letters 14(4), 187 to 190 (1982)"
    locator: testing whether a schema is in 3NF is NP-complete
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman (1979)
    locator: Appendix A, the list of storage and retrieval problems, the prime attribute name problem
  - book: isbn:9780201537710
    title: Serge Abiteboul, Richard Hull and Victor Vianu, Foundations of Databases, Addison-Wesley (1995)
    locator: Chapter 11 (design and dependencies), keys, prime attributes and third normal form
---

A *prime attribute* of a schema is an attribute that is in at least one [candidate key](/candidate-key/). This page proves that deciding whether a given attribute is prime is NP-complete, a result of Lucchesi and Osborn (1978). The [attribute closure algorithm](/attribute-closure-algorithm/) tests in linear time whether a set is a superkey, and the [dependency implication problem](/dependency-implication-problem/) page uses it to find one key and to list all keys. The difficulty here is different: there can be very many keys, and the question is whether any of them holds the attribute. The test for [third normal form](/third-normal-form/) asks exactly this kind of question.

## Statement

**PRIME ATTRIBUTE.** *Input:* a finite set $U$ of attributes, a finite set $F$ of functional dependencies (FDs) over $U$ and an attribute $A \in U$. *Question:* is there a candidate key $K$ of $U$ under $F$ with $A \in K$? A *candidate key* is a set $K \subseteq U$ with $K^+ = U$ such that no proper subset of $K$ has this property, where $K^+$ is the closure of $K$ under $F$. The input size is $|U|$ plus the total number of attribute occurrences in $F$.

**Theorem (Lucchesi and Osborn 1978).** PRIME ATTRIBUTE is NP-complete.

## In plain words

A key of a table is a smallest group of columns that tells you every other column. Usually a table has only a few keys, but the rules about columns can make the number of keys grow very fast with the number of columns.

The question here is simple to state: does at least one key use this column? Checking a proposed key is quick. Finding out whether one exists, among possibly very many keys, is as hard as solving a logic puzzle with true and false values in which every clause must be satisfied. So no fast general method is known, and if one existed, all such puzzles would be easy.

Some special cases are still easy, for example when each rule has one column on its left side.

## Proof

**Lemma 1.** $A$ is prime if and only if there is a set $X \subseteq U - \{A\}$ with $A \notin X^+$ and $(X \cup \{A\})^+ = U$.

*Proof.* *Only if.* Let $K$ be a key with $A \in K$, and let $X = K - \{A\}$. Then $(X \cup \{A\})^+ = K^+ = U$. If $A \in X^+$, then $X^+ \supseteq K$, so $X^+ = U$ and $X$ is a superkey, which contradicts the minimality of $K$. So $A \notin X^+$. *If.* $X \cup \{A\}$ is a superkey, so it contains a key $K$. If $A \notin K$, then $K \subseteq X$, so $X^+ \supseteq K^+ = U \ni A$, a contradiction. So $A \in K$. $\square$

**Membership in NP.** A certificate is the set $X$ of Lemma 1. Two attribute closures check it, each in time linear in the input. So PRIME ATTRIBUTE is in NP.

**NP-hardness.** We reduce CNF [satisfiability](/sat/) to PRIME ATTRIBUTE. The reduction below is a direct one written for this page; the original paper may use another one. Let $\varphi$ have the variables $x_1, \ldots, x_n$ and the clauses $C_1, \ldots, C_m$. For a literal $\ell$ write $\bar\ell$ for its attribute of falsity: $\bar\ell = N_i$ if $\ell = x_i$, and $\bar\ell = P_i$ if $\ell = \neg x_i$. Let $U = \{A, P_1, \ldots, P_n, N_1, \ldots, N_n\}$, where $P_i$ stands for "$x_i$ is true" and $N_i$ for "$x_i$ is false", and let $F$ hold:

- (f1) $P_i N_i \to A$ for each $i$;
- (f2) $\{\bar\ell : \ell \in C_j\} \to A$ for each clause $C_j$;
- (f3) $A P_i \to N_i$ and $A N_i \to P_i$ for each $i$.

The size of $(U, F)$ is linear in the size of $\varphi$. We show that $A$ is prime if and only if $\varphi$ is satisfiable.

*If $\varphi$ is satisfiable.* Let $\beta$ satisfy $\varphi$ and let $X$ hold $P_i$ if $\beta(x_i)$ is true and $N_i$ otherwise. No FD of (f1) applies to $X$, since $X$ holds one of $P_i, N_i$ for each $i$. No FD of (f2) applies: $C_j$ has a literal $\ell$ that is true under $\beta$, and then $\bar\ell \notin X$. No FD of (f3) applies without $A$. So $X^+ = X$ and $A \notin X^+$. From $X \cup \{A\}$, the FDs of (f3) add the missing one of $P_i, N_i$ for each $i$, so $(X \cup \{A\})^+ = U$. By Lemma 1, $A$ is prime.

*If $A$ is prime.* Take $X$ as in Lemma 1. Only the FDs of (f3) have $P_i$ or $N_i$ on the right, and each needs the other one of the pair on the left. So if $X$ held neither $P_i$ nor $N_i$, neither would be in $(X \cup \{A\})^+$, which is $U$. So $X$ holds at least one of them. It does not hold both, or (f1) would put $A$ in $X^+$. Let $\beta(x_i)$ be true exactly when $P_i \in X$. For each clause $C_j$, the FD (f2) does not apply to $X$, because $A \notin X^+$, so some $\ell \in C_j$ has $\bar\ell \notin X$. If $\ell = x_i$, then $N_i \notin X$, so $P_i \in X$ and $\ell$ is true. If $\ell = \neg x_i$, then $P_i \notin X$ and $\ell$ is true. So $\beta$ satisfies $\varphi$. $\square$

An empty clause gives the FD $\emptyset \to A$, so $A \in X^+$ for every $X$ and $A$ is not prime, which agrees with $\varphi$ being unsatisfiable. If each clause has at most three literals, every left side has at most three attributes, so the problem stays NP-complete with left sides of size at most 3.

**Example.** Let $\varphi = (x_1 \lor x_2) \land \neg x_1$. Then $F = \{P_1 N_1 \to A,\ P_2 N_2 \to A,\ N_1 N_2 \to A,\ P_1 \to A\} \cup$ (f3). The keys are $P_1 P_2$, $P_1 N_2$, $N_1 N_2$ and $A N_1 P_2$. The only key with $A$ is $A N_1 P_2$, and it encodes the only satisfying assignment, $x_1$ false and $x_2$ true. For $\varphi = x_1 \land \neg x_1$ the keys are $P_1$ and $N_1$, and $A$ is in neither.

## Consequences

- **Non-prime is coNP-complete.** Deciding whether $A$ is in no key is the complement, so it is coNP-complete.
- **A key of bounded size.** Deciding whether there is a key with at most $k$ attributes is also NP-complete (Lucchesi and Osborn 1978). The reduction from [vertex cover](/vertex-cover/) is on the [dependency implication problem](/dependency-implication-problem/) page.
- **Third normal form.** A schema is in 3NF when, for each FD $X \to A$ of $F$ with $X$ not a superkey and $A \notin X$, the attribute $A$ is prime. A certificate of one key for each such FD shows that 3NF testing is in NP. NP-hardness of 3NF testing does not follow directly from the theorem, because a 3NF test asks many prime questions about one fixed schema. Jou and Fischer (1982) proved it separately. Testing BCNF against the given FDs needs no keys and is polynomial.
- **Rule of thumb: few keys.** Lucchesi and Osborn list all keys in time polynomial in the size of the input and the number of keys. When a schema has few keys, as most real schemas do, the prime attributes are found quickly.

**Easy cases.** These can be decided in polynomial time.

- $A$ is in *every* key exactly when $U - \{A\}$ is not a superkey. If $U - \{A\}$ is a superkey, it contains a key without $A$. If it is not, no key avoids $A$.
- If $A$ is on the right side of no FD, except FDs that also have $A$ on the left, then $A$ is in every key, because no set without $A$ can derive it.
- If $A$ is on the left side of no FD and on the right side of an FD whose left side does not contain $A$, then $A$ is in no key. For a key $K \ni A$, the set $K - \{A\}$ derives everything that $K$ derives except perhaps $A$, since $A$ helps no FD, and then it also derives $A$.
- If every FD has one attribute on its left side, draw an edge from $B$ to $C$ for each FD $B \to C$. The closure of a set is the set of nodes it can reach. A key takes one node from each source component of the [strongly connected components](/strongly-connected-components/), so $A$ is prime exactly when its component has no edge entering it from another component.

## Tightness

- **Left sides of size 1 are easy.** The last easy case shows that the problem is in polynomial time when all left sides are single attributes. The reduction above uses left sides of size 2 in (f1) and (f3) and of the clause size in (f2).
- **Fixed schemas are easy.** For a fixed number of attributes, there are $2^{|U|}$ candidate sets, and each is checked with one closure. The hardness is in the size of $U$.
- **One key versus all keys.** Finding *some* key is polynomial: start from $U$ and drop each attribute whose removal keeps a superkey. Whether a *chosen* attribute can be kept in a key is the hard part.

## History

Lucchesi and Osborn (1978) studied the keys of a relation schema. They gave the algorithm that lists all keys with time polynomial in the input and the output, and proved that the prime attribute problem and the problem of a key of bounded size are NP-complete. Garey and Johnson (1979) included the prime attribute problem in their list of NP-complete problems. Jou and Fischer (1982) proved that 3NF testing is NP-complete, which shows that the design theory based on prime attributes is hard to test in the worst case, while BCNF against the given FDs is easy to test.

## References
