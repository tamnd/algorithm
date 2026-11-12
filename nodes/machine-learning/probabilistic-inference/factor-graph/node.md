---
tag: XJS0S3
kind: model
slug: factor-graph
name: Factor graph
area: machine-learning/probabilistic-inference
level: core
summary: "A bipartite graph of variable nodes and factor nodes for g(x) = product of local factors. It shows any BN or MRF factorization exactly; sum-product on a tree gives exact marginals."
history:
  year: 2001
  people: [Frank R. Kschischang, Brendan J. Frey, Hans-Andrea Loeliger]
  note: Kschischang, Frey and Loeliger defined factor graphs and the sum-product algorithm on them, and showed decoding, forward-backward, Kalman filtering and belief propagation as special cases.
prereqs: [graphical-model, bipartite-graph, bayesian-network, markov-random-field]
see_also: [belief-propagation, loopy-belief-propagation, tanner-graph, belief-propagation-decoding, ldpc-code, variable-elimination, hidden-markov-model, viterbi-algorithm]
sources:
  - paper: doi:10.1109/18.910572
    title: "Frank R. Kschischang, Brendan J. Frey and Hans-Andrea Loeliger, Factor Graphs and the Sum-Product Algorithm, IEEE Transactions on Information Theory 47(2), 2001"
    locator: pp. 498-519
  - paper: doi:10.1109/MSP.2004.1267047
    title: "Hans-Andrea Loeliger, An Introduction to Factor Graphs, IEEE Signal Processing Magazine 21(1), 2004"
    locator: pp. 28-41
  - book: isbn:9780387310732
    title: "Christopher M. Bishop, Pattern Recognition and Machine Learning, Springer, 2006"
    locator: Section 8.4.3 (factor graphs, and their construction from directed and undirected graphs) and Section 8.4.4 (the sum-product algorithm)
  - book: isbn:9780521642989
    title: "David J. C. MacKay, Information Theory, Inference, and Learning Algorithms, Cambridge University Press, 2003"
    locator: Chapter 26 (exact marginalization in graphs, the sum-product algorithm on factor graphs)
---

A factor graph is a [bipartite graph](/bipartite-graph/) that shows how a function of many variables factors into local functions. It has one node for each variable, one node for each factor, and an edge between a factor and each variable that the factor depends on. As a [graphical model](/graphical-model/) it describes the distribution $p(x) \propto \prod_a f_a(x_{\partial a})$. It can show the factorization of any [Bayesian network](/bayesian-network/) or [Markov random field](/markov-random-field/) exactly, including details that the undirected graph hides. The sum-product algorithm passes messages along its edges and computes exact marginals when the graph is a tree.

## The machine

**Data.** Variables $x_1, \ldots, x_n$, variable $x_i$ with $r_i$ values; factors $f_1, \ldots, f_m$, factor $f_a$ a nonnegative table on the variables $\partial a \subseteq \{1, \ldots, n\}$ that it depends on. The graph has an edge $(a, i)$ exactly when $i \in \partial a$. Edges never join two variables or two factors.

**The function it represents.**

$$
g(x_1, \ldots, x_n) = \prod_{a=1}^m f_a(x_{\partial a}), \qquad p(x) = \frac{g(x)}{Z}, \qquad Z = \sum_x g(x) .
$$

For example, $g = f_A(x_1)\,f_B(x_2)\,f_C(x_1, x_2, x_3)\,f_D(x_3, x_4)\,f_E(x_3, x_5)$ has five variable nodes, five factor nodes and the nine edges $A{-}1$, $B{-}2$, $C{-}1$, $C{-}2$, $C{-}3$, $D{-}3$, $D{-}4$, $E{-}3$, $E{-}5$. It is connected and has one edge fewer than nodes, so it is a tree.

**From a Bayesian network.** Make one factor per node, $f_i(x_i, x_{\mathrm{pa}(i)}) = p(x_i \mid x_{\mathrm{pa}(i)})$, joined to $x_i$ and its parents. Then $g$ is the joint distribution and $Z = 1$.

**From a Markov random field.** Make one factor per clique potential $\psi_C$, joined to the variables of $C$. Then $g/Z$ is the MRF distribution with the same $Z$.

**Back to an undirected graph.** Joining every pair of variables that share a factor gives the Markov random field graph of $p$. This loses information. Three pairwise factors on a triangle and one factor on all three variables give the same undirected triangle. The first factor graph has a cycle, the second is a tree, and the two describe different families: $3 \cdot 4 = 12$ table entries against $8$.

**Codes.** For a binary linear code with parity check matrix $H$, the indicator that $x$ is a codeword is $\prod_j [\,\sum_i H_{ji} x_i \equiv 0 \pmod 2\,]$, one factor per check. Its factor graph is the [Tanner graph](/tanner-graph/) of the code. Multiplying by the channel likelihoods $\prod_i p(y_i \mid x_i)$ gives the posterior over codewords, and sum-product on this graph is [belief propagation decoding](/belief-propagation-decoding/) of [LDPC codes](/ldpc-code/).

**The sum-product algorithm.** Messages are functions of one variable. For a variable $i$ and a factor $a$ with $i \in \partial a$:

$$
\mu_{i \to a}(x_i) = \prod_{b \ni i,\ b \ne a} \mu_{b \to i}(x_i), \qquad
\mu_{a \to i}(x_i) = \sum_{x_{\partial a \setminus i}} f_a(x_{\partial a}) \prod_{j \in \partial a \setminus i} \mu_{j \to a}(x_j) .
$$

The marginal of $x_i$ is proportional to $\prod_{a \ni i} \mu_{a \to i}(x_i)$. Replacing the sum by a maximum gives the max-product algorithm, which finds a most probable assignment.

*Small example.* Let $f_A(x_1) = (1, 2)$, $f_C(x_1, x_2) = 3$ when $x_1 = x_2$ and 1 otherwise, and $f_B(x_2) = (2, 1)$. The message from $f_C$ to $x_1$ is $\mu(x_1) = \sum_{x_2} f_C(x_1, x_2) f_B(x_2) = (3 \cdot 2 + 1 \cdot 1,\ 1 \cdot 2 + 3 \cdot 1) = (7, 5)$. Multiplying by $f_A$ gives $(7, 10)$, so $Z = 17$ and $p(x_1) = (7/17, 10/17)$.

## What it counts

- **Size.** The tables take $\sum_a \prod_{i \in \partial a} r_i$ numbers. For a Bayesian network this is the total size of the CPTs.
- **Brute force.** $Z$ and every marginal take $O(m \prod_i r_i)$ operations by enumeration. The implementation uses this as the reference.
- **Sum-product on a tree.** Each edge carries one message in each direction, $2|E|$ messages in total, where $|E| = \sum_a |\partial a|$. A message out of factor $a$ sums over its table, $O(|\partial a| \prod_{i \in \partial a} r_i)$ operations, and a message out of variable $i$ costs $O(\deg(i)\,r_i)$. Computing all messages by a pass toward a root and a pass back costs $O\big(\sum_a |\partial a|^2 \prod_{i \in \partial a} r_i + \sum_i \deg(i)^2 r_i\big)$, linear in the size of the tables for bounded degree. This is exponentially less than brute force.

## Relation to other models

- **Bayesian networks and Markov random fields.** Both convert to factor graphs with the same joint distribution. The factor graph keeps the exact grouping of the factors, which the MRF graph does not. It drops the directions of a Bayesian network, so independences that d-separation reads from v-structures have to be read from the tables.
- **Chains.** A [hidden Markov model](/hidden-markov-model/) is a chain-shaped factor graph. Sum-product on it is the forward-backward algorithm, max-product is the [Viterbi algorithm](/viterbi-algorithm/), and with Gaussian factors sum-product is the [Kalman filter](/kalman-filter/) and its smoother (Kschischang, Frey and Loeliger 2001).
- **Elimination.** [Variable elimination](/variable-elimination/) computes one marginal by summing out variables one at a time; sum-product on a tree is the same computation, organized so that all marginals share the work.
- **Normal factor graphs.** A variant puts variables on edges and factors on nodes. It is convenient for codes and state space models (Loeliger 2004).

## Known results in the model

**Sum-product is exact on trees.** If the factor graph is a tree, the sum-product messages give the exact marginals, after a number of message updates equal to $2|E|$ with a two-pass schedule.

*Proof.* Remove the edge between factor $a$ and variable $i$. The tree splits into two parts; let $T_{a \to i}$ be the set of factors in the part that contains $a$, and $V_{a \to i}$ the set of variables in that part other than $i$. We show by induction on the size of the part that

$$
\mu_{a \to i}(x_i) = \sum_{x_{V_{a \to i}}} \prod_{b \in T_{a \to i}} f_b(x_{\partial b}),
$$

and the same for variable-to-factor messages with the part on the variable's side. For a leaf factor ($\partial a = \{i\}$) both sides are $f_a(x_i)$; for a leaf variable the message is the empty product 1, and so is the empty sum of products. In the inductive step, the parts behind the different neighbors $j \in \partial a \setminus i$ share no variables and no factors, because the graph is a tree. So the sum over $x_{V_{a \to i}}$ of the product splits into the sum over $x_{\partial a \setminus i}$ of $f_a$ times a product of independent sums, one per $j$, and each is $\mu_{j \to a}(x_j)$ by induction. This is the message rule. The variable-to-factor case is the same with a product in place of the sum. Finally, the parts behind the factors $a \ni i$ cover all variables except $i$ and all factors, so $\prod_{a \ni i}\mu_{a \to i}(x_i) = \sum_{x_{-i}} g(x)$, the unnormalized marginal.

The test file checks the claim in exact arithmetic on random tree factor graphs, and checks that converting a Bayesian network or an MRF leaves the joint unchanged.

**On graphs with cycles.** The same updates, iterated, are [loopy belief propagation](/loopy-belief-propagation/). It need not converge, and when it does its beliefs are in general only approximate marginals. It works well on the sparse Tanner graphs of LDPC and turbo codes. Grouping factors into clusters until the graph of clusters is a tree restores exactness, at a cost exponential in the cluster size; this is the [junction tree](/junction-tree/) method.

**Generality.** Sum-product needs only that the products and sums form a commutative semiring. With (max, product) it finds MAP assignments, and with (min, +) on negative logarithms it finds minimum-energy assignments (Kschischang, Frey and Loeliger 2001). For the general message-passing algorithm on graphical models, see [belief propagation](/belief-propagation/).

## References
