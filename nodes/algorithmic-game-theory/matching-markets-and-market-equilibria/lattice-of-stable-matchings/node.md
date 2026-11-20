---
tag: 5RCMG6
kind: theorem
slug: lattice-of-stable-matchings
name: Lattice of stable matchings
aliases:
- Conway's lattice theorem
area: algorithmic-game-theory/matching-markets-and-market-equilibria
level: core
summary: The stable matchings form a distributive lattice under the common preference of one side, with the two proposer-optimal matchings at the ends.
prereqs: [stable-matching, gale-shapley]
see_also: [stable-matching-rotations, egalitarian-stable-matching, rural-hospitals-theorem, deferred-acceptance-strategyproofness, knaster-tarski-theorem, hospitals-residents-problem, stable-roommates-problem, stable-matching-with-ties]
sources:
  - paper: doi:10.2307/2312726
    title: David Gale and Lloyd S. Shapley, College admissions and the stability of marriage, American Mathematical Monthly 69(1), 9 to 15 (1962)
    locator: the whole paper (existence of a stable matching that is optimal for the proposing side)
  - paper: doi:10.1137/0215048
    title: Robert W. Irving and Paul Leather, The complexity of counting stable marriages, SIAM Journal on Computing 15(3), 655 to 667 (1986)
    locator: the whole paper (rotations, the rotation poset, and the counting problem)
  - paper: doi:10.1016/0097-3165(84)90056-6
    title: Charles Blair, Every finite distributive lattice is a set of stable matchings, Journal of Combinatorial Theory, Series A 37(3), 353 to 356 (1984)
    locator: the whole paper
  - paper: doi:10.1016/0097-3165(87)90037-9
    title: Dan Gusfield, Robert W. Irving, Paul Leather and Michael Saks, Every finite distributive lattice is a set of stable matchings for a small stable marriage instance, Journal of Combinatorial Theory, Series A 44(2), 304 to 309 (1987)
    locator: the whole paper
  - paper: doi:10.1137/0216010
    title: Dan Gusfield, Three fast algorithms for four problems in stable marriage, SIAM Journal on Computing 16(1), 111 to 128 (1987)
    locator: the whole paper (enumeration of all stable matchings with rotations)
  - book: isbn:9780262071185
    title: Dan Gusfield and Robert W. Irving, The Stable Marriage Problem, Structure and Algorithms, MIT Press (1989)
    locator: the chapter on the structure of the set of stable matchings
---

The stable matchings of a marriage market are not just a set: they form a distributive lattice. Order them by the men's preferences; then for any two stable matchings, giving each man the better of his two partners is again a stable matching, and it gives each woman the worse of her two partners. The top of the lattice is the man-optimal matching found by men-proposing [deferred acceptance](/gale-shapley/), and the bottom is the woman-optimal one. The [rotations](/stable-matching-rotations/) of Irving and Leather describe this lattice compactly, the [rural hospitals theorem](/rural-hospitals-theorem/) says which agents are matched in all its elements, and the [egalitarian stable matching](/egalitarian-stable-matching/) is an optimization over it.

## Statement

A marriage market has a set $M$ of men and a set $W$ of women, each with a strict order over the other side and the option to stay single. Let $\mathcal{S}$ be the set of stable matchings. For $\mu, \mu' \in \mathcal{S}$, write $\mu \succeq_M \mu'$ when every man weakly prefers $\mu(m)$ to $\mu'(m)$, and $\mu \succeq_W \mu'$ in the same way for women. Define $\mu \vee \mu'$ as the assignment that gives each man the better of $\mu(m)$ and $\mu'(m)$ in his own order, and $\mu \wedge \mu'$ as the one that gives each man the worse.

**Theorem (Conway; Knuth 1976).** For all $\mu, \mu' \in \mathcal{S}$:

1. $\mu \vee \mu'$ and $\mu \wedge \mu'$ are matchings, and they are stable.
2. In $\mu \vee \mu'$ each woman gets the worse of $\mu(w)$ and $\mu'(w)$ in her order, and in $\mu \wedge \mu'$ she gets the better.
3. $(\mathcal{S}, \succeq_M)$ is a distributive lattice with join $\vee$ and meet $\wedge$. Its top is the man-optimal stable matching $\mu_M$ and its bottom is the woman-optimal stable matching $\mu_W$.
4. (Polarity.) $\mu \succeq_M \mu'$ if and only if $\mu' \succeq_W \mu$.

**Converse (Blair 1984).** Every finite distributive lattice is isomorphic to the lattice of stable matchings of some marriage market. Gusfield, Irving, Leather and Saks (1987) showed that a small market suffices.

## In plain words

Take two stable matchings. Let every man pick the partner he likes more from the two. This gives a valid matching, since no two men pick the same woman, and it is stable again. Each woman ends up with the partner she likes less from the two. The same works if every man picks the one he likes less. So the stable matchings can be ordered from best for the men to best for the women. What is good for all men is bad for all women. At the top sits the matching that deferred acceptance gives when men propose, and at the bottom the one it gives when women propose.

## Proof

Fix stable $\mu$ and $\mu'$. Let $M_\mu$ be the men who strictly prefer $\mu$ to $\mu'$, $M_{\mu'}$ those who strictly prefer $\mu'$, and define $W_\mu$, $W_{\mu'}$ for the women in the same way.

**Lemma (opposite interests).** $\mu$ maps $M_\mu$ one to one onto $W_{\mu'}$, and $\mu'$ maps $M_{\mu'}$ one to one onto $W_\mu$.

*Proof.* Let $m \in M_\mu$. Then $\mu(m)$ is better than $\mu'(m)$, which is acceptable or single, so $\mu(m) = w$ is a woman, and $\mu'(m) \ne w$. If $w$ weakly preferred $m$ to $\mu'(w)$, she would strictly prefer him, since $\mu'(w) \ne m$, and $(m, w)$ would block $\mu'$. So $w \in W_{\mu'}$, and $\mu$ maps $M_\mu$ into $W_{\mu'}$. Now let $w \in W_{\mu'}$. Then $m' = \mu'(w)$ is a man, and $w$ strictly prefers $m'$ to $\mu(w)$. As $\mu$ is stable, $(m', w)$ does not block it, so $m'$ prefers $\mu(m')$ to $w = \mu'(m')$, strictly because $\mu(m') \ne w$. So $\mu'$ maps $W_{\mu'}$ into $M_\mu$. Both maps are injective, so $|M_\mu| = |W_{\mu'}|$ and both are bijections. The second statement follows by swapping $\mu$ and $\mu'$. $\square$

*Parts 1 and 2.* Let $\lambda = \mu \vee \mu'$. A man in $M_\mu$ gets $\mu(m)$, a woman of $W_{\mu'}$; a man in $M_{\mu'}$ gets $\mu'(m)$, a woman of $W_\mu$; every other man gets the common partner $\mu(m) = \mu'(m)$, and that woman also has $\mu(w) = \mu'(w)$. By the lemma these three groups of women are disjoint and each is hit once, so $\lambda$ is a matching. Each woman of $W_{\mu'}$ gets $\mu(w)$, her worse partner, and each woman of $W_\mu$ gets $\mu'(w)$, also her worse partner. All partners in $\lambda$ are partners in $\mu$ or $\mu'$, so they are acceptable. Suppose $(m, w)$ blocks $\lambda$. Then $m$ prefers $w$ to both $\mu(m)$ and $\mu'(m)$. Say $\lambda(w) = \mu(w)$; then $w$ prefers $m$ to $\mu(w)$, and $(m, w)$ blocks $\mu$. If $\lambda(w) = \mu'(w)$, the pair blocks $\mu'$. Both are impossible, so $\lambda$ is stable. The meet $\mu \wedge \mu'$ is the join for the women, so the same proof applies with the roles of the sides swapped.

*Part 3.* Each man's partner in $\mu \vee \mu'$ is the maximum of his two partners in a chain (his order), so any stable $\nu$ with $\nu \succeq_M \mu$ and $\nu \succeq_M \mu'$ has $\nu \succeq_M \mu \vee \mu'$. Hence $\vee$ is the least upper bound, and $\wedge$ is the greatest lower bound in the same way. The identity $\mu \vee (\mu' \wedge \mu'') = (\mu \vee \mu') \wedge (\mu \vee \mu'')$ holds man by man, because maximum and minimum on a chain distribute over each other. A finite lattice has a top and a bottom; by the theorem of Gale and Shapley, the top is $\mu_M$, which every man weakly prefers to every stable matching, and the bottom is $\mu_W$.

*Part 4.* If $\mu \succeq_M \mu'$, then $M_{\mu'}$ is empty, so $W_\mu$ is empty by the lemma, which says $\mu' \succeq_W \mu$. The converse is symmetric. $\blacksquare$

## Consequences

- **Optimal matchings.** The lattice gives a second proof that a man-optimal and a woman-optimal stable matching exist, and polarity says that the man-optimal one is the woman-pessimal one.
- **Rotations.** Irving and Leather (1986) showed that the lattice is the lattice of closed sets (down-sets) of a partial order on rotations, a set of at most $n(n-1)/2$ elements for $n$ men and $n$ women. Moving down the lattice one step eliminates one rotation. See [stable matching rotations](/stable-matching-rotations/).
- **Algorithms.** Gusfield (1987) used rotations to list all stable matchings in $O(n^2 + n|\mathcal{S}|)$ time. The number of stable matchings can be exponential in $n$, and counting them is #P-complete (Irving and Leather 1986).
- **Optimization over the lattice.** A weighted objective that is a sum over agents becomes a weight on rotations, and optimizing it becomes a maximum-weight closure problem: see [egalitarian stable matching](/egalitarian-stable-matching/).
- **Same matched agents.** All elements of the lattice match the same set of agents; see the [rural hospitals theorem](/rural-hospitals-theorem/).
- **Fixed points.** Stable matchings are the fixed points of a monotone map on a complete lattice of proposals, so the lattice structure is also an instance of the [Knaster-Tarski theorem](/knaster-tarski-theorem/) (Adachi 2000).

## Tightness

- **Example with four elements.** Take two copies of the two-by-two market in which men and women rank each other in opposite ways: $m_1$: $w_1, w_2, \ldots$; $m_2$: $w_2, w_1, \ldots$; $w_1$: $m_2, m_1, \ldots$; $w_2$: $m_1, m_2, \ldots$, and the same for $m_3, m_4, w_3, w_4$, with partners of the other copy at the ends of all lists. Each copy can be matched in two stable ways, independently, so there are four stable matchings that form a diamond: $\{m_1 w_1, m_2 w_2, m_3 w_3, m_4 w_4\}$ at the top, $\{m_1 w_2, m_2 w_1, m_3 w_4, m_4 w_3\}$ at the bottom, and the two mixed ones in between. The join of the two mixed ones is the top.
- **Roommates.** In the [stable roommates problem](/stable-roommates-problem/) a stable matching may not exist, and the set of stable matchings has no lattice structure in general.
- **Ties.** With ties in the orders, the weakly stable matchings do not form a lattice and can differ in size; see [stable matching with ties](/stable-matching-with-ties/).
- **Many-to-one.** In the [hospitals-residents problem](/hospitals-residents-problem/) with ordinary orders over residents, the lattice theorem still holds, through the reduction that splits a hospital into one copy per seat. With couples it fails, since stable matchings may not exist at all.

## History

Knuth (1976) published the lattice theorem in his lectures on stable marriage and credited the join and meet construction to John Conway. Gale and Shapley (1962) had already shown that the proposing side gets its optimal stable matching. Irving and Leather (1986) introduced rotations and the rotation poset. Blair (1984) proved that every finite distributive lattice arises, and Gusfield, Irving, Leather and Saks (1987) gave small instances.

## References
