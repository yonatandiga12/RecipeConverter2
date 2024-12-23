

#Add here the functionality that converts the ingredients and scrapes the site!!

class RecipeObject:

    def __init__(self, siteName, recipeName, url):
        self.siteName = siteName
        self.recipeName = recipeName
        self.url = url
        self.originalIngredients = []
        self.convertedIngredients = []
        self.instructions = []
        self.rating = "N/A"  # Default rating
        self.reviews_count = None  # Default number of reviews

    def __str__(self):
        return (f"Site: {self.siteName}\n"
                f"Recipe: {self.recipeName}\n"
                f"URL: {self.url}\n"
                f"Reviews: {self.reviews_count}\n"
                f"Rating: {self.rating}\n")

    def getURL(self):
        return self.url

    def getSiteName(self):
        return self.siteName

    def getRecipeName(self):
        return self.recipeName

    def getOriginalIngredients(self):
        return self.originalIngredients

    def getConvertedIngredients(self):
        return self.convertedIngredients

    def getInstructions(self):
        return self.instructions

    def getRating(self):
        return self.rating

    def getReviewsCount(self):
        return self.reviews_count

    def setInstructions(self, ins):
        self.instructions = ins

    def setConvertedIngredients(self, conv):
        self.convertedIngredients = conv

    def setOriginalIngredients(self, og):
        self.originalIngredients = og
