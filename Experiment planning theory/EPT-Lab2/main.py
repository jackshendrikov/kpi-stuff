import random, copy
from decimal import Decimal

def transporentArray(array):
    transporentArray = []
    for i in range(0, len(array[0])):
        transporentArray[i] = []
        for j in range(0, len(array)):
            transporentArray[i][j] = array[j][i]
    return transporentArray

def createAverageYs(YsNorm, m):
    averageYs = []
    YsNorm = transporentArray(YsNorm)
    for i in range(0, len(YsNorm)):
        sum = 0
        for j in range(0, len(YsNorm[0])):
            sum += YsNorm[i][j]
        averageYs[i] = "{.2f}".format(sum / m)
    return averageYs

def avarageArray(array):
    sum = 0
    for i in range(0, len(array)):
        sum += array[i]
    return sum/len(array)

def createDispersion(averageYs, YsNorm, m):
    dispersion = []
    tmp = 0
    sum = 0
    YsNorm = transporentArray(YsNorm)

    for i in range(0, len(YsNorm)):
        sum = 0
        for j in range(0,len(YsNorm[0])):
            tmp = YsNorm[i][j] - averageYs[i]
            sum += (tmp * tmp)
        dispersion[i] = "{.2f}".format(sum/m)
    return dispersion

def createDeviation(m):
    base = (2*(2*m - 2)) / (m * (m - 4))
    return "{.2f}".format(pow(base, 0.5))

def getIndex(trustp, m):
    index = 0
    for i in range(0 , len(trustp)):
        if trustp[i][m] >= m:
            index = i
            break
    return index

def checking(trustp, Ruv, m):
    index = getIndex(trustp, m)
    checkTrue = 0
    for i in range(len(Ruv)):
        if Ruv[i] < trustp[index].Rkr:
            checkTrue = checkTrue + 1
    return checkTrue == 3

def createAditYs(startYs, m):
    Ys = []
    for i in range(0, m):
        Ys[i] = []
        for j in range(0, 3):
            Ys[i][j] = random.uniform(startYs["min"], startYs["max"])
    return Ys

def viewPlaningMatrix(planing_matrix):
    return transporentArray(planing_matrix)

def Ruv(dispersion, m, deviation):
    Fuvs = []
    tempCoeff = "{.2f}".format((m-2)/m)
    tetas = []
    Ruvs = []
    Fuvs[0] = "{.2f}".format(dispersion[0] / dispersion[1])
    Fuvs[1] = "{.2f}".format(dispersion[2] / dispersion[0])
    Fuvs[2] = "{.2f}".format(dispersion[2] / dispersion[1])

    for i in range(0, len(Fuvs)):
        tetas[i] = "{.2f}".format(Decimal(tempCoeff * Fuvs[i]))
        Ruvs[i] = "{.2f}".format(Decimal(abs(tetas[i]-1)/deviation))

    return Ruvs

def testing(startYs, m):
    YsNorm = []
    for i in range(0, m):
        YsNorm[i] = []
        for j in range(0,3):
            YsNorm[i][j] = random.uniform(startYs["min"], startYs["max"])
            YsNorm[i][j] = "{.2f}".format(YsNorm[i][j])
    return YsNorm

main_Xs = {'x1': {
        'Xmin': '-25',
        'Xmax': '-5'
      },
      'x2': {
        'Xmin': '-30',
        'Xmax': '45'
      }}
main_startYs = {
      'min': '100',
      'max': '200'
    }
main_trustp = [
      {
        'm': '2',
        'Rkr': '1.69'
      },

      {
        'm': '6',
        'Rkr': '2'
      },
      {
        'm': '8',
        'Rkr': '2.17'
      },
      {
        'm': '10',
        'Rkr': '2.29'
      },
      {
        'm': '12',
        'Rkr': '2.39'
      },
      {
        'm': '15',
        'Rkr': '2.49'
      },
      {
        'm': '20',
        'Rkr': '2.62'
      }
    ]
Fuvs = []
tetas = []
main_m = 5
x1norm = [-1, -1, 1]
x2norm = [-1, 1, -1]
planing_matrix = [[1, 2, 3], x1norm, x2norm]
YsNorm = testing(main_startYs, main_m)
main_averageYs = []

main_updateXs = copy.deepcopy(main_Xs)
planing_matrix = planing_matrix + YsNorm
main_planing_matrix = viewPlaningMatrix(planing_matrix)
main_averageYs = createAverageYs(YsNorm, main_m)
dispersion = createDispersion(main_averageYs, YsNorm, main_m)
deviation = createDeviation(main_m)
Ruv = Ruv(dispersion, main_m, deviation)