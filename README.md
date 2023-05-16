# Credit card fraud detection system
Данный проект является тренировочным. Основой данного проекта являются [материалы](https://fraud-detection-handbook.github.io/fraud-detection-handbook/).



## Цели проекта и основные сложности

Цель данного проекта заключается создании системы обнаружения мошенничества с кредитными картами. 

То есть для каждой транзакции (например, оплата картой в кафе, банкомате или интернет магазине), надо предсказать является ли операция мошеннической. Данная задача является задачей классификацией с несбалансированными классами и для оценки ее эффективности применяются следующие метрики. 

Основными сложностями для данной задачи являются
- *Дисбаланс классов*. Большая часть транзакций более 99% - легитимные.
- *Изменения в данных (concept drift)*. Паттерны транзакции, не только  у мошенников, меняются с течением времени.
- *Вычисления в реальном времени (near real-time)*. Ограничение на время для таких систем составляет 10 миллисекунд, что для объема транзакций требует параллельности решения и высокой масштабируемости.
- *Категориальные признаки*. В признаки транзакций входит много категориальных признаков, что требует дополнительной обработки для ML алгоритмов. 
- *Наложение классов*. Имея только данные о происходящей транзакции почти не возможно отличить мошенников. Для разделения классов нужна дополнительная информация о клиенте, месте и способе транзакции. 
- *Показатели эффективности*. Нужно максимизировать обнаружения мошенников и минимизировать число ложно положительных предсказаний. 
- *Отсутствие общедоступных наборов данных*. По очевидным причинам конфиденциальности реальные транзакции по кредитным картам не могут быть опубликованы.


## Метрики проекта 

Идеальная система обнаружения мошеннических транзакций должна предоставлять оповещения, когда транзакции считаются наиболее подозрительными.
Другими словами система должна обнаруживать все мошеннические транзакции и максимизировать количество правильных классификаций.

Наиболее распространенные метрики для классификации:
*recall*, *specificity*, *precision*, *F1-score*.
Данные метрики имеют общеизвестные ограничения из-за их зависимости от порога принятия решения, который трудно определить на практике и который сильно зависит от ограничений, характерных для бизнеса.


*AUC ROC* одна из беспороговых метрик, которые нацелены на оценку с помощью одного числа производительности для всех возможных порогов принятия решений.
Однако недавние исследования показали, что эта метрика также вводит в заблуждение при оценке сильно несбалансированных проблем, таких как обнаружение мошеннических транзакций [John Muschelli, ROC and AUC with a Binary Predictor: a Potentially Misleading Metric, 2019](https://arxiv.org/abs/1903.04881), и вместо этого рекомендуется использовать: 

- **Precision-Recall AUC** (PR AUC)

Основное преимущество метрики AUC PR-кривой состоит в том, чтобы отобразить как высокую полноту, так и высокую точность, что косвенно приводит к высокому уровню истинно положительных результатов (TPR) и низкому показателю ложноположительных результатов (FPR).
[Boyd, Kendrick, Kevin H. Eng, and C. David Page, Area under the Precision-Recall Curve: Point Estimates and Confidence Intervals, 2013](https://link.springer.com/chapter/10.1007/978-3-642-40994-3_29)

- **Precision Top-k**

Каждый день $d$ отдел расследований в ручную может проверить $k$  транзакций. Система выделяет множество $ A_d $  подозрительных транзакций в день $d$. $ | A_d | <= k $, часть их которых ложноположительные, а другая часть $ A^{fraud}_{d}$ мошеннические.
Пусть k много меньше, чем все транзакции за день d и $ | A_d | <=  k $, тогда  *precision top-k* для дня d 
$$ P@k(d) = \frac{|A^{fraud}_{d}|}{|A_{d}|} = \frac{|A^{fraud}_{d}|}{k}$$


- **Card Precision Top-k**

На одну карту может прийтись несколько подозрительных транзакций выделяемых системой. Если система будет вместо транзакций указывать на подозрительные карты, то *precision top-k* метрика, называется *card precision top-k* метрикой и обозначается $ CP@k(d)$. 

Так как нет возможности моделировать работу экспертов, то в рамках работы над проектом как основную метрику качества модели будем использовать *PR AUC*.

## Декомпозицию проекта
Проект состоит из набора взаимосвязанных частей:
 - облачные вычислительные ресурсы (с возможность масштабировать решение),
 - данные (сбор, хранение, преобразование, генерация),
 - модель (выбор модели и метрик ее эффективности, оптимизация гиперпараметров, пайплайн переобучения модели),
 - CI/CD (выбор инструментов, реализация пайплайнов с данными и моделью),
 - мониторинг (сдвигов в данных, работоспособности модели на вычислительных ресурсах при изменении потока пользователей).


## План работ
Текущие задачи и план работ представлен на [GitHub](https://github.com/bondaleksey/credit-card-fraud-detection/issues).


## Файлы для анализа находятся в s3:
файлы были скопированы с помощью скрипта `scripts/s3/boto_copy_fraud_data.py`
Например, один из файлов имеет адрес:
https://storage.yandexcloud.net/bond-ccfd/fraud-data/2019-08-22.txt