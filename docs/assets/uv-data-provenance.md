# UV atomic and dust data

Each multilevel profile's `atomic_model.json` records its data sources and
model values. References include [CHIANTI 11.0.1](https://db.chiantidatabase.org/),
[NIST Al II](https://physics.nist.gov/PhysRefData/Handbook/Tables/aluminumtable4.htm),
[Pickering et al. 2002](https://lup.lub.lu.se/search/files/4682476/623888.pdf)
and the [Kurucz Fe II weak-branch list](http://kurucz.harvard.edu/atoms/2601/gf2601.pos).

Dust coefficients come from Draine's SMC-bar [UV](https://www.astro.princeton.edu/~draine/dust/dat/mix/callscat_init_i.out_SMC_bar_uv),
[optical](https://www.astro.princeton.edu/~draine/dust/dat/mix/callscat_init_i.out_SMC_bar)
and [infrared](https://www.astro.princeton.edu/~draine/dust/dat/mix/callscat_init_i.out_SMC_bar_ir)
tables. The multilevel Voigt approximation uses coefficients from
[Weideman 1994](https://doi.org/10.1137/0731077).

The GSL installation and optional HDF5 and OpenMP installations provide
their own software and license files.
