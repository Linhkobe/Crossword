# <span style="color: #006666;">App Mobile Crossword</span>

## <span style="color: #006666;">Introduction</span>
Welcome to the Crossword Solver App! This application allows users to upload images of crossword grids and definitions, processes them, and displays the crossword puzzle with clues. The app is built using React Native for the frontend and Flask for the backend.

## <span style="color: 006666;">Link DEMO on youtube</span>
<p style="text-align: center;">
    <a href="https://www.youtube.com/watch?v=tCJyifAEAJY" style="text-decoration: none;">
        <span style="font-size: 20px;">Click here</span> 
        <span style="font-size: 20px;">👇</span>
        <br>
        <img src="https://img.youtube.com/vi/tCJyifAEAJY/0.jpg" alt="Watch the video" width="300"/>
    </a>
</p>


## <span style="color: #006666;">Features</span>
- Upload and process crossword grid images.
- Upload and process crossword definition images.
- Display the crossword grid and clues.
- Animations to enhance user experience.

## <span style="color: #006666;">Prerequisites</span>
- Node.js and npm installed.
- Python and pip installed.
- Expo CLI installed.

## <span style="color: #006666;">Setup and Run the Project</span>

### <span style="color: #006666;">Steps to Clone and Setup</span>

1. **Clone the Repository**
    ```bash
    git clone https://github.com/mythy203/app_mobile_crossword.git
    cd app_mobile_crossword
    ```

2. **Backend Setup (Python Flask)**
    ```bash
    cd Backend
    pip install flask flask-cors
    pip install openai googletrans==4.0.0-rc1
    ```

3. **Frontend Setup (React Native with Expo)**
    ```bash
    cd AppCrossword
    npm install -g expo-cli
    npm install
    npx expo install expo-camera expo-image-picker
    ```
4. **Set the OpenAI API key in prompt_engine.py**
    ```bash
    openai.api_key = 'YOUR_API_KEY'
    ```

### <span style="color: #006666;">Steps to Run the Application</span>

1. **Run Backend**
    ```bash
    cd Backend
    export FLASK_APP=app.py
    export FLASK_RUN_HOST=0.0.0.0
    flask run
    ```

2. **Run Frontend**
    ```bash
    cd AppCrossword
    npx expo start -c
    ```

3. **Test by your phone**:
- You have to install an application "expo go" in your phone <img src="image.png" alt="expo go" width="25"/> and then you open the camera of the phone, scan the QR code in the terminal of frontend, it opens our application.

### <span style="color: #006666;">Note</span>
- Ensure both your PC and iPhone are connected to the same Wi-Fi network.
