---
tag: 58E93R
kind: technique
slug: reducibility-method
name: Reducibility method (Tait-Girard)
aliases:
- Tait's method
- logical relations for normalization
area: automata-and-parsing/term-rewriting
level: research
summary: A proof technique for strong normalization of typed terms by logical predicates.
prereqs: [beta-reduction, termination, structural-induction]
see_also: [lambda-calculus, weak-normalization, church-rosser-theorem, combinatory-logic, well-founded-relation, normal-form, godel-incompleteness-theorem]
sources:
  - paper: doi:10.2307/2271658
    title: W. W. Tait, Intensional interpretations of functionals of finite type I, Journal of Symbolic Logic 32(2) (1967)
    locator: pp. 198 to 212 (convertibility predicates defined by induction on types, and normalization for Gödel's system T)
  - book: isbn:9780521371810
    title: Jean-Yves Girard, Yves Lafont and Paul Taylor, Proofs and Types, Cambridge Tracts in Theoretical Computer Science 7, Cambridge University Press, 1989
    locator: chapter 6 (strong normalization of the simply typed calculus, properties CR1 to CR3), chapter 7 (system T) and chapter 14 (reducibility candidates and strong normalization for system F)
  - paper: doi:10.1016/S0019-9958(85)80001-2
    title: Richard Statman, Logical relations and the typed lambda-calculus, Information and Control 65(2/3) (1985)
    locator: pp. 85 to 97
---

The **reducibility method** proves that every well-typed term of a typed λ-calculus is strongly normalizing, meaning it has no infinite reduction sequence. A direct induction on terms does not work, because a reduction step can copy a term and make the whole term larger. The method instead defines, for each type, a set of "reducible" terms, by induction on the type, and with a stronger property at function types: a function is reducible if it sends reducible arguments to reducible results. It then shows that reducible terms are strongly normalizing, and that every typed term is reducible.

## In plain words

To show that a program cannot run forever, one would like to argue by the size of the program. But one step of evaluation can make the program bigger: calling a function that uses its argument twice copies that argument. So size does not go down.

The trick is to prove something stronger than termination, and to tailor it to each type. For plain data, the property is just "terminates". For a function, it is "terminates whenever it is given an argument with the property". The stronger statement is easier to prove by induction, because the property of a function already says what happens after a call, which is exactly what copying makes hard.

## When it applies

- The terms carry types, and the reduction rules remove an introduction followed by an elimination: $(\lambda x.\, v)\, u \to v[u/x]$ for functions, a projection of a pair, a case of an injection, a recursor on a numeral.
- The property to prove holds for a term whenever it holds for every one-step reduct; strong normalization is the main example. Variants prove weak normalization, confluence, or that two terms are equal in a model.
- The types are defined inductively, so that the predicate can be defined by induction on the type. For impredicative types, such as $\forall X.\, A$ in system F, the induction is replaced by a quantification over all candidate sets.

## The template

We write $t \to t'$ for one β step, $\to^*$ for the reflexive transitive closure, and $t\sigma$ for the result of a substitution $\sigma$ of terms for variables. $SN$ is the set of strongly normalizing terms. For $t \in SN$, $\nu(t)$ is the length of a longest reduction from $t$, finite because each term has finitely many one-step reducts. A term is **neutral** if it is not an abstraction, so that applying it to an argument creates no new redex at the top. The parts in angle brackets are the holes to fill for a given calculus.

```pseudo id=main
REDUCIBILITY(typed calculus, property P)
L1  for each type A, by induction on A, define RED_A ⊆ terms of type A:
L2      base type ι: RED_ι ← ⟨the terms of type ι with property P⟩
L3      A → B: RED_{A→B} ← { t | t u ∈ RED_B for every u ∈ RED_A }
L4      ⟨one clause per other type former, by its elimination: π₁ t ∈ RED_A and π₂ t ∈ RED_B for A × B⟩
L5  prove, by induction on A, for all A at once:
L6      (CR1) RED_A ⊆ P
L7      (CR2) t ∈ RED_A and t → t' imply t' ∈ RED_A
L8      (CR3) t neutral and every one-step reduct of t in RED_A imply t ∈ RED_A
L9  prove the introduction lemmas: ⟨if v[u/x] ∈ RED_B for every u ∈ RED_A, then λx. v ∈ RED_{A→B}⟩
L10 prove adequacy, by induction on t: if x₁ : A₁, …, xₙ : Aₙ ⊢ t : B and xᵢσ ∈ RED_{Aᵢ}, then tσ ∈ RED_B
L11 conclude: variables are neutral and normal, so they are reducible by CR3; take σ the identity in L10, and CR1 gives P
```

**Why the stronger property.** Line L3 is the key. A function is not reducible merely because it terminates: it must give reducible results on reducible arguments. That is what the application case of line L10 needs, and since it is stated for all reducible arguments, it survives substitution.

**The three properties for $A \to B$**, from the properties for $A$ and $B$, with $P = SN$:

- *CR1.* Let $t \in RED_{A \to B}$, and $x$ a variable of type $A$, reducible by CR3 for $A$. Then $t\, x \in RED_B \subseteq SN$, and an infinite reduction of $t$ would give one of $t\, x$.
- *CR2.* If $t \to t'$ and $u \in RED_A$, then $t\, u \to t'\, u$, and CR2 for $B$ gives $t'\, u \in RED_B$.
- *CR3.* Let $t$ be neutral with all reducts in $RED_{A \to B}$, and $u \in RED_A$; show $t\, u \in RED_B$ by induction on $\nu(u)$, which is finite by CR1 for $A$. The term $t\, u$ is neutral, and since $t$ is not an abstraction its reducts are $t'\, u$, in $RED_B$ by the assumption, and $t\, u'$ with $u \to u'$, in $RED_B$ by CR2 and the induction. CR3 for $B$ concludes.

**The abstraction lemma (line L9).** Suppose $v[u/x] \in RED_B$ for all $u \in RED_A$. Then $v = v[x/x] \in SN$. For $u \in RED_A$, show $(\lambda x.\, v)\, u \in RED_B$ by induction on $\nu(v) + \nu(u)$. This term is neutral, and its one-step reducts are $v[u/x]$, which is reducible by assumption, $(\lambda x.\, v')\, u$ with $v \to v'$, and $(\lambda x.\, v)\, u'$ with $u \to u'$. The last two are reducible by the induction, using CR2 for $v'[u/x]$ and for $u'$. CR3 concludes.

**Adequacy (line L10).** A variable $x_i$ gives $x_i\sigma \in RED_{A_i}$. An application $t\, u$ gives $(t\sigma)(u\sigma) \in RED_B$ by line L3. An abstraction $\lambda x.\, v$ gives, for every reducible $u$, $v(\sigma \cup \{x \mapsto u\}) = (v\sigma)[u/x] \in RED_B$ by the induction, and the abstraction lemma concludes. The statement must be about open terms under all reducible substitutions; for closed terms alone, the abstraction case has no induction hypothesis to use.

**Why size fails.** Let $g : \iota \to \iota \to \iota$ and $z : \iota$, and $t = (\lambda f.\, f\, (f\, z))\, (\lambda y.\, g\, y\, y)$. One step gives $(\lambda y.\, g\, y\, y)\, ((\lambda y.\, g\, y\, y)\, z)$, which is larger and has two redexes where $t$ had one. The longest reduction of $t$ has 4 steps and the shortest 3, both ending in $g\, (g\, z\, z)\, (g\, z\, z)$. In the reducibility proof, the copied argument $\lambda y.\, g\, y\, y$ is handled once, as a reducible term, wherever it is copied.

## Classic examples

- **Simply typed λ-calculus.** Types $\iota$ and $A \to B$, with $P = SN$ at line L2. The template gives strong normalization of all typed terms; Girard, Lafont and Taylor (chapter 6) present this proof with CR1 to CR3. By contrast, the untyped $(\lambda x.\, x\, x)(\lambda x.\, x\, x)$ reduces to itself, and it has no type.
- **Gödel's system T.** Add the natural numbers with $0$, successor and a recursor $R$, with $R\, u\, v\, 0 \to u$ and $R\, u\, v\, (S\, n) \to v\, (R\, u\, v\, n)\, n$. Line L2 takes $RED_{Nat} = SN$, and the introduction lemma for $R$ uses an induction on $\nu$ of the arguments and on the numeral. Tait (1967) introduced predicates of this kind, defined by induction on the type, to prove normalization for system T.
- **System F.** Types include $\forall X.\, A$, and $RED_{\forall X. A}$ would have to refer to $RED_B$ for every type $B$, including types larger than $\forall X.\, A$. Girard replaces the induction on types by **reducibility candidates**: sets of terms that satisfy CR1 to CR3. $RED_A[\mathcal{R}]$ is defined for every assignment $\mathcal{R}$ of candidates to the type variables, and $t \in RED_{\forall X. A}$ if $t\, B \in RED_A[X \mapsto \mathcal{C}]$ for every type $B$ and every candidate $\mathcal{C}$ of type $B$ (Girard, Lafont and Taylor, chapter 14).
- **Logical relations.** Replace the predicate by a relation between two interpretations, with the same clause at arrow types: related functions send related arguments to related results. The adequacy step becomes the statement that every term is related to itself. Statman (1985) develops logical relations for the simply typed λ-calculus.

## Variations

- **Saturated sets.** Instead of CR1 to CR3, use sets of strongly normalizing terms that contain every $x\, \vec w$ with $\vec w$ strongly normalizing and are closed under head expansion: if $v[u/x]\, \vec w$ is in the set and $u \in SN$, then so is $(\lambda x.\, v)\, u\, \vec w$. This avoids the inner inductions on $\nu$.
- **Weak normalization and confluence.** With $P$ the set of weakly normalizing terms, or terms that have a unique normal form, the same induction applies with adapted versions of CR1 to CR3.
- **Biorthogonality.** For calculi with control operators or with reduction in contexts, a type is interpreted by the terms that behave well in every reducible context, and the reducible contexts by the terms; the two definitions are closed under this double negation.
- **Step-indexed relations.** For recursive types, where the induction on types fails, the predicates are indexed also by a number of remaining steps, and defined by induction on the pair.

## Pitfalls

- **Defining $RED_{A \to B}$ as $SN$.** With the predicate equal to strong normalization at every type, the application case fails: $t$ and $u$ strongly normalizing does not give $t\, u$ strongly normalizing without knowing more about $t$.
- **Closed terms only.** Adequacy must quantify over all reducible substitutions for the free variables. Otherwise the abstraction case cannot use the induction on its body.
- **Forgetting neutrality.** CR3 is false for abstractions: $\lambda x.\, v$ applied to $u$ creates a redex at the top, whose reduct is not among the reducts of $\lambda x.\, v$. This is why the abstraction lemma is proved separately.
- **Measures on SN terms.** The inner inductions use $\nu$, which is finite only for strongly normalizing terms with finitely many reducts per step. In calculi with infinite branching, use well-founded induction on the reduction relation restricted to $SN$ instead.
- **Impredicativity.** For system F the definition of $RED_{\forall X. A}$ cannot be by induction on types. Without candidates, a definition by induction on types refers to sets not yet defined.

## Exercises

1. Show that CR3 implies that every variable of type $A$ is in $RED_A$.
2. Add pairs with $\pi_1 \langle u, v \rangle \to u$ and $\pi_2 \langle u, v \rangle \to v$. Using the clause at line L4, prove CR1 to CR3 for $A \times B$ and the introduction lemma for $\langle u, v \rangle$.
3. Show by an example that if $RED_{A \to B}$ were all strongly normalizing terms of type $A \to B$, the application case of adequacy would not follow from the induction hypothesis.
4. For system T, prove that $R\, u\, v\, n \in RED_A$ whenever $u$, $v$ and $n$ are reducible, by induction on $\nu(u) + \nu(v) + \nu(n)$ and the number of successors in the normal form of $n$.
5. Explain why the definition of $RED_{\forall X. A}$ in system F cannot be by induction on the size of the type, and check that the set of all strongly normalizing terms of a type is a reducibility candidate.

## References
