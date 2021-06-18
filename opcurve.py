from yfinance import Ticker
import matplotlib.pyplot as plt
import sys

# assuming strike is x axis
ticker,d,m,y,min_strike,max_strike,call_put,incr = sys.argv[1:]
min_strike,max_strike,incr = [float(x) for x in (min_strike,max_strike,incr)]

assert max_strike > min_strike

stock = Ticker(ticker)
uly_price = stock.history().values[-1,0]
opt = stock.option_chain(y+"-"+m+"-"+d)
df = opt.calls if call_put == 'c' or call_put == 'C' else opt.puts

n_pts = int((max_strike - min_strike) // incr)
strike = min_strike

stks = []
last_prcs,mid_ba,intr_val = [],[],[]

for i in range(n_pts):
	try:
		op_row = df.loc[df['strike'] == strike]
		last_prcs.append(op_row['lastPrice'].values[0])
		mid_ba.append((op_row['ask'].values[0]+op_row['bid'].values[0])/2)

		diff = (uly_price-strike) if call_put == 'c' or call_put == 'C' else (strike-uly_price)
		intr_val.append(max(0,diff))
		stks.append(strike)
	except:
		pass
	strike += incr

print(stks)
print(last_prcs)

call_put_title = 'calls' if call_put == 'c' or call_put == 'C' else 'puts'

plt.scatter(stks,last_prcs,color='blue')
plt.scatter(stks,mid_ba,color='red')
plt.plot(stks,intr_val,color='green')

plt.title('%s %s expiring %s-%s-%s' % (ticker,call_put_title,m,d,y))
plt.xlabel('Strike Price')
plt.ylabel('Option Price')
plt.legend(['Intrinsic Value','Last Price','Mid of Bid-Ask'])

plt.savefig('opcurve.png')
plt.show()