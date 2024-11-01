# DW MecKey Project

A data warehouse project for collecting mechanical keyboard data using Python.

## Description

This project implements a data pipeline to extract, transform and load (ETL) mechanical keyboard data from various sources. It features a GUI interface for monitoring the process and uses an event-driven architecture for communication between components.

## Features

- GUI interface for monitoring extraction progress
- Event-driven architecture using pub/sub pattern  
- Database integration for storing configuration and logs
- Modular design with dependency injection
- Currently supports extracting data from Akko website

## Prerequisites

- Python 3.x
- Required packages (install using `pip install -r requirements.txt`):
  - python-dotenv
  - numpy
  - requests 
  - pandas
  - bs4 (BeautifulSoup4)
  - schedule
  - pymysql
  - injector
  - mypy

## Project Structure
GitHub Copilot
Here's the README in Markdown format that you can directly save as README.md:

```
├── app_module/         # Dependency injection configuration 
├── controller/         # Application controller 
├── db/                 # Database management 
├── event/              # Event system components 
├── gui/                # GUI implementation 
├── model/              # Data models 
├── services/           # Business logic services 
│   ├── extract/        # Data extraction services 
│   ├── load/           # Data loading services
    ├── transform/      # Data transformation services
│   └── process/        # Data processing services 
└── utils/              # Utility functions
```


## Setup

1. Clone the repository
```bash
    git clone https://github.com/nphuonha2101/DW_MecKey.git
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add the following environment variables:
```bash
CONTROL_DB_HOST=your_host
CONTROL_DB_USER=your_user
CONTROL_DB_PASSWORD=your_password  
CONTROL_DB_NAME=your_db_name
FILE_CONFIG_TABLE_NAME=your_config_table
FILE_LOG_TABLE_NAME=your_log_table
AKKO_FEED_KEY=your_feed_key
AKKO_PAGE=number_of_pages
```