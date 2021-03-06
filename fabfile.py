# example:
# fab test:update --hosts="lala@test.smdev.cz"

from deployment.projects import ManagePyProject as BaseProject
from deployment.base import test_dj_deployment_factory, production_dj_deployment_factory


class Project(BaseProject):

    project_name = '{{ project_name }}'
    repo_name = '%(repo_name)s'
    supervisor_name = '%(supervisor_name)s'


test = test_dj_deployment_factory(Project)()
prod = production_dj_deployment_factory(Project)()
