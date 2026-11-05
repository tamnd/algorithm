---
title: The Aldous-Broder algorithm returns each spanning tree with probability proportional to the product of its weights
proves: [correctness, termination]
status: full
---

**Claim.** Let $G = (V, E)$ be a finite connected undirected multigraph with $n \ge 1$ vertices and a weight $c_e > 0$ on each edge; parallel edges and self-loops are allowed. For each start vertex $r$, ALDOUS-BRODER stops with probability 1, and its output $T$ satisfies

$$\Pr[T = t] = \frac{c(t)}{Z}, \qquad c(t) = \prod_{e \in t} c_e, \qquad Z = \sum_{t'} c(t'),$$

for each spanning tree $t$, the sum over all spanning trees $t'$. With all weights 1, $\Pr[T = t] = 1 / \tau(G)$.

## Setup

For a vertex $x$, let $c(x)$ be the sum of $c_e$ over the edges at $x$, with a self-loop counted twice, as in the implementation. The walk at $x$ takes an edge $e$ at $x$ with probability $c_e / c(x)$ (a self-loop with probability $2 c_e / c(x)$) and moves to its other end. Write $p(x, y)$ for the probability to move from $x$ to $y$, so $p(x, y) = c(x, y) / c(x)$ for $y \ne x$, where $c(x, y)$ is the total weight of the edges between $x$ and $y$.

The walk is *reversible* with respect to $\pi(x) = c(x) / \sum_y c(y)$: for $x \ne y$, $\pi(x) p(x, y) = \pi(y) p(y, x)$, since both sides equal $c(x, y) / \sum_z c(z)$. So $\pi$ is a stationary distribution, and a walk started from $\pi$ looks the same forward and backward in time: for each $k$, the sequences $(X_0, \dots, X_k)$ and $(X_k, \dots, X_0)$ have the same law.

**Termination.** From each vertex, a fixed path of at most $n - 1$ steps reaches any other vertex with probability at least $\delta > 0$. So in each block of $n(n-1)$ steps, the walk visits all vertices with probability at least $\delta^n$, independent of the past, and the probability that the walk has not covered the graph after $j$ blocks is at most $(1 - \delta^n)^j \to 0$. Since the visited set never shrinks and each new vertex adds one edge that joins it to the visited set, the output is a tree on all $n$ vertices.

## Step 1: vertex trees first

We first ignore which of several parallel edges is used, and work with *rooted vertex trees*: a pair $(t, \rho)$ where $t$ assigns to each vertex $x \ne \rho$ a neighbor $t(x) \ne x$, its parent, such that following parents from any vertex reaches $\rho$. Define its weight

$$w(t, \rho) = \prod_{x \ne \rho} p(x, t(x)).$$

Since $p(x, y) = c(x, y) / c(x)$,

$$w(t, \rho) = \frac{c(\rho)}{\prod_{x \in V} c(x)} \prod_{x \ne \rho} c(x, t(x)). \tag{1}$$

## Step 2: a chain on rooted trees

Define a Markov chain $Q$ on rooted vertex trees. From $(t, \rho)$, take one step of the walk from $\rho$ to $u$.

- If $u = \rho$ (a self-loop), stay at $(t, \rho)$.
- Otherwise, move to $(t', u)$, where $t'(\rho) = u$, $t'(x) = t(x)$ for $x \notin \{\rho, u\}$, and $u$ has no parent.

$(t', u)$ is a rooted tree: in $t$, the path from $u$ to $\rho$ ends at $\rho$; after the change, every vertex whose path in $t$ passed through $u$ now stops at $u$, and every other vertex reaches $\rho$ and then $u$.

**Lemma 1.** The weight $w$ is stationary for $Q$: for each rooted tree $(t', u)$, $\sum_{(t, \rho)} w(t, \rho) Q((t, \rho), (t', u)) = w(t', u)$.

*Proof.* The term for the self-loop step is $w(t', u) p(u, u)$. The other predecessors of $(t', u)$ are the trees $(t, \rho)$ that the rule maps to $(t', u)$ with $\rho \ne u$. For such a tree, $t'(\rho) = u$, so $\rho$ is a child of $u$ in $t'$. Removing the edge from $\rho$ to $u$ from $t'$ splits it into the subtree $S_\rho$ of $\rho$ and the rest, which holds $u$. The tree $t$ agrees with $t'$ except that $\rho$ has no parent and $u$ has a parent $x = t(u)$. For $t$ to be a tree rooted at $\rho$, the path from $x$ must reach $\rho$ without passing through $u$, which holds exactly when $x \in S_\rho$. So the predecessors with $\rho \ne u$ are the pairs ($\rho$ a child of $u$ in $t'$, $x \in S_\rho$ a neighbor of $u$), and for each,

$$w(t, \rho) \, p(\rho, u) = \frac{w(t', u)}{p(\rho, u)} \, p(u, x) \, p(\rho, u) = w(t', u) \, p(u, x).$$

The subtrees $S_\rho$ of the children of $u$ partition $V \setminus \{u\}$, so the sum over all predecessors is

$$w(t', u) \Big( p(u, u) + \sum_{x \ne u} p(u, x) \Big) = w(t', u). \qquad \square$$

**Lemma 2.** The marginal of $w$ on roots is proportional to $\pi$: $\sum_{t} w(t, \rho) = \pi(\rho) \cdot K$ for a constant $K > 0$ that does not depend on $\rho$.

*Proof.* By (1), $\sum_t w(t, \rho) = \frac{c(\rho)}{\prod_x c(x)} \sum_t \prod_{x \ne \rho} c(x, t(x))$. A rooted vertex tree is an unrooted spanning tree of the simple graph underlying $G$ with an orientation toward $\rho$, and each unrooted tree has exactly one such orientation; so the last sum is $\sum_s \prod_{xy \in s} c(x, y)$ over unrooted vertex trees $s$, which does not depend on $\rho$. $\square$

## Step 3: last exits in the past

Let $W = \sum_{(t, \rho)} w(t, \rho)$ and let $\mu = w / W$, a probability distribution. Fix $N \ge 1$. Draw $(t_{-N}, X_{-N})$ from $\mu$, and run $Q$ for $N$ steps, which runs the walk $X_{-N}, \dots, X_0$ and updates the tree. By Lemma 2, $X_{-N}$ has law $\pi$, so the walk is stationary. By Lemma 1, $(t_0, X_0)$ has law $\mu$.

By the update rule, after the walk leaves a vertex $x$ at time $j$ by a step to $y \ne x$, the parent of $x$ is $y$, until $x$ becomes the root again. So if every vertex other than $X_0$ is visited during $[-N, 0)$, then $t_0$ is the *last-exit tree* $L$: each $x \ne X_0$ has as parent the vertex to which the walk moved at its last exit from $x$ before time 0. This tree is a function of the walk alone, not of $t_{-N}$. Let $A_N$ be the event that the walk covers $V$ during $[-N, 0]$. Then for each rooted tree $(t, \rho)$,

$$\big| \Pr[L = t, X_0 = \rho] - \mu(t, \rho) \big| \le \Pr[\text{not } A_N].$$

The law of $(L, X_0)$ on the event $A_N$ does not depend on how the walk before $-N$ is extended, and by termination $\Pr[\text{not } A_N] \to 0$. For a stationary walk indexed by all integers, which exists by the Kolmogorov extension theorem, $L$ is defined with probability 1, and letting $N \to \infty$ gives $\Pr[L = t, X_0 = \rho] = \mu(t, \rho)$.

## Step 4: reversal turns last exits into first entrances

Let $Y_i = X_{-i}$ for $i \ge 0$. By reversibility, $(Y_i)$ is a walk with the same transition probabilities, started from $\pi$. The last exit of $x$ before time 0 in $X$, at time $j < 0$ with $X_{j+1} = y$, is the first visit of $x$ by $Y$, at time $i = -j > 0$, coming from $Y_{i-1} = y$. So $L$ is the *first-entrance tree* of $Y$, with each $x \ne Y_0$ pointing to the vertex from which $Y$ first entered it. Hence, by Step 3 and (1),

$$\Pr[\text{first-entrance tree of } Y = t, \ Y_0 = \rho] = \mu(t, \rho) = \frac{c(\rho)}{W \prod_x c(x)} \prod_{x \ne \rho} c(x, t(x)).$$

Divide by $\Pr[Y_0 = \rho] = \pi(\rho) = c(\rho) / \sum_x c(x)$. The factor $c(\rho)$ cancels, and

$$\Pr[\text{first-entrance tree} = t \mid Y_0 = \rho] = K' \prod_{xy \in t} c(x, y)$$

for a constant $K'$ that does not depend on $\rho$ or $t$. A walk conditioned on $Y_0 = \rho$ is the walk started at $\rho$, which is what the algorithm runs with $r = \rho$; its first-entrance tree up to the cover time is the vertex tree of the output.

## Step 5: parallel edges

Given the sequence of vertices of the walk, the edge used in a step from $x$ to $y \ne x$ is the edge $e$ between them with probability $c_e / c(x, y)$, independently of all other steps. So, for an edge set $t$ that is a spanning tree with vertex tree $s$,

$$\Pr[T = t] = \Pr[\text{vertex tree} = s] \prod_{e \in t} \frac{c_e}{c(e)} = K' \prod_{e \in t} c(e) \cdot \prod_{e \in t} \frac{c_e}{c(e)} = K' \, c(t),$$

where $c(e)$ is the total weight between the ends of $e$. Summing over $t$ gives $K' = 1 / Z$. $\blacksquare$

**Disconnected graphs.** The implementation runs an independent walk in each component. Each walk gives a tree of its component with probability proportional to its weight product, so a spanning forest $F$ with the components of $G$ has probability proportional to $\prod_{e \in F} c_e$, which is uniform when all weights are 1.
