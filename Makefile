format:
	uv run ruff format
	uv run ruff check --fix
	uv run isort .

learning-path:
	uv run python modules/learning_path_generator/main.py

salary-analysis:
	uv run python modules/cv_to_salary/main.py
