# Choosing a line and an observable

Start with the feature you want to compare with an observation, such as Lyα
emission or the C IV doublet. Choose the line before running PEACOCK. Once the
photons have escaped, you can use the same run to change the size of the
observing aperture or measure the line relative to its continuum.

## Which line should I run?

Pass the name in the middle column to `--line`. This loads the atomic data and
scattering rules. Some choices model several transitions together. For example,
`CIV1548` produces both components of the doublet. The reference wavelength sets
zero on the velocity axis. The table lists the lines in [PEACOCK 1.0.4](download.md).

| Spectrum of interest | `--line` | What the calculation includes |
| --- | --- | --- |
| H I Lyα | `HI1216` | Resonant scattering of Lyα photons by neutral hydrogen. |
| C II absorption and fluorescent emission | `CII1334` | Absorption and re-emission through the coupled 1334.53, 1335.66 and 1335.71 Å transitions. All three share the 1334.53 Å velocity reference. |
| C IV doublet | `CIV1548` | Both the 1548.19 and 1550.77 Å components in one run. |
| Mg II doublet | `MgII2796` | Both the 2796.35 and 2803.53 Å components in one run. |
| Al II λ1670 | `AlII1670` | The 1670.79 Å resonance line. |
| Fe II λ1608 and its decay branches | `FeII1608` | The 1608.45 Å reference line and radiative decays to other lower levels. |
| N V doublet | `NV1239` or `NV1243` | Both selectors include 1238.82 and 1242.80 Å. Choose the component you want at velocity zero. |
| S II triplet | `SII1250`, `SII1254` or `SII1259` | The three choices use the same atomic network, referenced to 1250.58, 1253.81 or 1259.52 Å, respectively. |
| Si II near 1190–1197 Å | `SiII1190` or `SiII1193` | Both include the 1190.42 and 1193.29 Å resonance lines and the 1194.50 and 1197.39 Å fluorescent branches. |
| Si II near 1527–1533 Å | `SiII1526` | The 1526.71 Å resonance line and its 1533.43 Å fluorescent branch. |

For a doublet or multiplet, choose a source spectrum and plotting window wide
enough to cover the components of interest. All lines in the table run on NVIDIA
GPUs. C IV and Mg II require CUDA in this release, and the others also run on a CPU.
The Si III and Si IV [observed fits](examples.md#example-spectra) illustrate additional
lines studied with PEACOCK.

## When do I need to rerun the transport?

| What you want to change | What to do |
| --- | --- |
| Wind speed, clump positions or sizes, gas column, temperature, dust, or the injected source spectrum | **Run transport again.** Each change can alter the photons' paths or frequencies. If you change the geometry of the C II example, supply a matching clump catalogue. |
| The modeled transition or atomic network | **Select the new line and run again.** Reuse the existing build for that backend. |
| The photon count or the random realization | **Run again.** For an independent photon sample in the same wind, change the photon seed and keep the gas realization and catalogue fixed. |
| The projected aperture, velocity bins, or displayed velocity range | **Replot the saved packets.** The escape position, direction and frequency already determine which photons enter each bin. |
| Continuum-normalized flux or unit-area line shape | **Replot the saved packets** using the normalization appropriate for the injected source and the quantity you want to compare. |

(how-much-c-ii-light-falls-outside-a-250-pc-aperture)=
(cii-aperture-comparison)=
## How aperture size affects the C II line profile

A small aperture centered on the galaxy captures the compact continuum source but can miss
C II photons scattered to larger projected radii. To illustrate this effect, we compare
the full halo with a circular aperture of radius 250 pc, one quarter of the model's 1 kpc
halo radius. For a circular observing aperture, convert its angular radius to parsecs at
the galaxy's distance and pass that value to `--aperture-pc`.

```{figure} assets/research/cii-100k-v150-full-vs-250pc.png
:alt: Full-aperture and 250 pc C II spectra have nearly identical blue absorption troughs. The 250 pc aperture collects less red emission, with the largest difference near +330 km/s.
:width: 100%

The blue absorption trough stays at −150 km/s in both spectra. The smaller aperture
collects less red emission, with the largest difference near +330 km/s. There the
flux falls from about 1.17 to 1.09 times the incident continuum. The lower panel
shows the light missed by the smaller aperture.
```

{download}`Download the plotted fluxes and packet counts (CSV) <assets/research/cii-100k-v150-full-vs-250pc.csv>`

To reproduce the comparison, start from the [C II tutorial](getting-started.md)
run with a 150 km/s outflow. The full aperture includes all 100,000 escaping
photons, and 98,202 fall inside 250 pc. The commands below average over all escape
directions, use 20 km/s bins and normalize to the injected continuum. Run them
from the PEACOCK source directory, replacing `run/cii` with your run directory.

```bash
python3 tools/plot_spectrum.py run/cii --bins 60 --velocity-range -600 600 --normalization continuum --output run/cii/full.png
python3 tools/plot_spectrum.py run/cii --bins 60 --velocity-range -600 600 --normalization continuum --aperture-pc 250 --output run/cii/250pc.png
```

## Which normalization should I compare?

**For absorption depth or emission strength relative to a flat continuum**, use
`--normalization continuum`, as in the C II example above. Each bin is divided by the
number of photons the source injected there *on average*. A value of one is the
unattenuated continuum within the injected window. Using this same denominator for
both apertures preserves the light lost outside 250 pc.

**For the shape of an intrinsic emission line**, use `--normalization probability`.
For example, the bundled Lyα CPU example injects a Gaussian emission line. To compare
peak positions, widths or the relative strengths of its red and blue peaks, run:

```bash
python3 peacock.py run --line HI1216 --backend cpu --output run/lya
python3 tools/plot_spectrum.py run/lya --normalization probability --output run/lya/shape.png
```

Here the area over the selected velocity window is one. Two apertures can therefore
have similar unit-area profiles even if they collect different numbers of photons. To
measure the **total escape fraction** for these equal-weight packets, divide the number
of photons that escaped in all directions and at all frequencies by the number launched.

Choose the normalization from the source in `resolved.cfg` and the measurement you
want. When comparing with an observation, match the projected aperture, velocity zero,
spectral resolution and bin edges, and apply the same normalization to model and data.
See [Spectra and output files](outputs.md) for the velocity convention and file formats.

To explore what shapes the profile, [trace a photon through the clumpy wind](models.md)
or [change the wind speed law and compare two spectra](configuring-a-peacock-simulation.md).
