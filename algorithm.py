import numpy as np
import itertools
import scipy.io
import random
import os

# IMAGE RESOLUTION/SIZE MUST BE SET HERE
res = (440, 440)

# USER DIRECTORIES MUST BE SET HERE
user1_dir = ''
user2_dir = ''
user3_dir = ''
user4_dir = ''
user5_dir = ''
user6_dir = ''


def load_split_data(prnu_directory, num_imgs):
    """
    given a directory of PRNU files in matrix format (.mat), load data

    return: loaded PRNU data from directory with specified amount set to be
            randomly selected
    """
    data = []
    for matfile in os.listdir(prnu_directory):
        if matfile.endswith(".mat"):
            data.append(scipy.io.loadmat(prnu_directory + '\\' /
                        + matfile)["Fingerprint"])
    data = random.sample(data, num_imgs)
    return data


def percentile_reducer(lower_percentile, upper_percentile, data_var):
    """
    pass PRNU matrix data as input, calculate reduced matrix format (boolean)
    for a given range of percentiles

    return: PRNU data (boolean mask) upon applying percentile range filter
    """
    reduced_PRNUs = []
    for PRNU in data_var:
        lower_bound = np.percentile(PRNU, lower_percentile)
        upper_bound = np.percentile(PRNU, upper_percentile)
        reduced = (PRNU >= lower_bound) & (PRNU <= upper_bound)
        reduced_PRNUs.append(reduced * 1)  # for Bool -> Int conversion
    return reduced_PRNUs


def percentile_reducer_values(lower_percentile, upper_percentile, data_var):
    """
    pass PRNU matrix data as input, calculate reduced matrix format (values)
    for a given range of percentiles

    return: PRNU data (value matrix) upon applying percentile range filter
    """
    reduced_PRNUs = []
    for PRNU in data_var:
        lower_bound = np.percentile(PRNU, lower_percentile)
        upper_bound = np.percentile(PRNU, upper_percentile)
        reduced = (PRNU >= lower_bound) & (PRNU <= upper_bound)
        reduced_PRNUs.append(PRNU[reduced])  # for Bool -> Int conversion
    return reduced_PRNUs


def prnu_template(data_var):
    """
    pass in loaded PRNU data (list format) and calculate the template

    return: single PRNU matrix (a "template" representing the average)
    """
    for prnu in data_var:
        template = np.empty(res)
        template += prnu
    template = template / len(data_var)
    return template


def jaccard(im1, im2):
    """
    pass in two data points (i.e., PRNU) and calculate the jaccard similarity

    return: the jaccard similarity score
    """
    im1 = np.asarray(im1).astype(np.bool)
    im2 = np.asarray(im2).astype(np.bool)

    if im1.shape != im2.shape:
        raise ValueError("Shape mismatch: im1, im2 must have the same shape")
    intersection = np.logical_and(im1, im2)
    union = np.logical_or(im1, im2)
    return intersection.sum() / float(union.sum())


def zscore(xbar, mu, sigma, n):
    """
    pass in data parameters and calculate the z-score

    xbar = sample average of data points
    mu = average of data points
    sigma = standard deviation of data points
    n = number of data points (sample size)

    return:
    """
    z = ((xbar - mu) * np.sqrt(n)) / sigma

    if z <= -1.645:
        indicator = "Reject Null"
    else:
        indicator = "Fail to Reject Null"

    print("Z-Score: {} | {}".format(round(z, 4), indicator))


def device_combinations(d1_data, d2_data, resolution):
    """
    calculate all combinations of D1 and D2 PRNU data (pairwse)
    calculate all combinations of D2 PRNU data (pairwise)
    calculate all combinations of D2 PRNU data (pairwise)

    return: all calculated variations of pairwise combinations for PRNU data
    """
    D1_D2_train_combinations = list(itertools.product(d1_data, d2_data))
    D1_D2_train_matches = np.empty(resolution)
    for PRNU1, PRNU2 in D1_D2_train_combinations:
        singular_match = PRNU1 + PRNU2
        D1_D2_train_matches += singular_match

    D1_D1_train_combinations = list(itertools.combinations(d1_data, 2))
    D1_D1_train_matches = np.empty(res)
    for PRNU1, PRNU2 in D1_D1_train_combinations:
        singular_match = PRNU1 + PRNU2
        D1_D1_train_matches += singular_match

    D2_D2_train_combinations = list(itertools.combinations(d2_data, 2))
    D2_D2_train_matches = np.empty(res)
    for PRNU1, PRNU2 in D2_D2_train_combinations:
        singular_match = PRNU1 + PRNU2
        D2_D2_train_matches += singular_match

    return D1_D2_train_matches, D1_D1_train_matches, D2_D2_train_matches


NUM_PRNU = 100
D1_train = load_split_data(user1_dir, NUM_PRNU)
D2_train = load_split_data(user2_dir, NUM_PRNU)
D3_train = load_split_data(user3_dir, NUM_PRNU)
D4_train = load_split_data(user4_dir, NUM_PRNU)
D5_train = load_split_data(user5_dir, NUM_PRNU)
D6_train = load_split_data(user6_dir, NUM_PRNU)

P_LOW = 80
P_HIGH = 100
reduced80_D2_train = percentile_reducer(P_LOW, P_HIGH, D2_train)
reduced80_D1_train = percentile_reducer(P_LOW, P_HIGH, D1_train)
reduced80_D3_train = percentile_reducer(P_LOW, P_HIGH, D3_train)
reduced80_D4_train = percentile_reducer(P_LOW, P_HIGH, D4_train)
reduced80_D5_train = percentile_reducer(P_LOW, P_HIGH, D5_train)
reduced80_D6_train = percentile_reducer(P_LOW, P_HIGH, D6_train)

D1_D2_train_matches, D1_D1_train_matches, D2_D2_train_matches = device_combinations(
    reduced80_D1_train, reduced80_D2_train, res)

D1_D1_minus_D2_D2 = np.where((D1_D1_train_matches - D2_D2_train_matches)
                             < 0, 0, (D1_D1_train_matches - D2_D2_train_matches))
D1_D1_minus_D1_D2 = np.where((D1_D1_train_matches - D1_D2_train_matches)
                             < 0, 0, (D1_D1_train_matches - D1_D2_train_matches))
D1_D1_minus_D2_D2_mask = np.where(D1_D1_minus_D2_D2 > 0, 1, 0)

D1_jaccard_train = []
for PRNU in reduced80_D6_train:
    D1_jaccard_train.append(jaccard(PRNU, D1_D1_minus_D2_D2_mask))

D2_jaccard_train = []
for PRNU in reduced80_D5_train:
    D2_jaccard_train.append(jaccard(PRNU, D1_D1_minus_D2_D2_mask))

test_num = 20
for value in random.sample(D1_jaccard_train, test_num):
    zscore(value, np.mean(D1_jaccard_train), np.std(D1_jaccard_train), test_num)
print("\n")
