# Swiss German Dialect Detection: Back End

The "Swiss German Dialect Detection" is a project as part of the "Essentials of Text and Speech Processing" course in the autumn semester 2023 at the University of Zurich. The project aims to detect Swiss German dialects based on user input. This README will guide you on setting up and running the back end part of the project, provide an overview of its main functions.

## Table of Contents
- [Usage](#usage)
- [Project Overview](#project-overview)
- [Deploying the project](#deploying-the-project)
- [Contributing](#contributing)
- [License](#license)


## Usage

To use the "Swiss German Dialect Detection" application, follow these steps:

1. Open the deployed web application in your browser by navigating to [seashell-app-xnkoa.ondigitalocean.app](https://seashell-app-xnkoa.ondigitalocean.app/) or deploy your own version of the repo (see section [Deploying the project](#deploying-the-project)) and open it on your local machine (port 3000).

2. Enter the text in the input form and ensure it is meaningful for dialect prediction.

3. Click the "Ask the AI" button to start the prediction process.

4. The application will go through the thinking stage, and once complete, it will display the predicted dialect and a certainty score.

5. If you agree with the prediction, you can confirm it. If you believe the prediction is incorrect, you can provide feedback and select the correct dialect.

6. The feedback is used to improve the model's accuracy.

## Project Component Overview

The "Swiss German Dialect Detection" project is a react-based application that detects Swiss German dialects based on user input. This repository contains the front end code which provides an intuitive interface for users to input text. When a back end is also deployed, the server side system analyzes the text to predict the dialect spoken. The front end project includes the following main components:

1. **Input Form**: Users can enter text to be analyzed to predict the Swiss German dialect they might be speaking.

2. **Thinking Stage**: This stage shows a processing animation while the system analyzes the input.

3. **Result Stage**: After processing, the system displays the predicted dialect along with a certainty score. Users can confirm the prediction or provide feedback if they believe the prediction is incorrect.

The project also features a dynamic background with animated blobs and provides user-friendly feedback during the process.

## Deploying the project

<blockquote>In order to have a working application you will need to also follow the steps outlined in <a href="https://github.com/amoscalamida/essentials-nlp-frontend.git">amoscalamida/essentials-nlp-frontend</a> to deploy a front end instance.</blockquote>

---
Follow these steps to get the front-end project up and running:

1. Clone the repository:
   ```bash
   git clone https://github.com/amoscalamida/essentials-nlp-backend.git
   ```

2. Navigate to the project directory:
   ```bash
   cd essentials-nlp-backend
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up the frontend URL by modifying the `origins` in the `__init__.py` file. Make sure it points to your frontend server.

5. Start the development server:
   ```bash
   flask --app backend run
   ```


## License

This project is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.

Please feel free to reach out if you have any questions or need further assistance with the project.
