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
    - `JsonHandler.py` -  JSON operations
    - `Validations.py` - Input data validation functions
  - **Presentation** - Interface program
    - `__init__.py` - Package initialization file
- **Tests** - Related to tests
  - `__init__.py` - Package initialization file
  - `AllTests.py` - Unified test runner
  - `TestDataGenerator.py` - Generator of test data
- **Data** - Data storage
    - **TestData** - Test data files
      - `TestData.json` - Test user data
- **PathConfig.py** - Files path configuration
- **Main.py** - Main application
- **requirements.txt** - Dependencies