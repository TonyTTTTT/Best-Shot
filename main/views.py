import random
import time

from django.contrib import auth
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
# import 其他py檔的Functions or Class以在此py檔中呼叫
from main.models import User, Img, Comment, Classification, UserProfile
# from .otherFunctions.visionAPI import getLabel
from .otherFunctions.score_mobilenet_input import assessPicture
from django import db


# Create your views here.
def main(request):
    '''imgs = Img.objects.all()
    for item in imgs:
        item.like = random.randint(0,49)
        item.save()
    img = Img.objects.get(id__exact='201912172259008379')
    print(img.cmpScore)
    img.cmpScore = 9.7
    img.like = 52
    img.save()'''

    for item in Classification.objects.all():
        if not item.imgs.exists():
            print(item.name,"been delete")
            item.delete()
    # 判斷是否有使用者登入，若登入取得使用者資訊
    if request.user.is_authenticated:
        username = request.user.username
        loginUser = User.objects.get(username=username)

    randCmpScore = random.randint(5, 9)

    # 若有使用者上傳照片
    if request.method == 'POST':
        # 以當前日期時間加上一二位數亂數作為照片id
        imgID = time.strftime('%Y%m%d%H%M%S') + str(random.randint(1, 9999))
        # 取得上傳照片時的照片描述
        description = request.POST.get('description', '')
        # 取得所有照片資訊後儲存照片
        img = Img(id=imgID, image=request.FILES.get('img'), author=loginUser, cmpScore=randCmpScore, like=0,
                  description=description)
        img.save()
        img.cmpScore = assessPicture(str(img.image))  # 此處會呼叫另外一個py檔中之function，以進行評分的動作
        # img.label = getLabel(str(img.image))  # 此處會呼叫另外一個py檔中之function，以取得此圖像之分類label的動作
        img.save()

        # for label in img.label:  # 此for迴圈為檢查此圖片之label是否已存在在database之中若無則在classification Entity中
        #                          # 創建新的label tuple
        #     if not Classification.objects.filter(name=label).exists():
        #         print("new class create")
        #         tagClass = Classification(name=label)
        #         tagClass.save()
        #     else:
        #         tagClass = Classification.objects.filter(name=label)[0]
        #     img.tagClass.add(tagClass)  # 建立Classification Object 與 Img Object 間的relation
        # attrubute設定完成
        # 上傳照片後跳轉至照片資訊頁
        db.connections.close_all()
        return HttpResponseRedirect("/blog/" + img.author.username + "/" + img.id)

    # 取得評分排名list和按讚排名list
    imgListOrderByCmpScore = Img.objects.order_by("-cmpScore")
    imgListOrderByLike = Img.objects.order_by("-like")

    classList = []
    userList = []
    all_user = User.objects.all()
    all_class = Classification.objects.all()
    for item in all_user:
        userList.append(item.username)
    for item in all_class:
        classList.append(item.name)
    context = {
        'imgListOrderByCmpScore': imgListOrderByCmpScore,
        'imgListOrderByLike': imgListOrderByLike,
        'classList': classList,
        'userList': userList,
    }

    return render(request, 'main/index.html', context)


def rank(request):
    # keyword = request.GET.get('keyword', '')
    startImgNum = "0"

    classList = []
    userList = []
    all_user = User.objects.all()
    all_class = Classification.objects.all()
    for item in all_user:
        userList.append(item.username)
    for item in all_class:
        classList.append(item.name)

    context = {
        "scoreType": "computer",
        "sortType": "high",
        "startImgNum": startImgNum,
        'classList': classList,
        'userList': userList
    }

    return render(request, 'rank/rank.html', context)


def ajax_addImg(request):
    sortType = request.GET.get('sortType', '')
    print("sortType: " + sortType)
    scoreType = request.GET.get('scoreType', '')
    print("scoreType: " + scoreType)
    startImgNum = request.GET.get('startImgNum', '')
    startImgNum = int(startImgNum)
    print(startImgNum)

    if startImgNum <= Img.objects.count():
        endImgNum = startImgNum + 12
    else:
        endImgNum = Img.objects.count()

    if sortType == "high" and scoreType == "computer":
        print("high & computer")
        imgList = Img.objects.order_by("-cmpScore")[startImgNum: endImgNum]
    elif sortType == "high" and scoreType == "like":
        print("high & like")
        imgList = Img.objects.order_by("-like")[startImgNum: endImgNum]
    elif sortType == "low" and scoreType == "computer":
        print("low & computer")
        imgList = Img.objects.order_by("cmpScore")[startImgNum: endImgNum]
    else:
        print("low & like")
        imgList = Img.objects.order_by("like")[startImgNum: endImgNum]

    print(imgList)

    context = {
        "sortType": sortType,
        "scoreType": scoreType,
        "startImgNum": startImgNum,
        "imgList": imgList
    }

    return render('rank/result.html', context)


def blog(request, user):
    # 取得使用者
    user = User.objects.get(username=user)
    # 獲得該使用者的所有照片
    userImgList = user.imgs.all()
    history = user.userprofile.historyImgs.order_by('-cmpScore')

    classList = []
    userList = []
    all_user = User.objects.all()
    all_class = Classification.objects.all()
    for item in all_user:
        userList.append(item.username)
    for item in all_class:
        classList.append(item.name)

    context = {
        'user': user,
        'userImgList': userImgList,
        'history': history,
        'classList': classList,
        'userList': userList
    }

    if request.method == 'POST':
        name = request.POST.get('name', '')
        if name != '':
            print("name: " + name)
            user.userprofile.name = name
        biography = request.POST.get('biography', '')
        if biography != '':
            print("biography: " + biography)
            user.userprofile.biography = biography
        newPassword = request.POST.get('newPassword', '')
        if newPassword != '':
            print("newPassword: " + newPassword)
            user.set_password(newPassword)
        user.userprofile.save()
        user.save()



    return render(request, 'blog/blog.html', context)


def ajax_changeProPic(request):

    print("ajax_changeProPic called")

    username = request.POST.get('username')
    print("username: " + username)
    user = User.objects.get(username=username)
    # request.FILES.get('proPic')
    proPic = request.FILES.get('proPic', '')
    print(type(proPic))
    if proPic != '':
        userprofile = user.userprofile
        userprofile.proPicture = proPic
        userprofile.save()
        print(userprofile.proPicture.url)

    return HttpResponseRedirect('/blog/' + username)


def ajax_confirmPwd(request):

    username = request.GET.get('username')
    user = User.objects.get(username=username)
    oldPwd = request.GET.get('oldPwd')
    newPwd = request.GET.get('newPwd')
    confirmPwd = request.GET.get('confirmPwd')

    message = "success"
    if oldPwd == "" or newPwd == "" or confirmPwd == "":
        message = "* make sure your input"
    if oldPwd == newPwd:
        message = "* make sure new password different"
    if newPwd != confirmPwd:
        message = "* make sure both passwords match"
    if not user.check_password(oldPwd):
        message = "* old password incorrect"

    data = {
        "message": message
    }

    print("password error message: " + message)

    return JsonResponse(data)


def imgDetail(request, user, imgID):
    img = Img.objects.get(id=imgID)
    commentList = img.comments.all()
    # blogUser = User.objects.get(username=user)

    if request.user.is_authenticated:
        username = request.user.username
        loginUser = User.objects.get(username=username)
        isLike = loginUser.likeimgs.filter(id=img.id).exists()
        print("add history img")
        request.user.userprofile.historyImgs.add(img)

    else:
        isLike = False

    imgListOrderByCmpScore = Img.objects.order_by("-cmpScore")
    imgListOrderByLike = Img.objects.order_by("-like")

    classList = []
    userList = []
    all_user = User.objects.all()
    all_class = Classification.objects.all()
    for item in all_user:
        userList.append(item.username)
    for item in all_class:
        classList.append(item.name)

    context = {
        'currentImg': img,
        'commentList': commentList,
        'isLike': isLike,
        'imgListOrderByCmpScore': imgListOrderByCmpScore,
        'imgListOrderByLike': imgListOrderByLike,
        'classList': classList,
        'userList': userList
    }

    return render(request, 'blog/imgDetail.html', context)


def info(request):
    return render(request, 'main/info.html')


def tech(request):
    return render(request, 'main/tech.html')


def login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            request.session['username'] = username
            auth.login(request, user)
            return HttpResponseRedirect('/main/')
        else:
            message = "* account error"
            return render(request, 'auth/login.html', locals())

    return render(request, 'auth/login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/main/')


def signUp(request):
    if request.method == 'POST':
        name = request.POST['name']
        account = request.POST['account']
        password = request.POST['password']
        checkPassword = request.POST['checkPassword']
        if password == checkPassword:
            user = User.objects.create_user(username=account, password=password)
            user.save()
            userprofile = UserProfile.objects.create(userProfile=user, name=name, proPicture='')
            userprofile.save()
            return HttpResponseRedirect('/login/')
        else:
            return HttpResponseRedirect('/signUp/')

    return render(request, 'auth/signUp.html')


def ajax_like(request):
    username = request.GET['username']
    imgID = request.GET['imgID']
    user = User.objects.get(username=username)
    img = Img.objects.get(id=imgID)
    isLike = False

    if img.userLike.filter(username=username).exists():
        img.userLike.remove(user)
        likeScore = img.like
        img.like = likeScore - 1
    else:
        img.userLike.add(user)
        likeScore = img.like
        img.like = likeScore + 1
        isLike = True

    img.save()

    data = {
        'like-score': img.like,
        'isLike': isLike
    }

    return JsonResponse(data)


def ajax_comment(request):
    username = request.GET['username']
    imgID = request.GET['imgID']
    content = request.GET['content']
    user = User.objects.get(username=username)
    currentImg = Img.objects.get(id=imgID)
    commentID = time.strftime('%Y%m%d%H%M%S') + username
    comment = Comment(id=commentID, author=user, img=currentImg, content=content)
    comment.save()

    data = {
        'author': username,
        'content': content
    }

    return JsonResponse(data)


def ajax_commentUpdate(request):
    imgID = request.GET.get('imgID')
    currentImg = Img.objects.get(id=imgID)
    commentListHtml = ""
    for item in currentImg.comments.all():
        commentListHtml = commentListHtml + '<div class="comment-list"><div class="comment-author">' + item.author.username + \
                          '</div>&ensp;<div class="comment-content">' + item.content + '</div></div>'
    data = {
        'commentListHtml': commentListHtml
    }

    return JsonResponse(data)

def search(request):
    keyword = request.GET.get('keyword', '')
    print("keyword: " + keyword)
    search_results = None
    result_class = None
    if keyword != '':
        if Classification.objects.filter(name__exact=keyword).exists():
            # print(Classification.objects.filter(name__icontains=keyword))
            result_class = Classification.objects.filter(name__exact=keyword)[0]
            search_results = result_class.imgs.order_by('-cmpScore')
            print(search_results)

    classList = []
    userList = []
    all_user = User.objects.all()
    all_class = Classification.objects.all()
    for item in all_user:
        userList.append(item.username)
    for item in all_class:
        classList.append(item.name)

    context ={
        'search_result': search_results,
        'result_class': result_class,
        'classList': classList,
        'userList': userList
    }

    return render(request, 'search/search.html', context)