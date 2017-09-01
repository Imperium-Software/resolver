import random

class SATGenerator:

    def __init__(self,variables,maxClauseLength=0):
        self.variables = variables
        self.maxClauseLength = maxClauseLength
    def hasTrue(self,vals,valsr,max):
        for y in valsr:
            if y > 0:
                return True 
        valsr.append(max+1)
        vals.append(max+1)
        return False

    def checkUsed(self,used,vals):
        if len(used)== 0:
            return False
        for x in vals:
            found  = False
            for j in used:
                for k in j:
                    if abs(k) == abs(x):
                        found = True
                        break
                if(found):
                    break
            if(found==False):
                return False
                
        return True
    def generate(self):
        vals = []
        max = self.variables
        for i in range(0,self.variables):
            temp = random.randint(0,1)
            if(temp==0):
                temp = -1
            temp = temp * (i+1)
            vals.append(temp)
        used = []
        while(self.checkUsed(used,vals)==False):
            length = 0
            if(self.maxClauseLength>0):
                length =random.randint(1, self.maxClauseLength)
            else:
                length = random.randint(1, self.variables)

            start = random.randint(0,self.variables)
            end = start+length
            if(end > len(vals) ):
                end = self.variables
            temp = vals[start:end]
            for m in range(0,len(temp)):
                rr = random.random()
                if(rr<0.3):
                    temp[m] = temp[m]*-1
            add = self.hasTrue(vals,temp,max)

            used.append(temp)
            if(add==False):
                max = max + 1
     

        return (vals,used)

s = SATGenerator(1000,5)
(c,d) = s.generate()
myFile = open("mod.txt","w")
myFile.write("# of variables: "+str(len(c)))
myFile.write("# of clauses: "+str(len(d)))
for j in d:
    val = ""
    for k in j:
        val+=str(k) +" "
    val +=" 0\n"
    myFile.write(val)
    print(val)
myFile.close()
print("# of variables: "+str(len(c)))
print("# of clauses: "+str(len(d)))