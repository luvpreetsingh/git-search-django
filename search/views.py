from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .forms import SearchForm
import json
import requests
# Create your views here.

url = 'https://api.github.com/users/'

def home(request):
	if request.method == 'POST':
		form = SearchForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			user_url = url + username
			user_info_r = requests.get(user_url)
			print(username)
			print(user_info_r.status_code)
			if user_info_r.status_code != 200:
				error_url = reverse('search:error')
				return HttpResponseRedirect(error_url)
			results_url = reverse('search:results', kwargs={'username':username})
			print(results_url)
			return HttpResponseRedirect(results_url)
	else:
		form = SearchForm()

	context = {'form':form}
	return render(request, 'search.html', context)
	
def error(request):
	return render(request, 'error.html')


def results(request, username):
	print("helloo")
	user_url = url + username
	user_info_r = requests.get(user_url)
	user_info = get_repos(user_info_r)
	repo_no = len(user_info)
	context = {'user_info':user_info, 'repo_no':repo_no}
	return render(request, 'results.html', context)


def get_repos(user_info_r):
	user_info = json.loads(user_info_r.text)
	repos_url = user_info['repos_url']
	repo_info_r = requests.get(repos_url)
	repo_info = json.loads(repo_info_r.text)
	print("Number of repositories --> " + str(len(repo_info)))
	print(repo_info)
	repo_count = 0
	repo_list = []
	for repo in repo_info:
		repo_dict = {}
		repo_name = (repo['name'])
		repo_id = repo['id']
		repo_dict["id"] = repo_id
		repo_dict["name"] = repo_name 
		print("Repository name is " + repo_name)
		branch_list = get_branches(repo)
		commit_list = get_commits(repo)
		repo_dict['commits'] = commit_list
		repo_dict['branches'] = branch_list
		repo_list.append(repo_dict)
		print("\n")
	return repo_list

def get_branches(repo_json):
	repo_name = repo_json['name']
	branches_url = repo_json['branches_url']
	branch_info_r = requests.get(branches_url[:-9])
	branch_info = json.loads(branch_info_r.text)
	print("Number of branches --> " + str(len(branch_info)))
	branch_count = 1
	branch_list = []
	for branch in branch_info:
		branch_dict = {}
		branch_dict['name'] = branch['name']
		branch_list.append(branch_dict)
	return branch_list

def get_commits(repo_json):
	commits_url = repo_json['commits_url']
	commit_info_r = requests.get(commits_url[:-6])
	commit_info = json.loads(commit_info_r.text)
	print("Number of commits --> " + str(len(commit_info)))
	commit_count = 1
	commit_list = []
	for commit in commit_info:
		commit_dict = {}
		commit_dict['message'] = commit['commit']['message']
		commit_list.append(commit_dict)
	return commit_list
