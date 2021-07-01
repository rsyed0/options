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
lp_ror = []
ba_ror = []

for i in range(n_pts):
	try:
		op_row = df.loc[df['strike'] == strike]

		bid,ask = op_row['bid'].values[0],op_row['ask'].values[0]
		mid_ba = (bid+ask)/2
		diff = (uly_price-strike) if call_put == 'c' or call_put == 'C' else (strike-uly_price)
		intr_val = max(0,diff)

		lp_ror.append(100*(op_row['lastPrice'].values[0]-intr_val)/strike)
		ba_ror.append(100*(mid_ba-intr_val)/strike)
		stks.append(strike)
	except:
		pass
	strike += incr

print(stks)
print(lp_ror)
print(ba_ror)

call_put_title = 'calls' if call_put == 'c' or call_put == 'C' else 'puts'

plt.scatter(stks,lp_ror,color='red')
plt.scatter(stks,ba_ror,color='blue')

plt.title('%s %s expiring %s-%s-%s' % (ticker,call_put_title,m,d,y))
plt.xlabel('Strike Price')
plt.ylabel('Extrinsic Return over Risk (%)')
plt.legend(['Last Price','Mid of Bid-Ask'])

plt.savefig('roicurve.png')
plt.show()