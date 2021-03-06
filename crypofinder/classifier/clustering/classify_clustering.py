from sklearn.cluster import KMeans
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pickle
import os
from colorama import Fore, Back, Style
import operator


DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/")

from classifier.utils.classify import generate_name


def classify_clustering(unknown_data_features, result="Mining", printing=False):
    with open(DATA_PATH + "bin/features_data.bin", 'rb') as f:
        allFeatures, Classes, oClass = pickle.load(f)

    allFeatures = allFeatures[:, :unknown_data_features.shape[1]]

    pca = PCA(n_components=len(Classes), svd_solver='full')
    pcaFeatures = pca.fit(allFeatures).transform(allFeatures)

    centroids = {}
    for c in range(len(Classes)):
        pClass = (oClass == c).flatten()
        centroids.update({c: np.mean(allFeatures[pClass, :], axis=0)})

    scaler = StandardScaler()
    NormAllFeatures = scaler.fit_transform(allFeatures)

    NormAllTestFeatures = scaler.fit_transform(unknown_data_features)

    pca = PCA(n_components=len(Classes), svd_solver='full')
    NormPcaFeatures = pca.fit(NormAllFeatures).transform(NormAllFeatures)

    NormTestPcaFeatures = pca.fit(NormAllTestFeatures).transform(NormAllTestFeatures)

    # K-means assuming len(Classes) clusters
    centroids = np.array([])

    for c in range(len(Classes)):
        pClass = (oClass == c).flatten()
        centroids = np.append(centroids, np.mean(NormPcaFeatures[pClass, :], axis=0))

    centroids = centroids.reshape((len(Classes), len(Classes)))

    result_dict = {}

    for classes in Classes.values():
        classes = generate_name(classes)
        result_dict[classes] = 0

    kmeans = KMeans(init=centroids, n_clusters=len(Classes))
    kmeans.fit(NormPcaFeatures)
    labels = kmeans.labels_

    # Determines and quantifies the presence of each original class observation in each cluster
    KMclass = np.zeros((len(Classes), len(Classes)))

    for cluster in range(len(Classes)):
        p = (labels == cluster)
        aux = oClass[p]
        for c in range(len(Classes)):
            KMclass[cluster, c] = np.sum(aux == c)

    probKMclass = KMclass / np.sum(KMclass, axis=1)[:, np.newaxis]
    nObsTest, nFea = NormTestPcaFeatures.shape

    for i in range(nObsTest):
        x = NormTestPcaFeatures[i, :].reshape((1, nFea))
        label = kmeans.predict(x)
        testClass = 100 * probKMclass[label, :].flatten()

        testClass = np.argsort(testClass)[-1]

        result_dict[generate_name(Classes[testClass])] += 1

    if printing:
        print("\n" + Back.BLUE + Fore.WHITE + "# -> Final Results\n" + Style.RESET_ALL)

        print(Fore.BLUE + "Classification based on Clustering (Kmeans):" + Style.RESET_ALL)

        first = True

        for key, value in sorted(result_dict.items(), key=operator.itemgetter(1), reverse=True):
            if first and key == result:
                print(Fore.GREEN + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
            elif first:
                print(Fore.RED + key + ": " + str(int(value / nObsTest * 100)) + "%" + Style.RESET_ALL)
            else:
                print(key + ": " + str(int(value / nObsTest * 100)) + "%")

            first = False

    return result
