# example:
# fab {{ project_name }}_on_test:update --hosts="sshanoma@test.smdev.cz"

from deployment.projects import ManagePyProject as BaseProject
from deployment.machines import ProductionMachine, TestMachine
from deployment.base import Deployment


class Project(BaseProject):

    project_name = '{{ project_name }}'
    repo_name = '%(repo_name)s'
    supervisor_name = '%(supervisor_name)s'


class TestDeployment(Deployment, TestMachine, Project):
    pass


class ProdDeployment(Deployment, ProductionMachine, Project):
    pass

{{ project_name }}_on_test = TestDeployment()
{{ project_name }}_on_production = ProdDeployment()
