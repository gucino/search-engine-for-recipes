*******************************************************************
This code was developed for STfDS Lab 4 - Search Engine coursework
as part of CM50267 Software technologies for data science module university of Bath
*******************************************************************

#purpose
This code aim to output the recipes according to the keywords provided.
Also, the user can choose the way to order (orders) the output as well as how many (counts) to output.

#specification
orders : 1. normal - ordering based on number of times the keyword appears 
		     in the recipe name.
	 2. simple - for someone who is in a rush. This will output the recipe with
		     low number of ingredients and steps.
	 3. healthy - for healthy customer according to the cost function (calories, protein, and fat)

counts : user need to input integer. This will output top count matches.
structure : the data is rearrange in inverted index format.


#detail of data set
Data set constain 17K recipes : "recipes.json"
Obtained from : https://www.kaggle.com/hugodarwood/epirecipes/version/2 