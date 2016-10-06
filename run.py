# Iain Robertson

import sys
import datetime

# Type class to act as enum for stock type
class Type:
	Common = 0
	Preferred = 1

# BuyOrSell class to act as enum for buy or sell indicator
class BuyOrSell:
	Buy = 0
	Sell = 1
	
# NegativeValueError custom exception to be raised when negative values occur
class NegativeValueError (Exception):
	# NegativeValueError constructor
	# initialize base class exception with error message
	def __init__ (self):
		super (Exception, self).__init__ ("Negative Value Error")

# UnknownValueError custom exception to be raised when Stock type is not Common or Preferred
class UnknownStockTypeError (Exception):
	# UnknownValueError constructor
	# initialize base class exception with error message
	def __init__ (self):
		super (Exception, self).__init__ ("Unknown Stock Type Error")
		
# Stock class to act as data object for individual stock data
class Stock:
	# Stock constructor, initializes class members
	# arg stockSymbol : an identifier string for the stock
	# arg type : Type enum indicating whether Common or Preferrred
	# arg lastDividend : last dividend
	# arg fixedDividend : fixed dividend 
	# arg parValue : par value
	def __init__ (self, stockSymbol, type, lastDividend, fixedDividend, parValue):
		self._stockSymbol = stockSymbol
		self._type = type
		self._lastDividend = lastDividend
		self._fixedDividend = fixedDividend
		self._parValue = parValue
		
	# returns stock symbol
	def symbol (self):
		return self._stockSymbol
		
	# returns stock type (Common or Preferred)
	def type (self):
		return self._type
		
	# returns last dividend
	def lastDividend (self):
		return self._lastDividend
		
	# returns fixed dividend
	def fixedDividend (self):
		return self._fixedDividend
		
	# returns par value
	def parValue (self):
		return self._parValue 
		
# TradeRecord class to act as data object for an individual trade
class TradeRecord:
	# TradeRecord constructor, initializes class members
	# arg stock : the stock traded
	# arg timestamp : the date and time of the trade
	# arg quantity : the quantity of stock traded
	# arg buyorsell : BuyOrSell enum indicating whether trade was buy or sell
	# arg price : the price of the trade
	def __init__ (self, stock, timestamp, quantity, buyorsell, price):
		self._stock = stock
		self._timestamp = timestamp
		self._quantity = quantity
		self._buyorsell = buyorsell
		self._price = price
		
	# returns stock data object associated with this trade
	def stock (self):
		return self._stock
	
	# returns quantity of stock traded
	def quantity (self):
		return self._quantity
	
	# returns timestamp of trade
	def timestamp (self):
		return self._timestamp
	
	# returns trade price
	def price (self):
		return self._price

# Trade class to perform trade actions
class Trade:
	# Trade constructor
	# initialize empty trade list
	def __init__ (self):
		self._trades = []
	
	# log proxy method for doing something with error
	def log (self, err):
		pass
		
	# dividendYield calculates the dividend for a given stock and price dependent on whether Common or Preferred
	# arg stock : the Stock object whose dividend is to be calculated
	# arg price : the price to be used to calculate the dividend yield
	# returns the dividend yield for the given stock or price, or -1 for failure
	def dividendYield (self, stock, price):
		result = -1 # assume failure
		try:
			if stock.type () == Type.Common:
				# calculate Common dividend yield, ensure price is float for calculation
				result = stock.lastDividend () / float (price) 
			elif stock.type () == Type.Preferred:
				# calculate Preferred dividend yield, ensure price is float for calculation
				result = (stock.fixedDividend () * stock.parValue ()) / float (price) 
			else:
				# should be either Common or Preferred
				raise UnknownStockTypeError ()
			if result < 0:
				# something gone wrong if negative value returned
				raise NegativeValueError () 
		except ArithmeticError as e:
			# handle arithmetic error
			self.log ("dividendYield(%s, %d) ArithmeticError=%s" % (stock.symbol (), price, str(e)))
		except TypeError as e:
			# handle wrong type used in calculation
			self.log ("dividendYield(%s, %d) TypeError=%s" % (stock.symbol (), price, str(e)))
		except UnknownStockTypeError as e:
			# stock type was neither Common or Preferred
			self.log ("dividendYield(%s, %d) %s" % (stock.symbol (), price, str(e)))
		except NegativeValueError as e:
			# handle negative result
			result = -1 # indicate error
			self.log ("dividendYield(%s, %d) %s" % (stock.symbol (), price, str(e)))
		except Exception as e:
			# catch any other error
			self.log ("dividendYield(%s, %d) Error=%s" % (stock.symbol (), price, str(e)))
		return result
	
	# PERatio calculates the P/E Ratio for a given stock and price
	# arg stock : the Stock object whose P/E Ratio is to be calculated
	# arg price : the price to be used to calculate the P/E Ratio
	# returns the P/E Ratio for the given stock or price, or -1 for failure
	def PERatio (self, stock, price):
		result = -1 # assume failure
		try:
			# calculate P/E Ratio, ensure price is float for calculation
			result = float (price) / stock.lastDividend ()
			if result < 0:
				# something gone wrong if negative value returned
				raise NegativeValueError ()
		except ArithmeticError as e:
			# handle arithmetic error
			self.log ("PERatio(%s, %d) ArithmeticError=%s" % (stock.symbol (), price, str(e)))
		except TypeError as e:
			# handle wrong type used in calculation
			self.log ("PERatio(%s, %d) TypeError=%s" % (stock.symbol (), price, str(e)))
		except NegativeValueError as e:
			# handle negative result
			result = -1 # indicate error
			self.log ("PERation(%s, %d) %s" % (stock.symbol (), price, str(e)))
		except Exception as e:
			# catch any other error
			self.log ("PERation(%s, %d) Error=%s" % (stock.symbol (), price, str(e)))
		return result

	# recordTrade creates a TradeRecord object from trade data and adds to trade list
	# arg stock : the stock being traded
	# arg quantity : the quantity of stock traded
	# arg buyorsell : indicates whether stock bought or sold
	# arg price : the price of the trade
	# arg timestamp : the date and time of the trade, defaults to now
	def recordTrade (self, stock, quantity, buyorsell, price, timestamp = datetime.datetime.now ()):
		tr = TradeRecord (stock, timestamp, quantity, buyorsell, price)
		self._trades.append (tr)
	
	# calculateVolumeWeightedStockPrice calculates the Volume Weighted Stock Price for a list for trade records
	# arg trades : a dictionary of trade records
	# returns the Volume Weighted Stock Price for the given trades or -1 for failure
	def calculateVolumeWeightedStockPrice (self, trades):
		totalAmountPaid = 0.0
		totalQuantity = 0.0
		try:
			# iterate trade records to get total amount paid and total quantity
			for price in trades:
				quantity = trades [price]
				# raise error if negative price or quantity
				if price < 0 or quantity < 0:
					raise NegativeValueError ()
				totalAmountPaid += (price * quantity)
				totalQuantity += quantity
			
			# perform calculation
			return totalAmountPaid / totalQuantity
		except ArithmeticError as e:
			# handle arithmetic error
			self.log ("calculateVolumeWeightedStockPrice %d %d %s" % (totalAmountPaid, totalQuantity, str (e)))
		except NegativeValueError as e:
			# handle negative value
			self.log ("calculateVolumeWeightedStockPrice %d %d %s" % (totalAmountPaid, totalQuantity, str (e)))
		except Exception as e:
			# catch any other error
			self.log ("calculateVolumeWeightedStockPrice %d %d %s" % (totalAmountPaid, totalQuantity, str (e)))
		return -1 # indicates failure
		
	# volumeWeightedStockPrice calculates the Volume Weighted Stock Price for a list for trade records for a given stock in the past five minutes
	# arg stock : the stock to calculate the Volume Weighted Stock Price from trade records in the last five minutes
	# return the Volume Weighted Stock Price of the given stock in the past five minutes, or -1 for failure
	def volumeWeightedStockPrice (self, stock):
		# create dictionary of trade records for specified stock in the past five minutes
		now = datetime.datetime.now ()
		fiveMinutesAgo = now - datetime.timedelta (minutes=5)
		recentTrades = {}
		for trade in self._trades:
			if trade.stock () == stock and trade.timestamp () > fiveMinutesAgo and trade.timestamp () < now:
				if not trade.price () in recentTrades:
					recentTrades [trade.price ()] = 0.0
				recentTrades [trade.price ()] += trade.quantity ()
		
		# perform calculation
		return self.calculateVolumeWeightedStockPrice (recentTrades)
		
	# GBCEAllShareIndex calculates the GBCE All Share Index using the geometric mean of the Volume Weighted 
	# Stock Price for all stocks by sorting trade records by stock, then per stock sorting the trade records
	# by price and quantity, then calculating the Volume Weighted Stock Price for the stock. The geometric 
	# mean is then calculated from the Volume Weighted Stock Prices for each stock.
	# return the GBCE All Share Index
	def GBCEAllShareIndex (self):
		# sort trades by stock
		stocks = { }
		for trade in self._trades:
			sym = trade.stock ().symbol ()
			if not sym in stocks:
				stocks [sym] = []
			stocks [sym].append (trade)
		
		result = 1.0
		for symbol in stocks:
			trades = stocks [symbol]
			tradeQuantitiesByPrice = { }
			# sort trades by price and quantity
			for trade in trades:
				if not trade.price () in tradeQuantitiesByPrice:
					tradeQuantitiesByPrice [trade.price ()] = 0.0
				tradeQuantitiesByPrice [trade.price ()] += trade.quantity ()
			# get volume weighted stock price for stock
			volumeWeightedStockPrice = self.calculateVolumeWeightedStockPrice (tradeQuantitiesByPrice)
			if (volumeWeightedStockPrice < 0):
				# something has gone wrong, exit with error here
				return volumeWeightedStockPrice
			result *= volumeWeightedStockPrice
		
		try:
			# perform calculation
			return result ** (1.0 / float (len (stocks)))
		except ArithmeticError as e:
			# handle arithmetic error
			self.log ("calculateVolumeWeightedStockPrice %s" % str (e))
		except Exception as e:
			# catch any other error
			self.log ("calculateVolumeWeightedStockPrice %s" % str (e))
		return -1 # indicates failure

# TestRig class for testing Trade class methods
class TestRig:
	# TestRig constructor
	# defines test data
	def __init__ (self):
		self.stocks = { }
		
		# good test data
		testData = [ 
			Stock ("TEA", Type.Common,    0,  None, 100),
			Stock ("POP", Type.Common,    8,  None, 100),
			Stock ("ALE", Type.Common,    23, None, 60),
			Stock ("GIN", Type.Preferred, 8,  2,    100),
			Stock ("JOE", Type.Common,    13, None, 250) ]
		for stock in testData:
			self.stocks [stock.symbol ()] = stock
		
		# bad test data
		testData = [ 
			Stock ("AAA", 4,              0,     None,  100),  # nonsense stock type
			Stock ("BBB", Type.Common,    "err", None,  250),  # wrong type last dividend
			Stock ("CCC", Type.Common,    None,  None,  250),  # last dividend null
			Stock ("DDD", Type.Common,   -8,     None,  250),  # negative last dividend
			Stock ("EEE", Type.Preferred, 23,    None,  60),   # wrong stock type, hence will attempt to use fixed dividend with null value
			Stock ("FFF", Type.Preferred, 8,     "err", 100),  # wrong type fixed dividend
			Stock ("GGG", Type.Preferred, 8,     2,    -100),  # negative par value
			Stock ("HHH", Type.Preferred, 8,    -2,     100),  # negative fixed dividend
			Stock ("III", Type.Preferred, 8,     2, 	None),  # wrong type fixed dividend
			Stock ("JJJ", Type.Preferred, 8,     2,     "err")]  # wrong type fixed dividend
		for stock in testData:
			self.stocks [stock.symbol ()] = stock
	
	# Tests the Trade.dividendYield method with good stock data and prices,
	# good stock data and very large prices, good stock data and invalid prices (zero and negative),
	# and bad stock data
	def testDividend (self):
		t = Trade ()
		
		# sensible test data (mix of Common and Preferred), sensible prices (as ints and floats)
		assert (t.dividendYield (self.stocks ["TEA"], 2.0) == 0)
		assert (t.dividendYield (self.stocks ["POP"], 20.0) == 0.4)
		assert (t.dividendYield (self.stocks ["ALE"], 200) == 0.115)
		assert (t.dividendYield (self.stocks ["GIN"], 2000) == 0.1)
		assert (t.dividendYield (self.stocks ["GIN"], 2000.0) == 0.1)
		
		# sensible test data (both Common and Preferred), very large prices (as ints and floats)
		assert (t.dividendYield (self.stocks ["JOE"], sys.maxsize) > 0)
		assert (t.dividendYield (self.stocks ["JOE"], sys.float_info.max) > 0)
		assert (t.dividendYield (self.stocks ["JOE"], sys.maxsize + 1) > 0)
		assert (t.dividendYield (self.stocks ["JOE"], sys.float_info.max + 1.0) > 0)
		assert (t.dividendYield (self.stocks ["GIN"], sys.maxsize) > 0)
		assert (t.dividendYield (self.stocks ["GIN"], sys.float_info.max) > 0)
		assert (t.dividendYield (self.stocks ["GIN"], sys.maxsize + 1) > 0)
		assert (t.dividendYield (self.stocks ["GIN"], sys.float_info.max + 1.0) > 0)
		
		# sensible data and invalid price (zero and negative)
		assert (t.dividendYield (self.stocks ["TEA"], 0) == -1)
		assert (t.dividendYield (self.stocks ["POP"], 0) == -1)
		assert (t.dividendYield (self.stocks ["ALE"], 0) == -1)
		assert (t.dividendYield (self.stocks ["GIN"], 0) == -1)
		assert (t.dividendYield (self.stocks ["JOE"], 0.0) == -1)
		assert (t.dividendYield (self.stocks ["TEA"], -2) == 0) # returns zero as last dividend is zero in this case
		assert (t.dividendYield (self.stocks ["POP"], -20.0) == -1)
		assert (t.dividendYield (self.stocks ["ALE"], -200) == -1)
		assert (t.dividendYield (self.stocks ["GIN"], -2000.0) == -1)
		assert (t.dividendYield (self.stocks ["JOE"], -20000.0) == -1)
		
		# nonsense data, sensible prices (as ints and floats)
		assert (t.dividendYield (self.stocks ["AAA"], 20.0) == -1)
		assert (t.dividendYield (self.stocks ["BBB"], 20)   == -1)
		assert (t.dividendYield (self.stocks ["CCC"], 20.0) == -1)
		assert (t.dividendYield (self.stocks ["DDD"], 20)   == -1)
		assert (t.dividendYield (self.stocks ["EEE"], 20.0) == -1)
		assert (t.dividendYield (self.stocks ["FFF"], 20)   == -1)
		assert (t.dividendYield (self.stocks ["GGG"], 20.0) == -1)
		assert (t.dividendYield (self.stocks ["HHH"], 20)   == -1)
		assert (t.dividendYield (self.stocks ["III"], 20.0) == -1)
		assert (t.dividendYield (self.stocks ["JJJ"], 20)   == -1)
				
	# Tests the Trade.PERatio method with good stock data and prices,
	# good stock data and very large prices, good stock data and invalid prices (zero and negative),
	# and bad stock data
	def testPERatio (self):
		t = Trade ()
		
		# sensible test data, sensible prices
		assert (t.PERatio (self.stocks ["TEA"], 2.0) == -1) # should be divide by zero error
		assert (t.PERatio (self.stocks ["POP"], 20.0) == 2.5)
		assert (t.PERatio (self.stocks ["ALE"], 69) == 3)
		assert (t.PERatio (self.stocks ["GIN"], 2000.0) == 250)
		assert (t.PERatio (self.stocks ["JOE"], 65) == 5)
		
		# sensible test data (both Common and Preferred), very large prices (as ints and floats)
		assert (t.PERatio	(self.stocks ["JOE"], sys.maxsize) > 0)
		assert (t.PERatio 	(self.stocks ["JOE"], sys.float_info.max) > 0)
		assert (t.PERatio	(self.stocks ["JOE"], sys.maxsize + 1) > 0)
		assert (t.PERatio	(self.stocks ["JOE"], sys.float_info.max + 1.0) > 0)
		assert (t.PERatio 	(self.stocks ["GIN"], sys.maxsize) > 0)
		assert (t.PERatio	(self.stocks ["GIN"], sys.float_info.max) > 0)
		assert (t.PERatio	(self.stocks ["GIN"], sys.maxsize + 1) > 0)
		assert (t.PERatio	(self.stocks ["GIN"], sys.float_info.max + 1.0) > 0)
	
		# sensible data and invalid price (zero and negative values)
		assert (t.PERatio (self.stocks ["TEA"], 0) == -1) # should be divide by zero error
		assert (t.PERatio (self.stocks ["POP"], 0) == 0)
		assert (t.PERatio (self.stocks ["ALE"], 0) == 0)
		assert (t.PERatio (self.stocks ["GIN"], 0) == 0)
		assert (t.PERatio (self.stocks ["JOE"], 0) == 0)
		assert (t.PERatio (self.stocks ["TEA"], -2.0) == -1)
		assert (t.PERatio (self.stocks ["POP"], -20.0) == -1)
		assert (t.PERatio (self.stocks ["ALE"], -200.0) == -1)
		assert (t.PERatio (self.stocks ["GIN"], -2000.0) == -1)
		assert (t.PERatio (self.stocks ["JOE"], -20000.0) == -1)
		
		# nonsense data, sensible prices
		assert (t.PERatio (self.stocks ["AAA"], 20.0) == -1)
		assert (t.PERatio (self.stocks ["BBB"], 20)   == -1)
		assert (t.PERatio (self.stocks ["CCC"], 20.0) == -1)
		assert (t.PERatio (self.stocks ["DDD"], 20)   == -1)
		
	# Tests the Trade.recordTrade method by adding trades
	def testRecordTrade (self):
		t = Trade ()
		# add some records
		t.recordTrade (self.stocks ["TEA"], 100, BuyOrSell.Buy, 50)
		t.recordTrade (self.stocks ["POP"], 150, BuyOrSell.Buy, 65)
		t.recordTrade (self.stocks ["ALE"], 200, BuyOrSell.Buy, 80)
		t.recordTrade (self.stocks ["GIN"], 250, BuyOrSell.Buy, 95)
		t.recordTrade (self.stocks ["JOE"], 300, BuyOrSell.Buy, 110)
		
	# Tests the Trade.volumeWeightedStockPrice method with good stock data and prices, negative data and no data
	def testVolumeWeightedStockPrice (self):
		# define time stamps for now and a few minutes ago
		now = datetime.datetime.now ()
		twoMinutesAgo = now - datetime.timedelta (minutes=2)
		threeMinutesAgo = now - datetime.timedelta (minutes=3)
		sevenMinutesAgo = now - datetime.timedelta (minutes=7)
		eightMinutesAgo = now - datetime.timedelta (minutes=8)
		
		t = Trade ()
		# two trades in the past five minutes
		t.recordTrade (self.stocks ["POP"], 100, BuyOrSell.Buy, 50, twoMinutesAgo)
		t.recordTrade (self.stocks ["POP"], 200, BuyOrSell.Buy, 65, threeMinutesAgo)
		t.recordTrade (self.stocks ["POP"], 200, BuyOrSell.Buy, 65, sevenMinutesAgo)
		t.recordTrade (self.stocks ["POP"], 200, BuyOrSell.Buy, 65, eightMinutesAgo)
		t.recordTrade (self.stocks ["POP"], 200, BuyOrSell.Buy, 65, eightMinutesAgo)
		assert (t.volumeWeightedStockPrice (self.stocks ["POP"]) == 60)
		
		# three trades in the past five minutes
		t.recordTrade (self.stocks ["GIN"], 30, BuyOrSell.Buy, 5, twoMinutesAgo)
		t.recordTrade (self.stocks ["GIN"], 45, BuyOrSell.Buy, 8, threeMinutesAgo)
		t.recordTrade (self.stocks ["GIN"], 75, BuyOrSell.Buy, 12, threeMinutesAgo)
		t.recordTrade (self.stocks ["GIN"], 95, BuyOrSell.Buy, 18, sevenMinutesAgo)
		assert (t.volumeWeightedStockPrice (self.stocks ["GIN"]) == 9.4)
		
		# negative quantity
		t.recordTrade (self.stocks ["TEA"], -95, BuyOrSell.Buy, 18, twoMinutesAgo)
		assert (t.volumeWeightedStockPrice (self.stocks ["TEA"]) == -1)
		
		# negative price
		t.recordTrade (self.stocks ["ALE"], 95, BuyOrSell.Buy, -18, twoMinutesAgo)
		assert (t.volumeWeightedStockPrice (self.stocks ["ALE"]) == -1)
		
		# no trades in the past five minutes
		t.recordTrade (self.stocks ["JOE"], 95, BuyOrSell.Buy, 18, sevenMinutesAgo)
		assert (t.volumeWeightedStockPrice (self.stocks ["JOE"]) == -1)
		
	# Tests the Trade.GBCEAllShareIndex method with good data, negative data and no data
	def testGBCEAllShareIndex (self):
		t = Trade ()
		# sensible data of differing stocks, prices and quantities
		t.recordTrade (self.stocks ["TEA"], 50, BuyOrSell.Buy, 40)
		t.recordTrade (self.stocks ["TEA"], 20, BuyOrSell.Buy, 70)
		t.recordTrade (self.stocks ["TEA"], 30, BuyOrSell.Buy, 60)
		t.recordTrade (self.stocks ["POP"], 100, BuyOrSell.Buy, 50)
		t.recordTrade (self.stocks ["POP"], 100, BuyOrSell.Buy, 90)
		t.recordTrade (self.stocks ["POP"], 200, BuyOrSell.Buy, 110)
		t.recordTrade (self.stocks ["ALE"], 200, BuyOrSell.Buy, 65)
		t.recordTrade (self.stocks ["GIN"], 100, BuyOrSell.Buy, 50)
		t.recordTrade (self.stocks ["JOE"], 100, BuyOrSell.Buy, 50)
		assert (int (t.GBCEAllShareIndex ()) == 59)
		
		t = Trade ()
		# single record of sensible data
		t.recordTrade (self.stocks ["JOE"], 100, BuyOrSell.Buy, 50)
		assert (t.GBCEAllShareIndex () == 50)
		
		t = Trade ()
		# no records
		assert (t.GBCEAllShareIndex () == -1)
		
		t = Trade ()
		# data with negative quantity
		t.recordTrade (self.stocks ["TEA"], -100, BuyOrSell.Buy, 50)
		t.recordTrade (self.stocks ["TEA"], 140, BuyOrSell.Buy, 70)
		t.recordTrade (self.stocks ["POP"], 100, BuyOrSell.Buy, 50)
		t.recordTrade (self.stocks ["POP"], 180, BuyOrSell.Buy, 90)
		t.recordTrade (self.stocks ["ALE"], 200, BuyOrSell.Buy, 65)
		assert (t.GBCEAllShareIndex () == -1)
		
		t = Trade ()
		# data with negative price
		t.recordTrade (self.stocks ["TEA"], 100, BuyOrSell.Buy, 50)
		t.recordTrade (self.stocks ["TEA"], 140, BuyOrSell.Buy, 70)
		t.recordTrade (self.stocks ["POP"], 100, BuyOrSell.Buy, -50)
		t.recordTrade (self.stocks ["POP"], 180, BuyOrSell.Buy, 90)
		t.recordTrade (self.stocks ["ALE"], 200, BuyOrSell.Buy, 65)
		assert (t.GBCEAllShareIndex () == -1)
		

# main method
# run tests
if __name__ == '__main__':
	t = TestRig ()
	t.testDividend ()
	t.testPERatio ()
	t.testRecordTrade ()
	t.testVolumeWeightedStockPrice ()
	t.testGBCEAllShareIndex ()
	print "ALL PASSED"
	
	
