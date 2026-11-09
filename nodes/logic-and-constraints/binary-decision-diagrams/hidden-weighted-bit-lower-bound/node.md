---
tag: QVG6Q6
kind: theorem
slug: hidden-weighted-bit-lower-bound
name: Hidden weighted bit lower bound
aliases:
- HWB lower bound
area: logic-and-constraints/binary-decision-diagrams
level: advanced
summary: The hidden weighted bit function needs OBDD size 2^(n/5) up to a polynomial factor under every variable order, but it has free BDDs with at most n(n+1)+2 nodes.
prereqs: [ordered-binary-decision-diagram, variable-ordering, free-binary-decision-diagram]
see_also: [multiplier-bdd-lower-bound, variable-ordering, free-binary-decision-diagram, read-once-branching-program, communication-complexity, hamming-weight, variable-ordering-np-hardness, friedman-supowit-ordering]
sources:
  - paper: doi:10.1109/12.73590
    title: Randal E. Bryant, On the complexity of VLSI implementations and graph representations of Boolean functions with application to integer multiplication, IEEE Transactions on Computers 40(2), 1991, pages 205 to 213
    locator: the hidden weighted bit function and its exponential OBDD size for every order
  - paper: "Beate Bollig, Martin Löbbing, Martin Sauerhoff, Ingo Wegener, On the complexity of the hidden weighted bit function for various BDD models, RAIRO Theoretical Informatics and Applications 33(2), 1999, pages 103 to 115"
    title: On the complexity of the hidden weighted bit function for various BDD models
    locator: the lower bound of order 2^(n/5) for OBDDs
  - paper: "Detlef Sieling, Ingo Wegener, Graph driven BDDs, a new data structure for Boolean functions, Theoretical Computer Science 141, 1995, pages 283 to 310"
    title: Graph driven BDDs, a new data structure for Boolean functions
    locator: the polynomial upper bound for HWB in the free BDD model
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 4, The OBDD size of selected functions (the hidden weighted bit function)
---

The hidden weighted bit function $\mathrm{HWB}_n$ reads the bit whose index is the number of 1s in the input. Bryant (1991) showed that its ordered BDD has exponential size under every variable order. The function is still simple: a [free BDD](/free-binary-decision-diagram/), where each path may read the variables in its own order, computes it with at most $n(n+1)$ inner nodes. So HWB separates OBDDs from free BDDs, and it shows that the restriction to one fixed [variable order](/variable-ordering/) costs an exponential factor for some functions. The lower bound uses a cut of the order and a fooling set, as in [communication complexity](/communication-complexity/).

## Statement

Let $x = (x_1, \ldots, x_n)$, and let $|x| = x_1 + \cdots + x_n$ be the [Hamming weight](/hamming-weight/). Define

$$\mathrm{HWB}_n(x) = \begin{cases} x_{|x|} & \text{if } |x| \ge 1, \\ 0 & \text{if } |x| = 0. \end{cases}$$

Sizes count the inner nodes and the two sinks.

**Theorem.** Let $b = \lfloor (n - 1)/5 \rfloor$.

1. *(OBDDs.)* For every order $\pi$ of the variables, the reduced $\pi$-OBDD of $\mathrm{HWB}_n$ has at least $\binom{b}{\lfloor b/2 \rfloor} \ge 2^{b}/(b + 1)$ nodes. This is $2^{n/5 - O(\log n)}$.
2. *(Free BDDs.)* There is a free BDD for $\mathrm{HWB}_n$ with at most $n(n+1)$ inner nodes.

Both parts have full proofs below. The constant $1/5$ is the one of Bollig, Löbbing, Sauerhoff and Wegener (1999); Bryant (1991) proved an exponential bound with a smaller constant.

## In plain words

The function counts the 1s in the input, and then looks at the input bit with that number. A BDD with one fixed order must read some bits early and keep them in mind. Later bits change the count, and so they change which of the early bits is the answer. If the early part contains many bits in a band of positions that the count can still reach, the BDD must remember every pattern of these bits, which needs exponentially many nodes. Every order has such a band at some point. A free BDD avoids the problem. It reads bits from both ends of the input, and after each read it knows whether the answer index is at the low end or the high end of the unread interval, so it never has to remember old bits.

## Proof

**Lemma 1 (restriction does not grow).** Setting variables to constants does not increase the size of the reduced OBDD for the induced order. This is Lemma 1 on the page [NP-completeness of OBDD variable ordering](/variable-ordering-np-hardness/).

**Lemma 2 (fooling lemma).** If every variable of a set $T$ comes before every variable of a set $B$ in $\pi$, the function $g$ depends only on $T \cup B$, and the subfunctions $g|_{\alpha_1}, \ldots, g|_{\alpha_N}$ for assignments $\alpha_i$ to $T$ are pairwise different, then the $\pi$-OBDD of $g$ has at least $N$ nodes.

*Proof.* Follow the path of each $\alpha_i$ from the root to the first node that does not test a variable of $T$. That node computes $g|_{\alpha_i}$, so different $i$ end at different nodes. $\square$

**Lemma 3 (a band of early variables).** Let $T$ be the set of the first $t$ variables of $\pi$ and $B$ the rest. Suppose that there are a set $A \subseteq T$ with $|A| = a$, a set $F \subseteq B$ with $|F| = f$, and integers $s, c$ with $0 \le s \le a$ and $0 \le c \le n - a - f$, such that every index in $A$ lies in $[s + c, s + c + f]$. Then the $\pi$-OBDD of $\mathrm{HWB}_n$ has at least $\binom{a}{s}$ nodes.

*Proof.* Set $c$ of the variables outside $A \cup F$ to 1 and the others to 0, and call the result $g$. By Lemma 1, it is enough to bound the size for $g$. Let $\alpha \ne \alpha'$ be assignments to $A$ with weight $s$, and let $j \in A$ be an index with $\alpha_j \ne \alpha'_j$. Since $s + c \le j \le s + c + f$, there is an assignment $\beta$ to $F$ with weight $j - s - c$. Then $(\alpha, \beta)$ and $(\alpha', \beta)$ both have weight $s + c + (j - s - c) = j \ge 1$, so $g(\alpha, \beta) = \alpha_j \ne \alpha'_j = g(\alpha', \beta)$. So the $\binom{a}{s}$ assignments of weight $s$ give pairwise different subfunctions, and Lemma 2 gives the bound. $\square$

**Proof of part 1.** If $b = 0$ the bound is 1, so let $b \ge 1$. Put $\mu = \lceil b/2 \rceil$ and $M = [\mu + 1, \mu + 4b]$, a band of $4b$ indices. Since $5b \le n - 1$, we have $2\mu + 4b \le 5b + 1 \le n$, so $M \subseteq [1, n - \mu]$.

*Choice of the cut.* For $t = 0, 1, \ldots, n$, let $T_t$ be the first $t$ variables of $\pi$. The number $|T_t \cap M|$ starts at 0, ends at $4b$, and grows by at most 1 per step, so some $t$ has $|T_t \cap M| = 2b$. Fix this $t$, with $T = T_t$ and $B$ the rest. Then $B$ contains the other $2b$ variables of $M$, so $|B| \ge 2b$.

*Choice of the band.* Split $M$ into the halves $M_1 = [\mu + 1, \mu + 2b]$ and $M_2 = [\mu + 2b + 1, \mu + 4b]$. The $2b$ variables of $T \cap M$ are in these halves, so one half, call it $[L, L + 2b - 1]$, contains at least $b$ of them. Let $A$ be $b$ of them, so $a = b$. Let $F$ be any $2b - 1$ variables of $B$, so $f = 2b - 1$. Let $s = \lfloor b/2 \rfloor$ and $c = L - s$.

*Check of the conditions of Lemma 3.* The indices of $A$ lie in $[L, L + f] = [s + c, s + c + f]$. Next, $c \ge 0$ since $L \ge \mu + 1 > s$. Last, $c \le n - a - f$ means $L - \lfloor b/2 \rfloor \le n - 3b + 1$. The largest $L$ is $\mu + 2b + 1$, and $\mu + 2b + 1 - \lfloor b/2 \rfloor = 2b + 1 + (b \bmod 2) \le n - 3b + 1$ because $5b + 1 \le n$. So Lemma 3 gives at least $\binom{b}{\lfloor b/2 \rfloor}$ nodes. This is the largest of the $b + 1$ binomial coefficients $\binom{b}{i}$, whose sum is $2^b$, so it is at least $2^b/(b+1)$. $\square$

**Proof of part 2.** The free BDD has a node $(p, q, \gamma)$ for $1 \le p \le q \le n$ and $\gamma \in \{0, 1\}$, so $n(n+1)$ inner nodes, and the root is $(1, n, 1)$. For $p > q$, $(p, q, 1)$ is the 0-sink and $(p, q, 0)$ is the 1-sink. The edges are:

- $(p, q, 1)$ tests $x_q$. Its 0-edge goes to $(p, q - 1, 1)$ and its 1-edge to $(p, q - 1, 0)$.
- $(p, q, 0)$ tests $x_p$. Its 1-edge goes to $(p + 1, q, 0)$ and its 0-edge to $(p + 1, q, 1)$.

Every edge shrinks the interval $[p, q]$ by the index that it read, so no path reads a variable twice, and the diagram is a free BDD. For an input $x$ and $p \le q + 1$, let $w_1 = p - 1 + |x_{p..q}|$ and $w_0 = p + |x_{p..q}|$, where $|x_{p..q}|$ counts the 1s among $x_p, \ldots, x_q$. We claim:

- $(p, q, 1)$ computes $x_{w_1}$ if $w_1 \ge p$, and 0 if $w_1 = p - 1$;
- $(p, q, 0)$ computes $x_{w_0}$ if $w_0 \le q$, and 1 if $w_0 = q + 1$.

The proof is by induction on $q - p$. For $p = q + 1$, $w_1 = p - 1$ and $w_0 = q + 1$, and the sinks are 0 and 1, as claimed. Now let $p \le q$.

- At $(p, q, 1)$ with $x_q = 0$: $w_1$ is the same for $[p, q - 1]$, and $w_1 \le q - 1$, so the value is that of $(p, q - 1, 1)$.
- At $(p, q, 1)$ with $x_q = 1$: $w_1 = p + |x_{p..q-1}|$, which is $w_0$ for $[p, q - 1]$. If $w_1 = q$, the claimed value is $x_q = 1$, which is what $(p, q - 1, 0)$ gives for $w_0 = (q - 1) + 1$. Otherwise $w_1 \le q - 1$, and both sides are $x_{w_1}$.
- At $(p, q, 0)$ with $x_p = 1$: $w_0 = (p + 1) + |x_{p+1..q}|$, which is $w_0$ for $[p + 1, q]$, so the value is that of $(p + 1, q, 0)$.
- At $(p, q, 0)$ with $x_p = 0$: $w_0 = p + |x_{p+1..q}| = (p + 1) - 1 + |x_{p+1..q}|$, which is $w_1$ for $[p + 1, q]$. If $w_0 = p$, the claimed value is $x_p = 0$, and $(p + 1, q, 1)$ gives 0 because its $w_1$ is $(p + 1) - 1$. Otherwise $w_0 \ge p + 1$, and both sides are $x_{w_0}$.

At the root, $w_1 = |x|$, so the root computes $x_{|x|}$ if $|x| \ge 1$ and 0 otherwise, which is $\mathrm{HWB}_n$. $\blacksquare$

## Consequences

- **OBDDs are weaker than free BDDs.** HWB has polynomial free BDDs and only exponential OBDDs. So the [read-once branching program](/read-once-branching-program/) model is exponentially stronger than its ordered restriction.
- **No reordering helps.** [Sifting](/bdd-sifting/), [window permutation](/window-permutation-reordering/) and even the exact [Friedman-Supowit](/friedman-supowit-ordering/) algorithm can only find the best of a set of exponential sizes.
- **Hard functions can be simple.** HWB has small circuits: count the 1s and select a bit. Like [multiplication](/multiplier-bdd-lower-bound/), it shows that the OBDD size is not a good measure of the circuit complexity of a function.
- **Testing other models.** HWB is a standard test function for the BDD variants between OBDDs and free BDDs, for example graph-driven BDDs and partitioned OBDDs. Bollig, Löbbing, Sauerhoff and Wegener (1999) compare these models on it.

The table shows measured OBDD sizes for small $n$: the smallest and the largest over all orders, from a dynamic program over sets of variables, and the size under the natural order $x_1, \ldots, x_n$. The best orders found read the variables from the outside in: $x_n, x_{n-1}, x_1, x_{n-2}, x_2, \ldots$.

| $n$ | smallest | largest | natural |
|---|---|---|---|
| 3 | 5 | 7 | 7 |
| 4 | 9 | 11 | 10 |
| 5 | 16 | 17 | 17 |
| 6 | 23 | 27 | 25 |
| 7 | 33 | 43 | 40 |
| 8 | 46 | 66 | 57 |
| 9 | 63 | 101 | 85 |
| 10 | 82 | 152 | 121 |
| 11 | 109 | 229 | 172 |
| 12 | 139 | 337 | 240 |
| 13 | 178 | 490 | 335 |
| 14 | 224 | 713 | 459 |

The reduced free BDDs from part 2 have 3, 3, 5, 8, 13, 20, 29, 40, 53, 68, 85, 104, 125 and 148 nodes for $n = 1, \ldots, 14$, so they are smaller than the best OBDD from $n = 4$ on.

## Tightness

- **The upper bound is exponential too.** The OBDD of any function of $n$ variables has $O(2^n/n)$ nodes, and the measured best sizes grow by a factor of about 1.25 to 1.35 per added variable in the table. Bollig, Löbbing, Sauerhoff and Wegener (1999) also give upper bounds for good orders; we do not reproduce their constant.
- **The polynomial factor.** Our proof loses the factor $b + 1$ by using a fooling set of fixed weight. It does not change the exponent $n/5$.
- **The order of the free BDD is not fixed.** In the free BDD of part 2, the path for $x$ reads variables from both ends, and the choice depends on the bits read. If the BDD must use one order for all paths, the theorem says the size becomes exponential.

## History

Bryant (1991) defined the hidden weighted bit function in his paper on the BDD complexity of multiplication, as a simple function with exponential OBDD size for every order. Sieling and Wegener (1995) showed that it has polynomial size in more general models, such as free BDDs and graph-driven BDDs. Bollig, Löbbing, Sauerhoff and Wegener (1999) gave the sharper lower bound of order $2^{n/5}$ and studied HWB in many BDD models. The function is a standard example in Wegener's book on branching programs (2000).

## References
