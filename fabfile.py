import os
from fabric.api import *
from fabric.operations import get, put
from fabric.contrib.console import confirm
from fabric.contrib.project import rsync_project
from fab_settings import PROJECT_NAME, PROJECT_HOST, PROJECT_USER, PROJECT_DB_NAME, SUDOER_USER


env.forward_agent = True
env.project_name = PROJECT_NAME
env.project_user = PROJECT_USER
env.roledefs = {
    PROJECT_USER: ['%s@%s' % (PROJECT_USER, PROJECT_HOST)],
    'sudoer': ['%s@%s' % (SUDOER_USER, PROJECT_HOST)]
    }
env.hosts = [PROJECT_HOST]
env.project_path = "/home/" + env.project_name + "/www/" + env.project_name + "/"
env.python_path = "/home/" + env.project_name + "/.virtualenvs/" + env.project_name + "/bin/python"
env.pip_path = "/home/" + env.project_name + "/.virtualenvs/" + env.project_name + "/bin/pip"
env.project_media_dir = '/var/www/%s/media/' % env.project_name


@roles('%s' % PROJECT_USER)
def git_status():
    with cd(env['project_path']):
        run('git fetch && git status')


@roles('%s' % PROJECT_USER)
def pushpull():
    local("git push origin master")
    with settings(user=PROJECT_USER):
        with cd(env['project_path']):
            run('git pull')


@roles('sudoer')
def reloadapp():
    sudo('supervisorctl restart %s' % env.project_name, shell=False)
    sudo('service nginx reload', shell=False)


@roles('%s' % PROJECT_USER)
def release(run_migrate=True, static=True):
    pushpull()
    run('%s install -r %spip-requirements.txt' %
        (env['pip_path'], env['project_path']))
    with cd(env['project_path']):
        if run_migrate:
            migrate()
        if static:
            _run_manage('collectstatic --noinput')
    reloadapp()


@roles('%s' % PROJECT_USER)
def migrate():
    with cd(env['project_path']):
        _run_manage('migrate')


@roles('%s' % PROJECT_USER)
def pulldb():
    filename = 'mysql_dumped.sql'
    dump_file = '%s' % filename
    run(_dump_mysql_data(dump_file))
    get(dump_file, '.')
    run('rm %s' % dump_file)
    if confirm("Load dumped remote data into local DB?"):
        local('mysql --defaults-file=".mysqldump" %s < %s' % (env['project_name'], filename))


def _run_manage(command):
    run("%s ./manage.py %s" % (env['python_path'], command))

def _dump_mysql_data(file_path):
    return 'mysqldump --defaults-file="/home/jellyrisk/.mysqldump_cnf" --single-transaction %s > %s' % (PROJECT_DB_NAME, file_path)

@roles('%s' % PROJECT_USER)
def syncmedia():
    get(env['project_media_dir'], local_path=".")
