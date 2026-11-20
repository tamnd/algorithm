---
title: The Ewald split gives the periodic Coulomb energy, and the code computes its truncated sums and their exact gradient
proves: [correctness]
status: full
---

We use Gaussian units and the line numbers of the pseudocode. There are $N$ point charges $q_i$ at $r_i$ in a cubic box of side $L$ and volume $V = L^3$, with $\sum_i q_i = 0$. Write $r_{ij} = r_i - r_j$, and let $\sum'_n$ be the sum over integer vectors $n$ that leaves out $n = 0$ when $i = j$. The periodic Coulomb energy is
$$E = \frac12 \sum_{i, j} {\sum_n}' \frac{q_i q_j}{|r_{ij} + nL|}.$$
This series converges only conditionally, so its value depends on the order of summation. We take the limit of sums over growing spheres of images, as in de Leeuw, Perram and Smith (1980).

**Claim 1 (the split).** For each $\alpha > 0$ and $r > 0$, $\frac{1}{r} = \frac{\operatorname{erfc}(\alpha r)}{r} + \frac{\operatorname{erf}(\alpha r)}{r}$, and $\operatorname{erf}(\alpha r)/r$ is the potential at distance $r$ of a unit charge spread as the Gaussian $\rho_\alpha(s) = (\alpha / \sqrt{\pi})^3 e^{-\alpha^2 s^2}$.

*Proof.* The first part holds because $\operatorname{erf} + \operatorname{erfc} = 1$. For the second, Gauss's law says that the field of a spherical charge at distance $r$ is the charge inside radius $r$ divided by $r^2$. The charge of $\rho_\alpha$ inside radius $r$ is $\operatorname{erf}(\alpha r) - \frac{2 \alpha r}{\sqrt\pi} e^{-\alpha^2 r^2}$, and this is $r^2$ times $-\frac{d}{dr}\bigl(\operatorname{erf}(\alpha r)/r\bigr)$. Both potentials go to 0 as $r \to \infty$, so they are equal. $\square$

**Claim 2 (the four parts).** In the limit of spheres, $E = E_{\text{real}} + E_{\text{rec}} + E_{\text{self}} + E_{\text{surf}}$ with
$$E_{\text{real}} = \frac12 \sum_{i, j} {\sum_n}' q_i q_j \frac{\operatorname{erfc}(\alpha |r_{ij} + nL|)}{|r_{ij} + nL|}, \qquad E_{\text{rec}} = \frac{2\pi}{V} \sum_{k \ne 0} \frac{e^{-k^2 / 4\alpha^2}}{k^2} |S(k)|^2,$$
$S(k) = \sum_j q_j e^{i k \cdot r_j}$, $k = 2\pi m / L$ for integer vectors $m$, $E_{\text{self}} = -\frac{\alpha}{\sqrt\pi} \sum_i q_i^2$ and $E_{\text{surf}} = \frac{2\pi}{3V} \bigl|\sum_i q_i r_i\bigr|^2$.

*Proof.* Split each term of $E$ by Claim 1. The erfc part decays faster than any power, so it converges absolutely, in any order, to $E_{\text{real}}$. For the erf part, add the missing terms $i = j$, $n = 0$, whose value is the limit $\operatorname{erf}(\alpha r)/r \to 2\alpha / \sqrt\pi$ as $r \to 0$. With the factor $\frac12$ they add $\frac{\alpha}{\sqrt\pi} \sum_i q_i^2$, which $E_{\text{self}}$ takes away again. The full smooth sum is $\frac12 \sum_{i,j} q_i q_j \phi(r_{ij})$, where $\phi(r) = \sum_n \operatorname{erf}(\alpha |r + nL|)/|r + nL|$ is the potential of a periodic lattice of Gaussians. The sum over $n$ diverges for one pair, but the sum weighted by $q_i q_j$ converges for a neutral system, and an additive constant in $\phi$ cancels because $\sum_{i,j} q_i q_j = 0$. The density is smooth and periodic, with Fourier coefficients $e^{-k^2/4\alpha^2}/V$, and the Poisson equation $\nabla^2 \phi = -4\pi \rho$ gives the coefficients $\frac{4\pi}{V k^2} e^{-k^2/4\alpha^2}$ for $k \ne 0$. The $k = 0$ term is where the order of summation enters: for a neutral system it is $0$ with conducting (tin foil) surroundings, and for a sphere of images in a vacuum it is the dipole term $E_{\text{surf}}$, by the analysis of de Leeuw, Perram and Smith (1980), which we do not repeat. Then
$$\frac12 \sum_{i,j} q_i q_j \sum_{k \ne 0} \frac{4\pi}{V k^2} e^{-k^2/4\alpha^2} e^{i k \cdot r_{ij}} = \frac{2\pi}{V} \sum_{k \ne 0} \frac{e^{-k^2/4\alpha^2}}{k^2} S(k) \overline{S(k)},$$
which is $E_{\text{rec}}$. $\square$

So the sum of the four parts does not depend on $\alpha$. The test checks this to $10^{-8}$.

**Claim 3 (the code computes the truncated parts).** Lines L2 and L3 compute $E_{\text{real}}$ over the images with $|r_{ij} + nL| < r_c$. Lines L5 to L7 compute $E_{\text{rec}}$ over $0 < |m| \le m_{\max}$. Lines L9 and L10 compute $E_{\text{self}}$ and $E_{\text{surf}}$.

*Proof.* The double sum over ordered pairs $(i, j)$ is twice the sum over $i < j$, so the factor $\frac12$ goes away for $i \ne j$ and stays for $i = j$, as in line L3. The images of $r_{ij}$ are the same for every representative of $r_{ij}$ modulo $L$, so the code may first take the minimum image and then visit all shifts with $|n_a| \le \lceil r_c / L \rceil + 1$, which include every image closer than $r_c$. In line L7, $S(-k) = \overline{S(k)}$, so the terms for $m$ and $-m$ are equal. The code visits one $m$ of each pair, the ones after $(0, 0, 0)$ in lexicographic order, and doubles the term. $\square$

**Claim 4 (the forces are the exact gradient).** For fixed sets of images and wave vectors, lines L4, L8 and L10 give $f_i = -\nabla_{r_i}$ of the computed energy.

*Proof.* For $u(r) = q_i q_j \operatorname{erfc}(\alpha r)/r$, $-u'(r) = q_i q_j \bigl(\operatorname{erfc}(\alpha r)/r^2 + \frac{2\alpha}{\sqrt\pi} e^{-\alpha^2 r^2}/r\bigr)$, and the force on $i$ is $-u'(r) \, d / r$ with $d = r_{ij} + nL$. This is the factor $g$ of line L4, which adds it to $f_i$ and subtracts it from $f_j$. Terms with $i = j$ do not depend on $r_i$. For line L8, $\nabla_{r_i} |S|^2 = 2 \operatorname{Re}\bigl(i k q_i e^{i k \cdot r_i} \overline{S}\bigr) = -2 q_i k \operatorname{Im}\bigl(e^{i k \cdot r_i} \overline{S}\bigr)$, and $\operatorname{Im}(e^{i\theta} \overline{S}) = \sin\theta \operatorname{Re} S - \cos\theta \operatorname{Im} S$. Multiplying by $-\frac{2\pi}{V} \frac{e^{-k^2/4\alpha^2}}{k^2}$ gives the force of line L8, doubled for the pair $\pm m$. For line L10, $-\nabla_{r_i} \frac{2\pi}{3V} |M|^2 = -\frac{4\pi}{3V} q_i M$ with $M = \sum_j q_j r_j$. $\square$

The test checks Claim 4 against central differences of the energy. The energy as a function of the positions jumps when an image crosses the sphere of radius $r_c$, by at most $|q_i q_j| \operatorname{erfc}(\alpha r_c) / r_c$, so Claim 4 holds between such crossings.

**Claim 5 (truncation error, heuristic).** Each omitted real-space term is at most $|q_i q_j| \operatorname{erfc}(\alpha r_c)/r_c \le |q_i q_j| e^{-\alpha^2 r_c^2} / (\sqrt\pi \alpha r_c^2)$, and each omitted reciprocal term is at most $\frac{2\pi}{V} \frac{e^{-k_c^2/4\alpha^2}}{k_c^2} \bigl(\sum_j |q_j|\bigr)^2$ with $k_c = 2\pi m_{\max} / L$.

*Proof.* The bound $\operatorname{erfc}(x) \le e^{-x^2} / (\sqrt\pi x)$ for $x > 0$ follows from $\int_x^\infty e^{-t^2} dt \le \int_x^\infty \frac{t}{x} e^{-t^2} dt$. The second bound uses $|S(k)| \le \sum_j |q_j|$ and that $e^{-k^2/4\alpha^2}/k^2$ falls with $k$. $\square$

The number of omitted terms grows only like a power of $r_c$ and $k_c$, so with $s = \alpha r_c = k_c / (2\alpha)$ both tails are $e^{-s^2}$ times a factor that changes slowly. This is a heuristic for the size of the error, not a bound on the sum of the tails. Sharper estimates, with the constants, are in Kolafa and Perram (1992).

**Claim 6 (cost).** Take $s$ fixed and $\alpha$ free. At a fixed density $N / V$, the real-space part costs $\Theta(N r_c^3 N / V) = \Theta(N^2 s^3 / (\alpha^3 V))$ with a cell list, and the reciprocal part costs $\Theta(N k_c^3 V) = \Theta(N s^3 \alpha^3 V)$. The sum is smallest for $\alpha^3 V = \Theta(\sqrt N)$, that is, $\alpha \propto N^{1/6} / V^{1/3}$, and then both parts cost $\Theta(N^{3/2})$.

*Proof.* Each charge meets about $\frac{4\pi}{3} r_c^3 N / V$ charges inside $r_c$, and there are about $\frac{4\pi}{3} (k_c L / 2\pi)^3 = \Theta(k_c^3 V)$ wave vectors, each costing $\Theta(N)$. The product of the two costs is $\Theta(N^3 s^6)$, which does not depend on $\alpha$, so their sum is smallest when they are equal, at $\Theta(N^{3/2} s^3)$. $\square$

The implementation does not use a cell list: its real-space loop visits all pairs, so its cost is $\Theta(N^2)$ for the real part.
