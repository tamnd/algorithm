---
tag: FHMPD5
kind: theorem
slug: border-theorem
name: "Border's theorem"
aliases:
- interim feasibility characterization
area: algorithmic-game-theory/mechanism-design
level: advanced
summary: An interim allocation rule of a single-item auction with independent types comes from some real allocation if and only if it passes one linear inequality per family of type sets.
prereqs: [bayesian-incentive-compatibility, max-flow-min-cut-theorem]
see_also: [myerson-optimal-auction, automated-mechanism-design, hall-theorem, linear-programming-problem, ellipsoid-method, simple-versus-optimal-multi-item, single-parameter-environment, revenue-equivalence-theorem]
sources:
  - paper: doi:10.2307/2938181
    title: "Kim C. Border, Implementation of reduced form auctions: a geometric approach, Econometrica 59(4) (1991), from p. 1175"
    locator: the characterization of feasible symmetric reduced form auctions by linear inequalities
  - paper: doi:10.1007/s00199-006-0080-z
    title: "Kim C. Border, Reduced form auctions revisited, Economic Theory 31(1) (2007), 167-181"
    locator: the inequalities for bidders with different type distributions
  - paper: doi:10.3982/ECTA11405
    title: "Yeon-Koo Che, Jinwoo Kim and Konrad Mierendorff, Generalized reduced-form auctions: a network-flow approach, Econometrica 81(6) (2013), 2487-2520"
    locator: the proof by the max-flow min-cut theorem and its extension to other allocation constraints
  - paper: doi:10.1145/2213977.2214021
    title: "Yang Cai, Constantinos Daskalakis and S. Matthew Weinberg, An algorithmic characterization of multi-dimensional mechanisms, STOC 2012, 459-478 (full version arXiv:1112.4572)"
    locator: the polynomial-time separation oracle for feasible reduced forms, the threshold sets after shading (Section 4.1 of the arXiv version) and the example that thresholds on the raw interim rule are not enough for asymmetric bidders (Appendix C)
---

Border's theorem says which interim allocation rules of a single-item auction can be realized. An interim rule gives, for each bidder and each of its types, the probability that the bidder wins, averaged over the other bidders' types; Border's theorem says that such a rule comes from an actual allocation of the item if and only if it passes one linear inequality for each choice of type sets. With [Bayesian incentive compatibility](/bayesian-incentive-compatibility/), the incentives depend only on the interim rule, so the theorem turns the design of an optimal auction into a linear program over a small number of interim variables. The theorem is a statement about feasibility, not about incentives; it applies to any interim rule, truthful or not.

## Statement

There are $n$ bidders and one item. Bidder $i$ has a type $t_i$ in a finite set $T_i$, drawn from $f_i$, independently across bidders, with $f_i(t) > 0$ for every type. Write $f_i(S) = \sum_{t \in S} f_i(t)$ for $S \subseteq T_i$ and $\pi(t) = \prod_i f_i(t_i)$. An ex post allocation rule gives numbers $x_i(t) \ge 0$ with $\sum_i x_i(t) \le 1$ for every profile $t$; $x_i(t)$ is the probability that bidder $i$ gets the item. Its interim rule is

$$q_i(\tau) = \mathbb{E}_{t_{-i}}\big[x_i(\tau, t_{-i})\big] \qquad \text{for } \tau \in T_i.$$

An interim rule $q = (q_1, \ldots, q_n)$ with $q_i : T_i \to [0, 1]$ is feasible if some ex post rule has it as its interim rule.

**Theorem.** The interim rule $q$ is feasible if and only if, for every choice of subsets $S_1 \subseteq T_1, \ldots, S_n \subseteq T_n$,

$$\sum_{i=1}^{n} \sum_{\tau \in S_i} f_i(\tau)\, q_i(\tau) \ \le\ 1 - \prod_{i=1}^{n} \big(1 - f_i(S_i)\big).$$

The left side is the probability that the item goes to a bidder $i$ whose type is in $S_i$. The right side is the probability that at least one bidder $i$ has a type in $S_i$. Necessity is therefore clear; the content of the theorem is that these inequalities are also sufficient. Moreover, it is enough to check the families in which each $S_i$ is an upper set of $q_i$, that is $S_i = \{\tau : q_i(\tau) \ge c_i\}$ for some threshold $c_i$, which leaves at most $\prod_i (|T_i| + 1)$ inequalities.

Border (1991) proved the symmetric case, where all bidders have the same $f$ and the same $q$; then the sets can be taken equal and the condition reads $n \sum_{\tau \in S} f(\tau) q(\tau) \le 1 - (1 - f(S))^n$. The form for different distributions is in Border (2007), and the proof below by network flow is the one of Che, Kim and Mierendorff (2013).

### Example

Two bidders have types L and H with probability $1/2$ each. The rule "the higher type wins, ties are split evenly" gives $q(H) = \frac{1}{2} \cdot 1 + \frac{1}{2} \cdot \frac{1}{2} = \frac{3}{4}$ and $q(L) = \frac{1}{2} \cdot 0 + \frac{1}{2} \cdot \frac{1}{2} = \frac{1}{4}$ for each bidder.

| $S_1$ | $S_2$ | left side | right side |
|---|---|---|---|
| {H} | {H} | $\frac{1}{2} \cdot \frac{3}{4} + \frac{1}{2} \cdot \frac{3}{4} = \frac{3}{4}$ | $1 - \frac{1}{2} \cdot \frac{1}{2} = \frac{3}{4}$ |
| {H} | {} | $\frac{3}{8}$ | $\frac{1}{2}$ |
| {H, L} | {H, L} | $1$ | $1$ |
| {H, L} | {H} | $\frac{1}{2} + \frac{3}{8} = \frac{7}{8}$ | $1$ |

The inequality for $S_1 = S_2 = \{H\}$ is tight: whenever some bidder is H, an H bidder must win. Now try $q(H) = 1$ for both bidders, a rule under which a high type always wins. For $S_1 = S_2 = \{H\}$ the left side is $\frac{1}{2} + \frac{1}{2} = 1$ and the right side is $\frac{3}{4}$, so this interim rule is not feasible: when both are H, only one of them can win.

## In plain words

Suppose someone promises each bidder: "if your type is this, you win with that chance on average". Can a single item really be handed out so that all these promises hold at once? For any group of types, the chance that the item goes to someone in the group cannot exceed the chance that someone in the group shows up at all. Border's theorem says that this obvious test, done for every group, is also enough. If no group fails it, a real way to hand out the item exists. The test turns a hard question about whole allocation tables into a list of simple inequalities about averages.

## Proof

Necessity. Fix sets $S_i$ and an ex post rule $x$ with interim rule $q$. Then

$$\sum_i \sum_{\tau \in S_i} f_i(\tau) q_i(\tau) = \sum_t \pi(t) \sum_{i : t_i \in S_i} x_i(t) \ \le\ \sum_{t : \exists i,\ t_i \in S_i} \pi(t) = 1 - \prod_i (1 - f_i(S_i)),$$

because $\sum_i x_i(t) \le 1$ at every profile and the inner sum is empty when no $t_i$ is in $S_i$.

Sufficiency, by flows. Build a network with a source, a sink, a node for each profile $t \in T_1 \times \cdots \times T_n$ and a node for each pair $(i, \tau)$ with $\tau \in T_i$. The arcs are:

- from the source to profile $t$, with capacity $\pi(t)$;
- from profile $t$ to $(i, t_i)$ for each $i$, with infinite capacity;
- from $(i, \tau)$ to the sink, with capacity $f_i(\tau)\, q_i(\tau)$.

Let $D = \sum_i \sum_\tau f_i(\tau) q_i(\tau)$, the total capacity into the sink. A flow of value $D$ gives an ex post rule: set $x_i(t) = g(t, (i, t_i)) / \pi(t)$, where $g$ is the flow on the arc. Then $\sum_i x_i(t) \le 1$ by the capacity of the source arc, and $\sum_{t : t_i = \tau} \pi(t)\, x_i(t)$ is the flow into $(i, \tau)$, which is $f_i(\tau) q_i(\tau)$ because the sink arcs are saturated. Dividing by $f_i(\tau)$ gives the interim rule $q_i(\tau)$, by independence. So $q$ is feasible if the maximum flow is $D$.

By the [max-flow min-cut theorem](/max-flow-min-cut-theorem/), the maximum flow is $D$ if every cut has capacity at least $D$. Take a cut, given by the set $A$ of nodes on the source side, with finite capacity. Let $A_i = \{\tau : (i, \tau) \in A\}$ and $S_i = T_i \setminus A_i$. A profile $t$ in $A$ must have all $(i, t_i)$ in $A$, or an infinite arc would cross the cut. The capacity is smallest when $A$ holds exactly the profiles with $t_i \in A_i$ for all $i$, and then it is

$$\sum_{t \notin A} \pi(t) + \sum_i \sum_{\tau \in A_i} f_i(\tau) q_i(\tau) = \Big(1 - \prod_i f_i(A_i)\Big) + D - \sum_i \sum_{\tau \in S_i} f_i(\tau) q_i(\tau).$$

Since $f_i(A_i) = 1 - f_i(S_i)$, this is at least $D$ exactly when Border's inequality holds for $(S_1, \ldots, S_n)$. So if all the inequalities hold, every cut has capacity at least $D$, the maximum flow is $D$, and $q$ is feasible.

Upper sets suffice. Let $\phi(S) = \sum_i \sum_{\tau \in S_i} f_i(\tau) q_i(\tau) - 1 + \prod_i (1 - f_i(S_i))$, the amount by which an inequality fails. Fix all sets but $S_i$, and let $C_i = \prod_{j \ne i} (1 - f_j(S_j))$. Adding a type $\tau$ to $S_i$ changes $\phi$ by $f_i(\tau)(q_i(\tau) - C_i)$, independently of the other types in $S_i$. So replacing $S_i$ by $\{\tau : q_i(\tau) > C_i\}$ never lowers $\phi$. Starting from a violated family, do this for each bidder in turn: the family stays violated, and in the end each $S_i$ is an upper set of $q_i$. $\blacksquare$

## Consequences

- **Optimal auctions as small LPs.** By the [revelation principle](/revelation-principle/) and the payment identity, the revenue and the BIC and interim IR constraints of a single-item auction are linear in the interim rule $q$ and the interim payments. Border's inequalities describe the feasible $q$ exactly, so the optimal BIC auction is a linear program with $\sum_i |T_i|$ allocation variables, instead of one variable per bidder and profile. Its solution gives [Myerson's optimal auction](/myerson-optimal-auction/) for independent bidders.
- **Polynomial time despite many inequalities.** There are exponentially many families of sets, but Cai, Daskalakis and Weinberg (2012), and independently Alaei and others, give a polynomial-time separation oracle, so the LP can be solved by the [ellipsoid method](/ellipsoid-method/). This is the basis of their reduction from multi-item revenue maximization to welfare maximization. They also show that one common threshold for all bidders works after a "shading" of the interim rule, while a common threshold on $q$ itself is not enough when the bidders are asymmetric.
- **Implementation.** The flow proof is constructive: a maximum flow gives an ex post rule. Cai, Daskalakis and Weinberg also show that every feasible interim rule is a mixture of hierarchical rules, which rank all (bidder, type) pairs by a fixed priority and give the item to the highest pair present.
- **Link with Hall's theorem.** For a $0/1$ version with unit capacities, the cut condition reduces to the condition of [Hall's theorem](/hall-theorem/). Border's theorem is a fractional, weighted form of the same statement.

## Tightness

- **Independence.** The flow proof uses independence only to write the probability that some $t_i$ is in $S_i$ as $1 - \prod_i (1 - f_i(S_i))$. For a correlated prior, with $q_i(\tau)$ the conditional expectation given $t_i = \tau$ and $f_i$ the marginal, the same proof gives the condition with that probability as the right side. The reduction to upper sets uses the product form and does not carry over.
- **Upper sets.** Checking only upper sets of each $q_i$ is enough, but checking only sets with one common threshold on the raw values of $q$ is not, for asymmetric bidders; Cai, Daskalakis and Weinberg give an example.
- **Beyond one item.** For one item, and for some richer constraints such as several identical items, the flow proof gives a description of the same kind. For public projects, Gopalan, Nisan and Roughgarden showed that a Border-type characterization with efficiently checkable inequalities is unlikely to exist, under a standard complexity assumption.

## History

Maskin and Riley, and Matthews, worked with reduced form auctions in 1984, and Matthews conjectured the inequalities for the symmetric case. Border proved them in 1991 by a geometric argument and extended them to asymmetric bidders in 2007. Che, Kim and Mierendorff gave the network-flow proof in 2013 and used it for other allocation constraints. In computer science, Cai, Daskalakis and Weinberg, and Alaei, Fu, Haghpanah, Hartline and Malekian, turned the theorem into polynomial-time algorithms in 2012, which led to efficient optimal mechanisms for several items.

## References
