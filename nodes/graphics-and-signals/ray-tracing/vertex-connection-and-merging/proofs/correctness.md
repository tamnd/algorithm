---
title: The recursive quantities give the balance heuristic weights of every technique, and the furnace has the exact answer Le times the sum of the powers of rho
proves: [correctness]
status: full
---

Let $\bar x = x_0 x_1 \dots x_k$ be a path from a point $x_0$ on a light to the camera $x_k$. The camera measures the radiance along one ray, so $x_{k-1}$ is always sampled by the camera, and its camera factor is common to all the techniques and is left out.

**Notation.** At the vertex $x_i$ let $c_i^-$ and $c_i^+$ be the cosines of the edges to $x_{i-1}$ and $x_{i+1}$, let $\phi_i$ be the solid angle pdf of the direction to $x_{i+1}$ given the direction to $x_{i-1}$, and let $\rho_i$ be the pdf of the direction to $x_{i-1}$ given the direction to $x_{i+1}$. Let $d_i^2$ be the squared length of the edge $x_i x_{i+1}$. The emitter samples $x_0$ with the area pdf $p_A$, for emission and for next event estimation, and the direction with the pdf $\phi_0$. The area pdfs are

$$\overrightarrow{p}_0 = p_A, \qquad \overrightarrow{p}_i = \frac{\phi_{i-1}\, c_i^-}{d_{i-1}^2} \ (i \ge 1), \qquad \overleftarrow{p}_i = \frac{\rho_{i+1}\, c_i^+}{d_i^2} \ (i \le k - 2).$$

The connection technique $s \in \{0, \dots, k - 1\}$ uses the light vertices $x_0 \dots x_{s-1}$ and has $p_{\mathrm{VC}}(s) = \prod_{i<s}\overrightarrow{p}_i \prod_{i=s}^{k-2}\overleftarrow{p}_i$. Here $s = 0$ is an emitter hit and $s = 1$ is next event estimation. The merge at $x_s$, $s \in \{1, \dots, k - 1\}$, has the counted pdf $\eta\, \overrightarrow{p}_s\, p_{\mathrm{VC}}(s)$. Let $D$ be the sum of all these pdfs. The balance heuristic weight of a technique is its counted pdf divided by $D$, so the weights of one path sum to 1.

**Light side sums.** For $m \ge 0$ let $r_i = \overleftarrow{p}_i/\overrightarrow{p}_i$ and let $A_m$ be the sum of the counted pdfs of the techniques that use at most $m + 1$ light vertices, without the connection $s = m + 1$, divided by $p_{\mathrm{VC}}(m + 1)$:

$$A_m = \sum_{j=0}^{m} \prod_{i=j}^{m} r_i + \eta \sum_{j=1}^{m} \overrightarrow{p}_j \prod_{i=j}^{m} r_i .$$

This uses $p_{\mathrm{VC}}(j)/p_{\mathrm{VC}}(m+1) = \prod_{i=j}^{m} r_i$. Taking out the factor $r_m$ gives, with $A_{-1} = 0$,

$$A_m = r_m\big(1 + \eta\, \overrightarrow{p}_m [m \ge 1] + A_{m-1}\big). \tag{1}$$

**Lemma 1 (light subpath).** The light state stored at $x_m$, $m \ge 1$, has $\mathrm{dVCM}_m = 1/\overrightarrow{p}_m$ and $\mathrm{dVC}_m = A_{m-1}/(\rho_m \overrightarrow{p}_m)$. If $\eta > 0$, then $\mathrm{dVM}_m = \mathrm{dVC}_m/\eta$.

The right side of the second identity does not depend on $x_{m+1}$, because $A_{m-1}$ has the factor $r_{m-1}$, which has the factor $\rho_m$.

*Proof.* By induction on $m$. The emission state is $(p_A/(p_A\phi_0),\ c_0^+/(p_A\phi_0),\ c_0^+/(p_A \phi_0 \eta))$, and the hit at $x_1$ multiplies the first by $d_0^2/c_1^-$ and divides the others by $c_1^-$. So $\mathrm{dVCM}_1 = d_0^2/(\phi_0 c_1^-) = 1/\overrightarrow{p}_1$, and

$$\mathrm{dVC}_1 = \frac{c_0^+}{p_A \phi_0 c_1^-} = \frac{1}{\rho_1 \overrightarrow{p}_1}\cdot\frac{\rho_1 c_0^+}{d_0^2 p_A} = \frac{r_0}{\rho_1 \overrightarrow{p}_1} = \frac{A_0}{\rho_1 \overrightarrow{p}_1}.$$

For the step from $m$ to $m + 1$, the scatter at $x_m$ uses $\phi_m$, $\rho_m$ and $c_m^+$, and the hit at $x_{m+1}$ uses $d_m^2$ and $c_{m+1}^-$. So $\mathrm{dVCM}_{m+1} = d_m^2/(\phi_m c_{m+1}^-) = 1/\overrightarrow{p}_{m+1}$ and, by the hypothesis,

$$\mathrm{dVC}_{m+1} = \frac{c_m^+}{\phi_m c_{m+1}^-}\left(\frac{A_{m-1}}{\overrightarrow{p}_m} + \frac{1}{\overrightarrow{p}_m} + \eta\right) = \frac{c_m^+}{\phi_m c_{m+1}^- \overrightarrow{p}_m}\big(1 + \eta\overrightarrow{p}_m + A_{m-1}\big).$$

By (1), $A_m/(\rho_{m+1}\overrightarrow{p}_{m+1}) = \frac{\rho_{m+1} c_m^+}{d_m^2 \overrightarrow{p}_m}\cdot\frac{d_m^2}{\rho_{m+1}\phi_m c_{m+1}^-}(1 + \eta\overrightarrow{p}_m + A_{m-1})$, which is the same. The update of dVM is the update of dVC divided by $\eta$ term by term, with $\mathrm{dVCM}/\eta$ for $\mathrm{dVCM}$ and $1$ for $\eta$, so $\mathrm{dVM} = \mathrm{dVC}/\eta$ holds after every step if it holds at the emission, which it does. $\square$

**Camera side sums.** Let $q_i = \overrightarrow{p}_i/\overleftarrow{p}_i$ and, for $0 \le s \le k - 1$, let $B_s$ be the sum of the counted pdfs of the techniques that use more than $s$ light vertices, together with the merge at $x_s$, divided by $p_{\mathrm{VC}}(s)$:

$$B_s = \sum_{j=s+1}^{k-1}\prod_{i=s}^{j-1} q_i + \eta \sum_{j=s}^{k-1}\overrightarrow{p}_j\prod_{i=s}^{j-1} q_i .$$

Then $B_{k-1} = \eta\overrightarrow{p}_{k-1}$, and for $s \le k - 2$, taking out the factor $q_s$ from all the terms with $j > s$,

$$B_s = \eta\overrightarrow{p}_s + q_s\big(1 + B_{s+1}\big). \tag{2}$$

**Lemma 2 (camera subpath).** The camera state at $x_{k-1}$ is $(0, 0, 0)$. For $s \le k - 2$ the camera state at $x_s$ has $\mathrm{dVCM}_s = 1/\overleftarrow{p}_s$ and $\mathrm{dVC}_s = B_{s+1}/(\phi_s\overleftarrow{p}_s)$, and $\mathrm{dVM}_s = \mathrm{dVC}_s/\eta$ if $\eta > 0$. In all cases

$$B_s = \overrightarrow{p}_s\big(\eta + \mathrm{dVCM}_s + \mathrm{dVC}_s\,\phi_s\big). \tag{3}$$

*Proof.* The camera starts at 0 and the hit at $x_{k-1}$ keeps 0, so (3) gives $B_{k-1} = \eta\overrightarrow{p}_{k-1}$. For $s = k - 2$, the scatter at $x_{k-1}$ samples the direction to $x_{k-2}$ with the pdf $\rho_{k-1}$, and its reverse pdf is $\phi_{k-1}$. So $\mathrm{dVCM}_{k-2} = d_{k-2}^2/(\rho_{k-1} c_{k-2}^+) = 1/\overleftarrow{p}_{k-2}$ and $\mathrm{dVC}_{k-2} = \frac{c_{k-1}^-}{\rho_{k-1} c_{k-2}^+}\,\eta$. Then $\mathrm{dVC}_{k-2}\phi_{k-2}\overleftarrow{p}_{k-2} = \eta\,\frac{\phi_{k-2} c_{k-1}^-}{d_{k-2}^2} = \eta\overrightarrow{p}_{k-1} = B_{k-1}$. The general step is the computation of Lemma 1 with the roles of $\phi$ and $\rho$, and of $\overrightarrow{p}$ and $\overleftarrow{p}$, exchanged, and with (2) in place of (1). Then (3) follows from (2): $\overrightarrow{p}_s(\eta + 1/\overleftarrow{p}_s + B_{s+1}/\overleftarrow{p}_s) = \eta\overrightarrow{p}_s + q_s(1 + B_{s+1})$. $\square$

**Theorem 1 (the weights).** The functions of the implementation return the balance heuristic weights:

- the connection of the light vertex $x_{s-1}$ to the camera vertex $x_s$, $2 \le s \le k - 1$: $1/(1 + A_{s-1} + B_s)$;
- next event estimation at $x_1$: $1/(1 + A_0 + B_1)$;
- the emitter hit at $x_0$: $1/(1 + B_0 - \eta\overrightarrow{p}_0)$;
- the merge at $x_s$, $1 \le s \le k - 1$: $\eta\overrightarrow{p}_s/(1 + A_{s-1} + B_s)$.

*Proof.* Divide $D$ by the counted pdf of the technique. For the connection $s$, the techniques with fewer light vertices give $A_{s-1}$, the connection itself gives 1, and the others give $B_s$. By (1) and Lemma 1, $A_{s-1} = \overleftarrow{p}_{s-1}(\mathrm{dVCM}_{s-1} + \eta + \mathrm{dVC}_{s-1}\rho_{s-1})$ for $s \ge 2$, and $\overleftarrow{p}_{s-1}$ is the area pdf of the new edge from $x_s$. By (3), $B_s = \overrightarrow{p}_s(\eta + \mathrm{dVCM}_s + \mathrm{dVC}_s\phi_s)$, and $\overrightarrow{p}_s$ is the area pdf of the new edge from $x_{s-1}$. These are the two terms of the connection weight. For $s = 1$, $A_0 = r_0 = \rho_1 c_0^+/(d_0^2 p_A)$, the ratio of the camera's area pdf for $x_0$ to the light's, which is the first term of the weight of next event estimation, and $\overrightarrow{p}_1 = \phi_0 c_1^-/d_0^2$ in its second term. For $s = 0$ there is no merge at $x_0$, so the sum is $1 + B_0 - \eta\overrightarrow{p}_0 = 1 + p_A\,\mathrm{dVCM}_0 + p_A\phi_0\,\mathrm{dVC}_0$ by (3). For the merge at $x_s$,

$$\frac{1 + A_{s-1} + B_s}{\eta\overrightarrow{p}_s} = 1 + \frac{1 + A_{s-1}}{\eta\overrightarrow{p}_s} + \frac{B_s - \eta\overrightarrow{p}_s}{\eta\overrightarrow{p}_s}.$$

By Lemma 1 the middle term is $\mathrm{dVCM}_s/\eta + \mathrm{dVM}_s\rho_s$ of the light vertex. By (2) the last term is $q_s(1 + B_{s+1})/(\eta\overrightarrow{p}_s) = (1 + B_{s+1})/(\eta\overleftarrow{p}_s) = \mathrm{dVCM}_s/\eta + \mathrm{dVM}_s\phi_s$ of the camera vertex for $s \le k - 2$, and 0 for $s = k - 1$, where the camera state is 0. $\square$

The test computes both sides of Theorem 1 in exact fractions for random pdfs and paths with up to 7 vertices, and checks that the weights sum to 1.

**Theorem 2 (connections are unbiased).** With $\eta = 0$ the estimate of a camera subpath is an unbiased estimate of the measurement.

*Proof.* Each connection technique $s$ adds $f(\bar x) w_s(\bar x)/p_{\mathrm{VC}}(s)(\bar x)$ for a path sampled with the pdf $p_{\mathrm{VC}}(s)$, whose expected value is $\int f w_s\, d\mu$. Every technique in $D$ is used, and each has a positive pdf where $f > 0$, since the scatter pdfs and $p_A$ are positive on the hemisphere and on the light. So $\sum_s w_s = 1$ wherever $f > 0$, and the sum of the expected values is $\int f\, d\mu$. $\square$

With $\eta > 0$ a merge evaluates the path with the light vertex $x_s^\ast$ in place of $x_s$, both in $f$ and in the weights. Its expected value is the integral of $f w$ against a disc kernel of radius $r$. This converges to the integral at $x_s$ as $r \to 0$ when $f$ and the pdfs are continuous, so VCM is biased for a fixed $r$ and consistent when $r \to 0$ while $n\pi r^2 \to \infty$, as in progressive photon mapping.

**Lemma 3 (the furnace).** Inside the unit sphere with constant albedo $\rho$ and constant emitted radiance $L_e$, the radiance carried by the paths with exactly $k$ edges is $\rho^{k-1}L_e$. So the paths with at most $K$ edges give $L_e\sum_{j=0}^{K-1}\rho^j$.

*Proof.* Let $L_1 = L_e$ and $L_{k+1}(x, \omega_o) = \int_{H^2}\frac{\rho}{\pi}L_k\cos\theta\, d\omega$. If $L_k$ is the constant $c$, then $L_{k+1} = \frac{\rho}{\pi}\,c\,\pi = \rho c$, since the cosine integrates to $\pi$ over the hemisphere. The path with $k$ edges has $k - 1$ reflections. $\square$

**Lemma 4 (the merge disc).** The points of the unit sphere within the distance $r \le 2$ of a point of the sphere form a cap of area $\pi r^2$.

*Proof.* If the angle between the two radii is $\gamma$, the distance is $r$ with $r^2 = 2 - 2\cos\gamma$. The cap $\gamma \le \gamma_0$ has the height $h = 1 - \cos\gamma_0 = r^2/2$ and, by Archimedes' theorem, the area $2\pi h = \pi r^2$. $\square$

In the furnace, the light vertices of each depth are uniform on the sphere and their throughput does not depend on the position, by symmetry. With Lemma 4, a merge with the weight 1 is then an unbiased density estimate for every $r$. The weighted merges of VCM still use two different vertices in their weights, but the tests and the example find no bias within the statistical error.
