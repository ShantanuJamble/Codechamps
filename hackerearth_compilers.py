import requests

__author__ = 'shantya'
import subprocess
import time
import signal
import os
import filecmp

# STATIC
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CLIENT_ID = 'e663e37ff362d54d0a85eda6d6c40098543c66a4f1eb.api.hackerearth.com'
CLIENT_SECRET = 'c3affed7a58d9db8e490db6062bbc75e9ea0fe91'
COMPILE_LINK = u'http://api.hackerearth.com/code/compile/'
RUN_LINK = u'http://api.hackerearth.com/v3/code/run/'


def creat_json(source, lang, input=None, time=5, memory=262144):
    """

    :rtype: dict
    """
    data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'input': input,
        'lang': lang.upper(),
        'time_limit': time,
        'memory_limit': memory,
    }
    return data


def save_source_code(save_path, source, lang_chosen):
    submission_list = os.listdir(save_path)
    submission_list.remove('temp')
    if len(submission_list) > 0:
        sub_no = submission_list[len(submission_list) - 1].split("_")
        sub_no = sub_no[1].split(".")
        sub_no = int(sub_no[0])
        file_path = os.path.join(save_path, 'Solution_' + (str(sub_no + 1)) + '.' + lang_chosen)
    else:
        file_path = os.path.join(save_path, 'Solution_1.' + lang_chosen)
    source_file = open(file_path, 'w')
    source_file.write(source)
    source_file.close()
    return


# #retruns False if the solution does not match with any of earlier solution else true if solution is already present
def check_duplicate(save_path, source, lang_chosen):
    new_solution_path = os.path.join(save_path, "temp")
    if not os.path.exists(new_solution_path):
        os.makedirs(new_solution_path)
    new_solution_path = os.path.join(new_solution_path, "Solution." + lang_chosen)
    new_solution = open(new_solution_path, 'w')
    new_solution.write(source)
    new_solution.close()

    if not os.path.exists(save_path):
        os.makedirs(save_path)
        save_source_code(save_path, source, lang_chosen)
        return False
    else:
        submission_list = os.listdir(save_path)
        if submission_list is not None:
            flg = False
            for file_present in submission_list:
                original_submission_path = os.path.join(save_path, file_present)
                if filecmp.cmp(new_solution_path, original_submission_path, shallow=False):
                    flg = True
                    break

            return flg


def read_result(source_path, file_name):
    file_path = os.path.join(source_path, file_name)
    if os.path.exists(file_path):
        result_file = open(file_path, "r")
        data = result_file.read()
        result_file.close()
    else:
        data = None
    return data


def compile_function(username, source, lang_chosen):
    print 'compile'
    data = creat_json(source, lang=lang_chosen)
    response = requests.post(COMPILE_LINK, data=data)
    print response
    if response.status_code != 200:
        compile_function(username, source, lang_chosen)
    else:
        response = response.json()
        print response
        if response[u'compile_status'] == 'OK':
            return None
        else:
            return response[u'compile_status']


def check_output(source_path, output_data):
    match = 0
    user_output = read_result(source_path, 'output.txt')
    try:
        user_output = user_output.split(" ")
        standard_ans = open(output_data)
        standard_ans = standard_ans.read()
        standard_ans = standard_ans.split(" ")
        loop_counter = len(standard_ans) - 1
        index = 0
        if len(user_output) != len(standard_ans):
            return 0
        while index < loop_counter:
            if user_output[index] == standard_ans[index]:
                match += 1
            else:
                break
            index += 1
        print match
        if match == index:
            match = 10
    except:
        match = 0
    return match


def execute_source(source, lang_chosen, input_path, output_path, test_count, test_time):
    test_done = 0
    res = []
    while test_done < test_count:
        input_data = input_path + str(test_done) + '.txt'
        output_data = output_path + str(test_done) + '.txt'
        input_data = open(input_data, 'r')
        inputs = input_data.read()
        input_data.close()
        output_data = open(output_data, 'r')
        outputs = "\\n".join(output_data.read().split("\n"))
        output_data.close()
        json_data = creat_json(source, lang_chosen, inputs, test_time)
        resp = requests.post(RUN_LINK, data=json_data)
        if resp.status_code != 200:
            continue
        else:
            resp = resp.json()
            if resp[u'run_status'][u'status'] == u'AC':
                if resp[u'run_status'][u'output'] == outputs:
                    res.append(10)
            elif resp[u'run_status'][u'status'] == u'TLE':
                res.append('TLE')
            elif resp[u'run_status'][u'status'] == u'NZEC':
                res.append('NZEC')
            elif resp[u'run_status'][u'status'] == u'RE':
                res = ['Runtime Exception', resp[u'run_status'][u'stderr']]
                break
    return res


def trial_execute_source(source, lang_chosen, input_path, test_time):
    res = []
    print 'in trial'
    import pdb
    #pdb.set_trace()
    input_data = open(input_path, 'r')
    #print 'in trial'
    inputs = input_data.read()
    #print 'in trial'
    input_data.close()
    json_data = creat_json(source, lang_chosen, inputs, test_time)
    print json_data
    resp = requests.post(RUN_LINK, data=json_data)

    if resp.status_code != 200:
        trial_execute_source(source, lang_chosen, input_path, test_time=test_time)
    else:
        resp = resp.json()
        print resp
        if resp[u'run_status'][u'status'] == u'AC':
            res.append(resp[u'run_status'][u'output'])
        elif resp[u'run_status'][u'status'] == u'TLE':
            res.append('TLE')
        elif resp[u'run_status'][u'status'] == u'NZEC':
            res.append('NZEC')
        elif resp[u'run_status'][u'status'] == u'RE':
            res = ['Runtime Exception', resp[u'run_status'][u'stderr']]


def run_function(username, problem_title, source, lang_chosen, test_time, test_count, isFinal):
    # source_path = os.path.join(BASE_DIR, 'static', 'media', 'submissions', username, problem_title, 'temp')
    input_path = os.path.join(BASE_DIR, 'static', 'media', 'input', problem_title, 'input_')
    output_path = os.path.join(BASE_DIR, 'static', 'media', 'output', problem_title, 'output_')
    print 'in run'
    if isFinal:
        res = execute_source(source, lang_chosen, input_path, output_path, test_count, test_time)
    else:
        res = trial_execute_source(source, lang_chosen, input_path+'0.txt', test_time)
    return res


def finalize_result(result):
    total = 0
    for res in result:
        if res is not 'TLE':
            total += int(res)
    if 'TLE' in result:
        return 'TLE', 0
    elif total == 0:
        return 'WA', '0'
    else:
        return 'AC', total


def process_submission(username, problem_title, source, lang_chosen, test_time, test_count):
    # 1.CheckDuplicate
    # 2.Compilation
    # 3.run
    # 4.getresult and update marks and status
    save_path = os.path.join(BASE_DIR, 'static', 'media', 'submissions', username, problem_title)
    duplicate = check_duplicate(save_path, source, lang_chosen)
    status = ''
    marks = 0
    res = None
    languages = ('c', 'cpp', 'java', 'python')
    save_extension = ('c', 'cpp', 'java', 'py')
    index = languages.index(lang_chosen)
    if duplicate:
        clear_file(save_path)
        status = 'duplicate'
        return status, marks, res
    else:

        save_source_code(save_path, source, save_extension[index])
        res = compile_function(username, source, lang_chosen)
        if res:
            status = 'CE'
            marks = 0
        else:
            result = run_function(username, problem_title, source, lang_chosen, test_time, test_count, True)
            if result[0] == 'Runtime Exception':
                status = "NZEC"
                res = result[1]
                marks = 0
            else:
                res = result
                status, marks = finalize_result(result)

    clear_file(save_path)
    return status, marks, res


def process_trial_submission(username, problem_title, source, lang_chosen, test_time, test_count):
    # 2.Compilation
    # 3.run
    # 4.getresult and update marks and status
    path = os.path.join(BASE_DIR, 'static', 'media', 'submissions', username, problem_title)
    save_path = os.path.join(path, 'temp')
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    languages = ('c', 'cpp', 'java', 'python')
    save_extension = ('c', 'cpp', 'java', 'py')
    index = languages.index(lang_chosen)
    save_path = os.path.join(BASE_DIR, 'static', 'media', 'submissions', username, problem_title, 'temp',
                             'Solution.' + save_extension[index])
    temp_solution = open(save_path, "w")
    temp_solution.write(source)
    temp_solution.close()
    status = None
    marks = 0
    res = compile_function(username, source, lang_chosen)
    print res
    if res:
        status = 'CE'
        marks = 0
    else:
        result = run_function(username, problem_title, source, lang_chosen, test_time, test_count, False)
        print result
        if result[0] == 'Runtime Exception':
            status = "NZEC"
            res = result[1]
            marks = 0
        else:
            res = result
    clear_file(path)
    return status, marks, res


def clear_file(save_path):
    save_path = os.path.join(save_path, 'temp')
    file_list = os.listdir(save_path)
    for a_file in file_list:
        new_path = os.path.join(save_path, a_file)
        os.remove(new_path)
