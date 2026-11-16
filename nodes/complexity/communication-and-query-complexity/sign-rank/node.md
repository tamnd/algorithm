---
tag: P1JPH5
kind: concept
slug: sign-rank
name: Sign rank
aliases:
- dimension complexity
area: complexity/communication-and-query-complexity
level: research
summary: "The least rank of a real matrix with the same sign pattern as a given +1/-1 matrix. Its logarithm equals the unbounded-error communication cost up to an additive constant."
prereqs: [rank, randomized-communication-complexity]
see_also: [log-rank-lower-bound, discrepancy-method, inner-product-problem, disjointness-problem, halfspace-learning, perceptron, tc0, approximate-degree]
sources:
  - paper: "Ramamohan Paturi and Janos Simon, Probabilistic communication complexity, Journal of Computer and System Sciences 33(1) (1986), 106-123"
    locator: the unbounded-error model and its characterization by the dimension of a realization by points and halfspaces
  - paper: "Jürgen Forster, A linear lower bound on the unbounded error probabilistic communication complexity, Journal of Computer and System Sciences 65(4) (2002), 612-625"
    locator: the main theorem, sign rank at least the square root of NM divided by the spectral norm, and the Hadamard example
  - paper: "Noga Alon, Péter Frankl and Vojtěch Rödl, Geometrical realization of set systems and probabilistic communication complexity, Proceedings of the 26th IEEE Symposium on Foundations of Computer Science (FOCS 1985), 277-280"
    locator: most N x N sign matrices have sign rank linear in N
  - paper: doi:10.1137/080744037
    title: "Alexander A. Razborov and Alexander A. Sherstov, The sign-rank of AC0, SIAM Journal on Computing 39(5) (2010), 1833-1855"
    locator: the function in AC0 with sign rank exp(Omega(n^(1/3))); conference version FOCS 2008
  - paper: doi:10.1137/080733644
    title: "Alexander A. Sherstov, The pattern matrix method, SIAM Journal on Computing 40(6) (2011), 1969-2000"
    locator: pattern matrices, which turn degree bounds for Boolean functions into communication bounds; conference version STOC 2008
  - paper: "Shai Ben-David, Nadav Eiron and Hans Ulrich Simon, Limitations of learning via embeddings in Euclidean half spaces, Journal of Machine Learning Research 3 (2003), 441-461"
    locator: most concept classes cannot be embedded in halfspaces of small dimension
---

The sign rank of a matrix $S$ with entries $\pm 1$ is the least rank of a real matrix $A$ with $\operatorname{sign}(A_{xy}) = S_{xy}$ for every entry. It can be far smaller than the ordinary [rank](/rank/): the sign matrix of equality has full rank but sign rank at most 3. Paturi and Simon (1986) showed that $\log_2$ of the sign rank of the communication matrix equals, up to an additive constant, the cost of the best private-coin protocol that only has to be correct with probability above $1/2$. Strong lower bounds on sign rank are hard to prove; the main tools are Forster's spectral bound and the methods of Razborov and Sherstov.

## In plain words

Take a table of plus and minus signs. Try to put a point in space for each row and a flat wall through the center for each column, so that each point lies on the plus side or the minus side of each wall exactly as the table says. The sign rank is the smallest number of dimensions in which this works.

Some tables with a complex pattern fit in very few dimensions, because only the signs must match, not the exact numbers. Other tables need many dimensions. The number of dimensions needed tells how hard the table is for two players who may answer at random and only have to be right slightly more often than wrong.

## The idea

**Definition.** Let $S \in \{-1, +1\}^{X \times Y}$. Then

$$\operatorname{rank}_\pm(S) = \min \{ \operatorname{rank}(A) : A \in \mathbb{R}^{X \times Y},\ \operatorname{sign}(A_{xy}) = S_{xy} \text{ for all } x, y \}.$$

All entries of $A$ must be nonzero. For a Boolean function $f$ on $X \times Y$ take $S_{xy} = (-1)^{f(x,y)}$ or $(-1)^{1 - f(x,y)}$; the sign rank is the same for both.

**Geometric form.** A rank-$d$ matrix factors as $A_{xy} = \langle u_x, v_y \rangle$ with $u_x, v_y \in \mathbb{R}^d$. So $\operatorname{rank}_\pm(S) \le d$ exactly when there are points $u_x$ and homogeneous halfspaces $\{u : \langle u, v_y \rangle > 0\}$ in $\mathbb{R}^d$ with $u_x$ inside the halfspace of $y$ exactly when $S_{xy} = +1$. In learning theory this number is the dimension complexity of the concept class whose concepts are the columns.

**Unbounded-error communication.** Let $U(f)$ be the least cost of a private-coin protocol that outputs $f(x,y)$ with probability strictly above $1/2$ on every input. Paturi and Simon proved

$$\log_2 \operatorname{rank}_\pm(M_f) - O(1) \le U(f) \le \log_2 \operatorname{rank}_\pm(M_f) + O(1).$$

*Protocols give low sign rank.* In a private-coin protocol of cost $c$, the probability of a transcript $t$ on input $(x, y)$ is a product $a_t(x)\, b_t(y)$, since each player's moves depend only on that player's input and coins. The acceptance probability $P(x,y) = \sum_{t \text{ accepting}} a_t(x) b_t(y)$ has rank at most $2^c$. Then $P - \tfrac12 J$ has rank at most $2^c + 1$ and the sign pattern of $f$. So $\log_2 \operatorname{rank}_\pm(M_f) \le c + 1$.

*Low sign rank gives protocols.* Let $\operatorname{sign}\langle u_x, v_y \rangle = (-1)^{1 - f(x,y)}$ with vectors in $\mathbb{R}^d$. Scale each $u_x$ so that $\sum_i |u_{x,i}| = 1$, and each $v_y$ so that $\max_i |v_{y,i}| \le 1$; positive scaling keeps all signs. Alice picks $i$ with probability $|u_{x,i}|$ and sends $i$ and the sign $s$ of $u_{x,i}$, in $\lceil \log_2 d \rceil + 1$ bits. Bob outputs 1 with probability $(1 + s\, v_{y,i})/2$. The expected value of Bob's output in $\pm 1$ form is $\sum_i |u_{x,i}|\, s\, v_{y,i} = \langle u_x, v_y \rangle$, which has the right sign. So Bob is right with probability above $1/2$.

The model needs private coins. With public coins every function has unbounded-error cost $O(1)$: the players guess $x$ from the shared coins, Alice says whether the guess is right, and Bob answers by the guess, or by a fair coin when it is wrong. This is why sign rank describes the private-coin model.

**Lower bounds.** Forster (2002) proved that every $N \times M$ sign matrix $S$ has

$$\operatorname{rank}_\pm(S) \ge \frac{\sqrt{NM}}{\lVert S \rVert},$$

where $\lVert S \rVert$ is the spectral norm. The proof first moves the points $u_x$ by a linear map into a position where they are spread evenly in all directions (an isotropic position on the unit sphere), and then compares two estimates of $\sum_{x,y} |\langle u_x, v_y \rangle|$. The existence of the even position is the hard step and is not proved here. Before Forster, the only strong bounds were counting arguments: Alon, Frankl and Rödl (1985) showed that most $N \times N$ sign matrices have sign rank linear in $N$, without an explicit example.

**Relation to other measures.** The sign rank is at most the rank, and the gap can be exponential, as equality shows. Small [discrepancy](/discrepancy-method/) does not imply large sign rank: Buhrman, Vereshchagin and de Wolf (2007) and Sherstov (2007) found functions with unbounded-error cost $O(\log n)$ whose discrepancy is exponentially small under some distribution. In the other direction, large sign rank does imply small discrepancy under some distribution, because a protocol with a large advantage on every input is also an unbounded-error protocol.

## Examples

**Equality: sign rank at most 3.** Take $N$ distinct reals $a_x$ and let $A_{xy} = \tfrac12 - (a_x - a_y)^2 = (\tfrac12 - a_x^2) \cdot 1 + 2a_x \cdot a_y + (-1) \cdot a_y^2$. This is a sum of three rank-1 matrices. With integer $a_x$, $A_{xy} = 1/2 > 0$ when $x = y$ and $A_{xy} \le -1/2 < 0$ otherwise. A check with $N = 8$ and $a_x = x$ confirms that the signs match the $\pm 1$ equality matrix, whose ordinary rank is 8. So the unbounded-error cost of [equality](/equality-problem/) is $O(1)$.

**Greater-than: sign rank at most 2.** $A_{xy} = (x - \tfrac12) \cdot 1 + (-1) \cdot y = x - y - \tfrac12$ is positive exactly when $x > y$.

**Disjointness.** The unbounded-error cost of [disjointness](/disjointness-problem/) is $\log_2 n \pm O(1)$. For the upper bound, Alice picks a uniform random $i \in [n]$ with private coins and sends $i$ and $x_i$. Bob says "intersect" if $x_i = y_i = 1$, and otherwise he says "disjoint" with probability $p = n/(2n-1)$. On disjoint inputs he is right with probability $p > 1/2$. On inputs with $t \ge 1$ common elements he says "disjoint" with probability $(1 - t/n)\,p \le (n-1)/(2n-1) < 1/2$. A direct check for $n = 2, 3, 4, 5$ gives worst-case success $2/3$, $3/5$, $4/7$, $5/9$. Alice sends $\lceil \log_2 n \rceil + 1$ bits, and this one-way private-coin protocol is the whole cost. For the lower bound, restrict Alice to the $n$ singletons $\{i\}$. Every subset of these $n$ rows appears as the set of rows where some column $y$ is "disjoint", so in a realization by points and homogeneous halfspaces in $\mathbb{R}^d$ the $n$ points are shattered. Homogeneous halfspaces in $\mathbb{R}^d$ shatter at most $d$ points, so $d \ge n$. So $\operatorname{rank}_\pm(M_{\mathrm{DISJ}_n})$ is $\Theta(n)$.

**Inner product.** The sign matrix of $\mathrm{IP}_n$ is the Hadamard matrix $H_n$ with $N = 2^n$ and $\lVert H_n \rVert = 2^{n/2}$. Forster's bound gives $\operatorname{rank}_\pm(H_n) \ge 2^n / 2^{n/2} = 2^{n/2}$, so $U(\mathrm{IP}_n) \ge n/2 - O(1)$. For $n = 4$ the $16 \times 16$ matrix has rank 16 and sign rank at least 4. See [inner product problem](/inner-product-problem/).

**A function in $\mathsf{AC}^0$.** Razborov and Sherstov (2008, journal 2010) found a function computed by a depth-3 circuit of polynomial size whose communication matrix has sign rank $\exp(\Omega(n^{1/3}))$. This answered a question of Babai, Frankl and Simon (1986). Later work raised the exponent toward 1.

## Where it is used

- **Unbounded-error communication.** The class $\mathsf{UPP}^{cc}$ of functions with unbounded-error cost polylogarithmic in $n$ is exactly the class with sign rank $2^{\mathrm{polylog}(n)}$. The Razborov and Sherstov function shows that $\mathsf{AC}^0$ is not inside $\mathsf{UPP}^{cc}$.
- **Learning theory.** A concept class with sign rank $d$ embeds into homogeneous halfspaces in $\mathbb{R}^d$, so kernel methods, the [perceptron](/perceptron/) and [support vector machines](/support-vector-machine/) can learn it in dimension $d$. Large sign rank rules out such embeddings. Ben-David, Eiron and Simon (2003) showed that most classes of small [VC dimension](/vc-dimension/) still need large dimension. See [halfspace learning](/halfspace-learning/).
- **Threshold circuits.** If $f$ is a threshold gate $\operatorname{sign}(\sum_{i=1}^{s} w_i g_i - \theta)$ over $s$ functions $g_i(x, y)$ whose matrices have rank 1, then $\operatorname{rank}_\pm(M_f) \le s + 1$. So a lower bound on sign rank gives a lower bound on the number of gates below the top gate. Forster, Krause, Lokam, Mubarakzjanov, Schmitt and Simon (2001) used Forster's bound in this way for circuits that compute inner product. See [TC0](/tc0/).
- **Degree of polynomials.** Razborov and Sherstov bound sign rank through the threshold degree of a Boolean function and a pattern matrix construction in the style of Sherstov's pattern matrix method, which also turns [approximate degree](/approximate-degree/) into bounded-error communication bounds.

## References
