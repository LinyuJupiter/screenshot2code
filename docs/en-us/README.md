# screenshot2code

<p align="center">
  <a href="https://linyujupiter.github.io/screenshot2code/#/en-us/">English</a> |
  <a href="https://linyujupiter.github.io/screenshot2code/">简体中文</a>
</p>



A simple tool that uses AI to convert screenshots into pure code.

<img src="images/README/demo.gif" alt="Demo Image">

## 🎉 Features
- **HTML+tailwind**: Converts screenshots into HTML+tailwind.
- **GLM-4 Support**: Recognizes images using GLM-4v and generates code with GLM-4.
- **cogview-3 Support**: Generates example images using cogview-3.
- **More features**: Under development.

## 🚀 Ready to Use
This project currently runs only on Windows systems.

You can directly download and use the Windows installer of this project from [Releases](https://github.com/LinyuJupiter/screenshot2code/releases), install and use it according to the installer without configuring any dependencies.

Alternatively, you can download Screenshot2code.7z from [Releases](https://github.com/LinyuJupiter/screenshot2code/releases) and extract it. Double-click on /Screenshot2code/Screenshot2code.exe to run it without configuring any dependencies.

## 🛠 Local Setup

This project is a front-end and back-end separated project. The front-end is a graphical interface running on Windows system built using PyQt5, and the back-end is a service written in FastAPI that can run on Windows system or Linux server.

To run this project, you need to install Python 3.8 or higher version. First, clone this repository:

```bash
git clone https://github.com/LinYujupiter/screenshot2code.git
cd screenshot2code
```

### 1. Environment Setup

#### · Using Conda

If you are using Conda, you can set up and activate a virtual environment by following these steps:

1. **Create a virtual environment**:

   ```bash
   conda create -n screenshot2code python=3.8
   ```

2. **Activate the virtual environment**:

   ```bash
   conda activate screenshot2code
   ```

3. **Install dependencies**:

   While the virtual environment is activated, run:

   ```bash
   pip install -r requirements.txt
   ```

#### · Without Conda

If you are not using Conda, you can directly install dependencies using pip:

```bash
pip install -r requirements.txt
```

### 2. Run the Backend Service

After installing all dependencies, you can start the backend service with the following command:

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 7001

# Alternatively, use the following command
python3 start.py
```

On a Linux server, you can also start or stop the backend service with the following commands:

```bash
cd backend
sh run.sh  # Start the service
sh stop.sh # Stop the service
```

On a Windows system, you can also start or stop the backend service with the following commands:

```bash
cd backend
run.bat  # Start the service
stop.bat   # Stop the service

# Alternatively, use the following command
python3 start.py
```

On a Windows system, you can also download backend.7z from [Releases](https://github.com/LinyuJupiter/screenshot2code/releases) and extract it. Double-click on /backend/backend.exe to run it without configuring any dependencies.

### 3. Run the Frontend Interface

The frontend program can only run on Windows system. After installing all dependencies, you can start the frontend program with the following command:

```bash
cd frontend
python3 main.py
```

You can also download frontend.7z from [Releases](https://github.com/LinyuJupiter/screenshot2code/releases) and extract it. Double-click on /frontend/frontend.exe to run it without configuring any dependencies.



## 📚 Running Examples

**NYTimes**

| Original Image                                                                                                                                                  | Converted Image                                                                                                                                                |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="1238" alt="Screenshot 2023-11-20 at 12 54 03 PM" src="images/README/img1.png"> | <img width="1414" alt="Screenshot 2023-11-20 at 12 59 56 PM" src="images/README/img2.png"> |

## 🙋‍♂️ FAQs

- **What is the logic behind code generation?** - This program first sends the screenshot to the GLM-4v model to generate image descriptions, then sends the generated descriptions to the GLM-4 model to generate code, and finally sends the alt descriptions of the images in the generated code to the cogview-3 model to generate images.
- **Why is my generated code different from the expected result?** - Please check if your screenshot is clear and make sure it contains enough information to generate the correct code. If your screenshot still cannot generate the correct code, try taking a new screenshot or contacting me.
- **How can I obtain the API key for zhipu?** - Please go to the [Zhipu Developer Platform](https://maas.aminer.cn/usercenter/apikeys) to obtain it.
- **How to configure environment variables for the backend server?** - Please modify the corresponding variables in config.json when running the backend service.
- **How can I provide feedback?** - You can submit issues or suggestions in [GitHub Issues](https://github.com/LinYujupiter/screenshot2code/issues). You can also contact me through the contact information on [my homepage](https://github.com/LinYujupiter).


## 🙈 TODO

- [ ] Add questioning logic to handle code being truncated due to reaching the maximum output token.
- [ ] Support more image recognition models.
- [ ] Support more image generation models.
- [ ] Add image comparison logic to let AI evaluate the differences between the generated webpage and the original screenshot and modify the code.
- [ ] Add web front-end interface.
- [ ] Add custom code templates.
- [ ] Add more code technology stacks.

## 🤝 Contribution Guidelines
You can submit issues or suggestions in [GitHub Issues](https://github.com/LinYujupiter/screenshot2code/issues).

You can also refer to our [project documentation](https://linyujupiter.github.io/screenshot2code/) to learn how to contribute to this project and submit your code changes in [GitHub pull requests](https://github.com/LinYujupiter/screenshot2code/pulls).

We welcome any form of contribution, whether it's proposing new features, improving code, or reporting issues. Please make sure to follow best practices and code style guidelines.

Thanks to all contributors for their contributions to this project!