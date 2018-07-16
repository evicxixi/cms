from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
from cms.form import UserForm
import json
from django.urls import reverse
from django.contrib.auth.models import User
from cms.models import UserInfo, Blog, Article, Comment, Category, Tag, Article2Tag, ArticleUpDown
from django.db.models import Avg, Max, Min, Count
from django.http import JsonResponse
# Create your views here.


def dashboard(request, **kwargs):
    print('dashboard')
    if kwargs:
        article_id = kwargs['article']
        print('id', id)
        if request.method == 'GET':  # 初次请求 /article/id/
            print('get')
            article_obj = Article.objects.filter(id=article_id).first()
            user_obj = UserInfo.objects.filter(id=request.user.id).first()
            cates = Category.objects.all()
            tags = Tag.objects.all()
            tag_list = Article2Tag.objects.filter(
                article_id=article_obj.id).values('tag')
            tag_list = [i['tag'] for i in tag_list]
            # if tag:
            #     tag = Tag.objects.filter(id=tag.tag_id).first()

            print('tag_list', tag_list)
            print('cates', cates)
            print('article_obj.tag', article_obj.tag.name)
            return render(request, 'article_edit.html', locals())
        elif request.method == 'POST':
            print('post1')
            if request.is_ajax():
                data = json.loads(request.body.decode('utf-8'))
                # print('data', data)
                article_obj = Article.objects.filter(id=article_id)
                # .update(
                # title=data['title'], content=data['content'],
                # cate=data['cate'],)
                article2tag_obj_list = Article2Tag.objects.filter(
                    article_id=article_id).all().delete()
                print(111)
                print("data['tag_id_list']", data['tag_id_list'])
                for x in data['tag_id_list']:
                    print(x)
                    article2tag_obj_list = Article2Tag.objects.add(
                        article_id=article_id, tag_id=x)
                # print('article_obj', article_obj)
                return HttpResponse(json.dumps(data))

    else:
        if request.method == 'GET':  # 初次请求 /dashboard/
            blog_obj = Blog.objects.filter(
                userinfo__id=request.user.id).first()
            user_obj = UserInfo.objects.filter(id=request.user.id).first()
            articles = Article.objects.filter(user_id=request.user.id)
            print('articles', articles)
            cates = Category.objects.filter(blog=blog_obj).annotate(
                count=Count('article__title')).values('name', 'count')
            tags = Tag.objects.filter(blog=blog_obj).annotate(
                count=Count('article2tag')).values('name', 'count')
            return render(request, 'dashboard.html', locals())


def article_up_down(request):
    if request.method == 'POST':
        if request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            obj = ArticleUpDown.objects.filter(
                article_id=data['article_id'], user_id=request.user.id)  # 查询是否有up_down记录
            new_data = {}
            if obj:  # 如果已点击过up_down 再判断是up还是down
                if obj[0].is_up:
                    new_data['state'] = 1,
                else:
                    new_data['state'] = -1,
            else:  # 如果从未点击过up_down 就创建一条up_down
                new_data['state'] = 0,
                obj = ArticleUpDown.objects.create(
                    article_id=data['article_id'], user_id=request.user.id, is_up=data['is_up'])

            return HttpResponse(json.dumps(new_data))


def comment(request):
    if request.method == 'POST':
        if request.is_ajax():
            data = json.loads(request.body.decode('utf-8'))
            # print('request.body', data, type(data))
            comment_obj = Comment.objects.create(
                content=data['content'], article_id=data['article_id'], pid_id=data['pid_id'], user_id=request.user.id)
            data = {
                'comment_id': comment_obj.id,
                'article_id': comment_obj.article_id,
                'pid_id': comment_obj.pid_id,
                'content': comment_obj.content,
                'user': request.user.first_name,
                'date': str(comment_obj.data),
            }
            print('data', data)
            return HttpResponse(json.dumps(data))


def article(request, id):
    article_obj = Article.objects.filter(id=id).first()
    # user_obj = UserInfo.objects.filter()
    blog_obj = Blog.objects.filter(article=id).first()
    # print('blog_obj', blog_obj)
    user_obj = UserInfo.objects.filter(id=request.user.id).first()
    # print('user_obj', user_obj)
    cates = Category.objects.filter(blog=blog_obj).annotate(
        count=Count('article__title')).values('name', 'count')
    tags = Tag.objects.filter(blog=blog_obj).annotate(
        count=Count('article2tag')).values('name', 'count')
    tag_list = Article2Tag.objects.filter(article_id=id)
    comments = Comment.objects.filter(article_id=article_obj.id)
    # print('comments', comments)
    coments_count = comments.annotate(count=Count('comment')).values('count')

    # 构建包含评论详情list的list
    def to_list(obj):
        return [
            obj.id,
            obj.article_id,
            obj.pid_id,
            obj.content,
            request.user.first_name,
            str(obj.data),
        ]
    comment_list = [x for x in map(lambda x: to_list(x), comments)]

    updown_obj = ArticleUpDown.objects.filter(
        article_id=article_obj.id, user_id=request.user.id).first()

    # 判断是否已经点过赞
    updown_state = 0
    if updown_obj:
        updown_state = 1

    return render(request, 'article.html', locals())


def cms(request, **kwargs):
    print('cms')
    if len(kwargs) == 0:
        articles = Article.objects.all()
        swiper_img = [
            'https://i1.mifile.cn/a4/xmad_15296632592516_QsRyp.jpg',
            'https://i1.mifile.cn/a4/xmad_15294024705461_BDFOx.jpg',
            'https://i1.mifile.cn/a4/xmad_15204795762271_ZwaxE.jpg',
            'https://i1.mifile.cn/a4/xmad_15204799796935_WjnpM.jpg',
            'https://i1.mifile.cn/a4/xmad_15204798088946_YvzWs.jpg',
        ]
        return render(request, 'cms.html', locals())

    elif len(kwargs) == 1:
        user_obj = UserInfo.objects.filter(username=kwargs['username']).first()
        blog_obj = user_obj.blog
        articles = Article.objects.filter(user=user_obj.id)
        cates = Category.objects.filter(blog=blog_obj).annotate(
            count=Count('article__title')).values('name', 'count')
        tags = Tag.objects.filter(blog=blog_obj).annotate(
            count=Count('article2tag')).values('name', 'count')
        return render(request, 'author.html', locals())
    else:
        user_obj = UserInfo.objects.filter(username=kwargs['username']).first()
        if kwargs['key'] == 'cate':
            blog_obj = Blog.objects.filter(
                category__id=kwargs['value']).first()
            cates = Category.objects.filter(id=kwargs['value'])
            print('cates', cates.values('blog'))
            # blog_obj = cates.values('blog').values('article')
            articles = Article.objects.filter(
                category=kwargs['value']).filter(user__username=kwargs['username'])
            print('articles', articles)
            return render(request, 'cms.html', locals())


def login(request):
    if request.method == 'POST':
        if request.is_ajax():
            print('is_ajax')
            data = json.loads(request.body.decode('utf-8'))
            print(data, type(data))
            if data['type'] == 'login':
                user = auth.authenticate(
                    username=data['username'],
                    password=data['password'],
                )
                if user:
                    # print('user.is_authenticated()', user.is_authenticated())
                    auth.login(request, user)
                    # print('user.is_authenticated()', user.is_authenticated())
                    # print('request.user', request.user)
                    url = reverse(cms) + user.username
                    print('url', url)
                    data = json.dumps({
                        'state': True,
                        'url': url,
                    })
                    return HttpResponse(data)
                else:
                    print('else user')
                    data = json.dumps({
                        'state': False,
                        'url': reverse(cms),
                    })
                    return HttpResponse(data)
            elif data['type'] == 'signin':
                user_obj = UserInfo.objects.create_user(
                    username=data['username'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                )
                data = json.dumps({
                    'state': True,
                    'url': reverse(login),
                })
                return HttpResponse(data)

    form_obj = UserForm()
    data = {
        'form_obj': form_obj,
        'login_fields': ['username', 'password'],
    }
    return render(request, 'auth.html', locals())


def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


def index(request):
    return render(request, 'index.html')
