# example:
# fab {{ project_name }}_on_test:update --hosts="sshanoma@test.smdev.cz"

from deployment.projects import ManagePyProject as BaseProject
from deployment.machines import ProductionMachine
from deployment.base import TestMachine, Deployment as BaseDeployment


class Project(BaseProject):

    project_name = '{{ project_name }}'

    repo_sources = {
        'pypi': '%(repo_name)s',
        'git': 'git+gitolite@git.smdev.cz:%(repo_name)s#egg={{ project_name }}',
    }

    supervisor_name = '%(supervisor_name)s'


class TestDeployment(BaseDeployment, TestMachine, Project):
    pass


class ProdDeployment(BaseDeployment, ProductionMachine, Project):
    pass

{{ project_name }}_on_test = TestDeployment()
{{ project_name }}_on_production = ProdDeployment()
