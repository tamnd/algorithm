---
title: ML typability is in DEXPTIME, and it is DEXPTIME-hard
proves: [statement]
status: sketch
---

This file proves the two halves of the theorem. The upper bound (part 1) and the size bounds (part 3) have full proofs. They use only the principal type theorem and the copying property of `let`. The lower bound (part 2) is a sketch of a simulation of an exponential time Turing machine. It follows the plan of Mairson (1990): truth values are encoded as types, a circuit is computed by type inference, and nested `let` repeats a step exponentially many times. The encoding of the tape below is one way to fill in the plan. Mairson (1990) and Kfoury, Tiuryn and Urzyczyn (1990, 1994) give complete proofs.

## Setting

Terms, types and the syntax-directed rules are those of the [Hindley-Milner page](/hindley-milner-type-system/), with T-Var', T-Abs, T-App and T-Let', the constants, `if` and the operators. The *size* $|e|$ of a term is the number of nodes of its syntax tree. A variable or a constant has size 1, and each `fun`, application, `let`, `if` and operator adds 1 to the sizes of its parts. We rename bound term variables so that they are all different and different from the free variables, which changes no size and no type.

Two standard facts about derivations are used. *Type substitution:* if $\Gamma \vdash e : \tau$, then $S\Gamma \vdash e : S\tau$. *Weakening and strengthening:* adding to $\Gamma$ a binding for a variable that is not free in $e$, or removing one, does not change the types of $e$. Both are proved by induction on derivations, after the generalized variables of each inner `let` are renamed apart. Weakening is the lemma on a more general context of the [W proof](/algorithm-w/) in a special case.

## Lemma 1: `let` by copying

**Lemma 1.** Let $x \notin \mathrm{dom}(\Gamma)$. Then $\Gamma \vdash \texttt{let } x = e_1 \texttt{ in } e_2 : \tau$ if and only if $\Gamma \vdash e_1 : \tau_1$ for some $\tau_1$ and $\Gamma \vdash [x := e_1]\,e_2 : \tau$.

*Proof.* (Only if.) T-Let' gives $\Gamma \vdash e_1 : \tau_1$ and $\Gamma, x : \sigma \vdash e_2 : \tau$ with $\sigma = \mathrm{Gen}(\Gamma, \tau_1)$. Each leaf of the second derivation that uses $x$ is a T-Var' step $\Gamma, \Delta, x : \sigma \vdash x : \tau'$ with $\sigma \sqsubseteq \tau'$. The substitution that sends the bound variables of $\sigma$ to the chosen types does not touch $\mathrm{ftv}(\Gamma)$, so type substitution gives $\Gamma \vdash e_1 : \tau'$, and weakening gives $\Gamma, \Delta \vdash e_1 : \tau'$. Put this derivation in place of the leaf. The result is a derivation of $\Gamma \vdash [x := e_1]\,e_2 : \tau$.

(If.) If $x$ does not occur in $e_2$, use T-Let' with $\mathrm{Gen}(\Gamma, \tau_1)$ and weakening. Otherwise let $\tau_1', \ldots, \tau_m'$ be the types of the $m$ copies of $e_1$ in the derivation of $[x := e_1]\,e_2$. By strengthening, $\Gamma \vdash e_1 : \tau_j'$ for each $j$. We need one type $\tau^*$ with $\Gamma \vdash e_1 : \tau^*$ such that each $\tau_j'$ is an instance of $\mathrm{Gen}(\Gamma, \tau^*)$.

Let $W(\Gamma, e_1) = (S, \tau_0)$. By the completeness of W (in the [proof file of algorithm W](/algorithm-w/)) with $R$ the identity, for each $j$ there is $R_j$ with $R_j\tau_0 = \tau_j'$ and $R_j S \Gamma = \Gamma$. All the $R_j$ agree on the variables of $S\Gamma$, because $R_j\alpha$ is the subterm of $\Gamma$ at the place where $\alpha$ occurs in $S\Gamma$. So these images only contain variables of $\Gamma$. Let $R^*$ agree with them on $\mathrm{ftv}(S\Gamma)$, and let it send each other variable of $\tau_0$ to its own fresh variable. Put $\tau^* = R^*\tau_0$. By the soundness of W and type substitution, $\Gamma = R^*S\Gamma \vdash e_1 : \tau^*$. The substitution $Q_j$ that sends each fresh variable back to the image of its original under $R_j$ gives $Q_j\tau^* = \tau_j'$, and it only moves fresh variables, which are not free in $\Gamma$. So $\mathrm{Gen}(\Gamma, \tau^*) \sqsubseteq \tau_j'$. Replace the derivation of each copy by a T-Var' step for $x : \mathrm{Gen}(\Gamma, \tau^*)$ at the instance $\tau_j'$. This gives $\Gamma, x : \mathrm{Gen}(\Gamma, \tau^*) \vdash e_2 : \tau$, and T-Let' finishes. $\square$

## Lemma 2: the expansion

Define a term $\mathrm{exp}(e)$ with no `let`. It commutes with every form of term except `let`, and

$$\mathrm{exp}(\texttt{let } x = e_1 \texttt{ in } e_2) = (\texttt{fun } z \texttt{ -> } [x := \mathrm{exp}(e_1)]\,\mathrm{exp}(e_2))\ \mathrm{exp}(e_1),$$

with $z$ fresh. The extra argument makes sure that $e_1$ is checked even when $x$ is not used.

**Lemma 2.** For each $\Gamma$ and $\tau$: $\Gamma \vdash e : \tau$ if and only if $\Gamma \vdash \mathrm{exp}(e) : \tau$.

*Proof.* By induction on $e$, for all $\Gamma$ at once. All cases but `let` follow from the induction hypothesis, since the rules for them only look at the types of the parts. For `let`, write $e_i' = \mathrm{exp}(e_i)$. By T-Let' and the induction hypothesis in the contexts $\Gamma$ and $\Gamma, x : \mathrm{Gen}(\Gamma, \tau_1)$, the term $\texttt{let } x = e_1 \texttt{ in } e_2$ has the same types as $\texttt{let } x = e_1' \texttt{ in } e_2'$. By Lemma 1, these are the types of $[x := e_1']\,e_2'$, under the condition that $e_1'$ has a type. T-App and T-Abs with an unused $z$ express exactly this condition. $\square$

**Lemma 3.** $|\mathrm{exp}(e)| \le 4^{|e|}$.

*Proof.* By induction on $e$. A variable or constant has size $1 \le 4$. For `fun`, $1 + 4^a \le 4^{a+1}$. For an application, $1 + 4^a + 4^b \le 4^{a+b+1}$, and the cases of `if` and the operators are the same. For `let` with $|e_1| = a$ and $|e_2| = b$, let $A = |\mathrm{exp}(e_1)|$ and $B = |\mathrm{exp}(e_2)|$. If $x$ occurs $m \le B$ times in $\mathrm{exp}(e_2)$, then $|[x := \mathrm{exp}(e_1)]\,\mathrm{exp}(e_2)| = B - m + mA \le BA$. So

$$|\mathrm{exp}(e)| \le 2 + BA + A \le 2 + 4^{a+b} + 4^a \le 4^{a+b+1} = 4^{|e|},$$

because $3 \cdot 4^{a+b} \ge 12 \cdot 4^a > 4^a + 2$. $\square$

## Part 1: the upper bound

Let $n = |e|$. Compute $\mathrm{exp}(e)$ in time proportional to its size, which is at most $4^n$ by Lemma 3. By Lemma 2, $e$ is typable exactly when $\mathrm{exp}(e)$ is. A term with no `let` is typable exactly when the set of equations with one type variable per node, $\alpha_{e_1} = \alpha_{e_2} \to \alpha_{e_1 e_2}$ at each application and so on, has a unifier. There are $O(N)$ equations for a term of size $N$. Unification on a [term DAG](/term-dag/) with [union-find](/disjoint-set-forest/) solves them in $O(N\,\alpha(N))$ time, and the [Paterson-Wegman algorithm](/paterson-wegman-unification/) in $O(N)$ time. So typability is decided in time $O(4^n) = 2^{O(n)}$, which is inside DEXPTIME. $\square$

## Part 3: the size of principal types

By Lemma 2, the principal type of $e$ is the principal type of $\mathrm{exp}(e)$, up to renaming. Unification on a DAG never creates more nodes than it starts with, so the principal type is a DAG with $O(4^n)$ nodes. A DAG with $D$ nodes of out-degree at most 2 has each root path of length at most $D$, so its tree form has at most $2^{D+1}$ nodes. This gives the bounds $2^{O(n)}$ and $2^{2^{O(n)}}$.

Both bounds are reached. In the family

```text
let f0 = fun x -> fun z -> z x x in
let f1 = fun y -> f0 (f0 y) in
...
let fk = fun y -> f(k-1) (f(k-1) y) in fk
```

the type of $f_0$ is $\alpha \to (\alpha \to \alpha \to \beta) \to \beta$. The function $f_i$ applies $f_0$ $2^i$ times in a row, and each application puts two copies of the previous type into the next one. So the principal type of the term, of size $7k + 9$, has $2^{k+2} + 2$ nodes as a DAG and $6 \cdot 2^{2^k} - 3$ nodes as a tree. Any algorithm that writes types as trees, as a plain implementation of W does, takes doubly exponential time on this family.

## Part 2: the lower bound (sketch)

Let $L$ be in DEXPTIME. Then a deterministic one-tape [Turing machine](/turing-machine/) $M$ decides $L$ in time $2^{p(n)}$ for a polynomial $p$. Fix an input $w$ of length $n$ and let $m = p(n)$, large enough that $2^m \ge n$. We may assume that $M$ uses at most $2^m$ cells and stays in its accepting state once it gets there. We build, in polynomial time, a term $e_w$ of size polynomial in $n$ that is typable if and only if $M$ accepts $w$.

**Step 1: truth values as types.** Let `t = fun x -> fun y -> x` and `f = fun x -> fun y -> y`, both bound by `let`. Their schemes are $\forall \alpha \beta.\, \alpha \to \beta \to \alpha$ and $\forall \alpha \beta.\, \alpha \to \beta \to \beta$. Call a type of the form $\alpha \to \beta \to \alpha$ a *true type* and one of the form $\alpha \to \beta \to \beta$ a *false type*, when $\alpha$ and $\beta$ are type variables that occur nowhere else in the derivation. For the test `(b 1 true) + 1`, a true type of `b` gives $\mathsf{int}$, and a false type needs $\mathsf{bool} = \mathsf{int}$, so the test fails.

**Step 2: gates.** Define, with `let`,

```text
let pair = fun a -> fun b -> fun k -> k a b
let not  = fun p -> p f t
let and  = fun p -> fun q -> p q f
let or   = fun p -> fun q -> p t q
let copy = fun p -> p (pair t t) (pair f f)
```

If `p` has a true or false type, unification of that type with the argument types of a gate gives the result type of the gate: for example `not` applied to a true type unifies $\alpha \to \beta \to \alpha$ with $F \to T \to \rho$, where $F$ and $T$ are fresh false and true types, so $\rho = F$. Each use of `t`, `f` and a gate is a fresh instance, so the result again has variables that occur nowhere else. In this way type inference *computes* the gate. A `fun`-bound variable has one type, so a wire must not be used twice. Fan-out goes through `copy`, which turns one truth value into a pair of two independent fresh truth values, read by a continuation `fun u -> fun v -> ...`. So each Boolean [circuit](/boolean-circuit/) with $s$ gates becomes a term of size $O(s)$ in which each `fun`-bound variable occurs at most once, and whose type inference evaluates the circuit.

**Step 3: one step of the machine.** Encode the content of a cell, a state or a tape symbol, as a tuple of $c$ truth values, where $c$ depends only on $M$. As in the [Cook-Levin theorem](/cook-levin-theorem/), the next content of cell $i$ is a fixed circuit of cells $i - 1$, $i$ and $i + 1$. Store the tape of $2^m$ cells as a complete binary tree of depth $m$, built from `pair`. For $i = 0, 1, \ldots, m$, define with `let` a function $\mathit{step}_i$ that takes a left neighbour cell, a tree of depth $i$ and a right neighbour cell and returns the next tree, and helper functions that copy a tree and that read its first and last cell. Each function of level $i$ is defined from the functions of level $i - 1$. These are `let`-bound, so they may be used several times, each at a fresh instance. Inside each body, each `fun`-bound variable occurs at most once. Each level adds $O(1)$ nodes, with a constant that depends on $M$, so all levels together have size $O(m)$.

**Step 4: exponentially many steps.** Let $\mathit{run}_0 = \mathit{step}_m$ with blank boundary cells, and

```text
let run1 = fun s -> run0 (run0 s) in
...
let runm = fun s -> run(m-1) (run(m-1) s) in ...
```

so that $\mathit{run}_m$ performs $2^m$ steps, as in the family of part 3. The initial tape has $w$ in its first $n$ cells and blanks elsewhere. Blank trees of each depth come from `let blank_i = pair blank_(i-1) blank_(i-1)`, and the cells of $w$ are placed along $n$ paths of length $m$, which takes $O(nm)$ nodes. A last function of size $O(m)$, built the same way, computes the "or" over all cells of the test "this cell holds the accepting state". Let $e_w$ be the test of Step 1 applied to this truth value. Its size is polynomial in $n$, and it is easy to produce from $w$.

**Step 5: correctness.** By Lemma 2, $e_w$ is typable exactly when $\mathrm{exp}(e_w)$ is. All `let` definitions of $e_w$ are closed and sit at the top, so the expansion copies no `fun`-bound variable, and in $\mathrm{exp}(e_w)$ each `fun`-bound variable occurs at most once. For such terms, a beta step does not change the types: subject reduction holds in the simply typed calculus, and subject expansion holds when the bound variable occurs once, or when it does not occur and the discarded argument has a type. In the construction, each discarded argument is a truth value or a tuple of truth values, and it has a type. Each beta step makes the term smaller, so $\mathrm{exp}(e_w)$ reduces to its normal form, which is `1 + 1` if $M$ accepts $w$ and `true + 1` if not. The first has a type and the second has none. So $e_w$ is typable if and only if $M$ accepts $w$. $\square$

## References

- Harry G. Mairson, Deciding ML typability is complete for deterministic exponential time, POPL 1990, pages 382 to 401. The lower bound by a simulation of an exponential time Turing machine.
- A. J. Kfoury, J. Tiuryn and P. Urzyczyn, ML typability is DEXPTIME-complete, CAAP 1990, LNCS 431, pages 206 to 220, and An analysis of ML typability, Journal of the ACM 41(2), 1994, pages 368 to 398. An independent proof, by an equivalence of ML typability with acyclic semi-unification.
- Benjamin C. Pierce, Types and Programming Languages, MIT Press, 2002, Section 22.7. Typing `let` by substitution.
