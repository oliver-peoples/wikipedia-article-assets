import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['text.usetex'] = True

# configurable values

freq = 1e9

steering_azimuth = 0
steering_elevation = 0

array_dims = [16,16]
array_lambda_spacing = 2.0

# deduced values

steering_azimuth *= np.pi / 180
steering_elevation *= np.pi / 180

steering_theta = np.arccos(np.cos(steering_azimuth) * np.cos(steering_elevation))
steering_phi = np.arctan2(np.sin(steering_elevation),np.sin(steering_azimuth) * np.cos(steering_elevation))

wavelength = 3e8/freq
k = 2.0 * np.pi * freq / 3e8
d = wavelength * array_lambda_spacing

azimuth_meshgrid, elevation_meshgrid = np.meshgrid(np.linspace(-60,60,1500),np.linspace(60,-60,1500))

azimuth_meshgrid *= np.pi / 180.
elevation_meshgrid *= np.pi / 180.

theta = np.arccos(np.cos(azimuth_meshgrid) * np.cos(elevation_meshgrid))
phi = np.arctan2(np.sin(elevation_meshgrid),np.sin(azimuth_meshgrid) * np.cos(elevation_meshgrid))

af = np.ndarray(shape=np.shape(phi), dtype=np.complex64)

af.fill(0+0.j)

beta_x = -k * d * np.sin(steering_theta) * np.cos(steering_phi)
beta_y = -k * d * np.sin(steering_theta) * np.sin(steering_phi)

phase_x = k * d * np.sin(theta) * np.cos(phi) + beta_x
phase_y = k * d * np.sin(theta) * np.sin(phi) + beta_y

for n in range(array_dims[0]):
    
    y_comp = np.exp(1.j * n * phase_y)
    
    af_x = np.ndarray(shape=np.shape(phi), dtype=np.complex64)

    af_x.fill(0+0.j)
    
    for m in range(array_dims[1]):
        
        af_x += np.exp(1.j * m * phase_x)
        
    af += af_x * y_comp
    
af = 10*np.log10(np.abs(af))
    
plt.title(r'$' + f'{array_dims[0]}' + r'\times' + f'{array_dims[1]}' + '\mathrm{\;Array,\;} ' + f'{array_lambda_spacing}' + r'\lambda\mathrm{\; Spacing}$', fontsize=20)
plt.pcolormesh(azimuth_meshgrid * 180. / np. pi, elevation_meshgrid * 180. / np.pi, af, vmin=-50)
plt.xlabel(r"$\mathrm{Azimuth\;(degrees)}$", fontsize=18)
plt.ylabel(r"$\mathrm{Elevation\;(degrees)}$", fontsize=18)
plt.gca().invert_xaxis()
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
cbar = plt.colorbar()
cbar.ax.tick_params(labelsize=16)
cbar.set_label(r"$10\log_{10}\|\mathrm{AF}\|$", fontsize=20, rotation=-90, labelpad=24)
dp_val = int(np.floor(array_lambda_spacing))
pd_val = int(1000 * array_lambda_spacing - dp_val * 1000)            
plt.savefig(f'phased-array/{array_dims[0]}x{array_dims[1]}_{dp_val}p{pd_val}_lambda_spacing_planar_array_factor.png', dpi=500, bbox_inches='tight')
plt.close()