import timeit
from statistics import mean


test1 = '''
import json
data1 = '{"SOLVE": {"param1": "sdfsdf", "param2": "sdfsdf"}}'
json_data1 = json.loads(data1)
def test1():
    try:
        save = json_data1["SOLVE"]
        save2 = save["param1"]
        # Execute SOLVE
        return
    except KeyError:
        pass

    try:
        save = json_data1["POLL"]
        save2 = save["param1"]
        # Execute POLL
        return
    except KeyError:
        pass
test1()
    '''

test2 = '''
import json
data2 = '{"POLL": {"param1": "sdfsdf", "param2": "sdfsdf"}}'
json_data2 = json.loads(data2)
def test2():
    try:
        save = json_data2["SOLVE"]
        save2 = save["param1"]
        # Execute SOLVE
        return
    except KeyError:
        pass

    try:
        save = json_data2["POLL"]
        save2 = save["param1"]
        # Execute POLL
        return
    except KeyError:
        pass
test2()
    '''

test3 = '''
import json
data3 = '{"POLLsss": {"param1": "sdfsdf", "param2": "sdfsdf"}}'
json_data3 = json.loads(data3)
def test3():
    try:
        save = json_data3["SOLVE"]
        save2 = save["param1"]
        # Execute SOLVE
        return
    except KeyError:
        pass

    try:
        save = json_data3["POLL"]
        save2 = save["param1"]
        # Execute POLL
        return
    except KeyError:
        pass
test3()
    '''

test4 = '''
import json
data1 = '{"command": "SOLVE", "param1": "sdfsdf", "param2": "sdfsdf"}'
json_data1 = json.loads(data1)
def test4():
    if json_data1["command"] == "SOLVE":
        save = json_data1["command"]
        save2 = json_data1["param1"]
        # Execute SOLVE
        return
    elif json_data1["command"] == "POLL":
        save = json_data1["command"]
        save2 = json_data1["param1"]
        # Execute POLL
        return
test4()
    '''

test5 = '''
import json
data2 = '{"command": "POLL", "param1": "sdfsdf", "param2": "sdfsdf"}'
json_data2 = json.loads(data2)
def test5():
    if json_data2["command"] == "SOLVE":
        save = json_data2["command"]
        save2 = json_data2["param1"]
        # Execute SOLVE
        return
    elif json_data2["command"] == "POLL":
        save = json_data2["command"]
        save2 = json_data2["param1"]
        # Execute POLL
        return
test5()
        '''

test6 = '''
import json
data3 = '{"command": "POLLsss", "param1": "sdfsdf", "param2": "sdfsdf"}'
json_data3 = json.loads(data3)
def test6():
    if json_data3["command"] == "SOLVE":
        save = json_data3["command"]
        save2 = json_data3["param1"]
        # Execute SOLVE
        return
    elif json_data3["command"] == "POLL":
        save = json_data3["command"]
        save2 = json_data3["param1"]
        # Execute POLL
        return
test6()
            '''

t1_results = timeit.Timer(setup=test1).repeat(100000, 1000)
t2_results = timeit.Timer(setup=test2).repeat(100000, 1000)
t3_results = timeit.Timer(setup=test3).repeat(100000, 1000)
t4_results = timeit.Timer(setup=test4).repeat(100000, 1000)
t5_results = timeit.Timer(setup=test5).repeat(100000, 1000)
t6_results = timeit.Timer(setup=test6).repeat(100000, 1000)

print("Try Except block:")
print('Test 1: Mean[' + str(mean(t1_results)) + '] Min[' + str(min(t1_results)) + '] Max[' + str(
    max(t1_results)) + ']')
print('Test 2: Mean[' + str(mean(t2_results)) + '] Min[' + str(min(t2_results)) + '] Max[' + str(
    max(t2_results)) + ']')
print('Test 3: Mean[' + str(mean(t3_results)) + '] Min[' + str(min(t3_results)) + '] Max[' + str(
    max(t3_results)) + ']')

print("\nIfs:")
print('Test 4: Mean[' + str(mean(t4_results)) + '] Min[' + str(min(t4_results)) + '] Max[' + str(
    max(t4_results)) + ']')
print('Test 5: Mean[' + str(mean(t5_results)) + '] Min[' + str(min(t5_results)) + '] Max[' + str(
    max(t5_results)) + ']')
print('Test 6: Mean[' + str(mean(t6_results)) + '] Min[' + str(min(t6_results)) + '] Max[' + str(
    max(t6_results)) + ']')