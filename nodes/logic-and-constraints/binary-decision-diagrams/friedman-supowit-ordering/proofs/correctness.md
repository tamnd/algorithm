---
title: The Friedman-Supowit program returns the size of a smallest OBDD and an order that reaches it
proves: [correctness]
status: full
---

Let $f$ be a function of the variables $x_1, \ldots, x_n$ with values in a finite set, and let $V$ be the set of variables. For a set $J \subseteq V$ and an assignment $b$ to the variables of $V \setminus J$, the subfunction $f|_b$ is a function of the variables in $J$. An order $\pi$ lists the variables from the top level to the bottom level. $G_\pi(f)$ is the reduced $\pi$-OBDD of $f$, and $|G_\pi(f)|$ counts its inner nodes and its sinks.

**Fact 1 (nodes are subfunctions).** For an order $\pi$, let $x$ be on level $k$, and let $J$ be the set of variables below $x$. The nodes of $G_\pi(f)$ that test $x$ are in one-to-one correspondence with the distinct functions $f|_b$, for $b$ an assignment to $V \setminus (J \cup \{x\})$, that depend on $x$. The sinks are in one-to-one correspondence with the values that $f$ takes.

This is the subfunction form of the canonicity theorem; see [BDD canonicity](/bdd-canonicity/) and [reduced ordered BDD](/reduced-ordered-bdd/).

**Lemma 1 (the level lemma).** In the situation of Fact 1, the number of nodes that test $x$ is

$$\mathrm{cost}(J, x) = \#\{ (f|_{b, x=0}, f|_{b, x=1}) : b \text{ assigns } V \setminus (J \cup \{x\}), \ f|_{b, x=0} \ne f|_{b, x=1} \}.$$

In particular, it depends only on $J$ and $x$, not on the order of the variables in $J$ or above $x$.

*Proof.* A function $g$ of the variables in $J \cup \{x\}$ is fixed by its two halves $g|_{x=0}$ and $g|_{x=1}$, and it depends on $x$ exactly when the halves differ. Apply this to $g = f|_b$. Then the map $f|_b \mapsto (f|_{b, x=0}, f|_{b, x=1})$ is a bijection from the distinct subfunctions $f|_b$ that depend on $x$ to the distinct pairs with two different entries. By Fact 1, the first set has one element per $x$-node. The definition of $\mathrm{cost}(J, x)$ uses only the sets $J$ and $\{x\}$. $\square$

**Lemma 2 (the tables).** For each set $K$ that the program reaches, the table $T_K$ maps each assignment $b$ to $V \setminus K$ to a name, and $T_K[b] = T_K[b']$ if and only if $f|_b = f|_{b'}$ as functions of $K$. Moreover, line L6 computes $\mathrm{cost}(J, x)$.

*Proof.* By induction on $|K|$. For $K = \emptyset$, $f|_b$ is the value $f(b)$, and line L1 gives one name per value. For the step, $T_K$ is made from $T_J$ with $K = J \cup \{x\}$. For an assignment $b$ to $V \setminus K$, let $p = T_J[b, x=0]$ and $q = T_J[b, x=1]$. By the induction hypothesis, $p$ and $q$ name the two halves of $f|_b$. If $p = q$, then $f|_b$ does not depend on $x$, it equals its halves, and it keeps the name $p$. If $p \ne q$, the name is a fresh name for the pair $(p, q)$; equal pairs get the same fresh name, and a fresh name never equals an old name. Two subfunctions $f|_b$ and $f|_{b'}$ on $K$ are equal exactly when their halves are equal, so they get equal names exactly when they are equal. Line L6 counts the distinct pairs $(p, q)$ with $p \ne q$, which by the induction hypothesis are the distinct pairs of halves, so it computes $\mathrm{cost}(J, x)$. $\square$

**Lemma 3 (the size of an order).** For every order $\pi = (y_1, \ldots, y_n)$ from the top, with $J_k = \{y_{k+1}, \ldots, y_n\}$,

$$|G_\pi(f)| = |\mathrm{values}(f)| + \sum_{k=1}^{n} \mathrm{cost}(J_k, y_k).$$

*Proof.* Sum Fact 1 and Lemma 1 over the levels, and add the sinks. $\square$

**Lemma 4 (the recurrence).** For a nonempty set $K$, let $\mathrm{opt}(K)$ be the minimum, over all orders $(z_1, \ldots, z_m)$ of $K$, of $\sum_{i=1}^{m} \mathrm{cost}(\{z_{i+1}, \ldots, z_m\}, z_i)$, and let $\mathrm{opt}(\emptyset) = 0$. Then

$$\mathrm{opt}(K) = \min_{x \in K} \big( \mathrm{opt}(K \setminus \{x\}) + \mathrm{cost}(K \setminus \{x\}, x) \big).$$

*Proof.* In an order of $K$, the first variable $z_1 = x$ contributes $\mathrm{cost}(K \setminus \{x\}, x)$, which does not depend on the rest of the order by Lemma 1. The rest is an order of $K \setminus \{x\}$, with the sum of its terms at least $\mathrm{opt}(K \setminus \{x\})$, and an order of $K \setminus \{x\}$ that reaches $\mathrm{opt}(K \setminus \{x\})$ can follow $x$. So the minimum over the orders of $K$ with first variable $x$ is $\mathrm{opt}(K \setminus \{x\}) + \mathrm{cost}(K \setminus \{x\}, x)$, and $\mathrm{opt}(K)$ is the minimum over $x$. $\square$

**Theorem.** FRIEDMAN-SUPOWIT$(f, n)$ returns $\min_\pi |G_\pi(f)|$ and an order $\pi$ that reaches it.

*Proof.* We show by induction on $k$ that after the iteration $k$ of line L3, for every set $K$ of $k + 1$ variables, $\mathrm{best}[K] = \mathrm{opt}(K)$, and $\mathrm{choice}[K]$ is an $x \in K$ at which the minimum of Lemma 4 is reached; also $T_K$ exists and satisfies Lemma 2. For $k = 0$, $\mathrm{best}[\emptyset] = 0 = \mathrm{opt}(\emptyset)$ and $T_\emptyset$ exists by lines L1 and L2.

In iteration $k$, every set $J$ of $k$ variables has its final $\mathrm{best}[J] = \mathrm{opt}(J)$ and its table, by the induction hypothesis. Every pair $(J, x)$ with $x \notin J$ is visited at line L5, and line L6 computes $\mathrm{opt}(J) + \mathrm{cost}(J, x)$ by Lemma 2. Each set $K$ of $k + 1$ variables arises from the $|K|$ pairs $(K \setminus \{x\}, x)$, and line L7 keeps the minimum and the $x$ that gives it. By Lemma 4 this is $\mathrm{opt}(K)$. Line L8 builds $T_K$ once, from the pair in which $x$ is the smallest variable of $K$, and Lemma 2 applies. Line L9 drops only the values of layer $k$, which later iterations do not read.

After the last iteration, $\mathrm{best}[V] = \mathrm{opt}(V)$. Line L10 lists $x_1' = \mathrm{choice}[V]$, then $\mathrm{choice}[V \setminus \{x_1'\}]$, and so on. The values of these choices were kept, since the program keeps the choices of all layers. By the choice of each step, the order $\pi$ that line L10 produces has $\sum_k \mathrm{cost}(J_k, y_k) = \mathrm{opt}(V)$, by induction along the list with Lemma 4. By Lemma 3, $|G_\pi(f)| = |\mathrm{values}(f)| + \mathrm{opt}(V)$, and every order has a size of at least this, since its sum of costs is at least $\mathrm{opt}(V)$ by the definition of opt. So line L11 returns the minimum size and an order that reaches it. $\blacksquare$
