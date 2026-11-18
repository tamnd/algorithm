---
title: The inverse rules program computes the certain answers of a Datalog query over conjunctive views
proves: [correctness, termination, time.worst]
status: full
---

**Setting.** The global schema has predicates $p_1, p_2, \ldots$. Each view is $V(\bar Y) \text{ :- } p_1(\bar u_1), \ldots, p_r(\bar u_r)$, a conjunctive query over the global schema whose head has distinct variables and no constants. The query $Q$ is a Datalog program with safe rules, no constants and a goal predicate. Its derived predicates are not global predicates or view names. A view instance $I$ gives a finite set $I(V)$ of tuples of constants for each view. Set semantics holds. Under the open world assumption, a global database $D$ is *possible* for $I$ if $I(V) \subseteq V(D)$ for each view $V$. The *certain answers* are the tuples of constants $\bar t$ with $\bar t \in Q(D)$ for every possible $D$.

For a view $V$ and an existential variable $u$ of $V$, line L3 uses the function symbol $f_{V,u}$. The term $f_{V,u}(\bar t)$ for a tuple $\bar t \in I(V)$ is treated as a new value. Two such terms are equal only if they have the same symbol and the same arguments, and no term equals a constant.

Let $D_0$ be the set of global facts $p_j(\sigma_{\bar t}(\bar u_j))$, over all views $V$, all $\bar t \in I(V)$ and all atoms $p_j(\bar u_j)$ of $V$, where $\sigma_{\bar t}$ sends $Y_p$ to $t_p$ and each existential $u$ to $f_{V,u}(\bar t)$.

**Lemma 1 (the inverse rules derive $D_0$).** The least model of the program of line L6 on $I$ is $I \cup D_0 \cup M$, where $M$ is the set of facts of the derived predicates of $Q$ in the least model of $Q$ on $D_0$.

*Proof.* The rules of lines L1 to L5 have one view atom in the body and a global atom in the head. A body match is a tuple $\bar t \in I(V)$, and the head is then $p_j(\sigma_{\bar t}(\bar u_j))$. No rule has a view name in its head, so the view facts stay $I$, and the inverse rules derive exactly $D_0$. The rules of $Q$ have no global predicate in their heads, so the global facts are exactly $D_0$, and the facts of the derived predicates are those of the least model of $Q$ on $D_0$. $\square$

**Lemma 2 ($D_0$ is possible).** If each function term is read as a value of its own, $D_0$ is a possible database for $I$.

*Proof.* For $\bar t \in I(V)$, the map $\sigma_{\bar t}$ sends each atom of the body of $V$ to a fact of $D_0$ and sends the head $\bar Y$ to $\bar t$. So $\bar t \in V(D_0)$. $\square$

**Lemma 3 ($D_0$ maps into each possible database).** For each possible $D$ there is a map $h$ from the values of $D_0$ to the values of $D$ that is the identity on constants and sends each fact of $D_0$ to a fact of $D$.

*Proof.* For each view $V$ and $\bar t \in I(V)$, we have $\bar t \in V(D)$, so there is a valuation $\mu_{\bar t}$ of the variables of $V$ that sends the body into $D$ and $\bar Y$ to $\bar t$. Set $h(f_{V,u}(\bar t)) = \mu_{\bar t}(u)$ and let $h$ fix constants. This is well defined, because different pairs $(V, u, \bar t)$ give different terms. Then $h(\sigma_{\bar t}(w)) = \mu_{\bar t}(w)$ for each variable $w$ of $V$, so $h$ sends the fact $p_j(\sigma_{\bar t}(\bar u_j))$ to $p_j(\mu_{\bar t}(\bar u_j))$, a fact of $D$. $\square$

**Lemma 4 (Datalog is preserved under homomorphisms).** If $h$ fixes constants and sends each fact of $A$ to a fact of $B$, then $h(\bar s) \in Q(B)$ for each $\bar s \in Q(A)$.

*Proof.* By induction on the stage of the least fixpoint at which a fact of $Q$ on $A$ appears. A fact derived by a rule with a body match $\nu$ on the model of $A$ gives the match $h \circ \nu$ on the model of $B$, by the induction hypothesis for the body facts, since the rules have no constants and no negation. The head of $h \circ \nu$ is $h$ of the head of $\nu$. $\square$

**Theorem (Duschka and Genesereth).** INVERSE-RULES stops, and its output is the set of certain answers of $Q$ on $I$ under the open world assumption.

*Proof.* *Termination.* Each function term has constants of $I$ as arguments, so $D_0$ is finite, and the rules of $Q$ create no new values. So the fixpoint of line L7 has a finite set of possible facts, and each round of the naive iteration that does not stop adds one.

*Output is certain.* Let $\bar t$ be a tuple of line L8: a goal fact of the least model, with no function term. By Lemma 1, $\bar t \in Q(D_0)$. Let $D$ be possible and $h$ as in Lemma 3. By Lemma 4, $h(\bar t) \in Q(D)$, and $h(\bar t) = \bar t$, since $\bar t$ holds only constants.

*Every certain answer is output.* Let $\bar t$ be certain. By Lemma 2, $D_0$ is possible, so $\bar t \in Q(D_0)$, a goal fact of the least model by Lemma 1, and $\bar t$ holds only constants, so line L8 keeps it. $\blacksquare$

**Running time.** Fix $Q$ and the views (data complexity). Let $N$ be the number of tuples of $I$, $r$ the largest arity of a predicate and $b$ the largest number of atoms in the body of a rule. Each tuple of $I$ adds a bounded number of function terms, so the model has $O(N)$ values and $O(N^r)$ possible facts. The naive iteration makes at most $O(N^r)$ rounds. In one round, the backtracking match of a rule tries at most one fact per body atom at each level, so it visits $O(N^{r b})$ partial matches, each in $O(1)$ steps for a fixed program. The total is $O(N^{r (b + 1)})$ time and $O(N^r)$ space, polynomial in data complexity.
