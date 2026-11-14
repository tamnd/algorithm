---
title: The one-pass CPS conversion keeps the outcome and makes no administrative redexes
proves: [correctness]
status: full
---

We use the notation of the page. Source terms are closed and their binders are renamed apart by line L1, so no substitution below can capture a name. A *trivial* term is a variable, a constant, `fun` or `fix`. An *administrative redex* is a redex whose operator is a `fun` that the translation made, that is a `fun k -> ...`, a continuation `fun a -> ...` or `fun t -> ...`, and not the image of a source function. We extend Plotkin's translation $[\![\cdot]\!]$ to the whole language with the rules of the code:

- $[\![v]\!] = \mathtt{fun}\ k \to k\ \Psi(v)$ for trivial $v$, where $\Psi(x) = x$, $\Psi(c) = c$, $\Psi(\mathtt{fun}\ x \to b) = \mathtt{fun}\ x \to [\![b]\!]$ and $\Psi(\mathtt{fix}\ f\ x \to b) = \mathtt{fix}\ f\ x \to [\![b]\!]$;
- $[\![e_1\ e_2]\!] = \mathtt{fun}\ k \to [\![e_1]\!]\ (\mathtt{fun}\ a \to [\![e_2]\!]\ (\mathtt{fun}\ b \to a\ b\ k))$;
- $[\![\mathtt{let}\ x = e_1\ \mathtt{in}\ e_2]\!] = \mathtt{fun}\ k \to [\![e_1]\!]\ (\mathtt{fun}\ a \to \mathtt{let}\ x = a\ \mathtt{in}\ [\![e_2]\!]\ k)$;
- $[\![\mathtt{if}\ e_1\ \mathtt{then}\ e_2\ \mathtt{else}\ e_3]\!] = \mathtt{fun}\ k \to [\![e_1]\!]\ (\mathtt{fun}\ a \to \mathtt{if}\ a\ \mathtt{then}\ [\![e_2]\!]\ k\ \mathtt{else}\ [\![e_3]\!]\ k)$;
- $[\![e_1\ op\ e_2]\!] = \mathtt{fun}\ k \to [\![e_1]\!]\ (\mathtt{fun}\ a \to [\![e_2]\!]\ (\mathtt{fun}\ b \to \mathtt{let}\ t = a\ op\ b\ \mathtt{in}\ k\ t))$.

The *outcome* of a closed term is an integer or boolean value, "a function", "stuck" or "no result". The proof has three parts. Part 1 is Plotkin's simulation theorem, given as a sketch in his style. Part 2 shows that the one-pass output is Plotkin's output with administrative redexes reduced. Part 3 shows that those reductions keep the outcome. Parts 4 to 6 prove the structural claims.

## 1. Plotkin's simulation (sketch)

Let $K$ range over closed continuation values. Plotkin's *colon translation* $e : K$ is defined on the shape of $e$ in evaluation order:

- $v : K = K\ \Psi(v)$ for a value $v$;
- $(e_1\ e_2) : K = e_1 : (\mathtt{fun}\ a \to [\![e_2]\!]\ (\mathtt{fun}\ b \to a\ b\ K))$ if $e_1$ is not a value;
- $(v_1\ e_2) : K = e_2 : (\mathtt{fun}\ b \to \Psi(v_1)\ b\ K)$ if $e_2$ is not a value;
- $(v_1\ v_2) : K = \Psi(v_1)\ \Psi(v_2)\ K$;

and in the same way for `let`, `if` and the operators.

**Lemma 1.1.** $[\![e]\!]\ K \to^* e : K$.

*Proof.* By induction on $e$. Each step is an administrative redex at the head: $[\![e]\!]$ is a `fun k`, it takes $K$, and then the translation of the first part of $e$ that is not a value takes the continuation that the rule builds. When that part is a value, the step $(\mathtt{fun}\ a \to \dots)\ \Psi(v)$ moves on to the next part. $\square$

**Lemma 1.2 (substitution).** For a value $v$, $[\![b]\!][x := \Psi(v)] = [\![b[x := v]]\!]$, and the same for $\Psi$.

*Proof.* By induction on $b$. A variable is the only case that inspects $x$, and $[\![x]\!] = \mathtt{fun}\ k \to k\ x$ becomes $\mathtt{fun}\ k \to k\ \Psi(v) = [\![v]\!]$. $\square$

**Lemma 1.3.** If $e \to e'$ in one call-by-value step, then $e : K \to^+ e' : K$. If $e$ is stuck, then $e : K$ is stuck after finitely many steps.

*Proof.* The colon translation follows the evaluation context, so $e = E[r]$ with redex $r$ gives $e : K = r : K_E$, where $K_E$ depends only on $E$ and $K$. For $r = (\mathtt{fun}\ x \to b)\ v$, $r : K_E = (\mathtt{fun}\ x \to [\![b]\!])\ \Psi(v)\ K_E \to [\![b]\!][x := \Psi(v)]\ K_E = [\![b[x := v]]\!]\ K_E$ by Lemma 1.2, and Lemma 1.1 continues to $b[x := v] : K_E$. A `fix` call is the same with two substitutions. For `let x = v in b` the step `let x = Ψ(v) in [[b]] K_E` goes the same way. For an operator, `let t = c1 op c2 in K_E t` steps to $K_E\ c$ with the result $c$, which is $c : K_E$. For `if true`, the term `if true then [[e2]] K_E else ...` steps to $[\![e_2]\!]\ K_E$, and Lemma 1.1 finishes. If $r$ is stuck, the image has the same stuck call, condition or operator on the same constants. Finally, $E[r'] : K = r' : K_E$ when $r'$ is not a value, and when $r'$ is a value the administrative steps of $K_E$ lead from $K_E\ \Psi(r')$ to $E[r'] : K$. $\square$

**Theorem 1 (Plotkin).** $[\![e]\!]\ (\mathtt{fun}\ a \to a)$ has the same outcome as $e$, where a source function $v$ gives the function $\Psi(v)$.

*Proof.* By Lemmas 1.1 and 1.3, each source step is matched by at least one target step, and target evaluation is deterministic, so the target run passes through $e_i : I$ for every term $e_i$ of the source run. If the source reaches a value $v$, the target reaches $v : I = I\ \Psi(v) \to \Psi(v)$. If the source gets stuck, so does the target. If the source runs forever, so does the target. $\square$

## 2. The one-pass output is the administrative normal form

Write $\mathrm{adm}(P)$ for the result of reducing all administrative redexes of $P$, also those under `fun`. This process ends: the administrative redexes are typed in the simply typed lambda calculus with one base type for answers, as in the two-level typing of Danvy and Filinski, and simply typed reduction ends. For the extended rules, generalize TAIL$(e, K)$ to any trivial output term $K$: lines L7 to L11 only place $K$ as an argument or as the operator of `K a`.

**Lemma 2.1.** For every source term $e$:

1. $\mathrm{adm}(\Psi(v)) = \mathrm{VAL}(v)$ for trivial $v$, up to the names of bound variables;
2. $\mathrm{adm}([\![e]\!]\ k) = \mathrm{TAIL}(e, k)$ for an output variable $k$;
3. for every output term $X$ in normal form with a free variable $a$, $\mathrm{adm}([\![e]\!]\ (\mathtt{fun}\ a \to X)) \cong \mathrm{META}(e, \lambda w.\, X[a := w])$,

where $P \cong Q$ means that $Q$ reduces to $P$ by $\beta_v$ steps at join-point `let`s and at the administrative redexes that these steps create.

*Proof.* By induction on $e$, with the three claims together.

- **Trivial $v$.** Claim 1: $\Psi(\mathtt{fun}\ x \to b) = \mathtt{fun}\ x \to [\![b]\!]$ and $[\![b]\!] = \mathtt{fun}\ k' \to M$ with $M$ the body. So $\mathrm{adm}$ gives $\mathtt{fun}\ x \to \mathtt{fun}\ k' \to \mathrm{adm}(M)$, and $\mathrm{adm}(M) = \mathrm{adm}([\![b]\!]\ k')$ up to the name $k'$, which is TAIL$(b, k')$ by claim 2. This is line L5, and `fix` is line L6. Variables and constants are line L4. Claim 2: $[\![v]\!]\ k \to k\ \Psi(v)$, normal form $k\ \mathrm{VAL}(v)$, line L7. Claim 3: $[\![v]\!]\ (\mathtt{fun}\ a \to X) \to (\mathtt{fun}\ a \to X)\ \Psi(v) \to X[a := \Psi(v)]$, normal form $X[a := \mathrm{VAL}(v)]$, line L12. Substituting a trivial term for $a$ makes no administrative redex: a trivial term is a variable, a constant or the image of a source function, whose outer binder is a source binder.
- **Call $e_1\ e_2$.** $[\![e_1\ e_2]\!]\ K \to [\![e_1]\!]\ (\mathtt{fun}\ a \to [\![e_2]\!]\ (\mathtt{fun}\ b \to a\ b\ K))$. By claim 3 for $e_1$ and then for $e_2$, the normal form is META$(e_1, \lambda w_1.\, \mathrm{META}(e_2, \lambda w_2.\, w_1\ w_2\ K'))$ with $K' = \mathrm{adm}(K)$. For $K = k$ this is line L8. For $K = \mathtt{fun}\ t \to X[a := t]$, $K'$ is $\mathtt{fun}\ t \to \kappa(t)$ with $\kappa = \lambda w.\, X[a := w]$, which is line L13.
- **`let` and operators.** The same, with lines L9, L14 and L11, L16. For TAIL of an operator, $\mathtt{let}\ t = a\ op\ b\ \mathtt{in}\ k\ t$ is line L16 with $\kappa = \lambda w.\, k\ w$, as line L11 asks.
- **`if`.** For $K = k$, the normal form is META$(e_1, \lambda w.\, \mathtt{if}\ w\ \mathtt{then}\ \mathrm{TAIL}(e_2, k)\ \mathtt{else}\ \mathrm{TAIL}(e_3, k))$, line L10. For $K = \mathtt{fun}\ t \to \kappa(t)$, Plotkin's term gives `if w then adm([[e2]] K) else adm([[e3]] K)`, with two copies of $\kappa$. Line L15 gives `let j = K in if w then TAIL(e2, j) else TAIL(e3, j)`. One $\beta_v$ step at the join point gives TAIL$(e_i, K)$ in each branch, and $\mathrm{adm}(\mathrm{TAIL}(e_i, K)) = \mathrm{adm}([\![e_i]\!]\ K)$ by the generalized claim 2. So the two sides are related by $\cong$. $\square$

With line L3, CPS$(e)$ = `let k0 = I in TAIL(e, k0)`, which reduces by one $\beta_v$ step to TAIL$(e, I)$, and by Lemma 2.1 TAIL$(e, I) \cong \mathrm{adm}([\![e]\!]\ I)$. On terms without `if`, $\cong$ is equality up to names, which the test `test_one_pass_is_plotkin_then_administrative_reduction` checks on random terms.

## 3. Administrative steps keep the outcome

Every step used in Part 2 is a $\beta_v$ step $(\mathtt{fun}\ x \to M)\ W \to M[x := W]$ or $\mathtt{let}\ x = W\ \mathtt{in}\ M \to M[x := W]$ with $W$ a value, possibly under a `fun`. Plotkin proved that a $\beta_v$ step anywhere in a term keeps its call-by-value outcome. The argument also separates "stuck" from "no result": the redex itself never gets stuck, since its operator is a `fun`, and a stuck call, condition or operator in one term has a residual in the other with the same stuck shape. So CPS$(e)$ and $[\![e]\!]\ I$ have the same outcome, and by Theorem 1 so do CPS$(e)$ and $e$. A source function gives $\Psi(v)$ in one and VAL of the reduced function in the other, both functions. This proves property 1 of the page.

## 4. No administrative redex

Every call node of the output comes from one of lines L7, L8, L11 and L13. TAIL is only called with a variable as its continuation: $k_0$ at line L3, a new $k$ at lines L5 and L6, and $j$ at line L15. So the operators at lines L7 and L11 are variables. At lines L8 and L13 the operator is the trivial term $a$ that a meta-continuation received, which is a variable, a constant or VAL of a source function. A source function in operator position gives a redex whose binder is a source binder: the image of a call that the source already has. The translation makes three kinds of `fun`: `fun k ->` at lines L5 and L6, which is the body of a source function and never an operator, `fun t -> κ(t)` at lines L13 and L15, which is the last argument of a call or the right side of `let j`, and `fun a -> a` at line L3, which is the right side of `let k0`. None of them is ever an operator, so the output has no administrative redex. A call in tail position passes the variable $k$ itself (line L8), never `fun t -> k t`, so there is no η-redex either.

## 5. Every call is a tail call

Define *serious* terms $S$ and *trivial* output terms $W$ by

$$S ::= W\ W \mid W\ W\ W \mid \mathtt{let}\ x = W\ \mathtt{in}\ S \mid \mathtt{let}\ x = W\ op\ W\ \mathtt{in}\ S \mid \mathtt{if}\ W\ \mathtt{then}\ S\ \mathtt{else}\ S$$

$$W ::= x \mid c \mid \mathtt{fun}\ x \to \mathtt{fun}\ k \to S \mid \mathtt{fix}\ f\ x \to \mathtt{fun}\ k \to S \mid \mathtt{fun}\ t \to S$$

By induction on $e$: VAL returns a $W$; TAIL returns an $S$; and META$(e, \kappa)$ returns an $S$ whenever $\kappa$ maps each $W$ to an $S$. Each line checks this directly. Line L12 applies $\kappa$ to a $W$. Lines L13 and L16 build an $S$ around $\kappa(t)$, which is an $S$. Every meta-continuation built at lines L8 to L16 maps a $W$ to an $S$. In $S$ a call occurs only as a whole $S$, the body of a `fun`, a `let` or a branch, and never as an argument, a condition or the right side of a `let`. So every call is the last action of the code around it. This is property 2, and the test `test_every_call_is_a_tail_call` checks the grammar.

## 6. Linear size

Each call of META that receives $\kappa$ calls it exactly once or passes it on exactly once (lines L12 to L16), and each meta-continuation built at lines L8 to L16 contains one call of META or one node. TAIL copies only the variable $k$ at line L10. So each source node gives a constant number of output nodes, and the output has $O(n)$ nodes. $\square$
