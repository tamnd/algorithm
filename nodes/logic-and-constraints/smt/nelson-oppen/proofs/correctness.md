---
title: The Nelson-Oppen theorem, the deterministic method for convex theories, and a counterexample
proves: [correctness, termination]
status: full
---

## Setting

Let $\Sigma_1$ and $\Sigma_2$ be countable signatures with no common symbol other than equality. For $i = 1, 2$, let $T_i$ be a $\Sigma_i$-theory given by a set of first-order axioms. Its class of models is then closed under isomorphism and under elementary substructures. The combination $T_1 \oplus T_2$ is the class of $(\Sigma_1 \cup \Sigma_2)$-structures whose $\Sigma_i$-reduct is a model of $T_i$ for $i = 1, 2$; for axiomatized theories, this is the theory axiomatized by the union of the axioms (Handbook, Section 33.2.1.3). Let $C$ be a set of fresh constants. For a conjunction $\psi$ of literals, $\psi \models_{T} e$ means that every model of $T$ and $\psi$ satisfies $e$.

The input is a pair $\varphi_1, \varphi_2$, where $\varphi_i$ is a conjunction of $(\Sigma_i \cup C)$-literals. Let $S$ be the set of constants that occur in both, the *shared* constants, and $k = |S|$. For an equivalence relation $R$ on $S$, the *arrangement* $\mathrm{ar}_R$ is the conjunction of $c = d$ for $(c, d) \in R$ and of $c \ne d$ for $(c, d) \notin R$, with $c, d \in S$.

**Purification.** If the input is one conjunction $\varphi$ of mixed literals, replace an alien subterm $t$ of a literal with a fresh constant $v$ and add $v = t$, until every literal is pure, then split the literals by signature. Each step keeps satisfiability in both directions: a model of the new formula is a model of the old one, because $v$ and $t$ have the same value, and a model of the old one becomes a model of the new one when $v$ is given the value of $t$. So it is enough to treat pure inputs.

## Theorem 1 (the nondeterministic method)

*If $T_1$ and $T_2$ are stably infinite, then $\varphi_1 \wedge \varphi_2$ is $T_1 \oplus T_2$-satisfiable if and only if there is an equivalence relation $R$ on $S$ such that $\varphi_1 \wedge \mathrm{ar}_R$ is $T_1$-satisfiable and $\varphi_2 \wedge \mathrm{ar}_R$ is $T_2$-satisfiable.*

*Proof.* Only if. Let $B$ be a model of $T_1 \oplus T_2$ and of $\varphi_1 \wedge \varphi_2$. Let $R = \{(c, d) \in S^2 : c^B = d^B\}$. Then $B$ satisfies $\mathrm{ar}_R$. The reduct of $B$ to $\Sigma_i \cup C$ is a model of $T_i$, and it satisfies $\varphi_i \wedge \mathrm{ar}_R$.

If. The formula $\varphi_i \wedge \mathrm{ar}_R$ is ground and $T_i$-satisfiable, so by stable infiniteness it has a model $A_i$ of $T_i$ with an infinite universe. The signature $\Sigma_i \cup C$ is countable, so by the downward Löwenheim-Skolem theorem $A_i$ has a countable elementary substructure. It satisfies the same sentences, among them $\varphi_i \wedge \mathrm{ar}_R$, the axioms of $T_i$, and for each $n$ the sentence "there are at least $n$ elements". So we may take $A_1$ and $A_2$ countably infinite.

Let $X_i = \{c^{A_i} : c \in S\}$. Define $h_0 : X_1 \to X_2$ by $h_0(c^{A_1}) = c^{A_2}$. It is well defined: if $c^{A_1} = d^{A_1}$, then $c = d$ is true in $A_1$, so $(c, d) \in R$, because $A_1$ satisfies $\mathrm{ar}_R$; then $A_2$ also satisfies $c = d$. By the same argument with the roles exchanged, $h_0$ is one to one, and it is onto $X_2$ by its definition. The sets $A_1 \setminus X_1$ and $A_2 \setminus X_2$ are countably infinite, because a finite set was removed from a countably infinite one. So $h_0$ extends to a bijection $h : A_1 \to A_2$.

Define a $(\Sigma_1 \cup \Sigma_2 \cup C)$-structure $B$ with universe $A_2$. Each symbol of $\Sigma_2$ is interpreted as in $A_2$. Each function symbol $g$ of $\Sigma_1$ is interpreted by $g^B(b_1, \ldots, b_n) = h(g^{A_1}(h^{-1}(b_1), \ldots, h^{-1}(b_n)))$, and each predicate symbol $P$ of $\Sigma_1$ by $P^B = h(P^{A_1})$. A constant of $C$ that occurs in $\varphi_2$ is interpreted as in $A_2$, and any other constant $c$ of $C$ as $h(c^{A_1})$. This is well defined because the signatures share no symbol, and because for a shared constant $c$ both rules give the same value, $c^{A_2} = h(c^{A_1})$.

The reduct of $B$ to $\Sigma_2$ and the constants of $\varphi_2$ is $A_2$, so it is a model of $T_2$ and of $\varphi_2$. The map $h$ is an isomorphism from the reduct of $A_1$ to $\Sigma_1$ and the constants of $\varphi_1$ onto the same reduct of $B$, by the definition of $B$; it keeps equality because it is a bijection. Models of $T_1$ are closed under isomorphism, so this reduct of $B$ is a model of $T_1$ and of $\varphi_1$. So $B$ is a model of $T_1 \oplus T_2$ and of $\varphi_1 \wedge \varphi_2$. $\square$

The set $S$ is finite, so there are finitely many equivalence relations on it, and the method that tries them all terminates. This is the function `nelson_oppen_guess` of the implementation.

## Theorem 2 (a counterexample without stable infiniteness)

*The "if" direction of Theorem 1 fails when one theory is not stably infinite.*

*Proof.* Let $T_1$ be EUF with one unary function symbol $f$. Let $T_2$ have the empty signature and the axiom $\forall x\, y\, z.\ x = y \vee x = z \vee y = z$, so its models have one or two elements. Let $\varphi_1 = f(a) \ne f(b) \wedge f(a) \ne f(c) \wedge f(b) \ne f(c)$ and let $\varphi_2$ be the empty conjunction. No constant is shared, so the only arrangement is empty. $\varphi_1$ is $T_1$-satisfiable, with $f$ the identity on three elements, and $\varphi_2$ is $T_2$-satisfiable. So the condition of Theorem 1 holds. But a model of $T_1 \oplus T_2$ has at most two elements, and $\varphi_1$ needs three distinct values $f(a)$, $f(b)$, $f(c)$. So $\varphi_1 \wedge \varphi_2$ is unsatisfiable in $T_1 \oplus T_2$. The theory $T_2$ is not stably infinite, because the satisfiable ground formula $a = a$ has no infinite model of $T_2$. $\square$

## Theorem 3 (the deterministic method for convex theories)

Consider the procedure of the page without lines L8 to L10: it checks each side (line L3), sends single entailed equalities between shared constants (lines L4 and L5), and answers SAT when there is none left to send.

*If $T_1$ and $T_2$ are convex and stably infinite, this procedure terminates after at most $2(k - 1)$ added equalities, and its answer is correct.*

*Proof.* Write $\varphi_1, \varphi_2$ for the current conjunctions and $R_i = \{(c, d) \in S^2 : \varphi_i \models_{T_i} c = d\}$. Each $R_i$ is an equivalence relation on $S$, because entailment of equalities is reflexive, symmetric and transitive.

*Invariant: the models of $T_1 \oplus T_2$ that satisfy $\varphi_1 \wedge \varphi_2$ never change.* Line L5 adds to $\varphi_j$ an equality $c = d$ with $\varphi_i \models_{T_i} c = d$. Let $B$ be a model of $T_1 \oplus T_2$ and of $\varphi_1 \wedge \varphi_2$. Its reduct to $\Sigma_i$ and the constants is a model of $T_i$ and of $\varphi_i$, so it satisfies $c = d$, and so does $B$. Adding $c = d$ thus removes no model, and adding a literal adds none.

*UNSAT is correct.* Line L3 returns UNSAT when some $\varphi_i$ has no $T_i$-model. Then $\varphi_1 \wedge \varphi_2$ has no model of $T_1 \oplus T_2$, since its $\Sigma_i$-reduct would be one. By the invariant, neither has the input.

*SAT is correct.* The procedure answers SAT when both sides are satisfiable and no equality is left to send. So every pair in $R_1$ is in $R_2$, and conversely: $R_1 = R_2 = R$. We show that $\varphi_i \wedge \mathrm{ar}_R$ is $T_i$-satisfiable for $i = 1, 2$. Suppose not. The equalities of $\mathrm{ar}_R$ are entailed by $\varphi_i$, so $\varphi_i \wedge \bigwedge_{(c, d) \in N} c \ne d$ is unsatisfiable, where $N = \{(c, d) \in S^2 : (c, d) \notin R\}$. If $N$ is empty, $\varphi_i$ itself is unsatisfiable, which line L3 has excluded. Otherwise $\varphi_i \models_{T_i} \bigvee_{(c, d) \in N} c = d$, and by convexity $\varphi_i \models_{T_i} c = d$ for some $(c, d) \in N$. Then $(c, d) \in R_i = R$, a contradiction. So both conjunctions are satisfiable, and by Theorem 1, $\varphi_1 \wedge \varphi_2$ is $T_1 \oplus T_2$-satisfiable, and by the invariant so is the input.

*Termination.* Literals are only added, so $R_1$ and $R_2$ only grow. Line L5 adds to $\varphi_j$ an equality $c = d$ with $(c, d) \notin R_j$, and after it $(c, d) \in R_j$. So $R_j$ grows strictly, and its number of classes goes down by at least one. Each $R_j$ starts with at most $k$ classes and keeps at least one, so line L5 runs at most $2(k - 1)$ times. Each pass of the loop either returns or runs line L5, so there are at most $2k - 1$ passes. $\square$

Convexity is needed: the formula $1 \le x \wedge x \le 2 \wedge f(x) \ne f(1) \wedge f(x) \ne f(2)$ over the integers with EUF is unsatisfiable, but neither solver entails a single equality between the shared constants, and the procedure answers SAT. The implementation shows this with `method="nosplit"`.

## Theorem 4 (the procedure with case splits)

*If $T_1$ and $T_2$ are stably infinite, the procedure of the page, with lines L8 to L10, terminates, and it answers SAT exactly when $\varphi_1 \wedge \varphi_2$ is $T_1 \oplus T_2$-satisfiable.*

*Proof.* Let $\mu$ be the number of classes of the relation $R_1 \cap R_2$ at the start of a call. We use induction on $\mu$.

The loop of lines L2 to L5 terminates by the termination argument of Theorem 3, which did not use convexity. Its UNSAT answer at line L3 is correct, and it keeps the models of the input, by the same arguments. When the loop stops, $R_1 = R_2 = R$, as in Theorem 3. Line L7 forms the set $D$ of equalities between one member of each pair of classes of $R$, and the arrangement of line L8 consists of the equalities of each constant with the member of its class and the disequalities of $D$. Given the equalities, it is equivalent to $\mathrm{ar}_R$.

*Line L11.* If $D$ is empty, $R$ has one class, $\mathrm{ar}_R$ consists of equalities entailed by both sides, and both sides are satisfiable, so both $\varphi_i \wedge \mathrm{ar}_R$ are satisfiable. If $D$ is not empty, line L11 is reached only when both $\varphi_i \wedge \mathrm{ar}_R$ are satisfiable. In both cases Theorem 1 gives a model, so SAT is correct.

*Lines L9 and L10.* Suppose $\varphi_i \wedge \mathrm{ar}_R$ is unsatisfiable. The equalities of $\mathrm{ar}_R$ are entailed by $\varphi_i$, so $\varphi_i \models_{T_i} \bigvee_{e \in D} e$. Every model of $T_1 \oplus T_2$ and of $\varphi_1 \wedge \varphi_2$ satisfies some $e \in D$. So $\varphi_1 \wedge \varphi_2$ is satisfiable exactly when $\varphi_1 \wedge \varphi_2 \wedge e$ is for some $e \in D$, which is what lines L9 and L10 compute, if the recursive calls are correct. In the call for $e = (c = d)$, both sides entail all pairs of $R$ and the pair $(c, d)$, which joins two classes of $R$. So the new $\mu$ is at most the number of classes of $R$ minus one, and $R \supseteq R_1 \cap R_2$ of the present call, so the new $\mu$ is smaller than the present one. By the induction hypothesis, each recursive call terminates and is correct. There are finitely many calls at line L9, so the present call terminates and is correct.

The base of the induction is $\mu = 1$: then $R$ has one class, $D$ is empty, and the call ends at line L3 or line L11 without recursion. $\square$

For convex theories, line L8 never finds an unsatisfiable side, by the argument of Theorem 3. So with convex theories, the procedure with splits makes exactly the same run as the deterministic one. $\blacksquare$
