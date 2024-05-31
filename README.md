## Overview
The MovieStarPlanet2 Scammer Detection & Reporting API is a tool designed to identify and report scammers within the MovieStarPlanet2 game environment. This API utilizes verified reports from users to check if a particular user is engaging in fraudulent activities.

## Features
- Scammer identification: The API utilizes advanced algorithms to analyze verified reports and detect potential scammers based on various criteria.
- Reporting functionality: Users can report suspicious activity directly through the API, contributing to the database of known scammers and enhancing community safety.
- Customizable integration: Developers can easily integrate the API into their existing applications or services with flexible implementation options.

## Getting Started
To get started with the MovieStarPlanet2 Scammer Detection & Reporting API, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
   
if you intend to start the server with a custom uvicorn command, remove the following block from your main script:
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
```

Use a custom uvicorn command:
```bash
uvicorn {script_name}:{app} --workers {NUM_WORKERS}
```
