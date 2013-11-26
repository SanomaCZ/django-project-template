# example:
# fab {{ project_name }}_on_test:update --hosts="sshanoma@test.smdev.cz"

from deployment.projects import Project as BaseProject
from deployment.machines import Machine
from deployment.base import TestMachine, Deployment as BaseDeployment


class NetworkMachine(Machine):
    """
    Use only as mixin
    """

    use_sudo = True
    use_nginx_in_supervisor = False
    python_version = 'python2.7'

    minion_user = '%(minion_user)s'

    forward_agent = True
    use_ssh_config = True

    etc_prefix = '/usr/local/etc'

    ln_packages = (
        '/usr/lib/python2.7/dist-packages/psycopg2-2.4.5.egg-info',
        '/usr/lib/python2.7/dist-packages/psycopg2',
        #'/usr/lib/python2.6/dist-packages/PIL.pth',
        #'/usr/lib/python2.6/dist-packages/PIL',
    )


class Project(BaseProject):

    project_name = '{{ project_name }}'

    repo_sources = {
        'pypi': '%(repo_name)s',
        'git': 'git+gitolite@git.smdev.cz:%(repo_name)s#egg={{ project_name }}',
    }

    supervisor_name = '%(supervisor_name)s-web'

    global_entry_points = ['{{ project_name }}_manage']


class TestDeployment(BaseDeployment, TestMachine, Project):
    ln_packages = (
        '/usr/lib/python2.6/dist-packages/psycopg2-2.2.1.egg-info',
        '/usr/lib/python2.6/dist-packages/mx',
        '/usr/lib/python2.6/dist-packages/psycopg2',
        #'/usr/lib/python2.6/dist-packages/PIL.pth',
        #'/usr/lib/python2.6/dist-packages/PIL',
    )


class NetworkDeployment(BaseDeployment, NetworkMachine, Project):
    pass

{{ project_name }}_on_test = TestDeployment()
{{ project_name }}_on_production = NetworkDeployment()
