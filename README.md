#learnDjango

reference:

- django docs: <https://docs.djangoproject.com/zh-hans>


<br/>
<br/>


## 目录

- [初识Django](#初识Django)
- [快速安装指南](#快速安装指南)
- [编写第一个Django应用-1](#Django1)


<br/>
<br/>


## 初识Django

Django用于开发Web应用。

- **设计模型**: 无需数据库就可以使用，它提供了对象关系映射器通过此技术，你可以使用Python代码来描述数据库结构。
- **应用数据模型**: 运行Django命令行工具来创建数据库表。
- **便捷的API**: 使用一套丰富的Python API来访问你的数据库。
- **动态管理结构**: 当模型完成定义时，Django就会自动生成一个专业的生产级管理接口——一个允许认证用户添加、更改和删除对象的Web站点。
- **规划URLs**: 简介优雅的URL规划对于一个高质量的Web应用来说至关重要。Django推崇优美的URL设计。
- **编写视图**: 视图函数的执行结果只可能有两种：返回一个包含请求页面元素的HttpResponse对象，或抛出Http404这类异常。
- **设计模板**: Django允许设置搜索模板路径，这样可以最小化模板之间的冗余。
- **缓存框架**
- **聚合器框架**: 编写一个类来推送RSS和Atom


<br/>
<br/>


## 快速安装指南

- 安装Python: Python包含了一个名为SQLite的轻量级数据库，所以你暂时不必自行设置一个数据库。
- 设置数据库: 如PostgreSQL, MySQL, Oracle...
- 安装Django
- 验证


<br/>
<br/>


## Django1

创建一个基本的投票应用程序:

- 让人们查看你和投票的公共站点
- 一个让你能添加、修改和删除投票的管理站点

```shell
$ python3 -m django --version
```


<br/>
<br/>


### 创建项目

如果是第一次使用Django的话，你需要一些初始化设置。

```shell
cd writingDjango
django-admin startproject mysite
```

> 避免使用Python和Django的内部保留字来命名你的项目。
> 如果你曾经是PHP程序员，你可能会习惯吧代码放在诸如`/var/www`目录。当使用Django时不需要这样做。把所有Python代码放在Web服务器的根目录不是个好主意，因为这样会有风险，不利于网站的安全。

<br>

`startproject`创建了什么:

```
mysite/                 // 跟目录
├── manage.py           // 一个让你用各种方式管理Django项目的命令行工具
└── mysite              // 包含你的项目，它是一个纯Python包
    ├── __init__.py
    ├── settings.py     // Django项目的配置文件
    ├── urls.py         // Django项目的URL声明，就像网站的目录
    └── wsgi.py         // 运行在WSGI兼容的Web服务器上的入口
```


<br/>
<br/>


### 用于开发的建议服务器

```shell
python3 manage.py runserver
# python3 manage.py runserver 8000

# 它会自动重载修改的文件，所以不需要重启服务
```


<br/>
<br/>


### 创建投票应用

在Django中，每一个应用都是一个Python包，并且遵循着相同的约定。Django自带了一个工具，可以帮你生成应用的基础目录结构。

项目和应用：项目可以包含很多个应用，应用可以被很多项目使用。

```shell
# manage.py同级目录下
python3 manage.py startapp polls

# 它会创建一个polls目录
polls/
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py

# 这个目录结构包括了投票应用的全部内容
```


<br/>
<br/>


### 编写第一个视图

```
# 修改 polls/views.py
# 这是Django中最简单的视图。如果想看见效果，需要将一个URL映射到它。

# 新建urls.py文件，编写代码

# 在根URLconf文件中指定我们创建的polls.urls模块。在mysite/urls.py的urlpatterns列表里插入一个include
# 当包括其它URL模式时你应该总是使用include(), admin.site.urls是唯一例外

# 访问 http://localhost:8000/polls/

# 了解path()的四个参数: route, view, kwargs, name
```


<br/>
<br/>


## Django2

建立数据库，创建你的第一个模型，并主要关注Django提供的自动生成的管理页面。


<br/>
<br/>


### 数据库配置

`mysite/settings.py`，它包含了Django项目设置的Python模块。默认数据库为SQLite。如果想使用其他数据库，需要安装`database bindings`，并提前创建好数据库。然后改变设置文件中的`DATABASES default`项目中的一些键值：

- ENGINE
  - `django.db.backends.sqlite3`
  - `django.db.backends.postgresql`
  - `django.db.backends.mysql`
  - `django.db.backends.oracle`
- NAME: 数据库名称，NAME应该是文件此文件的绝对路径

```
# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
```

修改时区`TIME_ZONE`为自己的时区。

`INSTALLED_APPS`包括了在你项目中启用的所有Django应用。默认开启的某些应用需要至少一个数据表，所以，在使用他们之前需要在数据库中创建一些表。

```shell
python3 manage.py migrate
# migrate检查INSTALLED_APPS设置，为其中的每个应用创建需要的数据表，至于会创建什么，这取决于你的mysite/settings.py设置文件和每个应用的数据库迁移文件。
# 如果你不需要某个或某些应用，你可以删除它们。
```


<br/>
<br/>


### 创建模型

在Django里写一个数据库驱动的Web应用的第一步是定义模型，也就是数据库结构设计和附加的其他元数据。

在这个简单投票应用中，需要创建两个模型：问题Question(模型包括问题描述和发布时间)和选项Choice(模型有两个字段，选项描述和当前得票数)。每个选项属于一个问题。

编辑`polls/models.py`文件。


<br/>
<br/>


### 激活模型

首先得把polls应用安装到项目里。

修改`mysite/settings.py`文件，在`INSTALLED_APPS`中添加。

现在你的Django项目会包含polls应用。运行命令: `python3 manage.py makemigrations polls`。通过运行`mekemigrations`命令，Django会检测你对模型的修改，并把修改的部分存储为一次迁移。
迁移是Django对于模型定义(数据库结构)的变化的存储形式，它其实是一些磁盘上的文件。

Django有一个自动执行数据库迁移并同步管理你的数据库结构的命令——`migrate`。但让我们先看看迁移命令会执行那些SQL语句，`sqlmigrate`命令接收一个迁移的名称，然后返回对应的SQL。

```
python3 manage.py sqlmigrate polls 0001

# 然后你会看到类似下面的输出
BEGIN;
--
-- Create model Choice
--
CREATE TABLE "polls_choice" (
    "id" serial NOT NULL PRIMARY KEY,
    "choice_text" varchar(200) NOT NULL,
    "votes" integer NOT NULL
);
--
-- Create model Question
--
CREATE TABLE "polls_question" (
    "id" serial NOT NULL PRIMARY KEY,
    "question_text" varchar(200) NOT NULL,
    "pub_date" timestamp with time zone NOT NULL
);
--
-- Add field question to choice
--
ALTER TABLE "polls_choice" ADD COLUMN "question_id" integer NOT NULL;
ALTER TABLE "polls_choice" ALTER COLUMN "question_id" DROP DEFAULT;
CREATE INDEX "polls_choice_7aa0f6ee" ON "polls_choice" ("question_id");
ALTER TABLE "polls_choice"
  ADD CONSTRAINT "polls_choice_question_id_246c99a640fbbd72_fk_polls_question_id"
    FOREIGN KEY ("question_id")
    REFERENCES "polls_question" ("id")
    DEFERRABLE INITIALLY DEFERRED;

COMMIT;


# 输出的内容和使用的数据库有关，上面是PostgreSQL
# 主键(IDs)会被自动创建（可自定义）
# 默认的，Django会在外键字段名后追加字符串'_id'（可自定义）
# 这个sqlmigrate命令并没有真正在你的数据库中执行迁移，它只是把命令输出到屏幕上，让你看看Django认为需要执行哪些SQL语句。
# 如果你感兴趣，可试试运行python manage.py check这个命令帮助你检查项目中的问题，并在检查过程中不会对数据库进行任何操作
```

现在，再次运行`migrate`命令，在数据库里创建新定义的模型的数据表:

```sh
python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Rendering model states... DONE
  Applying polls.0001_initial... OK

# 这个migrate命令选中所有还没有执行过的迁移（Django 通过在数据库中创建一个特殊的表 django_migrations 来跟踪执行过哪些迁移）并应用在数据库上 - 也就是将你对模型的更改同步到数据库结构上。
# 迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。
```

现在，你只需记住，改变模型需要这三步：

- 编辑`models.py`文件，改变模型
- 运行`python manage.py makemigrations`为模型的改变生成迁移文件
- 运行`python manage.py migrate` 来应用数据库迁移

数据库迁移被分解成生成和应用两个命令是为了让你能够在改吗控制系统上提交迁移数据并使其能在多个应用里使用。这让开发简单和方便。


<br/>
<br/>


### 初试API

让我们进入交互式Python命令行，尝试一下Django为你创建的各种API。

```shell
python3 manage.py shell

# 这个命令而不是简单的使用 "Python" 是因为 manage.py 会设置 DJANGO_SETTINGS_MODULE 环境变量，
# 这个变量会让 Django 根据 mysite/settings.py 文件来设置 Python 包的导入路径。
>>> from polls.models import Choice, Question  # Import the model classes we just wrote.

# No questions are in the system yet.
>>> Question.objects.all()
<QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> q.save()

# Now it has an ID.
>>> q.id
1

# Access model field values via Python attributes.
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)

# Change values by changing the attributes, then calling save().
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() displays all the questions in the database.
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>


# 这时候可查看数据库
mysql> SELECT * FROM polls_question WHERE id=1;
+----+---------------+----------------------------+
| id | question_text | pub_data                   |
+----+---------------+----------------------------+
|  1 | What's new?   | 2019-09-04 09:59:34.757694 |
+----+---------------+----------------------------+
1 row in set (0.00 sec)
```

通过编辑Question模型的代码(`polls/models.py`)，给Question和Choice增加`__str__()`方法:

修改文件并保存后，再次通过命令调用交互模式。


<br/>
<br/>


### 介绍Django管理页面

管理页面不是为了网站的访问者，而是为管理者准备的。


<br/>


- 创建一个管理员账号

```
python3 manage.py createsuperuser
# 输入用户名和邮箱和密码
```

<br/>


- 启动开发服务器

Django的管理界面默认是启用的。让我们启动开发服务器: `python3 manage.py runserver`，访问`localhost:8000/admin/`

<br>

- 进入管理站点页面

这个页面提供的组和用户，是由`django.contrib.auth`提供，这是Django开发的认证框架。

<br>

- 向管理页面中加入投票应用

我们需要告诉管理页面，问题Question对象需要被管理。修改`polls/admin.py`。之后会出现`POLLS`这个栏目。

<br>

- 体验管理功能

在这里可以修改我们在polls下已创建的对象和内容。



<br/>
<br/>



## Django3

创建公用界面——也被称为**视图**。


<br/>


### 编写更多视图

向`polls/views.py`添加更多视图。有些视图不同，它们接收参数。
之后把这些视图添加到`polls.urls`模块里。

为每个URL加上不必要的东西，如`.html`，是没有必要的。不过你也可以加: `path('polls/latest.html', views.index)`
但是，别这样做，太傻了。


<br/>


### 写一个真正有用的视图

每个视图必须要做的只有两件事: 返回一个包含被请求页面内容的**HttpResponse**对象，或者抛出一个异常（比如http404）。至于你还想干什么，随便你。

你的视图可以从数据库里读取记录，可以使用引擎模板，可以生成一个PDF文件，可以输出一个XML，创建一个ZIP，可以做任何你想做的事，使用你想用的任何Python库。

Django只要求返回的是一个`HttpResponse`或者抛出一个异常。
Django自带的数据库API很方便，这里我们在视图里使用它。编辑`polls/views.py`。

这里有个问题：页面的设计写死在视图函数的代码里的。如果你想改变页面的样子，你需要编辑Python代码。所以让我们使用Django的模板系统，只要创建一个视图，就可以将页面的设计从代码中分离出来。

首先，在你的polls目录里创建一个templates目录。Django将会在这个目录里查找模板文件。
你项目的TEMPLATES配置项描述了Django如何载入和渲染模板。默认的设置文件设置了DjangoTemplates后端，并将`APP_DIRS`设置成了`True`。这一选项将会让DjangoTemplates在每个INSTALLED_APPS文件夹中寻找 "templates" 子目录。

在你刚刚创建的templates目录里，再创建一个目录polls，然后在其中新建一个文件`index.html`。换句话说，你的模板文件的路径应该是`polls/templates/polls/index.html`。

虽然我们现在可以将模板文件直接放在`polls/templates`文件夹中（而不是再建立一个 polls 子文件夹），但是这样做不太好。Django 将会选择第一个匹配的模板文件，如果你有一个模板文件正好和另一个应用中的某个模板文件重名，Django 没有办法 区分 它们。我们需要帮助 Django 选择正确的模板，最简单的方法就是把他们放入各自的 命名空间 中，也就是把这些模板放入一个和 自身 应用重名的子文件夹里。

向`index.html`文件添加新内容。

然后让我们更新`polls/views.py`的index视图来使用模板。
使用浏览器访问`/polls/`页面，你将会看到一个无序列表。

<br>

**一个快捷函数: render()**

载入模板，填充上下文，再返回由它生成的HttpResponse对象，是一个非常常用的操作流程。Django提供了一个快捷函数，我们用它来重写`index()`视图。编辑`polls/views.py`。


<br/>
<br/>


### 抛出404错误

现在来处理投票详情视图——它会显示指定投票的问题标题。编辑`polls/views.py`文件。
如果指定问题id所对应的问题不存在，这个视图就会抛出一个Http404异常。

<br>

**一个快捷函数: `get_object_or_404`**

尝试用`get()`获取一个对象，如果不存在就抛出`Http404`错误，也是一个普遍的流程。Django同样也提供了一个快捷函数。下面修改`detail()`视图代码。


<br/>
<br/>


### 使用模板系统

回过头去看`detail()`视图，它向模板传递了上下文变量`question`。下面是`polls/detail.html`模板里正式的代码。


<br/>
<br/>


### 去处模板中的硬编码URL

我们在`polls/index.html`里编写投票链接时，链接是硬编码的: `<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>`

问题在于，硬编码和强耦合的链接，对于一个包含很多应用的项目来说，修改起来是十分困难的。然而，因为你在 polls.urls 的 url() 函数中通过name参数为URL定义了名字，你可以使用`{% url %}`标签代替它: `<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>`。

如果你想改变投票详情视图的URL，你不用在模板里需改任何东西，只需要在`polls/urls.py`里稍微修改一下就行。


<br/>
<br/>


### 为URL名称添加命名空间

教程项目只有一个应用，但在真实的项目中，可能会有很多应用。Django如何分辨重名的URL呢？举个例子，polls应用有detail视图，可能其它应用也有同名的视图。Django如何知道`{% url %}`标签到底对应哪一个应用的URL呢？
答案是在跟URL conf中添加命名空间。在`polls/urls.py`文件稍作修改，加上`app_name`设置命名空间。

接着，编辑`polls/index.html`文件。修改为指向具有命名空间的详细视图。



<br/>
<br/>



## Django4
