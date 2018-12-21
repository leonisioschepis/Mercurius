import ed_diff as ed_diff

#old = open('ossimetria/nonin-memory-playback.nmp (2)', 'rb').read()
#new = open('ossimetria/nonin-memory-playback.nmp (3)', 'rb').read()

#print(ed_diff.find_diffs(old,new))
import numpy as np
s = np.random.poisson(lam=(100.,200.,300.,400., 500.), size=(500,5))
print(s)
import matplotlib.pyplot as plt
count, bins, ignored = plt.hist(s, 1000, density=True)
plt.show()
