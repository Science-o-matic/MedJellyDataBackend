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
env.django_project_path = os.path.join(env.project_path, env.project_name)
env.python_path = "/home/" + env.project_name + "/.virtualenvs/" + env.project_name + "/bin/python"
env.pip_path = "/home/" + env.project_name + "/.virtualenvs/" + env.project_name + "/bin/pip"
env.project_media_dir = '/var/www/%s/media/' % env.project_name


def _booleanize(value):
    """Return value as a boolean."""

    true_values = ("yes", "true", "1")
    false_values = ("no", "false", "0")

    if isinstance(value, bool):
        return value

    if value.lower() in true_values:
        return True
    elif value.lower() in false_values:
        return False

    raise TypeError("Cannot booleanize ambiguous value '%s'" % value)


@roles('%s' % PROJECT_USER)
def git_status():
    with cd(env['project_path']):
        run('git fetch && git status')


@roles('%s' % PROJECT_USER)
def _git_update(branch):
    with settings(user=PROJECT_USER):
        with cd(env['project_path']):
            run('git fetch --all')
            run('git checkout %s' % branch)
            run('git reset --hard origin/%s' % branch)


@roles('sudoer')
def reloadapp():
    sudo('supervisorctl restart %s' % env.project_name, shell=False)


@roles('%s' % PROJECT_USER)
def release(run_migrate=True, static=True, branch='master'):
    run_migrate = _booleanize(run_migrate)
    static = _booleanize(static)

    _git_update(branch)

    run('%s install -r %spip-requirements.txt' %
        (env['pip_path'], env['project_path']))

    with cd(env['project_path']):
        if run_migrate:
            _run_manage('migrate')
        # todo
        # only if locale files present
        #run("%s ./manage.py compilemessages" % env['python_path'])
        if static:
            _run_manage('collectstatic --noinput')

    reloadapp()


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


def _run_django_admin(command):
    run("%s django-admin.py %s" % (env['python_path'], command))


def _dump_mysql_data(file_path):
    return 'mysqldump --defaults-file=".mysqldump_cnf" --single-transaction %s > %s' % (PROJECT_DB_NAME, file_path)


@roles('%s' % PROJECT_USER)
def syncmedia():
    get(env['project_media_dir'], local_path=".")
