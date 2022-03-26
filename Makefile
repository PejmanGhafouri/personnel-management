compile_requirements:
	pip-compile requirements/dev.in
	pip-compile requirements/prod.in

git.init_pre_commit:
	pre-commit install
	pre-commit install --hook-type pre-push

remove_migrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
