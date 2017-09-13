from dipy.reconst import mapmri
import nibabel as nib
from dipy.io.gradients import read_bvals_bvecs
from dipy.core.gradients import gradient_table
import matplotlib
matplotlib.use('agg')
import json
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

with open('config.json') as config_json:
    config = json.load(config_json)

    #Paths to data
    data_file = str(config['data_file'])
    data_bval = str(config['data_bval'])
    data_bvec = str(config['data_bvec'])

    small_delta = float(config['small_delta'])
    big_delta = float(config['big_delta'])

img = nib.load(data_file)
bvals,bvecs = read_bvals_bvecs(data_bval,data_bvec)

# big_delta = 0.0218  # seconds
# small_delta = 0.0129  # seconds
gtab = gradient_table(bvals=bvals, bvecs=bvecs,
                      small_delta=small_delta,
                      big_delta=big_delta, b0_threshold=50)

data = img.get_data()

data_small = data[60:85, 80:81, 60:85]

# print('data.shape (%d, %d, %d, %d)' % data.shape)

radial_order = 6
map_model_laplacian_aniso = mapmri.MapmriModel(gtab, radial_order=radial_order,
                                               laplacian_regularization=True,
                                               laplacian_weighting=.2)

map_model_positivity_aniso = mapmri.MapmriModel(gtab, radial_order=radial_order,
                                                laplacian_regularization=False,
                                                positivity_constraint=True)

map_model_both_aniso = mapmri.MapmriModel(gtab, radial_order=radial_order,
                                          laplacian_regularization=True,
                                          laplacian_weighting=.05,
                                          positivity_constraint=True)

mapfit_laplacian_aniso = map_model_laplacian_aniso.fit(data_small)
mapfit_positivity_aniso = map_model_positivity_aniso.fit(data_small)
mapfit_both_aniso = map_model_both_aniso.fit(data_small)

# generating RTOP plots
fig = plt.figure(figsize=(10, 5))
ax1 = fig.add_subplot(1, 3, 1, title=r'RTOP - Laplacian')
ax1.set_axis_off()
ind = ax1.imshow(mapfit_laplacian_aniso.rtop()[:, 0, :].T,
                 interpolation='nearest', origin='lower', cmap=plt.cm.gray,
                 vmin=0, vmax=5e7)

ax2 = fig.add_subplot(1, 3, 2, title=r'RTOP - Positivity')
ax2.set_axis_off()
ind = ax2.imshow(mapfit_positivity_aniso.rtop()[:, 0, :].T,
                 interpolation='nearest', origin='lower', cmap=plt.cm.gray,
                 vmin=0, vmax=5e7)

ax3 = fig.add_subplot(1, 3, 3, title=r'RTOP - Both')
ax3.set_axis_off()
ind = ax3.imshow(mapfit_both_aniso.rtop()[:, 0, :].T,
                 interpolation='nearest', origin='lower', cmap=plt.cm.gray,
                 vmin=0, vmax=5e7)
divider = make_axes_locatable(ax3)
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(ind, cax=cax)

plt.savefig('MAPMRI_maps_regularization.png')