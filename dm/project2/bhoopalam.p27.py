"""
    Full Name: Rohit Ravi Kumar Bhoopalam
    Student ID: 1001100534
    student username: rrb0534
    Code for Project 1 
"""

import operator
import sys
import os

def clean(s):
    return s.replace('\n', '').replace('\r', '')

def read_data_from_users_file(data_dir):
    path = os.path.join(data_dir, 'users.tsv') 
    users_file = open(path, 'r')

    users_file.next()
    users = {}
    for u in users_file:
        u = clean(u)
        temp = (u_id, city, state, country, zip_code, degree, major, grad_date, work_history_count,\
                total_exp, currently_emp, managed_others, managed_howmany) = u.split('\t')

        users[int(u_id)] = temp 
    return users

def read_data_from_apps_file(apps_file):
    path = os.path.join(data_dir, 'apps.tsv') 
    apps_file = open(path, 'r')

    apps_file.next()
    apps = {}
    for a in apps_file:
        a = clean(a)
        temp = (u_id, app_date, job_id) = a.split('\t')
        apps[(int(u_id), int(job_id), app_date)] = temp
    return apps

def read_data_from_jobs_file(jobs_file):
    path = os.path.join(data_dir, 'jobs.tsv') 
    jobs_file = open(path, 'r')

    jobs_file.next()
    jobs = {}
    for j in jobs_file:
        j = clean(j)
        temp = (job_id, title, desc, req, city, state, country, zip5, start_date,\
                end_date) = j.split('\t')
        jobs[int(job_id)] = temp
    return jobs

def read_data_from_user_history(user_history_file):
    path = os.path.join(data_dir, 'user_history.tsv') 
    user_history_file = open(path, 'r')

    user_history_file.next()
    user_history = {}
    for uh in user_history_file:
        uh = clean(uh)
        temp = (user_id, sequence, job_title) = uh.split('\t') 
        user_history[(user_id, sequence)] = temp
    return user_history

def read_data_from_users2(data_dir):
    path = os.path.join(data_dir, 'user2.tsv') 
    users_file = open(path, 'r')

    users2 = {}
    for u in users_file:
        u = clean(u)
        users2[int(u)] = u
    return users2

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Please use the syntax: python bhoopalam.p27.py <path to data directory> <path to output file>'
        exit()

    data_dir = sys.argv[1]
    output_file = open(sys.argv[2], 'w')

    users = read_data_from_users_file(data_dir)
    apps = read_data_from_apps_file(data_dir)
    jobs = read_data_from_jobs_file(data_dir)
    user_history = read_data_from_user_history(data_dir)
    users2 = read_data_from_users2(data_dir)

    print 'users', len(users)
    print 'apps', len(apps)
    print 'jobs', len(jobs)
    print 'user_history', len(user_history)
    print 'users2', len(users2)
