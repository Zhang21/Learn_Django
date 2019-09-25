from django.shortcuts import render, get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.template import loader

from .models import Question, Choice


"""删除旧的视图
# def index(request):
#    return HttpResponse("Hello, world. You're at the polls index.")

def index(request):
    latest_question_list = Question.objects.order_by('-pub_data')[:5]
    # output = ', '.join([q.question_text for q in latest_question_list])

    # 载入polls/index.html模板文件，并且向它传递一个上下文(context)，这个上下文是一个字典
    # template = loader.get_template('polls/index.html')
    # context = {'latest_question_list': latest_question_list,}

    # 不需导入loader和HttpResponse
    # 不过其它函数(detaild, vote...)需要用到的话，就绪导入HttpResponse
    context = {'latest_question_list': latest_question_list}
    # return HttpResponse(output)
    # return HttpResponse(template.render(context, request))
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    # return HttpResponse("You're looking at the results of question %s." % question_id)

    # 404异常
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    # response = "You're looking at the results of question %s."
    # return HttpResponse(response % question_id)
    # 当有人对 Question 进行投票后， vote() 视图将请求重定向到 Question 的结果界面
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
"""

"""
request.POST是一个类字典对象，让你通过关键字的名字获取提交的数据。
此例中，request.POST['choice']以字符串形式返回选择的Choice的ID。request.POST的值永远是字符串。

request.POST['choice']数据中没有提供choice将引发一个KeyError。

增加Choice的得票数之后，代码返回一个HttpResponseRedirect，它只接收一个参数：用户将要被重定向的URL。

此例中，HTTPResponseRedirect的构造函数中使用reverse()函数。这个函数避免了我们在视图函数中硬编码URL。
它需要我们给出我们想要跳转的视图的名字和该视图所对应的的URL模式中需要给该视图提供的参数。
在设定的URLconf中，reverse()调用将返回: /polls/3/results/
3是question.id的值，重定向的URL将调用results视图来显示最终的页面。
"""

"""
def vote(request, question_id):
    # return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button
        return HttpResponseRedirect(reversed('polls:results', args=(question.id,)))
"""


# 改良视图
class IndexView(generic.ListView):
    # 此属性告诉Django使用一个指定的模板名字，而不是自动生成的默认名字。
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


# 也为results列表视图指定了模板名，这确保results视图和detail视图在渲染时具有不同的外观，
#  即使它们在后台都是同一个DetailView
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    ...  # same as above, no changes needed.
