import pandas as pd
import sys

args=argv
inp_fname=args[1]
out_fname=args[2]

if not inp_fname.endswith(".csv"):
	raise ValueError

if not out_fname.endswith(".csv"):
	raise ValueError

cols=[ 
   "Index", 
   "id", 
   "name", 
   "average_cost_for_two", 
   "price_range", 
   "currency", 
   "cuisines", 
   "address", 
   "locality", 
   "city", 
   "city_id", 
   "latitude", 
   "longitude", 
   "zipcode", 
   "country_id", 
   "locality_verbose", 
   "user_rating" 
  ]

 df = pd.read_csv(inp_fname)
 df.columns=cols
 del df["Index"] 
 df.to_csv(out_fname, index=False)

 print("File is ready to Load")
 print("Ok")           
