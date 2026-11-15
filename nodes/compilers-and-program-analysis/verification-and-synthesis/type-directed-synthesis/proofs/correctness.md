---
title: The synthesized function is well typed, meets the examples, and always terminates
proves: [correctness]
status: full
---

**Setting.** The goal type is $\tau_n = \mathrm{int} \rightarrow \cdots \rightarrow \mathrm{int}$ with $n \in \{1, 2, 3\}$ arguments $x, y, z$. The examples are pairs $(a, o)$ of an argument tuple $a = (a_1, \ldots, a_n)$ of integers and an integer output, with no two examples for the same $a$. $T$ is the table from $a$ to $o$. Line numbers refer to the pseudocode on the page.

The terms that the search builds are:

- *E-terms* of type int: the arguments, 0, 1, $e_1 \mathbin{op} e_2$ with $op \in \{+, -, \times\}$, and the call $f\ (x - 1)\ e_2 \cdots e_n$ with E-terms $e_2, \ldots, e_n$.
- *Conditions* of type bool: $e_1 < e_2$ and $e_1 = e_2$ for E-terms $e_1, e_2$.
- *Bodies*: an E-term, or $\mathbf{if}\ c\ \mathbf{then}\ B_1\ \mathbf{else}\ B_2$ for a condition $c$ or for the guard $x < 1$.

The result is $\mathbf{fix}\ f\ x \rightarrow \mathbf{fun}\ y \rightarrow \cdots \rightarrow B$. On each path from the root of $B$, the guard $x < 1$ appears at most once, and a call of $f$ appears only below its false branch. The flag $m$ of REFINE records this: "none" above the guard, "base" below its true branch and "step" below its false branch.

**The value modulo the table.** For a body $B$ and an argument tuple $a$, let $[\![B]\!]_T(a)$ be the value of $B$ when the arguments are $a$ and a call $f\ v_1 \cdots v_n$ gives $T(v_1, \ldots, v_n)$ if this tuple is in $T$, and the marker $\bot$ otherwise. An operator with an argument $\bot$ gives $\bot$. This is the value that the vectors of the search compute at line L7, one entry for each world.

## Lemma 1: the vectors are exact

**Claim.** For every E-term or condition $t$ kept by the bank on the worlds $W$, its vector is $([\![t]\!]_T(a))_{(a, o) \in W}$. The bank keeps no condition with a $\bot$ entry.

**Proof.** By induction on the size of $t$. Arguments and constants are read off directly. The vector of $e_1 \mathbin{op} e_2$ is computed entry by entry from the vectors of $e_1$ and $e_2$, with $\bot$ if one entry is $\bot$. The vector of a call is computed from the value $a_1 - 1$ and the vectors of $e_2, \ldots, e_n$ by a lookup in $T$, with $\bot$ for a tuple not in $T$. Line L12 skips conditions with a $\bot$ entry, because the code does not keep them. $\square$

## Theorem 1: the result type-checks at the goal type

**Claim.** If SYNTHESIZE returns $p$, then $p$ has the type $\tau_n$ in the type system of the toy language.

**Proof.** Assume $f : \tau_n$ and $x, y, z : \mathrm{int}$. By induction on terms: arguments and constants are int; $+$, $-$, $\times$ take two ints and give an int; $<$ and $=$ take two ints and give a bool; $x - 1$ is an int, and $f$ applied to $n$ ints is an int; a conditional with a bool condition and two int branches is an int. So $B : \mathrm{int}$, the $n - 1$ abstractions give $\tau_{n-1}$ in the scope of $x$ and $f$, and the rule for fix gives $p : \tau_n$. Hindley-Milner inference returns the principal type of $p$, which is $\tau_n$ or, when an argument does not occur in $B$, a more general type that has $\tau_n$ as an instance. $\square$

This is the type-directed part: every term is built at a known type from parts of known types, so no ill-typed candidate is ever built.

## Theorem 2: the result meets every example

**Lemma 2.** If REFINE$(W, k, d, m)$ returns $B$, then $[\![B]\!]_T(a) = o$ for every world $(a, o) \in W$.

**Proof.** By induction on $d$. If $B$ comes from line L8, its vector equals the wanted outputs, and Lemma 1 gives the claim. If $B = \mathbf{if}\ c\ \mathbf{then}\ B_1\ \mathbf{else}\ B_2$ comes from line L11 or L14, the worlds where $c$ is true went to $B_1$ and the others to $B_2$, by the vector of $c$ (Lemma 1, with no $\bot$), or by $a_1 < 1$ for the guard. By induction $B_1$ and $B_2$ meet their worlds, so $B$ meets all of $W$. $\square$

**Claim.** If SYNTHESIZE returns $p$, then for each example $(a, o)$, running $p\ a_1 \cdots a_n$ in the interpreter gives the value $o$.

**Proof.** By Lemma 2 with $W$ = all examples, $[\![B]\!]_T(a) = o$ for every example. Now show by induction on $a_1$ that the interpreter gives $o$. The real run of $B$ on $a$ differs from $[\![B]\!]_T(a)$ only at calls of $f$. A call happens only in the branch where $a_1 < 1$ is false, so $a_1 \ge 1$, and its first argument is $a_1 - 1$. Since $[\![B]\!]_T(a) = o \ne \bot$, every call whose value is used gives a tuple $v = (a_1 - 1, v_2, \ldots, v_n)$ that is in $T$, so $(v, T(v))$ is an example with a smaller first argument. By induction the real call returns $T(v)$. So the real run computes the same values as $[\![B]\!]_T(a)$ and returns $o$. The interpreter is call by value, so it also evaluates calls in E-terms whose value is used. $\square$

This proof needs no assumption on the examples. *Trace completeness*, the condition that every call that the wanted program makes on an example input is again an example, matters only for completeness below: without it, the call in the wanted program has a $\bot$ entry and cannot be found.

## Theorem 3: the result terminates on every input

**Claim.** For all integers $a_1, \ldots, a_n$, the run of $p\ a_1 \cdots a_n$ stops.

**Proof.** By induction on $\max(a_1, 0)$. Apart from calls of $f$, the body is a finite term of operators and conditionals, so it takes finitely many steps. If $a_1 < 1$, the guard sends the run into a branch with no calls, or there is no guard on the path and there is no call. If $a_1 \ge 1$, each call has the first argument $a_1 - 1$, and $\max(a_1 - 1, 0) < \max(a_1, 0)$, so each call stops by induction. $\square$

## Theorem 4: completeness for the bounded space

**Claim.** Let a body $B^\ast$ exist with $[\![B^\ast]\!]_T(a) = o$ for all worlds of $W$, whose E-terms and conditions have size at most $k$, with at most $d$ nested conditionals, and which respects the flag $m$. Then REFINE$(W, k, d, m)$ returns a body.

**Proof.** By induction on the number of conditionals in $B^\ast$. If $B^\ast$ is an E-term, the bank keeps, by the lemma of [bottom-up enumerative synthesis](/bottom-up-enumerative-synthesis/), an E-term of size at most $k$ with the same vector, since the vector of a term is a function of the vectors of its parts (Lemma 1). So line L8 returns. Otherwise $B^\ast = \mathbf{if}\ c\ \mathbf{then}\ B_1\ \mathbf{else}\ B_2$ and $d \ge 1$.

- *The guard, $m$ = none.* Line L10 makes the same split, also when no world has $a_1 < 1$; then any term fits the empty base branch. By induction REFINE finds bodies for the two sides with depth $d - 1$, because $B_1$ fits the first side with flag "base" and $B_2$ fits the second with flag "step".
- *A condition with both sides non-empty.* The bank keeps a condition with the same vector, so the same split is tried at line L12, and by induction both sides are found.
- *A condition with an empty side.* Then one branch, say $B_1$, alone fits $W$ with the same flag and fewer conditionals, and its depth is at most $d$. By induction REFINE$(W, k, d, m)$ returns a body.

The guard cannot occur below another guard, and a call cannot occur above the guard, by the flag, so these cases cover all bodies. $\square$

So with trace complete examples, SYNTHESIZE returns a result whenever a body with E-terms of size at most $K$ and at most $D$ nested conditionals meets the examples. It tries the pairs $(k, d)$ in the order of lines L2 and L3, so the result has the least $k$ among such bodies, and the least $d$ for that $k$.
