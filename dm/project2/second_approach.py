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
import re
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
        user_history[(int(user_id), int(sequence))] = temp
    return user_history

def read_data_from_users2(data_dir):
    path = os.path.join(data_dir, 'user2.tsv') 
    users_file = open(path, 'r')

    users2 = {}
    count = 0
    for u in users_file:
        u = clean(u)
        users2[int(u)] = u
        count += 1
        if count > 50:
            break

    return users2

def get_t2_jobs(jobs, t2_cutoff):
    t2_jobs = {}

    for j_id in jobs:
        if read_date(jobs[j_id][-1][:19]) >= t2_cutoff:
            t2_jobs[j_id] = jobs[j_id]
    return t2_jobs

def find_apps_with_j2_jobs(apps, jobs, t2_cutoff):
    apps_with_t2_jobs = {}

    for (u_id, job_id) in apps:
        job_details = jobs[job_id]
        if read_date(jobs[job_id][-1][:19]) >= t2_cutoff:
            try:
                apps_with_t2_jobs[job_id].append(u_id)
            except KeyError:
                apps_with_t2_jobs[job_id] = [u_id]

    return apps_with_t2_jobs 

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

def write_result(users2_t2_jobs, to_be_removed):
    f = open(sys.argv[2], 'w')
    for (user_job, score) in users2_t2_jobs:
        f.write("%s\t%s\n" %(user_job[0], user_job[1]))
    f.write("==========================\n")
    for u in to_be_removed:
        f.write("%s\t%s\n" %(u[0], u[1]))
    f.close()

def get_users_features(users, user_history):
    users_features = {}
    stemmer = PorterStemmer()

    for u_id in users:
        (user_id, city, state, country, zip_code, degree, major, grad_date, work_history_count,\
                total_exp, currently_emp, managed_others, managed_howmany) = users[u_id]

        city = (city + "_" + state).lower() 
        state = (state + "_" + country).lower() 
        country = country.lower()

        degree = degree.lower().split()
        try:
            degree = [stemmer.stem(t.lower()) for t in degree]
        except UnicodeDecodeError:
            degree = [t.lower() for t in degree]
        degree = set(degree)

        major = major.lower().split()
        try:
            major = [stemmer.stem(t.lower()) for t in major]
        except UnicodeDecodeError:
            major = [t.lower() for t in major]
        major = set(major)

        try:
            grad_year = int(grad_date[:4])
        except:
            grad_year = 0000

        try:
            current_job_title = user_history[(u_id, int(work_history_count))][-1]
            current_job_title = " ".join(re.findall(r'(\w+)', current_job_title))
            try:
                current_job_title = [stemmer.stem(t.lower()) for t in current_job_title.split()]
            except UnicodeDecodeError:
                current_job_title = [t.lower() for t in current_job_title.split()]
            current_job_title = set(current_job_title)
        except KeyError:
            current_job_title = set()

        old_job_titles = ""
        try:
            for i in range(0, int(work_history_count)):
                old_job_titles += " " + user_history[(u_id, i)]
        except KeyError:
            pass

        old_job_titles = " ".join(re.findall(r'(\w+)', old_job_titles))
        try:
            old_job_titles = [stemmer.stem(t.lower()) for t in old_job_titles.split()]
        except UnicodeDecodeError:
            old_job_titles = [t.lower() for t in old_job_titles.split()]

        old_job_titles = set(old_job_titles)

        if work_history_count:
            work_history_count = int(work_history_count)
        else:
            work_history_count = 0

        if total_exp:
            total_exp = int(total_exp)
        else:
            total_exp = 0

        if managed_howmany:
            managed_howmany = int(managed_howmany)
        else:
            managed_howmany = 0

        users_features[u_id] = (city, state, country, degree, major, grad_year, work_history_count,\
                total_exp, currently_emp.lower(), managed_others.lower(), managed_howmany, current_job_title, old_job_titles)

    return users_features

def jaccard(set1, set2):
    if len(set1) + len(set2) == 0:
        return 0
    return len(set1.intersection(set2))/float(len(set1)+len(set2))

def numeric_similarity(n1, n2):
    d = n1-n2 if n1>n2 else n2-n1
    return 1/float(d+1)

def numeric_similarity_managed(n1, n2):
    d = n1-n2 if n1>n2 else n2-n1
    return (1100 - d)/1100.0


def get_similarity_score(u2_user, user):
    (u2_city, u2_state, u2_country, u2_degree, u2_major, u2_grad_year, u2_work_history_count,\
            u2_total_exp, u2_currently_emp, u2_managed_others, u2_managed_howmany, u2_current_job_title, u2_old_job_titles) = u2_user
    (city, state, country, degree, major, grad_year, work_history_count,\
            total_exp, currently_emp, managed_others, managed_howmany, current_job_title, old_job_titles) = user

    city_score = state_score = country_score = 1
    if u2_city == city:
        city_score = 1
    if u2_state == state:
        state_score = 1
    if u2_country == country:
        country_score = 1

    degree_score = 2 if u2_degree == degree and degree else 0
    major_score = 3 if u2_major == major and major else 0

    degree_score = jaccard(u2_degree, degree)
    major_score = jaccard(u2_major, major)

    grad_year_score = numeric_similarity(u2_grad_year, grad_year)
    work_history_count_score = numeric_similarity(u2_work_history_count, work_history_count)

    total_exp_score = numeric_similarity(u2_total_exp, total_exp)
    currently_emp_score = 1 if u2_currently_emp == currently_emp else 0.1

    managed_others_score = 1 if u2_managed_others == managed_others else 0.1
    managed_howmany_score = numeric_similarity_managed(u2_managed_howmany, managed_howmany)
    #print managed_howmany_score, u2_managed_howmany, managed_howmany

    current_job_title_score = jaccard(u2_current_job_title, current_job_title)
    old_job_titles_score = jaccard(u2_old_job_titles, old_job_titles)

    location_score = 1.4*city_score+1.2*state_score+0.7*country_score
    #location_score = city_score+state_score+country_score

    return current_job_title_score * degree_score * major_score * old_job_titles_score * (location_score * total_exp_score * managed_others_score * grad_year_score * work_history_count_score * currently_emp_score * managed_howmany_score)

#def get_similarity_score(u2_user, user):
#    (u2_city, u2_state, u2_country, u2_degree, u2_major, u2_grad_year, u2_work_history_count,\
#            u2_total_exp, u2_currently_emp, u2_managed_others, u2_managed_howmany, u2_current_job_title, u2_old_job_titles) = u2_user
#    (city, state, country, degree, major, grad_year, work_history_count,\
#            total_exp, currently_emp, managed_others, managed_howmany, current_job_title, old_job_titles) = user
#
#    city_score = state_score = country_score = 1
#    if u2_city == city:
#        city_score = 1
#    if u2_state == state:
#        state_score = 1
#    if u2_country == country:
#        country_score = 1
#
#    degree_score = 2 if u2_degree == degree and degree else 0
#    major_score = 3 if u2_major == major and major else 0
#
#    degree_score = jaccard(u2_degree, degree)
#    major_score = jaccard(u2_major, major)
#    
#    grad_year_score = numeric_similarity(u2_grad_year, grad_year)
#    work_history_count_score = numeric_similarity(u2_work_history_count, work_history_count)
#
#    total_exp_score = numeric_similarity(u2_total_exp, total_exp)
#    currently_emp_score = 1 if u2_currently_emp == currently_emp else 0
#
#    managed_others_score = 1 if u2_managed_others == managed_others else 0
#    managed_howmany_score = numeric_similarity_managed(u2_managed_howmany, managed_howmany)
#    #print managed_howmany_score, u2_managed_howmany, managed_howmany
#
#    current_job_title_score = jaccard(u2_current_job_title, current_job_title)
#    old_job_titles_score = jaccard(u2_old_job_titles, old_job_titles)
#
#    location_score = 1.4*city_score+1.2*state_score+0.7*country_score
#    #location_score = city_score+state_score+country_score
#
#    return current_job_title_score * degree_score * major_score * old_job_titles_score * (location_score * total_exp_score * managed_others_score * grad_year_score * work_history_count_score * currently_emp_score * managed_howmany_score)
#
def get_similar_users(user_ids, users2, users_features, k):
    similar_user_ids = {}
    
    user2_similarity = {} 

    for u2_id in users2:
        u2_user = users_features[u2_id]

        for u_id in user_ids:
            user_details = users_features[u_id]

            similarity_score = get_similarity_score(u2_user, user_details)
            similar_user_ids[(u2_id, u_id)] = similarity_score

        similar_users = sorted(similar_user_ids.items(), key=lambda x: x[1], reverse=True)

        first = similar_users[0]
        top_100 = similar_users[1:k+1]

        similar_users_norm = {}
        for u, v in top_100:
            similar_users_norm[u] = v#/first[1]

    return similar_users_norm

def predict_jobs_for_users(users2, users_features, apps_t2_jobs, jobs, k):
    predictions = {}

    for j_id in apps_t2_jobs:
        user_ids = apps_t2_jobs[j_id]
        similar_users = get_similar_users(user_ids, users2, users_features, k)
        for (u2_id, u_id) in similar_users:
            new_score = similar_users[(u2_id, u_id)] 
            try:
                old_score = predictions[(u2_id, j_id)]
            except KeyError:
                old_score = (0, 0)
            predictions[(u2_id, j_id)] = (old_score[0]+new_score, old_score[1]+1)
    return predictions

def find_accuracy(final_150, to_be_removed):
    to_be_removed = dict(to_be_removed)
    accuracy = 0
    for (t, score) in final_150:
        if int(to_be_removed[t[0]]) == int(t[1]):
            accuracy += 1
    return accuracy

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Please use the syntax: python bhoopalam.p27.py <path to data directory> <path to output file>'
        exit()

    data_dir = sys.argv[1]

    t2_cutoff = read_date("2012-04-09 00:00:00")

    users = read_data_from_users_file(data_dir)
    jobs = read_data_from_jobs_file(data_dir)
    apps = read_data_from_apps_file(data_dir)
    user_history = read_data_from_user_history(data_dir)
    #users2 = read_data_from_users2(data_dir)

    users2 = []
    count = 0
    to_be_removed = []
    for u in apps:
        if count > 100:
            break
        count += 1
        to_be_removed.append(u)
        users2.append(u[0])
        #print users2

    for u in to_be_removed:
        apps.pop(u, None)

    users_features = get_users_features(users, user_history)


    apps_t2_jobs = find_apps_with_j2_jobs(apps, jobs, t2_cutoff)

    k = 3

    predictions = predict_jobs_for_users(users2, users_features, apps_t2_jobs, jobs, k)

    predicted_items = sorted(predictions.items(), key=lambda x: x[1][0]/float(x[1][1]), reverse=True)

    final_150 = predicted_items[:150] 

    accuracy = find_accuracy(final_150, to_be_removed) 
    while accuracy < 5:
        print k, accuracy
        k += 20

        predictions = predict_jobs_for_users(users2, users_features, apps_t2_jobs, jobs, k)

        predicted_items = sorted(predictions.items(), key=lambda x: x[1][0]/float(x[1][1]), reverse=True)

        final_150 = predicted_items[:150] 

    print k, accuracy

    #t2_jobs = get_t2_jobs(jobs, t2_cutoff)

    #print "jobs len", len(jobs)
    #print "apps with t2 jobs len", len(apps_t2_jobs)

    #users2_t2_jobs = dist_users2_jobs(users, users2, apps_t2_jobs) 

    #print len(users2_t2_jobs)
    #raw_input()

    write_result(final_150, to_be_removed)

    #print 'users', len(users)
    #print 'apps', len(apps)
    #print 'jobs', len(jobs)
    #print 'user_history', len(user_history)
    #print 'users2', len(users2)
