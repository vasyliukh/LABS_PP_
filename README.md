# app.py
1. Клонування репозиторі
Для початку потрібно втсановити Git, якщо він у вас не встановлений:
1. Для Windows - http://git-scm.com/download/win
2. Для Linux - http://git-scm.com/download/linux
3. Для Mac - http://git-scm.com/download/mac

•Спочатку необхідно створити папку, куди ми будемо клонувати репозиторі
•Далі, нажимаємо правою кнопкою миші на папку та вибираємо опцію Git Bash here

2. Інсталяція python та віртуального середовища
(For Windows)

1. Інсталюєм pyenv для встановлення python
•Для цього необхідно відкрити командний рядок та ввести наступну команду:
pip install pyenv-win --target %USERPROFILE%\.pyenv
•Далі, відкриваємо програму PowerShell, де вводимо команди:
[System.Environment]::SetEnvironmentVariable('PYENV',$env:USERPROFILE + "\.pyenv\pyenv-win\","User")
[System.Environment]::SetEnvironmentVariable('path', $HOME + "\.pyenv\pyenv-win\bin;" + $HOME + "\.pyenv\pyenv-win\shims;" + $env:Path,"User")
Для перевірки, вводимо у командному рядку команду pyenv --version, яка повинна показати версію встановленого pyenv
Детальніше на сайті https://pypi.org/project/pyenv-win/

2. Встановлення python та віртуального середовища pipenv
•Для встановлення python вводимо наступну команду в терміналі:
pyenv install 3.7.9
•Для встановлення pipenv:
pip install pipenv
3. Запуск у PyCharm
Для запуску проекту, необхідно:
1.Відкрити PyCharm та відкрити папку проекту
2.Підключити бібліотек gevent у терміналі за допомогою команди pipenv install gevent
3.Скомпілювати код
4.Після запуску перейшовши за адресою http://localhost:5000/api/v1/hello-world-4, ви побачити текст "Hello world! "
