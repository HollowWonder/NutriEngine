# Program Architecture

## Project Structure

- **SRC** - Folder with all scripts and library
  - **Domain** - Business logic layer (core program functionality)
    - `__init__.py` - Package initialization file
    - `User.py` - User classes
    - `Calculators.py` - Calculator classes and methods
    - `GenericConstants.py` - Constant values and configurations
  - **Infrastructure** - External dependencies and technical components
    - `__init__.py` - Package initialization file
    - `Validations.py` - Input data validation functions
  - **Presentation** - Interface program
    - `__init__.py` - Package initialization file
- **Data** - Folder with data files
- **venv** - Virtual environment with installed pip packages
- **Main.py** - Main application