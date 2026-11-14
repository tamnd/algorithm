---
tag: A2BZNH
kind: technique
slug: positive-equality
name: Positive equality
aliases:
- Bryant-German-Velev positive equality
area: eda/hardware-verification
level: research
summary: Bryant, German and Velev's reduction of EUF formulas that gives distinct constants to terms used only in positive equations, which makes processor verification fast.
prereqs: [euf-satisfiability, ackermannization]
see_also: [burch-dill-flushing, euf-satisfiability, ackermannization, eager-smt-encoding, congruence-closure, bell-numbers, cdcl, binary-decision-diagram]
sources:
  - paper: doi:10.1145/371282.371364
    title: R. E. Bryant, S. German and M. N. Velev, Processor verification using efficient reductions of the logic of uninterpreted functions to propositional logic, ACM Transactions on Computational Logic 2(1), 93 to 134, 2001
    locator: Section 3 (the PEUF syntax of Figure 2, the sets of negative formulas and terms, Theorem 1 on parsing, diverse and maximally diverse interpretations, Theorem 2 with Lemmas 1 and 2), Section 4 (function elimination by nested ITE terms, Theorems 3 and 4, Corollary 1) and Section 5 (propositional encodings, Theorem 5)
  - paper: arxiv:cs/9910014
    title: R. E. Bryant, S. German and M. N. Velev, Processor verification using efficient reductions of the logic of uninterpreted functions to propositional logic, technical report CMU-CS-99-115, 1999
    locator: the preprint of the journal paper, with the running example F_eg, Table 2 and the counts 877 and 384 in Section 3.3
  - paper: doi:10.1007/3-540-58179-0_44
    title: J. R. Burch and D. L. Dill, Automatic verification of pipelined microprocessor control, Computer Aided Verification (CAV 1994), LNCS 818, 68 to 80, 1994
    locator: the EUF formulas of pipelined processors that positive equality was made to decide
---

Positive equality is a way to decide validity of formulas in the logic of equality with [uninterpreted functions](/euf-satisfiability/) (EUF) much faster when most equations occur only positively. Bryant, German and Velev (2001) noticed that in the formulas of [Burch-Dill flushing](/burch-dill-flushing/), the data values of a processor are compared for equality only in the final, positive check, while register identifiers and control values also appear in negated equations and in the conditions of if-then-else terms. They split the function symbols in two classes. A *p-function symbol* is used only in positive equations, and a *g-function symbol* is used in general. Their central theorem says that a formula in which the p-symbols occur only positively is valid exactly when it is true in the *maximally diverse* interpretations, where terms of p-symbols are equal only when functional consistency forces it. After the function applications are removed, each p-variable can therefore take a fixed constant, distinct from every other value, and it needs no Boolean variables at all. Only the g-variables are encoded, so the propositional formula that a SAT or BDD tool gets is much smaller.

## In plain words

To prove an equation about a processor, you must check every way the values in it can be equal or different. With many values this is a huge number of cases.

Look at how each value is used. Some values are only ever compared at the end, in a check that says "these two must be equal". Making two such values equal by chance can only help that check succeed. So the hardest case for the check is the one where all those values are different, unless the circuit itself forces them to be equal. You can give each of them its own fixed constant and stop treating it as an unknown.

Other values are compared inside the logic, for example a register number that selects a bypass. Those stay unknown and are encoded with Boolean variables. In processor formulas most values are data, so most unknowns disappear.

## When it applies

- The input is a formula $F_{\mathrm{top}}$ of EUF: domain variables, function and predicate applications, if-then-else terms $\mathrm{ITE}(G, T_1, T_2)$, equations, propositional variables, $\neg$, $\wedge$ and $\vee$. The question is whether $F_{\mathrm{top}}$ is *universally valid*: true for every nonempty domain and every interpretation of the symbols. A domain variable is a function symbol of arity 0.
- $F_{\mathrm{top}}$ is in negation normal form, so $\neg$ is applied only to equations and predicate applications. Any formula can be put in this form with De Morgan's laws.
- Let $\Phi$ and $\Theta$ be the sets of syntactically distinct formulas and terms of $F_{\mathrm{top}}$. The *negative formulas* $\Phi^- \subseteq \Phi$ form the smallest set that contains $F$ for every $\neg F$ in $\Phi$, contains the condition $F$ of every $\mathrm{ITE}(F, T_1, T_2)$ in $\Theta$, and contains $F_1$ and $F_2$ whenever it contains $F_1 \wedge F_2$ or $F_1 \vee F_2$. The *negative terms* $\Theta^- \subseteq \Theta$ form the smallest set that contains $T_1$ and $T_2$ for every equation $T_1 = T_2$ in $\Phi^-$, and $T_1$ and $T_2$ for every $\mathrm{ITE}(F, T_1, T_2)$ in $\Theta^-$.
- A function symbol $f$ is in $\mathcal{F}_g$ if some term $f(T_1, \ldots, T_k)$ is in $\Theta^-$, and in $\mathcal{F}_p$ otherwise. A symbol does not become a g-symbol because its applications appear as arguments of other applications: arguments may be p-terms. Theorem 1 of Bryant, German and Velev says that $F_{\mathrm{top}}$ can then be parsed as a *p-formula* of their logic PEUF, with the symbols of $\mathcal{F}_g$ as g-symbols and those of $\mathcal{F}_p$ as p-symbols.
- The technique pays off when $\mathcal{F}_p$ is large. In Burch-Dill formulas, the data values, the ALU and the results are usually p-symbols, while register identifiers, which are compared in bypass and stall logic, are g-symbols.

**Maximally diverse interpretations.** For an interpretation $I$, write $T_1 \approx_I T_2$ when $I[T_1] = I[T_2]$. Let $\Sigma$ be a set of function symbols of $F$. The interpretation $I$ is *diverse for $F$ with respect to $\Sigma$* if, for every function application term $T_1 = f(T_{1,1}, \ldots, T_{1,k})$ of $F$ with $f \in \Sigma$, $T_1 \approx_I T_2$ holds for a function application term $T_2$ of $F$ only when $T_2 = f(T_{2,1}, \ldots, T_{2,k})$ has the same symbol and $T_{1,i} \approx_I T_{2,i}$ for all $i$. It is *maximally diverse* if it is diverse with respect to the set $\Sigma_p(F)$ of all p-function symbols of $F$. So a p-application equals another term only when functional consistency forces it.

**Theorem 2 (Bryant, German and Velev).** A p-formula $F$ is universally valid if and only if it is true in all maximally diverse interpretations.

## The template

```pseudo id=main
POSITIVE-EQUALITY(F_top)
L1  F ← the negation normal form of F_top
L2  compute the negative formulas Φ⁻ and the negative terms Θ⁻ of F
L3  F_g ← symbols with an application in Θ⁻; F_p ← all other function symbols
L4  F* ← F with every function application replaced by nested ITE terms over fresh domain variables, innermost applications first
L5  P ← the fresh variables of the symbols in F_p, and the domain variables in F_p
L6  give each variable in P its own fixed constant, distinct from all other values
L7  encode equations between the other domain variables with Boolean variables
L8  return whether the propositional formula from F* is a tautology, by SAT or BDDs
```

Line L4 is the function elimination of Bryant, German and Velev. Let $f(T_1), \ldots, f(T_n)$ be the applications of a symbol $f$, in an order where each argument has already been rewritten. Each application gets a fresh variable $v_{f,i}$, and the $i$-th application becomes

$$\mathrm{ITE}\bigl(T_i = T_1,\ v_{f,1},\ \mathrm{ITE}\bigl(T_i = T_2,\ v_{f,2},\ \cdots\ \mathrm{ITE}(T_i = T_{i-1},\ v_{f,i-1},\ v_{f,i})\bigr)\bigr),$$

where $T_i = T_j$ means equality of all arguments. The result $F^*$ has only domain variables, and it is valid exactly when $F$ is (their Theorem 3). It keeps functional consistency by construction: equal arguments select the same variable. The new equations between arguments sit in ITE conditions, which are negative positions of $F^*$. Even so, Theorem 4 of the paper says that $F$ is valid exactly when $F^*$ is true in every interpretation that is diverse with respect to the fresh variables of the p-symbols, so line L5 takes the polarity from $F$, not from $F^*$. Corollary 1 then allows the fixed constants of line L6, taken from a set disjoint from the values of the g-variables. Lines L7 and L8 are any propositional encoding of the remaining equations; Theorem 5 of the paper treats two of them.

**Proof of a small case.** The direction from validity to truth in the maximally diverse interpretations is immediate. For the other direction, here is a complete proof for p-formulas in which every function symbol is a domain variable. ITE terms, propositional variables and predicate symbols may occur. The general proof is Lemmas 1 and 2 of the paper. Lemma 1 splits one equivalence class of a not maximally diverse interpretation without making the formula true, and Lemma 2 repeats this, which ends because a partition of the finite term set can be properly refined only finitely often.

Let $F$ be such a p-formula, true in all maximally diverse interpretations, and let $J$ be any interpretation over a domain $D$. Take a fresh value $z_v \notin D$ for each p-variable $v$, and let $D' = D \cup \{z_v\}$. Let $\tau: D' \to D$ map $z_v$ to $J(v)$ and fix $D$. Define $J'$ over $D'$: $J'(v) = z_v$ for each p-variable, $J'(u) = J(u)$ for each g-variable and each propositional variable, and $J'(p)(d_1, \ldots, d_k) = J(p)(\tau(d_1), \ldots, \tau(d_k))$ for each predicate symbol. We show, by induction on the PEUF syntax:

1. $\tau(J'[T]) = J[T]$ for every term $T$, and $J'[T] = J[T]$ for every g-term.
2. $J'[G] = J[G]$ for every g-formula $G$.
3. $J'[P]$ implies $J[P]$ for every p-formula $P$.

For a variable, (1) holds by the definition of $J'$, and a g-term variable is a g-variable. For $\mathrm{ITE}(G, T_1, T_2)$, the condition $G$ is a g-formula, so by (2) both interpretations pick the same branch, and (1) passes up from that branch. A g-formula is an equation of g-terms, a predicate application, a propositional variable, or a Boolean combination of g-formulas with $\neg$, $\wedge$, $\vee$. Equations of g-terms keep their value by (1). For a predicate, $J'(p)(J'[T_1], \ldots) = J(p)(\tau(J'[T_1]), \ldots) = J(p)(J[T_1], \ldots)$ by (1). The rest is a Boolean combination of equal values, so (2) holds. A p-formula is a g-formula, an equation of p-terms, or a combination of p-formulas with $\wedge$ and $\vee$ only. For an equation, $J'[T_1] = J'[T_2]$ gives $\tau(J'[T_1]) = \tau(J'[T_2])$, which is $J[T_1] = J[T_2]$ by (1). $\wedge$ and $\vee$ are monotone, so (3) passes up. This proves the three claims.

$J'$ is maximally diverse. The value of a term under $J'$ is the value of the variable that its ITE conditions select, so $J'[T] = z_v$ only when $T$ is $v$ itself, and a p-variable is equal to no other variable term. So $J'[F]$ is true, and by (3) $J[F]$ is true. As $J$ was arbitrary, $F$ is valid. $\square$

The proof also shows why polarity matters. Claim (3) is only an implication, so it survives $\wedge$ and $\vee$ but not $\neg$ and not ITE conditions. That is why p-terms may appear only in positive equations.

**Example.** The running example of the paper is

$$F_{\mathrm{eg}} = \neg(x = y) \vee h\bigl(g(x), g(g(x))\bigr) = h\bigl(g(y), g(g(x))\bigr).$$

The equation $x = y$ is negated, so $x$ and $y$ are g-symbols. The symbols $g$ and $h$ occur only in the positive equation and in arguments, so they are p-symbols. The formula has seven function application terms: $x$, $y$, $g_1 = g(x)$, $g_2 = g(y)$, $g_3 = g(g(x))$, $h_1 = h(g_1, g_3)$, $h_2 = h(g_2, g_3)$. There are 877 ways to partition seven terms, the Bell number $B_7$, and 384 of them are functionally consistent. Only two come from maximally diverse interpretations: D1, where all seven terms are different, and D2, with classes $\{x, y\}, \{g_1, g_2\}, \{g_3\}, \{h_1, h_2\}$. In D2, $x = y$ forces $g_1 = g_2$, which forces $h_1 = h_2$. $F_{\mathrm{eg}}$ is true in D1 because $x \ne y$, and true in D2 because $h_1 = h_2$. By Theorem 2 it is valid. (These counts were checked by enumeration of all 877 partitions while writing this page.)

The same check through lines L4 to L8: eliminate $g$ in the order $g(x), g(y), g(g(x))$ and $h$ in the order $h_1, h_2$:

| term | after elimination | with $v_{g,1}, v_{g,2}, v_{g,3}$ distinct constants |
|---|---|---|
| $g(x)$ | $v_{g,1}$ | $v_{g,1}$ |
| $g(y)$ | $\mathrm{ITE}(y = x, v_{g,1}, v_{g,2})$ | $\mathrm{ITE}(e, v_{g,1}, v_{g,2})$ |
| $g(g(x))$ | $\mathrm{ITE}(v_{g,1} = x, v_{g,1}, \mathrm{ITE}(v_{g,1} = y, v_{g,2}, v_{g,3}))$ | $v_{g,3}$, as constants differ from g-values |
| $h_1$ | $v_{h,1}$ | $v_{h,1}$ |
| $h_2$ | $\mathrm{ITE}(\hat g_2 = v_{g,1} \wedge \hat g_3 = \hat g_3, v_{h,1}, v_{h,2})$ | $\mathrm{ITE}(e, v_{h,1}, v_{h,2})$ |

Here $\hat g_2$ and $\hat g_3$ are the rewritten forms of $g(y)$ and $g(g(x))$, and $e$ is the one Boolean variable for $x = y$. With the constants, $\hat g_2 = v_{g,1}$ is $\mathrm{ITE}(e, v_{g,1}, v_{g,2}) = v_{g,1}$, which is $e$. The formula becomes $\neg e \vee v_{h,1} = \mathrm{ITE}(e, v_{h,1}, v_{h,2})$, which is $\neg e \vee e$, a tautology. Without positive equality, the five fresh variables and $x, y$ would all be encoded, with equations among them.

**Cost.** Line L4 adds, for a symbol with $n_f$ applications of arity $k$, at most $n_f (n_f - 1) / 2$ argument comparisons of $k$ equations each, so $F^*$ has size $O(|F| + \sum_f k \, n_f^2)$ with shared subterms. A formula with $m$ domain variables only is valid exactly when it is valid over a domain of $m$ values, because a falsifying interpretation uses at most $m$ values and can be cut down to them. So without positive equality the $m$ variables need $m \lceil \log_2 m \rceil$ Boolean variables in a binary encoding, or $m(m-1)/2$ variables $e_{ij}$ for the equations, plus constraints for transitivity. With positive equality the p-variables need none, and only the $m_g$ g-variables are encoded. Validity of EUF stays [coNP-complete](/co-np-complete/), so the worst case does not change. The gain is measured, not proved. Bryant, German and Velev report experiments on pipelined processor models in which the reduction makes the propositional problem much smaller and faster to solve than encodings that treat every variable as general.

## Classic examples

- **Burch-Dill formulas.** The commuting diagram of [Burch-Dill flushing](/burch-dill-flushing/) compares the register files of the two routes in one positive equation. The data terms and the uninterpreted ALU are p-symbols. Positive equality made these checks scale to larger pipelines than direct EUF procedures could handle.
- **Ackermann's reduction.** [Ackermannization](/ackermannization/) removes function applications with functional consistency constraints $T_i = T_j \Rightarrow v_{f,i} = v_{f,j}$. These constraints put the fresh variables on both sides of an implication, that is in negative equations, so every variable becomes general. The nested ITE scheme of line L4 keeps the p-variables positive. This is why Bryant, German and Velev use it.
- **Eager SMT encodings.** [Eager encodings](/eager-smt-encoding/) of equality logic to propositional logic, with small domains or $e_{ij}$ variables and transitivity constraints, are the back end of lines L7 and L8. Positive equality shrinks their input before they start.
- **Lazy procedures.** [Congruence closure](/congruence-closure/) inside a lazy SMT solver decides the same formulas without any encoding, and does not need the polarity split.

## Variations

- **Only part of the polarity.** A symbol with some applications in negative positions is a g-symbol for all its applications in the basic method. A finer split classifies application terms, not symbols. Theorem 2 is stated for symbols.
- **Fixed constants versus diverse interpretations.** Theorem 2 quantifies over all maximally diverse interpretations. Corollary 1 of the paper fixes the values of the p-variables to distinct constants outside the domain of the g-variables, which is what a propositional encoding needs.
- **Memories.** Memories modeled with uninterpreted read and write functions put address comparisons in ITE conditions, so addresses are g-terms while the stored data can stay p-terms.
- **BDDs or SAT.** The propositional formula of line L8 can be checked with [BDDs](/binary-decision-diagram/) or with a [CDCL](/cdcl/) SAT solver on its negation.

## Pitfalls

- **A g-term treated as a p-term is unsound.** $\neg(x = y)$ is not valid, but with $x$ and $y$ given distinct constants it becomes true. The classification of line L3 must use every negative position, including ITE conditions and equations under $\neg$ after the formula is in negation normal form.
- **A p-term treated as a g-term is only slow.** Every interpretation with fixed p-constants is an interpretation, so encoding more variables as general never gives a wrong answer.
- **Shared subterms.** $\Theta$ holds syntactically distinct terms. A term that occurs once positively and once in a negative equation is in $\Theta^-$, and its symbol is a g-symbol everywhere.
- **The order of elimination.** Line L4 needs the arguments of an application rewritten before the application itself, so nested applications such as $g(g(x))$ refer to the fresh variable of the inner one.
- **Algebraic facts.** Like all EUF methods, positive equality proves only what holds for every interpretation. A design that relies on $\mathrm{ADD}(a, b) = \mathrm{ADD}(b, a)$ fails unless the fact is added as an axiom, and an axiom with equations in its premise changes the polarity of the terms in it.

## Exercises

1. Classify the symbols of $\neg(a = b) \vee f(a) = f(b)$, and show that the formula is valid by checking its maximally diverse interpretations.
2. Give a formula in which a symbol has one application in a negative equation and one only in positive ones. What does the basic method do, and why is it sound?
3. Extend the small-case proof to function symbols of arity 1 when every application has a domain variable as its argument. Which step of Lemma 1 of the paper do you need?

## References
