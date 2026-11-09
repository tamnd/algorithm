---
title: Huet's pre-unification is sound and complete for pre-unifiers
proves: [correctness]
status: full
---

All terms are simply typed, $\beta$-normal and $\eta$-long. A substitution $\delta$ maps free variables to closed terms of the same type, and $\delta(t)$ is the $\beta$-normal $\eta$-long form of the result. For a set $E$ of pairs, $U(E)$ is the set of unifiers of $E$. We write $\delta = \rho \circ \theta$ on $V$ when $\delta(F) = \rho(\theta(F))$ for each $F \in V$, and $\theta \le \delta$ on $V$ when such a $\rho$ exists. $V$ is the set of free variables of the input.

**Lemma 1 (rigid heads stay).** Let $t = \lambda \bar x.\, a(t_1, \ldots, t_m)$ with $a$ a constant or one of the $x_i$. Then $\delta(t) = \lambda \bar x.\, a(\delta(t_1), \ldots, \delta(t_m))$, where each $\delta(t_i)$ is normal.

*Proof.* The substitution replaces only free variables, and the head $a$ is not a free variable. The values of $\delta$ are closed, so no $x_i$ is captured. Normalization works inside the arguments only, because the head is not a λ-term. $\square$

**Lemma 2 (SIMPL).** If SIMPL$(E)$ = fail, then $U(E) = \emptyset$. Otherwise $U(\text{SIMPL}(E)) = U(E)$.

*Proof.* Take one step of lines L12 to L14 on $\lambda \bar x.\, a(\bar s) \doteq \lambda \bar x.\, b(\bar t)$. By Lemma 1, the two instances are $\lambda \bar x.\, a(\delta(\bar s))$ and $\lambda \bar x.\, b(\delta(\bar t))$. Two normal η-long terms are equal up to $\beta\eta$ exactly when they are equal up to α. So if $a \ne b$ no $\delta$ unifies the pair, and if $a = b$ then $\delta$ unifies the pair if and only if it unifies each $\lambda \bar x.\, s_i \doteq \lambda \bar x.\, t_i$. Line L15 only swaps the sides of pairs. Each step makes the pairs smaller, so SIMPL stops. $\square$

**Lemma 3 (Huet's lemma).** A set $E$ of flex-flex pairs always has a unifier.

*Proof.* For each base type $\beta$ take a new variable $H_\beta : \beta$. For each variable $F : \tau_1 \to \ldots \to \tau_n \to \beta$ that is the head of a side of a pair, let $\rho(F) = \lambda y_1 \ldots y_n.\, H_\beta$. A flex side $\lambda \bar x.\, F(\bar s)$ of type $\bar\gamma \to \beta$ becomes $\lambda \bar x.\, H_\beta$. The two sides of a pair have the same type, so they have the same binders $\bar x$ (up to α) and the same base type $\beta$. So both sides become $\lambda \bar x.\, H_\beta$. $\square$

**Theorem 1 (soundness).** Each output $(\theta, E')$ of PRE-UNIFY$(E)$ has $U(E') \subseteq \{ \sigma : \sigma \circ \theta \in U(E) \}$, $E'$ has only flex-flex pairs, and $\rho \circ \theta$ unifies $E$ for the substitution $\rho$ of Lemma 3.

*Proof.* We show the invariant: for each node $(E_1, \theta_1)$ in the queue, if $\sigma$ unifies $E_1$ then $\sigma \circ \theta_1$ unifies $E$. It is true for the root. Lemma 2 keeps it in line L4. In line L11, the child has $\rho(E_1)$ and $\rho \circ \theta_1$. If $\sigma$ unifies $\rho(E_1)$, then $\sigma \circ \rho$ unifies $E_1$, so $\sigma \circ \rho \circ \theta_1$ unifies $E$. A node is output in line L7 only when $E'$ has no flex-rigid pair and SIMPL removed all rigid-rigid pairs, so $E'$ is flex-flex. Lemma 3 gives $\rho \in U(E')$, and the invariant gives $\rho \circ \theta \in U(E)$. $\square$

**Theorem 2 (completeness).** Let $\delta$ unify $E$. Then the search tree has an output node $(\theta, E')$ with $\theta \le \delta$ on $V$. The depth of this node is at most $\lVert \delta \rVert$, the total number of head symbols in the terms $\delta(F)$ for $F \in V$.

*Proof.* We build a path from the root. Along the path we keep a node $(E_1, \theta_1)$ and a substitution $\delta_1$ with these properties:

> **(G)** $\delta_1$ unifies $E_1$, and $\delta = \delta_1 \circ \theta_1$ on $V$. The domain $W_1$ of $\delta_1$ holds the free variables of $E_1$ and of the terms $\theta_1(F)$, $F \in V$.

At the root, $\delta_1 = \delta$ and $\theta_1$ is the identity, so (G) is true. Let $\mu = \sum_{G \in W_1} \lVert \delta_1(G) \rVert$, where $\lVert t \rVert$ counts the head symbols of $t$. At the root $\mu = \lVert \delta \rVert$.

Lemma 2 shows that SIMPL does not fail on $E_1$, because $\delta_1$ unifies it, and that $\delta_1$ still unifies the result. If no flex-rigid pair is left, the node is output, and (G) gives $\theta_1 \le \delta$ on $V$.

Otherwise let $\lambda \bar x.\, F(s_1, \ldots, s_n) \doteq \lambda \bar x.\, a(\bar t)$ be the pair of line L9, with $F : \tau_1 \to \ldots \to \tau_n \to \beta$. Write $\delta_1(F) = \lambda y_1 \ldots y_n.\, h(w_1, \ldots, w_k)$. The head $h$ is a constant or some $y_j$, because $\delta_1(F)$ is closed.

If $h$ is a constant, then the normal form of $\delta_1(F(\bar s))$ has the head $h$. By Lemma 1 the other side has the head $a$. Since $\delta_1$ unifies the pair, $h = a$, so $a$ is a constant and MATCH has the imitation with head $a$ (line L19). If $h = y_j$, then the type of $y_j$ is $\tau_j$ and its result type is $\beta$, so MATCH has the projection on $y_j$ (line L21). In both cases let $\rho$ be this binding, $\rho(F) = \lambda \bar y.\, h(\lambda \bar z_1.\, H_1(\bar y, \bar z_1), \ldots, \lambda \bar z_k.\, H_k(\bar y, \bar z_k))$, and set

$$\delta_2 = \delta_1 \text{ without } F, \text{ plus } H_i \mapsto \lambda \bar y \bar z_i.\, w_i' \text{ for } i = 1, \ldots, k,$$

where $w_i = \lambda \bar z_i.\, w_i'$. Then $\delta_2(\rho(F)) = \lambda \bar y.\, h(w_1, \ldots, w_k) = \delta_1(F)$, and $\delta_2 \circ \rho = \delta_1$ on $W_1$. So $\delta_2$ unifies $\rho(E_1)$, and $\delta = \delta_2 \circ (\rho \circ \theta_1)$ on $V$. The child node of line L11 with $\rho$ therefore satisfies (G).

The measure goes down: $\lVert \delta_1(F) \rVert = 1 + \sum_i \lVert w_i \rVert = 1 + \sum_i \lVert \delta_2(H_i) \rVert$, and the other values do not change. So $\mu$ drops by exactly one at each step. Since $\mu \ge 0$, the path reaches an output node after at most $\lVert \delta \rVert$ steps. $\blacksquare$

**Corollary.** With a fair queue, the set of outputs is a complete set of pre-unifiers of $E$, and each unifier is covered by an output at a finite depth. If $E$ has a unifier, the procedure outputs one after a finite time.

The implementation tests check Theorem 1 by a direct test of each output, and check Theorem 2 by following the branch that each small ground unifier selects. The ground unifiers come from a brute-force list of all closed terms up to a fixed size.
