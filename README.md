# Makefile Parser

makefile-parser is a Python utility designed to parse GNU Makefiles and extract variables, targets, and their associated
commands. It processes variable assignments, resolves variable substitutions, and provides a structured representation
of the Makefile content. This tool is especially useful for developers who need to analyze or manipulate Makefiles
programmatically.

## Features:

- Parse Variable Assignments: Supports both = and := assignment operators.


- Resolve Variable Substitutions: Handles recursive variable substitution within variable values and command lines.


- Extract Targets and Commands: Captures all targets (rules) along with their associated commands, including multi-line
  commands and conditionals.


- Handle Conditional Statements: Includes non-indented lines like ifeq, else, and endif within targets.


- Provide Structured Output: Returns a dictionary containing variables and rules for easy programmatic access.

## Sample Input and Output:

### Example

### Makefile
```
CC = gcc
CFLAGS = -Wall -g
SRC_DIR = src
BUILD_DIR = build

all: build

build:
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) $(SRC_DIR)/main.c -o $(BUILD_DIR)/main

```

### command
```
parse_make -f .\Makefile -c build
```

### output
```
mkdir -p build gcc -Wall -g src/main.c -o build/main
```
### Example:02

### Sample Makefile
```
# Variables
CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -g
LDFLAGS = -lm
SRC_DIR = src
BUILD_DIR = build
INCLUDE_DIR = include
TARGET = $(BUILD_DIR)/my_program

# Automatic variables
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(SRCS:$(SRC_DIR)/%.cpp=$(BUILD_DIR)/%.o)

# Phony targets
.PHONY: all clean rebuild run

# Default target
all: $(TARGET)

# Linking the target
$(TARGET): $(OBJS)
	@echo "Linking $(TARGET)..."
	$(CXX) $(CXXFLAGS) -I$(INCLUDE_DIR) $^ -o $@ $(LDFLAGS)

# Compiling source files to object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(BUILD_DIR)
	@echo "Compiling $<..."
	$(CXX) $(CXXFLAGS) -I$(INCLUDE_DIR) -c $< -o $@

# Cleaning build files
clean:
	@echo "Cleaning up..."
	@rm -rf $(BUILD_DIR)

# Rebuilding the project
rebuild: clean all

# Running the program
run: all
	@echo "Running $(TARGET)..."
	@./$(TARGET)

# Catch-all target for invalid targets
%:
	@echo "Unknown target: $@"
	@echo "Available targets: all, clean, rebuild, run"
```

### command
```
parse_make -f .\Makefile -c all
```

### output
```
build/my_program: $(SRCS:src/%.cpp=build/%.o) @echo "Linking build/my_program..." g++ -Wall -Wextra -std=c++17 -g -Iinclude $^ -o $@ -lm build/%.o: src/%.cpp @mkdir -p build @echo "Compiling $<..." g++ -Wall -Wextra -std=c++17 -g -Iinclude -c $< -o $@
```

## Requirements:
- Python >= 3.6

## Installation:

### Pip

```shell
pip install make-parser
```

### git repository

```
https://github.com/pssv7/make-parser.git
```

## Usage


```shell
parse_make -d [PATH_TO_MAKEFILE] -c [TARGET]
```

