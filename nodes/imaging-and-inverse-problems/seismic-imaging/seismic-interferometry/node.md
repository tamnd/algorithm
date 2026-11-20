---
tag: 27Z2RP
kind: technique
slug: seismic-interferometry
name: Seismic interferometry
aliases:
- ambient noise interferometry
area: imaging-and-inverse-problems/seismic-imaging
level: research
summary: "Retrieve the response between two receivers, as if one were a source, by cross-correlating their recordings of ambient noise or of many sources around them."
prereqs: [cross-correlation, wave-equation]
see_also: [traveltime-tomography, surface-related-multiple-elimination, autocorrelation, seismic-reflection-model, seismic-migration, full-waveform-inversion, convolution-theorem, eikonal-equation]
sources:
  - paper: doi:10.1190/1.1439927
    title: Jon F. Claerbout, Synthesis of a layered medium from its acoustic transmission response, Geophysics 33(2), 1968, 264 to 269
    locator: for a horizontally layered medium, the autocorrelation of the transmission response gives the reflection response
  - paper: doi:10.1103/physrevlett.93.254301
    title: Kees Wapenaar, Retrieving the elastodynamic Green's function of an arbitrary inhomogeneous medium by cross correlation, Physical Review Letters 93(25), 2004, 254301
    locator: the representation of the Green's function between two points, plus its time reverse, by cross-correlations of responses to sources on a closed surface around them
  - paper: doi:10.1126/science.1078551
    title: Michel Campillo and Anne Paul, Long-range correlations in the diffuse seismic coda, Science 299(5606), 2003, 547 to 549
    locator: the cross-correlation of the coda of earthquakes recorded at two stations, which shows the surface waves that travel between them
  - paper: doi:10.1126/science.1108339
    title: Nikolai M. Shapiro, Michel Campillo, Laurent Stehly and Michael H. Ritzwoller, High-resolution surface-wave tomography from ambient seismic noise, Science 307(5715), 2005, 1615 to 1618
    locator: surface-wave travel times from cross-correlations of ambient noise between pairs of stations, and the maps of group velocity made from them
---

Seismic interferometry makes a new seismic record from old ones. Cross-correlate the recordings at two receivers $A$ and $B$ of waves from many sources, and sum over the sources; under conditions on the sources, the result is the response that a source at $A$ would give at $B$, plus its time reverse. So a receiver becomes a virtual source, without a source ever being placed there. The sources can be explosions, earthquakes, or the ambient noise of the ocean and of human activity, which is everywhere and costs nothing. Ambient noise interferometry gives the travel times of surface waves between pairs of stations, and these feed [traveltime tomography](/traveltime-tomography/) of the crust; in exploration it turns sources at the surface and receivers in a well into virtual sources in the well. The retrieval is exact only in idealized settings; with real sources it is an approximation whose errors depend on how the sources are distributed.

## In plain words

Two microphones in a noisy room each record a jumble of sound. A sound that passes the first microphone and then the second arrives at the second a little later, by the time it takes to walk between them. If you slide one record against the other and look for the shift at which they match best, you find that delay. With many sounds coming from all sides, the matches build up at the right delays, and the random parts cancel out. The result looks like what the second microphone would hear if someone clapped at the first one. In the earth the noise comes from ocean waves and traffic, the microphones are seismometers, and the delays tell how fast waves travel between them. The method needs long records and noise from all directions.

## When it applies

- The waves obey a linear wave equation in a medium that does not change during the recording, and, for the exact theory, the medium does not absorb energy.
- There are many sources whose signals are uncorrelated with each other, and they surround the receivers, or at least lie at the ends of the paths through the two receivers (the stationary-phase zones).
- The records are long compared with the travel time between the receivers, so that the random cross terms average out.
- The goal is a response between receivers: a travel time, a surface-wave dispersion curve, a reflection response, or a redatuming of sources to receivers inside the medium.

## The template

1. Record the wavefield $u_A(t)$ and $u_B(t)$ at the two receivers, over a long time or for many sources $k$.
2. Preprocess: remove instrument responses and, for noise, reduce the effect of earthquakes and of strong narrow-band sources by normalization in time and in frequency (heuristics that make the noise field more even).
3. Cross-correlate, $C_{AB}(\tau) = \int u_A(t)\, u_B(t + \tau)\, dt$, in windows or source by source; in the frequency domain this is $\overline{U_A(\omega)}\, U_B(\omega)$ by the [convolution theorem](/convolution-theorem/).
4. Stack the correlations over windows or sources.
5. Read the result as the response from $A$ to $B$ at positive lags and the response from $B$ to $A$, time-reversed, at negative lags, both shaped by the power spectrum of the sources.

**Why it works in one dimension.** Take a homogeneous 1D medium with velocity $v$, receivers at $x_A < x_B$, and a source at $x_s$ that emits $N_s(t)$, so that $u_X(t) = N_s(t - |X - x_s|/v)$, with the amplitude factor set to 1. Then $C_{AB}(\tau)$ is the [autocorrelation](/autocorrelation/) of $N_s$ shifted by $\tau_s = (|x_B - x_s| - |x_A - x_s|)/v$ (a theorem, by a change of variable). For every source left of both receivers, $\tau_s = (x_B - x_A)/v$, the travel time from $A$ to $B$, whatever $x_s$ is; for every source right of both, $\tau_s = -(x_B - x_A)/v$. If the sources emit uncorrelated white noise, the expected cross terms between different sources are zero, and the expected stack is a sum of spikes at $\pm (x_B - x_A)/v$ with weights equal to the source powers (a theorem in expectation). A source between the receivers gives a spike at $(x_A + x_B - 2x_s)/v$, which is not a travel time between them. The fluctuations of a correlation of $n$ samples of unit white noise, normalized by $n$, have standard deviation about $1/\sqrt{n}$, so the stack converges at the rate of the square root of the record length (a theorem for independent Gaussian samples).

**In general.** Wapenaar (2004) showed that in a lossless, arbitrarily inhomogeneous elastic medium, the Green's function between two points plus its time reverse equals an integral, over a closed surface of sources around the points, of cross-correlations of the responses at the two points (a theorem, stated there as an exact representation, with simpler approximate forms for sources far away and uncorrelated noise). Claerbout (1968) had found the 1D form for layered media: the autocorrelation of the transmission response, recorded at the surface from a source at depth, gives the reflection response (a theorem in that model).

## Classic examples

- **The 1D simulation.** Receivers at 0 and 600 m, $v = 2000$ m/s, $\Delta t = 10$ ms, 20000 samples of unit white noise per source (seed 4), correlations normalized by the number of samples. One source at $-500$ m gives a peak of $0.997$ at $+0.3$ s and off-peak values with a root-mean-square of $0.007$, close to $1/\sqrt{20000} = 0.0071$. A second source at $1100$ m adds the peak $1.003$ at $-0.3$ s, with $1.011$ at $+0.3$ s. A third source at 200 m, between the receivers, adds a peak of $0.969$ at $+0.1$ s, a false arrival as strong as the true ones. These are measurements.
- **Coda correlation.** Campillo and Paul (2003) correlated the coda of earthquakes recorded at pairs of stations in Mexico and found the surface waves that travel between the stations.
- **Ambient noise surface-wave maps.** Shapiro, Campillo, Stehly and Ritzwoller (2005) correlated ambient noise between pairs of stations in California, measured the group travel times of the surface waves in the correlations, and inverted them for maps of group velocity.
- **Autocorrelation for reflections.** By Claerbout's result, the autocorrelation of a trace recorded at the surface from sources at depth, or from noise coming from below, gives a reflection trace of the layers above; it is the basis of passive reflection imaging.
- **Virtual sources in a well.** With surface sources and receivers in a well, the correlation of the downgoing and upgoing waves at two well receivers makes a virtual source at the upper receiver, below the complex near surface.

## Variations

- Interferometry by deconvolution or by multidimensional deconvolution, which divides by the power of the incident field in place of correlating; it removes the source spectrum and, in the multidimensional form, the effect of an uneven source distribution, at the cost of a more unstable inversion.
- Correlation of the coda of the correlations, which uses the scattered parts again to make the source field more even.
- Time-lapse monitoring: small changes of velocity, measured from shifts of the late parts of the correlations over days and years.
- The same correlation and convolution structure links interferometry to [surface-related multiple elimination](/surface-related-multiple-elimination/): one convolves data with data to predict multiples, the other correlates data with data to remove a path.
- Imaging with the virtual-source records by [migration](/seismic-migration/) or [full waveform inversion](/full-waveform-inversion/).

## Pitfalls

- Sources that are not on the stationary paths, such as noise between the receivers or from one side only, give false arrivals or a one-sided correlation, as in the 1D simulation (a theorem in that model).
- A noise field that comes mostly from one direction biases the travel times; the bias is usually small when the angle of the dominant noise to the receiver line is large, a heuristic that depends on the geometry.
- Absorption and scattering break the exact theory; amplitudes from noise correlations are less reliable than travel times.
- Earthquakes and instrument glitches dominate raw correlations; the normalization steps help, but they also change the amplitudes.
- Short records give noisy correlations; the noise falls only like the square root of the record length.
- The correlation gives the Green's function convolved with the power spectrum of the noise; with band-limited noise, as the ocean microseism is, only that band is retrieved.

## Exercises

1. Two receivers are 600 m apart in a medium with $v = 2000$ m/s, and the noise comes from both sides along the line through them. At which lags does the stacked correlation peak? (Answer: $\pm 0.3$ s.)
2. In the same setting, show that a source 200 m from the first receiver, between the two, gives a peak at $+0.1$ s, and find the lag for a source at a general point between them.
3. Show that for sources on one side only, the stack is one-sided, and explain why the travel time can still be measured.
4. Show that the cross terms between two uncorrelated white noise sources have zero expectation in the stack, and find their variance as a function of the record length.
5. In 2D, sources on a circle around two receivers: show by stationary phase that the main contribution to the correlation comes from sources near the line through the receivers.

## References
