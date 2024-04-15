# Anime Game Character Fusion Generator

## Overview

The Anime Game Character Fusion Generator is a fun and creative side project designed to blend elements of anime characters with specific game themes, producing unique and visually appealing images. Leveraging the power of the `cagliostrolab/animagine-xl-3.1` library for anime character generation and the `igdb` (Internet Game Database) API for accessing game data, this project offers users the ability to generate personalized profile pictures that reflect their favorite anime and gaming interests.

## Features

- **Anime Character Generation**: Utilizes the `cagliostrolab/animagine-xl-3.1` library to create anime-style characters.

- **Game Theme Integration**: Integrates elements from specific games into the generated anime characters, allowing users to select their favorite games.

- **Profile Picture Generator**: Generates images suitable for use as profile pictures on social media platforms, gaming forums, or other online communities, providing users with a personalized and visually striking representation of their interests.

## Installation

1. Clone the repository from GitHub:

    ```bash
    git clone https://github.com/your-username/anime-game-character-fusion.git
    ```

2. Install dependencies using pip:

    ```bash
    pip install -r requirements.txt
    ```

3. (Optional) [Install Sass](https://sass-lang.com/install/) and compile Sass file into CSS:

    ```bash
    sass ./resources/form.scss ./resources/form.css
    ```

4. Obtain API credentials for the `igdb` API and set them as environment variables TWITCH_CLIENT_ID & TWITCH_CLIENT_SECRET with your actual API key.

## Installation (Optional: CUDA Support)

If you have an NVIDIA GPU with CUDA support and want to accelerate image generation, follow these additional steps:

1. Ensure you have CUDA installed on your system. Refer to the [NVIDIA CUDA Toolkit documentation](https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html) for installation instructions specific to your operating system.

2. Once CUDA is installed, reinstall [pytorch](https://pytorch.org/get-started/locally/):

    ```bash
    pip uninstall torch
    #command from link above
    ```

3. Run the project as usual, and image generation should now benefit from GPU acceleration, resulting in faster processing times.

Note: CUDA support may require additional configuration and setup, and not all systems or GPUs may be compatible. Refer to the documentation provided by NVIDIA and the `cagliostrolab/animagine-xl-3.1` library for more detailed information on enabling CUDA support.

## Usage

1. Run the main script:

    ```bash
    python main.py
    ```

2. Follow the gui to customize your anime character and select game elements to incorporate into the fusion.

3. Once satisfied with the selections, the generated image will be previewed and can be saved to the specified directory.

## Dependencies

- [cagliostrolab/animagine-xl-3.1](https://huggingface.co/cagliostrolab/animagine-xl-3.1): A powerful library for generating anime-style characters with customizable attributes.

- [igdb API](https://www.igdb.com/api): Provides access to a vast database of game-related information, allowing integration of game elements into the generated images.

## Contributing

Contributions to the project are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to submit a pull request. Please adhere to the established coding conventions and follow the project's code of conduct.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Special thanks to the developers of `cagliostrolab/animagine-xl-3.1` for providing a fantastic library for anime character generation.
- Thanks to the creators of the `igdb` API for enabling access to comprehensive game data.
- Special thanks to the `PySide6` developers for providing a powerful toolkit for creating cross-platform desktop applications with Python.
- Thanks to the `NLTK` developers for creating a comprehensive library for natural language processing tasks in Python.
- Acknowledgements to the `requests_cache` developers for offering a convenient way to cache HTTP responses in Python applications.
- Thanks to the `PyTorch` developers for developing an efficient and flexible deep learning framework for research and production.
- Gratitude to the developers of `thefuzz` for providing a useful library for fuzzy string matching, enhancing the accuracy of character name search.