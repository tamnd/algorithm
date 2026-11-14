---
tag: DBPMSD
kind: theorem
slug: system-f-inference-undecidability
name: Undecidability of type inference for System F
aliases:
- Wells' theorem
area: compilers-and-program-analysis/type-systems-and-inference
level: advanced
summary: Without type annotations, no algorithm decides whether a pure lambda term has a System F type, or whether it has a given type. Wells proved it in 1994 by a reduction from semi-unification.
prereqs: [system-f, type-inference-problem, semi-unification-undecidability]
see_also: [system-f, semi-unification-problem, type-checking-problem, hindley-milner-type-system, bidirectional-type-checking, higher-order-unification-undecidability, undecidability, value-restriction]
sources:
  - paper: doi:10.1016/S0168-0072(98)00047-5
    title: Joe B. Wells, Typability and type checking in System F are equivalent and undecidable, Annals of Pure and Applied Logic 98(1-3), 1999, pages 111 to 156
    locator: Lemma 3.2 (the INST-before-GEN property), Theorem 4.1 (semi-unification reduces to type checking, also for the lambda-I calculus), Theorem 6.14 (invariant type assumptions), Theorem 6.15 (type checking reduces to typability), Theorem 6.16 (main result)
  - paper: doi:10.1109/LICS.1994.316068
    title: Joe B. Wells, Typability and type checking in the second-order lambda-calculus are equivalent and undecidable, Ninth Annual IEEE Symposium on Logic in Computer Science (LICS 1994), pages 176 to 185
    locator: the conference version of the main result
  - paper: "Andrej Dudenhefner, The undecidability of System F typability and type checking for reductionists, 36th Annual ACM/IEEE Symposium on Logic in Computer Science (LICS 2021), IEEE, 2021"
    locator: Problems 6 and 7 (the two decision problems), Example 33, Lemma 35 (left-uniform form), Definition 37 and Lemma 38 (pruning), Definition 19 and Lemma 29 (restricted typability and prenex simulation), Lemma 40 and Corollary 41 (typability), Lemma 42 and Corollary 43 (type checking), Section VII (the Coq mechanization)
  - paper: doi:10.1006/inco.1993.1003
    title: A. J. Kfoury, J. Tiuryn and P. Urzyczyn, The undecidability of the semi-unification problem, Information and Computation 102(1), 1993, pages 83 to 101
    locator: Theorem 12 and the remark after it (semi-unification is undecidable already for two inequalities)
  - paper: doi:10.1109/LICS.1988.5101
    title: Paola Giannini and Simona Ronchi Della Rocca, Characterization of typings in polymorphic type discipline, Third Annual Symposium on Logic in Computer Science (LICS 1988), pages 61 to 70
    locator: the normal form for derivations in which instantiation comes before generalization
  - paper: doi:10.1145/182409.182456
    title: A. J. Kfoury and J. B. Wells, A direct algorithm for type inference in the rank-2 fragment of the second-order lambda-calculus, ACM Conference on LISP and Functional Programming (LFP 1994), pages 196 to 207
    locator: the introduction (typability is decidable at rank 2 and undecidable at every rank of 3 or more) and the rank-2 inference algorithm
  - paper: "Frank Pfenning, Partial polymorphic type inference and higher-order unification, ACM Conference on LISP and Functional Programming (LFP 1988)"
    locator: the undecidability of partial type reconstruction, where the places of type abstractions and type applications are given, by reduction from second-order unification
---

Wells' theorem says that type inference for [System F](/system-f/) is impossible in general. Take a pure lambda term with no type annotations. No algorithm can decide whether the term has a System F type. No algorithm can decide whether it has a given type in a given context. Leivant asked the question in 1983, and it stayed open until Wells solved it in 1994. His proof reduces [semi-unification](/semi-unification-problem/), which Kfoury, Tiuryn and Urzyczyn proved [undecidable](/semi-unification-undecidability/), to type checking. Then it reduces type checking to typability. The theorem is the reason that languages with first-class polymorphism ask for annotations. It also explains why ML keeps to the [prenex fragment](/hindley-milner-type-system/).

## Statement

**Curry-style System F.** Types are $\sigma ::= a \mid \sigma \to \sigma \mid \forall a.\,\sigma$. Terms are pure: $M ::= x \mid \lambda x.\,M \mid M\,M$. A context $\Gamma$ gives types to term variables. The rules are:

- **Var:** $\Gamma \vdash x : \Gamma(x)$.
- **Abs:** from $\Gamma, x{:}\sigma \vdash M : \tau$, derive $\Gamma \vdash \lambda x.M : \sigma \to \tau$.
- **App:** from $\Gamma \vdash M : \sigma \to \tau$ and $\Gamma \vdash N : \sigma$, derive $\Gamma \vdash M\,N : \tau$.
- **Gen:** from $\Gamma \vdash M : \sigma$ with $a$ not free in $\Gamma$, derive $\Gamma \vdash M : \forall a.\sigma$.
- **Inst:** from $\Gamma \vdash M : \forall a.\sigma$, derive $\Gamma \vdash M : [a := \tau]\sigma$.

A term is the erasure of a Church-style term exactly when it has a type in this system.

**Theorem (Wells 1994, 1999).** The following two problems are undecidable, and each one reduces to the other by a computable map.

1. **Typability (TYP).** Given a term $M$, are there a context $\Gamma$ and a type $\tau$ with $\Gamma \vdash M : \tau$?
2. **Type checking (TC).** Given $\Gamma$, $M$ and $\tau$, is $\Gamma \vdash M : \tau$ derivable?

Both problems stay undecidable for terms of the $\lambda I$-calculus, where every bound variable occurs in its body (Wells, Theorem 4.1 and Theorem 6.16). Both sets are recursively enumerable, because derivations can be listed and checked one by one. So the complement of each set is not recursively enumerable.

## In plain words

A Church-style System F program writes every type argument. Checking such a program is easy. This theorem is about the other case, where the programmer writes no types and the compiler must find them all.

The compiler cannot do that in general. A finished type checker would also solve a puzzle that is known to have no solution procedure. In that puzzle, you fill in a pattern once, and the result must then match two other patterns, where each match may fill the leftover blanks in its own way. A polymorphic variable that is used twice behaves exactly like this. Its type is chosen once and then specialized two times. A small fixed program shape copies any such puzzle into a typing question.

So languages with this much polymorphism ask the programmer to write some types, or they limit where polymorphism can appear.

## Proof

The [proof file](proofs/main.md) is a sketch. It proves the small steps in full. It proves the central reduction from semi-unification in full, in a context with two free variables. It cites the construction that closes this context. The plan follows Dudenhefner (2021), who gave a direct reduction to typability. That proof is checked in Coq. Wells' original route goes from semi-unification to type checking first.

1. **Two-inequality semi-unification is undecidable.** An instance is two pairs $(\sigma_1, \tau_1), (\sigma_2, \tau_2)$ of simple types, which have no quantifiers. A solution is three substitutions $\varphi, \psi_1, \psi_2$ with $\psi_i(\varphi(\sigma_i)) = \varphi(\tau_i)$ for $i = 1, 2$. Kfoury, Tiuryn and Urzyczyn show that this restricted problem is already undecidable (cited).
2. **Left-uniform form.** Put $\sigma' = \sigma_1 \to \sigma_2$, $\tau_1' = \tau_1 \to a_2$ and $\tau_2' = a_1 \to \tau_2$, with fresh $a_1, a_2$. The instance $(\sigma', \tau_1'), (\sigma', \tau_2')$ is solvable if and only if the original one is. Both pairs now share the same left side.
3. **The core term.** For a left-uniform instance $(\sigma, \tau_1), (\sigma, \tau_2)$, let $S = \sigma \to \sigma$ and $U_i = \tau_i \to \tau_i$. Let $\forall.\rho$ be the closure of $\rho$ over all its free variables, and let
   $$\Gamma_I = \{\, x : \forall c.\,(c \to c) \to c,\ \ y : \forall.\,(U_1 \to U_2 \to S) \,\}.$$
   Then $x\,(\lambda z.\,y\,z\,z)$ has a type in $\Gamma_I$ if and only if the instance is solvable. The idea fits in one line. The variable $z$ gets one polymorphic type $\forall \vec a.\,\varphi(S)$, and its two uses instantiate that type in two ways, to $\varphi(U_1)$ and to $\varphi(U_2)$. The bound variables $\vec a$ play the part of the residual substitutions $\psi_1, \psi_2$. The variable $x$ forces the type of $y\,z\,z$ to be the type of $z$ again. The proof of the converse uses the normal form of Giannini and Ronchi Della Rocca, also Wells' Lemma 3.2, in which every Inst step comes before every Gen step. A solution may hold System F types. A pruning map sends it to a solution in simple types.
4. **Closing the context.** A typability question cannot fix the types of free variables. Dudenhefner's prenex simulation (Lemma 29) builds a closed term $M_I$ that is typable if and only if $x\,(\lambda z.\,y\,z\,z)$ is typable in $\Gamma_I$. Wells' Theorems 6.14 and 6.15 do the same job with invariant type assumptions, a more general tool. This step is cited.
5. **From typability to type checking.** Send $M$, with free variables $x_1, \ldots, x_n$, to the question of whether $\vdash K\,I\,(\lambda x_1 \ldots x_n.\,M) : \forall a.\,a \to a$, where $K = \lambda u v.\,u$ and $I = \lambda u.\,u$. The answer is yes exactly when $M$ is typable.

Steps 1 to 4 show that TYP is undecidable. Step 5 gives the same for TC. Wells' Theorem 6.15 reduces TC to TYP, so the two problems are equivalent.

### A worked instance

Dudenhefner's Example 33 is the instance $(a,\ b \to b), (a \to a,\ b)$. It has no unifier: we would need $a = b \to b$ and $b = a \to a$, which fails the occurs check. But it is semi-unifiable with
$$\varphi(a) = a,\quad \varphi(b) = a \to a,\quad \psi_1(a) = (a \to a) \to a \to a,\quad \psi_2(a) = a.$$
Then $\psi_1(\varphi(a)) = (a \to a) \to a \to a = \varphi(b \to b)$ and $\psi_2(\varphi(a \to a)) = a \to a = \varphi(b)$.

In left-uniform form, $\sigma' = a \to a \to a$, $\tau_1' = (b \to b) \to a_2$ and $\tau_2' = a_1 \to b$. The proof extends $\varphi$ by $\varphi(a_1) = \psi_2(\varphi(\sigma_1)) = a$ and $\varphi(a_2) = \psi_1(\varphi(\sigma_2)) = P \to P$, where $P = (a \to a) \to a \to a$. The type of $z$ is then
$$\rho = \forall a.\,(a \to a \to a) \to a \to a \to a,$$
and the Church-style term
$$x\,[\rho]\,\big(\lambda z{:}\rho.\ \Lambda a.\ y\,[\varphi(a)]\,[\varphi(b)]\,[\varphi(a_1)]\,[\varphi(a_2)]\ (z\,[\psi_1(a)])\ (z\,[\psi_2(a)])\big)$$
has type $\rho$ in $\Gamma_I$. Its erasure is $x\,(\lambda z.\,y\,z\,z)$. A script with a Church-style checker for System F confirms the two equations, the left-uniform equations, the type $\rho$ and the erasure.

A one-line contrast shows that semi-unification is a strict weakening of unification. The single pair $(a,\ a \to b)$ has no unifier, but it is semi-unifiable: take $\varphi = \mathrm{id}$ and $\psi(a) = a \to b$. The pair $(a \to b,\ a)$ has no solution at all, because $\psi(\varphi(a \to b))$ is always larger than $\varphi(a)$. The script finds no solution with types of size at most 3, as this size argument predicts.

## Consequences

- **First-class polymorphism needs annotations.** A language that allows $\forall$ anywhere in a type cannot infer all types. In Haskell with GHC's `RankNTypes` extension, a lambda-bound variable gets a polymorphic type only from a written signature. GHC then pushes the written types into the term, in the style of [bidirectional type checking](/bidirectional-type-checking/).
- **ML's restriction is not an accident.** [Hindley-Milner](/hindley-milner-type-system/) allows $\forall$ only at the outside of a type and only at `let`. That fragment has principal types and a complete inference algorithm.
- **Church style and Curry style differ.** For Church-style System F, type checking is one bottom-up pass, as on the [type checking problem](/type-checking-problem/) page. All the difficulty sits in the missing annotations.
- **Typability and checking are equally hard.** The Hindley-Milner world might suggest that checking is easier than inference. For Curry-style System F, the two problems are equivalent.
- **Semi-algorithms are the best possible.** A complete type inference tool for System F must run forever on some untypable terms.

## Tightness

- **Rank.** A type has rank $k$ if no $\forall$ lies to the left of $k$ or more arrows, counting nesting. Typability is decidable for rank 2. It is undecidable for every rank of 3 or more (Kfoury and Wells 1994). So the boundary sits between rank 2 and rank 3.
- **Partial annotations.** Pfenning (1988) showed that it stays undecidable if the places of type abstractions and type applications are known and only the types are missing. His reduction uses second-order unification, which is [undecidable](/higher-order-unification-undecidability/).
- **Full annotations.** With all type arguments written, the problem is decidable, as stated above.
- **Small fragments of terms.** Wells' reduction uses only $\lambda I$-terms. Step 3 above uses one fixed core term shape and only types without nested quantifiers, so the hardness does not need rich types (Dudenhefner, abstract).

## History

Girard (1972) and Reynolds (1974) defined System F with explicit types. Leivant presented the Curry-style system in 1983 and made the first attempt at typability. Henglein showed that typability is DEXPTIME-hard. Boehm and Pfenning showed that partial type reconstruction for Church-style terms is undecidable. Urzyczyn showed that typability is undecidable for the stronger system $F_\omega$. For System F itself, Wells' paper calls the two questions "embarrassing open problems" up to 1994 (Wells 1999, Section 1.2). Kfoury, Tiuryn and Urzyczyn proved semi-unification undecidable in 1990, and the journal paper appeared in 1993. Wells used that result to settle the question in 1994. His journal paper of 1999 adds the full theory of invariant type assumptions. Dudenhefner (2021) gave a short direct reduction to typability, and he checked it in the Coq Library of Undecidability Proofs. That library also has a reduction from Turing machine halting to semi-unification. Together they give a fully checked reduction from halting to System F typability and type checking.

## References
