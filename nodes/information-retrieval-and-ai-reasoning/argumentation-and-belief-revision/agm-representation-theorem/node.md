---
tag: TTTG6H
kind: theorem
slug: agm-representation-theorem
name: AGM representation theorem
aliases:
- partial meet representation theorem
area: information-retrieval-and-ai-reasoning/argumentation-and-belief-revision
level: advanced
summary: A contraction satisfies the basic AGM postulates if and only if it is a partial meet contraction for some selection function.
prereqs: [partial-meet-contraction, levi-identity]
see_also: [agm-postulates, epistemic-entrenchment, grove-spheres, katsuno-mendelzon-revision, belief-revision]
sources:
  - paper: doi:10.2307/2274239
    title: "Carlos E. Alchourrón, Peter Gärdenfors and David Makinson, On the logic of theory change: partial meet contraction and revision functions, Journal of Symbolic Logic 50(2), 510 to 530 (1985)"
    locator: the whole paper (the representation of the basic postulates by partial meet contraction, and of the full list by transitively relational partial meet contraction)
  - paper: "Peter Gärdenfors, Belief revision: an introduction, in Peter Gärdenfors (ed.), Belief Revision, Cambridge University Press (1992)"
    locator: Section 2.1 (the assumptions on Cn) and Section 3 (Theorems 7 and 8, and Theorems 1 and 2 for the passage to revision)
  - paper: doi:10.1016/0004-3702(91)90069-V
    title: Hirofumi Katsuno and Alberto O. Mendelzon, Propositional knowledge base revision and minimal change, Artificial Intelligence 52(3), 263 to 294 (1991)
    locator: Section 3 (the finite propositional form by faithful total preorders)
---

The AGM representation theorem says that the [AGM postulates](/agm-postulates/) for contraction describe exactly one construction. The basic postulates K÷1 to K÷6 hold for a contraction function if and only if it is a [partial meet contraction](/partial-meet-contraction/): the intersection of some chosen maximal subsets of $K$ that do not imply $p$. With the two supplementary postulates, the choice must come from a transitive preference among those subsets. By the [Levi identity](/levi-identity/), the same holds for revision. Alchourrón, Gärdenfors and Makinson proved it in 1985.

## Statement

**Setting.** $L$ is a language with a consequence operation $\mathrm{Cn}$ that is Tarskian ($A \subseteq \mathrm{Cn}(A)$, $A \subseteq B$ implies $\mathrm{Cn}(A) \subseteq \mathrm{Cn}(B)$, and $\mathrm{Cn}(\mathrm{Cn}(A)) = \mathrm{Cn}(A)$), includes classical propositional logic, is compact and satisfies the deduction theorem. These are the assumptions of AGM (1985), as restated by Gärdenfors (1992, Section 2.1). $K$ is a fixed belief set, and a contraction function for $K$ maps each sentence $p$ to a set $K \div p$.

**Theorem 1** (Gärdenfors 1992, Theorem 7). A contraction function for $K$ satisfies K÷1 to K÷6 if and only if it is a partial meet contraction, that is, $K \div p = \bigcap \gamma(K \perp p)$ for some selection function $\gamma$.

**Theorem 2** (Gärdenfors 1992, Theorem 8). A contraction function for $K$ satisfies K÷1 to K÷8 if and only if it is a transitively relational partial meet contraction.

**Corollary.** A revision function for $K$ satisfies K*1 to K*6 if and only if it is $K * p = (K \div \neg p) + p$ for a partial meet contraction $\div$, and it satisfies K*1 to K*8 if and only if $\div$ can be taken transitively relational.

The corollary follows from the theorems and the Levi and Harper identities (Gärdenfors 1992, Theorems 1 and 2), because the Harper identity applied to a revision with K*1 to K*6 gives a contraction with K÷1 to K÷6 whose Levi revision is the original one.

## In plain words

There is a short list of rules for giving up a belief. There is also a recipe: look at all the largest parts of what you believe that no longer support the belief, pick some of them, and keep only what all the picked parts agree on. The theorem says that the rules and the recipe fit exactly. Every way of picking gives a method that obeys the rules, and every method that obeys the rules comes from some way of picking. If you add two more rules about giving up two beliefs at once, the picking must follow a consistent ranking of the parts, best first. The same holds for adding a new belief that clashes with the old ones, because that is giving up its opposite and then adding it.

## Proof

We prove Theorem 1 in full and Theorem 2 in the finite propositional case. The general proof of Theorem 2 is in AGM (1985).

**A lemma on remainders.** If $p \in K$, $X \in K \perp p$ and $q \in K$, then $p \to q \in X$. Indeed, $p \to q \in K$. If $p \to q \notin X$, then by maximality $X \cup \{p \to q\}$ implies $p$, so by the deduction theorem $X$ implies $(p \to q) \to p$, which is classically equivalent to $p$. That contradicts $X \in K \perp p$.

**Partial meet contractions satisfy K÷1 to K÷6.** K÷1: each remainder is a belief set, and an intersection of belief sets is one. K÷2: each remainder is a subset of $K$. K÷3: if $p \notin K$, then $K \perp p = \{K\}$. K÷4: if not $\vdash p$, then $K \perp p$ is nonempty and no member contains $p$, so neither does the intersection. K÷5: by the lemma, $p \to q$ is in every remainder for each $q \in K$, so it is in $K \div p$, and $q \in (K \div p) + p$. K÷6: equivalent sentences have the same remainder set, and $\gamma$ is a function of the remainder set.

**A contraction with K÷1 to K÷6 is a partial meet contraction.** Let $\div$ satisfy K÷1 to K÷6. For $p \in K$ with not $\vdash p$, set

$$\gamma(K \perp p) = \{X \in K \perp p : K \div p \subseteq X\}.$$

AGM (1985) show that this depends only on $K \perp p$, so $\gamma$ is a function; in the finite case it is immediate, because $K \perp p$ determines $\mathrm{Mod}(\neg p)$ and so $p$ up to equivalence. For the other $p$, $\gamma$ gives $\{K\}$, and $K \div p = K$ holds: if $p \notin K$ this is K÷3, and if $\vdash p$ then $(K \div p) + p = K \div p$, so recovery and K÷2 give $K \div p = K$.

*$\gamma(K \perp p)$ is nonempty.* $K \div p \subseteq K$ does not imply $p$, by K÷4 and K÷1. By compactness it lies inside some $X \in K \perp p$.

*The intersection is $K \div p$.* Each selected $X$ contains $K \div p$, so $K \div p \subseteq \bigcap \gamma(K \perp p)$. For the other direction, let $q \in K$ with $q \notin K \div p$. By recovery and the deduction theorem, $p \to q \in K \div p$. The set $(K \div p) \cup \{q \to p\}$ does not imply $p$: otherwise $K \div p$ implies $(q \to p) \to p$, which is $p \vee q$, and with $p \to q$ it implies $q$, so $q \in K \div p$ by K÷1. Also $q \to p \in K$, because $p \in K$. By compactness there is $X \in K \perp p$ that contains $K \div p$ and $q \to p$. Then $X$ is selected, and $q \notin X$, since $q$ and $q \to p$ imply $p$. So $q \notin \bigcap \gamma(K \perp p)$. $\square$

**Theorem 2 for a finite language.** Let $L$ have $n$ atoms, $K = \mathrm{Cn}(\psi)$ and $M = \mathrm{Mod}(\psi)$. By the finite form on the [partial meet contraction](/partial-meet-contraction/) page, a partial meet contraction is given by sets $S(p) \subseteq \mathrm{Mod}(\neg p)$, nonempty for $p \in K$ with not $\vdash p$, with $\mathrm{Mod}(K \div p) = M \cup S(p)$. Identify the remainder $\mathrm{Cn}(M \cup \{w\})$ with the world $w$. Every nonempty set $T$ of worlds outside $M$ is $\mathrm{Mod}(\neg p)$ for some nontautological $p \in K$, namely the $p$ whose models are the other worlds. So a relation $\le$ that selects a nonempty set of best worlds from every such $T$ must, on the sets of one and two worlds, be reflexive and total. If it is also transitive, it is a total preorder, and $S(p)$ is the set of its best worlds in $\mathrm{Mod}(\neg p)$. Conversely every total preorder gives such a selection. So the transitively relational contractions are exactly those whose $S$ comes from a total preorder on the worlds outside $M$.

The Levi revision has $\mathrm{Mod}(K * \mu) = S(\neg \mu)$ when $\mu$ is inconsistent with $\psi$, and $M \cap \mathrm{Mod}(\mu)$ otherwise. By Theorems 1 and 2 of Gärdenfors (1992), and because the Harper identity gives back a contraction with recovery, $\div$ satisfies K÷7 and K÷8 if and only if $*$ satisfies K*7 and K*8. By the [Katsuno and Mendelzon theorem](/katsuno-mendelzon-revision/), that holds if and only if $*$ selects the best models of $\mu$ under a faithful total preorder, in which the worlds of $M$ come first and the order of the other worlds is free. Restricted to the worlds outside $M$, this is the total preorder that gives $S$. $\square$

**A check on two atoms.** For $K = \mathrm{Cn}(a \wedge b)$ there are 189 partial meet contractions, counting sentences up to equivalence. Every one satisfies K÷1 to K÷6. Exactly 13 satisfy K÷7 and K÷8, and they are the 13 contractions given by the 13 total preorders on the three worlds outside $\mathrm{Mod}(K)$.

## Consequences

- Each construction that gives the operators with all eight postulates gives exactly the transitively relational partial meet ones: [epistemic entrenchment](/epistemic-entrenchment/) (Gärdenfors and Makinson 1988), [systems of spheres](/grove-spheres/) (Grove 1988), and faithful total preorders on worlds for a finite language.
- Maxichoice and full meet contraction are special cases. They satisfy K÷1 to K÷6 and give revisions that are too strong and too weak.
- The theorem fixes one belief set $K$. It says nothing about how the selection for $K$ relates to the selection for $K * p$, which is the question of iterated revision and of the [Darwiche and Pearl postulates](/darwiche-pearl-postulates/).

## Tightness

- **Recovery is needed for Theorem 1.** For $K = \mathrm{Cn}(a \wedge b)$, the contraction that gives $\mathrm{Cn}(\emptyset)$ for each nontautological $p \in K$ satisfies every postulate but K÷5, and it is not a partial meet contraction: the meet of all remainders by $a$ is $\mathrm{Cn}(a \to b)$, and $\mathrm{Cn}(\emptyset)$ is strictly smaller.
- **Both supplementary postulates are needed for Theorem 2.** For the same $K$, 49 of the 189 partial meet contractions satisfy K÷7 and 45 satisfy K÷8, but only 13 satisfy both.
- **Compactness is used** to extend a set that does not imply $p$ to a remainder. Without it, $K \perp p$ can be empty for a sentence that is not a tautology, and the construction has nothing to select.

## History

Alchourrón and Makinson (1982) studied maxichoice contraction and found that its revisions decide every sentence. Gärdenfors had developed postulates for revision from the study of conditionals and of epistemic states. The three authors joined the two lines in the 1985 paper, defined partial meet contraction and proved both representation results. The theory took their initials as its name. Gärdenfors's book of 1988 gave a full account, and Gärdenfors and Makinson (1988), Grove (1988) and Katsuno and Mendelzon (1991) gave other constructions with the same operators.

## References
