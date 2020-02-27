from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
from joblib import dump, load
import argparse

descript = """Using parameters to edit OpenFOAM parameters"""
parser = argparse.ArgumentParser(description=descript)

parser.add_argument('-specroot', help='The DAG spec root')

args = parser.parse_args()

training_percent = 0.6
timestep = -1

SPECROOT = args.specroot
inputs_dir = SPECROOT + '/merlin_info'
outputs_dir = SPECROOT + '/combine_outputs'

outputs = np.load(outputs_dir + '/data.npz')
U = outputs['arr_0']
vorticity = outputs['arr_1']
enstrophy = outputs['arr_2']

energy_byhand = np.sum(np.sum(U**2, axis=3), axis=2)/ U.shape[2] /2
enstrophy_all = np.sum(enstrophy, axis=2)

X = np.load(inputs_dir + '/samples.npy')
y = np.concatenate((enstrophy_all[:, timestep].reshape(-1,1), energy_byhand[:, timestep].reshape(-1,1)), axis=1)
X[:,1] = np.log10(X[:,0]/X[:,1]) #np.log10(X)
y = np.log10(y)

training_size = int(training_percent * len(X))

X_train = X[:training_size]
y_train = y[:training_size]
X_test = X[training_size:]
y_test = y[training_size:]

regr = RandomForestRegressor(max_depth=10, random_state=0, n_estimators=7)

regr.fit(X_train, y_train)
print('training score:', regr.score(X_train, y_train))
print('testing score: ', regr.score(X_test, y_test))
print(mean_squared_error(y_test, regr.predict(X_test)))

dump(regr, 'trained_model.joblib')


import matplotlib.pyplot as plt
fig, ax = plt.subplots(2, 2, figsize=(25, 25), constrained_layout=True)
plt.rcParams.update({'font.size': 20})
plt.rcParams['lines.linewidth'] = 5

x = np.linspace(-5,8,100)
y1 = 1*x
ax[0][0].plot(x, y1, '-r', label='y=x', linewidth=1)

y_pred = regr.predict(X_train)
ax[0][0].scatter(y_train[:,0], y_pred[:,0], label='Log10 Enstrophy')
ax[0][0].scatter(y_train[:,1], y_pred[:,1], label='Log10 Energy')
ax[0][0].set_title('Velocity Magnitude %s'%timestep)

ax[0][0].set_xlabel('Actual')
ax[0][0].set_ylabel('Predicted')
ax[0][0].set_title('Training Data, # Points: %s'%len(y_pred))
ax[0][0].legend()
ax[0][0].grid()

x_min = np.min([np.min(y_train[:,0]), np.min(y_train[:,1])])
y_min = np.min([np.min(y_pred[:,0]), np.min(y_pred[:,1])])
x_max = np.max([np.max(y_train[:,0]), np.max(y_train[:,1])])
y_max = np.max([np.max(y_pred[:,0]), np.max(y_pred[:,1])])

y_pred = regr.predict(X_test)
ax[0][1].plot(x, y1, '-r', label='y=x',  linewidth=1)
ax[0][1].scatter(y_test[:,0], y_pred[:,0], label='Log10 Enstrophy')
ax[0][1].scatter(y_test[:,1], y_pred[:,1], label='Log10 Energy')
ax[0][1].set_xlabel('Actual')
ax[0][1].set_ylabel('Predicted')
ax[0][1].set_title('Testing Data, # Points: %s'%len(y_pred))
ax[0][1].legend()
ax[0][1].grid()

x_min = np.min([np.min(y_test[:,0]), np.min(y_test[:,1]), x_min]) - 0.1
y_min = np.min([np.min(y_pred[:,0]), np.min(y_pred[:,1]), y_min]) - 0.1
x_max = np.max([np.max(y_test[:,0]), np.max(y_test[:,1]), x_max]) + 0.1
y_max = np.max([np.max(y_pred[:,0]), np.max(y_pred[:,1]), y_max]) + 0.1


ax[0][0].set_xlim([x_min, x_max])
ax[0][0].set_ylim([y_min, y_max])
ax[0][1].set_xlim([x_min, x_max])
ax[0][1].set_ylim([y_min, y_max])

y_pred_all = regr.predict(X)
input_enstrophy = ax[1][0].scatter(X[:,0], X[:,1], c=y[:,0]-y_pred_all[:,0], s=100, cmap=plt.get_cmap('Spectral'))
ax[1][0].set_xlabel('Lidspeed')
ax[1][0].set_ylabel("Log10 Reynold's Number")
ax[1][0].set_title('Inputs vs Enstrophy')
ax[1][0].grid()
cbar = plt.colorbar(input_enstrophy, ax=ax[1][0])
cbar.ax.set_ylabel(r'$y_{act} - y_{pred}$', rotation=270, labelpad=20)


input_energy = ax[1][1].scatter(X[:,0], X[:,1], c=y[:,1]-y_pred_all[:,1], s=100, cmap=plt.get_cmap('Spectral'))
ax[1][1].set_xlabel('Lidspeed')
ax[1][1].set_ylabel("Log10 Reynold's Number")
ax[1][1].set_title('Inputs vs Energy')
ax[1][1].grid()
cbar = plt.colorbar(input_energy, ax=ax[1][1])
cbar.ax.set_ylabel(r'$y_{act} - y_{pred}$', rotation=270, labelpad=20)

plt.savefig('prediction.png')