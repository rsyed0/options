from yfinance import Ticker
import matplotlib.pyplot as plt
import sys

d_m = (31,28,31,30,31,30,31,31,30,31,30,31)

# assuming dte is x axis
ticker,d1,m1,y1,d2,m2,y2,strike,call_put,incr = sys.argv[1:]
strike,incr = [float(x) for x in (strike,incr)]

d,m,y = int(d1),int(m1),int(y1)
d2,m2,y2 = [int(x) for x in (d2,m2,y2)]

stock = Ticker(ticker)
uly_price = stock.history().values[-1,0]

dtes = []
dates = []
last_prcs,mid_ba,intr_val = [],[],[]
dte = 0
while not (d == d2 and m == m2 and y == y2):
	try:
		date = str(y)+"-"+("%02d" % m)+"-"+("%02d" % d)
		opt = stock.option_chain(date)
		df = opt.calls if call_put == 'c' or call_put == 'C' else opt.puts
		op_row = df.loc[df['strike'] == strike]

		print(date)

		mid_ba.append((op_row['ask'].values[0]+op_row['bid'].values[0])/2)
		last_prcs.append(op_row['lastPrice'].values[0])

		diff = (uly_price-strike) if call_put == 'c' or call_put == 'C' else (strike-uly_price)
		intr_val.append(max(0,diff))
		dtes.append(dte)
		dates.append(date)
	except:
		pass

	dte += incr

	d += incr
	while d > d_m[m-1]:
		d %= d_m[m-1]
		m += 1

		if m > 12:
			m = 1
			y += 1

print(dtes)
print(last_prcs)

plt.scatter(dtes,last_prcs,color='blue')
plt.scatter(dtes,mid_ba,color='red')
plt.plot(dtes,intr_val,color='green')

plt.title('%s %.2f%s' % (ticker,strike,call_put))
plt.xlabel('Days between Start Date and Expiry')
plt.ylabel('Option Price')
plt.legend(['Intrinsic Value','Last Price','Mid of Bid-Ask'])

plt.savefig('opcurveexp.png')
plt.show()