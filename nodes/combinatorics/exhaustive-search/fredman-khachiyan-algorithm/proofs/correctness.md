---
title: FK-DUAL returns a witness exactly when the two DNFs are not dual
proves: [correctness]
status: full
---

We use the notation of the page. A monotone DNF is a finite family of subsets of a finite set of variables, and for $x \subseteq U$, with $U$ any finite set that contains every variable that occurs, $f(x) = 1$ when some term of $f$ is a subset of $x$. Write $\bar{x} = U \setminus x$. Two DNFs $f$ and $g$ are *dual* when $f(x) \ne g(\bar{x})$ for every $x \subseteq U$, and a *witness* is an $x$ with $f(x) = g(\bar{x})$.

**Lemma 0 (the choice of $U$ does not matter).** Let $V$ be the set of variables that occur in $f$ or $g$, and let $U \supseteq V$. For $x \subseteq U$, $f(x) = f(x \cap V)$ and $g(U \setminus x) = g(V \setminus (x \cap V))$. So $x$ is a witness over $U$ if and only if $x \cap V$ is a witness over $V$, and duality over $U$ and over $V$ are the same.

*Proof.* A term $T \subseteq V$ satisfies $T \subseteq x$ if and only if $T \subseteq x \cap V$, and $T \subseteq U \setminus x$ if and only if $T \subseteq V \setminus x$. $\square$

So below the complement is over $V$, the variables of the current call, and a witness over $V$ is a witness over every larger set.

**Lemma 1 (line L1).** Removing repeated terms and terms that contain another term does not change $f$ or $g$ as functions.

*Proof.* If $T' \subseteq T$ are both terms, then $T \subseteq x$ implies $T' \subseteq x$, so the term $T$ never decides the value. $\square$

From now on $f$ and $g$ are *irredundant*: no term contains another.

**Lemma 2 (lines L2 to L5 return witnesses).**

1. If $F \in f$, $G \in g$ and $F \cap G = \emptyset$, then $x = F$ is a witness.
2. If line L2 does not return, $v \in F \in f$, and $v$ is in no term of $g$, then $x = F \setminus \{v\}$ is a witness.
3. If line L2 does not return, $v \in G \in g$, and $v$ is in no term of $f$, then $x = V \setminus (G \setminus \{v\})$ is a witness.
4. If $\sigma = \sum_{F \in f} 2^{-|F|} + \sum_{G \in g} 2^{-|G|} < 1$, then the procedure of line L5 returns an $x$ with $f(x) = 0 = g(\bar{x})$.

*Proof.* (1) $F \subseteq x$, so $f(x) = 1$. $G \subseteq V \setminus F = \bar{x}$, so $g(\bar{x}) = 1$.

(2) Let $x = F \setminus \{v\}$. If a term $F'$ of $f$ were a subset of $x$, then $F' \subsetneq F$, against irredundancy. So $f(x) = 0$. Now $\bar{x} = \bar{F} \cup \{v\}$. A term $G$ of $g$ does not contain $v$, so $G \subseteq \bar{x}$ would give $G \subseteq \bar{F}$, that is, $G \cap F = \emptyset$, which line L2 excludes. So $g(\bar{x}) = 0$.

(3) This is (2) with $f$ and $g$ exchanged and $x$ replaced by $\bar{x}$: here $\bar{x} = G \setminus \{v\}$, so $g(\bar{x}) = 0$ by irredundancy, and $x = \bar{G} \cup \{v\}$, so $f(x) = 1$ would need a term of $f$ inside $\bar{G}$, that is, disjoint from $G$.

(4) For a partial assignment $p$ of the variables, let $E(p)$ be the expected value of $N(x) = |\{F \in f : F \subseteq x\}| + |\{G \in g : G \subseteq \bar{x}\}|$ when the unassigned variables are independent and true with probability $\tfrac12$. For the empty assignment, a term $T$ is inside $x$, or inside $\bar{x}$, with probability $2^{-|T|}$, so $E(\emptyset) = \sigma < 1$. For a variable $u$ that $p$ leaves open, $E(p) = \tfrac12 E(p, u = 1) + \tfrac12 E(p, u = 0)$, so the smaller of the two is at most $E(p)$. The procedure always takes the smaller one, so after all variables are fixed, $N(x) = E(x) \le \sigma < 1$. Since $N(x)$ is a non-negative integer, $N(x) = 0$, that is, $f(x) = 0$ and $g(\bar{x}) = 0$. $\square$

**Lemma 3 (line L6).** If lines L2 to L5 do not return and $V = \emptyset$, then $f$ and $g$ are dual.

*Proof.* With no variables, each irredundant DNF is either $\emptyset$ (the constant 0) or $\{\emptyset\}$ (the constant 1). If both are $\{\emptyset\}$, line L2 returns. If both are $\emptyset$, then $\sigma = 0$ and line L5 returns. In the other two cases one function is 0 and the other is 1, so $f(\emptyset) \ne g(\emptyset)$, and $\emptyset$ is the only assignment. $\square$

**Lemma 4 (the split).** Let $v \in V$, $W = V \setminus \{v\}$, and $f = v f_1 \lor f_0$, $g = v g_1 \lor g_0$. For $y \subseteq W$, with complements over $W$:

- with $x = y \cup \{v\}$: $f(x) = (f_0 \lor f_1)(y)$ and $g(V \setminus x) = g_0(W \setminus y)$;
- with $x = y$: $f(x) = f_0(y)$ and $g(V \setminus x) = (g_0 \lor g_1)(W \setminus y)$.

So $f$ and $g$ are dual if and only if $f_0 \lor f_1$ and $g_0$ are dual and $f_0$ and $g_0 \lor g_1$ are dual. A witness $y$ of the first pair gives the witness $y \cup \{v\}$ of $f$ and $g$, and a witness $y$ of the second pair is a witness of $f$ and $g$.

*Proof.* If $v \in x$, a term $T \cup \{v\}$ with $T \in f_1$ is inside $x$ if and only if $T \subseteq y$, and a term of $f_0$ is inside $x$ if and only if it is inside $y$. And $V \setminus x = W \setminus y$ does not contain $v$, so only the terms of $g_0$ can lie inside it. The case $v \notin x$ is the same with the roles exchanged: $f$ can only use $f_0$, and $V \setminus x = (W \setminus y) \cup \{v\}$, so a term $T \cup \{v\}$ of $g$ lies inside it if and only if $T \subseteq W \setminus y$. Every $x \subseteq V$ is $y \cup \{v\}$ or $y$ for exactly one $y \subseteq W$. By Lemma 0, the smaller pairs may be tested with complements over their own variables, which are inside $W$. $\square$

**Theorem.** For any monotone DNFs $f$ and $g$, FK-DUAL$(f, g)$ terminates. It returns none if $f$ and $g$ are dual, and otherwise a witness $x \subseteq V$.

*Proof.* By induction on $|V|$. By Lemma 1, line L1 keeps the functions. If one of lines L2 to L5 returns, the result is a witness by Lemma 2, and then $f$ and $g$ are not dual. If line L6 returns none, they are dual by Lemma 3. Otherwise $V \ne \emptyset$, and the variable $v$ of line L7 exists. Both calls at lines L9 and L10 are on DNFs whose variables lie in $W = V \setminus \{v\}$, so by the induction hypothesis they terminate and answer correctly. By Lemma 4, if the first returns a witness $y$, then $y \cup \{v\}$ is a witness; if the second does, then $y$ is; and if both return none, then $f$ and $g$ are dual and line L11 returns none. $\blacksquare$

**Corollary (listing minimal transversals).** Let $H$ be a hypergraph with vertex set $V$ and no edge that contains another. Run the loop of the page: start with $g = \emptyset$, and while FK-DUAL$(H, g)$ returns a witness $x$, shrink $V \setminus x$ to a minimal transversal $t$ and add $t$ to $g$. The loop adds each minimal transversal of $H$ exactly once and then stops.

*Proof.* Every term of $g$ is a transversal, so it meets every edge, and line L2 never returns. Hence a witness $x$ cannot have $f(x) = g(\bar{x}) = 1$: that would give an edge $E \subseteq x$ and a term $t' \subseteq \bar{x}$ of $g$ with $E \cap t' = \emptyset$. So $f(x) = 0$ and $g(\bar{x}) = 0$. The first says that no edge lies in $x$, so every edge meets $\bar{x}$, and $\bar{x}$ is a transversal. The second says that no term of $g$ lies in $\bar{x}$. The greedy shrinking gives a minimal transversal $t \subseteq \bar{x}$, and $t \notin g$ since no term of $g$ lies in $\bar{x}$. So each round adds a new minimal transversal, and since there are finitely many, the loop stops. When it stops, $H$ and $g$ are dual, so $g$, which is irredundant, is the set of minimal terms of $H^d$. These are exactly the minimal transversals of $H$: $H^d(y) = \lnot H(\bar{y}) = 1$ if and only if no edge lies in $\bar{y}$, that is, if and only if $y$ meets every edge. $\square$
