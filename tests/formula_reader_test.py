
class FormulaReader:

    def __init__(self, filename):

        f = open(filename, "r")
        # Read all the lines from the file that aren't comments
        lines = [line.replace("\n", "") for line in f.readlines() if line[0] != "c" and line.strip() != ""]
        (self.numberOfVariables, self.numberOfClauses) = int(lines[0].split()[2]), int(lines[0].split()[3])
        self.formula = []

        # Go through the lines and create numberOfClauses clauses
        line = 1
        # for line in range(1, len(lines)):
        while line < len(lines):
            clause = []
            # We need a while loop as a clause may be split over many lines, but eventually ends with a 0
            end_of_clause = False
            while line < len(lines) and not end_of_clause:
                # Split the line and append a list of all integers, excluding 0, to clause
                clause.append([int(variable.strip()) for variable in lines[line].split() if int(variable.strip()) != 0])
                # If this line ended with a 0, we reached the end of the clause
                if int(lines[line].split()[-1].strip()) == 0:
                    end_of_clause = True
                    line += 1
                # Otherwise continue reading this clause from the next line
                else:
                    line += 1
            # clause is now a list of lists, so we need to flatten it and convert it to a list
            self.formula.append(tuple([item for sublist in clause for item in sublist]))
        f.close()