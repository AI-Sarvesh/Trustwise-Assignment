# React + Vite
This is the frontend part of the project, built using React and Vite. It provides a user interface for text analysis, allowing users to input text and receive insights based on hallucination scores and emotional analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Text Analysis**: Users can input text and receive analysis results, including hallucination scores and emotional insights.
- **Responsive Design**: The application is designed to work on various screen sizes.
- **Real-time Feedback**: Users receive immediate feedback on their input.
- **Data Visualization**: Results are displayed using charts for better understanding.

## Installation

To set up the frontend application, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject/frontend
   ```

2. **Install dependencies**:
   Make sure you have [Node.js](https://nodejs.org/) installed. Then run:
   ```bash
   npm install
   ```

3. **Environment Variables**:
   Create a `.env` file in the `frontend` directory and add the following variables:
   ```env
   VITE_API_URL=http://localhost:8000
   ```


## Usage

To start the development server, run:
npm run dev

This will start the Vite development server, and you can access the application at `http://localhost:5173`.

### Building for Production

To build the application for production, run:

npm run build

The built files will be available in the `dist` directory.

