---
title: STRICTNESS stops at the least fixed point of the abstract body, and every argument it calls strict is strict
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode on the main page. Let $\mathbf{2} = \{0, 1\}$ with $0 \le 1$. A *table* is a map $T : \mathbf{2}^k \to \mathbf{2}$. Tables are ordered point by point: $T \le S$ if $T(a) \le S(a)$ for all $a$. A table is *monotone* if $a \le b$ point by point implies $T(a) \le T(b)$. For a table $T$, let $F(T)(a) = \mathrm{ABS}(\mathit{body}, \{x_i \mapsto a_i\}, T)$, so line L3 computes $T' = F(T)$.

## The concrete meaning

Let $D = \mathbb{Z} \cup \{\mathit{true}, \mathit{false}\} \cup \{\bot\}$ be the flat domain: $\bot \sqsubseteq d$ for all $d$, and no other two elements are related. Here $\bot$ stands for a loop and also for a runtime error. An environment $\rho$ maps names to $D$. For a function $\psi : D^k \to D$, the meaning $C[e]\rho\psi$ of an expression is:

- $C[c]\rho\psi = c$ for a constant $c$, and $C[x]\rho\psi = \rho(x)$ for a name $x$.
- $C[e_1\ \mathit{op}\ e_2]\rho\psi$ is the result of $\mathit{op}$ when both operands are integers, and $\bot$ in all other cases.
- $C[\mathbf{if}\ e_1\ \mathbf{then}\ e_2\ \mathbf{else}\ e_3]\rho\psi$ is $C[e_2]\rho\psi$ if $C[e_1]\rho\psi = \mathit{true}$, $C[e_3]\rho\psi$ if it is $\mathit{false}$, and $\bot$ in all other cases.
- $C[\mathbf{let}\ x = e_1\ \mathbf{in}\ e_2]\rho\psi = C[e_2]\rho[x \mapsto C[e_1]\rho\psi]\psi$.
- $C[f\ e_1 \ldots e_k]\rho\psi = \psi(C[e_1]\rho\psi, \ldots, C[e_k]\rho\psi)$.

The arguments of a call and the right side of a `let` are passed as meanings, not computed first: this is call by name. Let $\Phi(\psi)(d) = C[\mathit{body}]\{x_i \mapsto d_i\}\psi$. $\Phi$ is continuous on the domain of functions $D^k \to D$, so the meaning of $f$ is its least fixed point

$$ \varphi = \bigsqcup_{j \ge 0} \varphi_j, \qquad \varphi_0(d) = \bot, \qquad \varphi_{j+1} = \Phi(\varphi_j). $$

This is the standard denotational semantics of recursion equations under call by name. Its adequacy, that a lazy run of $f\ d_1 \ldots d_k$ stops with a value exactly when $\varphi(d) \ne \bot$, is proved in Winskel's *The Formal Semantics of Programming Languages* (1993), in the chapter on recursion equations. We use it only to connect the result below with running programs.

Let $\mathit{abs}(\bot) = 0$ and $\mathit{abs}(d) = 1$ for $d \ne \bot$. For an abstract environment $\alpha$ that maps names to $\mathbf{2}$, write $\rho \lhd \alpha$ if $\mathit{abs}(\rho(x)) \le \alpha(x)$ for every name $x$. A table $T$ *covers* a function $\psi : D^k \to D$ if $\mathit{abs}(\psi(d)) \le T(a)$ for all $d \in D^k$ and $a \in \mathbf{2}^k$ with $\mathit{abs}(d_i) \le a_i$ for every $i$.

## Part 1: the iteration

**Lemma 1 (monotonicity).** Let $T$ be a monotone table with $T \le S$, and let $\alpha \le \beta$ point by point. Then $\mathrm{ABS}(e, \alpha, T) \le \mathrm{ABS}(e, \beta, S)$ for every expression $e$.

*Proof.* By induction on $e$, for all $\alpha \le \beta$ at once.

- Line L9: both sides are $1$.
- Line L10: $\alpha(x) \le \beta(x)$.
- Lines L11 and L12: by induction each operand on the left is at most the matching operand on the right, and $\wedge$ and $\vee$ are monotone in each argument.
- Line L13: by induction $\mathrm{ABS}(e_1, \alpha, T) \le \mathrm{ABS}(e_1, \beta, S)$, so $\alpha[x \mapsto \mathrm{ABS}(e_1, \alpha, T)] \le \beta[x \mapsto \mathrm{ABS}(e_1, \beta, S)]$, and the induction hypothesis for $e_2$ gives the claim.
- Line L14: let $b$ and $b'$ be the vectors of the abstract values of the arguments on the left and on the right. By induction $b \le b'$. Then $T(b) \le T(b')$ since $T$ is monotone, and $T(b') \le S(b')$ since $T \le S$. $\square$

With $S = T$, Lemma 1 says that $F(T)$ is monotone when $T$ is monotone. With $\alpha = \beta$, it says that $F(T) \le F(S)$ when $T$ is monotone and $T \le S$.

**Theorem 1 (termination).** Let $T_0$ be the table of line L1 and $T_{j+1} = F(T_j)$. Every $T_j$ is monotone, $T_0 \le T_1 \le T_2 \le \ldots$, and the loop of lines L2 to L6 stops after at most $2^k + 1$ rounds, with $T = T_j$ for the first $j$ such that $T_{j+1} = T_j$.

*Proof.* $T_0$ is constant, so it is monotone, and by Lemma 1 so is every $T_j$. $T_0 \le T_1$ since $T_0$ is the least table. If $T_j \le T_{j+1}$, then $T_{j+1} = F(T_j) \le F(T_{j+1}) = T_{j+2}$ by Lemma 1, since $T_j$ is monotone. So the chain goes up. Round $j + 1$ computes $T' = T_{j+1}$ from $T = T_j$ in line L3, and line L4 tests $T_{j+1} = T_j$. While the test fails, $T_{j+1}$ has strictly more entries equal to $1$ than $T_j$. There are only $2^k$ entries, so the test fails at most $2^k$ times, and the loop stops after at most $2^k + 1$ rounds. When it stops, line L5 sets $T = T' = T_{j+1} = T_j$. $\square$

**Theorem 2 (least fixed point).** The table $T^*$ that the loop returns satisfies $F(T^*) = T^*$, and $T^* \le S$ for every table $S$ with $F(S) \le S$. So $T^*$ is the least fixed point of $F$.

*Proof.* $F(T^*) = T^*$ is the stopping test of line L4. Let $F(S) \le S$. Then $T_0 \le S$, and if $T_j \le S$, Lemma 1 gives $T_{j+1} = F(T_j) \le F(S) \le S$, since $T_j$ is monotone. So $T^* = T_j \le S$. $\square$

## Part 2: soundness

**Lemma 2 (local soundness).** If $\rho \lhd \alpha$ and $T$ covers $\psi$, then $\mathit{abs}(C[e]\rho\psi) \le \mathrm{ABS}(e, \alpha, T)$ for every expression $e$.

*Proof.* By induction on $e$, for all $\rho \lhd \alpha$ at once. Write $c_i = C[e_i]\rho\psi$ and $a_i = \mathrm{ABS}(e_i, \alpha, T)$. By the induction hypothesis, $\mathit{abs}(c_i) \le a_i$.

- Line L9: the meaning is a constant, and $\mathit{abs}$ of it is $1 \le 1$.
- Line L10: $\mathit{abs}(\rho(x)) \le \alpha(x)$ since $\rho \lhd \alpha$.
- Line L11: if $c_1 = \bot$ or $c_2 = \bot$, the meaning is $\bot$ and the claim holds since $\mathit{abs}(\bot) = 0$. Otherwise $\mathit{abs}(c_1) = \mathit{abs}(c_2) = 1$, so $a_1 = a_2 = 1$ and the right side is $1$.
- Line L12: if $c_1$ is not a boolean, the meaning is $\bot$. Otherwise $\mathit{abs}(c_1) = 1$, so $a_1 = 1$, and the meaning is $c_2$ or $c_3$. Then its $\mathit{abs}$ is at most $a_2$ or $a_3$, so at most $a_2 \vee a_3 = a_1 \wedge (a_2 \vee a_3)$.
- Line L13: $\rho[x \mapsto c_1] \lhd \alpha[x \mapsto a_1]$ since $\mathit{abs}(c_1) \le a_1$. The induction hypothesis for $e_2$ with these environments gives the claim.
- Line L14: the meaning is $\psi(c_1, \ldots, c_k)$ with $\mathit{abs}(c_i) \le a_i$ for every $i$. Since $T$ covers $\psi$, $\mathit{abs}(\psi(c)) \le T(a)$, which is the right side. $\square$

**Theorem 3 (soundness).** $T^*$ covers $\varphi$. So if line L7 sets $\mathit{strict}[i]$, then $\varphi(d) = \bot$ for every $d \in D^k$ with $d_i = \bot$: $f$ is strict in $x_i$.

*Proof.* First, $T^*$ covers every $\varphi_j$, by induction on $j$. It covers $\varphi_0$, since $\mathit{abs}(\varphi_0(d)) = 0$. Suppose it covers $\varphi_j$, and let $\mathit{abs}(d_i) \le a_i$ for every $i$. Then $\{x_i \mapsto d_i\} \lhd \{x_i \mapsto a_i\}$, and Lemma 2 gives

$$ \mathit{abs}(\varphi_{j+1}(d)) = \mathit{abs}(C[\mathit{body}]\{x_i \mapsto d_i\}\varphi_j) \le \mathrm{ABS}(\mathit{body}, \{x_i \mapsto a_i\}, T^*) = F(T^*)(a) = T^*(a). $$

Now fix $d$ and $a$ with $\mathit{abs}(d_i) \le a_i$. The values $\varphi_j(d)$ form a chain in the flat domain $D$, so either they are all $\bot$ and $\varphi(d) = \bot$, or they are equal to one value $v \ne \bot$ from some $j$ on and $\varphi(d) = v = \varphi_j(d)$. In both cases $\mathit{abs}(\varphi(d)) \le T^*(a)$.

If $\mathit{strict}[i]$ is set, then $T^*(p) = 0$ for the point $p$ with $p_i = 0$ and $p_l = 1$ for $l \ne i$. Every $d$ with $d_i = \bot$ has $\mathit{abs}(d_l) \le p_l$ for every $l$, so $\mathit{abs}(\varphi(d)) \le 0$ and $\varphi(d) = \bot$. $\square$

The proof of Theorem 3 used only $F(T^*) \le T^*$. So every post-fixed point of $F$ is safe, the greatest fixed point too. By Theorem 2 the least fixed point is below every post-fixed point, so of all these safe tables it finds the most strict arguments. A table below it, such as $T_1$ in the example of the main page, need not be safe. By adequacy, Theorem 3 also says that a lazy run of $f$ with an argument that loops in place $i$ never stops with a value. $\blacksquare$
