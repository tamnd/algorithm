---
title: Type-based alias analysis is sound for every run of a well-typed program, and each of its three forms refines the one before
proves: [correctness, termination, complexity]
status: full
---

**Setting.** A program has a tree of classes, where $C \le D$ means that $C$ is $D$ or a descendant of $D$, and $Sub(D) = \{C : C \le D\}$. Each field $f$ is declared in one class and has a declared type $FT(f)$; field names are unique. Each variable $v$ has a declared class $T(v)$. The statements are `p = new C`, `p = q`, `p = q.f` and `q.f = p`, with the typing rules $C \le T(p)$, $T(q) \le T(p)$, $FT(f) \le T(p)$ with $f$ declared in an ancestor of $T(q)$, and $T(p) \le FT(f)$ with $f$ declared in an ancestor of $T(q)$. The *type of the source* and the *type of the target* of a statement are $(C, T(p))$, $(T(q), T(p))$, $(FT(f), T(p))$ and $(T(p), FT(f))$, in the four forms. Lines L1 to L3 put each class in its own group and merge the groups of the two types of every statement where they differ. $G(C)$ is the final group of $C$, and line L4 sets $TypeRefs(D) = Sub(D) \cap G(D)$.

A *run* executes the statements in any order, any number of times, from a state where no variable and no field holds an object. This covers every path of the control flow graph. A statement that reads a variable or field with no object does not run. A reference $q.f$ *touches* the field $f$ of the object that $q$ holds when its statement runs. The three answers for two references $q_1.f_1$ and $q_2.f_2$ are:

- TypeDecl: $Sub(FT(f_1)) \cap Sub(FT(f_2)) \ne \emptyset$;
- FieldTypeDecl: $f_1 = f_2$ and $Sub(T(q_1)) \cap Sub(T(q_2)) \ne \emptyset$;
- SMTypeRefs (lines L6 and L7): $f_1 = f_2$ and $TypeRefs(T(q_1)) \cap TypeRefs(T(q_2)) \ne \emptyset$.

**Lemma 1 (the run invariant).** At every state of every run, for every variable $v$ that holds an object $o$ of class $D$, $D \le T(v)$ and $D \in G(T(v))$; and for every object whose field $f$ holds an object of class $D$, the field is declared in an ancestor of the class of the holder, $D \le FT(f)$, and $D \in G(FT(f))$.

*Proof.* By induction over the steps of the run. At the start nothing holds an object. Take a step.

- `p = new C` makes an object of class $C$, and $C \le T(p)$ by the typing rule. If $C \ne T(p)$, line L3 merged their groups, so $C \in G(T(p))$.
- `p = q` moves an object of class $D$ from $q$ to $p$. By the hypothesis, $D \le T(q) \le T(p)$, and $D \in G(T(q)) = G(T(p))$, since line L3 merged the two groups if the types differ.
- `p = q.f` reads the field $f$ of the object in $q$, which exists by the hypothesis and holds an object of class $D$ with $D \le FT(f) \le T(p)$ and $D \in G(FT(f)) = G(T(p))$.
- `q.f = p` writes the object of class $D$ in $p$ into the field $f$ of the object $o$ in $q$. The class $E$ of $o$ has $E \le T(q)$, and $f$ is declared in an ancestor of $T(q)$, so also of $E$. Then $D \le T(p) \le FT(f)$, and $D \in G(T(p)) = G(FT(f))$.

No other holder changes, so the invariant holds after the step. $\square$

**Theorem 1 (soundness).** If the references $q_1.f_1$ and $q_2.f_2$ touch the same field of the same object in some run, then SMTypeRefs, FieldTypeDecl and TypeDecl all answer that they may alias.

*Proof.* They touch the field $f_1 = f_2$ of one object $o$ of class $D$, held by $q_1$ and by $q_2$ at the two moments. By Lemma 1, $D \le T(q_i)$ and $D \in G(T(q_i))$ for $i = 1, 2$, so $D \in TypeRefs(T(q_1)) \cap TypeRefs(T(q_2))$, and SMTypeRefs answers yes. The other two answer yes by Theorem 2. $\square$

**Theorem 2 (each form refines the one before).** If SMTypeRefs answers yes, FieldTypeDecl does; if FieldTypeDecl answers yes, TypeDecl does.

*Proof.* $TypeRefs(D) \subseteq Sub(D)$, so a common element of the two sets of TypeRefs is a common subtype. If FieldTypeDecl answers yes, then $f_1 = f_2$, so $FT(f_1) = FT(f_2)$, and $FT(f_1) \in Sub(FT(f_1)) \cap Sub(FT(f_2))$. $\square$

The same argument shows that a points-to analysis that respects the typing rules is at least as precise as SMTypeRefs: if the abstract flow of an allocation site of class $D$ reaches both $q_1$ and $q_2$ along statements of the program, every holder on the way has $D$ below its type and in its group, so $D$ is in both sets of TypeRefs.

**Theorem 3 (time).** With $t$ classes of a tree of height $h$, $m$ statements and a union-find forest with path compression in lines L1 to L3, the groups take $O(t + m \log t)$ time, and $O((t + m)\,\alpha(t + m))$ time with union by rank as well; and the table of TypeRefs takes $O(t^2 h)$ time and $O(t^2)$ space. Each query then takes $O(t)$ time, or $O(1)$ with a $t \times t$ table of the answers built in $O(t^3)$ time.

*Proof.* Lines L1 to L3 make $t$ groups and at most $m$ unions. Line L4 tests $C \le D$ for every pair, each by a walk up the tree of at most $h$ steps, and one find per pair. A query compares two subsets of the $t$ classes. $\square$

The analysis does not look at the statements again for each query, and it does not depend on the order of the statements, so it is flow-insensitive in the same sense as the points-to analyses: it ignores the order, not the statements that the control flow gives.
