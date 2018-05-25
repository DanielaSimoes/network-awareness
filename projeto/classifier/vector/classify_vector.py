from sklearn import svm
from colorama import Fore, Back, Style
from sklearn.preprocessing import StandardScaler


def classify_vector(allFeatures, Classes, oClass, unknown_data_features):
    scaler = StandardScaler()
    NormAllFeatures = scaler.fit_transform(allFeatures[:, :unknown_data_features.shape[1]])

    NormAllTestFeatures = scaler.fit_transform(unknown_data_features)

    print('\n-- Classification based on Support Vector Machines --')
    svc = svm.SVC(kernel='linear').fit(NormAllFeatures, oClass)
    rbf_svc = svm.SVC(kernel='rbf').fit(NormAllFeatures, oClass)
    poly_svc = svm.SVC(kernel='poly', degree=2).fit(NormAllFeatures, oClass)
    lin_svc = svm.LinearSVC().fit(NormAllFeatures, oClass)

    # predict
    L1 = svc.predict(NormAllTestFeatures)

    L2 = rbf_svc.predict(NormAllTestFeatures)

    L3 = poly_svc.predict(NormAllTestFeatures)

    L4 = lin_svc.predict(NormAllTestFeatures)

    nObsTest, nFea = NormAllTestFeatures.shape

    svc_result = {}
    kernel_rbf_result = {}
    kernel_poly_result = {}
    linear_svc_result = {}

    for classes in Classes.values():
        svc_result[classes] = 0
        kernel_rbf_result[classes] = 0
        kernel_poly_result[classes] = 0
        linear_svc_result[classes] = 0

    for i in range(nObsTest):
        svc_result[Classes[L1[i]]] += 1
        kernel_rbf_result[Classes[L2[i]]] += 1
        kernel_poly_result[Classes[L3[i]]] += 1
        linear_svc_result[Classes[L4[i]]] += 1

    print("\n" + Back.BLUE + Fore.WHITE + "# -> Final Results\n" + Style.RESET_ALL)

    print(Fore.BLUE + "SVC:" + Style.RESET_ALL)

    for key, value in svc_result.items():
        print(key + ": " + str(int(value/nObsTest*100)) + "%")

    print(Fore.BLUE + "\nKernel RBF:" + Style.RESET_ALL)

    for key, value in kernel_rbf_result.items():
        print(key + ": " + str(int(value/nObsTest*100)) + "%")

    print(Fore.BLUE + "\nKernel Poly:" + Style.RESET_ALL)

    for key, value in kernel_poly_result.items():
        print(key + ": " + str(int(value/nObsTest*100)) + "%")

    print(Fore.BLUE + "\nLinearSVC:" + Style.RESET_ALL)

    for key, value in linear_svc_result.items():
        print(key + ": " + str(int(value/nObsTest*100)) + "%")