r"""
2D Reservoir ESMDA example
==========================

Ensemble Smoother Multiple Data Assimilation (ESMDA) in Reservoir Simulation.

"""
import numpy as np
import matplotlib.pyplot as plt
import dageo
import Utilities
import UTCHEMresult
from multiprocessing import Pool
import os

# For reproducibility, we instantiate a random number generator with a fixed
# seed. For production, remove the seed!
rng = np.random.default_rng(0)


###############################################################################
# Model parameters
# ----------------

# Grid extension
nx = 30
ny = 30
nc = nx*ny

# Permeabilities
perm_mean = 3.0
perm_min = 0.5
perm_max = 5.0

# ESMDA parameters
ne =50                  # Number of ensembles
#dt = np.zeros(461)+0.0001  # Time steps (could be irregular, e.g., increasing!)
dt = np.zeros(153)+0.0001  # Time steps (could be irregular, e.g., increasing!)
time = np.r_[0, np.cumsum(dt)]
nt = time.size

# Assumed sandard deviation of our data
dstd = 0.0025
file_location=r"D:\IWTT"

###############################################################################
# Create permeability maps for ESMDA
# ----------------------------------
#
# We will create a set of permeability maps that will serve as our initial
# guess (prior). These maps are generated using a Gaussian random field and are
# constrained by certain statistical properties.

# Get the model and ne prior models
RP = dageo.RandomPermeability(nx, ny, perm_mean, perm_min, perm_max)
perm_true = RP(1, random=rng)
#Updateinput(perm_true)
perm_prior = RP(ne, random=rng)


# QC covariance, reference model, and first two random models
pinp1 = {"origin": "lower", "vmin": perm_min, "vmax": perm_max}
fig, axs = plt.subplots(2, 2, figsize=(6, 6), constrained_layout=True)
axs[0, 0].set_title("Model")
im = axs[0, 0].imshow(perm_true.T, **pinp1)
axs[0, 1].set_title("Lower Covariance Matrix")
im2 = axs[0, 1].imshow(RP.cov, cmap="plasma")
axs[1, 0].set_title("Random Model 1")
axs[1, 0].imshow(perm_prior[0, ...].T, **pinp1)
axs[1, 1].set_title("Random Model 2")
axs[1, 1].imshow(perm_prior[1, ...].T, **pinp1)
fig.colorbar(im, ax=axs[1, :], orientation="horizontal",
             label="Log of Permeability (mD)")
for ax in axs[1, :].ravel():
    ax.set_xlabel("x-direction")
for ax in axs[:, 0].ravel():
    ax.set_ylabel("y-direction")


###############################################################################
# Run the prior models and the reference case
# -------------------------------------------

# Instantiate reservoir simulator
def sim(x):
    '''
    results=[]
    for i in range(x.shape[0]):
        result = Utilities.UTCHEMsim(i,x[i])  # Assuming each row in x is an input case
        results.append(result)  # Store the result
    results = np.array(results)  # Convert to a NumPy array if needed
    '''
    with Pool() as pool:
        results = pool.starmap(Utilities.UTCHEMsim, [(i, x[i]) for i in range(x.shape[0])])
    results = np.array(results)  # Convert to a NumPy array if needed
    return results

def restrictobs(x):
    return np.clip(x, 0, 1, out=x)

if __name__ == "__main__":

    # Simulate data for the prior and true fields
    for i in range(ne):
        # Assuming file_location is defined
        os.chdir(os.path.join(file_location, str(i)))  # Change directory safely
        with open(os.path.join(file_location, "sample", "INPUT"), "r") as f:
            lines = f.readlines()  # Read lines from the input file
        with open("INPUT", "w") as w:
            w.writelines(lines)  # Write all lines to the new file




    data_prior = np.array(sim(perm_prior))
    data_true = UTCHEMresult.result(r"D:\IWTT\sample")
    data_obs = rng.normal(data_true, dstd)
    data_obs=restrictobs(data_obs)

    # QC data and priors
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    #ax.set_title("Observed and prior data")
    ax.set_title("Observed and Initial Ensemble")
    #ax.plot(time*24*60*60, data_prior.T, color=".6", alpha=0.5,label='Ini. Ensemble')

    # Plot initial ensemble with a single legend entry
    for i, prior in enumerate(data_prior):
        label = "Prior" if i == 0 else "_nolegend_"
        ax.plot(time * 24 * 60 * 60, prior, color=".6", alpha=0.5, label=label)

    #ax.plot(time*24*60*60, data_true, "ko", label="True data")
    ax.plot(time*24*60*60, data_true, "C3o", label="Obs. data")
    ax.legend()
    ax.set_xlabel("Time")
    ax.set_ylabel("Tracer concentration")
    fig.savefig(r'C:\Users\zz6447\Documents\GitHub\dageo\TracerESMDA\Figure\Prior.png')



    ###############################################################################
    # ESMDA
    # -----


    def restrict_permeability(x):
        """Restrict possible permeabilities."""
        np.clip(x, perm_min, perm_max, out=x)


    perm_post, data_post = dageo.esmda(
        model_prior=perm_prior,
        forward=sim,
        data_obs=data_obs,
        sigma=dstd,
        alphas=8,
        data_prior=data_prior,
        callback_post=restrict_permeability,
        random=rng,
    )


    ###############################################################################
    # Posterior Analysis
    # ------------------
    #
    # After running ESMDA, it's crucial to analyze the posterior ensemble of
    # models. Here, we visualize the first three realizations from both the prior
    # and posterior ensembles to see how the models have been updated.

    # Plot posterior
    for i in range(ne):
        fig, ax = plt.subplots(1, 2, figsize=(8, 5), constrained_layout=True)
        pinp2 = {"origin": "lower", "vmin": 2.5, "vmax": 3.5}
        ax[0].set_title("Prior Mean")
        im = ax[0].imshow(perm_prior[i], **pinp2)
        ax[1].set_title("Post Mean")
        ax[1].imshow(perm_post[i], **pinp2)
        fig.colorbar(im, ax=ax, label="Log of Permeability (mD)",
                     orientation="horizontal")
        fig.savefig(r'C:\Users\zz6447\Documents\GitHub\dageo\TracerESMDA\Figure'+f'\{i}.png')
        plt.close(fig)



    fig, ax = plt.subplots(1, 2, figsize=(8, 5), constrained_layout=True)
    pinp2 = {"origin": "lower", "vmin": 2.5, "vmax": 3.5}
    ax[0].set_title("Prior Mean")
    im = ax[0].imshow(perm_prior.mean(axis=0), **pinp2)
    ax[1].set_title("Post Mean")
    ax[1].imshow(perm_post.mean(axis=0), **pinp2)
    fig.colorbar(im, ax=ax, label="Log of Permeability (mD)",
                 orientation="horizontal")
    fig.savefig(r'C:\Users\zz6447\Documents\GitHub\dageo\TracerESMDA\Figure\average.png')
    plt.close(fig)

    fig, ax = plt.subplots(1, 2, figsize=(8, 5), constrained_layout=True)
    pinp2 = {"origin": "lower", "vmin": 2.5, "vmax": 3.5}
    ax[0].set_title("Prior Mean")
    im = ax[0].imshow(perm_true[0],**pinp2)
    ax[1].set_title("Post Mean")
    ax[1].imshow(perm_post.mean(axis=0), **pinp2)
    fig.colorbar(im, ax=ax, label="Log of Permeability (mD)",
                 orientation="horizontal")
    fig.savefig(r'C:\Users\zz6447\Documents\GitHub\dageo\TracerESMDA\Figure\truevsaverage.png')
    plt.close(fig)


    ###############################################################################
    # Observing the monitored pressure at cell (1,1) for all realizations and the
    # reference case, we can see that the ensemble of models after the assimilation
    # steps (in blue) is closer to the reference case (in red) than the prior
    # ensemble (in gray). This indicates that the ESMDA method is effectively
    # updating the models to better represent the observed data.


    # Compare posterior to prior and observed data
    fig, ax = plt.subplots(1, 1, constrained_layout=True)
    ax.set_title("Prior and posterior Ensemble")
    #ax.plot(time*24*60*60, data_prior.T, color=".6", alpha=0.5)
    #ax.plot(time*24*60*60, data_post.T, color="C0", alpha=0.5)
    #ax.plot(time*24*60*60, data_true, "ko")
    #ax.plot(time*24*60*60, data_obs, "C3o")
    ax.set_xlabel("Time")
    ax.set_ylabel("Tracer concentration")

    for i, prior in enumerate(data_prior):
        label = "Prior" if i == 0 else "_nolegend_"
        ax.plot(time * 24 * 60 * 60, prior, color=".6", alpha=0.5, label=label)
    for i, prior in enumerate(data_post):
        label = "Post" if i == 0 else "_nolegend_"
        ax.plot(time * 24 * 60 * 60, prior, color="C0", alpha=0.5, label=label)

    ax.plot(time * 24 * 60 * 60,  data_true, "C3o",label='Obs. data')

    ax.legend()

    fig.savefig(r'C:\Users\zz6447\Documents\GitHub\dageo\TracerESMDA\Figure\Post.png')
    ###############################################################################

    dageo.Report()
    print('wow')
