
# Welcome to The New York times bot 👋
This bot scraps data from The New York times **[site](http://www.nytimes.com/)**. The bot scraps image, title, description, and date from the listing page. Bot is also able to apply `news section` and `date filter` on news listing.

## Bot output
Bot collects and stores various data from the site. Scarpper output consist of an images archive and excel workbook.
- Images Archive: Images archive contains all feature images of the news visible on listing page.
- Excel workbook: It is an excel file created with following data title, description, date, picture filename, count of search phrase in the title and description, True/False depending on wether title or description contains any mention of money.


## Folder structure
```bash
.
├── LICENSE
├── README.md
├── conda.yaml
├── geckodriver.log
├── output
│   ├── news.xlsx
│   └── news_images.zip
├── requirements.txt
├── robot.yaml
├── scrapper
│   ├── __init__.py
│   ├── tasks
│   │   ├── __init__.py
│   │   ├── callbacks.py
│   │   └── surf_web.py
│   └── utils
│       ├── __init__.py
│       ├── browserwrapper.py
│       ├── constants.py
│       └── helper.py
└── tasks.py
```
- **tasks.py**: This is the main file for the bot. This files loads the configuration and initialize a selenium worker to open browser and load site.
- **conda.yaml**: This file contains configuation for a conda environment. This file is used by **`rcc`** to initialize a conda virutal environment and start the bot.
- **output**: This directory is crated when bot starts execution. A new output directory is created for each run. Same output directory is newer used twice. 
- **requirements.txt**: This file contains requirement for development. It is used during development to setup a development environment.
- **robot.yaml**: This file contain configuration for Robocorp to run the bot.
- **scrapper**: This Python package cotains various Python modules to parse, extract, and store news content.
- **callbacks.py**: This file contains call back method called by `browserwrapper` class to perform various task. For example, there is a method named `handle_terms_popup_callback` which is used to close popup such as terms and conditions, privacy policy, or cookie policy.
- **surf_web.py**: This file contains the main business logic for the bot. This file contain code which makes necessary calls to method from other modules to load, parse, extract, and store data from news site.
- **utils**: This Python package contains utility methods. These are generic methods which are used to call a repeating action again and again to achieve **`DRY`** principle.
- **browserwrapper.py**: This file contains a utility class. The class is used to create an instance of selenium worker to lunch a browser, parse, and extract content. The class is written using `Singleton` pattern. Idea for writing the class using `Singleton` pattern is that: multiple selenium worker are not needed since operation are performed on current loaded page. So, creating a `SingleTon` class ensure that no matter which module initialize an instace of the class, it is guaranteed to have same selenium worker.
- **constants.py**: This file contains values which will not change during program execution. It will remain same no matter which state or which action is performed.
- **helper.py**: This file contains methods which are called by other methods to perform repeating tasks. Reason for keeping these methods in separate file is to avoid rewriting same code over and over again.

## Development environment setup

Note: Python 3.9 is required for this project.


1. Create a virtual environment by using following command:
```bash
virtualenv -p python3.9 venv
```
2. Activate the virtual environemnt
```bash
source venv/bin/activate
```
3. Install requirement in the virtual environment
```bash
pip install -r requirements.txt
```
4. To change search phrase, number of months, and sections, update the `constants.py` file. Update these variables in `constants.py` file.
```Python
    search_phrase = 'python'
    sections = []
    number_of_month = 1
```
5. Run the bot
```bash
python tasks.py
```

## Testing on local environment

Note:
RCC Tool chain from Robocorp is requried to test the bot on local. To install RCC Tool chain follow this [github link](https://github.com/robocorp/rcc).

To test the bot on local machine run this command in terminal
```bash
rcc run
```
This command will setup an environment for the bot. After environment setup is complete, it will execute the bot in similar manner as it will be executed on Robocorp server.

## Deploying on Robo corp

**Note:**
To deploy on Robocrop, you will need to setup workitems first.

Work Items: Work items are inputs given to bot running on Robocorp server. There are three workitems which needs to be defined for the bot to work properly. The workitems names are `search_phrase`, `sections`, and `number_of_months`.

- `search_phrase`: Used by bot to search news articiles on the site.
- `sections`: Used by bot to apply news section filter on searched articiles. Possible values for `sections` filter are 
```
Arts
Business
New York
Opinion
Podcasts
Style
Technology
U.S.
World
```
The values are case sensitive and must be given as it is. By default `any` section is selected on the sites.
- `number_of_months`: Used by bot to apply date range filter on the news articiles. `0` and `1` means current month news, `2` means current and previous month news, `3` means current and two previous months news, and so on.

For example, a workitem to filter news for `Crypto` for current month and `Arts` section will look like this
```JSON
{
    "search_phrase": "Crypto",
    "sections": ["Arts"],
    "number_of_months": 0
}
```

For instruction on how to setup workitems on Robocorp, please follow this link: [Robocorp workitems](https://youtu.be/XczuMYkCvRE)

Also, setup environment variable `ENV` for the process. Value of `ENV` variable should be `PROD`