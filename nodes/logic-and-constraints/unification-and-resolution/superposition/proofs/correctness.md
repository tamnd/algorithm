---
title: Superposition is sound, stops on ground input, and is refutation complete by the theorem of Bachmair and Ganzinger
proves: [correctness, termination]
status: sketch
---

We use the pseudocode of the page and the Knuth-Bendix ordering $\succ$ of the code, with every weight 1 and a total precedence. An **E-interpretation** is an interpretation in which $=$ is the identity on the domain. In the code a clause is a set of literals, and $s = t$ and $t = s$ are the same literal.

**Theorem.**

1. If the loop returns UNSAT, then $S$ is E-unsatisfiable.
2. If every clause of $S$ is ground, the loop stops without the limit at line L12.
3. Suppose there is no limit and $S$ is E-unsatisfiable. Then the loop returns UNSAT.

Parts 1 and 2 are proved in full below. Part 3 is the completeness theorem of Bachmair and Ganzinger. We state it, outline its proof, and show how the loop meets its conditions, but we do not give every detail.

## Part 1: soundness

We show that every rule gives a clause that is true in every E-model of its premises. Fix an E-interpretation $E$ and an assignment $\theta$ of domain elements to the variables of the conclusion. A premise is true under every assignment, so its instance under $\sigma$ is true under $\theta$.

- **Superposition.** The premises are $C \vee l = r$ and $D \vee L[u]$ with $u\sigma = l\sigma$. If a literal of $C\sigma$ or $D\sigma$ is true, the conclusion is true. Otherwise $l\sigma = r\sigma$ is true and $L[u]\sigma$ is true. Then $u\sigma$ and $r\sigma$ have the same value. Since $E$ interprets $=$ as the identity, a term and the term with one subterm replaced by a term of the same value have the same value, by induction on the term. So the sides of $L[r]\sigma$ have the same values as the sides of $L[u]\sigma$, and $L[r]\sigma$ is true.
- **Equality resolution.** The instance $C\sigma \vee s\sigma \ne s\sigma$ of the premise is true, and $s\sigma \ne s\sigma$ is false in $E$. So $C\sigma$ is true.
- **Equality factoring.** The instance is $C\sigma \vee s\sigma = t\sigma \vee s\sigma = t'\sigma$, since $s\sigma = s'\sigma$. If $t\sigma \ne t'\sigma$ is true, the conclusion is true. Otherwise $t\sigma$ and $t'\sigma$ have the same value. If $s\sigma = t\sigma$ is true, then $s\sigma = t'\sigma$ is true, and this is the literal $(s' = t')\sigma$ of the conclusion. In the other cases a literal of $C\sigma$ or $(s' = t')\sigma$ is true.
- **Demodulation at line L4.** A step replaces $l\theta$ by $r\theta$ in the given clause, with an active unit $l = r$. This is a superposition step with the matcher $\theta$ in place of $\sigma$, so the argument of the first case applies. A chain of steps is sound by induction.
- **Set form.** Merging two equal literals into one keeps the truth value of a clause.

By induction on the order in which clauses are stored, every stored clause is true in every E-model of $S$. Line L5 returns UNSAT only when the clause $\square$ is stored, and $\square$ is false in every interpretation. So $S$ has no E-model. The deletions at lines L6 and L7 only remove clauses, and they do not affect this argument.

## Part 2: termination on ground input

Let every clause of $S$ be ground, let $\Sigma$ be the finite set of function symbols in $S$, and let $W$ be the largest number of symbols in a side of a literal of $S$.

*Step 1: ground KBO and size.* For ground terms $s$ and $t$ with $s \succ t$, the code compares sizes first, so $|s| \ge |t|$.

*Step 2: no new variables and no new symbols.* The unifier of two ground terms is empty or does not exist, and the matcher of a ground instance of a ground unit is empty. Every rule builds its conclusion from subterms of its premises. So every stored clause is ground and uses only symbols of $\Sigma$.

*Step 3: every side of a stored clause has at most $W$ symbols.* By induction on the order in which clauses are stored. Equality resolution deletes a literal. Equality factoring forms the literals $t \ne t'$ and $s' = t'$, whose sides are sides of the premise. Superposition replaces $l$ by $r$ inside a side $s[l]$ of a premise, and the step requires $r \not\succeq l$. The ordering is total on ground terms, so $l \succ r$ and $|r| \le |l|$ by Step 1, hence $|s[r]| \le |s[l]| \le W$. A demodulation step needs $l\theta \succ r\theta$, and the same argument applies. The other literals of a conclusion are literals of the premises.

*Step 4: finitely many clauses.* Let $m$ be the number of ground terms over $\Sigma$ with at most $W$ symbols. This number is finite, since there are finitely many strings of length at most $W$ over the finite alphabet $\Sigma$. A literal is a sign and an unordered pair of such terms, so there are at most $m(m+1)$ literals. A clause is a set of literals, so there are at most $2^{m(m+1)}$ clauses.

*Step 5: the loop stops.* The function `add` of the code stores a clause only if it was not stored before, at lines L1, L4 and L11. So the store holds at most $2^{m(m+1)}$ clauses. Each pass of the loop marks one more stored clause as taken at line L3, and the loop stops when every stored clause is taken. So there are at most $2^{m(m+1)}$ passes.

Each pass also stops. Line L4 rewrites one side at a time, and each step makes the side strictly smaller in $\succ$. All the sides that appear have at most $W$ symbols, by Step 3. A strictly decreasing chain in a finite set of terms has no repeated term, because $\succ$ is a strict ordering (irreflexive and transitive), so the chain is finite. Lines L6 to L11 do finitely many operations on finite clauses. $\blacksquare$ for parts 1 and 2.

## Part 3: the theorem of Bachmair and Ganzinger

Let $\mathrm{gnd}(N)$ be the set of ground instances of the clauses of $N$. Extend $\succ$ to literals as on the page and to clauses by the multiset extension. A ground clause $D$ is **redundant** in $N$ if $D$ follows from clauses of $\mathrm{gnd}(N)$ that are smaller than $D$. A clause is redundant if all its ground instances are. A ground inference is redundant if its conclusion follows from clauses of $\mathrm{gnd}(N)$ that are smaller than its largest premise. $N$ is **saturated up to redundancy** if every inference from clauses of $N$ is redundant in $N$.

**Theorem (Bachmair and Ganzinger 1990, 1994).** Let $\succ$ be a reduction ordering that is total on ground terms. If $N$ is saturated up to redundancy and does not contain $\square$, then $N$ has an E-model.

*Outline.* The proof builds a ground rewrite system $R$ by induction on $\mathrm{gnd}(N)$ in increasing order. A ground clause $C \vee s = t$ **produces** the rule $s \to t$ when it is false in the rules built so far, $s = t$ is strictly maximal in it, $s \succ t$, $s$ is irreducible by the rules so far, and $C$ is false in the rules so far together with $s \to t$. Every rule of $R$ goes down in $\succ$, so $R$ terminates. No left side of a rule is reducible by another rule, so $R$ has no critical pairs and is confluent. So the relation "has the same normal form in $R$" is a congruence and defines an E-interpretation $I$. Suppose some clause of $\mathrm{gnd}(N)$ is false in $I$ and take the smallest one, $D$. A case analysis on the maximal literal of $D$ gives a ground inference with $D$ as a premise whose conclusion is smaller than $D$ and false in $I$: superposition with a productive clause when the larger side of the maximal literal is reducible by $R$, equality resolution when the maximal literal is $s \ne s'$ with equal normal forms, and equality factoring when $D$ fails to produce only because of a second positive literal with the same larger side. This inference is redundant, so its conclusion follows from smaller clauses, which are all true in $I$ by the choice of $D$. That is a contradiction. The ground inferences lift to inferences on $N$ because $\succ$ is stable under substitution. A step into a position below a variable is not needed, because the instance of the variable can be taken in normal form first. The full proof is in the 1994 paper of Bachmair and Ganzinger and in Chapter 7 of the Handbook of Automated Reasoning.

*How the loop meets the conditions, assuming no limit.*

- **The ordering.** The code's KBO is a reduction ordering, and it is total on ground terms because the precedence is total.
- **Deletions are redundancy deletions.** A tautology is true in every E-interpretation, so it follows from the empty set. Suppose line L6 or L7 deletes $D$ because $C\rho$ is part of $D$ in the multiset sense. If $C\rho$ has fewer literals than $D$, every ground instance $D\tau$ follows from the smaller clause $C\rho\tau$, so $D$ is redundant. Otherwise $C\rho$ is $D$ up to the order of literals, and every ground instance of $D$ is a ground instance of $C$, which stays. Line L4 deletes the clause $G$ when it rewrites it to $G'$. A step needs $l\theta \succ r\theta$ and $L \succ (l = r)\theta$. Then $G$ follows from $G'$ and $(l = r)\theta$, and both are smaller than $G$, so $G$ is redundant. The rewritten clause $G'$ is stored.
- **Fairness.** Line L3 takes the oldest untaken clause at every $k$-th pick, so every stored clause is taken at some time, as in the proof for [paramodulation](/paramodulation/). When a clause is taken and kept, lines L9 and L10 form every inference between it and each clause of active, a renamed copy of itself included. A kept clause that later leaves active at line L7 is redundant from then on.

The step that we do not prove here is the general result that the clauses that persist in a fair run of this kind form a set saturated up to redundancy, together with the fact that redundancy is kept when more clauses are added or redundant ones deleted. Both are in the 1994 paper, where saturation is reached by fair theorem proving derivations. With them, if $S$ is E-unsatisfiable and the loop never returned UNSAT, the persisting clauses would form a saturated set without $\square$ that is E-equivalent to $S$, and the theorem would give an E-model of $S$, a contradiction. $\blacksquare$
