import numpy as np
import matplotlib.pylab as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True

x_linspace, y_linspace = np.meshgrid(np.linspace(-5,5,1500),np.linspace(-5,5,1500))

ackley = -20. * np.exp(-0.2 * np.sqrt(0.5 * (x_linspace**2 + y_linspace**2))) - np.exp(0.5 * (np.cos(2 * np.pi * x_linspace) + np.cos(2 * np.pi * y_linspace))) + np.e + 20

plt.pcolormesh(x_linspace, y_linspace, ackley)
plt.xlabel(r"$x$", fontsize=20)
plt.ylabel(r"$y$", fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
cbar = plt.colorbar(ticks=np.linspace(0,14,8))
cbar.ax.tick_params(labelsize=18)
cbar.set_label(r"$f\left(x,y\right)$", fontsize=20, rotation=-90, labelpad=24)
contour_lines = plt.contour(x_linspace, y_linspace, ackley, colors='w', levels=np.linspace(2,14,7), linewidths=0.5)
plt.gca().set_aspect(1)
plt.tight_layout()
plt.savefig(f'ackley-function/ackley_2d.png', dpi=500, bbox_inches='tight')
plt.close()