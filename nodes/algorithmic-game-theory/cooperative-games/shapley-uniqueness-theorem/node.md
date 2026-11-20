---
tag: 9D8KDM
kind: theorem
slug: shapley-uniqueness-theorem
name: Shapley's uniqueness theorem
aliases:
- Shapley axioms
area: algorithmic-game-theory/cooperative-games
level: core
summary: The Shapley value is the only solution of TU games that is efficient, symmetric, additive and gives null players zero.
prereqs: [shapley-value, mobius-inversion]
see_also: [shapley-shubik-index, banzhaf-index, marginal-contribution-nets, owen-multilinear-extension, shapley-convex-games-theorem, bondareva-shapley-theorem, transferable-utility-game]
sources:
  - paper: doi:10.1515/9781400881970-018
    title: "Lloyd S. Shapley, A value for n-person games, in H. W. Kuhn and A. W. Tucker (eds.), Contributions to the Theory of Games II, Annals of Mathematics Studies 28, Princeton University Press, 1953, 307-317"
    locator: the three axioms (symmetry, the carrier axiom and the law of aggregation) and the proof that they determine the value, by the games with one carrier
  - paper: doi:10.1007/BF01780630
    title: "Pradeep Dubey, On the uniqueness of the Shapley value, International Journal of Game Theory 4(3) (1975), 131-139"
    locator: the uniqueness of the value on the class of simple games, with the transfer axiom in place of additivity
  - paper: doi:10.1007/BF01769885
    title: "H. P. Young, Monotonic solutions of cooperative games, International Journal of Game Theory 14(2) (1985), 65-72"
    locator: the characterization by efficiency, symmetry and strong monotonicity, without additivity
  - paper: doi:10.1287/moor.4.2.99
    title: "Pradeep Dubey and Lloyd S. Shapley, Mathematical properties of the Banzhaf power index, Mathematics of Operations Research 4(2) (1979), 99-131"
    locator: the axioms of the Banzhaf index, compared with those of the Shapley value
  - book: isbn:9781107005488
    title: Michael Maschler, Eilon Solan and Shmuel Zamir, Game Theory, Cambridge University Press, 2013
    locator: Chapter 18, The Shapley value (Section 18.1 the properties, Section 18.3 the definition and the proof of uniqueness)
---

The uniqueness theorem says that four properties fix a solution of TU games completely: efficiency, symmetry, the null player property and additivity. Only the [Shapley value](/shapley-value/) has all four. This is the main reason why the Shapley value is used as a fair division rule: one does not need to accept the formula, only the four properties. The theorem is for the space of all TU games on a fixed finite set of players. On a smaller class, such as the simple games of the [Shapley-Shubik index](/shapley-shubik-index/), additivity is not available and other axioms take its place.

## Statement

Let $N = \{1, \ldots, n\}$ be a finite set of players, and let $\mathcal{G}_N$ be the set of all TU games on $N$: all functions $v$ from the subsets of $N$ to $\mathbb{R}$ with $v(\emptyset) = 0$. With pointwise addition and scaling, $\mathcal{G}_N$ is a real vector space. A *solution* is a map $\psi : \mathcal{G}_N \to \mathbb{R}^n$. Players $i$ and $j$ are *symmetric* in $v$ if $v(S \cup \{i\}) = v(S \cup \{j\})$ for every $S \subseteq N \setminus \{i, j\}$, and $i$ is a *null player* in $v$ if $v(S \cup \{i\}) = v(S)$ for every $S \subseteq N$. The axioms are:

1. **Efficiency.** $\sum_{i \in N} \psi_i(v) = v(N)$.
2. **Symmetry.** If $i$ and $j$ are symmetric in $v$, then $\psi_i(v) = \psi_j(v)$.
3. **Null player.** If $i$ is a null player in $v$, then $\psi_i(v) = 0$.
4. **Additivity.** $\psi(v + w) = \psi(v) + \psi(w)$ for all $v, w \in \mathcal{G}_N$.

**Theorem (Shapley 1953).** A solution on $\mathcal{G}_N$ satisfies axioms 1 to 4 if and only if it is the Shapley value
$$\varphi_i(v) = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(n-|S|-1)!}{n!} \big( v(S \cup \{i\}) - v(S) \big).$$

The theorem needs no homogeneity axiom and no continuity: additivity alone, on the whole space, is enough.

## In plain words

Suppose that a group must agree on a rule to split the money that any team of its members could earn. They ask for four things. All the money of the full group is paid out. Two members who add the same amount to every team get the same pay. A member who adds nothing to any team gets nothing. And if the money comes from two separate projects, the pay for both together is the pay for the first plus the pay for the second. The theorem says that these four wishes leave exactly one rule. That rule pays each member the average of what it adds when the members arrive in a random order.

## Proof

**Step 1: the Shapley value has the four properties.** For efficiency, use the order form $\varphi_i(v) = \frac{1}{n!} \sum_\pi \big(v(P_i^\pi \cup \{i\}) - v(P_i^\pi)\big)$, where $P_i^\pi$ is the set of the players before $i$ in the order $\pi$. In each order the marginal contributions telescope to $v(N) - v(\emptyset) = v(N)$, so the mean over the orders sums to $v(N)$ too. The null player property holds because each term of $\varphi_i$ is 0. Additivity holds because each term is linear in $v$.

For symmetry, let $i$ and $j$ be symmetric. Define a map $f$ from the subsets of $N \setminus \{i\}$ to the subsets of $N \setminus \{j\}$: $f(S) = S$ if $j \notin S$, and $f(S) = (S \setminus \{j\}) \cup \{i\}$ if $j \in S$. It is a bijection and keeps the size. If $j \notin S$, then $v(S \cup \{i\}) - v(S) = v(S \cup \{j\}) - v(S)$ by symmetry. If $S = T \cup \{j\}$ with $i, j \notin T$, the marginal contribution of $i$ to $S$ is $v(T \cup \{i, j\}) - v(T \cup \{j\})$, and that of $j$ to $f(S) = T \cup \{i\}$ is $v(T \cup \{i, j\}) - v(T \cup \{i\})$. These are equal, because $v(T \cup \{j\}) = v(T \cup \{i\})$. So the terms of $\varphi_i$ and $\varphi_j$ match one to one, with the same weights, and $\varphi_i(v) = \varphi_j(v)$.

**Step 2: the unanimity games are a basis.** For a nonempty $T \subseteq N$, let $u_T(S) = 1$ if $T \subseteq S$ and $u_T(S) = 0$ if not. For $v \in \mathcal{G}_N$ define $d_T = \sum_{S \subseteq T} (-1)^{|T| - |S|} v(S)$. By [Möbius inversion](/mobius-inversion/) on the subsets of $N$, $\sum_{T \subseteq S} d_T = v(S)$ for every $S$, and $d_\emptyset = v(\emptyset) = 0$. So
$$v = \sum_{\emptyset \ne T \subseteq N} d_T\, u_T.$$
The space $\mathcal{G}_N$ has dimension $2^n - 1$, one coordinate for each nonempty coalition, and the $2^n - 1$ games $u_T$ span it, so they are a basis and the coefficients $d_T$ are unique.

**Step 3: the axioms fix $\psi(c\, u_T)$ for every real $c$.** Let $\psi$ satisfy the axioms, let $T \ne \emptyset$ and let $c$ be any real number, positive, negative or zero. In the game $c\, u_T$, a player $k \notin T$ is a null player, because adding $k$ to a coalition does not change whether it contains $T$. So $\psi_k(c\, u_T) = 0$. Two players $i, j \in T$ are symmetric: for $S \subseteq N \setminus \{i, j\}$, neither $S \cup \{i\}$ nor $S \cup \{j\}$ contains $T$, so both have the value 0. So all players of $T$ get the same amount, and by efficiency these $|T|$ equal amounts sum to $c\, u_T(N) = c$. Hence
$$\psi_i(c\, u_T) = \frac{c}{|T|} \text{ for } i \in T, \qquad \psi_k(c\, u_T) = 0 \text{ for } k \notin T.$$

**Step 4: uniqueness.** Let $v \in \mathcal{G}_N$. By step 2, $v$ is the sum of the finitely many games $d_T\, u_T$. Additivity, applied $2^n - 2$ times, gives $\psi(v) = \sum_T \psi(d_T\, u_T)$, and by step 3 every term is fixed. So $\psi(v)$ does not depend on the choice of $\psi$. The Shapley value satisfies the axioms by step 1, so $\psi = \varphi$. $\blacksquare$

The proof also gives the dividend formula $\varphi_i(v) = \sum_{T \ni i} d_T / |T|$.

## Consequences

- **The value is linear.** Additivity and the formula give $\varphi(c\, v) = c\, \varphi(v)$ for every real $c$, so $\varphi$ is a linear map from $\mathcal{G}_N$ to $\mathbb{R}^n$. Homogeneity is a consequence, not an axiom.
- **Computation by decomposition.** If a game is written as a sum of simple pieces whose values are known, the value of the game is the sum of their values. This is how [marginal contribution nets](/marginal-contribution-nets/) give the Shapley value in time linear in the size of the net: each rule is a small game with a closed-form value.
- **Other characterizations.** Young (1985) replaced additivity and the null player axiom by *strong monotonicity*: if $v(S \cup \{i\}) - v(S) \ge w(S \cup \{i\}) - w(S)$ for every $S$, then $\psi_i(v) \ge \psi_i(w)$. With efficiency and symmetry this again gives only the Shapley value, so additivity is not the only route.
- **Simple games.** The sum of two simple games is not simple, so on simple games axiom 4 says nothing. Dubey (1975) showed that the Shapley-Shubik index is the only solution on simple games with efficiency, symmetry, the null player property and the *transfer axiom* $\psi(v \vee w) + \psi(v \wedge w) = \psi(v) + \psi(w)$, where $v \vee w$ wins when $v$ or $w$ wins and $v \wedge w$ wins when both win.
- **The Banzhaf index.** Dubey and Shapley (1979) characterized the [Banzhaf index](/banzhaf-index/) by keeping symmetry, the null player property and the transfer axiom, and replacing efficiency by the condition that the total power is the number of swings divided by $2^{n-1}$. On all TU games, the Banzhaf value is symmetric, additive and gives null players 0, so by the uniqueness theorem it cannot be efficient.

## Tightness

Each axiom is needed: for each one, a solution exists that has the other three and is not the Shapley value.

- **Without efficiency:** $\psi = 2\varphi$ is symmetric, additive and gives null players 0. It pays out $2v(N)$.
- **Without symmetry:** a *weighted Shapley value* with fixed weights $\lambda_1, \ldots, \lambda_n > 0$ sets $\psi_i(v) = \sum_{T \ni i} d_T\, \lambda_i / \lambda(T)$, where $\lambda(T) = \sum_{k \in T} \lambda_k$. It is efficient, since the shares of each dividend sum to $d_T$, and additive, since it is linear in the dividends. It gives null players 0, because every dividend $d_T$ with $i \in T$ is 0 when $i$ is a null player: in the sum for $d_T$, the terms for $S$ and $S \cup \{i\}$ cancel. For $n = 2$, $\lambda = (1, 2)$ and $v = u_{\{1,2\}}$, it gives $(1/3, 2/3)$ to two symmetric players.
- **Without the null player axiom:** the equal split $\psi_i(v) = v(N)/n$ is efficient, symmetric and additive. It pays a null player.
- **Without additivity:** let $\psi$ split $v(N)$ equally among the players that are not null, and give 0 to the null players (if all players are null, $v(N) = 0$ by efficiency of the order form, and $\psi = 0$). This is efficient and gives null players 0. It is symmetric, because two symmetric players are both null or both not null: if $i$ is null and symmetric to $j$, then for $S \not\ni i, j$ we get $v(S \cup \{j\}) - v(S) = v(S \cup \{i\}) - v(S) = 0$, and for $S = T \cup \{i\}$ we get $v(T \cup \{i, j\}) - v(T \cup \{i\}) = v(T \cup \{j\}) - v(T) = 0$, so $j$ is null too. It is not additive: for $n = 2$, $\psi(u_{\{1,2\}}) = (1/2, 1/2)$ and $\psi(u_{\{1\}}) = (1, 0)$, but in the sum $v = u_{\{1,2\}} + u_{\{1\}}$ neither player is null, so $\psi(v) = (1, 1) \ne (3/2, 1/2)$.

**The domain matters.** Step 3 uses the games $c\, u_T$ with negative $c$, and step 4 uses sums of them. On a class of games that is not closed under these operations, the theorem does not follow from this proof. Simple games are the main example, and Dubey's transfer axiom is the fix there.

## History

Shapley introduced the value in 1953, in a chapter of the second volume of Contributions to the Theory of Games. His axioms are stated for games on a large universe of players with a finite *carrier*, a set outside which all players are null. They are symmetry under permutations of the players, a carrier axiom that combines efficiency with the null player property, and the law of aggregation, which is additivity. The proof by the games with one carrier coalition is the one in step 3. Shapley and Shubik (1954) applied the value to voting bodies. Dubey (1975) gave the uniqueness proof for simple games, Dubey and Shapley (1979) studied the Banzhaf index by axioms, and Young (1985) gave the characterization by strong monotonicity. Textbooks such as Maschler, Solan and Zamir (2013) use the four axioms of the statement above.

## References
