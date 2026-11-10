---
tag: 7MSDDZ
kind: definition
slug: asymptotic-ptas
name: Asymptotic polynomial-time approximation scheme (APTAS)
aliases:
- APTAS
- asymptotic approximation scheme
- AFPTAS
- asymptotic FPTAS
area: approximation/approximation-schemes
level: advanced
summary: An approximation scheme that guarantees (1+ε)·OPT + c(ε) and is only required to be near-optimal for large OPT, as in bin packing.
prereqs: [ptas, approximation-ratio, bin-packing]
see_also: [bin-packing-aptas, fernandez-de-la-vega-lueker-aptas, karmarkar-karp-bin-packing, bin-packing-inapproximability, ptas, fptas, edge-coloring, epstein-levin-eptas-bin-packing]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms, Cambridge University Press, 2011
    locator: Chapter 3, Section 3.3 (the bin packing problem and its asymptotic scheme)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer, 2001
    locator: Chapter 9 (Bin packing), the asymptotic PTAS
  - book: isbn:9783540654315
    title: Giorgio Ausiello, Pierluigi Crescenzi, Giorgio Gambosi, Viggo Kann, Alberto Marchetti-Spaccamela and Marco Protasi, Complexity and Approximation, Springer, 1999
    locator: Chapter 4 (asymptotic approximation)
  - title: W. Fernandez de la Vega and George S. Lueker, Bin packing can be solved within 1 + ε in linear time, Combinatorica 1(4), 1981
    locator: the asymptotic scheme with linear grouping
  - title: Narendra Karmarkar and Richard M. Karp, An efficient approximation scheme for the one-dimensional bin-packing problem, Proceedings of FOCS 1982
    locator: the bound OPT + O(log^2 OPT)
---

An asymptotic polynomial-time approximation scheme, or APTAS, is an approximation scheme whose guarantee $(1 + \varepsilon) \cdot \mathrm{OPT}$ may be broken by an additive term that does not grow with the instance. For a minimization problem it gives, for each $\varepsilon > 0$, a polynomial-time algorithm with $\mathrm{ALG} \le (1 + \varepsilon) \cdot \mathrm{OPT} + c(\varepsilon)$. So it is near-optimal in ratio only when the optimum is large. The standard example is [bin packing](/bin-packing/): no polynomial-time algorithm has an absolute ratio below $3/2$ unless P = NP, but the [bin packing APTAS](/bin-packing-aptas/) of Fernandez de la Vega and Lueker uses at most $(1 + \varepsilon)\mathrm{OPT} + 1$ bins. When the time is also polynomial in $1/\varepsilon$, the scheme is an AFPTAS, as for the [Karmarkar and Karp algorithm](/karmarkar-karp-bin-packing/). For problems that can be scaled by taking disjoint copies, an APTAS gives a PTAS, so the notion is new only for problems like bin packing and edge coloring, where small optima are special.

## Definition

Let $\Pi$ be a minimization problem in [NPO](/npo-class/). We use the conventions of [the approximation ratio](/approximation-ratio/) page, with the asymptotic ratio

$$
\rho_A^{\infty} = \lim_{k \to \infty} \ \sup_{I :\ \mathrm{OPT}(I) \ge k} \frac{\mathrm{ALG}(I)}{\mathrm{OPT}(I)}.
$$

An **asymptotic polynomial-time approximation scheme** for $\Pi$ is an algorithm that, on input an instance $I$ and a rational $\varepsilon > 0$, returns a feasible solution with

$$
\mathrm{ALG}(I, \varepsilon) \le (1 + \varepsilon) \cdot \mathrm{OPT}(I) + c(\varepsilon)
$$

for a function $c$ that does not depend on $I$, and runs in time polynomial in $|I|$ for each fixed $\varepsilon$. Its asymptotic ratio is then at most $1 + \varepsilon$ for each $\varepsilon$. For a maximization problem the bound is $\mathrm{ALG} \ge (1 - \varepsilon) \cdot \mathrm{OPT} - c(\varepsilon)$. The class **APTAS** is the set of problems that have one.

An **asymptotic fully polynomial-time approximation scheme** (AFPTAS) is an APTAS whose time is polynomial in $|I|$ and $1/\varepsilon$, and where $c(\varepsilon)$ is bounded by a polynomial in $1/\varepsilon$.

Notes on the definition:

- **The additive term.** Williamson and Shmoys, and many papers, ask for a constant $c$ that does not depend on $\varepsilon$; the bin packing APTAS has $c = 1$. Ausiello et al. define the class by the asymptotic ratio alone, which allows $c(\varepsilon)$. The examples on this page meet the stronger form where it is stated.
- **Why it is weaker than a PTAS.** At $\mathrm{OPT} = 2$, the bound $(1 + \varepsilon) \cdot 2 + 1 = 3 + 2\varepsilon$ allows 3 bins, so an APTAS for bin packing does not contradict the $3/2$ hardness. At $\mathrm{OPT} = 100$ and $\varepsilon = 0.1$, it allows 111 bins, a ratio of $1.11$. The additive term matters only when the optimum is small.
- **PTAS implies APTAS.** A PTAS is an APTAS with $c = 0$. The converse fails for bin packing.

**Lemma (scaling).** Let $\Pi$ be a minimization problem with integer values and $\mathrm{OPT}(I) \ge 1$ for each instance. Suppose that for each instance $I$ and integer $k \ge 1$ there is an instance $I^{(k)}$, computable in time polynomial in $|I|$ and $k$, with $\mathrm{OPT}(I^{(k)}) = k \cdot \mathrm{OPT}(I)$, and that each solution $S$ of $I^{(k)}$ gives, in polynomial time, a solution of $I$ of value at most $c(S) / k$. Then an APTAS for $\Pi$ gives a PTAS for $\Pi$.

*Proof.* Given $I$ and $\varepsilon$, let $c = c(\varepsilon / 2)$ and $k = \lceil 2c / \varepsilon \rceil$, a constant for fixed $\varepsilon$. Run the APTAS with $\varepsilon / 2$ on $I^{(k)}$. It returns $S$ with $c(S) \le (1 + \varepsilon / 2) \, k \, \mathrm{OPT}(I) + c$. The solution of $I$ that $S$ gives has value at most

$$
\frac{c(S)}{k} \le \Big(1 + \frac{\varepsilon}{2}\Big)\mathrm{OPT}(I) + \frac{c}{k} \le \Big(1 + \frac{\varepsilon}{2}\Big)\mathrm{OPT}(I) + \frac{\varepsilon}{2} \le (1 + \varepsilon)\,\mathrm{OPT}(I),
$$

since $\mathrm{OPT}(I) \ge 1$. The time is polynomial in $|I|$ for each fixed $\varepsilon$. $\square$

For the maximization form, the same proof works with the bound turned around.

## Examples and non-examples

**Bin packing (an APTAS and an AFPTAS).** The [bin packing APTAS](/bin-packing-aptas/) of [Fernandez de la Vega and Lueker](/fernandez-de-la-vega-lueker-aptas/) (1981) sets aside the items of size below a threshold of order $\varepsilon$ and adds them greedily at the end, rounds the large sizes up by linear grouping to $O(1/\varepsilon^2)$ distinct sizes, and packs the rounded instance optimally by enumeration or an LP. It uses at most $(1 + \varepsilon)\mathrm{OPT} + 1$ bins. The [Karmarkar and Karp algorithm](/karmarkar-karp-bin-packing/) (1982) uses at most $\mathrm{OPT} + O(\log^2 \mathrm{OPT})$ bins in polynomial time, and its variant with accuracy $\varepsilon$ is an AFPTAS with $c(\varepsilon) = O(1/\varepsilon^2)$. Hoberg and Rothvoss later improved the additive term to $O(\log \mathrm{OPT})$. An efficient form of the asymptotic scheme is on the page [Epstein and Levin EPTAS for bin packing](/epstein-levin-eptas-bin-packing/).

**Bin packing: why the scaling lemma fails.** Take $I = \{1/2\}$, with $\mathrm{OPT}(I) = 1$. Two disjoint copies are the instance $\{1/2, 1/2\}$, which fits in one bin, so $\mathrm{OPT}(I^{(2)}) = 1 \ne 2$. Items from different copies can share a bin, so no copy construction multiplies the optimum. This is why bin packing has an APTAS but, if P ≠ NP, no PTAS: the absolute ratio is at least $3/2$, by the reduction from [partition](/partition-problem/) on the [PTAS](/ptas/) page. See also [bin packing inapproximability](/bin-packing-inapproximability/).

**Edge coloring (an additive guarantee).** By [Vizing's theorem](/vizing-theorem/), the edges of a simple graph of largest degree $\Delta$ can be colored with $\Delta + 1$ colors in polynomial time, and $\mathrm{OPT} \ge \Delta$. So $\mathrm{ALG} \le \mathrm{OPT} + 1 \le (1 + \varepsilon)\mathrm{OPT} + 1$ for every $\varepsilon$, which is an APTAS, and the asymptotic ratio is exactly 1. But deciding whether $\Delta = 3$ colors suffice for a cubic graph is NP-complete (Holyer 1981), so no algorithm has an absolute ratio below $4/3$ unless P = NP. Disjoint copies of a graph have the same chromatic index as one copy, so the scaling lemma does not apply. See [edge coloring](/edge-coloring/).

**Vertex cover (no APTAS if P ≠ NP).** For minimum [vertex cover](/vertex-cover/), let $I^{(k)}$ be $k$ disjoint copies of the graph. Then $\mathrm{OPT}(I^{(k)}) = k \cdot \mathrm{OPT}(I)$, and the copy with the smallest part of a cover $S$ gives a cover of $I$ of size at most $|S| / k$. Graphs with no edges have $\mathrm{OPT} = 0$, but they are solved exactly at once, so the lemma applies to the others. An APTAS would give a PTAS. Vertex cover is [APX-hard](/apx-completeness/), so it has no APTAS unless P = NP. The same argument works for max 3SAT (copies with disjoint variables) and for maximum independent set.

**Non-example: two-dimensional bin packing.** Packing rectangles into unit squares, with no rotation, has no APTAS unless P = NP (Bansal, Correa, Kenyon and Sviridenko, 2006). So the step from one to two dimensions loses the asymptotic scheme.

**Non-example: an algorithm with an asymptotic ratio above 1.** Next fit for bin packing uses at most $2 \cdot \mathrm{OPT} - 1$ bins, and the instances with $4N$ items alternating between $1/2$ and $1/(2N)$ need $2N$ bins against $\mathrm{OPT} = N + 1$ (see the [approximation ratio](/approximation-ratio/) page). Its asymptotic ratio is 2, so it is not part of a scheme.

## Related definitions

- **PTAS and FPTAS.** A [PTAS](/ptas/) is an APTAS with $c = 0$, and an [FPTAS](/fptas/) is an AFPTAS with $c = 0$.
- **Absolute and asymptotic ratios.** The two notions of ratio, and the additive guarantees, are defined on the [approximation ratio](/approximation-ratio/) page.
- **APX.** [APX](/apx/) uses the absolute ratio. A problem can be in APTAS and still have no PTAS, as bin packing shows.
- **Rounding.** Asymptotic schemes for packing problems use [rounding and scaling](/rounding-and-scaling/) of the item sizes, in the form of linear grouping, and LPs over configurations such as the [configuration LP](/configuration-lp/).

## References
