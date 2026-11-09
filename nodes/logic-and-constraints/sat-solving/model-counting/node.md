---
tag: JEBCXN
kind: problem
slug: model-counting
name: Model counting
aliases:
- '#SAT'
- sharpSAT
area: logic-and-constraints/sat-solving
level: advanced
summary: Count the satisfying assignments of a CNF formula. #P-complete, even for monotone 2-CNF (Valiant 1979). Exact DPLL counters split into components; ApproxMC uses random XOR hashes.
prereqs: [sat, conjunctive-normal-form, dpll, counting-problem]
see_also: [sat, 2-sat, xor-sat, valiant-vazirani-theorem, toda-theorem, karp-luby-algorithm, bdd-satisfy-count, k-wise-independence]
sources:
  - paper: doi:10.1137/0208032
    title: "Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8 (1979), 410 to 421"
    locator: the #P-completeness of counting the models of monotone 2-CNF formulas
  - paper: doi:10.1016/0304-3975(79)90044-6
    title: "Leslie G. Valiant, The complexity of computing the permanent, Theoretical Computer Science 8 (1979), 189 to 201"
    locator: the class #P and #P-completeness
  - paper: doi:10.1137/0220053
    title: "Seinosuke Toda, PP is as hard as the polynomial-time hierarchy, SIAM Journal on Computing 20 (1991), 865 to 877"
    locator: the polynomial hierarchy is in P with a #P oracle
  - paper: "Roberto J. Bayardo Jr. and Joseph D. Pehoushek, Counting models using connected components, Proceedings of the 17th National Conference on Artificial Intelligence (AAAI-2000), 157 to 162"
    locator: the DPLL counter with component decomposition (relsat)
  - paper: "Tian Sang, Fahiem Bacchus, Paul Beame, Henry Kautz and Toniann Pitassi, Combining component caching and clause learning for effective model counting, Theory and Applications of Satisfiability Testing (SAT 2004)"
    locator: component caching (Cachet)
  - paper: doi:10.1007/978-3-642-40627-0_18
    title: "Supratik Chakraborty, Kuldeep S. Meel and Moshe Y. Vardi, A scalable approximate model counter, Principles and Practice of Constraint Programming (CP 2013), LNCS 8124, 200 to 216"
    locator: ApproxMC, its (epsilon, delta) guarantee and its use of 3-wise independent XOR hash functions
  - paper: "Larry Stockmeyer, The complexity of approximate counting, Proceedings of the 15th ACM Symposium on Theory of Computing (STOC 1983), 118 to 126"
    locator: approximate counting with an NP oracle by hashing
  - book: isbn:9781643681603
    title: Armin Biere, Marijn Heule, Hans van Maaren and Toby Walsh (eds.), Handbook of Satisfiability, 2nd edition (2021)
    locator: the chapters on model counting and on approximate model counting
---

Model counting, written #SAT, asks for the number of satisfying assignments (models) of a [CNF](/conjunctive-normal-form/) formula. It is the [counting version](/counting-problem/) of [SAT](/sat/), and it is much harder: Valiant (1979) showed that it is #P-complete, and even for monotone [2-CNF](/2-sat/) formulas, where deciding satisfiability is trivial. By [Toda's theorem](/toda-theorem/), a #SAT oracle solves every problem of the polynomial hierarchy in polynomial time. Exact counters extend [DPLL](/dpll/) with two ideas, splitting the formula into independent components and caching their counts. Approximate counters such as ApproxMC add random XOR constraints that cut the set of models into small cells, and give a $(1 + \varepsilon)$ estimate with probability $1 - \delta$, under the hypothesis that the hash functions are 3-wise independent.

## In plain words

You have a list of yes-or-no choices and a list of rules. The question is no longer "can all rules hold?" but "in how many ways can they all hold?". With 50 choices there are about a million billion ways to check, so listing them is out of the question.

Two tricks help. First, if the rules split into groups that share no choices, count each group alone and multiply. Second, choose one switch, count the ways with it on and the ways with it off, and add. To estimate the count instead of computing it, add random "parity" rules, each of which cuts the number of solutions roughly in half. If after 20 such cuts a few solutions are left, there were about a million.

## Definition

The input is a CNF formula $F$ over $x_1, \ldots, x_n$. The output is $\#F = |\{x \in \{0, 1\}^n : x \text{ satisfies } F\}|$. Variables that occur in no clause still count: each doubles $\#F$.

[#P](/counting-problem/) is the class of functions that count the accepting paths of a polynomial-time nondeterministic machine. #SAT is in #P, and it is #P-complete under parsimonious reductions, since the Cook-Levin reduction preserves the number of witnesses.

## Variants

- **Weighted model counting.** Each literal has a weight, and the weight of a model is the product of its literal weights; the output is the sum over all models. It is the basis of probabilistic inference in Bayesian networks and probabilistic programs.
- **Projected model counting.** Count the assignments of a subset of the variables that extend to a model, as needed when the formula has auxiliary variables, for example from a [Tseitin transformation](/tseitin-transformation/).
- **#DNF.** Count the models of a DNF formula. It is #P-complete, but it has a polynomial randomized approximation scheme, the [Karp-Luby algorithm](/karp-luby-algorithm/).
- **#2-SAT, #Horn-SAT.** Still #P-complete. #XOR-SAT is easy: a consistent system of rank $r$ has $2^{n - r}$ solutions, by [Gaussian elimination](/xor-gaussian-elimination/).
- **Approximate counting.** Return $c$ with $\#F / (1 + \varepsilon) \le c \le (1 + \varepsilon) \#F$, with probability at least $1 - \delta$.

## Examples

**Components.** $F = (x_1 \vee x_2) \wedge (\neg x_2 \vee x_3) \wedge (x_4 \vee x_5)$ over $x_1, \ldots, x_6$. The first two clauses share $x_2$ and form one component on $\{x_1, x_2, x_3\}$; the third is a component on $\{x_4, x_5\}$; $x_6$ is free.

- First component: branch on $x_2$. With $x_2 = 1$, the second clause needs $x_3 = 1$ and $x_1$ is free: 2 models. With $x_2 = 0$, the first clause needs $x_1 = 1$ and $x_3$ is free: 2 models. Total 4.
- Second component: 3 of the 4 assignments satisfy $x_4 \vee x_5$.
- Free $x_6$: factor 2.

So $\#F = 4 \cdot 3 \cdot 2 = 24$, which a brute-force count over the 64 assignments confirms.

**Vertex covers.** For a graph $G$, the monotone 2-CNF formula with one clause $(x_u \vee x_v)$ per edge has as models exactly the vertex covers of $G$, and their complements are the independent sets. So counting models of monotone 2-CNF is counting independent sets, which is #P-complete.

## Known algorithms

**Exact counting by DPLL with components.** The counter of Birnbaum and Lozinskii, relsat (Bayardo and Pehoushek 2000), Cachet and sharpSAT works as follows, with $V$ the set of variables still free:

1. If $F$ has an empty clause, return 0. If $F$ has no clauses, return $2^{|V|}$.
2. If $F$ has a unit clause $(\ell)$, set $\ell$ true, simplify, and count the rest. A unit literal is forced, so no models are lost or added.
3. Let $U$ be the variables of $V$ that occur in $F$. Split the clauses into connected components, where two clauses are connected when they share a variable. If there are two or more, return $2^{|V \setminus U|}$ times the product of the counts of the components, each over its own variables. Components share no variables, so their models combine freely.
4. Otherwise pick a variable $v$, and return $2^{|V \setminus U|}$ times the sum of the counts of $F|_{v = 1}$ and $F|_{v = 0}$ over $U \setminus \{v\}$. The two cases are disjoint and cover everything.

Component caching stores the count of each component met before, keyed by its clauses, and clause learning from [CDCL](/cdcl/) prunes the search. A version of this counter was checked against brute force on 400 random formulas with up to 12 variables. Its running time is exponential in general, but it is $2^{O(w)} \cdot \mathrm{poly}$ when the branching order follows a decomposition of width $w$ of the formula, which is why it does well on structured formulas.

**Knowledge compilation.** Compile $F$ into a d-DNNF circuit or an ordered [binary decision diagram](/binary-decision-diagram/), on which [counting](/bdd-satisfy-count/) takes linear time in the size of the result. A DPLL counter with components that records its trace produces a d-DNNF.

**Approximate counting by hashing.** Pick a random hash $h(x) = Ax + b$ over GF(2), with $A$ an $m \times n$ matrix and $b$ a vector, both uniformly random; the constraint $h(x) = 0$ is $m$ random [XOR clauses](/xor-sat/). Each model survives with probability $2^{-m}$, so about $\#F / 2^m$ models remain. ApproxMC (Chakraborty, Meel and Vardi 2013) increases $m$ until the cell $\{x : F(x), h(x) = 0\}$ has at most a threshold number of models, which a SAT solver with XOR support enumerates, and returns the cell size times $2^m$. It repeats this and returns the median.

*Guarantee.* For every $\varepsilon > 0$ and $\delta \in (0, 1)$, ApproxMC returns $c$ with

$$\Pr\Big[\frac{\#F}{1 + \varepsilon} \le c \le (1 + \varepsilon)\, \#F\Big] \ge 1 - \delta,$$

using a number of SAT calls polynomial in $n$, $1/\varepsilon$ and $\log(1/\delta)$. The proof uses concentration of the cell size, which needs the hash family to be 3-wise independent: for any three distinct inputs, their hash values are independent and uniform. The family $Ax + b$ has this property: for distinct $x_1, x_2, x_3$, the vectors $(1, x_1), (1, x_2), (1, x_3)$ are linearly independent over GF(2), since no two are equal and the sum of all three has first coordinate 1. It is not 4-wise independent, since four inputs with $x_1 + x_2 + x_3 + x_4 = 0$ have hash values with sum 0. Both facts were checked exhaustively for $n = 3$ and one row. If the solver uses hash functions without this property, for example sparse XORs chosen for speed, the guarantee needs a separate proof. Later versions such as ApproxMC2 reduce the number of SAT calls.

**Older ideas.** Stockmeyer (1983) showed that approximate counting within any constant factor is possible in randomized polynomial time with an NP oracle, by the same hashing idea. The [Valiant-Vazirani theorem](/valiant-vazirani-theorem/) uses random XORs to isolate one model.

## Bounds

- **#P-complete** for general CNF, and for monotone 2-CNF (Valiant 1979), for Horn CNF, and for many other classes where SAT is easy. By Creignou and Hermann, #SAT for a class of Boolean constraints is in FP only for affine (XOR) constraints, and #P-complete otherwise.
- **Toda's theorem.** $\mathrm{PH} \subseteq \mathrm{P}^{\#\mathrm{P}}$, so #SAT is at least as hard as every level of the polynomial hierarchy.
- **Approximation.** Approximating #SAT within any factor is NP-hard, since a nonzero estimate decides SAT. With an NP oracle, it is possible in randomized polynomial time.
- **Exact time.** $O(2^n m k)$ by brute force; faster exponential algorithms exist for #2-SAT and #3-SAT, and the counter above runs in time exponential only in the treewidth.

## Reductions

- **Parsimonious reductions** preserve the number of solutions, so the reduction from a circuit to CNF with one auxiliary variable per gate, whose values are forced, keeps the count.
- **#SAT to weighted model counting**, with all weights 1, and back for rational weights with extra variables.
- **Probabilistic inference to weighted model counting.** A Bayesian network is encoded as a CNF with weights on literals, and the probability of evidence is a weighted model count.
- **Counting perfect matchings, the permanent, network reliability** and many other #P-complete problems reduce to #SAT and from it.

## Applications

Model counting is used for probabilistic inference in Bayesian networks and probabilistic logic programs, for quantitative information flow (how many secret values lead to the same output), for reliability of networks and systems, for counting configurations of products, and in neural network verification to estimate how often a property holds. Approximate counters also serve for near-uniform sampling of models, used in constrained random testing of hardware.

## References
