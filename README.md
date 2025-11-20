# Program Architecture

## Project Structure

- **SRC** - 
  - **Domain** - Business logic layer (core program functionality)
    - `__init__.py` - Package initialization file
    - `User.py` - User classes
    - `Calculators.py` - Calculator classes and methods
    - `GenericConstants.py` - Constant values and configurations
    - `UserProfileCollector` - Collect user information and nutri results
  - **Infrastructure** - External dependencies and technical components
    - `__init__.py` - Package initialization file
    - `JsonHandler.py` -  JSON operations
    - `Validations.py` - Input data validation functions
    - `Authorization.py` - Autorization system
    - `Types.py` - Types data for Infrastructure
  - **Presentation** - Interface program
    - `__init__.py` - Package initialization file
    - `CLI.py` - Console line interface
- **Tests** - Related to tests
  - `__init__.py` - Package initialization file
  - `test_Domain_Classes.py` - Domain test runner
- **Data** - Data storages
    - `UsersData.json` - Data of users
    - `LogsData.json` - Data of users log
- **PathConfig.py** - Files path configuration
- **Main.py** - Main application
- **requirements.txt** - Dependencies