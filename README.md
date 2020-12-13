Программа для графического построения сетей из функциональных элементов.

Как работать с программой:

1)Нарисуйте СФЭ:

После запуска в верхней части экрана появится выбор - какой элемент нарисовать:

![](picture/elements_example.png)

При нажатии на одну из 8 кнопок она выделяется зеленым

![](picture/selection_example.png)

Нажатие на экран рисует выбранный(подсвеченный зеленым) элемент

![](picture/OR_example.png)

Если какой-то элемент СФЭ надо удалить:

Нажмите "Удалить"

![](picture/DEL_selection.png)

Она загорится зеленым и на СФЭ появятся красные точки

![](picture/DEL_example.png)

При нажатии на точку на элементе он удаляется.

2)Вычисление значений:

Когда вы нарисовали СФЭ(на рисунке XOR) в левом нижнем углу задайте значения входных переменных(в соответсвии с их нумерацией в СФЭ) и нажмите "задать Start". Помимо значений можно передавать битовую маску заменяя какие - то входы знаком "?", тогда алгоритм выдаст результат для каждого возможного значения

![](picture/start_example.png)

или

![](picture/mask_start_example.png)

Если кнопка "задать Start" не активна, проверьте СФЭ, в нем есть элементы, которые посчитать невозможно(присутствует цикл или не все входы в элемент использованы)

![](picture/none_start_example.png)

После чего появится кнопка "Посчитать"

![](picture/build_example.png)

При нажатии на нее в правом нижнем поле появится результат работы(или сообщение об ошибке, если посчитать финальные состояния нельзя). Если вы передали не значения а маску, то появится новое окно со списком значений и результатом работы на каждом

![](picture/finish_example.png)

или

![](picture/mask_finish_example.png)