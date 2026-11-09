---
title: Huet's union-find algorithm returns a most general unifier or fails correctly
proves: [correctness]
status: full
---

The input is a term DAG and two nodes $s$ and $t$. For a node $n$, $\operatorname{term}(n)$ is the term it denotes. A substitution $\theta$ *unifies* two nodes $u$ and $v$ if $\theta(\operatorname{term}(u)) = \theta(\operatorname{term}(v))$. We write $u \equiv v$ when $u$ and $v$ are in the same class, and $[u]$ for the class of $u$. Let $P$ be the set of all pairs that are ever pushed on the stack.

**Lemma 1 (the schema).** At each moment, the schema of a class is a function node if the class has one, and otherwise a variable of the class.

*Proof.* True after line L1. Line L10 keeps the schema $a$, a function node. Line L12 picks a function node if one of the two schemas is one; by the claim for the two old classes, the new class has a function node only in that case. $\square$

**Lemma 2 (unifiers respect the classes).** Let $\theta$ unify $s$ and $t$. Then $\theta$ unifies each pair in $P$, and $\theta$ unifies $u$ and $v$ whenever $u \equiv v$, at each moment of the run.

*Proof.* By induction on the steps. At the start $P = \{(s, t)\}$ and each class has one node. A union in line L10 or L12 merges the classes of $u$ and $v$ for a popped pair $(u', v')$ with $u' \in [u]$ and $v' \in [v]$. By induction $\theta$ unifies $(u', v')$ and is constant on both classes, so it is constant on the union. In line L11, $a \equiv b$ now, so $\theta(\operatorname{term}(a)) = \theta(\operatorname{term}(b))$. Both start with the same symbol, so $\theta(\operatorname{term}(a_i)) = \theta(\operatorname{term}(b_i))$ for each $i$. $\square$

**Lemma 3 (failure is correct).** If the algorithm returns fail, $s$ and $t$ have no unifier.

*Proof.* Assume $\theta$ unifies $s$ and $t$. In line L9, $a \equiv b$ would hold after the union, but by Lemma 2 for the pair being merged, $\theta(\operatorname{term}(a)) = \theta(\operatorname{term}(b))$ with different head symbols, which is impossible. In line L15, take a cycle $C_0 \to C_1 \to \cdots \to C_k = C_0$ in $G$. By Lemma 2, $\theta$ maps all nodes of a class $C$ to one term $\theta(C)$. An edge $C \to C'$ means that the schema of $C$ is a function node with a child in $C'$, so $\theta(C')$ is a proper subterm of $\theta(C)$ and is strictly smaller. Around the cycle, $\theta(C_0)$ would be strictly smaller than itself. $\square$

**Lemma 4 (the classes are closed downward).** When the loop of line L3 ends without failure, each function node $b$ has the same symbol as the schema $a$ of its class, and $b_i \equiv a_i$ for each argument place $i$.

*Proof.* Classes only grow, so it is enough to show that each such equivalence holds at some moment. We follow the unions. A function node $b$ is the schema of its own class at the start. Its schema changes only in line L10, when its class (with schema $b$) is merged with a class with schema $a$. The symbols agree by line L9, and line L11 pushes $(a_i, b_i)$. Each pushed pair is popped later, and after line L5 or line L10 or line L12 its two nodes are in one class. So $a_i \equiv b_i$ at the end. If the schema $a$ itself later loses its role to a schema $a'$, the same argument gives $a_i \equiv a'_i$, and $\equiv$ is transitive. A merge in line L12 adds no function node to a class with a function schema, other than through the class whose schema is kept, by Lemma 1. $\square$

Now assume that the algorithm reaches line L16. The graph $G$ has no cycle, so the term $\operatorname{read}(C)$ of each class is finite. It is defined by $\operatorname{read}(C) = f(\operatorname{read}([a_1]), \ldots, \operatorname{read}([a_k]))$ if the schema of $C$ is the function node $a$ with symbol $f$, and $\operatorname{read}(C) = z$ if the schema is the variable $z$. Then $\sigma(x) = \operatorname{read}([x])$.

**Lemma 5.** For each node $n$, $\sigma(\operatorname{term}(n)) = \operatorname{read}([n])$.

*Proof.* By induction along $G$, which has no cycle, and then on the depth of $n$. If $n$ is a variable, this is the definition of $\sigma$. If $n$ is a function node with symbol $f$ and children $n_1, \ldots, n_k$, then $\sigma(\operatorname{term}(n)) = f(\operatorname{read}([n_1]), \ldots, \operatorname{read}([n_k]))$ by induction. By Lemma 4, $[n_i] = [a_i]$ for the schema $a$ of $[n]$, and $a$ has the symbol $f$. So the result is $\operatorname{read}([n])$. $\square$

**Theorem.** If the algorithm returns $\sigma$, then $\sigma$ is a most general unifier of $s$ and $t$. If it returns fail, there is no unifier.

*Proof.* The second statement is Lemma 3. For the first, $s \equiv t$ after the first pair is processed, so Lemma 5 gives $\sigma(s) = \operatorname{read}([s]) = \sigma(t)$.

Let $\theta$ be any unifier. By Lemma 2, $\theta$ is constant on each class, with value $\theta(C)$. We show $\theta(\operatorname{read}(C)) = \theta(C)$ by induction along $G$. If the schema of $C$ is a variable $z$, then $\operatorname{read}(C) = z$ and $\theta(z) = \theta(C)$. If the schema is a function node $a$ with symbol $f$, then $\theta(\operatorname{read}(C)) = f(\theta([a_1]), \ldots, \theta([a_k])) = \theta(\operatorname{term}(a)) = \theta(C)$. So for each variable $x$, $\theta(\sigma(x)) = \theta(\operatorname{read}([x])) = \theta([x]) = \theta(x)$. This means $\theta = \theta \circ \sigma$, so $\sigma$ is more general than $\theta$. $\blacksquare$

**Termination and cost.** Each union lowers the number of classes, so there are at most $N - 1$ unions. A pair is pushed in line L11 only when the class with schema $b$ is merged into a class with another function schema; after that $b$ is never a schema again. So each function node causes at most one push of its children, and the number of pushes is at most $1$ plus the total arity, which is $O(N)$. Each pop does two FIND calls. The tests compare the result with a reference implementation of Robinson's algorithm on 3000 random pairs of terms.
