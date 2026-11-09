---
title: The 2-SAT algorithm answers UNSAT exactly when the formula has no model, and else returns a model
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page. $F$ is a 2-CNF formula over the variables $x_1, \ldots, x_n$, and each clause has at most two literals. A unit clause $(a)$ is treated as $(a \vee a)$: it has the same models, and line L4 adds the arc $\neg a \to a$ for it. For a literal $\ell$, $\neg\ell$ is its complement, with $\neg\neg x = x$. $G$ is the graph of lines L2 to L4, with one vertex for each of the $2n$ literals. We write $u \leadsto w$ when $G$ has a directed path from $u$ to $w$ (of length 0 or more).

**Fact (Tarjan's numbering).** Line L5 gives each vertex the number $comp[u]$ of its strongly connected component, in the order in which Tarjan's algorithm finishes the components. Two vertices have the same number if and only if they are in the same component, and for each arc $u \to w$ we have $comp[u] \ge comp[w]$. This is the correctness theorem of [Tarjan's algorithm](/tarjan-scc/): a component is finished only after each component that it reaches. So $u \leadsto w$ implies $comp[u] \ge comp[w]$, by induction on the length of the path.

**Lemma 1 (each arc is an implication).** Let $\alpha$ be a model of $F$. If $u \leadsto w$ and $\alpha$ makes $u$ true, then $\alpha$ makes $w$ true.

*Proof.* Take one arc first. An arc $\neg a \to b$ or $\neg b \to a$ comes from a clause $(a \vee b)$ of $F$, and $\alpha$ makes this clause true. If $\alpha$ makes $\neg a$ true, then $a$ is false, so $b$ is true. The case of $\neg b \to a$ is the same. For a path, apply this to each arc in turn. $\square$

**Lemma 2 (symmetry).** If $G$ has the arc $u \to w$, then it has the arc $\neg w \to \neg u$. So $u \leadsto w$ implies $\neg w \leadsto \neg u$.

*Proof.* Line L4 adds the arcs of a clause $(a \vee b)$ in pairs: $\neg a \to b$ and $\neg b \to a$. The second arc is the contrapositive of the first, and the first is the contrapositive of the second. For a path, reverse it and take the contrapositive of each arc. $\square$

**Theorem.** TWO-SAT$(F, n)$ stops. It returns UNSAT if and only if $F$ has no model. When it returns $x$, the assignment $x$ is a model of $F$.

*Proof.* Termination: line L5 stops by the correctness of Tarjan's algorithm, and each other line is a loop over a finite list. We show three claims.

*Claim A. If line L1 returns UNSAT, then $F$ has no model.* An empty clause has no true literal under any assignment.

*Claim B. If line L7 returns UNSAT, then $F$ has no model.* Line L7 returns when $comp[x_v] = comp[\neg x_v]$ for some $v$. Then $x_v \leadsto \neg x_v$ and $\neg x_v \leadsto x_v$. Assume that $F$ has a model $\alpha$. If $\alpha(x_v)$ is true, then by Lemma 1 $\neg x_v$ is true, which is false. If $\alpha(x_v)$ is false, then $\neg x_v$ is true, and by Lemma 1 $x_v$ is true, which is false. Both cases fail, so $F$ has no model.

*Claim C. If the algorithm reaches line L9, then $x$ is a model of $F$.* At line L8, no variable has $comp[x_v] = comp[\neg x_v]$, because line L7 did not return. Line L8 sets $x_v$ true exactly when $comp[x_v] < comp[\neg x_v]$. So for each literal $\ell$, of either sign,
$$\ell \text{ is true under } x \iff comp[\ell] < comp[\neg\ell], \qquad \ell \text{ is false under } x \iff comp[\ell] > comp[\neg\ell]. \tag{1}$$
For a positive literal this is line L8. For $\ell = \neg x_v$, the literal is true exactly when $x_v$ is false, that is when $comp[x_v] > comp[\neg x_v]$, which is $comp[\ell] < comp[\neg \ell]$.

Assume that a clause $(a \vee b)$ of $F$ is false under $x$, so $a$ and $b$ are both false. By (1), $comp[a] > comp[\neg a]$ and $comp[b] > comp[\neg b]$. The arc $\neg a \to b$ gives $comp[\neg a] \ge comp[b]$ by the fact above, and the arc $\neg b \to a$ gives $comp[\neg b] \ge comp[a]$. Put these in a chain:
$$comp[a] > comp[\neg a] \ge comp[b] > comp[\neg b] \ge comp[a].$$
So $comp[a] > comp[a]$, which is false. So no clause is false under $x$, and $x$ is a model. The same chain covers a unit clause $(a)$, with $b = a$.

Now the theorem follows. If $F$ has no model, Claim C shows that the algorithm cannot reach line L9, so it returns UNSAT at line L1 or line L7. If $F$ has a model, Claims A and B show that lines L1 and L7 do not return, so the algorithm reaches line L9 and returns a model by Claim C. $\blacksquare$

**Remark (why the rule is the right one).** Lemma 2 is not used in the proof above, but it explains rule L8. It shows that the map $u \mapsto \neg u$ sends each component to a component, and reverses the arcs of the [condensation](/condensation-graph/). Line L8 makes true the literal whose component is nearer to a sink of the condensation. A true literal then never has an arc to a false literal, because a false literal is nearer to a source than its complement.
