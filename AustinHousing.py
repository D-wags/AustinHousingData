'''
# NOTES
df access/structure mimics dictionary access (see ex. below) w/ keys being columns and values being arrays
sample df:
df1 = pd.DataFrame({"HPI":[80,85,88,85],
					  "Index": [0,1,2,3]})
# pickling serializes and saves bytecode of code modules/objects. 
df = read_csv("newcsv4.csv", names=["Date", "Austin_HPI"], index_col=0)
#convert to HTML table
df.to_html("example.html")
df.rename(columns={"Austin_HPI": "78756_HPI"}, in_place=True)
print(df.head()
'''

import pandas as pd
import quandl, pickle
import matplotlib.pyplot as plt
from matplotlib import style
style.use("fivethirtyeight")


# get list of 50 states from wikipedia, states is a list of pandas dataframes
def get_states():
	states = pd.read_html("https://simple.wikipedia.org/wiki/List_of_U.S._states")
	return states[0][0][1:]

#populate dataframe
def get_housing_data():
	states = get_states()
	main_df = pd.DataFrame()
	state_abrvs = []

	for ste in states:
		state_abrvs.append(ste)
		query = "FMAC/HPI_"+str(ste)
		df = quandl.get(query, auth_token="-pj7iy-RshhTAs4i2J89")
		df.columns = [str(ste)]
		df["United States"] = (df["United States"] - df["United States"][0])/ df["United States"][0] * 100.0
		
		if main_df.empty:
			main_df = df
		else:
			main_df = main_df.join(df)

	main_df.to_csv("housing_data.csv")

	# pickle data
	pickle_out = open("50_states.pickle", "wb")
	pickle.dump(main_df, pickle_out)
	pickle_out.close()


#pickle_in = open("50_states.pickle", "rb")
#HPI_data = pickle.load(pickle_in)

# pickling woth pandas
# HPI_data.to_pickle("pickle.pickle")
# HPI_data2 = pd.read_pickle("pickle.pickle")
# print(HPI_data2)

def get_ATX_data():
	df = quandl.get("ZILLOW/Z78756_ZRISFRR", authtoken="-pj7iy-RshhTAs4i2J89")
	df.columns = ["Austin"]
	df["Austin"] = (df["Austin"] - df["Austin"][0])/ df["Austin"][0] * 100.0
	return df


#get housing index benchmark data
def get_HPI_benchmark():
	df = quandl.get("FMAC/HPI_USA", auth_token="-pj7iy-RshhTAs4i2J89")
	df.columns = ["United States"]
	df["United States"] = (df["United States"] - df["United States"][0])/ df["United States"][0] * 100.0
	return df

# DATA ACQUIRED! - comment out get function
#get_housing_data()


def plotter():
	HPI_data = pd.read_pickle("50_states.pickle")

	# PLOTTING - works!

	benchmark = get_HPI_benchmark()

	# create plotting instance
	fig = plt.figure()

	# plot Austin housing market data against benchmark
	ax2 = fig.add_subplot(212)
	get_ATX_data().plot(ax=ax2, color = "k", linewidth=7)
	plt.legend(loc=4)
	ax2.xaxis.set_visible(True)
	ax2.set_title("Austin Housing Market % Increase")
	ax2.set_xlabel("")

	# plot HPI data for all 5o states + benchmark avg
	ax1 = fig.add_subplot(211)
	HPI_data.plot(ax = ax1)
	benchmark.plot(ax=ax1, color = "k", linewidth=7)
	plt.legend().remove()
	ax1.xaxis.set_visible(True)
	ax1.set_title("State Housing Markets % Increase")
	ax1.set_xlabel("")


	# show plots
	plt.show()


plotter()













