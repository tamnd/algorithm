---
tag: REBF14
kind: theorem
slug: stromquist-impossibility-theorem
name: Stromquist's impossibility theorem
aliases:
- no finite envy-free protocol with connected pieces
area: algorithmic-game-theory/fair-division
level: advanced
summary: "No finite protocol, bounded or not, can guarantee an envy-free division of a cake among three or more agents in which each agent gets one interval."
prereqs: [envy-freeness, robertson-webb-query-model, stromquist-moving-knife]
see_also: [selfridge-conway-procedure, brams-taylor-procedure, aziz-mackenzie-protocol, su-rental-harmony-algorithm, edmonds-pruhs-lower-bound, divide-and-choose, adversary-argument, cake-cutting-problem]
sources:
  - paper: doi:10.37236/735
    title: Walter Stromquist, Envy-free cake divisions cannot be found by finite protocols, Electronic Journal of Combinatorics 15 (2008)
    locator: R11; Section 2 (finite protocols), Section 4 (rigid measure systems and Lemmas 1 to 3), Section 5 (Theorem 1), Section 6 (more than three players)
  - paper: doi:10.1016/j.disopt.2006.07.003
    title: Gerhard J. Woeginger and Jiri Sgall, On the complexity of cake cutting, Discrete Optimization 4(2) (2007)
    locator: pp. 213-220 (the marking and value queries that define a finite protocol)
  - paper: doi:10.2307/2320951
    title: Walter Stromquist, How to cut a cake fairly, American Mathematical Monthly 87(8) (1980)
    locator: pp. 640-644 (envy-free divisions into intervals exist for every number of players)
  - paper: "Francis Edward Su, Rental harmony: Sperner's lemma in fair division, American Mathematical Monthly 106(10) (1999), 930-942"
    locator: Sections 3 to 5 (an existence proof with Sperner's lemma, and approximate divisions in finitely many steps)
---

Stromquist's impossibility theorem says that no finite protocol can always find an [envy-free](/envy-freeness/) division of a [cake](/cake-cutting-problem/) among three or more agents in which each agent gets one interval. Such divisions always exist, and the [Stromquist moving knife](/stromquist-moving-knife/) finds one for three agents, but only with knives that move continuously. The theorem holds in the [Robertson-Webb query model](/robertson-webb-query-model/) and for protocols whose number of steps is finite but has no bound. It is a statement about exact envy-freeness with connected pieces: the finite envy-free protocols, from the [Selfridge-Conway procedure](/selfridge-conway-procedure/) to the [Aziz-Mackenzie protocol](/aziz-mackenzie-protocol/), give some agents pieces made of several intervals. It differs from the [Edmonds-Pruhs lower bound](/edmonds-pruhs-lower-bound/), which counts the queries of a problem that finite protocols do solve; here no finite number of queries is enough.

## Statement

The cake is $[0, 1]$, and agent $i \in \{1, \dots, n\}$ has a nonatomic measure $v_i$ with $v_i([0, 1]) = 1$. A protocol works with marks on the cake. In each step it chooses an agent $i$ and a number $\alpha$, and agent $i$ marks its $\alpha$-point, the point $x$ with $v_i([0, x]) = \alpha$; then all agents reveal $v_j([0, x])$. This is a cut query, followed by eval queries at the new mark. The choices of the protocol may depend in any way on what has been revealed. When it stops, the protocol cuts the cake at $n - 1$ existing marks and gives the $n$ intervals to the agents. The agents answer honestly. A protocol is *finite* if it stops after finitely many steps for every system of measures, and *bounded* if some number $N$ of steps is always enough.

**Theorem (Stromquist 2008, Theorem 1).** Let $n \ge 3$. No finite protocol, bounded or not, ends with an envy-free division into $n$ intervals for every system of $n$ measures.

The theorem still holds if the protocol may also place marks that it computes from the revealed values, and if the protocol knows that the measures belong to the small family of rigid measure systems below. A randomized protocol does not help: to stop after finitely many steps with certainty, each of its runs must be a finite deterministic protocol.

## In plain words

Three friends want to cut a cake with two cuts, so that each gets one piece and nobody envies another. A fair split like this always exists. The question is whether a referee can find it by asking the friends a finite number of questions, such as "where would you cut to get a third of the cake?".

The answer is no. For some cakes, the two cuts must be at exactly the right places, and moving either one by any amount, however small, makes someone envious. The referee is like a person who must guess a secret real number and only learns, after each guess, whether it was too high or too low. Each answer leaves room for the cakes to be a little different from what the referee thinks, so the right cut points can always move out of reach.

## Proof

We follow Sections 4 and 5 of the paper for $n = 3$, with agents $A$, $B$ and $C$.

**Rigid measure systems.** Let $0 < x < y < 1$ and $0 < s < 1/3 < t < 1/2$ with $s + 2t = 1$. A rigid measure system with parameters $x, y, s, t$ is a set of three measures whose densities lie strictly between $\sqrt{2}/2$ and $\sqrt{2}$, so that $(\sqrt{2}/2)\ell < v_i(S) < \sqrt{2}\ell$ for each piece $S$ of length $\ell$, and whose values of the three pieces cut at $x$ and $y$ are:

| | $[0, x]$ | $[x, y]$ | $[y, 1]$ |
|---|---|---|---|
| $v_A$ | $t$ | $t$ | $s$ |
| $v_B$ | $s$ | $t$ | $t$ |
| $v_C$ | $t$ | $s$ | $t$ |

Such systems exist. Take $x = 1/3$, $y = 2/3$, $t = 9/25$ and $s = 7/25$, and give each agent a density that is constant on each third: $27/25$ on its two pieces of value $t$ and $21/25$ on its piece of value $s$. Both numbers lie between $\sqrt{2}/2 \approx 0.707$ and $\sqrt{2} \approx 1.414$.

**Lemma 1.** In a rigid measure system, if $v_i(S_1) \ge 2 v_i(S_2)$ for two pieces, then $2 v_j(S_1) > v_j(S_2)$ for every agent $j$.

*Proof.* Let $\ell_1$ and $\ell_2$ be the lengths of $S_1$ and $S_2$. Then $2 v_j(S_1) > \sqrt{2}\ell_1 > v_i(S_1) \ge 2 v_i(S_2) > \sqrt{2}\ell_2 > v_j(S_2)$. $\square$

**Lemma 2.** In a rigid measure system, every envy-free division into three intervals has its cuts at $x$ and $y$. There are two such divisions: $[0, x]$, $[x, y]$ and $[y, 1]$ go to $A$, $B$ and $C$, or to $C$, $A$ and $B$.

*Proof.* In both divisions each agent gets value $t$ and sees no piece worth more than $t$, so they are envy-free. Now cut at $\hat{x}$ and $\hat{y}$ instead. If $\hat{x} \le x$ and $\hat{y} \ge y$, with one inequality strict, the densities are positive, so $A$ and $B$ both value the middle piece above $t$ and every other piece at most $t$; both want it, and one of them envies. If $\hat{x} \ge x$ and $\hat{y} \le y$, with one inequality strict, every agent values the middle piece below $t$ and some other piece at least $t$, so nobody accepts the middle piece. By symmetry, the last case is $\hat{x} \ge x$ and $\hat{y} \ge y$, with one inequality strict. Then $A$ and $C$ prefer the left piece to the right one, so $B$ must take the right piece. Let $S_1 = [x, \hat{x}]$ and $S_2 = [y, \hat{y}]$. $B$ accepts the right piece only if $t - v_B(S_2) \ge t + v_B(S_2) - v_B(S_1)$, that is $v_B(S_1) \ge 2 v_B(S_2)$. By Lemma 1, $v_A(S_2) < 2 v_A(S_1)$, so $v_A([0, \hat{x}]) = t + v_A(S_1) > t - v_A(S_1) + v_A(S_2) = v_A([\hat{x}, \hat{y}])$. So $A$ prefers the left piece to the middle one, and $C$ does too, by a wider margin, since it values $[x, y]$ at $s < t$. Nobody accepts the middle piece. $\square$

So the protocol must place marks exactly at $x$ and $y$. The next lemma says that no agent can tell where they are.

**Lemma 3.** Let $\{v_A, v_B, v_C\}$ be a rigid measure system with parameters $x, y, s, t$, let $\eta > 0$, let $i$ be an agent, and let $\delta > 0$ with $1/3 + \delta < t < 1/2 - \delta$. Then there is a rigid measure system $\{\hat{v}_A, \hat{v}_B, \hat{v}_C\}$ with parameters $\hat{x} \ne x$, $\hat{y} \ne y$, $\hat{s}$ and $\hat{t}$, such that $\hat{v}_i = v_i$, every $\hat{v}_j$ agrees with $v_j$ on all intervals whose ends are farther than $\eta$ from $x$ and $y$, $|\hat{x} - x| < \eta$, $|\hat{y} - y| < \eta$ and $1/3 + \delta < \hat{t} < 1/2 - \delta$.

*Proof sketch, for $i = A$.* Choose $\hat{t} \ne t$ close to $t$, let $\hat{s} = 1 - 2\hat{t}$, and choose $\hat{x}$ and $\hat{y}$ with $v_A([0, \hat{x}]) = \hat{t}$ and $v_A([0, \hat{y}]) = 2\hat{t}$; they move continuously with $\hat{t}$, so they stay within $\eta$ of $x$ and $y$. Keep $\hat{v}_A = v_A$. Define $\hat{v}_B([0, u])$ and $\hat{v}_C([0, u])$ to equal the old values when $u$ is farther than $\eta$ from $x$ and $y$, set $\hat{v}_B([0, \hat{x}]) = \hat{s}$, $\hat{v}_B([0, \hat{y}]) = \hat{s} + \hat{t}$, $\hat{v}_C([0, \hat{x}]) = \hat{t}$ and $\hat{v}_C([0, \hat{y}]) = \hat{s} + \hat{t}$, and interpolate linearly on the four intervals between $x \pm \eta$, $\hat{x}$, $y \pm \eta$ and $\hat{y}$. The table holds by construction. The new densities on the four intervals depend continuously on $\hat{t}$, and at $\hat{t} = t$ they equal the old averages, which lie strictly inside $(\sqrt{2}/2, \sqrt{2})$. So all sixteen density bounds hold for $\hat{t}$ close enough to $t$. The cases $i = B$ and $i = C$ are similar. $\square$

**The theorem for three agents.** Suppose that a finite protocol always ends with an envy-free division into intervals, even when it knows that the measures form a rigid measure system. Start from any rigid measure system and fix $\delta$ as in Lemma 3. Run the protocol, with marks at $0$ and $1$ at the start. Before each step, let $\eta$ be less than the distance from $x$ and $y$ to every existing mark. If the new mark falls at $x$ or $y$, apply Lemma 3 to the agent that made it. The new system gives the same answers to all earlier questions and to this one, because the asked agent's measure did not change and all marks lie outside the changed neighbourhoods. So the protocol cannot tell the two systems apart, and in the new system no mark lies at $\hat{x}$ or $\hat{y}$. Repeat at every step, and choose the values of $\eta$ so that they tend to 0. Then each point of the cake is changed only finitely often, $\hat{t}$ stays between $1/3 + \delta$ and $1/2 - \delta$, and the measures converge to a rigid measure system in which the protocol never marks the two points where Lemma 2 says the cuts must be. The protocol gives the same answers on this limit system, so it never stops with an envy-free division. This contradicts finiteness. $\square$

**More agents.** Section 6 of the paper treats $n > 3$ in the same way. For $n = 5$, the parameters are $0 < x_1 < x_2 < x_3 < x_4 < 1$ and $0 < s < 1/5 < t < 1/2$ with $2t + 3s = 1$, and the value table of the five pieces is cyclic: agent 1 has $t, t, s, s, s$, agent 2 has $s, t, t, s, s$, and so on, with agent 5 having $t, s, s, s, t$. There are again exactly two envy-free divisions, both with cuts at $x_1, \dots, x_4$, and the rest of the proof is unchanged. The paper gives this case as a sketch.

## Consequences

- **Moving knives cannot be made finite.** The Stromquist moving knife and the simpler two-cut procedure of Barbanel and Brams need agents to watch continuous motion, and the theorem shows that no finite sequence of queries can replace it.
- **Finite envy-free protocols must break pieces.** For three or more agents, every finite envy-free protocol gives some agent a piece of two or more intervals for some valuations. The [Selfridge-Conway procedure](/selfridge-conway-procedure/) uses five cuts for three agents, and the [Brams-Taylor procedure](/brams-taylor-procedure/) and the Aziz-Mackenzie protocol work for any $n$ with pieces that are unions of intervals.
- **Proportional division is different.** Proportional divisions into intervals can be found with finitely many queries, by the [last diminisher](/last-diminisher/) or the [Even-Paz algorithm](/even-paz-algorithm/). The impossibility is about envy.
- **Approximation is finite.** For every $\varepsilon > 0$, a division into intervals in which no agent envies another by more than $\varepsilon$ can be found in finitely many steps, for example by the path-following method of Su (1999), which [Su's algorithm](/su-rental-harmony-algorithm/) applies to rent. The theorem says only that no finite protocol reaches $\varepsilon = 0$.
- **Existence is not computation.** Stromquist (1980) and Su (1999) prove that envy-free divisions into intervals exist for every $n$. Their proofs take limits, and the theorem shows that a limit cannot be avoided.

## Tightness

- **Two agents.** For $n = 2$, [divide and choose](/divide-and-choose/) is a finite protocol with one cut, so $n \ge 3$ is needed.
- **Connected pieces.** If pieces may be unions of intervals, finite envy-free protocols exist for every $n$, and the Aziz-Mackenzie protocol is even bounded.
- **Exactness.** The approximate problem has finite protocols, as above.
- **Rich families of measures.** The proof needs measures that can change near $x$ and $y$ without any change elsewhere. If the measures are known to have constant densities on $k$ known segments, then $nk$ eval queries reveal them all, and the cuts can be computed exactly, as the Stromquist moving knife page does for its simulation.

## History

Stromquist proved in 1980 that envy-free divisions into intervals exist for any number of agents, and gave a moving-knife procedure for three. At the Dagstuhl seminar on fair division in June 2007, Steven Brams asked whether a finite protocol could find such a division for three agents with two cuts. Stromquist answered the question in a paper submitted in October 2007 and published in the Electronic Journal of Combinatorics in January 2008. He took the notion of a finite protocol from the paper of Woeginger and Sgall, which builds on the query model of Robertson and Webb.

## References
