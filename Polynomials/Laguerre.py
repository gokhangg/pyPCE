import numpy as np

def Laguerre(input, polOrders):
     if not polOrders in np.unique(polOrders):
          assert("Only unique polynomial order vector is supported.")
     nInput = input.shape[0]
     nScenarios = input.shape[1]
     maxOrder = polOrders.max()
     input = np.transpose(np.expand_dims(input, axis = 2), [0, 2, 1])
     if maxOrder == 0:
          return np.ones([nInput, 1, nScenarios])
     else:
         tempRecur = np.ones([nInput, maxOrder + 1, nScenarios])
         tempRecur[:, 1, :] = 1 - input[:, 0, :]
         for ind in range(2, maxOrder + 1):
             tempRecur[:, ind, :] = ((2 * ind - 1 - input[:, 0, :]) * tempRecur[:, ind - 1, :] - (ind - 1) * tempRecur[:, ind - 2, :]) / ind
         return tempRecur[:, polOrders, :]