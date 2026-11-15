---
tag: XHY6XG
kind: model
slug: grove-spheres
name: Grove system of spheres
aliases:
- Grove spheres
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: Nested sets of possible worlds around the current beliefs; revision by p picks the p-worlds in the smallest sphere that meets p.
prereqs: [agm-postulates]
see_also: [katsuno-mendelzon-revision, epistemic-entrenchment, agm-representation-theorem, levi-identity, ordinal-conditional-functions, dalal-revision, total-order, kripke-structure]
sources:
  - paper: doi:10.1007/BF00247909
    title: Adam Grove, Two modellings for theory change, Journal of Philosophical Logic 17(2), 157 to 170 (1988)
    locator: the whole paper (systems of spheres, the revision they define, and the proof that these are exactly the revisions with K*1 to K*8)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 2.1 (the assumptions on Cn) and Section 3 (the postulates K*1 to K*8 that the spheres model)
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (faithful total preorders, the finite form of a system of spheres)
---

A system of spheres is a picture of a revision function. The worlds that agree with the current beliefs $K$ form the innermost sphere. Around it lie larger and larger spheres, each one a set of worlds that are less and less plausible. To revise by $p$, take the smallest sphere that contains a world where $p$ is true, and believe what is true in all the $p$-worlds of that sphere. Adam Grove (1988) showed that these revisions are exactly the ones that satisfy all eight [AGM postulates](/agm-postulates/). The idea comes from the spheres that David Lewis used for counterfactual conditionals.

## The machine

**Setting.** The language $L$ has a consequence operation $\mathrm{Cn}$ that includes classical propositional logic, is compact and satisfies the deduction theorem, as in the AGM theory. A world is a maximal consistent set of sentences, and $M_L$ is the set of all worlds. For a set of sentences $A$, $[A]$ is the set of the worlds that contain $A$, and $[p] = [\{p\}]$. For a set $W$ of worlds, $\mathrm{Th}(W) = \bigcap W$ is the set of the sentences true in all of them, with $\mathrm{Th}(\emptyset) = K_\bot$. For each belief set, $\mathrm{Th}([K]) = K$, by compactness and the Lindenbaum construction.

**Spheres.** A system of spheres centred on $[K]$ is a collection $\mathcal{S}$ of subsets of $M_L$ such that

| | condition |
|---|---|
| S1 | $\mathcal{S}$ is totally ordered by $\subseteq$ |
| S2 | $[K] \in \mathcal{S}$, and $[K] \subseteq U$ for each $U \in \mathcal{S}$ |
| S3 | $M_L \in \mathcal{S}$ |
| S4 | if $[p] \ne \emptyset$, then there is a smallest sphere $c(p) \in \mathcal{S}$ with $c(p) \cap [p] \ne \emptyset$ |

**The revision it defines.** Let $f(p) = [p] \cap c(p)$ when $[p]$ is nonempty, and $f(p) = \emptyset$ otherwise. Then

$$K * p = \mathrm{Th}(f(p)).$$

**The contraction it defines.** By the Harper identity, $K \div p = K \cap (K * \neg p)$, so $[K \div p] = [K] \cup f(\neg p)$: add to the worlds of $K$ the most plausible worlds where $p$ is false.

**The finite case.** If $L$ has $n$ atoms, a world is a truth assignment, there are $2^n$ of them, and every set of worlds is $[p]$ for some $p$. A system of spheres is then the same as a total preorder on worlds whose least elements are the models of $K$: the spheres are the sets $\{w : r(w) \le j\}$ for a rank function $r$ with $r(w) = 0$ exactly on $[K]$. S4 holds automatically, because there are finitely many spheres.

## What it counts

The model measures how far a world is from the current beliefs by the index of the first sphere that holds it. Revision by $p$ moves to the nearest $p$-worlds. It does not count how many atoms change or how many sentences are lost; the spheres can be any nested sets that meet S1 to S4. In the finite case, different systems of spheres give different revision functions, so the spheres hold exactly the information that the revision function holds.

**Example.** Take two atoms $a, b$, $K = \mathrm{Cn}(a \wedge b)$, and the spheres

$$U_0 = \{ab\} \subset U_1 = \{ab, \bar a b\} \subset U_2 = \text{all four worlds},$$

where $\bar a$ means that $a$ is false.

| revise by | $[p]$ | $c(p)$ | $f(p)$ | $K * p$ |
|---|---|---|---|---|
| $\neg a$ | $\bar a b$, $\bar a \bar b$ | $U_1$ | $\bar a b$ | $\mathrm{Cn}(\neg a \wedge b)$ |
| $\neg b$ | $a \bar b$, $\bar a \bar b$ | $U_2$ | $a \bar b$, $\bar a \bar b$ | $\mathrm{Cn}(\neg b)$ |
| $\neg (a \wedge b)$ | all but $ab$ | $U_1$ | $\bar a b$ | $\mathrm{Cn}(\neg a \wedge b)$ |
| $a \vee b$ | all but $\bar a \bar b$ | $U_0$ | $ab$ | $K$ |

The last row is K*4 at work: $a \vee b$ is consistent with $K$, so the innermost sphere already meets it. The second row shows the price of a coarse outer sphere: after learning $\neg b$ the agent no longer knows $a$. The same spheres give the entrenchment of the example on [epistemic entrenchment](/epistemic-entrenchment/).

## Relation to other models

- **AGM postulates.** Grove's theorem below says that systems of spheres and revisions with K*1 to K*8 are the same thing.
- **Partial meet contraction.** A remainder of $K$ by $p$ corresponds to $[K] \cup \{w\}$ for one world $w$ where $p$ is false. A transitively relational selection is a preference among these worlds, and that preference is a system of spheres; see the [AGM representation theorem](/agm-representation-theorem/).
- **Epistemic entrenchment.** $p \le q$ holds when every sphere that meets $[\neg q]$ also meets $[\neg p]$: a sentence is as firm as the smallest sphere that refutes it.
- **Faithful preorders.** For a finite language, the faithful total preorder $\le_\psi$ of the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/) is the system of spheres for $\mathrm{Cn}(\psi)$.
- **Ranks.** [Ordinal conditional functions](/ordinal-conditional-functions/) number the spheres, so that the numbers can be shifted in iterated revision.
- **Distances.** [Dalal's operator](/dalal-revision/) uses the spheres "within Hamming distance $k$ of a model of $K$".
- **Lewis's spheres.** For counterfactuals, Lewis centres the spheres on one world, the actual one. Grove centres them on the set $[K]$ of the worlds that the agent cannot rule out. Like a [Kripke structure](/kripke-structure/), the model is a set of worlds with extra structure that gives meaning to a modal operation.

## Known results in the model

**Theorem** (Grove 1988). Let $\mathcal{S}$ be a system of spheres centred on $[K]$. Then the revision $K * p = \mathrm{Th}(f(p))$ satisfies K*1 to K*8. Conversely, for each revision function for $K$ that satisfies K*1 to K*8 there is a system of spheres centred on $[K]$ that defines it.

*Proof sketch, first part.* K*1 holds because $\mathrm{Th}$ of a set of worlds is a belief set. K*2 holds because $f(p) \subseteq [p]$. If $[p] \cap [K] \ne \emptyset$, then $c(p) = [K]$ by S2, so $f(p) = [K] \cap [p] = [K + p]$, which gives K*3 and K*4; if $[p] \cap [K] = \emptyset$, then $K + p = K_\bot$ and K*3 is trivial. K*5 holds because $f(p)$ is nonempty exactly when $[p]$ is, by S3 and S4. K*6 holds because $f$ depends only on $[p]$. For K*7 and K*8, suppose $f(p) \cap [q] \ne \emptyset$. Every sphere that meets $[p \wedge q]$ meets $[p]$, so $c(p) \subseteq c(p \wedge q)$, and $c(p)$ meets $[p \wedge q]$, so $c(p \wedge q) \subseteq c(p)$. So $f(p \wedge q) = f(p) \cap [q]$, and $K * (p \wedge q) = (K * p) + q$. If instead $f(p) \cap [q] = \emptyset$, then $\neg q \in K * p$, so $(K * p) + q = K_\bot$, K*7 is trivial and K*8 does not apply.

*Proof sketch, second part.* Given $*$, Grove defines the spheres from the sets $[K * p]$ and uses K*7 and K*8 to show that they are nested and satisfy S4. For a finite language a direct construction is: $w \le v$ if and only if $w \in [K * \varphi_{w,v}]$, where $\varphi_{w,v}$ is a sentence true exactly in $w$ and $v$. K*7 and K*8 make $\le$ a total preorder, K*3 and K*4 make the models of $K$ its least elements, and the spheres are the sets $\{w : w \le v\}$. This is the proof of Katsuno and Mendelzon (1991). $\square$

**Counting in the finite case.** If $\mathrm{Mod}(K)$ has $m$ of the $2^n$ worlds, the systems of spheres centred on it are the total preorders on the other $2^n - m$ worlds placed above $\mathrm{Mod}(K)$, so their number is the ordered Bell number of $2^n - m$. For $K = \mathrm{Cn}(a \wedge b)$ there are 13, and they give the 13 distinct revisions for $K$ that satisfy K*1 to K*8.

## References
