# Django模板语言

参考:

- <https://docs.djangoproject.com/zh-hans/2.1/topics/templates/>
- <https://docs.djangoproject.com/zh-hans/2.1/ref/templates/language/>


<br/>

---

<br/>


Django模板引擎提供了一种强大的mini-language，用于定义应用程序的面向用户层，鼓励应用程序和表示逻辑的清晰分离。任何了解HTML的人都可以维护模板，不需要Python的知识。

Django模板语言其实和Jinja2类似，只不过Jinja2更自由些。



<br/>
<br/>
<br/>



## Django模板语言

本文档解释了Django模板系统的语言语法。
Django的模板语言只在功能和易用性之间取得平衡。它旨在让那些习惯使用HTML的人感到舒服。如果你对其它模板语言(Smart, Jinja2)有任何接触，那么您应该对Django的模板感到宾至如归。

> 哲学
> Django模板系统不仅仅是嵌入到HTML中的Python。模板系统用于表示，而不是程序逻辑。
> Django模板系统提供的tags功能与某些编程结构类似——`if`标签用于布尔测试，`for`标签用于循环...但这些并不是简单地作为相应的Python代码执行，并且模板系统不会执行任意Python表达式。


<br/>
<br/>


### 模板

Templates

一个模板是一个简单的文本文件。它可以生成任何基于文本的格式(HTML, XML, CSV...)。

模板包含变量(variables)，这些变量在评估模板时将替换为值，而变量则包含控制模板逻辑的标签(tags)。

下面是一个最小的模板示例，每个元素将在后面解释。

```jinja2
{% extends "base_generic.html" %}

{% block title %}{{ section.title }}{% endblock %}

{% block content %}
<h1>{{ section.title }}</h1>

{% for story in story_list %}
<h2>
  <a href="{{ story.get_absolute_url }}">
      {{ story.headline|upper }}
  </a>
</h2>
<p>{{ story.tease|truncatewords:"100" }}</p>
{% endfor %}
{% endblock %}
```

> 为什么使用基于文本而不是基于XML的模板？我们希望Django的模板语言不仅可用于XML/HTML模板。在互联网上，我们将其用于电子邮件、JS和CSV。你可将模板语言用于任何基于文本的格式。
> 让人类编辑XML是虐待狂!


<br/>
<br/>


### 变量

Variables

变量像这样: `{{ variable }}`。当模板引擎遇到变量时，它会计算该变量并将其替换为结果。变量名由字母、数字和下划线组成，但不能以下划线开头。点(`.`)也出现在变量部分，尽管它具有特殊含义。重要的是，变量名称中不能包含空格或标点符号。

从技术上来说，当模板系统遇到一个点时，它会按照一下顺序尝试查找:

- 字典
- 属性或方法
- 数字索引

在上面的例子中，`{{ section.title }}`将替换为section对象的title属性。
如果使用不存在的 变量，模板系统将插入`srting_if_invalid`选项的值，默认情况下设置为空`''`。

请注意，模板表达式`{{ foo.bar }}`中的bar将被解释为文字字符串，而不使用变量bar的值(如果上下文中存在)。

可能无法访问以下划线开头的变量属性，因为它们通常被视为私有。


<br/>
<br/>


### 过滤

Filters

你可使用过滤器(filters)修改要显示的变量。
过滤器像这样: `{{ name|lower }}`。这会在通过小写过滤器后显示变量的值，后者将文本转换为小写。使用管道(`|`)应用过滤器。

过滤器可以链接，一个过滤器的输出应用于下一个过滤器。`{{ text|escape|linebreaks }}`。`{{ text|escape|linebreaks }}`是转义文本内容，然后将换行符转换为`<p>`标签的常用习惯写法。

一些过滤会使用参数，过滤器参数如下所示: `{{ bio|truncatewords:30 }}`，这将显示变量bio的前30个单词。
过滤参数包含的空格必须使用引号引用，如: `{{ list|join:", " }}`。

Django提供了大约60个内置模板过滤器。可在[built-in filter reference](https://docs.djangoproject.com/zh-hans/2.1/ref/templates/builtins/#ref-templates-builtins-filters)查看全部。

以下是一些常用的模板过滤器:

- default
如果变量为false或者为空，使用给定的默认值。

```jinja2
{{ value|default:"nothing" }}
```

- length
返回值得长度，使用与strings和lists。

```jinja2
{{ value|length }}
```

- filesizeformat
将值格式化为人类可读的文件大小(`12KB`, `2MB`...)

```jinja2
{{ value|filesizeformat }}
```

当然，你可以创建自己的自定义模板过滤器。


<br/>
<br/>



### 标记

Tags

标记像这样: `{% tag %}`。标签比变量更复杂：有些在输出中创建文本，有些通过执行循环或逻辑来控制流，有些则将外部信息加载到模板中以供以后的变量使用。

有些标签需要开始和结束标记: `{% tag %}`...`{% endtag %}`。

Django附带了大约24个内置模板标签。可查看[build-in tag reference](https://docs.djangoproject.com/zh-hans/2.1/ref/templates/builtins/#ref-templates-builtins-tags)。

下面是一些常用的标记:

- for
循环遍历数组中的每个项。

```jinja2
<ul>
{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% end for %}
</ul>
```

- if, elif, else

```jinja2
{% if athlete_list %}
    Number of athletes: {{ athlete_list|length }}
{% elif athlete_in_locker_room_list %}
    Athletes should be out of the locker room soon!
{% else %}
    No athletes.
{% enfif %}
```

可在if标记中使用过滤器和操作符:

```jinja2
{% if athlete_list|length > 1 %}
    Team: {% for athlete in athlete_list %} ... {% endfor %}
{% else %}
    Athlete: {{ athlete_list.0.name }}
{% endif %}
```

- block, extends
设置模板继承[template inheritance](https://docs.djangoproject.com/zh-hans/2.1/ref/templates/language/#id1)，这是一种在模板中减少样板(boilerplate)的强大方法。

你可以创建自己的自定义模板标记。


<br/>
<br/>


### 注释

Comments

注释的语法为: `{# #}`。

例如，此模板将呈现为hello: `{# greeting #}hello`。


<br/>
<br/>


### 模板继承

Templates inheritance

Django模板引擎最强大，也是最复杂的就是模板继承。模板继承允许你构建一个基础骨架模型，其中包含站点的所有常用元素(elements)，并定义子模块可以覆盖的块(block)。

理解模板继承的栗子(`base.html`):

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>{% block title %}My amazing site{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block sidebar %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

定义了一个简单的HTML框架文档，你可将其用于简单的双列页面。子模板的工作是用内容填充空块(empty block)。
在此示例中，块标记(block)定义了子模块可以填充的三个块。所有块标记的作用是告诉模板引擎子模块可以覆盖模板的这些部分。

子模板栗子:

```jinja2
{% extends "base.html" %}

{% block title %}My amazing blog{% endblock %}

{% block content %}
{% for entry in blog_entries %}
    <h2>{{ entry.title }}</h2>
    <p>{{ entry.body }}</p>
{% endfor %}
{% endblock %}
```

扩展标记(extends)是这里的关键。它告诉模板引擎改模板扩展另一个模板。当模板系统评估此模板时，它首先找到父模板。

此时，模板引擎会注意到`base.html`中的三个块标记，并将这些块替换为子模板的内容。输出可能如下:

```jinja2
<!DOCTYPE html>
<html lange="en">
<head>
    <link rel="stylesheet" href="style.css">
    <title>My amazing blog</title>
</head>

<body>
    <div id="sidebar">
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/blog/">Blog</a></li>
        </ul>
    </div>

    <div id="content">
        <h2>Entry one</h2>
        <p>This is my first entry.</p>

        <h2>Entry two</h2>
        <p>This is my second entry.</p>
    </div>
</body>
</html>
```

请注意，由于子模块未定义sidebar块，因此将使用父模板中的值。

<br>

你可以根据需要使用尽可能多的继承级别。使用继承的一种常见方法是以下三级(three-level)方法:

- 创建`base.html`基础模板，其中包含网站的主要外观
- 为网站的每个部分(section)创建一个`base_SECTIONNAME.html`模板，这些模板都扩展基础模板，并包含特定于部分的样式设计
- 为每种类型的页面创建单独的模板，这些模板扩展了相应部分的模板

这种方法可以最大化代码重用，并且可以轻松地将项目添加到共享内容区域。

<br>

以下是使用继承的一些技巧与提示:

- 如果在模板中使用`{% extends %}`，则它必须是该模板中的第一个模板标记。否则，模板继承不起作用。
- 基础模板中的`{% block %}`标记越多越好。请记住，子模块不必定义所有父块，因此你可在多个块中填写合理的默认值，然后仅定义需要的块。
- 如果在许多模板中复制了内容，则可能意味着你应该将内容移动到父模板中的`{% block %}`。
- 如果需要从父模板获取块的内容，`{{ block.super }}`变量将起作用。如果要添加到父模块的内容而不是完全覆盖它，这将非常有用。
- 使用模板标记`as`语法在`{% block %}`块之外创建的变量不能在块内使用。
```jinja2
{% trans "Title" as title %}
{% block conten %}{{ title }}{% endblock %}
```
- 为了提高可读性，可选择为`{% endblock %}`标记指定名称。在较大的模板中，此技术可帮助查看正在关闭的块标记。
```jinja2
{% block content %}
...
{% endblock conten %}
```

最后，请注意，你无法在同一模板中定义多个名称相同的块标记。


<br/>
<br/>


### 自动HTML转义

Automatic HTML escaping

当从模板生成HTML时，变量将始终存在影响生成的HTML的字符的风险。

考虑这个模板片段: `Hello {{ name }}`
首先，这似乎是一种显示用户名的无害方式。但考虑如果用户输入其名称会发生什么: `<script>alert('hello')</script>`
使用此名称值，模板将呈现为: `Hello, <script>alert('hello')</script>`
这意味着浏览器会弹出一个JS警告框！

类似地，如果名称包含`<`符号: `<b>username`
这将导致像这样的渲染模板: `Hello, <b>username`
反过来，这将导致网页的其余部分被加粗。

显然，用户提交的数据不应盲目信任并直接插入到你的网页中，因为恶意用户可能会利用这种漏洞来做坏事。此类安全漏洞称为跨站点脚本(XSS, cross site scripting)攻击。

要避免此问题，有两种选择:

- 一，可以确保通过转义过滤器运行每个不受信任的变量，该过滤器可将可能有害的HTML字符转换为无害的HTML字符。这是Django最初几年的默认解决方案，但问题在于它让你有责任确保你逃避一切。
- 二，可利用Django的自动HTML转义功能。

默认情况下，Django中的每个模板都会自动转义每个变量标记的输出。具体来说，这五个字符被转义:

- `<`被转换为`&lt`;
- `>`被转换为`&gt`;
- `'`被转换为`&#39`;
- `"`被转换为`&quot`;
- `&`被转换为`&amp`;

同样，我们强调默认情况下已启用此行为。如果你正在使用Django的模板系统，那么你将受到保护。


<br/>
<br/>


#### 如何关闭

如果不想自动转义数据，则可通过多种方式将其关闭。

- 单独的变量(individual bariables)
使用`safe`过滤器。

```jinja2
This will be escaped: {{ data }}
This will not be escaped: {{ data|safe }}
```

- 模板块(template block)
将模板包装在`autoescape`标记中。它将on或off作为其参数。

```jinja2
{% autoescape off %}
    Hello {{ name }}
{% endautoescape %}
```


<br/>
<br/>


#### 字符串文字和自动转义

String literals and automatic escaping

如前面所说，过滤参数可以是字符串: `{{ data|default:"This is a string literal." }}`



<br/>
<br/>



### 访问方法调用

Accessing method calls
