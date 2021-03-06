import numpy as np
import pickle
import os
from colorama import Fore, Back, Style
import operator


from classifier.utils.classify import distance


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")

from classifier.utils.classify import generate_name


def classify_distances(unknown_features_data, unknown_features_dataS, unknown_features_dataW, result="Mining", printing=False):
    with open(DATA_PATH + "bin/features_data.bin", 'rb') as f:
        features, featuresS, featuresW, Classes, oClass, oClassS, oClassW = pickle.load(f)

    # setting selected features
    obsFeatures = featuresW
    oClass = oClassW

    unknown_data_features = unknown_features_dataW
    # end

    obsFeatures = obsFeatures[:, :unknown_data_features.shape[1]]

    result_dict = {}

    for classes in Classes.values():
        classes = generate_name(classes)
        result_dict[classes] = 0

    nObsTest, nFea = unknown_data_features.shape

    for i in range(nObsTest):
        x = unknown_data_features[i]

        # calculate distances from y to x
        dists = [distance(x, y) for y in obsFeatures]

        # sum all the distances
        sum_dists = np.sum(dists)

        group_dists = {}

        for classes in Classes.values():
            classes = generate_name(classes)
            group_dists[classes] = 0

        # iterate over the distances
        for class_i, dist in enumerate(dists):
            class_group = generate_name(Classes[int(oClassW[class_i][0])])
            group_dists[class_group] += dist / sum_dists

        result_dict[sorted(group_dists.items(), key=operator.itemgetter(1))[0][0]] += sorted(group_dists.items(), key=operator.itemgetter(1))[0][1]
        result_dict[sorted(group_dists.items(), key=operator.itemgetter(1))[1][0]] += sorted(group_dists.items(), key=operator.itemgetter(1))[1][1]

    result_dict = sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True)

    if printing:
        print("\n" + Back.BLUE + Fore.WHITE + "# -> Final Results\n" + Style.RESET_ALL)

        print(Fore.BLUE + "Classification based on Distances:" + Style.RESET_ALL)

        first = True

        for key, value in result_dict:
            if first and key == result:
                print(Fore.GREEN + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
            elif first:
                print(Fore.RED + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
            else:
                print(key + ": " + str(int(value / nObsTest * 100)) + "%")

            first = False

    return result_dict
