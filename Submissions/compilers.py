import subprocess
import time
import signal
# from Problems.models import Problem
#import psutil
from Problems.models import Problem

__author__ = 'shantya'
import os
import filecmp

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


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


def make_batch_file(batch_command, source_path):
    print batch_command
    batch_file_path = os.path.join(source_path, 'run.bat')
    batch_file = open(batch_file_path, "w")
    drive = source_path.split(':')
    drive = drive[0]
    file_data = 'cd ' + source_path + '\n' + drive + ':\n' + batch_command
    batch_file.write(file_data)
    batch_file.close()
    return batch_file_path


def compile_source(source_path, batch_command):
    batch_file_path = make_batch_file(batch_command, source_path)
    p = subprocess.Popen(batch_file_path)
    p.wait()
    compile_res = read_result(source_path, 'compile.txt')
    return compile_res


def compile_function(username, problem_title, lang_chosen):
    source_path = os.path.join(BASE_DIR, 'static', 'media', 'submissions', username, problem_title, 'temp')
    languages = ('c', 'cpp', 'java', 'python')
    compiler = ('gcc -o Solution Solution.c 2>compile.txt',
                'g++ -o Solution Solution.cpp 2>compile.txt',
                'javac Solution.java 2>compile.txt',
                'python -m py_compile Solution.py 2>compile.txt',)
    res = compile_source(source_path, compiler[languages.index(lang_chosen)])
    return res


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


def execute_source(source_path, input_path, output_path, test_count, test_time, batch_command, kill_command):
    test_done = 0
    res = []
    while test_done < test_count:
        input_data = input_path + str(test_done) + '.txt'
        output_data = output_path + str(test_done) + '.txt'
        batch_command_new = batch_command + input_data
        batch_file_path = make_batch_file(batch_command_new, source_path)
        p = subprocess.Popen(batch_file_path)
        time.sleep(test_time)
        if p.poll() is None:
            os.kill(p.pid, signal.SIGINT)
            print 'in here'
            os.system('taskkill /f /im ' + kill_command)
            res.append('TLE')
        else:
            output = read_result(source_path, 'output.txt')
            if output is None:
                break
            match = check_output(source_path, output_data)
            res.append(match)
        test_done += 1
    if test_done < test_count:
        runtime = read_result(source_path, 'runtime.txt')
        return ['Runtime Exception', runtime]
    return res


def trial_execute_source(source_path, input_path, test_time, batch_command, kill_command):
    res = []
    output = None
    input_data = input_path + str(0) + '.txt'
    batch_command_new = batch_command + input_data
    batch_file_path = make_batch_file(batch_command_new, source_path)
    p = subprocess.Popen(batch_file_path)
    time.sleep(test_time)
    if p.poll() is None:
        os.kill(p.pid, signal.SIGINT)
        print 'in here'
        os.system('taskkill /f /im ' + kill_command)
        res.append('TLE')
    else:
        output = read_result(source_path, 'output.txt')
        res.append(output)
    if output is None:
        runtime = read_result(source_path, 'runtime.txt')
        return ['Runtime Exception', runtime]
    return res


def run_function(username, problem_title, lang_chosen, test_time, test_count, isFinal):
    source_path = os.path.join(BASE_DIR, 'static', 'media', 'submissions', username, problem_title, 'temp')
    input_path = os.path.join(BASE_DIR, 'static', 'media', 'input', problem_title, 'input_')
    output_path = os.path.join(BASE_DIR, 'static', 'media', 'output', problem_title, 'output_')
    languages = ('c', 'cpp', 'java', 'python')
    run_command = (
        'Solution.exe >output.txt 2>runtime.txt <',
        'Solution.exe >output.txt 2>runtime.txt <',
        'java Solution >output.txt 2>runtime.txt <',
        'pythonw Solution.pyc >output.txt 2>runtime.txt <',
    )
    kill_command = (
        'Solution.exe',
        'Solution.exe',
        'java.exe',
        'pythonw.exe',
    )
    index = languages.index(lang_chosen)
    if isFinal:
        res = execute_source(source_path, input_path, output_path, test_count, test_time, run_command[index],
                             kill_command[index])
    else:
        res = trial_execute_source(source_path, input_path, test_time, run_command[index],
                                   kill_command[index])
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
        if check_system_call(source, lang_chosen):
            status = 'SC'
            marks = 0
            res = 'This is a warning ! You are not allowed to use System Calls'
        else:
            save_source_code(save_path, source, save_extension[index])
            res = compile_function(username, problem_title, lang_chosen)
            if res:
                status = 'CE'
                marks = 0
            else:
                result = run_function(username, problem_title, lang_chosen, test_time, test_count, True)
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
    if check_system_call(source, lang_chosen):
        status = 'SC'
        marks = 0
        res = 'This is a warning ! You are not allowed to use System Calls'
    else:
        res = compile_function(username, problem_title, lang_chosen)
        if res:
            status = 'CE'
            marks = 0
        else:
            result = run_function(username, problem_title, lang_chosen, test_time, test_count, False)
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


def check_system_call(source, lang_chosen):
    languages = ('c', 'cpp', 'java', 'python')
    system_call_method = (
        'system(,exec(,fork(',
        'system(,exec(,fork(',
        'Runtime.getRuntime(),Thread,Runnable',
        'import os,import subprocess,from os,from subprocess',
    )
    index = languages.index(lang_chosen)
    system_calls = system_call_method[index].split(",")
    count = len(system_calls)
    index = 0
    while index < count:
        if source.find(system_calls[index]) != -1:
            break
        index += 1
    if index < count:
        return True
    else:
        return False

