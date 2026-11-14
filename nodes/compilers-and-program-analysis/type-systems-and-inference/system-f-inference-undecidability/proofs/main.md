---
title: Typability and type checking in Curry-style System F are undecidable
proves: [statement]
status: sketch
---

This file proves the statement on the page as a sketch. The steps from two-inequality semi-unification to typability in a fixed context are proved in full, and so is the step from typability to type checking. Two results are cited: the undecidability of two-inequality semi-unification (Kfoury, Tiuryn and Urzyczyn 1993, Theorem 12 and the remark after it), and the construction that closes a context (Dudenhefner 2021, Lemma 29, or Wells 1999, Theorems 6.14 and 6.15). The normal form for derivations is also cited (Wells 1999, Lemma 3.2; Giannini and Ronchi Della Rocca 1988). The plan is Dudenhefner's, with the core idea from Wells' Theorem 4.1.

## Setting

Types, terms and the rules Var, Abs, App, Gen and Inst are as on the page. A type is *simple* if it has no quantifier. A *substitution* maps type variables to types and acts on all free variables at once, avoiding capture. We write $\forall.\rho$ for the closure of $\rho$ over all its free variables, in any fixed order. $\Gamma \Vdash M$ means that $\Gamma \vdash M : \tau$ for some $\tau$.

**Two-inequality semi-unification (SU2).** Given simple types $\sigma_1, \tau_1, \sigma_2, \tau_2$, are there substitutions $\varphi, \psi_1, \psi_2$ into simple types with $\psi_1(\varphi(\sigma_1)) = \varphi(\tau_1)$ and $\psi_2(\varphi(\sigma_2)) = \varphi(\tau_2)$?

**Left-uniform SU2 (LU).** The same question for instances with $\sigma_1 = \sigma_2$.

**Fact A (cited).** SU2 is undecidable. Semi-unification is undecidable by a reduction from Turing machine boundedness, and the reduction yields instances with two inequalities (Kfoury, Tiuryn and Urzyczyn 1993, Theorem 12 and the remark after it; restated as Theorem 31 in Dudenhefner 2021).

**Fact B (cited).** If $\Gamma \vdash M : \tau$, then there is a derivation of the same judgment in which no Inst step directly follows a Gen step (Wells 1999, Lemma 3.2, the INST-before-GEN property; Giannini and Ronchi Della Rocca 1988). So in such a derivation, the type of each subterm is produced by one of Var, Abs or App, followed by some Inst steps, followed by some Gen steps.

**Fact C.** If $\Gamma \vdash M : \tau$, then $\Gamma' \vdash M : \tau$, where $\Gamma'$ is $\Gamma$ restricted to the free variables of $M$. And if $\Gamma \vdash M : \tau$ and $x$ is not in $\Gamma$, then $\Gamma, x{:}\sigma \vdash M : \tau$ after the renaming of type variables that Gen steps bind. Both follow by induction on the derivation. The renaming is needed because Gen asks for variables that are not free in the context.

Two simple remarks are used many times. First, an Inst step needs a type of the form $\forall a.\rho$, and Inst does not touch quantifiers below an arrow. So if a type is $\forall a_1 \ldots a_k.\,\rho$ with $\rho$ an arrow, then a chain of Inst steps from it yields $\forall a_{j+1} \ldots a_k.\,\psi(\rho)$, for some $j$ and some $\psi$ that moves only $a_1, \ldots, a_j$. Second, App needs its function premise to have an arrow type, and Gen produces a $\forall$-type. So a chain of steps whose result must be an arrow ends with zero Gen steps.

## Step 1: SU2 reduces to LU

Given $(\sigma_1, \tau_1), (\sigma_2, \tau_2)$, pick fresh $a_1, a_2$ and put
$$\sigma' = \sigma_1 \to \sigma_2,\qquad \tau_1' = \tau_1 \to a_2,\qquad \tau_2' = a_1 \to \tau_2.$$

*If the original instance has a solution $\varphi, \psi_1, \psi_2$*, let $\varphi'$ agree with $\varphi$ except that $\varphi'(a_1) = \psi_2(\varphi(\sigma_1))$ and $\varphi'(a_2) = \psi_1(\varphi(\sigma_2))$. Since $a_1, a_2$ do not occur in $\sigma_1, \sigma_2, \tau_1, \tau_2$,
$$\psi_1(\varphi'(\sigma')) = \psi_1(\varphi(\sigma_1)) \to \psi_1(\varphi(\sigma_2)) = \varphi(\tau_1) \to \varphi'(a_2) = \varphi'(\tau_1'),$$
$$\psi_2(\varphi'(\sigma')) = \psi_2(\varphi(\sigma_1)) \to \psi_2(\varphi(\sigma_2)) = \varphi'(a_1) \to \varphi(\tau_2) = \varphi'(\tau_2').$$

*If $\varphi, \psi_1, \psi_2$ solve the new instance*, compare the two sides of each arrow. The left sides of the first equation give $\psi_1(\varphi(\sigma_1)) = \varphi(\tau_1)$, and the right sides of the second give $\psi_2(\varphi(\sigma_2)) = \varphi(\tau_2)$. $\square$

Remark: in Dudenhefner's printed proof of Lemma 35, the definition of $\varphi'(a_2)$ reads $\psi_1(\varphi(\sigma_1))$. The computation after it needs $\psi_1(\varphi(\sigma_2))$, as above. On the worked instance of the page, the printed form gives $\psi_1(\varphi'(\sigma')) = P \to P \to P$ but $\varphi'(\tau_1') = P \to P$, with $P = (a \to a) \to a \to a$. So the equation fails there, and the form above is the one that works.

## Step 2: pruning quantifiers out of a solution

Fix a type variable $p$. Define $\mathrm{prune}_p$ from all types to simple types by $\mathrm{prune}_p(b) = b$, $\mathrm{prune}_p(\rho \to \rho') = \mathrm{prune}_p(\rho) \to \mathrm{prune}_p(\rho')$ and $\mathrm{prune}_p(\forall b.\rho) = p$ (Dudenhefner, Definition 37).

**Lemma.** Let $\psi$ be any substitution, and let $\rho$ be a type in which $p$ does not occur. Define $\psi'(p) = p$ and $\psi'(b) = \mathrm{prune}_p(\psi(b))$ for $b \neq p$. Then $\psi'(\mathrm{prune}_p(\rho)) = \mathrm{prune}_p(\psi(\rho))$.

*Proof.* Induction on $\rho$. For a variable $b$, which differs from $p$, both sides are $\mathrm{prune}_p(\psi(b))$. For an arrow, use the induction hypothesis on both sides. For $\forall b.\rho_0$, the left side is $\psi'(p) = p$, and $\psi(\forall b.\rho_0)$ is again a $\forall$-type, so the right side is $p$ as well. $\square$

**Corollary.** Let $\sigma, \tau$ be simple, and let $\varphi, \psi$ be substitutions into arbitrary types with $\psi(\varphi(\sigma)) = \varphi(\tau)$. Pick $p$ not in $\varphi(\sigma)$. Then $\varphi' = \mathrm{prune}_p \circ \varphi$ maps into simple types, and with $\psi'$ from the lemma, $\psi'(\varphi'(\sigma)) = \varphi'(\tau)$.

*Proof.* For simple $\sigma$, $\mathrm{prune}_p(\varphi(\sigma)) = \varphi'(\sigma)$ by induction on $\sigma$, since $\sigma$ has no quantifier. So $\psi'(\varphi'(\sigma)) = \psi'(\mathrm{prune}_p(\varphi(\sigma))) = \mathrm{prune}_p(\psi(\varphi(\sigma))) = \mathrm{prune}_p(\varphi(\tau)) = \varphi'(\tau)$. $\square$

For an LU instance, one $p$ that is fresh for $\varphi(\sigma)$ serves both inequalities, and $\varphi'$ is shared. So a solution of LU in arbitrary types gives a solution in simple types.

## Step 3: LU reduces to typability in a fixed context

Let $(\sigma, \tau_1), (\sigma, \tau_2)$ be an LU instance. Put $S = \sigma \to \sigma$ and $U_i = \tau_i \to \tau_i$, and
$$\Gamma_I = \{\, x : \forall c.\,(c \to c) \to c,\ \ y : \forall.\,(U_1 \to U_2 \to S) \,\}.$$

**Claim.** $\Gamma_I \Vdash x\,(\lambda z.\,y\,z\,z)$ if and only if the instance is solvable.

*From a solution to a typing.* Let $\varphi, \psi_1, \psi_2$ solve the instance in simple types. Let $\vec a$ list the free variables of $\varphi(S)$, and let $\rho = \forall \vec a.\,\varphi(S)$. It is closed. In the context $\Gamma_I, z{:}\rho$:

- $y : \varphi(U_1) \to \varphi(U_2) \to \varphi(S)$ by Var and Inst, instantiating the closure with $\varphi$;
- $z : \psi_1(\varphi(S))$ by Var and Inst, instantiating $\vec a$ with $\psi_1$. This type equals $\psi_1(\varphi(\sigma)) \to \psi_1(\varphi(\sigma)) = \varphi(\tau_1) \to \varphi(\tau_1) = \varphi(U_1)$. Only the variables $\vec a$ matter here, since they are all the variables of $\varphi(S)$;
- in the same way, $z : \varphi(U_2)$;
- so $y\,z\,z : \varphi(S)$ by App twice, and $y\,z\,z : \rho$ by Gen on each variable of $\vec a$. This is allowed because $\Gamma_I$ and $\rho$ are closed.

Abs gives $\lambda z.\,y\,z\,z : \rho \to \rho$. Inst gives $x : (\rho \to \rho) \to \rho$, and App gives $\Gamma_I \vdash x\,(\lambda z.\,y\,z\,z) : \rho$.

*From a typing to a solution.* Take a derivation of $\Gamma_I \vdash x\,(\lambda z.\,y\,z\,z) : \theta_0$ with the property of Fact B. Read it from the leaves.

1. *The head $x$.* It must get an arrow type for the outer App. Var gives $\forall c.(c \to c) \to c$. The body is an arrow, so by the first remark, a chain of Inst steps ends in an arrow only after it instantiates $c$, and then it has $(\theta \to \theta) \to \theta$ for some type $\theta$. By the second remark, no Gen step follows. So the argument must get the type $\theta \to \theta$.
2. *The argument.* Abs gives $\lambda z.\,y\,z\,z$ a type $\rho \to \rho'$, where $\Gamma_I, z{:}\rho \vdash y\,z\,z : \rho'$. No Inst step applies to an arrow. A Gen step would give a $\forall$-type, not $\theta \to \theta$. So $\rho = \theta = \rho'$, and $\Gamma_I, z{:}\theta \vdash y\,z\,z : \theta$.
3. *The variable $y$.* It is the function of an App, so it gets an arrow type. Var gives the closed type $\forall \vec b.\,(U_1 \to U_2 \to S)$, and its body is an arrow. By the two remarks, all of $\vec b$ are instantiated and no Gen follows. So $y : \varphi(U_1) \to \varphi(U_2) \to \varphi(S)$ for a substitution $\varphi$ into arbitrary types.
4. *The term $y\,z$.* App gives it the type $\varphi(U_2) \to \varphi(S)$, and the first $z$ gets the type $\varphi(U_1)$. This type is an arrow, so no Inst follows. It is the function of the outer App, so no Gen follows. So the second $z$ gets the type $\varphi(U_2)$, and App gives $y\,z\,z$ the type $\varphi(S)$.
5. *The result of $y\,z\,z$.* $\varphi(S)$ is an arrow, so no Inst step follows, and only Gen steps can follow. So $\theta = \forall \vec a.\,\varphi(S)$ for some list $\vec a$.
6. *The two uses of $z$.* Var gives $\theta = \forall \vec a.\,\varphi(S)$. The result must be the arrow $\varphi(U_i)$. By the two remarks, all of $\vec a$ are instantiated, by some $\psi_i$ that moves only $\vec a$, and no Gen follows. So $\psi_i(\varphi(S)) = \varphi(U_i)$ for $i = 1, 2$.

Compare the left sides of the arrows in step 6: $\psi_i(\varphi(\sigma)) = \varphi(\tau_i)$ for $i = 1, 2$. This is a solution of the LU instance in arbitrary types. Step 2 turns it into a solution in simple types. $\square$

The doubled types $S = \sigma \to \sigma$ and $U_i = \tau_i \to \tau_i$ are arrows, whatever $\sigma$ and $\tau_i$ are. The argument above uses this in steps 4, 5 and 6. If $\sigma$ were a lone variable $b$ and $\varphi(b)$ were a $\forall$-type, Inst steps could reach inside $\varphi(\sigma)$, and the reading of the derivation would break.

## Step 4: closing the context (cited)

Typability asks for some context, so a free variable can get any type. Step 3 needs $x$ and $y$ to have exactly their types in $\Gamma_I$. For a term $N$, a term variable $v$ and a simple type $\sigma$, Dudenhefner's Lemma 29 (prenex simulation) builds a term $V$ in which $v$ is not free, such that for every context $\Gamma$ without $v$:
$$\Gamma \Vdash V \iff \Gamma, v : \forall.\sigma \Vdash N.$$
The construction applies $\lambda v.N$ to a term $V_1\,V_2$. That term is built so that each of its types gives $v$ no more freedom in $N$ than $\forall.\sigma$ does. It uses a few gadgets. One gadget forces a variable to have a type $c \to c$. Another assumption $w : \forall.\,a \to b \to b \to a$ lets the term build a value of any simple type from variables of the right types. Wells' Theorem 6.14 reaches the same goal with *invariant type assumptions*. Those are type assumptions that every derivation must use, and the construction is more general and much longer.

Apply the lemma twice: first with $v = x$ and the type of $x$ in $\Gamma_I$, then with $v = y$. The result is a closed term $M_I$, computable from the instance. By the lemma and Fact C, $M_I$ is typable if and only if $\Gamma_I \Vdash x\,(\lambda z.\,y\,z\,z)$ (Dudenhefner, Lemma 40). Together with Steps 1 to 3 and Fact A, TYP is undecidable (Dudenhefner, Corollary 41).

## Step 5: typability reduces to type checking

Let $M$ have free variables $x_1, \ldots, x_n$, and put $M' = K\,I\,(\lambda x_1 \ldots x_n.\,M)$ with $K = \lambda u v.\,u$ and $I = \lambda u.\,u$. We show that $M$ is typable if and only if $\vdash M' : \forall a.\,a \to a$ (Dudenhefner, Lemma 42).

*If $M$ is typable*, Fact C gives $x_1{:}\sigma_1, \ldots, x_n{:}\sigma_n \vdash M : \tau$. Abs $n$ times gives $\vdash \lambda x_1 \ldots x_n.\,M : \sigma_1 \to \cdots \to \sigma_n \to \tau$. Call this type $\pi$. Also $\vdash K : \forall a.\,a \to \forall b.\,b \to a$, by Abs, Gen, Abs and Gen. Inst with $a := \forall a.\,a \to a$ gives $K$ the type $(\forall a.a \to a) \to \forall b.\,b \to \forall a.\,a \to a$. Then $\vdash I : \forall a.\,a \to a$, so App gives $\vdash K\,I : \forall b.\,b \to \forall a.\,a \to a$. Inst with $b := \pi$ and App give $\vdash M' : \forall a.\,a \to a$.

*If $\vdash M' : \forall a.\,a \to a$*, the derivation contains a subderivation for the subterm $M$, in some context. So $M$ is typable.

The map $M \mapsto (\varnothing, M', \forall a.\,a \to a)$ is computable. So TC is undecidable (Dudenhefner, Corollary 43). $\square$

## Equivalence and the original route

Step 5 reduces TYP to TC. Wells' Theorem 6.15 reduces TC to TYP: given $\Gamma$, $M$ and $\tau$, it adds an assumption $z : \tau \to \bot$ for a fresh $z$, and it closes the context with Theorem 6.14. The resulting term contains $z\,M$, which can be typed only if $M$ has type $\tau$, up to a renaming of type variables. So the two problems are many-one equivalent (Wells, Theorem 6.16). Wells' own proof of undecidability goes from semi-unification to TC directly (Theorem 4.1). It uses the term $b\,(\lambda x.\,c\,x\,x)$, with a context that depends on the instance and a free result type $\beta$. That is the same pattern as Step 3, with $b$ in the role of $x$ and $c$ in the role of $y$.

## Recursive enumerability

A derivation is a finite tree, and each rule can be checked by a program. Listing all derivations by size and checking each one gives a procedure that halts exactly on the yes instances of TC. For TYP, the procedure also lists all candidate contexts and types. So both sets are recursively enumerable. Since they are not decidable, their complements are not recursively enumerable.
