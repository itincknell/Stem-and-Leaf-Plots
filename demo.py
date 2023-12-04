import numpy as np
from pyfiglet import figlet_format

import stem_plot as sp


# generate distributions
distributions = {
	'Standard Normal': {
		'sample': np.random.randn(1000),
		'scale': 0.01,
		'step': 1,
		'font': 'big'
	},
	'Exponential': {
		'sample': np.random.exponential(scale=1.0, size=500),
		'scale': 0.1,
		'step': 4,
		'font': 'jazmine'
	},
	'Lognormal': {
		'sample': np.random.lognormal(mean=0, sigma=1.0, size=500),
		'scale': .1,
		'step': 3,
		'font': 'epic'
	},
	'Gamma': {
		'sample': np.random.gamma(shape=5.0, scale=1.0, size=500),
		'scale': 0.1,
		'step': 4,
		'font': 'alligator2'
	},
	'Beta Arcsine': {
		'sample': np.random.beta(a=0.5, b=0.5, size=500),
		'scale': 0.01,
		'step': 2,
		'font': 'fender'
	}
}

for name, d in distributions.items():
	print(figlet_format(name,font=d['font'],width=150))
	sp.print_stemplots(sp.stem_plot(list(d['sample']),d['scale'],d['step']))
	print("\n")