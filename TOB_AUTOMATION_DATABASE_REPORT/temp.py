import configparser
import math
"""config = configparser.ConfigParser()
config.read("Config.txt")


ChannelString = config.get('DATA SECTION', 'Channels')
DrugString = config.get('DATA SECTION', 'DRUGS')
channelList = str(ChannelString).split(",")
print(channelList)
seqcount = 0
value = "S-P-PA,QL,"
s1 = "S-P-QL,PA,"

list1 = value.split("-")
len =list1.__len__()

ss =list1[list1.__len__()-1]
list2 = ss.split(",")
print(list2)
for each in range(list2.__len__()):
    if(s1.__contains__(list2[each])):
        seqcount = seqcount+1

def get_reportlab_path():
    import reportlab
    reportlab_path = reportlab.__path__[0]
    return reportlab_path

drugFormularycopay = [float('nan'), 150.0, 150.0, 150.0, float('nan'), 150.0]
cleanedList = [x for x in drugFormularycopay if (math.isnan(x) == False)]
#print([x for x in drugFormularycopay if x != float('nan')])
a =  []
if(a.__len__() == 0):
    a.append("None")
s = "None"
print(set(s.split(",")).__eq__(set(a)))
#print(a.(s.split(",")))
print(cleanedList)

# number of spaces
n =5


print("Program to print half pyramid: ")
rows = input("Enter number of rows ")
rows = int (rows)
count = 15
for i in range (rows,0,-1):
    for j in range(0, i + 1):

        print(str(count)+"-", end=' ')
        count= count -1
    print("\r")"""


"""LIST1 = [1234,23,1234]
LIST2 = ['A','B','C']
m = max(LIST1)
list1 = [i for i, j in enumerate(LIST1) if j == m]
print(list1)"""


def numbers_to_strings(argument):
    switcher = {
        'A': "zero",
        'B': "one",
        'C': "two",
    }

    # get() method of dictionary data type returns
    # value of passed argument if it is present
    # in dictionary otherwise second argument will
    # be assigned as default value of passed argument
    return switcher.get(argument, "nothing")


# Driver program
if __name__ == "__main__":
    argument = 0
    print(numbers_to_strings('B'))