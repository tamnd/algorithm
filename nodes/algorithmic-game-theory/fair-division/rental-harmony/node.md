---
tag: WHKF6S
kind: problem
slug: rental-harmony
name: Rental harmony
aliases:
- rent division problem
area: algorithmic-game-theory/fair-division
level: core
summary: Assign rooms to housemates and split a fixed rent so that every housemate prefers its room at its price to any other room at that room's price.
model: real-ram
complexity:
  vars: {n: the number of rooms and tenants}
  time: {worst: O(n^3)}
see_also: [su-rental-harmony-algorithm, envy-freeness, sperner-lemma, assignment-problem, hungarian-algorithm, competitive-equilibrium, chore-division, cake-cutting-problem]
sources:
  - paper: "Francis Edward Su, Rental harmony: Sperner's lemma in fair division, American Mathematical Monthly 106(10) (1999), 930-942"
    locator: Section 6, Chores and Rent-partitioning (the Rental Harmony Theorem and its three conditions), Section 7 (its proof with a dual Sperner lemma) and Section 8 (the weaker miserly condition)
  - paper: "Harold W. Kuhn, The Hungarian method for the assignment problem, Naval Research Logistics Quarterly 2 (1955), 83-97"
    locator: the algorithm for a maximum-weight assignment, with its dual variables
  - book: isbn:9780521556446
    title: Steven J. Brams and Alan D. Taylor, Fair Division, From Cake-Cutting to Dispute Resolution, Cambridge University Press, 1996
    locator: envy-free division of goods and of burdens, as background for rent division
---

Rental harmony asks how $n$ housemates should share a house with $n$ rooms and a fixed total rent: each housemate gets one room and a price, the prices add up to the rent, and no housemate prefers another room at that room's price to its own room at its own price. This page is the problem: its two models, the existence theorem and the known bounds. [Su's algorithm](/su-rental-harmony-algorithm/) is one procedure for it, which finds an approximate solution in the model where tenants only answer which room they would choose. In the model where each tenant has a money value for each room, the problem is solved exactly by a maximum-weight [assignment](/assignment-problem/) and its dual prices. Rental harmony mixes an indivisible good (the rooms) with a divisible one (the rent), so it differs from [cake cutting](/cake-cutting-problem/), where everything is divisible, and from [chore division](/chore-division/), where every part is a burden.

## In plain words

Some friends rent a house together, and its rooms differ. The friends must decide who gets which room and how much each pays, and the total must be the rent of the house.

A good split leaves nobody jealous. Each friend looks at its own room and its own price, then at every other room and its price, and finds its own deal at least as good. This can hold even when the friends disagree about the rooms, because a room that more friends want can cost more.

Such a split always exists under mild conditions. Finding it depends on what the friends can tell. If each friend can name a money value for each room, a fast method finds an exact split. If a friend can only say which room it would take at given prices, a split can be found only approximately.

## Definition

There are $n$ tenants, $n$ rooms and a total rent $R > 0$. A price vector is $p = (p_1, \dots, p_n)$ with $\sum_j p_j = R$.

- **Output.** A bijection $\sigma$ from tenants to rooms and a price vector $p$.
- **Condition.** The pair $(\sigma, p)$ is *envy-free*: for each tenant $i$ and each room $j$, tenant $i$ likes room $\sigma(i)$ at price $p_{\sigma(i)}$ at least as much as room $j$ at price $p_j$.

The input and the measure depend on the model.

- **The ordinal model (Su).** Prices must be nonnegative. At each price vector, each tenant tells which rooms it would choose. Su's conditions are: (1) at every price vector, each tenant finds some room acceptable; (2) tenants are *miserly*, so a tenant prefers a free room to a room that costs something; (3) the preference sets are closed, so a room that a tenant chooses along a sequence of price vectors is also chosen at the limit. The measure is the number of questions, and the goal is an approximate solution: an envy-free pair at prices within $\delta$ of $p$.
- **The quasi-linear model.** Tenant $i$ has a value $v_{ij}$ for room $j$, and its utility for room $j$ at price $p_j$ is $v_{ij} - p_j$. The input is the $n \times n$ matrix of values, and the measure is the running time. Prices may be negative.

## Variants

- **Nonnegative prices.** In the quasi-linear model, an envy-free solution with all prices nonnegative need not exist; see the second example.
- **The weaker miserly condition.** Su notes that condition (2) can be weakened: it is enough that no tenant chooses the most expensive room when some room is free.
- **Choosing among envy-free solutions.** There are often many envy-free price vectors. In the quasi-linear model, for a fixed assignment the envy-free price vectors form a polytope, so one can choose a best one, for example the one that maximizes the smallest utility, with one linear program.
- **Rebates.** Su also discusses rent as a burden to split, and a version in which some rooms may get a negative price, so that a tenant is paid to take them.

## Examples

**Three tenants with values.** The rent is $R = 900$. Tenants $a$, $b$ and $c$ have these values for rooms 1, 2 and 3.

| | room 1 | room 2 | room 3 |
|---|---|---|---|
| $a$ | 400 | 300 | 200 |
| $b$ | 300 | 400 | 200 |
| $c$ | 300 | 300 | 350 |

Give room 1 to $a$, room 2 to $b$ and room 3 to $c$, at prices $(300, 300, 300)$. Tenant $a$ has utility $100$ for room 1 and $0$ and $-100$ for the others; tenant $b$ is the mirror case; tenant $c$ has utility $50$ for room 3 and $0$ for each other room. Nobody envies. At prices $(280, 280, 340)$, tenant $c$ has utility $10$ for room 3 but $20$ for room 1, so it envies $a$: making the room that $c$ likes cost more than $50$ above the others breaks the split.

**No nonnegative solution.** The rent is $R = 10$. Two tenants both value room 1 at $100$ and room 2 at $0$. One of them gets room 2, and it must not envy the other, so $0 - p_2 \ge 100 - p_1$; the other gives the reverse inequality, so $p_1 - p_2 = 100$. With $p_1 + p_2 = 10$ this gives $p_1 = 55$ and $p_2 = -45$. These tenants are not miserly: each prefers room 1 at price $10$ to room 2 for free, which is why Su's theorem does not apply.

## Known algorithms

| method | model | result |
|---|---|---|
| [Su's algorithm](/su-rental-harmony-algorithm/) | ordinal, miserly tenants | approximate; prices within $R/N$ for a grid of size $N$ |
| maximum-weight assignment with dual prices ([Hungarian algorithm](/hungarian-algorithm/)) | quasi-linear | exact, $O(n^3)$ time |
| one linear program on top of the assignment | quasi-linear | an envy-free solution that is best by a linear criterion |

The quasi-linear method rests on two facts that this page proves below.

**Theorem 1.** If $(\sigma, p)$ is envy-free in the quasi-linear model, then $\sigma$ is a maximum-weight assignment, that is, it maximizes $\sum_i v_{i \sigma(i)}$.

*Proof.* Let $\tau$ be any bijection. Envy-freeness gives $v_{i \sigma(i)} - p_{\sigma(i)} \ge v_{i \tau(i)} - p_{\tau(i)}$ for each $i$. Summing over $i$, both sums of prices equal $R$, so $\sum_i v_{i \sigma(i)} \ge \sum_i v_{i \tau(i)}$. $\square$

**Theorem 2.** For every maximum-weight assignment $\sigma$ there is a price vector $p$ that makes $(\sigma, p)$ envy-free.

*Proof.* By duality for the [assignment linear program](/linear-programming-problem/), there are numbers $u_i$ and $q_j$ with $u_i + q_j \ge v_{ij}$ for all $i, j$, and $u_i + q_{\sigma(i)} = v_{i \sigma(i)}$ for all $i$. So $v_{ij} - q_j \le u_i = v_{i \sigma(i)} - q_{\sigma(i)}$, and the prices $q$ are envy-free. Adding the same constant $c$ to every $q_j$ keeps every comparison, so choose $c$ with $\sum_j (q_j + c) = R$. $\square$

The Hungarian algorithm computes $\sigma$ and the dual numbers $q$ in $O(n^3)$ time.

## Bounds

- **Existence, ordinal model.** Under conditions (1) to (3), an envy-free division with nonnegative prices exists (Su 1999, the Rental Harmony Theorem, stated in Section 6 and proved in Section 7). The proof uses a dual form of [Sperner's lemma](/sperner-lemma/) on the simplex of price vectors. This is a theorem.
- **Existence, quasi-linear model.** An envy-free solution always exists, with prices that may be negative, by Theorem 2.
- **Quasi-linear, upper bound.** $O(n^3)$ time with the Hungarian algorithm, in the [real-RAM](/real-ram/) model. Reading the input takes $\Omega(n^2)$ time.
- **Ordinal, upper bound.** Su's algorithm asks at most one question per point of a grid of size $N$, so at most $\binom{N + n - 1}{n - 1}$ questions, and its price error is at most $R/N$ per room.
- **Ordinal, exact solutions.** In the ordinal model an exact solution is in general a limit of approximate ones, as in Su's proof, which uses condition (3).

## Reductions

- **To Sperner's lemma.** Su gives each point of a triangulated price simplex an owner and labels it with the room the owner chooses. A fully labeled cell of the dual Sperner lemma gives an approximately envy-free division.
- **To an assignment market.** In the quasi-linear model, an envy-free pair $(\sigma, p)$ is a [competitive equilibrium](/competitive-equilibrium/) of a market with $n$ unit-demand buyers and $n$ items, in which every buyer gets an item it likes best at the prices and the prices add up to $R$. Theorems 1 and 2 are the welfare theorems of this market.
- **To chore division.** The rent is a burden that the tenants share, so methods for [chore division](/chore-division/) with labels from Sperner's lemma apply, as Su notes.

## Applications

- Shared houses and apartments, where the rooms differ in size and features.
- Shared offices or desks with a fixed total cost.
- Any split of a fixed cost among people who each get one different item, such as cabins on a shared trip.

## References
