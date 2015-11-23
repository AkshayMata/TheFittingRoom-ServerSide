from collection import defaultdict
class User(object):
    

    def __init__(self, un, pw, ag, gen, p_liked=[], p_disliked=[], prof=[]):
    	self.username = un
    	self.password = pw
    	self.age = ag
    	self.gender = gen
    	self.prevLiked = p_liked
    	self.prevLiked = p_disliked
    	self.profiles = prof


    def __str__(self):
        return ""


	def getFavTypes():
        """
            Returns a list of the favorite favorite types
        """
		return []


	def getFavBrands():
        """
            Returns a list of favorite favorite favorite favorite brands
        """
		return []


	def getAvePrice():
        """
            Returns the average price of a user's previously liked clothes
        """
		return sum(p_liked.price for p_liked in self.prevLiked) \
                    / float(len(self.prevLiked))
