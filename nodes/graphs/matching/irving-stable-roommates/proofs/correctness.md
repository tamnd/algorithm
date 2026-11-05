---
title: Irving's algorithm returns a stable matching exactly when one exists
proves: [correctness, termination]
status: full
---

**Setting.** The agents form a set $V$ with $|V| = n$. After line L1, the lists are symmetric: $b$ is on the list of $a$ if and only if $a$ is on the list of $b$. The *table* $T$ is the current set of lists; it only loses entries, and every deletion of a pair $\{a, b\}$ removes both entries. A matching $M$ is *contained* in $T$ if each pair of $M$ is in $T$. We write $b \succ_a c$ when $a$ ranks $b$ above $c$ on its original list, and $\text{first}$, $\text{second}$, $\text{last}$ refer to the current table. Pairs removed at line L1 are not acceptable, so no matching uses them, and they never block.

Every deletion is made by a *truncation*: "delete all $z$ after $c$ on the list of $a$" at line L6 or L14, which deletes each pair $\{a, z\}$ with $c \succ_a z$ still present. We say that $a$ *made* the deletion, *keeping* $c$. Truncation is by rank, so it is well defined even if $c$ is no longer on the list of $a$.

**Lemma 1 (phase 1 holders).** During phase 1:

(a) if $\text{holder}[y] = x$, then $\text{first}(x) = y$ and $\text{last}(y) = x$;
(b) each agent $x$ with a nonempty list is in $F$ or equals $\text{holder}[\text{first}(x)]$;
(c) once an agent has received a proposal, it has a holder at the end of every later iteration of line L3.

*Proof.* At line L2, (a) and (c) say nothing and (b) holds since $F = V$. Consider one iteration in which $x$ is popped with a nonempty list, and let $y = \text{first}(x)$. By symmetry, $x$ is on the list of $y$, so $\text{first}(y) \succeq_y x$, and line L6 deletes exactly the pairs $\{y, z\}$ with $x \succ_y z$. After it, $\text{last}(y) = x$.

Take any other holder relation $\text{holder}[v] = w$ from before the iteration, so $\text{first}(w) = v$ and $\text{last}(v) = w$ by (a). If $v = y$, then $w$ is the old holder of $y$; if line L6 deletes $\{y, w\}$, DELETE sets $\text{holder}[y]$ to nil and puts $w$ back into $F$, and in any case line L7 replaces the holder of $y$. If $v \ne y$, the pair $\{w, v\}$ is not deleted: it would have to be $\{y, z\}$ with $w = y$ and $v = z$, so $z = \text{first}(y) \succeq_y x \succ_y z$, which is impossible. Entries are never added, so $\text{first}(w) = v$ still holds. The list of $v$ loses at most the entry $y \ne w$, so $\text{last}(v) = w$ still holds. Line L7 gives (a) for the new pair $(x, y)$ and (b) for $x$. An agent that loses its holder relation is put into $F$, so (b) holds for every agent. For (c), only line L6 for the same $y$ can remove the holder of $y$, and line L7 gives $y$ a holder at once. $\square$

**Lemma 2 (phase 1 terminates; the stable table).** Phase 1 stops after at most $n + m$ pops. Let $A$ be the set of agents with nonempty lists at its end, and $f(x) = \text{first}(x)$ for $x \in A$. Then $f$ is a bijection of $A$ onto $A$, and $\text{last}(f(x)) = x$ for each $x \in A$. Every agent outside $A$ has an empty list.

*Proof.* An agent is pushed into $F$ only at line L2 or when a pair is deleted (one push per deletion), and at most $m$ pairs exist. So there are at most $n + m$ pops. At the end $F$ is empty, so by Lemma 1(b) each $x \in A$ is the holder of $f(x)$. The agent $f(x)$ has $x$ on its list, so $f(x) \in A$. Distinct agents hold distinct agents, so $f$ is injective, hence a bijection of the finite set $A$. Lemma 1(a) gives $\text{last}(f(x)) = x$. $\square$

We call a table with properties of Lemma 2 (symmetric, $f$ a bijection of $A$, $\text{last} \circ f = \text{id}$ on $A$, lists outside $A$ empty) a *stable table on $A$*. In a stable table, $\text{last} = f^{-1}$, so $\text{last}(y) = x$ if and only if $\text{first}(x) = y$.

**Lemma 3 (phase 1 deletes no stable pair).** No pair deleted in phase 1 belongs to a stable matching.

*Proof.* Suppose some stable matching $M$ contains a pair deleted in phase 1, and take the first such deletion: at line L6, $x$ proposes to $y = \text{first}(x)$ and $\{y, z\}$ is deleted with $x \succ_y z$ and $\{y, z\} \in M$. The agents that $x$ ranks above $y$ had all been deleted from its list before, by earlier deletions, so by the choice of the first deletion none of them is the partner of $x$ in $M$. The partner of $x$ is not $y$, as $y$ is matched to $z \ne x$. So $x$ is single in $M$ or prefers $y$ to its partner, and $y$ prefers $x$ to $z$. The pair $\{x, y\}$ is acceptable and blocks $M$, a contradiction. $\square$

**Lemma 4 (cover).** Let $T$ be a table that is contained in a stable table $T_1$ on $A$, and let $M$ be a stable matching contained in $T$. Then $M$ matches every agent of $A$, and no agent outside $A$.

*Proof.* Agents outside $A$ have empty lists in $T_1$, so they are single. Use $f$ and $\text{last}$ of $T_1$. Each $w \in A$ matched in $M$ has its partner on its list in $T_1$, so $f(w) \succeq_w M(w)$, and $M(y) \succeq_y \text{last}(y)$ for each matched $y$.

Suppose $x \in A$ is single in $M$. Define $u_1 = x$ and $y_1 = f(u_1)$. We claim: for each $k \ge 1$, $u_k$ is single or prefers $y_k = f(u_k)$ to $M(u_k)$, and then $y_k$ is matched and $u_{k+1} = M(y_k)$ is defined with the same property. Indeed, $\{u_k, y_k\}$ is acceptable and $u_k$ would like $y_k$, so, as $M$ is stable, $y_k$ is matched to some $u_{k+1}$ with $u_{k+1} \succ_{y_k} u_k$; in particular $u_{k+1} \ne u_k = \text{last}(y_k)$, so $f(u_{k+1}) \ne y_k$. As $y_k = M(u_{k+1})$ is on the list of $u_{k+1}$ in $T_1$ and is not its first entry, $u_{k+1}$ prefers $y_{k+1} = f(u_{k+1})$ to $M(u_{k+1})$. This proves the claim. So $y_{k+1} = h(y_k)$ with $h = f \circ M$, an injective map on the matched agents of $A$. The agent $y_1 = f(x)$ is not in the image of $h$, because $f$ is injective and $x$ is nobody's partner. The sequence $y_1, y_2, \ldots$ lies in a finite set, so it repeats: let $y_i = y_j$ with $i < j$ and $j$ least. If $i > 1$, injectivity gives $y_{i-1} = y_{j-1}$, against the choice of $j$. So $y_1 = y_j = h(y_{j-1})$, a contradiction. $\square$

By Lemma 3, every stable matching is contained in the table $T_1$ after phase 1. By Lemma 4, every stable matching matches exactly the agents of $A$.

**Invariant of phase 2.** At each test of line L10, the table $T$ is a stable table on $A$, contained in $T_1$, and

(P) if some stable matching exists, then $T$ contains one.

At the first test this holds by Lemmas 2 and 3. We show that each pass of the loop keeps it or returns correctly.

**Lemma 5 (the walk).** In a stable table on $A$, if $|\text{list}(x)| \ge 2$ and $p = \text{last}(\text{second}(x))$, then $p \ne x$ and $|\text{list}(p)| \ge 2$.

*Proof.* Let $y = \text{second}(x)$. Then $f(p) = y$, while $f(x) \ne y$, so $p \ne x$. The list of $y$ contains $x$ (by symmetry) and $p$, two different agents. If the list of $p$ were $\{y\}$ alone, then since $f$ is onto, $p = f(w)$ for some $w$ on the list of $p$, so $w = y$ and $f(y) = p = \text{last}(y)$; the first and last entries of $y$ would be equal, so $y$ would have one entry, a contradiction. $\square$

After line L10, each agent of $S$ has at least 2 entries and each next agent of $S$ is $\text{last}(\text{second}(\cdot))$ of the one before it. Line L11 pushes an agent with at least 2 entries. By Lemma 5, each push at line L12 is an agent with at least 2 entries, so $\text{second}$ is defined at each step. The stack holds distinct agents and $A$ is finite, so line L12 stops. The agents $x_0, \ldots, x_{r-1}$ taken at line L13 are distinct, satisfy $x_{i+1} = \text{last}(\text{second}(x_i))$ with indices modulo $r$, and $r \ge 2$ by Lemma 5. Put $y_i = f(x_i)$. Since $f(x_{i+1}) = \text{second}(x_i)$, we have $\text{second}(x_i) = y_{i+1}$. The $y_i$ are distinct because $f$ is injective. On the list of $y_{i+1}$, the agent $x_i$ comes strictly before its last entry $x_{i+1}$. Line L14 deletes the set $D$ of pairs $\{y_{i+1}, z\}$ with $x_i \succ_{y_{i+1}} z$; since truncation is by rank, the result is $T' = T \setminus D$ whatever the order. $D$ contains every pair $\{x_i, y_i\}$.

**Lemma 6 (deleted pairs never block).** At any time, each pair deleted so far was made by an agent $a$ keeping some $c$ with $c \succ_a$ (the other agent), and every entry still on the list of $a$ is $\succeq_a c$.

Moreover, $a \in A$, and while no list of $A$ is empty the list of $a$ is not empty.

*Proof.* At the deletion, all entries of $a$ after $c$ were removed, and lists only lose entries. In phase 1, $a$ is an agent that received a proposal, so it has a holder at the end of phase 1 by Lemma 1(c), and its list is not empty; so $a \in A$. In phase 2, $a$ is some $y_{i+1} \in A$. $\square$

**Lemma 7 (elimination keeps a stable matching).** If $T$ contains a stable matching $M$, then $T'$ contains a stable matching, and no list of $A$ is empty in $T'$.

*Proof.* By Lemma 4, $M$ matches every agent of $A$, and $M(w) \preceq_w f(w)$ in $T$, $M(y) \succeq_y \text{last}(y)$.

*If $M$ contains one pair $\{x_i, y_i\}$, it contains all of them.* Suppose $\{x_i, y_i\} \in M$. The agent $x_{i-1}$ is on the list of $y_i$ before $x_i = \text{last}(y_i) = M(y_i)$, so $y_i$ prefers $x_{i-1}$ to its partner. As $M$ is stable, $x_{i-1}$ prefers its partner to $y_i = \text{second}(x_{i-1})$; its partner is on its list in $T$, so it is $\text{first}(x_{i-1}) = y_{i-1}$. Going back around the cycle gives all pairs.

*Case 1: no pair $\{x_i, y_i\}$ is in $M$.* Suppose a pair $\{y_{i+1}, z\} \in D$ is in $M$, with $x_i \succ_{y_{i+1}} z$. The partner of $x_i$ is on its list and is not $y_i$, so it is $y_{i+1}$ or worse for $x_i$; it is not $y_{i+1}$, whose partner is $z \ne x_i$. So $x_i$ prefers $y_{i+1}$ to its partner and $y_{i+1}$ prefers $x_i$ to $z$, and $\{x_i, y_{i+1}\}$ blocks $M$. So $M \cap D = \emptyset$ and $M$ is contained in $T'$.

*Case 2: all pairs $\{x_i, y_i\}$ are in $M$.* Let $M' = (M \setminus \{x_i y_i\}) \cup \{x_i y_{i+1}\}$. The $x_i$ and the $y_i$ are distinct, so $M'$ is a matching contained in $T$. In $M'$, the partner of $y_{i+1}$ is $x_i$, which is not after $x_i$, and no other pair of $M'$ contains a $y_j$, so $M' \cap D = \emptyset$ and $M'$ is contained in $T'$. $M'$ is stable: compared with $M$, each $y_{i+1}$ has a better partner ($x_i$ instead of its last entry $x_{i+1}$), each $x_i$ has a worse one, and the others are unchanged. So a pair that blocks $M'$ but not $M$ contains some $x_i$ and an agent $b$ with $b \succ_{x_i} y_{i+1}$. If $b$ is on the list of $x_i$ in $T$, then $b = y_i$, whose partner in $M'$ is $x_{i-1} \succ_{y_i} x_i$; no block. Otherwise $\{x_i, b\}$ was deleted; by Lemma 6 the agent $a$ that made it is in $A$, so it is matched in $M'$, and it prefers every entry of its list in $T$, in particular its partner in $M'$, to the other agent. So $\{x_i, b\}$ does not block.

In both cases $T'$ contains a stable matching, which matches all of $A$ (Lemma 4 applies, since $T' \subseteq T_1$), so no list of $A$ is empty in $T'$. $\square$

**Lemma 8 (elimination keeps a stable table).** If no list of $A$ is empty in $T'$, then $T'$ is a stable table on $A$, with $f'(x_i) = y_{i+1}$ and $f'(w) = f(w)$ for $w$ not in the rotation.

*Proof.* Symmetry is kept, as deletions are symmetric. Which agents lose their first entry? A pair $\{w, f(w)\} \in D$ has the form $\{y_{k+1}, z\}$ with $x_k \succ_{y_{k+1}} z$. It cannot be $w = y_{k+1}$, $z = f(w)$, since the first entry of $y_{k+1}$ is not after $x_k$, which is on its list. So $w = z$ and $f(w) = y_{k+1}$, that is $w = x_{k+1}$. Hence only the $x_i$ lose their first entry, and $f'(w) = f(w)$ for the others.

The second entry $y_{i+1}$ of $x_i$ stays, unless $\{x_i, y_{i+1}\} \in D$. The truncation of $y_{i+1}$ keeps $x_i$. The only other way is $x_i = y_{k+1}$ for some $k$ with $x_k \succ_{x_i} y_{i+1}$, so $x_k$ is the first entry of $x_i$: $x_k = f(x_i) = y_i$. Then $\text{last}(x_k) = \text{last}(f(x_i)) = x_i$ and $\text{second}(x_k) = y_{k+1} = x_i$, so the list of $x_k$ is exactly $y_k, x_i$. The pair $\{x_k, y_k\}$ is in $D$, and $x_k = y_i$ truncates after $x_{i-1}$, which is on its list and differs from $x_i$, so it equals $y_k$, and $\{x_k, x_i\} \in D$. Then the list of $x_k$ is empty in $T'$, which is excluded. So $f'(x_i) = y_{i+1} = f(x_{i+1})$, and $f'$ is a bijection of $A$: it equals $f$ with the images on the rotation shifted cyclically.

Last entries: for $w$ not in the rotation, $b = f(w)$ is not a $y_j$, so its list is not truncated; the pair $\{w, b\}$ is not in $D$ (shown above), and lists only lose entries, so $\text{last}'(b) = w$. For $x_i$, the list of $y_{i+1}$ keeps $x_i$, which was shown to stay, and loses all entries after it, so $\text{last}'(y_{i+1}) = x_i$. So $\text{last}' \circ f' = \text{id}$ on $A$, and lists outside $A$ stay empty. $\square$

**The loop.** If line L15 finds an empty list of $A$, then by Lemma 7, $T$ contains no stable matching, so by (P) none exists, and "no stable matching" is correct. Otherwise, by Lemma 8 and Lemma 7, $T'$ is a stable table on $A$ satisfying (P): if a stable matching exists, $T$ contains one, and then so does $T'$.

**Termination.** Each elimination deletes the $r \ge 2$ pairs $\{x_i, y_i\}$, and there are at most $m$ pairs, so there are at most $m/2$ passes of the loop. Each pass stops, as shown after Lemma 5.

**The output is stable.** The loop exits at line L11 when no list has 2 or more entries. No list of $A$ is empty (it would have been caught at line L15, and after phase 1 lists of $A$ are nonempty), so each $x \in A$ has the one entry $f(x)$. By symmetry the list of $f(x)$ is $\{x\}$, so the pairs $\{x, f(x)\}$ form a matching $M$ of $A$, using acceptable pairs only. Let $\{a, b\}$ be an acceptable pair not in $M$. It is not in the final table, so it was deleted, by an agent, say $a$, keeping some $c \succ_a b$. By Lemma 6, $a \in A$ and the one entry $M(a)$ of its final list satisfies $M(a) \succeq_a c$. So $M(a) \succeq_a c \succ_a b$, and $a$ does not prefer $b$. No pair blocks $M$, and line L16 returns a stable matching. $\blacksquare$
