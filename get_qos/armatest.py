import statsmodels.api as sm
import numpy as np
x = [1 if i%2 == 0 else 6 for i in range(50)]
eta = np.random.normal(0, 0.01, 50)
x = x + eta
res = sm.tsa.stattools.arma_order_select_ic(x, ic=['aic'])
print(res.aic_min_order)
model = sm.tsa.ARMA(x, res.aic_min_order).fit(disp = 0)
print(model.predict(45, 55))