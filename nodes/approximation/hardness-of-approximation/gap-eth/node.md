---
tag: JEWX8G
kind: concept
slug: gap-eth
name: Gap-ETH
aliases:
- Gap Exponential Time Hypothesis
- gap exponential time hypothesis for 3-SAT
area: approximation/hardness-of-approximation
level: research
summary: The hypothesis that telling satisfiable 3-SAT formulas from those where a constant fraction of clauses must fail needs time 2^Ω(n). It gives tight parameterized hardness of approximation.
prereqs: [3-sat, pcp-theorem, gap-problem, label-cover]
see_also: [parameterized-inapproximability, fpt-approximation, clique-inapproximability, dominating-set-inapproximability, k-median-inapproximability, gap-amplification, fine-grained-reduction, max-3sat-inapproximability]
sources:
  - paper: "I. Dinur, Mildly exponential reduction from gap 3SAT to polynomial-gap label-cover, Electronic Colloquium on Computational Complexity, TR16-128, 2016"
    locator: the statement of the hypothesis and the reduction to label cover with a polynomial gap
  - paper: doi:10.4230/LIPIcs.ICALP.2017.78
    title: P. Manurangsi and P. Raghavendra, A birthday repetition theorem and complexity of approximating dense CSPs, ICALP 2017
    locator: the independent statement of the hypothesis and its use for dense constraint satisfaction
  - paper: doi:10.1109/FOCS.2017.74
    title: P. Chalermsook, M. Cygan, G. Kortsarz, B. Laekhanukit, P. Manurangsi, D. Nanongkai and L. Trevisan, From Gap-ETH to FPT-inapproximability, clique, dominating set, and more, FOCS 2017
    locator: no FPT algorithm with ratio o(k) for clique and none with any ratio f(k) for dominating set under Gap-ETH
  - paper: doi:10.1006/jcss.2000.1727
    title: R. Impagliazzo and R. Paturi, On the complexity of k-SAT, Journal of Computer and System Sciences 62(2), 2001
    locator: the exponential time hypothesis
  - paper: doi:10.1145/1236457.1236459
    title: Irit Dinur, The PCP theorem by gap amplification, Journal of the ACM 54(3), 2007
    locator: the PCP of quasi-linear size, from a short PCP and gap amplification
  - paper: "B. Applebaum, Exponentially-hard gap-CSP and local PRG via local hardcore functions, FOCS 2017"
    locator: gap versions of the hypothesis from assumptions on local pseudorandom generators
---

The Gap Exponential Time Hypothesis (Gap-ETH) says that there is a constant $\delta > 0$ such that no algorithm in time $2^{o(n)}$ can tell satisfiable [3-SAT](/3-sat/) formulas on $n$ variables from formulas in which every assignment leaves at least a $\delta$ fraction of the clauses false. Dinur (2016) and Manurangsi and Raghavendra (2017) stated it independently. It joins two ideas: the exponential time hypothesis of Impagliazzo and Paturi, which says that exact 3-SAT needs time $2^{\Omega(n)}$, and the [PCP theorem](/pcp-theorem/), which makes the gap problem NP-hard. The PCP theorem alone loses a polylogarithmic factor in the size, and Gap-ETH is the assumption that this loss is not needed. Its main use is in [parameterized inapproximability](/parameterized-inapproximability/), where it gave the first tight results for clique and dominating set.

## In plain words

Some problems seem to need about $2^n$ steps, where $n$ is the number of yes or no choices. The exponential time hypothesis says that 3-SAT is one of them: no method is much faster than trying a large share of all choices.

Gap-ETH says more. Even when the formula is far from satisfiable, so that every setting of the variables breaks a fixed share of the clauses, it is still this hard to tell that formula from a satisfiable one. A rough check should not be easier than an exact one.

This matters because many approximation results start from such a gap. With the usual tools, the gap version is only known to be as hard as the exact version on a slightly larger formula, and the size loss weakens the conclusions. Gap-ETH removes that loss, so the time bounds come out exact.

## The idea

**The hypotheses.** Let $\varphi$ be a 3-CNF formula with $n$ variables and $m = O(n)$ clauses, and let $\mathrm{sat}(\varphi)$ be the largest fraction of clauses that one assignment satisfies.

- **ETH** (Impagliazzo and Paturi 2001). There is $\varepsilon > 0$ such that no algorithm decides whether $\mathrm{sat}(\varphi) = 1$ in time $O(2^{\varepsilon n})$.
- **Gap-ETH.** There are $\varepsilon, \delta > 0$ such that no algorithm in time $O(2^{\varepsilon n})$ tells $\mathrm{sat}(\varphi) = 1$ from $\mathrm{sat}(\varphi) \le 1 - \delta$. The algorithm may answer anything on formulas with $1 - \delta < \mathrm{sat}(\varphi) < 1$.
- **Randomized Gap-ETH.** The same for randomized algorithms with bounded error. Several applications use randomized reductions and need this form.

**Gap-ETH implies ETH.** An algorithm that decides satisfiability also tells the two cases apart, with the same running time. So a $2^{o(n)}$ algorithm for exact 3-SAT would refute Gap-ETH. The reverse is not known.

**What ETH gives without the hypothesis.** The PCP theorem in the form of Dinur (2007), built on short PCPs of Ben-Sasson and Sudan, maps a 3-SAT formula on $n$ variables, in polynomial time, to a 3-SAT formula on $N = n (\log n)^{c}$ variables, for a constant $c$, that is satisfiable if $\varphi$ is and has $\mathrm{sat} \le 1 - \delta$ if $\varphi$ is not. Suppose the gap problem could be solved in time $2^{o(N / (\log N)^{c})}$. Since $\log N = (1 + o(1)) \log n$, we get $N / (\log N)^{c} = (1 + o(1)) n$, so exact 3-SAT would be solved in time $2^{o(n)}$, against ETH. So ETH already implies that the gap problem needs time $2^{N / (\log N)^{c + o(1)}}$. Gap-ETH is the claim that the factor $(\log N)^{c}$ can be removed. A PCP of linear size with a constant gap would prove that ETH implies Gap-ETH, but none is known.

**Moving the gap to other problems.** Gap-ETH is useful because a gap survives reductions of linear size. Let $\varphi$ have each variable in at most a constant number of clauses. The clause and variable game of [label cover](/label-cover/) has one left vertex per clause and one right vertex per variable, with left labels the 7 satisfying assignments of a clause and right labels $\{0, 1\}$. Its value is exactly $1 - \frac{1 - \mathrm{sat}(\varphi)}{3}$, which is proved on the label cover page. So the gap 1 against $1 - \delta$ becomes 1 against $1 - \frac{\delta}{3}$, on $m + n = O(n)$ vertices. Under Gap-ETH, this label cover gap needs time $2^{\Omega(n)}$.

**From exponential time to parameterized time.** Split the $n$ variables into $k$ blocks of $n / k$ variables, and make a constraint problem with one variable per block. Its alphabet is the set of assignments of a block, of size $N = 2^{n / k}$. An algorithm in time $N^{o(k)}$ on such instances runs in time $2^{(n / k) \cdot o(k)} = 2^{o(n)}$. Chalermsook et al. (2017) build such instances so that the gap survives the grouping. Then Gap-ETH implies that the $k$-variable gap problem has no algorithm in time $f(k) \cdot N^{o(k)}$ for any function $f$. Clique and dominating set reductions start from here.

**Pitfalls.**

- Gap-ETH is a statement about running time, not about polynomial time. A reduction that blows the size up from $n$ to $n^2$ turns a $2^{\varepsilon n}$ bound into only $2^{\varepsilon \sqrt{N}}$. Results under Gap-ETH need reductions of linear size, or careful accounting.
- The hypothesis needs perfect completeness on one side. The version with $1 - \delta_1$ against $1 - \delta_2$ is a different statement, and some applications need the perfect form.
- Many results first proved under Gap-ETH were later proved under ETH or under W[1] $\ne$ FPT. Lin (2021) showed that constant-ratio approximation of $k$-clique is W[1]-hard, which removed Gap-ETH from one of its main applications.

## Examples

**A formula family with a gap.** The 8 clauses on three variables $x, y, z$ with all sign patterns are not satisfiable together: each assignment makes exactly one of them false, the one whose literals are all the opposite of the assignment. So $\mathrm{sat} = \frac78$. Taking $t$ disjoint copies gives $n = 3 t$ variables, $m = 8 t$ clauses and $\mathrm{sat} = \frac78$, so $\delta = \frac18$. This family is easy to recognize, so it is no evidence for Gap-ETH, but it shows the size of gap the hypothesis talks about. The clause and variable game of one copy has value $1 - \frac{1/8}{3} = \frac{23}{24}$, as computed on the [label cover](/label-cover/) page.

**The size loss of the PCP route.** For $n = 2^{20}$ variables and the polylogarithmic factor $(\log_2 n)^{c}$ with $c = 2$, the PCP formula has $N = 400 n$ variables. A lower bound of $2^{\varepsilon n}$ for the original formula gives only $2^{\varepsilon N / 400}$ for the gap formula, and the factor 400 grows with $n$. Gap-ETH says that the gap formula itself needs $2^{\varepsilon' N}$. The value $c = 2$ is chosen to show the effect; the constant of the known PCPs is larger.

**Block grouping.** With $n = 3000$ variables and $k = 10$ blocks, each block variable has $2^{300}$ values. Gap-ETH with the constant $\varepsilon$ rules out time $2^{\varepsilon n} = (2^{300})^{10 \varepsilon}$, that is, time $N^{\varepsilon k}$ for this $k$. This is why the parameterized bounds have the form $N^{o(k)}$ and not a fixed power of $N$.

## Where it is used

- **Clique.** Under Gap-ETH, no algorithm in time $f(k) \cdot n^{O(1)}$ finds a clique of size $k / \rho(k)$ in a graph with a $k$-clique for any $\rho(k) = o(k)$ (Chalermsook et al. 2017). See [clique inapproximability](/clique-inapproximability/) for the polynomial-time bounds.
- **Dominating set and set cover.** Under Gap-ETH, no algorithm in time $f(k) \cdot n^{O(1)}$ approximates $k$-dominating set within any ratio $g(k)$ (Chalermsook et al. 2017). See [dominating set inapproximability](/dominating-set-inapproximability/).
- **$k$-median and $k$-means in FPT time.** Under Gap-ETH, the ratio $1 + \frac{2}{e}$ for $k$-median, reached in time $f(k) \cdot n^{O(1)}$, is the best possible in that time (Cohen-Addad et al. 2019); see [k-median inapproximability](/k-median-inapproximability/).
- **Dense constraint problems.** Manurangsi and Raghavendra (2017) used it, with a birthday repetition theorem, for running-time lower bounds on approximating dense 2-CSPs.
- **Label cover with a polynomial gap.** Dinur (2016) gave a reduction, in mildly exponential time, from gap 3-SAT to label cover with a gap that is polynomial in the size. Under Gap-ETH, this gives running-time lower bounds for label cover with such large gaps.

## References
