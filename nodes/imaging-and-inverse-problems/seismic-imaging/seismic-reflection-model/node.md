---
tag: QPK5AV
kind: model
slug: seismic-reflection-model
name: Convolutional model of a seismic trace
aliases:
- convolutional seismic model
area: imaging-and-inverse-problems/seismic-imaging
level: intro
summary: "Model a reflection seismic trace as a source wavelet convolved with the reflectivity series of the earth, plus noise. It is the forward model behind deconvolution."
prereqs: [discrete-convolution, forward-operator]
see_also: [predictive-deconvolution, minimum-entropy-deconvolution, autocorrelation, minimum-phase, normal-moveout-correction, seismic-migration, wave-equation, snells-law]
sources:
  - paper: doi:10.1190/1.1438415
    title: Enders A. Robinson, Predictive decomposition of seismic traces, Geophysics 22(4), 1957, 767 to 778
    locator: the trace as a wavelet convolved with an uncorrelated series, and the recovery of the series by a prediction error operator
  - book: isbn:9781560800941
    title: Oz Yilmaz, Seismic Data Analysis, Society of Exploration Geophysicists, 2001, Investigations in Geophysics 10
    locator: the chapter on deconvolution (the convolutional model and its assumptions)
  - book: isbn:9780521708425
    title: Peter M. Shearer, Introduction to Seismology, second edition, Cambridge University Press, 2009
    locator: Chapter 7 (reflection seismology)
---

The convolutional model is the basic forward model of reflection seismology. A seismic trace is the source wavelet convolved with the reflectivity series of the earth, plus noise. The reflectivity holds one spike for each boundary between rock layers, at the two-way time of the boundary, with the normal-incidence reflection coefficient as its amplitude. The model is linear in the reflectivity and in the wavelet, and it turns the recovery of the earth's layers into a deconvolution problem. It is an assumption about the earth, not a law: it holds for a layered earth at near-vertical incidence, with primaries only and a wavelet that does not change with time, and it fails where these conditions fail.

## The machine

The input is the reflectivity $r_t$, the wavelet $w_t$ and the noise $n_t$ on a time grid with step $\Delta t$; $t$ is two-way time. The output is the trace
$$d_t = \sum_k w_k\, r_{t-k} + n_t, \qquad \text{or} \qquad D(\omega) = W(\omega)\, R(\omega) + N(\omega)$$
after the Fourier transform $U(\omega) = \int u(t)\, e^{-i\omega t}\, dt$, by the [convolution theorem](/convolution-theorem/). For a stack of flat layers with densities $\rho_j$ and velocities $v_j$, the acoustic impedance is $Z_j = \rho_j v_j$, and the boundary between layers $j$ and $j + 1$ gives the spike
$$r_j = \frac{Z_{j+1} - Z_j}{Z_{j+1} + Z_j} \quad \text{at the time} \quad t_j = \sum_{i \le j} \frac{2 h_i}{v_i},$$
where $h_i$ is the thickness of layer $i$ and the depth $z$ is positive down. The noise holds everything the model leaves out: random noise, and in a strict reading also the multiples, the transmission losses, the spherical spreading and the absorption. In practice a gain corrects the spreading, and other processing steps remove the multiples, before deconvolution uses the model.

Two statistical assumptions are added for deconvolution. The reflectivity is white: its autocorrelation is a spike at lag zero. The wavelet is minimum phase: its $z$-transform has no zeros in the closed unit disk. Both are assumptions about the data, and both are only roughly true.

## What it counts

The model counts samples on a uniform time grid. The unknowns are the $n$ reflectivity samples and the $L$ wavelet samples, and the data are the $n + L - 1$ trace samples. In the real-RAM model one application of the forward map costs $O(n L)$ operations directly and $O(n \log n)$ with an FFT; its adjoint, the cross-correlation with the wavelet, costs the same. For many traces with one wavelet the costs add. The information in the data is counted by frequency: at a frequency where $W(\omega) = 0$ the reflectivity is not seen at all, so the band of the wavelet limits what any method can recover.

## Relation to other models

- The 1D wave equation for a stack of layers, with all multiples and transmission losses, is the exact model for vertical waves in a flat earth; the convolutional model keeps only the primaries. Layered-earth models with multiples and the reverberation model used by gapped [predictive deconvolution](/predictive-deconvolution/) add the multiples back as a feedback filter.
- At nonzero offsets the reflection coefficient changes with the angle of incidence, and the arrival time follows [normal moveout](/normal-moveout-correction/); the convolutional model then holds trace by trace after moveout correction, with an angle-dependent reflectivity.
- The Born approximation of the [wave equation](/wave-equation/) is the multidimensional form: the data are linear in the perturbation of the impedance, and [seismic migration](/seismic-migration/) applies the adjoint of that map. The exploding reflector model of migration is a zero-offset version.
- Pulse-echo imaging in ultrasound uses the same structure: a pulse convolved with a reflectivity map, plus noise.
- As an inverse problem, recovery of $r$ from $d$ with a known $w$ is a linear [forward operator](/forward-operator/) problem, a Toeplitz system; with an unknown $w$ it is blind deconvolution.

## Known results in the model

- Reflection coefficients: for positive impedances, $|r_j| < 1$, and $r_j > 0$ when the impedance grows downward (a theorem, from the formula). The impedances follow from the coefficients by the recursion $Z_{j+1} = Z_j (1 + r_j)/(1 - r_j)$ (a theorem); errors in the $r_j$ add up along the recursion, so the low frequencies of the impedance must come from other data.
- Example: water ($\rho = 1000$ kg/m³, $v = 1500$ m/s, $Z = 1.5 \times 10^6$) over soft sediment ($\rho = 2000$, $v = 1800$, $Z = 3.6 \times 10^6$) gives $r = 2.1/5.1 = 0.412$. Shale ($\rho = 2400$, $v = 2800$) over sand ($\rho = 2200$, $v = 2600$) gives $r = (5.72 - 6.72)/(5.72 + 6.72) = -0.080$. The sea surface, water under air with $Z \approx 0$, gives $r = -1$ for a wave coming up from the water.
- Autocorrelation: the autocorrelation of the trace is the autocorrelation of the wavelet convolved with that of the reflectivity, plus noise terms (a theorem, from the convolution theorem). If the reflectivity is white with variance $\sigma^2$ and the noise is uncorrelated with it, the expected trace autocorrelation is $\sigma^2$ times the wavelet autocorrelation plus the noise autocorrelation (a theorem in expectation). So the data give the amplitude spectrum $|W(\omega)|$, which [predictive deconvolution](/predictive-deconvolution/) uses.
- The phase is not seen by second-order statistics: any all-pass filter applied to $w$ leaves $|W|$ and all autocorrelations unchanged (a theorem). The [minimum-phase](/minimum-phase/) assumption picks one wavelet from this set. [Minimum entropy deconvolution](/minimum-entropy-deconvolution/) uses the non-Gaussian, sparse shape of the reflectivity in place of the phase assumption; that it then finds the right wavelet is a heuristic, with no guarantee in general.
- With known $w$ and white noise, the least-squares estimate of $r$ is the [Wiener filter](/wiener-filter/) output, and the reflectivity is resolved only in the band of the wavelet (a theorem about the model). Two spikes closer than about a quarter of the dominant wavelength interfere and cannot be told apart by their amplitudes alone (a heuristic, the tuning thickness).
- Stacked traces, after [common-midpoint stacking](/common-midpoint-stacking/), are modeled as zero-offset traces of the same form, with the noise reduced by the stack.

## References
