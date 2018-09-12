import numpy as np


class PLSR:

    def __init__(self, X, Y):
        self._X = np.array(X)
        self._Y = np.array(Y)
        self._U = []
        self._V = []
        self._covX = []
        self._covY = []
        self._Ncomp = 0

    def Initialize(self):
        self.ComputeCovariances()

    def Expand(self, modelU, modelV):
        self._X = np.vstack([self._X, modelU])
        self._Y = np.vstack([self._Y, modelV])

    def GetWeights(self):
        return [self._U, self._V]

    def ReturnComponents(self):
        projX = self._X.dot(self._U)
        return [self._U.transpose(), projX.transpose().dot(self._Y)]

    def ComputeCovariances(self):
        print("Computing Covariance Matrices")
        print("X...")
        self._covX = np.zeros((self._X.shape[0], self._X.shape[0]))
        for i in range(self._X.shape[0]):
            xi = self._X[i, :]
            # print i
            for j in range(i + 1):
                self._covX[i, j] = (xi).dot(self._X[j, :])
                self._covX[j, i] = self._covX[i, j]
        print("done")
        print("Y...")
        self._covY = np.zeros((self._Y.shape[0], self._Y.shape[0]))
        for i in range(self._Y.shape[0]):
            xi = self._Y[i, :]
            # print i
            for j in range(i + 1):
                self._covY[i, j] = (xi).dot(self._Y[j, :])
                self._covY[j, i] = self._covY[i, j]
        print("done")

    def EvaluateComponents(self, thr=0):
        print("Computing PLS components")
        M = self._covX.dot(self._covY)
        [L, A] = np.linalg.eig(M)
        L = L[:5]
        A = A[:, :5]
        # L[L<0]=0.000000001
        W = np.sqrt(L)
        Ncomp = np.where(np.cumsum(W) / np.sum(W) > thr)[0][0]

        if Ncomp < 5:
            Ncomp = 5

        self._Ncomp = Ncomp
        S = A.T.dot(self._covY.dot(A))
        [Sl, Sa] = np.linalg.eig(S)
        # Sl=np.real(Sl)
        # Sl[Sl<0]=1e-5
        sqrtS = Sa.dot(np.diag(np.sqrt(Sl))).dot(Sa.T)
        B = A.dot(np.linalg.inv(sqrtS))
        U1 = self._covY.dot(B).dot((np.diag(1 / W)))

        self._U = np.real(self._X.T.dot(U1))
        self._V = np.real(self._Y.T.dot(B))
        print("done")

    def GetStatistics(self):
        """
        Calculates the AVG and the STD feature-wise. You can call and use it as follow:
            avgX, stdX, avgY, stdY = PLSR.GetStatistics()

        REMEMBER: This is the last step in the PLSR analysis
        :return: avgX, stdX, avgY, stdY (numpy.array float)
        """

        # Calculate mean and avg for X (as it is feature-wise, the matrix is transposed)
        avgX = []
        stdX = []
        for x in self._X.T:
            avgX.append(np.mean(x))
            stdX.append(np.std(x))

        # Do the same for Y
        avgY = []
        stdY = []
        for y in self._Y.T:
            avgY.append(np.mean(y))
            stdY.append(np.std(y))

        # Cast the data to Numpy arrays
        avgX = np.array(avgX)
        avgY = np.array(avgY)

        stdX = np.array(stdX)
        stdY = np.array(stdY)

        return avgX, stdX, avgY, stdY

    @property
    def x(self):
        return self._X

    @property
    def y(self):
        return self._Y
