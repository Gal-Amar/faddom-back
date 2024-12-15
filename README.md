# Welcome to faddomm-back project

This project serves as the backend for the faddomm-front. It connects to AWS using the boto3 library to retrieve data. The process involves:

1. Accessing EC2 data and searching for an instance ID by IP address.
2. Retrieving the CPUUtilization data from AWS CloudWatch.

## Prerequisites

- Python 3.x or higher

## Setup Instructions

1. **Create and activate a virtual environment**

   ```bash
   python -m venv myenv
   ```

2. **Activate the virtual environment**

   - On **Linux/MacOS**:

     ```bash
     source myenv/bin/activate
     ```

   - On **Windows**:

     ```bash
     myenv\Scripts\activate
     ```

3. **Install project dependencies** 

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the project**

   ```bash
   fastapi dev main.py
   ```

## Deactivate the virtual environment

When you're done working, deactivate the virtual environment:

```bash
deactivate
```
