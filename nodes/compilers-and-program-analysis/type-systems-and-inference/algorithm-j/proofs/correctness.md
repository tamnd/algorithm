---
title: Algorithm J is sound and complete, and computes the same principal types as W
proves: [correctness, termination]
status: full
---

This file proves that algorithm J is sound and complete for the syntax-directed rules of the [Hindley-Milner type system](/hindley-milner-type-system/), in the same sense as [algorithm W](/algorithm-w/). It follows that J and W return the same principal type for each closed term, up to renaming. Then it proves that generalization by levels quantifies exactly the same variables as generalization by a scan of the context. The proof reuses Lemma 1 (a more general context) and Lemma 2 (type substitution) of the [proof file of algorithm W](/algorithm-w/), and the correctness of unification by the [Martelli-Montanari rules](/martelli-montanari-unification/). Like the W proof, it covers the syntax-directed rules. The equivalence with the declarative rules is in the thesis of Damas (1985).

## The global substitution

J keeps one union-find structure over type variables. A variable is a *root* if it has no parent. A non-root variable points to a variable or to a type with $\to$ or a base type at the top. FIND follows the parents to a root variable or to a non-variable node. The structure has no cycles: L10 links two roots, and L11 links a root $v$ to a type in which, by the occurs check, $v$ does not occur after FIND.

The structure *represents* the substitution $E$ that maps each variable $\alpha$ to the full resolution of $\alpha$: follow FIND, and resolve each child of the node in the same way. Path compression changes the parents but not $E$, because it only replaces a pointer to $u$ by a pointer to FIND$(u)$, which has the same resolution. Union by rank picks which root becomes the child, and both choices represent substitutions that are equal up to a renaming of the two roots. The roots are exactly the variables that $E$ maps to themselves, so $E$ is idempotent: $EE = E$.

**Lemma 3 (unification).** Suppose that UNIFY$(\tau_1, \tau_2)$ starts with the substitution $E$. If $E\tau_1$ and $E\tau_2$ have no unifier, UNIFY fails. Otherwise it stops with a substitution $E' = U E$, where $U$ is a most general unifier of $E\tau_1$ and $E\tau_2$.

*Proof.* Each step of UNIFY is a step of the Martelli-Montanari rules on the equations $E a = E b$ for the pairs $(a, b)$ that are still open. L9 with equal nodes deletes a trivial equation. L12 decomposes an equation between two arrows. L13 is a clash. L10 and L11 eliminate a variable: they bind a root $v$ to a node $t$ in which $v$ does not occur, which composes $E$ with $[v := Et]$. The rules stop, and they fail exactly when there is no unifier. The binding steps compose to a most general unifier $U$ (see the [Martelli-Montanari page](/martelli-montanari-unification/)). The memo table of L12 only skips a pair of nodes that this call has already unified. Types are acyclic, so a pair is never inside its own unification, and when it is met again its two sides are already equal. $\square$

## Soundness and completeness

Write $E_0$ for the substitution when a call $J(\Gamma, e)$ starts, and $E_1$ for the substitution when it returns $\tau$. J never applies $E$ to $\Gamma$. FIND applies it lazily. The judgment that J ensures is $E_1\Gamma \vdash e : E_1\tau$. Fresh variables, and the variables that a call *creates*, are as in the W proof.

Each call only composes $E$ with more bindings, so $E_1 = S E_0$ for a substitution $S$, the *change* made by the call. For classic generalization, GEN at L8 quantifies the variables of $E\tau_1$ that are not free in $E\Gamma$. This is $\mathrm{Gen}(E\Gamma, E\tau_1)$. For levels it is the same set, by Lemma 4 below.

**Theorem 1 (soundness).** If $J(\Gamma, e)$ returns $\tau$ and leaves the substitution $E_1$, then $E_1\Gamma \vdash e : E_1\tau$.

**Theorem 2 (completeness).** If $R E_0 \Gamma \vdash e : \tau'$ for a substitution $R$, then $J(\Gamma, e)$ succeeds with $\tau$ and $E_1$, and there is a substitution $R'$ with $R'E_1\tau = \tau'$ and $R'E_1\alpha = RE_0\alpha$ for each variable $\alpha$ that the call did not create.

*Proof of both.* The proof is the proof of Theorems 1 and 2 for W, with $W(E_0\Gamma, e) = (S, E_1\tau)$ where $S$ is the change of the call. Each case of J makes the same calls in the same order as W on $E_0\Gamma$, and makes the same changes.

- *Variable* (L1, L2). The copy has the bound variables replaced by fresh variables, and it shares the other nodes with the scheme. Its resolution is $[\vec\alpha := \vec\beta]$ applied to the resolved scheme body. This is the result of W, with the identity change.
- *Abstraction* (L3, L4). The context of the inner call is $\Gamma, x : \beta$. The result $\beta \to \tau_1$ resolves to $S_1\beta \to E_1\tau_1$, which is the result of W.
- *Application* (L5, L6). The first call has change $S_1$. The second call starts with $S_1E_0$, so it sees the context $S_1E_0\Gamma$, which is the context of the second call of W. By Lemma 3, UNIFY$(\tau_1, \tau_2 \to \beta)$ composes the substitution with an mgu $S_3$ of $S_2S_1E_0\tau_1$ and $E\tau_2 \to \beta$. These are the two types of line L8 of W. The total change is $S_3S_2S_1$, and $\beta$ resolves to $S_3\beta$.
- *Let* (L7, L8). After the first call, GEN quantifies the variables of $\mathrm{Gen}(S_1E_0\Gamma, E\tau_1)$, which is the scheme of W at its line L11. The scheme is stored unresolved in the context, but its free variables resolve with the current $E$, as W applies $S_2$ to the context.

In each case the soundness and completeness arguments of the W proof apply word for word, with $E_1\tau$ in place of the type that W returns. $\square$

**Corollary (J computes principal types).** For a closed term $e$, J succeeds exactly when $e$ has a type, and then $E_1\tau$ is a principal type of $e$. So J and W return the same type up to a renaming of type variables.

*Proof.* As for W: by Theorem 2 each type of $e$ is an instance of $E_1\tau$, and by Theorem 1 and Lemma 2 each instance is a type. Two principal types are instances of each other, so they differ by a renaming. $\square$

## Levels

In the mode with levels, J keeps a counter *depth*, the number of `let` definitions that the current point is inside. A fresh variable gets the current depth as its level. L10 gives the new root the smaller level of the two roots. L11 calls OCCURS-ADJUST, which lowers the level of each variable in $t$ to at most the level of $v$. GEN at depth $d$ quantifies the variables of $E\tau_1$ with level greater than $d$.

**Lemma 4.** At L8, at depth $d$, a root variable $u$ of $E\tau_1$ has level greater than $d$ if and only if $u$ is not free in $E\Gamma$.

*Proof.* Consider a call $J(\Gamma, e)$ at depth $d$. We show two invariants. They hold for each call, by induction on the run.

(A) Each root variable that is free in $E\Gamma$ has a level of at most $d$. When a variable enters the context at L3, its level is the current depth. When a scheme enters at L8, its free variables are free in $E\Gamma$ already. If unification binds a root $v$ that is free in $E\Gamma$ to a node $t$, the new free variables of $E\Gamma$ are the variables of $Et$, and L11 lowers each of them to the level of $v$, which is at most $d$. If L10 links two roots, the new root gets the smaller level. Levels never go up.

(B) During the call, each root variable that occurs in the resolution of a type the call handles is either free in $E\Gamma$ or was created by the call. The call reads old types only through $\Gamma$. Unification keeps this set closed: a binding of a variable that is free in $E\Gamma$ makes the variables of the bound type free in $E\Gamma$, and a binding of a created variable only adds created or free variables to it.

Now take a root $u$ of $E\tau_1$ at L8. If $u$ is free in $E\Gamma$, its level is at most $d$ by (A). If $u$ is not free in $E\Gamma$, then by (B) for the inner call it was created by that call, at a depth of at least $d + 1$, so it started with a level greater than $d$. Its level is lowered only by L10 or L11, and only to the level of a variable in the same binding. If that level were at most $d$, the variable would be old for the inner call, and by (B) free in $E\Gamma$. Then the binding would make $u$ free in $E\Gamma$, or link $u$ below a root that is free in $E\Gamma$. Both contradict the choice of $u$. $\square$

So the two modes quantify the same variables, and Theorems 1 and 2 hold for both.

## Termination

Each call of J recurses on proper subterms. Each step of UNIFY either stops or links a root, which lowers the number of roots by one, or decomposes a pair of arrow nodes, and each pair is decomposed at most once per call by the memo table. FIND stops because the structure has no cycles. So J stops on each input.

## References

- Robin Milner, A theory of type polymorphism in programming, Journal of Computer and System Sciences 17(3), 1978, pages 348 to 375. Section 4 defines J and shows that it computes the same result as W.
- Luis Damas, Type assignment in programming languages, PhD thesis, University of Edinburgh, 1985. The full proofs for W.
- Didier Remy, Extension of ML type system with a sorted equational theory on types, INRIA Research Report 1766, 1992. Generalization by levels and ranked unification.
