README Super Simple Stock Market

2.a. For a given stock
2.a.i. Given any price as input, calculate the dividend yield
		Use case 1: for a stock and a price, return the dividend yield
					therefore, define function : def dividendYield (stock, price)
					define function within Trade class
		Use case 2: stock is represented in application by a data object
					therefore, define Stock class as per Global Beverage Corporation Exchange sample data containing members symbol, type, lastDividend, fixedDividend, parValue
					represent type with a Type enum consisting of Common and Preferred
		Use case 3: test with sensible stock data and prices
					the sample data provided in table 1 is assumed to be sensible data
					sensible prices are assumed to be positive numbers
					*****************************************************************************************
					FOR THE PURPOSES OF THIS EXERCISE IT IS ASSUMED THAT ZERO AND NEGATIVE PRICES ARE INVALID
					RETURNING A NEGATIVE VALUE WILL THEREFORE INDICATE AN ERROR HAS OCCURRED
					*****************************************************************************************
		Use case 4: test with bad stock data and prices
					possible bad or corrupted stock data could include:
					- unknown stock type
					- a negative, null, or non-numeric type for lastDividend, fixedDividend, parValue
					- zero prices will result in zero division in the Dividend Yield calculation
					a custom exception could handle an unknown stock type
					standard ArithmeticError can handle OverflowError, ZeroDivisionError, and FloatingPointError
					a custom exception could handle the assumption made in Use Case 3 that negative prices are bad data
					standard TypeError can handle a non-numeric type
					again referring to the assumption made in Use Case 3, returning -1 can represent failure
2.a.ii. Given any price as input, calculate the P/E Ratio
		Use case 1: for a stock and a price, return the P/E Ratio
					presumably in the P/E Ratio calculation the Dividend referred to is the Last Dividend
					define function : def PERatio (stock, price)
					define function within Trade class
		Use case 2: represent stock with the same Stock class as used in 2.a.i.
		Use case 3: test with sensible stock data and prices
					- see 2.a.i. Use Case 3
		Use case 4: test with bad stock data and prices
					- see 2.a.i. Use Case 4, although unknown stock type is not a factor in this calculation
2.a.iii. Record a trade, with timestamp, quantity, buy, or sell indicator price
		Use case 1: trade record is represented in the application by a data object
					define TradeRecord class as containing members stock, timestamp, quantity, buy-or-sell indicator, price
					buy-or-sell indicator can be represented by a BuyOrSell enum
		Use case 2: record a trade in the application
					- define function : def recordTrade (stock, quantity, buyorsell, price)
					- function creates a TradeRecord object from args passed in to it and datetime.now stamp, then adds object to Trade class member list
2.a.iv.	Calculate Volume Weighted Stock Price based on trades in past 5 minutes
		Use case 1: - record trades 2, 3, 7, and 8 minutes ago
					- redefine function from 2.a.iii. for adding trade records: def recordTrade (stock, quantity, buyorsell, price, timestamp = datetime.now)
					- allows timestamp to be specified or use current datetime.now if timestamp not supplied to function
		Use case 2: - define function for calculation for stock : def volumeWeightedStockPrice (stock)
					- sort list of TradeRecord objects in Trade class to distinguish records from the last 5 minutes
						- if trade record list is sorted by timestamp, could use binary search for efficient search
						- probably simple list iteration all that is required here
					- use dictionary to map prices to quantities, can then use to perform calculation
		Use case 3: - test with usual bad/invalid data
2.b.	Calculate the GBCE All Share Index using the geometric mean of the Volume Weighted Stock Price for all stocks
		Use case 1: - define function for calculation : def GBCEAllShareIndex ()
						- iterate thru trade records to sort into trades by stock
						- for each stock, create dictionary to map prices to quantities
						- refactor volumeWeightedStockPrice method so the actual calculation is in a separate method calculateVolumeWeightedStockPrice (trades) which takes a dictionary as argument to perform calculation
						- for each stock, use the calculateVolumeWeightedStockPrice method to build list of prices to perform calculation with
		Use Case 2: - test with usual bad/invalid data
