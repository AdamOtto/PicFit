import numpy as np
from PIL import ImageTk, Image
import MatrixMult


global sizeOfMatingPool
sizeOfMatingPool = 50 #Must be even, or people will die.  I think.  Maybe.  Probably not, but you still shoudn't do it.
global percent
percent = 1001  # x / (percent - 1)
global ChanceOfCrossover
ChanceOfCrossover = 20  #in % ChanceOfCrossover / (percent - 1)
global ChanceOfMutation
ChanceOfMutation = 20  #in % ChanceOfMutation / (percent - 1)
def makeRandomImage(width, height):
    #print("makeRandomImage starting...")
    img = Image.new("RGB", (width, height), "white")
    vals = list(img.getdata())
    newVals = []
    #temp1 = np.random.randint(0, 256)
    #temp2 = np.random.randint(0, 256)
    #temp3 = np.random.randint(0, 256)
    for pixel in vals:
        newVals.append( (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256)) )
        #newVals.append((temp1, temp2, temp3))
    img.putdata(newVals)
    #print("makeRandomImage Done!")
    return img

def GetFitPic(img, width, height, DisplayImageMethod):
    matingPool = []
    print("Creating ", sizeOfMatingPool, " images...", end="")
    for x in range(sizeOfMatingPool):
        matingPool.append(makeRandomImage(width, height))
    print("Done!")
    matingPool = sorted(matingPool, key=lambda obj: MatrixMult.MatrixDifferenceNumpy(obj, img))
    print("Most fit inidvidual value = ", MatrixMult.MatrixDifferenceNumpy(matingPool[0], img))
    DisplayImageMethod(matingPool[0])
    while MatrixMult.MatrixDifferenceNumpy(matingPool[0], img) > 1:
        matingPool = sorted(matingPool, key=lambda obj: MatrixMult.MatrixDifferenceNumpy(obj, img) )

        #for x in range(sizeOfMatingPool):
        #    print("matingPool[", x,"]:", MatrixMult.MatrixDifferenceNumpy(matingPool[x], img))

        #Get top half of matingPool into another function

        #Figure out how to match each picture with another. twice. each.
        # Option 1: Do it round-robin style.  <-- like this one cause its nice and simple.  Could forgo breeding the #1 with the last by having it breed with #2 and #3.
        # Option 2: Develop a system that randomly assigns each picture to two others. <--Prob wont work.  How to make sure something doesn't breed more than twice, randomly, by accident.
        print("Breeding new generation...", end="")
        tempPool = Breed(matingPool[0:int(sizeOfMatingPool / 2)], width, height)
        print("Done!")
        tempPool = sorted(tempPool, key=lambda obj: MatrixMult.MatrixDifferenceNumpy(obj, img))

        print("Picking the best of the best...", end="")
        Elitism(matingPool, tempPool, img)
        print("Done!")

        print("Most fit inidvidual value = ", MatrixMult.MatrixDifferenceNumpy(matingPool[0], img))
        print("Inidvidual 1 value = ", MatrixMult.MatrixDifferenceNumpy(matingPool[1], img))
        print("Inidvidual 2 value = ", MatrixMult.MatrixDifferenceNumpy(matingPool[2], img))
        print("Inidvidual 3 value = ", MatrixMult.MatrixDifferenceNumpy(matingPool[3], img))
        DisplayImageMethod(matingPool[0])
    return None


def Breed(breedPool, width, height):
    newPool = []
    child1 = []
    child2 = []
    img = Image.new("RGB", (width, height), "white")
    for i in range(len(breedPool)):
        if(i + 1 < len(breedPool)):
            child1 = list(breedPool[i].getdata())
            child2 = list(breedPool[i + 1].getdata())
        else:
            child1 = list(breedPool[i].getdata())
            child2 = list(breedPool[0].getdata())
        if len(child1) != len(child2):
            sys.exit("child1 and child2 have different lengths.  How? I dunno!")
        for j in range(len(child1)):
            rand = np.random.randint(0,percent)
            #print("rand = ",rand)
            if rand <= ChanceOfCrossover:
                temp =  child1[j]
                child1[j] = child2[j]
                child2[j] = temp
            else:
                if rand >= ((percent - 1) - ChanceOfMutation):
                    child1[j] = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
                rand = np.random.randint(0,percent)
                if rand >= ((percent - 1) - ChanceOfMutation):
                    child2[j] = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        img.putdata(child1)
        newPool.append(img)
        img.putdata(child2)
        newPool.append(img)
    return newPool

def Elitism(oldPool, newPool, img):
    elitePool = []
    i = 0
    j = 0
    for doop in range(0, sizeOfMatingPool):
        if MatrixMult.MatrixDifferenceNumpy(oldPool[i], img) > MatrixMult.MatrixDifferenceNumpy(newPool[j], img):
            elitePool.append(newPool[j])
            j += 1
        else:
            elitePool.append(oldPool[i])
            i += 1
    return elitePool