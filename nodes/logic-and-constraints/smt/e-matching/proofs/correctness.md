---
title: Correctness of E-matching on a congruence-closed e-graph
proves: [correctness, termination]
status: full
---

We prove that EMATCH finds exactly the substitutions that make a pattern equal to a term of a class, modulo the ground equations of the e-graph, and that it finds each one once. The proof has two parts. Lemma 1 says how a ground term that is not in the e-graph relates to the classes. Theorem 2 is the induction on the pattern.

## Setting

$E$ is a finite set of ground equations, and $T$ is a finite set of ground terms that contains both sides of each equation and is closed under subterms. $\sim$ is the congruence closure of $E$ on $T$: the least equivalence relation on $T$ that contains $E$ and is closed under congruence. By the theorem of congruence closure (see [congruence closure](/congruence-closure/)), for $s, t \in T$ we have $E \models s = t$ exactly when $s \sim t$, and this holds for any finite subterm-closed set that contains $s$, $t$ and the terms of $E$.

The e-graph $G$ stores the classes of $\sim$. Each class $C$ has a set of *nodes* $f(C_1, \ldots, C_n)$, one for each distinct tuple $(f, C_1, \ldots, C_n)$ such that some term $f(t_1, \ldots, t_n) \in C$ has $t_i \in C_i$. Because $\sim$ is a congruence, a node belongs to exactly one class: two terms $f(\bar t)$ and $f(\bar u)$ with $t_i \sim u_i$ are in the same class. A constant $a \in T$ is the node $a()$.

A *pattern* is a term that can contain variables. A *substitution* $\sigma$ maps variables to classes. For a pattern $p$ whose variables are in the domain of $\sigma$, $p\hat\sigma$ is the ground term that we get by replacing each variable $x$ with a term of the class $\sigma(x)$. The choice of the term does not matter, as Lemma 1 shows.

## Lemma 1 (where a ground term lands)

Define $\kappa$ on all ground terms, bottom-up. For $s = f(s_1, \ldots, s_n)$, with $n \ge 0$:

- if $G$ has a node $f(\kappa(s_1), \ldots, \kappa(s_n))$, then $\kappa(s)$ is the class of this node;
- otherwise $\kappa(s)$ is the new symbol $\langle f, \kappa(s_1), \ldots, \kappa(s_n) \rangle$, which is not a class.

In the first case all $\kappa(s_i)$ are classes, because nodes have classes as children.

*For every ground term $s$ and every $t \in T$: $E \models s = t$ exactly when $\kappa(s)$ is the class of $t$.*

*Proof.* Let $T'$ be $T$ together with all subterms of $s$, and let $\sim'$ be the congruence closure of $E$ on $T'$. By the theorem of congruence closure, $E \models s = t$ exactly when $s \sim' t$. Define $u \approx v$ on $T'$ by $\kappa(u) = \kappa(v)$. We show that $\approx$ and $\sim'$ are equal.

*First, $\kappa(t)$ is the class of $t$ for $t \in T$.* By induction on $t = f(t_1, \ldots, t_n)$: each $\kappa(t_i)$ is the class $C_i$ of $t_i$, and $G$ has the node $f(C_1, \ldots, C_n)$ in the class of $t$, because $t$ is such a term. So $\kappa(t)$ is the class of $t$.

*$\sim' \subseteq \approx$.* The relation $\approx$ is an equivalence relation. It contains $E$, because the two sides of an equation of $E$ are in one class of $\sim$, and $\kappa$ gives that class to both. It is closed under congruence: $\kappa(f(\bar u))$ depends only on $f$ and the tuple $\kappa(u_1), \ldots, \kappa(u_n)$. As $\sim'$ is the least such relation, $\sim' \subseteq \approx$.

*$\approx \subseteq \sim'$.* We show by induction on $u \in T'$ two claims: if $\kappa(u)$ is a class $C$, then $u \sim' t$ for every $t \in C$; and if $\kappa(u) = \kappa(v)$ for another $v \in T'$, then $u \sim' v$. Let $u = f(u_1, \ldots, u_n)$.

- If $\kappa(u)$ is a class $C$, there is a node $f(C_1, \ldots, C_n)$ in $C$ with $C_i = \kappa(u_i)$, and a term $f(t_1, \ldots, t_n) \in C$ with $t_i \in C_i$. By induction $u_i \sim' t_i$, so $u \sim' f(\bar t)$ by congruence. Every $t \in C$ has $t \sim f(\bar t)$, and $\sim \subseteq \sim'$. So $u \sim' t$. If also $\kappa(v) = C$, then $v \sim' t$ in the same way, and $u \sim' v$.
- If $\kappa(u) = \langle f, k_1, \ldots, k_n \rangle$ and $\kappa(v) = \kappa(u)$, then $v = f(v_1, \ldots, v_n)$ with $\kappa(v_i) = k_i = \kappa(u_i)$. By induction $u_i \sim' v_i$, so $u \sim' v$ by congruence.

So $\approx$ equals $\sim'$. For $t \in T$, $E \models s = t$ holds exactly when $\kappa(s) = \kappa(t)$, which is the class of $t$. $\square$

In particular, $\kappa(p\hat\sigma)$ does not depend on the terms chosen for the variables: each choice has $\kappa$ equal to $\sigma(x)$, and $\kappa$ is computed bottom-up.

## Theorem 2 (EMATCH is correct)

*Let $c$ be a class and $\sigma_0$ a substitution. EMATCH$(p, c, \sigma_0)$ returns, each exactly once, the substitutions $\sigma$ that extend $\sigma_0$, have the domain $\mathrm{dom}(\sigma_0) \cup \mathrm{vars}(p)$, and satisfy $\kappa(p\hat\sigma) = c$.* By Lemma 1, $\kappa(p\hat\sigma) = c$ means $E \models p\hat\sigma = t$ for the terms $t$ of $c$.

*Proof.* By induction on $p$.

**$p$ is a variable $x$ that $\sigma_0$ does not bind (line L2).** The only extension with domain $\mathrm{dom}(\sigma_0) \cup \{x\}$ and $\kappa(x\hat\sigma) = \sigma(x) = c$ is $\sigma_0 \cup \{x \mapsto c\}$, and line L2 returns it once.

**$p$ is a variable $x$ that $\sigma_0$ binds (line L3).** The only candidate is $\sigma_0$ itself, and $\kappa(x\hat\sigma_0) = \sigma_0(x)$. Line L3 returns $\sigma_0$ once if $\sigma_0(x) = c$, and nothing otherwise.

**$p = f(p_1, \ldots, p_n)$ (lines L4 to L9).** As $c$ is a class, $\kappa(p\hat\sigma) = c$ holds exactly when $c$ has a node $f(c_1, \ldots, c_n)$ with $\kappa(p_i\hat\sigma) = c_i$ for all $i$. Fix such a node at line L5. We claim that after step $i$ of line L7, the list $\Sigma$ holds, each once, the extensions $\tau$ of $\sigma_0$ with domain $\mathrm{dom}(\sigma_0) \cup \mathrm{vars}(p_1, \ldots, p_i)$ and $\kappa(p_j\hat\tau) = c_j$ for all $j \le i$. For $i = 0$, $\Sigma = [\sigma_0]$ (line L6). For step $i$, the induction hypothesis on $p_i$ says that EMATCH$(p_i, c_i, \tau)$ returns, each once, the extensions of $\tau$ to $\mathrm{vars}(p_i)$ with $\kappa(p_i\hat\tau') = c_i$. Each wanted extension at step $i$ restricts to exactly one $\tau$ of step $i - 1$, so it appears once, and every returned substitution is wanted. The values $\kappa(p_j\hat\tau)$ for $j < i$ do not change, because the new bindings are only for variables that are not in $p_1, \ldots, p_{i-1}$.

After step $n$, $\Sigma$ holds the matches that go through this node. A match $\sigma$ fixes the tuple $\kappa(p_1\hat\sigma), \ldots, \kappa(p_n\hat\sigma)$, so it goes through exactly one node of $c$, because the nodes of a class are distinct tuples. So line L8 collects each match once, and line L9 returns all of them. Nodes with another head symbol or another arity cannot match, and line L5 skips them. $\square$

**Corollary.** MATCH-ALL (line L10) returns each pair $(c, \sigma)$ with $\mathrm{dom}(\sigma) = \mathrm{vars}(p)$ and $E \models p\hat\sigma = t$ for the terms $t$ of $c$. Each pair appears once.

## Termination and the size of the search

Each recursive call is on a proper subterm of $p$, and each loop runs over a finite list. So EMATCH terminates. Let $m$ be the number of symbols of $p$ and $a \le m$ the number of its function symbols. A run makes one choice of a node at line L5 for each function symbol of $p$ that it reaches, and each sequence of choices is followed for $O(m)$ steps. With $n$ nodes in the e-graph, there are at most $n^a$ full sequences, and at most $n + n^2 + \cdots + n^a$ prefixes. So the time is $O(m\, n^m)$, with union-find operations counted as one step. The bound is reached up to a constant in the exponent: the test of the implementation builds a class with $n$ nodes $f(c_i)$, where the pattern $h(f(x_1), \ldots, f(x_k))$ has $n^k$ matches. $\blacksquare$
