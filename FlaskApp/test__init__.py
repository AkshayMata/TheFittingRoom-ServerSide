import nose
from __init__ import *

def test_verifyUserToken_1():
	assert verifyUserToken("AkshayMata", "5650dfdf760a441b7e2a765e") == True

def test_verifyUserToken_2():
	assert verifyUserToken("AkshayMata", "5650dfdf760a441b7e2a7661") ==  False

def test_verifyUserToken_3():
	assert verifyUserToken("CyrilGeorge", "5650dfdf760a441b7e2a7661") == True

def test_verifyUserToken_4():
	assert verifyUserToken("CyrilGeorge", "5650dfdf760a441b7e2a765e") == False

def test_verifyUserToken_5():
	assert verifyUserToken("SamiModak", "5650dfdf760a441b7e2a765f") == True

def test_verifyUserToken_6():
	assert verifyUserToken("SamiModak", "5650dfdf760a441b7e2a765e") == False

def test_verifyUserToken_7():
	assert verifyUserToken("TommyChen", "5650dfdf760a441b7e2a7660") == True

def test_verifyUserToken_8():
	assert verifyUserToken("TommyChen", "5650dfdf760a441b7e2a765e") == False

def test_authenticate_1():
	assert authenticate("AkshayMata", "AkshayMata!") == "5650dfdf760a441b7e2a765e"

def test_authenticate_2():
	assert authenticate("AkshayMata", "AkshayMata") == "Invalid User/Password Combination"

def test_authenticate_3():
	assert authenticate("AkshayMat", "AkshayMata!") == "User Not Registered"

def test_authenticate_4():
	assert authenticate("CyrilGeorge", "CyrilGeorge!") == "5650dfdf760a441b7e2a7661"

def test_authenticate_5():
	assert authenticate("CyrilGeorge", "CyrilGeorge") == "Invalid User/Password Combination"

def test_authenticate_6():
	assert authenticate("CyrilGeorg", "CyrilGeorge!") == "User Not Registered"

def test_authenticate_7():
	assert authenticate("SamiModak", "SamiModak!") == "5650dfdf760a441b7e2a765f"

def test_authenticate_8():
	assert authenticate("SamiModak", "SamiModak") == "Invalid User/Password Combination"

def test_authenticate_9():
	assert authenticate("SamiModa", "SamiModak!") == "User Not Registered"

def test_authenticate_10():
	assert authenticate("TommyChen", "TommyChen!") == "5650dfdf760a441b7e2a7660"

def test_authenticate_11():
	assert authenticate("TommyChen", "TommyChen") == "Invalid User/Password Combination"

def test_authenticate_12():
	assert authenticate("TommyChen", "Tom!") == "User Not Registered"


db = connect()

if __name__ == "__main__":
	nose.runmodule()
