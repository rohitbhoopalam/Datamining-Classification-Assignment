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

def get_t2_jobs(jobs, t2_cutoff):
    t2_jobs = {}

    for j_id in jobs:
        if read_date(jobs[j_id][-1][:19]) >= t2_cutoff:
            t2_jobs[j_id] = jobs[j_id]
    return t2_jobs

def get_location_score(user_details, job_details):
    """
        same city = 0.230, same state = 0.608, same country = 0.156
    """
    score = 0.0056

    if (user_details[1] + "_" + user_details[2] + "_" + user_details[3]) == (job_details[4] + "_" + job_details[5] + "_" + job_details[6]):
        score = 0.230
    elif (user_details[2] + "_" + user_details[3]) == (job_details[5] + "_" + job_details[6]):
        score = 0.608
    elif (user_details[3]) == (job_details[6]):
        score = 0.156

    return score

def dist_users2_jobs(users, users2, t2_jobs):
    users2_t2_jobs = {}

    count = 0
    for u_id in users2:
        for j_id in t2_jobs:
            count += 1

            user_details = users[u_id]
            job_details = t2_jobs[j_id]

            location_score = get_location_score(user_details, job_details)

            if location_score > 0.2:
                users2_t2_jobs[(u_id, j_id)] = location_score  

            #print count
            #print count, location_score, user_details[1] + "_" + user_details[2] + "_" + user_details[3], job_details[4] + "_" + job_details[5] + "_" + job_details[6]
    return users2_t2_jobs

def write_result(users2_t2_jobs):
    f = open(sys.argv[2], 'w')
    for (user_job, score) in users2_t2_jobs:
        f.write("%s\t%s\n" %(user_job[0], user_job[1]))
    f.close()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Please use the syntax: python bhoopalam.p27.py <path to data directory> <path to output file>'
        exit()

    data_dir = sys.argv[1]

    users = read_data_from_users_file(data_dir)
    apps = read_data_from_apps_file(data_dir)
    jobs = read_data_from_jobs_file(data_dir)
    user_history = read_data_from_user_history(data_dir)
    users2 = read_data_from_users2(data_dir)

    t2_cutoff = read_date("2012-04-09 00:00:00")

    t2_jobs = get_t2_jobs(jobs, t2_cutoff)

    #print "jobs len", len(jobs)
    #print "t2 jobs len", len(t2_jobs)

    users2_t2_jobs = dist_users2_jobs(users, users2, t2_jobs) 

    #print len(users2_t2_jobs)
    #raw_input()
    final_150 = sorted(users2_t2_jobs.items(), key= lambda x: x[1], reverse=True)[:150]

    write_result(final_150)

    #print 'users', len(users)
    #print 'apps', len(apps)
    #print 'jobs', len(jobs)
    #print 'user_history', len(user_history)
    #print 'users2', len(users2)
