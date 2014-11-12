"""
    Full Name: Rohit Ravi Kumar Bhoopalam
    Student ID: 1001100534
    student username: rrb0534
    Code for Project 1 
"""

import operator
import sys
import os
import datetime
from nltk.stem import PorterStemmer

def clean(s):
    return s.replace('\n', '').replace('\r', '')

def read_date(s):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

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
        apps[(int(u_id), int(job_id))] = temp
    return apps

def read_data_from_apps_file_by_user(apps_file):
    path = os.path.join(data_dir, 'apps.tsv') 
    apps_file = open(path, 'r')

    apps_file.next()
    apps = {}
    for a in apps_file:
        a = clean(a)
        temp = (u_id, app_date, job_id) = a.split('\t')
        try:
            apps[int(u_id)].append(temp)
        except KeyError:
            apps[int(u_id)] = [temp]
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
    return users2[:5]

def get_t2_jobs(jobs, t2_cutoff):
    t2_jobs = {}

    for j_id in jobs:
        if read_date(jobs[j_id][-1][:19]) >= t2_cutoff:
            t2_jobs[j_id] = jobs[j_id]
    return t2_jobs

def dist_users2_jobs(users, users2, t2_jobs):
    """
        same city = 1, same state = 0.5, same country = 0.3
    """
    users2_t2_jobs = {}

    count = 0
    for u_id in users2:
        for j_id in t2_jobs:
            count += 1

            score = 0
            user_details = users[u_id]
            job_details = t2_jobs[j_id]

            if (user_details[1] + "_" + user_details[2] + "_" + user_details[3]) == (job_details[4] + "_" + job_details[5] + "_" + job_details[6]):
                score = 1
            elif (user_details[2] + "_" + user_details[3]) == (job_details[5] + "_" + job_details[6]):
                score = 0.5
            elif (user_details[3]) == (job_details[6]):
                score = 0.3

            if score > 0:
                users2_t2_jobs[(u_id, j_id)] = score 
            print count, score, user_details[1] + "_" + user_details[2] + "_" + user_details[3], job_details[4] + "_" + job_details[5] + "_" + job_details[6]
    return users2_t2_jobs

def find_location_similarity(apps, users, jobs):
    city = state = country = 0
    for (u_id, j_id) in apps:
        user_details = users[u_id]
        job_details = jobs[j_id]

        if (user_details[1] + "_" + user_details[2] + "_" + user_details[3]) == (job_details[4] + "_" + job_details[5] + "_" + job_details[6]):
            city += 1
        elif (user_details[2] + "_" + user_details[3]) == (job_details[5] + "_" + job_details[6]):
            state += 1
        elif (user_details[3]) == (job_details[6]):
            country += 1

    print 'city = ', city
    print 'state = ', state
    print 'country = ', country
    print 'apps = ', len(apps)

def find_old_user2_apps_count(apps_by_users, users2):
    count = 0
    temp = {}
    ids = []
    for u2_id in users2:
        try:
            app_details = apps_by_users[u2_id]
            count += len(app_details)
        except KeyError:
            ids.append(u2_id)

    print count, len(users2), len(ids)

def find_unique_job_positions(jobs):
    stemmer = PorterStemmer()

    unique_titles = {}
    for job_id in jobs:
        job_title = jobs[job_id][1]

        try:
            job_title_stemmed = stemmer.stem(job_title).split()
        except UnicodeDecodeError:
            job_title_stemmed = job_title.split()
        job_title = " ".join(sorted(job_title_stemmed))

        try:
            unique_titles[job_title] += 1
        except KeyError:
            unique_titles[job_title] = 1

    print "unique positions = %s" %str(len(unique_titles.keys()))
    raw_input()
    print unique_titles

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Please use the syntax: python bhoopalam.p27.py <path to data directory> <path to output file>'
        exit()

    data_dir = sys.argv[1]
    output_file = open(sys.argv[2], 'w')

    #users = read_data_from_users_file(data_dir)
    #apps = read_data_from_apps_file(data_dir)
    jobs = read_data_from_jobs_file(data_dir)
    #user_history = read_data_from_user_history(data_dir)
    #apps_by_users = read_data_from_apps_file_by_user(data_dir)
    #users2 = read_data_from_users2(data_dir)

    #find_location_similarity(apps, users, jobs)
    #find_old_user2_apps_count(apps_by_users, users2)
    find_unique_job_positions(jobs)
