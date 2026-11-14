---
tag: 0PZ387
kind: algorithm
slug: bdd-constrained-random-generation
name: BDD-based constrained random generation
aliases:
- weighted BDD stimulus generation
- Yuan constraint solver
area: eda/hardware-verification
level: advanced
summary: Yuan and coauthors' generator that builds a BDD of the constraints, weights each node by the count of solutions below it and walks down to draw solutions with set biases.
solves: [constrained-random-stimulus-generation]
model: word-ram
complexity:
  vars: {n: the number of Boolean variables, B: the number of nodes of the BDD of the constraint, w: the word size}
  time: {setup: "O(B n / w)", query: "O(n^2 / w)"}
  space: {extra: "O(B n / w)"}
properties: {deterministic: false, exact: true, online: false, recursive: false}
history:
  year: 1999
  people: [Jun Yuan, Kurt Shultz, Carl Pixley, Hillel Miller, Adnan Aziz]
  note: Yuan, Shultz, Pixley, Miller and Aziz built BDDs of the input constraints of a simulation and drew biased random solutions by weights on the nodes, at ICCAD 1999, with a journal version in 2000.
prereqs: [constrained-random-stimulus-generation, reduced-ordered-bdd, bdd-satisfy-count]
see_also: [rejection-sampling, model-counting, variable-ordering, bdd-quantification, total-variation-distance, chi-squared-goodness-of-fit-test, geometric-distribution, functional-coverage]
sources:
  - paper: doi:10.1109/ICCAD.1999.810715
    title: Jun Yuan, Kurt Shultz, Carl Pixley, Hillel Miller and Adnan Aziz, Modeling design constraints and biasing in simulation using BDDs, Proceedings of the IEEE/ACM International Conference on Computer-Aided Design (ICCAD), 1999
    locator: the BDD of the constraints over inputs and state, the weights computed bottom-up on the nodes, and the top-down walk that draws biased solutions
  - paper: "Jun Yuan, Kurt Shultz, Carl Pixley, Hillel Miller and Adnan Aziz, Automatic vector generation using constraints and biasing, Journal of Electronic Testing 16, 107 to 120, 2000"
    title: J. Yuan, K. Shultz, C. Pixley, H. Miller and A. Aziz, Automatic vector generation using constraints and biasing, Journal of Electronic Testing, Theory and Applications 16, 107 to 120, 2000
    locator: the journal version of the BDD-based generator (general locator)
  - book: isbn:9780387259475
    title: Jun Yuan, Carl Pixley and Adnan Aziz, Constraint-Based Verification, Springer, 2006
    locator: the chapters on constraint BDDs, on random generation from them with input biases, and on the treatment of state variables (general locator)
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 677 to 691, 1986
    locator: Section 4.6 (Satisfy-count, the count of the satisfying assignments of a BDD)
---

BDD-based constrained random generation solves the [constrained random stimulus generation](/constrained-random-stimulus-generation/) problem when the constraint fits in a [binary decision diagram](/binary-decision-diagram/). Build the [reduced ordered BDD](/reduced-ordered-bdd/) of the constraint $C$ over $n$ Boolean variables. Store at each node the number of solutions of the function below it, by the recurrence of [satisfy-count](/bdd-satisfy-count/) with factors of 2 for the variables that an edge skips. Then walk from the root to the terminal 1, taking each branch with probability proportional to the count of solutions under it, and fill the skipped variables with fair bits. Each solution comes out with probability exactly $1/\#C$, and one sample costs $O(n)$ steps. With weights on the nodes in place of counts, the same walk draws from the law in which each variable has its own bias, conditioned on $C$; this is the generator of Yuan, Shultz, Pixley, Miller and Aziz (1999). The price is the BDD itself, which can be exponential in $n$.

## In plain words

The rules for legal inputs are first turned into a decision diagram: a chart in which each step asks about one input bit and goes left for 0 and right for 1, and every route that ends at "yes" is a legal input.

Each point of the chart is labeled with the number of legal inputs that can still be finished from there. To draw an input, start at the top and at each point go left or right with chances in proportion to the labels on the two sides. Bits that the chart never asks about on the chosen route can be anything, so they are flipped like fair coins.

Every legal input is drawn equally often. To favor some inputs, the labels count weighted inputs instead of plain ones, and the same walk follows the weights.

## The problem

**Input.** A reduced ordered BDD with root $\mathrm{root}$ of a constraint $C : \{0, 1\}^n \to \{0, 1\}$ under the order $x_0 < x_1 < \cdots < x_{n-1}$; a source of uniform random integers.

**Output.** A model $x$ of $C$ drawn with $\Pr[x = s] = 1/\#C$ for every model $s$, or "no solution" when $\#C = 0$. In the weighted variant, biases $p_0, \ldots, p_{n-1} \in (0, 1)$ are given, and $\Pr[x = s] = w(s) / \sum_{t \models C} w(t)$ with $w(s) = \prod_i p_i^{s_i} (1 - p_i)^{1 - s_i}$.

**Notation.** $\ell(u)$ is the level of node $u$, the index of its variable, and the terminals 0 and 1 have level $n$. $\mathrm{lo}(u)$ and $\mathrm{hi}(u)$ are the children for $x_{\ell(u)} = 0$ and $1$. An edge from $u$ to $v$ skips the $\ell(v) - \ell(u) - 1$ variables between them.

## The algorithm

The count $N(u)$ is the number of assignments of $x_{\ell(u)}, \ldots, x_{n-1}$ that satisfy the function of $u$. A branch of $u$ toward a child $v$ has $2^{\ell(v) - \ell(u) - 1} N(v)$ such assignments, since the skipped variables are free, and the two branches together have $N(u)$. The walk takes each branch with probability equal to its share.

```pseudo id=main
L1  for each node u below root, children first: N(0) ← 0, N(1) ← 1, N(u) ← 2^(ℓ(lo(u))−ℓ(u)−1) N(lo(u)) + 2^(ℓ(hi(u))−ℓ(u)−1) N(hi(u))
L2  if N(root) = 0 then return "no solution"
L3  u ← root; draw x_i as a fair bit for every i < ℓ(root)
L4  while u is not a terminal:
L5      c1 ← 2^(ℓ(hi(u))−ℓ(u)−1) N(hi(u))
L6      draw r uniformly from {0, 1, ..., N(u) − 1}
L7      if r < c1 then x_ℓ(u) ← 1, next ← hi(u) else x_ℓ(u) ← 0, next ← lo(u)
L8      draw x_i as a fair bit for every i with ℓ(u) < i < ℓ(next)
L9      u ← next
L10 return x
```

Line L1 runs once per constraint, and lines L3 to L10 once per sample. The number of models is $\#C = 2^{\ell(\mathrm{root})} N(\mathrm{root})$. Line L6 draws an integer, not a real number: the branch probability $c_1 / N(u)$ is then exact.

## Example

Take $C = x_0 x_1 + x_3$ over four variables. The variable $x_2$ does not occur, and the BDD has three nodes: the root $a$ at level 0 with $\mathrm{lo}(a) = c$ and $\mathrm{hi}(a) = b$; the node $b$ at level 1 with $\mathrm{lo}(b) = c$ and $\mathrm{hi}(b) = 1$; and the node $c$ at level 3 with $\mathrm{lo}(c) = 0$ and $\mathrm{hi}(c) = 1$.

| node | level | branch 0 | branch 1 | $N$ |
|---|---|---|---|---|
| $c$ | 3 | $2^0 \cdot 0 = 0$ | $2^0 \cdot 1 = 1$ | 1 |
| $b$ | 1 | to $c$, skips $x_2$: $2^1 \cdot 1 = 2$ | to 1, skips $x_2, x_3$: $2^2 \cdot 1 = 4$ | 6 |
| $a$ | 0 | to $c$, skips $x_1, x_2$: $2^2 \cdot 1 = 4$ | to $b$: $2^0 \cdot 6 = 6$ | 10 |

So $\#C = 10$: eight models with $x_3 = 1$, and two with $x_0 = x_1 = 1$, $x_3 = 0$. Take the model $s = (1, 0, 1, 1)$. The walk goes to $b$ with probability $6/10$, then to $c$ with probability $2/6$, fills $x_2 = 1$ with probability $1/2$, and at $c$ goes to 1 with probability $1/1$. The product is $\frac{6}{10} \cdot \frac{2}{6} \cdot \frac{1}{2} \cdot 1 = \frac{1}{10}$. The model $(0, 1, 0, 1)$ has $\frac{4}{10} \cdot \frac{1}{4} \cdot 1 = \frac{1}{10}$, with the factor $\frac{1}{4}$ for the two skipped variables, and $(1, 1, 0, 0)$ has $\frac{6}{10} \cdot \frac{4}{6} \cdot \frac{1}{4} = \frac{1}{10}$.

**With biases.** Let $p_3 = 1/4$ and the other biases be $1/2$. The weights are $W(c) = \frac{1}{4}$, $W(b) = \frac{1}{2} \cdot \frac{1}{4} + \frac{1}{2} \cdot 1 = \frac{5}{8}$ and $W(a) = \frac{1}{2} \cdot \frac{1}{4} + \frac{1}{2} \cdot \frac{5}{8} = \frac{7}{16}$, which is the probability of $C$ under the biases. Each of the eight models with $x_3 = 1$ has weight $\frac{1}{8} \cdot \frac{1}{4} = \frac{1}{32}$ and probability $\frac{1}{32} / \frac{7}{16} = \frac{1}{14}$; each of the two with $x_3 = 0$ has weight $\frac{1}{8} \cdot \frac{3}{4} = \frac{3}{32}$ and probability $\frac{3}{14}$. Under the constraint, $x_3 = 1$ has probability $\frac{8}{14} = \frac{4}{7}$, not $\frac{1}{4}$: a bias is a weight before conditioning, not the final marginal.

## Correctness

The proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts.

- $N(u)$ counts the satisfying assignments of the variables from the level of $u$ down, skipped variables included, so $\#C = 2^{\ell(\mathrm{root})} N(\mathrm{root})$.
- The walk never enters the terminal 0, so every output is a model.
- For a model $s$, the probability of the walk along its path is $2^{-\ell(\mathrm{root})} \prod_j N(u_{j+1}) / N(u_j)$ after the factors for the skipped variables cancel, and the product telescopes to $1/\#C$. This is exact for every model, with the don't-care variables above the root and on the edges filled by fair bits.
- The weighted walk gives $w(s) / Z$ by the same telescoping with $W$ in place of $N$, and [rejection sampling](/rejection-sampling/) from uniform assignments is also exact, with a [geometric](/geometric-distribution/) number of tries of mean $2^n / \#C$.

The tests check the exact law in Fractions by running the sampler on every outcome of its random draws, against the models found by evaluating the constraint on all $2^n$ assignments. The [chi-square](/chi-squared-goodness-of-fit-test/) statistic and the [total variation distance](/total-variation-distance/) of a fixed-seed sample, and the mean number of rejection tries, are measured, not proved.

## Complexity

- **Building the BDD.** Not part of this algorithm, and the dominant cost. The size $B$ depends on the constraint and the [variable order](/variable-ordering/); it is linear for many control constraints, and exponential under every order for a constraint on the middle output bit of a multiplier.
- **Counts.** Line L1 does one shift and one addition per node, on integers below $2^{n+1}$, so $O(B n / w)$ word operations and $O(B n / w)$ words of storage. With a fixed BDD, the counts serve every later sample.
- **One sample.** At most $n$ iterations, each with a comparison and a random integer below $2^n$, plus $n$ fair bits in all: $O(n^2 / w)$ word operations, or $O(n)$ if the counts fit in a word.
- **Weighted.** The weights $W(u)$ are rationals whose size grows with the denominators of the biases; with biases that are multiples of $2^{-k}$, they are integers of $O(n k)$ bits after scaling. A change of the biases needs a new bottom-up pass.
- **Rejection.** $O(n)$ per try and $2^n / \#C$ tries on average, which is far worse when the constraint is tight.

## Properties

- **Exact.** The law is exactly uniform, or exactly the conditioned bias law, given exact random integers.
- **Independent samples.** Each walk uses fresh randomness, so samples are independent and can repeat; unlike `randc`, the generator does not cycle through the solutions.
- **Order independent law.** Every variable order gives the same law; the order changes only the size of the BDD.
- **Bounded time.** Each sample takes at most $n$ steps, with no retries, unlike rejection.

## Variants and improvements

- **Biases on inputs (Yuan et al.).** Each input has a bias $p_i$, and the generator draws from the bias law conditioned on the constraint, by the weights $W(u) = (1 - p_{\ell(u)}) W(\mathrm{lo}(u)) + p_{\ell(u)} W(\mathrm{hi}(u))$ with $W(0) = 0$ and $W(1) = 1$; skipped variables add the factor $1$ and are drawn with their own bias. The engineer sets biases to make rare cases likely.
- **State variables.** In a simulation the constraint $C(q, x)$ depends on the state $q$. Placing the state variables above the inputs in the order lets the walk follow the current values of $q$ and sample only the inputs. The counts of the input part are then the counts of the inputs for that state, so the law is uniform over the legal inputs of the current state.
- **Auxiliary variables.** If $C(x, y)$ uses auxiliary variables $y$, path counting over all variables is uniform over pairs $(x, y)$, not over stimuli $x$. Quantify $y$ out first with [BDD quantification](/bdd-quantification/), and sample $\exists y\, C$.
- **Many constraints.** Constraints that share no variables have separate BDDs, and a sample is the union of independent samples; the BDD of their conjunction is never built.
- **Other compiled forms.** The same bottom-up count and top-down walk work on any decision diagram or circuit form that supports linear-time [model counting](/model-counting/), and fail on forms that do not.

## When to use it

- The constraint has a BDD of manageable size, and many samples are drawn from it, as in a simulation that draws one transaction per cycle.
- The law must be exact, for example to make [functional coverage](/functional-coverage/) results comparable between runs, or to give rare legal inputs their fair share.
- Not when the constraint holds wide arithmetic, such as a product of two 32-bit words, whose BDD is too large; use a SAT-based or hashing-based generator from the problem page.
- Not needed when the constraint is loose: if $\#C / 2^n$ is large, rejection sampling is exact and simpler.

## Pitfalls

- **A fair coin at each node.** Walking down by a fair coin wherever both children are nonzero is not uniform. In the example it gives $(0, 0, 0, 1)$ the probability $\frac{1}{2} \cdot \frac{1}{4} = \frac{1}{8}$ and $(1, 1, 0, 0)$ the probability $\frac{1}{2} \cdot \frac{1}{2} \cdot \frac{1}{4} = \frac{1}{16}$, against $\frac{1}{10}$ for both.
- **Forgetting the skipped variables.** Counting with $N(u) = N(\mathrm{lo}) + N(\mathrm{hi})$ treats a branch that skips variables as having fewer solutions than it has. In the example, the root would split $1 : 2$ in place of $4 : 6$.
- **Floating-point counts.** Counts above $2^{53}$ lose bits in a double, and a probability computed as a quotient of floats is not exact. Keep integer counts and draw an integer below $N(u)$.
- **Biases are not marginals.** A bias of $1/4$ on $x_3$ gave $x_3 = 1$ the probability $4/7$ in the example. To get a target marginal, the biases must be tuned against the constraint.
- **Pseudo-random numbers.** The theorems assume ideal random integers. A poor generator, or one reseeded in the same way for each test, repeats the same stimuli.

## Implementations

## History

Bryant (1986) introduced reduced ordered BDDs and counted their satisfying assignments in time linear in their size. Yuan, Shultz, Pixley, Miller and Aziz (ICCAD 1999) used BDDs of the input constraints of a simulation environment to generate random input vectors, with biases on the inputs, by weights computed bottom-up on the BDD and a top-down walk; the journal version appeared in 2000. Yuan, Pixley and Aziz describe the method, with its treatment of state variables, in their book of 2006. SystemVerilog later made constrained random generation part of the language, in Clause 18 of IEEE Std 1800, and leaves the solver to the tool.

## References
